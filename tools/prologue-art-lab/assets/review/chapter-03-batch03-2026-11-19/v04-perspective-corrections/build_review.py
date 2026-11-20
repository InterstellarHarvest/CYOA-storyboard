"""Review-only seven-environment perspective and cannon-placement package; all selected sources immutable."""
from pathlib import Path
from PIL import Image, ImageChops
import json, hashlib, subprocess, io, tarfile, html
R=Path(__file__).resolve().parent;V1=R.parent/'v01';V2=R.parent/'v02-localized-corrections';V3=R.parent/'v03-continuity-corrections';REPO=R.parents[5]
PIN='2f51cfd909ca443b64e52285af17cb00bdb770b6';SELECTED='5e0449b3da84764176f9744f5624a88868f5fdcb'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(name,data):(R/name).write_text(json.dumps(data,indent=2)+'\n')
def rgba(p):return Image.open(p).convert('RGBA')
def rgb(p):return Image.open(p).convert('RGB')
def row(paths,name):
 ims=[rgb(p) for p in paths];out=Image.new('RGB',(sum(i.width for i in ims),max(i.height for i in ims)),'#1e3038');x=0
 for im in ims:out.paste(im,(x,0));x+=im.width
 out.save(R/'comparisons'/f'{name}.png');out.resize((out.width*4,out.height*4),Image.Resampling.NEAREST).save(R/'comparisons'/f'{name}-4x.png');return out
records=read(R/'sources/corrections.json');byid={r['candidateId']:r for r in records};assert len(records)==7
canonical=read(R/'sources/canonical-qa.json');assert canonical['result']=='PASS' and all(c['exitCode']==0 for c in canonical['checks'])
assert all(r['status']=='generated' and not r['selected'] and not r['approved'] and r['assetPath'] is None for r in records)
preserved=[]
for oldroot in [V1,V2,V3]:
 for entry in subprocess.check_output(['git','ls-tree','-r',PIN,'--',str(oldroot.relative_to(REPO))],cwd=REPO,text=True).splitlines():
  meta,path=entry.split('\t');blob=meta.split()[2]
  assert subprocess.check_output(['git','hash-object',path],cwd=REPO,text=True).strip()==blob,path
  preserved.append({'file':path,'gitBlob':blob,'sha256':sha(REPO/path)})
write('sources/historical-preservation.json',{'sourceCommit':PIN,'files':preserved})
protected=read(V1/'sources/protected-files.json')['files']
for p in protected:assert sha(REPO/p['file'])==p['sha256'],p['file']
assert subprocess.check_output(['git','diff',PIN,'--','story','assets/selected','.github'],cwd=REPO)==b''
assert subprocess.check_output(['git','hash-object','story/chapters/chapter-03.reboot-candidate.json'],cwd=REPO,text=True).strip()=='857ffdf1bc9432cf4bbbfd7819f5f430a06d9036'
hist_count=0
for archive in read(V1/'sources/historical-review-pins.json')['archives']:
 data=subprocess.check_output(['git','archive',archive['sourceCommit'],archive['root']],cwd=REPO)
 with tarfile.open(fileobj=io.BytesIO(data),mode='r:') as tf:
  got={p.name:hashlib.sha256(tf.extractfile(p).read()).hexdigest() for p in tf if p.isfile()}
 assert got=={p['file']:p['sha256'] for p in archive['files']};hist_count+=len(got)
qa=[]
for r in records:
 ident=r['candidateId'];src=R.parent/r['sourceFile'];file=R/r['file'];a=rgb(src);b=rgb(file)
 assert sha(src)==r['sourceSha256'] and sha(file)==r['sha256']
 assert Image.open(file).mode=='RGB' and list(b.size)==r['dimensions']
 assert b.size==((314,206) if r['kind']=='main' else (564,278))
 preview=rgb(R/'previews'/f'{ident}-v04-4x.png')
 assert preview.tobytes()==b.resize((b.width*4,b.height*4),Image.Resampling.NEAREST).tobytes()
 allowed=Image.open(R/'masks'/f'{ident}-allowed.png').convert('L');changed=Image.open(R/'masks'/f'{ident}-changed.png').convert('L')
 coords=read(R/'sources'/f'{ident}-changed-pixels.json')['pixels'];expected={(p['x'],p['y']):p for p in coords};actual=[]
 assert len(coords)==len(expected)==r['changedPixels']
 for y in range(b.height):
  for x in range(b.width):
   diff=a.getpixel((x,y))!=b.getpixel((x,y));assert bool(changed.getpixel((x,y)))==diff
   if diff:
    assert allowed.getpixel((x,y));p=expected[(x,y)]
    assert p['before']==list(a.getpixel((x,y))) and p['after']==list(b.getpixel((x,y)));actual.append([x,y])
 assert len(actual)==r['changedPixels']
 reconstructed=rgba(src);reconstructed.alpha_composite(rgba(R/'layers'/f'{ident}-correction.png'))
 assert reconstructed.convert('RGB').tobytes()==b.tobytes()
 q={'candidateId':ident,'sha256':r['sha256'],'dimensions':list(b.size),'mode':'RGB','alpha':'opaque','exact4x':'PASS','changedPixels':len(actual),'unexpectedChangesOutsidePredeclaredMasks':0,'allChangedPixelsAccountedFor':True,'sourcePlusLayerReconstructsFinal':True,'uniqueRGB':len(b.getcolors(b.width*b.height))}
 qa.append(q);row([src,file],ident+'-before-after')

mainids=['CH3-A04-verification-continuity','CH3-C01-urgency','CH3-C03-locomotion','CH3-C04-surprise']
bgids=['CH3-A05-verification-bg-continuity','CH3-C02-urgency-bg','CH3-C05-surprise-bg']
wall_checks=[]
for ids,box in [(mainids,(277,50,314,135)),(bgids,(496,20,564,193))]:
 reference=rgb(R/byid[ids[0]]['file']).crop(box).tobytes()
 for ident in ids:
  assert rgb(R/byid[ident]['file']).crop(box).tobytes()==reference
  wall_checks.append({'candidateId':ident,'box':list(box),'pixelDifferences':0})

# Native source sprite identity/scale checks and firing-side semantics.
fg_checks=[]
for ident,path,offset in [('CH3-C03-locomotion',V3/'layers/locomotion-presenter-original-silhouette.png',(0,1)),('CH3-C04-surprise',R/'layers/surprise-presenter-firing-side.png',(0,0))]:
 sprite=rgba(path);final=rgba(R/byid[ident]['file']);count=0
 for y in range(sprite.height-offset[1]):
  for x in range(sprite.width):
   if sprite.getpixel((x,y))[3]:
    assert final.getpixel((x+offset[0],y+offset[1]))==sprite.getpixel((x,y)),(ident,x,y)
    count+=1
 fg_checks.append({'candidateId':ident,'exactForegroundPixels':count,'translation':list(offset),'scale':1,'pixelMismatches':0})
old_person=rgba(V3/'layers/surprise-presenter-front.png');new_person=rgba(R/'layers/surprise-presenter-firing-side.png')
old_bounds=old_person.getchannel('A').getbbox();new_bounds=new_person.getchannel('A').getbbox()
assert new_bounds[2]<168 and new_bounds[1]==old_bounds[1] and new_bounds[3]==old_bounds[3]
for y in range(206):
 for x in range(73,314):
  if old_person.getpixel((x,y))[3]:assert old_person.getpixel((x,y))==new_person.getpixel((x-73,y))
firing_side={'result':'PASS','cannonMouthX':168,'presenterBounds':list(new_bounds),'allPresenterPixelsLeftOfCannon':True,'horizontalMove':-73,'verticalMove':0,'resized':False,'spriteIdentityPixelsExact':True}
wall_geometry=read(R/'sources/wall-projection.json')
for p in wall_geometry:
 vx,vy=p['vanishingPoint'];corners=p['projectedCorners']
 for j,k in [(0,1),(3,2)]:
  x1,y1=corners[j];x2,y2=corners[k]
  assert abs((x1-vx)*(y2-vy)-(y1-vy)*(x2-vx))<1e-8
# The four heads share geometry/functions; only surprise's BEGIN light differs.
pedestal_checks=[]
from PIL import ImageDraw
for ids,points in [(mainids,[(225,129),(246,129),(246,132),(244,142),(220,142),(220,139)]),(bgids,[(424,187),(464,187),(464,191),(460,211),(418,211),(418,207)])]:
 first=rgba(R/byid[ids[0]]['file']);m=Image.new('L',first.size);ImageDraw.Draw(m).polygon(points,fill=255)
 for ident in ids:
  a=rgba(R/byid[ident]['file']);active=ident in ['CH3-C04-surprise','CH3-C05-surprise-bg']
  differences=sum(first.getpixel((x,y))!=a.getpixel((x,y)) for y in range(a.height) for x in range(a.width) if m.getpixel((x,y)))
  assert differences>0 if active else differences==0
  pedestal_checks.append({'candidateId':ident,'sameHeadGeometry':True,'activeBEGIN':active,'differencesFromInactiveHead':differences,'controlFunctions':['green BEGIN','covered red emergency release']})
hand=read(V2/'sources/bell-edit-spec.json')['protectedHandPixels'];src=rgba(V2/'candidates/CH3-C01-urgency-v02.png');out=rgba(R/byid['CH3-C01-urgency']['file'])
assert all(src.getpixel(tuple(p))==out.getpixel(tuple(p)) for p in hand)
for phase in read(V3/'sources/operation-coordinates.json'):
 if phase['operation'].startswith('Connect the net'):
  before=rgb(V3/'candidates/CH3-C03-locomotion-v03.png');after=rgb(R/byid['CH3-C03-locomotion']['file'])
  assert all(before.getpixel(tuple(p))==after.getpixel(tuple(p)) for p in phase['coordinates'])
assert rgb(V3/'candidates/CH3-C01-urgency-v03.png').crop((100,95,120,117)).tobytes()==rgb(R/byid['CH3-C01-urgency']['file']).crop((100,95,120,117)).tobytes()
row([V3/byid[i]['sourceFile'].split('/',1)[1] for i in mainids],'previous-v03-four-scenes')
row([R/byid[i]['file'] for i in mainids],'revised-four-scenes')
for tag,mi,bi in [('verification',mainids[0],bgids[0]),('urgency',mainids[1],bgids[1]),('surprise',mainids[3],bgids[2])]:row([R/byid[mi]['file'],R/byid[bi]['file']],tag+'-main-portrait')
for ident in mainids:row([R/byid[ident]['file'],V1/'references/chapter-01-foyer.png',V1/'references/chapter-02-groundskeeper.png'],ident+'-chapter-style')
details=[('presenter-on-firing-side','CH3-C04-surprise',(104,55,214,132)),('right-wall-main','CH3-C01-urgency',(276,50,314,135)),('right-wall-close','CH3-C02-urgency-bg',(496,20,564,193)),('pedestal-main','CH3-C04-surprise',(218,127,248,163)),('pedestal-close','CH3-C05-surprise-bg',(417,185,466,255))]
for name,ident,box in details:
 a=rgb(R.parent/byid[ident]['sourceFile']).crop(box);b=rgb(R/byid[ident]['file']).crop(box);sheet=Image.new('RGB',(a.width*2,a.height));sheet.paste(a,(0,0));sheet.paste(b,(a.width,0))
 sheet.resize((sheet.width*8,sheet.height*8),Image.Resampling.NEAREST).save(R/'comparisons'/f'{name}-before-after-8x.png')

# Geometry proof marks are never present in candidate images.
for kind,ident in [('main','CH3-A04-verification-continuity'),('close','CH3-A05-verification-bg-continuity')]:
 proof=rgb(R/byid[ident]['file']);d=ImageDraw.Draw(proof)
 for p in wall_geometry:
  if p['camera']!=kind:continue
  vx,vy=p['vanishingPoint']
  for x,y in p['projectedCorners']:d.line([(vx,vy),(round(x),round(y))],fill='#dfb65d')
 d.ellipse((vx-2,vy-2,vx+2,vy+2),fill='#fd7a86')
 proof.resize((proof.width*4,proof.height*4),Image.Resampling.NEAREST).save(R/'comparisons'/f'{kind}-wall-vanishing-point-4x.png')

oldmanifest=read(V2/'manifest.json');oldby={c['candidateId']:c for c in oldmanifest['candidates']};poses=[]
for ident in ['CH3-C06-presenter-excited','CH3-C07-presenter-alarmed','CH3-B07-attendant-alarmed']:
 p=V2/oldby[ident]['file'];assert sha(p)==oldby[ident]['sha256'];a=rgba(p);assert set(a.getchannel('A').tobytes())=={0,255}
 poses.append({'candidateId':ident,'file':'../v02-localized-corrections/'+oldby[ident]['file'],'sha256':sha(p),'status':'approved unchanged v02 reference','dimensions':list(a.size),'anchor':[0,0],'scale':1})
contexts=[(poses[0],bgids[1]),(poses[0],bgids[0]),(poses[1],bgids[2]),(poses[1],bgids[0])]
comps=[]
for fg,bgid in contexts:
 a=rgba(R/fg['file']);b=rgba(R/byid[bgid]['file']);b.alpha_composite(a,(0,0));file='composites/'+fg['candidateId']+'--'+bgid+'.png';b.convert('RGB').save(R/file)
 # Every visible foreground pixel survives exactly; no equipment relocation or
 # alpha processing is used to make a portrait fit its new environment.
 assert all(b.getpixel((x,y))==a.getpixel((x,y)) for y in range(278) for x in range(564) if a.getpixel((x,y))[3])
 assert not a.getchannel('A').crop((420,190,462,255)).getbbox()
 comps.append({'foreground':fg['candidateId'],'background':bgid,'file':file,'sha256':sha(R/file),'anchor':[0,0],'scale':1,'exactForegroundPixels':True,'pedestalOverlap':0})

preservation={'v01V02V03FilesBytePreserved':len(preserved),'protectedCurrentFilesUnchanged':len(protected),'pinnedBatchABHistoricalFilesVerified':hist_count,'approvedA04A05Unchanged':True,'threeApprovedPoseReferencesUnchanged':True,'narrativeRegistryProductionAndWorkflowsUnchanged':True}
report={'result':'PASS','candidateCount':7,'additionalA04A05Options':2,'candidates':qa,'wallContinuity':wall_checks,'presenterOcclusion':fg_checks,'cannonFiringSide':firing_side,'wallGeometry':wall_geometry,'pedestalClarity':pedestal_checks,'bellGrip':{'inheritedV03VerticalShift':3,'protectedFingerPixelsUnchanged':len(hand)},'composites':comps,'preservation':preservation,'canonicalQA':canonical,'browserQA':read(R/'browser-qa.json'),'nativeGridAuthorship':'UNRESOLVED / UNPROVEN. Local target-grid component edits do not certify original source authorship.','creativeApproval':'Seven v04 environment revisions unselected. Prior v02 approval retained historically; never auto-promote revisions.','pagesDeployed':False,'imageGenerationCalls':0}
write('qa.json',report);write('manifest.json',{'gameTitle':'Out of Order','version':'Chapter 3 Batch C v04 perspective and firing-side corrections','sourceSelectedCommit':SELECTED,'branch':'art/ch3-pavilion-batch03-20261119','narrativeBlob':'857ffdf1bc9432cf4bbbfd7819f5f430a06d9036','candidates':records,'approvedPoseReferences':poses,'composites':comps,'status':'generated/unselected revisions','selected':False,'approved':False,'assetPath':None,'pagesDeployed':False,'nativeGridAuthorship':'UNRESOLVED / UNPROVEN'})
(R/'CANDIDATE_HASHES.md').write_text('| Revision | SHA-256 |\n|---|---|\n'+''.join(f'| {r["candidateId"]} | `{r["sha256"]}` |\n' for r in records))
def art(path,scaled=True):
 a=Image.open(R/path);return f'<div class="viewport"><img class="{"scaled" if scaled else "fixed"}" src="{path}" width="{a.width}" height="{a.height}" data-w="{a.width}" data-h="{a.height}" alt="Pixel-art review proof"></div>'
style='*{box-sizing:border-box;min-width:0}body{margin:0;background:#17292f;color:#f4eadc;font:16px/1.5 system-ui}main{max-width:1380px;margin:auto;padding:24px}a{color:#a4dbd9}p,li,a,code,h1,h2,h3{overflow-wrap:anywhere}.viewport{max-width:100%;overflow:auto;border:1px solid #5c767d}.viewport img{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}.controls{position:sticky;top:0;background:#17292ff7;z-index:3;padding:12px 0}button{padding:10px 16px;font:inherit;background:#31505b;color:inherit;border:1px solid #90a5a4}button[aria-pressed=true]{background:#f0d1a7;color:#17272c}section,article{margin-top:28px;border-top:1px solid #5c767d;padding-top:18px}.notice{padding:16px;border-left:4px solid #e4b578;background:#503d31}.hash{font-size:13px}'
page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Out of Order — Chapter 3 v04 perspective corrections</title><style>'+style+'</style><main><h1>Chapter 3 — v04 perspective corrections</h1><p>Five Batch C environment revisions plus two separately labeled A04/A05 continuity options. The three approved portrait foregrounds remain unchanged.</p><p class="notice">All seven revised environments are unselected. Prior v02 and approved A04/A05 images remain immutable; this gallery does not approve or register replacements. Original native-grid authorship remains unresolved. No Pages deployment, gameplay integration or Batch D.</p><p><a href="../v02-localized-corrections/">Selected v02 history</a> · <a href="../v01/">v01 history</a> · <a href="qa.json">Technical QA</a> · <a href="manifest.json">Manifest</a> · <a href="CANDIDATE_HASHES.md">Hashes</a> · <a href="HANDOFF.md">Correction handoff</a> · <a href="browser-qa.json">Browser QA</a></p><div class="controls"><button data-scale="1" aria-pressed="true">Native 1×</button> <button data-scale="4" aria-pressed="false">Exact 4×</button></div><section id="continuity"><h2>Four-scene perspective and cannon placement</h2><p>Previous v03 sequence, then revised v04 sequence: verification / urgency / locomotion / surprise. The verification revisions are separate A04/A05 options; approved originals are untouched.</p>'+art('comparisons/previous-v03-four-scenes.png')+art('comparisons/revised-four-scenes.png')+'</section><section id="pairs"><h2>Main and independent portrait layouts</h2><p>Matching pedestals now show a large green BEGIN button and a separate red covered release. Wall plates, borders and slats converge to a shared vanishing point per camera. Urgency alone remains red. The main presenter is left of the left-pointing cannon mouth; the portrait foreground was already on that side.</p>'+''.join(art('comparisons/'+t+'-main-portrait.png') for t in ['verification','urgency','surprise'])+'</section><section id="details"><h2>Localized 8× before / after proofs</h2>'+''.join('<h3>'+name.replace('-',' ')+'</h3>'+art('comparisons/'+name+'-before-after-8x.png',False) for name,_,_ in details)+'</section>'
for r in records:
 ident=r['candidateId'];page+='<article class="candidate" id="'+ident+'"><h2>'+ident+'</h2><p><strong>Generated / unselected revision</strong>'+(' · Additional A04/A05 continuity option' if r['additionalContinuityOption'] else '')+'</p>'+art(r['file'])+'<ul>'+''.join('<li>'+html.escape(x)+'</li>' for x in r['operations'])+'</ul><p class="hash">SHA-256: <code>'+r['sha256']+'</code></p><p>Before / after:</p>'+art('comparisons/'+ident+'-before-after.png')+f'<p><a href="{r["file"]}">Native PNG</a> · <a href="previews/{ident}-v04-4x.png">Exact 4× PNG</a> · <a href="masks/{ident}-allowed.png">Predeclared edit mask</a> · <a href="masks/{ident}-changed.png">Exact changed mask</a> · <a href="sources/{ident}-changed-pixels.json">Every changed pixel</a></p></article>'
page+='<section id="geometry"><h2>Wall-plane proof overlays</h2><p>Rays show one declared vanishing point per camera. Overlays are absent from candidates.</p>'+art('comparisons/main-wall-vanishing-point-4x.png',False)+art('comparisons/close-wall-vanishing-point-4x.png',False)+'</section><section id="composites"><h2>Unchanged approved foregrounds on revised backgrounds</h2>'+''.join('<h3>'+c['foreground']+' / '+c['background']+'</h3>'+art(c['file']) for c in comps)+'</section><section><h2>Approved chapter style references</h2>'+''.join(art('comparisons/'+i+'-chapter-style.png') for i in mainids)+'</section><section><h2>Technical limits and provenance</h2><p>No image generation was called. All edits occur on the existing target grids. Native-authored flat wall components are projected locally; this derived component mapping does not establish original full-scene grid authorship. No scene resize or global filtering. Historical v01-v03 and approved images remain byte-preserved.</p><p><a href="sources/operation-coordinates.json">Operation coordinates</a> · <a href="sources/historical-preservation.json">Historical file pins</a> · <a href="sources/layout.json">Shared layout specification</a> · <a href="edit_scenes.py">Exact native edit implementation</a> · <a href="../v01/sources/generation-records.json">Original generation provenance</a> · <a href="PNG_SHA256SUMS.txt">PNG hashes</a> · <a href="SOURCE_SHA256SUMS.txt">Package hashes</a></p><p>PR #13 remains draft and pinned to historical selected v02; do not substitute these unselected revisions before Nate’s decision.</p></section></main><script>document.querySelectorAll("[data-scale]").forEach(b=>b.onclick=()=>{const s=+b.dataset.scale;document.querySelectorAll("img.scaled").forEach(i=>{i.width=+i.dataset.w*s;i.height=+i.dataset.h*s});document.querySelectorAll("[data-scale]").forEach(x=>x.setAttribute("aria-pressed",String(x===b)))});</script></html>'
(R/'index.html').write_text(page)
(R/'PNG_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(R).as_posix()}\n' for p in sorted(R.rglob('*.png'))))
(R/'SOURCE_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(R).as_posix()}\n' for p in sorted(R.rglob('*')) if p.is_file() and p.suffix!='.png' and p.name!='SOURCE_SHA256SUMS.txt'))
print(json.dumps({'result':'PASS','revisionCount':7,'preservation':preservation,'hashes':{r['candidateId']:r['sha256'] for r in records}},indent=2))
