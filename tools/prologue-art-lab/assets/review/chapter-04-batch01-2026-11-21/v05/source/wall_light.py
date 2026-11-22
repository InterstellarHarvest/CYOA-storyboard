"""Restricted corrections to the lamp's wall illumination and blank plaster.
No room-wide lighting change, image filtering or source raster sampling.
"""
from pixel_brush import Brush

def illuminate_panel(c):
 # Light on an actual wall plane: a soft, weak falloff rather than nested rings.
 # Lamp housing and its cast shadow are subsequently redrawn from unchanged source.
 for y in range(64,214):
  for x in range(465,554):
   falloff=(1+((x-499)/57)**2+((y-108)/82)**2)**-1.5
   c.px[x,y]=(round(199+25*falloff),round(187+20*falloff),round(159+12*falloff))

def plaster_variation(c):
 # Shallow older repair and hand-finished plaster; broad low-contrast native marks.
 b=Brush(c)
 for p,col,a in [
  ([(136,150),(161,143),(188,148),(194,158),(178,169),(150,167),(134,161)],'#938c76',.08),
  ([(185,181),(204,174),(225,181),(229,194),(211,204),(188,198)],'#c2b89c',.09),
  ([(282,144),(304,139),(325,145),(328,162),(313,172),(290,165)],'#9b927b',.08),
  ([(254,212),(275,205),(302,209),(313,221),(306,231),(281,231),(263,224)],'#8f8873',.06)]:b.area(p,col,a)
 b.stroke([(146,161),(160,164),(177,162)],'#c7bfa3',(1,2,1),.08)
 b.stroke([(293,157),(307,161),(320,157)],'#c9bea0',(1,2,1),.07)
