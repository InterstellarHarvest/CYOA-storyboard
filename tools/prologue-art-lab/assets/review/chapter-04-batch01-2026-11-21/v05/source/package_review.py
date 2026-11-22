"""v05 delivery exports only: reads finished native art for comparison/presentation.

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

SPECS=[('CH4-01', 'Grand Bellevue Lobby — targeted wear corrections', 'CH4-01-lobby', 'lobby.py', 'CH4-01-reference-v01.png', 'Continue the v04 working composition unchanged. Replace repetitive carpet islands with an uneven lower-contrast walking track, broken nap and short scuffs. Replace decorative plaster chips with moisture tracks below real duct fixings, corner cracks and lower-wall impact/damp loss. Successful lighting, perspective, ductwork, furniture, flowers and simple NPCs are byte-preserved outside the correction mask.', 'These remain small-scale illustrated wear cues. Judge whether their placement and contrast look natural at native size; no creative acceptance is implied by the mask checks.'), ('CH4-02', 'Auctioneer background — lamp and wall corrections', 'CH4-02-auctioneer-background', 'backdrop.py', 'CH4-02-reference-v02-empty.png', 'Continue v04. Replace the three obvious lamp rings with a weak continuous falloff only on the actual lamp panel; add low-contrast native plaster repair/finishing marks to blank wall areas. Curtain construction, duct wear, molding and fixtures are preserved outside the wall correction mask.', 'The lamp-wall falloff is computed locally as illumination, not a whole-image style pass. Blank-wall variation is deliberately subtle; assess it beside the approved receptionist background.'), ('CH4-03', 'Auctioneer — detailed frontal portrait', 'CH4-03-auctioneer-showman', 'auctioneer.py', 'CH4-03-front-reference-v04.png', 'Preserve the frontal elderly identity, proportions, silhouette and low-held gavel. Rebuild the socket/weighted lids/brows to reduce the startled stare; paint nuanced forehead/crow’s-foot/cheek/nose/mouth/neck marks, neutral silver locks, knuckles/grip and gavel wood, cloth folds/seams, satin crests and cotton construction. Use layered native pixel-brush pigment marks over a reconstructed substrate rather than another global procedural face-lighting pass.', 'The result remains an illustrated, relatively graphic candidate; it is not claimed to match the approved receptionist/Pavilion finish automatically. Owner must judge whether the face, hair, hands and costume now have sufficient natural craft and character.')]

def main():
 req=json.loads((BATCH/'v02/evidence/canonical-requirements.json').read_text())
 assets=[]
 for id,title,stem,src,ref,changes,limits in SPECS:
  native=ROOT/'native'/f'{stem}-v05.png';im=Image.open(native)
  p=ROOT/'previews'/f'{stem}-v05-4x.png';im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(p)
  old=BATCH/'v02/native'/f'{stem}-v02.png';oldim=Image.open(old)
  old4=ROOT/'previews'/f'{stem}-v02-4x.png';oldim.resize((oldim.width*4,oldim.height*4),Image.Resampling.NEAREST).save(old4)
  prev3=BATCH/'v03/native'/f'{stem}-v03.png'
  prev3im=Image.open(prev3);prev34=ROOT/'previews'/f'{stem}-v03-4x.png';prev3im.resize((prev3im.width*4,prev3im.height*4),Image.Resampling.NEAREST).save(prev34)
  prev4=BATCH/'v04/native'/f'{stem}-v04.png'
  prev4im=Image.open(prev4);prev44=ROOT/'previews'/f'{stem}-v04-4x.png';prev4im.resize((prev4im.width*4,prev4im.height*4),Image.Resampling.NEAREST).save(prev44)
  nodes=req[id]['sourceNodeIds']
  if id=='CH4-03':nodes=[k for k,v in req[id]['verbatimNodes'].items() if v.get('pose')=='showman']
  r={'id':id,'title':title,'version':'v05','status':'generated / unselected','assetPath':None,
   'native':info(native),'preview4x':info(p),'previousV02':info(old),'previousV02Preview4x':info(old4),'previousV03':info(prev3),'previousV03Preview4x':info(prev34),'previousV04':info(prev4),'previousV04Preview4x':info(prev44),
   'previousV01':info(BATCH/'v01/native'/f'{stem}-v01.png'),
   'detailedReference':info(BATCH/'v04/detailed'/ref) if id=='CH4-03' else info(BATCH/'v02/detailed'/ref),'authoredSource':['source/'+src,'source/materials.py']+(['source/room_detail.py'] if id=='CH4-01' else ['source/close_detail.py','source/wall_light.py','source/pixel_brush.py'] if id=='CH4-02' else ['source/portrait_paint.py','source/pixel_brush.py']),
   'sourceNodeIds':nodes,'canonicalRequirements':'../v02/evidence/canonical-requirements.json',
   'changes':changes,'knownLimitations':limits}
  if id=='CH4-03':r['previousDetailedReference']=info(BATCH/'v02/detailed/CH4-03-reference-v01.png')
  # Compare exact native pixels in the last accepted working base and this pass.
  sheet=Image.new('RGBA',(im.width*2+36,im.height+46),'#1c282b');d=ImageDraw.Draw(sheet)
  for index,(label,obj) in enumerate([('v04',prev4im),('v05',im)]):
   x=12+index*(im.width+12);d.text((x,10),label+' / '+id,fill='#e9dbc0')
   for yy in range(30,30+im.height,8):
    for xx in range(x,x+im.width,8):d.rectangle((xx,yy,min(xx+7,x+im.width-1),min(yy+7,29+im.height)),fill='#3e4e47' if ((xx-x)//8+(yy-30)//8)%2 else '#2c3a35')
   sheet.alpha_composite(obj.convert('RGBA'),(x,30))
  cp=ROOT/'previews'/f'{id}-v04-v05-native.png';sheet.convert('RGB').save(cp);r['comparisonSheet']=info(cp)
  assets.append(r)
 bg=Image.open(ROOT/'native/CH4-02-auctioneer-background-v05.png').convert('RGBA')
 fg=Image.open(ROOT/'native/CH4-03-auctioneer-showman-v05.png')
 composite=Image.alpha_composite(bg,fg).convert('RGB');composite.save(ROOT/'previews/auctioneer-composite-v05.png')
 composite.resize((2256,1112),Image.Resampling.NEAREST).save(ROOT/'previews/auctioneer-composite-v05-4x.png')
 canonical=[
  ('Bureau','../v02/references/scenes__biology_park__conveniences_bureau.png'),
  ('Control Tower','../v02/references/scenes__biology_park__control_tower.png'),
  ('Reception scene','../v02/references/scenes__conference_hall__reception__reception_scene.png'),
  ('Reception background','../v02/references/portraits__receptionist__reception_background.png'),
  ('Receptionist foreground','../v02/references/portraits__receptionist__receptionist_idle.png'),('Pavilion attendant','../v04/references/pavilion_attendant_idle.png'),('Pavilion presenter','../v04/references/pavilion_presenter_idle.png')]
 refs=[]
 for name,file in canonical:
  p=(ROOT/file).resolve();v=info(p);v['title']=name
  out=ROOT/'previews'/('approved-'+name.lower().replace(' ','-')+'-4x.png');im=Image.open(p);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(out);v['preview4x']=info(out);refs.append(v)
 manifest={'schema':'out-of-order-ch4-review-v05','dateEastern':'2026-11-22','version':'v05','reviewBranch':'art/ch4-batch01-review-20261121',
  'reviewedBaseCommit':'ca08ce8917a6ae24ada6c6b83182cd0104ebfbd8','approval':'UNSELECTED. Technical passing is not creative approval.',
  'scope':'CH4-01, CH4-02, CH4-03 only. Restroom and ballroom are not revised.',
  'method':{'A':'Use the unchanged v04 detailed frontal study as primary character guide; hotel concepts and all approved portraits are unchanged. No new imagegen call in v05; original prompt and receipt remain preserved in v04.',
   'B':'Reconstruct from blank native canvases. Portrait authoring adds explicitly placed pressure/width/opacity pigment brush marks for anatomy, hair, hands and tailoring on the native substrate; marks may mix only with that writer’s own native paint, never with reference raster pixels. No global procedural portrait-lighting field, blur, supersampling, source downsampling or palette reduction. Room corrections are mask-restricted.',
   'C':'Exact 4x NEAREST from completed native art. Portrait 4x exports are supplemental inspection views, not a change to the 564x278 portrait presentation contract.'},
  'assets':assets,'approvedReferences':refs,'composite':info(ROOT/'previews/auctioneer-composite-v05.png'),
  'preservationBaseline':'evidence/preservation-baseline.json','direction':'evidence/direction-v05.txt','validation':'evidence/validation.json'}
 dump(ROOT/'manifest.json',manifest)
 axes=[('Native scale', '314x206 lobby, 564x278 separate opaque background and binary-transparent foreground. Review actual artwork at 1x before 4x inspection.'), ('Anatomy and expression', 'Frontal proportions/silhouette retained; sockets and lower brows reconstructed, upper lids weighted, mouth and smile folds defined, neck/jowl planes repainted. Intended expression is slightly cantankerous and dignified; owner must judge it.'), ('Meaningful portrait detail', 'Native brush marks add forehead/crow’s-foot/eyelid/cheekbone/nose/mouth detail, grouped silver locks and strands, a wrapped gavel grip, gavel bevel/grain, cloth seams/folds and cotton/satin distinctions. More marks do not automatically equal sufficient craft.'), ('Ramps and palette', 'Hand-chosen pigment colors and local brush mixtures; neutral silver hair, warm skin, muted burgundy, charcoal satin and ivory are compared directly with approved human NPCs. No arbitrary global palette quota or color-count quality score.'), ('Environment scope', 'Lobby edits are limited to carpet wear and architectural plaster damage. Background edits are limited to lamp-panel light and blank-wall variation. Explicit changed-pixel masks and protected fixture/geometry checks prove successful details are retained.'), ('Lighting and materials', 'Retain v04 room lighting and pose. One local wall-light falloff replaces visible rings; no new broad mathematical face/cloth rendering pass. Brush layers illustrate material/anatomical structure.'), ('Reference comparisons', 'Actual receptionist, Pavilion attendant and presenter art are shown with v04/v05, the unchanged frontal study and original hotel concepts. Earlier v01/v02/v03 galleries remain intact.'), ('Export and review', 'Native and exact 4x comparisons, direct PNGs, transparent foreground, layered composite and targeted-delta evidence are included. QA establishes file/preservation properties only; all candidates stay UNSELECTED.')]
 comparison={'assets':{r['id']:{'changes':r['changes'],'knownLimitations':r['knownLimitations'],'references':['v04','unchanged frontal study','receptionist','Pavilion attendant','Pavilion presenter','Bureau','Control Tower'],'axes':dict(axes)} for r in assets},'assessment':'v05 prioritizes the frontal portrait and confines room edits to the owner’s specified areas. The portrait remains a relatively graphic painting candidate. Technical passing is not a claim that approved human-NPC craft has been achieved.'}
 dump(ROOT/'comparison.json',comparison)
 for r in assets:
  (ROOT/'prompts'/f'{r["id"]}-reconstruction-v05.txt').write_text('Independent native-grid reconstruction brief — v05\n'+r['changes']+'\n\nUse original detailed reference: '+r['detailedReference']['file']+'\nCompare directly with actual approved Bureau/Control Tower/reception art and unchanged v01/v02.\n\nNative method: '+manifest['method']['B']+'\nPresentation: '+manifest['method']['C']+'\nKnown limitations for review: '+r['knownLimitations']+'\nRemain UNSELECTED.\n')
 write_gallery(manifest,axes)

def write_gallery(m,axes):
 e=html.escape
 css='''*{box-sizing:border-box}html{color-scheme:dark}body{background:#172024;color:#eee3cd;font:16px/1.55 system-ui;margin:0}main{max-width:1440px;margin:auto;padding:30px}h1{font-size:32px}h2{font-size:24px}h3{font-size:17px}a{color:#b6dbc9}.status{color:#e6be95}article,section{background:#242f32;border:1px solid #58685a;border-radius:8px;margin:24px 0;padding:22px}.strip{overflow:auto;max-width:100%;padding:12px;background:#172024;margin:14px 0}.row{display:flex;gap:18px;width:max-content}.pixel{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}figure{margin:0}figcaption{padding:5px 0 10px}.checker{width:max-content;background:repeating-conic-gradient(#3e4e47 0% 25%,#2c3a35 0% 50%) 0 0/16px 16px}.concept{max-width:100%;height:auto}button,select{background:#405849;color:#fff;border:1px solid #84947f;border-radius:4px;padding:9px;font:inherit;cursor:pointer}nav{display:flex;flex-wrap:wrap;gap:18px}summary{cursor:pointer;padding:10px 0}table{border-collapse:collapse;min-width:580px}th,td{border:1px solid #6a7766;padding:10px;text-align:left;vertical-align:top}code{font-size:12px;overflow-wrap:anywhere}@media(max-width:640px){main{padding:12px}article,section{padding:14px}h1{font-size:25px}}'''
 body=f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 4 Batch 1 · v05 material and light review</title><style>{css}</style><main><h1>Chapter 4 · v05 rendering review</h1><p class="status">CH4-01 / CH4-02 / CH4-03 · UNSELECTED · November 22, 2026</p><p>Priority: reconstruct the frontal auctioneer’s facial character, hair, hands and costume with native pixel-brush painting. Keep v04 as the room base and make only specified carpet/plaster/lamp/wall corrections. Judge against the actual approved human NPC art, not file dimensions or color count. Review at 1× first. The approved artwork is a comparison target; passing file checks does not establish equivalent craft.</p><nav><a href="#CH4-01">Lobby</a><a href="#CH4-02">Background</a><a href="#CH4-03">Showman</a><a href="#approved">Approved references</a><a href="../v04/index.html">v04 gallery</a><a href="../v03/index.html">v03 gallery</a><a href="../v02/index.html">v02 gallery</a><a href="../v01/index.html">v01 gallery</a></nav><p><a href="manifest.json">Manifest / hashes</a> · <a href="comparison.json">Per-asset assessment</a> · <a href="evidence/direction-v05.txt">Owner direction</a> · <a href="../v02/evidence/canonical-requirements.json">Verbatim storyboard requirements</a> · <a href="evidence/validation.json">Native authorship / image QA</a> · <a href="evidence/browser-qa.json">Browser QA</a> · <a href="evidence/targeted-change-qa.json">Targeted room changes</a></p>'
 for i,r in enumerate(sorted(m['assets'],key=lambda a:0 if a['id']=='CH4-03' else 1 if a['id']=='CH4-01' else 2)):
  id=r['id'];w,h=r['native']['dimensions'];ref=m['approvedReferences'][0 if id=='CH4-01' else 3 if id=='CH4-02' else 4]
  body+=f'<article id="{id}"><h2>{id} · {e(r["title"])}</h2><p>{e(r["changes"])}</p><p class="status">Review limitation: {e(r["knownLimitations"])}</p><p><button class="scale" data-target="{id}" data-scale="1" aria-pressed="true">Native 1×</button> <button class="scale" data-target="{id}" data-scale="4" aria-pressed="false">Exact 4×</button></p><div class="strip"><div class="row">'
  for label,key,preview,role in [('v04 — preserved working base','previousV04','previousV04Preview4x','previous'),('v05 — unselected','native','preview4x','candidate'),('v03 — historical','previousV03','previousV03Preview4x','previous2')]:
   n=r[key];large=r[preview]['file']
   body+=f'<figure><figcaption>{label} · {w}×{h}</figcaption><div class="checker"><img class="pixel scaled {role}" data-target="{id}" data-native="{n["file"]}" data-large="{large}" data-w="{w}" data-h="{h}" src="{n["file"]}" width="{w}" height="{h}" alt="{id} {label}"></div></figure>'
  body+='</div></div>'
  if id=='CH4-01':
   body+='<label>Approved room benchmark: <select id="benchmark">'+''.join(f'<option value="{x["file"]}" data-large="{x["preview4x"]["file"]}">{x["title"]}</option>' for x in m['approvedReferences'][:3])+'</select></label>'
  body+=f'<h3>Approved {e(ref["title"])} · native comparison</h3><div class="strip"><div class="checker"><img class="pixel scaled benchmark" data-target="{id}" data-native="{ref["file"]}" data-large="{ref["preview4x"]["file"]}" data-w="{ref["dimensions"][0]}" data-h="{ref["dimensions"][1]}" src="{ref["file"]}" width="{ref["dimensions"][0]}" height="{ref["dimensions"][1]}" alt="Approved {e(ref["title"])}"></div></div>'
  body+=f'<p><a href="{r["comparisonSheet"]["file"]}">Direct v04/v05 comparison PNG</a> · <a href="{r["native"]["file"]}">Native PNG</a> · <a href="{r["preview4x"]["file"]}">4× PNG</a> · <a href="{r["authoredSource"][0]}">Editable native source</a> · <a href="prompts/{id}-reconstruction-v05.txt">Reconstruction brief</a></p><p><code>SHA-256 {r["native"]["sha256"]}</code></p>'
  body+=f'<details><summary>Preserved v01 candidate</summary><div class="strip"><img class="pixel" src="{r["previousV01"]["file"]}" width="{w}" height="{h}" alt="{id} preserved v01"></div></details><details><summary>Original detailed concept reference — unchanged</summary><img class="concept" loading="lazy" src="{r["detailedReference"]["file"]}" alt="{id} original detailed reference"><p>Study reference; not the authored native source.</p></details></article>'
  if id=='CH4-03':body+='<section><h3>Earlier profile concept — preserved, superseded by frontal direction</h3><details><summary>Show the unchanged original detailed profile reference</summary><img class="concept" loading="lazy" src="../v02/detailed/CH4-03-reference-v01.png" alt="Earlier profile concept reference"></details></section>'
 body+='<section id="composite"><h2>Layered portrait comparison · native 564×278</h2><div class="strip"><div class="row">'
 for title,p in [('v04','../v04/previews/auctioneer-composite-v04.png'),('v05','previews/auctioneer-composite-v05.png'),('Approved receptionist','../v01/previews/approved-receptionist-composite.png')]:body+=f'<figure><figcaption>{title}</figcaption><img class="pixel" src="{p}" width="564" height="278" alt="{title} composite portrait"></figure>'
 body+='</div></div><p><a href="previews/auctioneer-composite-v05-4x.png">Exact 4× v05 portrait inspection</a></p></section><section id="approved"><h2>Canonical approved-art comparisons</h2><p>Bureau and Control Tower set the scene benchmark. Receptionist background and foreground set the close-up finish target. All benchmark PNGs are byte-unchanged; none was regenerated.</p>'
 for r in m['approvedReferences']:
  w,h=r['dimensions'];body+=f'<details><summary>{r["title"]} · native and exact 4×</summary><div class="strip"><div class="checker"><img class="pixel" src="{r["file"]}" width="{w}" height="{h}" alt="Approved {r["title"]}"></div></div><div class="strip"><img class="pixel" loading="lazy" src="{r["preview4x"]["file"]}" width="{w*4}" height="{h*4}" alt="Approved {r["title"]} exact 4x"></div></details>'
 body+='<div class="strip"><table><thead><tr><th>Axis</th><th>v05 assessment</th></tr></thead><tbody>'+''.join(f'<tr><td>{e(k)}</td><td>{e(v)}</td></tr>' for k,v in axes)+'</tbody></table></div><p>No declaration of artistic acceptance is made. The frontal portrait and illustrated material finish still require owner selection. Earlier versions remain byte-unchanged. Room correction masks and preservation checks are in evidence/targeted-change-qa.json. Nate selects the standard before any restroom/ballroom revision.</p></section>'
 body+='''<script>const scales={};document.querySelectorAll('.scale').forEach(b=>b.addEventListener('click',()=>{const id=b.dataset.target,s=Number(b.dataset.scale);scales[id]=s;document.querySelectorAll('.scaled[data-target="'+id+'"]').forEach(i=>{i.src=s===1?i.dataset.native:i.dataset.large;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;});document.querySelectorAll('.scale[data-target="'+id+'"]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));}));document.querySelector('#benchmark').addEventListener('change',e=>{const o=e.target.selectedOptions[0],i=document.querySelector('.benchmark[data-target="CH4-01"]'),s=scales['CH4-01']||1;i.dataset.native=o.value;i.dataset.large=o.dataset.large;i.src=s===1?o.value:o.dataset.large;});</script></main></html>'''
 (ROOT/'index.html').write_text(body)

if __name__=='__main__':main()
