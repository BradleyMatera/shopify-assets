from PIL import Image, ImageOps, ImageDraw, ImageFont
from pathlib import Path
p=Path(__file__).resolve().parents[1]
W,H=1480,1420
pine='#142B22'; paper='#F7F3EA'; clay='#9C4E38'; gold='#E4AD89'
im=Image.new('RGB',(W,H),paper);d=ImageDraw.Draw(im)
serif='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
sans='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def f(path,s):return ImageFont.truetype(path,s)
def txt(x,y,s,size,face=bold,c=pine):d.text((x,y),s,font=f(face,size),fill=c)
def crop(q,xy,wh,cent=(.5,.5)):
 src=Image.open(p/q).convert('RGB')
 im.paste(ImageOps.fit(src,wh,Image.Resampling.LANCZOS,centering=cent),xy)
d.rectangle((0,0,W,220),fill=pine)
mark=Image.open(p/'identity/shopify/mdb-horizontal-dark-880x203.png').convert('RGBA')
mark.thumbnail((474,115),Image.Resampling.LANCZOS);im.paste(mark,(57,47),mark)
txt(1030,63,'BRAND STANDARDS',18,c=gold);txt(1030,97,'KITCHEN & MARKET',26,c=paper)
txt(1030,143,'MATERA DIGITAL BOUTIQUE',15,c=paper)
crop('storefront/mdb-hero-wide-desktop-1440.webp',(57,253),(864,533),(.50,.48))
crop('storefront/mdb-hero-mobile-mobile-900.webp',(951,253),(472,533),(.50,.59))
txt(57,807,'01 / EDITORIAL WEB IMAGERY',17,c=clay)
txt(951,807,'02 / MOBILE ART DIRECTION',17,c=clay)
d.line((57,854,1423,854),fill='#D9CDB9',width=2)
for xy,lab,he in [(57,'PINE',pine),(404,'IVORY',paper),(751,'CLAY',clay),(1098,'APRICOT',gold)]:
 d.rounded_rectangle((xy,878,xy+324,989),radius=7,fill=he,outline='#D0C7B9',width=2)
 txt(xy+18,909,lab,19,c=paper if he in [pine,clay] else pine)
 txt(xy+18,944,he,16,face=sans,c=paper if he in [pine,clay] else pine)
txt(57,1032,'A small shop. A considered edit.',52,face=serif)
txt(58,1112,'Built for Shopify, social, editorial motion, and print.',21,face=sans)
cols=[('01 / IDENTITY','Responsive marks and icons'),('02 / CAMPAIGN','Templates across five networks'),('03 / OPERATIONS','Print-ready and accessible CX')]
for x,(title,lesson) in zip((58,518,980),cols):
 txt(x,1224,title,16,c=clay);txt(x,1255,lesson,20,face=sans)
d.line((57,1320,1423,1320),fill='#D9CDB9',width=2)
txt(57,1350,'PRODUCTION KIT  /  EDITORIAL PHOTOGRAPHY IS NOT SKU EVIDENCE',15,c=pine)
im.save(p/'guidelines/mdb-brand-overview.jpg',quality=91,progressive=True,optimize=True)
