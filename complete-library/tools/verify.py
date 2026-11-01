#!/usr/bin/env python3
"""Verify the extracted pack with Python 3: python tools/verify.py"""
from pathlib import Path
import hashlib, json, sys
root=Path(__file__).resolve().parents[1]
errors=[]; count=0
for line in (root/'checksums.sha256').read_text().splitlines():
    expected,name=line.split('  ',1); path=root/name
    if not path.is_file(): errors.append('Missing: '+name); continue
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    if actual!=expected: errors.append('Changed: '+name)
    count+=1
manifest=json.loads((root/'asset-manifest.json').read_text())
for asset in manifest['assets']:
    for variant in asset['variants']:
        if not (root/variant['path']).is_file():errors.append('Missing registered media: '+variant['path'])
print(f'Checked {count} files; {len(errors)} errors.')
for error in errors: print(error)
sys.exit(bool(errors))
