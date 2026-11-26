"""B2-17: separately raster-constructed native slot and inspection illustrations.

No source image is opened by this renderer. Shared object geometry establishes
identity; each size is rasterized directly with its own illustration/detail and
lettering decisions. No reduction, pixel transfer, AA, smooth colour gradient,
random grain or global palette quantization is used. Designs are source-derived.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import math,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
FONT=json.loads((ROOT/'source/chunky-glyphs.json').read_text())
RECIPES={};TEXT={};GEOMETRY={}
P={
 'paper':['#623735','#85443e','#ad5b50','#c87969','#dc9682','#edb39c','#f8ccb2'],
 'ink':['#48272b','#643237','#814047'],
 'desk':['#514b40','#6f6551','#8f7e62','#ac9674','#bfaa85','#cdbb96'],
 'silver':['#29333b','#485560','#687983','#8d9fa8','#b4c4c8','#d6dfdb','#eef0df','#fff8e5'],
 'reflection':['#69685f','#a4987c','#cfbfa1','#e8d6b4'],
 'ribbon':['#294b5d','#426e82','#6395a8','#8bb9c9','#b4d5df','#dcebee'],
}
def c(k,n):return P[k][n]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def curve(points,steps=6):
 p=[points[0]]+list(points)+[points[-1]];out=[]
 for k in range(1,len(p)-2):
  a,b,q,e=p[k-1:k+3]
  for i in range(steps):
   t=i/steps;out.append(tuple(.5*(2*b[j]+(-a[j]+q[j])*t+(2*a[j]-5*b[j]+4*q[j]-e[j])*t*t+(-a[j]+3*b[j]-3*q[j]+e[j])*t*t*t)for j in [0,1]))
 out.append(points[-1]);return out
class Draw:
 def __init__(self,d,transform=lambda x,y:(x,y),scale=1):self.d=d;self.transform=transform;self.scale=scale
 def xy(self,p):return tuple(round(v)for v in self.transform(*p))
 def poly(self,pts,col):self.d.polygon([self.xy(p)for p in pts],fill=col)
 def line(self,pts,col,w=1):self.d.line([self.xy(p)for p in pts],fill=col,width=max(1,round(w*self.scale)))
 def path(self,pts,col,w=1):self.line(curve(pts),col,w)
 def rect(self,box,col):
  x,y,r,b=box;self.poly([(x,y),(r,y),(r,b),(x,b)],col)
 def ellipse(self,box,col):
  x,y,r,b=box;self.poly([(x+(r-x)/2+(r-x)/2*math.cos(t*math.tau/128),y+(b-y)/2+(b-y)/2*math.sin(t*math.tau/128))for t in range(128)],col)
 def ribbon(self,pts,widths,col):
  mid=curve(pts);a=[];b=[]
  for i,(x,y)in enumerate(mid):
   u=mid[max(0,i-1)];v=mid[min(len(mid)-1,i+1)];dx=v[0]-u[0];dy=v[1]-u[1];length=max(1,math.hypot(dx,dy));f=i/(len(mid)-1)*(len(widths)-1);k=min(int(f),len(widths)-2);w=widths[k]+(widths[k+1]-widths[k])*(f-k)
   a.append((x-dy*w/length/2,y+dx*w/length/2));b.append((x+dy*w/length/2,y-dx*w/length/2))
  self.poly(a+b[::-1],col)
class Painting:
 def __init__(self,id,size,slot,transform=None,scale=1):self.id=id;self.size=size;self.slot=slot;self.transform=transform;self.scale=scale;self.records=[];self.layers=[];TEXT[id]=[]
 def add(self,name,fn,semantic=False):
  im=Image.new('RGBA',self.size);fn(Draw(ImageDraw.Draw(im),self.transform or(lambda x,y:(x,y)),self.scale),im)
  p=f'layers/{self.id}-{name}.png';im.save(ROOT/p);self.layers.append(im);self.records.append({'file':p,'sha256':sha(ROOT/p),'bbox':im.getchannel('A').getbbox()})
  if semantic:im.getchannel('A').save(ROOT/f'masks/{self.id}-{name}.png')
 def save(self,slug):
  out=Image.new('RGBA',self.size)
  for layer in self.layers:out=Image.alpha_composite(out,layer)
  if not self.slot:out=out.convert('RGB')
  p=f'native/{self.id}-{slug}-v01.png';out.save(ROOT/p);out.resize((out.width*4,out.height*4),Image.Resampling.NEAREST).save(ROOT/f'previews/{Path(p).stem}-4x.png');RECIPES[self.id]=self.records

def desk(d,im):
 d.rect((0,0,564,450),c('desk',3))
 d.poly([(0,0),(564,0),(564,30),(384,72),(137,55),(0,91)],c('desk',4))
 d.poly([(0,315),(155,290),(286,329),(564,302),(564,451),(0,451)],c('desk',2))
 # Native connected grain / old polish, quiet beneath the object; no noise field.
 for pts,col in [([(0,56),(83,48),(157,51),(229,43)],4), ([(332,29),(406,34),(479,22),(564,26)],5), ([(0,416),(108,397),(174,400),(224,389)],3), ([(349,413),(398,402),(479,405),(564,387)],3), ([(0,270),(42,263),(79,265)],2), ([(505,177),(548,173),(564,175)],4)]:d.path(pts,c('desk',col),2)

def homography(quad):
 (x0,y0),(x1,y1),(x2,y2),(x3,y3)=quad
 dx1=x1-x2;dx2=x3-x2;dy1=y1-y2;dy2=y3-y2;sx=x0-x1+x2-x3;sy=y0-y1+y2-y3
 den=dx1*dy2-dx2*dy1
 g=(sx*dy2-dx2*sy)/den if abs(den)>1e-9 else 0
 h=(dx1*sy-sx*dy1)/den if abs(den)>1e-9 else 0
 a=x1-x0+g*x1;b=x3-x0+h*x3;e=y1-y0+g*y1;f=y3-y0+h*y3
 return lambda u,v:((a*(u/430)+b*(v/278)+x0)/(g*(u/430)+h*(v/278)+1),(e*(u/430)+f*(v/278)+y0)/(g*(u/430)+h*(v/278)+1))

def paper_shape(d,im,slot):
 # One tear-off ticket with a red carbon-copy edge, not a pile of extra tickets.
 edge=[(0,0)]
 for i in range(1,21):
  x=i*21;amplitude=(5 if slot else 2)+(i%3)
  edge.extend([(x-9,1),(x-7,amplitude),(x-3,amplitude),(x,0)])
 edge.extend([(430,1),(430,251),(420,272),(404,278),(0,278)])
 d.poly([(u+2,v+3)for u,v in edge],c('paper',0))
 d.poly(edge,c('paper',3))
 d.poly([(2,8),(422,6),(426,248),(405,272),(5,274)],c('paper',4))
 d.poly([(3,10),(123,8),(152,60),(126,117),(10,134)],c('paper',5))
 d.poly([(160,9),(422,8),(426,106),(309,120),(174,114)],c('paper',4))
 d.poly([(7,148),(129,124),(271,133),(424,120),(426,248),(405,272),(5,274)],c('paper',4))
 d.path([(8,121),(69,116),(132,116),(204,120),(278,116),(350,112),(421,113)],c('paper',3),2)
 d.path([(8,119),(69,114),(132,114),(204,118),(278,114),(350,110),(421,111)],c('paper',5))
 d.line([(2,13),(2,272),(402,276)],c('paper',2))
 d.line([(5,10),(6,270),(400,273)],c('paper',5))
 # Lower-right reverse curl / thin carbon edge stays clear of the stamp.
 d.poly([(406,259),(429,247),(425,265),(407,276)],c('paper',1))
 d.poly([(406,259),(429,247),(420,264),(407,272)],c('paper',5))
 d.path([(406,260),(416,260),(426,251)],c('paper',6))
 if not slot:
  # Deliberate tiny fiber bundles, restricted to unused margins and a crease.
  for pts in [[(14,29),(21,29),(26,27)],[(20,82),(24,80),(30,80)],[(388,23),(395,23),(401,21)],[(382,98),(389,97)],[(17,210),(25,208),(30,208)],[(57,258),(66,257)],[(178,266),(185,264),(191,265)],[(378,186),(386,185)],[(220,117),(229,119),(237,118)]]:
   d.path(pts,c('paper',5));d.path([(u,v+1)for u,v in pts],c('paper',3))
  for x in [17,61,109,156,203,251,298,347,395]:d.line([(x,1),(x+3,4),(x+7,3)],c('paper',6))

def glyphs(d,text,x,y,unit,ink,id,role,record=True):
 width=(len(text)*6-1)*unit;bounds=[]
 for n,char in enumerate(text):
  for j,row in enumerate(FONT[char]):
   for i,v in enumerate(row):
    if v=='1':
     u=x+(n*6+i)*unit;vv=y+j*unit;p=[(u,vv),(u+unit-.08,vv),(u+unit-.08,vv+unit-.08),(u,vv+unit-.08)];d.poly(p,ink);bounds.extend(d.xy(q)for q in p)
 if record:TEXT[id].append({'role':role,'text':text,'unit':unit,'localBox':[x,y,x+width,y+7*unit],'pixelBounds':[min(q[0]for q in bounds),min(q[1]for q in bounds),max(q[0]for q in bounds)+1,max(q[1]for q in bounds)+1],'projectedAtNative':True})
def centered(d,text,y,unit,ink,id,role,cx=215):glyphs(d,text,cx-(len(text)*6-1)*unit/2,y,unit,ink,id,role)

def ticket_ink(d,im,id,slot):
 if slot:
  # Readable short lot code and a few economical form/stamp blocks. No fake words.
  d.rect((46,34,385,46),c('ink',1));centered(d,'LOT 53',70,7,c('ink',0),id,'slot-lot-code')
  for b in [(73,137,192,146),(204,137,361,146),(74,166,169,174),(183,166,359,174)]:d.rect(b,c('ink',1))
  d.line([(238,211),(402,206),(405,260),(241,266),(238,211)],c('ink',1),9)
  d.line([(261,226),(380,222)],c('ink',1),9);d.line([(261,246),(381,242)],c('ink',1),9)
 else:
  centered(d,'DISPUTE TICKET',25,3,c('ink',0),id,'ticket-heading')
  d.line([(45,57),(385,57)],c('ink',1),2)
  centered(d,'LOT 53',72,5,c('ink',0),id,'lot-number')
  centered(d,'LACK OF PRIVACY',133,3,c('ink',0),id,'reason-first-line')
  centered(d,'— CUSTOMER PRESENT',165,3,c('ink',0),id,'reason-second-line')
  # Ink stamp sits on the paper plane. Legibility is preserved despite a few
  # real rubber-stamp edge breaks; no pseudo-text, serials or new rules appear.
  d.line([(236,207),(404,207),(404,265),(236,265),(236,207)],c('ink',1),3)
  for pts in [[(248,207),(251,207)],[(376,265),(380,265)],[(404,247),(404,250)]]:d.line(pts,c('paper',4),2)
  centered(d,'HOLD FOR',216,2,c('ink',1),id,'stamp-first-line',320)
  centered(d,'INSPECTION',241,2,c('ink',1),id,'stamp-second-line',320)

CX,CY,RX,RY=246,211,185,109
def arc(rx,ry,cy,a,b):
 return [(CX+rx*math.cos(math.radians(t)),cy+ry*math.sin(math.radians(t)))for t in [a+(b-a)*i/max(2,math.ceil(abs(b-a)/2))for i in range(max(2,math.ceil(abs(b-a)/2))+1)]]
def cylinder_strip(d,a,b,rx,ry,cy0,cy1,col):d.poly(arc(rx,ry,cy0,a,b)+arc(rx,ry,cy1,a,b)[::-1],col)
def annulus(d,a,b,outer,inner,cy,col):d.poly(arc(*outer,cy,a,b)+arc(*inner,cy,a,b)[::-1],col)

def ring_metal(d,im,slot):
 # Inner rear wall, a real vertical band below the top inner lip. Each angular
 # interval is a deliberately selected reflection group, not a colour gradient.
 inside=[(180,200,1),(200,216,2),(216,232,4),(232,247,3),(247,282,4),(282,298,3),(298,314,4),(314,333,2),(333,360,1)]
 for a,b,tone in inside:cylinder_strip(d,a,b,155,84,CY,254,c('silver',tone))
 for a,b in [(218,226),(294,301)]:cylinder_strip(d,a,b,155,84,218,250,c('reflection',2))
 d.line(arc(155,84,254,180,360),c('silver',0),3)
 d.line(arc(155,84,251,187,353),c('silver',2))
 # Forward outside wall. A few large reflected light shapes turn the metal;
 # the low warm strip reflects the desk, not a second decorative metal band.
 fronts=[(0,15,1),(15,30,3),(30,47,4),(47,52,6),(52,59,5),(59,74,4),(74,94,2),(94,111,3),(111,127,5),(127,131,6),(131,143,5),(143,159,4),(159,180,2)]
 for a,b,tone in fronts:cylinder_strip(d,a,b,RX,RY,CY,254,c('silver',tone))
 for a,b,tone in [(3,36,1),(36,64,2),(64,104,1),(104,143,2),(143,176,1)]:cylinder_strip(d,a,b,RX,RY,244,251,c('reflection',tone))
 d.line(arc(RX,RY,254,0,180),c('silver',0),3)
 d.line(arc(RX-2,RY-1,250,3,177),c('silver',2))
 # Rounded rim: narrow rolled outer lip, crown and inner arris.
 rim=[(0,27,2),(27,52,4),(52,70,6),(70,101,3),(101,122,5),(122,143,7),(143,165,5),(165,190,2),(190,221,4),(221,247,6),(247,281,5),(281,315,4),(315,340,3),(340,360,2)]
 for a,b,tone in rim:
  annulus(d,a,b,(185,109),(181,106),CY,c('silver',1 if tone<4 else 4))
  annulus(d,a,b,(181,106),(165,93),CY,c('silver',tone))
  annulus(d,a,b,(165,93),(155,84),CY,c('silver',max(1,tone-2)))
 d.line(arc(185,109,CY,0,360),c('silver',0))
 d.line(arc(180,105,CY,188,313),c('silver',7),2)
 d.line(arc(169,96,CY,15,169),c('silver',7),2)
 d.line(arc(155,84,CY,180,360),c('silver',5))
 d.line(arc(155,84,CY,0,180),c('silver',1),2)
 if not slot:
  # Selected shallow polishing/scuff marks follow the metal, not all-over grain.
  for a,b,cy,col in [(28,41,229,6),(48,55,235,4),(112,120,234,6),(129,137,241,5)]:d.line(arc(185,109,cy,a,b),c('silver',col))
  d.line(arc(172,98,CY,224,235),c('silver',5))

def ribbon(d,im,slot):
 # One continuous ribbon: one wrap, one compact knot and its two short ends.
 # Tail and fold masks are grouped; the inscription is fully separate and clear.
 d.ribbon([(421,277),(440,305),(469,342),(495,366)],[20,23,25,17],c('ribbon',1))
 d.ribbon([(422,276),(437,305),(463,343),(487,365)],[13,15,18,12],c('ribbon',3))
 d.ribbon([(419,283),(430,320),(449,354),(461,395)],[20,23,25,18],c('ribbon',1))
 d.ribbon([(418,283),(428,320),(445,356),(456,393)],[13,16,17,12],c('ribbon',3))
 d.path([(416,286),(425,321),(441,354),(451,385)],c('ribbon',4),3)
 d.path([(430,286),(443,315),(468,346),(488,361)],c('ribbon',4),3)
 d.poly([(448,391),(456,389),(462,396),(457,398),(450,400)],c('ribbon',2))
 d.poly([(484,361),(494,365),(498,370),(489,369),(485,371)],c('ribbon',2))
 # Loop around the right rim, with a lit woven front and deep fold underside.
 d.ribbon([(403,254),(407,236),(421,226),(434,229),(439,240),(432,254),(421,261)],[19,22,23,18,15],c('ribbon',0))
 d.ribbon([(403,251),(408,235),(421,228),(432,230),(436,240),(430,251)],[15,18,19,16,11],c('ribbon',2))
 d.ribbon([(405,246),(411,236),(421,231),(432,233)],[7,11,10,4],c('ribbon',4))
 d.path([(401,252),(408,237),(419,230),(429,230)],c('ribbon',5),2)
 d.path([(409,253),(419,245),(432,245)],c('ribbon',1),4)
 # A compact crossing knot is textile, not a bow or decorative jewel.
 d.poly([(410,258),(421,253),(434,259),(437,270),(431,283),(419,285),(410,276),(408,266)],c('ribbon',1))
 d.poly([(411,261),(421,256),(431,260),(431,268),(424,279),(416,277),(411,270)],c('ribbon',3))
 d.poly([(411,262),(419,258),(427,260),(420,264),(414,271)],c('ribbon',4))
 d.path([(411,262),(418,258),(425,259)],c('ribbon',5),2)
 d.poly([(419,268),(429,263),(432,266),(427,275),(420,281),(415,276)],c('ribbon',2))
 d.path([(418,273),(424,268),(430,267)],c('ribbon',4),2)
 if not slot:
  # Hem/warp detail follows the physical fold, with a few grouped stitch runs.
  for pts in [[(411,242),(417,236),(427,235)],[(431,297),(439,313),(450,329)],[(436,349),(444,367),(449,382)],[(460,334),(471,347),(484,360)]]:d.path(pts,c('ribbon',5))
  for x,y in [(411,238),(417,234),(424,233),(421,266),(425,271),(435,312),(440,321),(445,331),(441,359),(445,369),(449,379),(470,349),(479,358)]:
   d.line([(x-2,y),(x+2,y+2)],c('ribbon',4))
   d.line([(x-1,y+2),(x+2,y+3)],c('ribbon',2))

def engraving(d,im,id):
 text='AS IS, WHERE IS.';unit=2;advance=12
 # True tangent-oriented native glyphs, laid out by distance along the inner
 # wall's ellipse. Rotation is geometry, never a rotated/filtered raster font.
 samples=[];distance=0;previous=None
 for i in range(1601):
  t=math.radians(205+130*i/1600);p=(CX+151*math.cos(t),241+85*math.sin(t))
  if previous:distance+=math.dist(previous,p)
  samples.append((distance,t,p));previous=p
 total=(len(text)*6-1)*unit;start=(distance-total)/2;glyph_records=[]
 for n,char in enumerate(text):
  target=start+n*advance+5
  dist,t,(x,y)=min(samples,key=lambda q:abs(q[0]-target))
  dx=-151*math.sin(t);dy=85*math.cos(t);length=math.hypot(dx,dy);tx,ty=dx/length,dy/length;nx,ny=-ty,tx
  def local(u,v):return (x+u*tx+v*nx,y+u*ty+v*ny)
  points=[]
  for j,row in enumerate(FONT[char]):
   for i,v in enumerate(row):
    if v=='1':
     u=(i-2.5)*unit;vv=(j-3.5)*unit
     box=[local(u,vv),local(u+unit-.06,vv),local(u+unit-.06,vv+unit-.06),local(u,vv+unit-.06)]
     # Dark incised stroke, no bright duplicate text or illegible micro-engraving.
     d.poly(box,c('silver',0));points.extend(d.xy(p)for p in box)
  glyph_records.append({'character':char,'angleDegrees':math.degrees(t),'center':[round(x,3),round(y,3)],'tangentDegrees':math.degrees(math.atan2(ty,tx)),'bounds':([min(q[0]for q in points),min(q[1]for q in points),max(q[0]for q in points)+1,max(q[1]for q in points)+1]if points else None)})
 TEXT[id].append({'role':'inside-ring-engraving','text':text,'unit':unit,'glyphs':glyph_records,'followsInnerCurve':True,'nativeGlyphConstruction':True})

def maker(d,im):
 # Canon specifies existence only. Anonymous geometric punch; no invented brand,
 # initials, purity figure, date or additional words.
 d.poly([(246,133),(251,138),(246,143),(241,138)],c('silver',1))
 d.line([(241,138),(246,143),(251,138)],c('silver',5))
 d.poly([(246,135),(249,138),(246,141),(243,138)],c('silver',2))

def main():
 for p in ['native','previews','layers','masks','evidence']:(ROOT/p).mkdir(exist_ok=True)
 for id,slot,quad in [('CH4-NEW-10',True,[(11,29),(82,26),(86,75),(14,79)]),('CH4-NEW-11',False,[(58,86),(496,66),(512,365),(69,384)])]:
  plane=homography(quad);size=(96,96)if slot else(565,451);a=Painting(id,size,slot,plane,.175 if slot else 1)
  if not slot:
   a.add('quiet-clerk-desk',lambda d,im:desk(Draw(d.d),im))
   a.add('paper-contact-shadow',lambda d,im:d.poly([(2,7),(431,7),(437,275),(409,285),(1,285)],c('desk',1)))
  a.add('red-carbon-ticket',lambda d,im,slot=slot:paper_shape(d,im,slot),True)
  a.add('canonical-form-ink',lambda d,im,id=id,slot=slot:ticket_ink(d,im,id,slot),True)
  a.save('dispute-ticket-'+('slot'if slot else'inspection'));GEOMETRY[id]={'paperQuad':quad,'paperLocalSize':[430,278],'sharedObject':'one red carbon-copy ticket / perforated top / curled lower right','imageSize':list(size)}
 for id,slot in [('CH4-NEW-12',True),('CH4-NEW-13',False)]:
  transform=(lambda x,y:(x*.18-3,y*.18+5))if slot else None
  a=Painting(id,(96,96)if slot else(565,451),slot,transform,.18 if slot else 1)
  if not slot:
   a.add('quiet-desk',desk)
   a.add('ring-contact-shadow',lambda d,im:d.ellipse((61,300,443,377),c('desk',1)))
  a.add('plain-silver-band',lambda d,im,slot=slot:ring_metal(d,im,slot),True)
  if not slot:a.add('inside-engraving',lambda d,im:engraving(d,im,'CH4-NEW-13'),True);a.add('anonymous-maker-punch',maker,True)
  a.add('single-pale-blue-ribbon',lambda d,im,slot=slot:ribbon(d,im,slot),True)
  a.save('wedding-ring-'+('slot'if slot else'inspection'));GEOMETRY[id]={'sharedObject':'one plain low-domed silver band / one short pale blue ribbon / one wrap and knot with two ends','outerRadii':[RX,RY],'innerRadii':[155,84],'camera':{'scale':.18,'offset':[-3,5]}if slot else{'scale':1,'offset':[0,0]},'imageSize':[96,96]if slot else[565,451],'engravingVisible':not slot}
 (ROOT/'evidence/native-layer-recipes.json').write_text(json.dumps(RECIPES,indent=2)+'\n');(ROOT/'evidence/native-text-layout.json').write_text(json.dumps(TEXT,indent=2)+'\n');(ROOT/'evidence/object-geometry.json').write_text(json.dumps(GEOMETRY,indent=2)+'\n');(ROOT/'evidence/material-ramps.json').write_text(json.dumps(P,indent=2)+'\n')
 print(json.dumps({'status':'UNSELECTED','assets':[{'file':str(p.relative_to(ROOT)),'sha256':sha(p),'dimensions':list(Image.open(p).size),'mode':Image.open(p).mode,'colours':len(Image.open(p).getcolors(565*451))}for p in sorted((ROOT/'native').glob('*.png'))]}))
if __name__=='__main__':main()
