"""New 564x278 Focus composition; immutable approved inspection art is reference.

Source-derived wall light/material fields are observed inside native masks.
The panel, status, camera, badges, button, door profiles, lamp and pipe structures
are separately painted at the target grid. No square-image resize or crop, no
whole-reference palette-reduction deliverable, no independent-whole-art claim.
"""
from native_support import *
SIZE=(564,278)
def build():
 c=Canvas('wide',SIZE,ROOT/'originals/widescreen-detailed-reference.png')
 c.material('cream-plaster',[(0,0),(563,0),(563,277),(0,277)],'plaster',merge=8)
 c.material('door-painted-wood',[(0,8),(201,8),(203,277),(0,277)],'green',merge=5)
 c.material('lower-green-paneling',[(204,270),(563,270),(563,277),(204,277)],'green',merge=5)
 c.material('duct-surface',[(295,0),(563,0),(563,18),(504,19),(492,16),(319,19),(304,14)],'steel',merge=4)
 def wall_extension(d,im):
  # Owner correction: rail BELOW the plate and its shadow, not behind it.
  # Erase the source's old rail/green field and reconstruct a plaster band.
  d.polygon([(204,232),(414,232),(417,226),(426,231),(434,229),(443,231),(452,225),(466,229),(474,226),(482,230),(495,226),(506,231),(516,225),(524,229),(535,226),(548,230),(555,225),(563,229),(563,269),(204,269)],fill='#c1a584')
  d.polygon([(204,232),(218,232),(220,244),(217,258),(218,269),(204,269)],fill='#a68b6c')
  d.polygon([(416,232),(433,232),(430,241),(435,250),(430,258),(435,269),(416,269)],fill='#a68b6c')
  d.polygon([(486,232),(494,238),(502,239),(505,247),(498,254),(499,269),(486,269),(490,259),(487,251),(491,242)],fill='#d5bd99')
  d.polygon([(552,232),(563,232),(563,269),(556,269),(557,257),(553,250)],fill='#d5bd99')
  d.line([(495,234),(500,239),(501,245),(498,251),(498,258)],fill='#a68b6c')
 c.layer('plaster-extension-above-relocated-wainscot',wall_extension)
 def door(d,im):
  # Native nested profiles track a single front-on architectural plane.
  d.polygon([(199,12),(207,18),(207,232),(203,240),(201,277),(197,277)],fill='#655442')
  d.line([(0,9),(196,9),(202,14),(202,277)],fill='#1f302b',width=3)
  d.line([(0,10),(196,10),(199,13),(199,277)],fill='#c29a53')
  d.line([(1,14),(193,14),(195,17),(195,277)],fill='#748072',width=2)
  d.line([(3,19),(189,19),(189,277)],fill='#1f302b',width=3)
  d.line([(4,22),(186,22),(186,277)],fill='#566659',width=2)
  d.line([(7,27),(180,27),(180,277)],fill='#9aa18a')
  d.line([(12,31),(176,31),(176,277)],fill='#1f302b',width=3)
  d.line([(14,34),(172,34),(172,277)],fill='#2d4038',width=2)
  # Closed leaf. Its original material field remains behind these recesses.
  for box in [(47,57,153,213),(47,239,153,286)]:
   x,y,r,b=box
   d.line([(x-2,b),(x-2,y-2),(r+2,y-2),(r+2,b)],fill='#1f302b',width=2)
   d.line([(x,b),(x,y),(r,y)],fill='#9aa18a')
   d.line([(x+2,b),(x+2,y+2),(r-2,y+2)],fill='#566659',width=2)
   d.line([(x+5,b-5),(x+5,y+6),(r-6,y+6),(r-6,b-5)],fill='#1f302b',width=3)
   d.line([(x+8,b-7),(r-8,b-7),(r-8,y+9)],fill='#748072')
   d.line([(x+11,b-10),(r-10,b-10),(r-10,y+11)],fill='#566659')
  # Finish losses follow raised edges; no speckle field or invented hardware.
  for pts in [[(52,60),(64,60),(68,61)],[(80,62),(88,62)],[(151,73),(151,83)],[(52,206),(62,206),(67,205)],[(180,110),(180,117)],[(173,197),(173,210)]]:d.line(pts,fill='#748072')
  d.line([(205,270),(563,270)],fill='#a27a3e',width=2)
  d.line([(205,273),(563,273)],fill='#1f302b',width=3)
  d.line([(207,275),(563,275)],fill='#748072')
  # Mortar/finish cracks are selected as connected paths, subordinate to panel.
  d.line([(219,61),(215,72),(218,82),(212,96),(214,104)],fill='#88715b')
  d.line([(498,143),(503,149),(504,161),(496,171),(494,181),(486,187)],fill='#88715b')
  d.line([(499,143),(504,149),(505,160)],fill='#d5bd99')
 c.layer('door-jamb-recesses-wall-moldings',door)
 def services(d,im):
  # One uncomplicated conduit with elbow, collars and real wall brackets.
  d.line([(496,20),(525,20),(532,25),(536,33),(536,268)],fill='#252f2d',width=9)
  d.line([(496,19),(526,19),(533,24),(536,32),(536,268)],fill='#58635a',width=6)
  d.line([(497,17),(526,17),(534,23),(538,31),(538,268)],fill='#abb09a',width=2)
  d.line([(496,22),(523,22),(529,26),(532,34),(532,268)],fill='#3a4741',width=2)
  for y in [76,173,231]:
   bevel(d,(525,y-3,547,y+6),'#58635a','#abb09a','#252f2d',1)
   d.rectangle((532,y-2,540,y+5),fill='#7c8373');d.line([(533,y-2),(533,y+4)],fill='#d5d2b7')
   for x in [528,544]:d.point((x,y+1),fill='#d5d2b7');d.point((x,y+2),fill='#252f2d')
  for x in[325,374,439,486]:
   d.line([(x,0),(x,15),(x+2,18)],fill='#252f2d',width=3)
   d.line([(x,0),(x,14)],fill='#abb09a')
  d.rectangle((442,0,485,15),fill='#252f2d');d.line([(442,15),(485,15)],fill='#abb09a')
  for y in[3,7,11]:d.line([(445,y),(482,y)],fill='#7c8373')
 c.layer('duct-and-associated-conduit',services)
 def lamp(d,im):
  # Sconce shares the source room's warm glass, brackets and wall shadow.
  d.polygon([(466,61),(478,67),(486,85),(483,133),(473,150),(462,146),(456,139),(458,78)],fill='#88715b')
  d.polygon([(462,66),(472,69),(478,84),(478,136),(470,144),(457,139),(454,128),(456,81)],fill='#7d5c30')
  d.line([(461,69),(470,72),(475,84),(475,134),(468,140)],fill='#debb73')
  for x,y in[(471,78),(473,135)]:d.point((x,y),fill='#f1d99b');d.point((x+1,y+1),fill='#584227')
  d.polygon([(447,59),(453,55),(464,55),(473,59),(470,65),(448,65)],fill='#584227')
  d.line([(447,60),(454,56),(465,56),(472,60)],fill='#debb73')
  d.ellipse((457,48,463,55),fill='#c29a53');d.point((460,49),fill='#f1d99b')
  d.polygon([(449,64),(470,64),(466,106),(452,107)],fill='#debb73')
  d.polygon([(452,65),(459,64),(461,104),(454,104)],fill='#f1d99b')
  d.polygon([(460,65),(467,65),(464,103),(461,104)],fill='#e7d2ac')
  d.line([(447,64),(451,106),(466,106),(472,64)],fill='#7d5c30',width=2)
  d.line([(460,65),(460,105)],fill='#c29a53')
  bevel(d,(451,106,468,112),'#a27a3e','#f1d99b','#584227',1)
  d.polygon([(454,113),(465,113),(464,126),(461,131),(455,127)],fill='#7d5c30')
  d.line([(455,114),(455,124),(459,127)],fill='#debb73',width=2)
  d.rectangle((457,128,463,131),fill='#a27a3e');d.ellipse((458,132,463,136),fill='#584227')
 c.layer('warm-glass-brass-sconce',lamp)
 def plate(d,im):
  # New full-height native brass plate, not a scaled/cropped approved panel.
  pts=[(235,22),(396,22),(406,28),(410,38),(410,244),(404,254),(395,258),(235,258),(225,253),(221,244),(221,36),(225,28)]
  d.polygon([(x+4,y+4)for x,y in pts],fill='#655442');d.line([(239,263),(397,263),(411,254),(415,241),(415,43)],fill='#2d4038',width=3)
  d.polygon(pts,fill='#a27a3e')
  d.polygon([(228,36),(237,28),(396,28),(404,36),(404,244),(395,251),(236,251),(228,243)],fill='#c29a53')
  # Native reflected brass planes: stepped larger shapes, not gradients.
  d.polygon([(230,39),(239,31),(397,31),(400,40),(397,64),(235,66)],fill='#debb73')
  d.polygon([(229,65),(237,63),(239,234),(245,247),(234,247),(228,239)],fill='#c29a53')
  d.polygon([(238,68),(396,68),(399,234),(394,246),(241,246)],fill='#a27a3e')
  d.polygon([(245,200),(395,195),(397,226),(391,244),(242,244)],fill='#c29a53')
  d.polygon([(397,36),(404,39),(404,242),(397,249),(391,249),(397,239)],fill='#7d5c30')
  d.line([(223,242),(223,37),(228,29),(236,25),(395,25),(403,30)],fill='#f1d99b')
  d.line([(225,242),(225,37),(231,30),(395,28)],fill='#debb73')
  d.line([(226,247),(235,253),(395,253),(406,245),(406,39)],fill='#584227',width=2)
  d.line([(235,255),(396,255),(406,247)],fill='#debb73')
  # Selected connected scratches/chips around mounting edges only.
  for pts in [[(229,89),(232,85),(234,85)],[(229,139),(231,136),(232,129)],[(235,250),(246,250),(249,249)],[(379,251),(391,251),(396,248)],[(399,186),(401,182),(401,174)],[(239,29),(248,29),(252,30)],[(348,28),(355,28)]]:d.line(pts,fill='#7d5c30')
  for pts in [[(230,91),(233,87)],[(233,239),(234,242),(240,245)],[(383,248),(390,247)],[(399,176),(399,182)]]:d.line(pts,fill='#f1d99b')
  for x,y in[(235,36),(396,36),(235,244),(396,244)]:
   d.ellipse((x-6,y-6,x+6,y+6),fill='#584227');d.ellipse((x-5,y-6,x+5,y+4),fill='#c29a53')
   d.arc((x-5,y-6,x+5,y+4),190,315,fill='#f1d99b');d.line([(x-3,y+2),(x+3,y-4)],fill='#584227')
 c.layer('new-native-brass-plate-and-fixings',plate)
 def header(d,im):
  pts=[(248,33),(379,33),(386,40),(386,55),(379,62),(247,62),(242,57),(242,39)]
  d.polygon([(x+1,y+2)for x,y in pts],fill='#7d5c30');d.polygon(pts,fill='#debb73');d.line(pts+[pts[0]],fill='#f1d99b')
  d.line([(248,60),(379,60),(384,55)],fill='#a27a3e')
  text(d,(248,38,380,58),['BRIDAL PRIVACY','SYSTEM'],1,gap=3)
 c.layer('native-header',header)
 def optics(d,im):
  bevel(d,(241,72,295,126),'#a27a3e','#debb73','#584227',2)
  d.rectangle((244,76,292,123),fill='#302b20')
  d.rectangle((238,94,243,107),fill='#7d5c30');d.line([(239,94),(242,94),(242,104)],fill='#debb73')
  d.rectangle((294,94,298,107),fill='#584227');d.line([(296,95),(296,104)],fill='#c29a53')
  d.ellipse((246,77,291,122),fill='#7d5c30');d.arc((246,77,291,122),185,310,fill='#f1d99b',width=2)
  d.ellipse((250,81,287,118),fill='#302b20');d.ellipse((254,85,284,115),fill='#151e1c')
  d.arc((254,85,284,115),20,150,fill='#58635a',width=2)
  d.arc((257,88,282,112),188,260,fill='#637d7c',width=2)
  d.polygon([(258,87),(263,85),(266,88),(261,92)],fill='#abc6c0');d.polygon([(256,90),(258,89),(260,93),(257,95)],fill='#86a3a0')
  d.point((276,108),fill='#748072')
  for x,y in[(244,75),(292,75),(244,123),(292,123)]:d.point((x,y),fill='#f1d99b');d.point((x+1,y+1),fill='#584227')
  bevel(d,(302,71,398,127),'#302b20','#debb73','#584227',2)
  d.rounded_rectangle((306,75,395,124),radius=7,fill='#151e1c')
  d.line([(308,117),(308,85),(311,80),(318,78),(386,78)],fill='#3a4741',width=2)
  d.line([(313,123),(386,123),(392,119)],fill='#7d5c30')
 c.layer('camera-native-optical-rings-and-inset-crt',optics)
 def policies(d,im):
  for x in[255,316,377]:
   d.ellipse((x-25,136,x+25,186),fill='#584227');d.ellipse((x-24,134,x+24,182),fill='#debb73')
   d.ellipse((x-21,137,x+21,179),fill='#302b20');d.arc((x-20,138,x+20,178),20,130,fill='#7d5c30')
  # Eye.
  d.polygon([(236,158),(242,152),(250,149),(260,149),(269,153),(275,158),(268,163),(259,167),(250,167),(242,163)],fill='#debb73')
  d.polygon([(241,158),(248,154),(255,152),(263,154),(269,158),(261,162),(252,163),(245,161)],fill='#302b20')
  d.ellipse((250,152,260,163),fill='#debb73');d.ellipse((253,155,257,160),fill='#302b20')
  # Veil and empty gown silhouette (no actual person).
  d.arc((306,139,326,153),180,360,fill='#debb73')
  d.line([(307,146),(300,168),(305,166),(309,151)],fill='#debb73')
  d.line([(325,146),(332,168),(327,165),(323,151)],fill='#debb73')
  d.polygon([(311,152),(316,154),(322,152),(320,162),(329,175),(304,175),(312,162)],fill='#debb73')
  d.line([(315,163),(312,173)],fill='#a27a3e');d.line([(319,163),(323,173)],fill='#7d5c30')
  # Bow tie/suit crossed out, matching approved policy identity.
  d.polygon([(365,155),(373,159),(377,170),(382,159),(390,155),(388,174),(366,174)],fill='#debb73')
  d.polygon([(371,145),(377,148),(383,145),(383,152),(377,150),(371,152)],fill='#debb73')
  d.line([(361,175),(393,142)],fill='#302b20',width=5);d.line([(361,175),(393,142)],fill='#debb73',width=3)
  for x,lines in [(255,['VISUAL','ID']),(316,['BRIDE','ONLY']),(377,['GROOM','EXCLUDED'])]:
   bevel(d,(x-29,184,x+29,208),'#c29a53','#f1d99b','#7d5c30',1)
   d.rectangle((x-27,186,x+27,205),fill='#debb73');text(d,(x-26,187,x+26,205),lines,1,gap=2)
 c.layer('native-policy-icons-and-plaques',policies)
 def button(d,im):
  bevel(d,(243,214,392,243),'#302b20','#debb73','#584227',2)
  bevel(d,(247,217,388,239),'#c29a53','#f1d99b','#7d5c30',2)
  d.rectangle((250,220,385,236),fill='#debb73');text(d,(253,220,382,236),['EMERGENCY','ASSISTANCE'],1,gap=2)
 c.layer('native-physical-assistance-button',button)
 shared=c.records[:];base_layers=c.layers[:]
 def state(which):
  def paint(d,im):
   d.rounded_rectangle((312,81,389,120),radius=4,fill='#182e2a')
   d.line([(314,116),(314,88),(317,84),(326,83)],fill='#40554a')
   if which=='locked':lines=['LOCKED','BRIDE ONLY'];ink='#b2d3bd';led='#bd4631';hi='#f1aa6c'
   else:lines=['PROVISIONAL','AUTHORIZED'];ink='#bad6a0';led='#6f9e53';hi='#c4dd9b'
   text(d,(316,84,387,110),lines,1,ink,gap=4)
   d.ellipse((390,49,402,61),fill='#584227');d.ellipse((392,50,400,58),fill=led)
   d.arc((393,51,399,57),180,290,fill=hi);d.point((395,53),fill=hi)
   if which=='locked':d.arc((347,112,353,117),180,360,fill=ink)
   else:d.arc((351,111,357,116),175,350,fill=ink)
   d.rectangle((347,115,354,119),fill=ink);d.point((350,117),fill='#182e2a')
  return paint
 result={}
 for key,name in [('locked','CH4-NEW-07-focus-locked-v02'),('provisional','CH4-NEW-07-focus-provisional-v02')]:
  c.layers=base_layers[:];c.records=shared[:];c.layer(key+'-status',state(key));result[key]=c.save(name)
  RECIPES[key]=c.records[:]
 allowed=Image.new('L',SIZE);d=ImageDraw.Draw(allowed);d.rectangle((312,81,389,120),fill=255);d.rectangle((390,49,402,61),fill=255)
 allowed.save(ROOT/'masks/authorized-status-change.png')
 diff=ImageChops.difference(result['locked'],result['provisional']);actual=ImageChops.lighter(ImageChops.lighter(diff.getchannel('R'),diff.getchannel('G')),diff.getchannel('B')).point(lambda p:255 if p else 0)
 actual.save(ROOT/'masks/actual-status-change.png')
 rail=Image.new('L',SIZE);ImageDraw.Draw(rail).rectangle((205,269,563,276),fill=255);rail.save(ROOT/'masks/wainscot-rail.png')
 Image.open(ROOT/'layers/wide-new-native-brass-plate-and-fixings.png').getchannel('A').save(ROOT/'masks/plate-and-shadow.png')
 (ROOT/'evidence/native-layer-recipes.json').write_text(json.dumps({'sharedLayers':shared,'states':{k:RECIPES[k]for k in['locked','provisional']}},indent=2)+'\n')
 (ROOT/'evidence/lettering-layout.json').write_text(json.dumps(LETTERS,indent=2)+'\n')
 (ROOT/'evidence/material-ramps.json').write_text(json.dumps({k:['#'+bytes(c).hex()for c in v]for k,v in RAMPS.items()},indent=2)+'\n')
 print(json.dumps({'native':[(p.name,list(Image.open(p).size),sha(p))for p in sorted((ROOT/'native').glob('*.png'))],'sourceDerived':True,'whollyIndependentNativeAuthorship':False,'status':'UNSELECTED'}))
if __name__=='__main__':build()
