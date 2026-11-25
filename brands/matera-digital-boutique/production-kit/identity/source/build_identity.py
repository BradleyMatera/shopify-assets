#!/usr/bin/env python3
"""Original vector monogram, static outlined wordmark and platform exports."""
from pathlib import Path
import argparse, html, json, math, os, shutil, subprocess
from concurrent.futures import ThreadPoolExecutor
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent.parent
PINE='#142B22'; IVORY='#F7F3EA'; RUST='#9C4E38'; APRICOT='#E4AD89'
SERIF='/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf'
SANS='/usr/share/fonts/truetype/open-sans/OpenSans-Semibold.ttf'
MONO='/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf'
SERIF=os.getenv('MDB_SERIF',SERIF)
SANS=os.getenv('MDB_SANS',SANS)
# Authored unconnected ink contour, with counter. Both initials share the right M stem.
MARK='M9 80V20h11L40.5 48.5 61 20h12c20.5 0 33 12.6 33 30.1C106 67.4 93.5 80 73 80H61V36.2L42.5 62h-4.2L20 36.3V80Zm63-50v40h1.6c14.5 0 22.2-8 22.2-19.9C95.8 38.1 88.1 30 73.6 30Z'
# Slightly widened negative space and stems for the 16px icon only.
MARK_TINY='M7 82V18h13l21 29 22-29h10c21 0 34 14 34 32S94 82 73 82H62V39L43 64h-5L19 39v43Zm68-52v40c12-.6 20-8.8 20-20S87 30.6 75 30Z'
TRIM=(9,20,106,80)
KERN={('M','a'):-1.4,('a','t'):-1.0,('t','e'):-1.45,('r','a'):-1.1,('D','i'):-1.75,('i','g'):-.5,('g','i'):-.6,('t','a'):-1.25}

class Face:
 def __init__(self,p):
  self.font=TTFont(p);self.g=self.font.getGlyphSet();self.c=self.font.getBestCmap();self.u=self.font['head'].unitsPerEm
 def outlines(self,s,size,t=0,kern=False):
  scale=size/self.u; x=0; allpaths=[]; box=[]
  for i,ch in enumerate(s):
   if i and kern:x+=KERN.get((s[i-1],ch),0)*(size/57)
   gn=self.c[ord(ch)]
   p=SVGPathPen(self.g,ntos=lambda v: f'{v:.3f}'.rstrip('0').rstrip('.') or '0')
   self.g[gn].draw(TransformPen(p,(scale,0,0,-scale,x,0)))
   b=BoundsPen(self.g);self.g[gn].draw(TransformPen(b,(scale,0,0,-scale,x,0)))
   if b.bounds:box.append(b.bounds)
   if p.getCommands():allpaths.append(p.getCommands())
   x+=self.font['hmtx'][gn][0]*scale+t
  return ' '.join(allpaths), tuple(fn(v[i] for v in box) for i,fn in enumerate((min,min,max,max)))

FS=Face(SERIF); FN=Face(SANS)
main=FS.outlines('Matera Digital',57,-1.05,True)
cap=FN.outlines('BOUTIQUE',18,6.8)
def n(v):return f'{v:.3f}'.rstrip('0').rstrip('.') or '0'
def group(p,x,y,c):
 return f'<path fill="{c}" transform="translate({n(x-p[1][0])} {n(y)})" d="{p[0]}"/>'
def centered(p,x,y,c):return group(p,x-(p[1][2]-p[1][0])/2,y,c)
def make_svg(w,h,title,desc,body):
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="identity-title identity-desc"><title id="identity-title">{html.escape(title)}</title><desc id="identity-desc">{html.escape(desc)}</desc>{body}</svg>\n'
def mark(x,y,w,c,tiny=False):
 d=MARK_TINY if tiny else MARK
 l,top,right,_=(7,18,107,82) if tiny else TRIM
 k=w/(right-l)
 return f'<path fill="{c}" fill-rule="evenodd" transform="translate({n(x-l*k)} {n(y-top*k)}) scale({n(k)})" d="{d}"/>'

assignments=[]
def save(rel,w,h,title,desc,body):
 p=HERE/rel;p.write_text(make_svg(w,h,title,desc,body));return p
def raster(p,rel,w,h):
 assignments.append((p,HERE/rel,w,h))
def pngjob(a):
 src,dest,w,h=a
 subprocess.run(['inkscape',str(src),'--export-type=png',f'--export-filename={dest}',f'--export-width={w}',f'--export-height={h}'],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 im=Image.open(dest); im.load()
 assert im.size==(w,h),(dest,im.size)
 im.save(dest,optimize=True)

STYLE={
 'light':(PINE,RUST),
 'dark':(IVORY,APRICOT),
 'mono-black':('#000000','#000000'),
 'mono-white':('#FFFFFF','#FFFFFF'),
}
for tag,(ink,accent) in STYLE.items():
 label='Matera Digital Boutique'
 detail='Outlined Noto Serif wordmark and Open Sans label with an original linked M and D monogram.'
 body=mark(21,31,92,ink)+group(main,145,70,ink)+group(cap,149,105,accent)
 s=save(f'masters/mdb-horizontal-{tag}.svg',555,128,label,detail,body)
 if tag in ('light','dark'):
  raster(s,f'shopify/mdb-horizontal-{tag}-220x51.png',220,51)
  raster(s,f'shopify/mdb-horizontal-{tag}-440x102.png',440,102)
  raster(s,f'shopify/mdb-horizontal-{tag}-880x203.png',880,203)
 # Wordmark only. Align cap with main left edge; no artificial spaces.
 body=group(main,11,58,ink)+group(cap,14,88,accent)
 s=save(f'masters/mdb-wordmark-{tag}.svg',420,104,label,'Outlined Noto Serif heading and Open Sans descriptor.',body)
 if tag in ('light','dark'):
  for w,h in [(180,45),(360,89),(720,178)]:
   raster(s,f'shopify/mdb-wordmark-{tag}-{w}x{h}.png',w,h)
 # Stacked arrangement with intentional breathing room.
 body=mark(159,42,102,ink)+centered(main,210,174,ink)+centered(cap,210,211,accent)
 s=save(f'masters/mdb-stacked-{tag}.svg',420,252,label,'Centered stacked identity and original M and D monogram.',body)
 if tag in ('light','dark'):
  raster(s,f'shopify/mdb-stacked-{tag}-840x504.png',840,504)
 s=save(f'masters/mdb-symbol-{tag}.svg',154,126,label+' monogram','Interlocked M and D, aligned within a clear-space canvas.',mark(25,30,104,ink))

for tag,bg,ink,rule in [('pine',PINE,IVORY,'#527361'),('ivory',IVORY,PINE,'#C1ADA0')]:
 art=f'<rect width="512" height="512" fill="{bg}"/><circle cx="256" cy="256" r="168" fill="none" stroke="{rule}" stroke-width="3"/>'+mark(138,183,236,ink)
 s=save(f'masters/mdb-avatar-{tag}.svg',512,512,'Matera Digital Boutique avatar','Circle-safe identity on a solid matte background.',art)
 for x in (180,512,1080):
  raster(s,f'social/mdb-avatar-{tag}-{x}x{x}.png',x,x)

icon_bg=f'<rect x="3" y="3" width="58" height="58" rx="11" fill="{PINE}"/>'
base=save('icons/favicon.svg',64,64,'Matera Digital Boutique favicon','Ivory monogram on a green tile.',icon_bg+mark(12,19,40,IVORY))
tiny=save('masters/mdb-optical-favicon.svg',64,64,'Matera Digital Boutique tiny favicon','Small-size monogram with widened features.',f'<rect width="64" height="64" rx="8" fill="{PINE}"/>'+mark(8,16.5,48,IVORY,tiny=True))
for x in (16,32,48,64):
 raster(tiny if x<=32 else base,f'icons/favicon-{x}x{x}.png',x,x)
app=save('masters/mdb-app-tile.svg',192,192,'Matera Digital Boutique app icon','Solid pine social or app tile.',f'<rect width="192" height="192" fill="{PINE}"/>'+mark(34,58,124,IVORY))
raster(app,'icons/apple-touch-icon-180x180.png',180,180)
raster(app,'icons/icon-192x192.png',192,192)
raster(app,'icons/icon-512x512.png',512,512)
# Maskable fast path guarantees the mark fits within 80% central safe area.
raster(app,'icons/icon-maskable-512x512.png',512,512)
with ThreadPoolExecutor(max_workers=6) as ex:list(ex.map(pngjob,assignments))
Image.open(HERE/'icons/favicon-64x64.png').save(HERE/'icons/favicon.ico',sizes=[(16,16),(32,32),(48,48),(64,64)],append_images=[Image.open(HERE/f'icons/favicon-{x}x{x}.png') for x in (16,32,48)])
print(f'{len(assignments)} PNG exports plus ICO; all sizes verified')
