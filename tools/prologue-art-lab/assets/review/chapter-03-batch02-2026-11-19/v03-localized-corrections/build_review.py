"""Build and validate v03 without writing to historical or production files."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import json,hashlib,html,os
ROOT=Path(__file__).resolve().parent;OLD=ROOT.parent/'v02-additive-continuity';REPO=ROOT.parents[5]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads((ROOT/p).read_text())
def write(p,data):(ROOT/p).write_text(json.dumps(data,indent=2)+'\n')
def rgba(p):return Image.open(p).convert('RGBA')
def rgb(p):return Image.open(p).convert('RGB')
edits=read('sources/localized-edit-records.json');records=edits['candidates'];briefs=read('sources/briefs.json')['candidates']
assert len(records)==6
for pins,root in [('sources/prior-package-pins.json',ROOT.parent),('sources/protected-files.json',REPO),('sources/history-pins.json',REPO),('sources/batch-a-archive-pins.json',Path(os.environ.get('CH3_BATCH_A_ARCHIVE_ROOT',str(REPO.parent/'CYOA-ch3-art-batch01'))))]:
 for f in read(pins)['files']:assert sha(root/f['file'])==f['sha256'],f['file']
for f in read('sources/reference-manifest.json'):
 assert sha(ROOT/f['file'])==f['sha256']
 if 'repositoryPath' in f:assert sha(REPO/f['repositoryPath'])==f['sha256']
generation=read('sources/v03-generation-record.json');assert sha(ROOT/generation['source'])==generation['sha256'];assert sha(ROOT/generation['prompt'])==generation['promptSha256']
raw=rgba(ROOT/generation['source']);assert list(raw.size)==generation['actualDimensions']
fg=rgba(ROOT/'references/A03-attendant.png');fg_hash=sha(ROOT/'references/A03-attendant.png')
assert fg_hash=='28fdf5523454ea2ccdb397bd4d7006fc1fb8f04109046b7646361692422c3ef2'
assert set(fg.getchannel('A').getdata())=={0,255}
qa=[];composites=[]
notes={
'CH3-B01-arrival':['Byte-identical to v02. No edit.'],
'CH3-B02-record-printer':['Removed the added right-hand printer and restored the original plant/counter from approved A01.','Receipt originates at the existing left cream unit’s lower slot. Approved microphone, attendant and chair pixels are unchanged.','New paper is authored on the actual grid with restrained native polygons and non-letter marks; no base filtering.'],
'CH3-B03-record-printer-bg':['Removed the contradictory right-hand printer; approved A02 plant/counter are restored.','The same left slotted housing feeds a short receipt tail. Microphone is untouched.','Approved A03 foreground is byte-identical and composited at(0,0), scale1; paper stays to its left.'],
'CH3-B04-record-scanner':['Only the door leaf/handle and document intake mark change. Frame, reader, light, signs and room remain unchanged.','Door is nearly closed with a four-pixel clear slit at its leading edge.','The form is already engaged under the roller; its arrow points into the one-way reader. Green authorizes the document, not a person.'],
'CH3-B05-record-scanner-bg':['Matching nearly closed door with a seven-pixel clear slit in this closer view. Only the local door/handle and paper intake mark change.','The same document/roller arrangement and intake direction agree with B04.','Approved A03 is unchanged at(0,0), scale1; no foreground regeneration or movement.'],
'CH3-B06-paper-emergency':['Removed the added printer and all rectangular attendant protection. Uses approved A01 below the new paper/brush layers.','A manually traced one-pixel attendant silhouette, plus separate microphone/chair silhouettes, preserves those exact pixels. Paper passes behind the body with hard native occlusion.','The same left unit feeds fewer ribbons. A local fold carries paper up the original plant; jointed brush arms attach to the cornice and bristles contact paper toward the right exit.','Generated plant fragments were manually excluded; the approved plant remains at its original position. No room architecture was rerendered.']}

def pair(before,after,name,scale=1):
 a=before.convert('RGB');b=after.convert('RGB');im=Image.new('RGB',(a.width+b.width,max(a.height,b.height)));im.paste(a,(0,0));im.paste(b,(a.width,0))
 if scale!=1:im=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
 im.save(ROOT/'comparisons'/name);return im.size

for r,b in zip(records,briefs):
 ident=r['candidateId'];im=rgba(ROOT/r['file']);before=rgba(OLD/f'candidates/{ident}-v02.png');assert list(im.size)==b['dimensions'];assert sha(ROOT/r['file'])==r['sha256']
 assert im.getchannel('A').getextrema()==(255,255)
 if 'B01' in ident:assert (ROOT/r['file']).read_bytes()==(OLD/f'candidates/{ident}-v02.png').read_bytes()
 main=im.size==(314,206)
 if main:
  p=rgb(ROOT/f'previews/{ident}-v03-4x.png');assert p.size==(1256,824)
  assert p.tobytes()==im.convert('RGB').resize((1256,824),Image.Resampling.NEAREST).tobytes()
  pair(before,im,f'{ident}-v02-v03-4x.png',4)
  comparison=Image.new('RGB',(1256,206));comparison.paste(im.convert('RGB'),(0,0))
  for j,ref in enumerate(['A01-restroom.png','chapter-01-foyer.png','chapter-02-groundskeeper.png'],1):comparison.paste(rgb(ROOT/'references'/ref),(314*j,0))
  comparison.save(ROOT/f'comparisons/{ident}-style.png')
  comparison.resize((5024,824),Image.Resampling.NEAREST).save(ROOT/f'comparisons/{ident}-style-4x.png')
 pair(before,im,f'{ident}-v02-v03.png')
 # Allowed edit masks include removal of prior additions, not just new pixels.
 allowed=Image.new('L',im.size)
 if 'B02' in ident:allowed=ImageChops.lighter(rgba(OLD/'layers/B02-additions.png').getchannel('A'),rgba(ROOT/'layers/B02-left-unit-paper.png').getchannel('A'))
 elif 'B03' in ident:allowed=ImageChops.lighter(rgba(OLD/'layers/B03-additions.png').getchannel('A'),rgba(ROOT/'layers/B03-left-unit-paper.png').getchannel('A'))
 elif 'B06' in ident:
  allowed=ImageChops.lighter(rgba(OLD/'layers/B02-additions.png').getchannel('A'),rgba(OLD/'layers/B06-emergency-additions.png').getchannel('A'))
  allowed=ImageChops.lighter(allowed,rgba(ROOT/'layers/B06-silhouette-occluded-additions.png').getchannel('A'))
 elif 'B04' in ident:
  d=ImageDraw.Draw(allowed)
  for box in [(102,130,143,146),(123,56,142,194),(198,125,207,136)]:d.rectangle(box,fill=255)
 elif 'B05' in ident:
  d=ImageDraw.Draw(allowed)
  for box in [(8,196,73,241),(51,18,73,277),(180,195,204,223)]:d.rectangle(box,fill=255)
 changed=Image.new('L',im.size);unexpected=0;coords=[]
 for y in range(im.height):
  for x in range(im.width):
   if im.getpixel((x,y))!=before.getpixel((x,y)):
    coords.append([x,y]);changed.putpixel((x,y),255)
    if not allowed.getpixel((x,y)):unexpected+=1
 assert unexpected==0,(ident,unexpected)
 allowed.save(ROOT/f'masks/{ident}-v02-v03-allowed.png');changed.save(ROOT/f'masks/{ident}-v02-v03-changed.png')
 write(f'sources/{ident}-v02-v03-coordinates.json',coords)
 q={'candidateId':ident,'dimensions':list(im.size),'mode':'RGB','alphaExtrema':[255,255],'opacity':'PASS','dimensionsCheck':'PASS','sha256':r['sha256'],'changedPixelsFromV02':len(coords),'allowedEditMask':f'masks/{ident}-v02-v03-allowed.png','actualChangeMask':f'masks/{ident}-v02-v03-changed.png','unexpectedChangesOutsideAllowedMask':unexpected,'noBaseResampling':True,'uniqueRGB':len(im.convert('RGB').getcolors(im.width*im.height)),'globalFilterApplied':False,'nativeGridAuthorship':'UNPROVEN for inherited/generated raster sources; explicit native edits are documented.','status':'generated','selected':False,'approved':False,'assetPath':None,'inspection':notes[ident]}
 if main:q['exact4xPreview']={'dimensions':[1256,824],'allBlocksExact':True}
 else:
  comp=im.copy();comp.alpha_composite(fg)
  for y in range(im.height):
   for x in range(im.width):
    if fg.getpixel((x,y))[3]:assert comp.getpixel((x,y))==fg.getpixel((x,y))
  dest=f'composites/{ident}-A03-idle.png';comp.convert('RGB').save(ROOT/dest)
  oldcomp=before.copy();oldcomp.alpha_composite(fg);pair(oldcomp,comp,f'{ident}-composite-v02-v03.png')
  c={'candidateId':ident,'file':dest,'sha256':sha(ROOT/dest),'foregroundSha256':fg_hash,'anchor':[0,0],'scale':1,'alphaValues':[0,255],'allForegroundPixelsExact':True};composites.append(c);q['composite']=c
 qa.append(q)

# Explicit protection checks, independent of the composition script.
a01=rgba(ROOT/'references/A01-restroom.png');a02=rgba(ROOT/'references/A02-restroom-bg.png')
protected=[]
for ident in ['CH3-B02-record-printer','CH3-B06-paper-emergency']:
 im=rgba(ROOT/f'candidates/{ident}-v03.png')
 for name in ['attendant-one-pixel-silhouette.png','microphone-silhouette.png','chair-visible-silhouette.png']:
  m=Image.open(ROOT/'masks'/name);n=0
  for y in range(206):
   for x in range(314):
    if m.getpixel((x,y)):n+=1;assert im.getpixel((x,y))==a01.getpixel((x,y)),(ident,name,x,y)
  protected.append({'candidate':ident,'mask':name,'protectedPixels':n,'changedProtectedPixels':0})
assert rgba(ROOT/'candidates/CH3-B02-record-printer-v03.png').crop((241,110,270,145)).tobytes()==a01.crop((241,110,270,145)).tobytes()
assert rgba(ROOT/'candidates/CH3-B03-record-printer-bg-v03.png').crop((453,119,564,270)).tobytes()==a02.crop((453,119,564,270)).tobytes()
# Evidence: paper is allowed within the old rectangle wherever no body exists.
mask=Image.open(ROOT/'masks/attendant-one-pixel-silhouette.png');em=rgba(ROOT/'layers/B06-silhouette-occluded-additions.png')
formerly_boxed=sum(1 for y in range(96,142) for x in range(201,245) if not mask.getpixel((x,y)) and em.getpixel((x,y))[3]>0)
assert formerly_boxed>0
pair(rgba(OLD/'candidates/CH3-B02-record-printer-v02.png').crop((176,110,274,151)),rgba(ROOT/'candidates/CH3-B02-record-printer-v03.png').crop((176,110,274,151)),'B02-printer-placement-8x.png',8)
pair(rgba(OLD/'candidates/CH3-B06-paper-emergency-v02.png').crop((193,94,272,147)),rgba(ROOT/'candidates/CH3-B06-paper-emergency-v03.png').crop((193,94,272,147)),'B06-former-rectangle-8x.png',8)
pair(rgba(OLD/'candidates/CH3-B06-paper-emergency-v02.png').crop((223,22,314,159)),rgba(ROOT/'candidates/CH3-B06-paper-emergency-v03.png').crop((223,22,314,159)),'B06-brush-motion-4x.png',4)
proof=Image.new('RGB',a01.size,'#1e343d');proof.paste(a01.convert('RGB'),mask=mask)
pair(a01.crop((195,94,242,144)),proof.crop((195,94,242,144)),'B06-attendant-trace-8x.png',8)
pair(rgba(ROOT/'candidates/CH3-B02-record-printer-v03.png'),rgba(ROOT/'candidates/CH3-B06-paper-emergency-v03.png'),'B02-B06-printer-continuity.png')
preservation={'priorBatchBFiles':len(read('sources/prior-package-pins.json')['files']),'canonicalHistoricalReviewFiles':len(read('sources/history-pins.json')['files']),'archivedBatchAFiles':len(read('sources/batch-a-archive-pins.json')['files']),'selectedStoryAuthorityFiles':len(read('sources/protected-files.json')['files']),'result':'PASS; all pinned files byte-identical. A01 v09 unchanged; A03 foreground unchanged. No production registry, narrative or gameplay edits.'}
report={'result':'PASS for dimensions, opacity, exact integer previews, allowed masks, foreground and history preservation.','nativeGridAuthorship':'UNPROVEN / NOT PASSED for source rasters; inherited limitation retained.','crossChapterStyleApproval':'PENDING NATE','candidates':qa,'composites':composites,'protectedPixelChecks':protected,'pixelsOfPaperInsideFormerRectanglesOutsideActualBody':formerly_boxed,'rectangularAttendantProtection':'REMOVED; binary manually traced row-run silhouette only, plus separate actual mic/chair silhouettes; no feathering.','plantRestoration':'Entire original plant regions are byte-identical in B02 and B03. Original plant remains the B06 base; added paper naturally occludes parts. Generated plant pixels were excluded.','scannerDoorSlits':edits['scannerDoorSlits'],'preservation':preservation,'v03Generation':generation}
write('qa.json',report)
manifest={'version':'Batch B v03 localized corrections','sourceCommit':'2699abbd651817961b76d87fa0d4c78a57b04bc5','branch':'art/ch3-pavilion-batch02-20261119','currentCandidateCount':6,'status':'generated/unselected','selected':False,'approved':False,'assetPath':None,'candidates':records,'composites':composites,'preservation':preservation,'productionRegistryChanged':False,'gameplayIntegrated':False,'nativeGridAuthorship':'UNPROVEN'}
write('manifest.json',manifest)
(ROOT/'CANDIDATE_HASHES.md').write_text('| Candidate | SHA-256 |\n|---|---|\n'+''.join(f"| {r['candidateId']} | `{r['sha256']}` |\n" for r in records))

def art(path,w,h,main=False,alt='Review proof'):
 return f'<div class="viewport"><img class="{"scene-art" if main else "portrait-art"}" src="{path}" width="{w}" height="{h}" data-w="{w}" data-h="{h}" alt="{html.escape(alt)}"></div>'
cards=[]
for r,q in zip(records,qa):
 ident=r['candidateId'];w,h=r['dimensions'];main=w==314
 card=f'<article class="candidate" id="{ident}"><h2>{ident}</h2><p><strong>Generated / unselected</strong> · {w}×{h}</p>'+art(r['file'],w,h,main)+f'<p class="meta">SHA-256: <code>{r["sha256"]}</code></p><ul>'+''.join('<li>'+html.escape(n)+'</li>' for n in notes[ident])+'</ul><h3>v02 / v03</h3><p>Left: preserved v02. Right: localized v03.</p>'+art(f'comparisons/{ident}-v02-v03.png',w*2,h,main)
 if main:card+=f'<p><a href="previews/{ident}-v03-4x.png">Exact 4× candidate</a> · <a href="comparisons/{ident}-v02-v03-4x.png">Exact 4× before/after</a></p><h3>Approved pixel-style references</h3><p>Candidate, approved A01, Chapter 1 foyer, Chapter 2 groundskeeper. Style acceptance remains Nate’s release gate.</p>'+art(f'comparisons/{ident}-style.png',1256,206,True)
 else:card+='<h3>Unchanged A03 foreground — before / after</h3><p>Both composites use the approved foreground at(0,0), scale1, original binary alpha.</p>'+art(f'comparisons/{ident}-composite-v02-v03.png',1128,278)+f'<p><a href="composites/{ident}-A03-idle.png">Current native composite</a></p>'
 if 'B02' in ident:card+='<h3>Printer placement and restored plant · 8×</h3>'+art('comparisons/B02-printer-placement-8x.png',1568,328)
 if 'B06' in ident:
  card+='<h3>Former rectangular mask area · 8×</h3><p>Old v02 / current v03. Paper may occupy background within the former box; only actual object silhouettes protect pixels.</p>'+art('comparisons/B06-former-rectangle-8x.png',1264,424)+'<h3>Actual attendant trace · 8×</h3><p>Approved source crop / exact pixels selected by the traced binary silhouette.</p>'+art('comparisons/B06-attendant-trace-8x.png',752,400)+'<h3>Brush contact and exitward paper · 4×</h3>'+art('comparisons/B06-brush-motion-4x.png',728,548)
 card+=f'<p><a href="{q["allowedEditMask"]}">Allowed v02→v03 edit mask</a> · <a href="{q["actualChangeMask"]}">Actual changed-pixel mask</a> · <a href="sources/{ident}-v02-v03-coordinates.json">Exact change coordinates</a></p><p>Unexpected changes outside allowed mask: <strong>0</strong>. RGB colors: {q["uniqueRGB"]:,}, diagnostic only. No global palette filter or sharpening.</p></article>'
 cards.append(card)
style='*{box-sizing:border-box;min-width:0}body{margin:0;background:#15252a;color:#f3e9d9;font:16px/1.55 system-ui}main{max-width:1380px;margin:auto;padding:24px}p,li,a,code,h1,h2,h3{overflow-wrap:anywhere}a{color:#9de0db}.viewport{width:100%;max-width:100%;overflow:auto;background:#091519;border:1px solid #55727a}.viewport img{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}.candidate{border-top:1px solid #55727a;margin-top:36px;padding-top:18px}.controls{position:sticky;top:0;z-index:2;display:flex;flex-wrap:wrap;gap:12px;padding:12px 0;background:#15252afa}button{font:inherit;padding:10px 16px;border:1px solid #819c9f;background:#25444d;color:inherit;border-radius:4px}button[aria-pressed=true]{background:#f4d3ac;color:#17272c}.notice{padding:16px;background:#563e31;border-left:4px solid #f0b984}.meta{font-size:14px;color:#c5d5d6}nav{display:flex;flex-wrap:wrap;gap:12px}li{margin:8px 0}'
nav=''.join(f'<a href="#{r["candidateId"]}">{r["candidateId"]}</a>' for r in records)
page=f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 3 Batch B v03</title><style>{style}</style><main><h1>Chapter 3 Batch B — localized v03 corrections</h1><p><strong>Generated / unselected. Awaiting Nate’s Art Director review.</strong></p><p>The existing left cream desk unit is the sole printer housing. The plant is restored. B06 uses a traced attendant silhouette, fewer receipts, and visible brush supports/contact. Scanner views share a nearly closed door and document-intake direction. B01 is byte-identical to v02.</p><p class="notice">Original native-grid authorship remains unproven. Approved room pixels are not rerendered, resized, recolored or sharpened. This pass combines explicit native pixel edits and one oversized transparent addition source, retained unchanged with its actual dimensions. Paper/brush source softness remains a visual-review limitation.</p><nav>{nav}<a href="qa.json">Technical QA</a><a href="manifest.json">Manifest</a><a href="PMO-HANDOFF.md">PMO handoff</a></nav><div class="controls"><button data-scale="1" aria-pressed="true">Main scenes · native 1×</button><button data-scale="4" aria-pressed="false">Main scenes · exact 4×</button></div><p>Portrait backgrounds/composites remain native 564×278. Comparison rows and close-ups scroll at their exact integer size; no fit-to-width scaling.</p>'+''.join(cards)
page+='<h2>Same housing before / during emergency</h2>'+art('comparisons/B02-B06-printer-continuity.png',628,206,True)
page+='<h2>Source and preservation records</h2><p><a href="sources/localized-edit-records.json">Construction / dimensions / base hashes</a> · <a href="sources/v03-generation-record.json">New addition source / actual dimensions / hash</a> · <a href="prompts/emergency-transparent-additions.txt">Exact new submitted prompt</a> · <a href="sources/attendant-silhouette-row-runs.json">Manual silhouette coordinates</a> · <a href="masks/attendant-one-pixel-silhouette.png">Binary attendant silhouette</a> · <a href="layers/B06-silhouette-occluded-additions.png">Final transparent emergency additions</a> · <a href="sources/prior-package-pins.json">All prior Batch B hashes</a> · <a href="sources/protected-files.json">Protected production/narrative hashes</a> · <a href="sources/batch-a-archive-pins.json">Historical Batch A hashes</a> · <a href="../v02-additive-continuity/">Preserved v02 gallery / full original catalogue prompts and source provenance</a> · <a href="CANDIDATE_HASHES.md">Candidate hashes</a> · <a href="PNG_SHA256SUMS.txt">PNG checksums</a> · <a href="SOURCE_SHA256SUMS.txt">Package checksums</a> · <a href="browser-qa.json">Browser QA</a></p><p>All historical and approved artwork, A01 v09, the four portrait assets, narrative, registry and gameplay remain unchanged. No approvals, integration, merge or Batch C. Stop for Nate’s visual review.</p></main><script>document.querySelectorAll("[data-scale]").forEach(b=>b.onclick=()=>{const s=Number(b.dataset.scale);document.querySelectorAll("img.scene-art").forEach(i=>{i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s});document.querySelectorAll("[data-scale]").forEach(n=>n.setAttribute("aria-pressed",String(n===b)))});</script></html>'
(ROOT/'index.html').write_text(page)
(ROOT/'README.md').write_text('''# Chapter 3 Batch B v03 — localized corrections

Run `python3 compose_v03.py`, then `python3 build_review.py`. Native edits, source transfer, object traces and all coordinates are explicit. Prior v01/v02 packages and approved pixels are never written. Full catalogue prompts and initial generation records remain linked in the preserved v02 package. One new built-in transparent-addition generation is documented separately; it is not a full-scene rerender.

All six candidates remain generated/unselected. B01 is byte-identical. Original native-grid authorship remains unproven. Main scenes314×206, exact4×; closer backgrounds564×278; A03 unchanged at(0,0),scale1. No production registry/gameplay/narrative changes or Batch C.
''')
(ROOT/'PNG_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(ROOT).as_posix()}\n' for p in sorted(ROOT.rglob('*.png'))))
(ROOT/'SOURCE_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(ROOT).as_posix()}\n' for p in sorted(ROOT.rglob('*')) if p.is_file() and p.suffix!='.png' and p.name!='SOURCE_SHA256SUMS.txt'))
print(json.dumps({'preservation':preservation,'protectedPixels':protected,'paperInsideFormerBoxOutsideBody':formerly_boxed,'candidates':[{'id':q['candidateId'],'sha256':q['sha256'],'changedFromV02':q['changedPixelsFromV02']} for q in qa]},indent=2))
