"""Source-derived native corridor interpretation, not independent authorship.

Native silhouettes, structural profiles, door/window apertures, stair planes,
lettering, lamps, supports and state changes are painted on blank314x206 layers.
Reference-informed local material fields support these forms; source-derived
contours and lighting remain. No claim of a wholly independent native painting.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
from collections import Counter
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];SIZE=(314,206)
R={
 'plaster':['#615647','#81705a','#a28b6c','#bca07b','#cfb28a','#dfc49c','#ecd4aa'],
 'green':['#27362f','#3a483c','#4c5c48','#64715a','#7c8469','#969779','#b3af8a'],
 'blue':['#202e32','#2c4249','#3b5661','#4b6773','#617c83','#879696'],
 'wood':['#241f1b','#3c2d24','#554132','#72563e','#907055','#af8d66'],
 'steel':['#1f2a29','#34423e','#4c5951','#647065','#7b8574','#a5ad94','#c7c8a7'],
 'carpet':['#352627','#4b292e','#65323a','#7a3c44','#91494e','#a05b5a'],
 'brass':['#453a26','#74603a','#a3864e','#c8a263','#e0c28a','#f1db9e']}
def blank():return Image.new('RGBA',SIZE)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rgb(s):return tuple(bytes.fromhex(s[1:]))
def mask(points):
 m=Image.new('L',SIZE);ImageDraw.Draw(m).polygon(points,fill=255);return m
def main():
 source=ROOT/'originals/CH4-NEW-04-pixel-friendly-study.png'
 guide=Image.open(source).convert('RGB').resize(SIZE,Image.Resampling.NEAREST)
 guide.save(ROOT/'diagnostics/source-transfer-NOT-FINAL.png')
 layers=[];regions=[];quiet=[0]
 def material(points,name):
  """An independently specified silhouette with a local material shade field.
  Reference colors choose among a purposeful local ramp, never enter as RGB.
  Native contours, moldings and important edges are illustrated separately.
  """
  m=mask(points);out=blank();pal=[rgb(s)for s in R[name]];data=[]
  for c,a in zip(guide.get_flattened_data(),m.get_flattened_data()):data.append(min(pal,key=lambda p:sum((x-y)**2 for x,y in zip(c,p)))+(255,)if a else(0,0,0,0))
  prior=data[:]
  for y in range(1,205):
   for x in range(1,313):
    i=y*314+x;c=prior[i]
    if not c[3]:continue
    near=[prior[j]for j in [i-1,i+1,i-314,i+314]if prior[j][3]]
    if len(near)<3:continue
    v,n=Counter(near).most_common(1)[0]
    if n>=3 and c not in near and sum((a-b)**2 for a,b in zip(c[:3],v[:3]))<3000:data[i]=v;quiet[0]+=1
  out.putdata(data);regions.append({'material':name,'nativeSilhouette':points});return out
 def add(name,im):im.save(ROOT/'layers'/(name+'.png'));layers.append(name)
 # Large architectural planes establish one consistent corridor camera.
 room=blank();d=ImageDraw.Draw(room);d.rectangle((0,0,313,205),fill='#615647')
 room.alpha_composite(material([(0,0),(111,0),(119,51),(128,150),(0,205)],'plaster'))
 room.alpha_composite(material([(107,0),(252,0),(239,54),(115,54)],'plaster'))
 room.alpha_composite(material([(237,0),(313,0),(313,205),(231,151)],'plaster'))
 # The passage behind the arch recedes toward the stair landing.
 room.alpha_composite(material([(123,55),(164,65),(165,145),(123,156)],'plaster'))
 room.alpha_composite(material([(165,58),(214,54),(213,94),(179,94)],'plaster'))
 d=ImageDraw.Draw(room)
 for pts,c in [([(117,54),(127,54),(151,71),(165,72)],'#4c4538'), ([(126,56),(129,56),(153,73),(162,73)],'#a28b6c'), ([(109,0),(119,0),(137,15),(185,15)],'#34423e')]:d.polygon(pts,fill=c)
 d.line([(117,52),(166,53),(233,53)],fill='#dfc49c');d.line([(116,54),(234,54)],fill='#615647')
 # Existing architecture carries cracks at joints and broken plaster margins.
 for pts in [[(4,40),(6,46),(5,53),(8,58),(7,63)],[(42,16),(39,19),(41,22)],[(112,67),(109,75),(110,82),(107,86),(105,95)],[(251,16),(249,22),(247,23),(245,30)],[(242,86),(245,92),(244,99)]]:d.line(pts,fill='#81705a')
 d.polygon([(78,96),(81,94),(84,96),(85,99),(90,99),(92,102),(78,101)],fill='#9a7052');d.line([(79,95),(83,95),(85,98)],fill='#cfb28a')
 add('01-architecture-plaster',room)
 carpetmask=mask([(0,205),(127,149),(164,130),(168,151),(230,151),(258,171),(313,199),(313,205)])
 carpet=material([(0,205),(127,149),(164,130),(168,151),(230,151),(258,171),(313,199),(313,205)],'carpet');d=ImageDraw.Draw(carpet)
 # Curated connected wear, not a stippled field. Keep the central floor quiet.
 for pts,c in [([(30,200),(86,177),(108,177),(54,198)],'#7a3c44'), ([(110,183),(155,172),(180,172),(151,180)],'#7a3c44'), ([(165,204),(213,190),(242,194),(234,199),(200,202)],'#65323a'), ([(218,169),(243,170),(273,186),(257,186)],'#91494e'), ([(120,156),(141,151),(154,151),(145,155)],'#4b292e')]:d.polygon(pts,fill=c)
 d.line([(3,205),(126,151),(160,138)],fill='#a3864e');d.line([(259,173),(312,201)],fill='#c8a263')
 for x,y in [(36,191),(54,183),(79,173),(96,165),(119,155),(273,181),(280,186),(294,194)]:d.line([(x,y),(x+2,y)],fill='#c8a263')
 add('02-carpet-floor',carpet);carpetmask.save(ROOT/'masks/carpet-floor.png')
 panel=blank()
 for pts in [[(0,91),(126,106),(126,151),(0,206)],[(126,106),(164,109),(164,140),(126,153)],[(231,107),(259,106),(259,172),(231,154)]]:panel.alpha_composite(material(pts,'green'))
 d=ImageDraw.Draw(panel)
 def trim(points,shadow='#27362f',mid='#7c8469',light='#b3af8a'):
  d.line(points,fill=shadow,width=4);d.line(points,fill=mid,width=2);d.line([(x,y-1)for x,y in points],fill=light)
 trim([(0,92),(126,107),(164,110)]);trim([(231,108),(259,107)])
 trim([(0,202),(126,151),(164,138)],mid='#64715a',light='#969779');trim([(231,153),(259,171)],mid='#64715a',light='#969779')
 for pts in [[(74,114),(83,114),(83,169),(74,173),(74,114)],[(116,110),(122,110),(122,150),(116,153),(116,110)],[(242,114),(252,114),(252,162),(242,157),(242,114)],[(132,114),(138,114),(138,140),(132,143),(132,114)]]:
  d.line(pts,fill='#27362f',width=2);d.line([(x+1,y+1)for x,y in pts[:-1]],fill='#969779')
 add('03-painted-paneling',panel)
 doors=blank();d=ImageDraw.Draw(doors)
 # Substantial foreground STAFF door: independently drawn bevels and planes.
 outer=[(7,0),(72,36),(72,182),(7,206)];leaf=[(18,24),(64,43),(64,178),(18,198)]
 doors.alpha_composite(material(outer,'green'));doors.alpha_composite(material(leaf,'blue'));d=ImageDraw.Draw(doors)
 for pts,c,w in [([(10,0),(10,204)],'#a5ad94',2), ([(13,5),(69,37),(69,181)],'#27362f',3), ([(15,9),(67,39),(67,180),(15,201)],'#969779',1), ([(18,24),(64,43),(64,178),(18,198),(18,24)],'#202e32',2), ([(21,30),(59,46),(59,111),(21,114),(21,30)],'#202e32',2), ([(22,32),(58,47),(58,110)],'#617c83',1), ([(21,129),(59,128),(59,173),(21,188),(21,129)],'#202e32',2), ([(23,131),(57,130)],'#617c83',1), ([(23,186),(57,173)],'#879696',1)]:d.line(pts,fill=c,width=w)
 # Chipped paint follows exposed jambs/panel edges, not random noise.
 for pts in [[(24,34),(26,35),(26,38),(25,37)],[(59,48),(61,49),(61,52),(60,51)],[(24,111),(28,111),(28,113),(24,114)],[(55,128),(59,126),(59,128),(55,130)],[(21,178),(23,177),(23,181),(21,183)],[(36,182),(41,180),(42,181),(37,184)],[(61,154),(62,153),(62,159),(61,160)]]:d.polygon(pts,fill='#a3864e')
 for yy in [58,155]:
  d.rectangle((63,yy,65,yy+9),fill='#453a26');d.line([(64,yy+1),(64,yy+8)],fill='#e0c28a');d.line([(63,yy+4),(65,yy+4)],fill='#74603a')
 d.polygon([(20,112),(25,112),(25,135),(20,136)],fill='#74603a');d.line([(21,113),(24,113),(24,134)],fill='#e0c28a')
 d.ellipse((22,119,25,122),fill='#453a26');d.line([(24,120),(33,119)],fill='#e0c28a',width=2);d.line([(25,122),(32,121)],fill='#74603a')
 # Hand-built chunky lettering projected onto the door's perspective plane.
 plaque=[(31,64),(53,69),(53,79),(31,75)];d.polygon(plaque,fill='#a3864e');d.line([plaque[0],plaque[1],plaque[2]],fill='#e0c28a')
 glyph={'S':['111','100','111','001','111'],'T':['111','010','010','010','010'],'A':['010','101','111','101','101'],'F':['111','100','110','100','100']}
 x=33
 for ch in 'STAFF':
  for yy,row in enumerate(glyph[ch]):
   for xx,b in enumerate(row):
    if b=='1':d.point((x+xx,67+yy+(x-33)//5),fill='#241f1b')
  x+=4
 # Two receding guest-door silhouettes belong to the passage, not new routes.
 for pts in [[(131,77),(141,85),(141,143),(131,148)],[(149,86),(154,91),(154,135),(149,138)]]:
  doors.alpha_composite(material(pts,'wood'));d=ImageDraw.Draw(doors);d.line(pts+[pts[0]],fill='#241f1b',width=2);d.line([(pts[0][0]+2,pts[0][1]+3),(pts[1][0]-1,pts[1][1]+2),(pts[2][0]-1,pts[2][1]-2)],fill='#907055')
  x,y=pts[1];d.line([(x-1,y+27),(x+1,y+27)],fill='#c8a263');d.point((x-1,y+29),fill='#74603a')
 add('04-doors-and-lettering',doors)
 # The outside remains a secondary bright aperture, not another full scene.
 exit=blank();d=ImageDraw.Draw(exit)
 d.polygon([(264,47),(313,17),(313,201),(263,173)],fill='#c4d9d1')
 d.polygon([(268,81),(313,70),(313,132),(268,134)],fill='#d7cbb0');d.polygon([(269,89),(313,78),(313,84),(269,95)],fill='#81705a')
 d.polygon([(268,134),(313,130),(313,194),(266,172)],fill='#cfc5aa')
 for pts in [[(269,148),(313,148)],[(274,166),(313,170)],[(292,135),(287,182)]]:d.line(pts,fill='#a28b6c')
 d.rectangle((293,108,313,130),fill='#907055');d.rectangle((295,110,309,127),outline='#cfb28a');d.line([(295,110),(309,127)],fill='#cfb28a');d.line([(309,110),(295,127)],fill='#cfb28a')
 # Daylight through a modest yard glimpse; no new external destination/props.
 exit.alpha_composite(material([(255,42),(313,8),(313,23),(269,50),(269,172),(313,194),(313,205),(255,176)],'green'));d=ImageDraw.Draw(exit)
 d.line([(257,43),(310,13)],fill='#969779');d.line([(260,45),(310,17)],fill='#27362f',width=2);d.line([(262,47),(262,171)],fill='#b3af8a',width=2)
 d.line([(266,49),(266,171)],fill='#27362f',width=2);d.line([(269,51),(269,172)],fill='#dfc49c')
 for yy in [73,148]:d.rectangle((268,yy,270,yy+7),fill='#74603a');d.line([(269,yy),(269,yy+6)],fill='#e0c28a')
 d.polygon([(267,172),(308,192),(313,201),(258,175)],fill='#cfb28a');d.line([(267,173),(313,198)],fill='#615647')
 add('05-side-exit',exit)
 stairs=blank();d=ImageDraw.Draw(stairs)
 # One coherent ascending flight viewed frontally: wider at its near foot,
 # narrower at its higher landing; treads and both rails share that geometry.
 d.polygon([(177,88),(213,88),(232,151),(165,151)],fill='#1f2a29')
 d.polygon([(180,72),(211,72),(212,91),(177,91)],fill='#64715a');d.line([(178,91),(213,91)],fill='#a3864e')
 ys=[(92,96),(98,102),(104,108),(111,115),(118,122),(126,130),(134,138),(143,147)]
 for i,(y,z)in enumerate(ys):
  left=178-(y-92)//5;right=213+(y-92)//3
  d.polygon([(left,y),(right,y),(right+1,z),(left-1,z)],fill='#4c5951');d.line([(left,z),(right,z)],fill='#c8a263');d.line([(left,z+1),(right+1,z+1)],fill='#1f2a29',width=2)
  # A few broad grip groups show steel tread material without tiny lattices.
  for xx in range(left+4,right-2,7):d.line([(xx,y+1),(xx+2,y+2)],fill='#7b8574')
 def pipe(pts,w=2):
  d.line(pts,fill='#1f2a29',width=w+2);d.line(pts,fill='#7b8574',width=w);d.line([(x-1,y)for x,y in pts],fill='#c7c8a7')
 pipe([(168,119),(179,63)],2);pipe([(230,119),(211,63)],2)
 for x,y,foot in [(168,119,149),(174,89,120),(179,63,92),(230,119,149),(220,89,120),(211,63,92)]:pipe([(x,y),(x,foot)],1)
 d.line([(168,149),(230,149)],fill='#81705a');d.line([(167,151),(231,151)],fill='#27362f')
 # Glass blocks in the landing wall, with grouped highlights, not noise.
 d.rectangle((197,56,212,70),fill='#81705a')
 for yy in [57,62,67]:
  for xx in [198,203,208]:d.rectangle((xx,yy,xx+3,yy+3),fill='#d9d6b9');d.line([(xx,yy+2),(xx+2,yy)],fill='#f0e6c3');d.point((xx+3,yy+3),fill='#a5ad94')
 add('06-collection-stairs',stairs)
 arch=blank();d=ImageDraw.Draw(arch)
 for pts in [[(116,49),(128,49),(128,58),(125,61),(125,152),(118,156),(118,68),(116,67)],[(229,49),(239,49),(239,65),(235,66),(235,155),(229,151),(229,65),(226,60)],[(116,48),(239,48),(239,53),(116,53)]]:arch.alpha_composite(material(pts,'plaster'))
 d=ImageDraw.Draw(arch)
 for pts,c,w in [([(117,49),(237,49)],'#dfc49c',1), ([(118,51),(236,51)],'#615647',2), ([(120,67),(120,154)],'#cfb28a',2), ([(232,66),(232,152)],'#615647',2), ([(117,55),(128,55),(132,58)],'#bca07b',2), ([(224,57),(229,55),(237,55)],'#bca07b',2), ([(117,66),(126,66)],'#dfc49c',1), ([(230,65),(238,65)],'#dfc49c',1)]:d.line(pts,fill=c,width=w)
 add('07-arch-and-pilasters',arch)
 hatch=blank();d=ImageDraw.Draw(hatch)
 d.polygon([(87,120),(111,116),(111,161),(87,172)],fill='#27362f')
 hatch.alpha_composite(material([(89,122),(109,119),(109,160),(89,169)],'green'));d=ImageDraw.Draw(hatch)
 d.line([(87,120),(111,116),(111,161)],fill='#b3af8a');d.line([(89,122),(109,119),(109,160)],fill='#3a483c')
 for yy in [127,155]:d.rectangle((89,yy,90,yy+4),fill='#c8a263');d.point((89,yy+1),fill='#74603a')
 d.rectangle((106,140,107,145),fill='#74603a');d.point((107,142),fill='#27362f')
 for pts in [[(90,165),(92,162),(93,166)],[(95,165),(97,162),(98,163)],[(106,120),(108,119),(108,122)]]:d.polygon(pts,fill='#a3864e')
 add('08-hatch-closed',hatch)
 lamps=blank();d=ImageDraw.Draw(lamps)
 for x,y,s in [(85,55,1),(247,71,0)]:
  w=5 if s else 4;h=10 if s else 8
  d.ellipse((x-8,y+8,x-2,y+17),fill='#74603a');d.line([(x-5,y+11),(x-5,y+16),(x,y+16),(x+1,y+h+2)],fill='#c8a263',width=2)
  d.polygon([(x-w,y),(x+w,y),(x+w-1,y+h),(x-w+1,y+h)],fill='#c8a263');d.line([(x-w,y),(x+w,y)],fill='#453a26')
  d.polygon([(x-w+1,y+1),(x+w-1,y+1),(x+w-2,y+h-1),(x-w+2,y+h-1)],fill='#f1db9e');d.line([(x-1,y+2),(x,y+h-1)],fill='#fff0c2')
  d.line([(x-2,y+h+1),(x+2,y+h+1)],fill='#74603a',width=2)
 d.ellipse((153,74,162,77),fill='#74603a');d.ellipse((155,75,160,77),fill='#f1db9e')
 add('09-lamps',lamps)
 duct=blank();duct.alpha_composite(material([(63,0),(124,0),(131,12),(219,12),(236,19),(243,30),(243,42),(232,46),(219,40),(128,40),(114,37),(102,29),(67,16)],'steel'));d=ImageDraw.Draw(duct)
 for pts,c,w in [([(65,1),(96,1),(99,14),(110,27),(121,32),(229,32)],'#a5ad94',2), ([(69,17),(103,29),(115,36),(127,39),(221,39)],'#34423e',3), ([(126,13),(127,37)],'#27362f',3), ([(129,13),(130,37)],'#a5ad94',1), ([(160,12),(160,39)],'#27362f',3), ([(162,13),(162,38)],'#7b8574',1), ([(221,14),(222,35)],'#27362f',3), ([(222,15),(223,34)],'#a5ad94',1), ([(105,0),(105,17),(111,29),(120,34)],'#34423e',2)]:d.line(pts,fill=c,width=w)
 for x in [129,160,222]:
  for y in [16,34]:d.point((x,y),fill='#c8a263')
 d.polygon([(196,31),(225,31),(222,41),(194,41)],fill='#27362f');d.line([(196,31),(225,31),(222,41),(194,41),(196,31)],fill='#a5ad94')
 for yy in [33,35,37,39]:d.line([(197,yy),(222-(yy-33)//3,yy)],fill='#a3864e')
 d.polygon([(66,0),(72,0),(72,6),(99,6),(99,9),(72,9),(72,28),(68,28)],fill='#27362f');d.line([(70,1),(70,25),(96,8)],fill='#7b8574')
 for x,y in [(70,4),(70,21),(94,8)]:d.point((x,y),fill='#c8a263')
 add('10-duct-and-mounts',duct)
 def assemble(names):
  im=blank()
  for n in names:im=Image.alpha_composite(im,Image.open(ROOT/'layers'/(n+'.png')).convert('RGBA'))
  return im.convert('RGB')
 drynames=layers[:];dry=assemble(drynames);drypath=ROOT/'native/CH4-NEW-04-public-corridor-v01.png';dry.save(drypath);dry.resize((1256,824),Image.Resampling.NEAREST).save(ROOT/'previews/CH4-NEW-04-public-corridor-v01-4x.png')
 # A strictly localized state: dry geometry is the base; only floor/hatch/NPC
 # and sign pixels may differ. No new scene key, Focus ID or runtime binding.
 water=blank();d=ImageDraw.Draw(water)
 d.polygon([(0,205),(127,149),(164,130),(168,151),(230,151),(258,171),(313,199),(313,205)],fill='#526d67')
 for pts,c in [([(0,205),(95,174),(137,168),(126,174),(49,201)],'#70867a'), ([(90,199),(165,174),(191,177),(175,185),(119,202)],'#3d5957'), ([(171,201),(214,184),(232,184),(245,191),(224,195)],'#70867a'), ([(128,157),(151,146),(163,145),(157,152),(143,155)],'#798b78'), ([(240,174),(259,176),(285,190),(263,188)],'#a8b4a0'), ([(210,164),(229,162),(243,167),(229,170)],'#798b78'), ([(77,204),(95,198),(109,198),(98,203)],'#90a399'), ([(154,164),(175,161),(194,161),(183,164)],'#344e4d')]:d.polygon(pts,fill=c)
 for pts,c in [([(34,195),(56,190),(65,190)],'#b5c0a6'), ([(105,188),(130,182),(141,182)],'#90a399'), ([(177,193),(190,190),(209,191)],'#b5c0a6'), ([(227,180),(241,180),(251,182)],'#90a399'), ([(141,161),(153,158),(161,158)],'#b5c0a6'), ([(279,195),(293,197),(301,201)],'#d2cbb0'), ([(91,199),(105,197)],'#314c4c')]:d.line(pts,fill=c)
 # Water follows the open floor and spreads under door thresholds only.
 water.putalpha(ImageChops.multiply(water.getchannel('A'),carpetmask))
 # Shallow water retains the carpet's broad native shade groups. A fixed
 # blend of controlled ramps bounds the wet-surface palette.
 water=Image.blend(dry.convert('RGBA'),water,0.62);water.putalpha(carpetmask);d=ImageDraw.Draw(water)
 for pts,c in [([(83,184),(91,181),(95,181),(91,184)],'#a79f7b'), ([(76,190),(86,186),(91,186),(85,190)],'#8d927b'), ([(73,197),(83,193),(90,193),(81,197)],'#a79f7b'), ([(255,189),(263,189),(281,198),(273,198)],'#bec0a3'), ([(247,194),(254,195),(261,201),(254,200)],'#a5b0a0')]:d.polygon(pts,fill=c)
 for pts,c in [([(118,169),(129,167),(139,169),(145,168)],'#90a399'), ([(123,173),(134,171),(147,173)],'#70867a'), ([(145,191),(153,194),(166,192),(174,194)],'#b5c0a6'), ([(152,198),(163,196),(178,197)],'#90a399'), ([(58,198),(68,195)],'#b5c0a6'), ([(190,182),(201,182),(211,184)],'#90a399')]:d.line(pts,fill=c)
 water.putalpha(carpetmask);add('state-water',water)
 opened=blank();d=ImageDraw.Draw(opened)
 d.polygon([(89,122),(109,119),(109,160),(89,169)],fill='#1f2a29')
 d.line([(96,124),(96,156),(105,153)],fill='#647065',width=3);d.line([(97,125),(97,155),(105,152)],fill='#a5ad94')
 d.line([(102,123),(102,140),(107,142)],fill='#74603a',width=2)
 d.polygon([(87,120),(79,116),(79,158),(87,172)],fill='#3a483c');d.line([(79,116),(79,158),(87,172)],fill='#969779');d.line([(81,121),(81,157),(85,163)],fill='#64715a')
 add('state-hatch-open',opened)
 attendant=blank();d=ImageDraw.Draw(attendant)
 # Deliberately simplified scene silhouette, no portrait-level miniature face.
 d.ellipse((133,125,139,132),fill='#c8a98a');d.polygon([(132,125),(133,123),(138,123),(140,126)],fill='#34423e')
 d.polygon([(132,133),(139,133),(142,147),(140,153),(130,153),(130,141)],fill='#4c5951');d.line([(132,134),(135,138),(138,134)],fill='#c7c8a7')
 d.polygon([(131,136),(126,141),(123,139),(122,141),(127,144),(133,140)],fill='#647065');d.polygon([(139,136),(145,141),(148,137),(150,138),(146,145),(139,141)],fill='#647065')
 d.line([(131,153),(130,162)],fill='#34423e',width=3);d.line([(138,153),(140,162)],fill='#34423e',width=3);d.line([(128,163),(132,163)],fill='#1f2a29',width=2);d.line([(139,163),(143,164)],fill='#1f2a29',width=2)
 d.point((137,128),fill='#81705a');add('state-attendant',attendant)
 sign=blank();d=ImageDraw.Draw(sign)
 d.polygon([(144,182),(164,177),(178,188),(156,194)],fill='#74603a')
 face=Image.new('RGB',(21,13),'#c8a263');fd=ImageDraw.Draw(face)
 glyphs={'W':['101','101','101','111','101'],'E':['111','100','110','100','111'],'T':['111','010','010','010','010'],'F':['111','100','110','100','100'],'L':['100','100','100','100','111'],'O':['111','101','101','101','111'],'R':['110','101','110','101','101']}
 for word,x0,y0 in [('WET',5,1),('FLOOR',1,7)]:
  for n,ch in enumerate(word):
   for yy,row in enumerate(glyphs[ch]):
    for xx,b in enumerate(row):
     if b=='1':fd.point((x0+n*4+xx,y0+yy),fill='#453a26')
 # Project the native block lettering with the fallen face; no smooth text.
 for y in range(13):
  for x in range(21):
   px=145+x+(y*11)//13;py=181-(x*4)//21+(y*10)//13
   d.point((px,py),fill=face.getpixel((x,y)))
 d.line([(145,181),(165,177),(176,187)],fill='#e0c28a')
 d.line([(157,194),(166,193)],fill='#314c4c');d.line([(174,190),(181,190)],fill='#90a399');add('state-floating-sign',sign)
 floodnames=drynames+['state-water','state-hatch-open','state-attendant','state-floating-sign'];flood=assemble(floodnames)
 fp=ROOT/'native/CH4-NEW-04-public-corridor-flood-v01.png';flood.save(fp);flood.resize((1256,824),Image.Resampling.NEAREST).save(ROOT/'previews/CH4-NEW-04-public-corridor-flood-v01-4x.png')
 allowed=Image.new('L',SIZE)
 for n in floodnames[len(drynames):]:allowed=ImageChops.lighter(allowed,Image.open(ROOT/'layers'/(n+'.png')).getchannel('A'))
 allowed.save(ROOT/'masks/flood-authorized.png')
 (ROOT/'evidence/native-construction.json').write_text(json.dumps({'sourceDerived':True,'whollyIndependentAuthorshipClaim':False,'method':'Blank native structural layers and independently specified silhouettes/profiles, material-specific reference-informed local shade fields, native connected-cluster cleanup, deliberately painted perspective, stairs, doors, letters, lights, material edges and localized state overlays. Source influence is retained; not an independent-authorship claim or a direct resize finished asset.','source':str(source.relative_to(ROOT)),'sourceSha256':sha(source),'nativeSize':list(SIZE),'ramps':R,'materialRegions':regions,'isolatedWeakPixelsMerged':quiet[0],'dryLayerOrder':drynames,'floodLayerOrder':floodnames,'dryHash':sha(drypath),'floodHash':sha(fp),'status':'UNSELECTED'},indent=2)+'\n')
 print(json.dumps({'dry':sha(drypath),'flood':sha(fp),'sourceDerived':True}))
if __name__=='__main__':main()
