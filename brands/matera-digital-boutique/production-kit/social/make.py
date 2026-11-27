from pathlib import Path
import json,random,math,html
p=Path(__file__).resolve().parent
P,I,R,A='#142B22','#F7F3EA','#9C4E38','#E4AD89'
SERIF='Nimbus Roman, Georgia, serif'; SANS='Liberation Sans, Arial, sans-serif'
targets={
'facebook-feed':(1200,1500,'portrait'),'facebook-cover':(1640,624,'banner'),
'instagram-feed':(1080,1350,'portrait'),'instagram-square':(1080,1080,'portrait'),
'instagram-story':(1080,1920,'story'),'pinterest-pin':(1000,1500,'portrait'),
'x-post':(1600,900,'wide'),'x-header':(1500,500,'banner'),
'youtube-thumbnail':(1280,720,'wide'),'youtube-banner':(2560,1440,'yt')}
campaigns={
'market-notes':{'kicker':'KITCHEN & MARKET / 01','line':['Market','Notes.'],'description':'For the way we gather.','sub':'GATHER WELL.','paper':I,'ink':P,'accent':R},
'counter-edit':{'kicker':'KITCHEN & MARKET / 02','line':['The Counter','Edit.'],'description':'A softer kind of everyday.','sub':'MAKE ROOM.','paper':P,'ink':I,'accent':A}}
def esc(s):return html.escape(str(s),quote=True)
def tx(x,y,s,label,size,fill,serif=False,weight=400,tracking=0,align='start',italic=False):
 p=SERIF if serif else SANS
 return f'<text id="{label}" x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-family="{p}" font-size="{size:.1f}" font-weight="{weight}" letter-spacing="{tracking:.1f}" text-anchor="{align}"'+(' font-style="italic"' if italic else '')+'>'+esc(s)+'</text>'
def rect(x,y,w,h,c,o=1):return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{c}" opacity="{o}"/>'
def line(x,y,x2,y2,c,o=1):return f'<path d="M{x:.1f} {y:.1f}H{x2:.1f}" stroke="{c}" fill="none" opacity="{o}" stroke-width="{y2}"/>'
def group(name,s):return f'<g id="{name}" inkscape:groupmode="layer" inkscape:label="{name}">{s}</g>'
def monogram(x,y,n,ink):
 return f'<g transform="translate({x} {y}) scale({n/60})" fill="none" stroke="{ink}"><circle r="29" stroke-width="1.1"/><path d="M -15 10 V -12 L -5 3 L 5 -12 V 10 M 10 10 V -12 h 3 a 11 11 0 0 1 0 22 z" stroke-width="1.3"/></g>'
def arch(x,y,w,h):
 a=min(w*.5,h*.85)
 return f'M{x:.1f} {y+h:.1f}V{y+a:.1f}a{w/2:.1f} {a:.1f} 0 0 1 {w:.1f} 0V{y+h:.1f}Z'
def hallmark(x,y,w,h,fill,accent,seed):
 rng=random.Random(seed)
 s=rect(x,y,w,h,fill)
 for _ in range(min(3300,int(w*h/115))):
  xx=x+rng.random()*w;yy=y+rng.random()*h
  s+=f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="{rng.choice([.35,.48,.62,.85]):.2f}" fill="{accent}" opacity="{rng.choice([.13,.2,.26]):.2f}"/>'
 cx=x+w*.51;cy=y+h*.5;r=min(w,h)*.32
 for i in range(24):
  a=math.tau*i/24
  if i%6==0:continue
  x1=cx+r*1.06*math.cos(a);y1=cy+r*1.06*math.sin(a);x2=cx+r*1.13*math.cos(a);y2=cy+r*1.13*math.sin(a)
  s+=f'<path d="M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}" stroke="{accent}" opacity=".48" fill="none"/>'
 for k,o in [(1,.78),(.88,.4),(.72,.20)]:
  s+=f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*k:.1f}" fill="none" opacity="{o}" stroke="{accent}" stroke-width="{max(1,w/450):.1f}"/>'
 s+=monogram(cx,cy,r*.82,accent)
 return s
manifest=[]
for key,(W,H,kind) in targets.items():
 for name,c in campaigns.items():
  paper,ink,accent=c['paper'],c['ink'],c['accent']; Wf=float(W);Hf=float(H)
  if kind in ('portrait','story'):
   m=W*.095;safe_top=H*.15 if kind=='story' else H*.072;safe_end=H*.81 if kind=='story' else H*.91
   X,Y,V,T=W*.48,H*.245,W*.445,safe_end-H*.245
   headx=m;heady=H*.435;f=W*(.102 if name=='market-notes' else .076); gap=f*.89
   foot=safe_end; a='start'; box=(m,safe_top,W-m,safe_end); keyx=m
  elif kind=='wide':
   m=W*.075;safe_top=H*.12;safe_end=H*.875
   X,Y,V,T=W*.57,H*.092,W*.36,H*.82
   headx=m;heady=H*.47;f=W*(.085 if name=='market-notes' else .072);gap=f*.84
   foot=safe_end; a='start'; box=(m,safe_top,W-m,safe_end); keyx=m
  else:
   m=W*.09;safe_top=H*.20;safe_end=H*.83
   if key=='youtube-banner':
    bx=(W-1546)/2;by=(H-423)/2;m=bx+85;safe_top=by+72;safe_end=by+364
    X,Y,V,T=W*.57,(H-423)/2+28,W*.204,370
    headx=m;heady=by+170;f=98 if name=='market-notes' else 91;gap=f*.82
    foot=safe_end;a='start';box=(bx,by,bx+1546,by+423);keyx=m
   else:
    X,Y,V,T=W*.63,H*.04,W*.29,H*.94
    headx=m;heady=H*.47;f=H*(.245 if name=='market-notes' else .208);gap=f*.79
    foot=safe_end;a='start';box=(W*.12,H*.15,W*.88,H*.85);keyx=m
  if key=='x-header':
   m=W*.18;keyx=m;headx=m;box=(W*.16,H*.15,W*.88,H*.85)
  if key=='facebook-cover':
   m=W*.145;keyx=m;headx=m
  start=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><title>Matera Digital Boutique: {esc(name)}, {key}</title><desc>Editable {key} brand design for Matera Digital Boutique. Artwork layer accepts one editorial image.</desc>'
  start=start.replace('http://www.inkscape.org/namespaces/inkscape','http://www.inkscape.org/namespaces/inkscape')
  d=arch(X,Y,V,T)
  bg=rect(0,0,W,H,paper)+line(0,H*.017,W,max(2,H*.005),accent,.9)+line(0,H*.983,W,max(1,H*.002),accent,.72)
  if key=='youtube-banner':
   bg+=f'<circle cx="{W*.69:.1f}" cy="{H*.5:.1f}" r="{H*.405:.1f}" stroke="{accent}" opacity=".25" fill="none" stroke-width="2"/><circle cx="{W*.69:.1f}" cy="{H*.5:.1f}" r="{H*.452:.1f}" stroke="{accent}" opacity=".13" fill="none" stroke-width="2"/>'
  bcol=A if paper==I else R
  baseart=f'<g clip-path="url(#art-window)">'+hallmark(X,Y,V,T,bcol,P if paper==I else I,77 if name=='market-notes' else 127)+'</g>'
  border=f'<path d="{d}" fill="none" stroke="{ink}" opacity=".35" stroke-width="{max(1,W/800):.1f}"/>'
  sz=W*(.020 if kind in ('portrait','story') else .014)
  if key=='youtube-banner':sz=25
  if kind=='banner':sz=H*.038
  badge=tx(keyx,safe_top,c['kicker'],'eyebrow',sz*.88,accent,weight=700,tracking=sz*.20)
  label=tx(headx,heady,c['line'][0],'headline-1',f,ink,serif=True,tracking=-f*.044)+tx(headx,heady+gap,c['line'][1],'headline-2',f,ink,serif=True,tracking=-f*.044,italic=True)
  if kind in ('portrait','story'):
   rule_y=heady+gap+f*.36
   label+=line(headx,rule_y,headx+W*.102,max(1,W*.0011),accent,.82)
   wrapped=['For the way','we gather.'] if name=='market-notes' else ['A softer kind','of everyday.']
   label+=tx(headx,rule_y+sz*2.0,wrapped[0],'deck',sz*1.6,ink,serif=True)+tx(headx,rule_y+sz*3.7,wrapped[1],'deck-second',sz*1.6,ink,serif=True)
  else:
   if kind=='yt': rule_y=heady+gap+24
   else:rule_y=heady+gap+sz*1.05
   label+=tx(headx,rule_y+sz,c['description'],'deck',sz*1.25,ink,serif=True)
  label+=line(headx,foot-sz*1.12,headx+(W*.36 if kind in ('portrait','story') else W*.34),max(1,W*.00065),ink,.28)
  label+=tx(headx,foot,'Matera Digital Boutique','wordmark',sz*.95,ink,weight=700,tracking=sz*.055)
  if kind in ('portrait','story'):
   label+=tx(X+V*.95,foot+sz*1.45,c['sub'],'issue-tag',sz*.61,accent,weight=700,tracking=sz*.16,align='end')
  guides=f'<rect x="{box[0]:.1f}" y="{box[1]:.1f}" width="{box[2]-box[0]:.1f}" height="{box[3]-box[1]:.1f}" fill="none" stroke="#ff00ff" stroke-width="3" stroke-dasharray="14 10"/>'
  base=start+f'<defs><clipPath id="art-window"><path d="{d}"/></clipPath></defs>'+group('Background',bg)
  tail=group('Window border',border)+group('Editable copy',badge+label)+group('Safe guides',f'<g style="display:none">{guides}</g>')+'</svg>\n'
  stem=f'{name}--{key}'
  (p/'templates'/f'{stem}--brand.svg').write_text(base+group('Brand illustration',baseart)+tail)
  image=f'<g clip-path="url(#art-window)">{rect(X,Y,V,T,bcol)}<image id="REPLACE_EDITORIAL_IMAGE" x="{X:.1f}" y="{Y:.1f}" width="{V:.1f}" height="{T:.1f}" preserveAspectRatio="xMidYMid slice" xlink:href="EDITORIAL_IMAGE_GOES_HERE.jpg"/></g>'
  (p/'templates'/f'{stem}--photo.svg').write_text(base+group('Replace editorial photo',image)+tail)
  manifest.append(dict(file=stem,width=W,height=H,use=kind,channel=key,campaign=name,safe=[round(j) for j in box],photo=[round(j) for j in (X,Y,V,T)]))
(p/'formats.json').write_text(json.dumps(manifest,indent=2)+'\n')
