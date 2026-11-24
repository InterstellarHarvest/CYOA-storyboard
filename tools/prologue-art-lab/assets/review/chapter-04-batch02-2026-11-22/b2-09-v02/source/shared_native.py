"""Native material/cluster and portrait helpers reused from owner-approved B2-03 production; source-derived, no native-only authorship claim."""
from pathlib import Path
from collections import Counter
from functools import lru_cache
from PIL import Image,ImageDraw,ImageChops
from materials import RAMP,classify,nearest
ROOT=Path(__file__).resolve().parents[1]
def save(im,rel):
 p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True);im.save(p)
def mask(size,polys):
 im=Image.new('L',size);d=ImageDraw.Draw(im)
 for p in polys:d.polygon(p,fill=255)
 return im
def quiet_clusters(im,protected=None,threshold=400):
 """Merge only tiny low-contrast islands; preserve contrast edges and props."""
 src=list(im.getdata());out=src[:];w,h=im.size;seen=set();count=0
 for index,c in enumerate(src):
  if index in seen:continue
  todo=[index];component=[];seen.add(index);boundary=[]
  while todo:
   k=todo.pop();component.append(k);x,y=k%w,k//w
   for n in ([k-1]if x else [])+([k+1]if x<w-1 else [])+([k-w]if y else [])+([k+w]if y<h-1 else []):
    if src[n]==c:
     if n not in seen:seen.add(n);todo.append(n)
    else:boundary.append(src[n])
  if len(component)>2 or not boundary:continue
  if protected and any(protected.getpixel((k%w,k//w))for k in component):continue
  target,n=Counter(boundary).most_common(1)[0]
  if n>=3 and sum((a-b)**2 for a,b in zip(c,target))<=threshold:
   for k in component:out[k]=target
   count+=len(component)
 im=im.copy();im.putdata(out);return im,count
def materialize(im):
 @lru_cache(maxsize=None)
 def fit(p):return nearest(p,RAMP[classify(p)])
 out=Image.new('RGB',im.size);out.putdata([fit(p)for p in im.getdata()]);return out
def portrait(id_):
 source=Image.open(ROOT/('originals/CH4-B2-20-detailed-v02.png'if id_=='CH4-B2-20'else f'originals/{id_}-detailed.png')).convert('RGBA');size=(564,278)
 under=source.resize(size,Image.Resampling.NEAREST);save(under,f'diagnostics/{id_}-direct-transfer.png')
 alpha=under.getchannel('A').point(lambda a:255 if a>=128 else 0)
 rgb=under.convert('RGB');rgb=rgb.quantize(colors=64,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB');rgb,pruned=quiet_clusters(rgb,threshold=500)
 # Target-grid silhouette interpretation: remove detached one-pixel fragments.
 ap=list(alpha.getdata());clean=ap[:];w,h=size;removed=0
 for y in range(1,h-1):
  for x in range(1,w-1):
   k=y*w+x
   if ap[k]and not any(ap[n]for n in [k-1,k+1,k-w,k+w]):clean[k]=0;removed+=1
 alpha.putdata(clean)
 # Remove isolated warm/red generation fringe from the actual cutout boundary
 # using adjacent opaque character colors, preserving the silhouette geometry.
 edge_recolored=0;rp=list(rgb.getdata());original=rp[:]
 def fringe(c):return c[0]>95 and c[1]<c[0]*.48 and c[2]<c[0]*.48
 for y in range(h):
  for x in range(w):
   k=y*w+x
   if not clean[k]or not fringe(original[k]):continue
   rim=any(not(0<=x+dx<w and 0<=y+dy<h)or not clean[(y+dy)*w+x+dx]for dy in range(-2,3)for dx in range(-2,3))
   if not rim:continue
   inside=[original[yy*w+xx]for yy in range(max(0,y-4),min(h,y+5))for xx in range(max(0,x-4),min(w,x+5))if clean[yy*w+xx]and not fringe(original[yy*w+xx])]
   if inside:rp[k]=min(inside,key=lambda c:sum(c));edge_recolored+=1
 rgb.putdata(rp);out=rgb.convert('RGBA');out.putalpha(alpha)
 save(alpha,f'masks/{id_}-silhouette.png');save(out,f'layers/{id_}-native-foreground.png')
 # Export independently addressable native fabric/skin/hair regions.
 for name,predicate in [('skin',lambda r,g,b:r>g*1.13 and g>b*1.1),('fabric',lambda r,g,b:max(r,g,b)-min(r,g,b)<40),('hair',lambda r,g,b:r<110 and r>g*1.05)]:
  m=Image.new('L',size);m.putdata([255 if a and predicate(*c)else 0 for c,a in zip(rgb.getdata(),clean)]);save(m,f'masks/{id_}-{name}.png');part=out.copy();part.putalpha(m);save(part,f'layers/{id_}-{name}.png')
 return out,{'method':'Source-derived stepped portrait; separate native palette/cluster and binary silhouette interpretation, editable material layers','quietSurfacePixelsMerged':pruned,'detachedSilhouettePixelsRemoved':removed,'boundaryFringePixelsRecolored':edge_recolored,'opaqueColorCount':len(set(c for c in out.getdata()if c[3]))}
