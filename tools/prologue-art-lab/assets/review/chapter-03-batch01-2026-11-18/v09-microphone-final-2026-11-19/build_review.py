"""Package only the localized microphone correction and its preservation proof."""
from pathlib import Path
from PIL import Image
import json,hashlib
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent;REPO=BASE.parents[4]
ID='CH3-A01-restroom-v09'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads((ROOT/p).read_text())
def write(p,data):(ROOT/p).write_text(json.dumps(data,indent=2)+'\n')
pins=read('sources/history-pins.json')
for p in pins['files']:assert sha(BASE/p['file'])==p['sha256'],p['file']
refs=read('sources/references.json')
for p in refs:
 assert sha(ROOT/p['file'])==p['sha256'];assert sha(REPO/p['repositoryPath'])==p['sha256']
protected=read('sources/protected-artwork.json')
for p in protected:assert sha(REPO/p['file'])==p['sha256'],p['id']
record=read('sources/edit-record.json');candidate=ROOT/f'candidates/{ID}.png'
out=Image.open(candidate).convert('RGB');before=Image.open(ROOT/'references/A01-v08.png').convert('RGB');preview=Image.open(ROOT/f'previews/{ID}-4x.png').convert('RGB');mask=Image.open(ROOT/'diagnostics/explicit-edit-mask.png').convert('1')
assert sha(candidate)==record['sha256'];assert out.size==before.size==(314,206);assert preview.size==(1256,824)
assert all(preview.getpixel((4*x+dx,4*y+dy))==out.getpixel((x,y)) for y in range(206) for x in range(314) for dx in range(4) for dy in range(4))
changed=0
for y in range(206):
 for x in range(314):
  if before.getpixel((x,y))!=out.getpixel((x,y)):
   assert mask.getpixel((x,y));changed+=1
assert changed==record['changedPixels']
for box in [(69,38,180,62),(171,102,180,120),(102,139,155,183),(165,139,171,182),(244,127,254,142)]:assert before.crop(box).tobytes()==out.crop(box).tobytes()
qa={'result':'PASS for localized correction and preservation; no visual approval implied.','dimensions':[314,206],'previewDimensions':[1256,824],'every4x4PreviewBlockMatches':True,'alphaExtrema':list(out.convert('RGBA').getchannel('A').getextrema()),'changedPixels':changed,'changedBounds':record['changedBounds'],'unexpectedChangedPixelsOutsideExplicitMask':0,'wholeAttendantGuardPixelsUnchanged':record['wholeAttendantGuardPixelsUnchanged'],'all489RestoredNPCPixelsUnchanged':record['protected489RestoredNPCPixelsUnchanged'],'signageGateAndAbsentDeviceRegionsUnchanged':True,'A04AndFourPortraitsHashUnchanged':protected,'historicalFilesHashVerified':len(pins['files']),'visualInspection':{'order':['314x206 native scene first','1256x824 exact 4x preview second','8x microphone proof last'],'observations':['Dark capsule head is separated from the post by a background pixel.','One-pixel gooseneck curves subtly between the capsule and base.','Cool dark stem is distinct from the brown chair behind it; compact base is visible on the cream desktop.','Attendant position and every protected foreground pixel remain unchanged. Readability and final visual selection remain Nate’s decision.']},'generationCalls':0,'globalFiltering':False,'candidateResampled':False,'originalFullSceneNativeGridAuthorship':'UNPROVEN; inherited source-derived RGB remains. Only the explicit local pixel correction is directly native-grid authored.','selected':False,'approved':False,'integrated':False}
write('qa.json',qa)
write('manifest.json',{'candidateId':ID,'version':'v09','branch':'art/ch3-pavilion-batch01-20261118','sourcePin':pins['commit'],'candidate':f'candidates/{ID}.png','sha256':sha(candidate),'dimensions':[314,206],'preview4x':f'previews/{ID}-4x.png','method':record['method'],'generationCalls':0,'changedPixels':changed,'status':'generated/unselected','selected':False,'approved':False,'assetPath':None,'editRecord':'sources/edit-record.json','nativeAuthorshipLimitation':qa['originalFullSceneNativeGridAuthorship']})
(ROOT/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 3 A01 — final microphone correction / v09</title><style>*{box-sizing:border-box}body{margin:0;background:#15252a;color:#f3e9d9;font:16px/1.55 system-ui,sans-serif}main{max-width:1360px;margin:auto;padding:24px}a{color:#9de0db}code{overflow-wrap:anywhere}.viewport{max-width:100%;overflow:auto;background:#091519;border:1px solid #55727a}.viewport img{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}button{font:inherit;padding:9px 16px;background:#25444d;color:inherit;border:1px solid #819c9f;cursor:pointer}button[aria-pressed=true]{background:#f4d3ac;color:#17272c}.controls{display:flex;gap:12px;flex-wrap:wrap;margin:16px 0}.notice{border-left:4px solid #efb48a;background:#4c3b30;padding:16px}</style><main>
<h1>A01 — final microphone correction</h1><p><strong>CH3-A01-restroom-v09 · Generated / unselected</strong></p><p>Only the microphone and its immediately necessary background-repair pixels changed. Dark capsule head, narrow curved stem and small readable base; the microphone stays left of the attendant and unobstructed. No image generation, global palette work, sharpening or filtering.</p>
<p><a href="../v08-npc-revert-2026-11-19/">Preserved v08</a> · <a href="../v07-native-finishing-2026-11-19/#CH3-A04-verification-v07">Unchanged A04 v07</a> · <a href="manifest.json">Candidate hash / provenance</a> · <a href="qa.json">QA and visual inspection notes</a> · <a href="sources/changed-pixels.tsv">Every changed pixel</a> · <a href="browser-qa.json">Browser checks</a></p>
<div class="controls"><button data-scale="1" aria-pressed="true">Native 314×206</button><button data-scale="4" aria-pressed="false">Exact 4× nearest-neighbor</button></div>
<div class="viewport"><img class="art" src="candidates/CH3-A01-restroom-v09.png" width="314" height="206" data-w="314" data-h="206" alt="Restroom with protected v08 attendant and corrected desk microphone"></div><p>SHA-256: <code>CANDIDATE_HASH</code><br><a href="previews/CH3-A01-restroom-v09-4x.png">Exact 1256×824 preview PNG</a></p>
<h2>Microphone: before → after</h2><p>Fixed 8× nearest-neighbor proof. Left: v08. Right: v09. Each half comes from the same 18×27 native region.</p><div class="viewport"><img id="mic-proof" src="comparisons/microphone-before-after-8x.png" width="288" height="216" alt="Microphone close-up v08 left and v09 right"></div>
<h2>Complete scene: v08 → v09</h2><p>Same 314×206 grid and framing. Comparisons scroll without shrinking.</p><div class="viewport"><img class="art" src="comparisons/A01-v08-v09.png" width="628" height="206" data-w="628" data-h="206" alt="Complete restroom scene v08 left and v09 right"></div><p><a href="comparisons/A01-v08-v09-4x.png">Full scene comparison at exact 4×</a></p>
<h2>Explicit edit mask and actual changes</h2><p>White: allowed microphone/repair mask. Orange: the CHANGED_COUNT actual changed pixels. Every pixel outside this mask is identical to v08.</p><div class="viewport"><img class="art" src="diagnostics/explicit-edit-mask.png" width="314" height="206" data-w="314" data-h="206" alt="Explicit local edit mask"></div><div class="viewport"><img class="art" src="diagnostics/actual-changed-pixels.png" width="314" height="206" data-w="314" data-h="206" alt="Exact changed pixels"></div>
<p>All 489 restored NPC pixels, the complete attendant guard regions, signage, gate, architecture, bench, plant and counter outside the tiny microphone/repair mask are unchanged. The unwanted device remains absent. A04 v07 and all four portraits retain their source SHA-256 hashes. All HISTORY_COUNT earlier review files remain unchanged.</p>
<p><a href="sources/edit-record.json">Localized edit record</a> · <a href="sources/new-microphone-operations.json">Six authored pixel primitives</a> · <a href="sources/npc-protection.json">Attendant protection regions</a> · <a href="sources/protected-artwork.json">Protected artwork hashes</a> · <a href="sources/history-pins.json">Historical hashes</a> · <a href="PNG_SHA256SUMS.txt">PNG checksums</a> · <a href="SOURCE_SHA256SUMS.txt">Package checksums</a></p>
<p class="notice"><strong>Native-grid authorship limitation retained:</strong> original full-scene native authorship remains unproven. Only this logged local correction was authored directly on the native grid; inherited source-derived RGB remains.</p><p>Stop for Nate’s final visual selection. Nothing selected, approved, registered or integrated. Batch B has not begun.</p></main><script>document.querySelectorAll('[data-scale]').forEach(b=>b.onclick=()=>{const s=Number(b.dataset.scale);document.querySelectorAll('img.art').forEach(i=>{i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s});document.querySelectorAll('[data-scale]').forEach(n=>n.setAttribute('aria-pressed',String(n===b)));});</script></html>'''.replace('CANDIDATE_HASH',sha(candidate)).replace('CHANGED_COUNT',str(changed)).replace('HISTORY_COUNT',str(len(pins['files']))))
(ROOT/'README.md').write_text('''# A01 v09 — final microphone correction review

Localized native-grid pixel editing only. The old microphone mask is repaired with its exact v06 background pixels, then six explicit microphone primitives are drawn. No image generation or global filtering. The original full-scene native-grid authorship limitation remains.

Run `python3 edit-native.py`, then `python3 build_review.py`. Run `qa-browser.cjs` and rebuild the checksum lists afterward. All source operations, mask images, 489 restored foreground coordinates, final pixel deltas and protected artwork hashes are included.

The attendant, four portraits, A04 v07, all older review packages and all production files remain unchanged. Await Nate’s final visual selection; no approval, registration, integration or next batch.
''')
(ROOT/'PNG_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(ROOT).as_posix()}\n' for p in sorted(ROOT.rglob('*.png'))))
(ROOT/'SOURCE_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(ROOT).as_posix()}\n' for p in sorted(ROOT.rglob('*')) if p.is_file() and p.suffix!='.png' and p.name!='SOURCE_SHA256SUMS.txt'))
print(json.dumps({'candidateHash':sha(candidate),'changedPixels':changed,'historyFilesUnchanged':len(pins['files']),'protectedArtworkHashesUnchanged':len(protected)},indent=2))
