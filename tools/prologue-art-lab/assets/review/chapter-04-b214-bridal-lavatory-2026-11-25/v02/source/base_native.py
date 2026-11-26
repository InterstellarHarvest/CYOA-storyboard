"""B2-14 native painting from blank canvases; no source PNG is read.
Design is source-informed; illustration geometry/material clusters are native.
Curve mathematics describes shapes, never smooth colour gradients.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import math,json,hashlib
ROOT=Path(__file__).resolve().parents[1];RECIPES={};SHELLS={}
P={'cream':['#726754','#97856b','#b39c7b','#cfb794','#e3cfad','#efe1c5'],'green':['#1c302a','#2c463b','#425c4d','#677c66','#95a28a'],'brass':['#51442c','#806238','#af8848','#d4b16a','#efcf8b'],'steel':['#253a34','#43594d','#6d7e69','#a3ae95','#d1d4b7'],'stone':['#847c6b','#a79b83','#c5b79c','#ddcfb2','#f0e4cb'],'shell':['#8b806c','#ab997e','#c6b399','#dcc9ac','#eddfc6','#fbefd7']}
def c(k,n):return P[k][n]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def curve(pts,steps=5):
 p=[pts[0]]+list(pts)+[pts[-1]];out=[]
 for k in range(1,len(p)-2):
  a,b,q,e=p[k-1:k+3]
  for i in range(steps):
   t=i/steps;out.append(tuple(round(.5*(2*b[j]+(-a[j]+q[j])*t+(2*a[j]-5*b[j]+4*q[j]-e[j])*t*t+(-a[j]+3*b[j]-3*q[j]+e[j])*t*t*t))for j in[0,1]))
 out.append(pts[-1]);return out
def line(d,p,col,w=1):d.line(curve(p),fill=col,width=w)
def band(d,pts,widths,col):
 p=curve(pts);a=[];b=[]
 for i,(x,y)in enumerate(p):
  u=p[max(0,i-1)];v=p[min(len(p)-1,i+1)];dx=v[0]-u[0];dy=v[1]-u[1];length=max(1,math.hypot(dx,dy));f=i/(len(p)-1)*(len(widths)-1);k=min(int(f),len(widths)-2);w=widths[k]+(widths[k+1]-widths[k])*(f-k)
  a.append((round(x-dy*w/length/2),round(y+dx*w/length/2)));b.append((round(x+dy*w/length/2),round(y-dx*w/length/2)))
 d.polygon(a+b[::-1],fill=col)
def bevel(d,b,fill,hi,lo,w=1):
 x,y,r,t=b;d.rectangle(b,fill=fill)
 for i in range(w):d.line([(x+i,t-i),(x+i,y+i),(r-i,y+i)],fill=hi);d.line([(x+i+1,t-i),(r-i,t-i),(r-i,y+i+1)],fill=lo)
class Art:
 def __init__(self,key,size):self.key=key;self.size=size;self.layers=[];self.records=[]
 def add(self,name,fn):
  im=Image.new('RGBA',self.size);fn(ImageDraw.Draw(im),im);p=f'layers/{self.key}-{name}.png';im.save(ROOT/p);self.layers.append(im);self.records.append({'file':p,'sha256':sha(ROOT/p),'bbox':im.getchannel('A').getbbox()});return im
 def save(self,name):
  out=Image.new('RGBA',self.size)
  for im in self.layers:out=Image.alpha_composite(out,im)
  out=out.convert('RGB');out.save(ROOT/f'native/{name}.png');out.resize((out.width*4,out.height*4),Image.Resampling.NEAREST).save(ROOT/f'previews/{name}-4x.png');RECIPES[self.key]=self.records

def room_planes(d,im):
 d.rectangle((0,0,313,205),fill=c('cream',2));d.polygon([(22,8),(292,8),(247,27),(67,27)],fill=c('cream',3))
 d.polygon([(22,8),(67,27),(67,145),(22,185)],fill=c('cream',2));d.rectangle((67,27,247,145),fill=c('cream',3));d.polygon([(247,27),(292,8),(292,185),(247,145)],fill=c('cream',1))
 d.polygon([(69,42),(111,43),(131,51),(147,75),(156,94),(69,98)],fill=c('cream',4));d.polygon([(69,45),(94,44),(114,54),(128,77),(132,92),(70,93)],fill=c('cream',5))
 d.polygon([(22,100),(67,88),(247,88),(292,100),(292,185),(247,145),(67,145),(22,185)],fill=c('green',2))
 d.polygon([(22,100),(67,88),(67,145),(22,185)],fill=c('green',1));d.polygon([(247,88),(292,100),(292,185),(247,145)],fill=c('green',1))
 d.line([(22,100),(67,88),(247,88),(292,100)],fill=c('brass',3));d.line([(23,102),(67,90),(247,90),(291,102)],fill=c('green',0))
 # Continuous wall, no cupboards/doors/hatch beneath the floating counter.
 d.polygon([(69,114),(112,114),(129,126),(129,140),(69,140)],fill=c('green',3));d.line([(67,142),(247,142)],fill=c('green',3))
 d.line([(22,184),(67,145),(247,145),(292,184)],fill=c('green',0),width=2)
 d.polygon([(67,146),(247,146),(292,186),(292,205),(22,205),(22,186)],fill=c('stone',2))
 for x in[67,103,139,175,211,247]:
  near=round(157+(x-157)*140/81);d.line([(x,146),(near,205)],fill=c('stone',1))
 for y in[155,169,188]:
  f=(y-65)/81;d.line([(max(22,round(157-90*f)),y),(min(292,round(157+90*f)),y)],fill=c('stone',1))
 for pts in [[(115,170),(163,170),(166,187),(106,187)],[(83,189),(142,189),(141,205),(72,205)],[(94,158),(102,158),(101,167),(91,167)],[(87,173),(98,173),(96,180),(84,180)]]:d.polygon(pts,fill=c('stone',3))
 d.line([(115,170),(163,170)],fill=c('stone',1));d.line([(106,188),(166,188)],fill=c('stone',1))

def architecture(d,im):
 d.line([(23,13),(65,31)],fill=c('cream',4),width=2);d.line([(249,30),(291,13)],fill=c('cream',3))
 for pts in [[(75,51),(81,51),(83,47),(139,47)],[(174,47),(230,47),(234,51),(240,51)],[(75,52),(75,80),(81,80),(84,84),(231,84),(235,80),(240,80),(240,52)]]:
  d.line(pts,fill=c('cream',2));d.line([(x+1,y-1)for x,y in pts],fill=c('cream',4))
 d.line([(30,32),(57,44),(57,83),(30,92)],fill=c('cream',1));d.line([(32,34),(55,44),(55,81),(32,90)],fill=c('cream',3))
 d.line([(258,44),(284,31),(284,92),(258,83)],fill=c('cream',0));d.line([(260,45),(282,35),(282,90),(260,81)],fill=c('cream',2))
 # Intrusive ceiling ventilation, with no controls or AI face.
 d.polygon([(56,18),(68,12),(254,12),(272,6),(272,28),(255,34),(67,39),(55,33)],fill=c('steel',1))
 d.polygon([(67,15),(254,15),(254,30),(67,35)],fill=c('steel',2));d.polygon([(57,20),(66,16),(66,34),(56,31)],fill=c('steel',2));d.polygon([(255,14),(270,8),(270,26),(255,31)],fill=c('steel',2))
 d.line([(68,15),(252,15)],fill=c('steel',4));d.line([(69,33),(252,29)],fill=c('steel',0),width=2)
 for x,y in[(82,13),(113,0),(209,0),(239,13)]:
  d.polygon([(x,y),(x+3,y),(x+3,35),(x+6,36),(x+5,39),(x,37)],fill=c('steel',0));d.line([(x,y),(x,34)],fill=c('steel',3));d.point((x+1,y+4),fill=c('steel',4))
 bevel(d,(148,15,182,31),c('steel',0),c('steel',3),c('steel',0))
 for y in[18,22,26,30]:d.line([(151,y),(179,y)],fill=c('steel',2))
 d.polygon([(102,56),(109,60),(110,74),(106,81),(101,79)],fill=c('cream',1));d.polygon([(99,55),(105,55),(107,59),(106,76),(102,79),(98,76)],fill=c('brass',1));d.ellipse((99,51,103,55),fill=c('brass',3))
 d.polygon([(96,57),(99,54),(105,55),(107,58),(105,60),(97,60)],fill=c('brass',2));d.line([(97,57),(100,55),(104,56)],fill=c('brass',4))
 d.polygon([(98,60),(105,60),(104,71),(99,71)],fill=c('brass',3));d.rectangle((99,60,102,70),fill=c('cream',5));bevel(d,(98,72,105,75),c('brass',2),c('brass',4),c('brass',0));d.rectangle((101,76,103,79),fill=c('brass',1))
 d.rectangle((0,0,21,205),fill=c('green',0));d.rectangle((292,0,313,205),fill=c('green',0));d.rectangle((12,0,16,205),fill=c('green',1));d.line([(18,0),(18,205)],fill=c('brass',2));d.line([(21,0),(21,205)],fill=c('green',3));d.rectangle((298,0,303,205),fill=c('green',1));d.line([(294,0),(294,205)],fill=c('brass',2))

def counter(d,im):
 d.polygon([(94,94),(220,94),(242,104),(72,104)],fill=c('stone',3));d.rectangle((72,104,242,109),fill=c('stone',2));d.line([(73,104),(241,104)],fill=c('stone',4));d.line([(73,108),(241,108)],fill=c('stone',1));d.line([(72,110),(242,110)],fill=c('brass',3))
 d.polygon([(78,111),(235,111),(228,116),(91,116)],fill=c('green',1))
 for x in[100,218]:
  d.rectangle((x,111,x+3,127),fill=c('brass',1));d.line([(x,111),(x+2,112),(x+2,125)],fill=c('brass',3));d.line([(x+2,120),(x+7,112)],fill=c('brass',2),width=2);d.point((x+1,125),fill=c('brass',4))
 d.line([(85,102),(94,100),(101,100)],fill=c('stone',2));d.line([(212,102),(221,103),(230,102)],fill=c('stone',2))

def shell(size,center,width,height,kind):
 x0,y0=center;im=Image.new('RGBA',size);d=ImageDraw.Draw(im)
 def at(x,y):return round(x0+x*width),round(y0+y*height)
 angles=[-162,-155,-148,-143,-137,-132,-125,-120,-113,-108,-101,-96,-89,-84,-77,-72,-65,-60,-53,-48,-41,-36,-29,-24,-18]
 radii=[.92,.99,1,.95,1,1.03,.98,1,1.04,.99,1.02,1.05,1.02,1.02,1.05,1,1.01,1.03,.98,1,1.01,.97,.99,.98,.90]
 if kind=='third':radii=[r*(.98 if i%4==0 else 1)for i,r in enumerate(radii)]
 arc=curve([at(math.cos(math.radians(a))*.5*r,math.sin(math.radians(a))*r)for a,r in zip(angles,radii)],3)
 outline=curve(arc+[at(.16,-.08),at(.10,.015),at(-.08,.025),at(-.17,-.07),arc[0]],3)
 d.polygon([(x+1,y+max(1,round(height*.045)))for x,y in outline],fill=c('shell',1));d.polygon(outline,fill=c('shell',3));d.line(arc,fill=c('shell',4),width=max(1,round(width*.016)))
 inner=[(-.43,-.39),(-.36,-.65),(-.17,-.86),(.08,-.91),(.29,-.73),(.43,-.44),(.28,-.29),(.14,-.09),(.03,-.025),(-.09,-.025),(-.24,-.20),(-.43,-.39)]
 d.polygon(curve([at(*p)for p in inner],4),fill=c('shell',4))
 if kind=='smooth':
  light=[(-.35,-.55),(-.25,-.78),(-.08,-.89),(.09,-.87),(.20,-.73),(.13,-.53),(.03,-.33),(-.02,-.13),(-.08,-.055),(-.16,-.19),(-.22,-.37),(-.35,-.55)]
  d.polygon(curve([at(*p)for p in light],4),fill=c('shell',5));band(d,[at(.23,-.72),at(.33,-.49),at(.26,-.30),at(.12,-.11)],[max(1,width*.045),max(1,width*.065),max(1,width*.03)],c('shell',3))
  band(d,[at(-.44,-.36),at(-.30,-.22),at(-.20,-.12),at(-.13,-.02)],[max(1,width*.06),max(1,width*.045),1],c('shell',2));line(d,[at(-.42,-.37),at(-.29,-.25),at(-.17,-.11),at(-.10,-.02)],c('shell',5),max(1,round(width*.018)))
 elif kind=='ridged':
  for a in[-150,-130,-110,-90,-70,-50,-30]:
   t=math.radians(a);p=[at(0,-.02),at(.23*math.cos(t)-.012,.48*math.sin(t)),at(.46*math.cos(t),.91*math.sin(t))]
   band(d,p,[1,max(1,width*.045),max(1,width*.067)],c('shell',2));band(d,[(x-1,y)for x,y in p],[1,max(1,width*.026),max(1,width*.044)],c('shell',4));line(d,[(x-2,y)for x,y in p],c('shell',5),max(1,round(width*.017)))
 else:
  for a in[-132,-94,-56]:
   t=math.radians(a);line(d,[at(0,-.04),at(.23*math.cos(t),.48*math.sin(t)),at(.44*math.cos(t),.87*math.sin(t))],c('shell',3),max(1,round(width*.014)))
  band(d,[at(-.34,-.53),at(-.20,-.76),at(-.04,-.89)],[max(1,width*.045),max(1,width*.06),1],c('shell',5));band(d,[at(.24,-.74),at(.34,-.48),at(.25,-.28),at(.13,-.12)],[1,max(1,width*.05),max(1,width*.025)],c('shell',3))
 line(d,[at(-.17,-.08),at(-.10,.005),at(.025,.015),at(.12,-.03),at(.17,-.08)],c('shell',2),max(1,round(width*.02)));line(d,[at(-.13,-.06),at(-.07,-.015),at(.04,-.01),at(.12,-.05)],c('shell',5),max(1,round(width*.012)))
 return im

def add_shells(a,items):
 def shadows(d,im):
  for x,y,w,h,kind in items:
   d.ellipse((round(x-w*.44+3),round(y-h*.17),round(x+w*.51+5),round(y+h*.13)),fill=c('stone',1));d.ellipse((round(x-w*.28),round(y-h*.06),round(x+w*.31),round(y+h*.05)),fill=c('stone',0))
 a.add('contact-shadows',shadows);records=[]
 for x,y,w,h,kind in items:
  s=shell(a.size,(x,y),w,h,kind);a.add('shell-'+kind,lambda d,im,s=s:im.alpha_composite(s));mask=s.getchannel('A');p=f'masks/{a.key}-shell-{kind}.png';mask.save(ROOT/p);records.append({'kind':kind,'center':[x,y],'width':w,'height':h,'mask':p,'bbox':mask.getbbox(),'paletteFamily':'same neutral ivory ramp'})
 SHELLS[a.key]=records

def focus_wall(d,im):
 d.rectangle((0,0,563,277),fill=c('cream',3));d.polygon([(0,0),(162,0),(247,81),(0,89)],fill=c('cream',4));d.polygon([(0,0),(47,0),(132,72),(55,75),(0,42)],fill=c('cream',5))
 d.line([(18,0),(18,31),(27,42),(36,44),(44,55),(518,55),(529,44),(540,42),(548,31),(548,0)],fill=c('cream',2),width=2);d.line([(21,0),(21,30),(29,39),(38,42),(46,52),(517,52),(527,42),(538,39),(545,30),(545,0)],fill=c('cream',4))
 d.rectangle((0,88,563,115),fill=c('green',2));d.line([(0,88),(563,88)],fill=c('brass',1),width=3);d.line([(0,87),(563,87)],fill=c('brass',4));d.line([(0,92),(563,92)],fill=c('green',0));d.line([(0,114),(563,114)],fill=c('green',0),width=2)

def focus_counter(d,im):
 d.rectangle((0,116,563,240),fill=c('stone',3));d.polygon([(0,116),(159,116),(123,238),(0,238)],fill=c('stone',4));d.polygon([(451,116),(563,116),(563,238),(497,238)],fill=c('stone',2))
 for pts in[[(0,196),(31,187),(54,190),(69,184)],[(194,230),(225,216),(251,219),(268,210)],[(482,201),(506,194),(528,197),(562,187)]]:line(d,pts,c('stone',2));line(d,[(x,y+1)for x,y in pts],c('stone',4))
 d.rectangle((0,240,563,260),fill=c('stone',2));d.line([(0,239),(563,239)],fill=c('stone',4),width=2);d.line([(0,258),(563,258)],fill=c('stone',1));d.rectangle((0,261,563,277),fill=c('green',1));d.line([(0,261),(563,261)],fill=c('brass',3));d.line([(0,264),(563,264)],fill=c('green',0),width=2)

def main():
 a=Art('room',(314,206));a.add('clean-room-planes',room_planes);a.add('architectural-duct-light',architecture);a.add('open-counter',counter);add_shells(a,[(113,100,20,13,'smooth'),(157,100,21,13,'ridged'),(201,100,20,13,'third')]);a.save('CH4-NEW-02-bridal-lavatory-v01')
 a=Art('focus',(564,278));a.add('matching-wall',focus_wall);a.add('solid-counter',focus_counter);add_shells(a,[(112,188,106,77,'smooth'),(282,189,108,78,'ridged'),(451,188,106,76,'third')]);a.save('CH4-NEW-09-three-seashells-v01')
 (ROOT/'evidence/native-layer-recipes.json').write_text(json.dumps(RECIPES,indent=2)+'\n');(ROOT/'evidence/shell-identities.json').write_text(json.dumps(SHELLS,indent=2)+'\n');(ROOT/'evidence/material-ramps.json').write_text(json.dumps(P,indent=2)+'\n')
 (ROOT/'evidence/architecture.json').write_text(json.dumps({'vanishingPoint':[157,65],'nearRoom':[22,8,292,185],'backRoom':[67,27,247,145],'depthFactor':2/3,'counterTop':[[94,94],[220,94],[242,104],[72,104]],'openUnderCounter':True,'brackets':2,'shells':3,'plumbingFixtures':0,'textOrInstructions':0},indent=2)+'\n')
 print(json.dumps({'status':'UNSELECTED','assets':[{'file':p.name,'sha256':sha(p),'dimensions':list(Image.open(p).size)}for p in sorted((ROOT/'native').glob('*.png'))],'nativeFromBlank':True,'sourcePixelsTransferred':False}))
if __name__=='__main__':main()
