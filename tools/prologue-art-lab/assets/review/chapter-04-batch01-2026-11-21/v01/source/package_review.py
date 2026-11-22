"""Presentation/metadata only. Native authoring is in reconstruct.py/auctioneer.py.

This is the ONLY production step that reads raster files and scales them:
exact 4x NEAREST exports, comparison contact sheets, and portrait compositing.
"""
from pathlib import Path
import hashlib, html, json, sys
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parent.parent
def dump(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def info(p):
 im=Image.open(p);a=im.convert('RGBA').getchannel('A');values=sorted(set(a.getdata()))
 return {'file':str(p.relative_to(ROOT)),'sha256':digest(p),'dimensions':list(im.size),'mode':im.mode,'alphaValues':values,'opaque':values==[255]}

DATA=[
 ('CH4-01','Grand Bellevue Lobby','CH4-01-lobby-v01.png','CH4-01-reference-v01.png','grand_bellevue/lobby',[
  'Establishing entry state, before the restroom doors are removed. Later flooding, door removal and pod incidents require state-specific staging; this image is not asserted to depict every later node literally.',
  'Architecture and route silhouettes are clear. The tiled floor, panels and duct are much flatter and less detailed than Chapter 2. Not recommended as final-quality art yet.',
  'Small NPCs preserve crimson jacket/silver hair and formal guest silhouettes without facial detail. Tiny guests merge at native size and need a silhouette pass.',
  'Stage A side/back proportions and some flowers were recomposed to fit the native grid. The runner and clear routes remain.']),
 ('CH4-02','Auctioneer Lobby Portrait Background','CH4-02-auctioneer-background-v01.png','CH4-02-reference-v02-empty.png','grand_bellevue/lobby',[
  'Provisional tighter view at the lobby left podium. Spatial approval depends on selection of CH4-01.',
  'Empty opaque background, independently drawn at 564x278; no crop/enlargement of the main scene. Podium is confined to lower left so it does not occlude the separate foreground.',
  'Stage A v01 incorrectly contained a person; preserved unchanged. Corrected v02 removes him. Native reconstruction simplifies the curtain, changes its lower silhouette and shortens the podium.',
  'Material detail is visibly simpler than the approved receptionist background. Cream paneling needs more dimensional modeling.']),
 ('CH4-03','Auctioneer — Showman','CH4-03-auctioneer-showman-v01.png','CH4-03-reference-v01.png','grand_bellevue/lobby',[
  'Elderly silver-haired showman, crimson jacket, ivory shirt, black bow tie, thin silver moustache and raised wooden gavel. New proposed identity, not selected.',
  'Native transparent 564x278 foreground, independently authored from blank RGBA. The detailed reference has a gray backdrop; that backdrop was not extracted or keyed.',
  'Compared with the approved receptionist, the face, hands and cloth are more angular and less natural. The resting hand and smile need creative review.',
  'Head angle, hair mass and arm silhouette simplify the detailed identity reference. Future poses must use the selected identity; no additional poses are authorized here.']),
 ('CH4-04','Public Restroom','CH4-04-restroom-v01.png','CH4-04-reference-v01.png','grand_bellevue/restroom',[
  'Entry/pre-flood state: three modular stalls, nearest open, recognizable tank/seat/bowl, three sinks and fresh towels. No missing stalls or active crane.',
  'Service hatch is drawn broader than the nearest stall frontage, with a clear vertical route. This is a composition proposal, not a checked engineering model of crane geometry.',
  'The reference added a carpet and chandelier, excessive worn plaster and a clipboard woman instead of Eddie. Native reconstruction omits the carpet/chandelier and uses two small workmen.',
  'ISOLATE is the only readable native cabinet label. Full EMERGENCY WATER ISOLATION wording is preserved in canonical requirements/reference. No invented valve wheel is present.',
  'Compared with Chapter 2, fixtures are readable but the sink plumbing and kneeling plumber crowd together. Tile surfaces and metal shading are underdeveloped.']),
 ('CH4-05','Wedding Reception Hall','CH4-05-ballroom-v01.png','CH4-05-reference-v01.png','grand_bellevue/ballroom',[
  'Piano left, folding screen, organizer with clipboard, two workmen and chair by right service access, incidental tables/flowers/bunting and open walking route.',
  'The generated reference repeats the lobby architecture too closely; native reconstruction preserves that similarity. Nate should decide whether the hall needs a more distinct footprint.',
  'Main-scene figures are simple color/posture silhouettes; the musicians are deliberately small. The pictogram is a direction clue, not a view of a working bridal toilet.',
  'Native cloth folds and table silhouettes read, but flowers, stage and architectural surfaces are less rich than Chapter 2. Not recommended as final-quality art yet.'])
]

def main():
 requirements=json.loads((ROOT/'evidence/canonical-requirements.json').read_text())
 pin=json.loads((ROOT/'evidence/source-pin.json').read_text())
 records=[]
 for id,title,name,reference,scene,limitations in DATA:
  native=ROOT/'native'/name;im=Image.open(native)
  assert im.size==((564,278) if id in ['CH4-02','CH4-03'] else (314,206))
  transparent=id=='CH4-03'
  values=set(im.convert('RGBA').getchannel('A').getdata())
  assert values==({0,255} if transparent else {255})
  preview=None
  if im.size==(314,206):
   preview='previews/'+name.replace('.png','-4x.png')
   im.resize((1256,824),Image.Resampling.NEAREST).save(ROOT/preview)
  nodes=requirements[id]['sourceNodeIds']
  if id=='CH4-03':nodes=[k for k,v in requirements[id]['verbatimNodes'].items() if v.get('pose')=='showman']
  record={'id':id,'title':title,'version':'v01','status':'generated / unselected','scene':scene,
   'speakerPose':'hotel_auctioneer:showman' if id=='CH4-03' else None,
   'sourceNodeIds':nodes,'canonicalRegistryRecord':None,'assetPath':None,
   'canonicalRequirements':'evidence/canonical-requirements.json','ownerBrief':'evidence/owner-brief.txt',
   'detailedReference':info(ROOT/'detailed'/reference),'native':info(native),
   'preview4x':info(ROOT/preview) if preview else None,
   'authoredSource':['source/auctioneer.py','source/pixel_primitives.py'] if transparent else ['source/reconstruct.py','source/pixel_primitives.py'],
   'nativeGridAuthorship':'Coordinate-authored at the contracted dimensions from a blank canvas; no raster inputs or resampling. Reproducibility/forbidden-operation check is recorded in evidence/validation.json.',
   'comparison':'comparison.json','knownLimitationsAndDeviations':limitations}
  records.append(record)
 bg=Image.open(ROOT/'native/CH4-02-auctioneer-background-v01.png').convert('RGBA')
 fg=Image.open(ROOT/'native/CH4-03-auctioneer-showman-v01.png')
 Image.alpha_composite(bg,fg).convert('RGB').save(ROOT/'previews/auctioneer-composite-v01.png')
 refs=json.loads((ROOT/'evidence/approved-references.json').read_text())
 refbg=Image.open(ROOT/'references/portraits__receptionist__reception_background.png').convert('RGBA')
 reffg=Image.open(ROOT/'references/portraits__receptionist__receptionist_idle.png')
 Image.alpha_composite(refbg,reffg).convert('RGB').save(ROOT/'previews/approved-receptionist-composite.png')
 # A compact delivery sheet includes actual 1x candidates and actual 4x exports.
 for factor in [1,4]:
  sheet=Image.new('RGB',(314*factor+24,3*(206*factor+32)+16),'#20282b');d=ImageDraw.Draw(sheet)
  for row,id in enumerate(['CH4-01','CH4-04','CH4-05']):
   r=next(r for r in records if r['id']==id);y=16+row*(206*factor+32)
   d.text((12,y),id+' / '+r['title'],fill='#eee2c5')
   im=Image.open(ROOT/(r['native']['file'] if factor==1 else r['preview4x']['file']))
   sheet.paste(im,(12,y+18))
  sheet.save(ROOT/f'previews/main-scenes-{factor}x-contact.png')
 manifest={'schema':'out-of-order-ch4-review-v1','dateEastern':'2026-11-21','baseCommit':pin['baseCommit'],
  'reviewBranch':'art/ch4-batch01-review-20261121','approval':'None. Nate selects; do not register, integrate, publish or merge as approved.',
  'workflow':{'A':'Built-in image_gen detailed references, original bytes retained.','B':'Independent coordinate-authored native-grid reconstruction with Python/Pillow ImageDraw.','C':'Exact 4x nearest-neighbor scene presentation only.'},
  'canonicalRegistryGap':'Pinned main has no Chapter 4 artwork records. No registry was edited. Verbatim source nodes and owner brief are the requirements evidence.',
  'assets':records,'approvedReferences':refs,'composite':info(ROOT/'previews/auctioneer-composite-v01.png')}
 dump(ROOT/'manifest.json',manifest)
 comparison={
  'primaryBenchmarks':['biology_park/conveniences_bureau','biology_park/control_tower','biology_park/spore_garden','biology_park/tour_tram'],
  'secondaryBenchmarks':['conference_hall/reception','house_of_tomorrow/foyer','house_of_tomorrow/lounge'],
  'axes':[
   {'axis':'Logical pixel size','approved':'All selected main-scene benchmarks are 314x206; reception portrait pair 564x278.','candidates':'Exact same contracts, independently created blank canvases.'},
   {'axis':'Detail density','approved':'Chapter 2 resolves dense foliage, panels, fixtures and depth without losing paths.','candidates':'Less developed. Large flat surfaces dominate the lobby and hall; material modeling needs another art pass.'},
   {'axis':'Silhouette clarity','approved':'Clear doors, console masses, tram seating, paths and machinery.','candidates':'Primary doors/podium/piano/toilet are distinct. Lobby guests and restroom plumbing/plumber overlap too much.'},
   {'axis':'Color clusters','approved':'Rich controlled clusters describe plants, metal and stone; no color-count quota used.','candidates':'Deliberate solid clusters and discrete shade bands; no sampled palette or posterization. Color modeling is noticeably simpler.'},
   {'axis':'Architectural edges','approved':'Perspective-aware cornices, tiled planes, frames and cylindrical plumbing.','candidates':'Clean integer-coordinate edges, coherent broad planes, but ducts and moldings remain boxy.'},
   {'axis':'Object readability','approved':'Bureau barriers, control gauges, tram seats and garden paths read at native size.','candidates':'Paired facilities doors, three stalls, tank/seat/bowl, sinks, piano and broad service opening read. Small flowers and tools are simplified.'},
   {'axis':'NPC scale/simplicity','approved':'Receptionist is a small roughly 20px-tall scene cluster; the separate portrait carries face and acting. Chapter 2 room benchmarks have no prominent human portraits.','candidates':'Room people are roughly 27px tall and have no facial features. They were drawn separately from the 564x278 foreground; perspective/scale still needs selection.'},
   {'axis':'Native and 4x appearance','approved':'Both scales are supplied unchanged except exact NEAREST presentation.','candidates':'Exact native views and 1256x824 previews. No smoothing. 4x exposes the simpler surfaces; scaling does not fix artistic gaps.'}],
  'verdict':'Initial composition and native reconstruction candidates, not final-quality equivalence to Chapter 2. Native authorship is verifiable; artistic acceptance remains Nate\u2019s decision.',
  'perCandidate':{r['id']:r['knownLimitationsAndDeviations'] for r in records}}
 dump(ROOT/'comparison.json',comparison)
 write_gallery(manifest,comparison)

def write_gallery(m,comparison):
 e=html.escape
 css='''*{box-sizing:border-box}html{color-scheme:dark}body{margin:0;background:#171e22;color:#eee6d5;font:16px/1.55 system-ui,sans-serif}main{max-width:1420px;margin:auto;padding:28px}a{color:#b4d9cf}h1{font-size:32px;line-height:1.15}h2{font-size:24px}h3{font-size:18px}.muted{color:#b9c1bc}.badge{display:inline-block;padding:4px 10px;background:#603d46;border-radius:4px}.panel,article{padding:22px;margin:24px 0;background:#232d31;border:1px solid #43514f;border-radius:9px}nav{display:flex;gap:16px;flex-wrap:wrap}button,select{padding:9px 14px;border:1px solid #788d84;border-radius:5px;background:#354944;color:#fff;font:inherit;cursor:pointer}.strip{overflow:auto;max-width:100%;background:#151b1e;padding:12px;margin:12px 0}.pixel{image-rendering:pixelated;image-rendering:crisp-edges;max-width:none;display:block}.detailed{max-width:100%;height:auto}.twoup{display:flex;gap:28px;flex-wrap:wrap}.checker{background:repeating-conic-gradient(#465156 0% 25%,#303c41 0% 50%) 0 0/16px 16px;width:max-content}table{border-collapse:collapse;width:100%;font-size:14px}td,th{border:1px solid #59645e;padding:10px;text-align:left;vertical-align:top}code{overflow-wrap:anywhere;font-size:12px}summary{cursor:pointer;padding:10px 0}li{margin:7px 0}img{vertical-align:top}@media(max-width:640px){main{padding:12px}.panel,article{padding:14px}h1{font-size:26px}.twoup{gap:12px}table{font-size:12px}}'''
 body=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 4 Batch 1 — v01 creative review</title><style>{css}</style><main>
 <h1>Something Old, Something Sold</h1><p>Chapter 4 · Batch 1 · v01 · November 21, 2026</p><p class="badge">Generated / unselected — creative review</p>
 <p>Five initial candidates. Detailed AI references are preserved separately from independently drawn native-grid sources. The scenes currently fall below Chapter 2 in material detail. Technical validation is not creative approval.</p>
 <nav>{''.join(f'<a href="#{r["id"]}">{r["id"]}</a>' for r in m['assets'])}<a href="#benchmarks">Approved benchmarks</a><a href="#comparison">Quality comparison</a></nav>
 <div class="panel"><strong>Review the lobby first.</strong> The close background and auctioneer are provisional until its architecture is selected. Choose a candidate by ID/version or request specific changes. No artwork is registered or published as approved.
 <p><a href="manifest.json">Manifest and SHA-256</a> · <a href="comparison.json">Comparison record</a> · <a href="evidence/validation.json">Validation</a> · <a href="evidence/canonical-requirements.json">Verbatim canonical source nodes</a> · <a href="evidence/owner-brief.txt">Owner brief</a> · <a href="source/reconstruct.py">Editable reconstruction source</a> · <a href="source/auctioneer.py">Portrait source</a></p>
 <p class="muted">Pinned main: <code>{m['baseCommit']}</code><br>Branch: <code>{m['reviewBranch']}</code>. This local gallery is self-contained; it works from a file link and does not fetch data.</p></div>'''
 choices=[r for r in m['approvedReferences'] if 'biology_park' in r['canonicalPath']]
 for r in m['assets']:
  id=r['id'];n=r['native'];scene=bool(r['preview4x'])
  body+=f'<article id="{id}"><h2>{id} · {e(r["title"])}</h2><p>{n["dimensions"][0]}×{n["dimensions"][1]} · {n["mode"]} · v01 · generated / unselected</p>'
  if scene:
   opts=''.join(f'<option value="{e(x["reviewCopy"])}" data-large="{e(x["preview4x"])}">{e(Path(x["canonicalPath"]).stem.replace("_"," "))}</option>' for x in choices)
   body+=f'<p><button class="scale" data-target="{id}" data-scale="1" aria-pressed="true">Native 1×</button> <button class="scale" data-target="{id}" data-scale="4" aria-pressed="false">Exact 4×</button> <label>Compare: <select class="benchmark" data-target="{id}">{opts}</select></label></p>'
   body+=f'<h3>Candidate</h3><div class="strip"><img class="pixel candidate" data-id="{id}" data-native="{n["file"]}" data-large="{r["preview4x"]["file"]}" data-scale="1" src="{n["file"]}" width="314" height="206" alt="{e(r["title"])} native candidate"></div>'
   body+=f'<h3>Approved Chapter 2 reference</h3><div class="strip"><img class="pixel comparison" data-id="{id}" src="{choices[0]["reviewCopy"]}" width="314" height="206" alt="Approved Chapter 2 benchmark"></div>'
  else:
   body+=f'<div class="strip"><div class="checker"><img class="pixel" src="{n["file"]}" width="564" height="278" alt="{e(r["title"])} native layer"></div></div>'
   body+='<h3>Proposed layered portrait · native 564×278</h3><div class="strip"><img class="pixel" src="previews/auctioneer-composite-v01.png" width="564" height="278" alt="Provisional auctioneer over proposed background"></div>'
  body+='<h3>Known limitations and deviations</h3><ul>'+''.join(f'<li>{e(s)}</li>' for s in r['knownLimitationsAndDeviations'])+'</ul>'
  body+=f'<p><a href="{n["file"]}">Native PNG</a> · <a href="prompts/{id}-stage-A.txt">Expanded Stage A prompt</a> · <a href="prompts/{id}-stage-B.txt">Stage B reconstruction brief</a></p><p><code>SHA-256 {n["sha256"]}</code></p>'
  body+=f'<details><summary>Detailed reference — preserved unchanged, not the game asset</summary><img loading="lazy" class="detailed" src="{r["detailedReference"]["file"]}" alt="Detailed reference for {id}"><p><a href="{r["detailedReference"]["file"]}">Original reference PNG</a> · {r["detailedReference"]["dimensions"]}</p></details>'
  if id=='CH4-02':body+='<details><summary>Preserved first reference with unwanted person</summary><img loading="lazy" class="detailed" src="detailed/CH4-02-reference-v01-with-unrequested-person.png" alt="Superseded background reference with unrequested person"><p><a href="prompts/CH4-02-correction-stage-A.txt">Correction prompt</a></p></details>'
  body+='<details><summary>Canonical source node IDs</summary><p><code>'+e(', '.join(r['sourceNodeIds']))+'</code></p></details></article>'
 body+='<section id="benchmarks" class="panel"><h2>Approved benchmarks · unchanged</h2><p>The production reception files were found in the game checkout, dimension-checked and byte-matched to the canonical selected files. <a href="evidence/reception-production-verification.json">Verification</a> · <a href="evidence/reference-source-records.json">Approved source provenance</a></p>'
 body+='<p>Compare the tiny receptionist with her separate expressive portrait. Scene characters were not enlarged into portraits or detailed portraits shrunk into scenes.</p><div class="strip"><img class="pixel" src="references/scenes__conference_hall__reception__reception_scene.png" width="314" height="206" alt="Approved reception main scene"></div><div class="strip"><img class="pixel" src="previews/approved-receptionist-composite.png" width="564" height="278" alt="Approved receptionist layered portrait"></div>'
 for r in m['approvedReferences']:
  if r['dimensions']==[314,206]:
   body+=f'<details><summary>{e(r["canonicalPath"])}</summary><div class="strip"><img class="pixel" src="{r["reviewCopy"]}" width="314" height="206" alt="Approved native benchmark"></div><div class="strip"><img loading="lazy" class="pixel" src="{r["preview4x"]}" width="1256" height="824" alt="Approved benchmark exact four times"></div></details>'
 body+='</section><section id="comparison" class="panel"><h2>Quality comparison</h2><div class="strip"><table><thead><tr><th>Axis</th><th>Approved benchmark</th><th>Batch 1 v01</th></tr></thead><tbody>'
 for row in comparison['axes']:body+='<tr>'+''.join(f'<td>{e(row[k])}</td>' for k in ['axis','approved','candidates'])+'</tr>'
 body+='</tbody></table></div><p>'+e(comparison['verdict'])+'</p></section>'
 body+='''<script>
 document.querySelectorAll('.scale').forEach(b=>b.addEventListener('click',()=>{const id=b.dataset.target,s=Number(b.dataset.scale),a=document.querySelector('.candidate[data-id="'+id+'"]'),v=document.querySelector('.benchmark[data-target="'+id+'"]'),r=document.querySelector('.comparison[data-id="'+id+'"]');a.dataset.scale=s;a.src=s===1?a.dataset.native:a.dataset.large;a.width=r.width=314*s;a.height=r.height=206*s;r.src=s===1?v.value:v.selectedOptions[0].dataset.large;document.querySelectorAll('.scale[data-target="'+id+'"]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));}));
 document.querySelectorAll('.benchmark').forEach(v=>v.addEventListener('change',()=>{const id=v.dataset.target,s=Number(document.querySelector('.candidate[data-id="'+id+'"]').dataset.scale);document.querySelector('.comparison[data-id="'+id+'"]').src=s===1?v.value:v.selectedOptions[0].dataset.large;}));
 </script></main></html>'''
 (ROOT/'index.html').write_text(body)

if __name__=='__main__':main()
