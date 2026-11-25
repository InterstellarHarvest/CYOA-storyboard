"""B2-12 SOURCE-DERIVED native material and structural reconstruction.

Large images supply material/light observations, not finished deliverables.
Native semantic material masks, connected shade groups, independently specified
fixture profiles, cloth construction, steel assembly and pixel lettering are
assembled at the final grids. This is NOT wholly independent native authorship.
No dithering, image blur or interpolated enlargement is used in final artwork.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops, ImageFilter
from collections import Counter
import json, hashlib, math

ROOT=Path(__file__).resolve().parents[1]
RECIPES={}; LETTERS=[]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rgb(c): return tuple(bytes.fromhex(c.lstrip('#')))
RAMPS={
 'plaster':['#655442','#88715b','#a68b6c','#c1a584','#d5bd99','#e7d2ac'],
 'green':['#1f302b','#2d4038','#40554a','#566659','#748072','#9aa18a'],
 'velvet':['#3b2229','#532932','#70333d','#8d424c','#a7555a','#c07872'],
 'wood':['#292c27','#433b2d','#615039','#826446','#ab8456','#d8b67a'],
 'brass':['#302b20','#584227','#7d5c30','#a27a3e','#c29a53','#debb73','#f1d99b'],
 'steel':['#252f2d','#3a4741','#58635a','#7c8373','#abb09a','#d5d2b7','#eeead6'],
 'ivory':['#6c6c5c','#898572','#a49b83','#bdb098','#d2c4a9','#e5d8be','#f4e9d0'],
 'glass':['#465e60','#637d7c','#86a3a0','#abc6c0','#d1e2d7'],
 'black':['#151e1c','#27332c','#3a4739','#54604b','#768166'],
}
RAMPS={k:[rgb(c)for c in v]for k,v in RAMPS.items()}
FONT={
 'A':['01110','11011','11011','11111','11011','11011','11011'],
 'B':['11110','11011','11011','11110','11011','11011','11110'],
 'C':['01111','11000','11000','11000','11000','11000','01111'],
 'D':['11110','11011','11011','11011','11011','11011','11110'],
 'E':['11111','11000','11000','11110','11000','11000','11111'],
 'F':['11111','11000','11000','11110','11000','11000','11000'],
 'G':['01111','11000','11000','11011','11011','11011','01111'],
 'H':['11011','11011','11011','11111','11011','11011','11011'],
 'I':['11111','00100','00100','00100','00100','00100','11111'],
 'J':['00111','00011','00011','00011','11011','11011','01110'],
 'K':['11011','11011','11110','11100','11110','11011','11011'],
 'L':['11000','11000','11000','11000','11000','11000','11111'],
 'M':['10001','11011','10101','10101','10001','10001','10001'],
 'N':['10001','11001','11001','10101','10011','10011','10001'],
 'O':['01110','11011','11011','11011','11011','11011','01110'],
 'P':['11110','11011','11011','11110','11000','11000','11000'],
 'Q':['01110','11011','11011','11011','11111','01110','00011'],
 'R':['11110','11011','11011','11110','11100','11010','11011'],
 'S':['01111','11000','11000','01110','00011','00011','11110'],
 'T':['11111','00100','00100','00100','00100','00100','00100'],
 'U':['11011','11011','11011','11011','11011','11011','01110'],
 'V':['11011','11011','11011','11011','11011','01110','00100'],
 'W':['11011','11011','11011','11011','11111','11111','11011'],
 'X':['11011','11011','01110','00100','01110','11011','11011'],
 'Y':['11011','11011','01110','00100','00100','00100','00100'],
 'Z':['11111','00011','00110','01100','11000','11000','11111'],
 ' ':['00000']*7,
}
def text(d,box,lines,scale=2,fill='#1e271f',gap=5):
 x0,y0,x1,y1=box; h=len(lines)*7*scale+(len(lines)-1)*gap
 assert h<=y1-y0,(lines,box)
 y=y0+(y1-y0-h)//2
 for line in lines:
  w=(len(line)*6-1)*scale;assert w<=x1-x0,(line,w,box)
  x=x0+(x1-x0-w)//2
  LETTERS.append({'text':line,'box':list(box),'inkBox':[x,y,x+w,y+7*scale], 'scale':scale,'leftMargin':x-x0,'rightMargin':x1-x-w,'binaryGlyphs':True})
  for ch in line:
   for j,row in enumerate(FONT[ch]):
    for i,b in enumerate(row):
     if b=='1':d.rectangle((x+i*scale,y+j*scale,x+(i+1)*scale-1,y+(j+1)*scale-1),fill=fill)
   x+=6*scale
  y+=7*scale+gap

class Canvas:
 def __init__(self,name,size,guide):
  self.name=name;self.size=size;self.layers=[];self.records=[]
  self.guide=Image.open(guide).convert('RGB').resize(size,Image.Resampling.BOX)
  self.guide.save(ROOT/f'diagnostics/{name}-source-derived-diagnostic-NOT-production.png')
 def layer(self,name,paint):
  im=Image.new('RGBA',self.size);paint(ImageDraw.Draw(im),im);self.append(name,im)
 def append(self,name,im):
  rel=f'layers/{self.name}-{name}.png';im.save(ROOT/rel);self.layers.append(im)
  self.records.append({'file':rel,'sha256':sha(ROOT/rel),'bbox':im.getchannel('A').getbbox()})
 def material(self,name,mask,ramp,guide=None,merge=2):
  if not isinstance(mask,Image.Image):
   m=Image.new('L',self.size);ImageDraw.Draw(m).polygon(mask,fill=255);mask=m
  mask.save(ROOT/f'masks/{self.name}-{name}.png')
  guide=guide or self.guide;cols=RAMPS[ramp];cache={};pixels=[]
  for p in guide.get_flattened_data():
   if p not in cache:cache[p]=min(cols,key=lambda c:sum((x-y)**2 for x,y in zip(p,c)))
   pixels.append(cache[p])
  # Unify tiny connected material islands only; never blur across silhouettes.
  w,h=self.size;allowed=list(mask.get_flattened_data());seen=set();before=pixels[:]
  for s,c in enumerate(before):
   if not allowed[s]or s in seen:continue
   stack=[s];seen.add(s);component=[];around=[]
   while stack:
    k=stack.pop();component.append(k);x=k%w;y=k//w
    for nx,ny in[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
     if not(0<=nx<w and 0<=ny<h):continue
     n=ny*w+nx
     if not allowed[n]:continue
     if before[n]==c:
      if n not in seen:seen.add(n);stack.append(n)
     else:around.append(before[n])
   if len(component)<=merge and around:
    col=Counter(around).most_common(1)[0][0]
    for k in component:pixels[k]=col
  im=Image.new('RGB',self.size);im.putdata(pixels);im=im.convert('RGBA');im.putalpha(mask);self.append(name,im)
 def image(self):
  out=Image.new('RGBA',self.size)
  for im in self.layers:out=Image.alpha_composite(out,im)
  return out.convert('RGB')
 def save(self,file):
  im=self.image();im.save(ROOT/f'native/{file}.png');im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/f'previews/{file}-4x.png');RECIPES[self.name]=self.records;return im

def maskrect(size,box):
 m=Image.new('L',size);ImageDraw.Draw(m).rectangle(box,fill=255);return m

def room():
 c=Canvas('room',(314,206),ROOT/'originals/CH4-NEW-01-pixel-friendly-study.png')
 # Native semantic fields; source light observations are locally reinterpreted.
 c.material('plaster',[(0,0),(313,0),(313,205),(0,205)],'plaster',merge=3)
 c.material('wall-panels',[(36,0),(117,0),(117,151),(313,151),(313,205),(0,205),(0,111),(37,115)],'green',merge=2)
 c.material('lower-wall-panels',[(0,115),(75,116),(118,111),(303,111),(313,114),(313,154),(120,154),(70,165),(0,155)],'green',merge=3)
 c.material('floor-carpet',[(0,153),(68,166),(120,154),(207,153),(314,153),(314,206),(0,206)],'velvet',merge=6)
 c.material('curtain',[(54,0),(102,0),(109,30),(107,105),(100,119),(90,119),(92,97),(82,96),(75,51),(64,18),(54,17)],'velvet',merge=3)
 c.material('window',[(76,28),(90,36),(97,103),(74,110),(70,66)],'glass',merge=2)
 c.material('window-mullions',[(72,26),(91,34),(99,111),(73,114),(70,108),(90,105),(86,73),(73,69),(72,65),(86,68),(82,49),(73,45)],'steel',merge=1)
 c.material('mirror-silver',[(0,8),(10,5),(21,10),(22,22),(34,32),(34,112),(0,121)],'steel',merge=4)
 c.material('ceiling-duct',[(119,24),(143,15),(210,11),(288,7),(294,0),(313,0),(313,14),(302,19),(298,27),(153,34),(146,42),(124,41),(119,37)],'steel',merge=3)
 c.material('gilt-and-furniture',[(0,116),(47,116),(47,124),(67,126),(66,141),(62,143),(63,168),(60,192),(54,192),(51,166),(38,161),(15,163),(11,201),(4,200),(0,180)],'wood',merge=2)
 c.material('stool-velvet',[(4,157),(18,151),(41,150),(57,155),(61,161),(60,175),(11,178),(4,173)],'velvet',merge=3)
 # Source-derived gown field isolated from surrounding rack and shadows.
 gown=[(103,71),(107,67),(113,65),(121,70),(127,69),(134,66),(139,69),(139,74),(134,77),(130,77),(127,86),(127,91),(132,97),(140,114),(147,135),(153,150),(157,165),(151,170),(140,172),(121,173),(103,174),(86,174),(75,172),(68,165),(76,147),(86,124),(101,103),(115,94),(119,88),(116,78),(108,78),(103,75)]
 c.material('gown-cloth',gown,'ivory',merge=2)
 def structural(d,im):
  # Coherent single-pixel profile and bevel pairs: no superimposed blur.
  d.line([(74,112),(98,109),(97,114),(76,117)],fill='#d5bd99',width=1)
  for a,b in [([(38,0),(38,124)],'#202f2a'), ([(40,0),(40,122)],'#a27a3e'), ([(47,0),(47,119)],'#566659'), ([(48,0),(48,120)],'#202f2a')]:d.line(a,fill=b)
  # Plaster losses occur from a pipe chase/door head, not random stipple.
  d.line([(279,34),(278,43),(281,48),(278,53),(276,58)],fill='#88715b')
  d.line([(279,35),(279,42),(282,48)],fill='#d5bd99')
  d.polygon([(181,101),(185,99),(191,97),(194,91),(194,106),(187,108),(179,107)],fill='#88715b')
  d.line([(181,101),(186,101),(192,97)],fill='#d5bd99')
  # Existing floor and furniture light profiles retain source perspective.
  d.line([(2,134),(63,129),(65,127)],fill='#e5d8be');d.line([(0,137),(65,132)],fill='#433b2d')
  for x,y in [(17,141),(55,137)]:d.line([(x,y),(x+6,y)],fill='#debb73',width=1)
  # Duct flange supports and rectangular vent are designed at native size.
  for x,top,bot in [(146,14,35),(167,3,30),(208,12,33),(249,0,29),(286,8,27)]:
   d.polygon([(x,top),(x+2,top),(x+2,bot),(x+5,bot+1),(x+4,bot+3),(x,bot+2)],fill='#252f2d')
   d.line([(x,top),(x,bot)],fill='#abb09a');d.point((x+1,top+3),fill='#d5d2b7')
  d.rectangle((217,9,242,26),fill='#252f2d');d.line([(216,8),(242,8),(243,26)],fill='#d5d2b7')
  for y in range(11,26,3):d.line([(219,y),(240,y)],fill='#7c8373')
  # Wall molding near the door follows a continuous horizontal room plane.
  d.line([(158,112),(196,112)],fill='#debb73');d.line([(158,114),(196,114)],fill='#2d4038')
  d.line([(268,112),(304,112),(313,115)],fill='#c29a53')
  d.line([(268,114),(304,114),(313,117)],fill='#1f302b')
  # Native wall lamp: warm glass enclosed by a tarnished brass cage.
  d.polygon([(171,60),(176,59),(180,62),(179,73),(174,77),(170,72)],fill='#584227')
  d.polygon([(172,61),(176,60),(178,63),(177,71),(174,73),(172,70)],fill='#f1d99b')
  d.line([(172,62),(172,71),(175,73)],fill='#debb73');d.line([(177,62),(177,71)],fill='#c29a53')
  d.line([(171,61),(176,59),(179,62)],fill='#debb73');d.rectangle((173,75,175,77),fill='#a27a3e')
 c.layer('architecture-profiles',structural)
 def door(d,im):
  # Handle-less leaf and its recessed panels: no knob/keyhole at any scale.
  d.rectangle((201,39,266,155),fill='#1f302b');d.rectangle((203,40,264,44),fill='#748072')
  d.line([(203,155),(203,40),(265,40)],fill='#ab8456')
  d.line([(206,155),(206,46),(261,46),(261,155)],fill='#566659',width=2)
  d.line([(208,155),(208,48),(259,48)],fill='#151e1c')
  d.rectangle((211,50,257,153),fill='#40554a')
  d.line([(212,51),(255,51)],fill='#566659')
  for box in [(218,56,251,109),(218,116,251,143)]:
   x,y,r,b=box;d.rectangle(box,fill='#2d4038');d.line([(x,y),(r,y),(r,b)],fill='#1f302b')
   d.line([(x,b),(x,y),(r,y)],fill='#748072')
   d.rectangle((x+3,y+3,r-3,b-3),fill='#40554a')
   d.line([(x+4,b-4),(r-4,b-4),(r-4,y+4)],fill='#566659')
  d.line([(210,154),(258,154)],fill='#171f1d');d.line([(211,155),(258,155)],fill='#a68b6c')
 c.layer('closed-door-leaf-and-insets',door)
 def rack(d,im):
  # Grounded H-base: three visible casters, one occluded by the dress.
  d.line([(78,174),(108,180),(160,167)],fill='#292c27',width=3)
  d.line([(78,172),(107,177),(160,165)],fill='#58635a',width=3)
  d.line([(79,171),(107,176),(158,164)],fill='#d5d2b7')
  for x,y in [(79,178),(108,182),(160,168)]:
   d.rectangle((x-2,y-3,x+1,y),fill='#7c8373');d.ellipse((x-4,y-1,x+3,y+5),fill='#252f2d')
   d.line([(x-3,y+2),(x-2,y+4),(x+1,y+4)],fill='#58635a');d.rectangle((x-1,y-1,x+1,y+2),fill='#d5d2b7')
  d.line([(90,170),(90,51),(92,49),(140,56),(143,58),(143,65)],fill='#252f2d',width=4)
  d.line([(90,170),(90,52),(92,50),(140,57),(142,59),(142,65)],fill='#7c8373',width=2)
  d.line([(89,168),(89,52),(92,49),(140,56)],fill='#eeead6')
  for x,y in [(90,54),(90,166),(117,54),(142,62)]:
   d.line([(x-2,y),(x+2,y+1)],fill='#252f2d');d.line([(x-1,y-1),(x+2,y)],fill='#d5d2b7')
  # Deliberately leave the rear upright occluded by cloth, as in the source.
  d.line([(143,64),(143,91)],fill='#7c8373',width=2)
  d.line([(142,65),(142,87)],fill='#d5d2b7')
  # Empty hanger visible in the neckline; not a mannequin's neck or head.
  d.line([(119,60),(119,58),(121,57),(122,59),(121,61)],fill='#debb73')
  d.line([(121,61),(112,66),(106,68),(110,70),(121,66),(130,71),(134,69),(121,61)],fill='#826446',width=2)
  d.line([(109,68),(121,63),(132,69)],fill='#d8b67a')
 c.layer('steel-rolling-stand-and-empty-hanger',rack)
 # Cloth sits before the hidden rear steel post, while near post is in front.
 def cloth(d,im):
  # Native seams and lengthwise satin folds; preserve large source cloth groups.
  d.line([(116,75),(120,81),(122,89),(121,93)],fill='#a49b83')
  d.line([(127,76),(124,86),(125,91),(128,94)],fill='#f4e9d0')
  d.line([(118,78),(121,89),(120,93)],fill='#e5d8be')
  d.line([(118,93),(123,94),(128,93)],fill='#898572')
  d.rectangle((123,92,126,94),fill='#a27a3e');d.point((124,92),fill='#f1d99b')
  for pts,col in [([(122,97),(114,120),(104,147),(101,169)],'#bdb098'), ([(124,99),(125,125),(130,151),(132,170)],'#f4e9d0'), ([(129,101),(136,126),(145,154),(148,168)],'#a49b83'), ([(110,108),(101,122),(87,146),(79,164)],'#f4e9d0')]:d.line(pts,fill=col,width=2)
  # Irregular scallop groups along only the lace hems, not all-over dither.
  for x,y in [(74,168),(80,171),(88,172),(100,172),(113,172),(127,171),(141,170),(151,168),(106,77),(111,74),(133,74),(137,72)]:
   d.line([(x,y),(x+1,y+1),(x+3,y+1),(x+4,y-1)],fill='#e5d8be')
  d.line([(89,162),(89,78)],fill='#252f2d',width=3);d.line([(89,161),(89,79)],fill='#abb09a');d.line([(88,162),(88,78)],fill='#d5d2b7')
 c.layer('gown-native-seams-and-lace-clusters',cloth)
 def panel(d,im):
  # Same layout as the Focus, kept subordinate in the main scene.
  d.rectangle((270,62,302,102),fill='#1f302b');d.rectangle((270,62,301,100),fill='#584227')
  d.rectangle((271,63,300,99),fill='#a27a3e');d.line([(271,99),(271,63),(300,63)],fill='#debb73')
  d.rectangle((273,65,296,67),fill='#debb73');d.rectangle((273,69,281,80),fill='#584227')
  d.ellipse((274,71,280,77),fill='#151e1c');d.point((276,72),fill='#d1e2d7')
  d.rectangle((283,69,298,81),fill='#151e1c');d.rectangle((284,70,297,79),fill='#27332c')
  # Closed lock, no shower or lavatory icon on the privacy screen.
  d.arc((288,71,293,76),180,360,fill='#abc6c0');d.rectangle((288,74,293,77),fill='#abc6c0')
  d.point((298,65),fill='#d35b42')
  for x in [275,285,295]:d.ellipse((x-3,83,x+3,89),fill='#302b20')
  d.line([(273,86),(275,84),(277,86),(275,88),(273,86)],fill='#debb73');d.point((275,86),fill='#f1d99b')
  d.polygon([(285,85),(283,88),(287,88)],fill='#debb73');d.point((285,84),fill='#debb73')
  d.line([(293,84),(297,88)],fill='#debb73');d.line([(297,84),(293,88)],fill='#debb73')
  d.rectangle((277,92,295,97),fill='#584227');d.rectangle((278,92,294,96),fill='#debb73')
  d.line([(286,93),(286,94)],fill='#302b20');d.line([(284,95),(288,95)],fill='#302b20')
  for p in[(272,64),(299,64),(272,98),(299,98)]:d.point(p,fill='#f1d99b')
 c.layer('privacy-panel-native-fixtures',panel)
 return c.save('CH4-NEW-01-bridal-dressing-room-v01')

def bevel(d,box,fill,light,dark,width=2):
 x,y,r,b=box;d.rectangle(box,fill=fill)
 for k in range(width):
  d.line([(x+k,b-k),(x+k,y+k),(r-k,y+k)],fill=light)
  d.line([(x+k+1,b-k),(r-k,b-k),(r-k,y+k+1)],fill=dark)

def panel():
 size=(565,451);c=Canvas('panel',size,ROOT/'originals/CH4-NEW-07-detailed-reference.png')
 c.material('mounting-wall',[(0,0),(564,0),(564,450),(0,450)],'green',merge=4)
 c.material('left-lamp',[(0,0),(65,0),(62,159),(43,181),(0,174)],'brass',merge=3)
 c.material('right-plaster',[(532,0),(564,0),(564,450),(530,450)],'plaster',merge=4)
 # Material observations are transferred inside a separately drawn native plate.
 plate=[(123,15),(439,15),(450,19),(457,29),(457,409),(452,422),(440,428),(123,428),(113,423),(109,413),(109,32),(113,22)]
 c.material('aged-brass-plate',plate,'brass',merge=4)
 def frame(d,im):
  d.line([(111,410),(112,31),(116,23),(124,19),(440,19),(448,24)],fill='#f1d99b',width=2)
  d.line([(114,412),(116,34),(120,26),(438,26),(449,31)],fill='#c29a53')
  d.line([(117,415),(124,421),(440,421),(450,412),(450,33)],fill='#584227',width=3)
  d.line([(126,428),(442,428),(456,419),(459,407),(459,36)],fill='#1f302b',width=3)
  d.line([(121,418),(128,420),(437,420),(446,415)],fill='#debb73')
  # Wall panel moldings/cast shadow are parallel to this front-on plate.
  for x in [80,89,484,494,523]:d.line([(x,0),(x,450)],fill='#a27a3e'if x in[80,494]else'#2d4038',width=2)
  d.line([(468,37),(468,418),(458,436),(132,436)],fill='#1f302b',width=5)
  # Broad abrasion clusters concentrated around corners and mounting points.
  for pts in [[(116,59),(119,51),(122,49)],[(116,273),(120,266),(121,261)],[(127,407),(135,409),(145,409)],[(430,418),(441,415),(445,407)],[(443,35),(446,43),(446,51)]]:d.line(pts,fill='#c29a53')
  # Rebuild the lower field completely: the reference button occupied a larger
  # area. It must not survive as a second inscription behind the native button.
  d.rectangle((149,318,419,398),fill='#a27a3e')
  d.polygon([(149,318),(419,318),(416,328),(408,332),(153,332)],fill='#c29a53')
  d.polygon([(149,332),(157,332),(160,388),(179,393),(412,393),(419,384),(419,398),(149,398)],fill='#7d5c30')
  for pts in [[(152,320),(165,319),(174,319)],[(417,325),(415,333)],[(153,390),(157,394),(168,395)],[(399,395),(410,395),(416,391)]]:d.line(pts,fill='#debb73')
  for x,y in[(132,38),(435,38),(132,403),(435,403)]:
   d.ellipse((x-10,y-9,x+10,y+10),fill='#584227');d.ellipse((x-9,y-10,x+9,y+8),fill='#c29a53')
   d.arc((x-9,y-10,x+9,y+8),195,330,fill='#f1d99b',width=2);d.line([(x-5,y+4),(x+5,y-5)],fill='#302b20',width=2)
 c.layer('plate-thickness-moldings-and-screws',frame)
 def header(d,im):
  pts=[(166,30),(395,30),(405,40),(405,66),(397,75),(167,75),(158,67),(158,40)]
  d.polygon([(x+2,y+3)for x,y in pts],fill='#584227');d.polygon(pts,fill='#c29a53')
  d.line(pts+[pts[0]],fill='#f1d99b');d.polygon([(168,34),(394,34),(401,41),(401,64),(395,71),(169,71),(162,65),(162,41)],fill='#debb73')
  text(d,(169,36,393,69),['BRIDAL PRIVACY','SYSTEM'],2,gap=3)
 c.layer('pixel-lettered-header',header)
 def camera(d,im):
  bevel(d,(154,88,244,178),'#a27a3e','#debb73','#584227',2)
  bevel(d,(161,96,238,171),'#302b20','#c29a53','#584227',1)
  # Swivel pivots and deep optical barrel, modelled in native step rings.
  d.rectangle((149,122,160,142),fill='#7d5c30');d.line([(151,122),(157,122),(157,139)],fill='#debb73',width=2)
  d.rectangle((238,122,247,141),fill='#584227');d.line([(240,123),(244,124),(244,137)],fill='#c29a53')
  d.ellipse((164,98,236,170),fill='#7d5c30');d.arc((164,98,236,170),180,310,fill='#f1d99b',width=3)
  d.ellipse((170,104,231,165),fill='#302b20');d.ellipse((176,110,226,160),fill='#151e1c')
  d.arc((176,110,226,160),20,150,fill='#58635a',width=3);d.arc((181,114,222,155),190,265,fill='#637d7c',width=3)
  d.ellipse((188,120,218,151),fill='#151e1c');d.polygon([(184,117),(191,114),(195,118),(189,124)],fill='#abc6c0')
  d.polygon([(180,122),(184,120),(187,127),(182,130)],fill='#86a3a0');d.point((210,143),fill='#748072')
  for x,y in[(159,94),(239,94),(159,172),(239,172)]:
   d.ellipse((x-3,y-3,x+3,y+3),fill='#debb73');d.line([(x-2,y+1),(x+2,y-1)],fill='#584227')
  # CRT glass is inset in a substantial metal housing, not a flat UI card.
  bevel(d,(264,84,439,182),'#302b20','#debb73','#584227',3)
  d.rounded_rectangle((271,91,434,177),radius=13,fill='#151e1c')
  d.line([(275,164),(275,111),(279,102),(288,97),(416,97)],fill='#3a4741',width=3)
  d.line([(282,171),(418,171),(428,163)],fill='#7d5c30',width=2)
 c.layer('camera-optics-swivel-and-crt-bezel',camera)
 def policy(d,im):
  for x in [176,282,388]:
   d.ellipse((x-43,193,x+43,279),fill='#584227');d.ellipse((x-43,190,x+43,276),fill='#debb73')
   d.ellipse((x-39,194,x+39,272),fill='#302b20');d.arc((x-38,194,x+38,270),30,140,fill='#7d5c30',width=2)
  # Visual identification eye, no portrait.
  d.polygon([(141,232),(153,221),(169,216),(183,216),(199,222),(211,232),(199,242),(183,248),(168,248),(152,242)],fill='#debb73')
  d.polygon([(148,232),(157,226),(170,221),(183,221),(197,227),(204,232),(195,238),(182,243),(169,242),(156,238)],fill='#302b20')
  d.ellipse((166,221,187,243),fill='#debb73');d.ellipse((172,226,181,236),fill='#302b20')
  # Bride pictogram is an empty garment with a veil, not a human likeness.
  d.arc((265,199,299,221),180,360,fill='#debb73',width=3)
  d.line([(266,210),(254,247),(263,243),(267,222)],fill='#debb73',width=2)
  d.line([(298,210),(311,247),(301,243),(296,222)],fill='#debb73',width=2)
  d.polygon([(272,223),(282,227),(291,223),(289,238),(281,241),(274,237)],fill='#debb73')
  d.polygon([(274,238),(289,238),(304,267),(260,267)],fill='#debb73')
  d.line([(280,242),(275,263)],fill='#7d5c30');d.line([(286,242),(292,263)],fill='#a27a3e')
  # Groom/bowtie exclusion, identity-free icon, visibly diagonal prohibition.
  d.polygon([(363,226),(380,236),(388,256),(397,236),(414,226),(410,264),(364,264)],fill='#debb73')
  d.polygon([(379,211),(388,215),(397,211),(397,221),(388,218),(379,221)],fill='#debb73')
  d.rectangle((385,230,390,246),fill='#debb73');d.line([(359,263),(414,207)],fill='#302b20',width=9);d.line([(359,263),(414,207)],fill='#debb73',width=5)
  for x,lines in [(176,['VISUAL','ID']),(282,['BRIDE','ONLY']),(388,['GROOM','EXCLUDED'])]:
   bevel(d,(x-52,277,x+52,316),'#c29a53','#f1d99b','#584227',2)
   d.rectangle((x-49,281,x+49,312),fill='#debb73');text(d,(x-51,281,x+51,312),lines,2,gap=3)
 c.layer('policy-badges-and-chunky-labels',policy)
 def assistance(d,im):
  bevel(d,(153,336,416,390),'#302b20','#debb73','#584227',3)
  bevel(d,(160,342,409,382),'#c29a53','#f1d99b','#7d5c30',3)
  d.rectangle((165,347,404,377),fill='#debb73')
  text(d,(168,347,401,377),['EMERGENCY','ASSISTANCE'],2,gap=2)
 c.layer('physical-emergency-button',assistance)
 base_count=len(c.layers)
 def status(state):
  def draw(d,im):
   # Entire screen payload/indicator replacement is a single explicit overlay.
   d.rounded_rectangle((280,101,426,166),radius=7,fill='#182e2a')
   d.line([(283,160),(283,111),(286,105),(299,104)],fill='#40554a')
   if state=='locked':lines=['LOCKED','BRIDE ONLY'];ink='#b2d3bd';led='#bd4631';hi='#f1aa6c'
   else:lines=['PROVISIONAL','AUTHORIZED'];ink='#bad6a0';led='#6f9e53';hi='#c4dd9b'
   text(d,(285,108,425,161),lines,2,ink,gap=6)
   # Closed/open padlock glyph is below the principal words, clear of them.
   d.ellipse((413,51,438,76),fill='#584227');d.ellipse((416,53,435,72),fill=led)
   d.arc((417,54,433,70),180,300,fill=hi,width=2);d.rectangle((423,59,427,65),fill=hi)
   # Actual lock pictogram in the lower screen margin, no new mode/binding.
   if state=='locked':d.arc((345,151,353,159),180,360,fill=ink,width=2)
   else:d.arc((349,149,359,158),180,350,fill=ink,width=2)
   d.rectangle((345,155,354,162),fill=ink);d.rectangle((349,157,350,160),fill='#182e2a')
  return draw
 c.layer('locked-status',status('locked'));a=c.save('CH4-NEW-07-bridal-privacy-panel-v01')
 c.layers=c.layers[:base_count];c.records=c.records[:base_count]
 c.layer('provisional-status',status('provisional'));b=c.save('CH4-NEW-07-provisional-authorized-v01')
 # Store independent replay orders for both conditions, with a shared geometry.
 RECIPES['panel-locked']=[r for r in RECIPES['panel'] if 'provisional-status'not in r['file']]
 RECIPES['panel-locked']=c.records[:base_count]+[{'file':'layers/panel-locked-status.png','sha256':sha(ROOT/'layers/panel-locked-status.png')}]
 RECIPES['panel-provisional']=c.records
 allowed=Image.new('L',size);d=ImageDraw.Draw(allowed);d.rectangle((280,101,426,166),fill=255);d.rectangle((413,51,438,76),fill=255)
 allowed.save(ROOT/'masks/panel-authorized-status-change.png')
 diff=ImageChops.difference(a,b);actual=ImageChops.lighter(ImageChops.lighter(diff.getchannel('R'),diff.getchannel('G')),diff.getchannel('B')).point(lambda p:255 if p else 0)
 actual.save(ROOT/'masks/panel-actual-status-change.png')
 return a,b

def main():
 for folder in ['native','previews','layers','masks','diagnostics','evidence']:(ROOT/folder).mkdir(exist_ok=True)
 room();panel()
 (ROOT/'evidence/native-layer-recipes.json').write_text(json.dumps(RECIPES,indent=2)+'\n')
 (ROOT/'evidence/lettering-layout.json').write_text(json.dumps(LETTERS,indent=2)+'\n')
 (ROOT/'evidence/material-ramps.json').write_text(json.dumps({k:['#'+bytes(c).hex()for c in v]for k,v in RAMPS.items()},indent=2)+'\n')
 print(json.dumps({'nativeFiles':[(p.name,Image.open(p).size,sha(p))for p in sorted((ROOT/'native').glob('*.png'))],'status':'UNSELECTED'}))
if __name__=='__main__':main()
