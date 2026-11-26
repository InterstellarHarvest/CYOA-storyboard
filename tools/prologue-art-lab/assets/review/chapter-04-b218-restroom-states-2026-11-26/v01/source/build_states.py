"""Localized conditional states from approved native masters, not R1 redraws.

Water marks are painted at the output grid. The raised enclosure reuses approved
native door/frame pixels by integer translation, with a small revealed-wall
plate, hatch and cables. Generated reference pixels are never read here.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,hashlib,zipfile,io,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
MAIN=Image.open(R/'references/approved-CH4-04.png').convert('RGB')
CLOSE=Image.open(R/'references/approved-CH4-B2-03.png').convert('RGB')
TAPE=[]
def poly(im,colour,pts):ImageDraw.Draw(im).polygon(pts,fill=colour);TAPE.append({'type':'polygon','colour':colour,'points':pts,'canvas':list(im.size)})
def line(im,colour,pts,w=1):ImageDraw.Draw(im).line(pts,fill=colour,width=w);TAPE.append({'type':'line','colour':colour,'points':pts,'width':w,'canvas':list(im.size)})
def blank(size=(314,206)):return Image.new('RGBA',size)
def figmask():
 m=Image.new('L',MAIN.size);d=ImageDraw.Draw(m)
 d.polygon([(45,124),(51,123),(58,127),(63,133),(63,139),(69,144),(72,154),(71,162),(75,172),(79,181),(75,184),(63,185),(60,175),(58,175),(58,183),(51,187),(40,186),(40,179),(42,173),(39,165),(37,158),(32,151),(29,144),(24,142),(24,133),(29,131),(36,133),(41,137),(43,136),(42,131)],fill=255)
 d.polygon([(99,120),(109,117),(116,119),(120,125),(120,131),(125,134),(125,143),(126,150),(123,156),(129,159),(128,164),(119,165),(114,159),(111,164),(98,165),(95,162),(98,155),(98,150),(95,145),(94,139),(90,137),(87,133),(90,129),(96,130),(99,133),(99,127)],fill=255)
 return m
FIG=figmask();FIG.save(R/'masks/main-source-figures-protected.png')
FLOOR=Image.new('L',MAIN.size);ImageDraw.Draw(FLOOR).polygon([(0,174),(139,146),(314,146),(314,206),(0,206)],fill=255)
ALLOWED=FLOOR.copy();ImageDraw.Draw(ALLOWED).polygon([(63,123),(102,123),(134,129),(138,175),(96,193),(60,191)],fill=255)
ALLOWED=ImageChops.multiply(ALLOWED,ImageChops.invert(FIG));ALLOWED.save(R/'masks/main-water-allowed.png')
def protect(im,allowed=ALLOWED):
 im.putalpha(ImageChops.multiply(im.getchannel('A'),allowed));return im
def wet_floor():
 im=blank()
 poly(im,(105,142,135,69),[(61,176),(89,168),(116,165),(141,167),(159,172),(183,174),(197,180),(187,185),(170,189),(144,189),(125,194),(99,193),(83,197),(63,193),(54,188)])
 poly(im,(151,177,164,61),[(76,177),(103,172),(134,173),(151,177),(175,179),(178,182),(162,185),(135,184),(116,189),(88,188),(72,190),(63,187)])
 line(im,(200,215,191,157),[(61,181),(70,178),(86,178)],1)
 line(im,(199,218,207,150),[(123,190),(140,187),(158,187)],1)
 line(im,(184,210,203,150),[(165,178),(180,180),(186,182)],1)
 line(im,(68,105,98,105),[(81,194),(95,191),(111,192)],1)
 line(im,(224,226,193,134),[(108,176),(120,175),(133,176)],1)
 return protect(im)
def main_jet(double=False):
 im=blank();w=4 if double else 3
 line(im,(89,141,139,174),[(128,134),(115,130),(100,128),(84,129),(69,132)],w)
 line(im,(191,220,210,227),[(128,133),(113,129),(99,127),(85,128),(71,131)],2 if double else 1)
 line(im,(236,243,213,232),[(119,131),(109,129),(99,128),(90,129)],1)
 poly(im,(197,222,211,207),[(69,130),(65,131),(63,134),(68,136),(73,134),(78,135),(74,132)])
 line(im,(133,181,175,158),[(72,135),(79,143),(89,151),(101,162),(116,174)],3 if double else 2)
 line(im,(219,235,216,219),[(73,136),(80,144),(90,153),(101,163),(112,171)],1)
 for pts in [[(81,138),(84,140)],[(87,145),(90,147)],[(97,151),(99,154)],[(106,159),(109,161)],[(116,167),(119,169)],[(119,173),(124,174),(129,173)]]:line(im,(214,233,221,190),pts)
 if double:
  line(im,(176,213,206,199),[(125,136),(112,136),(95,135),(80,136),(70,137)],2)
  line(im,(225,237,215,207),[(129,139),(135,143),(137,149)],1)
 return protect(im)
def dribble():
 im=blank()
 line(im,(129,175,164,150),[(128,134),(130,138),(130,143),(132,148)],1)
 for y in [137,144,151,155]:line(im,(219,231,204,185),[(131,y),(131,y+1)])
 line(im,(190,213,192,152),[(127,159),(132,160),(137,159)])
 return protect(im)
def flood_floor():
 im=blank()
 poly(im,(94,137,133,110),[(0,174),(139,146),(314,146),(314,206),(0,206)])
 poly(im,(125,165,156,98),[(140,150),(204,151),(217,156),(280,160),(314,167),(314,182),(254,175),(231,177),(184,166),(145,167),(107,179),(80,177)])
 poly(im,(154,180,163,77),[(0,193),(66,178),(108,181),(160,171),(199,173),(221,181),(286,184),(314,193),(314,206),(0,206)])
 for pts in [[(0,197),(29,192),(52,193),(69,188)],[(84,176),(106,172),(121,173)],[(134,157),(158,155),(179,157)],[(183,167),(208,168),(226,166)],[(235,154),(252,155),(272,154)],[(260,180),(280,181),(300,178)],[(117,199),(145,195),(170,196),(190,192)],[(212,201),(240,198),(262,200)],[(34,203),(58,200),(75,201)]]:
  line(im,(202,223,207,165),pts,1)
 for pts in [[(23,190),(47,183),(72,184)],[(138,183),(159,180),(185,181)],[(280,192),(299,189),(314,191)],[(95,205),(124,202)]]:line(im,(56,101,96,112),pts,1)
 # Warm strip reflections retain the established ceiling-light direction.
 poly(im,(233,225,184,90),[(146,152),(154,152),(162,156),(149,156)])
 poly(im,(233,225,184,80),[(244,151),(251,151),(263,157),(251,157)])
 return protect(im)
def close_jet():
 im=blank(CLOSE.size)
 line(im,(91,138,132,190),[(196,228),(184,225),(168,224),(153,227),(144,230)],4)
 line(im,(208,228,211,220),[(196,227),(183,224),(168,223),(154,226),(145,229)],2)
 line(im,(247,245,211,220),[(189,225),(180,224),(170,224),(162,225)],1)
 poly(im,(211,231,213,212),[(145,227),(140,229),(139,232),(143,234),(148,232),(151,233),(148,229)])
 line(im,(115,167,157,159),[(145,232),(150,243),(159,255),(174,267),(188,277)],3)
 line(im,(218,234,213,191),[(147,234),(152,245),(160,255),(175,268),(184,274)],1)
 for pts in [[(154,237),(156,240)],[(158,246),(161,248)],[(168,252),(170,255)],[(177,260),(180,262)],[(189,269),(192,272)]]:line(im,(222,237,216,180),pts)
 poly(im,(107,154,144,76),[(171,277),(190,269),(211,263),(235,265),(259,271),(274,277)])
 line(im,(207,224,203,150),[(196,273),(213,270),(228,271)])
 allowed=Image.new('L',CLOSE.size);ImageDraw.Draw(allowed).polygon([(136,220),(201,218),(204,240),(194,256),(276,277),(276,278),(162,278),(138,242)],fill=255)
 allowed.save(R/'masks/close-water-allowed.png');return protect(im,allowed)

def stall_overlay():
 """Approved native pixel relocation; no generated source is resized here."""
 im=blank();allowed=Image.new('L',MAIN.size);ad=ImageDraw.Draw(allowed)
 ad.rectangle((251,61,313,145),fill=255);ad.rectangle((251,39,313,103),fill=255)
 ad.polygon([(247,29),(308,29),(313,38),(313,45),(234,46),(234,39)],fill=255)
 toilet=Image.new('L',MAIN.size);ImageDraw.Draw(toilet).rectangle((260,102,289,142),fill=255)
 allowed=ImageChops.multiply(allowed,ImageChops.invert(toilet));allowed.save(R/'masks/stall-lift-allowed.png');toilet.save(R/'masks/toilet-grounded-protected.png')
 px=im.load();src=MAIN.load()
 # Newly exposed tile behind the removed jambs, copied at the same native scale.
 for y in range(79,145):
  for x in range(251,257):px[x,y]=(*src[258,y],255)
  for x in range(291,314):px[x,y]=(*src[258,y],255)
 for y in range(69,79):
  for x in range(251,314):px[x,y]=(*src[x,y-20],255)
 for y in range(62,69):
  for x in range(301+(69-y)//3,314):px[x,y]=(*src[292+(x%7),y],255)
 # Closed green door and its trim are an integer-translated approved neighbour.
 part=MAIN.crop((200,76,247,141)).convert('RGBA');im.paste(part,(259,36))
 # A narrow side return gives the original front-plane door believable depth.
 poly(im,(48,70,57,255),[(252,47),(259,42),(259,101),(252,105)])
 poly(im,(65,87,69,255),[(253,49),(257,46),(257,101),(253,103)])
 line(im,(128,143,112,255),[(252,47),(258,43)])
 # Native right jamb retained from the original open bay, translated vertically.
 part=MAIN.crop((304,78,314,144)).convert('RGBA');im.paste(part,(304,36))
 # Clip the hidden upper portion as the enclosure passes through the ceiling.
 ImageDraw.Draw(im).rectangle((251,29,313,40),fill=(0,0,0,0))
 poly(im,(86,97,77,255),[(246,31),(306,30),(313,37),(237,44)])
 poly(im,(31,52,43,255),[(248,33),(305,32),(309,37),(241,42)])
 line(im,(155,153,116,255),[(246,31),(306,30),(313,37)],1)
 line(im,(193,186,139,255),[(237,44),(313,37)],1)
 line(im,(44,68,54,255),[(238,45),(313,38)],1)
 # Four taut cables; their attachment positions share the hatch/box depth order.
 for start,end in [((249,34),(253,46)),((263,34),(266,43)),((293,33),(298,42)),((307,33),(309,42))]:
  line(im,(43,56,47,255),[start,end],2)
  line(im,(206,210,177,255),[start,end],1)
  x,y=start;poly(im,(193,172,111,255),[(x-1,y-1),(x+1,y-1),(x+1,y+1),(x-1,y+1)])
 im.putalpha(ImageChops.multiply(im.getchannel('A'),allowed));return im

def composite(base,images):
 im=base.convert('RGBA')
 for layer in images:im.alpha_composite(layer)
 return im.convert('RGB')
def save_ora(name,base,images):
 root=ET.Element('image',{'w':str(base.width),'h':str(base.height),'name':name+' — UNSELECTED'});stack=ET.SubElement(root,'stack')
 with zipfile.ZipFile(R/'source'/f'{name}.ora','w')as z:
  z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
  for idx,(label,img)in reversed(list(enumerate([('APPROVED MASTER — preserve',base)]+images))):
   b=io.BytesIO();img.save(b,format='PNG');path=f'data/layer{idx}.png';z.writestr(path,b.getvalue());ET.SubElement(stack,'layer',{'name':label,'src':path,'opacity':'1.0','visibility':'visible','composite-op':'svg:src-over','x':'0','y':'0'})
  b=io.BytesIO();composite(base,[im for _,im in images]).save(b,format='PNG');z.writestr('mergedimage.png',b.getvalue());z.writestr('stack.xml',ET.tostring(root))
def main():
 layers={'main-wet-floor':wet_floor(),'main-active-jet':main_jet(),'main-dribble':dribble(),'main-flood-floor':flood_floor(),'main-flood-jet':main_jet(True),'close-active-leak':close_jet(),'main-stall-lift':stall_overlay()}
 for name,im in layers.items():im.save(R/'layers'/f'{name}.png')
 specs=[('restroom-active-leak-main',MAIN,['main-wet-floor','main-active-jet'],'main-water-allowed.png'),('restroom-active-leak-close',CLOSE,['close-active-leak'],'close-water-allowed.png'),('restroom-braced-main',MAIN,['main-wet-floor','main-dribble'],'main-water-allowed.png'),('restroom-contained-main',MAIN,['main-wet-floor'],'main-water-allowed.png'),('restroom-flood-onset-main',MAIN,['main-flood-floor','main-flood-jet'],'main-water-allowed.png'),('restroom-stall-lifting-main',MAIN,['main-wet-floor','main-stall-lift'],None)]
 records=[]
 for name,base,names,mask in specs:
  images=[layers[n]for n in names];out=composite(base,images);path='native/'+name+'.png';out.save(R/path)
  if mask:allowed=Image.open(R/'masks'/mask)
  else:allowed=ImageChops.lighter(ALLOWED,Image.open(R/'masks/stall-lift-allowed.png'))
  allowed.save(R/'masks'/f'{name}-allowed.png')
  diff=ImageChops.difference(base,out);rs,gs,bs=diff.split();changed=ImageChops.lighter(ImageChops.lighter(rs,gs),bs).point(lambda v:255 if v else 0)
  changed.save(R/'masks'/f'{name}-changed.png');assert not ImageChops.multiply(changed,ImageChops.invert(allowed)).getbbox()
  if base.size==MAIN.size:assert not ImageChops.multiply(changed,FIG).getbbox()
  if 'stall' in name:assert not ImageChops.multiply(changed,Image.open(R/'masks/toilet-grounded-protected.png')).getbbox()
  save_ora(name,base,list(zip(names,images)))
  records.append({'file':path,'name':name,'status':'UNSELECTED','dimensions':list(out.size),'mode':out.mode,'sha256':hashlib.sha256((R/path).read_bytes()).hexdigest(),'base':'references/approved-CH4-04.png'if base.size==MAIN.size else'references/approved-CH4-B2-03.png','layers':names,'allowedMask':f'masks/{name}-allowed.png','changedMask':f'masks/{name}-changed.png','changedPixels':sum(bool(v)for v in changed.get_flattened_data()),'changedBounds':changed.getbbox(),'outsideAllowedChanges':0,'originalNPCChanges':0 if base.size==MAIN.size else None,'editableSource':'source/'+name+'.ora'})
 # Composability evidence only, not another primary state or runtime binding.
 composite(MAIN,[layers['main-wet-floor'],layers['main-dribble'],layers['main-stall-lift']]).save(R/'comparisons/lifting-over-braced-proof.png')
 (R/'evidence/native-state-build.json').write_text(json.dumps(records,indent=2)+'\n')
 (R/'source/native-event-marks.json').write_text(json.dumps({'canvasSizes':[[314,206],[564,278]],'newWaterAndHatchMarks':TAPE,'nativePixelCopies':'See stall_overlay() in build_states.py: approved source boxes only, integer translation, no resizing.','generatedReferencePixelsUsed':False},indent=2)+'\n')
 print(json.dumps([{'name':x['name'],'changedPixels':x['changedPixels']}for x in records]))
if __name__=='__main__':main()
