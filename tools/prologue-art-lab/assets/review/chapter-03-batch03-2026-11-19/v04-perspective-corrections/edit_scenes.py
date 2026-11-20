"""Native local components and explicit geometry edits; preserve all v01-v03 sources."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageColor
import json,hashlib,math
R=Path(__file__).resolve().parent;V1=R.parent/'v01';V2=R.parent/'v02-localized-corrections';V3=R.parent/'v03-continuity-corrections'
for d in ['candidates','previews','masks','layers','sources','comparisons','composites']:(R/d).mkdir(exist_ok=True)
def im(p):return Image.open(p).convert('RGBA')
def blank(size):return Image.new('RGBA',size)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):(R/p).write_text(json.dumps(d,separators=(',',':'))+'\n' if 'changed-pixels' in p or 'operation-coordinates' in p else json.dumps(d,indent=2)+'\n')
def mask(size,p):
 m=Image.new('L',size);ImageDraw.Draw(m).polygon(p,fill=255);return m
def cut(a,p):
 b=a.copy();b.putalpha(mask(a.size,p));return b
source= json.loads((V3/'manifest.json').read_text());previous={r['candidateId']:r for r in source['candidates']}
base={i:im(V3/r['file']) for i,r in previous.items()};work={i:a.copy() for i,a in base.items()}
allowed={i:Image.new('L',a.size) for i,a in base.items()};ops={i:[] for i in base};phases=[]
def edit(ident,label,limit,fn):
 a=work[ident];before=a.copy();fn(a);coords=[]
 for y in range(a.height):
  for x in range(a.width):
   if a.getpixel((x,y))!=before.getpixel((x,y)):
    assert limit.getpixel((x,y)),(ident,label,x,y);coords.append([x,y])
 allowed[ident]=ImageChops.lighter(allowed[ident],limit);ops[ident].append(label)
 phases.append({'candidateId':ident,'operation':label,'changedPixels':len(coords),'coordinates':coords})
def boxmask(size,box):
 a=Image.new('L',size);ImageDraw.Draw(a).rectangle((box[0],box[1],box[2]-1,box[3]-1),fill=255);return a

# Rebuild clean flat hardware at its logical component grid. Perspective is
# applied to each entire plate, including its border and slats, from one VP.
# No scene/background is resized and no whole-image color filter is used.
def pictogram(unit):
 a=blank((24*unit,27*unit));d=ImageDraw.Draw(a)
 def rect(b,c):d.rectangle(tuple(v*unit for v in b[:2])+tuple((v+1)*unit-1 for v in b[2:]),fill=c)
 rect((1,1,23,26),'#8d8a79');rect((0,0,22,25),'#ead0ab');rect((1,1,21,24),'#f7e3bc');rect((2,2,20,23),'#345762')
 rect((5,5,7,7),'#f7e6c2');rect((4,9,8,15),'#f7e6c2');rect((5,15,5,21),'#f7e6c2');rect((7,15,7,21),'#f7e6c2')
 rect((15,5,17,7),'#f7e6c2');d.polygon([(16*unit,9*unit),(12*unit,17*unit),(21*unit-1,17*unit)],fill='#f7e6c2')
 rect((15,17,15,21),'#f7e6c2');rect((17,17,17,21),'#f7e6c2');rect((11,4,11,22),'#e4d2ae')
 return a
def wall_buttons(width,height):
 a=blank((width,height));d=ImageDraw.Draw(a);d.rectangle((1,1,width-1,height-1),fill='#9c917a');d.rectangle((0,0,width-2,height-2),fill='#65716b');d.rectangle((1,1,width-3,height-3),fill='#f1d3a9')
 scale=1 if width<15 else 2
 for x in [2,width-5]:
  for y in [2,height-5]:d.rectangle((x,y,x+scale-1,y+scale-1),fill='#69716a')
 left=3 if scale==1 else 7;right=width-5 if scale==1 else width-7
 starts=[5,11,17] if scale==1 else [8,23,38];bh=4 if scale==1 else 10
 for y,c in zip(starts,['#e46640','#f2dbb2','#729f97']):
  d.rectangle((left-1,y-1,right+1,y+bh),fill='#354e54');d.rectangle((left,y,right,y+bh-1),fill=c)
  d.line((left,y,right,y),fill='#fff0cf');d.line((left,y+bh,right+1,y+bh),fill='#687570')
 return a
def grille(width,height):
 a=blank((width,height));d=ImageDraw.Draw(a);d.rectangle((0,0,width-1,height-1),fill='#bcc1ae');d.rectangle((1,1,width-2,height-2),fill='#698181')
 for y in range(2,height-1,2):d.line((2,y,width-3,y),fill='#29434e')
 return a

geometries={
 'main':{'vp':[157,107],'referenceX':279,'crop':[277,50,314,135],
  'components':[('pictogram',pictogram(1),279,68,26),('wall-buttons',wall_buttons(11,25),282,98,23),('speaker',grille(20,8),280,124,7)]},
 'close':{'vp':[280,148],'referenceX':499,'crop':[496,20,564,193],
  'components':[('pictogram',pictogram(2),500,48,54),('wall-buttons',wall_buttons(25,54),511,117,51),('speaker',grille(33,12),510,175,10)]}}
projection_records=[]
def wall_master(kind):
 source=im(V2/'candidates'/('CH3-C01-urgency-v02.png' if kind=='main' else 'CH3-C02-urgency-bg-v02.png'));out=source.copy();g=geometries[kind]
 # Restore only the old plate footprints with adjacent same-row wall pixels.
 boxes=[(279,68,304,97),(279,99,299,123),(279,122,298,134)] if kind=='main' else [(499,43,554,111),(509,113,542,174),(510,175,543,193)]
 sx=278 if kind=='main' else 555
 for x0,y0,x1,y1 in boxes:
  for y in range(y0,y1):
   for x in range(x0,x1):out.putpixel((x,y),source.getpixel((sx,y)))
 vx,vy=g['vp'];ref=g['referenceX']
 for name,sprite,x0,top,height in g['components']:
  sprite.save(R/'layers'/f'{kind}-{name}-flat-native.png')
  corners=[]
  for x,yref in [(x0,top),(x0+sprite.width-1,top),(x0+sprite.width-1,top+height),(x0,top+height)]:corners.append([x,vy+(yref-vy)*(x-vx)/(ref-vx)])
  # Inverse mapping fills every target pixel, including magnified far edges.
  # Nearest source component pixels only; all geometry and rounding retained.
  for dx in range(sprite.width):
   x=x0+dx;factor=(x-vx)/(ref-vx);y0=vy+(top-vy)*factor;y1=vy+(top+height-vy)*factor
   for y in range(round(y0),round(y1)):
    plane_y=vy+(y-vy)/factor
    sy=min(sprite.height-1,max(0,round((plane_y-top)/height*(sprite.height-1))))
    pixel=sprite.getpixel((dx,sy))
    if pixel[3]:out.putpixel((x,y),pixel)
  projection_records.append({'camera':kind,'component':name,'vanishingPoint':g['vp'],'referenceX':ref,'nativeSpriteSize':list(sprite.size),'targetLeft':x0,'planeTop':top,'planeHeight':height,'projectedCorners':corners,'method':'Inverse per-column nearest sampling of native-authored flat component only; no scene resampling.'})
 out.crop(tuple(g['crop'])).save(R/'layers'/f'{kind}-projected-wall-master.png')
 return out
walls={k:wall_master(k) for k in geometries}
for ident,a in work.items():
 kind='main' if a.width==314 else 'close';box=tuple(geometries[kind]['crop']);m=boxmask(a.size,box)
 edit(ident,'Replace constant upward tilt with a shared wall vanishing point: plate edges converge together, including downward-right lower panel/grille edges.',m,lambda a,k=kind,b=box:a.paste(walls[k].crop(b),b[:2]))

# Enlarge the functional controls WITHIN the existing pedestal head. Main
# and close heads are authored independently at their existing scene grids.
def readable_controls(a,active):
 d=ImageDraw.Draw(a);dark='#2d4651';frame='#ebd1a8';green='#9ad957' if active else '#618858';highlight='#e2f4b2' if active else '#9db685'
 if a.width==314:
  d.polygon([(225,129),(246,129),(246,132),(244,142),(220,142),(220,139)],fill=dark)
  d.polygon([(225,129),(246,129),(244,139),(220,139)],fill=frame)
  d.polygon([(225,130),(245,130),(243,138),(221,138)],fill='#3d5a63')
  # Large tactile BEGIN button with light play/activation glyph.
  d.polygon([(225,132),(233,132),(232,137),(224,137)],fill='#172e36')
  d.polygon([(226,132),(232,132),(231,136),(225,136)],fill=green)
  d.line((226,132,232,132),fill=highlight);d.polygon([(228,133),(228,135),(230,134)],fill='#f5f0cf')
  # Separate red release lever under a raised cream cover, not a third button.
  d.polygon([(236,131),(243,131),(242,137),(235,137)],fill='#223b45')
  d.rectangle((238,132,240,135),fill='#df633f');d.line((237,131,243,131),fill='#fff0cb');d.line((243,131,242,136),fill='#fff0cb');d.line((236,132,235,136),fill='#b7c8b7')
  d.line((220,140,243,140),fill='#6d888b')
 else:
  d.polygon([(424,187),(464,187),(464,191),(460,211),(418,211),(418,207)],fill=dark)
  d.polygon([(424,187),(464,187),(460,207),(418,207)],fill=frame)
  d.polygon([(425,189),(461,189),(458,205),(421,205)],fill='#3d5a63')
  d.polygon([(426,192),(441,192),(439,203),(423,203)],fill='#172e36')
  d.polygon([(427,193),(439,193),(437,201),(425,201)],fill=green)
  d.line((427,193,439,193),fill=highlight,width=2);d.polygon([(431,195),(430,199),(435,197)],fill='#f5f0cf')
  d.polygon([(447,191),(459,191),(457,203),(444,203)],fill='#223b45')
  d.polygon([(450,194),(454,194),(453,200),(449,200)],fill='#df633f')
  d.line((447,191,459,191),fill='#fff0cb',width=2);d.line((459,191,457,202),fill='#fff0cb',width=2);d.line((447,193,445,201),fill='#b7c8b7')
  d.line((420,208,459,208),fill='#6d888b',width=2)
for ident,a in work.items():
 box=(219,129,247,143) if a.width==314 else (418,187,465,212)
 edit(ident,'Clarify pedestal controls: larger green BEGIN button, activation glyph, separate red emergency release and raised cover; only surprise is brightly lit.',boxmask(a.size,box),lambda a,active=ident in ['CH3-C04-surprise','CH3-C05-surprise-bg']:readable_controls(a,active))

# Remove the old right-side performer through her EXACT silhouette, restoring
# the underlying display, curtain, raised deck, cannon and confetti locally.
ident='CH3-C04-surprise';a=work[ident]
old_person=im(V3/'layers/surprise-presenter-front.png')
main=im(V1/'references/A04-verification.png');s=im(V1/'donors/CH3-C04-surprise-native-donor.png')
clean=im(V3/'candidates/CH3-A04-verification-continuity-v03.png')
screen=Image.new('L',clean.size);ImageDraw.Draw(screen).rounded_rectangle((134,73,183,117),radius=6,fill=255)
face=Image.new('RGBA',clean.size,'#284b55');face.putalpha(screen);clean.alpha_composite(face)
d=ImageDraw.Draw(clean)
for cx in [149,172]:d.ellipse((cx-6,88,cx+6,100),fill='#918363');d.ellipse((cx-4,89,cx+4,98),fill='#fff0bd')
platform=cut(main,[(126,126),(199,126),(209,129),(216,133),(218,137),(216,144),(209,148),(120,148),(111,145),(109,140),(110,134),(116,130)])
clean.alpha_composite(platform,(0,-8))
cannon=cut(s,[(171,108),(174,108),(180,111),(186,113),(190,117),(192,119),(192,123),(190,126),(188,126),(188,132),(191,132),(191,135),(171,135),(171,133),(177,131),(178,124),(173,122),(169,119),(168,114)])
clean.alpha_composite(cannon,(0,-8))
colors=['#e86c45','#eee3b4','#90b4a0']
for x,y,c in [(118,82,0),(128,92,1),(203,90,0),(198,109,1),(181,119,2),(155,124,1),(107,91,1),(121,103,2),(213,123,0),(224,144,1),(162,143,2),(194,147,0),(136,151,1),(244,162,0),(174,164,1),(101,155,0)]:ImageDraw.Draw(clean).polygon([(x,y),(x+3,y-1),(x+4,y+1),(x+1,y+2)],fill=colors[c])
new_person=blank(a.size);new_person.alpha_composite(old_person,(-73,0));new_person.save(R/'layers/surprise-presenter-firing-side.png')
limit=ImageChops.lighter(old_person.getchannel('A'),new_person.getchannel('A'))
def move_presenter(a):
 for y in range(a.height):
  for x in range(a.width):
   if old_person.getpixel((x,y))[3]:a.putpixel((x,y),clean.getpixel((x,y)))
 a.alpha_composite(new_person)
edit(ident,'Move the exact small presenter 73 pixels left, onto the firing side of the left-pointing cannon. Preserve sprite pixels, vertical placement and scale.',limit,move_presenter)
clean.save(R/'layers/surprise-under-performer-repair-source.png');old_person.getchannel('A').save(R/'masks/surprise-old-performer-silhouette.png')

records=[]
for ident,a in work.items():
 assert a.getchannel('A').getextrema()==(255,255),ident
 before=base[ident];pixels=[];changed=Image.new('L',a.size);layer=blank(a.size)
 for y in range(a.height):
  for x in range(a.width):
   p=(x,y)
   if a.getpixel(p)!=before.getpixel(p):
    assert allowed[ident].getpixel(p);changed.putpixel(p,255);layer.putpixel(p,a.getpixel(p));pixels.append({'x':x,'y':y,'before':list(before.getpixel(p)[:3]),'after':list(a.getpixel(p)[:3])})
 file=f'candidates/{ident}-v04.png';a.convert('RGB').save(R/file);a.convert('RGB').resize((a.width*4,a.height*4),Image.Resampling.NEAREST).save(R/'previews'/f'{ident}-v04-4x.png')
 allowed[ident].save(R/'masks'/f'{ident}-allowed.png');changed.save(R/'masks'/f'{ident}-changed.png');layer.save(R/'layers'/f'{ident}-correction.png')
 write(f'sources/{ident}-changed-pixels.json',{'coordinates':'Zero-based native x,y; RGB before/after','pixels':pixels})
 prev=previous[ident]
 records.append({**{k:prev[k] for k in ['candidateId','record','kind','dimensions','additionalContinuityOption']},'file':file,'sha256':sha(R/file),'sourceFile':'v03-continuity-corrections/'+prev['file'],'sourceSha256':sha(V3/prev['file']),'sourceCommit':'2f51cfd909ca443b64e52285af17cb00bdb770b6','changedPixels':len(pixels),'operations':ops[ident],'status':'generated','selected':False,'approved':False,'assetPath':None})
write('sources/corrections.json',records);write('sources/operation-coordinates.json',phases);write('sources/wall-projection.json',projection_records)
write('sources/layout.json',{'wallMainBox':geometries['main']['crop'],'wallCloseBox':geometries['close']['crop'],'wallGeometry':'One declared vanishing point per camera; upper and lower edges converge independently instead of constant shear. Local native component projection is derived, not original full-scene authorship.','mainVanishingPoint':geometries['main']['vp'],'closeVanishingPoint':geometries['close']['vp'],'pedestal':'Large green BEGIN at left; separate covered red release at right; main and close heads independently authored at native grids.','presenterMove':{'offsetFromV03':[-73,0],'scale':1,'newBounds':list(new_person.getchannel('A').getbbox()),'cannonMouthX':168,'meaning':'Presenter lies left of the cannon mouth, on its firing side. Portrait foreground already lies left of its cannon.'},'authorship':'Original native-grid authorship remains UNRESOLVED / UNPROVEN.'})
print(json.dumps({r['candidateId']:{'changedPixels':r['changedPixels'],'sha256':r['sha256']} for r in records},indent=2))
