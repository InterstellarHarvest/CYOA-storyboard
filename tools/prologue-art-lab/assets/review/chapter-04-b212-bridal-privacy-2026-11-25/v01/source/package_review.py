"""Package the frozen first-pass candidates without changing their PNG bytes."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json,html
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists())
BASE='9f49416c9dd2e8b02e84b04a6c4ed1f4bc5e65b5'
MAIN='13ea9b57ee3b5c670a3ab0ff0f160896559ce2ef'
BRANCH='art/ch4-b212-bridal-privacy-review-20261125'
ROOM='native/CH4-NEW-01-bridal-dressing-room-v01.png'
PANEL='native/CH4-NEW-07-bridal-privacy-panel-v01.png'
PROVISIONAL='native/CH4-NEW-07-provisional-authorized-v01.png'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def record(rel):
 p=ROOT/rel;im=Image.open(p);return {'file':rel,'sha256':sha(p),'dimensions':list(im.size),'mode':im.mode,'bytes':p.stat().st_size}
def preview(rel):
 p=Path(rel);im=Image.open(ROOT/p);name='previews/'+p.stem+'-4x.png'
 im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/name);return name
def main():
 refs=json.loads((ROOT/'evidence/benchmark-provenance.json').read_text())
 for r in refs:preview(r['file'])
 for p in (ROOT/'diagnostics').glob('*.png'):preview(p.relative_to(ROOT).as_posix())
 font=ImageFont.load_default(size=13);captions=[]
 def sheet(name,items):
  sizes=[Image.open(ROOT/p).size for label,p in items]
  widths=[max(w+20,int(font.getlength(label))+20)for(label,p),(w,h)in zip(items,sizes)]
  out=Image.new('RGB',(sum(widths)+8,max(h for w,h in sizes)+54),'#263a32');d=ImageDraw.Draw(out);x=8
  for (label,p),width in zip(items,widths):
   d.text((x+6,9),label,font=font,fill='#f0e2bd');out.paste(Image.open(ROOT/p).convert('RGB'),(x+6,44))
   captions.append({'sheet':name,'caption':label,'textWidth':font.getlength(label),'panelWidth':width,'fits':font.getlength(label)<=width-12});x+=width
  rel=f'comparisons/{name}-native.png';out.save(ROOT/rel);preview(rel);return rel
 sheet('scene-ch2',[('B2-12 candidate 314x206',ROOM),('Approved Ch2 Bureau','references/conveniences_bureau.png'),('Approved Ch2 Control Tower','references/control_tower.png')])
 sheet('scene-ch4',[('B2-12 candidate',ROOM),('Approved Ch4 Lobby','references/lobby.png'),('Approved Ch4 Ballroom','references/ballroom.png'),('Approved Staff Lavatory','references/staff_lavatory.png'),('Approved Public Corridor','references/public_corridor.png')])
 sheet('privacy-statuses',[('LOCKED / UNSELECTED',PANEL),('PROVISIONAL / conditional reference',PROVISIONAL)])
 sheet('focus-benchmarks',[('B2-12 brief: 565x451',PANEL),('Approved Ch4: 564x278','references/master_isolator.png'),('Approved Ch2: 564x278','references/exposure_dispenser_open.png')])
 sheet('scene-source-diagnostic-native',[('Source-derived diagnostic ONLY','diagnostics/room-source-derived-diagnostic-NOT-production.png'),('Native material / structural interpretation',ROOM)])
 sheet('panel-source-diagnostic-native',[('Source-derived diagnostic ONLY','diagnostics/panel-source-derived-diagnostic-NOT-production.png'),('Native fixtures / lettering',PANEL)])
 (ROOT/'evidence/caption-layout.json').write_text(json.dumps(captions,indent=2)+'\n')
 # Source originals, exact prompts and the actual reference inputs are retained.
 origins=[
  {'file':'originals/CH4-NEW-01-detailed-reference.png','prompt':'source/room-detailed-prompt.txt','purpose':'Detailed empty-room composition, material and light reference','inputs':[],'inputNote':'Exact textual prompt retained. The first call reference-attachment list was not retained; this empty list does not assert there were no attachments. The pixel-friendly study below has an explicit retained reference list. Canonical benchmark copies are separately hash-pinned.'},
  {'file':'originals/CH4-NEW-01-pixel-friendly-study.png','prompt':'source/room-pixel-friendly-prompt.txt','purpose':'Pixel-friendly material/cluster study; NOT production artwork','inputs':['originals/CH4-NEW-01-detailed-reference.png','references/conveniences_bureau.png','references/lobby.png','references/staff_lavatory.png']},
  {'file':'originals/CH4-NEW-07-detailed-reference.png','prompt':'source/focus-reference-prompt.txt','purpose':'Physical brass-panel closeup, lighting and hardware reference','inputs':['originals/CH4-NEW-01-pixel-friendly-study.png','references/master_isolator.png']},
 ]
 for r in origins:r.update(record(r['file']));r['promptSha256']=sha(ROOT/r['prompt']);r['inputHashes']={f:sha(ROOT/f)for f in r['inputs']}
 (ROOT/'evidence/generation-provenance.json').write_text(json.dumps({'tool':'Built-in image_gen.imagegen','generationDate':'2026-11-25','providerSeed':'not exposed','sources':origins,'sourceDerived':True,'whollyIndependentNativeAuthorship':False,'derivation':'Source-informed material fields inside native semantic masks, connected shade-group cleanup and separately specified final-grid architectural profiles, door geometry, rolling stand, gown seams, camera optics, brass frames, policy pictograms and hand-defined binary pixel lettering. Final images assembled from native layers. No dithering or interpolated enlargement. Diagnostics are explicitly source-derived and are not production images.'},indent=2)+'\n')
 ordinary=['hotel_bridal_room','hotel_bridal_door_knock','hotel_bridal_door_focus','hotel_bridal_criteria','hotel_bridal_false_claim','hotel_bridal_emergency_override','hotel_bridal_ring_argument','hotel_bridal_gown_focus','hotel_bridal_gown_motor','hotel_bridal_gown_camera','hotel_bridal_gown_try','hotel_bridal_autofit_survived','hotel_bridal_door_options']
 nodes=json.loads((ROOT/'evidence/canonical-nodes.json').read_text());ordinary=[n for n in ordinary if n in nodes]
 def asset(id,label,rel,kind,key,nodeids):
  return {'id':id,'label':label,'status':'UNSELECTED','ownerApproved':False,'selected':False,'class':kind,'proposedCanonicalKey':key,'canonicalAssetPath':None,'runtimeBinding':None,'native':record(rel),'preview4x':record('previews/'+Path(rel).stem+'-4x.png'),'canonicalNodes':nodeids,'provenance':'SOURCE-DERIVED','sourceDerived':True,'whollyIndependentNativeAuthorship':False}
 room=asset('CH4-NEW-01','Bridal dressing room',ROOM,'main','scenes:grand_bellevue/bridal_dressing_room',ordinary)
 room['coverageBoundary']='Room location baseline only. No bride/player/AI character, AutoFit Focus, fatal aftermath or later lavatory artwork is supplied. Closed door base does not implement later open-door dispatch.'
 focusnodes=['hotel_bridal_door_focus','hotel_bridal_criteria','hotel_bridal_false_claim','hotel_bridal_emergency_override','hotel_bridal_ring_argument','hotel_bridal_door_options']
 panel=asset('CH4-NEW-07','Bridal privacy system: locked',PANEL,'Focus A','focus:grand_bellevue/bridal_privacy_panel',focusnodes)
 panel['contractNotice']='565x451 follows the explicit review brief. Current approved/runtime Focus is564x278. NOT registered or asserted compatible. Dimension resolution belongs to separate engineering/approval, not this review.'
 variant=asset('CH4-NEW-07-provisional','Provisional bridal authorization',PROVISIONAL,'conditional production reference',None,['hotel_bridal_autofit_survived'])
 variant.update({'parentAsset':'CH4-NEW-07','newFocusId':None,'newFlag':None,'runtimeBinding':None,'existingNarrativeCondition':'hotel_bridal_autofit_survived; existing ch4_provisional_bride_registered flag after survival','stateFamily':'bridal_privacy_status','stateLabel':'provisional authorization / green LED / open lock','implementationBoundary':'Reference image only. No dispatch, bindings, new modes, new flags or narrative nodes. Shared physical panel geometry is exact outside the authorized screen/LED masks. Main-room bathroom door stays closed.'})
 manifest={'title':'Chapter4 B2-12 v01: Bridal dressing room and privacy panel','branch':BRANCH,'briefCommit':BASE,'canonicalReferenceCommit':MAIN,'preservationBaseline':BASE,'status':'UNSELECTED','ownerApproved':False,'selected':False,'primaryAssetCount':2,'supplementalReferenceCount':1,'primaryAssets':[room,panel],'supplementalReferences':[variant],'sourceDerived':True,'whollyIndependentNativeAuthorship':False,'dimensionContract':'evidence/dimension-contract.json','nativeLayerRecipes':'evidence/native-layer-recipes.json','generationProvenance':'evidence/generation-provenance.json','benchmarks':'evidence/benchmark-provenance.json','narrativeGameplayBindingsModified':False,'productionSelectionsModified':False,'nextQueueNotStarted':['B2-13','B2-14']}
 (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 def fig(title,rel):
  im=Image.open(ROOT/rel);four='previews/'+Path(rel).stem+'-4x.png'
  return f'<section class="figure"><h3>{html.escape(title)}</h3><nav><button data-scale="1">Native 1×</button><button data-scale="4">Exact 4×</button><a href="{rel}">Native PNG</a><a href="{four}">4× PNG</a></nav><div class="raster"><img src="{rel}" data-one="{rel}" data-four="{four}" data-w="{im.width}" data-h="{im.height}" width="{im.width}" height="{im.height}" alt="{html.escape(title)}"></div></section>'
 css='body{margin:0;background:#172a23;color:#efe5c8;font:16px/1.55 system-ui,sans-serif}main{padding:22px}header,article{padding:20px;border:1px solid #697c6d;margin-bottom:26px}h1,h2,h3{margin:0 0 12px}a{color:#c5dfca;margin-right:14px}nav{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0}button{padding:10px;background:#435e4d;border:1px solid #bacbaa;color:#fff0ca;cursor:pointer}.figure{padding:14px;margin:20px 0;background:#294136}.raster{overflow:auto;max-width:100%;background:#253b32}.raster img{display:block;max-width:none!important;image-rendering:pixelated}code{overflow-wrap:anywhere}.notice{border-left:5px solid #cfa562;padding:12px;background:#3c3e2b}p{max-width:1120px}'
 header='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>B2-12 v01 · Bridal privacy</title><style>'+css+'</style><main><header><h1>B2-12 v01 · Bridal privacy</h1><p><strong>Two primary candidates + one conditional reference. Everything UNSELECTED.</strong> Empty dressing room, conspicuously narrow white gown on a wheeled stand, closed handle-less bathroom door and voice-only brass camera/screen system. No character or AI portrait.</p><p>Source-derived native material/structural interpretation with editable masks/layers and binary pixel lettering. Detailed generation originals and their exact prompts are preserved. 4× buttons load exact nearest-neighbor exports at their full integer dimensions; wider sheets scroll horizontally.</p><p class="notice"><strong>Dimension boundary:</strong> the invoked brief explicitly requests 565×451 for Focus A; existing approved/runtime Focus uses564×278. These review PNGs follow565×451. No runtime compatibility, registration or binding change is claimed. The approved benchmarks keep their own actual dimensions.</p><nav><a href="#room">Room</a><a href="#panel">Locked panel</a><a href="#provisional">Authorized reference</a><a href="#comparisons">Comparisons</a><a href="#benchmarks">Approved benchmarks</a><a href="#sources">Sources</a><a href="manifest.json">Manifest / hashes</a><a href="README.md">Method / handoff</a><a href="evidence/validation.json">QA</a><a href="evidence/generation-provenance.json">Provenance</a><a href="source/build_native.py">Native recipe</a></nav></header>'
 body='<article id="room"><h2>CH4-NEW-01 · 314×206 opaque RGB</h2>'+fig('Bridal dressing room · UNSELECTED',ROOM)+'</article>'
 body+='<article id="panel"><h2>CH4-NEW-07 · locked / denied baseline · 565×451 RGB</h2><p>Camera, recessed CRT, red indicator, closed lock, bride-only rule and physical emergency button. Long narrative wording remains in dialogue.</p>'+fig('Bridal privacy system · UNSELECTED',PANEL)+'</article>'
 body+='<article id="provisional"><h2>Supplemental reference · provisional authorization</h2><p>Green light and open lock after canonical AutoFit survival. Only screen/indicator pixels change. No extra Focus ID, flag or runtime binding.</p>'+fig('Provisional bridal status · UNSELECTED',PROVISIONAL)+'</article>'
 body+='<article id="comparisons"><h2>Native / exact4× comparisons</h2>'
 for label,name in [('Scene against Chapter2','scene-ch2'),('Scene against Chapter4','scene-ch4'),('Locked / provisional shared geometry','privacy-statuses'),('Focus against actual approved object art','focus-benchmarks'),('Source diagnostic / native scene','scene-source-diagnostic-native'),('Source diagnostic / native panel','panel-source-diagnostic-native')]:body+=fig(label,f'comparisons/{name}-native.png')
 body+='</article><article id="benchmarks"><h2>Actual approved artwork · unchanged canonical bytes</h2>'
 for r in refs:body+=fig(('Main scene · 'if r['class']=='main'else'Focus · ')+Path(r['file']).stem,r['file'])
 body+='</article><article id="sources"><h2>Detailed originals and authoring evidence</h2><p>Large generated images are reference sources, not deliverables. The explicitly source-derived diagnostic reductions in the comparisons are not production artwork.</p><nav>'
 for r in origins:body+=f'<a href="{r["file"]}">{html.escape(Path(r["file"]).stem)}</a><a href="{r["prompt"]}">Exact prompt</a>'
 body+='</nav><nav><a href="evidence/native-layer-recipes.json">Layer orders</a><a href="evidence/material-ramps.json">Material ramps</a><a href="evidence/lettering-layout.json">Lettering / margins</a><a href="evidence/canonical-nodes.json">Canonical node excerpts</a><a href="evidence/dimension-contract.json">Dimension contract</a><a href="evidence/visual-review.md">Visual gate</a></nav></article>'
 script='<script>document.querySelectorAll("button[data-scale]").forEach(b=>b.onclick=()=>{const i=b.closest("section.figure").querySelector("img"),s=Number(b.dataset.scale);i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;});</script></main></html>'
 (ROOT/'index.html').write_text(header+body+script)
 print(json.dumps({'primary':2,'supplemental':1,'benchmarks':len(refs),'status':'UNSELECTED'}))
if __name__=='__main__':main()
