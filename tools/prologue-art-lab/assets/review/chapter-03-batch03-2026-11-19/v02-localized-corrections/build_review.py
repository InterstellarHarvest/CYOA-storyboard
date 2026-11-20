"""Validate v02 against immutable v01 and build a review-only static gallery."""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, html, io, json, subprocess, tarfile

R=Path(__file__).resolve().parent
V1=R.parent/'v01'
REPO=R.parents[5]
PIN='53358b9df78f72e815cd69ee4128b1c86c08818d'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(name,obj):(R/name).write_text(json.dumps(obj,indent=2)+'\n')
def rgba(p):return Image.open(p).convert('RGBA')
def rgb(p):return Image.open(p).convert('RGB')
def same(a,b):return a.size==b.size and a.tobytes()==b.tobytes()
def row(paths,name):
    ims=[rgb(p) for p in paths]
    out=Image.new('RGB',(sum(i.width for i in ims),max(i.height for i in ims)),'#1e3038')
    x=0
    for im in ims:out.paste(im,(x,0));x+=im.width
    out.save(R/'comparisons'/f'{name}.png')
    out.resize((out.width*4,out.height*4),Image.Resampling.NEAREST).save(R/'comparisons'/f'{name}-4x.png')
    return out

records=read(R/'sources/corrections.json')
canonical=read(R/'sources/canonical-qa.json')
assert canonical['result']=='PASS' and len(canonical['checks'])==6
assert all(c['exitCode']==0 for c in canonical['checks'])
original=read(V1/'manifest.json')
old={c['candidateId']:c for c in original['candidates']}
expected={'CH3-C01-urgency','CH3-C02-urgency-bg','CH3-C03-locomotion','CH3-C04-surprise','CH3-C05-surprise-bg','CH3-C06-presenter-excited','CH3-C07-presenter-alarmed','CH3-B07-attendant-alarmed'}
assert len(records)==8 and {r['candidateId'] for r in records}==expected
edited={'CH3-C01-urgency','CH3-C03-locomotion'}
assert {r['candidateId'] for r in records if r['changedPixels']}==edited

# Compare every historical v01 file to its Git blob, not merely candidate PNGs.
prefix=V1.relative_to(REPO).as_posix()
v1_entries=subprocess.check_output(['git','ls-tree','-r',PIN,'--',prefix],cwd=REPO,text=True).splitlines()
v1_pins=[]
for entry in v1_entries:
    metadata,path=entry.split('\t',1);blob=metadata.split()[2]
    actual=subprocess.check_output(['git','hash-object',path],cwd=REPO,text=True).strip()
    assert actual==blob,path
    v1_pins.append({'file':path,'gitBlob':blob,'sha256':sha(REPO/path)})
assert len(v1_pins)>150
write('sources/v01-preservation.json',{'sourceCommit':PIN,'fileCount':len(v1_pins),'files':v1_pins})
protected=read(V1/'sources/protected-files.json')['files']
for p in protected:assert sha(REPO/p['file'])==p['sha256'],p['file']
historic=0
for archive in read(V1/'sources/historical-review-pins.json')['archives']:
    data=subprocess.check_output(['git','archive',archive['sourceCommit'],archive['root']],cwd=REPO)
    expected_files={f['file']:f['sha256'] for f in archive['files']}
    with tarfile.open(fileobj=io.BytesIO(data),mode='r:') as a:
        actual={f.name:hashlib.sha256(a.extractfile(f).read()).hexdigest() for f in a if f.isfile()}
    assert actual==expected_files
    historic+=len(actual)
assert subprocess.check_output(['git','hash-object','story/chapters/chapter-03.reboot-candidate.json'],cwd=REPO,text=True).strip()==original['narrativeBlob']
assert subprocess.check_output(['git','diff',PIN,'--','.github','story','assets/selected'],cwd=REPO)==b''

qa=[]
for rec in records:
    ident=rec['candidateId'];before_file=V1/old[ident]['file'];file=R/rec['file']
    assert sha(before_file)==rec['sourceSha256']==old[ident]['sha256']
    assert sha(file)==rec['sha256']
    native=Image.open(file);before=rgba(before_file);after=rgba(file)
    assert list(after.size)==rec['dimensions']
    assert native.mode==('RGBA' if rec['kind']=='foreground' else 'RGB')
    alphas=set(after.getchannel('A').tobytes())
    assert alphas==({0,255} if rec['kind']=='foreground' else {255})
    preview=rgba(R/'previews'/f'{ident}-v02-4x.png')
    assert same(preview,after.resize((after.width*4,after.height*4),Image.Resampling.NEAREST))
    allowed=Image.open(R/rec['allowedMask']).convert('L')
    changed=Image.open(R/rec['changedMask']).convert('L')
    coords=read(R/rec['changedCoordinates'])['pixels']
    expected_changes={(p['x'],p['y']):(p['before'],p['after']) for p in coords}
    assert len(expected_changes)==len(coords)==rec['changedPixels']
    actual_changes=[]
    for y in range(after.height):
        for x in range(after.width):
            diff=before.getpixel((x,y))!=after.getpixel((x,y))
            assert bool(changed.getpixel((x,y)))==diff
            if diff:
                assert allowed.getpixel((x,y))
                p=(x,y);actual_changes.append(p)
                a,b=expected_changes[p]
                assert list(Image.open(before_file).getpixel(p))==a
                assert list(native.getpixel(p))==b
    assert set(actual_changes)==set(expected_changes)
    reconstructed=before.copy();reconstructed.alpha_composite(rgba(R/rec['correctionLayer']))
    assert same(reconstructed,after)
    if not rec['changedPixels']:assert file.read_bytes()==before_file.read_bytes()
    elif ident=='CH3-C01-urgency':
        # Whole presenter identity, pose and sleeve are exact left of the bell.
        assert same(before.crop((73,83,109,154)),after.crop((73,83,109,154)))
        for x,y in read(R/'sources/bell-edit-spec.json')['protectedHandPixels']:
            assert before.getpixel((x,y))==after.getpixel((x,y))
        for box in [(0,0,314,84),(119,84,314,206),(0,122,314,206)]:
            assert same(before.crop(box),after.crop(box))
    else:
        # Conveyor, pit, unfolding net and all room structure are exact.
        for box in [(0,0,314,129),(0,129,224,206),(0,146,314,206),(259,0,314,206)]:
            assert same(before.crop(box),after.crop(box)),box
    bounds=changed.getbbox()
    q={'candidateId':ident,'dimensions':list(after.size),'mode':native.mode,'alphaValues':sorted(alphas),
       'sha256':sha(file),'changedPixels':len(actual_changes),'changedBounds':list(bounds) if bounds else None,
       'unexpectedChangesOutsideAllowedMask':0,'exactChangedMaskAndCoordinates':True,
       'reconstructsFromV01AndLocalLayer':True,'byteIdenticalToV01':not actual_changes,
       'exact4x':'PASS','uniqueRGB':len(after.convert('RGB').getcolors(after.width*after.height)),
       'v01UniqueRGB':len(before.convert('RGB').getcolors(before.width*before.height)),
       'globalFiltering':False,'imageGenerationCalls':0,'nativeGridAuthorship':'ORIGINAL AUTHORSHIP UNPROVEN; localized edits explicitly authored at target grid'}
    if rec['kind']=='foreground':
        assert same(before.getchannel('A'),after.getchannel('A'))
        q.update({'alphaAndAnchorUnchanged':True,'bounds':list(after.getchannel('A').getbbox()),'anchor':[0,0],'scale':1})
    qa.append(q)
    row([before_file,file],ident+'-v01-v02')

byid={r['candidateId']:r for r in records}
mainids=['CH3-C01-urgency','CH3-C03-locomotion','CH3-C04-surprise']
row([V1/'references/A04-verification.png']+[R/byid[i]['file'] for i in mainids],'stage-continuity')
for ident in mainids:
    row([R/byid[ident]['file'],V1/'references/chapter-01-foyer.png',V1/'references/chapter-02-groundskeeper.png'],ident+'-chapter-style')
row([V1/'references/A06-presenter.png',V1/old['CH3-C06-presenter-excited']['file'],R/byid['CH3-C06-presenter-excited']['file']],'presenter-optional-decision')

# Tight unfiltered inspection sheets and proof overlays, never candidate files.
for ident,box,tag in [('CH3-C01-urgency',(101,95,120,113),'bell'),('CH3-C03-locomotion',(205,120,269,151),'landing')]:
    a=rgb(V1/old[ident]['file']).crop(box);b=rgb(R/byid[ident]['file']).crop(box)
    sheet=Image.new('RGB',(a.width*2,a.height));sheet.paste(a,(0,0));sheet.paste(b,(a.width,0))
    sheet.save(R/'comparisons'/f'{tag}-v01-v02-native-crop.png')
    sheet.resize((sheet.width*8,sheet.height*8),Image.Resampling.NEAREST).save(R/'comparisons'/f'{tag}-v01-v02-8x.png')
    im=rgba(V1/old[ident]['file']);mask=Image.open(R/byid[ident]['changedMask']).convert('L')
    tint=Image.new('RGBA',im.size,(244,64,139,0));tint.putalpha(mask.point(lambda a:140 if a else 0))
    im.alpha_composite(tint);im.convert('RGB').resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(R/'comparisons'/f'{tag}-changed-overlay-4x.png')

composites=[]
for old_comp in original['composites']:
    ident=old_comp['foreground'];bp=old_comp['backgroundFile']
    bg=R/bp if bp.startswith('candidates/') else V1/bp
    if bp.startswith('candidates/'):
        bg=R/byid[next(i for i in byid if i in bp)]['file']
    fg=rgba(R/byid[ident]['file']);base=rgba(bg);out=base.copy();out.alpha_composite(fg,(0,0))
    file=old_comp['file'];out.convert('RGB').save(R/file)
    assert sha(R/file)==old_comp['sha256']
    assert (R/file).read_bytes()==(V1/file).read_bytes()
    out.resize((2256,1112),Image.Resampling.NEAREST).convert('RGB').save(R/'previews'/(Path(file).stem+'-4x.png'))
    composites.append({**old_comp,'backgroundFile':str(bg.relative_to(R)) if bg.is_relative_to(R) else '../v01/'+bp,
        'byteIdenticalToV01':True,'allForegroundPixelsExact':True,'anchor':[0,0],'scale':1})

wall=[]
for ids,box in [(mainids,(277,50,314,133)),(['CH3-C02-urgency-bg','CH3-C05-surprise-bg'],(496,28,564,193))]:
    master=rgba(R/byid[ids[0]]['file']).crop(box)
    for ident in ids:
        assert same(master,rgba(R/byid[ident]['file']).crop(box))
        assert same(rgba(V1/old[ident]['file']).crop(box),rgba(R/byid[ident]['file']).crop(box))
        wall.append({'candidateId':ident,'box':list(box),'differences':0})
console=[]
for ident in mainids+['CH3-C02-urgency-bg','CH3-C05-surprise-bg']:
    box=(220,151,245,163) if byid[ident]['kind']=='main' else (420,225,460,243)
    assert same(rgba(V1/old[ident]['file']).crop(box),rgba(R/byid[ident]['file']).crop(box))
    console.append({'candidateId':ident,'box':list(box),'differencesFromV01':0})
preservation={'v01FilesUnchanged':len(v1_pins),'protectedCurrentFilesUnchanged':len(protected),
    'pinnedBatchABHistoricalFilesVerified':historic,'approvedArtNarrativeRegistryAndWorkflowsUnchanged':True,
    'unchangedCandidateCount':6,'publication':'No Pages deployment, merge or PR #13 change.'}
report={'result':'PASS','scope':'Export, masks, preservation, layout and anchoring; visual selection pending Nate.',
    'sourceCommit':PIN,'candidateCount':8,'editedCandidateCount':2,'changedPixelsTotal':sum(q['changedPixels'] for q in qa),
    'candidates':qa,'composites':composites,'fixedRightWallChecks':wall,'consoleContinuity':console,
    'canonicalChecks':{'result':'PASS','count':6,'record':'sources/canonical-qa.json'},
    'browserVerification':read(R/'browser-qa.json') if (R/'browser-qa.json').exists() else {'result':'PENDING'},
    'preservation':preservation,'nativeGridAuthorship':'UNRESOLVED / UNPROVEN for original image generation; v02 pixel edits are documented precisely.',
    'remainingVisualConcerns':['Bell is seven logical pixels wide; final native-size readability is Nate\'s decision.',
       'The stationary landing is articulated without widening it; verify the difficult d6 leap still reads plausibly.',
       'Inherited source-derived RGB softness remains; no global filter or palette reduction was applied.']}
write('qa.json',report)
write('manifest.json',{'gameTitle':'Out of Order','version':'Chapter 3 Batch C v02 localized corrections','sourceCommit':PIN,
    'branch':'art/ch3-pavilion-batch03-20261119','narrativeBlob':original['narrativeBlob'],
    'status':'generated/unselected','selected':False,'approved':False,'assetPath':None,'pagesDeployed':False,
    'currentCandidateCount':8,'candidates':records,'composites':composites,'preservation':preservation,
    'generationCallsThisPass':0,'originalGenerationProvenance':'../v01/sources/generation-records.json',
    'nativeGridAuthorship':'UNRESOLVED / UNPROVEN','gameRepositoryModified':False,'batchDBegun':False})
(R/'CANDIDATE_HASHES.md').write_text('| Candidate | Changed pixels | SHA-256 |\n|---|---:|---|\n'+''.join(f'| {r["candidateId"]} | {r["changedPixels"]} | `{r["sha256"]}` |\n' for r in records))

def art(path,cls='scaled',alt='Review proof'):
    im=Image.open(R/path)
    return f'<div class="viewport"><img class="{cls}" src="{path}" width="{im.width}" height="{im.height}" data-w="{im.width}" data-h="{im.height}" alt="{html.escape(alt)}"></div>'
cards=[]
for rec in records:
    ident=rec['candidateId'];n=rec['changedPixels']
    cards.append(f'<article class="candidate" id="{ident}"><h2>{ident}</h2><p><strong>Generated / unselected</strong> · {"Localized correction: "+str(n)+" changed pixels" if n else "Byte-identical to v01"} · {rec["dimensions"][0]}×{rec["dimensions"][1]}</p>'+
       art(rec['file'],alt=ident)+'<ul>'+''.join('<li>'+html.escape(x)+'</li>' for x in rec['operations'])+'</ul>'+
       f'<p class="hash">SHA-256: <code>{rec["sha256"]}</code></p><p><a href="{rec["file"]}">Native v02 PNG</a> · <a href="previews/{ident}-v02-4x.png">Exact 4× PNG</a> · <a href="../v01/{old[ident]["file"]}">Immutable v01 PNG</a></p>'+
       '<p>Comparison: v01 left / v02 right.</p>'+art(f'comparisons/{ident}-v01-v02.png')+
       f'<p><a href="comparisons/{ident}-v01-v02-4x.png">Exact 4× comparison PNG</a> · <a href="{rec["allowedMask"]}">Allowed edit mask</a> · <a href="{rec["changedMask"]}">Exact changed-pixel mask</a> · <a href="{rec["changedCoordinates"]}">Every modified pixel, before/after RGB</a> · <a href="{rec["correctionLayer"]}">Correction layer</a></p></article>')
style='*{box-sizing:border-box;min-width:0}body{margin:0;background:#17292f;color:#f4eadc;font:16px/1.5 system-ui}main{max-width:1380px;margin:auto;padding:24px}a{color:#a4dbd9}h1,h2,h3,p,li,a,code{overflow-wrap:anywhere}.viewport{max-width:100%;overflow:auto;border:1px solid #5c767d;background:repeating-conic-gradient(#405057 0 25%,#283b43 0 50%) 0/24px 24px}.viewport img{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}.controls{display:flex;gap:12px;flex-wrap:wrap;position:sticky;top:0;background:#17292ff7;padding:12px 0;z-index:3}button{padding:10px 16px;font:inherit;background:#31505b;color:inherit;border:1px solid #90a5a4}button[aria-pressed=true]{background:#f0d1a7;color:#17272c}article,section{margin-top:28px;border-top:1px solid #5c767d;padding-top:18px}.notice{padding:16px;border-left:4px solid #e4b578;background:#503d31}.hash{font-size:14px}nav{display:flex;gap:12px;flex-wrap:wrap}li{margin:8px 0}'
page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Out of Order — Chapter 3 Batch C v02</title><style>'+style+'</style><main><h1>Out of Order — Chapter 3 Batch C v02</h1><p><strong>Eight generated/unselected candidates. Only C01 and C03 changed; six candidates remain byte-identical.</strong></p><p>C01: a tapered silver bell, dark lip and visible clapper. C03: perspective tile seams and a shallow threshold edge on the existing stationary landing. No route widening or new bridge. Optional C06 facial changes were declined to preserve the current likeness and delighted expression.</p><p class="notice">Original native-grid authorship remains unresolved/unproven. This pass uses explicit target-grid pixel edits; it does not establish original native-grid authorship for the inherited images. No generation, global sharpening, resizing, scene redraw or palette filtering. No Pages deployment or PR #13 merge/update.</p><p><a href="../v01/">Immutable v01 gallery</a> · <a href="qa.json">Technical QA</a> · <a href="manifest.json">Candidate manifest</a> · <a href="CANDIDATE_HASHES.md">Eight hashes</a> · <a href="browser-qa.json">Browser QA</a> · <a href="HANDOFF.md">Art Director handoff</a></p><nav>'+''.join(f'<a href="#{r["candidateId"]}">{r["candidateId"]}</a>' for r in records)+'</nav><div class="controls"><button data-scale="1" aria-pressed="true">Native 1×</button><button data-scale="4" aria-pressed="false">Exact 4× nearest-neighbor</button></div><p>The scale control applies to scenes, portraits, comparisons and composites. The close-ups below stay at exact 8×. Oversized sheets scroll without fractional fitting.</p><section id="corrections"><h2>Localized before/after inspection</h2><h3>Bell — v01 left / v02 right, exact 8×</h3>'+art('comparisons/bell-v01-v02-8x.png','fixed-proof')+'<h3>Stationary landing — v01 left / v02 right, exact 8×</h3>'+art('comparisons/landing-v01-v02-8x.png','fixed-proof')+'<p>Highlighted changed-pixel proofs only; pink overlays are absent from candidate artwork.</p>'+art('comparisons/bell-changed-overlay-4x.png','fixed-proof')+art('comparisons/landing-changed-overlay-4x.png','fixed-proof')+'</section><section id="continuity"><h2>Stage continuity</h2><p>Approved A04 / current C01 / current C03 / unchanged C04. Doorway, two-person sign, wall buttons, separate PA grille and front-console positions remain intact.</p>'+art('comparisons/stage-continuity.png')+'<h3>Optional C06 decision</h3><p>Approved idle / excited v01 / excited v02 (unchanged). Hairstyle, identity, expression, costume, alpha and bottom anchor are exact.</p>'+art('comparisons/presenter-optional-decision.png')+'</section>'+''.join(cards)+'<section id="composites"><h2>Portrait composites</h2><p>Six native composites are byte-identical to v01, using the same foreground/background pixels at (0,0), scale 1. No pose or portrait background changed.</p>'+''.join('<h3>'+c['foreground']+' over '+c['background']+'</h3>'+art(c['file']) for c in composites)+'</section><section id="style"><h2>Approved chapter style references</h2><p>Each row: current stage / approved Chapter 1 / approved Chapter 2. Inherited source-derived softness remains.</p>'+''.join(art(f'comparisons/{i}-chapter-style.png') for i in mainids)+'</section><section><h2>Provenance and preservation</h2><p><a href="sources/corrections.json">Exact changes and source hashes</a> · <a href="sources/v01-preservation.json">Every immutable v01 file</a> · <a href="../v01/sources/generation-records.json">Original generation records</a> · <a href="../v01/prompts/canonical-direction.txt">Original shared direction</a> · <a href="../v01/sources/OWNER-CONTINUITY-CORRECTIONS.md">Owner layout authority</a> · <a href="finish_pixels.py">Deterministic pixel-edit implementation</a> · <a href="PNG_SHA256SUMS.txt">PNG checksums</a> · <a href="SOURCE_SHA256SUMS.txt">Package checksums</a></p><p>All original prompts and oversized generation sources remain in immutable v01. All approved artwork, historical galleries, narrative, registry, gameplay and publication workflows are unchanged. The main-only Pages restriction is preserved. No approval, registration, integration or Batch D. Stop for Nate’s final visual selection.</p></section></main><script>document.querySelectorAll("[data-scale]").forEach(b=>b.onclick=()=>{const s=+b.dataset.scale;document.querySelectorAll("img.scaled").forEach(i=>{i.width=+i.dataset.w*s;i.height=+i.dataset.h*s});document.querySelectorAll("[data-scale]").forEach(x=>x.setAttribute("aria-pressed",String(x===b)))});</script></html>'
(R/'index.html').write_text(page)
(R/'PNG_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(R).as_posix()}\n' for p in sorted(R.rglob('*.png'))))
(R/'SOURCE_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(R).as_posix()}\n' for p in sorted(R.rglob('*')) if p.is_file() and p.suffix!='.png' and p.name!='SOURCE_SHA256SUMS.txt'))
print(json.dumps({'result':'PASS','changedPixels':sum(q['changedPixels'] for q in qa),'candidateCount':8,'preservation':preservation,'hashes':{r['candidateId']:r['sha256'] for r in records}},indent=2))
