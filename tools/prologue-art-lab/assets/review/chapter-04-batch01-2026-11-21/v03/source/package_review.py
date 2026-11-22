"""v03 delivery exports only: reads finished native art for comparison/presentation.

Native writers are lobby.py, backdrop.py, auctioneer.py and materials.py.
Those writers read no image files. This packaging step performs exact NEAREST
presentation exports and lossless layer compositing, never native reconstruction.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,html,json

ROOT=Path(__file__).resolve().parent.parent
BATCH=ROOT.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
def info(p):
 im=Image.open(p);alpha=set(im.convert('RGBA').getchannel('A').tobytes())
 return {'file':str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else '../'+p.relative_to(BATCH).as_posix(),'dimensions':list(im.size),'mode':im.mode,'sha256':sha(p),'alpha':'transparent binary' if alpha=={0,255} else 'opaque' if alpha=={255} else 'partial alpha'}

SPECS=[
 ('CH4-01','Grand Bellevue Lobby','CH4-01-lobby','lobby.py','CH4-01-reference-v01.png',
  'Composition retained: podium/ballroom left, paired facilities center, broad service access right; small NPCs remain simple. Lamps/chandelier supply local warm light, window fill stays cooler, and recesses/under-duct shadows deepen. Curved shaded duct, irregular heavy drapes, separate stone/carpet/wood and existing wear clusters are reconstructed at 314×206.',
  'Still a compact stylized reconstruction. Large stone/plaster surfaces and the existing flower silhouettes remain simpler than the detailed reference and strongest Chapter 2 work. Lower service recess is deliberately dark; Nate should judge object visibility.'),
 ('CH4-02','Auctioneer Lobby Portrait Background','CH4-02-auctioneer-background','backdrop.py','CH4-02-reference-v02-empty.png',
  'Same close camera, architecture and empty foreground. Warm lamp light, cooler ambient fill, curtain/contact shadows, rounded tarnished duct, modeled velvet folds and darker doorway/wood give the surfaces separate light responses.',
  'Material lighting is procedurally evaluated from authored native geometry. Some surfaces can look cleaner and more smoothly shaded than the approved receptionist background; the wear and velvet finish still need creative comparison.'),
 ('CH4-03','Auctioneer — Showman','CH4-03-auctioneer-showman','auctioneer.py','CH4-03-reference-v01.png',
  'Identity, silver hairstyle, age cues, burgundy formalwear, gavel, camera and pose retained. Forehead/cheek/nose/chin/neck use rounded volume fields, hair uses broad lit locks, hands use curved finger masses, and wool/velvet, satin and cotton have distinct responses.',
  'The rounded reconstruction remains stylized and can read more sculpted than hand-painted. Face likeness, apparent age, rounded hands and warm theatrical expression need owner review beside the approved receptionist. No claim of equivalent finish or approval is made.')]

def main():
 req=json.loads((BATCH/'v02/evidence/canonical-requirements.json').read_text())
 assets=[]
 for id,title,stem,src,ref,changes,limits in SPECS:
  native=ROOT/'native'/f'{stem}-v03.png';im=Image.open(native)
  p=ROOT/'previews'/f'{stem}-v03-4x.png';im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(p)
  old=BATCH/'v02/native'/f'{stem}-v02.png';oldim=Image.open(old)
  old4=ROOT/'previews'/f'{stem}-v02-4x.png';oldim.resize((oldim.width*4,oldim.height*4),Image.Resampling.NEAREST).save(old4)
  nodes=req[id]['sourceNodeIds']
  if id=='CH4-03':nodes=[k for k,v in req[id]['verbatimNodes'].items() if v.get('pose')=='showman']
  r={'id':id,'title':title,'version':'v03','status':'generated / unselected','assetPath':None,
   'native':info(native),'preview4x':info(p),'previousV02':info(old),'previousV02Preview4x':info(old4),
   'previousV01':info(BATCH/'v01/native'/f'{stem}-v01.png'),
   'detailedReference':info(BATCH/'v02/detailed'/ref),'authoredSource':['source/'+src,'source/materials.py'],
   'sourceNodeIds':nodes,'canonicalRequirements':'../v02/evidence/canonical-requirements.json',
   'changes':changes,'knownLimitations':limits}
  # Comparison sheet uses exact native pixels, no source resizing.
  sheet=Image.new('RGBA',(im.width*2+36,im.height+46),'#1c282b');d=ImageDraw.Draw(sheet)
  d.text((12,10),'v02 / '+id,fill='#e9dbc0');d.text((im.width+24,10),'v03 / '+id,fill='#e9dbc0')
  def checker(x,y,w,h):
   for yy in range(y,y+h,8):
    for xx in range(x,x+w,8):d.rectangle((xx,yy,min(xx+7,x+w-1),min(yy+7,y+h-1)),fill='#3e4e47' if ((xx-x)//8+(yy-y)//8)%2 else '#2c3a35')
  for x,obj in [(12,oldim),(im.width+24,im)]:
   checker(x,30,im.width,im.height);sheet.alpha_composite(obj.convert('RGBA'),(x,30))
  cp=ROOT/'previews'/f'{id}-v02-v03-native.png';sheet.convert('RGB').save(cp);r['comparisonSheet']=info(cp)
  assets.append(r)
 bg=Image.open(ROOT/'native/CH4-02-auctioneer-background-v03.png').convert('RGBA')
 fg=Image.open(ROOT/'native/CH4-03-auctioneer-showman-v03.png')
 composite=Image.alpha_composite(bg,fg).convert('RGB');composite.save(ROOT/'previews/auctioneer-composite-v03.png')
 composite.resize((2256,1112),Image.Resampling.NEAREST).save(ROOT/'previews/auctioneer-composite-v03-4x.png')
 canonical=[
  ('Bureau','../v02/references/scenes__biology_park__conveniences_bureau.png'),
  ('Control Tower','../v02/references/scenes__biology_park__control_tower.png'),
  ('Reception scene','../v02/references/scenes__conference_hall__reception__reception_scene.png'),
  ('Reception background','../v02/references/portraits__receptionist__reception_background.png'),
  ('Receptionist foreground','../v02/references/portraits__receptionist__receptionist_idle.png')]
 refs=[]
 for name,file in canonical:
  p=(ROOT/file).resolve();v=info(p);v['title']=name
  out=ROOT/'previews'/('approved-'+name.lower().replace(' ','-')+'-4x.png');im=Image.open(p);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(out);v['preview4x']=info(out);refs.append(v)
 manifest={'schema':'out-of-order-ch4-review-v03','dateEastern':'2026-11-21','version':'v03','reviewBranch':'art/ch4-batch01-review-20261121',
  'reviewedBaseCommit':'6444d2218fb5563640788be314b8aa47b69eb11b','approval':'UNSELECTED. Technical passing is not creative approval.',
  'scope':'CH4-01, CH4-02, CH4-03 only. Restroom and ballroom are not revised.',
  'method':{'A':'Original detailed references reused unchanged and visually studied; no new image_gen calls in v03. Original built-in imagegen prompts/receipts remain in v01/v02.',
   'B':'Blank native canvases. Integer-coordinate geometry and curves, native 1-bit geometric coverage masks and material/volume lighting fields evaluated directly on 314x206 or 564x278. No source raster inputs, supersampling, filtering, source downsampling or palette reduction. Not represented as image-model-generated native art.',
   'C':'Exact 4x NEAREST from completed native art. Portrait 4x exports are supplemental inspection views, not a change to the 564x278 portrait presentation contract.'},
  'assets':assets,'approvedReferences':refs,'composite':info(ROOT/'previews/auctioneer-composite-v03.png'),
  'preservationBaseline':'evidence/preservation-baseline.json','direction':'evidence/direction-v03.txt','validation':'evidence/validation.json'}
 dump(ROOT/'manifest.json',manifest)
 axes=[
  ('Logical dimensions','Same native grid as approved artwork: 314×206 scene, 564×278 portrait layers. No enlargement to make room faces detailed.'),
  ('Detail density','v03 spends the budget on surface light and form rather than additional decorative objects. Bureau and Control Tower remain the primary room references; approved receptionist supplies the close-up minimum target.'),
  ('Silhouette clarity','v02 layout, paired facilities and small NPC silhouettes remain. Foreground is independently rebuilt with curved contours and the established silver hair, burgundy costume and gavel.'),
  ('Color clusters','Native material/volume fields replace large flat fills; light is grouped locally. There is no whole-image palette-count quota, quantization or source pixel sampling. Some transitions remain visibly procedural.'),
  ('Architectural edges','Cast/contact shadows and recess values add depth to the same doors, duct, panels, windows and podium; moldings do not substitute for surface modeling.'),
  ('Object readability','Restroom sightline, podium, door hardware, piano connection and service corridor remain. Owner should judge the darker service recess and small flower clusters at 1×.'),
  ('NPC scale/simplicity','Main-scene people retain single face clusters and small bodies. Portrait adds rounded face/hair/hands at a separately authored native scale; no character raster is reused between grids.'),
  ('Native/4× craft','All three candidates, matching v02 images and approved references are provided at native and exact 4×. v01 and original detailed references remain available unchanged; 4× does not confer visual approval.')]
 comparison={'assets':{r['id']:{'changes':r['changes'],'knownLimitations':r['knownLimitations'],'references':['Bureau','Control Tower','approved receptionist background','approved receptionist foreground','v01','v02','original detailed concept'],'axes':dict(axes)} for r in assets},
  'assessment':'v03 changes broad material/light/volume rendering. It remains a stylized coordinate-authored reconstruction, with a possible overly clean/sculpted finish relative to approved art. No declaration that the approved receptionist minimum has been met; Nate makes that decision.'}
 dump(ROOT/'comparison.json',comparison)
 for r in assets:
  (ROOT/'prompts'/f'{r["id"]}-reconstruction-v03.txt').write_text('Independent native-grid reconstruction brief — v03\n'+r['changes']+'\n\nUse original detailed reference: '+r['detailedReference']['file']+'\nCompare directly with actual approved Bureau/Control Tower/reception art and unchanged v01/v02.\n\nNative method: '+manifest['method']['B']+'\nPresentation: '+manifest['method']['C']+'\nKnown limitations for review: '+r['knownLimitations']+'\nRemain UNSELECTED.\n')
 write_gallery(manifest,axes)

def write_gallery(m,axes):
 e=html.escape
 css='''*{box-sizing:border-box}html{color-scheme:dark}body{background:#172024;color:#eee3cd;font:16px/1.55 system-ui;margin:0}main{max-width:1440px;margin:auto;padding:30px}h1{font-size:32px}h2{font-size:24px}h3{font-size:17px}a{color:#b6dbc9}.status{color:#e6be95}article,section{background:#242f32;border:1px solid #58685a;border-radius:8px;margin:24px 0;padding:22px}.strip{overflow:auto;max-width:100%;padding:12px;background:#172024;margin:14px 0}.row{display:flex;gap:18px;width:max-content}.pixel{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}figure{margin:0}figcaption{padding:5px 0 10px}.checker{width:max-content;background:repeating-conic-gradient(#3e4e47 0% 25%,#2c3a35 0% 50%) 0 0/16px 16px}.concept{max-width:100%;height:auto}button,select{background:#405849;color:#fff;border:1px solid #84947f;border-radius:4px;padding:9px;font:inherit;cursor:pointer}nav{display:flex;flex-wrap:wrap;gap:18px}summary{cursor:pointer;padding:10px 0}table{border-collapse:collapse;min-width:580px}th,td{border:1px solid #6a7766;padding:10px;text-align:left;vertical-align:top}code{font-size:12px;overflow-wrap:anywhere}@media(max-width:640px){main{padding:12px}article,section{padding:14px}h1{font-size:25px}}'''
 body=f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 4 Batch 1 · v03 material and light review</title><style>{css}</style><main><h1>Chapter 4 · v03 rendering review</h1><p class="status">CH4-01 / CH4-02 / CH4-03 · UNSELECTED · November 21, 2026</p><p>Composition retained. This pass rebuilds broad light, surface and rounded-form rendering on the actual native grids. Review at 1× first. The approved artwork is a comparison target; passing file checks does not establish equivalent craft.</p><nav><a href="#CH4-01">Lobby</a><a href="#CH4-02">Background</a><a href="#CH4-03">Showman</a><a href="#approved">Approved references</a><a href="../v02/index.html">v02 gallery</a><a href="../v01/index.html">v01 gallery</a></nav><p><a href="manifest.json">Manifest / hashes</a> · <a href="comparison.json">Per-asset assessment</a> · <a href="evidence/direction-v03.txt">Owner direction</a> · <a href="../v02/evidence/canonical-requirements.json">Verbatim storyboard requirements</a> · <a href="evidence/validation.json">Native authorship / image QA</a> · <a href="evidence/browser-qa.json">Browser QA</a></p>'
 for i,r in enumerate(m['assets']):
  id=r['id'];w,h=r['native']['dimensions'];ref=m['approvedReferences'][0 if i==0 else 3 if i==1 else 4]
  body+=f'<article id="{id}"><h2>{id} · {e(r["title"])}</h2><p>{e(r["changes"])}</p><p class="status">Review limitation: {e(r["knownLimitations"])}</p><p><button class="scale" data-target="{id}" data-scale="1" aria-pressed="true">Native 1×</button> <button class="scale" data-target="{id}" data-scale="4" aria-pressed="false">Exact 4×</button></p><div class="strip"><div class="row">'
  for label,key,preview,role in [('v02 — preserved','previousV02','previousV02Preview4x','previous'),('v03 — unselected','native','preview4x','candidate')]:
   n=r[key];large=r[preview]['file']
   body+=f'<figure><figcaption>{label} · {w}×{h}</figcaption><div class="checker"><img class="pixel scaled {role}" data-target="{id}" data-native="{n["file"]}" data-large="{large}" data-w="{w}" data-h="{h}" src="{n["file"]}" width="{w}" height="{h}" alt="{id} {label}"></div></figure>'
  body+='</div></div>'
  if i==0:
   body+='<label>Approved room benchmark: <select id="benchmark">'+''.join(f'<option value="{x["file"]}" data-large="{x["preview4x"]["file"]}">{x["title"]}</option>' for x in m['approvedReferences'][:3])+'</select></label>'
  body+=f'<h3>Approved {e(ref["title"])} · native comparison</h3><div class="strip"><div class="checker"><img class="pixel scaled benchmark" data-target="{id}" data-native="{ref["file"]}" data-large="{ref["preview4x"]["file"]}" data-w="{ref["dimensions"][0]}" data-h="{ref["dimensions"][1]}" src="{ref["file"]}" width="{ref["dimensions"][0]}" height="{ref["dimensions"][1]}" alt="Approved {e(ref["title"])}"></div></div>'
  body+=f'<p><a href="{r["comparisonSheet"]["file"]}">Direct v02/v03 comparison PNG</a> · <a href="{r["native"]["file"]}">Native PNG</a> · <a href="{r["preview4x"]["file"]}">4× PNG</a> · <a href="{r["authoredSource"][0]}">Editable native source</a> · <a href="prompts/{id}-reconstruction-v03.txt">Reconstruction brief</a></p><p><code>SHA-256 {r["native"]["sha256"]}</code></p>'
  body+=f'<details><summary>Preserved v01 candidate</summary><div class="strip"><img class="pixel" src="{r["previousV01"]["file"]}" width="{w}" height="{h}" alt="{id} preserved v01"></div></details><details><summary>Original detailed concept reference — unchanged</summary><img class="concept" loading="lazy" src="{r["detailedReference"]["file"]}" alt="{id} original detailed reference"><p>Study reference; not the authored native source.</p></details></article>'
 body+='<section id="composite"><h2>Layered portrait comparison · native 564×278</h2><div class="strip"><div class="row">'
 for title,p in [('v02','../v02/previews/auctioneer-composite-v02.png'),('v03','previews/auctioneer-composite-v03.png'),('Approved receptionist','../v01/previews/approved-receptionist-composite.png')]:body+=f'<figure><figcaption>{title}</figcaption><img class="pixel" src="{p}" width="564" height="278" alt="{title} composite portrait"></figure>'
 body+='</div></div><p><a href="previews/auctioneer-composite-v03-4x.png">Exact 4× v03 portrait inspection</a></p></section><section id="approved"><h2>Canonical approved-art comparisons</h2><p>Bureau and Control Tower set the scene benchmark. Receptionist background and foreground set the close-up finish target. All benchmark PNGs are byte-unchanged; none was regenerated.</p>'
 for r in m['approvedReferences']:
  w,h=r['dimensions'];body+=f'<details><summary>{r["title"]} · native and exact 4×</summary><div class="strip"><div class="checker"><img class="pixel" src="{r["file"]}" width="{w}" height="{h}" alt="Approved {r["title"]}"></div></div><div class="strip"><img class="pixel" loading="lazy" src="{r["preview4x"]["file"]}" width="{w*4}" height="{h*4}" alt="Approved {r["title"]} exact 4x"></div></details>'
 body+='<div class="strip"><table><thead><tr><th>Axis</th><th>v03 assessment</th></tr></thead><tbody>'+''.join(f'<tr><td>{e(k)}</td><td>{e(v)}</td></tr>' for k,v in axes)+'</tbody></table></div><p>No declaration of artistic acceptance is made. Some material transitions and anatomy remain visibly procedural or sculpted. Nate selects the standard before any restroom/ballroom revision.</p></section>'
 body+='''<script>const scales={};document.querySelectorAll('.scale').forEach(b=>b.addEventListener('click',()=>{const id=b.dataset.target,s=Number(b.dataset.scale);scales[id]=s;document.querySelectorAll('.scaled[data-target="'+id+'"]').forEach(i=>{i.src=s===1?i.dataset.native:i.dataset.large;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;});document.querySelectorAll('.scale[data-target="'+id+'"]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));}));document.querySelector('#benchmark').addEventListener('change',e=>{const o=e.target.selectedOptions[0],i=document.querySelector('.benchmark[data-target="CH4-01"]'),s=scales['CH4-01']||1;i.dataset.native=o.value;i.dataset.large=o.dataset.large;i.src=s===1?o.value:o.dataset.large;});</script></main></html>'''
 (ROOT/'index.html').write_text(body)

if __name__=='__main__':main()
