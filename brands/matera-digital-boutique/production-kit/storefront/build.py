from PIL import Image, ImageOps
from pathlib import Path
p=Path(__file__).resolve().parent
s=p.parent/'photography'/'source'
presets={
 'hero-wide': [('desktop', (1440,810),(.52,.45)),('desktop',(1080,608),(.52,.45)),('desktop',(768,432),(.52,.45)),('poster',(960,540),(.52,.45))],
 'hero-mobile': [('mobile',(900,1200),(.52,.56)),('mobile',(720,960),(.52,.56)),('mobile',(480,640),(.52,.56)),('poster-mobile',(720,960),(.52,.56))],
 'market-editorial': [('card',(900,600),(.60,.5)),('card',(540,360),(.60,.5)),('social',(1080,1080),(.74,.5)),('share',(1200,630),(.65,.51))],
 'kitchen-editorial': [('card',(900,600),(.55,.5)),('card',(540,360),(.55,.5)),('social',(1080,1080),(.67,.5)),('share',(1200,630),(.60,.51))]
}
for name, xs in presets.items():
 im=Image.open(s/f'{name}.png' if (s/f'{name}.png').exists() else s/f'{name}.webp').convert('RGB')
 for label,wh,pos in xs:
  if name.endswith('editorial') and label=='social': wh=(960,960)
  out=ImageOps.fit(im,wh,Image.Resampling.LANCZOS,centering=pos)
  out.save(p/f'mdb-{name}-{label}-{wh[0]}.webp', 'WEBP', quality=85, method=6)
  if label=='share':out.save(p/f'mdb-{name}-share-{wh[0]}.jpg',quality=92,progressive=True,optimize=True)
for name in presets:
 im=Image.open(s/f'{name}.png' if (s/f'{name}.png').exists() else s/f'{name}.webp').convert('RGB')
 im.save(s/f'{name}.webp','WEBP',quality=93,method=6)
