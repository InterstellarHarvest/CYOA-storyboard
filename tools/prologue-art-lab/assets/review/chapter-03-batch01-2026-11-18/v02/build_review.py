"""Package/verify finished native files; never alter candidate artwork."""
from pathlib import Path
from PIL import Image
from html import escape
import json,hashlib,subprocess

R=Path(__file__).resolve().parent
V1=R.parent
ROOT=V1.parents[4]
PIN='99b74b63a3407aafe7a468c2915291c997563700'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):(R/p).write_text(json.dumps(v,indent=2)+'\n')
def same(a,b):return a.size==b.size and a.convert('RGBA').tobytes()==b.convert('RGBA').tobytes()
def picture(p,w,h,alt):return f'<div class="viewport"><img class="art" src="{p}" width="{w}" height="{h}" data-w="{w}" data-h="{h}" alt="{escape(alt)}"></div>'
def link(p,s):return f'<a href="{p}">{escape(s)}</a>'

rows=json.loads((R/'realization-report.json').read_text())['candidates']
pins=json.loads((R/'sources/v01-pins.json').read_text())
checks=[]
def check(v,s):
 assert v,s
 checks.append(s)
for p in pins['files']:check(sha(V1/p['file'])==p['sha256'],'v01 unchanged: '+p['file'])
check(len(rows)==6,'Exactly six v02 candidates')
check(len(list((R/'candidates').glob('*.png')))==6,'No extra selectable native candidates')
for c in rows:
 p=R/c['candidate'];im=Image.open(p);w,h=im.size
 check([w,h]==c['dimensions'] and sha(p)==c['sha256'],c['id']+': dimension and candidate hash')
 check(c['status']=='generated' and c['selected'] is False and c['assetPath'] is None,c['id']+': unselected; no production path')
 check(sha(R/'generation-source'/c['filename'])==c['sourceSha256'],c['id']+': immutable tool-source hash')
 check(sha(R/c['prompt'])==c['promptSha256'],c['id']+': exact submitted prompt')
 check([sha(R/p) for p in c['references']]==c['referenceHashes'],c['id']+': supplied reference order/hashes')
 raw=Path(c['originalToolPath'])
 if raw.exists():check(sha(raw)==c['sourceSha256'],c['id']+': raw copy matches original tool output')
 alphas=set(im.convert('RGBA').getchannel('A').get_flattened_data())
 if c['character']:
  check(alphas=={0,255},c['id']+': strictly binary alpha')
  check(c['headroom']>=16 and c['bottomClearance']>=12,c['id']+': head and bottom clearance')
  check(c['silhouette']['offset']==json.loads((R/'sources/silhouettes.json').read_text())[c['character']]['offset'],c['id']+': declared fixed canvas anchor')
  check(c['changesBeyondSourceTransfer']>1000,c['id']+': manually reconstructed silhouette differs from simple source transfer')
 else:check(alphas=={255},c['id']+': opaque environment')
 prev='previews/'+c['id']+'-v02-4x.png'
 im.resize((4*w,4*h),Image.Resampling.NEAREST).save(R/prev)
 check(same(Image.open(R/prev),im.resize((4*w,4*h),Image.Resampling.NEAREST)),c['id']+': exact 4x pixels')
 c['preview4x']=prev;c['previewSha256']=sha(R/prev)
 old=Image.open(V1/'candidates'/f'{c["id"]}-v01.png').convert('RGBA')
 pair=Image.new('RGBA',(2*w+16,h),(240,235,222,255))
 pair.alpha_composite(old,(0,0));pair.alpha_composite(im.convert('RGBA'),(w+16,0))
 cp='comparisons/'+c['id']+'-v01-v02.png';pair.convert('RGB').save(R/cp)
 c['comparison']=cp;c['comparisonSha256']=sha(R/cp)
 c['v01']='../candidates/'+c['id']+'-v01.png';c['v01Sha256']=sha(R/c['v01'])

comps=[]
for char,bid,fid in [('attendant','CH3-A02-restroom-bg','CH3-A03-attendant-idle'),('presenter','CH3-A05-verification-bg','CH3-A06-presenter-idle')]:
 bg=Image.open(R/'candidates'/f'{bid}-v02.png').convert('RGBA');fg=Image.open(R/'candidates'/f'{fid}-v02.png').convert('RGBA')
 comp=Image.alpha_composite(bg,fg).convert('RGB');p=f'composites/{char}-v02.png';comp.save(R/p)
 prev=f'composites/{char}-v02-4x.png';comp.resize((2256,1112),Image.Resampling.NEAREST).save(R/prev)
 check(same(Image.open(R/p),Image.alpha_composite(bg,fg)),char+': exact foreground/background composite')
 for label,color in [('white','white'),('dark','#19222e')]:
  b=Image.new('RGBA',fg.size,color);b.alpha_composite(fg);b.convert('RGB').save(R/f'composites/{char}-on-{label}.png')
 old=Image.open(V1/'composites'/f'{char}-background-foreground.png').convert('RGBA');pair=Image.new('RGBA',(1144,278),'#f0ebde');pair.alpha_composite(old);pair.alpha_composite(comp.convert('RGBA'),(580,0));cp=f'comparisons/{char}-composite-v01-v02.png';pair.convert('RGB').save(R/cp)
 comps.append({'character':char,'file':p,'sha256':sha(R/p),'preview4x':prev,'comparison':cp,'background':bid,'foreground':fid})

# Prove native bitmap glyphs and unchanged stage pixels outside the digit discs.
for c in rows:
 if not c['id'].startswith(('CH3-A04','CH3-A05')):continue
 edit=next(e for e in c['nativeEdits'] if e['kind']=='native bitmap 30');cx,cy=edit['center'];rad=edit['clearDiscRadius'];s=edit['scale']
 im=Image.open(R/c['candidate']).convert('RGBA');guide=Image.open(R/'construction-guides'/f'{c["id"]}-transfer-only.png').convert('RGBA')
 start=round(cx-11*s/2);top=round(cy-7*s/2)
 # JavaScript Math.round uses floor(x+0.5), including the .5 used here.
 import math
 start=math.floor(cx-11*s/2+.5);top=math.floor(cy-7*s/2+.5)
 for k,ch in enumerate('30'):
  for y,row in enumerate(edit['glyphs'][ch]):
   for x,bit in enumerate(row):
    expected=(249,226,188,255) if bit=='1' else (57,79,89,255)
    for yy in range(top+y*s,top+(y+1)*s):
     for xx in range(start+(k*6+x)*s,start+(k*6+x+1)*s):check(im.getpixel((xx,yy))==expected,c['id']+f': native glyph {ch} cell {x},{y} pixel {xx},{yy}')
 outside=all(im.getpixel((x,y))==guide.getpixel((x,y)) for y in range(im.height) for x in range(im.width) if (x-cx)**2+(y-cy)**2>=rad**2)
 check(outside,c['id']+': stage unchanged outside local native countdown correction relative to edit source')

protected=['story','assets/selected','tools/storyboard']
subprocess.run(['git','diff','--exit-code',PIN,'--',*protected],cwd=ROOT,check=True,stdout=subprocess.PIPE)
checks.append('Narrative, canonical catalog, prior approved artwork and storyboard source unchanged')
manifest={'version':'v02','sourcePin':PIN,'branch':'art/ch3-pavilion-batch01-20261118','status':'generated','selected':False,'nativeAuthorship':'NOT DEMONSTRATED — disclosed source transfer plus local native painting/manual silhouette reconstruction. Not a complete original pixel-by-pixel redraw.','candidates':rows,'composites':comps}
save('manifest.json',manifest)
save('qa.json',{'reviewIntegrity':'PASS','binaryAlpha':'PASS for both foregrounds; no source alpha thresholding','portraitClearance':'PASS','countdown':'PASS — identical native bitmap family spells 30 in both stage views','v01Preservation':f'PASS — all {len(pins["files"])} pinned v01 files unchanged','originalNativeAuthorship':'NOT DEMONSTRATED / requirement remains unmet','remainingPixelStyleLimit':'Larger tool renders remain the basis of transferred RGB. Fine tonal variation and source antialiasing are not proven to be deliberately authored native clusters. No global palette filtering was used to conceal this.','checksPassed':len(checks),'checks':checks})
save('palette-qa.json',{c['id']:{'visibleRgbColors':c['visibleColors'],'globalQuantization':False,'alphaValues':c['alphaValues']} for c in rows})
(R/'CANDIDATE_HASHES.md').write_text('# v02 — generated / unselected\n\n'+'\n'.join(f'- `{c["id"]}-v02`: `{c["sha256"]}`' for c in rows)+'\n')
(R/'gallery.css').write_bytes((V1/'gallery.css').read_bytes())
parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 3 Batch A v02 corrections — The Acceptable Error</title><link rel="stylesheet" href="gallery.css"><body><header><div class="eyebrow">THE ACCEPTABLE ERROR · CHAPTER 3 · BATCH A · V02</div><h1>The Pavilion, corrected</h1><p class="status">SIX V02 CANDIDATES · GENERATED / UNSELECTED</p><p>Targeted corrections preserve the existing visual designs. Every pinned v01 file and hash is unchanged. Compare v01 on the left with v02 on the right.</p><p class="note"><strong>Technical status:</strong> Native dimensions, bitmap countdowns, headroom and strict binary alpha pass. Full-image original native-grid authorship remains <strong>unproven</strong>: these are honestly documented derived realizations with disclosed transfer, local native painting and hand-traced silhouettes. Fine source tonal variation remains.</p><nav><a href="#restroom">Restroom + attendant</a><a href="#stage">Stage + presenter</a><a href="#composites">Composite comparisons</a><a href="#evidence">Validation and sources</a><a href="../">Unchanged v01 gallery</a></nav></header><div class="toolbar"><span>Inspect:</span><button data-scale="1" aria-pressed="true">Native 1×</button><button data-scale="4" aria-pressed="false">Nearest 4×</button><span class="muted">No fractional fit-to-width scaling.</span></div><main>']
changes=json.loads((R/'sources/change-notes.json').read_text())
for anchor,title,group in [('restroom','Restroom and attendant',rows[:3]),('stage','Verification stage and presenter',rows[3:])]:
 parts.append(f'<section id="{anchor}"><h2>{title}</h2>')
 for c in group:
  w,h=c['dimensions'];parts.append(f'<article class="card candidate" id="{c["id"]}"><h3>{c["id"]} · v02</h3><p>{escape(changes[c["id"]])}</p>'+picture(c['candidate'],w,h,c['id']+' v02')+f'<p><code class="hash">SHA-256 {c["sha256"]}</code></p><div class="links">'+link(c['candidate'],'Native PNG')+link(c['preview4x'],'Exact 4× PNG')+link('generation-source/'+c['filename'],'Untouched edit source')+link(c['prompt'],'Exact edit prompt')+'</div><details open><summary>v01 left / v02 right · same canvas size</summary>'+picture(c['comparison'],2*w+16,h,c['id']+' v01 left and v02 right')+'</details><p class="muted">'+(f'Headroom {c["headroom"]} px · bottom clearance {c["bottomClearance"]} px · binary 0/255 alpha.' if c['character'] else 'Opaque background; original composition and scene function retained.')+'</p></article>')
 parts.append('</section>')
parts.append('<section id="composites"><h2>Layer and framing comparisons</h2>')
for c in comps:
 char=c['character'];parts.append(f'<article class="card"><h3>{char.title()} · v02 native composite</h3>'+picture(c['file'],564,278,char+' v02 composite')+'<details open><summary>Composite v01 left / v02 right</summary>'+picture(c['comparison'],1144,278,char+' v01 and v02 composites')+'</details><details><summary>Hand-traced silhouette on white and dark backings</summary>'+picture(f'composites/{char}-on-white.png',564,278,char+' white alpha proof')+picture(f'composites/{char}-on-dark.png',564,278,char+' dark alpha proof')+'</details></article>')
parts.append('</section><section id="evidence"><h2>Validation and complete provenance</h2><p>Six tool edit sources are immutable. The presenter source contains a large halo; final alpha was rebuilt from the supplied hand-authored contour, with no crude source-alpha threshold. Source-to-native transfer remains explicitly disclosed, and is not original native authorship. No candidates have been selected or approved.</p><div class="links">')
for p,title in [('CHANGELOG.md','Every visual change'),('VISUAL_QA.md','Inspection and remaining failures'),('manifest.json','Candidate identities and hashes'),('qa.json','Explicit technical validation'),('browser-qa.json','Browser validation'),('palette-qa.json','Measured palette and alpha'),('CANDIDATE_HASHES.md','Copyable SHA-256 hashes'),('PNG_SHA256SUMS.txt','All v02 PNG hashes'),('SOURCE_SHA256SUMS.txt','Source/code/prompt hashes'),('sources/edits.json','Edit sources and exact reference order'),('sources/silhouettes.json','Hand-traced contours and future pose anchors'),('sources/v01-pins.json','All 72 preserved v01 file hashes'),('realization-report.json','Transfer and native edit ledger'),('realize.mjs','Reproducible native realization code'),('README.md','Package instructions')]:parts.append(link(p,title))
parts.append('</div><p class="note"><strong>Stop for Nate’s visual selection.</strong> No narrative, approved prior artwork, items, gameplay or public-main changes. No approval, integration, new poses or Batch B generation.</p></section></main><footer>Source pin '+PIN+' · built-in image_gen edits + documented native finishing · generated/unselected</footer><script>for(const b of document.querySelectorAll("[data-scale]"))b.addEventListener("click",()=>{const s=Number(b.dataset.scale);for(const i of document.querySelectorAll("img.art")){i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;}for(const a of document.querySelectorAll("[data-scale]"))a.setAttribute("aria-pressed",String(a===b));});</script></body></html>')
(R/'index.html').write_text('\n'.join(parts))
(R/'PNG_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(R)}\n' for p in sorted(R.rglob('*.png'))))
sources=[p for p in R.rglob('*') if p.is_file() and (p.is_relative_to(R/'sources') or p.is_relative_to(R/'prompts') or p.name in ['realize.mjs','build_review.py','CHANGELOG.md','VISUAL_QA.md','README.md','qa-browser.cjs','package.json'])]
(R/'SOURCE_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(R)}\n' for p in sorted(sources)))
print(json.dumps({'reviewIntegrity':'PASS','checks':len(checks),'preservedV01Files':len(pins['files']),'nativeAuthorship':'UNPROVEN','hashes':{c['id']:c['sha256'] for c in rows}},indent=2))
