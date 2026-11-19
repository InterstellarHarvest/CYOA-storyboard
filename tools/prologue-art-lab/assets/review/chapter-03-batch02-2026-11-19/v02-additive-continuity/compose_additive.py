"""Owner-directed additive variants: immutable approved base pixels plus explicit layers."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rgba(p):return Image.open(ROOT/p).convert('RGBA')
def mask_object(src,points,box,size):
 m=Image.new('L',src.size);ImageDraw.Draw(m).polygon(points,fill=255)
 out=src.copy();out.putalpha(m);out=out.crop(box)
 if out.size!=size:out=out.resize(size,Image.Resampling.NEAREST)
 return out
def put(layer,obj,xy):layer.alpha_composite(obj,xy)
def poly(layer,points,color):ImageDraw.Draw(layer).polygon(points,fill=color)
def rect(layer,box,color):ImageDraw.Draw(layer).rectangle(box,fill=color)

base=rgba('references/A01-restroom.png')
close_base=rgba('references/A02-restroom-bg.png')
printer_src=rgba('donors/CH3-B03-record-printer-bg-v01.png')
# A single traced generated printer silhouette is shared by the main and close view.
printer_shape=[(355,178),(368,177),(374,169),(373,158),(379,148),(386,146),(436,146),(446,151),(451,157),(451,171),(471,173),(481,181),(486,194),(486,225),(471,229),(365,229),(350,228),(354,212),(354,195)]
printer_native=mask_object(printer_src,printer_shape,(347,144,491,237),(144,93))
printer_native.save(ROOT/'layers/printer-native-cutout.png')
printer_small=printer_native.resize((24,16),Image.Resampling.NEAREST)
printer_layer=Image.new('RGBA',(314,206));put(printer_layer,printer_small,(245,127))
paper=rgba('layers/B02-generated-paper.png')
paper.save(ROOT/'layers/B02-added-paper.png');printer_layer.save(ROOT/'layers/B02-added-printer.png')
added=Image.new('RGBA',base.size);added.alpha_composite(paper);added.alpha_composite(printer_layer)
added.save(ROOT/'layers/B02-additions.png')
b02=base.copy();b02.alpha_composite(added)

# Approved independently authored A02 close view, reused intact under the new unit.
close_layer=Image.new('RGBA',(564,278))
poly(close_layer,[(418,249),(445,251),(440,277),(415,277)],'#f6e9d0')
rect(close_layer,(424,267,435,269),'#b4ada0')
put(close_layer,printer_native,(410,179));close_layer.save(ROOT/'layers/B03-additions.png')
b03=close_base.copy();b03.alpha_composite(close_layer)

# B06 reuses the exact completed B02 raster, adding only harmless emergency props.
emergency=Image.new('RGBA',(314,206));brush_src=rgba('donors/CH3-B06-paper-emergency-v01.png')
big=[(213,23),(231,23),(231,38),(220,38),(220,64),(225,64),(225,71),(220,74),(220,80),(243,80),(248,83),(251,88),(250,92),(256,96),(262,105),(258,110),(252,108),(248,114),(243,110),(237,115),(232,111),(226,116),(220,112),(214,116),(208,112),(203,114),(197,110),(200,104),(204,98),(202,94),(202,88),(209,83),(216,81),(216,76),(211,73),(211,64),(215,64),(215,38),(213,38)]
small=[(276,41),(284,41),(284,65),(288,65),(288,71),(282,73),(282,79),(293,81),(298,84),(301,90),(306,94),(304,99),(298,102),(294,100),(289,104),(285,101),(279,104),(274,100),(269,102),(266,97),(269,90),(271,85),(278,81),(278,73),(275,71),(275,65),(278,65),(278,47),(276,47)]
big_cut=mask_object(brush_src,big,(193,22,264,120),(50,69))
small_cut=mask_object(brush_src,small,(264,40,310,108),(34,50))
rect(emergency,(236,30,312,34),'#748188');rect(emergency,(237,30,311,31),'#a8afb0');rect(emergency,(237,35,311,35),'#4e626b')
put(emergency,big_cut,(235,28));put(emergency,small_cut,(280,32))
emergency.save(ROOT/'layers/B06-brushes-only.png')
emergency.alpha_composite(rgba('layers/B06-generated-paper.png'))
emergency.save(ROOT/'layers/B06-emergency-additions.png')
b06=b02.copy();b06.alpha_composite(emergency)

# New scanner camera view: replace only its erroneous person/square pictogram.
b04=rgba('donors/CH3-B04-record-scanner-v01.png')
sign_layer=Image.new('RGBA',b04.size)
glyphs=close_base.crop((153,83,208,125)).resize((32,27),Image.Resampling.NEAREST)
put(sign_layer,glyphs,(248,44));sign_layer.save(ROOT/'layers/B04-two-person-sign.png')
b04.alpha_composite(sign_layer)

outputs={'CH3-B02-record-printer':(b02,base,added,'references/A01-restroom.png','layers/B02-additions.png'),'CH3-B03-record-printer-bg':(b03,close_base,close_layer,'references/A02-restroom-bg.png','layers/B03-additions.png'),'CH3-B04-record-scanner':(b04,rgba('donors/CH3-B04-record-scanner-v01.png'),sign_layer,'donors/CH3-B04-record-scanner-v01.png','layers/B04-two-person-sign.png'),'CH3-B06-paper-emergency':(b06,b02,emergency,'candidates/CH3-B02-record-printer-v02.png','layers/B06-emergency-additions.png')}
reports=[]
for ident in ['CH3-B01-arrival','CH3-B02-record-printer','CH3-B03-record-printer-bg','CH3-B04-record-scanner','CH3-B05-record-scanner-bg','CH3-B06-paper-emergency']:
 target=ROOT/f'candidates/{ident}-v02.png'
 if ident not in outputs:
  src=ROOT/f'donors/{ident}-v01.png';shutil.copyfile(src,target);reports.append({'candidateId':ident,'candidate':str(target.relative_to(ROOT)),'sha256':sha(target),'operation':'Unchanged genuinely new camera view; already has two-person restroom pictogram or no restroom pictogram.','base':str(src.relative_to(ROOT)),'baseSha256':sha(src),'changedPixels':0});continue
 result,under,layer,base_file,layer_file=outputs[ident];result.convert('RGB').save(target)
 changes=[]
 for y in range(result.height):
  for x in range(result.width):
   if layer.getpixel((x,y))[3]==0:assert result.getpixel((x,y))==under.getpixel((x,y)),(ident,x,y)
   if result.getpixel((x,y))!=under.getpixel((x,y)):changes.append((x,y))
 if ident in ['CH3-B02-record-printer','CH3-B06-paper-emergency']:
  for box in [(201,96,234,122),(202,122,245,142),(69,38,180,62),(202,67,231,92)]:assert result.crop(box).tobytes()==base.crop(box).tobytes(),(ident,box)
 reports.append({'candidateId':ident,'candidate':str(target.relative_to(ROOT)),'sha256':sha(target),'base':base_file,'baseSha256':sha(ROOT/base_file),'overlay':layer_file,'overlaySha256':sha(ROOT/layer_file),'changedPixels':len(changes),'unexpectedChangesOutsideOverlay':0,'basePixelsCopiedExactlyWhereVisible':True,'baseLayerResampled':False,'dimensions':list(result.size),'approvedAttendantAndBathroomSignsPreserved':True if ident in ['CH3-B02-record-printer','CH3-B06-paper-emergency'] else None,'derivation':'Generated printer/brush cutouts and transparent generated paper additions over immutable base pixels; only the rail, short close-view paper tail and sign placement use explicit native primitives. Only newly added object layers are transformed; no approved scene or foreground is resized or repainted.'})
 if result.size==(314,206):result.convert('RGB').resize((1256,824),Image.Resampling.NEAREST).save(ROOT/f'previews/{ident}-v02-4x.png')
 for name,im in [('base',under),('additions',layer),('result',result)]:
  if name=='base':im.convert('RGB').save(ROOT/f'comparisons/{ident}-base.png')
 mask=layer.getchannel('A');mask.convert('RGB').save(ROOT/f'comparisons/{ident}-addition-mask.png')
for ident in ['CH3-B01-arrival']:
 im=Image.open(ROOT/f'candidates/{ident}-v02.png');im.resize((1256,824),Image.Resampling.NEAREST).save(ROOT/f'previews/{ident}-v02-4x.png')
(ROOT/'sources/additive-edit-records.json').write_text(json.dumps({'ownerInstruction':'Two people on all restroom signs; preserve pixels of repeated scenes and add only new layers.','fullSceneRegenerationsAfterOwnerCorrection':0,'transparentPaperLayerGenerationCalls':2,'assemblyScriptGenerationCalls':0,'nativeAuthorshipLimitation':'Original full-scene native-grid authorship remains unproven. Approved bases are unchanged; generated source-derived object pixels and explicitly authored native additions are documented separately.','candidates':reports},indent=2)+'\n')
print(json.dumps([{k:r[k] for k in ['candidateId','sha256','changedPixels']} for r in reports],indent=2))
