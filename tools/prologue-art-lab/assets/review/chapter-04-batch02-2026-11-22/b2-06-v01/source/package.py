from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,subprocess,html
ROOT=Path(__file__).resolve().parents[1];REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists());CANON='f068f1005d313a3e2869f332398a97e2e4c772db';BASE='c6dbbaff7bf0edbda7a8ddff14556588c1eacd73'
CASES=[(31,'hotel_auctioneer:delighted','Auctioneer — delighted'),(32,'hotel_porter:alarmed','Porter — alarmed'),(33,'hotel_porter:curious','Porter — curious'),(34,'hotel_porter:relieved','Porter — relieved'),(35,'hotel_auctioneer:disappointed','Auctioneer — disappointed'),(36,'hotel_auctioneer:bureaucratic','Auctioneer — bureaucratic')]
BACKGROUNDS={'grand_bellevue/lobby':'approved-lobby-background','grand_bellevue/service_passage':'approved-service-background','grand_bellevue/boiler_access':'approved-boiler-background'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(rel):
 p=ROOT/rel;i=Image.open(p);return {'file':rel,'sha256':sha(p),'dimensions':list(i.size),'mode':i.mode}
def main():
 inventoryPath='tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21/v08/BATCH2-INVENTORY.json';inv=json.loads((REPO/inventoryPath).read_text());group=next(g for g in inv['groups']if g['id']=='B2-06');nodes=json.loads(subprocess.check_output(['git','show',CANON+':story/chapters/chapter-04.wip.json'],cwd=REPO))['nodes'];derivation=json.loads((ROOT/'evidence/derivation.json').read_text());assets=[]
 for num,key,title in CASES:
  id_=f'CH4-B2-{num}';demand=next(a for a in inv['assets']if a['inventoryId']=='portrait:'+key);ids=[n for n,v in nodes.items()if v.get('speaker','')+':'+v.get('pose','')==key];assert ids==demand['nodeIds'],key;im=Image.open(ROOT/f'native/{id_}-v01.png');primary=nodes[ids[0]]['scene'];comps={}
  for scene in demand['sceneKeys']:
   slug=scene.split('/')[-1];ref=BACKGROUNDS[scene];bg=Image.open(ROOT/f'references/{ref}.png').convert('RGBA');c=Image.alpha_composite(bg,im).convert('RGB');one=f'previews/{id_}-{slug}-native.png';four=f'previews/{id_}-{slug}-4x.png';c.save(ROOT/one);c.resize((2256,1112),Image.Resampling.NEAREST).save(ROOT/four);comps[scene]={'native':rec(one),'preview4x':rec(four),'backgroundReference':f'references/{ref}.png'}
  effective=next(a['sourceFile']for a in derivation['assets']if a['id']==id_);identity='approved-auctioneer'if num in[31,35,36]else'approved-porter';assets.append({'id':id_,'title':title,'version':'v01','key':'portraits:'+key,'inventoryId':'portrait:'+key,'kind':'portrait','nodeIds':ids,'sceneKeys':demand['sceneKeys'],'primaryScene':primary,'status':'UNSELECTED','selected':False,'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'native':rec(f'native/{id_}-v01.png'),'preview4x':rec(f'previews/{id_}-4x.png'),'detailedReference':rec(f'originals/{id_}-detailed.png'),'effectiveSource':rec(effective),'identityReference':f'references/{identity}.png','composites':comps,'composite':comps[primary]['native'],'prompt':f'prompts/{id_}-detailed.txt','processingSource':'source/native_build.py','derivation':'evidence/derivation.json'})
 refs=json.loads((ROOT/'evidence/canonical-benchmarks.json').read_text())
 for name in refs:
  im=Image.open(ROOT/f'references/{name}.png');im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/f'previews/{name}-4x.png')
 font=ImageFont.load_default(size=14)
 def sheetrow(size,items,out):
  s=Image.new('RGB',size,'#2d4439');d=ImageDraw.Draw(s)
  for x,title,file in items:
   d.text((x,8),title.replace('—','-'),font=font,fill='#eee0c4');im=Image.open(ROOT/file).convert('RGBA');s.paste(im,(x,30),im)
  s.save(ROOT/f'comparisons/{out}-native.png');s.resize((s.width*4,s.height*4),Image.Resampling.NEAREST).save(ROOT/f'comparisons/{out}-4x.png')
 for a in assets:
  id_=a['id'];sheetrow((1732,320),[(10,a['title'],a['native']['file']),(586,'Approved same-character identity',a['identityReference']),(1162,'Approved Pavilion presenter','references/approved-presenter.png')],id_+'-identity-pavilion')
  sheetrow((1232,320),[(10,a['title'],a['native']['file']),(586,'Chapter2 Bureau - native314x206','references/approved-bureau.png'),(910,'Chapter2 Tower - native314x206','references/approved-tower.png')],id_+'-chapter2')
 s=Image.new('RGB',(1160,930),'#30463c');d=ImageDraw.Draw(s)
 for i,a in enumerate(assets):
  x=10+i%2*580;y=10+i//2*310;d.text((x,y),a['id']+' '+a['title'].replace('—','-'),font=font,fill='#eee0c4');im=Image.open(ROOT/a['native']['file']);s.paste(im,(x,y+20),im)
 s.save(ROOT/'comparisons/all-native.png');s.resize((4640,3720),Image.Resampling.NEAREST).save(ROOT/'comparisons/all-4x.png')
 m={'title':'Chapter4 B2-06 v01 — Auctioneer and porter expression extensions','groupId':'B2-06','status':'UNSELECTED','branch':'art/ch4-batch01-review-20261121','canonicalApprovalBaseline':CANON,'reviewPreservationBaseline':BASE,'inventorySource':inventoryPath,'primaryUnits':6,'storyNodeCoverage':group['nodeIds'],'productionIntegrationPerformed':False,'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'assets':assets,'canonicalBenchmarks':refs,'method':'Built-in imagegen detailed references preserving approved identities, followed by native opaque-only palette fit, protected cluster/silhouette/fringe cleanup and editable material layers'};(ROOT/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 (ROOT/'evidence/canonical-node-evidence.json').write_text(json.dumps({'canonicalCommit':CANON,'group':group,'storyFile':'story/chapters/chapter-04.wip.json','nodes':{k:nodes[k]for k in group['nodeIds']},'runtimeBindingsChanged':False},ensure_ascii=False,indent=2)+'\n')
 def fig(title,one,four):
  w,h=Image.open(ROOT/one).size
  return f'<section class="figure"><h3>{html.escape(title)}</h3><nav><button data-scale="1">Native 1×</button><button data-scale="4">Exact 4×</button><a href="{one}">PNG</a><a href="{four}">4× PNG</a></nav><div class="raster"><img src="{one}" data-one="{one}" data-four="{four}" data-w="{w}" data-h="{h}" width="{w}" height="{h}" alt="{html.escape(title)}"></div></section>'
 style=(ROOT.parent/'b2-05-v01/index.html').read_text().split('<style>')[1].split('</style>')[0];body='';notes={31:'Bright but restrained showman smile; familiar gavel and open conversational hand.',32:'Raised stop hand and alert expression; complete cap, clipboard and both hands.',33:'Questioning head tilt and pencil/clipboard gesture; no invented pass or lettering.',34:'Softened smile and relieved chest gesture; unwanted source halo removed before native construction.',35:'Subtle downturned expression and lowered gavel; dignity and established age retained.',36:'Matter-of-fact skeptical face and measured explanatory gesture; no invented form or stamp text.'}
 for a in assets:
  id_=a['id'];num=int(id_.split('-')[-1]);identity=a['identityReference'].split('/')[-1][:-4];body+=f'<article id="{id_}"><h2>{id_} · {a["title"]}</h2><p><strong>UNSELECTED</strong> · {notes[num]} Native 564×278 transparent foreground.</p><p>Authored nodes: {html.escape(", ".join(a["nodeIds"]))}</p><p><a href="comparisons/{id_}-identity-pavilion-native.png">Identity/Pavilion comparison PNG</a> · <a href="comparisons/{id_}-identity-pavilion-4x.png">Exact 4×</a> · <a href="comparisons/{id_}-chapter2-native.png">Chapter2 comparison PNG</a> · <a href="comparisons/{id_}-chapter2-4x.png">Chapter2 exact 4×</a> · <a href="{a["effectiveSource"]["file"]}">Detailed source used</a> · <a href="{a["prompt"]}">Exact prompt</a></p><p class="hash">SHA-256 {a["native"]["sha256"]}</p>'
  body+=fig('New candidate foreground',a['native']['file'],a['preview4x']['file'])+fig('Approved same-character identity',a['identityReference'],f'previews/{identity}-4x.png')+fig('Approved Chapter3 Pavilion presenter','references/approved-presenter.png','previews/approved-presenter-4x.png')+fig('Approved Chapter2 Bureau — pixel-cluster/material benchmark','references/approved-bureau.png','previews/approved-bureau-4x.png')
  for scene,c in a['composites'].items():body+=fig('Over unchanged approved '+scene.split('/')[-1]+' background',c['native']['file'],c['preview4x']['file'])
  body+='</article>'
 header='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>B2-06 v01 — Auctioneer and porter expressions</title><style>'+style+'</style><main><header><h1>Chapter4 B2-06 v01 · Auctioneer and porter expressions</h1><p><strong>Six UNSELECTED candidates pending Nate.</strong> Exact canonical inventory: auctioneer delighted/disappointed/bureaucratic; porter alarmed/curious/relieved. Existing approved identities, costume and props are retained. All previous approvals, including the newly selected blonde/green-eyed bride and original precise clerk, remain exact.</p><p>Detailed built-in imagegen references followed by source-derived native palette/cluster/silhouette construction. Native 564×278 transparent foregrounds, exact nearest-neighbor 4×, direct approved Chapter2/3 comparisons and approved-context composites. No independent whole-image native authorship claim; palette counts are diagnostics, not visual approval.</p><nav><a href="manifest.json">Manifest/hashes</a><a href="README.md">Sources, prompts and method</a><a href="evidence/validation.json">Preservation/technical QA</a><a href="evidence/visual-review.md">Visual assessment</a><a href="comparisons/all-native.png">All six native PNG</a><a href="comparisons/all-4x.png">All six exact 4× PNG</a><a href="evidence/canonical-node-evidence.json">Canonical story evidence</a></nav></header>'
 aside='<aside><h2>Additional approved references</h2>'+fig('Approved Chapter3 Pavilion attendant','references/approved-attendant.png','previews/approved-attendant-4x.png')+fig('Approved Chapter2 Control Tower','references/approved-tower.png','previews/approved-tower-4x.png')+fig('Approved porter — practical','references/approved-porter-practical.png','previews/approved-porter-practical-4x.png')+'</aside>'
 script='<script>document.querySelectorAll("button[data-scale]").forEach(b=>b.onclick=()=>{const i=b.closest("section.figure").querySelector("img"),s=Number(b.dataset.scale);i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;});</script></main></html>'
 (ROOT/'index.html').write_text(header+body+aside+script)
 (ROOT/'README.md').write_text('''# Chapter4 B2-06 v01 — Auctioneer and porter expression extensions

Six **UNSELECTED** transparent portrait foregrounds from the exact canonical B2-06 inventory: CH4-B2-31 auctioneer delighted;32 porter alarmed;33 porter curious;34 porter relieved;35 auctioneer disappointed;36 auctioneer bureaucratic. Eight authored nodes, no invented keys, dialogue or story requirements. [Canonical evidence](evidence/canonical-node-evidence.json), [manifest/hashes](manifest.json), [gallery](index.html), [all native](comparisons/all-native.png), [all exact4×](comparisons/all-4x.png).

## Actual production and provenance

Built-in `image_gen.imagegen` generated six detailed portrait references using the exact approved auctioneer/porter identities and approved Pavilion attendant/presenter as human anatomy/clothing benchmarks. A seventh built-in background-extraction edit corrected an unwanted gray halo in the relieved porter reference. Original first source, corrected cutout, exact prompts, input references and generation receipts are all preserved. No CLI/API fallback was used.

The high-resolution artwork is reference material, not a finished native asset. The native recipe fits a coherent local palette using **only opaque character colors**, so invisible background RGB cannot consume detail colors. It constructs a target-grid binary silhouette, removes detached fragments, merges tiny low-contrast surface islands, preserves coherent facial/hand features and material edges, repairs colored boundary fringe, clears hidden RGB and exports separate editable material masks/layers. A selective warm-plane pass quiets isolated skin/hand shade flecks without smoothing coherent wrinkles, dark pupils/brows/creases or white catchlights. Source transfer diagnostics are retained as diagnostics only. This follows the approved B2-04/B2-05 portrait approach, not a new simplified coordinate-drawn figure or broad procedural lighting pass.

Every new image is explicitly **SOURCE-DERIVED**, not independently authored whole-image native-grid artwork. Local64-tone fitting is a portrait production choice calibrated to approved work, never a universal cap or proof of artistic readiness. No dithering, random texture, smooth generated gradients or arbitrary global palette rule is introduced. [Exact derivation and native decisions](evidence/derivation.json), [source recipe](source/native_build.py), [prompts](prompts/), [generation receipts](evidence/generation-receipts.json).

## Identity, context and visual checks

The auctioneer retains normally proportioned elderly anatomy, silver hair/mustache, expressive brows, burgundy formalwear, dark lapels, bow tie, pocket square, gavel and both hands. Expressions remain restrained and recognizable. The porter retains his approved face, gray cap/jacket, open-neck cream shirt, clipboard and pencil; all caps, hands and gestures remain inside the frame. The clipboard uses non-letter ruled bars, not invented readable clues. No ring, staff pass, tag, new document wording or extra character is added.

Auctioneer poses composite over the exact approved lobby portrait background. Curious/relieved porter use the approved service passage. Alarmed porter includes both existing authored lobby and boiler-access contexts. These are review composites, not new backgrounds or runtime bindings. Approved Chapter3 human portraits establish anatomy/costume finish; Chapter2 Bureau/Control Tower establish deliberate cluster/material/light craft. Every candidate includes direct native/exact4× comparisons with both chapters at their actual grids, plus same-identity comparisons. [Visual assessment](evidence/visual-review.md). Technical dimensions/color counts do not establish owner approval.

## Reproduce

Use the Python/Pillow versions recorded in derivation.json:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/native_build.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

B2-05 is APPROVED/SELECTED unchanged on canonical main f068f1005d313a3e2869f332398a97e2e4c772db, PR26, docs/133: four blonde/green-eyed bride v02 PNGs and original clerk v01. All35 prior approved primary Chapter4 images, three conditional B2-04 references, all earlier approvals/reviews and unselected plumber alternatives remain unchanged. No narrative, gameplay, canonical registry, production assetPath or engine integration changes. New B2-06 candidates stay UNSELECTED pending Nate.
''');print('Six-portrait B2-06 gallery and canonical comparisons packaged.')
if __name__=='__main__':main()
