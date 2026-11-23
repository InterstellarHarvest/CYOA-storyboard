from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,subprocess,html
ROOT=Path(__file__).resolve().parents[1];REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists());CANON='8a5b91f4effabda5e6ebb5f53f317850931db68b';BASE='11d126e0856695ace519acffe442954dec936095'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(rel):
 p=ROOT/rel;i=Image.open(p);return {'file':rel,'sha256':sha(p),'dimensions':list(i.size),'mode':i.mode}
def safe(s):return html.escape(s,quote=True)
def main():
 invpath='tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21/v08/BATCH2-INVENTORY.json';inv=json.loads((REPO/invpath).read_text());group=next(g for g in inv['groups']if g['id']=='B2-05');nodes=json.loads(subprocess.check_output(['git','show',CANON+':story/chapters/chapter-04.wip.json'],cwd=REPO))['nodes'];assets=[]
 cases=[(26,'hotel_bride:determined','Bride — determined'),(27,'hotel_auction_clerk:precise','Auction clerk — precise'),(28,'hotel_bride:hopeful','Bride — hopeful'),(29,'hotel_bride:grateful','Bride — grateful'),(30,'hotel_bride:helpful','Bride — helpful')]
 for n,key,title in cases:
  id_=f'CH4-B2-{n}';demand=next(a for a in inv['assets']if a['inventoryId']=='portrait:'+key);nids=[k for k,v in nodes.items()if v.get('speaker','')+':'+v.get('pose','')==key];assert nids==demand['nodeIds'],(key,nids,demand['nodeIds']);im=Image.open(ROOT/f'native/{id_}-v01.png');bg=Image.open(ROOT/'references/approved-lobby-background.png').convert('RGBA');comp=Image.alpha_composite(bg,im).convert('RGB');comp.save(ROOT/f'previews/{id_}-lobby-native.png');comp.resize((2256,1112),Image.Resampling.NEAREST).save(ROOT/f'previews/{id_}-lobby-4x.png')
  assets.append({'id':id_,'title':title,'key':'portraits:'+key,'inventoryId':'portrait:'+key,'kind':'portrait','nodeIds':nids,'sceneKeys':['grand_bellevue/lobby'],'status':'UNSELECTED','selected':False,'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'native':rec(f'native/{id_}-v01.png'),'preview4x':rec(f'previews/{id_}-4x.png'),'detailedReference':rec(f'originals/{id_}-detailed.png'),'composite':rec(f'previews/{id_}-lobby-native.png'),'prompt':f'prompts/{id_}-detailed.txt','derivation':'evidence/derivation.json'})
 # Direct same-size approved Chapter2 and Pavilion comparisons for EACH portrait.
 for name in ['approved-groundskeeper','approved-attendant','approved-presenter','approved-bureau','approved-tower','approved-lobby-background']:
  im=Image.open(ROOT/f'references/{name}.png');im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/f'previews/{name}-4x.png')
 font=ImageFont.load_default(size=14)
 def label(d,xy,s):d.text(xy,s.replace('—','-'),fill='#efe2c7',font=font)
 for a in assets:
  sheet=Image.new('RGB',(1732,320),'#293e35');d=ImageDraw.Draw(sheet)
  for x,title,rel in [(10,a['title'],a['native']['file']),(586,'Approved Chapter 2 groundskeeper','references/approved-groundskeeper.png'),(1162,'Approved Pavilion presenter','references/approved-presenter.png')]:
   im=Image.open(ROOT/rel).convert('RGBA');label(d,(x,8),title);sheet.paste(im,(x,30),im)
  sheet.save(ROOT/f'comparisons/{a["id"]}-approved-native.png');sheet.resize((6928,1280),Image.Resampling.NEAREST).save(ROOT/f'comparisons/{a["id"]}-approved-4x.png')
 sheet=Image.new('RGB',(1160,930),'#30463c');d=ImageDraw.Draw(sheet)
 for i,a in enumerate(assets):
  x=10+i%2*580;y=10+i//2*310;label(d,(x,y),a['id']+' '+a['title']);im=Image.open(ROOT/a['native']['file']);sheet.paste(im,(x,y+20),im)
 sheet.save(ROOT/'comparisons/all-native.png');sheet.resize((4640,3720),Image.Resampling.NEAREST).save(ROOT/'comparisons/all-4x.png')
 manifest={'title':'Chapter 4 B2-05 v01 — Bride and auction clerk','groupId':'B2-05','status':'UNSELECTED','branch':'art/ch4-batch01-review-20261121','canonicalApprovalBaseline':CANON,'reviewPreservationBaseline':BASE,'inventorySource':invpath,'primaryUnits':5,'productionIntegrationPerformed':False,'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'assets':assets,'canonicalBenchmarks':json.loads((ROOT/'evidence/canonical-benchmarks.json').read_text()),'method':'Built-in imagegen character references matched to approved Pavilion portraits; source-derived native palette/cluster, semantic material-layer, rare-prop and silhouette cleanup following approved B2-04 portrait technique'};(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 (ROOT/'evidence/canonical-node-evidence.json').write_text(json.dumps({'canonicalCommit':CANON,'group':group,'nodes':{k:nodes[k]for k in group['nodeIds']},'storyFile':'story/chapters/chapter-04.wip.json','runtimeBindingsChanged':False},ensure_ascii=False,indent=2)+'\n')
 def figure(title,one,four):
  w,h=Image.open(ROOT/one).size
  return f'<section class="figure"><h3>{safe(title)}</h3><nav><button data-scale="1">Native 1×</button><button data-scale="4">Exact 4×</button><a href="{one}">PNG</a> <a href="{four}">4× PNG</a></nav><div class="raster"><img src="{one}" data-one="{one}" data-four="{four}" data-w="{w}" data-h="{h}" width="{w}" height="{h}" alt="{safe(title)}"></div></section>'
 body=''
 notes={'CH4-B2-26':'Determined, wry expression; empty conversational hand and hand at waist.','CH4-B2-27':'Precise clerk with red carbon-copy ticket pad and ordinary stamp; no invented wording.','CH4-B2-28':'Hopeful anticipation; the player still holds the ring, so her hands are empty.','CH4-B2-29':'Grateful after receiving the silver band and pale-blue ribbon; dedicated native material ramps protect these rare story colors.','CH4-B2-30':'Helpful directional gesture; no invented key or other prop.'}
 for a in assets:
  id_=a['id'];body+=f'<article id="{id_}"><h2>{id_} · {safe(a["title"])}</h2><p><strong>UNSELECTED</strong> · {notes[id_]} Native 564×278 RGBA.</p><p>Authored nodes: {safe(", ".join(a["nodeIds"]))}</p><p><a href="comparisons/{id_}-approved-native.png">Direct native comparison</a> · <a href="comparisons/{id_}-approved-4x.png">Direct exact 4× comparison</a> · <a href="{a["detailedReference"]["file"]}">Original detailed reference</a> · <a href="{a["prompt"]}">Exact prompt</a></p><p class="hash">SHA-256: {a["native"]["sha256"]}</p>'
  body+=figure('Candidate foreground',a['native']['file'],a['preview4x']['file'])+figure('Approved Chapter 2 groundskeeper','references/approved-groundskeeper.png','previews/approved-groundskeeper-4x.png')+figure('Approved Pavilion presenter','references/approved-presenter.png','previews/approved-presenter-4x.png')+figure('Over unchanged approved lobby background',f'previews/{id_}-lobby-native.png',f'previews/{id_}-lobby-4x.png')+'</article>'
 style='''<style>*{box-sizing:border-box}html{color-scheme:dark}body{margin:0;background:#17251f;color:#efe3c8;font:16px/1.6 system-ui}main{max-width:1900px;margin:auto;padding:24px}a{color:#b8d8c5}header,article,aside{padding:22px;border:1px solid #637868;background:#253c30;margin-bottom:24px}h1{font-size:30px}h2{font-size:24px}h3{font-size:18px}.figure{margin:18px 0;padding:15px;background:#344b3e;border:1px solid #677e6b}nav{display:flex;gap:12px;flex-wrap:wrap}button{font:inherit;background:#4e6955;color:#f5e9cf;border:1px solid #a6b59a;padding:7px 14px;cursor:pointer}.raster{overflow:auto;max-width:100%;padding:10px;background:repeating-conic-gradient(#3f5147 0% 25%,#34463c 0% 50%) 50%/16px 16px;margin-top:12px}img{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}.hash{overflow-wrap:anywhere;font:12px/1.6 monospace}@media(max-width:700px){main{padding:8px}article,header,aside{padding:12px}.figure{padding:8px}h1{font-size:24px}}</style>'''
 page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>B2-05 v01 — Bride and auction clerk</title>'+style+'<main><header><h1>Chapter 4 B2-05 v01 · Bride and auction clerk</h1><p><strong>Five UNSELECTED candidates pending Nate.</strong> Four consistent bride poses and the precise auction clerk, from the exact canonical B2-05 inventory. B2-04 registration is complete; all previous approved images and historical packages remain unchanged. The alternate plumber portraits remain separate and unselected.</p><p>Detailed built-in imagegen references matched to approved Pavilion NPCs, followed by source-derived native palette/cluster and silhouette construction. Native 564×278 foregrounds, binary transparency and exact nearest-neighbor 4× views. No independent whole-image native authorship claim. Native anatomy and rare ring/ribbon material regions are protected; no smooth gradients, added noise or blanket palette cap.</p><nav><a href="manifest.json">Manifest / hashes</a><a href="README.md">Method and reproduction</a><a href="evidence/validation.json">Technical and preservation QA</a><a href="evidence/visual-review.md">Visual assessment</a><a href="comparisons/all-native.png">All native PNG</a><a href="comparisons/all-4x.png">All exact 4× PNG</a><a href="evidence/canonical-node-evidence.json">Canonical story evidence</a></nav></header>'+body+'<aside><h2>Additional approved benchmarks</h2>'+figure('Approved Pavilion attendant','references/approved-attendant.png','previews/approved-attendant-4x.png')+figure('Approved Chapter 2 Bureau','references/approved-bureau.png','previews/approved-bureau-4x.png')+figure('Approved Chapter 2 Control Tower','references/approved-tower.png','previews/approved-tower-4x.png')+'</aside><script>document.querySelectorAll("button[data-scale]").forEach(b=>b.onclick=()=>{const i=b.closest("section.figure").querySelector("img"),s=Number(b.dataset.scale);i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;});</script></main></html>'
 (ROOT/'index.html').write_text(page)
 (ROOT/'README.md').write_text('''# Chapter 4 B2-05 v01 — Bride and auction clerk

Five **UNSELECTED** transparent portraits: bride determined / hopeful / grateful / helpful, plus the precise auction clerk. Exact canonical inventory and six authored nodes are preserved in [node evidence](evidence/canonical-node-evidence.json). No added dialogue, props, items, characters, story modes or runtime bindings. The approved lobby conversation background is reused byte-exact, never repainted.

## Production and provenance

Built-in `image_gen.imagegen` generated five detailed character references using approved Pavilion attendant/presenter artwork as the primary style inputs and the approved groom as local wardrobe context. The four bride poses retain one design. [Exact prompts](prompts/) and [generation receipts](evidence/generation-receipts.json) preserve all input references and saved originals. No external CLI/API generation fallback was used.

The high-resolution artwork is reference material. A direct native transfer is retained only as a diagnostic. Following the approved B2-04 portrait method, `source/native_build.py` constructs the 564×278 foreground through a local coherent palette fit, protected face/hand/prop regions, selective native low-contrast cluster merging, binary silhouette construction, detached-fragment removal, native contour fringe repair, zero hidden RGB and separate editable skin/hair/fabric/object masks and layers. Source colors are retained intelligently: broad material classification must not recolor anatomy, stipple faces or turn red tickets brown. Rare pale-blue ribbon and silver-band material ramps are explicitly preserved in the grateful pose. This is more than a resize or global color-count exercise; visual comparison remains the gate.

All exports are explicitly **SOURCE-DERIVED**, not independently authored whole-image native-grid artwork. Local 64-tone fitting follows the approved portrait studies, with extra rare-object material ramps where necessary. It is not a universal cap. No dithering, smooth gradient synthesis or random noise is added. [Exact derivation](evidence/derivation.json).

The bride's hopeful pose has no ring in her hands: the player still owns it. Grateful receives the silver ring and pale-blue ribbon. Helpful carries no key: the organizer holds it in the story. The male clerk holds the authored red carbon-copy ticket pad and ordinary stamp; paper contains non-letter form bars, not invented clue text. The actual inspection artwork and inventory images remain separate later groups.

Every candidate has direct native/exact4× comparisons with approved Chapter 2 groundskeeper and Pavilion presenter, plus a composite over the unchanged approved lobby background. Bureau, Control Tower and Pavilion attendant benchmarks are also preserved. Native exports are564×278 RGBA; exact4× exports2256×1112. [Gallery](index.html), [all native](comparisons/all-native.png), [manifest/hashes](manifest.json), [visual assessment](evidence/visual-review.md).

## Reproduce

Use the recorded Pillow version in `evidence/derivation.json`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/native_build.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

All B2-04 approvals and earlier artwork/history remain byte-exact. Main's B2-04 completion is8a5b91f4effabda5e6ebb5f53f317850931db68b, PR25, docs/132. Seven primary images are approved/selected; three supplemental states are approved/preserved conditional references only. No new Focus IDs or state bindings. Alternative B2-01 plumber portraits remain UNSELECTED; original v01 approvals stay selected. This review alters no canonical story file, selected image, narrative, gameplay or engine integration.
''')
 print('Five-portrait B2-05 gallery/comparisons/manifest packaged.')
if __name__=='__main__':main()
