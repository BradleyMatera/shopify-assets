"""Regenerate fixed-size operational print graphics and email headers.
Requires ReportLab and Pillow plus the Noto Serif and Open Sans font paths below.
Usage: python build-production.py (writes siblings; existing graphic exports are replaced).
"""
from pathlib import Path
from reportlab.lib.colors import CMYKColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont

out=Path(__file__).resolve().parent
FONT={
  "NotoSerif":"/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf",
  "NotoSerifItalic":"/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf",
  "OpenSans":"/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf",
  "OpenSansSemi":"/usr/share/fonts/truetype/open-sans/OpenSans-Semibold.ttf",
}
for name, path in FONT.items(): pdfmetrics.registerFont(TTFont(name,path))

# Process inks are starting recipes, not a printer ICC conversion.
CMYK={k:CMYKColor(*[x/100 for x in v]) for k,v in {
"Pine":(74,41,65,65),"Ivory":(2,3,7,0),"Rust":(24,74,81,12),
"Apricot":(4,33,45,0),"Ink":(0,0,0,90),"Mist":(19,7,16,4),
"Keyline":(20,21,29,2)}.items()}
RGB={"Pine":"#142B22", "Ivory":"#F7F3EA", "Rust":"#9C4E38", "Apricot":"#E4AD89", "Mist":"#D4DED5", "Keyline":"#D8CBB8"}
BLEED=9

def make(filename,title,w,h):
    W,H=w+2*BLEED,h+2*BLEED
    c=canvas.Canvas(str(out/filename),pagesize=(W,H),pageCompression=1,
        enforceColorSpace="CMYK",trimBox=(BLEED,BLEED,BLEED+w,BLEED+h),bleedBox=(0,0,W,H),
        artBox=(BLEED+15,BLEED+15,BLEED+w-15,BLEED+h-15),invariant=True)
    c.setTitle(title);c.setAuthor("Matera Digital Boutique")
    c.setSubject("Production artwork; process CMYK; trim and bleed boxes set")
    return c

def bg(c,w,h,key):
    c.setFillColor(CMYK[key]);c.rect(0,0,w+18,h+18,fill=1,stroke=0)

def txt(c,s,x,y,size,font="OpenSans",key="Pine",tracking=0,align="left"):
    width=pdfmetrics.stringWidth(s,font,size)+tracking*max(0,len(s)-1)
    if align=="center": x-=width/2
    if align=="right": x-=width
    c.setFillColor(CMYK[key]);o=c.beginText(x,y);o.setFont(font,size);o.setCharSpace(tracking);o.textLine(s);c.drawText(o)
    return width

def line(c,x,y,X,Y,key="Apricot",width=.5):
    c.setStrokeColor(CMYK[key]);c.setLineWidth(width);c.line(x,y,X,Y)

def frame(c,x,y,w,h,key="Apricot",width=.5):
    c.setStrokeColor(CMYK[key]);c.setLineWidth(width);c.rect(x,y,w,h,stroke=1,fill=0)

def arch(c,x,y,r,key="Apricot",width=.75):
    """Three inset arches: reusable ornament, not a substitute for main logo."""
    c.setStrokeColor(CMYK[key]);c.setLineWidth(width)
    for d in range(3):
        rr=r-d*r*.27
        p=c.beginPath();p.moveTo(x-rr,y);p.lineTo(x-rr,y+r*.70);p.curveTo(x-rr,y+r*.70+rr*.55,x-rr*.55,y+r*.70+rr,x,y+r*.70+rr)
        p.curveTo(x+rr*.55,y+r*.70+rr,x+rr,y+r*.70+rr*.55,x+rr,y+r*.70);p.lineTo(x+rr,y)
        c.drawPath(p,stroke=1,fill=0)

def lockup(c,x,y,scale=1,reverse=False,align="left"):
    k="Ivory" if reverse else "Pine"
    txt(c,"Matera Digital",x,y,22*scale,"NotoSerif",k,0,align)
    txt(c,"BOUTIQUE",x,y-14*scale,8.4*scale,"OpenSansSemi",("Apricot" if reverse else "Rust"),2.45*scale,align)

def insert():
    w,h=288,432
    c=make("packing-insert-4x6-cmyk.pdf","Matera Digital Boutique | Packing insert (4 × 6 inches)",w,h)
    bg(c,w,h,"Pine")
    frame(c,23,23,260,404)
    lockup(c,41,386,1,True)
    line(c,41,349,265,349)
    arch(c,233,285,24)
    txt(c,"Thanks for",41,224,36,"NotoSerif","Ivory")
    txt(c,"being here.",41,177,38,"NotoSerifItalic","Ivory")
    line(c,41,145,80,145,width=1.2)
    txt(c,"We’re glad you found something",41,109,12,"OpenSans","Mist")
    txt(c,"you wanted to bring home.",41,90,12,"OpenSans","Mist")
    c.showPage()

    bg(c,w,h,"Ivory")
    lockup(c,32,406,.75)
    line(c,32,370,274,370,"Keyline")
    txt(c,"Keep this handy.",32,324,29,"NotoSerif")
    data=[
      ("01","Check your item","Compare the contents with your order","confirmation. Keep your order number."),
      ("02","Care comes first","Follow the maker’s care guidance for","your exact item."),
      ("03","Need a hand?","Use our storefront’s Contact link. Include","your order number, never payment details."),
    ]
    for idx,(n,heading,a,b) in enumerate(data):
        y=275-77*idx
        txt(c,n,33,y+1,9,"OpenSansSemi","Rust",.8)
        txt(c,heading,61,y,16,"NotoSerif","Pine")
        txt(c,a,61,y-19,9.8,"OpenSans","Ink")
        txt(c,b,61,y-34,9.8,"OpenSans","Ink")
        line(c,32,y-47,274,y-47,"Keyline")
    txt(c,"ORDER & CARE",32,35,7,"OpenSansSemi","Rust",1.7)
    c.showPage();c.save()

def round_seal():
    w=h=144
    c=make("round-seal-2in-cmyk.pdf","Matera Digital Boutique | 2-inch round box seal",w,h)
    bg(c,w,h,"Pine")
    c.setLineWidth(.6);c.setStrokeColor(CMYK["Apricot"]);c.circle(81,81,62,stroke=1,fill=0)
    arch(c,81,107,9.3,width=.6)
    lockup(c,81,84,.70,True,"center")
    line(c,55,57,107,57,width=.5)
    txt(c,"MATERA",81,40,6.5,"OpenSansSemi","Ivory",1.35,"center")
    c.showPage();c.save()

def wrap():
    w,h=216,90
    c=make("box-label-3x1.25-cmyk.pdf","Matera Digital Boutique | 3 × 1.25-inch box label",w,h)
    bg(c,w,h,"Ivory")
    frame(c,15,15,204,78,"Rust")
    line(c,172,26,172,82,"Keyline")
    lockup(c,29,57,.91)
    arch(c,196,47,12,"Rust",.6)
    c.showPage();c.save()

def get(name,size):return ImageFont.truetype(FONT[name],size)
def tracked(draw,t,x,y,font,color,gap):
    for ch in t: draw.text((x,y),ch,font=font,fill=color,anchor="ls");x+=draw.textlength(ch,font=font)+gap

def email(dark):
    w,h=1200,260
    bg,head,sub,r=(RGB["Pine"],RGB["Ivory"],RGB["Apricot"],RGB["Apricot"]) if dark else (RGB["Ivory"],RGB["Pine"],RGB["Rust"],RGB["Rust"])
    im=Image.new("RGB",(w,h),bg);d=ImageDraw.Draw(im)
    d.rectangle((38,38,w-38,h-38),outline=r,width=1)
    d.text((86,137),"Matera Digital",font=get("NotoSerif",74),fill=head,anchor="ls")
    tracked(d,"BOUTIQUE",88,183,get("OpenSansSemi",25),sub,6)
    for dlt in (0,15,30):
        a=56-dlt
        d.arc((998-a,100-a,998+a,100+a),180,360,fill=r,width=2)
        d.line([(998-a,100),(998-a,163)],fill=r,width=2)
        d.line([(998+a,100),(998+a,163)],fill=r,width=2)
    im.save(out/("email-header-pine-1200x260.png" if dark else "email-header-ivory-1200x260.png"),optimize=True)

insert();round_seal();wrap();email(True);email(False)
