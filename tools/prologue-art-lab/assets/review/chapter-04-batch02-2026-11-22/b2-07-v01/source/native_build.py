"""Source-derived B2-07 native illustration. No approved/canonical art is edited.
Separate detailed/pixel-friendly references, semantic ramps, protected story
objects, native structural/lettering/occluder layers and bounded state objects.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,subprocess,sys
from shared_native import mask,quiet_clusters
from materials import nearest
import block_letters,pixel_text
ROOT=Path(__file__).resolve().parents[1]
RAMPS={
 'ceramic':['#554c3d','#86745a','#b39872','#d7bc91','#eed5a8','#fff0c9'],
 'cardboard':['#352e24','#60492e','#866038','#a57947','#bc8e58','#d6ad76','#edca91'],
 'tile':['#142d2b','#24403c','#35564f','#4a6a60','#6b8170','#97a084','#b8b093'],
 'plaster':['#625447','#8b765c','#b49a76','#d0b58d','#e5cea2','#f3e0b7'],
 'floor':['#373c39','#52564d','#6d6d5d','#8d8570','#b2a087','#d0b994'],
 'metal':['#283c39','#3f554e','#60756a','#869487','#b0b7a2','#dfd4ad']}
RAMPS={k:[tuple(bytes.fromhex(c[1:]))for c in v]for k,v in RAMPS.items()}
def save(im,rel):im.save(ROOT/rel)
def apply(base,layer):return Image.alpha_composite(base.convert('RGBA'),layer).convert('RGB')
def changed(a,b):return sum(x!=y for x,y in zip(a.get_flattened_data(),b.get_flattened_data()))
def fit_region(out,under,region,ramp,predicate):
 for y in range(out.height):
  for x in range(out.width):
   c=under.getpixel((x,y))
   if region.getpixel((x,y))and predicate(*c):out.putpixel((x,y),nearest(c,RAMPS[ramp]))
def paper(quad,size):
 # Complete canonical copy, bitmap letters, >10px clean inner margin before
 # projection; no letter is allowed into the tag's worn edge or ribbon.
 im=Image.new('RGBA',(96,70),'#e9cf98');d=ImageDraw.Draw(im)
 d.rectangle((2,2,93,67),outline='#aa8551');d.line((6,66,14,66),fill='#c3a16b')
 lines=['LOT 58','STAFF TOILET','SOLD','COLLECTION AFTER','CEREMONY','DO NOT TEST']
 for i,t in enumerate(lines):
  sc=2 if i in[0,2]else 1;w=block_letters.measure(t,sc)
  block_letters.draw(im,t,((96-w)//2,[5,18,27,41,49,57][i]),scale=sc,color='#57392b'if i!=2 else'#7d302d')
 return pixel_text.project(im,quad,size=size)
def carton(layer,box,side=8,main=False):
 x,y,w,h=box;d=ImageDraw.Draw(layer);r=RAMPS['cardboard'];drop=3 if main else 5
 d.polygon([(x,y),(x+w,y),(x+w+side,y-drop),(x+side,y-drop)],fill=r[5],outline=r[1])
 d.rectangle((x,y,x+w,y+h),fill=r[3],outline=r[1])
 d.polygon([(x+w,y),(x+w+side,y-drop),(x+w+side,y+h-drop),(x+w,y+h)],fill=r[2],outline=r[1])
 d.line((x+1,y+1,x+w-1,y+1),fill=r[6]);d.rectangle((x+w//2-2,y,x+w//2+2,y+4),fill=r[5])
 # Purposeful folded edges and crush damage, not random surface noise.
 d.line([(x+1,y+h-5),(x+4,y+h-2),(x+11,y+h-1)],fill=r[4]);d.line((x+w-2,y+7,x+w-2,y+13),fill=r[2])
 for i,t in enumerate(['WEDDING','FAVORS']):
  sc=1 if main else 2;tw=block_letters.measure(t,sc)
  block_letters.draw(layer,t,(x+(w-tw)//2,y+(h-(11 if main else 22))//2+i*(6 if main else 12)),scale=sc,color=r[0])
def environment(num):
 id_=f'CH4-B2-{num}';main=num==37;size=(314,206)if main else(564,278)
 src=Image.open(ROOT/f'originals/{id_}-pixel-friendly.png').convert('RGB');under=src.resize(size,Image.Resampling.NEAREST);save(under,f'diagnostics/{id_}-direct-transfer.png')
 if main:
  props=[[(123,87),(172,87),(172,152),(164,179),(133,180),(123,170)],[(152,37),(199,36),(213,69),(213,179),(178,183),(174,153),(165,93),(152,85)],[(55,47),(126,47),(125,195),(55,197)],[(210,56),(286,56),(286,198),(211,198)]]
  floorpoly=[[(111,165),(215,165),(286,205),(32,205)]]
  ceramics=[[(125,91),(171,91),(169,179),(134,179),(125,170)]]
  cardboard=[[(56,47),(126,47),(125,196),(56,196)],[(210,56),(285,56),(285,197),(210,197)]]
 else:
  props=[[(86,88),(185,87),(201,103),(199,162),(256,187),(252,242),(226,277),(130,277),(102,252),(101,203),(116,183),(90,180)],[(17,94),(84,94),(91,278),(16,278)],[(428,91),(540,88),(540,278),(427,278)]]
  floorpoly=[[(249,214),(428,214),(509,278),(207,278)]]
  ceramics=[[(87,102),(198,99),(200,165),(256,185),(256,234),(231,277),(130,277),(112,245),(111,203),(118,183),(92,181)]]
  cardboard=[[(18,91),(84,91),(90,278),(18,278)],[(428,89),(540,89),(540,278),(428,278)]]
 protect=mask(size,props);floor=ImageChops.subtract(mask(size,floorpoly),protect);ceramic=mask(size,ceramics);cartons=mask(size,cardboard)
 save(protect,f'masks/{id_}-complete-story-objects.png');save(floor,f'masks/{id_}-floor.png');save(ceramic,f'masks/{id_}-ceramic.png');save(cartons,f'masks/{id_}-cardboard.png')
 # Local base palette preserves richer portrait-camera detail. Semantic ramps
 # are fitted separately, so scarce ribbon/card/skin colors are never lost.
 out=under.quantize(colors=96 if main else 128,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
 fit_region(out,under,ceramic,'ceramic',lambda r,g,b:r>g and g>b and r>110)
 fit_region(out,under,cartons,'cardboard',lambda r,g,b:r>g*1.16 and g>b*1.12 and r>65)
 fit_region(out,under,floor,'floor',lambda r,g,b:max(r,g,b)-min(r,g,b)<110)
 tilemask=Image.new('L',size);plastermask=Image.new('L',size)
 architecture=mask(size,[[(17,0),(86,0),(86,85),(17,85)],[(43,0),(149,0),(149,41),(43,41)],[(104,0),(267,0),(267,36),(104,36)],[(265,22),(287,22),(287,70),(265,70)],[(210,35),(257,35),(257,56),(210,56)]]if main else[[(27,0),(151,0),(151,99),(27,99)],[(143,0),(241,0),(241,99),(143,99)],[(235,0),(508,0),(508,49),(235,49)],[(388,46),(455,46),(455,86),(388,86)],[(493,0),(536,0),(536,97),(493,97)]])
 for y in range(size[1]):
  for x in range(size[0]):
   if protect.getpixel((x,y))or architecture.getpixel((x,y)):continue
   r,g,b=under.getpixel((x,y))
   if g>r*1.03 and g>b*.95:tilemask.putpixel((x,y),255)
   elif (y<69 if main else y<99)and r>g and g>b and r>105:plastermask.putpixel((x,y),255)
 fit_region(out,under,tilemask,'tile',lambda r,g,b:True)
 fit_region(out,under,plastermask,'plaster',lambda r,g,b:True)
 save(tilemask,f'masks/{id_}-tile-and-duct.png');save(plastermask,f'masks/{id_}-plaster.png')
 # Explicit rare story-color ramp overrides ceramic fitting. The red SOLD
 # ribbon must stay red; a broad ceramic material mask may never erase it.
 ribbon=Image.new('L',size);red=[(67,25,23),(105,34,28),(148,47,33),(190,66,40),(223,103,62)]
 for y in range(size[1]):
  for x in range(size[0]):
   r,g,b=under.getpixel((x,y))
   if ceramic.getpixel((x,y))and r>g*1.65 and r>b*1.5:
    ribbon.putpixel((x,y),255);out.putpixel((x,y),nearest((r,g,b),red))
 save(ribbon,f'masks/{id_}-red-story-ribbon.png');save(architecture,f'masks/{id_}-architectural-material-protection.png')
 out,pruned=quiet_clusters(out,protect,threshold=500);save(out,f'layers/{id_}-material-underpainting.png');before=out.copy()
 structure=Image.new('RGBA',size);d=ImageDraw.Draw(structure)
 # Native perspective tile joints follow the reference's doorway sightline.
 if main:
  for y in[174,185,201]:d.line((30,y,286,y),fill='#454b45')
  for x in[109,153,219,287]:d.line([(153,88),(x,205)],fill='#454b45')
 else:
  for a,b in[((251,231),(446,231)),((236,253),(478,253))]:d.line((*a,*b),fill='#444b45')
  for x in[245,328,415,511]:d.line([(326,165),(x,277)],fill='#444b45')
 structure.putalpha(ImageChops.multiply(structure.getchannel('A'),floor));out=apply(out,structure);save(structure,f'layers/{id_}-native-floor-joints.png')
 detail=Image.new('RGBA',size);d=ImageDraw.Draw(detail)
 if main:
  # Exact target-grid joints, screws, louver vanes and flush-lever highlights.
  for x in[142,192]:
   d.line((x,12,x,31),fill='#a6aa86');d.point((x,14),fill='#efd098');d.point((x,29),fill='#efd098')
  for y in[24,26,28]:d.line((172,y,186,y),fill='#b8b093')
  d.line((160,102,167,101),fill='#f0dfb5');d.point((160,103),fill='#52605a')
  for y in[39,65,82]:d.line((144,y,147,y),fill='#edbd7b')
  # Cards are preserved as coherent cream polygons, not speckled faces.
  d.line((136,91,145,91),fill='#fff0c9');d.line((150,91,157,91),fill='#fff0c9')
 else:
  for y in[57,62,67,72]:d.line((395,y,444,y),fill='#c7b58d')
  for y in[106,156]:d.line((228,y,236,y),fill='#e7b568');d.point((232,y+1),fill='#fff0c9')
  d.line((184,126,197,123),fill='#f1e0bb');d.point((184,128),fill='#52605a')
  d.line((112,110,130,107),fill='#fff0c9');d.line((138,107,153,104),fill='#fff0c9')
 out=apply(out,detail);save(detail,f'layers/{id_}-native-material-details.png')
 if not main:
  # Rebuild the source tag as a larger hanging paper plane. This retains
  # complete readable copy at native size rather than tiny crushed lettering.
  cleanpaper=Image.new('RGBA',size);cd=ImageDraw.Draw(cleanpaper)
  cd.polygon([(144,193),(234,178),(251,216),(163,226)],fill='#e5c99b')
  cd.polygon([(141,192),(239,187),(247,267),(148,275)],fill='#8d7757')
  out=apply(out,cleanpaper);save(cleanpaper,f'layers/{id_}-native-paper-construction.png')
  letters=paper([(138,190),(236,185),(244,264),(145,272)],size)
  # Wider than the apparent rectangle via perspective; all copy kept inside.
  out=apply(out,letters);save(letters,f'layers/{id_}-native-auction-tag-lettering.png')
 # All final closed-state detail survives; blocked entry is a separate native
 # occluder. Do not mistake intended box occlusion for loss during rendering.
 cleared=out.copy();occluder=Image.new('RGBA',size)
 if main:
  for box in[(124,154,40,26),(126,128,38,25),(127,108,37,19)]:carton(occluder,box,side=7,main=True)
 else:
  for box in[(124,225,103,52),(128,177,100,47),(139,146,84,30)]:carton(occluder,box,side=17)
 blocked=apply(cleared,occluder);save(occluder,f'layers/{id_}-entry-box-occluder.png');save(occluder.getchannel('A'),f'masks/{id_}-entry-box-occluder.png')
 # Source-derived permitted-state object guide is confined to the WC. All
 # architecture, source NPC, cartons and floor outside this region stay exact.
 state=Image.open(ROOT/f'originals/{id_}-permit-reference.png').convert('RGB').resize(size,Image.Resampling.NEAREST)
 state=state.quantize(colors=64 if main else 96,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB');state,_=quiet_clusters(state,threshold=500)
 allowed=mask(size,[[(126,102),(163,102),(169,123),(170,151),(163,157),(128,157)]]if main else[[(115,104),(198,104),(204,163),(242,168),(260,198),(257,235),(245,263),(247,277),(132,277),(132,246),(118,228)]])
 patch=state.convert('RGBA');patch.putalpha(allowed);permit=apply(cleared,patch);save(patch,f'layers/{id_}-permit-toilet-object.png');save(allowed,f'masks/{id_}-permit-toilet-allowed.png')
 report={'nativeSize':list(size),'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'localBasePalette':96 if main else 128,'quietSurfacePixelsMerged':pruned,'nativeStructuralPixels':sum(a>0 for a in structure.getchannel('A').get_flattened_data()),'floorStructureChangesInsideStoryProtection':sum(a!=b and m>0 for a,b,m in zip(before.get_flattened_data(),apply(before,structure).get_flattened_data(),protect.get_flattened_data())),'entryOcclusionPixels':changed(cleared,blocked),'permitChanges':changed(cleared,permit),'permitOutsideAllowedChanges':sum(a!=b and not m for a,b,m in zip(cleared.get_flattened_data(),permit.get_flattened_data(),allowed.get_flattened_data())),'method':'Separate generated pixel-friendly interpretation, native semantic material ramps, protected clusters, native floor/pipe/duct/card detail, bitmap lettering, separate native cardboard occlusion and bounded source-informed WC object state'}
 return {id_:blocked,id_+'-cleared':cleared,id_+'-permit':permit},report
def main():
 subprocess.run([sys.executable,str(ROOT/'source/portrait_native.py')],check=True)
 reports={};ims={}
 for n in[37,41]:
  new,r=environment(n);ims.update(new);reports[f'CH4-B2-{n}']=r
 for id_,im in ims.items():
  save(im,f'native/{id_}-v01.png');save(im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST),f'previews/{id_}-4x.png')
 (ROOT/'evidence/environment-derivation.json').write_text(json.dumps(reports,indent=2)+'\n')
 print('Five primary B2-07 native images; four conditional state references. All UNSELECTED.')
if __name__=='__main__':main()
