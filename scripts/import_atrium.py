"""Import the actual generated image from Shopify's transcoding CDN."""
import hashlib, io, json, urllib.request
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]
url='https://cdn.shopify.com/s/files/1/0855/4492/7460/files/rma-atrium-hero-master.png?v=1793567830'
p=root/'assets/masters/atrium-evening.png'
p.parent.mkdir(parents=True,exist_ok=True)
if not p.exists():
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'RealMallAssetProduction/1.0','Accept':'image/png'}),timeout=90) as response:
        data=response.read(25000000)
    with Image.open(io.BytesIO(data)) as image:
        if image.size!=(1672,941):
            raise RuntimeError(f'Unexpected source dimensions: {image.size}')
        image.convert('RGB').save(p,optimize=True)
    (root/'production').mkdir(exist_ok=True)
    (root/'production/atrium-transport.json').write_text(json.dumps({'source_url':url,'cdn_sha256':hashlib.sha256(data).hexdigest(),'saved_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'note':'Shopify can transcode image bytes. Dimensions verified; actual stored file has its own checksum.'},indent=2)+'\n')
print(f'Imported actual image: {p}, {p.stat().st_size} bytes')
