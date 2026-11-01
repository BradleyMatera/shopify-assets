"""Build concrete assets. No font files redistributed; no false resolution claims."""
from __future__ import annotations
import collections, hashlib, json, math, os, shutil, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
import cairosvg
ROOT=Path(os.environ.get('ASSET_ROOT',Path(__file__).resolve().parents[1])); A=ROOT/'assets'
for name in ['brand','icons','backgrounds','hero','departments','campaigns','social','email','motion']:(A/name).mkdir(parents=True,exist_ok=True)
for name in ['production','preview','theme','email','docs']:(ROOT/name).mkdir(exist_ok=True)
INK='#11181d'; IVORY='#f6f2e9'; BRONZE='#b89a68'; PALETTE={'ink':INK,'ivory':IVORY,'bronze':BRONZE}
DEPTS=[('fashion-accessories','Fashion & Accessories'),('home-kitchen','Home & Kitchen'),('bags-travel','Bags & Travel'),('beauty-self-care','Beauty & Self-Care'),('pets','Pets'),('tech-desk','Tech & Desk'),('outdoors-fitness','Outdoors & Fitness'),('kids-hobbies','Kids & Hobbies'),('digital-downloads','Digital Downloads')]
def font(size,serif=False):
    names=(['/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf','/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf','/usr/share/fonts/opentype/urw-base35/NimbusRoman-Regular.otf'] if serif else ['/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf','/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf','/usr/share/fonts/opentype/inter/Inter-Regular.otf'])
    for p in names:
        if Path(p).exists():return ImageFont.truetype(p,size)
    return ImageFont.load_default(size=size)
def tracked(draw,text,xy,size,fill,spacing=4,serif=False,center=False):
    f=font(size,serif); widths=[draw.textlength(c,font=f) for c in text]; total=sum(widths)+max(0,len(text)-1)*spacing;x,y=xy
    if center:x-=total/2
    for c,w in zip(text,widths):draw.text((x,y),c,font=f,fill=fill,anchor='lt');x+=w+spacing
    return total
def write_image(image,path,quality=90):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if path.suffix=='.webp':image.save(path,quality=quality,method=6)
    elif path.suffix in ('.jpg','.jpeg'):image.convert('RGB').save(path,quality=quality,subsampling=0,optimize=True)
    else:image.save(path,optimize=True)
def fitted(image,size):
    if max(size[0]/image.width,size[1]/image.height)>1.00001:raise ValueError(f'Upscaling refused: {image.size} -> {size}')
    return ImageOps.fit(image,size,method=Image.Resampling.LANCZOS,centering=(.5,.45))
def mark(size,color):
    im=Image.new('RGBA',(size,size));d=ImageDraw.Draw(im)
    def poly(points):d.polygon([(x*size/512,y*size/512) for x,y in points],fill=color)
    poly([(52,426),(208,90),(268,218),(233,291),(208,233),(118,426)])
    poly([(242,292),(339,90),(496,426),(423,426),(339,242),(308,310),(363,426),(289,426)])
    return im
for name,color in PALETTE.items():
    write_image(mark(1024,color).resize((512,512),Image.Resampling.LANCZOS),A/'brand'/f'monogram-{name}-512.png')
    canvas=Image.new('RGBA',(3200,720));canvas.alpha_composite(mark(640,color),(30,20));d=ImageDraw.Draw(canvas)
    tracked(d,'REAL MALL',(790,140),228,color,spacing=18,serif=True);tracked(d,'OF AMERICA',(807,421),88,color,spacing=29)
    write_image(canvas.resize((1600,360),Image.Resampling.LANCZOS),A/'brand'/f'wordmark-horizontal-{name}.png')
    stacked=Image.new('RGBA',(1800,1500));stacked.alpha_composite(mark(700,color),(550,20));d=ImageDraw.Draw(stacked)
    tracked(d,'REAL MALL',(900,875),188,color,spacing=12,serif=True,center=True);tracked(d,'OF AMERICA',(900,1130),70,color,spacing=22,center=True)
    write_image(stacked.resize((900,750),Image.Resampling.LANCZOS),A/'brand'/f'wordmark-stacked-{name}.png')
avatar=Image.new('RGBA',(512,512),INK);avatar.alpha_composite(mark(410,BRONZE),(51,51));write_image(avatar,A/'brand'/'social-avatar-512.png')
for s in [16,32,48,64,180,192]:write_image(avatar.resize((s,s),Image.Resampling.LANCZOS),A/'brand'/f'favicon-{s}.png')
avatar.save(A/'brand'/'favicon.ico',sizes=[(16,16),(32,32),(48,48),(64,64)])
ICONS={
'search':'<circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/>',
'shopping-bag':'<path d="M5 8h14l1 13H4L5 8Z"/><path d="M8 9V6a4 4 0 0 1 8 0v3"/>',
'cart':'<path d="M2 4h3l2.5 12h11.8L21 7H5.7"/><circle cx="9" cy="20" r="1"/><circle cx="18" cy="20" r="1"/>',
'account':'<circle cx="12" cy="7" r="4"/><path d="M4 21v-1a8 8 0 0 1 16 0v1"/>',
'heart':'<path d="M12 21 3.5 12.5C-1 6 6 1 12 7c6-6 13-1 8.5 5.5L12 21Z"/>',
'menu':'<path d="M3 5h18M3 12h18M3 19h18"/>',
'close':'<path d="m5 5 14 14M19 5 5 19"/>',
'arrow-right':'<path d="M3 12h17m-7-7 7 7-7 7"/>',
'arrow-left':'<path d="M21 12H4m7-7-7 7 7 7"/>',
'chevron-down':'<path d="m5 9 7 7 7-7"/>','chevron-up':'<path d="m5 15 7-7 7 7"/>',
'plus':'<path d="M12 4v16M4 12h16"/>','minus':'<path d="M4 12h16"/>','check':'<path d="m4 12 5 5L20 6"/>',
'filters':'<path d="M4 6h3m4 0h9M4 12h10m4 0h2M4 18h2m4 0h10"/><circle cx="9" cy="6" r="2"/><circle cx="16" cy="12" r="2"/><circle cx="8" cy="18" r="2"/>',
'grid':'<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
'list':'<path d="M9 5h12M9 12h12M9 19h12M3 5h1M3 12h1M3 19h1"/>',
'delivery':'<path d="M2 5h12v12H2V5Zm12 4h4l4 5v3h-8"/><circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="18" r="2.5"/>',
'return':'<path d="m8 3-5 5 5 5M3 8h11a7 7 0 1 1 0 14"/>',
'package':'<path d="m12 2 10 5-10 5L2 7 12 2ZM2 7v11l10 5 10-5V7M12 12v11M7 4.5l10 5V15"/>',
'help':'<circle cx="12" cy="12" r="9"/><path d="M9 8a3 3 0 0 1 6 0c0 2-3 2-3 5M12 17h.01"/>',
'mail':'<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 5 10 8L22 5"/>',
'chat':'<path d="M21 4H3v14h4v4l5-4h9V4Z"/>',
'pin':'<path d="M19 9c0 6-7 13-7 13S5 15 5 9a7 7 0 0 1 14 0Z"/><circle cx="12" cy="9" r="2.5"/>',
'clock':'<circle cx="12" cy="12" r="9"/><path d="M12 6v6l4 3"/>',
'download':'<path d="M12 2v14m-5-5 5 5 5-5M3 17v5h18v-5"/>',
'upload':'<path d="M12 17V3m-5 5 5-5 5 5M3 17v5h18v-5"/>',
'external-link':'<path d="M14 3h7v7M21 3 10 14M10 3H3v18h18v-7"/>',
'play':'<path d="m8 4 12 8-12 8V4Z"/>','pause':'<path d="M8 4v16M16 4v16"/>',
'volume-off':'<path d="m11 4-6 5H2v6h3l6 5V4Zm5 5 6 6m0-6-6 6"/>',
'gift':'<path d="M3 9h18v5H3V9Zm2 5v8h14v-8M12 9v13"/><path d="M12 9C1 9 4 0 9 4l3 5Zm0 0c11 0 8-9 3-5l-3 5Z"/>',
'home':'<path d="m2 11 10-9 10 9M5 9v13h5v-8h4v8h5V9"/>',
'sun':'<circle cx="12" cy="12" r="4"/><path d="M12 1v3m0 16v3M1 12h3m16 0h3M4 4l2 2m12 12 2 2M20 4l-2 2M6 18l-2 2"/>',
'moon':'<path d="M21 14A9 9 0 0 1 10 3a9 9 0 1 0 11 11Z"/>',
'info':'<circle cx="12" cy="12" r="9"/><path d="M12 11v7M12 7h.01"/>'}
(ROOT/'production'/'icon-geometry.json').write_text(json.dumps(ICONS,indent=2)+'\n')
for name,body in ICONS.items():
    for tone,color in PALETTE.items():
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{body}</svg>'
        for size in [32,96]:cairosvg.svg2png(bytestring=svg.encode(),write_to=str(A/'icons'/f'{name}-{tone}-{size}.png'),output_width=size,output_height=size)
rng=np.random.default_rng(261101);w,h=1600,1000;y,x=np.mgrid[0:h,0:w];xx=x/w;yy=y/h;noise=rng.normal(0,1,(h,w))
materials={
'graphite':((17,24,29),4*np.sin(xx*3+yy*2)+1.5*noise+5*np.cos(xx*7-yy*4)),
'warm-limestone':((237,231,218),2*noise+3*np.sin(yy*21+np.sin(xx*5)*.4)),
'brushed-bronze':((153,126,82),10*np.sin(xx*2.8+yy*.4)+rng.normal(0,1,(h,1))*1.3+noise*.7),
'midnight-silk':((18,24,30),12*np.sin(yy*5+np.sin(xx*2.3))*np.cos(xx*1.7)+noise*.5),
'ivory-linen':((245,241,232),noise+1.3*np.sin(x*math.pi)+1.3*np.cos(y*math.pi)),
'bronze-atmosphere':((30,29,28),55*np.exp(-((xx-.74)**2/.04+(yy-.43)**2/.16))+noise*.4)}
for name,(base,light) in materials.items():
    rgb=np.stack([np.clip(base[c]+light,0,255) for c in range(3)],axis=-1).astype('uint8');image=Image.fromarray(rgb)
    for ext in ['png','webp']:write_image(image,A/'backgrounds'/f'{name}.{ext}')
source_data=json.loads((ROOT/'production'/'sources.json').read_text()) if (ROOT/'production'/'sources.json').exists() else {'sources':[],'failures':[]}
sources={r['id']:r for r in source_data['sources']};hero=A/'masters'/'atrium-evening.png'
if hero.exists():
    image=Image.open(hero).convert('RGB')
    for width in [480,768,1280,1600]:
        if width<=image.width:
            for ext in ['webp','jpg']:write_image(fitted(image,(width,round(width*9/16))),A/'hero'/f'atrium-desktop-{width}.{ext}')
    for width in [360,480,648]:
        for ext in ['webp','jpg']:write_image(fitted(image,(width,width*4//3)),A/'hero'/f'atrium-mobile-{width}.{ext}')
    write_image(fitted(image,(1280,720)),A/'motion'/'atrium-poster.jpg')
for slug,title in DEPTS:
    path=A/'masters'/f'{slug}.jpg'
    if not path.exists():continue
    image=Image.open(path).convert('RGB');destination=A/'departments'/slug
    for width in [320,480,640]:
        for ratio,name in [(1,'square'),(1.6,'wide')]:
            size=(width,round(width/ratio))
            if size[0]<=image.width and size[1]<=image.height:
                for ext in ['webp','jpg']:write_image(fitted(image,size),destination/f'{name}-{width}.{ext}')
    for width in [320,480]:
        size=(width,round(width*4/3))
        if size[1]<=image.height:
            for ext in ['webp','jpg']:write_image(fitted(image,size),destination/f'portrait-{width}.{ext}')
campaigns=[
('discover','atrium-evening','A world of finds.','One destination.','Explore the departments','/collections/all'),
('new-arrivals','fashion-accessories','Fresh perspectives.','New arrivals.','Explore new arrivals','/collections/new-arrivals'),
('home-edit','home-kitchen','Make room','for everyday beauty.','Explore home & kitchen','/collections/home-kitchen'),
('outdoor-edit','outdoors-fitness','A little further.','A lot to discover.','Explore the outdoors','/collections/outdoors-fitness'),
('spring-edit','spring','Room to bloom.','The spring edit.','Explore the collection','/collections/all'),
('summer-edit','summer','A lighter outlook.','The summer edit.','Explore the collection','/collections/all'),
('autumn-edit','autumn','A warmer welcome.','The autumn edit.','Explore the collection','/collections/all'),
('holiday-edit','holiday','Thoughtful finds.','Beautifully given.','Discover gift ideas','/collections/all')]
(ROOT/'production'/'campaign-copy.json').write_text(json.dumps([dict(zip(['id','source','heading','subheading','cta','url'],c)) for c in campaigns],indent=2)+'\n')
def get_scene(slug):
    p=A/'masters'/('atrium-evening.png' if slug=='atrium-evening' else f'{slug}.jpg')
    return Image.open(p).convert('RGB') if p.exists() else None
for slug,source,title,subtitle,cta,url in campaigns:
    scene=get_scene(source)
    if scene is None:continue
    canvas=Image.new('RGB',(1600,640),INK);d=ImageDraw.Draw(canvas);canvas.paste(fitted(scene,(800,600)),(800,20))
    tracked(d,'REAL MALL OF AMERICA',(70,63),20,BRONZE,spacing=4)
    d.text((66,195),title,font=font(64,True),fill=IVORY);d.text((66,274),subtitle,font=font(49,True),fill=IVORY)
    d.line((70,428,540,428),fill=BRONZE,width=1);d.text((70,468),cta+'  →',font=font(25),fill=IVORY)
    for ext in ['webp','jpg']:write_image(canvas,A/'campaigns'/f'{slug}-banner-1600.{ext}')
    for label,size in [('square',(1080,1080)),('portrait',(1080,1350)),('landscape',(1200,630))]:
        out=Image.new('RGB',size,IVORY);dr=ImageDraw.Draw(out)
        if label=='landscape':
            out.paste(fitted(scene,(600,600)),(580,15));tracked(dr,'REAL MALL',(50,48),24,INK,spacing=5)
            dr.text((47,205),title,font=font(44,True),fill=INK);dr.text((47,267),subtitle,font=font(34,True),fill=INK)
            dr.line((50,422,450,422),fill=BRONZE,width=2);dr.text((50,460),cta,font=font(22),fill=INK)
        else:
            tracked(dr,'REAL MALL OF AMERICA',(540,62),20,INK,spacing=4,center=True)
            dr.text((540,146),title,font=font(64,True),fill=INK,anchor='mt');dr.text((540,228),subtitle,font=font(48,True),fill=INK,anchor='mt')
            top=350 if label=='square' else 455;out.paste(fitted(scene,(760,570)),(160,top))
            dr.line((160,top+600,920,top+600),fill=BRONZE,width=1);dr.text((540,top+637),cta,font=font(24),fill=INK,anchor='mt')
        write_image(out,A/'social'/f'{slug}-{label}.jpg')
    banner=Image.new('RGB',(1200,400),INK);dr=ImageDraw.Draw(banner);banner.paste(fitted(scene,(600,380)),(590,10))
    tracked(dr,'REAL MALL',(38,42),22,BRONZE,spacing=5);dr.text((35,141),title,font=font(43,True),fill=IVORY)
    dr.text((35,198),subtitle,font=font(31,True),fill=IVORY);dr.text((38,317),cta,font=font(20),fill=IVORY)
    write_image(banner,A/'email'/f'{slug}-1200.jpg')
def encode_loop(source,slug,width=1280,height=720):
    output=A/'motion'/f'{slug}-{width}x{height}'
    if output.with_suffix('.mp4').exists() and output.with_suffix('.webm').exists():return
    vf=f"scale=3344:-1,zoompan=z='1.02+0.025*(1-cos(2*PI*on/180))':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=180:s={width}x{height}:fps=30,format=yuv420p"
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(source),'-vf',vf,'-t','6','-an']
    subprocess.run(cmd+['-c:v','libx264','-preset','medium','-crf','22','-movflags','+faststart',str(output.with_suffix('.mp4'))],check=True,timeout=180)
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(output.with_suffix('.mp4')),'-c:v','libvpx-vp9','-b:v','0','-crf','33','-row-mt','1','-an',str(output.with_suffix('.webm'))],check=True,timeout=180)
if shutil.which('ffmpeg') and hero.exists() and os.environ.get('SKIP_MOTION')!='1':
    encode_loop(hero,'atrium-desktop',1280,720);encode_loop(A/'hero'/'atrium-mobile-648.jpg','atrium-mobile',648,864);encode_loop(A/'backgrounds'/'bronze-atmosphere.png','ambient-bronze',1280,720)
registry=[]
for path in sorted(A.rglob('*')):
    if not path.is_file():continue
    data=path.read_bytes();item={'path':str(path.relative_to(ROOT)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'group':path.relative_to(A).parts[0]}
    if path.suffix.lower() in ['.png','.jpg','.webp','.ico']:
        with Image.open(path) as image:item['width'],item['height']=image.size
    elif path.suffix.lower() in ['.mp4','.webm']:item['motion_type']='Six-second camera-motion loop from a still image; no generated live-action movement'
    registry.append(item)
counts=dict(collections.Counter(r['group'] for r in registry))
report={'total_files':len(registry),'groups':counts,'sources':len(sources),'department_sources':sum((A/'masters'/f'{s}.jpg').exists() for s,_ in DEPTS),'generation_failures':source_data.get('failures',[]),'scope':'Generated asset library, not a published Shopify theme','files':registry}
(ROOT/'production'/'asset-manifest.json').write_text(json.dumps(report,indent=2)+'\n')
(ROOT/'production'/'SHA256SUMS.txt').write_text(''.join(f"{r['sha256']}  {r['path']}\n" for r in registry))
print(json.dumps({k:v for k,v in report.items() if k!='files'},indent=2))
