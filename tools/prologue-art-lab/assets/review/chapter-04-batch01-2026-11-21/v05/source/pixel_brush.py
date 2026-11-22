"""Direct native pixel-brush layers, analogous to painting on a native raster.

Coverage is authored at the target grid, with no antialiasing, supersampling,
external raster input, blur, image filtering or resampling. Translucent pigment
mixes only with this writer's already-authored native canvas. Every brush mark
has explicit shape, color, width/pressure and opacity; there is no global shading
field, noise process, palette extraction or palette reduction.
"""
from PIL import Image,ImageDraw,ImageColor
from materials import curve

class Brush:
 def __init__(self,canvas):self.c=canvas
 def _apply(self,mask,color,opacity):
  rgb=ImageColor.getrgb(color);m=mask.load();b=mask.getbbox()
  if not b:return
  for y in range(b[1],b[3]):
   for x in range(b[0],b[2]):
    if not m[x,y]:continue
    old=self.c.px[x,y]
    if len(old)==4 and old[3]==0:continue
    value=tuple(round(old[i]*(1-opacity)+rgb[i]*opacity) for i in range(3))
    self.c.px[x,y]=value+(255,) if len(old)==4 else value
 def area(self,points,color,opacity=1,curved=True):
  mask=Image.new('1',(self.c.w,self.c.h),0);d=ImageDraw.Draw(mask)
  d.polygon(curve(points) if curved else points,fill=1)
  self._apply(mask,color,opacity)
 def stroke(self,points,color,widths=(1,1,1),opacity=1):
  p=curve(points,9);mask=Image.new('1',(self.c.w,self.c.h),0);d=ImageDraw.Draw(mask)
  for i,(a,b) in enumerate(zip(p,p[1:])):
   t=i/max(1,len(p)-2)
   w=(widths[0]*(1-t*2)+widths[1]*t*2) if t<.5 else (widths[1]*(2-t*2)+widths[2]*(t*2-1))
   d.line([a,b],fill=1,width=max(1,round(w)))
  self._apply(mask,color,opacity)
 def dab(self,x,y,color,w=1,h=1,opacity=1):
  mask=Image.new('1',(self.c.w,self.c.h),0);ImageDraw.Draw(mask).ellipse((x,y,x+w-1,y+h-1),fill=1)
  self._apply(mask,color,opacity)
