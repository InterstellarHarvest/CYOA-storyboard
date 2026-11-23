"""Source-derived native expression portraits; approved designs are never edited.
Opaque-only local palette fitting, protected native clusters, silhouette and material layers.
"""
from pathlib import Path
from PIL import Image,ImageDraw
from collections import Counter
import json,hashlib,platform
ROOT=Path(__file__).resolve().parents[1];SIZE=(564,278)
PROTECTED={
31:[(195,28,325,145),(190,150,280,260),(340,135,430,215)],
32:[(240,28,365,150),(210,130,280,215),(350,190,425,275)],
33:[(205,28,340,150),(205,150,300,230),(335,170,410,270)],
34:[(235,28,365,150),(235,145,335,225),(330,205,420,277)],
35:[(220,28,340,150),(215,170,330,250),(280,215,370,277)],
36:[(215,28,340,150),(220,175,335,270),(345,140,445,220)]}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(i,rel):i.save(ROOT/rel)
def quiet(im,protected):
 src=list(im.get_flattened_data());out=src[:];w,h=im.size;seen=set();changed=0
 for idx,c in enumerate(src):
  if idx in seen:continue
  todo=[idx];component=[];boundary=[];seen.add(idx)
  while todo:
   k=todo.pop();component.append(k);x,y=k%w,k//w
   for n in ([k-1]if x else[])+([k+1]if x<w-1 else[])+([k-w]if y else[])+([k+w]if y<h-1 else[]):
    if src[n]==c:
     if n not in seen:seen.add(n);todo.append(n)
    else:boundary.append(src[n])
  if len(component)>2 or not boundary or any(protected.getpixel((k%w,k//w))for k in component):continue
  target,n=Counter(boundary).most_common(1)[0]
  if n>=3 and sum((a-b)**2 for a,b in zip(c,target))<900:
   for k in component:out[k]=target
   changed+=len(component)
 im.putdata(out);return im,changed
def classify(c,y):
 r,g,b=c
 if max(c)<65:return'dark_ink'
 if max(c)-min(c)<42 and min(c)>125 and y<135:return'silver_or_light_detail'
 if r>g*1.25 and b>g*.92:return'burgundy_material'
 if r>g*1.17 and g>b*1.1:return'warm_skin_or_wood'
 if min(c)>145 and r>=b:return'ivory_material'
 return'neutral_material'
def main():
 records=[]
 for num in range(31,37):
  id_=f'CH4-B2-{num}';rel=f'originals/{id_}-cutout.png'if num==34 else f'originals/{id_}-detailed.png';src=Image.open(ROOT/rel).convert('RGBA');direct=src.resize(SIZE,Image.Resampling.NEAREST);save(direct,f'diagnostics/{id_}-direct-transfer.png');box=src.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox();crop=src.crop(box);nh=246;nw=round(crop.width*nh/crop.height);under=Image.new('RGBA',SIZE);under.paste(crop.resize((nw,nh),Image.Resampling.NEAREST),((564-nw)//2,32));alpha=under.getchannel('A').point(lambda a:255 if a>=128 else 0);ap=list(alpha.get_flattened_data());rgb=under.convert('RGB');raw=list(rgb.get_flattened_data());protected=Image.new('L',SIZE);pd=ImageDraw.Draw(protected)
  for b in PROTECTED[num]:pd.rectangle(b,fill=255)
  save(protected,f'masks/{id_}-anatomy-and-props-protected.png')
  # Fit ONLY opaque character colors. Invisible/halo RGB must not consume the
  # character's palette budget or erase silver hair, gavel and clipboard detail.
  colors=[c for c,a in zip(raw,ap)if a];strip=Image.new('RGB',(len(colors),1));strip.putdata(colors);palette=strip.quantize(colors=64,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE);fitted=rgb.quantize(palette=palette,dither=Image.Dither.NONE).convert('RGB');fitted,merged=quiet(fitted,protected)
  # Quiet only low-contrast one/two-pixel islands on warm skin/hand planes.
  # Dark brows/pupils/creases, white catchlights and coherent wrinkle lines stay
  # protected by the color gate, component length and contrast test.
  warm_protect=Image.new('L',SIZE,255)
  for y in range(50,278):
   for x in range(564):
    c=fitted.getpixel((x,y));r,g,b=c
    if protected.getpixel((x,y)) and ap[y*564+x] and r>150 and r>g*1.15 and g>b*1.10:warm_protect.putpixel((x,y),0)
  fitted,warm_merged=quiet(fitted,warm_protect)
  # Deliberate target-grid silhouette cleanup, not a white/gray matte export.
  clean=ap[:];removed=0
  for y in range(1,277):
   for x in range(1,563):
    i=y*564+x
    if ap[i]and not any(ap[k]for k in[i-1,i+1,i-564,i+564]):clean[i]=0;removed+=1
  pixels=list(fitted.get_flattened_data());out=pixels[:];edgefix=0
  def fringe(c):return c[0]>100 and(c[1]<c[0]*.53 or(c[0]>160 and c[1]>140 and c[2]<60))
  for y in range(278):
   for x in range(564):
    i=y*564+x
    if not clean[i]or not fringe(raw[i]):continue
    rim=any(not(0<=x+dx<564 and 0<=y+dy<278)or not clean[(y+dy)*564+x+dx]for dy in range(-2,3)for dx in range(-2,3))
    if not rim:continue
    near=[pixels[yy*564+xx]for yy in range(max(0,y-3),min(278,y+4))for xx in range(max(0,x-3),min(564,x+4))if clean[yy*564+xx]and not fringe(raw[yy*564+xx])]
    if near:out[i]=min(near,key=sum);edgefix+=1
  final=Image.new('RGBA',SIZE);final.putdata([c+(255,)if a else(0,0,0,0)for c,a in zip(out,clean)]);save(final,f'native/{id_}-v01.png');save(final.resize((2256,1112),Image.Resampling.NEAREST),f'previews/{id_}-4x.png');save(final,f'layers/{id_}-native-foreground.png');save(final.getchannel('A'),f'masks/{id_}-silhouette.png')
  categories=[classify(c,i//564)if clean[i]else'clear'for i,c in enumerate(out)];names=sorted(set(categories)-{'clear'})
  for name in names:
   m=Image.new('L',SIZE);m.putdata([255 if k==name and a else 0 for k,a in zip(categories,clean)]);save(m,f'masks/{id_}-{name}.png');part=final.copy();part.putalpha(m);save(part,f'layers/{id_}-{name}.png')
  records.append({'id':id_,'sourceFile':rel,'sourceSha256':sha(ROOT/rel),'sourceSilhouetteBox':list(box),'nativeComposition':{'top':32,'height':246,'width':nw,'uniformNearestTransfer':True},'method':'SOURCE-DERIVED native opaque-only coherent palette interpretation, protected cluster merging, binary silhouette and fringe cleanup with separate material layers; not independent whole-image native-grid authorship','localFitColors':64,'opaqueColorCount':len(set(c[:3]for c in final.get_flattened_data()if c[3])),'quietSurfacePixelsMerged':merged,'nativeWarmPlanePixelsMerged':warm_merged,'detachedSilhouettePixelsRemoved':removed,'boundaryFringePixelsRecolored':edgefix,'protectedRegions':PROTECTED[num],'materialMasks':names})
 (ROOT/'evidence/derivation.json').write_text(json.dumps({'python':platform.python_version(),'pillow':Image.__version__,'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'palettePolicy':'Local opaque-only64-tone fitting calibrated to approved B2-04/B2-05 portraits; not a universal cap or a visual approval test','assets':records},indent=2)+'\n');print('Six native B2-06 foregrounds and exact4x previews constructed.')
if __name__=='__main__':main()
