"""Approved native lobby plus local event layers; no reference resize/filter."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,hashlib,io,zipfile,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
BASE=Image.open(R/'references/approved-lobby.png').convert('RGB')
WC=Image.open(R/'references/approved-restroom.png').convert('RGB')
SIZE=BASE.size;MARKS=[]
P={'deep':'#253b34','dark':'#3b4e46','shadow':'#53645a','mid':'#748478','sage':'#95a396','silver':'#b3bcb0','light':'#d1d5c5','shine':'#ebebd6','white':'#fff4d7','gold':'#ac955e','goldlight':'#e3d19a','black':'#252c2c','tile':'#b6bea3','grout':'#82937c','tilelight':'#d1d0b1'}
def blank():return Image.new('RGBA',SIZE)
def poly(im,c,pts):ImageDraw.Draw(im).polygon(pts,fill=P.get(c,c));MARKS.append(['polygon',c,pts])
def line(im,c,pts,w=1):ImageDraw.Draw(im).line(pts,fill=P.get(c,c),width=w);MARKS.append(['line',c,pts,w])
def rect(im,c,box):ImageDraw.Draw(im).rectangle(box,fill=P.get(c,c));MARKS.append(['rectangle',c,box])
def ellipse(im,c,box):ImageDraw.Draw(im).ellipse(box,fill=P.get(c,c));MARKS.append(['ellipse',c,box])
def doors():
 im=blank();allowed=Image.new('L',SIZE);d=ImageDraw.Draw(allowed)
 for left,right in [(154,178),(195,216)]:
  d.rectangle((left,95,right,149),fill=255)
  rect(im,'deep',(left,95,right,149))
  # Lit rear wall with converging side planes, not a featureless black void.
  poly(im,'tile',[(left+3,100),(right-3,100),(right-3,135),(left+3,135)])
  poly(im,'grout',[(left,96),(left+4,103),(left+4,136),(left,149)])
  poly(im,'sage',[(right,96),(right-4,103),(right-4,136),(right,149)])
  poly(im,'shadow',[(left,96),(right,96),(right-4,103),(left+4,103)])
  line(im,'white',[(left+8,101),(right-7,101)])
  for y in [107,113,119]:line(im,'grout',[(left+4,y),(right-4,y)])
  line(im,'tilelight',[(left+6,104),(left+6,117)])
  # Distant installed green stall partitions are a glimpse, not another close-up.
  rect(im,'dark',(left+5,119,right-5,138));line(im,'sage',[(left+6,120),(right-6,120)])
  line(im,'mid',[(left+7,122),(left+7,136)]);line(im,'deep',[(right-7,121),(right-7,137)])
  rect(im,'goldlight',(right-9,129,right-8,129))
  poly(im,'tile',[(left+4,138),(right-4,138),(right,149),(left,149)])
  line(im,'grout',[(left+4,139),(left+1,149)]);line(im,'grout',[(right-4,139),(right-1,149)])
  line(im,'grout',[(left+3,143),(right-3,143)])
  line(im,'tilelight',[(left+1,148),(right-1,148)])
 im.save(R/'layers/doors-removed.png');allowed.save(R/'masks/doors-allowed.png');return im,allowed
def booth():
 im=blank()
 ellipse(im,(24,34,29,100),(145,189,227,201))
 # Wheels and structural plinth establish weight and floor contact.
 for x,y in [(166,195),(204,195),(214,189)]:
  ellipse(im,'black',(x-3,y-2,x+3,y+3));ellipse(im,'mid',(x-2,y-1,x+2,y+2));line(im,'light',[(x-1,y-1),(x+1,y-1)])
 poly(im,'deep',[(157,119),(161,114),(204,114),(217,109),(220,112),(220,187),(207,196),(157,196)])
 poly(im,'mid',[(205,117),(218,112),(218,185),(205,193)])
 poly(im,'sage',[(209,118),(216,114),(216,184),(209,188)])
 line(im,'silver',[(216,116),(216,182)])
 line(im,'shadow',[(210,126),(210,175)])
 poly(im,'silver',[(160,115),(173,110),(215,110),(205,116)])
 poly(im,'light',[(163,115),(173,111),(212,111),(204,115)])
 line(im,'shine',[(166,114),(175,111),(210,111)])
 line(im,'mid',[(178,111),(171,115)]);line(im,'mid',[(203,111),(197,115)])
 poly(im,'silver',[(158,120),(162,116),(203,116),(206,120),(206,191),(202,194),(158,194)])
 poly(im,'light',[(159,120),(163,117),(201,117),(204,120),(204,122),(162,122),(162,190),(159,192)])
 line(im,'shine',[(160,120),(163,118),(201,118),(204,120)])
 line(im,'shadow',[(205,123),(205,188)])
 # Open aperture: cool steel return, recessed rear panel and a fitted floor.
 rect(im,'deep',(163,124,201,188));rect(im,'dark',(166,126,200,185))
 poly(im,'shadow',[(166,126),(195,126),(195,177),(166,185)])
 poly(im,'mid',[(166,126),(171,130),(171,180),(166,185)])
 line(im,'sage',[(172,130),(194,130)]);line(im,'mid',[(188,131),(188,176)])
 poly(im,'silver',[(166,185),(195,177),(200,183),(200,188),(166,188)])
 line(im,'light',[(167,186),(198,184)]);line(im,'shadow',[(180,182),(180,187)])
 # The actual approved native porcelain fixture is reused, never resized.
 source=WC.crop((260,101,290,143)).convert('RGBA');mask=Image.new('L',source.size)
 points=[(4,1),(26,1),(28,4),(26,9),(26,18),(24,22),(28,23),(29,28),(27,34),(22,37),(23,40),(8,40),(8,37),(5,34),(2,30),(1,24),(5,21),(5,10),(2,9),(1,5),(1,2)]
 ImageDraw.Draw(mask).polygon(points,fill=255);source.putalpha(mask);im.alpha_composite(source,(169,144))
 source.save(R/'layers/native-approved-toilet-cutout.png');mask.save(R/'masks/approved-toilet-cutout-mask.png')
 # Small plate carries a warning pictogram; prose supplies the complete wording.
 rect(im,'gold',(158,136,162,143));rect(im,'goldlight',(159,137,161,142));line(im,'black',[(160,138),(160,140)]);rect(im,'black',(160,142,160,142))
 for y in [132,174]:
  rect(im,'deep',(157,y,162,y+3));rect(im,'silver',(158,y,161,y+2));line(im,'shine',[(159,y),(161,y)])
 line(im,'mid',[(207,170),(217,165)]);line(im,'light',[(207,171),(217,166)])
 line(im,'light',[(159,191),(202,191),(216,184)])
 # Open steel leaf projects toward the foreground, preserving a walkable entrance.
 poly(im,'deep',[(145,127),(158,122),(158,190),(145,198)])
 poly(im,'sage',[(146,128),(156,125),(156,189),(146,195)])
 poly(im,'silver',[(147,129),(154,127),(154,188),(147,192)])
 line(im,'light',[(146,129),(146,193)]);line(im,'shadow',[(155,130),(155,187)])
 line(im,'mid',[(148,153),(153,151)]);line(im,'light',[(148,154),(153,152)])
 line(im,'black',[(150,165),(152,164),(152,176),(150,177)],2)
 line(im,'light',[(151,165),(151,175)])
 im.save(R/'layers/lot61-open-pod.png');return im
def packed():
 im=blank();ellipse(im,(25,34,29,110),(175,192,216,201))
 poly(im,'deep',[(178,186),(183,182),(207,182),(214,186),(214,195),(210,198),(179,198),(177,195)])
 poly(im,'mid',[(211,187),(213,187),(213,194),(209,196),(209,189)])
 poly(im,'silver',[(179,187),(183,183),(207,183),(211,186),(208,189),(180,189)])
 poly(im,'light',[(182,186),(185,184),(204,184),(208,186),(206,187),(182,187)])
 line(im,'shine',[(183,185),(186,183),(204,183),(209,186)])
 poly(im,'sage',[(180,189),(209,189),(209,195),(181,196),(179,194)])
 line(im,'light',[(180,189),(208,189)]);line(im,'shadow',[(181,194),(208,194)])
 line(im,'silver',[(180,191),(180,194),(183,196),(207,196)])
 for x in [183,204]:
  rect(im,'gold',(x,189,x+2,193));line(im,'goldlight',[(x,189),(x+1,189),(x+1,191)]);rect(im,'deep',(x+1,192,x+1,193))
 line(im,'black',[(191,190),(191,193),(198,193),(199,190)],2)
 line(im,'silver',[(192,190),(192,192),(197,192)])
 im.save(R/'layers/lot61-packed-empty-case.png');return im
def composite(images):
 im=BASE.convert('RGBA')
 for x in images:im.alpha_composite(x)
 return im.convert('RGB')
def ora(name,images):
 root=ET.Element('image',{'w':'314','h':'206','name':name+' — UNSELECTED'});stack=ET.SubElement(root,'stack')
 with zipfile.ZipFile(R/'source'/f'{name}.ora','w')as z:
  z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
  for i,(title,im)in reversed(list(enumerate([('APPROVED MASTER — preserve',BASE)]+images))):
   f=io.BytesIO();im.save(f,format='PNG');dest=f'data/layer{i}.png';z.writestr(dest,f.getvalue());ET.SubElement(stack,'layer',{'name':title,'src':dest,'opacity':'1.0','visibility':'visible','composite-op':'svg:src-over','x':'0','y':'0'})
  f=io.BytesIO();composite([im for _,im in images]).save(f,format='PNG');z.writestr('mergedimage.png',f.getvalue());z.writestr('stack.xml',ET.tostring(root))
def main():
 door,door_allowed=doors();pod=booth();case=packed();layers={'doors-removed':door,'lot61-open-pod':pod,'lot61-packed-empty-case':case}
 pod_allowed=Image.new('L',SIZE);ImageDraw.Draw(pod_allowed).rectangle((144,109,227,202),fill=255);pod_allowed.save(R/'masks/pod-object-allowed.png')
 case_allowed=Image.new('L',SIZE);ImageDraw.Draw(case_allowed).rectangle((174,180,217,202),fill=255);case_allowed.save(R/'masks/case-object-allowed.png')
 protect=Image.new('L',SIZE);d=ImageDraw.Draw(protect)
 for box in [(0,86,92,173),(104,119,131,155),(258,122,274,158),(120,90,143,150),(226,85,255,154)]:d.rectangle(box,fill=255)
 protect.save(R/'masks/figures-furniture-protected.png')
 specs=[('lobby-doors-removed',['doors-removed'],door_allowed),('lot61-open',['doors-removed','lot61-open-pod'],ImageChops.lighter(door_allowed,pod_allowed)),('lot61-packed',['doors-removed','lot61-packed-empty-case'],ImageChops.lighter(door_allowed,case_allowed))]
 records=[]
 for name,names,allowed in specs:
  out=composite([layers[n]for n in names]);out.save(R/'native'/f'{name}.png')
  delta=ImageChops.difference(BASE,out);red,green,blue=delta.split();mask=ImageChops.lighter(ImageChops.lighter(red,green),blue).point(lambda v:255 if v else 0)
  assert not ImageChops.multiply(mask,ImageChops.invert(allowed)).getbbox()
  assert not ImageChops.multiply(mask,protect).getbbox()
  mask.save(R/'masks'/f'{name}-changed.png');allowed.save(R/'masks'/f'{name}-allowed.png');ora(name,[(n,layers[n])for n in names])
  records.append({'name':name,'file':f'native/{name}.png','dimensions':[314,206],'mode':'RGB','status':'UNSELECTED','sha256':hashlib.sha256((R/'native'/f'{name}.png').read_bytes()).hexdigest(),'layers':names,'changedPixels':sum(bool(v)for v in mask.get_flattened_data()),'changedMask':f'masks/{name}-changed.png','allowedMask':f'masks/{name}-allowed.png','outsideAllowedChanges':0,'protectedFigureOrFurnitureChanges':0,'editableSource':f'source/{name}.ora','runtimeBinding':None,'focusId':None})
 (R/'source/native-event-marks.json').write_text(json.dumps({'palette':P,'marks':MARKS,'toiletPixelCopy':{'source':'references/approved-restroom.png','crop':[260,101,290,143],'destination':[169,144],'resampling':False,'mask':'masks/approved-toilet-cutout-mask.png'},'generatedReferencePixelsUsed':False},indent=2)+'\n')
 (R/'evidence/native-build.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps([{'name':x['name'],'changedPixels':x['changedPixels']}for x in records]))
if __name__=='__main__':main()
