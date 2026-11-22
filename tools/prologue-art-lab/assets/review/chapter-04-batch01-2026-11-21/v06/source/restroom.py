"""CH4-04 v02: independently reconstructed at 314x206; no raster inputs.

The Stage-A architectural study informs forms/materials, not source pixels.
The study's extra basin is corrected to three. Entry/pre-flood state only.
"""
from pathlib import Path
from scene_tools import Canvas,project,floor,duct,pipe,sconce

ROOT=Path(__file__).resolve().parent.parent

def main():
 c=Canvas();vp=(185,88)
 # Camera: (VP 185,88), focal 220, eye 1.6, ceiling 3m, back z7.
 # Left-wall longitudinal joints and the floor rays share this vanishing point.
 c.poly([(0,0),(314,0),(308,44),(110,44)],'#a8a992')
 c.poly([(0,0),(110,44),(110,138),(0,212)],'#d3cdb0')
 c.poly([(0,0),(29,11),(29,192),(0,211)],'#c6c3a8')
 c.poly([(30,12),(72,29),(72,164),(30,192)],'#e2d8b9')
 c.poly([(73,30),(109,44),(109,139),(73,163)],'#ccc6ab')
 c.poly([(308,44),(314,32),(314,152),(308,138)],'#b7bba2')
 c.box((110,44,308,139),'#c9c5a9')
 for x0 in [-100,-26,43,112,184,256,330,404]:
  xb=round(185+(x0-185)*(88-44)/88)
  c.line([(x0,0),(xb,44)],'#7f8c7d');c.line([(x0+1,0),(xb+1,44)],'#c6c9ad')
 for yy in [16,31,43]:
  c.line([(0,yy),(110,round(88+(yy-88)*(185-110)/185)),(308,round(88+(yy-88)*(185-110)/185))],'#858e7b')
 c.line([(109,44),(308,44)],'#687c6d',2);c.line([(109,46),(308,46)],'#e0d7b6')
 floor(c,vp,(0,212),(110,138),(308,138))
 # Delicate clean reflections near the lamp/basin side; not a glossy marble room.
 for pts,col in [([(43,196),(47,193),(65,196),(62,198)],'#bdc0a8'),([(72,175),(76,174),(87,176),(83,178)],'#c7c7ab'),([(111,157),(114,155),(122,156),(120,157)],'#c4c5aa'),([(274,158),(282,158),(286,187),(280,186)],'#bcc2a9')]:c.poly(pts,col)
 # Back tile joints and left-wall joints are geometrically distinct planes.
 for y in range(50,139,10):
  c.line([(110,y),(308,y)],'#a4aa93');c.line([(111,y+1),(307,y+1)],'#e0d9b9')
 for x in range(111,309,13):c.line([(x,47),(x,138)],'#b3b69c')
 for y in [.35,.65,.95,1.25,1.55,1.85,2.15,2.45,2.75]:
  c.line([project(-2.4,y,2.8),project(-2.4,y,7)],'#aab29b')
 for z in [2.9,3.4,4.0,4.8,5.9,7]:
  c.line([project(-2.4,.2,z),project(-2.4,3,z)],'#b6bda4')
 c.poly([project(-2.4,0,2.9),project(-2.4,0,7),project(-2.4,.44,7),project(-2.4,.44,2.9)],'#65857a')
 for yy in [.1,.3]:c.line([project(-2.4,yy,2.9),project(-2.4,yy,7)],'#819c89')
 c.line([project(-2.4,.46,2.9),project(-2.4,.46,7)],'#c8bd8e',2)
 # Small, meaningful aging: a penetration stain and a replaced tile; fixtures clean.
 c.poly([(124,49),(130,49),(130,56),(128,60),(126,57)],'#b6b395')
 c.line([(127,47),(128,51),(126,54)],'#9da38a')
 c.poly([(3,185),(7,180),(8,184),(7,189),(3,192)],'#8b9983')
 c.poly([(110,112),(119,112),(119,120),(111,121)],'#d9cfb0')
 c.line([(111,111),(120,111),(120,122)],'#b5b49a')
 # Ceiling light boxes recede in size; common cool illumination, warm sconces left.
 for pts in [[(86,5),(158,5),(164,11),(92,11)],[(233,5),(302,5),(299,11),(232,11)],[(145,28),(191,28),(195,32),(149,32)]]:
  c.poly([(x+1,y+2) for x,y in pts],'#6d8072');c.poly(pts,'#526e62','#3f5e51')
  inner=[(pts[0][0]+3,pts[0][1]+1),(pts[1][0]-3,pts[1][1]+1),(pts[2][0]-4,pts[2][1]-1),(pts[3][0]+3,pts[3][1]-1)]
  c.poly(inner,'#fff1c6');c.line([inner[0],inner[1]],'#fff8dc')
 # Hatch corners are projected from the complete nearest-stall footprint at ceiling.
 hatch=[project(1.65,3,5.9),project(3.25,3,5.9),project(3.25,3,7.05),project(1.65,3,7.05)]
 c.poly(hatch,'#667c6d','#3a5548')
 inner=[(hatch[0][0]+3,hatch[0][1]+2),(hatch[1][0]-3,hatch[1][1]+2),(hatch[2][0]-2,hatch[2][1]-1),(hatch[3][0]+2,hatch[3][1]-1)]
 c.poly(inner,'#a8af93','#c8cbb0')
 c.line([(249,37),(298,37)],'#d8d7b8');c.box((265,39,273,41),'#4c6656');c.line([(267,40),(271,40)],'#b5bea0')
 for x,y in [(247,37),(301,37),(285,43),(240,43)]:c.box((x,y,x+1,y),'#d0d5b6')
 # Duct is a physically joined riser, elbow and tapered horizontal run.
 c.box((52,0,72,19),'#425d50');c.box((54,0,70,18),'#97a68f')
 for x,col in [(55,'#c8ceb1'),(58,'#aebba1'),(65,'#7e9680'),(69,'#556e5b')]:c.line([(x,0),(x,18)],col,2)
 c.poly([(53,17),(71,15),(73,22),(78,27),(88,29),(88,45),(77,42),(66,36),(57,28)],'#657e68','#3f5b4b')
 c.poly([(56,18),(67,18),(70,25),(77,31),(86,32),(85,37),(75,35),(65,29),(59,24)],'#b8c0a2')
 c.line([(55,18),(59,25),(66,31),(76,37),(87,39)],'#d2d4b4')
 c.line([(62,18),(65,24),(73,29),(82,31)],'#83977d')
 duct(c,84,30,64,15)
 c.poly([(146,29),(155,32),(155,48),(146,45)],'#687e67','#3c5947')
 for x,y in [(90,28),(129,27)]:
  c.box((x,y-7,x+2,y+20),'#3f5e4b');c.line([(x+2,y-6),(x+2,y+18)],'#a4af90');c.line([(x-2,y-7),(x+5,y-7)],'#657e65',2)
 # Copper run mounted along left upper wall, then down to the bare spindle.
 pipe(c,[(24,0),(24,43),(31,48),(100,75),(102,84),(102,108),(111,111)],3,True)
 pipe(c,[(30,0),(30,37),(35,41),(96,65)],2,True)
 for x,y in [(24,21),(62,60),(102,88)]:c.box((x-2,y,x+2,y+2),'#6f7c63');c.line([(x-1,y),(x+1,y)],'#c8c39f')
 # Long clean mirror, fine worn brass frame, limited reflected architecture.
 frame=[(16,44),(92,69),(92,112),(16,117)]
 c.poly([(x+2,y+2) for x,y in frame],'#8c9178');c.poly(frame,'#87724b','#5a624a')
 c.poly([(19,48),(89,71),(89,109),(19,114)],'#9aaea0','#e2cc94')
 c.poly([(22,52),(87,74),(87,85),(22,70)],'#bcc9b7')
 c.poly([(22,72),(87,87),(87,106),(22,111)],'#79978a')
 for pts in [[(36,66),(36,110)],[(61,74),(61,108)],[(22,83),(87,93)],[(22,107),(87,103)]]:c.line(pts,'#5e8071')
 c.line([(21,50),(87,72)],'#e7d8ab');c.line([(19,114),(88,109)],'#bdb486')
 # Mirror reflections are flat, muted panels, not additional physical stalls.
 c.poly([(37,83),(57,88),(57,107),(37,109)],'#55796b','#466c5f');c.line([(39,86),(55,90),(55,105)],'#829b83')
 sconce(c,7,65);sconce(c,98,87,True)
 # Cabinet is distinct, reachable, above the rear basin and keyed.
 c.box((112,76,139,105),'#614b43','#4a5140');c.box((114,78,137,103),'#7b5149')
 c.line([(115,79),(136,79),(136,102)],'#aa7560');c.box((116,81,135,87),'#ded0a1','#a8986d')
 # Explicit tiny 3x5 letter clusters; full label remains in canonical requirements.
 glyph={'I':['111','010','010','010','111'],'S':['111','100','111','001','111'],'O':['111','101','101','101','111'],'L':['100','100','100','100','111'],'A':['010','101','111','101','101'],'T':['111','010','010','010','010'],'E':['111','100','110','100','111']}
 for i,ch in enumerate('ISOLATE'):
  for yy,row in enumerate(glyph[ch]):
   for xx,v in enumerate(row):
    if v=='1':c.box((114+i*3+xx,82+yy,114+i*3+xx,82+yy),'#4a4836')
 c.ellipse((125,92,128,95),'#dec08a','#6c6445');c.box((126,94,127,97),'#4f523d')
 c.box((109,111,114,115),'#6a6951','#455d4c');c.line([(111,109),(111,116)],'#c9b384',2)
 c.box((111,108,113,110),'#d5c69b') # Bare shaft, deliberately no wheel.
 c.box((122,111,140,139),'#607e6a','#3f5f4d');c.box((124,113,138,137),'#9aab90')
 c.line([(125,114),(137,114),(137,136)],'#c8c7a5');c.box((134,122,135,126),'#435d49');c.line([(135,123),(135,125)],'#c7c5a2')
 # Sink-side plumbing: three individual traps and feed lines, not a crowded knot.
 for x,y,w in [(22,132,39),(63,122,31),(96,115,24)]:
  cx=x+w//2
  pipe(c,[(cx,y+10),(cx,y+20),(cx+5,y+23),(cx+9,y+20),(cx+9,y+10)],2)
  c.line([(cx+2,y+12),(cx+2,y+19),(cx+5,y+20)],'#d1d2b5')
  c.box((cx-2,y+9,cx+2,y+11),'#a7b498','#536e59')
 pipe(c,[(6,162),(107,138),(107,128)],3)
 # Three basins: rim, concave bowl, thick front apron, curved porcelain volume.
 for x,y,w in [(8,132,49),(52,122,38),(88,115,30)]:
  c.ellipse((x-1,y+7,x+w+2,y+18),'#718574')
  c.poly([(x,y+1),(x+w,y-2),(x+w-2,y+10),(x+w*.75,y+15),(x+w*.28,y+16),(x+2,y+11)],'#d5d5b9','#6f8571')
  c.poly([(x+2,y+4),(x+w-1,y+1),(x+w-3,y+8),(x+w*.74,y+12),(x+w*.3,y+12)],'#eee8cb')
  c.ellipse((x,y-4,x+w,y+6),'#f5efd6','#9aab93')
  c.ellipse((x+5,y-2,x+w-5,y+3),'#b8c8b3','#d2d8bd')
  c.line([(x+8,y),(x+w-8,y-1)],'#8fae9b')
  c.box((x+w//2,y+1,x+w//2+1,y+1),'#6b8b74')
  c.line([(x+3,y+6),(x+8,y+11),(x+w*.7,y+11)],'#fff3d6')
  cx=x+w//2
  c.line([(cx,y-5),(cx,y-10),(cx+3,y-12),(cx+6,y-10),(cx+6,y-7)],'#4b6953',3)
  c.line([(cx,y-5),(cx,y-10),(cx+3,y-11),(cx+5,y-9)],'#c9c8a5')
  for xx in [cx-10,cx+11]:c.box((xx-1,y-6,xx+1,y-4),'#7c957b');c.line([(xx-2,y-7),(xx+2,y-7)],'#dbd4af')
 # Fresh towels are folded, edged, softly shadowed and kept separate from taps.
 for x,y,w in [(8,121,19),(111,105,12)]:
  for dy in [0,-3,-6]:
   c.box((x,y+dy,x+w,y+dy+2),'#ece8cf','#b9c4a8');c.line([(x+2,y+dy),(x+w-1,y+dy)],'#fff2d5')
 # Stall modules: exact three bays; far two closed, nearest visibly open.
 c.poly([(145,142),(302,142),(304,149),(145,149)],'#526f5d')
 c.line([(146,147),(301,147)],'#a8b59a')
 # Recessed nearest cubicle and a side panel behind its frame establish depth.
 c.box((251,72,300,141),'#6a806b')
 c.poly([(251,73),(242,79),(242,137),(251,143)],'#a7b69b','#657e67')
 c.poly([(251,73),(300,73),(290,81),(242,81)],'#9aa78c')
 c.poly([(242,81),(290,81),(290,136),(242,137)],'#d1cfaf')
 for yy in [91,101,111,121,132]:c.line([(243,yy),(290,yy)],'#b1b79a')
 for xx in [247,259,271,283]:c.line([(xx,82),(xx,136)],'#bbc1a3')
 c.poly([(243,137),(290,136),(300,144),(251,144)],'#aab69b')
 c.line([(259,139),(291,138)],'#c5caab')
 # Seat, tank, bowl and pedestal are separately shaded porcelain forms.
 pipe(c,[(264,105),(260,108),(260,132),(269,133)],2)
 c.box((266,104,286,118),'#d9ddc0','#6d8b72')
 c.box((265,102,287,105),'#f7f0d3','#a3b397')
 c.poly([(268,106),(282,106),(282,116),(269,116)],'#f1ebcf')
 c.line([(285,106),(285,116)],'#b8c9ad');c.box((282,107,285,109),'#8ca38b')
 # Upright toilet lid behind the ring: a recognizable actual toilet, not a pedestal.
 c.ellipse((270,115,283,126),'#ece8cd','#9fb59a');c.ellipse((273,118,281,124),'#d3ddc1')
 c.poly([(271,131),(284,131),(281,139),(283,142),(269,142),(273,137)],'#e0e4c8','#809a7e')
 c.poly([(274,132),(281,132),(278,139),(280,141),(273,141)],'#f5edd2')
 c.ellipse((265,125,289,135),'#f8efd5','#9aaf92');c.ellipse((268,126,286,131),'#a4bba1')
 c.ellipse((271,126,283,129),'#4c7661');c.line([(268,132),(276,134),(284,132)],'#ced9b9')
 # Two closed doors: panel depth, worn lower paint and restrained metal hardware.
 for x in [146,198]:
  c.box((x,70,x+50,143),'#344f45','#304b3e')
  c.box((x+3,73,x+47,139),'#4b6b5d');c.box((x+7,79,x+42,135),'#527467','#2f5548')
  c.line([(x+8,80),(x+41,80),(x+41,134)],'#819983');c.line([(x+7,135),(x+7,80)],'#3e6151')
  c.line([(x+3,74),(x+45,74)],'#a1ad90');c.line([(x+4,138),(x+44,138)],'#384f42')
  c.poly([(x+10,83),(x+23,83),(x+27,111),(x+23,131),(x+11,131)],'#57796b')
  c.poly([(x+31,84),(x+40,84),(x+40,131),(x+34,131)],'#4a6c5e')
  c.line([(x+11,85),(x+11,129)],'#638574')
  for yy in [81,126]:c.box((x+1,yy,x+3,yy+5),'#a69c70','#5b7052');c.line([(x+2,yy),(x+2,yy+4)],'#d1bf87')
  c.box((x+38,112,x+42,115),'#8b8e60');c.line([(x+33,113),(x+41,113)],'#ddc58b',2)
  c.box((x+4,140,x+44,144),'#263f34')
  for dx,dy in [(10,132),(33,136)]:c.line([(x+dx,dy),(x+dx+3,dy-1)],'#78917a')
 # Posts and top rails form an intelligible complete removable enclosure.
 for x in [143,195,247,300]:
  c.box((x,65,x+4,146),'#405f4c','#304f3e');c.line([(x+1,68),(x+1,144)],'#95a78a')
  c.box((x-1,64,x+5,67),'#baa97b','#5e7656');c.line([(x,64),(x+4,64)],'#e0ce96')
  c.box((x-1,142,x+5,147),'#9f956b','#557450')
 c.box((144,69,302,73),'#3b5c49','#2c4c3b');c.line([(146,70),(300,70)],'#b9bda0')
 c.poly([(304,69),(313,60),(313,140),(304,146)],'#385e4c','#2a4d3b')
 c.line([(306,73),(311,68),(311,136)],'#8da486');c.line([(306,141),(310,138)],'#63846a')
 c.box((308,109,310,113),'#b8aa71');c.line([(306,111),(311,110)],'#dfc58c')
 # Native scene background only; separately illustrated NPCs are composited
 # by scene_people.py, with explicit source-derived provenance.
 c.save(ROOT/'backgrounds/CH4-04-restroom-background-v02.png')

if __name__=='__main__':main()
