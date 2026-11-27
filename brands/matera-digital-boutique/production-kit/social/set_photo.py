"""Create a self-contained photo variant, preserving all editable text and layers."""
import argparse, base64, mimetypes
from pathlib import Path
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('template',type=Path)
parser.add_argument('image',type=Path)
parser.add_argument('output',type=Path)
args=parser.parse_args()
tpl=args.template.read_text('utf-8')
old='EDITORIAL_IMAGE_GOES_HERE.jpg'
if tpl.count(old)!=1:
 raise SystemExit('Select a *--photo.svg template.')
data=args.image.read_bytes()
if data[:3]==b'\xff\xd8\xff': mime='image/jpeg'
elif data[:8]==b'\x89PNG\r\n\x1a\n': mime='image/png'
else: raise SystemExit('Use a JPEG or PNG.')
if len(data)>24*1024**2: raise SystemExit('Image over 24MB; downscale before embedding.')
args.output.write_text(tpl.replace(old,'data:'+mime+';base64,'+base64.b64encode(data).decode('ascii')),encoding='utf-8')
