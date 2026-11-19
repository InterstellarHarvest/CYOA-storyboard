"""Lossless rollback of the logged v07 attendant edits only."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent
ID='CH3-A01-restroom-v08'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,obj):(ROOT/name).write_text(json.dumps(obj,indent=2)+'\n')
pins=json.loads((ROOT/'sources/history-pins.json').read_text())
for f in pins['files']:assert sha(BASE/f['file'])==f['sha256'],f['file']
old=Image.open(ROOT/'references/A01-v06.png').convert('RGB')
v07=Image.open(ROOT/'references/A01-v07.png').convert('RGB')
assert old.size==v07.size==(314,206)
def make_mask(ops):
 m=Image.new('1',(314,206));d=ImageDraw.Draw(m)
 for o in ops:
  if o['kind']=='polygon':d.polygon([tuple(p) for p in o['points']],fill=1)
  elif o['kind']=='rectangle':d.rectangle(tuple(o['box']),fill=1)
  elif o['kind']=='line':d.line([tuple(p) for p in o['points']],fill=1,width=o['width'])
  else:
   for p in o['points']:d.point(tuple(p),fill=1)
 return m
reverted=json.loads((ROOT/'sources/reverted-operations.json').read_text())
mask=make_mask(reverted['operations'])
allops=json.loads((BASE/'v07-native-finishing-2026-11-19/sources/native-edit-record.json').read_text())['candidates'][0]['operations']
mic=make_mask([o for o in allops if o['label'].startswith('microphone')])
assert not any(mask.getpixel((x,y)) and mic.getpixel((x,y)) for y in range(206) for x in range(314))
out=v07.copy();changed=[]
for y in range(206):
 for x in range(314):
  if mask.getpixel((x,y)):
   out.putpixel((x,y),old.getpixel((x,y)))
  if out.getpixel((x,y))!=v07.getpixel((x,y)):changed.append((x,y))
assert all(out.getpixel((x,y))==old.getpixel((x,y)) for y in range(206) for x in range(314) if mask.getpixel((x,y)))
assert all(out.getpixel((x,y))==v07.getpixel((x,y)) for y in range(206) for x in range(314) if not mask.getpixel((x,y)))
for box in [(201,96,231,122),(202,122,244,140)]:assert out.crop(box).tobytes()==old.crop(box).tobytes()
candidate=ROOT/f'candidates/{ID}.png';out.save(candidate)
preview=out.resize((1256,824),Image.Resampling.NEAREST);preview.save(ROOT/f'previews/{ID}-4x.png')
assert all(preview.getpixel((x*4+dx,y*4+dy))==out.getpixel((x,y)) for y in range(206) for x in range(314) for dx in range(4) for dy in range(4))
triplet=Image.new('RGB',(942,206))
for i,im in enumerate([old,v07,out]):triplet.paste(im,(314*i,0))
triplet.save(ROOT/'comparisons/v06-v07-v08.png');triplet.resize((3768,824),Image.Resampling.NEAREST).save(ROOT/'comparisons/v06-v07-v08-4x.png')
box=(201,96,244,141);face=Image.new('RGB',(129,45))
for i,im in enumerate([old,v07,out]):face.paste(im.crop(box),(43*i,0))
face.save(ROOT/'comparisons/attendant-v06-v07-v08.png');face.resize((1032,360),Image.Resampling.NEAREST).save(ROOT/'comparisons/attendant-v06-v07-v08-8x.png')
out.crop((180,122,208,146)).resize((224,192),Image.Resampling.NEAREST).save(ROOT/'comparisons/microphone-v08-8x.png')
diff=Image.new('RGB',(314,206));d=ImageDraw.Draw(diff)
for p in changed:d.point(p,fill='#ed913f')
diff.save(ROOT/'comparisons/changed-pixels.png')
with (ROOT/'sources/restored-pixels.tsv').open('w') as f:
 f.write('x\ty\tv07_rgb\tto_v06_rgb\n')
 for x,y in changed:f.write(f'{x}\t{y}\t{v07.getpixel((x,y))}\t{out.getpixel((x,y))}\n')
qa={'result':'PASS','candidateId':ID,'dimensions':[314,206],'mode':out.mode,'alphaExtrema':[255,255],'previewDimensions':[1256,824],'all4x4BlocksMatch':True,'restoredPixels':len(changed),'revertedNPCOperations':len(reverted['operations']),'allLoggedNPCPixelsMatchV06':True,'headAndClothingCropPixelsMatchV06':True,'unexpectedChangedPixelsOutsideNPCMask':0,'microphonePixelsIdenticalToV07':True,'npcAndMicrophoneMaskOverlap':0,'historicalFilesUnchanged':len(pins['files']),'inheritedLimitation':'Original full-scene native-grid authorship remains unproven; inherited source-derived RGB remains. No regeneration, filtering, resizing or repainting of the candidate.','status':'generated/unselected','approved':False,'integrated':False}
write('qa.json',qa)
write('manifest.json',{'version':'v08','sourcePin':pins['commit'],'branch':'art/ch3-pavilion-batch01-20261118','candidateId':ID,'candidate':f'candidates/{ID}.png','sha256':sha(candidate),'method':'Restore v06 source pixels under the exact 28 logged v07 NPC-edit operation masks. All other v07 pixels unchanged.','generationCalls':0,'selected':False,'approved':False,'assetPath':None,'A04':'Unchanged; retained in ../v07-native-finishing-2026-11-19/','qa':'qa.json'})
(ROOT/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 3 A01 — v06 attendant restored / v08</title><style>*{box-sizing:border-box}body{margin:0;background:#15252a;color:#f3e9d9;font:16px/1.55 system-ui,sans-serif}main{max-width:1360px;margin:auto;padding:24px}a{color:#9de0db}code{overflow-wrap:anywhere}.viewport{max-width:100%;overflow:auto;background:#091519;border:1px solid #55727a}.viewport img{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}button{font:inherit;padding:9px 16px;background:#25444d;color:inherit;border:1px solid #819c9f;cursor:pointer}button[aria-pressed=true]{background:#f4d3ac;color:#17272c}.controls{display:flex;gap:12px;flex-wrap:wrap;margin:16px 0}</style><main>
<h1>A01 — v06 attendant restored</h1><p><strong>CH3-A01-restroom-v08 · Generated / unselected</strong></p><p>The v06 attendant is restored pixel-for-pixel, including his original face, hair, glasses and clothes. The v07 desk microphone and all other v07 scene edits remain unchanged. No regeneration, new drawing or filtering.</p>
<p><a href="../v07-native-finishing-2026-11-19/">Preserved v07 gallery / unchanged A04</a> · <a href="manifest.json">Manifest and candidate hash</a> · <a href="qa.json">Technical QA</a> · <a href="sources/reverted-operations.json">Exact reverted NPC edit masks</a> · <a href="sources/restored-pixels.tsv">Restored pixel values</a> · <a href="browser-qa.json">Browser QA</a></p>
<div class="controls"><button data-scale="1" aria-pressed="true">1×</button><button data-scale="4" aria-pressed="false">4× nearest-neighbor</button></div>
<div class="viewport"><img class="art" src="candidates/CH3-A01-restroom-v08.png" width="314" height="206" data-w="314" data-h="206" alt="Restroom with original v06 attendant and preserved v07 microphone"></div>
<p>SHA-256: <code>CANDIDATE_HASH</code><br><a href="previews/CH3-A01-restroom-v08-4x.png">Exact 4× PNG</a></p>
<h2>Scene comparison</h2><p>Left to right: v06, v07, v08. Each scene uses the same 314×206 grid. Wide comparisons scroll without shrinking.</p><div class="viewport"><img class="art" src="comparisons/v06-v07-v08.png" width="942" height="206" data-w="942" data-h="206" alt="v06, v07 and v08 scene comparison"></div>
<h2>Attendant and microphone proofs</h2><p>Fixed 8× attendant crops: v06 left, rejected v07 middle, restored v08 right.</p><div class="viewport"><img src="comparisons/attendant-v06-v07-v08-8x.png" width="1032" height="360" alt="Attendant v06, v07 and v08 identity proof"></div><p>Preserved v07 microphone, fixed 8× crop:</p><div class="viewport"><img src="comparisons/microphone-v08-8x.png" width="224" height="192" alt="Unchanged restored microphone beside intercom"></div>
<h2>Validation</h2><p>RESTORED_COUNT NPC pixels restored from v06; zero changes outside the NPC edit mask. The head and clothing crops match v06 exactly. Microphone pixels remain identical to v07. All HISTORY_COUNT earlier review files are unchanged. A04, all portraits, narrative, gameplay, selected artwork and production registry remain unchanged.</p><p>Original full-scene native-grid authorship remains unproven. No selection, approval, registration or integration. Stop for Nate’s review.</p></main><script>document.querySelectorAll('[data-scale]').forEach(b=>b.onclick=()=>{const s=Number(b.dataset.scale);document.querySelectorAll('img.art').forEach(i=>{i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s});document.querySelectorAll('[data-scale]').forEach(n=>n.setAttribute('aria-pressed',String(n===b)));});</script></html>'''.replace('CANDIDATE_HASH',sha(candidate)).replace('RESTORED_COUNT',str(len(changed))).replace('HISTORY_COUNT',str(len(pins['files']))))
(ROOT/'README.md').write_text('v08 restores the v06 attendant under the exact logged v07 NPC operation masks. The microphone and all other v07 pixels are unchanged. A04 is linked unchanged. All earlier review files preserved. No generation, filtering, approval or integration. Rebuild with `python3 build_review.py`.\n')
(ROOT/'PNG_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(ROOT).as_posix()}\n' for p in sorted(ROOT.rglob('*.png'))))
(ROOT/'SOURCE_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(ROOT).as_posix()}\n' for p in sorted(ROOT.rglob('*')) if p.is_file() and p.suffix!='.png' and p.name!='SOURCE_SHA256SUMS.txt'))
print(json.dumps({'restoredPixels':len(changed),'sha256':sha(candidate),'historyPreserved':len(pins['files'])},indent=2))
