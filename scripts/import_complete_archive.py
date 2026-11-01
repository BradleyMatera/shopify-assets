#!/usr/bin/env python3
"""Import the exact supplied ZIP without modifying the existing asset library.

The staging PNGs are lossless byte containers, not artwork. Nothing in the
archive is executed. Every part and the complete archive are SHA-256 checked.
"""
from __future__ import annotations
import argparse
import concurrent.futures
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import stat
import struct
import subprocess
import tempfile
import time
import urllib.parse
import urllib.request
import zipfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'production/complete-archive-transfer.json'
INVENTORY = ROOT / 'production/complete-library-inventory.json'
REPORT = ROOT / 'production/complete-library-verification.json'


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_sha(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def git_tree(ref: str, folder: str) -> dict[str, str]:
    output = subprocess.check_output(['git', 'ls-tree', '-r', '-z', ref, '--', folder], cwd=ROOT)
    result = {}
    for item in output.split(b'\0'):
        if not item:
            continue
        metadata, path = item.split(b'\t', 1)
        mode, kind, digest = metadata.decode().split()
        if kind == 'blob':
            result[path.decode()] = digest
    return result


def fetch_part(part: dict, directory: Path) -> Path:
    url = urllib.parse.urlparse(part['url'])
    if url.scheme != 'https' or url.hostname != 'cdn.shopify.com':
        raise ValueError('Unexpected transfer host')
    if not url.path.startswith('/s/files/1/0855/4492/7460/files/rma-'):
        raise ValueError('Unexpected transfer path')
    target = directory / f"part-{part['index']:02d}.bin"
    if target.exists() and sha256(target.read_bytes()) == part['sha256']:
        return target
    for attempt in range(4):
        try:
            request = urllib.request.Request(part['url'], headers={
                'Accept': 'image/png', 'User-Agent': 'RealMallAssetImport/1.0'})
            with urllib.request.urlopen(request, timeout=120) as response:
                encoded = response.read(20_000_001)
            if len(encoded) > 20_000_000:
                raise ValueError('Oversized transfer image')
            with Image.open(io.BytesIO(encoded)) as image:
                image.load()
                pixels = image.convert('RGB').tobytes()
            if pixels[:8] != b'RMAZIP01':
                raise ValueError('Transfer header changed')
            length = struct.unpack('>Q', pixels[8:16])[0]
            if length != part['bytes'] or length > 16_777_216:
                raise ValueError('Transfer length changed')
            data = pixels[48:48+length]
            if len(data) != length or sha256(data) != part['sha256']:
                raise ValueError('Transfer SHA-256 mismatch')
            if hashlib.sha256(data).digest() != pixels[16:48]:
                raise ValueError('Embedded checksum mismatch')
            target.write_bytes(data)
            print(f"Verified transfer part {part['index']}: {length} bytes", flush=True)
            return target
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError('Unreachable')


def verify_git(ref: str) -> None:
    inventory = json.loads(INVENTORY.read_text())
    destination = inventory['destination']
    tree = git_tree(ref, destination)
    failures = []
    for entry in inventory['files']:
        path = f"{destination}/{entry['path']}"
        if tree.get(path) != entry['git_blob_sha']:
            failures.append(path)
    if failures:
        raise RuntimeError(f'{len(failures)} missing or changed Git objects: {failures[:10]}')
    preserved = inventory.get('preserved_existing_assets', {})
    actual_existing = git_tree(ref, 'assets')
    changed = [path for path, digest in preserved.items() if actual_existing.get(path) != digest]
    if changed:
        raise RuntimeError(f'Existing assets were changed or removed: {changed[:10]}')
    print(f"GIT_VERIFIED: {len(inventory['files'])} package files match exact original bytes at {ref}; {len(preserved)} prior assets preserved", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', type=Path, help='Use the original local ZIP instead of transfer parts')
    parser.add_argument('--verify-ref', help='Verify every Git blob against the package inventory')
    args = parser.parse_args()
    if args.verify_ref:
        verify_git(args.verify_ref)
        return
    config = json.loads(CONFIG.read_text())
    work = Path(os.environ.get('RUNNER_TEMP', tempfile.gettempdir())) / 'rma-complete-archive'
    work.mkdir(parents=True, exist_ok=True)
    archive = work / config['archive_filename']
    if args.archive:
        archive = args.archive.resolve()
    elif not archive.exists() or sha256(archive.read_bytes()) != config['archive_sha256']:
        parts = sorted(config['parts'], key=lambda x: x['index'])
        if [p['index'] for p in parts] != list(range(1, len(parts)+1)):
            raise ValueError('Missing or duplicated transfer indexes')
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(lambda p: fetch_part(p, work), parts))
        with archive.open('wb') as output:
            for path in results:
                output.write(path.read_bytes())
    data = archive.read_bytes()
    if len(data) != config['archive_bytes'] or sha256(data) != config['archive_sha256']:
        raise ValueError('The reconstructed ZIP is not the original ZIP')
    print(f"ORIGINAL_ZIP_VERIFIED: {config['archive_sha256']}", flush=True)
    preserved = git_tree('HEAD', 'assets')
    destination = ROOT / config['destination']
    entries = []
    expected_paths = set()
    with zipfile.ZipFile(archive) as z:
        files = [x for x in z.infolist() if not x.is_dir()]
        if len(files) != config['file_count']:
            raise ValueError('Wrong ZIP file count')
        if sum(x.file_size for x in files) != config['uncompressed_bytes']:
            raise ValueError('Wrong extracted byte count')
        for item in files:
            if not item.filename.startswith(config['archive_prefix']):
                raise ValueError('Unexpected archive root')
            relative = item.filename[len(config['archive_prefix']):]
            path = PurePosixPath(relative)
            if path.is_absolute() or '..' in path.parts or '.git' in path.parts or '\\' in relative:
                raise ValueError('Unsafe archive path')
            if stat.S_ISLNK(item.external_attr >> 16) or item.file_size > 5_000_000:
                raise ValueError('Unexpected archive entry')
            if relative in expected_paths:
                raise ValueError('Duplicated ZIP path')
            expected_paths.add(relative)
            original = z.read(item)
            target = destination / relative
            if target.exists() and target.read_bytes() != original:
                raise ValueError(f'Refusing to replace a different existing file: {relative}')
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(original)
            actual = target.read_bytes()
            if actual != original:
                raise ValueError(f'Write verification failed: {relative}')
            entries.append({'path': relative, 'bytes': len(actual), 'sha256': sha256(actual), 'git_blob_sha': git_sha(actual)})
    actual_paths = {p.relative_to(destination).as_posix() for p in destination.rglob('*') if p.is_file()}
    if actual_paths != expected_paths:
        raise ValueError('Extracted tree does not exactly match the package')
    registry = json.loads((destination / 'asset-manifest.json').read_text())
    variants = [variant for asset in registry['assets'] for variant in asset['variants']]
    if len(variants) != config['registered_media_files']:
        raise ValueError('Wrong media registry count')
    for variant in variants:
        p = destination / variant['path']
        if not p.is_file() or p.stat().st_size != variant['bytes']:
            raise ValueError(f"Missing or wrong-size registered media: {variant['path']}")
    checksum_count = 0
    for line in (destination / 'checksums.sha256').read_text().splitlines():
        if not line.strip():
            continue
        digest, name = line.split('  ', 1)
        if name not in expected_paths or sha256((destination / name).read_bytes()) != digest:
            raise ValueError(f'Original package checksum failed: {name}')
        checksum_count += 1
    inventory = {'archive_sha256': config['archive_sha256'], 'destination': config['destination'],
                 'file_count': len(entries), 'preserved_existing_assets': preserved, 'files': entries}
    INVENTORY.write_text(json.dumps(inventory, indent=2) + '\n')
    report = {
        'status': 'local-files-verified-awaiting-remote-readback',
        'source_archive': config['archive_filename'], 'source_archive_sha256': config['archive_sha256'],
        'archive_bytes': config['archive_bytes'], 'package_file_count': len(entries),
        'registered_media_exports': len(variants), 'original_checksum_entries_verified': checksum_count,
        'existing_asset_files_preserved': len(preserved), 'destination': config['destination'],
        'formats': registry['formats'], 'missing_files': [], 'corrupt_files': [],
        'scope': 'Every file in the supplied ZIP; this does not certify the unfinished creative-production backlog.',
        'quality_notes': registry['notes']}
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    prefix = ('<!-- complete-library-import -->\n# Complete asset package\n\n'
              '**All 1,323 original ZIP files are available under [`complete-library/`](complete-library/): '
              '1,302 registered media exports plus gallery, manifests, integration examples and supporting files.**\n\n'
              'Open [`complete-library/START-HERE.html`](complete-library/START-HERE.html) after cloning or downloading '
              'to browse the full gallery. The original ZIP is attached to the '
              '[complete-package release](https://github.com/BradleyMatera/shopify-assets/releases/tag/complete-asset-pack-2026-11-01).\n\n'
              'See [`production/complete-library-verification.json`](production/complete-library-verification.json) '
              'for exact-byte verification status. Existing files below remain intact as a separate earlier batch.\n\n'
              '**Quality distinction:** small department crops and their enlarged versions remain labeled; '
              'concepts with unsupported promotional claims stay in `reference-only/`. Motion files animate stills. '
              'This import does not publish a Shopify theme or create new high-resolution photography.\n\n'
              '---\n\n## Earlier standalone library (separate batch)\n\n')
    readme = ROOT / 'README.md'
    previous = readme.read_text()
    if '<!-- complete-library-import -->' not in previous:
        readme.write_text(prefix + previous)
    (ROOT / 'ALL-ASSETS.md').write_text(prefix.split('---')[0])
    landing = ROOT / 'START-HERE.html'
    if not landing.exists():
        landing.write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Complete asset library</title><meta http-equiv="refresh" content="0;url=complete-library/START-HERE.html"><body><a href="complete-library/START-HERE.html">Open the complete asset library</a></body></html>\n')
    checksum_file = work / (config['archive_filename'] + '.sha256')
    checksum_file.write_text(config['archive_sha256'] + '  ' + config['archive_filename'] + '\n')
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a') as output:
            output.write(f'archive={archive}\nchecksum={checksum_file}\n')
    print(f'IMPORT_VERIFIED: {len(entries)} files, {len(variants)} media exports, {checksum_count} original checksums', flush=True)


if __name__ == '__main__':
    main()
