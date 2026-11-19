"""Package and independently inspect v04 localized native corrections."""
from pathlib import Path
from PIL import Image
from collections import Counter
from html import escape
import json,hashlib,subprocess,math
R=Path(__file__).resolve().parent;B=R.parent;V3=B/'v03';ROOT=B.parents[4]
PIN='0df9994a1162528cc0de33add680a7d43717b4fa'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):(R/p).write_text(json.dumps(v,indent=2)+'\n')
def rgba(p):return Image.open(p).convert('RGBA')
def same(a,b):return a.size==b.size and a.convert('RGBA').tobytes()==b.convert('RGBA').tobytes()
def picture(p,w,h,alt):return f'<div class="viewport"><img class="art" src="{p}" width="{w}" height="{h}" data-w="{w}" data-h="{h}" alt="{escape(alt)}"></div>'
def link(p,t):return f'<a href="{p}">{escape(t)}</a>'
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
def distance(x,y,a,b):
 dx=b[0]-a[0];dy=b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy))) if dx or dy else 0
 return math.hypot(x-a[0]-t*dx,y-a[1]-t*dy)
report=json.loads((R/'edit-report.json').read_text());rows=report['candidates']
pins=json.loads((R/'sources/history-pins.json').read_text())
for p in pins['files']:check(sha(B/p['file'])==p['sha256'],'Historical file unchanged: '+p['file'])
check(len(rows)==6 and len(list((R/'candidates').glob('*.png')))==6,'Exactly six current candidates')
for c in rows:
 im=rgba(R/c['candidate']);old=rgba(R/c['source']);w,h=im.size
 check([w,h]==c['dimensions'] and sha(R/c['candidate'])==c['sha256'],c['id']+': native dimensions/hash')
 check(sha(R/c['source'])==c['sourceSha256'],c['id']+': pinned v03 source')
 check(c['status']=='generated' and c['selected'] is False and c['assetPath'] is None,c['id']+': unselected/no production path')
 if not c['modified']:check((R/c['candidate']).read_bytes()==(R/c['source']).read_bytes(),c['id']+': byte-identical carry-forward')
 alpha=set(im.getchannel('A').get_flattened_data())
 check(alpha==({0,255} if c['character'] else {255}),c['id']+': correct opaque/binary-alpha contract')
 if c['id']=='CH3-A06-presenter-idle':
  expected=Image.new('RGBA',im.size);expected.paste(old,(-28,0));check(same(im,expected),'Presenter: exact -28/0 translation, no scaling or color changes')
  check(Counter(p for p in im.get_flattened_data() if p[3])==Counter(p for p in old.get_flattened_data() if p[3]),'Presenter: every visible RGBA source pixel preserved; no clipping')
 if c['id']=='CH3-A01-restroom':
  ledger=json.loads((R/'sources/a01-pixel-ledger.json').read_text());strokes=json.loads((R/'sources/outline-strokes.json').read_text())['strokes']
  points={(x,y) for y in range(h) for x in range(w) if im.getpixel((x,y))!=old.getpixel((x,y))}
  check(len(points)==934 and points=={(p['x'],p['y']) for p in ledger},'A01: complete exact 934-pixel before/after ledger')
  check(all(list(old.getpixel((p['x'],p['y'])))==p['before'] and list(im.getpixel((p['x'],p['y'])))==p['after'] for p in ledger),'A01: ledger matches actual source and final pixels')
  check(all(inside(x+.5,y+.5,report['deviceRemovalPolygon']) or any(distance(x,y,a,b)<.72 for s in strokes for a,b in zip(s['points'],s['points'][1:])) for x,y in points),'A01: no changes outside device polygon and authored one-pixel contour strokes')
  check(sum(p['reason']=='desktop device/base removal' for p in ledger)==138,'A01: device-removal scope is 138 pixels')
 prev='previews/'+c['id']+'-v04-4x.png';im.resize((4*w,4*h),Image.Resampling.NEAREST).save(R/prev)
 check(same(rgba(R/prev),im.resize((4*w,4*h),Image.Resampling.NEAREST)),c['id']+': exact 4x pixels')
 c['preview4x']=prev;c['previewSha256']=sha(R/prev)
 pair=Image.new('RGBA',(2*w+16,h),'#f0ebde');pair.alpha_composite(old);pair.alpha_composite(im,(w+16,0));cp='comparisons/'+c['id']+'-v03-v04.png';pair.convert('RGB').save(R/cp);c['comparison']=cp;c['comparisonSha256']=sha(R/cp)
comps=[]
for char,bid,fid in [('attendant','CH3-A02-restroom-bg','CH3-A03-attendant-idle'),('presenter','CH3-A05-verification-bg','CH3-A06-presenter-idle')]:
 bg=rgba(R/'candidates'/f'{bid}-v04.png');fg=rgba(R/'candidates'/f'{fid}-v04.png');comp=Image.alpha_composite(bg,fg).convert('RGB');p=f'composites/{char}-v04.png';comp.save(R/p)
 prev=f'composites/{char}-v04-4x.png';comp.resize((2256,1112),Image.Resampling.NEAREST).save(R/prev)
 check(same(rgba(R/p),Image.alpha_composite(bg,fg)),char+': actual candidate layers composed correctly')
 for label,color in [('white','white'),('dark','#19222e')]:
  backing=Image.new('RGBA',fg.size,color);backing.alpha_composite(fg);backing.convert('RGB').save(R/f'composites/{char}-on-{label}.png')
 old=rgba(V3/'composites'/f'{char}-v03.png');pair=Image.new('RGBA',(1144,278),'#f0ebde');pair.alpha_composite(old);pair.alpha_composite(comp.convert('RGBA'),(580,0));cp=f'comparisons/{char}-composite-v03-v04.png';pair.convert('RGB').save(R/cp)
 comps.append({'character':char,'file':p,'preview4x':prev,'comparison':cp,'sha256':sha(R/p)})

# Exact pixel crops expose native outline changes instead of a sharpening filter.
old=rgba(V3/'candidates/CH3-A01-restroom-v03.png');new=rgba(R/'candidates/CH3-A01-restroom-v04.png')
for name,box in [('npc',(199,93,241,142)),('device',(229,130,254,145))]:
 a=old.crop(box);b=new.crop(box);w,h=a.size;pair=Image.new('RGBA',(2*w+8,h),'#f0ebde');pair.alpha_composite(a);pair.alpha_composite(b,(w+8,0));pair.convert('RGB').save(R/f'diagnostics/{name}-native-comparison.png');pair.convert('RGB').resize(((2*w+8)*4,h*4),Image.Resampling.NEAREST).save(R/f'diagnostics/{name}-comparison-4x.png')

fg=rgba(R/'candidates/CH3-A06-presenter-idle-v04.png')
micrects=[[172,143,193,173],[179,172,185,263],[161,262,202,272]]
micpoints={(x,y) for a,b,c,d in micrects for y in range(b,d) for x in range(a,c)}
uncovered=sum(fg.getpixel(p)[3]!=255 for p in micpoints)
check(uncovered==0,'Presenter: full microphone head, stem and base mask covered')
check(all(fg.getpixel((x,y))[3]==0 for y in range(96,131) for x in range(265,320)),'Presenter: complete 30 digit region remains unobscured')
check(any(fg.getpixel((x,277))[3] for x in range(564)),'Presenter: lower body still reaches canvas edge')
cameraCovered=sum(fg.getpixel((x,y))[3]>0 for y in range(135,201) for x in range(17,150))
composition={'microphoneMaskRectangles':micrects,'microphoneMaskPixels':len(micpoints),'uncoveredMicrophoneMaskPixels':uncovered,'countdownDigitRegion':[265,96,320,131],'countdownOccludedPixels':0,'cameraBodyBoundingRegion':[17,135,150,201],'cameraBoundingRegionPixels':8778,'cameraBoundingRegionOverlappedPixels':cameraCovered,'cameraAssessment':'Recognizable in native/4x visual inspection; limited right-edge overlap is disclosed. The additional -28 shift is the smallest integer shift covering the conservative microphone mask.'}
subprocess.run(['git','diff','--exit-code',PIN,'--','story','assets/selected','tools/storyboard'],cwd=ROOT,check=True,stdout=subprocess.PIPE)
checks.append('Narrative, items/catalogue, selected production art and storyboard source untouched')
save('manifest.json',{'version':'v04','sourcePin':PIN,'branch':'art/ch3-pavilion-batch01-20261118','status':'generated','selected':False,'generationCalls':0,'nativeAuthorship':'UNPROVEN: inherited derived RGB remains; targeted native inking is not a full native redraw.','candidates':rows,'composites':comps,'composition':composition})
save('qa.json',{'reviewIntegrity':'PASS','pixelScope':'PASS','dimensions':'PASS','foregroundAlpha':'PASS','exact4x':'PASS','historyPreservation':f'PASS: {len(pins["files"])} historical files unchanged','nativeGridAuthorship':'UNPROVEN / NOT PASSED','composition':composition,'checksPassed':len(checks),'checks':checks})
(R/'CANDIDATE_HASHES.md').write_text('# v04 — generated / unselected\n\n'+'\n'.join(f'- `{c["id"]}-v04` — `{c["sha256"]}`'+(' (unchanged v03 bytes)' if not c['modified'] else '') for c in rows)+'\n')
(R/'gallery.css').write_bytes((V3/'gallery.css').read_bytes());notes=json.loads((R/'sources/change-notes.json').read_text())
parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 3 Batch A v04 — full microphone coverage and native outlines</title><link rel="stylesheet" href="gallery.css"><body><header><div class="eyebrow">OUT OF ORDER / THE ACCEPTABLE ERROR · CHAPTER 3 · BATCH A · V04</div><h1>Clearer outlines, complete microphone coverage</h1><p class="status">GENERATED / UNSELECTED · SIX CANDIDATES</p><p>The presenter moves another 28 pixels left. A01’s contactless device is removed, matching the portrait background. Selected native dark contours are reinforced, especially the seated attendant. No regeneration or global filter.</p><p class="note">The prior 4× export was already exact nearest-neighbor; its softness was baked into native RGB. This pass repairs selected contours, not the entire source rendering. Original native-grid authorship remains unproven; untouched soft tonal variation remains.</p><nav><a href="#restroom">Restroom / outline comparisons</a><a href="#stage">Presenter placement</a><a href="#composites">Composite comparison</a><a href="#evidence">Exact changes and QA</a><a href="../v03/">Immutable v03</a></nav></header><div class="toolbar"><span>Inspect:</span><button data-scale="1" aria-pressed="true">Native 1×</button><button data-scale="4" aria-pressed="false">Nearest 4×</button></div><main>']
for anchor,title,group in [('restroom','Restroom and attendant',rows[:3]),('stage','Stage and presenter',rows[3:])]:
 parts.append(f'<section id="{anchor}"><h2>{title}</h2>')
 for c in group:
  w,h=c['dimensions'];role='MODIFIED' if c['modified'] else 'UNCHANGED V03 BYTES';parts.append(f'<article class="card candidate" id="{c["id"]}"><h3>{c["id"]} · v04</h3><p class="status">{role}</p><p>{escape(notes[c["id"]])}</p>'+picture(c['candidate'],w,h,c['id']+' v04')+f'<p><code class="hash">SHA-256 {c["sha256"]}</code></p><div class="links">'+link(c['candidate'],'Native PNG')+link(c['preview4x'],'Exact 4× PNG')+link(c['source'],'Pinned v03 PNG')+'</div><details open><summary>v03 left / v04 right</summary>'+picture(c['comparison'],2*w+16,h,c['id']+' before and after')+'</details>')
  if c['id']=='CH3-A01-restroom':
   parts.append('<details open><summary>Native seated-NPC detail · v03 left / v04 right · use 4× control</summary>'+picture('diagnostics/npc-native-comparison.png',92,49,'NPC contour comparison')+'</details><details open><summary>Desktop device removal · v03 left / v04 right</summary>'+picture('diagnostics/device-native-comparison.png',58,15,'Main-scene desktop device removal')+'</details>')
  parts.append('</article>')
 parts.append('</section>')
parts.append('<section id="composites"><h2>Complete presenter composition</h2><p>The microphone head, stem and base are fully hidden. Both countdown digits remain clear. The camera remains recognizable, with a limited overlap along its right side.</p>')
for c in comps:
 char=c['character'];parts.append(f'<article class="card"><h3>{char.title()} · v04 actual layers</h3>'+picture(c['file'],564,278,char+' v04 composite')+'<details open><summary>Composite v03 left / v04 right</summary>'+picture(c['comparison'],1144,278,char+' composite comparison')+'</details><details><summary>White / dark silhouette proofs</summary>'+picture(f'composites/{char}-on-white.png',564,278,char+' white proof')+picture(f'composites/{char}-on-dark.png',564,278,char+' dark proof')+'</details></article>')
parts.append('</section><section id="evidence"><h2>Change scope and validation</h2><p>A01 changes exactly 934 pixels: 138 device-removal pixels, 200 attendant contour pixels and 596 architectural contour pixels. Every before/after RGBA value and reason is recorded. All four other images are byte-identical carry-forwards; the presenter’s visible pixel colors/details are losslessly retained.</p><div class="links">')
for p,t in [('CHANGELOG.md','Exact changes'),('VISUAL_QA.md','Visual results / remaining limitations'),('CANDIDATE_HASHES.md','Six SHA-256 hashes'),('qa.json','Automated QA'),('browser-qa.json','Browser checks'),('manifest.json','Candidate provenance'),('sources/a01-pixel-ledger.json','A01 pixel-by-pixel ledger'),('sources/outline-strokes.json','Authored native contour strokes'),('sources/pose-anchors.json','Updated anchors'),('sources/history-pins.json','Historical hashes'),('PNG_SHA256SUMS.txt','PNG checksums'),('SOURCE_SHA256SUMS.txt','Code/source checksums'),('README.md','Package guide')]:parts.append(link(p,t))
parts.append('</div><p class="note">Stop for Nate’s selection. No approval, integration, narrative/item/gameplay/production-art change, public-main merge or Batch B work.</p></section></main><footer>Pinned v03 '+PIN+' · native localized edits only</footer><script>for(const b of document.querySelectorAll("[data-scale]"))b.addEventListener("click",()=>{const s=Number(b.dataset.scale);for(const i of document.querySelectorAll("img.art")){i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;}for(const a of document.querySelectorAll("[data-scale]"))a.setAttribute("aria-pressed",String(a===b));});</script></body></html>')
(R/'index.html').write_text('\n'.join(parts))
(R/'PNG_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(R)}\n' for p in sorted(R.rglob('*.png'))))
sources=[p for p in R.rglob('*') if p.is_file() and (p.is_relative_to(R/'sources') or p.name in ['edit-native.mjs','build_review.py','CHANGELOG.md','VISUAL_QA.md','README.md','qa-browser.cjs','package.json'])]
(R/'SOURCE_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(R)}\n' for p in sorted(sources)))
print(json.dumps({'result':'PASS','checks':len(checks),'preservedHistory':len(pins['files']),'composition':composition,'hashes':{c['id']:c['sha256'] for c in rows}},indent=2))
