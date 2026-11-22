"""v05 independent close-camera reconstruction: native 564x278 opaque."""
from pathlib import Path
from materials import Canvas,curve

def portrait_background(out):
 c=Canvas(564,278,mode='close')
 c.surface('wall')
 c.box((0,0,563,277),'#d6cbb0');c.box((0,235,563,277),'#809187')
 from wall_light import plaster_variation
 plaster_variation(c)
 # Deep panel recesses: plaster, thin cheap trim, localized repairs.
 for x,w in [(331,111),(457,107)]:
  c.box((x+2,58,x+w+3,230),'#827c67')
  c.box((x,55,x+w,226),'#b7aa8d')
  c.line([(x+1,225),(x+1,56),(x+w-1,56)],'#efe0ba',2)
  c.box((x+5,60,x+w-5,221),'#d5c7a7')
  c.line([(x+5,220),(x+5,60),(x+w-5,60)],'#aa9e83',2)
  c.line([(x+8,217),(x+w-8,217),(x+w-8,63)],'#e6d4b0')
 c.box((446,47,453,277),'#b6ab90');c.line([(447,51),(447,234)],'#e5d5b0');c.line([(452,50),(452,234)],'#958c72')
 c.box((447,170,452,173),'#a89b80')
 # Restricted correction: continuous weak practical-light falloff within the panel.
 from wall_light import illuminate_panel, plaster_variation
 illuminate_panel(c)
 c.surface('wall')
 # Cast shadow behind the raised cylinder, independent of the cylinder paint.
 c.contour([(267,39),(563,39),(563,52),(284,54)],'#8c8068')
 c.surface('metal',(17,26));c.box((268,0,563,39),'#c3c7bb','#4a5c52')
 for x in [292,348,407,468,529]:
  c.box((x,0,x+4,39),'#92a697');c.line([(x+1,0),(x+1,38)],'#e4e2cb')
  c.box((x-1,23,x,25),'#566a59')
 for x in [334,442,552]:
  c.surface('wall');c.box((x+2,43,x+8,57),'#8d8067')
  c.surface('metal',(17,26));c.box((x,39,x+5,51),'#a3ac94','#637462');c.box((x+2,48,x+3,49),'#d5d1b0')
 # Heavy velvet has volume across each hanging fold; the hem remains uneven.
 c.surface('drape')
 c.contour([(104,0),(309,0),(306,32),(300,61),(286,88),(263,110),(230,122),(190,121),(151,102),(126,78),(114,47)],'#a64c58','#482a34')
 c.contour([(111,0),(126,0),(130,50),(144,79),(163,98),(152,100),(133,81),(120,54)],'#9b424f')
 c.contour([(155,0),(171,0),(177,66),(189,94),(207,113),(194,115),(178,98),(165,68)],'#a44a55')
 c.contour([(207,0),(221,0),(218,64),(226,99),(233,116),(222,119),(214,96)],'#b35b61')
 c.contour([(263,0),(278,0),(270,53),(255,88),(240,111),(231,118),(241,93),(256,53)],'#a14955')
 c.contour([(293,0),(304,0),(296,53),(283,80),(265,101),(269,88),(287,50)],'#ae5760')
 # An uneven heavy folded edge, with broken fringe lengths following gravity.
 c.line(curve([(125,76),(150,100),(188,120),(230,124),(263,111),(286,89),(302,59)]),'#c9a574',3)
 for i,(x,y) in enumerate([(132,85),(138,91),(145,97),(152,103),(160,108),(168,113),(177,117),(186,121),(195,124),(205,126),(215,127),(225,127),(236,125),(246,121),(255,116),(264,111),(273,104),(282,95),(289,86),(296,73)]):
  c.surface('wood');c.line([(x,y),(x,y+4+(i*3)%5)],'#c5a06b');c.line([(x+1,y+1),(x+1,y+5+(i*2)%4)],'#8f714e')
 c.surface('drape');c.box((103,0,113,277),'#813b49')
 # Ballroom recess at far left is a much darker secondary plane.
 c.surface('wood');c.box((0,42,94,277),'#73533c')
 c.surface('wall');c.box((0,47,86,277),'#baa88c')
 c.surface('corridor');c.box((0,55,76,277),'#715458')
 c.surface('drape');c.contour([(0,65),(15,65),(14,122),(10,178),(15,215),(0,220)],'#a4545a')
 c.contour([(53,65),(68,65),(66,159),(62,205),(53,209)],'#9c4b55')
 c.surface('wall');c.line(curve([(16,70),(29,85),(43,87),(54,72)]),'#e4cb9f',2)
 c.surface('corridor');c.poly([(22,174),(43,155),(48,157),(42,174)],'#242e31');c.box((18,175,51,178),'#263033')
 c.line([(23,179),(23,195)],'#303a35',2);c.line([(47,179),(47,191)],'#303a35',2)
 c.surface('wood');c.poly([(73,57),(93,50),(93,277),(73,277)],'#9c7350','#4c4237')
 for y1,y2 in [(63,161),(167,221)]:
  c.poly([(78,y1),(87,y1-3),(87,y2),(78,y2+2)],'#6c5139','#b49061')
  c.line([(80,y1+3),(85,y1+1),(85,y2-2)],'#9f794d')
 c.surface('metal',(140,140));c.ellipse((78,181,84,188),'#c1ad7f','#756849')
 # Plaster loss is layered: lit flaking edge over a darker granular substrate.
 c.surface('wall')
 c.contour([(346,187),(351,177),(357,180),(365,169),(369,178),(376,175),(383,181),(387,180),(385,194),(377,201),(366,197),(358,207),(348,201)],'#a4977f')
 c.contour([(351,187),(359,184),(363,178),(369,183),(376,180),(382,186),(379,193),(372,195),(366,192),(359,200),(353,197)],'#b29a80')
 c.line([(347,185),(352,176),(358,179),(365,168),(369,176),(376,173)],'#eddbb5')
 c.line([(349,201),(357,207),(366,199)],'#82775f')
 c.line([(406,80),(400,88),(402,98),(394,107),(397,119),(390,126)],'#8b806c')
 c.line([(402,88),(398,86),(396,80)],'#aa9a7e');c.line([(393,108),(389,112),(391,116)],'#a38f73')
 for pts in [[(467,242),(474,236),(486,240),(490,254),(481,260),(471,257)],[(534,264),(542,256),(551,258),(557,271),(547,277),(534,275)]]:
  c.poly(pts,'#a7a18a');c.line(pts[:3],'#d7c7a4')
 # Warm practical lamp: cast housing shadow, dark metal and luminous glass.
 c.surface('wall');c.contour([(504,82),(525,90),(521,139),(508,163),(500,160),(509,131)],'#a48c69')
 c.surface('wood');c.box((495,116,505,152),'#775f3e','#594e37')
 c.poly([(480,80),(518,80),(513,129),(486,129)],'#a88a54','#625035')
 c.surface('emissive');c.poly([(484,84),(514,84),(510,125),(489,125)],'#f1d197')
 c.poly([(493,84),(505,84),(504,125),(494,125)],'#fce9b7')
 c.surface('wood');c.line([(492,84),(494,125)],'#ac945e');c.line([(506,84),(505,125)],'#ad945f')
 c.ellipse((480,76,518,84),'#786446');c.line([(482,79),(516,79)],'#d3ad70')
 c.ellipse((495,71,504,77),'#b7985f');c.box((489,130,511,133),'#7c643f');c.box((493,134,507,136),'#ac8c55')
 c.line([(498,137),(498,151)],'#c2a263');c.box((496,153,504,155),'#9b7d4e')
 # Podium corner: wood grain belongs to broad light planes, with worn top edge.
 c.surface('wood')
 c.poly([(0,239),(117,219),(152,228),(1,255)],'#b78e5e','#5c4935')
 c.poly([(0,254),(152,228),(152,243),(0,270)],'#8e6947','#4b4031')
 c.line([(1,245),(117,224),(148,230)],'#e4bc81')
 c.line([(2,249),(117,229),(148,234)],'#6d5137')
 c.poly([(0,271),(147,245),(147,277),(0,277)],'#674f38')
 c.line([(4,274),(143,250)],'#c1945e')
 for pts,col in [([(10,247),(26,244),(34,244)],'#e0b17b'),([(44,240),(58,238),(65,238)],'#6f4f33'),([(78,234),(94,231)],'#d8a875')]:c.line(pts,col)
 from close_detail import illustrate
 illustrate(c)
 c.save(out)

if __name__=='__main__':portrait_background(Path(__file__).resolve().parent.parent/'native/CH4-02-auctioneer-background-v05.png')
