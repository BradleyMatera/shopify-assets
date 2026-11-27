#!/usr/bin/env python3
from pathlib import Path
import re, json
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET
root=Path(__file__).resolve().parent.parent
PINE='#142B22'; IVORY='#F7F3EA'; RUST='#9C4E38'; APRICOT='#E4AD89'
paper='#EEEADE'; hair='#D5CCB9'
bitmap_files=list(root.glob('*/*.png'))
seen_svg=[]
for p in sorted(root.glob('*/*.svg')):
 svg=ET.parse(p).getroot()
 assert not any(re.fullmatch(r'(text|image|script|foreignObject)',str(el.tag).split('}')[-1]) for el in svg.iter())
 assert 'viewBox' in svg.attrib
 assert not re.search(r'(?i)href\s*=',p.read_text())
 seen_svg.append(str(p.relative_to(root)))
for p in bitmap_files:
 m=re.search(r'(\d+)x(\d+)\.png$',p.name)
 assert m,p
 im=Image.open(p); im.verify()
 im=Image.open(p).convert('RGBA')
 assert im.size==tuple(map(int,m.groups())),p
 bb=im.getbbox(); assert bb,p
 if p.parent.name=='shopify':
  assert 0<bb[0]<bb[2]<im.width and 0<bb[1]<bb[3]<im.height,(p.name,bb,im.size)
  assert im.getpixel((0,0))[-1]==0,p
ico=Image.open(root/'icons/favicon.ico')
assert ico.ico.sizes()=={(16,16),(32,32),(48,48),(64,64)}
tiny_hashes=[]
for dim in (16,32,48,64):
 ref=Image.open(root/f'icons/favicon-{dim}x{dim}.png').convert('RGBA')
 got=ico.ico.getimage((dim,dim)).convert('RGBA')
 assert got.tobytes()==ref.tobytes(),(dim,got.size)
 # Central ink has visible contrast. Keep low-level anti-aliasing and transparent corners legal.
 assert sum(1 for c in ref.getdata() if c[0]>=185 and c[3]>=192)>20,dim
 tiny_hashes.append(dim)
def srgb(c):
 c=c/255
 return c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4
def l(c):
 r,g,b=[srgb(int(c[i:i+2],16)) for i in (1,3,5)]
 return .2126*r+.7152*g+.0722*b
def contrast(a,b):return (max(l(a),l(b))+.05)/(min(l(a),l(b))+.05)
report={'svgCount':len(seen_svg),'pngCount':len(bitmap_files),'iconFrames':tiny_hashes,'contrast':{'pineIvory':round(contrast(PINE,IVORY),2),'rustIvory':round(contrast(RUST,IVORY),2),'apricotPine':round(contrast(APRICOT,PINE),2)},'checks':['All viewBoxes and outlines valid XML, no live fonts, raster images, scripts or external references','PNG decodable, expected dimensions; Shopify marks have transparent clear space and no clipping','ICO contains byte-identical 16/32/48/64 PNG frames at correct sizes']}
(root/'source/qa-results.json').write_text(json.dumps(report,indent=2)+'\n')
# Proof sheet: native size samples, alternate backgrounds, and circle crop check.
sheet=Image.new('RGB',(1272,990),paper);draw=ImageDraw.Draw(sheet)
reg='/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf'
semi='/usr/share/fonts/truetype/open-sans/OpenSans-Semibold.ttf'
ser='/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf'
f=lambda p,s:ImageFont.truetype(p,s)
def rect(b,fill=IVORY):draw.rounded_rectangle(b,radius=10,fill=fill)
def label(s,xy,c=PINE):draw.text(xy,s,font=f(semi,15),fill=c)
def put(p,x,y,sz=None):
 i=Image.open(root/p).convert('RGBA')
 if sz:i=i.resize(sz,Image.Resampling.LANCZOS)
 sheet.paste(i,(x,y),i)
draw.text((36,22),'IDENTITY  /  FORM 01',font=f(semi,18),fill=RUST)
draw.text((35,45),'Matera Digital Boutique',font=f(ser,48),fill=PINE)
draw.text((38,112),'Full system proof: outlined marks, measured colors and production-size checks.',font=f(reg,17),fill=PINE)
for x,style,fill,ink in [(36,'light',IVORY,PINE),(648,'dark',PINE,IVORY)]:
 rect((x,159,x+588,391),fill); label('01   HORIZONTAL  /  '+style.upper(),(x+24,177),ink)
 put(f'shopify/mdb-horizontal-{style}-440x102.png',x+51,241)
 rect((x,409,x+289,703),fill); label('02   STACKED',(x+20,426),ink)
 put(f'shopify/mdb-stacked-{style}-840x504.png',x+19,485,(250,150))
 rect((x+305,409,x+588,703),fill);label('03   AVATAR CIRCLE CROP',(x+324,426),ink)
 av=Image.open(root/f'social/mdb-avatar-{("pine" if style=="light" else "ivory")}-180x180.png').convert('RGB')
 mask=Image.new("L",(180,180));ImageDraw.Draw(mask).ellipse((1,1,178,178),fill=255)
 sheet.paste(av,(x+355,477),mask)
rect((36,722,1236,958))
label('04   PRODUCTION SIZES  /  NO ZOOM',(56,740))
for p,w,x in [('shopify/mdb-horizontal-light-220x51.png',220,56),('shopify/mdb-wordmark-light-180x45.png',180,340)]:
 put(p,x,793);draw.text((x,869),f'{w}px storefront display',font=f(reg,15),fill=PINE)
for i,q in enumerate((16,32,48,64)):
 x=(600,708,816,924)[i]
 put(f'icons/favicon-{q}x{q}.png',x,817-q//2);draw.text((x,869),f'{q}px',font=f(reg,15),fill=PINE)
x=1045
for i,(tag,col) in enumerate([('Pine',PINE),('Ivory',IVORY),('Rust',RUST),('Apricot',APRICOT)]):
 draw.rectangle((x,782+i*30,x+20,802+i*30),fill=col,outline=hair)
 draw.text((x+28,783+i*30),f'{tag}  {col}',font=f(reg,14),fill=PINE)
sheet.save(root/'identity-proof.jpg',quality=94,optimize=True)
print(json.dumps(report))
