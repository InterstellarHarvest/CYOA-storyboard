"""Validate and publish a standalone local/Pages-compatible eight-candidate gallery."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,hashlib,subprocess,tarfile,io,html
R=Path(__file__).resolve().parent;REPO=R.parents[5]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads((R/p).read_text())
def write(p,o):(R/p).write_text(json.dumps(o,indent=2)+'\n')
def rgba(p):return Image.open(R/p).convert('RGBA')
def rgb(p):return Image.open(R/p).convert('RGB')
brief=read('sources/briefs.json');scene=read('sources/scene-assembly.json');fgs=read('sources/foreground-assembly.json');generation=read('sources/generation-records.json')
byid={r['candidateId']:r for r in scene+fgs};gens={r['candidateId']:r for r in generation};assert len(byid)==len(gens)==8
catalogue=read('sources/canonical/story/artwork.draft.json');direction=(R/'prompts/canonical-direction.txt').read_text();assert direction==catalogue['direction']+'\n'
assert subprocess.check_output(['git','hash-object','story/chapters/chapter-03.reboot-candidate.json'],cwd=REPO,text=True).strip()==brief['narrativeBlob']
for f in read('sources/protected-files.json')['files']:assert sha(REPO/f['file'])==f['sha256'],f['file']
for f in read('sources/reference-manifest.json'):
 assert sha(R/f['file'])==f['sha256'];assert sha(REPO/f['repositoryPath'])==f['sha256']
archive_count=0
for archive in read('sources/historical-review-pins.json')['archives']:
 data=subprocess.check_output(['git','archive',archive['sourceCommit'],archive['root']],cwd=REPO);expected={f['file']:f['sha256'] for f in archive['files']};got={}
 with tarfile.open(fileobj=io.BytesIO(data),mode='r:') as a:
  for f in a:
   if f.isfile():got[f.name]=hashlib.sha256(a.extractfile(f).read()).hexdigest()
 assert got==expected;archive_count+=len(got)

def row(paths,target):
 ims=[rgb(p) for p in paths];out=Image.new('RGB',(sum(i.width for i in ims),max(i.height for i in ims)),'#1d3038');x=0
 for im in ims:out.paste(im,(x,0));x+=im.width
 out.save(R/target);out.resize((out.width*4,out.height*4),Image.Resampling.NEAREST).save(R/target.replace('.png','-4x.png'));return out.size
def overlap(fg,box):
 return sum(fg.getpixel((x,y))[3]>0 for y in range(box[1],box[3]) for x in range(box[0],box[2]))

notes={
'CH3-C01-urgency':{'changes':['Approved stage composition with the owner-chosen red reveal/right-wall layout. Red inner curtains, genuine sink/mirror/stalls, rotating-deck cue, silver bell and a lone spectator.','Shared two-person sign, portrait-derived three-button panel and separate PA grille; no extra or relocated doorway.','Same right-front console as every other new main view, currently inactive.'],'attention':['Review whether the tiny hand bell reads clearly at 314×206.','The restroom glimpse is deliberately tantalizing; no protagonist or entry is shown.']},
'CH3-C02-urgency-bg':{'changes':['Independent close camera, using the same owner-selected curtain reveal and right-wall arrangement. The real restroom is visible.','The side chair and console are kept separate; the console is between the stage and chair, corresponding to the wide view.','No presenter baked into the background.'],'attention':['Check the main/close room correspondence, depth and console proportions in the paired proof.']},
'CH3-C03-locomotion':{'changes':['Same stage room, curtain opening, camera and fixed right-wall stack; teal curtains reveal landing/chairs/maintenance access through that opening.','Moving belt, soft padded pit, coarse unfolding net and stationary landing are separate readable shapes.','The common console stays at the same right-front origin, inactive.'],'attention':['Confirm the jump route and distinction between moving belt, padded pit and safe floor read immediately at native and 4×.']},
'CH3-C04-surprise':{'changes':['Same stage, with a raised platform, startled small presenter, early confetti and two lamps.','The fixed curtain opening now reveals backstage access; wall sign/panel/speaker remain identical to the other new mains.','Same console and button location; only its left button lights green.'],'attention':['Check the raised presenter’s stance and cannon/platform occlusion at 4×. The tiny scene figure remains source-derived.']},
'CH3-C05-surprise-bg':{'changes':['Same close camera and shared right-wall layout; teal curtains reveal the backstage exit through the same opening.','Raised platform/cannon, two lamps and sparse confetti. Same left console button lights green at the same physical right-front position.','No alarmed presenter baked in; new C07 is separately composited.'],'attention':['Review raised-platform edge reconstruction and the paired wide/close console proof.']},
'CH3-C06-presenter-excited':{'changes':['Same auburn bob, coral blouse, slate jacket and named character, with bright eyes and a broader delighted expression/presenting gesture.','Native hand-traced binary matte; no scenery/halo layer. Unrequested donor lapel microphone removed with localized approved-costume pixels.','Same head-top/bottom anchors and (0,0), scale1 compositing as approved A06.'],'attention':['Identity, expression and residual source-derived skin/clothing softness remain Nate’s creative review.']},
'CH3-C07-presenter-alarmed':{'changes':['Same presenter, with sympathetic alarm, slightly open mouth and a stop gesture; other hand interrupted mid-grip.','Binary native matte, no attached microphone stand or backdrop. Same anchor and scale as A06.'],'attention':['Inspect the hand contour and likeness against approved A06 on light/dark matte proofs.']},
'CH3-B07-attendant-alarmed':{'changes':['Explicit carry-forward candidate, outside approved Batch B B01–B06. Same gray temples, spectacles, cream shirt, tie and teal vest.','Courteous strained expression and raised viewer-right palm; unchanged composite anchor and head/bottom coordinates from A03.','The scanner/green authorization lamp stay on the unobstructed left.'],'attention':['Review likeness and sleeve/hand matte. This candidate remains unselected; it is not part of Batch B’s six approvals.']}}

composites=[];contexts=[('CH3-C06-presenter-excited','CH3-C02-urgency-bg','candidates/CH3-C02-urgency-bg-v01.png'),('CH3-C06-presenter-excited','A05-verification','references/A05-verification-bg.png'),('CH3-C07-presenter-alarmed','CH3-C05-surprise-bg','candidates/CH3-C05-surprise-bg-v01.png'),('CH3-C07-presenter-alarmed','A05-verification','references/A05-verification-bg.png'),('CH3-B07-attendant-alarmed','B05-scanner','references/B05-scanner-bg.png'),('CH3-B07-attendant-alarmed','A02-restroom','references/A02-restroom-bg.png')]
for ident,label,bp in contexts:
 fg=rgba(byid[ident]['file']);bg=rgba(bp);out=bg.copy();out.alpha_composite(fg,(0,0));file=f'composites/{ident}--{label}.png';out.convert('RGB').save(R/file)
 for y in range(278):
  for x in range(564):assert out.getpixel((x,y))==(fg.getpixel((x,y)) if fg.getpixel((x,y))[3] else bg.getpixel((x,y)))
 rois={}
 if 'urgency' in label:rois={'restroomReveal':[398,145,462,213],'rightWallPanel':[512,115,540,172],'demoConsole':[420,225,460,243]}
 elif 'surprise' in label:rois={'leftLamp':[254,98,282,129],'rightLamp':[298,98,326,129],'demoConsole':[420,225,460,243],'cannonMouth':[324,135,344,158]}
 elif label=='B05-scanner':rois={'greenDocumentLamp':[119,100,144,126],'readerRoller':[165,149,222,179]}
 counts=[]
 for name,box in rois.items():
  count=overlap(fg,box);area=(box[2]-box[0])*(box[3]-box[1]);counts.append({'feature':name,'box':box,'foregroundPixels':count,'fraction':count/area})
  if name!='cannonMouth':assert count==0,(ident,name,count)
  else:assert count/area<.1
 composites.append({'foreground':ident,'background':label,'backgroundFile':bp,'file':file,'sha256':sha(R/file),'foregroundSha256':sha(R/byid[ident]['file']),'anchor':[0,0],'scale':1,'allForegroundPixelsExact':True,'equipmentOverlap':counts})

qa=[]
for item in brief['candidates']:
 ident=item['candidateId'];r=byid[ident];g=gens[ident];im=rgba(r['file']);raw=Image.open(R/g['source']);assert list(im.size)==item['dimensions'];assert sha(R/r['file'])==r['sha256']
 assert sha(R/g['source'])==g['sourceSha256'];assert list(raw.size)==g['actualSourceDimensions'];assert sha(R/g['submittedPrompt'])==g['submittedPromptSha256']
 exact=(R/item['prompt']).read_text();submitted=(R/g['submittedPrompt']).read_text();assert exact.rstrip('\n') in submitted and direction.rstrip('\n') in submitted
 assert sha(R/item['prompt'])==item['promptSha256']
 for f in g['references']:assert sha(R/f['file'])==f['sha256']
 p=rgba(f'previews/{ident}-v01-4x.png');expected=im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST);assert p.tobytes()==expected.tobytes()
 alpha=set(im.getchannel('A').getdata());assert alpha==({0,255} if item['kind']=='foreground' else {255})
 q={'candidateId':ident,'dimensions':list(im.size),'file':r['file'],'sha256':r['sha256'],'alphaValues':sorted(alpha),'dimensionsAndAlpha':'PASS','previewDimensions':list(p.size),'exact4x':'PASS; every block matches source','uniqueRGB':len(im.convert('RGB').getcolors(im.width*im.height)),'globalPaletteFilter':False,'globalSharpening':False,'actualGeneratorDimensions':list(raw.size),'requestedGeneratorSourceSize':'FAIL; generator returned an oversized source','originalNativeGridAuthorship':'UNPROVEN / NOT PASSED','selected':False,'approved':False,'assetPath':None,'visualInspection':notes[ident]}
 if item['kind']!='foreground':
  base=rgba(r['base']);layer=rgba(r['incidentLayer']);reconstructed=base.copy();reconstructed.alpha_composite(layer);assert reconstructed.tobytes()==im.tobytes()
  changed=sum(base.getpixel((x,y))!=im.getpixel((x,y)) for y in range(im.height) for x in range(im.width));assert changed==r['changedPixels']
  assert all(im.getpixel((x,y))==base.getpixel((x,y)) for y in range(im.height) for x in range(im.width) if not layer.getpixel((x,y))[3])
  q['maskValidation']={'result':'PASS','unexpectedChangesOutsideMask':0,'changedPixels':changed,'base':r['base'],'baseSha256':r['baseSha256'],'layer':r['incidentLayer'],'layerSha256':sha(R/r['incidentLayer'])}
 else:
  bbox=list(im.getchannel('A').getbbox());assert bbox[1]==r['approvedBounds'][1] and bbox[3]==r['approvedBounds'][3]
  points={(x,y) for y in range(278) for x in range(564) if im.getpixel((x,y))[3]};components=0
  while points:
   components+=1;queue=[points.pop()]
   while queue:
    x,y=queue.pop()
    for dx in [-1,0,1]:
     for dy in [-1,0,1]:
      point=(x+dx,y+dy)
      if point in points:points.remove(point);queue.append(point)
  assert components==1
  q['foregroundValidation']={'binaryAlpha':True,'connectedComponents':components,'bounds':bbox,'approvedBounds':r['approvedBounds'],'topAndBottomAnchorsExact':True,'compositeAnchor':[0,0],'scale':1,'noWholeCharacterRescaleOrTranslation':True}
  dark=Image.new('RGBA',im.size,'#1e3038');dark.alpha_composite(im);light=Image.new('RGBA',im.size,'#f6eedf');light.alpha_composite(im)
  proof=Image.new('RGB',(1128,278));proof.paste(light.convert('RGB'),(0,0));proof.paste(dark.convert('RGB'),(564,0));proof.save(R/f'comparisons/{ident}-light-dark-matte.png')
  proof.resize((4512,1112),Image.Resampling.NEAREST).save(R/f'comparisons/{ident}-light-dark-matte-4x.png')
 qa.append(q)

# Pixel identity of fixed right-wall stack across scene states, per camera.
mainids=['CH3-C01-urgency','CH3-C03-locomotion','CH3-C04-surprise'];bgids=['CH3-C02-urgency-bg','CH3-C05-surprise-bg'];landmarks=[]
for ids,box in [(mainids,(277,50,314,133)),(bgids,(496,28,564,193))]:
 first=rgba(byid[ids[0]]['file']).crop(box)
 for ident in ids:
  assert rgba(byid[ident]['file']).crop(box).tobytes()==first.tobytes();landmarks.append({'candidateId':ident,'box':list(box),'rightWallPixelDifferences':0})
# Verify the SAME console component and button state at the paired physical
# right-front position. Only exact opaque component pixels are compared.
console_checks=[]
for ident in mainids+bgids:
 im=rgba(byid[ident]['file']);component=rgba(f'layers/{ident}-matched-console.png');xy=(220,151) if im.width==314 else (420,225)
 mismatch=sum(1 for y in range(component.height) for x in range(component.width) if component.getpixel((x,y))[3] and im.getpixel((x+xy[0],y+xy[1]))!=component.getpixel((x,y)))
 assert mismatch==0,(ident,mismatch)
 console_checks.append({'candidateId':ident,'origin':list(xy),'size':list(component.size),'active':ident in ['CH3-C04-surprise','CH3-C05-surprise-bg'],'unexpectedConsolePixels':mismatch,'buttonRole':'Same left button; three-button arrangement preserved'})
# Header and the main camera core stay on the original approved coordinates.
for ident in mainids:
 im=rgba(byid[ident]['file']);base=rgba('references/A04-verification.png')
 for box in [(0,0,314,50),(11,98,65,128)]:assert im.crop(box).tobytes()==base.crop(box).tobytes(),(ident,box)

row(['references/A04-verification.png']+[byid[i]['file'] for i in mainids],'comparisons/stage-continuity.png')
row(['references/A06-presenter.png',byid['CH3-C06-presenter-excited']['file'],byid['CH3-C07-presenter-alarmed']['file']],'comparisons/presenter-identity.png')
row(['references/A03-attendant.png',byid['CH3-B07-attendant-alarmed']['file']],'comparisons/attendant-identity.png')
for ident in mainids:row([byid[ident]['file'],'references/chapter-01-foyer.png','references/chapter-02-groundskeeper.png'],'comparisons/'+ident+'-chapter-style.png')

# Paired layout proof: same physical role/order in both independent cameras.
for tag,mi,bi in [('urgency','CH3-C01-urgency','CH3-C02-urgency-bg'),('surprise','CH3-C04-surprise','CH3-C05-surprise-bg')]:
 wide=rgb(byid[mi]['file']).resize((628,412),Image.Resampling.NEAREST);tight=rgb(byid[bi]['file']);proof=Image.new('RGB',(1192,412),'#1e3038');proof.paste(wide,(0,0));proof.paste(tight,(628,0));d=ImageDraw.Draw(proof)
 for box,color in [((201*2,70*2,264*2,144*2),'#eec96f'),((277*2,50*2,313*2,133*2),'#89d6dd'),((220*2,151*2,245*2,163*2),'#9fdf76')]:d.rectangle(box,outline=color,width=2)
 for box,color in [((628+389,64,628+475,224),'#eec96f'),((628+496,28,628+563,193),'#89d6dd'),((628+420,225,628+460,243),'#9fdf76')]:d.rectangle(box,outline=color,width=2)
 proof.save(R/f'comparisons/{tag}-main-close-layout.png')

preservation={'approvedStoryAndHistoricalMainFiles':len(read('sources/protected-files.json')['files']),'pinnedPriorChapter3ReviewFiles':archive_count,'result':'PASS; all pinned source hashes match; no approved artwork, registry, narrative, gameplay or historical review file changed.'}
report={'exportAndPreservation':'PASS','originalNativeGridAuthorship':'UNPROVEN / NOT PASSED for all eight','creativeApproval':'PENDING NATE; generated/unselected only','candidateCount':8,'generationCalls':8,'candidates':qa,'composites':composites,'fixedRightWallChecks':landmarks,'consoleCorrespondence':console_checks,'layoutAuthority':read('sources/shared-stage-layout.json'),'preservation':preservation,'pages':'NOT DEPLOYED; main-only restriction preserved. Separate publication proposal required.'}
write('qa.json',report)
manifest={**brief,'version':'Batch C v01 — owner-selected reveal layout','currentCandidateCount':8,'status':'generated/unselected','selected':False,'approved':False,'assetPath':None,'candidates':[{**i,**byid[i['candidateId']]} for i in brief['candidates']],'generationRecords':'sources/generation-records.json','composites':composites,'preservation':preservation,'gameRepositoryModified':False,'batchDBegun':False,'nativeGridAuthorship':'UNPROVEN','pagesDeployed':False}
write('manifest.json',manifest)
(R/'CANDIDATE_HASHES.md').write_text('| Candidate | SHA-256 |\n|---|---|\n'+''.join(f"| {q['candidateId']} | `{q['sha256']}` |\n" for q in qa))

def art(p,w,h,scene=False,alt='Review image'):
 return f'<div class="viewport"><img src="{p}" class="{"scene-art" if scene else "portrait-art"}" width="{w}" height="{h}" data-w="{w}" data-h="{h}" alt="{html.escape(alt)}"></div>'
cards=[]
for item,q in zip(brief['candidates'],qa):
 ident=item['candidateId'];w,h=item['dimensions'];main=item['kind']=='main';g=gens[ident];n=notes[ident]
 content=f'<article class="candidate" id="{ident}"><h2>{ident}</h2><p><strong>Generated / unselected</strong>{" · Batch B carry-forward, outside approved B01–B06" if item["carryForward"] else ""} · {w}×{h}</p>'+art(q['file'],w,h,main,ident)+'<ul>'+''.join('<li>'+html.escape(t)+'</li>' for t in n['changes'])+'</ul><p class="hash">SHA-256: <code>'+q['sha256']+'</code></p>'
 content+=f'<p><a href="{q["file"]}">Native PNG</a> · <a href="previews/{ident}-v01-4x.png">Exact 4× PNG</a> · <a href="{g["source"]}">Untouched original source ({g["actualSourceDimensions"][0]}×{g["actualSourceDimensions"][1]})</a> · <a href="{item["prompt"]}">Exact canonical prompt</a> · <a href="{g["submittedPrompt"]}">Exact submitted prompt</a></p>'
 if main:content+='<p>Left to right: candidate, approved Chapter 1 foyer, approved Chapter 2 groundskeeper.</p>'+art('comparisons/'+ident+'-chapter-style.png',942,206,True)
 if item['kind']=='foreground':content+='<h3>Light / dark matte proof</h3>'+art('comparisons/'+ident+'-light-dark-matte.png',1128,278)+f'<p><a href="masks/{ident}-native-silhouette.png">Native silhouette mask</a></p>'
 else:content+=f'<p><a href="masks/{ident}-allowed.png">Exact final edit mask</a> · <a href="{q["maskValidation"]["layer"]}">Final state layer</a> · <a href="sources/{ident}-changed-coordinates.json">Changed-pixel coordinates</a></p>'
 content+='<p><strong>Art Director attention:</strong> '+' '.join(html.escape(t) for t in n['attention'])+'</p><p class="meta">'+str(q['uniqueRGB'])+' RGB colors (diagnostic, no fixed palette limit). Original native-grid authorship remains unproven; source-derived softness is not passed by these export checks.</p></article>'
 cards.append(content)
comp_html=''
for c in composites:comp_html+='<h3>'+c['foreground']+' over '+c['background']+'</h3>'+art(c['file'],564,278)+f'<p class="meta">Exact foreground pixels at(0,0), scale1. <a href="{c["file"]}">Native proof PNG</a></p>'
style='*{box-sizing:border-box;min-width:0}body{margin:0;background:#16272d;color:#f4eadb;font:16px/1.55 system-ui}main{max-width:1380px;margin:auto;padding:24px}a{color:#9edbdc}p,li,a,code,h1,h2,h3,summary{overflow-wrap:anywhere}.viewport{width:100%;max-width:100%;overflow:auto;background:repeating-conic-gradient(#405057 0 25%,#283b43 0 50%) 0/24px 24px;border:1px solid #5f7b83}.viewport img{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}nav,.controls{display:flex;flex-wrap:wrap;gap:12px;margin:18px 0}.controls{position:sticky;top:0;z-index:2;background:#16272df5;padding:12px 0}button{font:inherit;padding:10px 16px;border:1px solid #829b9d;background:#2b4852;color:inherit;border-radius:4px}button[aria-pressed=true]{background:#f0d1a7;color:#17272c}.notice{background:#533c30;border-left:4px solid #edb677;padding:16px}.candidate,section{margin-top:30px;padding-top:18px;border-top:1px solid #5f7b83}.meta,.hash{font-size:14px;color:#c5d4d5}li{margin:8px 0}'
nav=''.join(f'<a href="#{i["candidateId"]}">{i["candidateId"]}</a>' for i in brief['candidates'])
page=f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Out of Order — Chapter 3 Batch C</title><style>{style}</style><main><h1>Out of Order — Chapter 3 Batch C</h1><p><strong>Eight generated / unselected candidates · seven Batch C + one explicit B07 carry-forward.</strong></p><p>The owner-selected red reveal is the right-side layout master. The same opening, two-person sign, three-button panel and separate loudspeaker are reused across each camera’s variants. The script changes what the curtain reveals. The front console stays between platform and chair, and the same left button illuminates green for surprise.</p><p class="notice">Original native-grid authorship remains <strong>unproven</strong>. All eight generator sources were oversized and are preserved unchanged. Target exports, component transfers, manual alpha mattes and localized native edits are documented; no global sharpening, palette filtering or disguised size conversion. Visual selection remains Nate’s decision.</p><p>Local / Pages-compatible review package. <strong>Not deployed from this branch.</strong> The main-only Pages restriction is preserved; the publication workflow change is a separate unmerged proposal.</p><nav>{nav}<a href="#layout">Layout proofs</a><a href="#composites">Composites</a><a href="qa.json">Technical QA</a></nav><div class="controls"><button data-scale="1" aria-pressed="true">Main scenes · native 1×</button><button data-scale="4" aria-pressed="false">Main scenes · exact 4×</button></div><p>Portraits and composites remain native 564×278. Main comparisons follow the chosen integer scale. Large sheets scroll; artwork is never squeezed to fit.</p><section id="layout"><h2>Shared layout and event states</h2><p>Approved A04, urgency, locomotion, surprise. A04 remains unchanged; the new right-side reveal follows Nate’s explicit layout direction.</p>'+art('comparisons/stage-continuity.png',1256,206,True)+'<p>Wide at2× / independent close at1×. Gold: fixed curtain reveal. Cyan: sign, three-button panel and PA grille. Green: same physical front console. Boxes appear only on proofs.</p>'+art('comparisons/urgency-main-close-layout.png',1192,412)+art('comparisons/surprise-main-close-layout.png',1192,412)+'<h3>Presenter identity — approved / excited / alarmed</h3>'+art('comparisons/presenter-identity.png',1692,278)+'<h3>Attendant identity — approved / alarmed</h3>'+art('comparisons/attendant-identity.png',1128,278)+'</section>'+''.join(cards)+'<section id="composites"><h2>Foreground/background composites</h2>'+comp_html+'</section><section><h2>Provenance and boundaries</h2><p><a href="manifest.json">Eight-candidate manifest</a> · <a href="CANDIDATE_HASHES.md">Exact candidate hashes</a> · <a href="sources/generation-records.json">Original filenames, dimensions, hashes and derivations</a> · <a href="sources/shared-stage-layout.json">Shared layout authority</a> · <a href="sources/OWNER-CONTINUITY-CORRECTIONS.md">Owner continuity directions</a> · <a href="sources/baseline-tests.json">Canonical preflight checks</a> · <a href="sources/protected-files.json">Approved/narrative pins</a> · <a href="sources/historical-review-pins.json">Historical Batch A/B pins</a> · <a href="PNG_SHA256SUMS.txt">PNG checksums</a> · <a href="SOURCE_SHA256SUMS.txt">Package checksums</a> · <a href="browser-qa.json">Browser QA</a></p><p>Game: <a href="https://github.com/InterstellarHarvest/out-of-order">InterstellarHarvest/out-of-order</a> — unchanged. Storyboard repository and Pages slug remain CYOA-storyboard. Historical prompt titles and schemas remain verbatim for provenance and compatibility.</p><p>All approved artwork, narrative, dialogue, choices, checks, endings, registry and gameplay remain unchanged. Menu-intake assets untouched. No approvals, production paths, gameplay integration or Batch D. Stop for Nate’s Art Director review.</p></section></main><script>document.querySelectorAll("[data-scale]").forEach(b=>b.onclick=()=>{let s=Number(b.dataset.scale);document.querySelectorAll("img.scene-art").forEach(i=>{i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s});document.querySelectorAll("[data-scale]").forEach(n=>n.setAttribute("aria-pressed",String(n===b)))});</script></html>'
(R/'index.html').write_text(page)
(R/'README.md').write_text('''# Out of Order — Chapter 3 Batch C

Open index.html or serve this repository and visit this package. Eight generated/unselected candidates; no approval registration or Batch D.

Reproduction order: `assemble_scenes.py`, `apply_layout_master.py`, `finish_foregrounds.py`, `build_review.py`. Untouched originals are in generation-source; exact prompts and records are linked from the gallery. Original native-grid authorship remains unproven. The owner-selected red reveal/right-wall master supersedes the earlier original-door lock for new Batch C images only. Approved A04/A05 remain byte-identical.

Main314×206; two opaque close backgrounds and three binary-alpha foregrounds564×278. All exact4× PNGs retained. Main/close console placement and right-wall sign/panel/speaker are compared explicitly. Separate publication proposal only; no generation-branch deployment or environment exception.
''')
(R/'PNG_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(R).as_posix()}\n' for p in sorted(R.rglob('*.png'))))
(R/'SOURCE_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(R).as_posix()}\n' for p in sorted(R.rglob('*')) if p.is_file() and p.suffix!='.png' and p.name!='SOURCE_SHA256SUMS.txt'))
print(json.dumps({'candidateCount':8,'preservation':preservation,'nativeAuthorship':'UNPROVEN','hashes':{q['candidateId']:q['sha256'] for q in qa},'compositeCount':len(composites)},indent=2))
