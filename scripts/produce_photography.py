"""Produce independently addressable raster campaign masters, not screenshots.
The native generated atrium is imported from the merchant's Shopify CDN.
Department and seasonal scenes use the documented, free public Classic image
endpoint; no paid calls, API keys, or account credentials are required.
Provider-marked originals are preserved. Responsive crops are separate exports.
"""
from __future__ import annotations
import hashlib, io, json, time, urllib.parse, urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MASTERS = ROOT / 'assets' / 'masters'
MASTERS.mkdir(parents=True, exist_ok=True)
PRODUCTION = ROOT / 'production'
PRODUCTION.mkdir(exist_ok=True)
HERO_URL = 'https://cdn.shopify.com/s/files/1/0855/4492/7460/files/rma-atrium-hero-master.png?v=1793567830'
HERO_HASH = 'fe30157a9d8b3d095f569ee5d83dc15c63d3bd108d763ec8bf9beec53a1051e8'
STYLE = ('Single full-frame editorial campaign photograph. Photorealistic premium department-store art direction, tactile material detail, carefully controlled warm daylight, rich charcoal shadows, restrained bronze and ivory palette, sophisticated natural composition. No writing, no lettering, no slogans, no logos, no labels, no collage, no graphic design layout, no website, no interface. Unbranded objects, editorial atmosphere rather than a specific product listing. ')
SCENES = [
 ('fashion-accessories', 'Fashion & Accessories', 'An adult woman in a beautifully tailored camel coat and dark unbranded sunglasses walking beside limestone architecture. A candid editorial moment, natural skin, realistic folds and fabric, medium-distance portrait with head and coat fully framed, late-afternoon side light.'),
 ('home-kitchen', 'Home & Kitchen', 'A serene architectural living and kitchen space with sculptural ivory seating, walnut cabinets, limestone counter, a handmade ceramic bowl and olive branches. Beautiful grazing daylight from a tall side window, warm tactile materials, realistic interior photography, no people.'),
 ('bags-travel', 'Bags & Travel', 'A beautifully made unbranded dark leather weekender and a natural canvas tote on a limestone bench in a quiet modern travel lounge. A coat folded nearby, sophisticated architectural shadows, elegant luggage still life, realistic stitching and handles.'),
 ('beauty-self-care', 'Beauty & Self-Care', 'A translucent amber glass bottle, a plain frosted glass jar, folded ivory linen and a branch of white blossoms on honed stone. Sculptural shadows, extremely realistic glass and liquid reflections, restrained luxury skincare editorial still life. Completely blank containers without labels.'),
 ('pets', 'Pets', 'A relaxed golden retriever sitting beside a soft textured ivory dog bed in an elegant warm contemporary home. Natural window light, realistic fur, kind expression, full head and paws visible, warm candid pet lifestyle campaign, no collar lettering.'),
 ('tech-desk', 'Tech & Desk', 'An unbranded pair of matte black over-ear headphones resting beside a closed thin laptop and a precisely machined keyboard on a walnut desk. Restrained blue screen reflection and warm side light, clean contemporary work studio, premium materials, no RGB clutter or text.'),
 ('outdoors-fitness', 'Outdoors & Fitness', 'A lone adult hiker with an unbranded charcoal backpack looking toward dramatic mountain ridges and a pine valley at golden hour. Wide scenic editorial adventure photography, natural ochre clothing, believable anatomy and terrain, crisp mountain detail, no logos.'),
 ('kids-hobbies', 'Kids & Hobbies', 'A beautifully arranged creative hobby table with unbranded wooden building shapes, colored pencils, a small unfinished paper model and a sketchbook with abstract blank shapes. Warm afternoon sunlight, refined walnut and ivory room, joyful color accents, realistic tactile still life, no characters or copyrighted toys.'),
 ('digital-downloads', 'Digital Downloads', 'A premium creative work desk with an unbranded drawing tablet showing a simple abstract ochre geometric artwork, neatly arranged blank paper sheets, a graphite stylus, and a closed charcoal notebook. Warm light crossing limestone, elegant creative-work editorial photography, no screen text.'),
 ('spring', 'Spring Edit', 'A sculptural clear glass vase with fresh white and pale blush spring blossoms on a limestone pedestal beside airy ivory linen curtains. Luminous soft daylight, botanical editorial still life, quietly luxurious, generous negative space.'),
 ('summer', 'Summer Edit', 'A woven natural-fiber travel tote, folded ivory linen and unbranded sunglasses on a sunlit stone terrace overlooking a calm blue sea. Soft coastal atmosphere, realistic materials, elegant summer lifestyle still life, no people or writing.'),
 ('autumn', 'Autumn Edit', 'A folded ochre wool scarf, a dark ceramic mug, an unbranded leather notebook and a few autumn leaves on warm walnut beside a window. Intimate editorial still life, golden light and deep charcoal shadows, no text.'),
 ('holiday', 'Holiday Edit', 'Beautiful unbranded ivory and charcoal gift boxes tied with restrained bronze satin ribbons, evergreen branches and soft warm lights in the background. Elegant holiday still life on dark stone, editorial luxury rather than glitter, no labels or writing.')
]

def fetch(url: str, attempts: int = 3) -> bytes:
    error = None
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'RealMallAssetProduction/1.0', 'Accept': 'image/*'})
            with urllib.request.urlopen(req, timeout=150) as response:
                data = response.read(25_000_000)
            with Image.open(io.BytesIO(data)) as image:
                image.verify()
            return data
        except Exception as exc:
            error = exc
            if attempt + 1 < attempts:
                time.sleep(60)
    raise RuntimeError(str(error))

records, failures = [], []
hero_path = MASTERS / 'atrium-evening.png'
if not hero_path.exists():
    data = fetch(HERO_URL)
    if hashlib.sha256(data).hexdigest() != HERO_HASH:
        raise RuntimeError('Atrium source checksum does not match the generated original')
    hero_path.write_bytes(data)
records.append({'id': 'atrium-evening', 'path': str(hero_path.relative_to(ROOT)), 'origin': 'Native image generation in this conversation', 'source_url': HERO_URL, 'use': 'Editorial architectural campaign; not a claim of physical premises ownership'})
for index, (slug, title, brief) in enumerate(SCENES):
    path = MASTERS / f'{slug}.jpg'
    prompt = STYLE + brief
    url = 'https://image.pollinations.ai/prompt/' + urllib.parse.quote(prompt, safe='') + '?' + urllib.parse.urlencode({'width': 1024, 'height': 768, 'seed': 2026110100 + index, 'safe': 'true'})
    try:
        if not path.exists():
            print(f'Generating {slug}', flush=True)
            data = fetch(url, attempts=2)
            with Image.open(io.BytesIO(data)) as image:
                if min(image.size) < 480:
                    raise RuntimeError(f'Unexpectedly small generation: {image.size}')
                image.convert('RGB').save(path, quality=96, subsampling=0)
            time.sleep(46)
        with Image.open(path) as image:
            size = list(image.size)
        records.append({'id': slug, 'title': title, 'path': str(path.relative_to(ROOT)), 'origin': 'Pollinations Classic image generation', 'prompt': prompt, 'source_url': url, 'native_size': size, 'use': 'Generated editorial scene, not an actual stocked product photograph', 'provider_mark': 'Preserved in source master'})
    except Exception as exc:
        print(f'FAILED {slug}: {exc}', flush=True)
        failures.append({'id': slug, 'error': str(exc)})
    (PRODUCTION / 'sources.json').write_text(json.dumps({'sources': records, 'failures': failures}, indent=2) + '\n')
(PRODUCTION / 'sources.json').write_text(json.dumps({'sources': records, 'failures': failures}, indent=2) + '\n')
print(json.dumps({'source_files': len(records), 'failures': failures}), flush=True)
if failures:
    raise SystemExit(1)
