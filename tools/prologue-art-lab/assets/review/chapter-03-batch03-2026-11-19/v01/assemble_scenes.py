"""Same-room incident states: approved bases + localized native layers only."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,hashlib,math
R=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rgba(p):return Image.open(R/p).convert('RGBA')
def empty(size):return Image.new('RGBA',size)
def poly(im,p,c):ImageDraw.Draw(im).polygon(p,fill=c)
def line(im,p,c,w=1):ImageDraw.Draw(im).line(p,fill=c,width=w)
def rect(im,b,c):ImageDraw.Draw(im).rectangle(b,fill=c)
def maskpoly(size,p):
 m=Image.new('L',size);ImageDraw.Draw(m).polygon(p,fill=255);return m
def cut(im,p):
 out=im.copy();out.putalpha(maskpoly(im.size,p));return out
def shifted(im,x,y):
 out=empty(im.size);out.alpha_composite(im,(x,y));return out

main=rgba('references/A04-verification.png');close=rgba('references/A05-verification-bg.png')
u=rgba('donors/CH3-C01-urgency-native-donor.png');uc=rgba('donors/CH3-C02-urgency-bg-native-donor.png')
l=rgba('donors/CH3-C03-locomotion-native-donor.png');s=rgba('donors/CH3-C04-surprise-native-donor.png');sc=rgba('donors/CH3-C05-surprise-bg-native-donor.png')

def red_curtain(base,donor,box):
 """Native per-pixel fabric selection within a declared incident region.

 Only an explicit fabric area is eligible; panels, clock, people, microphone
 and frame are excluded. New red pixels come from the generated donor.
 This is a scripted material layer, never a global palette/style filter.
 """
 out=empty(base.size);m=Image.new('L',base.size)
 for y in range(box[1],box[3]):
  for x in range(box[0],box[2]):
   # Copy a fixed unobstructed native fabric strip. Changing the sample
   # column at each row would imprint the donor's diagonal opening as bands.
   sx=(192+(x-box[0])%24) if base.width==314 else (350+(x-box[0])%26)
   sy=min(y,124 if base.width==314 else 188)
   out.putpixel((x,y),donor.getpixel((sx,sy)));m.putpixel((x,y),255)
 # Measured native row-run outline of the approved clock assembly. Excluding
 # the physical object avoids a protected-background rectangle or color noise.
 if base.width==314:roi=(128,70,195,121)
 else:roi=(230,63,353,162)
 for y in range(roi[1],roi[3]):
  xs=[x for x in range(roi[0],roi[2]) if (lambda c:c[0]>c[1]+8 and c[0]>c[2]+20 and c[0]>130)(base.getpixel((x,y)))]
  if xs:
   for x in range(min(xs)-1,max(xs)+2):out.putpixel((x,y),(0,0,0,0));m.putpixel((x,y),0)
 return out,m

def restore_platform(layer,base):
 if base.width==314:points=[(126,125),(199,125),(212,129),(219,135),(219,144),(209,149),(120,150),(109,145),(108,137),(113,131)]
 else:points=[(241,190),(350,190),(393,199),(416,213),(419,225),(418,242),(406,253),(375,261),(240,263),(208,255),(186,242),(184,223),(187,213),(207,201)]
 m=maskpoly(base.size,points)
 for y in range(base.height):
  for x in range(base.width):
   if m.getpixel((x,y)):
    c=base.getpixel((x,y))
    # Exclude only exposed teal fabric at the traced upper corners.
    if not(c[1]>c[0]+12):layer.putpixel((x,y),(0,0,0,0))

# URGENCY: red fabric is the one scripted curtain change. All existing static
# doorway/wall devices stay in their approved positions and original pixels.
urgency,um=red_curtain(main,u,(117,70,231,140))
# The owner-selected red reveal is applied as the shared right-side master
# by apply_layout_master.py. Do not invent a second restroom opening here.
restore_platform(urgency,main)
# The silver bell rests in the existing presenting hand; no invented stand.
line(urgency,[(112,99),(112,104)],'#4d5d61')
poly(urgency,[(110,103),(114,103),(116,107),(108,107)],'#c3c8c2')
line(urgency,[(110,104),(113,104),(114,106)],'#eee8d5');line(urgency,[(108,108),(116,108)],'#667478');rect(urgency,(111,108,113,109),'#89908b')
# Painted rotation cue on the original deck, no platform size/camera change.
line(urgency,[(148,132),(153,130),(160,130)],'#c45e42')
poly(urgency,[(158,128),(163,130),(159,133)],'#c45e42')
# Only the visitor is added to the original lone chair; no new wall plaque.
visitor=cut(u,[(280,135),(287,135),(291,138),(293,142),(293,149),(290,153),(289,155),(296,160),(296,167),(285,170),(277,170),(268,172),(263,177),(254,176),(254,172),(261,170),(264,162),(269,158),(275,156),(275,153),(273,150),(273,143),(275,139)])
urgency.alpha_composite(visitor)

# The independent approved closer camera is reused, never a main-scene crop.
urgency_bg,ubm=red_curtain(close,uc,(195,64,433,224))
# Close view uses the same owner-selected right-side reveal master.
restore_platform(urgency_bg,close)
# Native rotation marker on the unchanged close-view deck.
line(urgency_bg,[(352,217),(366,213),(380,213)],'#c25b40',2);poly(urgency_bg,[(376,210),(385,214),(377,217)],'#c25b40')

# LOCOMOTION: new moving belt/padded pit on the same stage. Original clock,
# curtains and doorway stay put; the safety net unfolds in front of them.
locomotion=empty(main.size)
floor=cut(l,[(59,136),(65,131),(72,130),(77,130),(77,128),(136,128),(143,126),(194,127),(211,135),(229,136),(259,136),(263,143),(247,148),(218,153),(135,155),(65,154),(57,151)])
# Preserve the entire approved door opening; new safe landing starts below it.
fd=ImageDraw.Draw(floor);fd.rectangle((231,75,260,135),fill=(0,0,0,0))
locomotion.alpha_composite(floor)
# Remove the unrequested donor's control post from the new belt casing using
# neighboring pixels of that new casing; no approved room pixel is repaired.
for y in range(130,153):
 for x in range(74,80):
  if floor.getpixel((x,y))[3]:locomotion.putpixel((x,y),l.getpixel((84,y)))
# Native net: explicit hard-grid steel joints and a readable coarse rope mesh.
for x in [131,218]:
 rect(locomotion,(x,112,x+1,131),'#687b7d');rect(locomotion,(x-1,111,x+2,114),'#bbc0ac')
rows=[[(132,116),(149,120),(166,122),(184,122),(201,120),(217,116)],[(136,122),(151,126),(166,129),(182,129),(197,126),(213,122)],[(143,128),(155,132),(168,134),(181,134),(192,132),(206,128)]]
for pts in rows:line(locomotion,pts,'#e4d5aa')
for j in range(6):line(locomotion,[row[j] for row in rows],'#d9cba5')
# Two folded chairs, a new object only, beside the original fixed doorway.
chair_src=cut(l,[(217,113),(227,113),(228,117),(231,113),(238,113),(240,117),(240,129),(237,131),(229,130),(227,131),(217,130),(216,121)])
chair_part=chair_src.crop((215,112,241,132)).resize((15,18),Image.Resampling.NEAREST)
# The folded chairs are inside the shared curtain reveal, not a second exit.

# SURPRISE: native lamp-state update inside the original display frame.
surprise=empty(main.size)
display=Image.new('L',main.size);ImageDraw.Draw(display).rounded_rectangle((134,73,183,117),radius=6,fill=255)
face=Image.new('RGBA',main.size,'#284b55');face.putalpha(display);surprise.alpha_composite(face)
dd=ImageDraw.Draw(surprise)
for cx in [149,172]:
 dd.ellipse((cx-6,88,cx+6,100),fill='#918363');dd.ellipse((cx-4,89,cx+4,98),fill='#fff0bd')
# Same approved platform silhouette translated upward; original lower tier is
# retained as its stationary base. No rescaling or auditorium reconstruction.
platform_mask=maskpoly(main.size,[(126,126),(199,126),(209,129),(216,133),(218,137),(216,144),(209,148),(120,148),(111,145),(109,140),(110,134),(116,130)])
platform=main.copy();platform.putalpha(platform_mask);raised=shifted(platform,0,-8);surprise.alpha_composite(raised)
# Source-derived cannon only, with its open support void left transparent.
cannon=cut(s,[(171,108),(174,108),(180,111),(186,113),(190,117),(192,119),(192,123),(190,126),(188,126),(188,132),(191,132),(191,135),(171,135),(171,133),(177,131),(178,124),(173,122),(169,119),(168,114)])
surprise.alpha_composite(shifted(cannon,0,-8))
# Replace the original small presenter only where the scripted lift changes
# her staging. Repair only her traced footprint with approved curtain/floor.
old_person=maskpoly(main.size,[(83,87),(90,87),(94,90),(95,94),(97,96),(96,100),(93,103),(95,106),(99,111),(103,112),(107,107),(109,104),(113,103),(116,105),(116,109),(109,112),(106,116),(100,121),(99,129),(98,137),(96,139),(95,146),(101,148),(103,151),(98,153),(91,152),(89,148),(88,148),(92,151),(89,153),(80,152),(77,150),(80,145),(80,138),(78,136),(77,128),(76,125),(76,113),(78,106),(76,104),(74,100),(75,94),(78,90)])
ImageDraw.Draw(old_person).polygon([(92,105),(103,110),(110,102),(117,103),(117,112),(108,117),(103,123),(95,123)],fill=255)
for yy in range(98,126):
 for xx in range(91,119):
  rr,gg,bb,aa=main.getpixel((xx,yy))
  # Local selection of the old skin/blue-cloth footprint catches its raised
  # fingers and antialiased cuff. Unoccluded teal fabric is left untouched.
  if rr>gg+7 or bb>gg+1 or (gg<105 and rr<80):old_person.putpixel((xx,yy),255)
for y in range(87,154):
 for x in range(74,119):
  if not old_person.getpixel((x,y)):continue
  target=main.getpixel((x,80));options=list(range(65,74))+list(range(197,229))
  sx=min(options,key=lambda q:sum((main.getpixel((q,80))[k]-target[k])**2 for k in range(3)))
  val=main.getpixel((sx,y))
  if y>=127 or val[0]>val[1]+15:val=main.getpixel((70,y))
  surprise.putpixel((x,y),val)
mic_restore=cut(main,[(104,117),(108,117),(110,120),(110,125),(108,127),(108,131),(107,132),(107,146),(111,147),(112,149),(110,151),(102,151),(99,149),(101,147),(104,146),(104,132),(103,131),(103,127),(102,125),(102,120)])
surprise.alpha_composite(mic_restore)
new_person=cut(s,[(73,87),(79,87),(83,89),(84,92),(86,96),(86,101),(84,104),(87,107),(88,104),(89,101),(92,98),(95,99),(96,102),(95,107),(93,110),(94,118),(93,126),(92,133),(90,138),(89,146),(91,149),(91,152),(88,153),(84,152),(82,148),(82,138),(81,138),(80,147),(83,150),(82,153),(77,153),(74,151),(73,148),(74,141),(74,135),(70,132),(69,127),(68,120),(67,117),(68,110),(68,106),(67,102),(68,96),(70,92)])
surprise.alpha_composite(shifted(new_person,115,-28))
# The shared console is placed consistently in all wide states below.

# CLOSE SURPRISE: retain all approved teal curtains and static room equipment.
surprise_bg=empty(close.size)
frame=Image.new('L',close.size);ImageDraw.Draw(frame).rounded_rectangle((241,69,341,156),radius=12,fill=255)
panel=Image.new('RGBA',close.size,'#284b55');panel.putalpha(frame);surprise_bg.alpha_composite(panel)
bd=ImageDraw.Draw(surprise_bg)
for cx in [268,312]:
 bd.ellipse((cx-14,98,cx+14,127),fill='#918363');bd.ellipse((cx-10,100,cx+10,123),fill='#fff0bd')
# Raised platform and its pedestal/floor aperture: explicit incident objects.
group=cut(sc,[(236,177),(355,176),(401,181),(416,188),(417,210),(410,220),(390,227),(391,235),(405,242),(391,251),(363,256),(238,256),(211,251),(195,243),(200,235),(220,228),(218,224),(192,220),(183,211),(183,190),(194,184)])
surprise_bg.alpha_composite(group)
bcannon=cut(sc,[(328,132),(334,133),(369,146),(378,153),(382,160),(381,166),(375,171),(371,170),(371,184),(382,185),(382,192),(335,192),(335,187),(350,184),(350,164),(337,159),(326,155),(322,150),(323,139)])
surprise_bg.alpha_composite(bcannon)
# One exact source polygon defines the same existing button in both cameras.
GREEN_BUTTON=[(484,237),(500,236),(499,245),(483,246)]
poly(surprise_bg,GREEN_BUTTON,'#75af44')

# Explicit source-independent native confetti clusters, fewer and larger than
# high-density texture: only scripted surprise contains them.
colors=['#e86c45','#eee3b4','#90b4a0']
for x,y,c in [(118,82,0),(128,92,1),(203,90,0),(198,109,1),(181,119,2),(155,124,1),(107,91,1),(121,103,2),(213,123,0),(224,144,1),(162,143,2),(194,147,0),(136,151,1),(244,162,0),(174,164,1),(101,155,0)]:
 poly(surprise,[(x,y),(x+3,y-1),(x+4,y+1),(x+1,y+2)],colors[c])
for x,y,c in [(203,85,0),(222,111,1),(366,80,0),(390,110,1),(351,149,1),(315,146,0),(297,162,2),(244,172,0),(280,176,1),(318,182,2),(365,209,0),(421,232,1),(304,262,0),(229,262,2),(410,175,2)]:
 poly(surprise_bg,[(x,y),(x+6,y-3),(x+10,y+1),(x+4,y+5)],colors[c])

# Shared physical right-front console: identical placement in every new wide
# scene. Only the left button lights for surprise, using the exact close-view
# button polygon BEFORE the component's source-derived grid transfer.
for lit in [False,True]:
 source_console=close.copy()
 if lit:poly(source_console,GREEN_BUTTON,'#75af44')
 console=source_console.crop((444,224,564,278)).resize((25,12),Image.Resampling.NEAREST)
 console.putalpha(maskpoly(console.size,[(5,0),(24,0),(24,11),(0,11)]))
 console.save(R/f'layers/common-console-{"active" if lit else "inactive"}-main.png')
 source_console.crop((444,224,564,278)).save(R/f'layers/common-console-{"active" if lit else "inactive"}-close.png')
 for target in ([surprise] if lit else [urgency,locomotion]):target.alpha_composite(console,(220,151))
(R/'sources/shared-stage-layout.json').write_text(json.dumps({'mainAuthority':'references/A04-verification.png','closeAuthority':'references/A05-verification-bg.png','mainConsoleOrigin':[220,151],'mainConsoleSize':[25,12],'closeConsoleCrop':[444,224,564,278],'closeGreenButtonPolygon':GREEN_BUTTON,'sourceComponentTransfer':'Nearest neighbor of the isolated approved console component only; never a scene/background resize. Identical source, mask, scale and placement across main variants.','surpriseChange':'Only the same left button illuminates green in both cameras.','doorway':'Approved original pixels and position unchanged in all five environment candidates.','curtain':'Red inner curtains only for the scripted urgency incident; original outer teal fabric retained. Locomotion and surprise keep approved teal.','wallDevices':'Approved original wall controls/poster/grille retained. Generated bathroom plaques and associated replacement buttons/speakers are excluded.'},indent=2)+'\n')

items=[('CH3-C01-urgency',main,urgency,'references/A04-verification.png'),('CH3-C02-urgency-bg',close,urgency_bg,'references/A05-verification-bg.png'),('CH3-C03-locomotion',main,locomotion,'references/A04-verification.png'),('CH3-C04-surprise',main,surprise,'references/A04-verification.png'),('CH3-C05-surprise-bg',close,surprise_bg,'references/A05-verification-bg.png')]
records=[]
for ident,base,layer,bp in items:
 # Static landmark policy: doorway frames/wall devices never move. Clip only
 # at their physical footprint, not at an unrelated character/background box.
 blocked=[(231,75,260,135),(277,55,305,120)] if base.size==(314,206) else [(465,71,563,218),(432,101,462,170)]
 d=ImageDraw.Draw(layer)
 for box in blocked:d.rectangle(box,fill=(0,0,0,0))
 out=base.copy();out.alpha_composite(layer)
 dest=R/f'candidates/{ident}-v01.png';out.convert('RGB').save(dest)
 lp=f'layers/{ident}-incident.png';layer.save(R/lp);layer.getchannel('A').save(R/f'masks/{ident}-allowed.png')
 changes=[];unexpected=[]
 for y in range(base.height):
  for x in range(base.width):
   if out.getpixel((x,y))!=base.getpixel((x,y)):
    changes.append([x,y])
    if not layer.getpixel((x,y))[3]:unexpected.append([x,y])
 assert not unexpected
 for box in blocked:assert out.crop((box[0],box[1],box[2]+1,box[3]+1)).tobytes()==base.crop((box[0],box[1],box[2]+1,box[3]+1)).tobytes(),(ident,box)
 (R/f'sources/{ident}-changed-coordinates.json').write_text(json.dumps(changes,separators=(',',':'))+'\n')
 out.resize((out.width*4,out.height*4),Image.Resampling.NEAREST).convert('RGB').save(R/f'previews/{ident}-v01-4x.png')
 records.append({'candidateId':ident,'file':str(dest.relative_to(R)),'sha256':sha(dest),'base':bp,'baseSha256':sha(R/bp),'incidentLayer':lp,'incidentLayerSha256':sha(R/lp),'changedPixels':len(changes),'unexpectedChangesOutsideMask':0,'staticLandmarkBoxesExact':blocked,'baseResized':False,'operation':'Approved base plus explicit incident objects/materials. No whole-scene rescaling or global filtering. Local donor cutouts/placement and native pixel edits are defined in assemble_scenes.py.','dimensions':list(out.size),'status':'generated','selected':False,'approved':False,'assetPath':None})
(R/'sources/scene-assembly.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps([{'id':r['candidateId'],'sha256':r['sha256'],'changed':r['changedPixels']} for r in records],indent=2))
