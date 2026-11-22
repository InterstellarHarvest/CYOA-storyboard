"""CH4 Batch 1 v01 independent reconstruction.

Starts directly at each contracted size using pixel primitives. Stage-A images
were visually inspected, but are never opened, sampled, traced, resized or used
as raster inputs here. This source is the editable native-grid master.
"""
from pathlib import Path
from pixel_primitives import *

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'native'

def lobby():
 c=Canvas(314,206)
 # Architectural masses: entrance-left camera, shallow back wall, tiled floor.
 c.poly([(0,0),(314,0),(314,25),(77,29)],'plaster')
 c.poly([(0,0),(79,28),(79,140),(0,179)],'wall')
 c.box((80,28,313,140),'cream')
 c.box((80,119,313,140),'tealLight')
 c.poly([(0,172),(80,137),(314,137),(314,205),(0,205)],'floor')
 for yy in [142,148,157,170,188]:
  c.line([(0,yy+(172-yy)//3),(80,yy),(314,yy)],'shadow')
 for x in range(-550,900,73):
  endx=round(185+(x-185)*0.18)
  c.line([(endx,138),(x,205)],'shadow')
 # The faded runner points to the actual facilities.
 c.poly([(159,139),(214,139),(251,205),(94,205)],'redDark')
 c.poly([(161,139),(212,139),(245,205),(101,205)],'red')
 c.line([(164,140),(110,205)],'gold');c.line([(209,140),(237,205)],'gold')
 for x,y in [(146,169),(177,151),(194,188),(152,193),(206,176),(188,161)]:
  c.line([(x,y),(x+7,y)],'redLight');c.line([(x+2,y+2),(x+10,y+2)],'redLight')
 # Ceiling bays and inexpensive cornice.
 for x in [86,150,220,284]:
  c.line([(x-25,0),(x+4,25)],'shadow');c.line([(x-22,0),(x+7,25)],'cream')
 c.line([(74,27),(313,24)],'shadow',3);c.line([(79,31),(313,28)],'light')
 # Tall left glazing; sky and the unremarkable neighbouring concrete wall.
 c.poly([(11,0),(63,21),(63,83),(11,67)],'metalDark','dark')
 c.poly([(14,0),(60,23),(60,79),(14,64)],'#b9c8bf')
 c.poly([(17,15),(53,27),(53,76),(17,64)],'#a0afa9')
 for y in [13,31,49]:
  c.line([(12,y),(62,y+18)],'shadow',2);c.line([(13,y-1),(61,y+17)],'cream')
 for x in [27,44]: c.line([(x,3+(x-11)//3),(x,68+(x-11)//3)],'shadow',2)
 c.line([(12,67),(63,84)],'light',3)
 # Shallow decorative panels; small omissions expose real plaster beneath.
 for x,w in [(100,40),(147,36),(190,41),(259,45)]:
  c.box((x,72,x+w,88),'wall','gold');c.line([(x+1,73),(x+w-1,73)],'light')
 for pts in [[(116,78),(119,75),(118,70),(123,65)],[(221,90),(220,83),(224,78)],[(288,77),(286,73),(288,68)]]:
  c.line(pts,'shadow')
 for pts in [[(92,111),(99,109),(103,114),(102,123),(93,125)],[(235,122),(240,117),(246,120),(246,130),(238,131)],[(292,120),(302,120),(304,128),(295,132)]]:
  c.poly(pts,'plaster');c.line(pts[:3],'shadow')
 # Scalloped drapes are thin cosmetic cover, interrupted by ventilation.
 for x,w in [(84,56),(141,47),(190,49),(262,51)]:
  c.poly([(x,32),(x+w,29),(x+w-3,39),(x+w-13,46),(x+15,43),(x+3,36)],'redDark','shadow')
  c.line([(x+4,33),(x+16,41),(x+w-15,44),(x+w-4,36)],'redLight')
  c.line([(x+7,37),(x+17,44),(x+w-15,47),(x+w-5,40)],'gold')
 drape(c,84,37,9,51)
 # Large industrial duct with a clear elbow and repeatable cylindrical bands.
 duct(c,94,51,242,68)
 c.poly([(75,12),(92,12),(92,41),(96,49),(103,51),(103,68),(91,65),(82,57),(76,45)],'metalDark','ink')
 c.poly([(78,13),(89,13),(89,42),(93,51),(100,55),(100,63),(90,60),(82,51),(79,42)],'silver')
 c.line([(80,15),(80,41),(83,49),(90,56),(98,58)],'metalLight',2)
 for yy in [19,32,43]: c.line([(77,yy),(91,yy)],'shadow');c.line([(78,yy+1),(90,yy+1)],'metalLight')
 for x in [126,198,239]:
  c.box((x,69,x+3,77),'shadow');c.box((x+1,70,x+2,74),'silver')
 # Lobby ballroom connection at left, with distant wedding piano.
 c.poly([(42,85),(87,90),(87,137),(42,147)],'shadow','woodDark')
 c.poly([(46,90),(82,94),(82,135),(46,142)],'redDark')
 c.box((52,96,78,125),'wall');drape(c,53,97,5,29);drape(c,75,97,4,30)
 c.poly([(59,120),(70,109),(73,110),(69,122)],'ink')
 c.box((58,123,76,126),'ink');c.line([(61,126),(60,133)],'woodDark');c.line([(74,126),(74,133)],'woodDark')
 c.poly([(44,91),(51,94),(51,141),(44,144)],'wood','woodDark');c.line([(46,93),(46,140)],'woodLight')
 c.poly([(83,93),(87,91),(87,136),(82,138)],'wood','woodDark')
 # Pair of true restroom doorways. Short, legible pictograms only.
 for x,female in [(155,False),(194,True)]:
  door(c,x,96,23,42)
  c.box((x+6,100,x+17,113),'tealDark')
  c.box((x+10,102,x+12,104),'cream')
  if female:c.poly([(x+10,105),(x+12,105),(x+15,111),(x+8,111)],'cream')
  else:c.box((x+9,105,x+13,109),'cream')
  c.line([(x+10,109),(x+10,113)],'cream');c.line([(x+12,109),(x+12,113)],'cream')
 # Deliberately plain broad collection/service route, empty enough for later lots.
 door(c,267,94,44,44,True)
 c.box((278,98,307,130),'tealDark')
 c.poly([(278,98),(307,98),(302,104),(284,104)],'metalDark')
 for y,w in [(100,16),(108,12),(115,8)]:c.box((285,y,285+w,y+1),'light')
 c.box((291,121,300,133),'wood','woodDark');c.line([(292,122),(299,132)],'woodLight')
 c.line([(279,137),(291,128),(311,128)],'metalDark')
 # Exposed plumbing/cabling are purposeful, not ornamental machinery.
 pipe(c,[(251,32),(251,120)],4)
 for yy in [44,87,114]: c.box((247,yy,255,yy+2),'metalDark');c.line([(248,yy),(254,yy)],'silver')
 c.line([(252,78),(241,78),(239,81),(239,103),(244,106),(251,106)],'ink')
 c.box((237,83,244,92),'metalDark','dark');c.box((239,85,242,89),'silver')
 c.line([(258,76),(313,76)],'dark',2);c.line([(259,78),(313,78)],'shadow')
 # Lamps, wilting flowers, small off-center chandelier.
 for x in [146,225]:
  c.box((x-1,101,x+1,109),'woodDark');c.poly([(x-3,96),(x+3,96),(x+2,104),(x-2,104)],'light','gold')
 flowers(c,133,124);flowers(c,235,126)
 chandelier(c,170,2)
 # Incidental small people: no eyes, nose or mouth attempted.
 person(c,108,113,'dark');person(c,118,113,'redDark',hair='woodDark')
 person(c,260,113,'metalDark',hair='tealDark')
 # Showman and wood podium on left: matching silver/crimson identity.
 c.poly([(0,153),(56,140),(76,147),(0,171)],'redDark','woodDark')
 c.poly([(0,153),(56,140),(76,147),(13,163)],'woodLight')
 person(c,24,93,'red','show')
 c.poly([(13,116),(43,113),(46,118),(15,122)],'woodLight','woodDark')
 c.poly([(15,122),(43,118),(43,143),(15,150)],'wood','woodDark')
 c.poly([(19,125),(39,122),(39,140),(19,145)],'woodDark')
 c.line([(21,126),(36,124),(36,139),(21,143),(21,126)],'woodLight')
 c.line([(34,115),(34,107),(32,105)],'ink');c.ellipse((30,103,33,106),'metalDark')
 c.line([(34,99),(37,94)],'woodDark',2);c.line([(34,93),(39,96)],'woodDark',3)
 c.line([(15,148),(44,142)],'gold')
 c.box((5,163,14,166),'shadow');c.line([(0,170),(19,165)],'cream')
 c.save(OUT/'CH4-01-lobby-v01.png')

def portrait_background():
 # Independently drawn tighter camera at the left-hand podium, no scene import.
 c=Canvas(564,278)
 c.box((0,0,563,277),'cream');c.box((0,235,563,277),'tealLight')
 # Wide cropped architectural panel on the right.
 c.box((331,55,442,226),'wall','shadow');c.box((335,59,438,222),'cream','gold')
 c.line([(337,61),(436,61)],'light');c.line([(337,61),(337,219)],'light')
 c.box((457,55,563,226),'wall','shadow');c.box((461,59,563,222),'cream','gold')
 c.line([(463,61),(563,61)],'light')
 c.box((446,48,453,277),'wall');c.line([(448,49),(448,235)],'light')
 # Large broken plaster cluster, not overall grime.
 c.poly([(345,186),(351,176),(358,179),(365,167),(368,175),(376,173),(380,180),(387,180),(386,195),(378,201),(365,198),(358,208),(348,202)],'plaster')
 c.line([(346,186),(352,177),(358,181),(365,169)],'shadow')
 c.line([(406,80),(400,88),(402,98),(394,107),(397,119),(390,126)],'shadow')
 c.line([(408,79),(403,89)],'light')
 for pts in [[(467,242),(474,236),(486,240),(490,254),(481,260),(471,257)],[(534,264),(542,256),(551,258),(557,271),(547,277),(534,275)]]:
  c.poly(pts,'plaster');c.line(pts[:3],'shadow')
 # Silver cylinder occupies upper crop, with discrete curved shading bands.
 c.box((268,0,563,39),'metalDark','ink')
 for yy,col in [(1,'shadow'),(5,'silver'),(11,'metalLight'),(17,'silver'),(28,'metalDark'),(35,'shadow')]:c.box((270,yy,563,yy+4),col)
 for x in [292,348,407,468,529]:
  c.box((x,0,x+4,39),'metalDark');c.line([(x+1,0),(x+1,37)],'metalLight')
 c.box((454,40,461,56),'shadow');c.box((456,42,459,52),'silver')
 # Heavy burgundy curtain at the podium side, enough folded structure for close-up.
 c.poly([(104,0),(309,0),(303,54),(287,87),(261,110),(228,121),(187,119),(149,101),(124,76)],'redDark','dark')
 for pts,col in [([(114,0),(136,0),(145,67),(163,96),(142,81),(125,54)],'red'),([(152,0),(171,0),(177,86),(202,113),(179,104),(163,78)],'red'),([(203,0),(219,0),(219,82),(229,114),(210,99)],'red'),([(252,0),(273,0),(260,79),(239,114),(249,68)],'red'),([(288,0),(302,0),(292,61),(266,96),(279,61)],'red')]:c.poly(pts,col)
 for pts in [[(125,2),(132,56),(150,85)],[(167,2),(172,68),(188,98)],[(213,2),(216,74),(223,100)],[(265,3),(255,67),(242,100)],[(296,3),(286,56),(272,81)]]:c.line(pts,'redLight',2)
 c.line([(124,76),(149,101),(187,119),(228,121),(261,110),(287,87),(303,54)],'gold',3)
 for x,y in [(132,85),(146,98),(160,108),(175,115),(190,122),(206,124),(222,124),(238,121),(254,115),(268,105),(281,92),(293,77)]:c.line([(x,y),(x,y+6)],'woodLight')
 c.box((102,0,113,277),'redDark');c.line([(108,0),(108,264)],'red',3)
 # Cropped doorway left confirms the ballroom connection, no whole-room floor.
 c.box((0,42,94,277),'woodDark');c.box((0,47,86,277),'wall')
 c.box((0,55,76,277),'redDark');c.line([(0,53),(79,53)],'cream',2)
 drape(c,0,65,16,150);drape(c,53,65,15,143)
 c.line([(16,70),(29,85),(43,87),(54,72)],'cream',2)
 c.box((18,175,51,178),'ink');c.poly([(22,174),(43,155),(48,157),(42,174)],'ink')
 c.line([(23,179),(23,195)],'dark',2);c.line([(47,179),(47,191)],'dark',2)
 c.poly([(73,57),(93,50),(93,277),(73,277)],'wood','woodDark')
 c.line([(78,63),(88,59),(88,267),(78,270),(78,63)],'woodLight')
 # Right lamp is native, sharply faceted, no blurred glow.
 c.box((494,116,505,152),'woodDark','shadow');c.box((497,151,502,158),'gold')
 c.poly([(480,80),(518,80),(513,129),(486,129)],'gold','woodDark')
 c.poly([(484,84),(514,84),(510,125),(489,125)],'light')
 c.poly([(484,84),(493,85),(494,124),(489,124)],'cream')
 c.line([(500,83),(501,125)],'cream',2)
 c.ellipse((480,76,518,84),'woodDark');c.ellipse((495,71,504,77),'gold')
 c.box((489,130,511,133),'woodDark')
 # Podium corner remains entirely left of the transparent character anchor.
 c.poly([(0,239),(117,219),(152,228),(1,255)],'woodLight','woodDark')
 c.poly([(0,254),(152,228),(152,243),(0,270)],'wood','woodDark')
 c.line([(1,250),(118,230),(147,233)],'gold')
 c.poly([(0,271),(147,245),(147,277),(0,277)],'woodDark')
 c.line([(4,274),(143,250)],'woodLight')
 c.save(OUT/'CH4-02-auctioneer-background-v01.png')

def restroom():
 c=Canvas(314,206)
 c.box((0,0,313,66),'wall')
 c.poly([(0,0),(134,62),(134,151),(0,196)],'cream')
 c.box((134,62,313,153),'cream')
 c.poly([(0,145),(134,125),(134,154),(0,197)],'tealLight')
 c.box((134,124,313,154),'tealLight')
 c.poly([(0,195),(134,151),(313,151),(313,205),(0,205)],'tile')
 # Subdued, clean tile grid rather than a carpet or reflected luxury finish.
 for yy in [156,164,177,194]:c.line([(0,yy+23),(134,yy),(313,yy)],'floor')
 for x in range(-700,1000,62):c.line([(197+(x-197)//7,151),(x,205)],'floor')
 for y in range(98,150,10):c.line([(134,y),(313,y)],'wall')
 for x in range(135,314,12):c.line([(x,78),(x,151)],'wall')
 for y in [91,104,118,134,151]:c.line([(0,y+12),(134,y)],'wall')
 for x in [15,38,61,84,107,130]:c.line([(x,93),(x,161-x//6)],'wall')
 c.line([(0,191),(134,150),(313,150)],'tealDark',3)
 # Patched ceiling panels: practical lift hatch is above nearest module.
 for x in [34,104,179,259]:
  c.line([(x-30,0),(x+25,60)],'shadow',3);c.line([(x-27,0),(x+28,60)],'cream')
 c.line([(130,62),(313,61)],'shadow',3);c.line([(133,64),(313,63)],'light')
 c.poly([(211,22),(305,19),(305,54),(230,59)],'shadow','ink')
 c.poly([(214,24),(302,22),(302,51),(232,56)],'plaster')
 c.line([(216,25),(301,23)],'light');c.line([(234,54),(300,50)],'wall')
 for x,y in [(219,26),(296,25),(236,51),(297,47)]:c.box((x,y,x+1,y+1),'metalLight')
 c.box((255,35,267,37),'metalDark','dark');c.line([(257,36),(265,36)],'silver')
 duct(c,90,40,157,53)
 c.poly([(76,0),(90,0),(90,31),(96,40),(102,42),(102,53),(89,48),(80,39),(76,31)],'metalDark','ink')
 c.poly([(79,0),(87,0),(87,31),(93,41),(100,44),(100,48),(89,44),(82,37),(79,30)],'silver')
 c.line([(80,1),(80,29),(84,37),(92,43)],'metalLight')
 pipe(c,[(67,0),(67,53),(75,57),(75,114)],4)
 pipe(c,[(18,0),(18,33),(12,39),(12,49)],3)
 # Red isolation cabinet. Exact long label remains in canonical source and Stage A.
 c.poly([(21,45),(57,52),(57,77),(21,70)],'redDark','dark')
 c.line([(23,47),(55,53)],'redLight')
 c.box((25,54,53,63),'redDark');label(c,26,56,'ISOLATE','cream')
 c.box((51,67,54,71),'gold');c.box((52,68,53,70),'ink')
 # A bare spindle, not a valve wheel; no premature repair-state illustration.
 c.box((79,70,92,86),'wall','shadow');c.line([(85,74),(85,83)],'metalDark',2)
 c.box((82,80,88,82),'redDark');c.box((84,73,86,76),'silver')
 # Native mirror: light reflected bands, no invented extra stalls/people.
 c.poly([(24,80),(110,91),(110,115),(24,105)],'woodDark','shadow')
 c.poly([(27,83),(107,93),(107,112),(27,103)],'silver')
 c.poly([(30,85),(78,92),(59,106),(30,102)],'metalLight')
 c.line([(28,103),(107,112)],'light');c.line([(28,83),(107,93)],'gold')
 c.poly([(21,110),(111,120),(111,123),(21,114)],'cream','shadow')
 for x,y in [(31,106),(77,111)]:
  for dy in [0,-3,-6]:
   c.box((x,y+dy,x+14,y+dy+2),'white');c.line([(x+1,y+dy+2),(x+13,y+dy+2)],'wall')
 # Three actual sinks and simple working taps, attached plumbing.
 for x,y,w in [(27,128,31),(61,132,26),(90,135,23)]:
  c.ellipse((x-1,y+6,x+w+1,y+15),'shadow')
  c.poly([(x,y),(x+w,y+2),(x+w-2,y+11),(x+4,y+10)],'cream','shadow')
  c.ellipse((x,y-3,x+w,y+5),'white','wall')
  c.ellipse((x+5,y-1,x+w-5,y+2),'metalLight','silver')
  c.line([(x+w//2,y-2),(x+w//2,y-7),(x+w//2+3,y-8),(x+w//2+4,y-6)],'metalDark',2)
  c.line([(x+w//2,y-6),(x+w//2+2,y-7)],'metalLight')
  c.box((x+5,y-4,x+7,y-2),'silver');c.box((x+w-7,y-3,x+w-5,y-1),'silver')
  pipe(c,[(x+w//2,y+11),(x+w//2,y+18),(x+w//2+5,y+21),(x+w//2+8,y+19),(x+w//2+8,y+11)],2)
 # Entire three-stall bank is modular, full-width ceiling access at right.
 c.box((141,147,306,153),'shadow','dark');c.box((142,146,305,149),'cream')
 c.line([(143,153),(306,153)],'light')
 for x,w in [(145,43),(193,43)]:
  c.box((x,78,x+w,141),'tealDark','ink')
  c.box((x+3,81,x+w-3,138),'teal');c.line([(x+4,82),(x+w-4,82)],'tealLight')
  c.box((x+w-7,114,x+w-4,119),'silver','metalDark')
  c.line([(x+w-7,118),(x+w-3,118)],'metalLight')
  for yy in [88,132]:c.box((x+1,yy,x+3,yy+4),'silver')
  c.box((x+3,141,x+w-3,145),'ink')
 # Near open stall interior: porcelain tank, seat, bowl, foot, drain and supply.
 c.box((241,78,302,146),'shadow')
 c.box((244,82,300,145),'cream')
 for yy in [89,101,113,125,137]:c.line([(244,yy),(300,yy)],'wall')
 for xx in [251,263,275,287,299]:c.line([(xx,82),(xx,144)],'wall')
 c.poly([(244,143),(299,140),(302,146),(241,146)],'tile')
 pipe(c,[(251,92),(251,133),(261,133)],2)
 c.box((265,106,288,122),'white','shadow');c.box((263,104,289,107),'white','wall')
 c.box((285,109,288,111),'silver');c.line([(266,108),(266,119)],'cream')
 c.poly([(270,131),(283,131),(281,140),(284,143),(269,143),(272,138)],'white','shadow')
 c.ellipse((264,122,289,134),'white','shadow')
 c.ellipse((266,122,287,128),'metalLight','wall');c.ellipse((270,123,284,126),'shadow')
 c.line([(268,129),(273,131),(283,131)],'cream')
 # Door swings toward camera right; it never covers the bowl.
 c.poly([(303,76),(313,68),(313,139),(303,146)],'tealDark','ink')
 c.line([(306,79),(311,75),(311,137)],'tealLight')
 c.box((308,107,310,112),'silver')
 for x in [141,190,238,302]:
  c.box((x,74,x+3,148),'metalDark','dark');c.line([(x+1,76),(x+1,147)],'silver')
  c.box((x-1,73,x+4,76),'metalLight','metalDark')
 c.box((141,76,304,79),'metalDark','dark');c.line([(143,77),(302,77)],'metalLight')
 # Tiny kneeling plumber and Eddie: body posture and clothes, no face details.
 c.ellipse((55,160,83,170),'shadow')
 c.poly([(62,148),(71,147),(76,153),(76,162),(82,165),(75,168),(65,162),(57,161)],'metalDark','dark')
 c.box((60,143,66,149),'skin');c.poly([(59,143),(61,140),(67,141),(68,144)],'tealDark')
 c.line([(62,151),(54,151),(50,146)],'metalDark',4);c.box((48,143,51,147),'skin')
 c.line([(70,154),(61,156),(55,150)],'metalDark',3);c.box((53,148,56,151),'skin')
 person(c,117,126,'teal','idle',hair='tealDark')
 c.box((114,139,117,146),'cream')
 c.box((41,163,53,171),'redDark','dark');c.line([(44,162),(44,159),(50,159),(50,162)],'dark')
 # Behind-entry maintenance access, closed but readable as a practical panel.
 c.poly([(7,143),(21,141),(21,168),(7,173)],'tealDark','dark')
 c.line([(9,146),(18,144),(18,166),(9,169),(9,146)],'tealLight');c.box((16,155,18,157),'silver')
 c.save(OUT/'CH4-04-restroom-v01.png')

def ballroom():
 c=Canvas(314,206)
 c.box((0,0,313,31),'plaster')
 c.poly([(0,0),(69,30),(69,141),(0,172)],'wall')
 c.box((70,31,313,141),'cream');c.box((70,118,313,141),'tealLight')
 c.poly([(0,172),(70,141),(314,141),(314,205),(0,205)],'floor')
 for yy in [144,152,164,180,201]:c.line([(0,yy+10),(70,yy),(313,yy)],'shadow')
 for x in range(-600,1000,80):c.line([(178+(x-178)//6,141),(x,205)],'shadow')
 c.poly([(155,141),(208,141),(258,205),(93,205)],'redDark')
 c.poly([(158,142),(205,142),(249,205),(102,205)],'red')
 c.line([(161,142),(110,205)],'gold');c.line([(202,142),(241,205)],'gold')
 for x,y in [(157,163),(171,180),(200,195),(185,152)]:c.line([(x,y),(x+8,y)],'redLight')
 for x in [69,140,213,286]:
  c.line([(x-24,0),(x+5,27)],'shadow',3);c.line([(x-20,0),(x+8,27)],'cream',2)
 c.line([(66,30),(313,27)],'shadow',3);c.line([(70,33),(313,30)],'light')
 # Left window upper portion.
 c.poly([(9,0),(58,22),(58,72),(9,57)],'metalDark','ink')
 c.poly([(12,2),(55,24),(55,68),(12,55)],'#aabeb3')
 for yy in [16,33,49]:c.line([(10,yy),(57,yy+16)],'shadow',2)
 for x in [25,42]:c.line([(x,8),(x,60+(x-9)//4)],'shadow',2)
 # Architectural repetitions shared with lobby, rearranged for the ballroom.
 for x in [91,145,198,262]:
  c.box((x,75,x+37,112),'wall','gold');c.line([(x+1,76),(x+36,76)],'light')
 for x,w in [(73,68),(143,60),(205,51),(259,54)]:
  c.poly([(x,34),(x+w,31),(x+w-5,41),(x+w-15,47),(x+17,44)],'redDark','shadow')
  c.line([(x+3,35),(x+17,42),(x+w-16,45),(x+w-6,38)],'redLight')
  c.line([(x+8,40),(x+19,46),(x+w-16,48),(x+w-8,43)],'gold')
 drape(c,73,41,11,74);drape(c,242,42,10,71)
 duct(c,90,51,241,69)
 c.poly([(74,13),(90,13),(90,43),(95,50),(102,52),(102,68),(88,64),(78,55),(74,43)],'metalDark','ink')
 c.poly([(77,14),(87,14),(87,43),(92,52),(100,56),(100,63),(88,59),(80,51),(78,42)],'silver')
 c.line([(79,15),(79,42),(82,49),(90,55)],'metalLight',2)
 for yy in [21,35]:c.line([(75,yy),(89,yy)],'shadow');c.line([(76,yy+1),(88,yy+1)],'metalLight')
 # Cheap wedding bunting deliberately in front of unsuitable ductwork.
 c.line([(11,74),(48,83),(84,80),(125,88),(169,80),(214,87),(254,79),(313,85)],'gold')
 for x,y in [(19,77),(32,80),(45,82),(59,82),(72,81),(90,82),(104,85),(118,87),(135,87),(148,84),(162,82),(176,82),(190,85),(205,87),(221,85),(237,82),(265,81),(280,83),(295,85)]:
  c.poly([(x,y),(x+7,y+1),(x+3,y+8)],'light' if x%2 else 'redLight')
 # Scarred panels and purposeful right service plumbing.
 for pts in [[(120,102),(124,99),(122,93),(129,88)],[(221,108),(218,101),(223,98)],[(294,114),(288,110),(289,105)]]:c.line(pts,'shadow')
 c.poly([(192,119),(201,116),(207,122),(204,131),(193,129)],'plaster')
 pipe(c,[(255,30),(255,121)],4)
 c.box((249,85,256,94),'metalDark','dark');c.line([(254,83),(244,79),(244,75),(313,75)],'dark')
 door(c,270,96,40,46,True)
 c.box((280,102,307,131),'tealDark')
 for yy,w in [(104,16),(111,12),(117,8)]:c.box((285,yy,285+w,yy+1),'light')
 # Stage with piano. Concert detail belongs to portraits, room people stay tiny.
 c.poly([(19,139),(88,130),(113,141),(37,156)],'woodDark','ink')
 c.poly([(19,138),(87,129),(113,138),(37,151)],'redDark')
 drape(c,25,93,7,40);drape(c,91,95,7,36)
 c.line([(33,92),(50,100),(72,100),(90,94)],'light')
 c.poly([(49,122),(71,104),(77,106),(70,124)],'ink','dark')
 c.line([(54,121),(72,108)],'shadow');c.box((45,125,81,130),'ink')
 c.box((45,124,69,126),'cream');c.line([(46,126),(70,126)],'metalDark')
 for x in range(48,68,3):c.line([(x,124),(x,125)],'ink')
 c.line([(49,130),(48,140)],'ink',2);c.line([(77,130),(79,137)],'ink',2)
 c.box((61,117,67,122),'light');c.line([(64,118),(64,121)],'shadow')
 person(c,39,109,'dark',hair='metalLight');person(c,85,106,'cream','show',hair='woodDark')
 # Folding ornamental screen: cheap printed leaves over the wall repair.
 for x,y in [(119,111),(131,109),(143,111)]:
  c.poly([(x,y),(x+10,y-1),(x+10,141),(x,140)],'wall','wood')
  c.line([(x+5,y+7),(x+4,135)],'green')
  for yy in [y+10,y+16,y+22]:c.poly([(x+5,yy),(x+1,yy-3),(x+2,yy)],'leaf')
 # Tablecloths use deliberate stepped folds, not texture noise.
 def table(x,y,w):
  c.ellipse((x-2,y+13,x+w+2,y+22),'shadow')
  c.poly([(x,y+3),(x+w,y+3),(x+w+3,y+21),(x-2,y+21)],'cream','shadow')
  for dx in range(4,w-2,7):c.poly([(x+dx,y+5),(x+dx+2,y+6),(x+dx+3,y+20),(x+dx,y+20)],'wall')
  c.ellipse((x-1,y-2,x+w+1,y+7),'light','wall')
  for dx in [7,w-9]:c.ellipse((x+dx-3,y,x+dx+3,y+3),'white','cream')
  c.line([(x+w//2,y-6),(x+w//2,y+1)],'green')
  c.ellipse((x+w//2-3,y-8,x+w//2+3,y-4),'cream');c.box((x+w//2-1,y-9,x+w//2+1,y-7),'white')
 def chair(x,y):
  c.ellipse((x,y,x+10,y+9),'red','woodDark');c.box((x,y+5,x+10,y+13),'red','woodDark')
  c.line([(x,y+13),(x-1,y+21)],'woodDark');c.line([(x+10,y+13),(x+12,y+21)],'woodDark')
  c.line([(x+2,y+2),(x+8,y+2)],'redLight')
 table(87,145,38);chair(84,144);chair(124,145)
 table(219,143,38);chair(215,142);chair(255,143)
 table(-12,171,66);chair(47,174)
 table(282,175,61);chair(275,171)
 # Organizer and workmen: clothing, posture and props carry their roles.
 person(c,180,123,'dark',hair='woodDark')
 c.box((177,134,182,143),'cream');c.line([(179,135),(181,135)],'woodLight')
 person(c,284,121,'metalDark',hair='tealDark');person(c,306,120,'metalDark',hair='tealDark')
 c.box((291,136,300,143),'redDark','woodDark');c.line([(292,143),(290,150)],'dark');c.line([(300,143),(301,148)],'dark')
 flowers(c,161,129);flowers(c,7,154)
 chandelier(c,123,1);chandelier(c,226,1)
 # Small clear direction clue; symbol, no invented readable prose.
 c.box((195,100,220,111),'tealDark','gold');c.ellipse((200,102,202,104),'cream')
 c.poly([(200,105),(202,105),(205,109),(198,109)],'cream')
 c.line([(208,106),(216,106)],'cream');c.poly([(216,103),(219,106),(216,109)],'cream')
 c.save(OUT/'CH4-05-ballroom-v01.png')

if __name__=='__main__':
 OUT.mkdir(exist_ok=True)
 lobby()
 portrait_background()
 restroom()
 ballroom()
