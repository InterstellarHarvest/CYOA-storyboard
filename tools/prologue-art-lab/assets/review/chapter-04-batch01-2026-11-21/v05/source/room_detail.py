"""Native material illustration: authored chips, seams, grain and folded forms.
No raster inputs, random scatter, high-resolution intermediates or pixel resampling.
"""
from materials import curve

def uv(p,u,v):
 a,b,c,d=p
 return (round((a[0]*(1-u)+b[0]*u)*(1-v)+(d[0]*(1-u)+c[0]*u)*v),round((a[1]*(1-u)+b[1]*u)*(1-v)+(d[1]*(1-u)+c[1]*u)*v))

def floor_tile(c,p,row,col):
 # Damage sits on chosen slab corners and follows individual slab planes.
 if (row,col) in [(1,4),(1,8),(2,3),(2,6),(3,4),(3,8),(4,3),(4,5),(4,9)]:
  c.poly([uv(p,.02,.03),uv(p,.21,.03),uv(p,.16,.14),uv(p,.09,.10),uv(p,.03,.21)],'#6b756a')
  c.line([uv(p,.20,.04),uv(p,.15,.14),uv(p,.08,.10)],'#bbc1aa')
 if (row,col) in [(2,5),(3,3),(3,7),(4,4),(4,8)]:
  c.line([uv(p,.28,.20),uv(p,.37,.32),uv(p,.33,.49),uv(p,.51,.68),uv(p,.55,.91)],'#788174')
  c.line([uv(p,.37,.34),uv(p,.49,.31),uv(p,.56,.39)],'#9ca592')
 if row>=2 and col in [4,7,9]:
  c.poly([uv(p,.25,.25),uv(p,.57,.20),uv(p,.74,.32),uv(p,.61,.42),uv(p,.35,.37)],'#a9ae9b')

def carpet_wear(c):
 c.surface('carpet')
 # One uneven walking track, interrupted nap and short scuffs, not repeated islands.
 c.contour([(182,155),(188,157),(185,162),(188,168),(184,176),(180,180),(179,187),(170,193),(167,200),(160,203),(161,198),(167,192),(168,187),(174,180),(175,173),(178,168),(177,162)],'#8d5a59')
 c.poly([(182,162),(184,164),(183,168),(180,170),(180,167)],'#99645e')
 c.poly([(176,178),(180,176),(181,180),(177,184),(175,183)],'#96615b')
 c.poly([(167,193),(173,190),(175,191),(172,194),(169,195)],'#95605a')
 c.line([(181,157),(184,158)],'#a16f64')
 c.line([(183,174),(185,172)],'#a37266')
 c.line([(172,189),(175,186)],'#a16d62')
 c.line([(164,199),(167,196)],'#9b685e')
 c.line([(179,168),(182,166)],'#774b50')
 # Uneven frayed edge, sewn repairs and interruptions in the border pattern.
 for x,y in [(140,180),(134,188),(124,198),(228,187),(237,200)]:
  c.line([(x,y),(x+3,y-1)],'#c19e78');c.box((x+1,y,x+2,y),'#80644e')
 c.line([(154,192),(160,190),(164,191)],'#bf9479')
 c.line([(156,191),(157,193)],'#d1ad88');c.line([(161,190),(162,192)],'#d1ad88')

def wall_wear(c):
 c.surface('wall')
 # Narrow moisture tracks begin at actual duct fixings and follow the old seam.
 c.poly([(123,78),(127,78),(129,84),(127,91),(128,99),(125,103),(122,98),(123,90)],'#b5a78a')
 c.poly([(212,78),(215,78),(217,85),(215,92),(216,98),(213,100),(211,94)],'#b7a88a')
 c.line([(125,83),(124,90),(125,95)],'#c4b18f')
 c.line([(214,82),(213,88),(214,93)],'#c5b292')
 # Cracks radiate from door-opening corners and the decorative-panel return.
 for pts in [[(149,89),(145,85),(144,81),(140,79)],[(226,89),(230,85),(230,80),(233,77)],[(283,86),(280,83),(281,79)]]:
  c.line(pts,'#8a846f')
 c.line([(145,85),(141,85),(139,83)],'#9c947b')
 c.line([(230,85),(234,84),(236,81)],'#9b9279')
 # Loss starts at lower-wall impact/damp edges; shapes follow the failed paint bond.
 for pts,col in [
  ([(92,135),(94,129),(94,122),(98,118),(101,120),(102,127),(106,131),(105,137),(100,140)],'#a59b80'),
  ([(95,132),(97,128),(97,123),(100,124),(100,130),(103,134),(101,137),(97,136)],'#b5a082'),
  ([(232,141),(234,136),(233,131),(236,126),(239,127),(240,133),(243,137),(241,142)],'#a69b80'),
  ([(235,138),(237,133),(237,130),(239,133),(240,139),(238,141)],'#b8a184'),
  ([(290,143),(290,138),(293,134),(294,130),(298,132),(298,138),(302,141),(301,144)],'#a99e82')]:c.poly(pts,col)
 c.line([(94,129),(94,122),(98,118),(101,120)],'#d2c09c')
 c.line([(234,135),(233,131),(236,126),(239,127)],'#d0bd99')
 c.line([(293,134),(294,130),(298,132)],'#d5c09b')
 # Chipped lower paint exposes the old cream coat beneath the teal repaint.
 for x,y in [(89,139),(103,142),(147,143),(188,140),(225,143),(258,137)]:
  c.poly([(x,y),(x+2,y-2),(x+5,y-1),(x+4,y+2),(x+1,y+3)],'#b4ac8e')
  c.line([(x+1,y),(x+3,y-1)],'#d2c5a2')

def duct_joints(c):
 c.surface('metal')
 # Connected overlaps, folded sheet edges and small screw heads follow collars.
 for x in [110,132,157,181,206,231]:
  c.line([(x-2,54),(x-2,68)],'#596e62')
  c.line([(x+3,55),(x+3,67)],'#b5c0a8')
  c.box((x,60,x+1,61),'#465b50');c.box((x,60,x,60),'#d0d5bc')
 for p,col in [([(116,64),(121,62),(125,63),(126,66),(122,68),(118,67)],'#83957f'),
  ([(166,59),(172,59),(175,61),(173,63),(168,62)],'#a3ad96'),
  ([(213,66),(218,64),(223,65),(224,68),(218,69)],'#5b7261')]:c.poly(p,col)
 c.line([(144,59),(151,60)],'#d2d8bf');c.line([(192,65),(198,64)],'#78917b')
 for x in [125,193,240]:
  c.box((x-1,73,x+4,75),'#55695b');c.box((x+1,74,x+2,74),'#d6d6b9')
  c.line([(x+3,76),(x+3,78)],'#364f42')
 # The service riser uses fastening straps and a real elbow into the junction box.
 c.line([(249,46),(255,46)],'#4d6555');c.box((250,45,251,46),'#d1d2b1')
 c.box((238,87,238,88),'#c6caac');c.box((245,95,245,96),'#b3bba0')

def wood_finish(c):
 c.surface('wood')
 # Long grain follows the podium's vertical face; dents sit at handled edges.
 for pts,col in [([(27,138),(28,144),(27,151),(28,155)],'#6e5036'),
  ([(31,137),(32,141),(31,145),(33,151)],'#b08b58'),
  ([(37,136),(36,142),(38,147),(37,152)],'#695038'),
  ([(42,135),(41,141),(43,146)],'#bd9560'),
  ([(10,127),(11,139),(10,150),(11,160)],'#92764b')]:c.line(pts,col)
 c.ellipse((33,143,36,147),'#755339');c.line([(34,143),(35,145),(34,147)],'#c39a60')
 for x,y in [(17,131),(28,129),(43,127),(53,153),(20,162)]:
  c.line([(x,y),(x+2,y-1)],'#d9b17b');c.box((x+1,y,x+2,y),'#5b4633')
 c.line([(13,122),(24,121),(29,122)],'#e5bd84');c.line([(32,120),(44,120)],'#88643d')

def flowers(c):
 c.surface('flower')
 # Rebuild petal silhouettes around visible centers, not identical star glyphs.
 for x,y in [(123,104),(131,109),(136,98),(142,111),(229,108),(236,102),(242,113),(246,119),(4,156),(11,164),(304,153),(311,161)]:
  c.poly([(x-3,y),(x-2,y-2),(x,y-1),(x+1,y-3),(x+2,y-1),(x+4,y),(x+1,y+1),(x,y+3),(x-1,y+1)],'#dcd4ad')
  c.box((x-1,y-1,x,y),'#f0e5be');c.box((x,y,x+1,y+1),'#a99258')
  c.line([(x+2,y),(x+3,y+2)],'#b8ad80')
 for x,y in [(126,118),(139,121),(231,124),(243,127),(7,178),(305,175)]:
  c.poly([(x,y),(x-5,y-5),(x-5,y-2),(x-2,y+1)],'#7e8e5d');c.line([(x-4,y-3),(x,y)],'#a1a56b')
 for x,y in [(134,132),(238,136),(4,186),(309,183)]:
  c.ellipse((x-6,y-2,x+7,y+2),'#b8b495','#5a6b55')
  c.ellipse((x-4,y-1,x+4,y+1),'#75866a')
  c.line([(x-2,y+2),(x-3,y+9),(x-1,y+13)],'#ded0a8')
  c.line([(x+3,y+3),(x+2,y+10)],'#65775e')
  c.box((x+1,y+7,x+2,y+8),'#b0a68a')

def cloth_swag(c,x,y,w):
 c.surface('drape')
 depth={83:15,141:19,192:13,262:17}[x]
 p=[(x,y),(x+w//4,y+1),(x+w-2,y-2),(x+w-3,y+5),(x+w-11,y+depth-2),(x+w//2,y+depth),(x+11,y+depth-4),(x+3,y+6)]
 c.contour(p,'#723643','#492d35')
 # Asymmetric broad crests, compressed folds and troughs model heavy fabric.
 c.contour([(x+3,y+1),(x+9,y+1),(x+14,y+6),(x+20,y+depth-4),(x+16,y+depth-3),(x+8,y+8)],'#9a4e54')
 c.contour([(x+13,y+3),(x+21,y+6),(x+w//2,y+depth-2),(x+w//2-4,y+depth),(x+20,y+9)],'#512d3a')
 c.contour([(x+w//2-2,y+3),(x+w//2+4,y+3),(x+w//2+3,y+depth-4),(x+w//2-1,y+depth-2)],'#a55759')
 c.contour([(x+w-12,y+1),(x+w-5,y),(x+w-10,y+depth-6),(x+w-16,y+depth-1),(x+w-18,y+depth-3)],'#b56b63')
 c.line(curve([(x+5,y+4),(x+15,y+depth-5),(x+w//2,y+depth),(x+w-10,y+depth-2),(x+w-3,y+5)]),'#a88b5d')
 for k in range(10,w-6,4):
  t=k/w;yy=y+round(depth*(.55+.45*__import__('math').sin(t*3.14159)))
  c.line([(x+k,yy),(x+k,yy+1+(k%3))],'#b59967')
 # A short loose seam at a loaded fold is distinct from decorative fringe.
 c.line([(x+9,y+5),(x+12,y+8),(x+13,y+10)],'#c28270')
