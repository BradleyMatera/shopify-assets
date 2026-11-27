#!/usr/bin/env python3
"""Build a local-file-safe gallery from actual assets; JSON extras are optional."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

FORMATS = {"png", "jpg", "jpeg", "webp", "avif", "svg", "ico", "gif", "mp4", "webm", "pdf", "zip", "json", "css", "liquid"}
IMAGE_FORMATS = {"png", "jpg", "jpeg", "webp", "avif", "gif", "ico"}
GROUPS = {"brand": "Identity", "identity": "Identity", "logos": "Identity", "palette": "Design tokens", "guidelines": "Guidelines", "hero": "Editorial", "editorial": "Editorial", "backgrounds": "Surfaces", "patterns": "Surfaces", "campaign": "Campaigns", "campaigns": "Campaigns", "collections": "Collection art", "departments": "Collection art", "icons": "Utility icons", "social": "Social", "email": "Email", "motion": "Motion", "shopify": "Shopify", "reference-only": "Reference only", "exports": "Raster exports", "print": "Print", "photography": "Photography", "storefront": "Storefront", "media-motion": "Motion"}
SAFE = re.compile(r"^(?:\.\./)?[A-Za-z0-9_./-]+$")

def dimensions(file: Path, kind: str) -> tuple[int,int] | None:
    try:
        if kind in IMAGE_FORMATS:
            from PIL import Image
            with Image.open(file) as im:
                return im.size
        if kind == "svg":
            doc = ET.parse(file).getroot()
            fields = doc.get("viewBox", "").replace(",", " ").split()
            if len(fields) == 4:
                return round(float(fields[2])), round(float(fields[3]))
        if kind in {"mp4", "webm"}:
            proc = subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=width,height","-of","csv=s=x:p=0",str(file)], capture_output=True,text=True,timeout=8,check=True)
            w,h=proc.stdout.splitlines()[0].split("x")
            return int(w),int(h)
    except (ImportError, OSError, ET.ParseError, ValueError, IndexError, subprocess.SubprocessError):
        return None
    return None

def sha256(file: Path) -> str:
    h = hashlib.sha256()
    with file.open("rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""):
            h.update(c)
    return h.hexdigest()

def relative(file: Path, out: Path) -> str:
    path=Path(os.path.relpath(file,out)).as_posix()
    if not SAFE.fullmatch(path) or ".." in path.removeprefix("../").split("/"):
        raise ValueError(f"Gallery requires local, simple path names directly inside/beside integration: {path}")
    return path

def lexical(file: Path, root: Path) -> str:
    return file.relative_to(root).as_posix()

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("assets_root",type=Path,help="Actual asset tree to scan (not the integration directory)")
    parser.add_argument("--out",type=Path,default=Path(__file__).resolve().parent,help="Directory containing index.html")
    parser.add_argument("--metadata",type=Path,help="JSON object keyed by asset path relative to assets_root; accepts title, family, status, tone, poster")
    parser.add_argument("--json",type=Path,help="Optional second manifest output")
    parser.add_argument("--include",nargs="*",help="Optional top-level folders to include when scanning a full package")
    args=parser.parse_args()
    root,out=args.assets_root.resolve(),args.out.resolve()
    if not root.is_dir() or not out.is_dir() or root==out:
        parser.error("Supply a distinct existing assets directory inside or beside the gallery location.")
    meta=json.loads(args.metadata.read_text(encoding="utf-8")) if args.metadata else {}
    if not isinstance(meta,dict) or any(not isinstance(v,dict) for v in meta.values()):
        parser.error("--metadata must be an object keyed by relative asset filename, with object values.")
    rows=[]
    for file in sorted(root.rglob("*")):
        if file.is_symlink() or not file.is_file() or out in file.parents:
            continue
        src=lexical(file,root)
        if any(p.startswith(".") for p in file.relative_to(root).parts) or (args.include and file.relative_to(root).parts[0] not in args.include):
            continue
        kind=file.suffix.lower().lstrip(".")
        if kind not in FORMATS:
            continue
        custom=meta.get(src,{})
        family=next((GROUPS[p.lower()] for p in file.relative_to(root).parts[:-1] if p.lower() in GROUPS),"Media assets")
        title=re.sub(r"\s+"," ",re.sub(r"[-_]+"," ",file.stem)).strip().title()
        info=dimensions(file,kind)
        record=dict(path=relative(file,out),title=custom.get("title",title), family=custom.get("family",family),format=kind,bytes=file.stat().st_size,sha256=sha256(file),status=custom.get("status","Reference only" if family=="Reference only" else "Candidate"))
        if not all(isinstance(record[k],str) for k in ["title","family","status"]):
            parser.error(f"Non-text metadata for {src}")
        if info and all(n>0 for n in info):
            record.update(width=info[0],height=info[1])
        if custom.get("tone") in {"light","dark"}:
            record["tone"]=custom["tone"]
        elif any(k in file.stem.lower().split("-") for k in ("ivory","reverse","offwhite")) or ("identity" in file.relative_to(root).parts and any(k in file.stem.lower().split("-") for k in ("dark","white"))):
            record["tone"]="light"
        if "poster" in custom:
            candidate=(root/custom["poster"]).resolve()
            if root not in candidate.parents or not candidate.is_file() or candidate.suffix.lower().lstrip(".") not in IMAGE_FORMATS-{"gif"}:
                parser.error(f"Invalid still poster for {src}")
            record["poster"]=relative(candidate,out)
        rows.append(record)
    if not rows:
        parser.error("No supported files found, no manifest written.")
    unknown=set(meta)-{lexical(file,root) for file in root.rglob("*") if file.is_file()}
    if unknown:
        parser.error(f"Metadata references missing assets: {', '.join(sorted(unknown))}")
    rows.sort(key=lambda r:(r["family"].casefold(),r["title"].casefold(),r["path"]))
    document=dict(schema=1,assets=rows)
    txt=json.dumps(document,ensure_ascii=True,indent=2)
    (out/"gallery-manifest.js").write_text("window.MDB_GALLERY = "+txt+";\n",encoding="utf-8")
    if args.json:
        args.json.write_text(txt+"\n",encoding="utf-8")
    print(f"Manifest verified: {len(rows)} real files in {len({r['family'] for r in rows})} families.")
if __name__ == "__main__":
    main()
