"""Editable, explicit native-grid construction. No source-image sampling or reduction.
All scene drawing occurs directly on a 314x206 RGBA canvas. Pillow's integer
primitives do not antialias. Only review previews are enlarged using NEAREST.
Semantic layers and the complete primitive/coordinate logs are exported.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import json,hashlib
B=Path(__file__).resolve().parent
P={
'ink':'#293c43','deep':'#1d343d','edge':'#485259','edge2':'#667073',
'wall0':'#b6b0a2','wall1':'#a49f95','wall2':'#96938b','wall3':'#858780','wall4':'#707a77','seam':'#7c817d',
'ceil':'#c7c6b8','ceilshade':'#a3aca5','ceilhi':'#dbd6c2',
'floor':'#a6a197','floorShade':'#92948b','floorLight':'#b7b0a1','tile':'#7f8982','shadow':'#6f7b75',
'cream':'#eee2bd','creamHi':'#fff0cd','creamShade':'#c9bfa3','creamDark':'#a69f87',
'teal0':'#284d54','teal1':'#365e62','teal2':'#487275','teal3':'#5c8684','teal4':'#77988e','tealhi':'#99b2a2',
'coralDark':'#aa4e3e','coral':'#d86d50','coralLight':'#ef8b63','coralHi':'#f7ad79',
'metalDark':'#4d5e60','metal':'#82928c','metalLight':'#b6c1ad','metalHi':'#e0dfc4',
'woodDark':'#765844','wood':'#ac8058','woodLight':'#d7b476','woodHi':'#e9ca8b',
'paper':'#e6d7af','paperShade':'#c3b38c','paperMark':'#779887',
'sky':'#91cbd2','skyLight':'#c2dfcf','greenDark':'#466755','green':'#6f8c54','greenLight':'#a3ad5f','greenHi':'#c1bf74',
'slateDark':'#304954','slate':'#405966','slateHi':'#59717a',
'hairDark':'#6f3d32','hair':'#a45737','hairHi':'#c87846',
'skinShade':'#b97950','skin':'#e3ae73','skinHi':'#f2c38b',
'orangeDark':'#b85a3b','orange':'#dc8453','orangeLight':'#efab6b','orangeHi':'#f5c187',
'red':'#c15c44','greenLamp':'#9cb56e','lampDark':'#687b55','blue':'#79aeb4'
}
FONT={
'A':['01110','10001','10001','11111','10001','10001','10001'],'B':['11110','10001','10001','11110','10001','10001','11110'],'C':['01111','10000','10000','10000','10000','10000','01111'],'D':['11110','10001','10001','10001','10001','10001','11110'],'E':['11111','10000','10000','11110','10000','10000','11111'],'F':['11111','10000','10000','11110','10000','10000','10000'],'G':['01111','10000','10000','10111','10001','10001','01111'],'H':['10001','10001','10001','11111','10001','10001','10001'],'I':['111','010','010','010','010','010','111'],'J':['00111','00010','00010','00010','10010','10010','01100'],'K':['10001','10010','10100','11000','10100','10010','10001'],'L':['10000','10000','10000','10000','10000','10000','11111'],'M':['10001','11011','10101','10101','10001','10001','10001'],'N':['10001','11001','11001','10101','10011','10011','10001'],'O':['01110','10001','10001','10001','10001','10001','01110'],'P':['11110','10001','10001','11110','10000','10000','10000'],'Q':['01110','10001','10001','10001','10101','10010','01101'],'R':['11110','10001','10001','11110','10100','10010','10001'],'S':['01111','10000','10000','01110','00001','00001','11110'],'T':['11111','00100','00100','00100','00100','00100','00100'],'U':['10001','10001','10001','10001','10001','10001','01110'],'V':['10001','10001','10001','10001','10001','01010','00100'],'W':['10001','10001','10001','10101','10101','11011','10001'],'X':['10001','10001','01010','00100','01010','10001','10001'],'Y':['10001','10001','01010','00100','00100','00100','00100'],'Z':['11111','00001','00010','00100','01000','10000','11111'],
'0':['01110','10001','10011','10101','11001','10001','01110'],'1':['010','110','010','010','010','010','111'],'2':['11110','00001','00001','01110','10000','10000','11111'],'3':['11110','00001','00001','01110','00001','00001','11110'],"'":['1','1','0','0','0','0','0'],' ':['000','000','000','000','000','000','000'],'-':['000','000','000','111','000','000','000']}
class Scene:
 def __init__(self,name):self.name=name;self.layers=[];self.layer('base')
 def layer(self,name):self.current={'name':name,'operations':[]};self.layers.append(self.current)
 def op(self,kind,pts,c,**kw):self.current['operations'].append({'kind':kind,'coordinates':pts,'color':c,**kw})
 def poly(self,pts,c):self.op('polygon',pts,c)
 def rect(self,b,c):self.op('rectangle',b,c)
 def line(self,pts,c,w=1):self.op('line',pts,c,width=w)
 def ellipse(self,b,c):self.op('ellipse',b,c)
 def arc(self,b,start,end,c,w=1):self.op('arc',b,c,start=start,end=end,width=w)
 def text(self,x,y,t,c,scale=1):self.op('text',[x,y],c,text=t,scale=scale)
 def panel(self,b,fill='teal1',outline='ink',inset='teal3'):
  x,y,x2,y2=b;self.rect(b,outline);self.rect([x+1,y+1,x2-1,y2-1],fill);self.line([(x+1,y+1),(x2-1,y+1)],inset)
 def save(self):
  d=B/'sources'/self.name;d.mkdir(parents=True,exist_ok=True);result=Image.new('RGBA',(314,206));(d/'scene.json').write_text(json.dumps({'canvas':[314,206],'palette':P,'font':FONT,'layers':self.layers},indent=2))
  for li,layer in enumerate(self.layers):
   im=Image.new('RGBA',(314,206));draw=ImageDraw.Draw(im)
   for op in layer['operations']:
    co=op['coordinates'];c=P[op['color']];k=op['kind']
    if k=='polygon':draw.polygon([tuple(q) for q in co],fill=c)
    elif k=='rectangle':draw.rectangle(co,fill=c)
    elif k=='line':draw.line([tuple(q) for q in co],fill=c,width=op['width'],joint='curve')
    elif k=='ellipse':draw.ellipse(co,fill=c)
    elif k=='arc':draw.arc(co,op['start'],op['end'],fill=c,width=op['width'])
    elif k=='text':
     x,y=co;z=op['scale']
     for char in op['text']:
      glyph=FONT[char]
      for gy,row in enumerate(glyph):
       for gx,v in enumerate(row):
        if v=='1':draw.rectangle([x+gx*z,y+gy*z,x+(gx+1)*z-1,y+(gy+1)*z-1],fill=c)
      x+=(len(glyph[0])+1)*z
   im.save(d/f'{li:02d}-{layer["name"]}.png');result=Image.alpha_composite(result,im)
  assert result.getchannel('A').getextrema()==(255,255)
  (B/'candidates').mkdir(exist_ok=True);(B/'previews').mkdir(exist_ok=True)
  result.convert('RGB').save(B/'candidates'/f'CH3-PILOT-{self.name}-v01.png');result.convert('RGB').resize((1256,824),Image.Resampling.NEAREST).save(B/'previews'/f'CH3-PILOT-{self.name}-v01-4x.png')

def backstage():
 s=Scene('backstage')
 s.rect([0,0,313,205],'wall1')
 s.poly([(0,0),(113,57),(113,133),(0,205)],'wall0');s.poly([(259,0),(313,0),(313,205),(214,132),(214,58)],'wall1')
 s.poly([(50,0),(262,0),(215,61),(113,61)],'ceil');s.rect([112,58,215,133],'wall2')
 s.poly([(0,205),(113,131),(213,131),(313,185),(313,205)],'floor')
 s.poly([(113,131),(142,131),(99,205),(0,205)],'floorLight');s.poly([(189,131),(214,131),(313,184),(313,205),(269,205)],'floorShade')
 s.layer('architectural-seams')
 for pts in [[(0,38),(113,78)],[(0,84),(113,101)],[(0,136),(112,123)],[(29,16),(29,185)],[(83,45),(83,151)],[(313,35),(214,80)],[(313,81),(214,102)],[(313,134),(214,123)],[(275,0),(247,154)],[(313,187),(214,132)]]:s.line(pts,'seam')
 for pts in [[(22,205),(121,132)],[(121,205),(150,132)],[(232,205),(181,132)],[(0,169),(274,165)],[(63,142),(231,141)]]:s.line(pts,'tile')
 # Clean ceiling panel divisions, with no texture stamps.
 for pts in [[(87,0),(131,59)],[(224,0),(200,59)],[(91,31),(237,31)]]:s.line(pts,'ceilshade')
 s.layer('teal-frame-and-lights')
 for poly in [[(41,0),(57,0),(122,55),(111,61)],[(253,0),(267,0),(220,61),(211,55)],[(105,55),(119,55),(119,134),(110,140)],[(209,54),(221,56),(221,137),(210,132)]]:s.poly(poly,'teal1')
 s.line([(48,0),(116,58)],'teal3',2);s.line([(263,0),(216,59)],'teal3',2);s.line([(112,59),(112,134)],'teal3',2);s.line([(215,59),(215,131)],'teal3',2)
 for b in [(106,55,218,63),(90,34,233,41),(72,15,250,24)]:
  x,y,x2,y2=b;s.poly([(x,y),(x2,y),(x2-4,y2),(x+4,y2)],'teal1');s.line([(x+2,y),(x2-2,y)],'teal3')
 for poly in [[(128,3),(220,3),(217,11),(131,11)],[(140,36),(197,36),(196,42),(141,42)],[(147,57),(182,57),(181,61),(148,61)]]:
  s.poly(poly,'edge');inside=[(x+1,y+1) if i<2 else (x,y-1) for i,(x,y) in enumerate(poly)];s.poly(inside,'creamHi')
 s.layer('daylight-exit')
 s.panel([141,63,202,132],'metalDark','edge','metalLight');s.rect([147,67,198,128],'sky')
 s.rect([147,87,198,128],'skyLight');s.poly([(152,86),(163,80),(173,81),(181,75),(194,78),(198,83),(198,106),(152,107)],'green');s.poly([(160,84),(173,80),(182,84),(189,79),(198,81),(198,91),(160,95)],'greenLight')
 s.rect([173,99,198,125],'creamShade');s.rect([172,96,198,100],'coral');s.rect([177,104,188,116],'teal1');s.rect([178,105,187,115],'cream');s.rect([180,108,181,113],'teal1');s.rect([184,108,185,113],'teal1');s.rect([180,106,181,107],'teal1');s.rect([184,106,185,107],'teal1')
 s.poly([(147,120),(172,112),(198,120),(198,128),(147,128)],'ceilhi');s.line([(148,126),(168,119),(195,124)],'creamShade')
 # Door leaf is a single ordinary metal plane opening into the corridor.
 s.poly([(143,65),(164,72),(164,128),(143,132)],'ink');s.poly([(145,68),(161,73),(161,126),(145,129)],'wall1');s.line([(145,68),(161,73)],'ceilhi');s.line([(160,74),(160,126)],'wall3')
 s.panel([146,78,159,91],'teal0','creamShade','teal3');None # ordinary inset door plate; main EXIT is readable above the lintel
 # Five-pixel letters at native size; use a separate clear sign above the frame.
 s.panel([148,49,179,61],'teal0','creamShade','teal4');s.text(151,52,'EXIT','creamHi')
 s.rect([147,106,156,109],'edge');s.line([(148,106),(155,106)],'metalHi');s.rect([147,108,149,110],'metalLight')
 s.poly([(145,132),(166,128),(197,129),(207,134),(146,137)],'floorShade')
 s.layer('attached-cable-loops')
 # Four distinct loops, thick enough to read; no random hairline texture.
 for x,y,w,h in [(39,4,12,34),(60,21,11,27),(80,34,10,24),(98,44,7,19)]:
  s.arc([x,y,x+w,y+h],0,355,'ink',3);s.arc([x+2,y+2,x+w-1,y+h-2],15,320,'edge2',1);s.line([(x+3,y+1),(x+3,y-5)],'ink',2)
 s.line([(34,0),(34,7),(44,11),(53,12),(62,23),(76,26),(81,35),(96,40),(102,47)],'ink',2)
 s.layer('leaning-painted-scenery')
 s.poly([(0,23),(54,43),(73,149),(17,167),(0,138)],'woodDark');s.poly([(2,25),(51,44),(68,146),(18,159),(2,134)],'woodLight')
 s.poly([(5,31),(48,46),(63,141),(20,153),(5,130)],'cream');s.poly([(6,34),(47,48),(53,79),(9,64)],'coral');s.ellipse([32,46,44,58],'cream')
 s.poly([(9,71),(54,86),(62,139),(20,150)],'teal2');s.poly([(20,118),(20,85),(26,87),(29,120)],'cream');s.poly([(31,125),(30,98),(38,101),(41,126)],'cream');s.poly([(46,135),(41,113),(47,114),(53,133)],'cream')
 # Rear scenic flat has a distinct blue sky / landscape, with rigid frame.
 s.poly([(55,55),(79,62),(93,135),(75,142)],'woodDark');s.poly([(58,58),(77,64),(89,132),(76,137)],'woodHi');s.poly([(62,64),(75,69),(85,129),(77,133)],'blue');s.poly([(71,107),(77,104),(82,112),(85,128),(77,132)],'green');s.line([(58,58),(77,64),(89,132)],'wood')
 # Unopened carton, then the overturned podium; distinct separate silhouettes.
 s.poly([(93,116),(111,113),(118,130),(99,135)],'woodDark');s.poly([(94,116),(109,115),(114,129),(99,132)],'woodLight');s.line([(103,115),(106,130)],'woodHi',2)
 s.poly([(71,111),(95,103),(103,130),(78,141)],'edge');s.poly([(74,112),(93,107),(98,128),(80,136)],'coralDark');s.poly([(78,139),(103,129),(109,134),(86,145)],'woodLight');s.line([(74,112),(93,107)],'coralLight',2)
 s.poly([(97,120),(110,115),(114,137),(103,140)],'woodDark');s.poly([(98,119),(111,116),(114,135),(104,138)],'woodHi')
 s.layer('foreground-crate-and-sandwich')
 s.poly([(0,148),(52,135),(74,144),(74,195),(0,205)],'ink');s.poly([(1,152),(71,145),(71,191),(1,201)],'teal0');s.poly([(0,148),(52,136),(72,144),(17,157)],'metalLight');s.poly([(4,147),(51,138),(66,144),(18,153)],'teal2');s.line([(1,157),(71,147)],'metalHi')
 s.rect([11,170,33,184],'edge');s.rect([12,171,32,182],'metalLight');s.rect([14,173,30,180],'ink');s.line([(15,174),(29,174)],'metalHi');s.rect([16,178,29,180],'teal1')
 s.line([(3,201),(70,191)],'metal');s.rect([3,198,8,201],'metalLight');s.rect([63,190,69,193],'metalLight');s.rect([65,150,68,153],'metalLight')
 # Half sandwich: bread triangle, one leaf and one filling, not tiny texture.
 s.poly([(21,142),(39,136),(49,142),(36,148)],'woodDark');s.poly([(22,140),(39,134),(49,140),(35,145)],'creamShade');s.poly([(23,138),(39,133),(49,138),(35,143)],'woodHi');s.poly([(24,142),(35,144),(47,139),(46,142),(35,147),(25,145)],'greenDark');s.line([(25,144),(35,146),(46,142)],'coral');s.poly([(25,146),(35,148),(46,144),(45,146),(35,151),(26,149)],'cream')
 # Small refill carton beside crate, no unreadable miniature prose.
 s.poly([(67,164),(76,160),(83,163),(83,187),(68,190)],'woodDark');s.poly([(68,165),(77,162),(81,164),(81,185),(69,188)],'paper');s.line([(77,163),(77,186)],'paperShade');s.poly([(69,179),(76,177),(76,184),(69,186)],'coral');s.poly([(71,167),(74,166),(75,171),(71,173)],'teal3')
 s.layer('two-readable-certificates')
 for points in [[(84,146),(101,142),(116,151),(98,156)],[(114,142),(130,139),(143,146),(127,153)]]:
  s.poly([(x+1,y+2) for x,y in points],'shadow');s.poly(points,'paper');s.line(points+[points[0]],'paperShade')
 s.line([(91,146),(101,144),(108,148)],'paperMark');s.rect([98,149,101,151],'coral');s.line([(122,143),(129,142),(136,146)],'paperMark');s.rect([128,146,131,148],'coral')
 s.layer('clapper-cabinet-attached-mechanism')
 # Cart remains the selected fixed mechanism design: plinth, shaft, linked paddles.
 s.ellipse([242,166,250,174],'ink');s.ellipse([269,164,277,172],'ink');s.rect([245,167,247,171],'metal');s.rect([272,165,274,169],'metal')
 s.poly([(239,125),(270,122),(281,128),(281,164),(248,169),(239,163)],'ink');s.poly([(241,130),(271,127),(278,130),(278,162),(248,166),(241,161)],'teal1');s.poly([(247,135),(275,132),(275,158),(247,161)],'cream');s.poly([(252,153),(257,146),(257,156),(252,157)],'coral');s.poly([(260,155),(266,141),(267,155)],'coral');s.poly([(270,154),(273,146),(273,153)],'coral')
 s.poly([(239,124),(269,121),(281,126),(249,131)],'teal3');s.line([(241,124),(269,122),(278,126)],'tealhi')
 # Fixed base plate bolted on the cart, rigid support and attached crank linkages.
 s.poly([(245,117),(271,115),(277,121),(249,124)],'metalDark');s.line([(247,118),(270,117)],'metalLight');s.rect([251,106,271,118],'ink');s.rect([253,108,269,115],'metal');s.rect([256,110,265,113],'edge');s.rect([263,112,266,113],'coralDark')
 s.rect([248,101,251,118],'metalDark');s.rect([270,100,273,117],'metalDark');s.line([(250,104),(271,104)],'ink',3);s.line([(251,103),(270,103)],'metalLight');s.rect([249,102,250,103],'metalHi');s.rect([271,101,272,102],'metalHi');s.line([(256,108),(256,99),(251,96)],'ink',3);s.line([(267,108),(267,98),(272,95)],'ink',3);s.line([(255,107),(255,100)],'metalLight');s.line([(266,107),(266,99)],'metalLight')
 s.poly([(242,94),(246,88),(257,89),(254,96)],'ink');s.poly([(244,93),(247,89),(255,90),(253,94)],'creamShade');s.line([(246,89),(254,90)],'creamHi')
 s.poly([(266,91),(268,87),(278,88),(281,94),(269,95)],'ink');s.poly([(267,91),(269,88),(277,89),(279,93),(269,94)],'creamShade');s.line([(270,88),(277,89)],'creamHi')
 s.line([(279,149),(287,148),(289,143),(289,133)],'ink',2);s.panel([287,128,293,136],'creamShade','edge','cream');s.rect([289,130,290,132],'ink')
 s.layer('wall-graphic')
 s.poly([(286,31),(307,20),(307,63),(286,72)],'edge');s.poly([(287,32),(305,23),(305,61),(287,69)],'cream');s.poly([(289,35),(303,28),(303,38),(289,44)],'coral');s.poly([(289,48),(303,42),(303,59),(289,65)],'teal2');s.line([(292,61),(292,50)],'cream',2);s.line([(298,58),(298,47)],'cream',2)
 s.save()

def restroom_symbol(s,x,y):
 s.panel([x,y,x+15,y+24],'teal0','creamShade','cream');s.ellipse([x+4,y+4,x+6,y+6],'cream');s.rect([x+4,y+8,x+6,y+15],'cream');s.line([(x+4,y+15),(x+4,y+20)],'cream');s.line([(x+6,y+15),(x+6,y+20)],'cream');s.ellipse([x+10,y+4,x+12,y+6],'cream');s.poly([(x+10,y+8),(x+12,y+8),(x+14,y+16),(x+8,y+16)],'cream');s.line([(x+10,y+16),(x+10,y+20)],'cream');s.line([(x+12,y+16),(x+12,y+20)],'cream')
def chair(s,x,y,w=23,h=20):
 s.poly([(x-2,y+h),(x+w+1,y+h),(x+w+3,y+h+3),(x,y+h+3)],'ink');s.poly([(x,y),(x+w-2,y),(x+w+1,y+3),(x+w-1,y+h),(x-2,y+h),(x-2,y+3)],'coralDark');s.poly([(x+1,y+1),(x+w-3,y+1),(x+w-1,y+3),(x+w-3,y+h-2),(x,y+h-2),(x,y+3)],'coral');s.line([(x,y+1),(x+w-3,y+1)],'coralHi');s.line([(x-2,y+3),(x-2,y+h)],'creamShade')
def locomotion():
 s=Scene('locomotion')
 s.rect([0,0,313,205],'wall0');s.rect([49,49,265,151],'teal2')
 s.poly([(0,21),(49,51),(49,154),(0,186)],'wall0');s.poly([(265,50),(313,20),(313,186),(265,154)],'creamShade')
 s.poly([(0,180),(49,159),(265,159),(313,183),(313,205),(0,205)],'floor')
 s.layer('ceiling-and-structural-trim')
 s.poly([(0,0),(313,0),(273,33),(40,33)],'creamShade');s.poly([(8,0),(304,0),(275,22),(38,22)],'coral');s.poly([(18,0),(293,0),(272,13),(41,13)],'cream');s.poly([(28,0),(284,0),(269,7),(45,7)],'wall0');s.line([(10,1),(39,23),(273,23),(304,1)],'coralLight',2)
 for pts in [[(0,16),(41,41),(273,41),(313,16)],[(0,23),(41,47)],[(313,23),(273,47)]]:s.line(pts,'creamHi',3)
 s.poly([(0,25),(10,29),(10,174),(0,181)],'teal0');s.line([(10,30),(10,173)],'teal3',2)
 s.poly([(42,43),(52,47),(52,156),(43,160)],'teal0');s.line([(49,48),(49,156)],'teal3',2)
 s.poly([(264,48),(274,43),(274,160),(264,155)],'teal0');s.line([(266,49),(266,155)],'teal3',2)
 s.poly([(304,28),(313,23),(313,182),(304,176)],'teal0');s.line([(304,29),(304,175)],'teal3',2)
 for b in [(58,3,94,12),(221,3,258,12),(132,44,182,50)]:
  x,y,x2,y2=b;s.poly([(x,y),(x2,y),(x2-2,y2),(x+2,y2)],'edge');s.poly([(x+2,y+1),(x2-2,y+1),(x2-3,y2-2),(x+3,y2-2)],'creamHi')
 # Title uses an explicit native bitmap alphabet, no font raster resampling.
 s.panel([65,24,250,43],'teal0','creamShade','creamHi');s.text(112,29,"PEOPLE'S PAVILION",'creamHi')
 # Pavilion emblems, same subject/position as approved signage.
 for x,flip in [(71,1),(236,-1)]:
  s.line([(x,36),(x+11*flip,36)],'cream',2);s.line([(x+2*flip,32),(x+10*flip,35)],'cream',2);s.line([(x+4*flip,28),(x+11*flip,33)],'cream',2)
 s.layer('curtain-and-backstage-opening')
 s.rect([53,66,263,146],'teal2')
 for x in [59,80,102,123,147,173,196]:
  s.poly([(x,66),(x+6,66),(x+4,143),(x+1,145)],'teal1');s.line([(x+7,69),(x+7,141)],'teal3')
 s.line([(51,62),(265,62)],'ink',3);s.line([(52,61),(264,61)],'metalLight')
 for x in range(57,263,17):s.rect([x,61,x+2,65],'creamShade')
 # Restroom glimpse behind right curtain, deliberately same geography.
 s.poly([(219,91),(238,68),(255,94),(255,141),(218,141)],'ink');s.poly([(221,94),(238,73),(252,95),(252,139),(220,139)],'wall0');s.rect([223,100,250,139],'creamShade');s.rect([225,100,248,105],'creamHi');s.rect([239,109,249,138],'teal2');s.line([(239,108),(249,108)],'teal4');s.rect([223,112,232,122],'metalLight');s.rect([224,113,231,120],'blue');s.line([(221,127),(235,127)],'creamHi',2);s.line([(222,129),(232,129)],'edge');s.line([(226,128),(226,135),(230,135)],'metalDark');s.rect([243,123,244,125],'creamShade')
 s.poly([(216,66),(228,66),(219,91),(220,135),(214,143),(208,143),(213,95)],'teal1');s.line([(222,68),(216,94),(216,137)],'teal4');s.poly([(240,66),(262,66),(260,141),(254,144),(254,95)],'teal2');s.line([(244,69),(257,95),(258,137)],'teal3',2)
 s.layer('side-wall-graphics-and-signs')
 s.poly([(12,53),(38,64),(38,95),(12,85)],'edge');s.poly([(14,55),(36,65),(36,92),(14,84)],'cream');s.poly([(15,58),(35,66),(35,76),(15,68)],'coral');s.ellipse([25,63,31,69],'cream');s.poly([(15,73),(35,81),(35,90),(15,83)],'teal2');s.line([(20,81),(20,75)],'cream',2);s.line([(27,84),(27,79)],'cream',2)
 restroom_symbol(s,281,69)
 s.panel([285,100,297,122],'cream','edge','creamHi');s.rect([288,104,294,109],'coral');s.rect([288,112,294,114],'teal2');s.rect([288,117,294,118],'teal2')
 s.poly([(280,128),(298,122),(298,126),(280,133)],'teal1');s.line([(281,130),(296,125)],'teal3')
 s.layer('countdown-display')
 s.rect([146,51,149,68],'metalDark');s.rect([174,51,177,68],'metalDark');s.line([(147,52),(147,66)],'metalLight');s.line([(175,52),(175,66)],'metalLight')
 s.panel([128,68,188,122],'teal0','creamShade','creamHi');s.rect([131,71,185,119],'teal0')
 # Discrete chunky arc markers with clean native edges.
 markers=[([(139,78),(144,74),(147,76),(142,80)],'cream'), ([(149,73),(155,72),(155,76),(150,77)],'cream'), ([(160,72),(165,73),(164,77),(159,76)],'coral'), ([(169,74),(174,77),(171,80),(167,77)],'coral'), ([(178,80),(181,85),(177,87),(175,82)],'coral'), ([(181,90),(182,95),(178,95),(178,90)],'coral'), ([(180,100),(179,106),(175,104),(176,99)],'cream'), ([(175,111),(170,115),(167,112),(172,108)],'cream'), ([(163,115),(157,116),(157,112),(162,112)],'cream'), ([(151,115),(145,112),(147,108),(152,111)],'cream'), ([(140,109),(136,105),(139,102),(143,106)],'cream'), ([(134,99),(134,93),(138,93),(138,98)],'cream'), ([(135,87),(137,81),(141,83),(139,88)],'cream')]
 for pts,c in markers:s.poly(pts,c)
 # 30, constructed as seven-segment glyphs; no new labels or changed numeral.
 x,y=145,85
 for pts in [[(x,y),(x+10,y),(x+10,y+2),(x,y+2)],[(x+9,y),(x+11,y),(x+11,y+10),(x+9,y+10)],[(x+1,y+9),(x+11,y+9),(x+11,y+11),(x+1,y+11)],[(x+9,y+10),(x+11,y+10),(x+11,y+20),(x+9,y+20)],[(x,y+18),(x+10,y+18),(x+10,y+20),(x,y+20)]]:s.poly(pts,'creamHi')
 s.rect([161,85,172,105],'creamHi');s.rect([164,88,169,102],'teal0')
 s.layer('raised-stage-architecture')
 s.poly([(43,146),(260,146),(281,155),(264,170),(43,170),(27,157)],'ink');s.poly([(43,145),(261,145),(278,155),(263,162),(43,162),(31,156)],'creamShade');s.poly([(45,146),(259,146),(271,153),(260,158),(45,158),(36,154)],'cream')
 s.poly([(34,157),(45,161),(263,161),(276,156),(274,166),(263,173),(43,173),(33,166)],'coralDark');s.poly([(38,158),(45,162),(263,162),(274,157),(272,164),(261,169),(44,169),(38,165)],'coral');s.line([(45,162),(263,162)],'coralHi');s.poly([(43,174),(264,174),(272,171),(273,175),(263,179),(43,179),(35,174)],'metalDark');s.line([(43,174),(264,174),(271,171)],'metalLight')
 s.layer('moving-floor-and-stationary-landing')
 # Left moving belt: bounded and visibly separate from the pit.
 s.poly([(63,137),(121,137),(131,153),(59,153)],'ink');s.poly([(66,139),(119,139),(127,150),(63,150)],'metalDark');s.poly([(68,140),(117,140),(123,148),(66,148)],'teal0')
 for x in [70,78,86,94,102,110]:s.line([(x,141),(x-1,147)],'teal2')
 s.poly([(93,142),(104,142),(104,140),(113,144),(104,148),(104,146),(91,146)],'creamShade')
 # Stationary landing is an uninterrupted cream platform around the rear/right.
 s.poly([(126,131),(217,131),(239,138),(250,147),(233,153),(216,142),(133,141)],'edge');s.poly([(131,131),(216,132),(236,139),(246,147),(235,150),(216,138),(135,138)],'creamShade');s.line([(134,132),(216,133),(235,140)],'creamHi')
 s.layer('single-perspective-padded-pit')
 # Four coordinated trapezoid edges, consistently narrowing toward rear.
 s.poly([(142,134),(211,134),(233,160),(126,160)],'ink');s.poly([(143,135),(210,135),(229,158),(130,158)],'orangeDark');s.poly([(149,139),(205,139),(219,154),(138,154)],'orangeLight')
 s.poly([(143,135),(149,139),(138,154),(130,158)],'coralDark');s.poly([(210,135),(205,139),(219,154),(229,158)],'coral');s.poly([(149,139),(205,139),(207,142),(146,142)],'orange')
 s.line([(176,141),(176,154)],'orangeDark');s.line([(145,148),(213,148)],'orangeDark');s.line([(144,149),(213,149)],'orangeHi');s.line([(177,143),(177,153)],'orangeHi')
 s.poly([(130,158),(229,158),(232,161),(126,161)],'coralLight');s.line([(131,158),(228,158)],'creamShade')
 s.layer('sparse-safety-net')
 # Native foreground corner ties ground the net in the pit rim.
 s.line([(131,143),(131,157)],'metalDark',2);s.line([(227,143),(227,157)],'metalDark',2);s.line([(130,144),(130,156)],'metalLight');s.line([(226,144),(226,156)],'metalLight')
 # Sparse net plane spans OVER the pit, broadening toward the front.
 # Exactly 3 draped crosswise ropes and 4 depth strands, not a rear fence.
 s.line([(134,138),(134,123)],'metalDark',3);s.line([(216,139),(216,123)],'metalDark',3);s.line([(133,124),(133,137)],'metalLight');s.line([(215,124),(215,138)],'metalLight')
 for pts in [[(134,124),(154,129),(191,129),(216,124)],[(133,134),(156,139),(197,139),(222,134)],[(131,143),(157,148),(204,148),(227,143)]]:s.line(pts,'creamShade')
 for pts in [[(148,127),(146,137),(144,146)],[(166,129),(165,139),(165,148)],[(184,129),(186,139),(188,148)],[(202,127),(207,138),(211,147)]]:s.line(pts,'cream')
 s.layer('presenter-native-silhouette')
 # Designed as a native sprite; small face and hand masses, no portrait sampling.
 s.ellipse([77,148,100,154],'shadow')
 s.poly([(80,131),(87,131),(86,149),(81,149)],'skin');s.poly([(91,132),(97,131),(96,149),(92,149)],'skin');s.line([(81,135),(81,147)],'skinShade');s.line([(92,136),(92,147)],'skinShade')
 s.poly([(80,148),(86,148),(88,151),(79,151)],'slateDark');s.poly([(92,148),(97,148),(100,151),(91,151)],'slateDark');s.line([(80,151),(88,151)],'metalDark');s.line([(92,151),(100,151)],'metalDark')
 s.poly([(79,117),(95,117),(97,134),(79,134)],'slateDark');s.poly([(80,118),(93,118),(95,132),(80,132)],'slate');s.line([(79,133),(95,133)],'slateHi')
 s.poly([(77,102),(83,99),(92,100),(98,108),(96,122),(82,123),(76,116)],'slateDark');s.poly([(79,103),(84,101),(91,101),(95,108),(93,121),(82,121),(78,115)],'slate');s.poly([(84,100),(89,101),(89,110),(85,107)],'coralLight');s.poly([(81,103),(84,101),(86,109),(82,107)],'slateHi')
 # One readable open arm/hand, preserving the established gesture.
 s.poly([(93,105),(96,103),(101,108),(108,105),(110,108),(100,113),(95,111)],'slateDark');s.poly([(95,105),(100,109),(107,106),(108,108),(100,111),(96,109)],'slateHi');s.poly([(107,105),(110,102),(112,103),(111,105),(115,105),(115,107),(109,109),(107,108)],'skin')
 # Near arm rests against the torso; no tiny individual fingers/buttons.
 s.poly([(78,107),(80,107),(82,115),(88,115),(88,119),(80,119),(76,112)],'slateDark');s.poly([(78,108),(80,115),(86,116),(86,118),(80,117),(77,112)],'slateHi');s.rect([85,115,89,118],'skin')
 s.rect([84,96,89,102],'skinShade');s.poly([(80,90),(83,86),(91,87),(94,92),(92,98),(85,100),(80,96)],'hairDark');s.poly([(79,88),(83,85),(90,85),(94,89),(93,96),(89,98),(80,97),(77,94)],'hair');s.poly([(81,87),(88,86),(91,88),(84,89),(82,93),(79,93)],'hairHi');s.poly([(85,90),(91,89),(92,94),(94,95),(91,98),(85,97),(83,94)],'skin');s.rect([90,92,90,93],'hairDark');s.rect([86,96,88,96],'skinShade')
 s.layer('microphone-and-green-console')
 s.ellipse([98,155,113,158],'metalDark');s.line([(105,154),(105,115)],'metalDark',2);s.line([(104,153),(104,115)],'metalLight');s.panel([102,111,108,119],'metal','ink','metalLight');s.line([(104,113),(106,113)],'metalDark');s.line([(104,116),(106,116)],'metalDark')
 s.poly([(227,132),(246,132),(250,142),(225,142)],'ink');s.poly([(228,133),(244,133),(247,139),(227,139)],'teal0');s.rect([230,135,235,137],'greenLamp');s.rect([240,135,243,138],'creamShade');s.line([(238,134),(237,138)],'teal3');s.poly([(231,143),(243,143),(245,154),(230,154)],'teal1');s.line([(231,143),(242,143)],'teal3')
 s.layer('foreground-camera-and-cart')
 s.ellipse([12,184,20,189],'ink');s.ellipse([37,181,45,187],'ink');s.rect([15,185,17,187],'metal');s.rect([40,182,42,185],'metal')
 s.poly([(8,181),(33,176),(49,181),(24,187)],'ink');s.poly([(10,180),(33,176),(47,180),(24,185)],'teal2');s.line([(12,180),(33,177),(44,180)],'teal4')
 s.line([(22,178),(22,135)],'ink',5);s.line([(21,177),(21,136)],'metalLight',2);s.line([(31,177),(31,139)],'metalDark',3);s.line([(30,176),(30,140)],'metalLight')
 s.ellipse([11,133,40,139],'ink');s.ellipse([13,132,38,137],'metal');s.line([(28,135),(28,130)],'metalDark',3)
 s.panel([9,107,50,132],'metal','ink','metalHi');s.rect([11,109,48,128],'creamShade');s.rect([12,110,46,112],'cream');s.rect([14,115,23,124],'teal0');s.line([(27,115),(42,115)],'metalDark',2);s.line([(27,120),(42,120)],'metalDark',2);s.line([(27,125),(40,125)],'metalDark',2)
 s.poly([(50,112),(59,115),(59,126),(50,129)],'ink');s.poly([(51,114),(56,116),(56,124),(51,126)],'teal1');s.rect([24,102,34,106],'ink');s.rect([26,102,32,105],'coral');s.line([(27,102),(31,102)],'coralHi')
 s.line([(12,134),(7,139),(7,170),(13,174)],'metalDark',2)
 s.layer('floor-joints-and-audience-seats')
 for pts in [[(52,180),(39,196)],[(99,180),(93,196)],[(152,180),(152,196)],[(204,180),(212,196)],[(253,180),(274,196)],[(31,188),(281,188)]]:s.line(pts,'tile')
 # Existing single empty coral chair at right, with grounded metal arms/feet.
 s.poly([(268,164),(294,159),(302,166),(298,189),(276,193),(264,184)],'ink');s.poly([(273,164),(293,161),(299,165),(295,183),(274,187),(268,182)],'coralDark');s.poly([(275,165),(293,163),(296,166),(293,181),(275,185),(271,180)],'coral');s.line([(276,164),(292,162)],'coralHi');s.line([(268,180),(265,179),(265,188),(274,192)],'creamShade',2);s.line([(294,183),(300,183),(300,190),(295,192)],'metalLight',2);s.line([(275,191),(273,196)],'metalDark',2);s.line([(295,190),(297,196)],'metalDark',2)
 for x in [0,40,81,122,163,204,245,286]:chair(s,x,198,33,15)
 s.save()

if __name__=='__main__':
 backstage();locomotion();print('Rebuilt two candidates directly at 314x206; exported exact 4x previews and semantic native layers.')
