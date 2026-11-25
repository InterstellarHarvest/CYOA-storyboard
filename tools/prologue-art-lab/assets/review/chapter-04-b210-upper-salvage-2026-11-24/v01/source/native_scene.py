"""CH4-NEW-03: explicit pixel painting on a blank314x206 grid.

The detailed illustration is a visual reference only. This builder reads no
source/reference raster, samples no source pixels and uses no resized base.
All forms, silhouettes, cluster paths, lettering and material ramps below are
authored at the actual target grid. Provenance remains SOURCE-DERIVED because
the composition/material study informed this interpretation.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib

ROOT=Path(__file__).resolve().parents[1]
SIZE=(314,206)
P={
 'ink':'#223732','void':'#182b28','dark':'#30423b',
 'g0':'#2f4740','g1':'#405d50','g2':'#5b7965','g3':'#829477','g4':'#a3b296',
 's0':'#344440','s1':'#536661','s2':'#788a80','s3':'#a5b3a1','s4':'#d0d6b7',
 'steel':'#687a73','joint':'#414f49',
 'wall0':'#777c68','wall1':'#a39e82','wall2':'#c5b998','wall3':'#dfcc9e',
 'chip0':'#6e6351','chip1':'#947e5b','chip2':'#b79762',
 'red0':'#78594c','red1':'#aa7a58',
 'floor0':'#505b51','floor1':'#737a71','floor2':'#8a9181','floor3':'#b3ad8c','floorWarm':'#989d87',
 'porc0':'#7d8270','porc1':'#aaa88e','porc2':'#cec8a8','porc3':'#e3d9b5','porc4':'#f9edcc','porcMid':'#bdb69b','porcEdge':'#e9dfbd',
 'tan0':'#62533c','tan1':'#90734a','tan2':'#b18e56','tan3':'#d3b16c',
 'brass0':'#716443','brass1':'#ae965a','brass2':'#d7bb76',
 'light0':'#bdba8b','light1':'#e7d6a0','light2':'#fff1cb',
 'mirror0':'#415955','mirror1':'#7d9990','mirror2':'#b6c7ae','mirror3':'#dee1be',
 'green':'#79aa54','greenlight':'#c2d391','amber':'#d3a856','red':'#ac6449',
}

def color(c):return P.get(c,c)
def blank():return Image.new('RGBA',SIZE)
def poly(d,pts,c):d.polygon(pts,fill=color(c))
def line(d,pts,c,w=1):d.line(pts,fill=color(c),width=w)
def rect(d,box,c):d.rectangle(box,fill=color(c))
def ellipse(d,box,c):d.ellipse(box,fill=color(c))
def bolt(d,x,y,light=True):
    rect(d,(x,y,x+1,y+1),'s0');d.point((x,y),fill=color('s4'if light else's2'))
def pipe(d,pts,width=5):
    line(d,pts,'s0',width+2);line(d,pts,'s2',width)
    line(d,[(x-1,y-1)for x,y in pts],'s3',max(1,width//3))
def box3(d,x,y,w,h,depth=4):
    poly(d,[(x,y),(x+w,y-2),(x+w+depth,y),(x+depth,y+3)],'tan3')
    poly(d,[(x,y),(x+w,y-2),(x+w,y+h),(x,y+h+2)],'tan1')
    poly(d,[(x+w,y-2),(x+w+depth,y),(x+w+depth,y+h-1),(x+w,y+h)],'tan0')
    line(d,[(x+1,y+4),(x+w-1,y+2)],'tan2');line(d,[(x+2,y+h-3),(x+w-1,y+h-4)],'tan0')

def structure():
    im=blank();d=ImageDraw.Draw(im)
    rect(d,(0,0,313,205),'wall1')
    poly(d,[(0,0),(314,0),(314,35),(0,22)],'s0')
    poly(d,[(0,23),(151,32),(314,28),(314,139),(0,152)],'wall1')
    poly(d,[(0,24),(28,29),(29,145),(0,155)],'wall2')
    poly(d,[(29,34),(202,37),(204,105),(30,111)],'wall2')
    poly(d,[(203,35),(313,30),(313,140),(204,144)],'wall0')
    poly(d,[(0,113),(28,111),(28,149),(0,157)],'g1')
    poly(d,[(30,107),(203,105),(204,138),(29,149)],'g1')
    poly(d,[(204,105),(314,104),(314,144),(204,140)],'g0')
    line(d,[(0,112),(29,109),(202,104)],'g3',2)
    line(d,[(0,116),(28,113),(201,108)],'g0')
    # Plaster losses follow joints, a leaking conduit and lower paint edges.
    for pts,c in [
      ([(2,57),(7,54),(8,48),(13,48),(16,53),(15,58),(20,60),(19,67),(14,66),(11,72),(6,71)],'chip1'),
      ([(15,82),(19,79),(22,80),(24,86),(22,90),(25,94),(22,98),(17,96),(16,90),(12,88)],'red0'),
      ([(131,72),(136,69),(140,72),(145,70),(151,74),(151,79),(147,78),(144,82),(137,80),(136,76)],'chip1'),
      ([(181,70),(186,66),(188,70),(191,69),(195,73),(194,78),(200,80),(198,86),(191,85),(191,80),(185,79)],'red0'),
      ([(135,103),(139,100),(144,102),(149,100),(151,104),(150,109),(142,108),(140,112),(134,112)],'chip0'),
      ([(194,128),(199,124),(204,125),(204,137),(198,136)],'chip1'),
    ]:poly(d,pts,c)
    line(d,[(133,48),(134,58),(131,64),(134,71)],'chip0')
    line(d,[(193,51),(190,57),(193,61),(190,67)],'chip1')
    # Ceiling joists and thin conduit, with attached brackets rather than grain.
    for x in [18,102,184,273]:
        poly(d,[(x,0),(x+7,0),(x+31,31),(x+25,34)],'s1')
        line(d,[(x+1,0),(x+26,32)],'s2')
    rect(d,(26,7,313,13),'g0');rect(d,(26,7,313,8),'g3')
    rect(d,(26,14,313,15),'ink')
    for x in [64,126,192,251,301]:bolt(d,x,9)
    line(d,[(1,13),(1,66),(4,69)],'s0',4);line(d,[(1,13),(1,65),(5,69)],'s3')
    for y in [22,45,64]:rect(d,(0,y,3,y+2),'s1');d.point((1,y),fill=color('s4'))
    # Left wall grille shares its perspective, no tiny invented prose.
    poly(d,[(8,29),(22,34),(22,61),(8,56)],'s0')
    poly(d,[(9,30),(21,34),(21,59),(9,55)],'s2')
    for y in range(34,54,4):line(d,[(11,y),(19,y+2)],'ink',2);line(d,[(11,y-1),(19,y+1)],'s3')
    # Joint-directed plaster flakes and dimensional paint edges.
    for pts,c in [([(136,70),(140,72),(142,71),(145,74),(141,76),(137,75)],'wall3'),([(187,69),(190,70),(190,75),(194,77),(193,79),(188,77)],'wall0'),([(16,82),(19,81),(21,84),(19,87),(17,86)],'wall3'),([(193,130),(196,128),(199,129),(200,133),(197,133)],'g3')]:poly(d,pts,c)
    for pts in [[(134,80),(133,84),(136,87)],[(186,80),(184,86),(186,90)],[(11,67),(9,73),(11,76)]]:line(d,pts,'chip1')
    # Two narrow repair seams stop at structural joints.
    line(d,[(153,50),(153,61)],'wall0');line(d,[(154,51),(154,60)],'wall3')
    line(d,[(143,83),(142,87),(143,90)],'chip1')
    # Ceiling hardware, contact shadows and small paint loss attached to beams.
    for x in [45,89,148,225,288]:
        rect(d,(x,8,x+3,13),'s0');bolt(d,x+1,9)
        poly(d,[(x+8,8),(x+12,8),(x+11,10),(x+7,10)],'chip2')
    return im

def floor():
    im=blank();d=ImageDraw.Draw(im)
    poly(d,[(0,151),(201,127),(314,139),(314,206),(0,206)],'floor1')
    poly(d,[(0,151),(83,141),(96,146),(52,206),(0,206)],'floor0')
    poly(d,[(117,137),(173,131),(191,206),(65,206)],'floor2')
    # Sparse worklight reflections remain within this metal floor, in quiet
    # connected groups. Straight panel seams share a coherent floor plane.
    for pts in [
        [(151,136),(161,136),(160,142),(149,143)],
        [(147,148),(161,147),(163,152),(146,154)],
        [(145,159),(165,158),(166,164),(143,166)],
        [(140,173),(168,171),(169,179),(137,181)],
        [(133,190),(171,187),(173,195),(129,198)],
    ]:poly(d,pts,'floorWarm')
    for pts in [[(151,138),(158,138)],[(149,150),(160,149)],[(147,161),(163,160)],[(143,175),(163,173)],[(137,193),(169,190)]]:line(d,pts,'floor3')
    for pts in [[(0,165),(314,151)],[(0,190),(314,172)],[(60,206),(143,132)],[(205,206),(178,131)]]:
        line(d,pts,'floor0');line(d,[(x,y+1)for x,y in pts],'floor2')
    for x,y in [(78,161),(108,181),(92,195),(206,169),(211,188),(139,134),(177,144)]:bolt(d,x,y,False)
    for pts in [[(111,153),(117,152),(120,154),(116,156),(110,155)],[(180,188),(189,186),(195,188),(191,190),(182,190)],[(95,201),(101,200),(105,202),(102,203)]]:poly(d,pts,'floor0')
    for pts in [[(98,171),(104,170),(107,171),(103,172)],[(182,153),(186,152),(189,153),(184,154)],[(115,192),(120,191),(123,192),(119,193)]]:poly(d,pts,'floorWarm')
    return im

def lift():
    im=blank();d=ImageDraw.Draw(im)
    # Recessed steel lift mouth; independent target-grid perspective and jambs.
    poly(d,[(33,45),(128,45),(128,126),(33,133)],'ink')
    poly(d,[(36,48),(124,48),(124,123),(36,130)],'g1')
    poly(d,[(38,55),(117,55),(117,121),(38,126)],'s0')
    poly(d,[(48,60),(106,60),(106,117),(48,122)],'s1')
    poly(d,[(50,62),(104,62),(104,115),(50,120)],'steel')
    poly(d,[(50,62),(60,66),(60,115),(50,120)],'s2')
    poly(d,[(97,63),(104,62),(104,115),(96,115)],'s0')
    line(d,[(60,66),(96,65),(96,115),(60,115),(60,66)],'joint')
    line(d,[(74,66),(74,114)],'s1');line(d,[(87,65),(87,115)],'s2')
    # Empty lift cabin's handrail, sill and grating; never a toilet cubicle.
    line(d,[(50,94),(62,91),(104,91)],'s0',4)
    line(d,[(50,93),(62,90),(104,90)],'s3')
    poly(d,[(49,119),(104,115),(115,121),(42,126)],'s0')
    for y in [119,121,123]:line(d,[(49,y),(103,y-3)],'s2')
    for x in range(52,106,6):line(d,[(x,117),(x-4,125)],'s1')
    poly(d,[(38,55),(48,58),(48,121),(38,127)],'s3')
    poly(d,[(40,57),(45,59),(45,119),(40,123)],'s2')
    poly(d,[(106,57),(117,55),(117,121),(106,122)],'s2')
    line(d,[(107,58),(107,120)],'s4');line(d,[(116,56),(116,121)],'s0',2)
    for x,y in [(43,93),(111,92)]:rect(d,(x,y,x+3,y+12),'s0');line(d,[(x+1,y+1),(x+1,y+10)],'s3')
    rect(d,(32,45,129,51),'g0');rect(d,(33,45,129,46),'g3')
    for x in [36,75,122]:bolt(d,x,48)
    line(d,[(33,51),(33,131)],'g2',2);line(d,[(127,51),(127,125)],'g2',2)
    for pts in [[(34,69),(36,66),(37,67),(36,73),(34,73)],[(121,118),(124,116),(125,120),(121,121)],[(70,46),(74,46),(76,48),(72,49)]]:poly(d,pts,'chip2')
    poly(d,[(32,131),(128,124),(130,127),(32,135)],'s0')
    line(d,[(33,132),(128,125)],'s4');line(d,[(34,134),(128,127)],'s1')
    # Cabin light casts localized illumination; small finite shade groups.
    poly(d,[(58,61),(93,61),(96,65),(56,65)],'s0')
    rect(d,(60,62,92,63),'light2')
    # Cabin molding, rear fasteners and satin steel groups with restrained wear.
    for xx in [62,76,91]:
        bolt(d,xx,69,False);bolt(d,xx,109,False)
    line(d,[(51,65),(51,90)],'s3');line(d,[(53,67),(53,88)],'s2')
    poly(d,[(62,68),(65,68),(65,82),(63,85),(62,79)],'s2')
    poly(d,[(89,96),(92,96),(92,108),(90,107)],'s0')
    line(d,[(108,61),(108,86)],'s3');line(d,[(112,62),(112,83)],'s1')
    line(d,[(108,99),(108,117)],'s3')
    for xx,yy in [(40,61),(40,117),(113,59),(113,117)]:bolt(d,xx,yy)
    poly(d,[(37,119),(39,117),(40,117),(39,121),(37,122)],'chip1')
    line(d,[(51,116),(102,113)],'s0')
    return im

GLYPHS={
 'W':['10001','10001','10001','10101','10101','11011','10001'],
 'C':['01110','10000','10000','10000','10000','10000','01110'],
 '.':['00','00','00','00','00','11','11']}
def panel():
    im=blank();d=ImageDraw.Draw(im)
    # Back wall is frontal, so this native bitmap lettering shares its plane.
    rect(d,(118,69,140,106),'ink');rect(d,(119,70,139,105),'brass0')
    rect(d,(120,71,138,104),'porc3');line(d,[(120,71),(137,71)],'porc4')
    x=121;y=73;glyphs=[]
    for char in 'W.C.':
        matrix=GLYPHS[char];coords=[]
        for yy,row in enumerate(matrix):
            for xx,bit in enumerate(row):
                if bit=='1':d.point((x+xx,y+yy),fill=color('ink'));coords.append([x+xx,y+yy])
        glyphs.append({'character':char,'pixels':coords});x+=len(matrix[0])+1
    for yy,c in [(87,'green'),(94,'amber'),(101,'red')]:
        ellipse(d,(126,yy-2,132,yy+3),'s0');ellipse(d,(127,yy-1,131,yy+2),c);d.point((128,yy-1),fill=color('porc4'))
    return im,glyphs

def hatch():
    im=blank();d=ImageDraw.Draw(im)
    rect(d,(145,86,190,121),'s0');rect(d,(147,88,187,118),'void')
    rect(d,(148,90,184,115),'ink')
    line(d,[(150,90),(184,90)],'s1');line(d,[(150,91),(150,115)],'s0',2)
    # Pipework is on the far internal wall; preserve a dark crawl gap above it.
    pipe(d,[(152,110),(177,110),(181,106),(181,94)],4)
    for x in [158,172]:rect(d,(x,107,x+2,112),'s0');line(d,[(x,107),(x,111)],'s3')
    line(d,[(161,94),(161,105)],'s1',2);rect(d,(158,103,164,106),'s0')
    # Hinged leaf swung open, with clear thickness/hinges and latch edge.
    poly(d,[(190,89),(205,83),(205,119),(190,116)],'s0')
    poly(d,[(192,90),(203,86),(203,116),(192,114)],'s2')
    poly(d,[(194,94),(201,90),(201,113),(194,111)],'wall0')
    line(d,[(192,91),(192,114)],'s3');line(d,[(203,86),(203,117)],'s1')
    for y in [92,111]:rect(d,(189,y,192,y+3),'s3');d.point((190,y+1),fill=color('s0'))
    line(d,[(200,100),(200,107),(201,107)],'s0',2);d.point((200,100),fill=color('s4'))
    line(d,[(145,121),(190,121)],'s3',2);line(d,[(146,123),(189,123)],'s0')
    for x in [147,185]:bolt(d,x,87)
    for y in [91,117]:bolt(d,146,y)
    poly(d,[(197,95),(199,94),(200,97),(198,99),(196,98)],'chip1')
    # Native small pipe collars, curved elbow highlight, back-wall shadows.
    rect(d,(154,108,156,111),'joint');line(d,[(154,108),(154,111)],'s3')
    rect(d,(170,108,172,112),'s0');line(d,[(170,108),(170,111)],'s3')
    line(d,[(178,107),(180,105),(180,95)],'s4')
    line(d,[(153,109),(167,109)],'s3')
    poly(d,[(195,91),(200,89),(201,92),(197,93)],'s3')
    line(d,[(193,112),(200,114)],'s1')
    return im

def overhead():
    im=blank();d=ImageDraw.Draw(im)
    # Native rounded elbow and cylinder: nested connected bands follow the form.
    pts=[(38,-8),(38,12),(40,20),(45,26),(53,30),(63,32),(139,38),(146,42),(151,47),(158,48),(217,48)]
    line(d,[(x,y+2)for x,y in pts],'ink',19)
    d.line(pts,fill=color('s0'),width=18,joint='curve')
    d.line([(x-1,y-1)for x,y in pts],fill=color('s2'),width=14,joint='curve')
    d.line([(x-2,y-3)for x,y in pts],fill=color('s3'),width=7,joint='curve')
    d.line([(x-3,y-4)for x,y in pts],fill=color('s4'),width=2,joint='curve')
    # Reflection-band shape turns through the bend, not broad procedural shading.
    poly(d,[(31,7),(34,7),(35,16),(39,23),(44,27),(42,29),(37,26),(33,18)],'s3')
    for pts2 in [[(64,31),(75,32)],[(88,33),(103,34)],[(116,36),(127,37)],[(168,46),(182,46)],[(199,46),(210,46)]]:line(d,pts2,'s4')
    for x,y in [(57,29),(82,31),(112,33),(137,35),(164,44),(194,44)]:
        poly(d,[(x,y-3),(x+3,y-2),(x+2,y+10),(x-1,y+9)],'s0')
        line(d,[(x,y-2),(x,y+8)],'s3');bolt(d,x,y-1)
    for pts in [[(78,36),(81,35),(82,37),(80,38)],[(121,38),(125,38),(126,40),(121,40)]]:poly(d,pts,'brass0')
    # Worklight housings, cast recess, cream tube and hanging attachments.
    for x,y,w in [(119,15,81),(262,22,42)]:
        for xx in [x+7,x+w-6]:line(d,[(xx,0),(xx,y)],'ink',2);line(d,[(xx+1,0),(xx+1,y)],'s2')
        poly(d,[(x,y),(x+w,y),(x+w+2,y+4),(x+1,y+5)],'s0')
        line(d,[(x,y),(x+w,y)],'s3')
        rect(d,(x+3,y+2,x+w-2,y+4),'light1');line(d,[(x+5,y+2),(x+w-4,y+2)],'light2')
    # Small caged worklight above hatch; local halo consists of stepped shapes.
    # Place it on the wall layer as the cage itself is attached with a conduit.
    line(d,[(140,55),(140,65),(160,65),(160,68)],'s0',3)
    line(d,[(140,55),(140,65),(160,65),(160,68)],'s2')
    ellipse(d,(158,65,174,74),'brass0');ellipse(d,(160,66,173,72),'light1')
    line(d,[(161,66),(161,72)],'brass1');line(d,[(166,66),(166,72)],'brass1');line(d,[(171,66),(171,71)],'brass0')
    return im

def mirror(d,x,y,w,h,lean=3):
    poly(d,[(x,y+2),(x+w,y),(x+w+lean,y+h),(x+lean,y+h+2)],'tan0')
    poly(d,[(x+1,y+3),(x+w-1,y+1),(x+w+lean-1,y+h-1),(x+lean+1,y+h+1)],'brass1')
    poly(d,[(x+3,y+5),(x+w-3,y+3),(x+w+lean-3,y+h-3),(x+lean+3,y+h-1)],'mirror0')
    poly(d,[(x+4,y+6),(x+w-4,y+4),(x+w+lean-4,y+h-4),(x+lean+4,y+h-2)],'mirror1')
    poly(d,[(x+4,y+h//2),(x+w-4,y+h//2-11),(x+w-3,y+h//2-4),(x+5,y+h//2+7)],'mirror3')
    line(d,[(x+4,y+h-9),(x+w-3,y+h-19)],'mirror2',2)
    line(d,[(x+3,y+5),(x+w-3,y+3)],'porc3')
    poly(d,[(x+4,y+8),(x+7,y+8),(x+10,y+h-4),(x+7,y+h-3)],'mirror0')
    line(d,[(x+5,y+13),(x+w-4,y+10)],'mirror2')
    line(d,[(x+6,y+h//2+6),(x+w-4,y+h//2-3)],'mirror1')
    # One credible edge chip, no all-over sparkling texture.
    poly(d,[(x+w-3,y+13),(x+w-1,y+11),(x+w,y+15),(x+w-2,y+16)],'s0')

def basin(d,x,y,w,h):
    # Hand-constructed convex porcelain wall, broad oval concavity and raised
    # back rim. Highlight/shadow clusters turn around the bowl rather than
    # flattening it to a rectangular icon or a pure outline.
    poly(d,[(x,y+3),(x+3,y+1),(x+w-5,y),(x+w-1,y+3),(x+w,y+7),(x+w-3,y+h-3),(x+w-8,y+h),(x+7,y+h+1),(x+2,y+h-2)],'porc0')
    poly(d,[(x+2,y+4),(x+6,y+2),(x+w-6,y+1),(x+w-2,y+4),(x+w-2,y+9),(x+w-5,y+h-4),(x+w-9,y+h-1),(x+8,y+h),(x+4,y+h-3)],'porc2')
    poly(d,[(x+3,y+4),(x+6,y+2),(x+w-7,y+1),(x+w-3,y+4),(x+w-4,y+8),(x+w-8,y+10),(x+7,y+11),(x+3,y+8)],'porc4')
    # Source-informed light model, but every curve/cluster is native geometry.
    poly(d,[(x+6,y+6),(x+w-7,y+5),(x+w-5,y+8),(x+w-8,y+h-8),(x+w-12,y+h-6),(x+10,y+h-5),(x+6,y+h-8)],'porc0')
    poly(d,[(x+8,y+7),(x+w-8,y+6),(x+w-7,y+9),(x+w-10,y+h-8),(x+w-13,y+h-7),(x+11,y+h-6),(x+8,y+h-9)],'porcMid')
    poly(d,[(x+10,y+9),(x+w-10,y+8),(x+w-10,y+h-10),(x+w-14,y+h-8),(x+13,y+h-7),(x+10,y+h-9)],'porc3')
    line(d,[(x+5,y+7),(x+6,y+h-8),(x+10,y+h-5),(x+w-12,y+h-6)],'porcEdge')
    # Rim thickness, front-belly volume, a side shadow and a small worn edge.
    poly(d,[(x+4,y+h-5),(x+9,y+h-2),(x+w-10,y+h-3),(x+w-5,y+h-6),(x+w-6,y+h-3),(x+w-11,y+h),(x+8,y+h+1),(x+4,y+h-2)],'porcMid')
    line(d,[(x+6,y+h-3),(x+10,y+h-1),(x+w-12,y+h-2)],'porc3')
    line(d,[(x+3,y+3),(x+5,y+2),(x+w-7,y+1)],'porcEdge')
    for xx in [x+w//2-5,x+w//2,x+w//2+5]:
        ellipse(d,(xx,y+2,xx+2,y+4),'porc0');ellipse(d,(xx+1,y+2,xx+2,y+3),'s0')
    xx=x+w//2;yy=y+h-9;ellipse(d,(xx-1,yy-1,xx+3,yy+2),'porc0');ellipse(d,(xx,yy,xx+2,yy+1),'s0');d.point((xx-1,yy),fill=color('porcEdge'))
    poly(d,[(x+w-4,y+9),(x+w-3,y+7),(x+w-1,y+7),(x+w-2,y+10)],'porcMid')

def storage():
    im=blank();d=ImageDraw.Draw(im)
    # Right storage rack is behind the stair opening; its feet stay on the deck.
    rect(d,(212,47,313,137),'g0')
    for x in [212,308]:rect(d,(x,46,x+3,139),'s0');line(d,[(x,47),(x,136)],'s3')
    for y in [65,89,118,137]:
        rect(d,(213,y,313,y+3),'s0');line(d,[(214,y),(313,y)],'s3')
        for x in [214,309]:bolt(d,x,y+1)
    # Upper shelf: nested sinks and a loose detached drain elbow.
    basin(d,220,48,28,14);basin(d,222,44,27,14)
    box3(d,257,58,17,7,2)
    pipe(d,[(255,56),(255,48),(260,47),(263,50)],3)
    # Two sideways toilet bowls, visibly disconnected and stored ABOVE floor.
    ellipse(d,(276,47,299,62),'porc0');ellipse(d,(277,47,299,60),'porc3')
    ellipse(d,(280,50,294,57),'porc0');ellipse(d,(282,51,293,55),'porc1')
    poly(d,[(291,57),(299,56),(302,62),(298,65),(292,64)],'porc2')
    ellipse(d,(297,60,302,65),'s0');ellipse(d,(298,61,301,64),'void')
    # Second shelf contains inverted sanitary bowls, no cistern or installed seat.
    poly(d,[(223,72),(228,68),(237,69),(239,75),(233,81),(222,82)],'porc0')
    poly(d,[(224,72),(229,69),(235,70),(237,75),(232,79),(222,80)],'porc3')
    ellipse(d,(227,72,233,77),'porc0');line(d,[(221,83),(238,82)],'porc2',3)
    poly(d,[(247,71),(260,69),(263,74),(258,81),(253,82),(251,86),(245,86),(247,80),(244,75)],'porc1')
    line(d,[(248,71),(258,70),(261,73)],'porc4',2)
    ellipse(d,(263,76,275,86),'porc3');ellipse(d,(266,79,273,84),'porc0');ellipse(d,(267,80,272,83),'void')
    # Stacked partition panels are narrow solid leaves, not an occupied cubicle.
    for x,y,w,h in [(284,69,21,42),(274,83,25,49),(301,42,11,44)]:
        poly(d,[(x,y+2),(x+w,y),(x+w-3,y+h),(x-4,y+h+2)],'s0')
        poly(d,[(x+1,y+3),(x+w-2,y+2),(x+w-5,y+h-2),(x-2,y+h)],'g1')
        line(d,[(x+1,y+4),(x-1,y+h-2)],'g3')
        line(d,[(x+w-2,y+3),(x+w-5,y+h-2)],'g2')
        for yy in [y+9,y+h-8]:rect(d,(x,yy,x+2,yy+3),'s3')
        poly(d,[(x+4,y+h-9),(x+7,y+h-11),(x+9,y+h-8),(x+5,y+h-5)],'chip2')
    # Stored toilet bowl is supported on its side: rounded open rim and loose
    # drain neck, no cistern, floor mounting or usable installed toilet.
    poly(d,[(221,72),(225,69),(234,69),(239,73),(238,79),(234,82),(226,82),(222,79)],'porc0')
    poly(d,[(223,73),(226,70),(234,70),(238,73),(237,78),(233,80),(226,80),(223,77)],'porc2')
    ellipse(d,(222,69,238,77),'porc3');ellipse(d,(225,71,234,76),'porc0');ellipse(d,(226,72,233,75),'porc1')
    line(d,[(224,70),(228,69),(234,70)],'porc4')
    poly(d,[(234,78),(239,77),(243,80),(242,85),(238,86),(236,82)],'porc2')
    ellipse(d,(239,80,244,85),'porc0');ellipse(d,(240,81,243,84),'void')
    line(d,[(224,78),(228,81),(233,81)],'porcMid')
    # Separate convex walls and the return of each rim show disconnected bowls.
    line(d,[(278,48),(282,47),(293,47),(297,49)],'porc4')
    line(d,[(279,57),(284,60),(294,59)],'porc2',2)
    line(d,[(282,52),(284,50),(292,51)],'porcMid')
    line(d,[(224,73),(227,70),(230,70)],'porc4')
    poly(d,[(224,77),(228,79),(234,77),(232,80),(223,81)],'porcMid')
    ellipse(d,(246,69,262,75),'porc2');line(d,[(247,70),(259,69),(262,72)],'porc4')
    poly(d,[(248,75),(252,76),(252,82),(255,84),(249,85),(247,82)],'porcMid')
    line(d,[(249,76),(250,81),(252,83)],'porc3')
    line(d,[(267,79),(270,78),(273,80)],'porc4')
    for pts in [[(218,65),(223,65),(225,67),(218,67)],[(296,89),(301,89),(302,91),(297,91)],[(216,119),(219,117),(220,119),(217,120)]]:poly(d,pts,'chip2')
    mirror(d,225,96,17,35,1);mirror(d,246,103,13,29,2)
    return im

def foreground_storage():
    im=blank();d=ImageDraw.Draw(im)
    # Leaning panels/mirrors keep salvaged fixtures physically detached.
    for pts,c in [([(0,77),(22,80),(29,169),(0,171)],'s0'),([(0,79),(20,82),(26,166),(0,169)],'g1'),([(4,91),(27,90),(39,172),(12,176)],'s0'),([(6,93),(25,92),(36,170),(14,173)],'g2')]:poly(d,pts,c)
    line(d,[(1,80),(19,83),(25,165)],'g3')
    for x,y in [(1,92),(13,117),(20,151)]:rect(d,(x,y,x+3,y+3),'s3');d.point((x+1,y+1),fill=color('s0'))
    mirror(d,18,104,20,62,9);mirror(d,9,121,12,53,5)
    # Pallet lies on the mezzanine, with slat thickness and its own cast shadow.
    poly(d,[(0,183),(86,172),(94,179),(83,198),(0,203)],'floor0')
    poly(d,[(1,177),(77,169),(89,175),(12,185)],'tan2')
    poly(d,[(12,185),(89,175),(85,189),(11,200)],'tan0')
    poly(d,[(1,177),(12,185),(11,200),(0,192)],'tan1')
    for y,x in [(181,7),(188,11),(196,11)]:line(d,[(x,y),(86,y-10)],'tan2',2)
    for x in [15,35,56,76]:line(d,[(x,176-(x//9)),(x+8,182-(x//9))],'tan0')
    for x,y in [(16,186),(40,184),(67,179)]:rect(d,(x,y,x+9,y+5),'tan0');line(d,[(x,y),(x+8,y-1)],'tan3')
    # Nested dismantled sinks: deliberately different profiles/depth and drains.
    basin(d,28,153,50,25);basin(d,32,139,39,25)
    pipe(d,[(18,171),(18,161),(22,160)],4)
    ellipse(d,(22,170,29,176),'s2');ellipse(d,(24,171,28,175),'void');line(d,[(24,171),(28,171)],'s4')
    # Ground contact and a chipped ceramic edge, not arbitrary surface noise.
    poly(d,[(73,171),(76,167),(78,167),(77,172)],'porc0')
    return im

def stairs():
    im=blank();d=ImageDraw.Draw(im)
    # Open cut in the floor, BELOW deck level. Near risers get wider and darker.
    poly(d,[(217,144),(313,138),(313,205),(243,205)],'void')
    poly(d,[(219,147),(232,153),(253,205),(243,205)],'wall0')
    poly(d,[(304,143),(313,140),(313,205),(307,205)],'g0')
    for pts in [
        [(225,154),(306,147),(312,151),(229,159)],
        [(230,164),(313,156),(313,161),(234,170)],
        [(235,175),(313,166),(313,172),(240,181)],
        [(241,187),(313,177),(313,184),(247,194)],
        [(248,201),(313,190),(313,198),(251,205)],
    ]:
        poly(d,pts,'s2');line(d,[pts[0],pts[1]],'s4');line(d,[pts[3],pts[2]],'s0',2)
        line(d,[(pts[0][0]+2,pts[0][1]+2),(pts[1][0]-2,pts[1][1]+2)],'brass1')
        for j in range(6,70,7):
            xx=pts[0][0]+j
            if xx<311:line(d,[(xx,pts[0][1]-j//10+2),(xx+3,pts[0][1]-j//10+2)],'s1')
    line(d,[(215,144),(240,205)],'s0',3);line(d,[(217,144),(243,205)],'g2',2)
    line(d,[(218,146),(242,205)],'brass1')
    return im

def railings():
    im=blank();d=ImageDraw.Draw(im)
    # Railing at shelf-side edge, then a handrail follows the downward stair run.
    pipe(d,[(205,111),(313,109)],3)
    pipe(d,[(205,111),(226,133)],3)
    for x,y,foot in [(205,112,147),(253,111,143),(309,110,140),(226,133,202)]:
        poly(d,[(x-3,foot),(x+3,foot-1),(x+5,foot+2),(x-2,foot+4)],'s0')
        line(d,[(x-2,foot),(x+3,foot-1)],'s3')
        pipe(d,[(x,y),(x,foot)],3)
    pipe(d,[(206,129),(313,126)],2)
    pipe(d,[(205,111),(227,132),(227,201)],3)
    pipe(d,[(208,139),(227,157)],2)
    # Stair rail beyond the top landing slopes DOWN; no second upper balcony.
    pipe(d,[(238,151),(253,175),(269,203)],2)
    for x,y in [(246,165),(259,187)]:line(d,[(x,y),(x,y+12)],'s2',2)
    return im

def main():
    layers=[('architecture',structure()),('mezzanine-floor',floor()),('descending-stairwell',stairs()),('freight-lift',lift()),('open-maintenance-hatch',hatch()),('storage-racks',storage()),('ceiling-duct-and-lights',overhead()),('foreground-sanitary-salvage',foreground_storage()),('guardrails',railings())]
    panel_layer,glyphs=panel();layers.append(('wc-three-button-panel',panel_layer))
    final=Image.new('RGBA',SIZE)
    order=[]
    for name,im in layers:
        rel=f'layers/{name}.png';im.save(ROOT/rel);im.getchannel('A').save(ROOT/f'masks/{name}.png');final=Image.alpha_composite(final,im);order.append(rel)
    final=final.convert('RGB');out=ROOT/'evidence/internal-study/native-structural-underpainting.png';final.save(out)
    final.resize((1256,824),Image.Resampling.NEAREST).save(ROOT/'evidence/internal-study/native-structural-underpainting-4x.png')
    (ROOT/'evidence/native-assembly.json').write_text(json.dumps({'canvas':[314,206],'initialCanvas':'blank RGBA, no source pixels','layers':order,'compositing':'RGBA source-over; final opaque RGB','output':'evidence/internal-study/native-structural-underpainting.png','sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'palette':P,'sourceDerived':True,'whollyIndependentAuthorshipClaim':False,'noSourceRasterReadOrResamplingInMasterBuilder':True,'noHalfResolutionSampling':True,'noPostSharpening':True,'noRandomTexture':True,'wcLettering':{'text':'W.C.','method':'native bitmap glyphs, no antialiasing','plane':'frontal rear-wall lift panel','glyphs':glyphs,'panelBounds':[118,69,140,106],'threeButtonCenters':[[129,87],[129,94],[129,101]]}},indent=2)+'\n')
    print('Blank-grid native mezzanine master and exact4x constructed; ten editable layers.')

if __name__=='__main__':main()
