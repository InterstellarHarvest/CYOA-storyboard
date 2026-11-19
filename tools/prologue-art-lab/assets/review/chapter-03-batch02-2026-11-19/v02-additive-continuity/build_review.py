"""Six Batch B candidates; honest source sizes, unchanged A03 and review-only proofs."""
from pathlib import Path
from PIL import Image
import hashlib,json,html,os
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[5]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads((ROOT/p).read_text())
def write(p,obj):(ROOT/p).write_text(json.dumps(obj,indent=2)+'\n')
brief=read('sources/briefs.json');generation_records=read('sources/generation-records.json');notes=read('sources/current-visual-inspection.json')
composition=read('sources/additive-edit-records.json');composed={c['candidateId']:c for c in composition['candidates']};records=[]
for original in generation_records:
 c=composed[original['candidateId']];r=dict(original);r['candidate']=c['candidate'];r['candidateSha256']=c['sha256'];r['additiveComposition']=c;r['originalGenerationRecord']=original;r['status']='generated';r['selected']=False;r['approved']=False;r['assetPath']=None
 if r['preview4x']:r['preview4x']=r['preview4x'].replace('-v01-','-v02-')
 records.append(r)
for f in read('sources/v01-study-pins.json')['files']:assert sha(ROOT.parent/f['file'])==f['sha256'],f['file']
for c in composition['candidates']:
 assert sha(ROOT/c['base'])==c['baseSha256']
 if 'overlay' in c:
  before=Image.open(ROOT/c['base']).convert('RGBA');overlay=Image.open(ROOT/c['overlay']).convert('RGBA');after=Image.open(ROOT/c['candidate']).convert('RGBA')
  assert sha(ROOT/c['overlay'])==c['overlaySha256']
  expected=before.copy();expected.alpha_composite(overlay);assert after.tobytes()==expected.tobytes()
  assert all(after.getpixel((x,y))==before.getpixel((x,y)) for y in range(after.height) for x in range(after.width) if overlay.getpixel((x,y))[3]==0)
for extra in read('sources/paper-layer-generation-records.json'):
 assert sha(ROOT/extra['source'])==extra['sourceSha256'];assert sha(ROOT/extra['workingLayer'])==extra['workingLayerSha256'];assert sha(ROOT/extra['submittedPrompt'])==extra['submittedPromptSha256']

ids=[b['candidateId'] for b in brief['candidates']]
assert len(records)==6 and [r['candidateId'] for r in records]==ids
catalogue=read('sources/canonical/story/artwork.draft.json')
direction=(ROOT/'prompts/canonical-direction.txt').read_text()
assert direction==catalogue['direction']+'\n'
for filename in ['sources/history-pins.json','sources/protected-files.json']:
 for f in read(filename)['files']:assert sha(REPO/f['file'])==f['sha256'],f['file']
archive=Path(os.environ.get('CH3_BATCH_A_ARCHIVE_ROOT',str(REPO.parent/'CYOA-ch3-art-batch01')))
archive_pins=read('sources/batch-a-archive-pins.json')
for f in archive_pins['files']:assert sha(archive/f['file'])==f['sha256'],f['file']
for f in read('sources/reference-manifest.json'):
 assert sha(ROOT/f['file'])==f['sha256']
 if 'repositoryPath' in f:assert sha(REPO/f['repositoryPath'])==f['sha256']
fg=Image.open(ROOT/'references/A03-attendant.png').convert('RGBA')
assert fg.size==(564,278) and set(fg.getchannel('A').getdata())=={0,255}
foreground_hash=sha(ROOT/'references/A03-attendant.png')
assert foreground_hash=='28fdf5523454ea2ccdb397bd4d7006fc1fb8f04109046b7646361692422c3ef2'
def art(path,w,h,alt,scene=False):
 cls='scene-art' if scene else 'portrait-art'
 return f'<div class="viewport"><img class="{cls}" src="{path}" width="{w}" height="{h}" data-w="{w}" data-h="{h}" alt="{html.escape(alt)}"></div>'
cards=[];qa=[];composites=[]
for item,r in zip(brief['candidates'],records):
 ident=r['candidateId'];main=item['kind']=='scene';im=Image.open(ROOT/r['candidate']).convert('RGB');raw=Image.open(ROOT/r['source'])
 assert list(im.size)==item['dimensions'] and list(raw.size)==r['actualSourceDimensions']
 assert sha(ROOT/r['source'])==r['sourceSha256'] and sha(ROOT/r['candidate'])==r['candidateSha256']
 submitted=(ROOT/r['submittedPrompt']).read_text();assert sha(ROOT/r['submittedPrompt'])==r['submittedPromptSha256']
 key=item['record'].split(':',1)[1].split('#')[0];expected=catalogue['scenes'][key]
 if not main:expected=expected['portraitBackground']
 exact=(ROOT/item['prompt']).read_text();assert exact==expected['prompt']+'\n';assert expected['prompt'] in submitted and catalogue['direction'] in submitted
 for ref in r['referencesInOrder']:assert sha(ROOT/ref['file'])==ref['sha256']
 assert raw.convert('RGBA').getchannel('A').getextrema()==(255,255)
 q={'candidateId':ident,'workingDimensions':list(im.size),'workingMode':im.mode,'sourceDimensions':list(raw.size),'sourceMode':raw.mode,'opacity':{'result':'PASS','sourceAlphaExtrema':[255,255],'workingAlphaExtrema':[255,255]},'workingDimensionCheck':'PASS','requestedGeneratorSourceDimensions':'FAIL' if r['derivedExport'] else 'PASS','originalNativeGridAuthorship':'UNPROVEN / NOT PASSED; this export does not establish original grid authorship.','palette':{'sourceUniqueRGB':len(raw.convert('RGB').getcolors(raw.width*raw.height)),'workingUniqueRGB':len(im.getcolors(im.width*im.height)),'quantizationApplied':False,'numericPaletteLimit':None},'exactCataloguePromptIncluded':True,'exactSharedDirectionIncluded':True,'selected':False,'approved':False,'assetPath':None,'visualInspection':notes[ident]}
 proof=''
 if main:
  p=Image.open(ROOT/r['preview4x']).convert('RGB');assert p.size==(1256,824)
  pixels=p.load();source=im.load()
  assert all(pixels[4*x+dx,4*y+dy]==source[x,y] for y in range(206) for x in range(314) for dx in range(4) for dy in range(4))
  q['preview4x']={'result':'PASS','dimensions':[1256,824],'every4x4BlockMatches':True}
  compare=Image.new('RGB',(1256,206));compare.paste(im,(0,0))
  for n,name in enumerate(['A01-restroom.png','chapter-01-foyer.png','chapter-02-groundskeeper.png'],1):compare.paste(Image.open(ROOT/'references'/name).convert('RGB'),(314*n,0))
  compare.save(ROOT/f'comparisons/{ident}-style.png');compare.resize((5024,824),Image.Resampling.NEAREST).save(ROOT/f'comparisons/{ident}-style-4x.png')
  proof=f'<p><a href="{r["preview4x"]}">Exact 1256×824 / 4× preview</a></p><h3>Cross-chapter pixel-style comparison</h3><p class="meta">Left to right: this candidate, approved Batch A A01, approved Chapter 1 foyer, approved Chapter 2 groundskeeper. Every panel is 314×206 at 1× or 1256×824 at 4×. Cross-chapter visual consistency is a release gate pending Nate; the comparison is not an automatic style approval.</p>'+art(f'comparisons/{ident}-style.png',1256,206,'Candidate and approved cross-chapter scenes',True)+f'<p><a href="comparisons/{ident}-style-4x.png">Full comparison at exact 4×</a></p>'
 else:
  result=im.convert('RGBA');result.alpha_composite(fg,(0,0));rgb=result.convert('RGB')
  for y in range(278):
   for x in range(564):
    front=fg.getpixel((x,y));assert rgb.getpixel((x,y))==(front[:3] if front[3]==255 else im.getpixel((x,y)))
  file=f'composites/{ident}-A03-idle.png';rgb.save(ROOT/file)
  pair=Image.new('RGB',(1128,278));pair.paste(im,(0,0));pair.paste(rgb,(564,0));pair.save(ROOT/f'composites/{ident}-background-composite.png')
  rois={'printerRightFace':[430,211,540,264],'receiptTail':[418,266,439,277]} if 'B03' in ident else {'greenAuthorizationLamp':[119,100,144,126],'exposedRollerCore':[165,149,222,179]}
  metrics=[]
  for label,box in rois.items():
   count=sum(fg.getpixel((x,y))[3]>0 for y in range(box[1],box[3]) for x in range(box[0],box[2]));area=(box[2]-box[0])*(box[3]-box[1]);metrics.append({'label':label,'box':box,'foregroundOverlapPixels':count,'area':area,'percentOverlap':round(count/area*100,2)})
  c={'backgroundCandidate':ident,'file':file,'sha256':sha(ROOT/file),'foreground':'references/A03-attendant.png','foregroundSha256':foreground_hash,'foregroundAlphaValues':[0,255],'anchor':[0,0],'translation':[0,0],'scale':1,'rotation':0,'foregroundBounds':list(fg.getchannel('A').getbbox()),'dimensions':[564,278],'allForegroundPixelsExact':True,'regionInspection':metrics,'purpose':'Approved idle foreground used as fixed-anchor compositing test only; no new pose generation.'};composites.append(c);q['composite']={'result':'PASS for exact anchoring, binary-alpha transfer and pixel preservation','proof':c}
  proof='<h3>Fixed-anchor composite proof</h3><p class="meta">Left: independently generated background. Right: exact approved A03 idle foreground at(0,0), scale1. No foreground translation, resizing, alpha thresholding or repainting. The idle pose is only the requested anchor test.</p>'+art(f'composites/{ident}-background-composite.png',1128,278,'Native background and unchanged approved foreground composite')+f'<p><a href="{file}">Native 564×278 composite PNG</a></p>'
 c=composed[ident]
 if 'overlay' in c:
  base_im=Image.open(ROOT/c['base']).convert('RGB');side=Image.new('RGB',(im.width*2,im.height));side.paste(base_im,(0,0));side.paste(im,(im.width,0));side.save(ROOT/f'comparisons/{ident}-base-and-additions.png')
  proof+='<h3>Pixel-preserving construction</h3><p>Left: immutable base. Right: base plus only the transparent additions. Zero pixels change outside the addition alpha mask. The original base was not resized or repainted.</p>'+art(f'comparisons/{ident}-base-and-additions.png',im.width*2,im.height,'Immutable base and additive variant',main)+f'<p>Base SHA-256: <code>{c["baseSha256"]}</code> · <a href="{c["overlay"]}">Transparent additions PNG</a> · <a href="comparisons/{ident}-addition-mask.png">Exact addition mask</a></p>'
  q['pixelPreservation']={'result':'PASS','base':c['base'],'baseSha256':c['baseSha256'],'overlay':c['overlay'],'overlaySha256':c['overlaySha256'],'baseResampled':False,'unexpectedChangesOutsideOverlay':0}
 q['workingPaletteInterpretation']='Diagnostic only; no fixed color-count gate and no automatic palette filtering. Native clustering and residual softness require visual review.';qa.append(q)
 observed=''.join('<li>'+html.escape(n)+'</li>' for n in notes[ident]['observations']);issues=''.join('<li>'+html.escape(n)+'</li>' for n in notes[ident]['reviewIssues'])
 cards.append(f'''<article class="candidate" id="{ident}"><h2>{ident}</h2><p><strong>Generated / unselected</strong> · {item['record']} · {im.width}×{im.height}</p>{art(r['candidate'],im.width,im.height,ident+' current candidate',main)}
<p class="meta">Candidate SHA-256: <code>{r['candidateSha256']}</code></p><p class="notice">Untouched generator source: <strong>{raw.width}×{raw.height}</strong>. {'Generated study/source is retained for provenance; the current construction method is shown in the immutable-base proof below.' if r['derivedExport'] else 'The returned source has the target dimensions.'} Original native-grid authorship remains unproven.</p><p><a href="{r['candidate']}">Working PNG</a> · <a href="{r['source']}">Untouched source / {r['originalSourceFilename']}</a> · <a href="{r['submittedPrompt']}">Full submitted prompt</a> · <a href="{item['prompt']}">Exact catalogue prompt</a></p>{proof}<h3>Visual inspection</h3><ul>{observed}</ul><h3>Art Director attention</h3><ul>{issues}</ul><p class="meta">Working palette: {q['palette']['workingUniqueRGB']:,} distinct RGB values; no palette quantization. Source nodes: {', '.join(item['sourceNodes'])}.</p><details><summary>Exact registered prompt</summary><pre>{html.escape(exact)}</pre></details></article>''')
pair=Image.new('RGB',(628,206));pair.paste(Image.open(ROOT/'candidates/CH3-B02-record-printer-v02.png'),(0,0));pair.paste(Image.open(ROOT/'candidates/CH3-B06-paper-emergency-v02.png'),(314,0));pair.save(ROOT/'comparisons/printer-paper-emergency.png');pair.resize((2512,824),Image.Resampling.NEAREST).save(ROOT/'comparisons/printer-paper-emergency-4x.png')
initial=read('sources/initial-attempts/generation-records.json')
for r in initial:
 assert sha(ROOT/r['source'])==r['sourceSha256'];assert sha(ROOT/r['candidate'])==r['candidateSha256'];assert sha(ROOT/r['submittedPrompt'])==r['submittedPromptSha256']
total_calls=sum(r['generationCalls'] for r in generation_records+initial)+sum(r['generationCalls'] for r in read('sources/paper-layer-generation-records.json'))
preservation={'canonicalReviewFiles':len(read('sources/history-pins.json')['files']),'BatchAHistoricalReviewFiles':len(archive_pins['files']),'selectedStoryAndAuthorityFiles':len(read('sources/protected-files.json')['files']),'result':'PASS; immutable hashes match. No existing file is edited except the review-only workflow.'}
write('qa.json',{'exportOpacityPreviewAndPreservation':'PASS','originalNativeGridAuthorship':'UNPROVEN / NOT PASSED for all six; actual sources are oversized.','crossChapterVisualConsistency':'PENDING NATE; mandatory release review, not an automatic QA pass.','generationCalls':total_calls,'currentCandidateCount':6,'supersededUnselectableAttempts':len(initial),'candidates':qa,'composites':composites,'preservation':preservation,'noProductionRegistration':True,'additiveConstruction':composition,'twoPersonRestroomSigns':'PASS by manual inspection; approved A01/A02 symbols are retained, and B04 uses approved two-person glyphs.','frozenV01StudyFiles':len(read('sources/v01-study-pins.json')['files'])})
write('manifest.json',{'version':'Batch B v02 — additive continuity','date':'2026-11-19','canonicalCommit':brief['canonicalCommit'],'narrativeBlob':brief['narrativeBlob'],'branch':brief['branch'],'method':'Built-in image_gen.imagegen; exact catalogue prompts and canonical direction retained.','generationCalls':total_calls,'currentCandidateCount':6,'ownerCorrection':'All restroom signs show two people. Repeated views reuse immutable approved pixels with transparent additions only.','additiveConstruction':composition,'status':'generated/unselected','approved':False,'selected':False,'candidates':[{**b,**r} for b,r in zip(brief['candidates'],records)],'composites':composites,'preservation':preservation,'supersededStudies':'sources/initial-attempts/generation-records.json','originalNativeAuthorship':'UNPROVEN. Do not interpret dimensionally correct derived exports as proof of native authorship.','productionRegistryChanged':False,'gameplayIntegrated':False})
(ROOT/'CANDIDATE_HASHES.md').write_text('| Candidate | SHA-256 |\n|---|---|\n'+''.join(f"| {r['candidateId']} | `{r['candidateSha256']}` |\n" for r in records))
ref_html=''
for name,label in [('A01-restroom.png','Approved A01 restroom'),('A02-restroom-bg.png','Approved A02 closer background'),('A03-attendant.png','Approved A03 foreground — reused unchanged'),('A04-verification.png','Approved A04 stage'),('A05-verification-bg.png','Approved A05 closer background'),('A06-presenter.png','Approved A06 foreground — reference only')]:
 im=Image.open(ROOT/'references'/name);ref_html+=f'<figure><figcaption>{label}</figcaption>'+art('references/'+name,im.width,im.height,label,im.size==(314,206))+'</figure>'
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 3 Batch B — additive continuity / v02</title><style>*{box-sizing:border-box;min-width:0}p,h1,h2,h3,li,a,figcaption,summary{overflow-wrap:anywhere}body{margin:0;background:#15252a;color:#f3e9d9;font:16px/1.55 system-ui,sans-serif}main{max-width:1380px;margin:auto;padding:24px}h1{font-size:30px;line-height:1.2}h2{font-size:23px;overflow-wrap:anywhere}h3{font-size:19px}a{color:#9de0db;overflow-wrap:anywhere}code{overflow-wrap:anywhere}nav,.controls{display:flex;flex-wrap:wrap;gap:12px;margin:18px 0}.controls{position:sticky;top:0;background:#15252af5;padding:12px 0;z-index:2}button{font:inherit;padding:9px 16px;border:1px solid #819c9f;background:#25444d;color:inherit;border-radius:4px;cursor:pointer}button[aria-pressed=true]{background:#f4d3ac;color:#17272c}.notice{padding:16px;background:#563e31;border-left:4px solid #f0b984}.viewport{width:100%;max-width:100%;overflow:auto;background:#091519;border:1px solid #55727a}.viewport img{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}.candidate{border-top:1px solid #55727a;margin-top:36px;padding-top:18px}.meta{color:#c5d5d6;font-size:14px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#0c1c20;padding:18px;font-size:13px}li{margin:8px 0}figure{margin:18px 0;max-width:100%}figcaption{margin:8px 0}</style>
<main><h1>Chapter 3 Batch B — additive continuity v02</h1><p><strong>Generated / unselected · no approval, registration or integration</strong></p><p>Four 314×206 main scenes and two 564×278 conversation backgrounds. Repeated views reuse approved A01/A02 pixels exactly, with only transparent new-object additions; genuinely different camera views remain independent. A03 is reused unchanged for both fixed-anchor tests. Canonical source: 3ac5422; narrative blob remains 857ffdf1bc9432cf4bbbfd7819f5f430a06d9036.</p>
<p class="notice"><strong>Technical limitation:</strong> generator sources were larger than requested. Untouched originals and actual dimensions are preserved. Original native-grid authorship remains unproven. Approved bases are immutable; generated source-derived additions, their masks and native primitives are documented separately. Residual RGB softness remains. Cross-chapter 4× visual consistency requires Nate’s release review.</p>
<nav>NAV_LINKS<a href="#composites">Composite notes</a><a href="#references">Approved Batch A references</a><a href="manifest.json">Manifest / hashes</a><a href="qa.json">Technical QA</a></nav>
<div class="controls"><button data-scale="1" aria-pressed="true">Main scenes · native 1×</button><button data-scale="4" aria-pressed="false">Main scenes · exact 4×</button></div><p class="meta">Portrait backgrounds and composite proofs always remain at native 564×278. Main scenes and cross-chapter comparison rows use the chosen exact integer scale; large rows scroll without fit-to-width shrinking.</p>
CARDS
<section id="composites"><h2>Composite and continuity review notes</h2><p>The approved A03 PNG is reused byte-for-byte at(0,0), scale1, with its binary alpha unchanged. Scanner close-view hardware was moved to the left through a new generation after the first attempt was obscured by the foreground. No foreground was moved or regenerated.</p><p>The printer close-up now reuses approved A02 and adds the printer wholly to the right of A03. No optional ORIGINAL lettering is emitted in this view; paper uses non-letter form marks. All bathroom signage uses the approved two-person family.</p><p><a href="../v01/index.html">Frozen superseded v01 studies</a> · <a href="sources/additive-edit-records.json">Immutable-base/overlay construction records</a> · <a href="sources/owner-continuity-correction.md">Owner correction</a> · <a href="sources/paper-layer-generation-records.json">Transparent paper-source provenance</a> · <a href="sources/initial-attempts/generation-records.json">Superseded scanner attempt — provenance only, unselectable</a> · <a href="sources/initial-attempts/CH3-B05-initial-composite.png">Initial occlusion proof</a></p><h3>Same printer room before / during paper emergency</h3>CONTINUITY</section>
<section id="references"><h2>Approved Batch A — read-only references</h2><p>The six approved selections are unchanged. Foreground previews below retain original alpha; only A03 is reused in the two composite tests.</p>REFERENCE_IMAGES</section>
<h2>Source and preservation records</h2><p><a href="sources/generation-records.json">Generation records / original filenames / actual sizes</a> · <a href="sources/briefs.json">Exact registry mappings and source nodes</a> · <a href="prompts/canonical-direction.txt">Verbatim canonical direction</a> · <a href="sources/reference-manifest.json">Approved reference hashes</a> · <a href="sources/protected-files.json">Selected artwork / narrative / registry hashes</a> · <a href="sources/history-pins.json">Canonical historical review hashes</a> · <a href="sources/batch-a-archive-pins.json">Immutable Batch A review archive hashes</a> · <a href="sources/baseline-tests.json">Canonical baseline checks</a> · <a href="CANDIDATE_HASHES.md">Six candidate hashes</a> · <a href="PNG_SHA256SUMS.txt">PNG checksums</a> · <a href="SOURCE_SHA256SUMS.txt">Package checksums</a> · <a href="browser-qa.json">Browser checks</a></p>
<p>Nine generation calls supplied the source studies and two transparent paper layers for six current additive candidates. The first full-scene v01 renders are frozen superseded studies and are not selectable current candidates. No new inventory, death-popup image, Focus A, human pose or next-batch artwork was generated. Production asset paths, narrative, dialogue, choices, checks, endings and all approved artwork remain unchanged.</p><p><strong>Stop for Nate’s visual review.</strong> Selection will constitute approval; approval registration is a separate Claude handoff. Batch C and D have not begun.</p></main><script>document.querySelectorAll('[data-scale]').forEach(b=>b.onclick=()=>{const s=Number(b.dataset.scale);document.querySelectorAll('img.scene-art').forEach(i=>{i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s});document.querySelectorAll('[data-scale]').forEach(n=>n.setAttribute('aria-pressed',String(n===b)));});</script></html>'''
page=page.replace('NAV_LINKS',''.join(f'<a href="#{i}">{i}</a>' for i in ids)).replace('CARDS','\n'.join(cards)).replace('CONTINUITY',art('comparisons/printer-paper-emergency.png',628,206,'Printer room before and during harmless emergency',True)).replace('REFERENCE_IMAGES',ref_html)
(ROOT/'index.html').write_text(page)
(ROOT/'README.md').write_text('''# Chapter 3 Batch B v02 — additive continuity

Six current generated/unselected candidates, created with built-in imagegen from verbatim registry prompts and canonical direction at commit 3ac5422. One superseded scanner-background attempt is retained separately; it is not a selectable seventh candidate.

All source rasters were oversized. Untouched originals, source dimensions, exact prompts, filenames and hashes are in `sources/generation-records.json`. Working files are honest target-size derivatives, not proof of original native-grid authorship. No sharpening, global palette filter or hidden pixelation pass was applied.

`prepare_paper_layers.py` reconstructs source-derived transparent paper additions; `compose_additive.py` composes immutable approved bases plus only new layers. Only newly added objects are transformed; no approved base or foreground is resized or repainted. `python3 build_review.py` validates source/prompt/reference hashes, original protected files, exact 4x main-scene blocks and unchanged approved A03 foreground pixels at(0,0), scale1. The historical Batch A archive root can be supplied with CH3_BATCH_A_ARCHIVE_ROOT; its immutable source commit is a87155b. The workflow checks and republishes that archive without changing its files.

Run `qa-browser.cjs`, then rebuild checksum lists. Main scenes and cross-chapter comparisons have 1x/4x controls; portraits and composites remain at native564x278. All six candidates await Nate. No registration, production paths, gameplay integration, merge or Batch C/D work.
''')
(ROOT/'PNG_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(ROOT).as_posix()}\n' for p in sorted(ROOT.rglob('*.png'))))
(ROOT/'SOURCE_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(ROOT).as_posix()}\n' for p in sorted(ROOT.rglob('*')) if p.is_file() and p.suffix!='.png' and p.name!='SOURCE_SHA256SUMS.txt'))
print(json.dumps({'currentCandidates':6,'generationCalls':total_calls,'preservation':preservation,'hashes':{r['candidateId']:r['candidateSha256'] for r in records},'compositeROIs':[c['regionInspection'] for c in composites]},indent=2))
