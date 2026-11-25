"""Reusable native pixel/mask/font helpers, copied from frozen v01 code only.
No approved image is resized, sampled or modified by this helper extraction.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageFilter
from collections import Counter
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
RECIPES={};LETTERS=[]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def rgb(c): return tuple(bytes.fromhex(c.lstrip('#')))

RAMPS={
 'plaster':['#655442','#88715b','#a68b6c','#c1a584','#d5bd99','#e7d2ac'],
 'green':['#1f302b','#2d4038','#40554a','#566659','#748072','#9aa18a'],
 'velvet':['#3b2229','#532932','#70333d','#8d424c','#a7555a','#c07872'],
 'wood':['#292c27','#433b2d','#615039','#826446','#ab8456','#d8b67a'],
 'brass':['#302b20','#584227','#7d5c30','#a27a3e','#c29a53','#debb73','#f1d99b'],
 'steel':['#252f2d','#3a4741','#58635a','#7c8373','#abb09a','#d5d2b7','#eeead6'],
 'ivory':['#6c6c5c','#898572','#a49b83','#bdb098','#d2c4a9','#e5d8be','#f4e9d0'],
 'glass':['#465e60','#637d7c','#86a3a0','#abc6c0','#d1e2d7'],
 'black':['#151e1c','#27332c','#3a4739','#54604b','#768166'],
}

RAMPS={k:[rgb(c)for c in v]for k,v in RAMPS.items()}

FONT={
 'A':['01110','11011','11011','11111','11011','11011','11011'],
 'B':['11110','11011','11011','11110','11011','11011','11110'],
 'C':['01111','11000','11000','11000','11000','11000','01111'],
 'D':['11110','11011','11011','11011','11011','11011','11110'],
 'E':['11111','11000','11000','11110','11000','11000','11111'],
 'F':['11111','11000','11000','11110','11000','11000','11000'],
 'G':['01111','11000','11000','11011','11011','11011','01111'],
 'H':['11011','11011','11011','11111','11011','11011','11011'],
 'I':['11111','00100','00100','00100','00100','00100','11111'],
 'J':['00111','00011','00011','00011','11011','11011','01110'],
 'K':['11011','11011','11110','11100','11110','11011','11011'],
 'L':['11000','11000','11000','11000','11000','11000','11111'],
 'M':['10001','11011','10101','10101','10001','10001','10001'],
 'N':['10001','11001','11001','10101','10011','10011','10001'],
 'O':['01110','11011','11011','11011','11011','11011','01110'],
 'P':['11110','11011','11011','11110','11000','11000','11000'],
 'Q':['01110','11011','11011','11011','11111','01110','00011'],
 'R':['11110','11011','11011','11110','11100','11010','11011'],
 'S':['01111','11000','11000','01110','00011','00011','11110'],
 'T':['11111','00100','00100','00100','00100','00100','00100'],
 'U':['11011','11011','11011','11011','11011','11011','01110'],
 'V':['11011','11011','11011','11011','11011','01110','00100'],
 'W':['11011','11011','11011','11011','11111','11111','11011'],
 'X':['11011','11011','01110','00100','01110','11011','11011'],
 'Y':['11011','11011','01110','00100','00100','00100','00100'],
 'Z':['11111','00011','00110','01100','11000','11000','11111'],
 ' ':['00000']*7,
}

def text(d,box,lines,scale=2,fill='#1e271f',gap=5):
 x0,y0,x1,y1=box; h=len(lines)*7*scale+(len(lines)-1)*gap
 assert h<=y1-y0,(lines,box)
 y=y0+(y1-y0-h)//2
 for line in lines:
  w=(len(line)*6-1)*scale;assert w<=x1-x0,(line,w,box)
  x=x0+(x1-x0-w)//2
  LETTERS.append({'text':line,'box':list(box),'inkBox':[x,y,x+w,y+7*scale], 'scale':scale,'leftMargin':x-x0,'rightMargin':x1-x-w,'binaryGlyphs':True})
  for ch in line:
   for j,row in enumerate(FONT[ch]):
    for i,b in enumerate(row):
     if b=='1':d.rectangle((x+i*scale,y+j*scale,x+(i+1)*scale-1,y+(j+1)*scale-1),fill=fill)
   x+=6*scale
  y+=7*scale+gap

class Canvas:
 def __init__(self,name,size,guide):
  self.name=name;self.size=size;self.layers=[];self.records=[]
  self.guide=Image.open(guide).convert('RGB').resize(size,Image.Resampling.BOX)
  self.guide.save(ROOT/f'diagnostics/{name}-source-derived-diagnostic-NOT-production.png')
 def layer(self,name,paint):
  im=Image.new('RGBA',self.size);paint(ImageDraw.Draw(im),im);self.append(name,im)
 def append(self,name,im):
  rel=f'layers/{self.name}-{name}.png';im.save(ROOT/rel);self.layers.append(im)
  self.records.append({'file':rel,'sha256':sha(ROOT/rel),'bbox':im.getchannel('A').getbbox()})
 def material(self,name,mask,ramp,guide=None,merge=2):
  if not isinstance(mask,Image.Image):
   m=Image.new('L',self.size);ImageDraw.Draw(m).polygon(mask,fill=255);mask=m
  mask.save(ROOT/f'masks/{self.name}-{name}.png')
  guide=guide or self.guide;cols=RAMPS[ramp];cache={};pixels=[]
  for p in guide.get_flattened_data():
   if p not in cache:cache[p]=min(cols,key=lambda c:sum((x-y)**2 for x,y in zip(p,c)))
   pixels.append(cache[p])
  # Unify tiny connected material islands only; never blur across silhouettes.
  w,h=self.size;allowed=list(mask.get_flattened_data());seen=set();before=pixels[:]
  for s,c in enumerate(before):
   if not allowed[s]or s in seen:continue
   stack=[s];seen.add(s);component=[];around=[]
   while stack:
    k=stack.pop();component.append(k);x=k%w;y=k//w
    for nx,ny in[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
     if not(0<=nx<w and 0<=ny<h):continue
     n=ny*w+nx
     if not allowed[n]:continue
     if before[n]==c:
      if n not in seen:seen.add(n);stack.append(n)
     else:around.append(before[n])
   if len(component)<=merge and around:
    col=Counter(around).most_common(1)[0][0]
    for k in component:pixels[k]=col
  im=Image.new('RGB',self.size);im.putdata(pixels);im=im.convert('RGBA');im.putalpha(mask);self.append(name,im)
 def image(self):
  out=Image.new('RGBA',self.size)
  for im in self.layers:out=Image.alpha_composite(out,im)
  return out.convert('RGB')
 def save(self,file):
  im=self.image();im.save(ROOT/f'native/{file}.png');im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/f'previews/{file}-4x.png');RECIPES[self.name]=self.records;return im

def bevel(d,box,fill,light,dark,width=2):
 x,y,r,b=box;d.rectangle(box,fill=fill)
 for k in range(width):
  d.line([(x+k,b-k),(x+k,y+k),(r-k,y+k)],fill=light)
  d.line([(x+k+1,b-k),(r-k,b-k),(r-k,y+k+1)],fill=dark)
