"""Native-resolution surface painting. No raster input, supersampling or resizing.

Geometric masks are rasterized directly on the contracted canvas. Each covered
logical pixel receives a material/light decision. Light ramps use grouped levels
locally; there is no global palette-count quota and no source-image sampling.
"""
import math
from PIL import Image,ImageDraw,ImageColor

def clamp(v,a=0,b=1):return max(a,min(b,v))
def g(x,y,cx,cy,rx,ry):return math.exp(-((x-cx)/rx)**2-((y-cy)/ry)**2)
def norm(v):
 d=math.sqrt(sum(x*x for x in v));return tuple(x/d for x in v)
KEY=norm((-.50,-.67,.78))

def curve(points,steps=7):
 """Cubic contour evaluated into integer native coordinates, no raster scaling."""
 out=[];p=[points[0]]+list(points)+[points[-1]]
 for i in range(1,len(p)-2):
  a,b,c,d=p[i-1:i+3]
  for k in range(steps):
   t=k/steps;t2=t*t;t3=t2*t
   out.append(tuple(round(.5*((2*b[j])+(-a[j]+c[j])*t+(2*a[j]-5*b[j]+4*c[j]-d[j])*t2+(-a[j]+3*b[j]-3*c[j]+d[j])*t3)) for j in [0,1]))
 out.append(points[-1]);return out

class Canvas:
 def __init__(self,w,h,transparent=False,mode='scene'):
  self.w,self.h=w,h;self.mode=mode;self.material='wall';self.form=None
  self.im=Image.new('RGBA' if transparent else 'RGB',(w,h),(0,0,0,0) if transparent else '#716f63')
  self.d=ImageDraw.Draw(self.im);self.px=self.im.load();self.clip=None
 def surface(self,material,form=None):self.material=material;self.form=form
 def _light(self,x,y,base):
  mat=self.material;f=self.form
  if mat in ['ink','emissive']:return base
  if self.mode=='portrait':
   if mat in ['skin','hair','velvet','satin','shirt','wood']:
    # Geometry-specific volumes are ellipsoidal height fields, evaluated here.
    components=f or []
    dx=dy=0;z=0
    for cx,cy,rx,ry,h in components:
     v=h*g(x,y,cx,cy,rx,ry);z+=v
     dx+=-2*(x-cx)/(rx*rx)*v;dy+=-2*(y-cy)/(ry*ry)*v
    nx,ny,nz=norm((-dx,-dy,1))
    lam=clamp(nx*KEY[0]+ny*KEY[1]+nz*KEY[2])
    light=.43+.68*lam
    warm=.06+.09*lam
    if mat=='skin':
     # Cool soft return under cheeks, warm key on nose/forehead.
     light=.58+.54*lam-.07*g(x,y,287,56,11,5)-.08*g(x,y,301,76,9,3)
     light+=.06*g(x,y,273,37,14,8)
     spec=.055*lam**14
    elif mat=='velvet':
     light=.33+.68*lam
     # Broad velvet nap varies with actual sleeve/chest folds.
     light+=.045*math.sin(x*.08+y*.038)
     spec=.025*lam**4
    elif mat=='satin':
     light=.35+.60*lam;spec=.30*lam**28
     spec+=.10*g(x,y,222,154,5,18)+.12*g(x,y,288,177,3,23)
    elif mat=='hair':light=.35+.72*lam;spec=.12*lam**8
    elif mat=='shirt':light=.55+.5*lam;spec=.025*lam**8
    else:light=.41+.68*lam;spec=.08*lam**14
    light=round(light*48)/48
    rgb=[base[0]*light+255*spec,base[1]*light+242*spec,base[2]*light+216*spec]
    return tuple(int(clamp(v,0,255)) for v in rgb)
   return base
  close=self.mode=='close';sx=564/314 if close else 1;sy=278/206 if close else 1
  if close and mat=='wall':
   # Architectural planes use coherent painted ramps, not contour-map gradients.
   factor=.90 if x<105 else .84 if x<331 else .95 if x<443 else .97 if x<457 else 1.01
   return tuple(int(clamp(v*factor,0,255)) for v in base)
  xx,yy=(x/sx,y/sy) if close else (x,y)
  if close:
   # Close camera: warm lamp right, ambient from ballroom left, curtain shadow.
   key=.33*g(x,y,490,102,125,137)+.19*g(x,y,70,65,160,180)
   light=.71+key-.13*g(x,y,316,120,35,120)-.13*g(x,y,229,140,90,22)
   warm=.18*g(x,y,490,102,135,160)
  else:
   key=.27*g(x,y,173,38,68,69)+.28*g(x,y,144,104,24,32)+.26*g(x,y,233,104,24,32)
   daylight=.22*g(x,y,30,73,100,140)
   light=.63+key+daylight
   warm=.13*g(x,y,173,64,71,79)+.20*g(x,y,144,105,24,32)+.20*g(x,y,233,105,24,32)
  if mat=='wall':
   # Broad plaster discoloration and material mottling, not random dither.
   # Weathering follows panel edges and lower-wall damp, with subdued variation.
   # Avoid periodic, all-over blotches that would compete with the light hierarchy.
   mott=.006*math.sin(x*.051+math.sin(y*.037)*.7)
   if close:mott-=.025*g(x,y,430,231,180,28)+.018*g(x,y,334,130,12,90)
   light+=mott
   if not close:
    light-=.15*g(x,y,168,77,85,5)+.11*g(x,y,258,94,4,66)
   else:light-=.11*g(x,y,385,47,180,9)
  elif mat=='ceiling':light*=.83;light+=.11*g(x,y,173,25,45,25)
  elif mat=='floor':
   light=.60+.24*g(x,y,28,183,100,64)+.13*g(x,y,183,165,75,30)
   light-=.15*g(x,y,184,150,120,5)
   # Worn slabs are illustrated in room_detail.py; no periodic texture field.
   warm=.09*g(x,y,177,163,41,11)+.1*g(x,y,231,157,16,6)
  elif mat=='carpet':
   light=.58+.18*g(x,y,181,163,70,60)+.10*g(x,y,124,196,24,7)
   light+=.05*g(x,y,189,188,32,10)+.025*math.sin(x*.14+y*.23)
   warm=.07
  elif mat=='metal':
   center,radius=(17,26) if close else (61.5,11)
   if f: center,radius=f
   v=clamp((y-center)/radius,-.99,.99)
   light=.40+.50*math.sqrt(1-v*v)-.27*v
   # A narrow reflection broken by broad tarnished patches.
   light+=.18*math.exp(-((v+.40)/.16)**2)
   light-=.12*g(x,y,397 if close else 159,center+radius*.3,31 if close else 11,radius*.8)
   light-=.08*g(x,y,503 if close else 218,center-radius*.1,21 if close else 10,radius)
   warm=.06*g(x,y,480 if close else 173,center,120 if close else 45,radius*2)
  elif mat=='drape':
   # v05 cloth volumes and folds are authored as interlocking color clusters.
   light=.80+(.10*g(x,y,490,102,180,200) if close else .12*g(x,y,173,32,70,40))
   warm=.06
  elif mat=='wood':
   light*=.93
   # Grain is illustrated explicitly in v05; no periodic grain function.
   warm+=.09
   if close:light+=.08*g(x,y,95,238,115,22)
  elif mat=='glass':light+=.17;warm=.04
  elif mat=='door':
   light*=.91
   light+=.08*g(x,y,164 if x<190 else 208,110,18,31)
  elif mat=='corridor':light*=.65;warm*=.25
  elif mat=='flower':
   nearest=min([4,134,238,309],key=lambda a:abs(x-a))
   light+=.12*math.cos((x-nearest)*.42)-.06*(y%15)/15
  elif mat=='npc':light=max(.72,min(1.03,light));warm*=.4
  # Local light decisions are grouped in native clusters, never filtered.
  grouping=40
  light=round(light*grouping)/grouping;warm=round(warm*32)/32
  rgb=(base[0]*light*(1+warm*.32),base[1]*light*(1+warm*.07),base[2]*light*(1-warm*.20))
  return tuple(int(clamp(v,0,255)) for v in rgb)
 def _paint(self,shape,coords,fill,outline=None,width=1):
  # Native masks are authored geometry, not external image inputs.
  mask=Image.new('1',(self.w,self.h),0);d=ImageDraw.Draw(mask)
  if shape=='poly':d.polygon(coords,fill=1)
  elif shape=='box':d.rectangle(coords,fill=1)
  elif shape=='ellipse':d.ellipse(coords,fill=1)
  else:d.line(coords,fill=1,width=width)
  bbox=mask.getbbox()
  if not bbox:return
  m=mask.load();base=ImageColor.getrgb(fill)
  for y in range(bbox[1],bbox[3]):
   for x in range(bbox[0],bbox[2]):
    if m[x,y] and (self.clip is None or self.clip[x,y]):
     rgb=self._light(x,y,base)
     self.px[x,y]=rgb+(255,) if self.im.mode=='RGBA' else rgb
  if outline:
   if shape=='poly':self.line(list(coords)+[coords[0]],outline)
   elif shape=='box':
    a,b,c,e=coords;self.line([(a,b),(c,b),(c,e),(a,e),(a,b)],outline)
   elif shape=='ellipse':
    # Only the authored native contour is stroked, with no antialiasing.
    x1,y1,x2,y2=coords;pts=[(round((x1+x2)/2+(x2-x1)/2*math.cos(i*math.pi/32)),round((y1+y2)/2+(y2-y1)/2*math.sin(i*math.pi/32))) for i in range(65)]
    self.line(pts,outline)
 def poly(self,p,fill,outline=None):self._paint('poly',p,fill,outline)
 def box(self,p,fill,outline=None):self._paint('box',p,fill,outline)
 def ellipse(self,p,fill,outline=None):self._paint('ellipse',p,fill,outline)
 def line(self,p,fill,width=1):self._paint('line',p,fill,width=width)
 def contour(self,p,fill,outline=None):self.poly(curve(p),fill,outline)
 def clip_polygon(self,points):
  mask=Image.new('1',(self.w,self.h),0);ImageDraw.Draw(mask).polygon(points,fill=1);self._clip_mask=mask;self.clip=mask.load()
 def clear_clip(self):self.clip=None
 def save(self,p):self.im.save(p)
