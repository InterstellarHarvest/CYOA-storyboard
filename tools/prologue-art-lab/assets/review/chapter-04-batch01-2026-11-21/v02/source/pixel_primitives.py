"""Native-grid primitives. No raster inputs, resampling, antialiasing or quantization.

All positions are authored in logical pixels. This module only makes blank
canvases and draws pixel clusters. Presentation scaling lives in package_review.py.
"""
from PIL import Image, ImageDraw

PAL = {
 'ink':'#303c3d','dark':'#414b49','shadow':'#626662','wall':'#b6b09c',
 'cream':'#d6cbb0','light':'#eee2c5','white':'#f4efda','plaster':'#a09f91',
 'teal':'#607a73','tealLight':'#809187','tealDark':'#435e59',
 'silver':'#a6b4ae','metalLight':'#d7ddd0','metalDark':'#6b7c78',
 'red':'#854d50','redLight':'#a26961','redDark':'#633e46','gold':'#a59365',
 'floor':'#92968b','tile':'#adb0a0','green':'#667b55','leaf':'#889268',
 'skin':'#ceb38d','skinLight':'#e5c69d','skinShadow':'#ac876b',
 'wood':'#78634e','woodLight':'#9e8563','woodDark':'#594b40',
}

class Canvas:
 def __init__(self,w,h,transparent=False):
  self.im=Image.new('RGBA' if transparent else 'RGB',(w,h),(0,0,0,0) if transparent else PAL['wall'])
  self.d=ImageDraw.Draw(self.im)
 def c(self,c): return PAL.get(c,c)
 def box(self,coords,fill,outline=None): self.d.rectangle(coords,fill=self.c(fill),outline=self.c(outline) if outline else None)
 def poly(self,pts,fill,outline=None): self.d.polygon(pts,fill=self.c(fill),outline=self.c(outline) if outline else None)
 def line(self,pts,fill,width=1): self.d.line(pts,fill=self.c(fill),width=width)
 def ellipse(self,coords,fill,outline=None): self.d.ellipse(coords,fill=self.c(fill),outline=self.c(outline) if outline else None)
 def save(self,p): self.im.save(p)

FONT={
 'W':['10101','10101','10101','10101','01110'],
 'C':['111','100','100','100','111'],
 'S':['111','100','111','001','111'],
 'E':['111','100','110','100','111'],
 'R':['110','101','110','101','101'],
 'V':['101','101','101','101','010'],
 'I':['111','010','010','010','111'],
 'L':['100','100','100','100','111'],
 'O':['111','101','101','101','111'],
 'T':['111','010','010','010','010'],
 'A':['010','101','111','101','101'],
 'U':['101','101','101','101','111'],
 'N':['1001','1101','1011','1001','1001'],
 '3':['111','001','111','001','111'],
 '1':['010','110','010','010','111'],
 '4':['101','101','111','001','001'],
 '5':['111','100','111','001','111'],
 ' ':['00']*5,
}
def label(c,x,y,s,color='light',scale=1):
 for ch in s:
  g=FONT[ch]
  for j,row in enumerate(g):
   for i,v in enumerate(row):
    if v=='1':c.box((x+i*scale,y+j*scale,x+(i+1)*scale-1,y+(j+1)*scale-1),color)
  x+=(len(g[0])+1)*scale

def pipe(c,pts,width=5):
 c.line(pts,'ink',width+2);c.line(pts,'metalDark',width)
 c.line([(x-1,y-1) for x,y in pts],'silver',max(1,width-2))
 c.line([(x-2,y-2) for x,y in pts],'metalLight',1)

def duct(c,x1,y1,x2,y2):
 c.box((x1,y1,x2,y2),'metalDark','ink')
 c.box((x1+1,y1+1,x2-1,y1+3),'metalLight')
 c.box((x1+1,y1+4,x2-1,y2-4),'silver')
 c.line([(x1+1,y2-2),(x2-1,y2-2)],'dark')
 for x in range(x1+7,x2,19):
  c.line([(x,y1+1),(x,y2-1)],'metalDark');c.line([(x+1,y1+1),(x+1,y2-1)],'metalLight')

def door(c,x,y,w,h,open=False):
 c.box((x-3,y-3,x+w+3,y+h+1),'shadow','ink');c.box((x-2,y-2,x+w+2,y+h),'cream')
 c.box((x,y,x+w,y+h),'ink')
 if not open:
  c.box((x+1,y+1,x+w-1,y+h-1),'tealDark');c.box((x+2,y+2,x+w-2,y+h-3),'teal')
  c.box((x+4,y+5,x+w-4,y+13),'cream');c.box((x+w-5,y+h//2,x+w-3,y+h//2+1),'metalLight')
  c.line([(x+3,y+h-9),(x+w-3,y+h-9)],'tealDark')
 else:
  c.box((x+3,y+3,x+w-3,y+h-3),'shadow');c.box((x+5,y+h-11,x+w-4,y+h-2),'floor')
  c.poly([(x,y+1),(x+6,y+5),(x+6,y+h-5),(x,y+h)],'teal','ink')

def person(c,x,y,coat='red',pose='idle',hair='metalLight'):
 """A 9–14px-wide, 27px-tall figure. Face is one cluster, no features."""
 c.ellipse((x-5,y+25,x+8,y+28),'shadow')
 c.poly([(x-2,y+17),(x+2,y+17),(x+1,y+25),(x-2,y+25)],'dark')
 c.poly([(x+3,y+17),(x+6,y+17),(x+7,y+25),(x+4,y+25)],'ink')
 c.box((x-3,y+25,x+1,y+26),'ink');c.box((x+4,y+25,x+8,y+26),'ink')
 c.poly([(x-3,y+8),(x+5,y+7),(x+7,y+18),(x-3,y+18)],coat,'ink')
 c.poly([(x,y+8),(x+3,y+8),(x+2,y+14)],'cream')
 c.box((x-1,y+2,x+4,y+7),'skin');c.poly([(x-2,y+2),(x+1,y),(x+5,y+1),(x+5,y+4),(x+3,y+3),(x-2,y+3)],hair)
 if pose=='show':
  c.line([(x+6,y+10),(x+11,y+5),(x+13,y+5)],coat,3);c.box((x+12,y+3,x+14,y+5),'skin')
  c.line([(x-3,y+11),(x-7,y+14)],coat,3);c.box((x-8,y+13,x-6,y+15),'skin')
 else:
  c.line([(x-3,y+10),(x-4,y+18)],coat,3);c.box((x-5,y+18,x-3,y+20),'skin')
  c.line([(x+6,y+10),(x+8,y+17)],coat,3);c.box((x+7,y+17,x+9,y+19),'skin')

def flowers(c,x,y,scale=1):
 c.poly([(x-4,y),(x+4,y),(x+3,y+12),(x-2,y+12)],'shadow','ink')
 c.poly([(x-3,y+1),(x+2,y+1),(x+1,y+11),(x-1,y+11)],'cream')
 for dx,dy in [(-8,-12),(-4,-19),(1,-15),(6,-21),(9,-10),(-1,-25)]:
  c.line([(x,y),(x+dx,y+dy)],'green')
  c.poly([(x+dx,y+dy+6),(x+dx-4,y+dy+4),(x+dx-2,y+dy+2)],'leaf')
  c.box((x+dx-2,y+dy,x+dx+2,y+dy+2),'cream');c.box((x+dx,y+dy-1,x+dx+2,y+dy),'white')

def cabinet(c,x,y,w,h):
 c.box((x,y,x+w,y+h),'metalDark','ink');c.line([(x+1,y+1),(x+w-1,y+1)],'silver')
 for yy in range(y+4,y+h-4,9):
  c.box((x+3,yy,x+w-3,yy+6),'tealDark','dark');c.box((x+w//2-2,yy+2,x+w//2+2,yy+3),'cream')

def chandelier(c,x,y):
 c.line([(x,y),(x,y+14)],'dark');c.ellipse((x-2,y+13,x+2,y+17),'gold')
 c.line([(x-13,y+21),(x-9,y+25),(x,y+27),(x+9,y+25),(x+13,y+21)],'gold',2)
 for dx in [-13,-7,0,7,13]:
  c.line([(x+dx,y+21),(x+dx,y+17)],'shadow');c.box((x+dx-2,y+15,x+dx+2,y+18),'cream')
  c.line([(x+dx,y+26),(x+dx,y+29)],'silver');c.box((x+dx,y+30,x+dx+1,y+32),'light')

def drape(c,x,y,w,h):
 c.box((x,y,x+w,y+h),'redDark','dark')
 for i in range(2,w,5):
  c.box((x+i,y+1,x+i+1,y+h-2),'red');c.line([(x+i+2,y+2),(x+i+2,y+h-2)],'redLight')
 c.line([(x,y+h),(x+w,y+h)],'gold')
