"""CH4-05 v02: independent native environment construction, no source rasters.

Fresh room footprint, parquet, stage, music/organizer/service-access hierarchy.
Small people stay simple. Material detail is native geometry, not noise.
"""
from pathlib import Path
from scene_tools import Canvas,floor,duct,pipe,sconce,flowers,drape

ROOT=Path(__file__).resolve().parent.parent

def main():
 c=Canvas();vp=(192,85)
 c.poly([(0,0),(314,0),(304,32),(104,32)],'#8a8c7b')
 c.poly([(0,0),(104,32),(104,126),(0,174)],'#c8bba0')
 c.box((104,32,313,132),'#c4b393')
 c.poly([(104,33),(159,33),(159,130),(104,130)],'#c4b392')
 c.poly([(160,33),(229,33),(229,131),(160,131)],'#cebc97')
 c.poly([(230,33),(314,33),(314,131),(230,131)],'#b3aa8d')
 floor(c,vp,(0,174),(104,126),(314,126),wood=True)
 # Purposeful local window reflections and warm lamp glints follow floor planes.
 for pts,col in [([(30,167),(43,163),(60,165),(48,170)],'#a5a397'),([(46,178),(58,173),(80,175),(66,181)],'#9d9c91'),([(67,161),(78,158),(94,160),(82,164)],'#b4b1a1'),([(81,188),(93,181),(109,184),(97,192)],'#92968b'),([(139,148),(146,147),(149,153),(141,154)],'#ba986b'),([(156,159),(163,157),(170,172),(161,175)],'#c7a773'),([(175,182),(183,180),(193,200),(181,204)],'#b59062')]:c.poly(pts,col)
 for pts in [[(66,186),(73,184),(79,185)],[(121,166),(131,164)],[(222,191),(229,189),(234,191)],[(193,143),(201,142)]]:c.line(pts,'#685a46')
 for pts in [[(83,192),(90,189)],[(151,175),(158,174)],[(211,155),(216,155)]]:c.line(pts,'#c7a578')
 # Longitudinal ceiling coffers converge to the room vanishing point.
 for x in [-120,-40,39,117,195,273,351,429]:
  xb=round(192+(x-192)*(85-32)/85)
  c.poly([(x-3,0),(x+4,0),(xb+3,32),(xb-2,32)],'#a6a68e')
  c.line([(x+4,0),(xb+3,32)],'#596e5d');c.line([(x-3,0),(xb-2,32)],'#c9c2a1')
 for yy in [11,23,31]:
  c.line([(0,yy),(104,round(85+(yy-85)*(192-104)/192)),(314,round(85+(yy-85)*(192-104)/192))],'#667c69')
 c.line([(102,32),(313,32)],'#4f6756',3);c.line([(104,35),(313,35)],'#d1bd91')
 c.line([(105,37),(313,37)],'#e2cda1')
 # Tall left glazing. Horizontal mullions converge to VP(192,85).
 def wy(x,near):return round(85+(near-85)*(192-x)/(192-5))
 window=[(4,0),(44,wy(44,0)),(44,wy(44,108)),(4,108)]
 c.poly(window,'#304f4b','#536b5d')
 c.poly([(7,0),(41,wy(41,0)),(41,wy(41,105)),(7,105)],'#9cb6b3')
 for x in [9,25,39]:
  c.poly([(x,wy(x,9)),(x+5,wy(x+5,9)),(x+5,wy(x+5,102)),(x,wy(x,102))],'#b8ccbf')
 for pts,col in [([(8,30),(23,42),(40,49),(40,59),(25,50),(8,38)],'#7c9d9c'),([(7,73),(21,68),(40,70),(40,79),(22,77),(7,82)],'#8ba9a3')]:c.poly(pts,col)
 # Quiet exterior masonry/building shapes rather than Chapter 2 vegetation.
 c.poly([(9,55),(16,56),(16,101),(9,103)],'#819e92');c.poly([(29,64),(40,67),(40,102),(29,103)],'#78958a')
 for yy in [13,29,47,65,83]:
  c.line([(5,yy),(43,wy(43,yy))],'#3d5a52',3);c.line([(5,yy-1),(43,wy(43,yy-1))],'#cfceae')
 for x in [17,31]:
  c.line([(x,wy(x,0)),(x,wy(x,106))],'#3e5a51',3);c.line([(x-1,wy(x,0)),(x-1,wy(x,106))],'#aebba4')
 c.line([(4,110),(45,wy(45,110))],'#cdbd95',3);c.line([(5,113),(46,wy(46,113))],'#6c7c65')
 # Left wall and rear wainscot: layered molding, worn edges, repaired corners.
 c.poly([(0,116),(104,112),(104,126),(0,174)],'#55786c')
 c.line([(0,116),(104,112)],'#ddc89a',2);c.line([(0,119),(104,115)],'#87987c')
 for pts in [[(4,126),(31,124),(31,153),(4,163)],[(36,123),(66,121),(66,140),(36,151)],[(71,120),(99,117),(99,128),(71,139)]]:
  c.poly(pts,'#4f7265','#3d5d50');c.line([pts[0],pts[1],pts[2]],'#98a184')
 c.box((104,108,313,132),'#55776a');c.line([(104,108),(313,108)],'#d2be8e',2);c.line([(105,111),(313,111)],'#879b7c')
 for x,w in [(108,29),(142,29),(176,28),(209,25),(299,13)]:
  c.box((x,115,x+w,129),'#4b6d60','#8c9879');c.line([(x+1,128),(x+w-1,128)],'#365a4a')
 for x in [114,160,206,300]:
  c.box((x,67,x+1,104),'#a89471');c.line([(x+2,66),(x+2,104)],'#dfc9a0')
 c.line([(106,66),(313,66)],'#8c8367');c.line([(107,68),(313,68)],'#e0c89d')
 for pts,col in [([(120,100),(124,96),(128,96),(130,102),(126,105),(121,104)],'#a2aa91'),([(192,98),(197,91),(198,96),(203,99),(200,104),(193,103)],'#929f86'),([(306,76),(310,72),(313,77),(311,85),(307,83)],'#a99d7b'),([(150,128),(151,123),(154,121),(158,124),(157,129)],'#b4a486')]:c.poly(pts,col)
 for pts in [[(267,51),(270,56),(269,60),(274,65)],[(122,41),(121,47),(124,52)],[(233,80),(231,85),(234,90)]]:c.line(pts,'#8f886c')
 c.line([(270,56),(274,55),(276,57)],'#aa9c7b')
 # Heavy faded swags and irregular fringe, rather than repeated scallops.
 for x,w,drop in [(49,47,21),(98,53,18),(154,56,20),(214,51,17),(269,48,22)]:
  c.poly([(x,20),(x+w,20),(x+w-4,20+drop*.5),(x+w-11,20+drop),(x+w*.49,23+drop),(x+9,20+drop*.7)],'#5b3840','#443f3c')
  c.poly([(x+3,21),(x+w-3,21),(x+w-10,27),(x+w*.56,27+drop*.5),(x+14,24+drop*.5)],'#8c4b52')
  c.poly([(x+7,22),(x+13,22),(x+21,29),(x+w*.6,32),(x+w-10,24),(x+w-4,22),(x+w-11,33),(x+w*.52,37),(x+15,31)],'#a05a5d')
  c.line([(x+6,27),(x+14,34),(x+w*.5,38),(x+w-11,32),(x+w-5,26)],'#bc976b')
  for xx,yy in [(x+12,34),(x+23,38),(x+w-12,34)]:c.line([(xx,yy),(xx,yy+2)],'#ac9165')
 drape(c,49,36,11,68);drape(c,302,39,12,38)
 # Intrusive metal riser/elbow and banded cylinder hide parts of the cheap grandeur.
 c.box((48,0,66,22),'#465f50');c.box((50,0,64,21),'#8d9f88')
 c.line([(52,0),(52,21)],'#c8cdb0',3);c.line([(63,0),(63,21)],'#617b65',2)
 for yy in [6,18]:c.line([(49,yy),(65,yy)],'#c4c8a5');c.line([(49,yy+2),(65,yy+2)],'#526d56')
 c.poly([(49,20),(65,18),(68,27),(75,34),(85,36),(85,52),(73,48),(61,39),(53,30)],'#7d9277','#3d5b47')
 c.poly([(51,21),(60,21),(65,29),(73,36),(82,38),(81,42),(72,40),(61,33),(55,27)],'#bac1a0')
 c.line([(53,24),(59,32),(69,40),(82,46)],'#d0d0ac')
 duct(c,82,38,174,15)
 c.poly([(255,38),(261,37),(266,32),(267,26),(279,26),(278,36),(272,44),(263,51),(255,52)],'#71896e','#3f5e47')
 c.poly([(257,39),(263,37),(270,29),(276,29),(273,37),(266,44),(256,47)],'#c0c5a3')
 c.box((266,18,280,28),'#6d856c','#3d5c45');c.line([(268,19),(268,27)],'#c6c9a5',2)
 for x in [87,128,171,218,255]:
  c.line([(x,11),(x,55)],'#3f5743',2);c.line([(x+2,13),(x+2,54)],'#b7bc99')
  c.box((x-2,38,x+3,54),'#4d674d');c.line([(x+1,39),(x+1,52)],'#9aaa88');c.box((x,53,x+1,54),'#d0c99d')
 # Ordinary cable trunking, joints and one wired service box.
 pipe(c,[(291,6),(291,67),(305,67),(305,103)],2)
 c.box((289,60,295,66),'#647d60','#3f5b44');c.line([(290,61),(294,61)],'#a4b18a')
 # Cheap bunting sits in front of equipment, not a new architectural feature.
 garland=[(52,62),(78,72),(105,65),(133,72),(160,65),(188,72),(215,65),(241,72),(271,64),(311,72)]
 c.line(garland,'#e5d4ae',2);c.line([(x,y+2) for x,y in garland],'#a89470')
 for x,y in [(52,62),(105,65),(160,65),(215,65),(271,64),(311,72)]:
  c.poly([(x-3,y-2),(x,y),(x+3,y-2),(x+3,y+2),(x,y+1),(x-3,y+2)],'#f0dfba')
  c.line([(x,y+2),(x-1,y+10)],'#ddd0ab',2);c.line([(x+1,y+2),(x+3,y+8)],'#b38f78')
 # Chandelier has an intelligible suspension and coherent warm local key.
 c.line([(173,0),(173,17)],'#5c583d',2)
 for yy in [3,8,13]:c.ellipse((171,yy,174,yy+3),'#bf9c62','#6b6544')
 c.line([(160,31),(162,36),(173,39),(185,35),(187,29)],'#af9259',2)
 c.line([(162,34),(173,37),(184,33)],'#e0bc7b')
 for x,y in [(159,24),(167,20),(176,22),(184,24)]:
  c.box((x,y,x+5,y+8),'#eed29a','#a58a52');c.box((x+1,y+1,x+4,y+6),'#ffedbf')
  c.line([(x+2,y+9),(x+2,y+12)],'#b9985f')
 c.ellipse((171,38,176,41),'#b79b63','#5c6043')
 # Natural wall lamp illumination is painted into irregular nearby planes.
 for pts,col in [([(145,76),(157,74),(165,82),(165,100),(157,104),(146,99)],'#d6bc90'),([(205,79),(216,75),(227,81),(227,101),(215,105),(204,97)],'#cdb58a')]:c.poly(pts,col)
 sconce(c,153,84,True);sconce(c,216,84,True)
 # Service doorway is a dimensional opening into a darker working passage.
 c.box((240,74,300,134),'#3a5346');c.box((243,77,298,132),'#839177')
 c.box((245,79,296,130),'#394e40');c.poly([(245,79),(257,86),(286,86),(296,79)],'#52644e')
 c.poly([(257,86),(286,86),(286,122),(257,122)],'#8c8966')
 c.poly([(245,130),(257,122),(286,122),(296,130)],'#908566')
 for yy in [125,129]:c.line([(247,yy),(294,yy)],'#6e7155')
 c.line([(254,129),(267,122)],'#626c50');c.line([(284,129),(278,122)],'#5e6b50')
 c.poly([(243,79),(252,84),(252,129),(243,134)],'#566e54','#2f4d39')
 c.line([(245,82),(250,85),(250,127)],'#a8aa82')
 c.poly([(297,79),(305,75),(305,130),(297,133)],'#526c50','#304c36')
 c.line([(299,82),(303,79),(303,126)],'#acb087')
 c.box((240,73,300,76),'#8c9a78','#3e5d43');c.line([(240,73),(300,73)],'#c6bc91')
 c.line([(274,84),(274,88)],'#3b4e36');c.poly([(270,90),(272,88),(277,88),(280,90)],'#556340');c.line([(271,91),(279,91)],'#ecd29c')
 c.box((282,99,288,118),'#616d4e');c.line([(283,101),(287,101)],'#b5a97a');c.box((284,104,287,110),'#9c8d64')
 # Discreet restroom-direction pictogram. No working bridal lavatory is shown.
 c.box((217,67,235,78),'#9a885d','#566447');c.box((219,69,233,76),'#405e4a')
 c.ellipse((221,69,223,71),'#e3cda1');c.poly([(221,72),(223,72),(224,75),(220,75)],'#e3cda1')
 c.line([(226,72),(232,72),(230,70)],'#e3cda1');c.line([(232,72),(230,74)],'#e3cda1')
 # Raised stage with depth, weighted velvet valance and practical steps.
 c.poly([(48,116),(122,116),(133,129),(57,138)],'#5d4f3e','#354d3c')
 c.poly([(49,115),(121,115),(131,125),(57,133)],'#947a59')
 c.line([(51,116),(120,116),(129,124),(57,131)],'#d1aa74')
 c.poly([(58,133),(131,125),(131,136),(58,145)],'#683a42','#4c3e39')
 for x in range(62,131,7):
  y=round(133-(x-58)*8/73)
  c.poly([(x,y),(x+2,y),(x+2,y+9),(x,y+10)],'#95515a');c.line([(x+3,y),(x+3,y+10)],'#4c333d')
 c.line([(60,144),(130,135)],'#b38e5d')
 for x,y,w in [(61,137,20),(58,142,20),(54,148,20)]:
  c.poly([(x,y),(x+w,y-2),(x+w+2,y+2),(x+1,y+5)],'#9c825f','#514f3b');c.line([(x+1,y),(x+w,y-2)],'#d0b084')
 # Grand piano: tilted lid, dark wood thickness, keyboard, pedals and legs.
 c.poly([(78,103),(95,78),(107,80),(101,89),(113,91),(113,111),(80,114)],'#3f3c35','#2c3831')
 c.poly([(79,103),(95,79),(105,81),(99,89),(110,91),(110,107)],'#242e2a')
 c.line([(80,101),(96,80),(104,81)],'#c09a63');c.line([(91,94),(91,108)],'#9d7c4e')
 c.poly([(77,110),(111,106),(111,112),(78,117)],'#76583e','#2e3d31')
 c.line([(79,111),(110,108)],'#c6a16a');c.box((78,112,102,115),'#e1d4ad')
 c.line([(83,109),(95,108),(106,108)],'#a18459')
 c.line([(102,95),(109,96)],'#4c4936');c.line([(101,99),(109,100)],'#55503a')
 for x in [80,83,87,90,94,98,101]:c.line([(x,112),(x,114)],'#333d31')
 c.poly([(79,116),(82,116),(81,129),(78,130)],'#293b2f');c.poly([(108,113),(111,112),(113,124),(110,125)],'#2b3b2e')
 c.line([(80,117),(80,127)],'#8f7952');c.line([(110,114),(112,123)],'#7a6c4b')
 c.poly([(92,109),(93,101),(100,101),(99,108)],'#daceac','#806e4e');c.line([(96,102),(96,107)],'#927b56')
 c.line([(94,119),(94,124),(98,124)],'#95855a')
 flowers(c,54,113,.7);flowers(c,135,111,.8)
 # Musicians, organizer and the chair-carrying group are illustrated separately
 # from approved NPC style references and composited by scene_people.py.
 # Round side tables: curved cloth silhouettes, varied folds, plates, glass and lamp.
 def chair(x,y,w=12,h=23):
  c.line([(x+1,y+10),(x-1,y+h)],'#544d35',2);c.line([(x+w-1,y+10),(x+w+2,y+h)],'#544d35',2)
  c.ellipse((x,y,x+w,y+12),'#8a4c4d','#b29460')
  c.ellipse((x+2,y+2,x+w-2,y+9),'#a5625d','#663e40')
  c.poly([(x,y+8),(x+w,y+8),(x+w+2,y+15),(x-1,y+15)],'#6c3f43','#ac8b59')
  c.line([(x+1,y+9),(x+w-1,y+9)],'#bb8270')
 def table(x,y,w,h):
  c.ellipse((x-3,y+h-5,x+w+3,y+h+3),'#6b5b47')
  c.poly([(x,y+3),(x+w,y+3),(x+w+3,y+h),(x+w-3,y+h-2),(x+w*.78,y+h+2),(x+w*.58,y+h-1),(x+w*.39,y+h+1),(x+w*.18,y+h-1),(x-2,y+h+2)],'#cfc6a5','#8d8b6d')
  for pts,col in [([(x+3,y+5),(x+8,y+5),(x+7,y+h-1),(x+3,y+h)],'#ece0ba'),([(x+w*.25,y+6),(x+w*.34,y+7),(x+w*.31,y+h),(x+w*.26,y+h-1)],'#abae8c'),([(x+w*.46,y+7),(x+w*.52,y+7),(x+w*.55,y+h),(x+w*.47,y+h)],'#e6d8b0'),([(x+w*.7,y+6),(x+w*.78,y+5),(x+w*.82,y+h),(x+w*.72,y+h-2)],'#aaa989'),([(x+w-5,y+5),(x+w-2,y+4),(x+w+1,y+h),(x+w-4,y+h-1)],'#eee0b7')]:c.poly(pts,col)
  c.ellipse((x-1,y-4,x+w+1,y+9),'#e8d9b0','#b7af8b');c.line([(x+6,y+6),(x+w-6,y+6)],'#f1dfb6')
  for xx,yy in [(x+w*.24,y+2),(x+w*.79,y+2)]:
   c.ellipse((xx-4,yy-1,xx+4,yy+2),'#c1c1a0','#f5e5bb');c.line([(xx-2,yy),(xx+2,yy)],'#f0e4c0')
  lampx=round(x+w*.6);c.box((lampx-2,y-9,lampx+2,y-3),'#f6d89c','#aa8d56');c.line([(lampx,y-2),(lampx,y+2)],'#9f8653');c.ellipse((lampx-3,y+2,lampx+3,y+3),'#9f8958')
  for xx in [round(x+w*.38),round(x+w*.87)]:
   c.line([(xx,y),(xx,y-6)],'#dfdac0');c.box((xx-1,y-7,xx+1,y-3),'#c3cbb9');c.line([(xx-1,y-7),(xx+1,y-7)],'#f0ead0')
  flowers(c,round(x+w*.43),y-2,.65 if w<50 else 1)
 # Rear tables first, foreground framing second. Keep the center navigable.
 chair(13,127,12,25);chair(48,132,12,24);table(12,141,43,24);chair(9,148,12,25)
 chair(284,130,12,24);table(280,145,42,25);chair(273,151,12,25)
 chair(7,170,17,32);chair(56,170,17,32);table(-17,187,81,37);chair(63,188,16,31)
 chair(290,177,17,32);chair(268,188,15,30);table(285,195,67,32)
 c.save(ROOT/'backgrounds/CH4-05-ballroom-background-v02.png')

if __name__=='__main__':main()
