"""Reproducible SOURCE-DERIVED native construction; no native-only authorship claim.

Detailed concepts and separately generated pixel-friendly interpretations remain
references. A target-grid transfer is diagnostic only. Native masks, quiet-surface
cluster decisions, material ramps, structural painting and letter layers create
the review exports. Existing approved artwork is never written by this script.
"""
from pathlib import Path
from collections import Counter
from PIL import Image, ImageDraw, ImageChops
from functools import lru_cache
import json, hashlib
from materials import RAMP, classify, nearest
import pixel_text

ROOT=Path(__file__).resolve().parents[1]
GUIDES={
 '12':{'floor':[(175,127),(265,125),(314,206),(118,206)],
       'protect':[[(122,43),(185,43),(209,71),(213,137),(194,165),(172,164)],[(192,94),(223,94),(232,134),(228,167),(193,167)],[(95,154),(130,149),(136,163),(165,133),(176,137),(178,175),(165,191),(133,200),(129,206),(95,206)]],
       'people':[[(193,95),(222,95),(231,135),(228,166),(194,166)]],
       'vanish':(247,126),'bands':[139,153,174,195], 'rays':[120,159,209,267,314]},
 '13':{'floor':[(110,178),(208,140),(230,151),(254,206),(49,206)],
       'protect':[[(0,53),(87,53),(99,180),(0,193)],[(118,134),(125,123),(137,124),(142,137),(147,128),(153,130),(156,149),(186,129),(187,166),(156,178),(117,181)],[(224,54),(314,36),(314,206),(240,206),(222,185)]],
       'people':[[(15,87),(40,87),(45,137),(48,183),(17,185)],[(71,89),(89,88),(92,128),(86,153),(74,153)]],
       'vanish':(208,141),'bands':[157,178,202], 'rays':[44,105,175,257]},
}
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
def scene(id_):
 key=id_[-2:];g=GUIDES[key];size=(314,206)
 source=Image.open(ROOT/f'originals/{id_}-pixel-friendly.png').convert('RGB')
 under=source.resize(size,Image.Resampling.NEAREST);save(under,f'diagnostics/{id_}-direct-transfer.png')
 protect=mask(size,g['protect']);floor=mask(size,[g['floor']]);floor=ImageChops.subtract(floor,protect)
 save(protect,f'masks/{id_}-protected-story-objects.png');save(floor,f'masks/{id_}-floor.png')
 mapped=materialize(under)
 # Surface semantics prevent warm lamp-lit plaster from being classified as
 # upholstery red, and keep floor reflections in their own material ramps.
 wall=mask(size,[[(112,0),(184,0),(190,131),(177,173),(111,177)]])if key=='13'else Image.new('L',size)
 save(wall,f'masks/{id_}-plaster.png')
 for y in range(size[1]):
  for x in range(size[0]):
   if protect.getpixel((x,y)):continue
   c=under.getpixel((x,y));r,gc,b=c
   if wall.getpixel((x,y))and r>gc and gc>b and max(c)>100:
    mapped.putpixel((x,y),nearest(c,RAMP['plaster']))
   elif floor.getpixel((x,y))and r>=gc*.9 and b<=r and max(c)-min(c)<130:
    mapped.putpixel((x,y),nearest(c,RAMP['cream']if min(c)>150 else RAMP['floor']))
 mapped,pruned=quiet_clusters(mapped,protect)
 # Small people keep clothing/head/hand grouping from the simplified source,
 # fitted separately so flesh is not mistaken for plaster/wood.
 for i,poly in enumerate(g['people']):
  pm=mask(size,[poly]);npc=under.quantize(colors=48,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
  mapped.paste(npc,(0,0),pm);layer=Image.new('RGBA',size);layer.paste(npc,(0,0),pm);save(layer,f'layers/{id_}-npc-{i}.png');save(pm,f'masks/{id_}-npc-{i}.png')
 save(mapped,f'layers/{id_}-material-underpainting.png')
 layer=Image.new('RGBA',size);d=ImageDraw.Draw(layer)
 # Author perspective grout at target grid, then clip every pass to the floor
 # excluding complete scuttle handles, furniture, boiler and human silhouettes.
 for y in g['bands']:d.line([(0,y),(313,y)],fill=RAMP['floor'][1]+(255,),width=1)
 for x in g['rays']:d.line([g['vanish'],(x,205)],fill=RAMP['floor'][1]+(255,),width=1)
 layer.putalpha(ImageChops.multiply(layer.getchannel('A'),floor))
 out=Image.alpha_composite(mapped.convert('RGBA'),layer)
 structure=Image.new('RGBA',size);sd=ImageDraw.Draw(structure)
 if key=='12':
  # Stable stair treads and rail highlights within the architecture itself.
  for y,x1,x2 in [(75,238,258),(79,237,260),(84,236,261),(90,234,262),(97,233,264),(105,232,265),(114,231,266),(123,230,268)]:
   sd.line((x1,y,x2,y),fill=RAMP['steel'][2]+(255,));sd.line((x1,y+1,x2,y+1),fill=RAMP['ink'][0]+(255,))
  sd.line([(235,70),(230,128)],fill=RAMP['steel'][4]+(255,));sd.line([(260,69),(268,128)],fill=RAMP['steel'][3]+(255,))
  # Native sign deliberately shortened to fit its real size, per legibility rule.
  sd.rectangle((240,60,258,67),fill=RAMP['cream'][3]+(255,))
  text='DOCK';width=pixel_text.measure(text,1);pixel_text.draw(structure,text,(240+(19-width)//2,61),scale=1,color='#202c2d')
  # Rebuild the practical two-lever inset's lower seam and corner hardware.
  sd.line((30,112,89,117),fill=RAMP['steel'][3]+(255,));sd.rectangle((30,111,31,113),fill=RAMP['cream'][3]+(255,))
 elif key=='13':
  # Native door-jamb planes, inset hinge shapes and the service-wall hatch.
  sd.line((103,34,103,174),fill=RAMP['steel'][4]+(255,));sd.line((106,34,106,173),fill=RAMP['ink'][0]+(255,))
  for y in [56,111,155]:
   sd.rectangle((102,y,105,y+5),fill=RAMP['steel'][1]+(255,));sd.line((102,y,105,y),fill=RAMP['steel'][4]+(255,))
  sd.line((163,85,178,87),fill=RAMP['green'][4]+(255,));sd.line((178,87,178,113),fill=RAMP['ink'][0]+(255,))
 # No structure pass can accidentally overwrite story-object upper silhouettes.
 structure.putalpha(ImageChops.subtract(structure.getchannel('A'),protect))
 out=Image.alpha_composite(out,structure).convert('RGB');save(layer,f'layers/{id_}-floor-structure.png');save(structure,f'layers/{id_}-architecture.png')
 changed=sum(a!=b for a,b in zip(mapped.getdata(),out.getdata()))
 return out,{'method':'Separate generated pixel-friendly interpretation + target-grid material/cluster/structural construction','quietSurfacePixelsMerged':pruned,'nativeStructuralPixelsChanged':changed,'protectedStoryObjects':g['protect'],'structuralPassChangesInsideProtectedMask':sum(a!=b and m>0 for a,b,m in zip(mapped.getdata(),out.getdata(),protect.getdata())),'guide':g}
def portrait(id_):
 source=Image.open(ROOT/f'originals/{id_}-detailed.png').convert('RGBA');size=(564,278)
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
 for y in range(1,h-1):
  for x in range(1,w-1):
   k=y*w+x;r,g,b=original[k];neighbors=[k-1,k+1,k-w,k+w]
   if clean[k]and r>g*1.7 and r>b*1.5 and any(not clean[n]for n in neighbors):
    inside=[original[n]for n in neighbors if clean[n]and not(original[n][0]>original[n][1]*1.7)]
    if inside:rp[k]=min(inside,key=lambda c:sum(c));edge_recolored+=1
 rgb.putdata(rp);out=rgb.convert('RGBA');out.putalpha(alpha)
 save(alpha,f'masks/{id_}-silhouette.png');save(out,f'layers/{id_}-native-foreground.png')
 # Export independently addressable native fabric/skin/hair regions.
 for name,predicate in [('skin',lambda r,g,b:r>g*1.13 and g>b*1.1),('fabric',lambda r,g,b:max(r,g,b)-min(r,g,b)<40),('hair',lambda r,g,b:r<110 and r>g*1.05)]:
  m=Image.new('L',size);m.putdata([255 if a and predicate(*c)else 0 for c,a in zip(rgb.getdata(),clean)]);save(m,f'masks/{id_}-{name}.png');part=out.copy();part.putalpha(m);save(part,f'layers/{id_}-{name}.png')
 return out,{'method':'Source-derived stepped portrait; separate native palette/cluster and binary silhouette interpretation, editable material layers','quietSurfacePixelsMerged':pruned,'detachedSilhouettePixelsRemoved':removed,'boundaryFringePixelsRecolored':edge_recolored,'opaqueColorCount':len(set(c for c in out.getdata()if c[3]))}
def closeup(id_):
 size=(564,278);source=Image.open(ROOT/f'originals/{id_}-pixel-friendly.png').convert('RGB')
 under=source.resize(size,Image.Resampling.NEAREST);save(under,f'diagnostics/{id_}-direct-transfer.png')
 # Closeups retain richer detail than scenes: source-informed128 colors, then
 # quiet-cluster reconstruction. This count is a local choice, not a rule.
 out=under.quantize(colors=128,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB');out,pruned=quiet_clusters(out,threshold=500);save(out,f'layers/{id_}-material-underpainting.png')
 layer=Image.new('RGBA',size);d=ImageDraw.Draw(layer);key=id_[-2:]
 if key=='18':
  # Three front-facing native text planes, all lettering inset from the plates.
  for text,box in [('RESTROOMS',(73,168,230,194)),('ENTIRE HOTEL',(337,168,496,194))]:
   x1,y1,x2,y2=box;tw=pixel_text.measure(text,2);pixel_text.draw(layer,text,(x1+(x2-x1-tw)//2,y1+7),scale=2,color='#303b38')
  for text,y in [('LOT NINETEEN — TWO MATCHING',220),('DECORATIVE LEVERS',238)]:
   tw=pixel_text.measure(text,2);pixel_text.draw(layer,text,((564-tw)//2,y),scale=2,color='#303b38')
  # Small physical plate edge highlights sit on existing rims; labels stay inset.
  d.line((72,167,229,167),fill='#dfd6b5',width=1);d.line((337,167,495,167),fill='#dfd6b5',width=1)
 elif key=='17':
  # Reconstruct the close boiler access hatch and valve highlights at native grid.
  d.line((119,134,177,134),fill='#b4bfb1');d.line((178,135,178,171),fill='#344b4a')
  for x,y in [(123,137),(171,137),(123,172),(171,172)]:d.rectangle((x,y,x+1,y+1),fill='#cec29e')
 elif key=='16':
  # Rebuild doorway inner-edge illumination and electrical-box corners.
  d.line((128,25,128,274),fill='#92a29a');d.line((131,25,131,274),fill='#344b4a')
  d.rectangle((147,145,155,158),outline='#303b38');d.line((149,147,153,147),fill='#b4bfb1')
 out=Image.alpha_composite(out.convert('RGBA'),layer).convert('RGB');save(layer,f'layers/{id_}-native-detail-lettering.png');save(layer.getchannel('A'),f'masks/{id_}-native-detail-lettering.png')
 return out,{'method':'Separate pixel-friendly source, native material/cluster decisions and structural/letter layer','quietSurfacePixelsMerged':pruned,'nativeDetailLayerPixels':sum(a>0 for a in layer.getchannel('A').getdata()),'lettering':{'source':'approved Tiny5 bitmap atlas','text':['RESTROOMS','ENTIRE HOTEL','LOT NINETEEN — TWO MATCHING','DECORATIVE LEVERS'],'plane':'front-facing native plates','integerGlyphScale':2}if key=='18'else None}
def main():
 reports={}
 for n in range(12,19):
  id_=f'CH4-B2-{n:02}';im,report=scene(id_)if n<14 else portrait(id_)if n<16 else closeup(id_)
  save(im,f'native/{id_}-v01.png');save(im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST),f'previews/{id_}-4x.png')
  report.update(sourceDerived=True,independentlyAuthoredAtNativeResolution=False,nativeSize=list(im.size),nativeColors=len(im.getcolors(im.width*im.height)),pillowVersion=Image.__version__)
  reports[id_]=report
 (ROOT/'evidence/native-reconstruction.json').write_text(json.dumps(reports,indent=2)+'\n');print('Constructed seven UNSELECTED native candidates with separate layers and provenance.')
if __name__=='__main__':main()
