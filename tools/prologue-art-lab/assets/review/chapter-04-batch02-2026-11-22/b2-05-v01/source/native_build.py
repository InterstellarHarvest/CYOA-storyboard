"""Source-derived native portrait interpretation, never independent whole-image authorship.
Reuses approved B2-04 cluster/silhouette principles; adds shared bride palette and explicit material ramps.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
from collections import Counter
from functools import lru_cache
import hashlib,json,platform
ROOT=Path(__file__).resolve().parents[1];SIZE=(564,278)
OBJECT_RAMPS={'ribbon':[(51,79,95),(78,115,136),(116,164,184),(157,200,214),(204,229,230)],'silver':[(55,63,73),(100,116,127),(153,171,181),(205,219,221),(238,240,230)]}
MATERIALS=['skin','ivory','hair','gray','plum','redpaper','ribbon','silver']
def save(im,path):im.save(ROOT/path)
def maskbox(boxes):
 m=Image.new('L',SIZE);d=ImageDraw.Draw(m)
 for b in boxes:d.rectangle(b,fill=255)
 return m
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def quiet(im,protect):
 src=list(im.get_flattened_data());out=src[:];seen=set();w,h=im.size;changed=0
 for i,c in enumerate(src):
  if i in seen:continue
  todo=[i];part=[];boundary=[];seen.add(i)
  while todo:
   q=todo.pop();part.append(q);x=q%w;y=q//w
   for n in ([q-1]if x else[])+([q+1]if x<w-1 else[])+([q-w]if y else[])+([q+w]if y<h-1 else[]):
    if src[n]==c:
     if n not in seen:seen.add(n);todo.append(n)
    else:boundary.append(src[n])
  if len(part)>2 or not boundary or any(protect.getpixel((q%w,q//w))for q in part):continue
  target,n=Counter(boundary).most_common(1)[0]
  if n>=3 and sum((a-b)**2 for a,b in zip(c,target))<900:
   for q in part:out[q]=target
   changed+=len(part)
 im.putdata(out);return im,changed
# Native coordinate regions protect face, gesture hands and the one received ring.
BOXES={
 'CH4-B2-26':[(244,30,318,116),(202,221,279,267),(352,117,429,169)],
 'CH4-B2-27':[(252,26,331,118),(255,150,293,207),(285,205,343,248)],
 'CH4-B2-28':[(242,29,317,117),(225,173,299,218),(332,166,397,210)],
 'CH4-B2-29':[(246,29,320,118),(265,221,335,257)],
 'CH4-B2-30':[(239,26,320,118),(194,218,274,254),(341,142,411,189)]}
def main():
 records=[]
 for num in range(26,31):
  id_=f'CH4-B2-{num}';src=Image.open(ROOT/f'originals/{id_}-detailed.png').convert('RGBA');under=src.resize(SIZE,Image.Resampling.NEAREST);save(under,f'diagnostics/{id_}-direct-transfer.png');box=src.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox();crop=src.crop(box);nh=246;nw=round(crop.width*nh/crop.height);under=Image.new('RGBA',SIZE);under.paste(crop.resize((nw,nh),Image.Resampling.NEAREST),((564-nw)//2,32));alpha=under.getchannel('A').point(lambda a:255 if a>=128 else 0);ap=list(alpha.get_flattened_data());rgb=under.convert('RGB');data=list(rgb.get_flattened_data());palettefit=rgb.quantize(colors=64,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB');fitted=list(palettefit.get_flattened_data());native=[];classes=[]
  # A local 64-tone fit follows the approved B2-04 portrait method. Preserve
  # original material colors; broad RGB heuristics must not recolor facial
  # anatomy, stipple skin or turn the red ticket pad brown.
  for i,(r,g,b)in enumerate(data):
   x=i%564;y=i//564
   if not ap[i]:classes.append('clear');native.append((0,0,0));continue
   if num==29 and 260<x<340 and 210<y<260 and b>r*1.07 and g>r*1.05:kind='ribbon'
   elif num==29 and 260<x<340 and 215<y<260 and max(r,g,b)-min(r,g,b)<34 and min(r,g,b)>65:kind='silver'
   elif num==27 and 250<x<355 and 195<y<240 and r>g*1.4 and g>b*.9:kind='redpaper'
   elif num==27 and 270<x<315 and 110<y<174 and r>g*1.12 and b>g*1.05:kind='plum'
   elif r>g*1.23 and g>b*1.10:kind='hair'if max(r,g,b)<150 else'skin'
   elif num!=27:kind='ivory'if max(r,g,b)>92 else'hair'
   else:kind='ivory'if max(r,g,b)>170 and r>=b else'gray'
   classes.append(kind);native.append(min(OBJECT_RAMPS[kind],key=lambda c:sum((a-b)**2 for a,b in zip(c,(r,g,b)))) if num==29 and kind in OBJECT_RAMPS else fitted[i])
  out=Image.new('RGB',SIZE);out.putdata(native);protect=maskbox(BOXES[id_]);save(protect,f'masks/{id_}-anatomy-and-props-protected.png');out,merged=quiet(out,protect)
  # Binary silhouette reconstruction; remove detached 1px fragments only.
  clean=ap[:];removed=0
  for y in range(1,277):
   for x in range(1,563):
    q=y*564+x
    if ap[q]and not any(ap[n]for n in[q-1,q+1,q-564,q+564]):clean[q]=0;removed+=1
  # Native border repair removes red/yellow generated alpha fringe using adjacent
  # genuine material colors, without moving silhouette or repainting anatomy.
  raw=list(out.get_flattened_data());repaired=raw[:];edgefix=0
  def warmfringe(c):return c[0]>100 and (c[1]<c[0]*.53 or(c[0]>160 and c[1]>140 and c[2]<60))
  for y in range(278):
   for x in range(564):
    q=y*564+x
    if not clean[q]or not warmfringe(data[q]):continue
    if not any(not(0<=x+dx<564 and 0<=y+dy<278)or not clean[(y+dy)*564+x+dx]for dy in range(-2,3)for dx in range(-2,3)):continue
    near=[raw[yy*564+xx]for yy in range(max(0,y-3),min(278,y+4))for xx in range(max(0,x-3),min(564,x+4))if clean[yy*564+xx]and not warmfringe(data[yy*564+xx])]
    if near:repaired[q]=min(near,key=sum);edgefix+=1
  out.putdata(repaired);alpha.putdata(clean);out=out.convert('RGBA');out.putalpha(alpha);pixels=list(out.get_flattened_data());out.putdata([c if c[3]else(0,0,0,0)for c in pixels]);save(alpha,f'masks/{id_}-silhouette.png');save(out,f'layers/{id_}-native-foreground.png')
  for name in MATERIALS:
   m=Image.new('L',SIZE);m.putdata([255 if k==name and a else 0 for k,a in zip(classes,clean)])
   if m.getbbox():save(m,f'masks/{id_}-{name}.png');part=out.copy();part.putalpha(m);save(part,f'layers/{id_}-{name}.png')
  save(out,f'native/{id_}-v01.png');save(out.resize((2256,1112),Image.Resampling.NEAREST),f'previews/{id_}-4x.png')
  records.append({'id':id_,'method':'SOURCE-DERIVED portrait interpretation using local coherent palette fitting, protected native anatomy/prop regions, quiet-cluster and binary-silhouette construction, native edge repair and separate editable material layers; not direct resizing alone and no independent authorship claim','sourceSha256':sha(ROOT/f'originals/{id_}-detailed.png'),'opaqueColorCount':len(set(c[:3]for c in out.get_flattened_data()if c[3])),'nativePalette':sorted(set(c[:3]for c in out.get_flattened_data()if c[3])),'quietSurfacePixelsMerged':merged,'detachedAlphaPixelsRemoved':removed,'nativeBoundaryFringePixelsRecolored':edgefix,'composition':{'sourceSilhouetteBox':list(box),'nativeSilhouetteHeight':246,'nativeTop':32,'uniformNearestTransfer':True},'protectedNativeRegions':BOXES[id_],'materialMasks':[name for name in MATERIALS if(ROOT/f'masks/{id_}-{name}.png').exists()]})
 (ROOT/'evidence/derivation.json').write_text(json.dumps({'pillow':Image.__version__,'python':platform.python_version(),'nativeSize':list(SIZE),'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'palettePolicy':'Local 64-tone source fit calibrated to approved B2-04 portraits, with separate native blue-ribbon/silver-band ramps to protect rare story materials; no universal cap','rareObjectRamps':OBJECT_RAMPS,'assets':records},indent=2)+'\n');print('Five native foregrounds and exact4x previews constructed.')
if __name__=='__main__':main()
