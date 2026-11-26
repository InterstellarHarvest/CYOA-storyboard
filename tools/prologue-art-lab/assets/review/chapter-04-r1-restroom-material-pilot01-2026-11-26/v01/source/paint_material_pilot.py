"""Localized, explicit native-grid material painting; never a reference filter.

All brush paths rasterize once on 564x278 layers, without antialiasing. Cubic
paths describe the basin's existing rounded forms, not colour gradients. The
approved image is read only after painting, for bounded opaque compositing and
the exact changed-pixel verification. No source colours are sampled.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import json, hashlib, io, zipfile, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SIZE=(564,278)
RAMPS={
 'ceramic':['#5e685b','#777f6d','#939b85','#a8ae96','#b9bda4','#c9cab0','#d8d6bc','#e4dfc4','#eee7cd','#f7efd6','#fff6df'],
 'glaze':['#f1dfbc','#d2c6a5','#b4ac8d','#8d9079'],
 'brass':['#2f392f','#475342','#606e54','#7d8765','#9ca17b','#bdbb91','#dbd0a3','#f1e1b6','#fff0ca','#8b7445','#b39a5e','#d2b578'],
 'shadow':['#203b32','#314b3e','#465b49','#61705a','#7c886f'],
 'wear':['#716a51','#9e9272','#bcaf89','#d8caa7'],
}
PAL={f'{name}{i}':c for name,cs in RAMPS.items()for i,c in enumerate(cs)}
layers=[];tape=[]

def raster_path(commands):
 """Native-grid path tessellation; no enlarged working bitmap exists."""
 pts=[];current=None;start=None
 for cmd in commands:
  if cmd[0]=='M':current=tuple(cmd[1:]);start=current;pts.append(current)
  elif cmd[0]=='L':current=tuple(cmd[1:]);pts.append(current)
  elif cmd[0]=='C':
   p0=current;p1=cmd[1:3];p2=cmd[3:5];p3=cmd[5:7]
   for i in range(1,49):
    t=i/48;u=1-t;pts.append((round(u*u*u*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t*t*t*p3[0]),round(u*u*u*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t*t*t*p3[1])))
   current=tuple(p3)
  elif cmd[0]=='Z':pts.append(start);current=start
 return pts

def layer(name,material):
 global canvas,draw,marks
 canvas=Image.new('RGBA',SIZE);draw=ImageDraw.Draw(canvas);marks=[]
 layers.append((name,material,canvas));tape.append({'name':name,'material':material,'commands':marks})
def path(colour,*commands):
 draw.polygon(raster_path(commands),fill=PAL[colour]);marks.append(['path',colour,commands])
def poly(colour,*points):
 draw.polygon(points,fill=PAL[colour]);marks.append(['polygon',colour,points])
def line(colour,*points,width=1):
 draw.line(points,fill=PAL[colour],width=width);marks.append(['line',colour,points,width])
def oval(colour,box):
 draw.ellipse(box,fill=PAL[colour]);marks.append(['ellipse',colour,box])

def independent_allowed_mask():
 """Approved-geometry work envelope, defined separately from painted marks."""
 mask=Image.new('L',SIZE);d=ImageDraw.Draw(mask)
 # Basin/apron silhouette and its immediate underside, clipped at canvas edges.
 d.polygon(raster_path([('M',-2,222),('C',14,218,33,214,46,213),('C',78,210,131,212,146,215),('C',156,217,160,220,156,226),('L',155,242),('C',142,258,118,266,100,278),('L',-2,278),('Z',)]),fill=255)
 # Faucet envelope excludes the mirror, wall lamp and both rear basin groups.
 d.polygon([(40,185),(43,181),(51,181),(53,179),(59,180),(62,183),(68,182),(72,186),(71,190),(63,191),(63,195),(83,193),(90,195),(96,201),(99,210),(97,214),(88,214),(85,204),(78,204),(67,207),(67,216),(71,222),(64,227),(43,225),(40,219),(44,211),(45,198),(50,193),(49,190),(42,190)],fill=255)
 # Foreground waste/support run and narrow occlusion shadow, not adjacent tiles.
 d.polygon([(93,277),(111,265),(133,255),(153,240),(160,240),(160,248),(145,262),(122,277),(122,278),(93,278)],fill=255)
 return mask

def paint():
 layer('01 immediate contact shadow','shadow')
 path('shadow1',('M',94,277),('C',113,265,140,253,155,241),('L',159,243),('C',155,253,139,264,120,278),('Z',))
 path('shadow0',('M',99,277),('C',119,265,144,252,156,244),('L',155,248),('C',137,262,125,269,113,278),('Z',))
 path('shadow2',('M',105,278),('C',121,268,145,256,158,245),('L',156,251),('C',138,263,129,269,119,278),('Z',))

 layer('02 foreground supporting waste pipe','brass')
 path('brass0',('M',114,278),('C',126,271,143,262,153,254),('L',157,258),('C',146,267,133,274,126,279),('Z',))
 path('brass9',('M',116,278),('C',131,269,144,263,154,255),('L',155,258),('C',140,268,130,273,121,278),('Z',))
 path('brass10',('M',117,277),('C',128,270,145,262,153,255),('L',153,256),('C',141,266,128,272,119,278),('Z',))
 line('brass5',(124,273),(135,267),(140,264))
 poly('brass0',(140,261),(143,259),(149,265),(146,268),(143,266))
 poly('brass9',(141,261),(143,260),(148,265),(146,267),(143,264))
 line('brass6',(142,260),(144,262),(146,264))
 line('brass2',(143,262),(146,265),(146,266))

 layer('03 curved ceramic apron and underbelly','ceramic')
 path('ceramic1',('M',-2,232),('C',47,234,94,235,119,230),('C',135,227,146,223,155,220),('L',154,242),('C',144,254,123,263,109,270),('L',99,278),('L',-2,278),('Z',))
 # Curved lower belly: continuous shade bands, never triangular facets.
 path('ceramic2',('M',-2,234),('C',45,237,88,238,116,232),('L',154,222),('L',153,241),('C',140,254,118,263,104,269),('C',77,273,31,272,-2,272),('Z',))
 path('ceramic3',('M',-2,235),('C',47,238,90,238,117,232),('C',134,229,146,225,153,223),('L',152,240),('C',140,251,118,260,102,265),('C',73,270,31,269,-2,268),('Z',))
 path('ceramic4',('M',-2,236),('C',48,239,92,238,117,233),('C',134,229,146,226,152,224),('L',151,239),('C',137,250,119,258,100,263),('C',72,267,32,267,-2,265),('Z',))
 path('ceramic5',('M',-2,237),('C',39,241,80,240,109,236),('C',127,234,143,229,151,225),('L',150,237),('C',135,247,115,254,101,257),('C',75,262,34,262,-2,261),('Z',))
 # The front is softly convex, with a darker zone immediately under the rolled lip.
 path('ceramic4',('M',-2,237),('C',40,241,82,241,111,237),('L',115,242),('C',87,245,38,245,-2,241),('Z',))
 path('ceramic3',('M',-2,237),('C',46,240,87,240,111,236),('L',111,238),('C',86,242,43,243,-2,239),('Z',))
 # Right turn catches the room's warm lamp: narrow curved glazing, not a bevel box.
 path('ceramic6',('M',116,236),('C',132,232,146,227,153,222),('L',152,238),('C',144,246,130,252,116,257),('C',119,250,119,243,116,236),('Z',))
 path('ceramic7',('M',124,233),('C',139,229,149,224,153,222),('L',152,235),('C',146,241,136,246,126,250),('C',129,243,128,238,124,233),('Z',))
 path('ceramic8',('M',130,230),('C',143,226,150,223,153,221),('L',152,231),('C',146,236,141,239,137,240),('L',137,234),('Z',))
 path('ceramic6',('M',12,248),('C',28,245,51,245,69,246),('L',72,251),('C',50,251,27,252,11,254),('Z',))
 path('ceramic6',('M',77,249),('C',89,248,98,246,104,244),('L',106,250),('C',98,254,89,256,77,257),('Z',))
 path('ceramic5',('M',3,261),('C',25,263,57,264,80,262),('L',79,265),('C',54,267,25,266,3,265),('Z',))
 # Glaze reflection follows the convex apron; the point highlight stays selective.
 path('ceramic7',('M',109,240),('C',111,246,112,253,110,261),('L',108,264),('L',107,264),('C',109,255,108,248,107,243),('Z',))
 poly('ceramic9',(108,242),(110,242),(111,244),(110,246),(108,245))
 line('ceramic8',(109,248),(110,253),(110,257))
 path('glaze1',('M',5,268),('C',32,270,72,270,94,267),('L',94,268),('C',69,272,29,272,5,270),('Z',))

 layer('04 rolled rim bowl and reflected tap','ceramic')
 # Same shallow, foreshortened rounded-rectangle opening as the approved bowl.
 path('ceramic7',('M',-2,224),('C',16,219,31,216,45,215),('C',75,211,120,212,143,215),('C',155,217,160,220,155,224),('C',149,229,130,234,113,237),('C',83,242,34,240,-2,236),('Z',))
 path('ceramic8',('M',-2,224),('C',17,219,31,217,45,216),('C',77,213,119,213,143,216),('C',151,217,157,220,153,223),('C',141,229,127,233,110,235),('C',82,239,33,238,-2,234),('Z',))
 path('ceramic9',('M',-2,225),('C',17,221,31,218,46,217),('L',46,218),('C',28,220,13,223,-2,227),('Z',))
 path('ceramic9',('M',68,214),('C',93,213,125,214,143,217),('C',151,218,155,220,151,222),('L',149,222),('C',151,219,145,219,140,218),('C',118,215,90,215,68,216),('Z',))
 # Bowl walls are darker toward their back lip, brighter on the rounded well.
 path('ceramic2',('M',13,228),('C',25,223,38,220,47,220),('C',78,216,121,216,138,219),('C',146,220,134,224,128,226),('C',113,232,78,234,47,233),('C',28,233,16,232,13,230),('Z',))
 path('ceramic3',('M',17,228),('C',29,224,40,222,49,222),('C',79,218,117,218,136,220),('C',139,221,130,224,125,226),('C',106,231,76,232,48,231),('C',30,231,20,230,17,229),('Z',))
 path('ceramic4',('M',19,229),('C',33,225,53,223,70,222),('C',90,220,116,220,130,221),('C',129,223,122,226,113,228),('C',94,232,49,232,27,231),('Z',))
 path('ceramic5',('M',27,230),('C',43,226,64,225,82,225),('C',104,224,120,224,124,224),('C',115,229,91,232,68,232),('L',42,232),('Z',))
 path('ceramic6',('M',68,230),('C',76,227,84,226,96,226),('C',104,226,112,226,114,227),('C',104,230,93,231,83,231),('Z',))
 path('ceramic7',('M',75,230),('C',83,228,94,228,103,228),('L',106,229),('C',97,231,84,231,75,231),('Z',))
 # Tap's shadow and warm reflection fall down the back wall into the bowl.
 path('glaze3',('M',42,221),('L',48,220),('L',55,222),('L',63,220),('L',69,220),('L',70,225),('L',68,230),('L',65,230),('L',64,225),('L',58,224),('L',52,226),('L',50,232),('L',46,232),('L',47,226),('L',43,226),('Z',))
 path('glaze2',('M',47,222),('L',51,222),('L',52,225),('L',51,232),('L',49,232),('L',49,226),('Z',))
 path('glaze1',('M',53,223),('L',57,223),('L',58,226),('L',57,232),('L',55,232),('L',55,226),('Z',))
 path('ceramic8',('M',-2,233),('C',33,237,82,238,110,234),('C',126,232,144,226,152,222),('L',152,223),('C',141,229,125,233,110,236),('C',80,240,32,239,-2,235),('Z',))
 path('ceramic10',('M',-2,233),('C',28,236,62,237,88,236),('L',89,237),('C',62,239,27,237,-2,235),('Z',))
 path('ceramic10',('M',104,236),('C',121,233,140,227,150,222),('L',150,223),('C',138,229,121,235,106,237),('Z',))
 path('glaze0',('M',116,235),('C',120,234,126,232,129,231),('L',128,233),('L',125,234),('L',124,238),('L',122,238),('L',121,236),('L',118,237),('Z',))

 layer('05 brass tap spout body and crosshead','brass')
 # Spout sits behind the cylindrical tap pillar; arcs are native stepped contours.
 path('brass0',('M',59,198),('C',67,198,77,194,83,195),('C',92,194,98,203,98,211),('L',96,214),('L',89,214),('L',88,208),('C',87,204,86,203,82,204),('L',62,208),('Z',))
 path('brass2',('M',60,199),('C',68,199,77,196,84,196),('C',91,196,96,204,96,211),('L',91,212),('L',90,208),('C',88,202,85,202,81,203),('L',61,207),('Z',))
 path('brass4',('M',60,199),('C',69,199,78,196,84,197),('C',90,197,94,203,95,208),('L',93,209),('C',91,203,88,200,84,200),('C',77,200,69,203,61,204),('Z',))
 path('brass6',('M',61,199),('C',70,198,78,196,85,197),('C',90,198,93,201,94,205),('L',93,205),('C',90,201,87,199,84,199),('C',77,199,69,202,61,202),('Z',))
 line('brass8',(65,199),(77,197),(83,197),(87,198))
 path('brass9',('M',62,204),('C',71,202,78,201,83,201),('L',86,203),('C',79,203,71,205,63,207),('Z',))
 oval('brass0',(89,210,98,214));oval('brass2',(90,210,97,212));line('brass6',(91,210),(96,210))
 # Broad face bands establish a round, tarnished cylinder, with a rolled foot.
 path('brass0',('M',48,196),('C',52,194,58,194,62,197),('L',63,214),('L',67,219),('L',66,222),('C',60,225,49,224,43,221),('L',43,218),('L',46,215),('Z',))
 path('brass2',('M',49,197),('C',53,196,57,196,60,198),('L',61,215),('L',65,219),('L',64,221),('C',58,223,51,222,46,220),('L',45,218),('L',48,215),('Z',))
 path('brass3',('M',50,198),('L',55,197),('L',57,215),('L',59,218),('L',56,221),('L',49,220),('L',48,217),('Z',))
 path('brass5',('M',51,198),('L',53,198),('L',53,215),('L',55,218),('L',52,220),('L',49,218),('L',50,213),('Z',))
 line('brass7',(51,199),(51,211),(50,215))
 path('brass1',('M',59,198),('L',61,199),('L',61,214),('L',64,219),('L',61,220),('L',58,217),('Z',))
 oval('brass0',(43,217,67,223));oval('brass4',(44,217,66,221));oval('brass2',(46,217,64,220))
 line('brass6',(45,219),(49,220),(58,220),(64,218))
 line('brass9',(45,222),(51,223),(60,223),(65,221))
 line('brass10',(49,222),(55,223),(59,222))
 # Neck and cap separate the spindle from the pillar, without extra machinery.
 oval('brass0',(49,192,62,198));oval('brass5',(50,192,61,196));oval('brass2',(51,191,60,194))
 poly('brass1',(52,187),(58,187),(59,192),(61,194),(50,195),(50,192),(52,191))
 poly('brass3',(53,187),(56,187),(56,191),(58,193),(52,194),(52,192))
 line('brass6',(53,189),(53,192),(52,193))
 path('brass0',('M',46,184),('L',66,184),('L',68,186),('L',67,190),('L',61,189),('L',51,189),('L',45,189),('Z',))
 path('brass3',('M',47,185),('L',66,185),('L',67,187),('L',62,188),('L',50,188),('L',46,187),('Z',))
 line('brass6',(48,185),(52,185),(60,186),(65,186))
 # Three compact round handle masses: light upper-left, occlusion lower-right.
 oval('brass0',(42,182,51,190));oval('brass3',(43,182,50,188));oval('brass5',(43,182,48,186));poly('brass7',(44,183),(47,182),(48,184),(45,185))
 oval('brass0',(63,182,71,190));oval('brass3',(63,182,70,188));oval('brass5',(64,183,69,186));line('brass7',(65,183),(67,183))
 oval('brass0',(51,179,60,189));oval('brass3',(51,180,59,188));oval('brass6',(52,180,57,184));poly('brass8',(53,181),(55,180),(57,182),(54,183));line('brass4',(53,187),(56,188),(58,186))

 layer('06 selective grouped glaze wear and fittings','wear')
 # Retain the existing glaze fracture rather than inventing a network of scratches.
 line('glaze2',(26,239),(27,243),(25,246),(23,248))
 line('wear1',(23,248),(20,250),(17,253),(14,257),(12,259))
 line('glaze3',(26,244),(28,247),(31,250))
 line('glaze1',(28,247),(30,249),(33,253))
 line('glaze0',(24,248),(22,250),(18,254))
 # Small connected patches follow the lower lip and tap runoff, not random noise.
 poly('wear1',(93,266),(98,265),(100,266),(98,268),(94,268),(92,267))
 poly('wear0',(94,267),(98,266),(99,267),(97,268),(94,268))
 line('glaze0',(91,266),(94,265),(97,265))
 poly('glaze2',(52,242),(54,242),(54,247),(53,251),(52,250))
 line('glaze1',(53,253),(53,258),(52,260))
 poly('glaze1',(75,260),(77,258),(79,259),(80,262),(78,263),(76,262))
 poly('wear2',(122,245),(124,244),(124,247),(122,249),(121,249))
 line('glaze0',(122,243),(123,242))
 poly('glaze0',(103,259),(104,258),(106,260),(106,262),(104,263))
 # Grouped tarnish on the tap's shaded side, preserving its metallic light strip.
 poly('brass9',(59,207),(61,206),(61,211),(60,212),(59,211))
 line('brass10',(60,216),(61,217),(62,217))
 line('brass11',(47,219),(48,220),(50,220))

def save():
 allowed=independent_allowed_mask();allowed.save(ROOT/'masks/allowed-edit-region.png')
 # Protection is independent of the paint tape: mirror and rear fixture windows.
 protected=Image.new('L',SIZE);pd=ImageDraw.Draw(protected)
 for box in [(20,29,163,178),(107,175,201,211),(163,212,203,240),(153,170,235,198)]:pd.rectangle(box,fill=255)
 assert not ImageChops.multiply(allowed,protected).getbbox(),'Work envelope overlaps protected fixtures'
 protected.save(ROOT/'masks/protected-fixtures.png')
 group=Image.new('RGBA',SIZE);material_masks={n:Image.new('L',SIZE)for n in ['ceramic','brass','shadow','wear']}
 for i,(name,material,im)in enumerate(layers):
  alpha=ImageChops.multiply(im.getchannel('A'),allowed);im.putalpha(alpha)
  im.save(ROOT/'layers'/f'{i+1:02d}.png');group.alpha_composite(im)
  material_masks[material]=ImageChops.lighter(material_masks[material],alpha)
 group.save(ROOT/'layers/material-group-composite.png')
 for name,im in material_masks.items():im.save(ROOT/'masks'/f'{name}-paint-mask.png')
 # This is the only read of approved raster pixels in the painting program.
 original=Image.open(ROOT/'references/approved-restroom-background.png').convert('RGB')
 result=original.copy();result.paste(group,(0,0),group.getchannel('A'))
 result.save(ROOT/'native/CH4-B2-03-R1-material-pilot01-v01.png')
 delta=ImageChops.difference(original,result);r,g,b=delta.split();changed=ImageChops.lighter(ImageChops.lighter(r,g),b).point(lambda v:255 if v else 0)
 changed.save(ROOT/'masks/changed-pixels.png')
 outside=ImageChops.multiply(changed,ImageChops.invert(allowed));assert not outside.getbbox()
 assert not ImageChops.multiply(changed,protected).getbbox()
 (ROOT/'source/native-paint.json').write_text(json.dumps({'size':SIZE,'palette':PAL,'layers':tape,'allowedEnvelopeSource':'independent_allowed_mask() in paint_material_pilot.py','resamplingDuringPainting':False,'sourcePixelColourSampling':False,'composition':'Opaque native painted layers over the exact approved RGB source. Source outside allowed edit region is never replaced.'},indent=2)+'\n')
 stackroot=ET.Element('image',{'w':'564','h':'278','name':'R1 material pilot 01 — unselected'});stack=ET.SubElement(stackroot,'stack')
 with zipfile.ZipFile(ROOT/'source/CH4-B2-03-material-pilot01.ora','w')as z:
  z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
  for i,(name,material,im)in reversed(list(enumerate(layers))):
   data=io.BytesIO();im.save(data,format='PNG');dest=f'data/layer{i}.png';z.writestr(dest,data.getvalue());ET.SubElement(stack,'layer',{'name':name,'src':dest,'opacity':'1.0','visibility':'visible','composite-op':'svg:src-over','x':'0','y':'0'})
  data=io.BytesIO();original.save(data,format='PNG');z.writestr('data/approved-base.png',data.getvalue());ET.SubElement(stack,'layer',{'name':'APPROVED ORIGINAL — preserve unchanged','src':'data/approved-base.png','opacity':'1.0','visibility':'visible','composite-op':'svg:src-over','x':'0','y':'0'})
  data=io.BytesIO();result.save(data,format='PNG');z.writestr('mergedimage.png',data.getvalue());z.writestr('stack.xml',ET.tostring(stackroot))
 stats={'status':'UNSELECTED — MATERIAL PILOT, NOT SELECTION-READY','dimensions':list(SIZE),'changedPixels':sum(bool(v)for v in changed.get_flattened_data()),'changedBounds':changed.getbbox(),'outsideAllowedRegionChanges':0,'protectedFixtureChanges':0,'nativePaintLayers':len(layers),'paintMarks':sum(len(l['commands'])for l in tape),'paintedRGBColours':len({p[:3]for p in group.get_flattened_data()if p[3]}),'wholeSceneRGBColours':len(result.getcolors(SIZE[0]*SIZE[1])),'globalPaletteReduction':False,'geometryRasterization':'Native cubic boundaries; no oversized intermediate, anti-aliasing, image resampling, sharpening, palette quantization or generated texture.'}
 (ROOT/'evidence/paint-statistics.json').write_text(json.dumps(stats,indent=2)+'\n');print(json.dumps(stats))
if __name__=='__main__':paint();save()
