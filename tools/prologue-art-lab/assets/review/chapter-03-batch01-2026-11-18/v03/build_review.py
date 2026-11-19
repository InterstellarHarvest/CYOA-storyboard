"""Package and independently verify the exact v03 native edits."""
from pathlib import Path
from PIL import Image
from collections import Counter
from html import escape
import json,hashlib,subprocess

R=Path(__file__).resolve().parent
B=R.parent
V2=B/'v02'
ROOT=B.parents[4]
PIN='32273a2839e3a941530a153b69fb9a508e92f57b'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):(R/p).write_text(json.dumps(v,indent=2)+'\n')
def rgba(p):return Image.open(p).convert('RGBA')
def same(a,b):return a.size==b.size and a.convert('RGBA').tobytes()==b.convert('RGBA').tobytes()
def picture(p,w,h,alt):return f'<div class="viewport"><img class="art" src="{p}" width="{w}" height="{h}" data-w="{w}" data-h="{h}" alt="{escape(alt)}"></div>'
def link(p,s):return f'<a href="{p}">{escape(s)}</a>'
checks=[]
def check(v,s):
 assert v,s
 checks.append(s)
def inside(x,y,ps):
 hit=False
 for i,(a,b) in enumerate(ps):
  c,d=ps[i-1]
  if (b>y)!=(d>y) and x<(c-a)*(y-b)/(d-b)+a:hit=not hit
 return hit

report=json.loads((R/'edit-report.json').read_text())
rows=report['candidates']
pins=json.loads((R/'sources/history-pins.json').read_text())
for p in pins['files']:check(sha(B/p['file'])==p['sha256'],'Historical bytes unchanged: '+p['file'])
check(len(rows)==6 and len(list((R/'candidates').glob('*.png')))==6,'Exactly six current v03 candidates')
for c in rows:
 p=R/c['candidate'];im=rgba(p);old=rgba(R/c['source']);w,h=im.size
 check([w,h]==c['dimensions'] and sha(p)==c['sha256'],c['id']+': exact dimensions/hash')
 check(sha(R/c['source'])==c['sourceSha256'],c['id']+': exact v02 source pin')
 check(c['status']=='generated' and c['selected'] is False and c['assetPath'] is None,c['id']+': generated/unselected with null assetPath')
 if not c['modified']:check(p.read_bytes()==(R/c['source']).read_bytes(),c['id']+': byte-identical carry-forward')
 alpha=set(im.getchannel('A').get_flattened_data())
 if c['character']:
  check(alpha=={0,255},c['id']+': binary alpha')
  expected=Image.new('RGBA',im.size);expected.paste(old,tuple(c['translation']))
  check(same(im,expected),c['id']+': exact integer translation; no scaling or color/detail changes')
  before=Counter(p for p in old.get_flattened_data() if p[3]);after=Counter(p for p in im.get_flattened_data() if p[3])
  check(before==after and c['clippedVisiblePixels']==0,c['id']+': every visible source pixel retained, including hair/fingers/costume')
  # Independent spatial scope: only the union of old/new occupied pixels changes.
  check(all(a==b or a[3]>0 or b[3]>0 for a,b in zip(old.get_flattened_data(),im.get_flattened_data())),c['id']+': no changes outside old/new sprite silhouettes')
 else:check(alpha=={255},c['id']+': opaque environment')
 if c['id']=='CH3-A02-restroom-bg':
  diffs=[(x,y) for y in range(h) for x in range(w) if im.getpixel((x,y))!=old.getpixel((x,y))]
  check(len(diffs)==3761 and all(inside(x+.5,y+.5,c['allowedRegion']) for x,y in diffs),'A02: all 3,761 changed pixels inside device/shadow removal polygon')
  check(im.crop((0,0,394,h)).tobytes()==old.crop((0,0,394,h)).tobytes(),'A02: left microphone, gate/access hardware and remaining left scene untouched')
  check(im.crop((485,0,w,h)).tobytes()==old.crop((485,0,w,h)).tobytes(),'A02: plant and right architecture untouched')
  check(set(im.get_flattened_data()).issubset(set(old.get_flattened_data())),'A02: only existing original RGB colors used; no generated or filtered pixels')
 prev='previews/'+c['id']+'-v03-4x.png';im.resize((4*w,4*h),Image.Resampling.NEAREST).save(R/prev)
 check(same(rgba(R/prev),im.resize((4*w,4*h),Image.Resampling.NEAREST)),c['id']+': exact 4x integer preview')
 c['preview4x']=prev;c['previewSha256']=sha(R/prev)
 pair=Image.new('RGBA',(2*w+16,h),(240,235,222,255));pair.alpha_composite(old);pair.alpha_composite(im,(w+16,0))
 cp='comparisons/'+c['id']+'-v02-v03.png';pair.convert('RGB').save(R/cp);c['comparison']=cp;c['comparisonSha256']=sha(R/cp)

comps=[]
for char,bid,fid in [('attendant','CH3-A02-restroom-bg','CH3-A03-attendant-idle'),('presenter','CH3-A05-verification-bg','CH3-A06-presenter-idle')]:
 bg=rgba(R/'candidates'/f'{bid}-v03.png');fg=rgba(R/'candidates'/f'{fid}-v03.png')
 comp=Image.alpha_composite(bg,fg).convert('RGB');p=f'composites/{char}-v03.png';comp.save(R/p)
 prev=f'composites/{char}-v03-4x.png';comp.resize((2256,1112),Image.Resampling.NEAREST).save(R/prev)
 check(same(rgba(R/p),Image.alpha_composite(bg,fg)),char+': actual candidate PNGs composited exactly')
 for label,color in [('white','white'),('dark','#19222e')]:
  b=Image.new('RGBA',fg.size,color);b.alpha_composite(fg);b.convert('RGB').save(R/f'composites/{char}-on-{label}.png')
 old=rgba(V2/'composites'/f'{char}-v02.png');pair=Image.new('RGBA',(1144,278),'#f0ebde');pair.alpha_composite(old);pair.alpha_composite(comp.convert('RGBA'),(580,0));cp=f'comparisons/{char}-composite-v02-v03.png';pair.convert('RGB').save(R/cp)
 comps.append({'character':char,'file':p,'sha256':sha(R/p),'preview4x':prev,'comparison':cp,'background':bid,'foreground':fid})

oldDesk=rgba(V2/'candidates/CH3-A02-restroom-bg-v02.png').crop((350,190,564,278))
newDesk=rgba(R/'candidates/CH3-A02-restroom-bg-v03.png').crop((350,190,564,278))
deskPair=Image.new('RGBA',(444,88),'#f0ebde');deskPair.alpha_composite(oldDesk);deskPair.alpha_composite(newDesk,(230,0))
deskPair.convert('RGB').save(R/'diagnostics/desk-removal-native-comparison.png')
deskPair.convert('RGB').resize((1776,352),Image.Resampling.NEAREST).save(R/'diagnostics/desk-removal-comparison-4x.png')
a=rgba(R/'candidates/CH3-A03-attendant-idle-v03.png');p=rgba(R/'candidates/CH3-A06-presenter-idle-v03.png')
def occupied(im,box):return sum(im.getpixel((x,y))[3]>0 for y in range(box[1],box[3]) for x in range(box[0],box[2]))
micbox=[95,201,212,270];camerabox=[17,135,150,201];standbox=[177,145,187,270]
check(occupied(a,micbox)==0,'Attendant: full left microphone/intercom region, including base, unobscured')
check(occupied(p,camerabox)==0,'Presenter: large camera body unobscured')
check(occupied(p,standbox)>0,'Presenter: overlaps microphone stand')
check(any(p.getpixel((x,277))[3]==255 for x in range(564)),'Presenter: torso reaches lower canvas edge')
glyphs={'3':['11110','00001','00001','01110','00001','00001','11110'],'0':['01110','10001','10001','10001','10001','10001','01110']}
glyphpoints=[]
for k,ch in enumerate('30'):
 for y,line in enumerate(glyphs[ch]):
  for x,bit in enumerate(line):
   if bit=='1':glyphpoints.extend((xx,yy) for yy in range(96+y*5,96+(y+1)*5) for xx in range(265+(k*6+x)*5,265+(k*6+x+1)*5))
occluded=sum(p.getpixel(pt)[3]>0 for pt in glyphpoints)
check(occluded==0,'Presenter: all 775 ink pixels of both countdown digits remain unobscured')
composition={'attendantMicrophoneRegion':micbox,'attendantMicrophoneOccludedPixels':occupied(a,micbox),'presenterCameraBodyRegion':camerabox,'presenterCameraBodyOccludedPixels':occupied(p,camerabox),'presenterMicrophoneStandRegion':standbox,'presenterMicrophoneStandOverlapPixels':occupied(p,standbox),'countdownGlyphPixels':len(glyphpoints),'countdownOccludedGlyphPixels':occluded,'competingCompositionRequired':False}
subprocess.run(['git','diff','--exit-code',PIN,'--','story','assets/selected','tools/storyboard'],cwd=ROOT,check=True,stdout=subprocess.PIPE)
checks.append('Narrative, canonical items/catalogue, selected production art and storyboard source unchanged')
save('manifest.json',{'version':'v03','sourcePin':PIN,'branch':'art/ch3-pavilion-batch01-20261118','status':'generated','selected':False,'generationCalls':0,'nativeAuthorship':'UNPROVEN; inherited v02 source transfer/soft tonal variation remains. No original-native pass claimed.','candidates':rows,'composites':comps,'composition':composition,'continuityConcern':'A01 retains the tiny desktop device; carried byte-identically under explicit preservation rule. A separate Nate-approved A01 cleanup would be needed for exact prop continuity.'})
save('qa.json',{'reviewIntegrity':'PASS','pixelPreservation':'PASS','dimensions':'PASS','foregroundAlpha':'PASS — 0/255 only','integer4xPreviews':'PASS','historyPreservation':f'PASS — {len(pins["files"])} pinned historical files unchanged','originalNativeAuthorship':'UNPROVEN / outstanding requirement not passed','composition':composition,'checksPassed':len(checks),'checks':checks})
(R/'CANDIDATE_HASHES.md').write_text('# v03 — generated / unselected\n\n'+'\n'.join(f'- `{c["id"]}-v03` — `{c["sha256"]}`'+(' (byte-identical v02 carry-forward)' if not c['modified'] else '') for c in rows)+'\n')
(R/'gallery.css').write_bytes((V2/'gallery.css').read_bytes())
notes=json.loads((R/'sources/change-notes.json').read_text())
parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 3 Batch A v03 — pixel-preserving corrections</title><link rel="stylesheet" href="gallery.css"><body><header><div class="eyebrow">OUT OF ORDER / THE ACCEPTABLE ERROR · CHAPTER 3 · BATCH A · V03</div><h1>Small moves, preserved pixels</h1><p class="status">SIX CANDIDATES · GENERATED / UNSELECTED</p><p>Integer translations and one localized desk-device removal. No character regeneration, scaling or global filtering. Compare v02 on the left with v03 on the right. A01, A04 and A05 are byte-identical carry-forwards.</p><p class="note"><strong>Outstanding:</strong> Original native-grid authorship is still unproven; soft source-derived tonal variation is inherited unchanged. A01 still shows the tiny desk device because its pixels are explicitly protected. Any A01 continuity cleanup needs Nate’s separate approval.</p><nav><a href="#restroom">Attendant set</a><a href="#stage">Presenter set</a><a href="#composites">Before / after composites</a><a href="#evidence">Exact scope and QA</a><a href="../v02/">Immutable v02</a><a href="../">Immutable v01</a></nav></header><div class="toolbar"><span>Inspect:</span><button data-scale="1" aria-pressed="true">Native 1×</button><button data-scale="4" aria-pressed="false">Nearest 4×</button><span class="muted">Pixel-exact integer presentation.</span></div><main>']
for anchor,title,group in [('restroom','Restroom and attendant',rows[:3]),('stage','Stage and presenter',rows[3:])]:
 parts.append(f'<section id="{anchor}"><h2>{title}</h2>')
 for c in group:
  w,h=c['dimensions'];role='MODIFIED' if c['modified'] else 'UNCHANGED · BYTE-IDENTICAL V02 CARRY-FORWARD'
  parts.append(f'<article class="card candidate" id="{c["id"]}"><h3>{c["id"]} · v03</h3><p class="status">{role}</p><p>{escape(notes[c["id"]])}</p>'+picture(c['candidate'],w,h,c['id']+' v03')+f'<p><code class="hash">SHA-256 {c["sha256"]}</code></p><div class="links">'+link(c['candidate'],'Native PNG')+link(c['preview4x'],'Exact 4× PNG')+link(c['source'],'Pinned v02 PNG')+'</div><details open><summary>v02 left / v03 right · same native canvas</summary>'+picture(c['comparison'],2*w+16,h,c['id']+' v02 left and v03 right')+'</details>')
  if c['id']=='CH3-A02-restroom-bg':parts.append('<details open><summary>Localized desktop removal · v02 left / v03 right</summary>'+picture('diagnostics/desk-removal-native-comparison.png',444,88,'Desk device and shadow before and after')+'</details>')
  parts.append('</article>')
 parts.append('</section>')
parts.append('<section id="composites"><h2>Compositions, before and after</h2><p>The attendant’s microphone and base are fully visible. The presenter overlaps the stand while all 775 countdown-ink pixels and the large camera body stay unobscured. Both goals fit in the same composition; no competing layout is required.</p>')
for c in comps:
 char=c['character'];parts.append(f'<article class="card"><h3>{char.title()} · actual v03 layers</h3>'+picture(c['file'],564,278,char+' v03 composite')+'<details open><summary>Composite v02 left / v03 right</summary>'+picture(c['comparison'],1144,278,char+' before and after composite')+'</details><details><summary>Unchanged silhouettes on white and dark backings</summary>'+picture(f'composites/{char}-on-white.png',564,278,char+' white backing')+picture(f'composites/{char}-on-dark.png',564,278,char+' dark backing')+'</details></article>')
parts.append('</section><section id="evidence"><h2>Exact change scope, anchors and validation</h2><p>All visible sprite RGBA pixels are preserved at scale 1. Only their integer coordinates change. A02’s device and shadow are replaced with original adjacent wall/desk pixels inside the declared polygon; the gate hardware, plant and surrounding architecture remain untouched.</p><div class="links">')
for p,title in [('CHANGELOG.md','Exact offsets and edit region'),('VISUAL_QA.md','Visual results and outstanding concerns'),('CANDIDATE_HASHES.md','All six SHA-256 hashes'),('manifest.json','Modified versus unchanged files'),('qa.json','Pixel and composition QA'),('browser-qa.json','Browser QA'),('edit-report.json','Native edit ledger'),('sources/pose-anchors.json','Updated fixed anchors'),('sources/history-pins.json','All historical file hashes'),('sources/owner-v03-instructions.txt','Exact owner instructions'),('edit-native.mjs','Reproducible native edits'),('PNG_SHA256SUMS.txt','PNG checksums'),('SOURCE_SHA256SUMS.txt','Source checksums'),('README.md','Package guide')]:parts.append(link(p,title))
parts.append('</div><p class="note"><strong>Stop for Nate’s review.</strong> No image selected, approved or integrated. No narrative, item, approved artwork, gameplay or public-main change. Batch B remains untouched.</p></section></main><footer>Pinned v02 source '+PIN+' · no image-generation calls · native pixel-preserving edits</footer><script>for(const b of document.querySelectorAll("[data-scale]"))b.addEventListener("click",()=>{const s=Number(b.dataset.scale);for(const i of document.querySelectorAll("img.art")){i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;}for(const a of document.querySelectorAll("[data-scale]"))a.setAttribute("aria-pressed",String(a===b));});</script></body></html>')
(R/'index.html').write_text('\n'.join(parts))
(R/'PNG_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(R)}\n' for p in sorted(R.rglob('*.png'))))
sources=[p for p in R.rglob('*') if p.is_file() and (p.is_relative_to(R/'sources') or p.name in ['edit-native.mjs','build_review.py','CHANGELOG.md','VISUAL_QA.md','README.md','qa-browser.cjs','package.json'])]
(R/'SOURCE_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(R)}\n' for p in sorted(sources)))
print(json.dumps({'result':'PASS','checks':len(checks),'historicalFilesPreserved':len(pins['files']),'composition':composition,'hashes':{c['id']:c['sha256'] for c in rows}},indent=2))
