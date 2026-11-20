"""Owner-selected red reveal/right-wall master, with scene-specific reveals.

This supersedes the earlier original-door lock for NEW Batch C candidates.
Approved A04/A05 and every historical artwork byte remain untouched.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,hashlib
R=Path(__file__).resolve().parent
def rgba(p):return Image.open(R/p).convert('RGBA')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blank(size):return Image.new('RGBA',size)
def poly(im,p,c):ImageDraw.Draw(im).polygon(p,fill=c)
def rect(im,b,c):ImageDraw.Draw(im).rectangle(b,fill=c)
def maskpoly(size,p):
 m=Image.new('L',size);ImageDraw.Draw(m).polygon(p,fill=255);return m
u=rgba('donors/CH3-C01-urgency-native-donor.png');uc=rgba('donors/CH3-C02-urgency-bg-native-donor.png')
l=rgba('donors/CH3-C03-locomotion-native-donor.png');s=rgba('donors/CH3-C04-surprise-native-donor.png');sc=rgba('donors/CH3-C05-surprise-bg-native-donor.png')
close=rgba('references/A05-verification-bg.png')
ap_main=maskpoly(u.size,[(236,74),(239,82),(245,91),(250,97),(252,101),(252,135),(223,135),(223,115),(226,105),(230,96),(233,86)])
ap_close=maskpoly(uc.size,[(429,70),(435,83),(442,96),(452,111),(461,123),(462,213),(398,213),(398,145),(405,125),(413,108),(421,90)])
ap_main.save(R/'masks/common-curtain-opening-main.png');ap_close.save(R/'masks/common-curtain-opening-close.png')

def master(kind,blue=False,reveal=None):
 src=u if kind=='main' else uc;out=blank(src.size)
 regions=[(201,70,264,144),(264,58,277,133),(277,50,314,133)] if kind=='main' else [(389,64,465,224),(465,34,496,278),(496,28,564,278),(420,222,564,278)]
 for box in regions:out.paste(src.crop(box),box[:2])
 aperture=ap_main if kind=='main' else ap_close
 # Teal versions retain the SAME curtain aperture/folds. Only the explicitly
 # selected fabric material changes; this never filters a whole scene.
 fabric=(201,70,264,138) if kind=='main' else (389,64,475,218)
 if blue:
  for y in range(fabric[1],fabric[3]):
   for x in range(fabric[0],fabric[2]):
    if aperture.getpixel((x,y)):continue
    r,g,b,a=out.getpixel((x,y))
    if a and r>g+8 and r>b+15:
     out.putpixel((x,y),(round(r*.40+10),round(r*.50+30),round(r*.47+31),255))
 if reveal is not None:
  view=blank(src.size)
  if kind=='main':view.alpha_composite(reveal.resize((31,63),Image.Resampling.NEAREST),(222,74))
  else:view.alpha_composite(reveal.resize((68,143),Image.Resampling.NEAREST),(397,72))
  view.putalpha(ImageChops.multiply(view.getchannel('A'),aperture));out.alpha_composite(view)
 # Use the owner's three-button portrait panel in both scales, not the main
 # donor's unrelated grille. Match order, housing and physical wall location.
 if kind=='main':
  for yy in range(99,123):
   for xx in range(279,298):out.putpixel((xx,yy),u.getpixel((304,yy)))
  panel=uc.crop((512,115,540,172)).resize((10,20),Image.Resampling.NEAREST)
  out.alpha_composite(panel,(282,101))
  speaker=(281,123,294,132)
 else:speaker=(511,176,541,192)
 x0,y0,x1,y1=speaker
 rect(out,speaker,'#c4c4b3');rect(out,(x0+1,y0+1,x1-1,y1-1),'#586b72')
 count=3 if kind=='main' else 4
 for j in range(count):
  yy=y0+2+j*(2 if kind=='main' else 4)
  rect(out,(x0+2,yy,x1-2,yy),'#263e48')
  rect(out,(x0+2,yy+1,x1-2,yy+1),'#819391')
 return out

masters={
'CH3-C01-urgency':master('main'),
'CH3-C02-urgency-bg':master('close'),
'CH3-C03-locomotion':master('main',True,l.crop((213,85,257,140))),
'CH3-C04-surprise':master('main',True,s.crop((229,85,254,141))),
'CH3-C05-surprise-bg':master('close',True,sc.crop((491,85,563,215)))}

def console(active,size):
 src=close.copy()
 if active:poly(src,[(484,237),(500,236),(499,245),(483,246)],'#75af44')
 out=src.crop((444,224,564,278)).resize(size,Image.Resampling.NEAREST)
 out.putalpha(maskpoly(size,[(round(size[0]*.2),0),(size[0]-1,0),(size[0]-1,size[1]-1),(0,size[1]-1)]));return out

records=json.loads((R/'sources/scene-assembly.json').read_text())
for r in records:
 ident=r['candidateId'];before=rgba(r['file']);layer=masters[ident]
 # In the close view the original stage rim remains in front of the reveal.
 # For surprise, the raised incident objects retain their own occlusion.
 old_incident=rgba(r['incidentLayer'])
 if ident=='CH3-C05-surprise-bg':
  # The earlier independent green patch belonged to the former large corner
  # console. It must never be reapplied onto the new shared side chair.
  ImageDraw.Draw(old_incident).rectangle((483,236,501,247),fill=(0,0,0,0))
 if ident=='CH3-C02-urgency-bg':
  # Only the physical original platform is restored, never a background box.
  pm=maskpoly(close.size,[(241,190),(350,190),(393,199),(416,213),(419,225),(418,242),(406,253),(375,261),(240,263),(208,255),(186,242),(184,223),(187,213),(207,201)])
  for y in range(190,264):
   for x in range(184,420):
    c=close.getpixel((x,y))
    if pm.getpixel((x,y)) and not c[1]>c[0]+12:layer.putpixel((x,y),(0,0,0,0))
 out=before.copy();out.alpha_composite(layer)
 if ident in ['CH3-C03-locomotion','CH3-C04-surprise']:
  # New floor, raised performer and confetti are in front of the shared
  # background. Never reintroduce the old fixed doorway behind these objects.
  out.alpha_composite(old_incident)
 elif ident=='CH3-C05-surprise-bg':
  # Only the explicit new raised platform/cannon/confetti matter here. Its
  # door region was transparent in the incident layer.
  out.alpha_composite(old_incident)
 # Green demo console is right-front, between platform and side chair, in
 # both views. This avoids the portrait donor's chair/console collision.
 is_main=out.width==314;active='C04' in ident or 'C05' in ident
 c=console(active,(25,12) if is_main else (40,18));xy=(220,151) if is_main else (420,225)
 out.alpha_composite(c,xy);c.save(R/f'layers/{ident}-matched-console.png')
 # Preserve the SAME wall sign, three-button panel and separate PA grille.
 # Later foreground incident layers may not repaint this fixed wall stack.
 boxes=[(277,50,314,133)] if is_main else [(496,28,564,193)]
 for b in boxes:out.paste(layer.crop(b),b[:2])
 out.convert('RGB').save(R/r['file']);out.resize((out.width*4,out.height*4),Image.Resampling.NEAREST).convert('RGB').save(R/f'previews/{ident}-v01-4x.png')
 # Record one final native replacement layer against the approved source.
 base=rgba(r['base']);final=blank(base.size);coords=[]
 for y in range(base.height):
  for x in range(base.width):
   if out.getpixel((x,y))!=base.getpixel((x,y)):
    final.putpixel((x,y),out.getpixel((x,y)));coords.append([x,y])
 lp=f'layers/{ident}-final-state.png';final.save(R/lp);final.getchannel('A').save(R/f'masks/{ident}-allowed.png')
 (R/f'sources/{ident}-changed-coordinates.json').write_text(json.dumps(coords,separators=(',',':'))+'\n')
 r.update({'sha256':sha(R/r['file']),'incidentLayer':lp,'incidentLayerSha256':sha(R/lp),'changedPixels':len(coords),'staticLandmarkBoxesExact':[],'layoutAuthority':'Owner selected the red curtain reveal and three-button portrait panel; latest direction supersedes original-door preservation for NEW candidates only.','commonRightSideMaster':'donors/CH3-C01-urgency-native-donor.png' if is_main else 'donors/CH3-C02-urgency-bg-native-donor.png','consoleOrigin':list(xy),'consoleSize':list(c.size),'consoleActive':active})
(R/'sources/scene-assembly.json').write_text(json.dumps(records,indent=2)+'\n')
(R/'sources/shared-stage-layout.json').write_text(json.dumps({'ownerLatestReference':'Red urgency main/close reveal, with the portrait three-button panel.','openingMasks':['masks/common-curtain-opening-main.png','masks/common-curtain-opening-close.png'],'mainWallFixedBox':[277,50,314,133],'closeWallFixedBox':[496,28,564,197],'rightWallOrder':'Two-person pictogram, red/cream/teal three-button panel, separate PA grille. Same pixels across event variants in each camera.','speakerAuthority':'Locked human_verification_arrival explicitly describes recorded laughter from a loudspeaker; recorded applause also occurs. Retain a consistent separate grille in every new stage environment.','console':'Same right-front console between platform and side chair; same left button lights green only for surprise. Whole scene/background is never resized to derive another view.','curtainReveals':{'urgency':'Genuine bathroom','locomotion':'Stationary landing, folding chairs and maintenance exit','surprise':'Backstage exit'},'approvedA04A05':'Unchanged historical/selected bytes. The owner-chosen right-side master is a new Batch C layout decision.'},indent=2)+'\n')
print(json.dumps([{'id':r['candidateId'],'sha256':r['sha256']} for r in records],indent=2))
