"""Four B2-16 aftermath illustrations constructed on blank native 314x206 layers.

No reference raster is loaded by this renderer. Literal material ramps, drawn
forms and final-grid curves describe the illustration; no smooth colour fields,
source reduction, sharpening, antialiasing, quantization or noise is used.
The visual design is source-derived from the preserved references.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import math, json, hashlib
ROOT=Path(__file__).resolve().parents[1]
SIZE=(314,206)
RECIPES={};INVENTORY={}
P={
 'green':['#1c302b','#2b4238','#41584b','#627563','#8d9a83','#bac1a5'],
 'plaster':['#625d4d','#847a62','#a49475','#beac88','#d3c19c','#e8d7b2','#f3e4c3'],
 'tile':['#444e45','#667262','#88927d','#a5ad94','#c4c7ab','#d9d9bd'],
 'brass':['#483e2c','#745a36','#a07c42','#c6a15f','#e7c682','#f7dfa5'],
 'metal':['#263630','#46574a','#6e7d6c','#98a38c','#c3cab0','#e3e4c9'],
 'silver':['#303b3b','#52605e','#7d8984','#a5b0a8','#cfd3c0','#e9e7d3'],
 'porcelain':['#626c5e','#8b9480','#b2b69c','#d0cdb0','#e9dfbd','#faf0ce'],
 'black':['#171e23','#252e34','#364149','#4c5960','#677375','#87908b'],
 'cloth':['#676e60','#878b75','#a5a18a','#c0b79a','#d7ccb0','#e9dfc4','#faf1d8'],
 'velvet':['#34282d','#4d2d36','#6c3741','#8a4a50','#ad6e70'],
 'paper':['#6b3f33','#a6533f','#bba077','#e0cea9','#f5e6c3'],
 'glass':['#3c5a58','#638580','#96b4a3','#c5d1b3'],
 'wood':['#433a2d','#765a39','#ad8953','#d5b577'],
}
def c(k,n):return P[k][n]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def curve(points,steps=6):
    pts=[points[0]]+list(points)+[points[-1]];out=[]
    for k in range(1,len(pts)-2):
        a,b,q,e=pts[k-1:k+3]
        for i in range(steps):
            t=i/steps
            out.append(tuple(round(.5*(2*b[j]+(-a[j]+q[j])*t+(2*a[j]-5*b[j]+4*q[j]-e[j])*t*t+(-a[j]+3*b[j]-3*q[j]+e[j])*t*t*t))for j in [0,1]))
    out.append(points[-1]);return out
def path(d,pts,col,w=1):d.line(curve(pts),fill=col,width=w)
def poly(d,pts,col):d.polygon(pts,fill=col)
def ribbon(d,pts,widths,col):
    mid=curve(pts);a=[];b=[]
    for i,(x,y)in enumerate(mid):
        u=mid[max(0,i-1)];v=mid[min(len(mid)-1,i+1)];dx=v[0]-u[0];dy=v[1]-u[1];length=max(1,math.hypot(dx,dy));f=i/(len(mid)-1)*(len(widths)-1);k=min(int(f),len(widths)-2);w=widths[k]+(widths[k+1]-widths[k])*(f-k)
        a.append((round(x-dy*w/length/2),round(y+dx*w/length/2)));b.append((round(x+dy*w/length/2),round(y-dx*w/length/2)))
    poly(d,a+b[::-1],col)
def bevel(d,box,fill,hi,lo,w=1):
    x,y,r,b=box;d.rectangle(box,fill=fill)
    for n in range(w):d.line([(x+n,b-n),(x+n,y+n),(r-n,y+n)],fill=hi);d.line([(x+n+1,b-n),(r-n,b-n),(r-n,y+n+1)],fill=lo)
class Painting:
    def __init__(self,id):self.id=id;self.layers=[];self.records=[];self.props=[]
    def add(self,name,fn,semantic=None):
        im=Image.new('RGBA',SIZE);fn(ImageDraw.Draw(im),im);p=f'layers/{self.id}-{name}.png';im.save(ROOT/p);self.layers.append(im);self.records.append({'file':p,'sha256':sha(ROOT/p),'bbox':im.getchannel('A').getbbox()})
        if semantic:
            mask=im.getchannel('A');p=f'masks/{self.id}-{name}.png';mask.save(ROOT/p);self.props.append({'entity':semantic,'mask':p,'bbox':mask.getbbox()})
    def save(self,slug):
        out=Image.new('RGBA',SIZE)
        for layer in self.layers:out=Image.alpha_composite(out,layer)
        out=out.convert('RGB');name=f'{self.id}-{slug}-v01';out.save(ROOT/f'native/{name}.png');out.resize((1256,824),Image.Resampling.NEAREST).save(ROOT/f'previews/{name}-4x.png');RECIPES[self.id]=self.records;INVENTORY[self.id]=self.props

def shoe(d,x,y,s=1):
    """One empty dress shoe, not a limb; continuous sole, heel, opening, toe cap."""
    def xy(p):return (round(x+p[0]*s),round(y+p[1]*s))
    def pp(pts,k,n):poly(d,curve([xy(p)for p in pts],3),c(k,n))
    pp([(0,0),(3,-13),(7,-19),(18,-18),(22,-10),(31,-7),(43,-4),(48,1),(46,6),(33,7),(16,5),(12,3),(2,4),(0,0)],'black',0)
    pp([(2,-1),(4,-12),(7,-17),(17,-16),(21,-9),(32,-6),(43,-3),(46,1),(43,3),(28,3),(18,1),(12,0),(4,1),(2,-1)],'black',2)
    pp([(3,-11),(7,-17),(17,-16),(18,-12),(12,-10),(7,-10),(3,-11)],'wood',1)
    path(d,[xy(p)for p in [(4,-13),(8,-18),(16,-17),(18,-14)]],c('cloth',3))
    pp([(23,-7),(32,-6),(43,-3),(46,0),(41,1),(30,0),(23,-2),(23,-7)],'black',1)
    path(d,[xy(p)for p in [(29,-5),(36,-4),(42,-2)]],c('black',4))
    path(d,[xy(p)for p in [(26,-6),(27,-1),(29,2)]],c('black',3))
    for a in range(3):path(d,[xy((16+a*2,-10+a*2)),xy((22+a*2,-11+a*2))],c('black',5))
    path(d,[xy(p)for p in [(2,2),(13,1),(18,3),(34,5),(45,4)]],c('black',3))
    path(d,[xy(p)for p in [(2,4),(12,4),(12,7),(2,7)]],c('black',0),max(1,round(s)))

def tiled_floor(d,im,top=132,vanish=(151,66),floor='tile'):
    d.rectangle((0,top,313,205),fill=c(floor,2))
    vx,vy=vanish;rows=[top,top+12,top+30,top+55,222];xs=[-45,7,59,111,163,215,267,319,371]
    def X(x,y):return round(vx+(x-vx)*(y-vy)/(top-vy))
    for j,(y0,y1)in enumerate(zip(rows,rows[1:])):
        for i,(x0,x1)in enumerate(zip(xs,xs[1:])):
            tone=2 if (i+j)%4 else 3
            poly(d,[(X(x0,y0),y0),(X(x1,y0),y0),(X(x1,y1),y1),(X(x0,y1),y1)],c(floor,tone))
            if (i,j)in [(2,1),(4,0),(3,3),(5,2)]:poly(d,[(X(x0,y0)+5,y0+3),(X(x1,y0)-3,y0+3),(X(x1,y0)-8,y0+5),(X(x0,y0)+8,y0+5)],c(floor,3))
    for x in xs:
        d.line([(X(x,top),top),(X(x,222),222)],fill=c(floor,1));d.line([(X(x,top)+1,top+1),(X(x,222)+1,222)],fill=c(floor,3))
    for y in rows[1:-1]:d.line([(0,y),(313,y)],fill=c(floor,1));d.line([(0,y+1),(313,y+1)],fill=c(floor,3))

def occupancy_room(d,im):
    d.rectangle((0,0,313,205),fill=c('plaster',3))
    poly(d,[(0,0),(313,0),(293,38),(95,38),(0,7)],c('tile',2))
    poly(d,[(0,7),(95,38),(95,134),(0,169)],c('plaster',3));d.rectangle((95,38,313,134),fill=c('plaster',4))
    for y in [47,65,84,105,126]:
        d.line([(95,y),(313,y)],fill=c('plaster',2));d.line([(96,y+1),(313,y+1)],fill=c('plaster',5))
    for x in [95,123,151,179,207,235,263,291]:
        d.line([(x,39),(x,132)],fill=c('plaster',2));d.line([(x+1,39),(x+1,131)],fill=c('plaster',5))
    for y in [27,52,77,102,127]:d.line([(0,y),(94,y+24)],fill=c('plaster',2))
    for x in [18,47,74]:d.line([(x,13+x//4),(x,151-x//4)],fill=c('plaster',2))
    poly(d,[(0,130),(95,111),(95,136),(0,167)],c('green',2));d.line([(0,131),(95,112)],fill=c('green',4))
    tiled_floor(d,im,134,(151,66));d.line([(95,133),(313,133)],fill=c('green',1),width=3)
    # Cropped washstand and mirror echo the approved restroom, not a new setting.
    bevel(d,(7,48,83,102),c('glass',1),c('brass',3),c('brass',0),2)
    poly(d,[(11,52),(78,52),(78,76),(11,68)],c('glass',2));poly(d,[(11,70),(78,79),(78,98),(11,98)],c('glass',0))
    d.line([(47,52),(47,98)],fill=c('green',3));d.line([(49,52),(49,98)],fill=c('glass',3))
    d.ellipse((3,109,78,126),fill=c('porcelain',1));d.ellipse((3,107,78,119),fill=c('porcelain',4));d.ellipse((14,108,66,116),fill=c('porcelain',0));d.ellipse((16,109,64,114),fill=c('tile',1));d.arc((5,108,77,124),0,180,fill=c('porcelain',2),width=2)
    path(d,[(42,108),(42,102),(47,99),(52,101),(52,105)],c('metal',0),3);path(d,[(42,107),(42,102),(47,100),(51,102)],c('metal',4))
    path(d,[(40,125),(40,139),(49,141),(53,137),(53,132)],c('brass',1),4);path(d,[(39,125),(39,138),(48,140),(51,137)],c('brass',3))
    # Established ceiling ventilation, clearly separate from suspension cables.
    path(d,[(48,0),(48,20),(59,28),(128,28)],c('metal',0),13);path(d,[(47,0),(47,18),(59,25),(126,25)],c('metal',2),9);path(d,[(44,0),(44,17),(57,22),(126,22)],c('metal',4),2)
    for x in [69,99,124]:bevel(d,(x,20,x+3,33),c('metal',1),c('metal',4),c('metal',0))
    # Brass-bordered ceiling hatch and dark open void above the empty partitions.
    poly(d,[(132,5),(273,5),(283,29),(123,29)],c('brass',1));poly(d,[(135,8),(270,8),(279,26),(128,26)],c('green',0))
    d.line([(133,6),(272,6),(281,28)],fill=c('brass',4));d.line([(137,12),(268,12)],fill=c('metal',1),width=3)
    for x in [154,242]:d.line([(x,10),(x,23)],fill=c('metal',2),width=4)
    # Quiet angled floor shadow from the lifted enclosure; impact is long over.
    poly(d,[(158,135),(258,135),(281,159),(164,159),(146,153)],c('tile',1))

def lifted_stall(d,im):
    # Four cables and only a partition frame: NO floor/toilet lifted with it.
    for top,bottom in [((145,13),(153,48)),((181,16),(186,53)),((243,13),(237,46)),((269,19),(262,50))]:
        d.line([top,bottom],fill=c('metal',0),width=2);d.line([top,bottom],fill=c('metal',4))
        x,y=top;bevel(d,(x-2,y-2,x+2,y+1),c('brass',2),c('brass',4),c('brass',0))
    # Far partition, open doorway and an ajar panel reveal the empty interior.
    poly(d,[(153,47),(237,44),(263,51),(184,55)],c('green',3))
    poly(d,[(153,49),(184,55),(184,101),(153,94)],c('green',1))
    poly(d,[(157,53),(178,58),(178,96),(157,92)],c('green',2))
    poly(d,[(184,55),(221,53),(221,95),(184,101)],c('green',0))
    poly(d,[(187,58),(218,56),(218,91),(188,96)],c('green',1))
    # One raised door, visibly offset from the open empty gap to its left.
    poly(d,[(221,53),(262,51),(262,99),(221,104)],c('green',0))
    poly(d,[(223,55),(259,53),(259,96),(223,101)],c('green',2))
    d.line([(224,56),(257,54),(257,95)],fill=c('green',4));d.line([(228,61),(253,59),(253,91),(228,94),(228,61)],fill=c('green',1))
    d.line([(230,62),(251,60)],fill=c('green',3));d.line([(230,92),(251,89)],fill=c('green',0))
    bevel(d,(247,75,257,78),c('brass',2),c('brass',4),c('brass',0))
    for x,y in [(221,61),(221,87)]:d.rectangle((x,y,x+2,y+6),fill=c('brass',2));d.line([(x,y),(x,y+5)],fill=c('brass',4))
    for pts in [[(153,47),(153,96),(184,103)],[(184,55),(184,102)],[(237,44),(263,50),(263,100)]]:d.line(pts,fill=c('metal',0),width=3);d.line([(x-1,y)for x,y in pts],fill=c('metal',3))
    # Narrow bottom rails only, not a sealed occupied cabinet or box.
    d.line([(154,95),(183,103)],fill=c('green',4));d.line([(185,102),(218,97)],fill=c('green',3))

def broken_toilet(d,im):
    d.ellipse((153,176,243,192),fill=c('tile',1))
    # Recognisable oval bowl with a missing right section and snapped pedestal.
    poly(d,curve([(175,160),(181,173),(193,177),(193,184),(208,184),(209,174),(217,166),(209,160),(175,160)],3),c('porcelain',2))
    poly(d,[(192,173),(199,172),(203,181),(209,183),(191,183)],c('porcelain',4))
    d.ellipse((169,146,222,171),fill=c('porcelain',1));d.ellipse((168,143,222,163),fill=c('porcelain',4));d.ellipse((175,147,214,159),fill=c('porcelain',0));d.ellipse((177,148,212,157),fill=c('tile',1))
    d.arc((169,145,222,168),5,176,fill=c('porcelain',2),width=3);d.arc((169,143,222,163),180,346,fill=c('porcelain',5),width=2)
    poly(d,[(208,145),(216,144),(218,151),(213,154),(217,162),(209,167),(205,159),(209,153)],c('tile',1))
    d.line([(207,146),(211,151),(207,157),(211,163)],fill=c('porcelain',0));d.line([(205,148),(208,151)],fill=c('porcelain',5))
    # A broken outer bowl section on its side, clean ivory fracture faces.
    poly(d,[(224,166),(230,156),(237,160),(244,176),(241,184),(226,181),(224,166)],c('porcelain',1))
    poly(d,[(225,167),(231,158),(235,162),(241,177),(238,181),(229,177)],c('porcelain',4))
    path(d,[(227,168),(231,165),(235,174),(235,180)],c('porcelain',2),3)
    for pts in [[(160,170),(168,166),(175,177),(166,183),(157,178)],[(183,189),(191,182),(196,190)],[(211,190),(216,184),(223,191)],[(147,185),(154,182),(158,186)],[(238,192),(244,186),(250,192)]]:
        poly(d,[(x+1,y+2)for x,y in pts],c('tile',1));poly(d,pts,c('porcelain',3));d.line(pts[:2],fill=c('porcelain',5))
    poly(d,[(159,171),(163,174),(165,178),(169,176),(170,172),(166,170)],c('porcelain',1))

def auction_tags(d,im):
    for pts,hole in [([(126,182),(142,178),(149,184),(133,190)],(142,182)), ([(247,169),(258,164),(271,171),(258,176)],(253,168)), ([(205,197),(218,192),(228,198),(215,203)],(216,196))]:
        poly(d,[(x,y+1)for x,y in pts],c('paper',0));poly(d,pts,c('paper',1));mid=[(round((x+sum(p[0]for p in pts)/4*0.12)/1.12),round((y+sum(p[1]for p in pts)/4*0.12)/1.12))for x,y in pts];poly(d,mid,c('paper',4))
        d.ellipse((hole[0]-1,hole[1]-1,hole[0]+1,hole[1]+1),fill=c('paper',0));path(d,[(hole[0],hole[1]),(hole[0]+4,hole[1]-5),(hole[0]+9,hole[1]-2)],c('brass',2))

def quiet_suit_wall(d,im):
    d.rectangle((0,0,313,205),fill=c('plaster',3))
    poly(d,[(0,0),(133,0),(0,101)],c('plaster',4));poly(d,[(314,0),(314,48),(218,111),(170,111)],c('plaster',4))
    poly(d,[(0,110),(130,24),(168,24),(0,139)],c('plaster',4))
    d.rectangle((0,164,313,205),fill=c('green',3));d.line([(0,164),(313,164)],fill=c('plaster',5));d.line([(0,167),(313,167)],fill=c('green',1));d.line([(0,170),(313,170)],fill=c('green',4))
    # Sole wall shadow comes from the hanging empty garment.
    poly(d,curve([(159,48),(177,53),(213,68),(222,151),(203,159),(196,197),(175,200),(144,198),(133,158),(105,158),(102,134),(109,73),(145,57),(159,48)],4),c('plaster',1))
    poly(d,[(141,168),(199,168),(197,198),(177,201),(143,199)],c('green',2))

def wire_hanger(d,im):
    # One ordinary continuous bent-wire triangle with one hook and one crossbar.
    path(d,[(155,44),(155,39),(161,34),(163,29),(161,24),(156,22),(151,24),(148,28)],c('metal',0),3)
    path(d,[(155,44),(155,39),(161,34),(162,29),(160,25),(156,24),(152,25),(149,29)],c('metal',4))
    d.line([(155,44),(104,69),(210,69),(155,44)],fill=c('metal',0),width=3)
    d.line([(155,44),(104,69),(210,69),(155,44)],fill=c('metal',4))
    d.line([(115,68),(200,68)],fill=c('metal',3))

def trousers(d,im):
    poly(d,[(145,68),(169,68),(178,111),(183,191),(160,193),(156,155),(153,193),(131,191),(136,111)],c('black',0))
    poly(d,[(147,70),(155,70),(155,153),(150,190),(133,189),(139,112)],c('black',2))
    poly(d,[(158,70),(167,70),(175,112),(180,189),(162,191),(158,152)],c('black',2))
    poly(d,[(147,72),(150,72),(143,187),(138,188)],c('black',3))
    poly(d,[(161,72),(164,72),(174,189),(170,189)],c('black',3))
    path(d,[(145,76),(145,117),(143,155),(142,187)],c('black',4))
    path(d,[(167,77),(166,114),(170,150),(173,187)],c('black',4))
    d.line([(145,69),(169,69)],fill=c('black',4));d.line([(156,72),(156,145)],fill=c('black',0))
    for b in [(132,184,151,191),(162,185,181,192)]:bevel(d,b,c('black',2),c('black',3),c('black',0));d.line([(b[0]+2,b[1]+2),(b[2]-2,b[1]+2)],fill=c('black',1))

def tuxedo(d,im):
    outline=[(137,49),(154,53),(174,49),(184,54),(208,64),(213,87),(217,147),(202,151),(194,111),(195,151),(177,155),(165,147),(156,128),(145,150),(131,154),(111,150),(112,109),(105,149),(89,147),(94,90),(100,65),(124,56),(137,49)]
    poly(d,curve(outline,3),c('black',0))
    poly(d,curve([(137,51),(140,60),(143,79),(151,103),(155,125),(143,146),(132,151),(113,148),(116,109),(113,82),(104,69),(124,59),(137,51)],4),c('black',2))
    poly(d,curve([(174,51),(168,71),(160,96),(157,125),(167,146),(177,152),(193,148),(190,107),(195,83),(204,67),(182,56),(174,51)],4),c('black',2))
    # Empty inner neck and jacket opening show the folded trousers and wire.
    poly(d,[(139,53),(155,56),(171,53),(166,63),(144,63)],c('black',1))
    path(d,[(142,54),(154,57),(169,54)],c('black',3))
    # Rounded sleeves and controlled wool folds, rather than scattered speckles.
    ribbon(d,[(105,68),(100,89),(98,116),(96,145)],[7,9,10],c('black',3))
    path(d,[(104,71),(103,96),(101,119),(99,143)],c('black',4))
    ribbon(d,[(204,68),(205,92),(209,117),(210,146)],[7,8,7],c('black',2))
    path(d,[(204,73),(202,94),(205,121),(207,144)],c('black',3))
    path(d,[(114,88),(118,108),(116,136)],c('black',1),2)
    path(d,[(191,88),(187,108),(191,139)],c('black',1),2)
    # Satin lapels: broader glints, separate from matte cloth.
    poly(d,[(136,50),(123,62),(131,75),(123,72),(137,102),(154,123),(141,87),(137,70),(142,59)],c('black',0))
    poly(d,[(135,53),(127,62),(136,77),(127,75),(141,103),(151,117),(140,84),(136,69),(140,59)],c('black',3))
    poly(d,[(128,64),(132,70),(138,76),(142,91),(138,88)],c('black',4))
    path(d,[(125,62),(133,75),(126,73),(139,99),(151,117)],c('black',5))
    poly(d,[(174,50),(188,62),(180,76),(190,72),(175,104),(158,124),(171,85),(174,68),(168,59)],c('black',0))
    poly(d,[(175,53),(184,62),(175,78),(185,75),(172,103),(161,116),(173,83),(177,68),(172,59)],c('black',3))
    poly(d,[(180,65),(176,73),(173,84),(169,94),(174,90),(183,76)],c('black',4))
    path(d,[(186,63),(178,76),(187,74),(175,101),(161,118)],c('black',2))
    # Cut the actual empty opening out of this foreground layer. The folded
    # trousers and SAME hanger crossbar behind it must remain visible, rather
    # than being painted over with a filled black torso-shaped triangle.
    poly(d,[(143,57),(169,57),(172,63),(167,80),(160,101),(157,115),(150,96),(144,79),(140,63)],(0,0,0,0))
    # Welt and pocket flaps, seam construction, tiny quiet buttons.
    path(d,[(179,91),(191,88)],c('black',0),2);path(d,[(179,90),(191,87)],c('black',3))
    for pts in [[(116,124),(132,126),(130,133),(116,131)],[(177,126),(192,123),(193,130),(179,133)]]:
        poly(d,[(x,y+1)for x,y in pts],c('black',0));poly(d,pts,c('black',3));d.line(pts[:2],fill=c('black',4))
    for x,y in [(147,128),(96,136),(97,140),(209,137),(210,141)]:d.rectangle((x,y,x+1,y+1),fill=c('black',5));d.point((x+1,y+2),fill=c('black',0))
    path(d,[(91,145),(104,147)],c('black',0),2);path(d,[(203,148),(216,146)],c('black',0),2)

def steam(d,im):
    # Three detached shaped wisps, no opaque cloud obscuring the formalwear.
    for pts,ws in [([(126,45),(123,39),(126,32),(129,26),(127,20)],[1,3,2,1]), ([(159,19),(155,14),(156,8),(160,4),(159,0)],[1,3,2,1]), ([(186,46),(184,39),(188,33),(190,26),(188,21)],[1,2,3,1])]:
        ribbon(d,pts,ws,c('plaster',5));path(d,[(x,y-1)for x,y in pts[1:-1]],c('plaster',6))

def case_room(d,im):
    d.rectangle((0,0,313,205),fill=c('plaster',3));d.rectangle((0,58,313,111),fill=c('green',2))
    poly(d,[(0,0),(33,0),(96,58),(74,58)],c('plaster',4));poly(d,[(69,0),(88,0),(148,58),(126,58)],c('plaster',4))
    for x in [11,86,164,242]:
        bevel(d,(x,68,x+59,101),c('green',1),c('green',3),c('green',0),2);d.line([(x+4,98),(x+55,98)],fill=c('green',2))
    d.line([(0,57),(313,57)],fill=c('brass',3));d.line([(0,60),(313,60)],fill=c('green',0),width=2)
    d.line([(0,106),(313,106)],fill=c('brass',1),width=2);d.line([(0,109),(313,109)],fill=c('green',0),width=3)
    # Architectural window edge and plaster fillets, no new story props.
    bevel(d,(4,-7,91,49),c('green',0),c('plaster',5),c('plaster',1),2)
    d.rectangle((10,0,83,41),fill=c('glass',1));poly(d,[(12,0),(30,0),(67,39),(44,39)],c('glass',2))
    for pts in [[(11,14),(82,14)],[(11,29),(82,29)],[(36,0),(36,40)],[(61,0),(61,40)]]:d.line(pts,fill=c('green',0),width=2);d.line([(x-1,y-1)for x,y in pts],fill=c('green',3))
    for x in [104,220]:d.line([(x,0),(x,46),(x+86,46)],fill=c('plaster',1));d.line([(x+1,0),(x+1,45),(x+86,45)],fill=c('plaster',4))
    tiled_floor(d,im,112,(154,53))
    # Narrow carpet edge is recognisably the approved lobby's burgundy runner.
    poly(d,[(314,127),(314,205),(199,205)],c('velvet',2));d.line([(314,131),(204,205)],fill=c('brass',2),width=2)
    d.line([(313,140),(217,205)],fill=c('velvet',4))
    for pts in [[(292,159),(298,153),(302,155)],[(266,177),(273,171),(277,173)],[(241,196),(249,189),(253,191)]]:d.line(pts,fill=c('velvet',3),width=2)

def compact_case(d,im):
    # One portable case, roughly 1.9 shoe-lengths wide at the same floor depth.
    poly(d,[(118,166),(240,159),(254,167),(227,180),(130,181),(115,176)],c('tile',1))
    poly(d,[(117,143),(214,147),(239,132),(239,163),(216,178),(117,173)],c('silver',0))
    poly(d,[(120,144),(213,148),(213,175),(120,171)],c('silver',2))
    poly(d,[(216,148),(236,135),(236,161),(216,174)],c('silver',1))
    # Slight asymmetric lid lift is only two native pixels; no excessive bulge.
    lid=[(118,142),(119,137),(140,122),(196,123),(214,125),(228,124),(238,130),(237,137),(215,151),(120,147)]
    poly(d,curve(lid+[lid[0]],2),c('silver',2))
    poly(d,[(122,138),(142,125),(195,126),(214,128),(229,127),(234,131),(214,145)],c('silver',3))
    poly(d,[(178,125),(196,126),(217,130),(208,144),(191,143)],c('silver',4))
    path(d,[(122,140),(153,141),(190,143),(214,146),(234,133)],c('silver',5))
    path(d,[(119,146),(213,150),(238,135)],c('silver',0),2)
    path(d,[(121,149),(212,153),(236,139)],c('silver',4))
    path(d,[(120,169),(211,173),(234,159)],c('silver',4))
    path(d,[(122,151),(122,167),(128,170)],c('silver',3))
    # Selected long brushed-metal glints and folded corner seams.
    for pts in [[(130,157),(149,158)],[(176,162),(201,163)],[(158,131),(176,132)],[(222,149),(233,142)]]:d.line(pts,fill=c('silver',3))
    for x,y in [(132,151),(197,154)]:
        bevel(d,(x,y,x+7,y+12),c('brass',2),c('brass',4),c('brass',0));d.rectangle((x+2,y+4,x+5,y+9),fill=c('brass',1));d.point((x+3,y+5),fill=c('brass',4))
    # A single carrying handle, distinct from lid and clasps.
    for x,y in [(157,156),(183,157)]:bevel(d,(x-2,y-2,x+3,y+2),c('brass',2),c('brass',4),c('brass',0))
    path(d,[(157,157),(157,165),(161,168),(180,169),(185,165),(185,158)],c('black',0),5)
    path(d,[(157,157),(158,164),(162,166),(180,167),(183,164),(184,158)],c('black',3),2)

def case_shoe(d,im):
    d.ellipse((41,174,104,186),fill=c('tile',1));shoe(d,45,174,1.12)

def bridal_room(d,im):
    d.rectangle((0,0,313,205),fill=c('plaster',2));d.rectangle((0,112,313,172),fill=c('green',2))
    poly(d,[(230,28),(245,22),(277,24),(286,36),(282,80),(269,99),(241,102),(229,84)],c('plaster',3))
    poly(d,[(242,36),(261,31),(276,38),(278,75),(265,89),(245,90),(237,72)],c('plaster',4))
    poly(d,[(0,171),(313,168),(313,205),(0,205)],c('velvet',2))
    for pts in [[(0,195),(73,176),(105,174)],[(196,193),(225,189),(254,190),(279,183)],[(213,204),(254,199),(281,200)]]:path(d,pts,c('velvet',3),2)
    d.rectangle((21,0,87,170),fill=c('green',0));d.rectangle((28,9,78,111),fill=c('glass',1))
    poly(d,[(30,11),(39,13),(46,110),(30,110)],c('glass',3));poly(d,[(52,16),(62,18),(71,109),(58,109)],c('glass',2))
    for y in [34,62,90]:d.line([(30,y),(78,y+6)],fill=c('green',0),width=3);d.line([(30,y-1),(78,y+5)],fill=c('green',3))
    for x in [47,66]:d.line([(x,10),(x+5,111)],fill=c('green',0),width=2);d.line([(x-1,10),(x+4,111)],fill=c('green',3))
    d.line([(28,112),(81,115)],fill=c('brass',3))
    # Same heavy burgundy curtain and tie-back as B2-12/B2-13, left of the stand.
    poly(d,[(14,0),(94,0),(91,169),(79,174),(76,119),(72,63),(62,24),(31,17),(18,47)],c('velvet',2))
    for pts,ws,shade in [([(22,0),(23,33),(19,65),(16,115),(17,172)],[7,6,9],1), ([(31,0),(35,24),(32,49),(26,76)],[5,7,4],3), ([(68,0),(72,24),(79,64),(85,112),(85,169)],[9,7,10],0), ([(84,0),(86,45),(89,102),(88,170)],[5,7,4],3)]:ribbon(d,pts,ws,c('velvet',shade))
    path(d,[(16,74),(27,84),(38,87)],c('brass',3),2);path(d,[(37,87),(37,101)],c('brass',3),2)
    # Fixed hotel paneling / warm sconce. No mirror showing a wearer, no text.
    d.line([(93,112),(313,112)],fill=c('brass',3));d.line([(93,115),(313,115)],fill=c('green',0),width=2)
    for b in [(238,125,266,159),(275,125,310,159)]:bevel(d,b,c('green',1),c('green',3),c('green',0),2)
    d.line([(93,165),(313,165)],fill=c('green',0),width=3);d.line([(93,163),(313,163)],fill=c('green',3))
    poly(d,[(266,44),(278,52),(280,79),(271,91),(263,89)],c('plaster',1))
    bevel(d,(262,45,275,77),c('brass',1),c('brass',3),c('brass',0));d.rectangle((264,48,272,69),fill=c('brass',4));d.rectangle((265,49,268,68),fill=c('plaster',6))
    poly(d,[(260,47),(264,41),(273,42),(277,47)],c('brass',2));path(d,[(261,46),(265,43),(272,43)],c('brass',4));bevel(d,(263,71,274,75),c('brass',2),c('brass',4),c('brass',0));d.rectangle((267,76,271,82),fill=c('brass',2))
    # Restrained damaged plaster just at the existing construction seam.
    path(d,[(295,0),(293,18),(296,24),(293,37)],c('plaster',1))

def rack_back(d,im):
    d.ellipse((71,176,237,197),fill=c('velvet',1))
    path(d,[(92,178),(92,24),(95,18),(223,20),(228,25),(228,177)],c('metal',0),6)
    path(d,[(92,177),(92,24),(95,20),(223,22),(226,25),(226,177)],c('metal',2),3)
    path(d,[(91,176),(91,24),(95,19),(223,21),(225,25),(225,176)],c('metal',4))
    for x,y in [(92,29),(92,82),(227,31),(227,82)]:bevel(d,(x-3,y-2,x+3,y+3),c('metal',2),c('metal',4),c('metal',0));d.point((x,y),fill=c('metal',5))
    # The gown hangs from the same wooden hanger; the neckline is visibly empty.
    path(d,[(157,25),(160,20),(161,16),(159,14),(157,16)],c('brass',2),2)
    path(d,[(133,40),(154,29),(160,28),(180,40)],c('wood',2),3)
    path(d,[(134,39),(154,28),(159,27),(179,39)],c('wood',3))
    d.line([(136,41),(178,41)],fill=c('wood',1))

def gown(d,im):
    # Layered B2-13 identity, re-illustrated on this scene's native grid.
    edge=[(154,80),(160,80),(174,91),(186,106),(198,126),(211,147),(227,168),(225,174),(208,178),(187,179),(168,181),(146,180),(126,181),(105,178),(86,178),(69,174),(66,170),(79,149),(95,127),(112,108),(129,94),(146,83),(154,80)]
    poly(d,curve(edge,3),c('cloth',3))
    for pts,ws,shade in [([(153,84),(139,105),(127,132),(110,156),(94,174)],[12,20,20],2), ([(159,85),(166,110),(182,143),(204,175)],[9,15,17],2), ([(166,89),(181,113),(200,145),(219,171)],[7,12,13],1)]:ribbon(d,pts,ws,c('cloth',shade))
    for pts,ws,shade in [([(151,86),(137,109),(125,137),(114,162),(111,176)],[3,9,11,5],5), ([(155,86),(151,114),(147,144),(146,178)],[3,7,11],4), ([(158,87),(161,117),(169,150),(181,178)],[3,8,9],5), ([(162,89),(172,116),(188,147),(209,174)],[3,6,8],4), ([(146,91),(126,119),(107,148),(82,173)],[4,9,8],5)]:
        ribbon(d,pts,ws,c('cloth',shade));path(d,[(x-1,y)for x,y in pts],c('cloth',6))
    for pts in [[(151,100),(140,128),(134,157),(132,177)],[(157,99),(156,127),(159,155),(165,178)],[(138,108),(121,135),(105,164)]]:path(d,pts,c('cloth',2),2)
    # Distinct asymmetric heavy swags, with grouped lace rather than all-over noise.
    swags=[([(150,86),(138,99),(121,109),(111,109)],[3,7,5]), ([(143,102),(127,121),(108,132),(97,130)],[3,8,5]), ([(134,124),(117,143),(96,153),(84,150)],[3,9,6]), ([(120,146),(102,164),(82,170),(74,167)],[3,9,6]), ([(162,88),(175,99),(188,116)],[3,6,2]), ([(180,130),(197,142),(208,158)],[3,7,4])]
    for pts,ws in swags:
        ribbon(d,[(x,y+3)for x,y in pts],[w+2 for w in ws],c('cloth',1));ribbon(d,pts,ws,c('cloth',5));path(d,[(x-1,y-1)for x,y in pts],c('cloth',6))
        cp=curve(pts)
        for f in [.25,.49,.72,.93]:
            x,y=cp[round((len(cp)-1)*f)];d.line([(x-2,y+1),(x-1,y+3),(x+1,y+3),(x+2,y+1)],fill=c('cloth',6));d.point((x,y+1),fill=c('cloth',2))
    path(d,[(69,172),(87,176),(105,176),(126,179),(146,178),(168,179),(188,177),(207,176),(225,172)],c('cloth',5),2)
    for x,y in [(82,176),(99,177),(120,179),(141,180),(165,180),(187,179),(209,177)]:d.line([(x-2,y-1),(x,y+1),(x+2,y)],fill=c('cloth',6))
    for x,y in [(125,151),(146,163),(177,161),(199,168)]:d.line([(x-2,y),(x,y-2),(x+1,y),(x+3,y+1)],fill=c('cloth',5))
    # Absurdly cinched EMPTY bodice: waist only four pixels, no body or mannequin.
    bodice=[(140,45),(151,48),(159,49),(173,44),(170,55),(163,66),(159,75),(160,80),(157,84),(153,80),(154,74),(150,65),(144,55),(140,45)]
    poly(d,curve(bodice,3),c('cloth',4))
    ribbon(d,[(143,48),(149,60),(154,73),(155,80)],[4,3,1],c('cloth',2))
    path(d,[(148,49),(152,61),(155,73),(156,80)],c('cloth',6),2)
    path(d,[(168,48),(163,60),(158,73),(158,80)],c('cloth',5),2)
    path(d,[(154,50),(156,62),(157,75)],c('cloth',3))
    path(d,[(139,43),(151,46),(160,47),(173,42)],c('cloth',1),2)
    path(d,[(139,42),(151,45),(160,46),(173,41)],c('cloth',6))
    # Shoulder lace rosettes / cutwork preserve the established sleeveless identity.
    for pts in [[(133,38),(140,40),(144,46),(139,50),(135,48),(131,51),(126,47),(125,43),(133,38)],[(174,38),(182,39),(189,44),(185,49),(180,47),(177,51),(171,47),(174,38)]]:
        poly(d,pts,c('cloth',3));path(d,pts,c('cloth',5))
    for x,y in [(132,43),(139,45),(178,43),(184,45)]:d.line([(x-2,y),(x,y-2),(x+2,y),(x,y+2),(x-2,y)],fill=c('cloth',6));d.point((x,y),fill=c('cloth',1))
    # Small settled cable / brass fitting only, not a new machinery diagram.
    d.rectangle((157,77,159,81),fill=c('brass',2));path(d,[(160,80),(165,91),(177,94),(179,90),(162,82)],c('brass',2));path(d,[(160,80),(165,90),(176,93)],c('brass',4))

def rack_feet(d,im):
    # Four casters on one ordinary rail stand, no extra clothing rack.
    for x,y in [(88,181),(224,177),(102,188),(211,187)]:
        d.ellipse((x-4,y-1,x+4,y+7),fill=c('metal',0));d.ellipse((x-2,y,x+3,y+5),fill=c('metal',2));d.point((x,y+2),fill=c('metal',4))
        d.rectangle((x-1,y-4,x+1,y+1),fill=c('metal',3))
    poly(d,[(77,176),(221,174),(231,179),(103,185),(75,180)],c('metal',0))
    poly(d,[(76,175),(221,173),(229,177),(103,182),(76,178)],c('metal',3))
    d.line([(76,175),(103,180),(228,176)],fill=c('metal',5));d.line([(102,181),(102,184)],fill=c('metal',1))

def bridal_shoe(d,im):
    d.ellipse((165,194,210,203),fill=c('velvet',1));shoe(d,169,194,.81)

def main():
    for n in ['native','previews','layers','masks','evidence']:(ROOT/n).mkdir(parents=True,exist_ok=True)
    a=Painting('CH4-NEW-14');a.add('restroom-context',occupancy_room);a.add('raised-empty-stall',lifted_stall,'one raised empty stall / four cables');a.add('broken-porcelain',broken_toilet,'one broken floor-level toilet and porcelain fragments');a.add('fallen-auction-tags',auction_tags,'three administrative auction tags');a.save('final-occupancy')
    a=Painting('CH4-NEW-15');a.add('quiet-wall',quiet_suit_wall);a.add('single-wire-hanger',wire_hanger,'exactly one ordinary wire clothes hanger');a.add('matching-trousers',trousers,'one pair of matching trousers on the same hanger');a.add('empty-tuxedo-jacket',tuxedo,'one empty tuxedo jacket on the same hanger');a.add('steam-wisps',steam,'three restrained wisps of steam');a.save('pressed-and-steamed')
    a=Painting('CH4-NEW-16');a.add('ordered-auction-room',case_room);a.add('compact-metal-case',compact_case,'one ordinary briefcase-sized metal case / slight two-pixel asymmetric lid bulge');a.add('single-loose-shoe',case_shoe,'exactly one loose dress shoe');a.save('folded-for-convenience')
    a=Painting('CH4-NEW-17');a.add('bridal-room-context',bridal_room);a.add('empty-stand-and-hanger',rack_back,'one wheeled B2-13 dressing stand / wooden hanger');a.add('cinched-empty-gown',gown,'one unworn cinched white AutoFit gown');a.add('stand-base-and-casters',rack_feet,'base of the same stand / four casters');a.add('single-abandoned-shoe',bridal_shoe,'exactly one abandoned dress shoe');a.save('made-to-measure')
    (ROOT/'evidence/native-layer-recipes.json').write_text(json.dumps(RECIPES,indent=2)+'\n');(ROOT/'evidence/material-ramps.json').write_text(json.dumps(P,indent=2)+'\n');(ROOT/'evidence/authored-semantic-inventory.json').write_text(json.dumps(INVENTORY,indent=2)+'\n')
    print(json.dumps({'status':'UNSELECTED','assets':[{'file':str(p.relative_to(ROOT)),'sha256':sha(p),'colours':len(Image.open(p).getcolors(314*206))}for p in sorted((ROOT/'native').glob('*.png'))]}))
if __name__=='__main__':main()
