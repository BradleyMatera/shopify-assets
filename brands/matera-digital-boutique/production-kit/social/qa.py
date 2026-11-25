import json,xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
p=Path(__file__).resolve().parent
f=json.loads((p/'formats.json').read_text())
TH=265;TW=280; w=TW*5;h=TH*4+90
im=Image.new('RGB',(w,h),'#ebe2d1');d=ImageDraw.Draw(im)
font='/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf'
font2='/usr/share/fonts/opentype/urw-base35/NimbusRoman-Regular.otf'
d.text((16,14),'The Kitchen & Market studio',fill='#142B22',font=ImageFont.truetype(font2,40))
d.text((18,60),'MATERA DIGITAL BOUTIQUE  /  SOCIAL CAMPAIGN SYSTEMS 01–02',fill='#9C4E38',font=ImageFont.truetype(font,15))
for i,r in enumerate(sorted(f,key=lambda x:(x['campaign'],x['channel']))):
 x,y=TW*(i%5),90+TH*(i//5)
 s=r['file']
 img=Image.open(p/'exports'/f'{s}--brand.png').convert('RGBA')
 assert img.size==(r['width'],r['height']), (s,img.size)
 assert img.getextrema()[3]==(255,255)
 for var in ['brand','photo']:
  svg=(p/'templates'/f'{s}--{var}.svg').read_text()
  ET.fromstring(svg)
  assert 'Matera Digital Boutique' in svg and (svg.count('REPLACE_EDITORIAL_IMAGE')==(1 if var=='photo' else 0))
 img.thumbnail((TW-26,TH-62),Image.Resampling.LANCZOS)
 d.rectangle((x+5,y+4,x+TW-6,y+TH-6),fill='#F7F3EA',outline='#cbbfab')
 im.paste(img,(x+(TW-img.width)//2,y+12),img)
 d.text((x+14,y+TH-44),r['channel'].replace('-',' ').title(),fill='#142B22',font=ImageFont.truetype(font,16))
 d.text((x+14,y+TH-24),f"{r['campaign'].replace('-',' ').title()}  /  {r['width']} × {r['height']}",fill='#725443',font=ImageFont.truetype(font,12))
im.save(p/'contact-sheet.jpg',quality=93)
print('Passed: 20 PNG dimensions & opacity, 40 SVG XML contracts and editable-photo markers.')
