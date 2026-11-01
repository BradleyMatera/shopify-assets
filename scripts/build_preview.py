"""Create a browsable library, Shopify-ready flat exports and truthful handoff."""
from pathlib import Path
import html,json,shutil
R=Path(__file__).resolve().parents[1]; A=R/'assets'; P=R/'production'
manifest=json.loads((P/'asset-manifest.json').read_text())
collections=json.loads((P/'collections.json').read_text())['departments']
files=manifest['files']; groups=manifest['groups']; store='https://realmallofamerica.myshopify.com'
T=R/'theme'/'assets';T.mkdir(parents=True,exist_ok=True)
def copy(src,name):
    p=R/src
    if p.exists():shutil.copyfile(p,T/name)
copy('assets/hero/atrium-desktop-1600.webp','rma-hero-desktop-1600.webp')
copy('assets/hero/atrium-mobile-648.webp','rma-hero-mobile-648.webp')
copy('assets/brand/wordmark-horizontal-ivory.png','rma-wordmark-ivory.png')
copy('assets/brand/wordmark-horizontal-ink.png','rma-wordmark-ink.png')
copy('assets/brand/favicon.ico','rma-favicon.ico')
copy('assets/motion/atrium-desktop-1280x720.mp4','rma-atrium-loop.mp4')
for c in collections:copy(f"assets/departments/{c['handle']}/square-640.webp",f"rma-dept-{c['handle']}-640.webp")
for p in (A/'icons').glob('*-96.png'):shutil.copyfile(p,T/('rma-icon-'+p.name.replace('-96','')))

# Curated gallery shows representative assets, while the inventory exposes every variant.
selected=[]
for f in files:
    p=f['path'];g=f['group']
    if g=='icons' and not p.endswith('-bronze-96.png'):continue
    if g=='hero' and not (p.endswith('-1600.webp') or p.endswith('-648.webp')):continue
    if g=='departments' and not p.endswith('square-640.webp'):continue
    if g in ('backgrounds','campaigns') and not p.endswith('.webp'):continue
    if g=='motion' and not p.endswith('.mp4'):continue
    if p.endswith('.ico'):continue
    if g=='brand' and 'favicon-' in p:continue
    selected.append(f)
css='''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#10171c;color:#f6f2e9;font:16px/1.6 Arial,sans-serif}a{color:inherit}button,input{font:inherit}button,a,input{outline-offset:5px}:focus-visible{outline:3px solid #e4c591}header{display:flex;align-items:center;justify-content:space-between;gap:25px;padding:24px max(24px,5vw);border-bottom:1px solid #394147}header img{width:235px;height:auto}header a{text-decoration:none;font-size:14px}.hero{padding:85px max(24px,5vw) 70px;background:linear-gradient(90deg,#10171cfa,#10171c88),url(assets/hero/atrium-desktop-1600.webp) center/cover}.eyebrow{text-transform:uppercase;letter-spacing:.22em;font-size:12px;color:#d9bd8f}h1{font:clamp(44px,6vw,84px)/1.02 Georgia,serif;letter-spacing:-.045em;max-width:920px;margin:20px 0}h2{font:42px/1.1 Georgia,serif;letter-spacing:-.025em}p{max-width:760px}.hero p{color:#d8dedf}.actions{display:flex;gap:15px;flex-wrap:wrap;margin-top:30px}.actions a{display:inline-block;padding:13px 22px;text-decoration:none;border:1px solid #b89a68;border-radius:2px}.actions .primary{background:#f6f2e9;color:#11181d}.controls{position:sticky;top:0;z-index:2;background:#10171cf7;backdrop-filter:blur(12px);padding:20px max(24px,5vw);border-block:1px solid #394147}.filters{display:flex;flex-wrap:wrap;gap:8px}.filters button{border:1px solid #657077;background:transparent;color:#fff;padding:8px 13px;border-radius:2px;cursor:pointer;min-height:44px}.filters button[aria-pressed=true]{background:#e3cdab;color:#11181d;border-color:#e3cdab}input{width:100%;max-width:540px;margin-top:14px;background:#192329;color:#fff;border:1px solid #7e898f;padding:12px 16px;border-radius:2px}.gallery{padding:38px max(24px,5vw);display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:26px}.card{min-width:0;border:1px solid #3b444a;background:#151f25;overflow:hidden}.media{height:255px;background:#263238;display:grid;place-items:center}.media img{width:100%;height:100%;object-fit:contain}.media video{width:100%;height:100%;object-fit:contain}.card.icons .media{height:150px}.card.icons .media img{width:64px;height:64px}.card.brand .media{padding:28px;background:#576269}.card h3{font:18px/1.35 Arial,sans-serif;margin:0 0 8px;overflow-wrap:anywhere}.card .info{padding:20px}.card small{color:#b3bfc3}.card a{display:inline-block;margin-top:12px;min-height:44px;color:#e7cfaa}.inventory{padding:45px max(24px,5vw);background:#f3eee5;color:#11181d}.inventory summary{cursor:pointer;font:30px/1.2 Georgia,serif}.file-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:25px}.file-list a{overflow-wrap:anywhere;font:13px/1.5 monospace}footer{padding:40px max(24px,5vw);color:#b2bdc2;font-size:14px}footer a{color:#ead1a4}[hidden]{display:none!important}@media(max-width:1000px){.gallery{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:600px){header{padding:19px 20px}header img{width:180px}header a{font-size:12px}.hero{padding:55px 22px}.gallery{grid-template-columns:1fr;padding:24px 20px}.controls{position:static;padding:20px}.filters button{font-size:13px}.file-list{grid-template-columns:1fr}.media{height:280px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{animation:none!important;transition:none!important}}'''
buttons='<button aria-pressed="true" data-filter="all">All assets</button>'+''.join(f'<button aria-pressed="false" data-filter="{html.escape(g)}">{html.escape(g.title())}</button>' for g in groups)
cards=[]
for f in selected:
    path=html.escape(f['path']);name=html.escape(Path(f['path']).name);group=html.escape(f['group'])
    if path.endswith('.mp4'):media=f'<video controls muted playsinline loop preload="none" poster="assets/motion/atrium-poster.jpg"><source src="{path}" type="video/mp4"></video>'
    else:media=f'<img src="{path}" alt="{name.replace("-"," ")}" loading="lazy" width="{f.get("width",640)}" height="{f.get("height",480)}">'
    size=f"{f.get('width','')} × {f.get('height','')} px" if 'width' in f else 'Silent, six-second still-image motion'
    cards.append(f'<article class="card {group}" data-group="{group}" data-name="{name}"><div class="media">{media}</div><div class="info"><h3>{name}</h3><small>{size} · {round(f["bytes"]/1024)} KB</small><br><a href="{path}" download>Open / save asset →</a></div></article>')
links=''.join(f'<a href="{html.escape(f["path"])}" download>{html.escape(f["path"])}</a>' for f in files)
js="""const filters=document.querySelectorAll('[data-filter]'),search=document.querySelector('#asset-search');let group='all';function apply(){const q=search.value.toLowerCase();document.querySelectorAll('.card').forEach(c=>{c.hidden=!((group==='all'||c.dataset.group===group)&&c.dataset.name.toLowerCase().includes(q));});}filters.forEach(b=>b.addEventListener('click',()=>{group=b.dataset.filter;filters.forEach(x=>x.setAttribute('aria-pressed',String(x===b)));apply();}));search.addEventListener('input',apply);"""
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Real Mall — Production Asset Library</title><link rel="icon" href="assets/brand/favicon.ico"><style>{css}</style></head><body><header><img src="assets/brand/wordmark-horizontal-ivory.png" alt="Real Mall of America"><a href="{store}">Open existing store ↗</a></header><main><section class="hero"><div class="eyebrow">Creative production / Asset library</div><h1>Real files.<br>One visual language.</h1><p>{manifest['total_files']} image and motion files, including responsive sizes, color variants and formats. The original source scenes are recorded separately; derivatives are not counted as additional original shoots.</p><div class="actions"><a class="primary" href="preview/storefront.html">View storefront composition</a><a href="#library">Browse the files</a><a href="production/asset-manifest.json">Inspect the inventory</a></div></section><section class="controls" id="library" aria-label="Filter asset library"><div class="filters">{buttons}</div><label for="asset-search" class="eyebrow">Find an asset by filename</label><br><input id="asset-search" type="search" placeholder="Search filenames…"></section><section class="gallery" aria-label="Asset previews">{''.join(cards)}</section><section class="inventory"><details><summary>Every export — {manifest['total_files']} files</summary><div class="file-list">{links}</div></details></section></main><footer>Generated editorial imagery is not product evidence. Motion clips animate stills; they are not live-action footage. The live Shopify theme has not been changed. <a href="production/sources.json">Source provenance</a> · <a href="production/SHA256SUMS.txt">File checksums</a></footer><script>{js}</script></body></html>'''
(R/'index.html').write_text(page)

# A functional HTML composition: search and shopping links lead to the real store.
nav=''.join(f'<a href="{store}/collections/{c["handle"]}">{html.escape(c["title"])}</a>' for c in collections)
depcards=[]
for c in collections:
    path=f'assets/departments/{c["handle"]}/square-640.webp'
    if not (R/path).exists():continue
    depcards.append(f'<a class="rma-department" href="{store}/collections/{c["handle"]}"><div class="rma-department__image"><img src="../{path}" width="640" height="640" loading="lazy" alt=""></div><div class="rma-department__label"><span>{html.escape(c["title"])}</span><span aria-hidden="true">→</span></div></a>')
extra='''body{margin:0;background:#11181d;color:#f6f2e9;font-family:Arial,sans-serif}.preview-notice{padding:9px 24px;text-align:center;background:#ead7b8;color:#192128;font-size:12px}.store-header{max-width:1600px;margin:auto;padding:26px 5vw;display:flex;align-items:center;gap:45px}.store-header img{width:235px;height:auto}.store-search{flex:1;display:flex;max-width:720px}.store-search input{width:100%;min-width:0;padding:15px;border:1px solid #718087;background:#f6f2e9;color:#11181d;font:15px Arial}.store-search button{padding:0 20px;background:#b89a68;border:1px solid #b89a68;color:#11181d;font:14px Arial}.cart-link{color:#f6f2e9;white-space:nowrap}.store-nav{display:flex;gap:27px;overflow:auto;padding:17px 5vw;border-block:1px solid #374248;white-space:nowrap}.store-nav a{font-size:13px;text-decoration:none;color:#e2e7e6}.store-footer{padding:55px 6vw;border-top:1px solid #374248;color:#b2bec3;line-height:1.65}.store-footer a{color:#e4c99f}.closing{padding:70px 6vw;background:#f6f2e9;color:#11181d;text-align:center}.closing h2{font:clamp(36px,4vw,58px)/1.1 Georgia,serif;margin:0 0 25px}.closing a{display:inline-block;background:#11181d;color:#f6f2e9;text-decoration:none;padding:15px 25px;border-radius:2px}@media(max-width:750px){.store-header{padding:20px;gap:20px;flex-wrap:wrap}.store-header img{width:200px}.store-search{order:3;flex-basis:100%;max-width:100%}.cart-link{margin-left:auto}.store-nav{padding:15px 20px;gap:22px}}'''
storepage=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Real Mall — Storefront Composition</title><link rel="icon" href="../assets/brand/favicon.ico"><link rel="stylesheet" href="../theme/assets/rma-editorial.css"><style>{extra}</style></head><body><div class="preview-notice">Design preview · Shopping links open the existing store · No checkout is hosted here</div><header class="store-header"><a href="{store}"><img src="../assets/brand/wordmark-horizontal-ivory.png" alt="Real Mall of America"></a><form class="store-search" action="{store}/search" method="get"><input name="q" type="search" aria-label="Search products" placeholder="Search products, brands, or categories"><button type="submit">Search</button></form><a class="cart-link" href="{store}/cart">Your bag</a></header><nav class="store-nav" aria-label="Shopping departments">{nav}</nav><main><section class="rma rma-hero" aria-labelledby="hero-heading"><picture class="rma-hero__media"><source media="(max-width:749px)" srcset="../assets/hero/atrium-mobile-648.webp"><img src="../assets/hero/atrium-desktop-1600.webp" width="1600" height="900" alt="" fetchpriority="high"></picture><div class="rma-hero__content"><p class="rma-kicker">Discover your next favorite</p><h1 id="hero-heading">A world of finds.<br>One destination.</h1><p class="rma-hero__description">Explore style, home, travel and the everyday details that make life yours.</p><a href="#departments" class="rma-button">Explore the departments <span aria-hidden="true">→</span></a></div><button class="rma-motion-toggle" type="button" data-rma-motion="../assets/motion/atrium-desktop-1280x720.mp4" aria-pressed="false">Play motion</button></section><section class="rma rma-departments" id="departments"><div class="rma-departments__inner"><p class="rma-kicker">Find your direction</p><h2>Explore the departments.</h2><div class="rma-department-grid">{''.join(depcards)}</div></div></section><section class="closing"><h2>Something new to discover.</h2><a href="{store}/collections/new-arrivals">Explore new arrivals →</a></section></main><footer class="store-footer">Real Mall of America · Creative storefront composition for Matera Digital.<br>Editorial scenes are AI-generated; supplier product photographs and live listings remain authoritative.<br><a href="../index.html">Return to the asset library</a> · <a href="{store}">Visit the current store</a></footer><script src="../theme/assets/rma-motion.js" defer></script></body></html>'''
(R/'preview').mkdir(exist_ok=True);(R/'preview'/'storefront.html').write_text(storepage)

# Exact inventory, not a completion promise.
rows='\n'.join(f'| {g} | {n} |' for g,n in groups.items())
failed=manifest.get('generation_failures',[])
warning=('\n## Unfinished image generations\n'+ '\n'.join(f'- {x["id"]}: {x["error"]}' for x in failed)) if failed else ''
readme=f'''# Real Mall of America — Actual Asset Library

![Real Mall visual identity](assets/brand/wordmark-horizontal-ivory.png)

**This repository contains {manifest['total_files']} actual media files, not only briefs or mockup screenshots.** File counts include color, responsive-size and format variants. They are not claims of {manifest['total_files']} unique photographs.

![Generated architectural campaign](assets/hero/atrium-desktop-1600.webp)

## Browse

Open `index.html` for the visual asset library or `preview/storefront.html` for the storefront composition. Both use relative local files. Shopping links in the preview lead to the existing Shopify store; no fake checkout is implemented.

## Produced files

| Folder | Files |
| --- | ---: |
{rows}

Department source coverage: **{manifest['department_sources']} of 9**. Source photography registry: `production/sources.json`. Exact dimensions, bytes and hashes: `production/asset-manifest.json` and `production/SHA256SUMS.txt`.

## What is included

- Raster identity system: transparent wordmarks, monograms, favicon variants and a social avatar.
- 36 original interface symbols, each in three tones and two raster sizes; **216 icon exports, not 216 different symbols**.
- Six atmospheric material backgrounds, supplied as PNG and WebP.
- Separately generated campaign masters and responsive JPEG/WebP crops where generation succeeded.
- Rendered campaign, social and email artwork with editable copy in JSON.
- Actual MP4/WebM silent camera-motion loops with still posters. **These animate still images; they are not live-action or independently generated cinematic footage.**
- Optional Shopify sections, scoped CSS and motion controls, with uniquely named flat media exports under `theme/assets/`.

## Scope and provenance

The native architectural campaign was generated in this conversation and transferred through the merchant's Shopify CDN. Additional independent scenes use the documented free Pollinations Classic generator; original provider-marked masters are preserved, along with prompts and provenance. Responsive crops are derivatives. All imagery is editorial atmosphere, not a representation of a stocked SKU or proof of premises ownership. No relationship with the physical Mall of America is asserted.

No font files are redistributed. Existing supplier product photographs must remain authoritative. No fabricated reviews, discounts, shipping promises, supplier badges or guarantees are included.

**The live Shopify theme has not been changed.** Install the optional sections in an unpublished theme, check actual image crops and commerce behavior, and complete storefront QA before publishing. This asset library is not a full Shopify theme ZIP and is not a compliance certification.
{warning}

## Rebuild

`python -m pip install Pillow numpy cairosvg` then `python scripts/import_atrium.py`, `python scripts/produce_photography.py`, `python scripts/build_library.py`, and `python scripts/build_preview.py`. Install FFmpeg for video encoding. Existing scene masters are reused; only missing sources are requested. No API keys are required and no paid generation calls are made.
'''
(R/'README.md').write_text(readme)
(R/'docs'/'ASSET-MANIFEST.md').write_text('# Actual produced inventory\n\n'+f'{manifest["total_files"]} media exports; {manifest["department_sources"]}/9 department masters.\n\n| Group | Files |\n| --- | ---: |\n'+rows+'\n\nThe machine-readable registry in `production/asset-manifest.json` enumerates every real file and its checksum. Source and derivative counts are distinct.\n'+warning)
status={'media_files':manifest['total_files'],'department_sources':manifest['department_sources'],'required_departments':9,'source_scenes':manifest['sources'],'generation_failures':failed,'live_shopify_theme_modified':False,'motion':'animated stills, not live-action video','visual_review':'Review individual masters and crops before live merchandising'}
(P/'status.json').write_text(json.dumps(status,indent=2)+'\n')
print(json.dumps(status,indent=2))
