"""Explicit local target-grid artwork corrections; never overwrite selected sources."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import json, hashlib, shutil
R=Path(__file__).resolve().parent;V1=R.parent/'v01';V2=R.parent/'v02-localized-corrections'
for d in ['candidates','previews','masks','layers','sources','comparisons','composites']:(R/d).mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def im(p):return Image.open(p).convert('RGBA')
def write(p,d):(R/p).write_text(json.dumps(d,indent=2)+'\n')
def blank(size):return Image.new('RGBA',size)
def mask(size,points):
 m=Image.new('L',size);ImageDraw.Draw(m).polygon(points,fill=255);return m
def cut(source,points):
 a=source.copy();a.putalpha(mask(a.size,points));return a
def put(base,layer):base.alpha_composite(layer)
def poly(base,points,color):ImageDraw.Draw(base).polygon(points,fill=color)
main=im(V1/'references/A04-verification.png');close=im(V1/'references/A05-verification-bg.png')
u=im(V1/'donors/CH3-C01-urgency-native-donor.png');uc=im(V1/'donors/CH3-C02-urgency-bg-native-donor.png');s=im(V1/'donors/CH3-C04-surprise-native-donor.png')
old=json.loads((V2/'manifest.json').read_text());oldids={c['candidateId']:c for c in old['candidates']}
base={i:im(V2/c['file']) for i,c in oldids.items() if c['kind']!='foreground'}
base['CH3-A04-verification-continuity']=main.copy();base['CH3-A05-verification-bg-continuity']=close.copy()
work={i:a.copy() for i,a in base.items()};allowed={i:Image.new('L',a.size) for i,a in base.items()}
ops={i:[] for i in base};phases=[]
def record(ident,label,fn):
 a=work[ident];before=a.copy();limit=Image.new('L',a.size);ld=ImageDraw.Draw(limit)
 if label.startswith('New continuity option'):
  boxes=[(201,70,264,144),(264,58,277,133)]
 elif label.startswith('New independent-close'):
  boxes=[(389,64,475,224),(465,34,496,278),(496,28,564,278),(420,222,564,278)]
 elif label.startswith('Urgency fabric'):
  boxes=[]
  ld.polygon([(64,62),(126,69),(201,69),(232,64),(266,61),(266,139),(104,139),(99,137),(79,138),(64,139)] if a.width==314 else [(124,58),(235,61),(389,62),(467,41),(475,220),(394,220),(194,201),(124,211)],fill=255)
 elif label.startswith('Lower the bell'):boxes=[(109,99,117,113)]
 elif label.startswith('Restore the complete'):boxes=[(74,87,117,155)]
 elif label.startswith('Remove the remaining'):boxes=[(99,111,112,130)]
 elif label.startswith('Connect the net'):boxes=[(128,111,135,136),(215,111,222,136),(131,115,150,122),(200,115,219,122),(133,128,144,135),(206,128,217,135)]
 elif label.startswith('Composite the existing'):
  boxes=[];limit=front.getchannel('A').copy();ld=ImageDraw.Draw(limit)
 elif label.startswith('Shared right-wall'):boxes=[(277,50,314,134)] if a.width==314 else [(496,28,564,193)]
 elif label.startswith('Mount the existing'):boxes=[(220,131,245,163)] if a.width==314 else [(420,190,462,255)]
 else:raise ValueError(label)
 for x0,y0,x1,y1 in boxes:ld.rectangle((x0,y0,x1-1,y1-1),fill=255)
 fn(a)
 changed=ImageChops.difference(before,a).convert('RGB').point(lambda v:255 if v else 0).convert('L')
 # RGB difference channels can differ only in one channel; explicit boolean mask.
 pts=[]
 for y in range(a.height):
  for x in range(a.width):
   if before.getpixel((x,y))!=a.getpixel((x,y)):
    assert limit.getpixel((x,y)),(ident,label,x,y)
    pts.append([x,y])
 allowed[ident]=ImageChops.lighter(allowed[ident],limit)
 ops[ident].append(label);phases.append({'candidateId':ident,'operation':label,'changedPixels':len(pts),'coordinates':pts})

# Construct independent main/close reveal masters for the two NEW A04/A05
# continuity candidates. This never rewrites the approved A04/A05 originals.
def default_reveal(a):
 src=u if a.width==314 else uc
 boxes=[(201,70,264,144),(264,58,277,133)] if a.width==314 else [(389,64,465,224),(465,34,496,278),(496,28,564,278),(420,222,564,278)]
 for box in boxes:a.paste(src.crop(box),box[:2])
 ap=Image.open(V1/('masks/common-curtain-opening-main.png' if a.width==314 else 'masks/common-curtain-opening-close.png')).convert('L')
 box=(201,70,264,138) if a.width==314 else (389,64,475,218)
 for y in range(box[1],box[3]):
  for x in range(box[0],box[2]):
   r,g,b,alpha=a.getpixel((x,y))
   if not ap.getpixel((x,y)) and r>g+8 and r>b+15:
    a.putpixel((x,y),(round(r*.40+10),round(r*.50+30),round(r*.47+31),255))
record('CH3-A04-verification-continuity','New continuity option only: same curtain opening and genuine restroom reveal; teal fabric. Approved A04 source untouched.',default_reveal)
record('CH3-A05-verification-bg-continuity','New independent-close continuity option only: matching curtain opening, restroom, side chair and floor. Approved A05 source untouched.',default_reveal)

# Curtain material-only mask. Navy costume, skin/hair, camera, display, rods,
# microphone, architecture and aperture interior are excluded explicitly.
person_points=[(83,87),(90,87),(94,90),(95,94),(97,96),(96,100),(93,103),(95,106),(99,111),(103,112),(107,107),(109,104),(113,103),(116,105),(116,109),(109,112),(106,116),(100,121),(99,129),(98,137),(96,139),(95,146),(101,148),(103,151),(98,153),(91,152),(89,148),(88,148),(92,151),(89,153),(80,152),(77,150),(80,145),(80,138),(78,136),(77,128),(76,125),(76,113),(78,106),(76,104),(74,100),(75,94),(78,90)]
person=cut(main,person_points)
for y in range(87,154):
 for x in range(74,117):
  rr,gg,bb,aa=person.getpixel((x,y))
  if aa and gg>rr+12 and gg>bb+2:person.putpixel((x,y),(0,0,0,0))
  if aa and x>=100 and y>=112 and max(rr,gg,bb)-min(rr,gg,bb)<80 and rr>=gg-7:person.putpixel((x,y),(0,0,0,0))
person.save(R/'layers/locomotion-presenter-original-silhouette.png')
def urgency_red(a):
 if a.width==314:
  area=mask(a.size,[(64,62),(126,69),(201,69),(232,64),(266,61),(266,139),(104,139),(99,137),(79,138),(64,139)])
  blocked=[(128,66,196,124),(0,98,65,138)]
  microphone=mask(a.size,[(102,111),(106,111),(109,114),(110,118),(109,123),(107,126),(107,146),(112,149),(110,152),(101,152),(99,149),(104,146),(104,126),(100,122),(99,115)])
  spec=json.loads((V2/'sources/bell-edit-spec.json').read_text())
  bell_pixels={(left+dx,int(y)) for y,(left,row) in spec['rows'].items() for dx in range(len(row))}
 else:
  area=mask(a.size,[(124,58),(235,61),(389,62),(467,41),(475,220),(394,220),(194,201),(124,211)])
  blocked=[(228,56,355,167)]
  camera=mask(a.size,[(124,136),(135,139),(147,145),(149,151),(149,173),(140,183),(124,185)])
  microphone=mask(a.size,[(180,143),(185,143),(190,146),(192,151),(192,168),(188,177),(185,181),(185,221),(181,221),(181,181),(177,178),(174,173),(173,148),(175,145)])
 aperture=Image.open(V1/('masks/common-curtain-opening-main.png' if a.width==314 else 'masks/common-curtain-opening-close.png')).convert('L')
 for y in range(a.height):
  for x in range(a.width):
   if not area.getpixel((x,y)) or aperture.getpixel((x,y)):continue
   if any(x0<=x<x1 and y0<=y<y1 for x0,y0,x1,y1 in blocked):continue
   r,g,b,alpha=a.getpixel((x,y))
   if a.width==314 and (person.getpixel((x,y))[3] or (x,y) in bell_pixels):continue
   if a.width!=314 and camera.getpixel((x,y)):continue
   if microphone.getpixel((x,y)) and (max(r,g,b)-min(r,g,b)<28 or r>=g):continue
   if g>r+6:
    a.putpixel((x,y),(min(245,round(g*1.35+15)),max(32,round(g*.65-10)),max(27,round(g*.43)),255))
for ident in ['CH3-C01-urgency','CH3-C02-urgency-bg']:
 record(ident,'Urgency fabric only: extend the scripted red curtain material across the full curtain assembly; no mixed blue/red fabric.',urgency_red)

# Bell: preserve the hand, move the discrete seven-pixel-wide bell three
# native rows down, and restore its old footprint from same-column fabric.
def lower_bell(a):
 spec=json.loads((V2/'sources/bell-edit-spec.json').read_text());hand={tuple(p) for p in spec['protectedHandPixels']}
 pixels=[]
 for sy,(left,row) in spec['rows'].items():
  y=int(sy)
  for dx,c in enumerate(row):
   p=(left+dx,y)
   if p not in hand:pixels.append((p,tuple(spec['palette'][c])+(255,)))
 for (x,y),c in pixels:a.putpixel((x,y),a.getpixel((x,96)))
 # Preserve all original finger pixels; they naturally overlap the handle.
 for (x,y),c in pixels:
  if (x,y+3) not in hand:a.putpixel((x,y+3),c)
 for p in hand:assert a.getpixel(p)==base['CH3-C01-urgency'].getpixel(p)
record('CH3-C01-urgency','Lower the bell 3 logical pixels into the existing fingers; hand pixels unchanged.',lower_bell)

# The complete approved silhouette above is reused for the foreground.
def locomotive_person(a):
 # Clean old above-belt outline with exact neighboring curtain pixels; new
 # silhouette is translated exactly +1y and composited in front of the belt.
 visible=person.copy()
 for y in range(87,130):
  for x in range(74,117):
   if visible.getpixel((x,y))[3]:a.putpixel((x,y),main.getpixel((x,80)) if y<127 else main.getpixel((70,y)))
 # Use same-column unobstructed curtain column, retaining its fold tone.
 for y in range(87,127):
  for x in range(74,117):
   if visible.getpixel((x,y))[3]:
    tone=main.getpixel((x,80));cols=list(range(65,74))+list(range(118,127))
    sx=min(cols,key=lambda q:sum((main.getpixel((q,80))[k]-tone[k])**2 for k in range(3)))
    a.putpixel((x,y),main.getpixel((sx,y)))
 a.alpha_composite(person,(0,1))
def remove_mic(a):
 # Only the visible upper microphone remains in v02; the lower stand was
 # already covered by the belt. Leave all belt casing and floor pixels alone.
 p=mask(a.size,[(102,111),(106,111),(109,114),(110,118),(109,123),(107,126),(107,129),(103,129),(103,126),(100,122),(99,115)])
 for y in range(111,130):
  for x in range(99,112):
   if p.getpixel((x,y)):a.putpixel((x,y),main.getpixel((112,y)))
record('CH3-C03-locomotion','Remove the remaining microphone from locomotion; repair only its visible curtain footprint above the conveyor.',remove_mic)
record('CH3-C03-locomotion','Restore the complete approved small presenter one native pixel lower, in front of the conveyor; feet rest on the stage rim instead of being cut off.',locomotive_person)
def net_support(a):
 d=ImageDraw.Draw(a)
 for x in [131,218]:
  d.line((x,113,x,134),fill='#42575d',width=3)
  d.line((x,113,x,133),fill='#aeb8ad',width=1)
  d.rectangle((x-3,134,x+3,135),fill='#52666a')
  d.point((x-2,134),fill='#d0d0b4');d.point((x+2,134),fill='#d0d0b4')
  d.rectangle((x-1,113,x+1,115),fill='#d5ceb0')
 # Connected upper corners, and explicit lower straps to fixed rim anchors.
 d.line([(131,116),(132,116),(149,120)],fill='#e4d5aa')
 d.line([(201,120),(217,116),(218,116)],fill='#e4d5aa')
 d.line([(143,128),(137,132),(134,134)],fill='#d9cba5')
 d.line([(206,128),(212,132),(215,134)],fill='#d9cba5')
 d.rectangle((133,133,135,134),fill='#b9c0af');d.rectangle((214,133,216,134),fill='#b9c0af')
record('CH3-C03-locomotion','Connect the net to two continuous metal uprights, bolted feet and lower rim straps; no floating endpoints.',net_support)

# Put the SAME source-derived performer in front of the cannon: no face,
# costume, scale or anchor changes. Her silhouette is the top occlusion layer.
surprise_points=[(73,87),(79,87),(83,89),(84,92),(86,96),(86,101),(84,104),(87,107),(88,104),(89,101),(92,98),(95,99),(96,102),(95,107),(93,110),(94,118),(93,126),(92,133),(90,138),(89,146),(91,149),(91,152),(88,153),(84,152),(82,148),(82,138),(81,138),(80,147),(83,150),(82,153),(77,153),(74,151),(73,148),(74,141),(74,135),(70,132),(69,127),(68,120),(67,117),(68,110),(68,106),(67,102),(68,96),(70,92)]
performer=cut(s,surprise_points);front=blank(main.size);front.alpha_composite(performer,(115,-28));front.save(R/'layers/surprise-presenter-front.png')
record('CH3-C04-surprise','Composite the existing small presenter silhouette in front of the cannon; preserve her identity, anchor and scale.',lambda a:put(a,front))

# Devices share one wall plane. Source pixels are shifted by column only,
# no scene or portrait is resized. Faces follow the existing upward-right
# wall line rather than reading as front-facing rectangles pasted onto it.
def wall_master(kind):
 source=base['CH3-C01-urgency'] if kind=='main' else base['CH3-C02-urgency-bg']
 out=source.copy()
 if kind=='main':
  crop=(277,50,314,134);devices=[(279,68,304,97),(279,99,299,123),(279,122,298,134)];sx=278;origin=279;slope=.23
 else:
  crop=(496,28,564,193);devices=[(499,43,554,111),(509,113,542,174),(510,175,543,193)];sx=555;origin=499;slope=.23
 # Same-row wall repairs keep original architectural paint/lighting intact.
 for box in devices:
  for y in range(box[1],box[3]):
   for x in range(box[0],box[2]):out.putpixel((x,y),source.getpixel((sx,y)))
 for box in devices:
  for y in range(box[1],box[3]):
   for x in range(box[0],box[2]):
    yy=y-round((x-origin)*slope)
    out.putpixel((x,yy),source.getpixel((x,y)))
 return out,crop
wm,mbox=wall_master('main');wc,cbox=wall_master('close')
wm.crop(mbox).save(R/'layers/main-right-wall-master.png');wc.crop(cbox).save(R/'layers/close-right-wall-master.png')
for ident,a in work.items():
 master,box=(wm,mbox) if a.width==314 else (wc,cbox)
 record(ident,'Shared right-wall pictogram, three buttons and separate PA grille follow one upward-right wall plane; identical across matching camera views.',lambda a,src=master,b=box:a.paste(src.crop(b),b[:2]))

# Pedestal: native existing control head translated upward, supported by a
# newly authored stem/base. Physical placement agrees in independent cameras.
def pedestal(a,active):
 ismain=a.width==314
 oldcomponent=im(V1/f'layers/CH3-C0{4 if active else 1}-{("surprise" if active else "urgency")}-matched-console.png') if ismain else im(V1/f'layers/CH3-C0{5 if active else 2}-{("surprise-bg" if active else "urgency-bg")}-matched-console.png')
 oldxy=(220,151) if ismain else (420,225)
 # New A05's old large corner console was removed by default_reveal already.
 floor=main if ismain else uc
 for y in range(oldcomponent.height):
  for x in range(oldcomponent.width):
   if oldcomponent.getpixel((x,y))[3]:a.putpixel((oldxy[0]+x,oldxy[1]+y),floor.getpixel((oldxy[0]+x,oldxy[1]+y)))
 d=ImageDraw.Draw(a)
 if ismain:
  d.polygon([(228,139),(239,139),(239,157),(228,157)],fill='#526a70')
  d.line([(229,140),(229,156)],fill='#94a6a0');d.line([(239,140),(239,157)],fill='#354d55')
  d.polygon([(227,157),(240,157),(243,160),(224,160)],fill='#3b535c')
  d.line((225,160,242,160),fill='#c3b69a')
  xy=(220,131)
 else:
  d.polygon([(433,205),(454,205),(454,249),(433,249)],fill='#526a70')
  d.line([(435,208),(435,248)],fill='#94a6a0',width=2);d.line([(453,208),(453,249)],fill='#354d55',width=2)
  d.polygon([(432,248),(454,248),(461,253),(425,253)],fill='#3b535c')
  d.line((427,253,459,253),fill='#c3b69a',width=2)
  xy=(420,190)
 # Head pixels and existing active-BEGIN state are exact component transfers.
 a.alpha_composite(oldcomponent,xy)
 # Small cover edge on the red emergency-release control, not a new switch.
 d=ImageDraw.Draw(a)
 if ismain:d.line([(239,132),(244,132),(244,136)],fill='#eedcb4')
 else:d.line([(450,192),(459,192),(459,200)],fill='#eedcb4')
for ident,a in work.items():
 active=ident in ['CH3-C04-surprise','CH3-C05-surprise-bg']
 record(ident,'Mount the existing BEGIN/control head on a raised slate-teal pedestal with a visible foot; same physical location and active button in both cameras.',lambda a,active=active:pedestal(a,active))

records=[]
for ident,a in work.items():
 before=base[ident];changes=[];layer=blank(a.size);changed=Image.new('L',a.size)
 for y in range(a.height):
  for x in range(a.width):
   p=(x,y)
   if a.getpixel(p)!=before.getpixel(p):
    assert allowed[ident].getpixel(p)
    changes.append({'x':x,'y':y,'before':list(before.getpixel(p)[:3]),'after':list(a.getpixel(p)[:3])})
    layer.putpixel(p,a.getpixel(p));changed.putpixel(p,255)
 dest=R/'candidates'/f'{ident}-v03.png';a.convert('RGB').save(dest)
 a.convert('RGB').resize((a.width*4,a.height*4),Image.Resampling.NEAREST).save(R/'previews'/f'{ident}-v03-4x.png')
 allowed[ident].save(R/'masks'/f'{ident}-allowed.png');changed.save(R/'masks'/f'{ident}-changed.png');layer.save(R/'layers'/f'{ident}-correction.png')
 write(f'sources/{ident}-changed-pixels.json',{'coordinates':'zero-based native x,y; RGB before/after','pixels':changes})
 src=(V2/oldids[ident]['file']) if ident in oldids else V1/('references/A04-verification.png' if a.width==314 else 'references/A05-verification-bg.png')
 key=oldids[ident]['record'] if ident in oldids else 'scenes:pavilion_reboot/human_verification_stage'+('' if a.width==314 else '#portraitBackground')
 records.append({'candidateId':ident,'record':key,'kind':'main' if a.width==314 else 'background','dimensions':list(a.size),'file':str(dest.relative_to(R)),'sha256':sha(dest),'sourceFile':str(src.relative_to(R.parent)),'sourceSha256':sha(src),'changedPixels':len(changes),'status':'generated','selected':False,'approved':False,'assetPath':None,'operations':ops[ident],'additionalContinuityOption':ident.startswith('CH3-A')})
write('sources/corrections.json',records);write('sources/operation-coordinates.json',phases)
write('sources/layout.json',{'rightWallMainBox':list(mbox),'rightWallCloseBox':list(cbox),'wallPlaneNativeShear':{'main':.23,'close':.23},'mainControlHeadOrigin':[220,131],'closeControlHeadOrigin':[420,190],'greenButton':'Same existing left BEGIN button illuminates only for surprise. Right red control has a cover edge.','urgencyCurtain':'All selected fabric red; no mixed assembly.','net':'Two continuous uprights, bolted feet, top eye connections and lower rim straps.','approvedSources':'v02 selected images and A04/A05 references are immutable. All v03 environment revisions require Nate selection.'})
print(json.dumps({r['candidateId']:{'changedPixels':r['changedPixels'],'sha256':r['sha256']} for r in records},indent=2))
