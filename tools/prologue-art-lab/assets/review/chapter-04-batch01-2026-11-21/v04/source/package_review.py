"""v04 delivery exports only: reads finished native art for comparison/presentation.

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

SPECS=[('CH4-01', 'Grand Bellevue Lobby', 'CH4-01-lobby', 'lobby.py', 'CH4-01-reference-v01.png', 'v03 lighting/composition retained, with chipped/stained plaster, localized slab cracks and worn tile corners, interrupted carpet nap, directional podium grain/dents, folded velvet seams, petal/urn clusters and fastened duct joints. Floor/window/ceiling long edges now share VP (182,112); podium long edges are corrected. Tiny NPCs remain simple.', 'The native room is still an economical stylized reconstruction. Aging and flower clusters are visible but less natural than the strongest approved Chapter 2 art. Perspective corrections are an illustration audit, not a full building model.'), ('CH4-02', 'Auctioneer Lobby Portrait Background', 'CH4-02-auctioneer-background', 'backdrop.py', 'CH4-02-reference-v02-empty.png', 'Same close hotel camera and warm practical-light hierarchy; illustrated cloth crests/troughs, loaded seams, broken fringe, plaster loss, trim mitres/splices, metal fasteners/tarnish, lamp joints and grain/dents replace smooth fabric gradients.', 'The close background remains simplified compared with the detailed concept. Lamp-lit planes are deliberately grouped and can still look graphic; owner should judge surface richness beside the approved receptionist background.'), ('CH4-03', 'Auctioneer — Front-facing older man', 'CH4-03-auctioneer-showman', 'auctioneer.py', 'CH4-03-front-reference-v04.png', 'Latest owner steering supersedes the old exaggerated profile: a front-facing ordinary older man, direct gaze, restrained dry expression, natural nose/ears, silver hair, burgundy formalwear and low-held gavel. Explicit skin/hair/cloth ramps restore wrinkles, eyes, fingers, seams, satin and shirt construction. Approved receptionist/attendant/presenter guide human style, detail and compatible palette.', 'This is a proposed new frontal identity, not an approved model sheet. It remains stylized: face/hair anatomy, apparent age, expression and gavel grip require owner review against the approved human NPCs. No claim that their minimum standard has been met.')]

def main():
 req=json.loads((BATCH/'v02/evidence/canonical-requirements.json').read_text())
 assets=[]
 for id,title,stem,src,ref,changes,limits in SPECS:
  native=ROOT/'native'/f'{stem}-v04.png';im=Image.open(native)
  p=ROOT/'previews'/f'{stem}-v04-4x.png';im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(p)
  old=BATCH/'v02/native'/f'{stem}-v02.png';oldim=Image.open(old)
  old4=ROOT/'previews'/f'{stem}-v02-4x.png';oldim.resize((oldim.width*4,oldim.height*4),Image.Resampling.NEAREST).save(old4)
  prev3=BATCH/'v03/native'/f'{stem}-v03.png'
  prev3im=Image.open(prev3);prev34=ROOT/'previews'/f'{stem}-v03-4x.png';prev3im.resize((prev3im.width*4,prev3im.height*4),Image.Resampling.NEAREST).save(prev34)
  nodes=req[id]['sourceNodeIds']
  if id=='CH4-03':nodes=[k for k,v in req[id]['verbatimNodes'].items() if v.get('pose')=='showman']
  r={'id':id,'title':title,'version':'v04','status':'generated / unselected','assetPath':None,
   'native':info(native),'preview4x':info(p),'previousV02':info(old),'previousV02Preview4x':info(old4),'previousV03':info(prev3),'previousV03Preview4x':info(prev34),
   'previousV01':info(BATCH/'v01/native'/f'{stem}-v01.png'),
   'detailedReference':info(ROOT/'detailed'/ref) if id=='CH4-03' else info(BATCH/'v02/detailed'/ref),'authoredSource':['source/'+src,'source/materials.py']+(['source/room_detail.py'] if id=='CH4-01' else ['source/close_detail.py'] if id=='CH4-02' else []),
   'sourceNodeIds':nodes,'canonicalRequirements':'../v02/evidence/canonical-requirements.json',
   'changes':changes,'knownLimitations':limits}
  if id=='CH4-03':r['previousDetailedReference']=info(BATCH/'v02/detailed/CH4-03-reference-v01.png')
  # All three versions are pasted at exact native size into a review sheet.
  sheet=Image.new('RGBA',(im.width*3+48,im.height+46),'#1c282b');d=ImageDraw.Draw(sheet)
  for index,(label,obj) in enumerate([('v02',oldim),('v03',prev3im),('v04',im)]):
   x=12+index*(im.width+12);d.text((x,10),label+' / '+id,fill='#e9dbc0')
   for yy in range(30,30+im.height,8):
    for xx in range(x,x+im.width,8):d.rectangle((xx,yy,min(xx+7,x+im.width-1),min(yy+7,29+im.height)),fill='#3e4e47' if ((xx-x)//8+(yy-30)//8)%2 else '#2c3a35')
   sheet.alpha_composite(obj.convert('RGBA'),(x,30))
  cp=ROOT/'previews'/f'{id}-v02-v03-v04-native.png';sheet.convert('RGB').save(cp);r['comparisonSheet']=info(cp)
  assets.append(r)
 bg=Image.open(ROOT/'native/CH4-02-auctioneer-background-v04.png').convert('RGBA')
 fg=Image.open(ROOT/'native/CH4-03-auctioneer-showman-v04.png')
 composite=Image.alpha_composite(bg,fg).convert('RGB');composite.save(ROOT/'previews/auctioneer-composite-v04.png')
 composite.resize((2256,1112),Image.Resampling.NEAREST).save(ROOT/'previews/auctioneer-composite-v04-4x.png')
 canonical=[
  ('Bureau','../v02/references/scenes__biology_park__conveniences_bureau.png'),
  ('Control Tower','../v02/references/scenes__biology_park__control_tower.png'),
  ('Reception scene','../v02/references/scenes__conference_hall__reception__reception_scene.png'),
  ('Reception background','../v02/references/portraits__receptionist__reception_background.png'),
  ('Receptionist foreground','../v02/references/portraits__receptionist__receptionist_idle.png'),('Pavilion attendant','references/pavilion_attendant_idle.png'),('Pavilion presenter','references/pavilion_presenter_idle.png')]
 refs=[]
 for name,file in canonical:
  p=(ROOT/file).resolve();v=info(p);v['title']=name
  out=ROOT/'previews'/('approved-'+name.lower().replace(' ','-')+'-4x.png');im=Image.open(p);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(out);v['preview4x']=info(out);refs.append(v)
 manifest={'schema':'out-of-order-ch4-review-v04','dateEastern':'2026-11-22','version':'v04','reviewBranch':'art/ch4-batch01-review-20261121',
  'reviewedBaseCommit':'1fe2685c11a0a156998a13cd24687050e4d9f158','approval':'UNSELECTED. Technical passing is not creative approval.',
  'scope':'CH4-01, CH4-02, CH4-03 only. Restroom and ballroom are not revised.',
  'method':{'A':'Hotel concept references reused unchanged. One new built-in image_gen call creates a detailed frontal auctioneer study, guided by approved human NPCs. Its original PNG, prompt and receipt are preserved in v04.',
   'B':'Independent blank-native reconstruction: explicit material/anatomy color clusters, native curves and geometric coverage masks. v03 environmental light retained selectively; no procedural portrait face or cloth-gradient substitute. No source raster input, supersampling, smoothing, downsampling or palette reduction. No global palette quota.',
   'C':'Exact 4x NEAREST from completed native art. Portrait 4x exports are supplemental inspection views, not a change to the 564x278 portrait presentation contract.'},
  'assets':assets,'approvedReferences':refs,'composite':info(ROOT/'previews/auctioneer-composite-v04.png'),
  'preservationBaseline':'evidence/preservation-baseline.json','direction':'evidence/direction-v04.txt','validation':'evidence/validation.json'}
 dump(ROOT/'manifest.json',manifest)
 axes=[('Logical dimensions', '314x206 scene and separately authored 564x278 opaque/transparent portrait layers. Portrait head/body scale is compared with actual approved human NPCs.'), ('Meaningful detail', 'Restore material construction and localized wear: slab edges, carpet nap, grain, plaster/lath loss, stitched cloth, joints, petals and container rims. Portrait features, hands and tailoring are explicitly drawn.'), ('Silhouettes and identity', 'Scene NPCs stay tiny/simple. The portrait is front-facing per latest owner direction: normal nose/ears, quiet old-coot expression, silver hair, burgundy jacket and low gavel; old profile is superseded.'), ('Coherent ramps and palette', 'Explicit portrait skin, silver hair, charcoal/satin, ivory and muted burgundy ramps align with approved receptionist/attendant/presenter. No global palette limit or mass reduction; compare actual style/finish at 1x.'), ('Perspective and construction', 'Unified lobby VP (182,112), floor clipping at wall boundary, corrected converging window/ceiling long lines and podium edges. Separate wear clusters follow slab planes and real joints. See perspective-audit.json.'), ('Lighting and visibility', 'Retain v03 warm lamps/cooler window fill/deep recesses selectively. Wall and fabric shapes are painted as grouped planes and folds; avoid smooth mathematical fabric gradients and broad periodic texture noise.'), ('Anatomy, hands and fabric', 'Front-facing eyes, age folds, modest moustache, directional hair locks, fingers wrapping the low gavel, differentiated shirt/satin/cloth and stitched seams. Artistically unselected; approved receptionist remains the minimum target.'), ('Native and exact 4x comparison', 'Each asset has v02/v03/v04 native rows and exact 4x views; unchanged original concepts, v01, Chapter 2 rooms and approved human portraits are shown. Exact exports and native authorship do not establish aesthetic quality.')]
 comparison={'assets':{r['id']:{'changes':r['changes'],'knownLimitations':r['knownLimitations'],'references':['v02','v03','original concepts','Bureau','Control Tower','receptionist background/foreground','Pavilion attendant/presenter'],'axes':dict(axes)} for r in assets},'assessment':'v04 restores illustrated information and introduces the owner-directed frontal portrait. All three remain UNSELECTED. Human portrait palette/detail and finish require Nate’s comparison; technical passing does not establish artistic approval.'}
 dump(ROOT/'comparison.json',comparison)
 for r in assets:
  (ROOT/'prompts'/f'{r["id"]}-reconstruction-v04.txt').write_text('Independent native-grid reconstruction brief — v04\n'+r['changes']+'\n\nUse original detailed reference: '+r['detailedReference']['file']+'\nCompare directly with actual approved Bureau/Control Tower/reception art and unchanged v01/v02.\n\nNative method: '+manifest['method']['B']+'\nPresentation: '+manifest['method']['C']+'\nKnown limitations for review: '+r['knownLimitations']+'\nRemain UNSELECTED.\n')
 write_gallery(manifest,axes)

def write_gallery(m,axes):
 e=html.escape
 css='''*{box-sizing:border-box}html{color-scheme:dark}body{background:#172024;color:#eee3cd;font:16px/1.55 system-ui;margin:0}main{max-width:1440px;margin:auto;padding:30px}h1{font-size:32px}h2{font-size:24px}h3{font-size:17px}a{color:#b6dbc9}.status{color:#e6be95}article,section{background:#242f32;border:1px solid #58685a;border-radius:8px;margin:24px 0;padding:22px}.strip{overflow:auto;max-width:100%;padding:12px;background:#172024;margin:14px 0}.row{display:flex;gap:18px;width:max-content}.pixel{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}figure{margin:0}figcaption{padding:5px 0 10px}.checker{width:max-content;background:repeating-conic-gradient(#3e4e47 0% 25%,#2c3a35 0% 50%) 0 0/16px 16px}.concept{max-width:100%;height:auto}button,select{background:#405849;color:#fff;border:1px solid #84947f;border-radius:4px;padding:9px;font:inherit;cursor:pointer}nav{display:flex;flex-wrap:wrap;gap:18px}summary{cursor:pointer;padding:10px 0}table{border-collapse:collapse;min-width:580px}th,td{border:1px solid #6a7766;padding:10px;text-align:left;vertical-align:top}code{font-size:12px;overflow-wrap:anywhere}@media(max-width:640px){main{padding:12px}article,section{padding:14px}h1{font-size:25px}}'''
 body=f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 4 Batch 1 · v04 material and light review</title><style>{css}</style><main><h1>Chapter 4 · v04 rendering review</h1><p class="status">CH4-01 / CH4-02 / CH4-03 · UNSELECTED · November 22, 2026</p><p>v03 environmental lighting is retained selectively while meaningful material/construction detail is restored. Latest owner steering: the auctioneer now faces forward with natural proportions and a restrained expression, using approved human NPC detail and palette benchmarks. Review at 1× first. The approved artwork is a comparison target; passing file checks does not establish equivalent craft.</p><nav><a href="#CH4-01">Lobby</a><a href="#CH4-02">Background</a><a href="#CH4-03">Showman</a><a href="#approved">Approved references</a><a href="../v03/index.html">v03 gallery</a><a href="../v02/index.html">v02 gallery</a><a href="../v01/index.html">v01 gallery</a></nav><p><a href="manifest.json">Manifest / hashes</a> · <a href="comparison.json">Per-asset assessment</a> · <a href="evidence/direction-v04.txt">Owner direction</a> · <a href="../v02/evidence/canonical-requirements.json">Verbatim storyboard requirements</a> · <a href="evidence/validation.json">Native authorship / image QA</a> · <a href="evidence/browser-qa.json">Browser QA</a></p>'
 for i,r in enumerate(m['assets']):
  id=r['id'];w,h=r['native']['dimensions'];ref=m['approvedReferences'][0 if i==0 else 3 if i==1 else 4]
  body+=f'<article id="{id}"><h2>{id} · {e(r["title"])}</h2><p>{e(r["changes"])}</p><p class="status">Review limitation: {e(r["knownLimitations"])}</p><p><button class="scale" data-target="{id}" data-scale="1" aria-pressed="true">Native 1×</button> <button class="scale" data-target="{id}" data-scale="4" aria-pressed="false">Exact 4×</button></p><div class="strip"><div class="row">'
  for label,key,preview,role in [('v03 — preserved','previousV03','previousV03Preview4x','previous'),('v04 — unselected','native','preview4x','candidate'),('v02 — preserved','previousV02','previousV02Preview4x','previous2')]:
   n=r[key];large=r[preview]['file']
   body+=f'<figure><figcaption>{label} · {w}×{h}</figcaption><div class="checker"><img class="pixel scaled {role}" data-target="{id}" data-native="{n["file"]}" data-large="{large}" data-w="{w}" data-h="{h}" src="{n["file"]}" width="{w}" height="{h}" alt="{id} {label}"></div></figure>'
  body+='</div></div>'
  if i==0:
   body+='<label>Approved room benchmark: <select id="benchmark">'+''.join(f'<option value="{x["file"]}" data-large="{x["preview4x"]["file"]}">{x["title"]}</option>' for x in m['approvedReferences'][:3])+'</select></label>'
  body+=f'<h3>Approved {e(ref["title"])} · native comparison</h3><div class="strip"><div class="checker"><img class="pixel scaled benchmark" data-target="{id}" data-native="{ref["file"]}" data-large="{ref["preview4x"]["file"]}" data-w="{ref["dimensions"][0]}" data-h="{ref["dimensions"][1]}" src="{ref["file"]}" width="{ref["dimensions"][0]}" height="{ref["dimensions"][1]}" alt="Approved {e(ref["title"])}"></div></div>'
  body+=f'<p><a href="{r["comparisonSheet"]["file"]}">Direct v02/v03/v04 comparison PNG</a> · <a href="{r["native"]["file"]}">Native PNG</a> · <a href="{r["preview4x"]["file"]}">4× PNG</a> · <a href="{r["authoredSource"][0]}">Editable native source</a> · <a href="prompts/{id}-reconstruction-v04.txt">Reconstruction brief</a></p><p><code>SHA-256 {r["native"]["sha256"]}</code></p>'
  body+=f'<details><summary>Preserved v01 candidate</summary><div class="strip"><img class="pixel" src="{r["previousV01"]["file"]}" width="{w}" height="{h}" alt="{id} preserved v01"></div></details><details><summary>Original detailed concept reference — unchanged</summary><img class="concept" loading="lazy" src="{r["detailedReference"]["file"]}" alt="{id} original detailed reference"><p>Study reference; not the authored native source.</p></details></article>'
  if id=='CH4-03':body+='<section><h3>Earlier profile concept — preserved, superseded by frontal direction</h3><details><summary>Show the unchanged original detailed profile reference</summary><img class="concept" loading="lazy" src="../v02/detailed/CH4-03-reference-v01.png" alt="Earlier profile concept reference"></details></section>'
 body+='<section id="composite"><h2>Layered portrait comparison · native 564×278</h2><div class="strip"><div class="row">'
 for title,p in [('v02','../v02/previews/auctioneer-composite-v02.png'),('v03','../v03/previews/auctioneer-composite-v03.png'),('v04','previews/auctioneer-composite-v04.png'),('Approved receptionist','../v01/previews/approved-receptionist-composite.png')]:body+=f'<figure><figcaption>{title}</figcaption><img class="pixel" src="{p}" width="564" height="278" alt="{title} composite portrait"></figure>'
 body+='</div></div><p><a href="previews/auctioneer-composite-v04-4x.png">Exact 4× v04 portrait inspection</a></p></section><section id="approved"><h2>Canonical approved-art comparisons</h2><p>Bureau and Control Tower set the scene benchmark. Receptionist background and foreground set the close-up finish target. All benchmark PNGs are byte-unchanged; none was regenerated.</p>'
 for r in m['approvedReferences']:
  w,h=r['dimensions'];body+=f'<details><summary>{r["title"]} · native and exact 4×</summary><div class="strip"><div class="checker"><img class="pixel" src="{r["file"]}" width="{w}" height="{h}" alt="Approved {r["title"]}"></div></div><div class="strip"><img class="pixel" loading="lazy" src="{r["preview4x"]["file"]}" width="{w*4}" height="{h*4}" alt="Approved {r["title"]} exact 4x"></div></details>'
 body+='<div class="strip"><table><thead><tr><th>Axis</th><th>v04 assessment</th></tr></thead><tbody>'+''.join(f'<tr><td>{e(k)}</td><td>{e(v)}</td></tr>' for k,v in axes)+'</tbody></table></div><p>No declaration of artistic acceptance is made. The frontal portrait and illustrated material finish still require owner selection. Earlier versions remain byte-unchanged. Nate selects the standard before any restroom/ballroom revision.</p></section>'
 body+='''<script>const scales={};document.querySelectorAll('.scale').forEach(b=>b.addEventListener('click',()=>{const id=b.dataset.target,s=Number(b.dataset.scale);scales[id]=s;document.querySelectorAll('.scaled[data-target="'+id+'"]').forEach(i=>{i.src=s===1?i.dataset.native:i.dataset.large;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;});document.querySelectorAll('.scale[data-target="'+id+'"]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));}));document.querySelector('#benchmark').addEventListener('change',e=>{const o=e.target.selectedOptions[0],i=document.querySelector('.benchmark[data-target="CH4-01"]'),s=scales['CH4-01']||1;i.dataset.native=o.value;i.dataset.large=o.dataset.large;i.src=s===1?o.value:o.dataset.large;});</script></main></html>'''
 (ROOT/'index.html').write_text(body)

if __name__=='__main__':main()
