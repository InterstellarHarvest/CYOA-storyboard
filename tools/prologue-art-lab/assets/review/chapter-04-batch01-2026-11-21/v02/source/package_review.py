"""Package v02 lobby and portrait revisions, preserving all v01 candidates."""
from pathlib import Path
import hashlib,html,json
from PIL import Image

ROOT=Path(__file__).resolve().parent.parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
def info(p):
 im=Image.open(p)
 return {'file':str(p.relative_to(ROOT)),'dimensions':list(im.size),'mode':im.mode,'sha256':digest(p)}

def main():
 assets=[]
 requirements=json.loads((ROOT/'evidence/canonical-requirements.json').read_text())
 specs=[
  ('CH4-01','Grand Bellevue Lobby','CH4-01-lobby','CH4-01-reference-v01.png','lobby.py',
   'Closer room proportions; taller facilities doors; shaped metal shading and collars; lit panel bevels; deeper room connections; patterned worn carpet; richer wood, porcelain lamps and flower clusters. Tiny characters remain simple.',
   'Still more stylized and planar than Chapter 2. Perspective and foliage/flower rendering do not yet match its richness. Door-intact establishing state; later incidents are not literally shown.'),
  ('CH4-02','Auctioneer close background','CH4-02-auctioneer-background','CH4-02-reference-v02-empty.png','backdrop.py',
   'More fabric folds and fringe, modeled silver duct bands, panel bevels, chipped plaster ledges, faceted lamp glass, worn wood and door hardware. Separate native close camera retained.',
   'Large wall planes remain simple; not yet equal to approved receptionist material modeling. Provisional until lobby accepted.'),
  ('CH4-03','Auctioneer — Showman','CH4-03-auctioneer-showman','CH4-03-reference-v01.png','auctioneer.py',
   'Smaller facial color planes, eye and eyebrow acting, crow\u2019s feet and smile folds, layered silver locks, neck tendons, knuckles/nails and gavel bevels. More shirt, satin and jacket tailoring detail.',
   'Angular face and cloth remain stylized. Head/hand anatomy and likeness to the detailed reference still need Nate\u2019s review. Additional line detail does not by itself establish improved acting.')]
 for id,title,stem,ref,source,change,limitations in specs:
  r={'id':id,'title':title,'version':'v02','status':'generated / unselected','native':info(ROOT/'native'/f'{stem}-v02.png'),
   'previous':'../v01/native/'+stem+'-v01.png','detailedReference':info(ROOT/'detailed'/ref),
   'authoredSource':'source/'+source,'assetPath':None,'changes':change,'knownLimitations':limitations,
   'sourceNodeIds':requirements[id]['sourceNodeIds'],'canonicalRequirements':'evidence/canonical-requirements.json'}
  if id=='CH4-03':r['sourceNodeIds']=[k for k,v in requirements[id]['verbatimNodes'].items() if v.get('pose')=='showman']
  if id=='CH4-01':
   p=ROOT/'previews/CH4-01-lobby-v02-4x.png';Image.open(ROOT/r['native']['file']).resize((1256,824),Image.Resampling.NEAREST).save(p);r['preview4x']=info(p)
  assets.append(r)
 bg=Image.open(ROOT/'native/CH4-02-auctioneer-background-v02.png').convert('RGBA')
 fg=Image.open(ROOT/'native/CH4-03-auctioneer-showman-v02.png')
 Image.alpha_composite(bg,fg).convert('RGB').save(ROOT/'previews/auctioneer-composite-v02.png')
 manifest={'schema':'out-of-order-ch4-review-v2','version':'v02','dateEastern':'2026-11-21','baseCommit':json.loads((ROOT/'evidence/source-pin.json').read_text())['baseCommit'],
  'reviewBranch':'art/ch4-batch01-review-20261121','status':'generated / unselected; no approval implied',
  'workflow':'Unchanged detailed AI references -> independently coordinate-authored native pixel reconstruction -> exact 4x scene presentation.',
  'scope':'Revised lobby and portrait pair establish the detail standard first. Restroom and hall remain in preserved v01 and have not been revised or selected.',
  'feedback':['too simple and not detailed enough compared to ch2 stuff imo.','which is to saythe portrait can be more detailed and the main scene less simpllistic'],
  'assets':assets,'composite':info(ROOT/'previews/auctioneer-composite-v02.png')}
 dump(ROOT/'manifest.json',manifest)
 comparison={'status':'Requires creative selection; technical checks do not assert Chapter 2 quality.',
  'benchmarks':['conveniences_bureau','control_tower','spore_garden','tour_tram'],
  'axes':[
   ['Logical pixel size','314x206 main; 564x278 separate portrait layers. Matches approved contracts.'],
   ['Detail density','Increased door/furniture size, molding layers, light planes, flower clusters and material-specific detail. Chapter 2 remains richer and more natural.'],
   ['Silhouette clarity','Restroom pair, podium, ballroom/piano and service connection remain legible. Crowded small guests and arrangements need review.'],
   ['Color clusters','New clustered light and shadow follow material planes. Portrait uses smaller facial planes and cloth highlights; no palette-count target, filtering or posterization.'],
   ['Architectural edges','New bevel light/shadow and cylinder shading. Still a strongly planar rendering with perspective limitations.'],
   ['Object readability','Larger doors, podium paneling, corridor lights/cart, lamps and urns. Their route roles take priority over texture.'],
   ['NPC scale and simplicity','Small scene figures have no facial features. Separate transparent portrait adds facial/hair/hand detail at 564x278.'],
   ['Native and 4x appearance','Both supplied at exact sizes; v01 side-by-side and four actual Chapter 2 benchmarks included. Scaling is NEAREST only.']],
  'portraitBenchmark':'Approved receptionist is more naturally rendered. v02 adds anatomy and costume detail but does not yet demonstrate equivalent facial realism.'}
 dump(ROOT/'comparison.json',comparison)
 write_gallery(manifest,comparison)
 for r in assets:
  text='Stage B v02. Continue independent coordinate-authored reconstruction at '+str(r['native']['dimensions'])+' from blank canvas; do not open/sample/resize/crop/quantize/filter source rasters. Use preserved detailed reference and approved Chapter 2 comparison.\nOwner feedback verbatim: '+repr(manifest['feedback'])+'\nChanges: '+r['changes']+'\nEditable source: '+r['authoredSource']+' and source/pixel_primitives.py.\nKnown limitations: '+r['knownLimitations']+'\nNot image_gen Stage B; source is native pixel drawing code. Stage A uses built-in image_gen. No CLI/API fallback.\n'
  (ROOT/'prompts'/f'{r["id"]}-stage-B-v02.txt').write_text(text)

def write_gallery(m,comparison):
 e=html.escape
 css='''*{box-sizing:border-box}html{color-scheme:dark}body{margin:0;background:#172023;color:#eee7d5;font:16px/1.55 system-ui}main{max-width:1420px;margin:auto;padding:28px}h1{font-size:32px}h2{font-size:24px}h3{font-size:18px}a{color:#b4d9ca}article,section{margin:24px 0;padding:24px;background:#242f32;border:1px solid #566659;border-radius:8px}.strip{max-width:100%;overflow:auto;padding:12px;background:#172024;margin:12px 0}.pixel{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}.detailed{max-width:100%;height:auto}.row{display:flex;gap:24px;flex-wrap:wrap}.checker{width:max-content;background:repeating-conic-gradient(#46564e 0% 25%,#303e38 0% 50%) 0 0/16px 16px}button,select{font:inherit;color:#fff;background:#40594c;border:1px solid #839583;border-radius:4px;padding:9px;cursor:pointer}.status{color:#e5ba99}nav{display:flex;gap:16px;flex-wrap:wrap}summary{cursor:pointer;padding:10px 0}code{font-size:12px;overflow-wrap:anywhere}table{border-collapse:collapse;min-width:560px}td,th{border:1px solid #6a7668;padding:12px;text-align:left;vertical-align:top}@media(max-width:640px){main{padding:12px}article,section{padding:14px}h1{font-size:26px}}'''
 body=f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 4 v02 — detail revision</title><style>{css}</style><main><h1>Chapter 4 · Detail revision v02</h1><p class="status">Generated / unselected · November 21, 2026</p><p>Lobby and portrait pair revised following Nate\u2019s request for more detail. Small scene characters stay simple; the separate close portrait carries facial and costume detail. <strong>Chapter 2 still exceeds these candidates in natural material rendering.</strong></p><p>{e(m["scope"])}</p><nav><a href="#CH4-01">Lobby</a><a href="#CH4-02">Close background</a><a href="#CH4-03">Showman</a><a href="#benchmarks">Approved references</a><a href="../v01/index.html">Preserved full v01 batch</a></nav><p><a href="manifest.json">Manifest / hashes</a> · <a href="comparison.json">Comparison</a> · <a href="evidence/validation.json">Native authoring QA</a> · <a href="evidence/browser-qa.json">Browser QA</a> · <a href="evidence/canonical-requirements.json">Verbatim canonical requirements</a></p>'
 refs=['conveniences_bureau','control_tower','spore_garden','tour_tram']
 for r in m['assets']:
  id=r['id'];n=r['native'];w,h=n['dimensions']
  body+=f'<article id="{id}"><h2>{id} · {e(r["title"])} · v02</h2><p>{e(r["changes"])}</p><p class="status">Review gap: {e(r["knownLimitations"])}</p>'
  if id=='CH4-01':
   opts=''.join(f'<option value="references/scenes__biology_park__{name}.png" data-large="references/scenes__biology_park__{name}-4x.png">{name.replace("_"," ")}</option>' for name in refs)
   body+=f'<p><button class="scale" data-target="CH4-01" data-scale="1">Native 1×</button> <button class="scale" data-target="CH4-01" data-scale="4">Exact 4×</button> <select class="benchmark" data-target="CH4-01" aria-label="Chapter 2 benchmark">{opts}</select></p><h3>v02 candidate</h3><div class="strip"><img class="pixel candidate" data-id="CH4-01" data-scale="1" data-native="{n["file"]}" data-large="{r["preview4x"]["file"]}" src="{n["file"]}" width="314" height="206" alt="Revised lobby"></div><h3>Approved Chapter 2</h3><div class="strip"><img class="pixel comparison" data-id="CH4-01" src="references/scenes__biology_park__conveniences_bureau.png" width="314" height="206" alt="Approved Chapter 2 reference"></div>'
  else:body+=f'<h3>v02 native layer · {w}×{h}</h3><div class="strip"><div class="checker"><img class="pixel" src="{n["file"]}" width="{w}" height="{h}" alt="Revised {e(r["title"])}"></div></div>'
  body+=f'<details><summary>v01 comparison · unchanged prior candidate</summary><div class="strip"><div class="checker"><img class="pixel" src="{r["previous"]}" width="{w}" height="{h}" alt="Unchanged previous candidate"></div></div></details><details><summary>Detailed reference · unchanged</summary><img class="detailed" loading="lazy" src="{r["detailedReference"]["file"]}" alt="Detailed reference"></details><p><a href="{n["file"]}">Native PNG</a> · <a href="{r["authoredSource"]}">Editable pixel source</a> · <a href="prompts/{id}-stage-B-v02.txt">Reconstruction brief</a></p><p><code>SHA-256 {n["sha256"]}</code></p></article>'
 body+='<section id="portrait"><h2>Portrait composition · native 564×278</h2><div class="strip"><img class="pixel" src="previews/auctioneer-composite-v02.png" width="564" height="278" alt="Revised composite portrait"></div><h3>Approved receptionist · facial and material benchmark</h3><div class="strip"><img class="pixel" src="../v01/previews/approved-receptionist-composite.png" width="564" height="278" alt="Approved receptionist portrait"></div></section>'
 body+='<section id="benchmarks"><h2>Approved benchmarks · unchanged</h2>'
 for name in refs:
  body+=f'<h3>{name.replace("_"," ")}</h3><div class="strip"><img class="pixel" src="references/scenes__biology_park__{name}.png" width="314" height="206" alt="Approved {name}"></div>'
 body+='<h3>Reception scene character scale</h3><div class="strip"><img class="pixel" src="references/scenes__conference_hall__reception__reception_scene.png" width="314" height="206" alt="Approved small receptionist"></div><div class="strip"><table><thead><tr><th>Comparison axis</th><th>Assessment</th></tr></thead><tbody>'
 for k,v in comparison['axes']:body+=f'<tr><td>{e(k)}</td><td>{e(v)}</td></tr>'
 body+='</tbody></table></div><p>'+e(comparison['portraitBenchmark'])+'</p></section>'
 body+='''<script>document.querySelectorAll('.scale').forEach(b=>b.onclick=()=>{let s=Number(b.dataset.scale),a=document.querySelector('.candidate'),v=document.querySelector('.benchmark'),r=document.querySelector('.comparison');a.dataset.scale=s;a.src=s===1?a.dataset.native:a.dataset.large;a.width=r.width=314*s;a.height=r.height=206*s;r.src=s===1?v.value:v.selectedOptions[0].dataset.large;});document.querySelector('.benchmark').onchange=()=>{let v=document.querySelector('.benchmark'),a=document.querySelector('.candidate'),r=document.querySelector('.comparison');r.src=Number(a.dataset.scale)===1?v.value:v.selectedOptions[0].dataset.large;};</script></main></html>'''
 (ROOT/'index.html').write_text(body)

if __name__=='__main__':main()
