"""Independent final-grid raster construction from a blank564x278 canvas.

Design references are not loaded, sampled, traced, resized or palette-reduced.
Every material shade is a deliberate constant-colour shape; curves describe
cloth and metal geometry, not mathematical shading gradients. All illustration
layers are authored directly on the final pixel grid, with binary alpha.
The visual design remains SOURCE-DERIVED from approved art/generated reference.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,math,hashlib
ROOT=Path(__file__).resolve().parents[1];SIZE=(564,278)
FONT=json.loads((ROOT/'source/bitmap-glyphs.json').read_text());TEXT=[];RECIPES={};VIEW_SCALE=1
MICRO={k:v.split('/')for k,v in {'A':'010/101/111/101/101','U':'101/101/101/101/111','T':'111/010/010/010/010','O':'111/101/101/101/111','F':'111/100/110/100/100','I':'111/010/010/010/111','B':'110/101/110/101/110','R':'110/101/110/101/101','D':'110/101/101/101/110','L':'100/100/100/100/111','S':'111/100/111/001/111','Y':'101/101/010/010/010','E':'111/100/110/100/111','M':'101/111/111/101/101'}.items()}
P={
 'plaster':['#645846','#85745c','#a28d70','#bda584','#d4bc97','#e5ceaa'],
 'green':['#1e302b','#2c4238','#40564a','#5e705f','#899681','#b5bba1'],
 'velvet':['#35262c','#4c2b35','#693540','#85434e','#a45b63','#c58883'],
 'brass':['#493e29','#715535','#9f7842','#c19b59','#dfbd7a','#f2dca6'],
 'steel':['#24332f','#435249','#6e7d6c','#a4ad95','#d4d7be','#f0eed7'],
 'cloth':['#666d61','#858775','#a39f87','#beb59b','#d3c9ae','#e7ddc4','#f5edd8'],
 'wood':['#302e25','#5d4831','#8b6946','#b5905c','#d4b47e'],
 'glass':['#446266','#678a8a','#96bab6','#c3d9cd'],
}
def c(k,n):return P[k][n]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def grid(v):return round(v*VIEW_SCALE)/VIEW_SCALE
def curve(points,steps=8):
 pts=[points[0]]+list(points)+[points[-1]];out=[];steps*=VIEW_SCALE
 for k in range(1,len(pts)-2):
  a,b,q,e=pts[k-1:k+3]
  for i in range(steps):
   t=i/steps
   out.append(tuple(grid(.5*((2*b[j])+(-a[j]+q[j])*t+(2*a[j]-5*b[j]+4*q[j]-e[j])*t*t+(-a[j]+3*b[j]-3*q[j]+e[j])*t*t*t))for j in[0,1]))
 out.append(points[-1]);return out
def path(d,pts,fill,width=1):d.line(curve(pts),fill=fill,width=width)
def ribbon(d,pts,widths,fill):
 # Hand-specified fold edges and widths, rasterized directly at native size.
 mid=curve(pts);left=[];right=[]
 for i,p in enumerate(mid):
  a=mid[max(0,i-1)];b=mid[min(len(mid)-1,i+1)];dx=b[0]-a[0];dy=b[1]-a[1];length=max(1,math.hypot(dx,dy));t=i/(len(mid)-1);f=t*(len(widths)-1);k=min(int(f),len(widths)-2);w=widths[k]+(widths[k+1]-widths[k])*(f-k)
  left.append((grid(p[0]-dy/length*w/2),grid(p[1]+dx/length*w/2)));right.append((grid(p[0]+dy/length*w/2),grid(p[1]-dx/length*w/2)))
 d.polygon(left+right[::-1],fill=fill)
def bevel(d,b,fill,light,dark,width=1):
 x,y,r,t=b;d.rectangle(b,fill=fill)
 for k in range(width):d.line([(x+k,t-k),(x+k,y+k),(r-k,y+k)],fill=light);d.line([(x+k+1,t-k),(r-k,t-k),(r-k,y+k+1)],fill=dark)
def lettering(d,box,lines,ink,scale=1,gap=1,role='label'):
 x,y,r,b=box;h=len(lines)*7*scale+(len(lines)-1)*gap;assert h<=b-y,(role,lines,box)
 top=y+(b-y-h)//2
 for line in lines:
  w=(len(line)*6-1)*scale;assert w<=r-x,(line,box);left=x+(r-x-w)//2
  TEXT.append({'role':role,'text':line,'box':d.box(box),'inkBox':d.box((left,top,left+w,top+7*scale)),'scale':scale*d.scale,'binaryGlyphs':True,'view':d.viewName})
  for char in line:
   for j,row in enumerate(FONT[char]):
    for i,v in enumerate(row):
     if v=='1':d.rectangle((left+i*scale,top+j*scale,left+(i+1)*scale-1,top+(j+1)*scale-1),fill=ink)
   left+=6*scale
  top+=7*scale+gap
class NativeDraw:
 def __init__(self,d,camera,viewName):self.draw=d;self.ox,self.oy,self.scale=camera;self.viewName=viewName
 def xy(self,p):return (round((p[0]-self.ox)*self.scale),round((p[1]-self.oy)*self.scale))
 def box(self,b):return [*self.xy(b[:2]),*self.xy(b[2:])]
 def polygon(self,pts,**kw):self.draw.polygon([self.xy(p)for p in pts],**kw)
 def line(self,pts,**kw):kw['width']=max(1,round(kw.get('width',1)*self.scale));self.draw.line([self.xy(p)for p in pts],**kw)
 def rectangle(self,b,**kw):
  # Inclusive native pixel cells retain solid glyph strokes at either camera.
  x,y,r,t=self.box(b);self.draw.rectangle((x,y,r+self.scale-1,t+self.scale-1),**kw)
 def rounded_rectangle(self,b,radius=0,**kw):self.draw.rounded_rectangle(self.box(b),radius=round(radius*self.scale),**kw)
 def ellipse(self,b,**kw):self.draw.ellipse(self.box(b),**kw)
 def arc(self,b,start,end,**kw):kw['width']=max(1,round(kw.get('width',1)*self.scale));self.draw.arc(self.box(b),start,end,**kw)
 def point(self,p,**kw):self.draw.point(self.xy(p),**kw)
class Painting:
 def __init__(self,camera=(0,0,1),viewName='default'):self.layers=[];self.records=[];self.camera=camera;self.viewName=viewName
 def add(self,name,fn):
  im=Image.new('RGBA',SIZE);fn(NativeDraw(ImageDraw.Draw(im),self.camera,self.viewName),im);im.save(ROOT/f'layers/{name}.png');self.layers.append(im);self.records.append({'file':f'layers/{name}.png','sha256':sha(ROOT/f'layers/{name}.png'),'bbox':im.getchannel('A').getbbox()})
 def image(self):
  im=Image.new('RGBA',SIZE)
  for layer in self.layers:im=Image.alpha_composite(im,layer)
  return im.convert('RGB')

def room(d,im):
 d.rectangle((0,0,563,277),fill=c('plaster',3))
 d.polygon([(0,0),(563,0),(563,20),(363,31),(203,20),(44,14)],fill=c('plaster',1))
 d.polygon([(180,28),(363,26),(360,145),(180,144)],fill=c('plaster',2))
 d.polygon([(364,29),(479,26),(486,142),(365,143)],fill=c('plaster',3))
 d.polygon([(381,39),(405,36),(416,42),(428,40),(446,46),(461,47),(468,81),(457,105),(440,119),(421,127),(395,120),(380,95)],fill=c('plaster',4))
 d.rectangle((0,145,563,224),fill=c('green',2));d.polygon([(0,145),(201,145),(199,224),(0,232)],fill=c('green',1))
 d.polygon([(0,231),(147,221),(564,221),(564,277),(0,277)],fill=c('velvet',2))
 for pts in [[(1,258),(128,230),(190,227)],[(0,270),(134,236),(189,232)],[(355,226),(548,229),(537,277)]]:path(d,pts,c('velvet',3),2)
 d.polygon([(13,259),(39,253),(70,252),(93,246),(106,247),(88,253),(57,258),(41,259)],fill=c('velvet',1))
 d.polygon([(365,248),(407,247),(423,241),(453,239),(466,242),(442,246),(430,253),(396,255)],fill=c('velvet',1))
 d.polygon([(399,268),(425,265),(456,265),(475,261),(506,263),(484,267),(451,269),(435,273),(403,274)],fill=c('velvet',3))
 # Window/curtain mass corresponds to the approved room's left wall.
 d.rectangle((53,0,198,221),fill=c('green',0));d.rectangle((62,0,66,217),fill=c('green',3));d.line([(69,0),(69,216)],fill=c('brass',3))
 d.polygon([(98,26),(153,31),(156,145),(98,148)],fill=c('glass',2))
 d.polygon([(101,32),(113,34),(117,145),(100,145)],fill=c('glass',3))
 d.polygon([(121,37),(134,39),(137,141),(122,144)],fill=c('glass',1))
 for pts in [[(99,51),(154,57)],[(99,85),(154,88)],[(98,117),(156,119)],[(117,29),(122,146)],[(138,31),(141,145)]]:path(d,pts,c('green',3),2)
 for pts in [[(99,53),(155,59)],[(98,119),(156,121)],[(118,29),(123,144)]]:path(d,pts,c('green',0))
 d.line([(98,149),(157,147)],fill=c('brass',3),width=2)
 d.polygon([(75,0),(193,0),(192,216),(178,221),(172,215),(173,82),(161,50),(145,32),(118,27),(99,22),(86,32)],fill=c('velvet',2))
 for pts,ws,col in [([(87,0),(89,38),(87,69),(81,101),(79,162),(80,221)],[10,8,5,9],1), ([(97,0),(102,28),(100,56),(93,87),(90,116)],[8,7,4],3), ([(117,0),(117,22),(132,28),(154,34)],[12,10,8],3), ([(144,0),(147,24),(161,37),(169,69),(177,119),(178,213)],[9,10,6,7],0), ([(167,0),(167,21),(178,30),(184,83),(187,142),(185,216)],[8,11,7],3)]:ribbon(d,pts,ws,c('velvet',col))
 path(d,[(80,96),(92,109),(104,114)],c('brass',4),2);path(d,[(105,113),(103,131),(103,141)],c('brass',3),3)
 # Wainscot rails and dimensional framed panels.
 d.line([(0,151),(198,149)],fill=c('brass',3),width=2);d.line([(337,145),(489,145)],fill=c('brass',3),width=2)
 d.line([(337,148),(489,148)],fill=c('green',0),width=2)
 for box in [(350,157,377,206),(386,157,473,206),(105,163,149,207)]:
  x,y,r,b=box;bevel(d,box,c('green',1),c('green',4),c('green',0));d.rectangle((x+4,y+5,r-4,b-4),fill=c('green',2));d.line([(x+5,b-5),(r-5,b-5),(r-5,y+5)],fill=c('green',3))
 d.line([(342,214),(489,214)],fill=c('green',0),width=3);d.line([(343,211),(487,211)],fill=c('green',3))
 # Coherent localized plaster losses beneath duct/joints.
 d.polygon([(349,31),(364,30),(365,39),(360,44),(359,58),(354,62),(347,57),(351,47)],fill=c('plaster',1))
 d.line([(464,30),(463,45),(468,56),(464,67),(466,79)],fill=c('plaster',1))
 d.polygon([(376,125),(386,124),(391,118),(398,120),(398,131),(389,136),(382,135),(377,141),(371,140)],fill=c('plaster',1))
 d.line([(378,125),(386,125),(392,120)],fill=c('plaster',4))
 # Door remains closed and entirely without handle/keyhole.
 bevel(d,(489,35,568,224),c('green',0),c('green',4),c('green',0),3)
 d.line([(491,224),(491,35),(563,35)],fill=c('brass',3));d.rectangle((498,44,563,223),fill=c('green',2))
 for b in[(510,56,569,136),(510,151,569,209)]:
  x,y,r,t=b;bevel(d,b,c('green',1),c('green',3),c('green',0),2);d.rectangle((x+5,y+6,r-4,t-5),fill=c('green',2));d.line([(x+5,t-5),(r-5,t-5)],fill=c('green',3))
 # Mirror is empty, with stepped tarnish patches, no face.
 d.polygon([(0,4),(20,4),(33,13),(38,27),(47,33),(47,153),(0,161)],fill=c('brass',1))
 path(d,[(0,4),(20,6),(30,15),(33,29),(43,36),(43,151),(0,156)],c('brass',4),2)
 d.polygon([(0,11),(18,11),(27,20),(29,34),(39,39),(39,150),(0,155)],fill=c('steel',1))
 d.polygon([(0,14),(15,15),(24,25),(24,43),(33,48),(32,124),(18,134),(8,135),(0,142)],fill=c('steel',2))
 for pts in [[(1,20),(9,21),(13,28),(9,37),(2,39)],[(20,47),(26,50),(24,59),(17,62),(15,54)],[(5,79),(15,77),(18,85),(13,93),(3,94)],[(24,110),(31,108),(31,118),(24,126),(17,125)],[(1,139),(10,135),(14,137),(11,147),(1,148)]]:d.polygon(pts,fill=c('steel',1))

def fittings(d,im):
 # Intrusive duct uses broad planes and meaningful flanges, no tiny clutter.
 d.polygon([(289,0),(564,0),(564,19),(324,30),(302,26),(291,18)],fill=c('steel',1))
 d.polygon([(296,1),(564,1),(564,10),(322,18),(304,15)],fill=c('steel',2))
 d.line([(299,4),(562,3)],fill=c('steel',3));d.line([(320,23),(563,15)],fill=c('steel',0),width=3)
 for x,y in[(321,2),(362,1),(408,1),(467,0),(520,0)]:
  d.polygon([(x,y),(x+3,y),(x+3,22),(x+8,23),(x+7,27),(x+1,25)],fill=c('steel',0));d.line([(x,y),(x,21)],fill=c('steel',3));d.point((x+1,y+4),fill=c('steel',4))
 bevel(d,(422,0,457,17),c('steel',0),c('steel',3),c('steel',0))
 for y in[3,7,11,15]:d.line([(425,y),(454,y)],fill=c('steel',2))
 # Lamp casts down/right on aged plaster, matching the approved room.
 d.polygon([(433,53),(446,62),(449,99),(440,113),(431,111),(425,99)],fill=c('plaster',1))
 d.polygon([(430,55),(439,57),(442,66),(441,102),(435,108),(425,103),(425,65)],fill=c('brass',1))
 d.line([(432,58),(437,61),(439,70),(439,100),(434,105)],fill=c('brass',3))
 d.ellipse((426,47,432,53),fill=c('brass',3));d.point((428,48),fill=c('brass',5))
 d.polygon([(417,57),(421,53),(435,53),(440,58),(437,62),(418,61)],fill=c('brass',2));d.line([(417,57),(422,54),(434,54),(439,58)],fill=c('brass',4))
 d.polygon([(419,61),(437,61),(434,88),(422,88)],fill=c('brass',4));d.polygon([(422,62),(428,61),(429,87),(424,87)],fill=c('brass',5))
 d.line([(419,61),(422,89),(434,89),(438,61)],fill=c('brass',1));d.line([(429,62),(429,87)],fill=c('brass',3))
 bevel(d,(421,89,435,94),c('brass',2),c('brass',4),c('brass',1));d.rectangle((425,95,432,103),fill=c('brass',2));d.line([(425,95),(425,101),(428,104)],fill=c('brass',4));d.rectangle((426,104,431,107),fill=c('brass',1))
 # Familiar vanity edge and velvet stool at left.
 d.polygon([(0,162),(83,157),(94,163),(92,173),(0,181)],fill=c('wood',1))
 d.polygon([(0,160),(82,156),(94,162),(3,169)],fill=c('cloth',3));d.line([(0,160),(82,156),(94,162),(3,170)],fill=c('brass',4))
 for x,y in[(6,178),(76,173)]:d.line([(x,y),(x+1,263)],fill=c('wood',1),width=5);d.line([(x-1,y),(x,258)],fill=c('brass',3))
 d.line([(2,184),(86,176)],fill=c('wood',0),width=2)
 for x,y in[(18,175),(63,171)]:d.line([(x,y),(x+10,y-1)],fill=c('brass',3),width=2)
 d.polygon([(9,210),(63,205),(77,213),(73,239),(14,247),(7,236)],fill=c('velvet',1))
 d.polygon([(10,210),(26,204),(59,202),(74,210),(76,218),(58,224),(21,226),(8,220)],fill=c('velvet',3))
 path(d,[(9,215),(25,207),(54,206),(71,211)],c('velvet',4),2)
 path(d,[(24,211),(36,213),(43,217),(58,218)],c('velvet',2),2)
 d.line([(14,231),(14,265)],fill=c('wood',1),width=4);d.line([(66,230),(68,260)],fill=c('wood',1),width=4)
 d.line([(16,231),(16,263)],fill=c('brass',3));d.line([(69,231),(70,257)],fill=c('brass',3))

def rack_back(d,im):
 d.ellipse((133,247,366,274),fill=c('velvet',1))
 path(d,[(163,245),(163,20),(166,13),(173,11),(318,15),(325,20),(325,235)],c('steel',0),7)
 path(d,[(163,244),(163,20),(166,13),(173,11),(318,15),(325,20),(325,234)],c('steel',2),4)
 path(d,[(162,242),(162,20),(166,13),(173,11),(317,15),(323,20),(323,233)],c('steel',4),1)
 d.line([(173,10),(316,14)],fill=c('steel',4));d.line([(175,14),(317,18)],fill=c('steel',1))
 for x,y in[(163,21),(325,25),(163,76),(325,78)]:
  bevel(d,(x-5,y-3,x+5,y+3),c('steel',2),c('steel',4),c('steel',0));d.point((x-2,y),fill=c('steel',4));d.point((x+2,y),fill=c('steel',0))
 # A literal empty wooden hanger, with no mannequin or wearer.
 path(d,[(247,18),(249,13),(251,11),(252,9),(250,7),(248,8)],c('brass',1),2)
 path(d,[(246,18),(249,14),(251,11),(250,8)],c('brass',4))
 d.polygon([(245,20),(250,20),(258,27),(281,38),(278,41),(248,30),(222,40),(218,38),(238,27)],fill=c('wood',2))
 path(d,[(221,38),(239,27),(247,23),(257,29),(278,39)],c('wood',4),2)
 d.line([(224,40),(274,40)],fill=c('wood',1))

SKIRT=[(241,86),(255,87),(270,95),(286,115),(301,138),(314,163),(325,186),(340,213),(348,236),(334,243),(309,247),(285,246),(258,249),(234,249),(209,248),(183,247),(160,243),(143,244),(124,238),(121,233),(139,204),(155,174),(178,141),(198,116),(219,99),(236,91)]
def skirt(d,im):
 d.polygon(curve(SKIRT+[SKIRT[0]],3),fill=c('cloth',3))
 # Coherent body masses and underfolds; each is a constant-colour native shape.
 ribbon(d,[(245,93),(224,119),(207,151),(192,186),(177,218),(161,239)],[20,32,28,21],c('cloth',2))
 ribbon(d,[(251,95),(254,130),(270,167),(286,204),(309,242)],[16,25,24,21],c('cloth',2))
 ribbon(d,[(259,99),(278,124),(296,155),(316,196),(338,233)],[10,19,18,17],c('cloth',1))
 # Long satin folds make rounded volume; widths taper deliberately.
 folds=[([(239,96),(224,122),(215,156),(197,193),(184,228),(180,242)],[6,13,17,11],5), ([(245,96),(239,128),(234,165),(228,203),(226,244)],[5,11,16,12],4), ([(249,97),(250,133),(254,174),(267,212),(279,244)],[5,10,14,8],5), ([(253,99),(265,134),(278,173),(296,209),(315,241)],[3,8,11,6],4), ([(234,100),(213,132),(193,171),(170,205),(148,238)],[5,11,12,9],5), ([(263,111),(283,148),(301,187),(321,223),(334,237)],[4,6,8,5],4)]
 for pts,widths,shade in folds:
  ribbon(d,pts,widths,c('cloth',shade));path(d,[(x-1,y)for x,y in pts],c('cloth',6),1)
 # Selected deep crease seams remain long connected shapes.
 for pts in [[(241,110),(228,142),(220,183),(214,222),(211,244)],[(248,113),(247,151),(250,195),(257,229),(264,246)],[(227,116),(204,150),(182,191),(167,224)]]:path(d,pts,c('cloth',2),2)
 # Heavy asymmetric fabric swags rather than regular scalloped decoration.
 swags=[([(238,94),(225,109),(207,124),(189,128),(183,124)],[5,9,10,3]), ([(229,112),(213,133),(192,148),(170,155),(161,151)],[4,9,11,4]), ([(221,137),(200,160),(178,181),(157,188),(146,184)],[4,10,13,5]), ([(206,165),(187,190),(164,211),(143,219),(132,216)],[4,9,13,5]), ([(257,98),(271,107),(285,121),(296,138)],[5,8,7,2]), ([(279,149),(296,161),(308,179),(317,193)],[4,9,8,4]), ([(283,186),(302,203),(320,222),(333,231)],[4,10,11,5])]
 for pts,ws in swags:
  shadow=[(x+1,y+4)for x,y in pts];ribbon(d,shadow,[w+3 for w in ws],c('cloth',1));ribbon(d,pts,ws,c('cloth',5));path(d,[(x-1,y-2)for x,y in pts],c('cloth',6),2)
  # Irregular few lace knots on the hem: material detail, not all-over grain.
  cp=curve(pts);indices=[int((len(cp)-1)*f)for f in[.22,.40,.61,.79,.95]]
  for n,i in enumerate(indices):
   x,y=cp[i]
   # Cutwork eyelets and connected lobes, confined to the lace edging.
   d.line([(x-3,y+2),(x-2,y+5),(x,y+6),(x+3,y+3)],fill=c('cloth',6))
   d.line([(x-2,y+2),(x,y),(x+2,y+2),(x,y+4),(x-2,y+2)],fill=c('cloth',5));d.point((x,y+2),fill=c('cloth',2))
 # Irregular hem groups follow cloth volume and ground plane.
 path(d,[(124,234),(143,241),(160,240),(184,245),(210,245),(234,247),(258,246),(285,243),(309,244),(334,240),(346,235)],c('cloth',5),3)
 for x,y in[(132,239),(148,242),(167,243),(187,246),(206,247),(224,248),(244,248),(266,247),(289,245),(312,246),(333,242)]:
  d.line([(x-3,y-1),(x-2,y+1),(x,y+2),(x+3,y)],fill=c('cloth',5));d.line([(x-2,y-1),(x,y),(x+2,y-1)],fill=c('cloth',6))
 # Selective embroidery on the broad satin panels, rather than a noise field.
 for x,y in[(191,195),(215,214),(239,231),(278,221),(304,229)]:
  d.line([(x-3,y),(x-1,y-2),(x+1,y-1),(x+1,y+1),(x+3,y+2)],fill=c('cloth',5))
  d.line([(x-2,y+2),(x,y+1),(x+2,y-1)],fill=c('cloth',6));d.point((x,y),fill=c('cloth',3))

def bodice(d,im):
 # Empty garment: shaped fabric, no skin, shoulders, head or torso inside.
 shape=[(224,43),(231,45),(241,46),(249,47),(258,46),(270,43),(269,52),(263,64),(259,76),(257,85),(261,90),(252,94),(242,91),(239,84),(238,75),(234,63),(228,54)]
 d.polygon(curve(shape+[shape[0]],3),fill=c('cloth',4))
 # Tailored empty fabric cups and an under-bust seam, not a flat triangle.
 d.ellipse((230,46,248,62),fill=c('cloth',3));d.ellipse((231,46,247,59),fill=c('cloth',5))
 d.arc((232,47,246,58),190,295,fill=c('cloth',6),width=2)
 d.ellipse((248,46,266,62),fill=c('cloth',3));d.ellipse((249,46,265,59),fill=c('cloth',5))
 d.arc((250,47,264,58),190,295,fill=c('cloth',6),width=2)
 path(d,[(233,60),(240,64),(248,63),(255,64),(263,60)],c('cloth',2))
 ribbon(d,[(231,48),(236,61),(242,77),(243,88)],[8,7,6],c('cloth',2))
 ribbon(d,[(239,49),(244,62),(247,77),(249,90)],[6,5,4],c('cloth',6))
 ribbon(d,[(259,48),(257,61),(253,77),(253,91)],[7,6,4],c('cloth',5))
 path(d,[(267,47),(261,62),(257,78),(257,86)],c('cloth',2),2)
 path(d,[(231,48),(237,64),(242,78),(242,86)],c('cloth',5))
 for pts in [[(237,49),(241,63),(245,78),(246,88)],[(251,49),(252,61),(250,76),(250,90)],[(260,49),(257,62),(254,78)]]:path(d,pts,c('cloth',3))
 path(d,[(239,88),(246,92),(253,91),(260,89)],c('brass',2),2);d.rectangle((247,89,251,92),fill=c('brass',3));d.point((248,89),fill=c('brass',5))
 # Collar void and lace sit in front of the empty hanger, not a mannequin.
 d.polygon([(228,41),(240,43),(250,44),(261,43),(271,40),(269,44),(259,48),(248,49),(237,47)],fill=c('cloth',1))
 path(d,[(227,41),(239,43),(249,44),(260,43),(272,40)],c('cloth',5),2)
 # Distinct shoulder lace, with larger airy lobes that survive the native grid.
 for pts in [[(221,36),(228,39),(232,44),(229,50),(222,50),(219,55),(213,52),(209,54),(205,49),(206,44),(212,41),(215,37)],[(272,36),(281,37),(286,41),(292,44),(291,50),(285,53),(280,51),(277,55),(273,50),(268,47),(268,42)]]:
  d.polygon(pts,fill=c('cloth',3));path(d,pts+[pts[0]],c('cloth',5),2)
 for x,y in[(211,45),(217,41),(224,44),(214,50),(279,42),(286,46),(281,50)]:
  d.line([(x-2,y),(x,y-2),(x+2,y),(x,y+2),(x-2,y)],fill=c('cloth',6));d.point((x,y),fill=c('cloth',1))

def machinery(d,im):
 # Outer lace is parted in the primary Focus; inner release lining stays shut.
 d.polygon([(259,97),(272,101),(288,111),(314,128),(320,159),(309,179),(281,177),(259,154),(252,116)],fill=c('green',0))
 path(d,[(259,98),(272,102),(289,112),(304,130),(312,151),(314,163)],c('cloth',1),4)
 # Tucked motor/gearbox: barrel, contacts and mounted geared drum.
 bevel(d,(253,110,323,151),c('steel',1),c('steel',3),c('steel',0),2)
 d.ellipse((250,115,269,144),fill=c('brass',0));d.ellipse((253,114,271,143),fill=c('brass',2));d.arc((253,114,271,143),160,290,fill=c('brass',4),width=2)
 d.rounded_rectangle((260,110,311,148),radius=6,fill=c('brass',1));d.rounded_rectangle((261,111,308,145),radius=5,fill=c('brass',3))
 d.line([(269,112),(300,112),(306,116)],fill=c('brass',5),width=2);d.line([(266,145),(302,145),(308,141)],fill=c('brass',0),width=2)
 # Readable gear teeth and axle, without impossible unsupported machinery.
 for i in range(12):
  a=math.tau*i/12;x=round(319+10*math.cos(a));y=round(130+10*math.sin(a));d.rectangle((x-1,y-1,x+1,y+1),fill=c('brass',2))
 d.ellipse((310,121,328,139),fill=c('brass',3));d.ellipse((313,124,325,136),fill=c('brass',0));d.ellipse((316,127,322,133),fill=c('steel',2));d.point((318,128),fill=c('steel',4))
 bevel(d,(250,148,276,153),c('steel',2),c('steel',4),c('steel',0));bevel(d,(310,146,330,151),c('steel',2),c('steel',4),c('steel',0))
 for x,y in[(254,150),(271,150),(314,148),(326,148)]:d.point((x,y),fill=c('steel',4))
 # Folded lace opens around the machinery, with heavy cloth depth.
 ribbon(d,[(260,95),(274,100),(292,113),(307,131),(318,157),(322,180)],[5,7,9,10],c('cloth',4))
 path(d,[(262,94),(276,100),(293,112),(308,132),(319,157),(323,179)],c('cloth',6),2)
 for x,y in[(273,100),(286,108),(300,122),(312,143),(321,166)]:d.line([(x-2,y),(x-1,y+3),(x+1,y+3),(x+3,y+1)],fill=c('cloth',5))

def front_labels(d,im):
 # The case-mounted plaque and hanging safety tag sit in FRONT of loose lace.
 # Rendering their physical surfaces last prevents fabric from clipping type.
 bevel(d,(269,117,304,140),c('cloth',4),c('cloth',6),c('brass',1))
 # Physical label size follows the motor, rather than expanding the machine
 # to carry large readable type in the wide view. Closer camera resolves it.
 top=120
 for line in ['AUTOFIT','BRIDAL','SYSTEM']:
  w=len(line)*4-1;left=round((270+303-w)/2)
  TEXT.append({'role':'small manufacturer label','text':line,'box':d.box((269,117,304,140)),'inkBox':d.box((left,top,left+w,top+5)),'scale':d.scale,'font':'3x5','binaryGlyphs':True,'view':d.viewName})
  for ch in line:
   for j,row in enumerate(MICRO[ch]):
    for i,v in enumerate(row):
     if v=='1':d.rectangle((left+i,top+j,left+i,top+j),fill=c('green',0))
   left+=4
  top+=6
 path(d,[(294,148),(296,151),(297,155)],c('brass',1))
 bevel(d,(276,153,306,168),c('cloth',4),c('cloth',6),c('brass',1))
 d.rectangle((280,158,286,162),fill=c('green',1));d.line([(281,155),(281,158)],fill=c('green',1));d.line([(284,155),(284,158)],fill=c('green',1));path(d,[(286,160),(290,160),(293,163)],c('green',1))
 d.line([(295,156),(302,156)],fill=c('green',1));d.line([(295,159),(301,159)],fill=c('green',1));d.line([(295,162),(299,162)],fill=c('green',1))

def cables(d,slack=False):
 # Cable geometry is a state layer; cloth and all housing stay shared.
 a=[(230,46),(236,58),(241,70),(244,81),(249,88),(256,97),(260,108),(260,116)]
 b=[(268,45),(265,58),(261,73),(257,85),(260,98),(270,107),(276,111)]
 if slack:
  a=[(230,46),(235,59),(240,72),(242,84),(240,92),(245,101),(253,106),(260,116)]
  b=[(268,45),(266,59),(262,75),(260,85),(264,96),(270,103),(275,111)]
 for pts in[a,b]:path(d,pts,c('brass',0),3);path(d,pts,c('brass',3),1)
 collar=[(230,46),(238,48),(248,49),(259,48),(268,45)]if not slack else[(230,46),(236,50),(245,53),(254,53),(262,50),(268,45)]
 path(d,collar,c('steel',0),2);path(d,[(x,y-1)for x,y in collar],c('brass',4))
 for x,y in[(241,70),(262,75)]:d.rectangle((x-1,y-1,x+1,y+2),fill=c('brass',2));d.point((x,y),fill=c('brass',5))

def covered_lining(d,im):
 # The default lower inner lining masks the release and its text entirely.
 d.polygon(curve([(239,96),(230,104),(222,117),(214,132),(208,145),(205,164),(200,181),(208,186),(223,172),(237,151),(246,130),(251,111),(249,100),(239,96)],3),fill=c('cloth',4))
 ribbon(d,[(241,100),(232,116),(223,137),(216,157),(204,181)],[5,10,10,4],c('cloth',5));path(d,[(237,103),(226,125),(215,147),(208,170)],c('cloth',2),2)
 path(d,[(238,99),(228,112),(216,133),(208,154),(201,181)],c('cloth',6),2)
 for x,y in[(231,114),(221,131),(212,150),(206,168)]:d.line([(x-2,y),(x-1,y+3),(x+2,y+3)],fill=c('cloth',5))

def release_revealed(d,im):
 # A moment within the motor node: lining lifted, tab examined/pressed,
 # cables now slack. Not a new Focus, choice, flag or persistent UI mode.
 d.polygon(curve([(240,96),(249,100),(254,121),(254,149),(257,183),(246,190),(217,187),(204,174),(205,144),(210,120),(222,104),(240,96)],3),fill=c('green',0))
 # Folded-back lining has thickness and visible underside.
 ribbon(d,[(240,97),(223,105),(210,123),(202,146),(199,169),(207,183)],[5,13,15,9],c('cloth',2))
 path(d,[(239,96),(221,105),(208,123),(198,146),(195,168),(204,184)],c('cloth',5),3)
 path(d,[(236,99),(221,110),(212,128),(206,149),(203,166)],c('cloth',6))
 bevel(d,(211,111,252,147),c('steel',1),c('steel',3),c('steel',0))
 bevel(d,(213,112,250,131),c('brass',3),c('brass',5),c('brass',1))
 lettering(d,(214,113,249,130),['MANUAL','SLACK'],c('green',0),gap=2,role='SUPPLEMENT ONLY - manual slack discovery')
 # Brass release tab, partly depressed; shaft remains mechanically connected.
 d.rectangle((221,132,241,139),fill=c('brass',0));d.rectangle((224,132,240,136),fill=c('brass',2));d.line([(224,132),(240,132)],fill=c('brass',5));d.line([(222,141),(244,141)],fill=c('steel',0),width=2)
 # Low, non-emergency warning remains distinct from the tab's label.
 bevel(d,(190,145,255,174),c('cloth',4),c('cloth',6),c('brass',1))
 lettering(d,(194,147,251,172),['NOT AN','EMERGENCY','STOP'],c('green',0),gap=2,role='SUPPLEMENT ONLY - not an emergency stop')
 # Looped cable at the release, visibly less taut after the authored press.
 path(d,[(248,135),(244,142),(236,145),(231,143),(226,144)],c('brass',0),3);path(d,[(248,135),(244,142),(236,145),(231,143),(226,144)],c('brass',3))

def rack_front(d,im):
 # Front upright occludes fabric consistently; back upright stays behind it.
 d.line([(163,78),(163,244)],fill=c('steel',0),width=6);d.line([(163,78),(163,244)],fill=c('steel',2),width=3);d.line([(161,79),(161,242)],fill=c('steel',4))
 for y in[78,238]:bevel(d,(158,y-3,168,y+3),c('steel',2),c('steel',4),c('steel',0))
 d.line([(140,245),(221,254),(358,240)],fill=c('steel',0),width=6)
 d.line([(140,243),(221,251),(358,237)],fill=c('steel',2),width=5)
 d.line([(140,241),(221,249),(358,235)],fill=c('steel',4))
 d.line([(143,246),(220,254),(355,241)],fill=c('steel',1))
 for x,y in[(141,249),(221,257),(357,244)]:
  bevel(d,(x-5,y-8,x+5,y-1),c('steel',2),c('steel',4),c('steel',0))
  d.ellipse((x-8,y-1,x+7,y+13),fill=c('steel',0));d.arc((x-7,y,x+6,y+12),50,210,fill=c('steel',2),width=2)
  d.rectangle((x-3,y-1,x+2,y+6),fill=c('steel',3));d.rectangle((x-2,y,x,y+4),fill=c('steel',4));d.point((x,y+5),fill=c('steel',1))

def shared(p,prefix=''):
 for name,fn in [('room-native-painted-fields',room),('native-duct-lamp-furniture',fittings),('rack-rear-and-empty-hanger',rack_back),('native-skirt-folds-and-lace',skirt),('native-empty-bodice',bodice),('native-motor-and-outer-lace',machinery),('manufacturer-and-disconnect-labels',front_labels)]:p.add(prefix+name,fn)
def main():
 global VIEW_SCALE
 p=Painting();shared(p)
 common_layers=p.layers[:];common_records=p.records[:];outputs={}
 for key,fn in [('default',covered_lining),('manual-slack',release_revealed)]:
  p.viewName=key if key=='default'else'diagnostic-world-slack';p.layers=common_layers[:];p.records=common_records[:];p.add(key+'-inner-lining',fn);p.add(key+'-cable-routes',lambda d,im,k=key:cables(d,k=='manual-slack'));p.add(key+'-front-rack-and-casters',rack_front)
  im=p.image();RECIPES[key]=p.records[:];outputs[key]=im
  if key=='default':
   im.save(ROOT/'native/CH4-NEW-08-autofit-gown-v01.png');im.resize((2256,1112),Image.Resampling.NEAREST).save(ROOT/'previews/CH4-NEW-08-autofit-gown-v01-4x.png')
  else:im.save(ROOT/'diagnostics/manual-slack-world-registration-NOT-candidate.png');RECIPES['manual-slack-world-diagnostic']=p.records[:]
 allowed=Image.new('L',SIZE);d=ImageDraw.Draw(allowed);d.rectangle((189,95,258,191),fill=255);d.rectangle((227,42,279,118),fill=255);allowed.save(ROOT/'masks/authorized-manual-slack-change.png')
 diff=ImageChops.difference(outputs['default'],outputs['manual-slack']);actual=ImageChops.lighter(ImageChops.lighter(diff.getchannel('R'),diff.getchannel('G')),diff.getchannel('B')).point(lambda v:255 if v else 0);actual.save(ROOT/'masks/actual-manual-slack-change.png')
 # Re-render shared geometry directly on the native canvas at the closer
 # camera. No crop/enlargement of a raster image is used for this candidate.
 VIEW_SCALE=2;close=Painting((165,36,2),'manual-slack');shared(close,'close-');close.add('close-lining-revealed',release_revealed);close.add('close-slack-cables',lambda d,im:cables(d,True));close.add('close-front-rack',rack_front)
 def close_details(d,im):
  # Higher camera resolution permits selected fastener highlights.
  for x,y in[(254,150),(271,150),(314,148),(326,148)]:
   nx,ny=d.xy((x,y));d.draw.ellipse((nx-2,ny-2,nx+2,ny+2),fill=c('steel',0));d.draw.point((nx-1,ny-1),fill=c('steel',4));d.draw.point((nx+1,ny+1),fill=c('steel',2))
 close.add('close-native-fastener-detail',close_details);im=close.image();im.save(ROOT/'native/CH4-NEW-08-manual-slack-revealed-v01.png');im.resize((2256,1112),Image.Resampling.NEAREST).save(ROOT/'previews/CH4-NEW-08-manual-slack-revealed-v01-4x.png');RECIPES['manual-slack']=close.records[:];VIEW_SCALE=1
 (ROOT/'evidence/native-layer-recipes.json').write_text(json.dumps({'sharedLayers':common_records,'states':RECIPES},indent=2)+'\n');(ROOT/'evidence/lettering-layout.json').write_text(json.dumps(TEXT,indent=2)+'\n');(ROOT/'evidence/native-palette-ramps.json').write_text(json.dumps(P,indent=2)+'\n')
 print(json.dumps({'newCandidates':'UNSELECTED','nativeImages':[{'file':x.name,'sha256':sha(x),'dimensions':list(Image.open(x).size)}for x in sorted((ROOT/'native').glob('*.png'))],'nativeRasterBuiltFromBlank':True,'sourcePixelsTransferred':False}))
if __name__=='__main__':main()
