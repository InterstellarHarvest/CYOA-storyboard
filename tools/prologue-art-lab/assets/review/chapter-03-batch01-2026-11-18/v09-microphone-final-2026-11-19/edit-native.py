"""Only localized microphone replacement on the actual inherited 314x206 grid."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
ROOT=Path(__file__).resolve().parent
ID='CH3-A01-restroom-v09'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads((ROOT/p).read_text())
def write(p,obj):(ROOT/p).write_text(json.dumps(obj,indent=2)+'\n')
old=read('sources/old-microphone-operations.json')
new=read('sources/new-microphone-operations.json')
source=Image.open(ROOT/'references/A01-v08.png').convert('RGB')
donor=Image.open(ROOT/'references/A01-v06-background-donor.png').convert('RGB')
assert source.size==donor.size==(314,206)
def draw_ops(im,ops,mask=False):
 d=ImageDraw.Draw(im)
 for o in ops:
  c=1 if mask else tuple(bytes.fromhex(o['color'].lstrip('#')))
  pts=[tuple(p) for p in o.get('points',[])]
  if o['kind']=='polygon':d.polygon(pts,fill=c)
  elif o['kind']=='line':d.line(pts,fill=c,width=o['width'])
  elif o['kind']=='rectangle':d.rectangle(tuple(o['box']),fill=c)
  else:
   for p in pts:d.point(p,fill=c)
def mask(ops):
 m=Image.new('1',(314,206));draw_ops(m,ops,True);return m
repair=mask(old);mic=mask(new);allowed=mask(old+new)
out=source.copy();repair_count=0
for y in range(206):
 for x in range(314):
  if repair.getpixel((x,y)):
   repair_count+=out.getpixel((x,y))!=donor.getpixel((x,y))
   out.putpixel((x,y),donor.getpixel((x,y)))
draw_ops(out,new)
guards=read('sources/npc-protection.json')
for name in ['headHairAndFaceBox','bodyArmsHandsAndClothingBox']:
 box=tuple(guards[name]);assert source.crop(box).tobytes()==out.crop(box).tobytes(),name
 assert not any(allowed.getpixel((x,y)) for y in range(box[1],box[3]) for x in range(box[0],box[2])),name
restored=[]
for line in (ROOT/guards['restoredPixelList']).read_text().splitlines()[1:]:
 x,y=map(int,line.split('\t')[:2]);assert source.getpixel((x,y))==out.getpixel((x,y));restored.append((x,y))
assert len(restored)==489
changed=[];delta=Image.new('RGB',(314,206));dd=ImageDraw.Draw(delta)
for y in range(206):
 for x in range(314):
  if source.getpixel((x,y))!=out.getpixel((x,y)):
   assert allowed.getpixel((x,y)),(x,y)
   changed.append((x,y));dd.point((x,y),fill='#ed913f')
file=ROOT/f'candidates/{ID}.png';out.save(file)
out.resize((1256,824),Image.Resampling.NEAREST).save(ROOT/f'previews/{ID}-4x.png')
for name,m in [('explicit-edit-mask',allowed),('old-microphone-background-repair-mask',repair),('new-microphone-mask',mic)]:
 m.convert('RGB').save(ROOT/f'diagnostics/{name}.png')
delta.save(ROOT/'diagnostics/actual-changed-pixels.png')
with (ROOT/'sources/changed-pixels.tsv').open('w') as f:
 f.write('x\ty\tbefore_rgb\tafter_rgb\n')
 for x,y in changed:f.write(f'{x}\t{y}\t{source.getpixel((x,y))}\t{out.getpixel((x,y))}\n')
box=(190,119,208,146)
close=Image.new('RGB',(36,27));close.paste(source.crop(box),(0,0));close.paste(out.crop(box),(18,0));close.save(ROOT/'comparisons/microphone-before-after-native.png');close.resize((288,216),Image.Resampling.NEAREST).save(ROOT/'comparisons/microphone-before-after-8x.png')
pair=Image.new('RGB',(628,206));pair.paste(source,(0,0));pair.paste(out,(314,0));pair.save(ROOT/'comparisons/A01-v08-v09.png');pair.resize((2512,824),Image.Resampling.NEAREST).save(ROOT/'comparisons/A01-v08-v09-4x.png')
report={'candidateId':ID,'sha256':sha(file),'dimensions':[314,206],'method':'Coordinate-authored microphone only. Restore exact v06 background under the old microphone mask, then draw six explicit native primitives.','generationCalls':0,'source':'references/A01-v08.png','sourceSha256':sha(ROOT/'references/A01-v08.png'),'backgroundDonor':'references/A01-v06-background-donor.png','donorSha256':sha(ROOT/'references/A01-v06-background-donor.png'),'oldMicrophoneRepairPixels':repair_count,'changedPixels':len(changed),'changedBounds':delta.getbbox(),'allowedEditBounds':allowed.getbbox(),'unexpectedChangedPixels':0,'foregroundGuardBoxes':guards,'protected489RestoredNPCPixelsUnchanged':True,'wholeAttendantGuardPixelsUnchanged':True,'nativeGridAuthorshipLimitation':'Original full-scene native-grid authorship remains unproven. Only this logged local edit is directly authored on the native grid; inherited source-derived RGB remains.','approved':False,'selected':False,'assetPath':None}
write('sources/edit-record.json',report)
print(json.dumps(report,indent=2))
