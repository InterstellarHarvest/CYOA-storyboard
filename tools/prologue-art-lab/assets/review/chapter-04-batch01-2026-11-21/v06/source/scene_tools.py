"""Direct native scene drawing, no raster reads, resampling or large canvas.

Only scene writers import this module. The authorized source-derived portrait
has a separate pipeline. Native material clusters use explicit selected ramps.
"""
from PIL import Image,ImageDraw
from pathlib import Path
import math

class Canvas:
    def __init__(self):
        self.im=Image.new('RGB',(314,206),'#aaa68c');self.d=ImageDraw.Draw(self.im);self.clip=None
    def poly(self,p,c,o=None):
        p=[(round(x),round(y)) for x,y in p];self.d.polygon(p,fill=c)
        if o:self.d.line(p+[p[0]],fill=o,width=1)
    def line(self,p,c,w=1):self.d.line([(round(x),round(y)) for x,y in p],fill=c,width=w)
    def box(self,p,c,o=None):self.d.rectangle(tuple(round(v) for v in p),fill=c,outline=o)
    def ellipse(self,p,c,o=None):self.d.ellipse(tuple(round(v) for v in p),fill=c,outline=o)
    def save(self,p):Path(p).parent.mkdir(exist_ok=True);self.im.save(p)

def project(x,y,z,vp=(185,88),f=220,eye=1.6):return (round(vp[0]+f*x/z),round(vp[1]-f*(y-eye)/z))

def floor(c,vp,left,back,right,wood=False):
    # All projected floor slab edges share the explicit camera vanishing point.
    mask=Image.new('1',(314,206),0);md=ImageDraw.Draw(mask)
    md.polygon([left,back,right,(314,206),(0,206)],fill=1)
    layer=Canvas();layer.box((0,0,313,205),'#999d8c' if not wood else '#8f775e')
    px,py=vp
    def point(x,y):return (round(px+(x-px)*(y-py)/(206-py)),y)
    rows=([back[1],back[1]+3,back[1]+7,back[1]+12,back[1]+18,back[1]+25,back[1]+33,back[1]+42,back[1]+52,back[1]+63,206] if wood else [back[1],back[1]+4,back[1]+10,back[1]+18,back[1]+29,back[1]+43,206])
    rays=list(range(-650,1050,58 if not wood else 34))
    colors=['#99a294','#a4ac9c','#acb29f','#929e92','#b1b6a2','#a5af9c'] if not wood else ['#8c7359','#967a5e','#9f8465','#897055','#927759','#a58a68','#8f7b61']
    for row,(ya,yb) in enumerate(zip(rows,rows[1:])):
        rowrays=[x+(17 if wood and row%2 else 0) for x in rays]
        for col,(xa,xb) in enumerate(zip(rowrays,rowrays[1:])):
            pts=[point(xa,ya),point(xb,ya),point(xb,yb),point(xa,yb)]
            layer.poly(pts,colors[(col*3+row*2)%len(colors)])
            layer.line([pts[0],pts[1]],'#79867d' if not wood else '#6b5745')
            layer.line([pts[0],pts[3]],'#7c8a80' if not wood else '#6b5745')
            if row>1:
                a,b=pts[0],pts[1]
                layer.line([(a[0]+1,a[1]+1),(b[0]-1,b[1]+1)],'#c2c7af' if not wood else '#b79b77')
            if wood and row>=2:
                # Fine longitudinal wood grain follows each board's long face.
                a,b,d,e=pts;yy=round(ya+(yb-ya)*.5)
                left=round((a[0]+e[0])*.5);right=round((b[0]+d[0])*.5)
                if right-left>6:
                    layer.line([(left+2,yy),(right-3,yy)],'#887056')
                    if (col+row)%3==0:layer.line([(left+3,yy+1),(left+6,yy+1)],'#b1946d')
                if row>=5 and (row,col) in [(5,16),(7,12),(8,14),(9,15)]:
                    layer.line([(left+2,yy),(left+5,yy-1),(right-2,yy)],'#6e5d47')
    c.im.paste(layer.im,(0,0),mask)

def duct(c,x,y,w,h):
    c.box((x-2,y-1,x+w+2,y+h+3),'#414f49')
    ramp=['#53685f','#71847a','#9caa98','#ced1b7','#b8c3ac','#a1b09c','#7b9282','#5c7567','#3d594d']
    for i,color in enumerate(ramp):
        a=round(y+i*h/len(ramp));b=round(y+(i+1)*h/len(ramp));c.box((x,a,x+w,b),color)
    c.line([(x+1,y+2),(x+w-1,y+2)],'#dae0c4')
    for xx in range(x+7,x+w,22):
        c.box((xx,y-1,xx+2,y+h+1),'#657969');c.line([(xx,y),(xx,y+h)],'#c0c8ac')
        c.box((xx+2,y+3,xx+3,y+4),'#3a5446');c.box((xx+2,y+h-3,xx+3,y+h-2),'#d1d5b8')
    for xx,yy in [(x+12,y+h-3),(x+45,y+3),(x+w-21,y+h-4)]:
        if xx<x+w:c.poly([(xx,yy),(xx+4,yy-1),(xx+7,yy+1),(xx+5,yy+3),(xx+1,yy+2)],'#7e927c')

def pipe(c,pts,w=3,copper=False):
    c.line([(x+1,y+1) for x,y in pts],'#4c5043',w+2)
    c.line(pts,'#735a3f' if copper else '#536c5c',w)
    c.line([(x-1,y-1) for x,y in pts],'#c19a66' if copper else '#aeb99d',max(1,w-2))
    c.line([(x,y-1) for x,y in pts],'#e2c191' if copper else '#d2d6b9')

def sconce(c,x,y,small=False):
    r=3 if small else 4;h=7 if small else 12
    c.box((x+1,y+2,x+r+3,y+h+6),'#62593e')
    c.box((x-2,y-2,x+r+1,y+h+1),'#8c7952','#554f36')
    c.box((x-1,y,x+r,y+h),'#fff0bc');c.line([(x,y),(x,y+h)],'#fffad9')
    c.box((x-3,y-2,x+r+2,y-1),'#b89c65');c.box((x-3,y+h+1,x+r+2,y+h+2),'#ab8b57')
    c.line([(x+1,y-3),(x+1,y-5)],'#b49e65')

def flowers(c,x,y,scale=1):
    # Flowers have stems, drooping heads, shaded petals and distinct containers.
    for dx,dy in [(-7,-11),(-3,-16),(1,-13),(5,-18),(8,-9),(-9,-5),(3,-7)]:
        xx=x+round(dx*scale);yy=y+round(dy*scale)
        c.line([(x,y),(xx,yy)],'#5f7951')
        c.line([(xx,yy),(xx-2,yy+3)],'#8c9b61')
        c.ellipse((xx-2,yy-2,xx+2,yy+1),'#e9dfb8','#a6a77d')
        c.box((xx,yy-2,xx+1,yy),'#fff0cc')
        c.line([(xx-1,yy+1),(xx-2,yy+3)],'#bdb98c')
    c.poly([(x-4,y),(x+4,y),(x+3,y+7),(x+1,y+9),(x-2,y+8),(x-4,y+5)],'#a49268','#625e40')
    c.line([(x-3,y+1),(x-2,y+6)],'#d7c28c');c.line([(x+2,y+1),(x+2,y+6)],'#7c7950')

def drape(c,x,y,w,h):
    c.poly([(x,y),(x+w,y),(x+w-2,y+h),(x+w*.7,y+h-2),(x+w*.5,y+h+1),(x+w*.2,y+h-1),(x-1,y+h)],'#603c44','#443b3d')
    for pts,col in [([(x+1,y),(x+w*.3,y),(x+w*.24,y+h*.5),(x+w*.35,y+h),(x+w*.15,y+h-2)],'#914e55'),([(x+w*.38,y),(x+w*.6,y),(x+w*.53,y+h*.4),(x+w*.65,y+h-1),(x+w*.42,y+h)],'#77414b'),([(x+w*.72,y),(x+w*.87,y),(x+w*.8,y+h*.5),(x+w*.9,y+h),(x+w*.7,y+h-2)],'#a45c60')]:c.poly(pts,col)
    c.line([(x+1,y+h),(x+w*.3,y+h+1),(x+w*.6,y+h),(x+w-1,y+h-1)],'#bc986b')

