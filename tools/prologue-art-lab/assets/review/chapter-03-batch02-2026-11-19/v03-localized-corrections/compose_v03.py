"""Localized v03 native-grid assembly. Never writes to prior/approved images."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import math, json, hashlib, shutil

ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/'v02-additive-continuity'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def opened(p): return Image.open(p).convert('RGBA')
def blank(size): return Image.new('RGBA',size)
def poly(im,points,color): ImageDraw.Draw(im).polygon(points,fill=color)
def rect(im,box,color): ImageDraw.Draw(im).rectangle(box,fill=color)
def line(im,points,color,width=1): ImageDraw.Draw(im).line(points,fill=color,width=width)
def mask_poly(size,points):
 m=Image.new('L',size);ImageDraw.Draw(m).polygon(points,fill=255);return m
def save_mask(m,name): m.save(ROOT/'masks'/name)
def save_layer(im,name): im.save(ROOT/'layers'/name)

base=opened(ROOT/'references/A01-restroom.png')
close=opened(ROOT/'references/A02-restroom-bg.png')

# Hand-traced row runs follow the one-pixel edge of the approved head/body.
# Bounds are inclusive; neither the old rectangle nor any dilation is used.
rows={
97:(213,218),98:(212,219),99:(211,220),100:(210,222),
101:(208,223),102:(207,223),103:(207,223),104:(206,223),
105:(206,223),106:(206,224),107:(206,225),108:(206,225),
109:(206,225),110:(206,225),111:(206,225),112:(207,226),
113:(207,226),114:(208,226),115:(208,226),116:(209,226),
117:(210,225),118:(211,224),119:(212,224),120:(213,227),
121:(210,230),122:(208,232),123:(207,233),124:(207,233),
125:(206,234),126:(206,234),127:(205,234),128:(205,235),
129:(205,235),130:(205,235),131:(205,236),132:(205,236),
133:(205,236),134:(205,236),135:(205,237),136:(205,237),
137:(205,237),138:(205,237),139:(205,237),140:(205,237),141:(205,237)}
attendant=Image.new('L',base.size);d=ImageDraw.Draw(attendant)
for y,(left,right) in rows.items(): d.line((left,y,right,y),fill=255)
save_mask(attendant,'attendant-one-pixel-silhouette.png')
(ROOT/'sources/attendant-silhouette-row-runs.json').write_text(json.dumps({'source':'references/A01-restroom.png','method':'Manual inclusive native row runs, inspected at 1x and enlarged grid; binary mask, no feather/dilation/threshold','rows':{str(k):list(v) for k,v in rows.items()}},indent=2)+'\n')
# Chair edge and the small microphone are separate actual-object silhouettes.
chair=mask_poly(base.size,[(203,126),(203,127),(201,127),(201,128),(200,128),(200,130),(199,130),(199,140),(201,141),(204,141),(204,128),(205,126)])
mic=mask_poly(base.size,[(195,123),(199,123),(200,124),(200,125),(198,126),(197,126),(197,129),(198,130),(198,133),(199,134),(199,139),(201,140),(201,142),(193,142),(193,140),(196,140),(196,135),(195,134),(195,127),(194,126),(194,124)])
save_mask(chair,'chair-visible-silhouette.png');save_mask(mic,'microphone-silhouette.png')

# Native vector-like polygons are rasterized directly on the logical grid.
# Only these new paper pixels are authored; no scene filter or resampling.
paper=blank(base.size)
poly(paper,[(184,138),(193,138),(194,142),(192,150),(190,157),(188,166),(185,175),(180,183),(172,190),(167,187),(174,179),(179,171),(182,161),(184,150)],'#d4c7b1')
poly(paper,[(185,139),(192,139),(193,142),(190,151),(187,160),(185,171),(181,179),(174,185),(170,187),(168,185),(176,177),(181,167),(183,157),(185,147)],'#f1e8d7')
line(paper,[(185,139),(186,145),(184,154),(182,165),(178,175),(172,182)],'#faf0db')
poly(paper,[(168,185),(162,187),(151,187),(138,186),(126,188),(117,192),(117,196),(124,200),(138,201),(151,199),(159,196),(166,195),(172,197),(169,200),(164,200),(160,198),(152,202),(137,204),(123,203),(114,199),(111,194),(116,189),(126,185),(138,183),(151,184),(164,184)],'#c0b6a5')
poly(paper,[(168,185),(162,188),(151,190),(138,189),(126,190),(118,193),(120,196),(128,199),(140,199),(151,197),(160,193),(168,192),(174,194),(176,197),(173,200),(166,201),(162,199),(166,198),(171,197),(168,195),(162,196),(153,200),(140,202),(127,202),(117,199),(113,195),(116,190),(126,186),(138,185),(151,186),(163,184)],'#eee4d1')
for pts in [[(185,145),(190,146)],[(183,154),(188,155)],[(181,164),(186,165)],[(178,174),(182,176)],[(169,182),(172,184)],[(151,186),(151,189)],[(135,187),(135,189)],[(122,190),(124,192)],[(124,198),(125,200)],[(141,199),(141,201)],[(155,197),(156,199)]]: line(paper,pts,'#b6b1a7')
# Nothing about the microphone is redrawn, including its original pixel edge.
paper.putalpha(ImageChops.subtract(paper.getchannel('A'),mic))
save_layer(paper,'B02-left-unit-paper.png')
b02=base.copy();b02.alpha_composite(paper)

cp=blank(close.size)
# The bottom slot of the same cream slotted housing is now the paper outlet.
poly(cp,[(122,242),(149,242),(150,247),(146,254),(141,261),(137,269),(134,277),(111,277),(114,269),(120,258),(125,250)],'#c0b3a0')
poly(cp,[(124,243),(148,243),(148,247),(143,254),(138,262),(134,271),(132,277),(113,277),(117,267),(123,256),(127,249)],'#f0e4cf')
line(cp,[(124,243),(128,246),(127,250),(122,259),(117,270),(115,277)],'#fff1d8')
for pts in [[(128,248),(144,248)],[(125,256),(139,257)],[(120,266),(134,267)],[(116,274),(130,275)]]:line(cp,pts,'#b6afa2',2)
save_layer(cp,'B03-left-unit-paper.png');b03=close.copy();b03.alpha_composite(cp)

# The scanner is the same housing in both views. Only the door leaf's local
# leading edge and its handle move toward closed; jambs, reader and room stay.
def close_door(im,kind):
 out=im.copy();pixels=im.load();change=blank(im.size)
 if kind=='main':
  # Restore the old handle's door-plane pixels, then shift its exact cutout.
  for y in range(130,147):
   for x in range(102,129):out.putpixel((x,y),pixels[94,y])
  for y in range(56,195):
   for x in range(123,138):out.putpixel((x,y),pixels[94 if 130<=y<147 else 116,y])
   for x in range(138,143):out.putpixel((x,y),pixels[x-15,y])
  hmask=Image.new('L',im.size);hd=ImageDraw.Draw(hmask)
  for hy,(hx0,hx1) in {133:(115,120),134:(114,121),135:(113,122),136:(112,123),137:(104,123),138:(103,123),139:(103,123),140:(103,123),141:(104,123),142:(112,122),143:(113,122),144:(114,121)}.items():hd.line((hx0,hy,hx1,hy),fill=255)
  obj=im.copy();obj.putalpha(hmask);out.alpha_composite(obj,(15,0))
  # A printed arrow on the inserted document points into the roller nip.
  poly(out,[(198,130),(202,125),(207,130),(204,130),(204,136),(200,136),(200,130)],'#658a83')
  slit={'jambInnerX':147,'doorLeadingEdgeX':142,'clearWidthPixels':4}
 else:
  for y in range(196,242):
   for x in range(8,55):out.putpixel((x,y),pixels[3,y])
  for y in range(18,278):
   for x in range(51,70):out.putpixel((x,y),pixels[3 if 196<=y<242 else 40,y])
   for x in range(70,74):out.putpixel((x,y),pixels[x-19,y])
  # Upper extension follows the existing sloped top of this closer door leaf.
  for x in range(51,74):
   top=18+round((x-51)*0.35)
   for y in range(18,top):out.putpixel((x,y),pixels[x,y])
  hmask=mask_poly(im.size,[(44,196),(49,196),(53,201),(54,208),(53,221),(50,227),(44,231),(36,229),(31,226),(13,225),(9,222),(9,213),(14,208),(32,207),(34,201),(38,198)])
  obj=im.copy();obj.putalpha(hmask);out.alpha_composite(obj,(19,0))
  poly(out,[(180,206),(190,195),(204,207),(197,207),(202,222),(191,223),(187,207)],'#658a83')
  slit={'jambInnerX':81,'doorLeadingEdgeX':73,'clearWidthPixels':7}
 for y in range(im.height):
  for x in range(im.width):
   if out.getpixel((x,y))!=im.getpixel((x,y)):change.putpixel((x,y),out.getpixel((x,y)))
 return out,change,slit
b04,b04edits,slit04=close_door(opened(OLD/'candidates/CH3-B04-record-scanner-v02.png'),'main')
b05,b05edits,slit05=close_door(opened(OLD/'candidates/CH3-B05-record-scanner-bg-v02.png'),'close')
save_layer(b04edits,'B04-local-door-and-document-edits.png');save_layer(b05edits,'B05-local-door-and-document-edits.png')

# New generated additions are object donors only. Manual object contours retain
# paper/brush alpha while excluding the unwanted generated plant and fringe.
donor=opened(ROOT/'layers/generated-additions-native-donor.png')
objects=Image.new('L',base.size);od=ImageDraw.Draw(objects)
od.polygon([(228,30),(309,30),(309,38),(296,40),(294,68),(300,75),(300,85),(307,90),(310,101),(309,107),(307,109),(307,125),(302,134),(295,139),(283,141),(288,137),(296,130),(298,121),(296,114),(292,110),(282,108),(273,104),(267,101),(260,103),(254,108),(247,115),(238,122),(232,128),(233,132),(238,135),(248,140),(258,144),(266,148),(268,153),(268,159),(264,164),(254,170),(248,174),(251,178),(261,181),(268,187),(270,193),(265,198),(253,200),(238,200),(223,198),(211,195),(198,200),(182,201),(167,198),(159,194),(146,198),(129,201),(111,200),(98,197),(91,193),(87,188),(89,179),(95,174),(106,169),(118,166),(130,168),(141,173),(153,181),(157,174),(162,155),(168,145),(175,141),(190,141),(182,145),(175,151),(171,162),(168,175),(168,184),(178,179),(186,172),(196,167),(211,165),(220,170),(230,177),(238,169),(248,162),(256,157),(257,153),(250,150),(241,146),(234,141),(226,138),(222,134),(220,130),(221,124),(229,115),(239,106),(246,101),(238,104),(229,106),(225,103),(227,96),(231,89),(239,84),(245,80),(246,75),(244,72),(244,68),(249,66),(249,40),(244,39),(244,38),(228,38)],fill=255)
# Explicitly traced generated plant fragments, NOT a rectangular exclusion.
for points in [[(241,113),(245,115),(249,120),(249,124),(246,128),(242,124),(241,119)],[(230,125),(236,123),(242,127),(246,130),(245,134),(238,133),(233,130)],[(248,122),(253,119),(259,117),(261,118),(256,123),(252,126),(248,127)],[(245,136),(250,133),(254,134),(252,139),(248,143),(245,141)],[(240,143),(243,141),(253,140),(256,143),(255,151),(253,154),(242,154),(240,151)]]:od.polygon(points,fill=0)
# One-pixel row-run cleanup of remaining generated leaf fragments. These
# manually inspected object-edge coordinates do not alter the approved plant.
plant_cleanup={111:[(243,247)],112:[(242,247)],113:[(241,250)],114:[(243,249)],115:[(239,241),(245,248)],116:[(239,241)],117:[(239,241)],118:[(236,241)],119:[(235,241)],120:[(230,241)],121:[(230,240)],122:[(232,239)],123:[(233,238)],138:[(243,245)]}
for y,runs in plant_cleanup.items():
 for x0,x1 in runs:od.line((x0,y,x1,y),fill=0)
(ROOT/'sources/generated-plant-edge-cleanup.json').write_text(json.dumps({'method':'Manually inspected native object-edge row runs, no palette or alpha threshold filter','rows':plant_cleanup},indent=2)+'\n')
save_mask(objects,'B06-traced-addition-objects.png')
emergency=donor.copy();emergency.putalpha(ImageChops.multiply(donor.getchannel('A'),objects))
# Remove the residual generated pot-rim fragment by tracing that fragment.
# The approved plant is already present below this completely transparent area.
fragment=mask_poly(base.size,[(237,140),(241,137),(246,139),(247,142),(244,144),(239,145),(237,143)])
emergency.putalpha(ImageChops.subtract(emergency.getchannel('A'),fragment))
# A short paper fold joins the rising strip to the original plant's pot and
# lower leaves, instead of leaving a detached remnant of the generated pot.
plant_fold=blank(base.size)
poly(plant_fold,[(262,149),(267,146),(270,140),(268,135),(263,132),(257,130),(251,126),(246,125),(246,129),(252,133),(259,136),(263,139),(262,143),(258,146)],'#bcb4aa')
poly(plant_fold,[(263,148),(267,144),(268,140),(266,137),(260,134),(254,131),(248,127),(246,127),(250,131),(256,135),(262,138),(264,141),(261,145)],'#eee4d6')
for pts in [[(261,146),(265,147)],[(263,140),(267,140)],[(257,133),(259,135)],[(249,128),(251,130)]]:line(plant_fold,pts,'#b2ada7')
emergency.alpha_composite(plant_fold)
# A native short connector seats the generated receipt feed in the existing
# left housing. Its paper lies in front of the counter but behind the mic.
feed=blank(base.size)
poly(feed,[(184,138),(193,138),(194,142),(188,146),(182,149),(178,155),(174,164),(172,173),(168,183),(165,187),(159,183),(165,174),(168,164),(172,153),(178,146)],'#cec3b2')
poly(feed,[(185,139),(192,139),(192,141),(186,145),(181,148),(176,156),(173,166),(171,175),(167,183),(164,185),(161,182),(166,173),(169,163),(173,153),(179,146)],'#f1e7d4')
for pts in [[(183,146),(188,148)],[(176,154),(181,156)],[(172,164),(177,166)],[(169,174),(173,176)]]:line(feed,pts,'#b5afa5')
emergency.alpha_composite(feed)
# Mount caps join the rail to the existing cornice; native rigid joints.
for x in [239,300]:
 rect(emergency,(x,26,x+5,31),'#5b6b70');rect(emergency,(x+1,26,x+4,28),'#a8afb0');rect(emergency,(x+2,28,x+3,29),'#3e5059')
protected=ImageChops.lighter(attendant,ImageChops.lighter(chair,mic))
emergency.putalpha(ImageChops.subtract(emergency.getchannel('A'),protected))
save_layer(emergency,'B06-silhouette-occluded-additions.png');save_mask(protected,'B06-protected-object-silhouettes.png')
b06=base.copy();b06.alpha_composite(emergency)

items=[('CH3-B01-arrival',opened(OLD/'candidates/CH3-B01-arrival-v02.png'),None,OLD/'candidates/CH3-B01-arrival-v02.png'),('CH3-B02-record-printer',b02,paper,ROOT/'references/A01-restroom.png'),('CH3-B03-record-printer-bg',b03,cp,ROOT/'references/A02-restroom-bg.png'),('CH3-B04-record-scanner',b04,b04edits,OLD/'candidates/CH3-B04-record-scanner-v02.png'),('CH3-B05-record-scanner-bg',b05,b05edits,OLD/'candidates/CH3-B05-record-scanner-bg-v02.png'),('CH3-B06-paper-emergency',b06,emergency,ROOT/'references/A01-restroom.png')]
records=[]
for ident,result,layer,bp in items:
 dest=ROOT/f'candidates/{ident}-v03.png'
 if layer is None:shutil.copyfile(bp,dest)
 else:result.convert('RGB').save(dest)
 before=opened(bp);changes=[];unexpected=[]
 mask=Image.new('L',result.size)
 for y in range(result.height):
  for x in range(result.width):
   if result.getpixel((x,y))!=before.getpixel((x,y)):
    changes.append([x,y]);mask.putpixel((x,y),255)
    if layer is None or not layer.getpixel((x,y))[3]:unexpected.append([x,y])
 assert not unexpected,(ident,unexpected[:10])
 if layer is not None:
  expected=before.copy();expected.alpha_composite(layer);assert expected.tobytes()==result.tobytes()
 save_mask(mask,f'{ident}-changed-pixels.png')
 (ROOT/f'sources/{ident}-changed-coordinates.json').write_text(json.dumps(changes,separators=(',',':'))+'\n')
 rec={'candidateId':ident,'file':str(dest.relative_to(ROOT)),'sha256':sha(dest),'dimensions':list(result.size),'mode':'RGB','alphaExtrema':[255,255],'base':str(bp.relative_to(ROOT)) if bp.is_relative_to(ROOT) else '../v02-additive-continuity/'+str(bp.relative_to(OLD)),'baseSha256':sha(bp),'baseResized':False,'changedPixels':len(changes),'unexpectedChangesOutsideMask':0,'mask':f'masks/{ident}-changed-pixels.png','coordinateList':f'sources/{ident}-changed-coordinates.json','status':'generated','selected':False,'approved':False,'assetPath':None}
 records.append(rec)
 if result.size==(314,206):result.convert('RGB').resize((1256,824),Image.Resampling.NEAREST).save(ROOT/f'previews/{ident}-v03-4x.png')
 # Attendant face/body and microphone remain exact actual-object pixels.
 if ident in ['CH3-B02-record-printer','CH3-B06-paper-emergency']:
  for name,m in [('attendant',attendant),('microphone',mic),('chair',chair)]:
   count=sum(1 for y in range(206) for x in range(314) if m.getpixel((x,y)) and result.getpixel((x,y))!=base.getpixel((x,y)))
   assert count==0,(ident,name,count)
  rec['approvedAttendantMicrophoneAndChairPixelsExact']=True
 # The entire untouched plant is present in ordinary print views.
 if ident=='CH3-B02-record-printer':assert result.crop((241,110,270,145)).tobytes()==base.crop((241,110,270,145)).tobytes()
 if ident=='CH3-B03-record-printer-bg':assert result.crop((453,119,564,270)).tobytes()==close.crop((453,119,564,270)).tobytes()

(ROOT/'sources/localized-edit-records.json').write_text(json.dumps({'sourceCommit':'2699abbd651817961b76d87fa0d4c78a57b04bc5','candidates':records,'scannerDoorSlits':{'B04':slit04,'B05':slit05},'nativeAuthorship':'UNPROVEN for inherited and generated raster sources. Native edits are limited to explicit paper polygons/marks, door repair sampling, handle transfer, intake arrows, mount caps and traced binary object masks; no whole-scene filtering or generation.'},indent=2)+'\n')
print(json.dumps([{'id':r['candidateId'],'hash':r['sha256'],'changedPixels':r['changedPixels']} for r in records],indent=2))
