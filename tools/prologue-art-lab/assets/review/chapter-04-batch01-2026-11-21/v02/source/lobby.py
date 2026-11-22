"""v02 lobby: independently authored directly at 314x206, with no raster inputs."""
from pathlib import Path
from pixel_primitives import Canvas

def lobby(out):
 c=Canvas(314,206)
 # Depth planes. All color modeling is painted as explicit native pixel clusters.
 c.box((0,0,313,205),'#96988b')
 c.poly([(0,0),(81,24),(81,149),(0,181)],'#9a9b8b')
 c.box((81,24,313,149),'#c4b99e')
 c.box((81,116,313,149),'#71877d')
 c.box((81,144,313,149),'#465850')
 c.line([(81,117),(313,117)],'#d1c5a6')
 # Back-wall light falls toward the service passage; localized planes, no haze.
 c.box((87,31,148,115),'#d6c8a8');c.box((149,31,223,115),'#cbbf9f');c.box((224,31,313,115),'#b6ad95')
 c.box((87,119,147,143),'#83958a');c.box((149,119,223,143),'#778b80');c.box((224,119,313,143),'#687c73')
 # Perspective floor tiles: differentiated slab faces, fine highlighted seams.
 c.poly([(0,181),(81,149),(313,149),(313,205),(0,205)],'#949b8c')
 horizon=(182,99)
 rows=[149,154,161,171,185,205]
 rays=[-680,-480,-300,-155,-40,58,137,211,294,397,530,700,910]
 def point(x,y):return (round(182+(x-182)*(y-99)/106),y)
 colors=['#939b8c','#9da494','#a3aa98','#8b9588','#a8ac9b','#989e8e']
 for row,(ya,yb) in enumerate(zip(rows,rows[1:])):
  for col,(xa,xb) in enumerate(zip(rays,rays[1:])):
   pts=[point(xa,ya),point(xb,ya),point(xb,yb),point(xa,yb)]
   c.poly(pts,colors[(col*3+row*2)%len(colors)])
   c.line([pts[0],pts[1]],'#626f66');c.line([pts[0],pts[3]],'#677369')
   c.line([(pts[0][0]+1,ya+1),(pts[1][0],ya+1)],'#b8bdab')
 # Left foreground floor continues from the same planar tiling.
 c.poly([(0,181),(81,149),(107,149),(6,205),(0,205)],'#9da494')
 for pts in [[(0,185),(89,151)],[(0,196),(103,153)],[(12,205),(104,158)]]:c.line(pts,'#6a776b')
 # Faded carpet with woven border motifs and concentrated worn patches.
 c.poly([(157,149),(218,149),(264,205),(91,205)],'#593c43')
 c.poly([(159,149),(216,149),(257,205),(98,205)],'#92555b')
 c.poly([(163,149),(212,149),(244,205),(111,205)],'#854b53')
 c.line([(161,150),(104,205)],'#bf9c72');c.line([(214,150),(250,205)],'#b49068')
 c.line([(165,150),(115,205)],'#b08165');c.line([(210,150),(239,205)],'#ad8065')
 for y,x,w in [(154,159,1),(160,153,2),(168,145,2),(179,134,3),(193,120,4)]:
  c.poly([(x,y),(x+w,y-2),(x+w*2,y),(x+w,y+2)],'#d1ad7e')
  xx=216+round((y-149)*0.65)
  c.poly([(xx,y),(xx+w,y-2),(xx+w*2,y),(xx+w,y+2)],'#c5a075')
 for pts in [[(170,159),(180,158),(184,160),(178,161)],[(146,186),(153,183),(164,183),(160,186)],[(201,192),(210,190),(218,192),(215,194)],[(169,199),(180,199),(183,201),(173,202)]]:c.poly(pts,'#a8736c')
 # Ceiling: coffers and the mundane concrete structure under the decoration.
 c.poly([(0,0),(313,0),(313,23),(81,27)],'#8d9286')
 for x in [57,127,199,273]:
  c.poly([(x-24,0),(x-15,0),(x+20,23),(x+11,23)],'#b5b39d')
  c.line([(x-15,1),(x+20,23)],'#737f74');c.line([(x-23,1),(x+11,22)],'#d1c8ac')
 c.line([(79,26),(313,22)],'#586a61',3)
 c.line([(83,27),(313,24)],'#ded1af',2)
 c.line([(83,31),(313,28)],'#a69b80')
 c.line([(84,33),(313,30)],'#e0d3b2')
 # Window wall. Larger objects receive physically connected frame sections.
 c.poly([(9,0),(65,18),(65,88),(9,70)],'#4c6056')
 c.poly([(12,0),(62,20),(62,84),(12,68)],'#b8c9b7')
 c.poly([(15,13),(48,23),(48,79),(15,68)],'#a1b3a6')
 c.poly([(19,25),(43,32),(43,77),(19,68)],'#c1cabc')
 c.line([(25,29),(25,71)],'#879c91');c.line([(35,32),(35,74)],'#e0dfc9')
 for yy in [38,50,62]:c.line([(20,yy),(43,yy+7)],'#8c9f93')
 for x in [27,45]:
  yy=(x-9)//3;c.line([(x,yy),(x,70+yy)],'#455e54',3);c.line([(x-1,yy),(x-1,68+yy)],'#e5dec4')
 for y in [14,34,54]:
  c.line([(10,y),(64,y+17)],'#465f54',3);c.line([(11,y-1),(63,y+15)],'#e0dcc4')
 c.line([(10,71),(65,89)],'#5c6b5c',3);c.line([(11,70),(65,87)],'#d8d2b7',2)
 c.poly([(9,73),(65,91),(65,94),(9,76)],'#bfb397')
 c.line([(12,77),(12,91),(18,93)],'#6e7969')
 # Concrete column at the entrance, chipped and covered by a cheap scalloped panel.
 c.poly([(0,0),(9,0),(9,164),(0,168)],'#b8b59d')
 c.line([(7,0),(7,163)],'#dad1b1')
 c.box((0,99,12,102),'#d9c9a7');c.box((0,103,10,108),'#9b997e')
 c.box((0,155,11,159),'#c7b798');c.box((0,160,13,164),'#7e8472')
 c.line([(2,84),(3,89),(1,92)],'#838b79')
 # Burgundy drapery: directional folds, pooled edge shadows, thin fringe.
 def swag(x,y,w):
  c.poly([(x,y),(x+w,y-1),(x+w-4,y+8),(x+w-13,y+14),(x+17,y+12),(x+5,y+5)],'#643942','#43333a')
  c.poly([(x+3,y+1),(x+w-3,y),(x+w-9,y+6),(x+w-17,y+10),(x+18,y+8)],'#83434c')
  c.line([(x+5,y+2),(x+19,y+7),(x+w-17,y+8),(x+w-6,y+2)],'#a3615e')
  c.line([(x+8,y+7),(x+19,y+12),(x+w-15,y+14),(x+w-5,y+7)],'#baa172')
  for k in range(x+17,x+w-12,4):c.line([(k,y+13),(k,y+15)],'#977f58')
 for x,w in [(83,57),(141,50),(192,50),(262,52)]:swag(x,32,w)
 c.poly([(81,39),(92,42),(92,94),(84,92)],'#6b3b43','#4a353a')
 c.line([(85,42),(87,87)],'#ad655f',2);c.line([(90,46),(90,91)],'#8a4b50')
 c.line([(84,93),(91,95)],'#bea071')
 # Raised/depressed panel moldings catch actual directional light.
 def panel(x,y,w,h):
  c.box((x,y,x+w,y+h),'#b2a68b')
  c.line([(x,y+h),(x+w,y+h),(x+w,y)],'#7e7c67')
  c.line([(x+1,y+h-1),(x+1,y+1),(x+w-1,y+1)],'#e0d2ae')
  c.box((x+3,y+3,x+w-3,y+h-3),'#c6b99a')
  c.line([(x+3,y+h-3),(x+3,y+3),(x+w-3,y+3)],'#a09478')
  c.line([(x+4,y+h-4),(x+w-4,y+h-4)],'#d8caa7')
 for x,w in [(102,42),(149,35),(189,43),(265,44)]:panel(x,78,w,12)
 for pts in [[(118,83),(122,78),(121,74),(128,69)],[(228,95),(225,91),(228,86)],[(282,86),(286,82),(285,77)]]:
  c.line(pts,'#777d68');c.line([(pts[0][0]+1,pts[0][1]),(pts[1][0]+1,pts[1][1])],'#e0d0aa')
 # Exposed substrate is shaped as flaking plaster, with a lit broken edge.
 for pts in [[(93,122),(99,118),(103,122),(108,121),(110,131),(103,137),(95,134)],[(232,130),(235,125),(242,126),(245,133),(240,142),(233,139)],[(286,136),(292,132),(300,135),(298,143),(289,144)]]:
  c.poly(pts,'#a99e83');c.line(pts[:3],'#d6c7a4');c.line(pts[-3:],'#5e7568')
 # Big cylindrical silver duct: multiple tonal planes, collars, curved elbow.
 c.box((97,52,244,72),'#455950')
 for ya,yb,col in [(53,54,'#8eaaa0'),(55,57,'#d6dfcc'),(58,61,'#b5c9b8'),(62,65,'#8fa99b'),(66,68,'#718c7e'),(69,70,'#567063')]:c.box((98,ya,243,yb),col)
 for x in [110,132,157,181,206,231]:
  c.box((x,52,x+2,72),'#596f62');c.line([(x+1,53),(x+1,57)],'#e3e7d2');c.line([(x+2,58),(x+2,68)],'#b0c4b0')
  c.box((x-1,62,x-1,63),'#526c5e')
 for x in [125,193,240]:
  c.box((x,72,x+4,79),'#5c6f61');c.box((x+1,73,x+2,77),'#b6c5b0');c.box((x+1,78,x+2,78),'#d4d5bd')
 c.poly([(75,9),(92,9),(92,37),(95,46),(103,52),(105,55),(105,72),(96,70),(85,62),(79,52),(75,39)],'#5c786a','#3b5149')
 c.poly([(78,10),(88,10),(88,39),(91,48),(98,54),(104,56),(104,63),(97,61),(87,54),(81,44),(78,33)],'#a7c0af')
 c.line([(80,11),(80,36),(84,47),(92,55),(103,59)],'#d9e2cb',2)
 c.line([(87,11),(87,35),(91,46),(97,50)],'#78998a',2)
 for pts in [[(76,19),(91,19)],[(76,33),(91,33)],[(80,48),(93,43)],[(87,61),(99,50)]]:
  c.line(pts,'#597466');c.line([(x,y+1) for x,y in pts],'#c4d1b9')
 # Large trim frames keep paired facilities the clearest destination.
 def door(x,y,w,h,female):
  c.box((x-5,y-5,x+w+5,y+h+1),'#756f5d')
  c.box((x-4,y-4,x+w+3,y+h),'#d4c7a5')
  c.line([(x-3,y+h-1),(x-3,y-3),(x+w+2,y-3)],'#f1e0b9')
  c.line([(x+w+2,y-2),(x+w+2,y+h)],'#9b9277')
  c.box((x-1,y-1,x+w+1,y+h),'#3b5148')
  c.box((x,y,x+w,y+h-1),'#5b796b');c.box((x+2,y+2,x+w-2,y+h-3),'#6f8a79')
  c.line([(x+2,y+2),(x+w-2,y+2)],'#9baa91');c.line([(x+2,y+3),(x+2,y+h-3)],'#829a85')
  c.box((x+4,y+7,x+w-4,y+23),'#4e685a')
  cx=x+w//2;c.ellipse((cx-1,y+9,cx+1,y+11),'#f0e4bf')
  if female:c.poly([(cx-1,y+12),(cx+1,y+12),(cx+4,y+18),(cx-4,y+18)],'#f0e4bf')
  else:c.box((cx-2,y+12,cx+2,y+16),'#f0e4bf')
  c.line([(cx-1,y+17),(cx-1,y+21)],'#f0e4bf');c.line([(cx+1,y+17),(cx+1,y+21)],'#f0e4bf')
  c.box((x+w-5,y+31,x+w-3,y+36),'#3e574b');c.box((x+w-5,y+31,x+w-3,y+34),'#a9bda6')
  c.line([(x+w-6,y+35),(x+w-2,y+35)],'#e5e3c6')
  c.box((x+3,y+h-10,x+w-3,y+h-4),'#91a18b');c.line([(x+4,y+h-9),(x+w-4,y+h-9)],'#bec5a9')
  for yy in [y+7,y+h-14]:c.box((x,yy,x+1,yy+3),'#bfccb2')
 door(154,93,25,55,False);door(197,93,25,55,True)
 # Ballroom opening, distant piano and actual hinge-connected open doors.
 c.poly([(42,89),(86,92),(86,146),(42,158)],'#5b4943','#493d37')
 c.poly([(46,94),(81,97),(81,143),(46,151)],'#b7a386')
 c.box((53,100,79,135),'#695851');c.poly([(53,100),(79,100),(74,106),(59,107)],'#d2bea0')
 c.line([(55,102),(62,111),(71,111),(77,102)],'#ede0bb')
 for x in [54,76]:
  c.box((x,104,x+3,131),'#84464c');c.line([(x+1,105),(x+1,129)],'#bd7b6b')
 c.poly([(58,128),(73,113),(77,115),(71,130)],'#303e38')
 c.line([(60,127),(73,116)],'#526358')
 c.box((55,130,80,134),'#2d3c36');c.box((55,129,69,130),'#e7d7b2')
 for xx in range(57,69,3):c.box((xx,129,xx,130),'#3e4940')
 c.line([(59,134),(58,142)],'#3e443b',2);c.line([(76,134),(78,139)],'#3e443b',2)
 c.poly([(44,94),(51,98),(51,151),(44,154)],'#765d46','#4c4436')
 c.line([(46,97),(49,100),(49,147),(46,149),(46,97)],'#b4986a')
 c.poly([(82,97),(86,94),(86,145),(82,147)],'#715742','#4b4134')
 c.line([(84,100),(84,141)],'#a48a5f')
 # Broad functional collection passage and rolling cart. Clearance remains open.
 c.box((268,90,313,150),'#474f43')
 c.line([(267,149),(267,89),(313,89)],'#d3c3a0',3)
 c.line([(269,91),(313,91)],'#a89d80')
 c.poly([(272,95),(313,95),(304,108),(285,108),(285,136),(272,147)],'#7f8e7b')
 c.poly([(286,109),(304,109),(304,136),(286,138)],'#596e5e')
 c.poly([(273,147),(286,136),(304,136),(313,148)],'#9ba592')
 c.line([(285,108),(285,137)],'#d0c8a7');c.line([(288,135),(288,115)],'#788f79')
 for x,y,w in [(281,98,26),(286,106,19),(290,112,11)]:
  c.box((x,y,x+w,y+2),'#dce0bd');c.line([(x,y+3),(x+w,y+3)],'#506454')
 c.box((295,126,305,138),'#9b8359','#5d604c');c.line([(297,128),(304,136)],'#d1b57e');c.line([(303,128),(297,136)],'#6e7057')
 c.line([(293,139),(307,139)],'#3e5949',2);c.ellipse((294,139,296,141),'#303e36');c.ellipse((304,139,306,141),'#303e36')
 # Exposed service riser and bent electrical conduit, silver instead of steampunk.
 for x,col in [(251,'#4c6759'),(252,'#a6b9a0'),(253,'#cdd6b8'),(254,'#79947e')]:c.line([(x,30),(x,128)],col)
 for yy in [42,83,119]:
  c.box((249,yy,257,yy+2),'#536c5a');c.line([(250,yy),(256,yy)],'#bfc9ab')
 c.line([(254,77),(244,77),(240,81),(240,103),(244,108),(252,108)],'#3d5145',2)
 c.line([(242,102),(242,82),(245,79)],'#9caa8c')
 c.box((237,84,246,98),'#536c59','#3f5144');c.box((239,86,244,94),'#9bad8e')
 c.box((240,88,243,89),'#c5c9a5');c.box((240,92,242,93),'#3e5847')
 c.line([(260,78),(313,78)],'#46594b',2);c.line([(260,80),(313,80)],'#9f9e80')
 # Wall sconces with four hard-edged lighting planes.
 for x in [143,232]:
  c.box((x,109,x+2,118),'#6c6b4f');c.box((x-1,117,x+3,119),'#aa9566')
  c.poly([(x-3,99),(x+5,99),(x+4,110),(x-2,110)],'#d6b67a','#726d4c')
  c.poly([(x-2,100),(x+3,100),(x+2,108),(x-1,108)],'#f7e7b1')
  c.box((x-2,97,x+4,99),'#78704d');c.line([(x,100),(x,108)],'#e9cc8c')
 # Small people use fabric masses, gesture and hair; faces remain single clusters.
 def human(x,y,coat,hair,gesture=False):
  c.ellipse((x-5,y+30,x+9,y+33),'#657b67')
  c.poly([(x-2,y+20),(x+2,y+20),(x+1,y+30),(x-3,y+31)],'#3a4e41')
  c.poly([(x+3,y+20),(x+6,y+20),(x+8,y+31),(x+4,y+31)],'#2e4338')
  c.line([(x-3,y+31),(x+1,y+31)],'#263e32',2);c.line([(x+4,y+31),(x+9,y+31)],'#263e32',2)
  c.poly([(x-3,y+9),(x+5,y+8),(x+7,y+21),(x-4,y+21)],coat,'#384b3f')
  c.poly([(x-1,y+10),(x+2,y+10),(x+1,y+16)],'#dcd1aa')
  c.box((x-1,y+3,x+4,y+8),'#c4a77d');c.poly([(x-2,y+3),(x,y),(x+5,y+1),(x+5,y+4),(x+2,y+3),(x-2,y+4)],hair)
  if gesture:
   c.line([(x+6,y+11),(x+11,y+6),(x+12,y+3)],coat,3);c.box((x+11,y+1,x+13,y+4),'#d1b286')
   c.line([(x-3,y+12),(x-6,y+17),(x-1,y+19)],coat,3);c.box((x-1,y+18,x+1,y+20),'#d1b286')
  else:
   c.line([(x-3,y+12),(x-4,y+21)],coat,3);c.box((x-5,y+21,x-3,y+23),'#c7a77b')
   c.line([(x+6,y+12),(x+8,y+20)],coat,3);c.box((x+7,y+20,x+9,y+22),'#c7a77b')
 human(112,118,'#4b5d4e','#bdc1a2');human(123,119,'#6f4d4a','#665540')
 human(261,120,'#6c7d67','#3d594b')
 # Showman, auction platform and bevelled worn wooden podium.
 c.poly([(0,166),(50,151),(71,159),(0,182)],'#4b3e38')
 c.poly([(0,165),(50,150),(71,157),(12,176)],'#8b6c50')
 c.poly([(0,177),(12,177),(70,159),(70,166),(1,188)],'#704047')
 for x in range(8,65,5):c.line([(x,176-x//4),(x,182-x//4)],'#a06159')
 human(23,92,'#90404d','#d4d3b8',True)
 c.poly([(8,120),(47,115),(57,121),(16,129)],'#be9a68','#514c39')
 c.line([(11,121),(47,117),(54,121)],'#e0bc81')
 c.poly([(16,130),(55,123),(55,157),(16,168)],'#8c6e4d','#514b39')
 c.poly([(8,123),(15,130),(15,167),(8,163)],'#6c5941','#4c4536')
 c.poly([(21,134),(50,128),(50,153),(21,161)],'#644f3a','#c19a64')
 c.poly([(24,137),(47,132),(47,150),(24,157)],'#91714c')
 c.line([(26,139),(26,154)],'#b58f5c');c.line([(45,134),(45,149)],'#725d41')
 c.line([(18,165),(54,155)],'#d2aa6c');c.line([(8,161),(14,164)],'#b69a67')
 c.line([(40,117),(40,106),(37,103)],'#364c3e');c.ellipse((34,101,38,104),'#839781','#344d3d')
 c.line([(37,99),(40,94)],'#75583b',2);c.line([(38,93),(43,96)],'#a77c4d',3)
 # Wilting arrangements: individual petal clusters, bent stems and faceted urns.
 def arrangement(x,y,large=False):
  s=1 if not large else 1.25
  c.ellipse((x-7,y+15,x+9,y+18),'#536d58')
  c.poly([(x-5,y),(x+6,y),(x+4,y+14),(x+7,y+16),(x-6,y+16),(x-3,y+13)],'#a1a28a','#626e58')
  c.poly([(x-3,y+1),(x+1,y+1),(x,y+13),(x-2,y+13)],'#ddd2af')
  c.line([(x+3,y+2),(x+2,y+12)],'#858e73');c.ellipse((x-6,y-2,x+7,y+2),'#c7bea0','#6e7d64')
  stems=[(-11,-20),(-7,-29),(-2,-23),(3,-33),(8,-25),(12,-15),(0,-35)]
  for i,(dx,dy) in enumerate(stems):
   dy=round(dy*s);dx=round(dx*s)
   c.line([(x,y),(x+dx//2,y+dy//2),(x+dx,y+dy)],'#66794f')
   c.poly([(x+dx//2,y+dy//2),(x+dx//2-5,y+dy//2-4),(x+dx//2-5,y+dy//2-1)],'#83925d')
   c.poly([(x+dx//2+1,y+dy//2-2),(x+dx//2+6,y+dy//2-6),(x+dx//2+5,y+dy//2-2)],'#9ba46a')
   xx,yy=x+dx,y+dy
   if i in [1,4]:
    c.line([(xx,yy),(xx+2,yy-2),(xx+4,yy)],'#9b9160');xx+=4
   c.poly([(xx-3,yy),(xx-1,yy-2),(xx,yy-4),(xx+1,yy-1),(xx+4,yy),(xx+1,yy+1),(xx,yy+3),(xx-1,yy+1)],'#ded9ae')
   c.box((xx-1,yy-1,xx+1,yy+1),'#f0e9c3');c.box((xx,yy,xx,yy),'#b49d62')
  c.line([(x+7,y-8),(x+10,y-3),(x+13,y-4)],'#8a9258')
 arrangement(134,132);arrangement(238,136)
 arrangement(4,186,True);arrangement(309,183,True)
 # A tired modest chandelier; light glass clusters, practical chain and metal.
 c.line([(173,0),(173,14)],'#536450')
 for yy in [3,7,11]:c.ellipse((172,yy,174,yy+2),'#a8a17d')
 c.ellipse((170,14,176,18),'#a3996b','#4d5e49')
 c.line([(161,23),(165,28),(173,30),(181,28),(185,23)],'#a99765',2)
 for dx,dy in [(-12,21),(-6,22),(0,20),(6,22),(12,21)]:
  c.box((173+dx-2,dy-4,173+dx+2,dy),'#e0cf9e','#9c9467')
  c.box((173+dx-1,dy-3,173+dx+1,dy-1),'#f3e5b5');c.line([(173+dx,dy+5),(173+dx,dy+9)],'#a9bc9d');c.box((173+dx,dy+10,174+dx,dy+11),'#dae0b6')
 c.save(out)

if __name__=='__main__':lobby(Path(__file__).resolve().parent.parent/'native/CH4-01-lobby-v02.png')
