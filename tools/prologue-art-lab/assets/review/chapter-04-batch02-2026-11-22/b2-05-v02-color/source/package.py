from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import shutil,json,hashlib,html
ROOT=Path(__file__).resolve().parents[1];OLD=ROOT.parent/'b2-05-v01';BASE='9afe76fe17dcb02633b82261a6c69457891da50f'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(rel):
 p=ROOT/rel;i=Image.open(p);return {'file':rel,'sha256':sha(p),'dimensions':list(i.size),'mode':i.mode}
def main():
 old=json.loads((OLD/'manifest.json').read_text());change=json.loads((ROOT/'evidence/targeted-change.json').read_text());assets=[]
 for name in ['approved-groom','approved-groundskeeper','approved-presenter','approved-lobby-background']:
  shutil.copyfile(OLD/f'references/{name}.png',ROOT/f'references/{name}.png');i=Image.open(ROOT/f'references/{name}.png');i.resize((i.width*4,i.height*4),Image.Resampling.NEAREST).save(ROOT/f'previews/{name}-4x.png')
 shutil.copyfile(OLD/'native/CH4-B2-27-v01.png',ROOT/'references/CH4-B2-27-v01.png');shutil.copyfile(OLD/'previews/CH4-B2-27-4x.png',ROOT/'previews/CH4-B2-27-v01-4x.png')
 font=ImageFont.load_default(size=14)
 for n in [26,28,29,30]:
  id_=f'CH4-B2-{n}';a=next(x for x in old['assets']if x['id']==id_).copy();shutil.copyfile(OLD/f'native/{id_}-v01.png',ROOT/f'references/{id_}-v01.png');shutil.copyfile(OLD/f'previews/{id_}-4x.png',ROOT/f'previews/{id_}-v01-4x.png');im=Image.open(ROOT/f'native/{id_}-v02.png');bg=Image.open(ROOT/'references/approved-lobby-background.png').convert('RGBA');comp=Image.alpha_composite(bg,im).convert('RGB');comp.save(ROOT/f'previews/{id_}-lobby-native.png');comp.resize((2256,1112),Image.Resampling.NEAREST).save(ROOT/f'previews/{id_}-lobby-4x.png')
  a.update({'version':'v02','native':rec(f'native/{id_}-v02.png'),'preview4x':rec(f'previews/{id_}-4x.png'),'base':rec(f'references/{id_}-v01.png'),'baseCommit':BASE,'detailedPoseReference':{'file':'../b2-05-v01/'+a['detailedReference']['file'],'sha256':a['detailedReference']['sha256']},'hairDirectionReference':rec('originals/bride-honey-blonde-direction-reference.png'),'processingSource':'source/recolor.py','hairMask':f'masks/{id_}-hair-only.png','hairLayer':f'layers/{id_}-blonde-hair.png','irisLayer':f'layers/{id_}-green-irises.png','irisMask':f'masks/{id_}-irises-only.png','allowedMask':f'masks/{id_}-allowed-hair-and-irises.png','composite':rec(f'previews/{id_}-lobby-native.png'),'prompt':'prompts/hair-color-direction.txt','derivation':'evidence/targeted-change.json'});a.pop('detailedReference',None);assets.append(a)
  sheet=Image.new('RGB',(1732,320),'#334b3e');d=ImageDraw.Draw(sheet)
  for x,title,rel in[(10,'v01 - preserved chestnut',f'references/{id_}-v01.png'),(586,'v02 - blonde hair / green eyes',f'native/{id_}-v02.png'),(1162,'Approved groom - unchanged dark brown','references/approved-groom.png')]:
   d.text((x,8),title,font=font,fill='#f1e1c4');i=Image.open(ROOT/rel).convert('RGBA');sheet.paste(i,(x,30),i)
  sheet.save(ROOT/f'comparisons/{id_}-v01-v02-groom-native.png');sheet.resize((6928,1280),Image.Resampling.NEAREST).save(ROOT/f'comparisons/{id_}-v01-v02-groom-4x.png')
 sheet=Image.new('RGB',(1160,930),'#334b3e');d=ImageDraw.Draw(sheet)
 for index,a in enumerate(assets+[{'title':'Approved groom - unchanged','native':{'file':'references/approved-groom.png'}}]):
  x=10+index%2*580;y=10+index//2*310;d.text((x,y),a['title'].replace('—','-'),font=font,fill='#f1e1c4');i=Image.open(ROOT/a['native']['file']).convert('RGBA');sheet.paste(i,(x,y+20),i)
 sheet.save(ROOT/'comparisons/all-native.png');sheet.resize((4640,3720),Image.Resampling.NEAREST).save(ROOT/'comparisons/all-4x.png')
 manifest={'title':'B2-05 v02 — bride honey-blonde hair and green eyes','status':'UNSELECTED','baseCommit':BASE,'canonicalApprovalBaseline':old['canonicalApprovalBaseline'],'groupId':'B2-05','revisedAssets':4,'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'approvedArtModified':False,'integrationPerformed':False,'assets':assets,'retainedClerk':{'id':'CH4-B2-27','version':'v01','status':'UNSELECTED','native':rec('references/CH4-B2-27-v01.png'),'sourceCommit':BASE},'canonicalBenchmarks':{k:v for k,v in old['canonicalBenchmarks'].items()if k in ['approved-groom','approved-groundskeeper','approved-presenter','approved-lobby-background']},'targetedChange':'evidence/targeted-change.json','priorHairOnlyStudy':{'commit':'97ccd2b8a0943374453c7a4a56af1868cb559c3f','directory':'tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/b2-05-v02-hair','preservedInGitHistory':True}};(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 def fig(title,one,four):
  w,h=Image.open(ROOT/one).size
  return f'<section class="figure"><h3>{html.escape(title)}</h3><nav><button data-scale="1">Native 1×</button><button data-scale="4">Exact 4×</button><a href="{one}">PNG</a><a href="{four}">4× PNG</a></nav><div class="raster"><img src="{one}" data-one="{one}" data-four="{four}" data-w="{w}" data-h="{h}" width="{w}" height="{h}" alt="{html.escape(title)}"></div></section>'
 style=(OLD/'index.html').read_text().split('<style>')[1].split('</style>')[0]
 body=''
 for a in assets:
  id_=a['id'];report=next(x for x in change['assets']if x['id']==id_);body+=f'<article id="{id_}"><h2>{id_} · {a["title"]} · v02</h2><p><strong>UNSELECTED</strong> · Honey-blonde hair and green eyes. {report["changedHairPixels"]} hair pixels and {report["changedIrisPixels"]} iris pixels changed; zero changes outside the allowed masks. Existing pupils, catchlights, eye whites, expression, hands, veil, gown, props, silhouette and alpha retained.</p><p><a href="comparisons/{id_}-v01-v02-groom-native.png">Direct before/after + groom PNG</a> · <a href="comparisons/{id_}-v01-v02-groom-4x.png">Exact 4× comparison</a> · <a href="masks/{id_}-allowed-hair-and-irises.png">Allowed color-change mask</a> · <a href="evidence/{id_}-changed-pixels.png">Changed pixels</a></p><p class="hash">SHA-256 {a["native"]["sha256"]}</p>'
  body+=fig('v02 blonde bride — green eyes',a['native']['file'],a['preview4x']['file'])+fig('Approved groom — unchanged','references/approved-groom.png','previews/approved-groom-4x.png')+fig('Previous v01 — unchanged',a['base']['file'],f'previews/{id_}-v01-4x.png')+fig('Approved Chapter 2 groundskeeper','references/approved-groundskeeper.png','previews/approved-groundskeeper-4x.png')+fig('Over unchanged approved lobby background',f'previews/{id_}-lobby-native.png',f'previews/{id_}-lobby-4x.png')+'</article>'
 header='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>B2-05 v02 — blonde bride with green eyes</title><style>'+style+'</style><main><header><h1>B2-05 v02 · Blonde hair and green eyes</h1><p><strong>Four UNSELECTED bride revisions.</strong> Nate requested a clearly different hair color and greener eyes than the groom. Honey blonde replaces chestnut, and green replaces brown iris rims within precise native masks. The updo, forehead curl, pupils, eye whites, catchlights, eyebrows, expression, ears/earrings, veil, gown, hands and ring/ribbon remain unchanged. Approved groom and all other approved art are untouched. The precise clerk remains the exact v01 candidate and unselected.</p><p>Imagegen supplied a hair-color direction reference only. Final edits are deterministic native palette substitutions with an eight-step honey-blonde ramp and three green iris tones; no generated face, pose or alpha pixels replace the existing native assets. Accurate source-derived provenance retained.</p><nav><a href="manifest.json">Manifest/hashes</a><a href="README.md">Method and original prompt</a><a href="evidence/targeted-change.json">Exact changes</a><a href="evidence/validation.json">Preservation QA</a><a href="comparisons/all-native.png">All four + groom — native PNG</a><a href="comparisons/all-4x.png">All four + groom — exact 4× PNG</a><a href="originals/bride-honey-blonde-direction-reference.png">Generated direction reference only</a></nav></header>'
 aside='<aside><h2>Preserved supporting candidates and references</h2>'+fig('Auction clerk — exact v01, still UNSELECTED','references/CH4-B2-27-v01.png','previews/CH4-B2-27-v01-4x.png')+fig('Approved Pavilion presenter','references/approved-presenter.png','previews/approved-presenter-4x.png')+'</aside>'
 script='<script>document.querySelectorAll("button[data-scale]").forEach(b=>b.onclick=()=>{const i=b.closest("section.figure").querySelector("img"),s=Number(b.dataset.scale);i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;});</script></main></html>'
 (ROOT/'index.html').write_text(header+body+aside+script)
 (ROOT/'README.md').write_text('''# B2-05 v02 — blonde bride with green eyes, targeted color revision

Four **UNSELECTED** revised bride portraits: determined, hopeful, grateful and helpful. Nate requested different hair color and greener eyes than the approved groom. Honey blonde and green irises are the new direction; the groom stays unchanged. The exact v01 clerk remains separate, unchanged and unselected. The initial hair-only edit is preserved at commit97ccd2b8a0943374453c7a4a56af1868cb559c3f; the current v02 combines both requested color changes.

## Exact scope

`source/recolor.py` starts from the four v01 PNGs at immutable review commit9afe76fe17dcb02633b82261a6c69457891da50f. Individually authored native hair silhouette polygons plus a warm-hair color predicate select only the existing hair clusters. Ear/earring exclusion boxes preserve anatomy. An eight-step honey-blonde ramp replaces chestnut shades, and a three-tone green ramp changes explicit iris-rim pixels. Original dark pupils, white/catchlight pixels, facial anatomy/brows/expression, transparency, silhouette, gown/veil, hands and props are preserved. No new shapes, texture, gradients or dithering. All pixels outside the final hair-and-iris masks are byte-identical; alpha is entirely unchanged. Exact source/final hashes and changed-pixel maps are retained.

Built-in `image_gen.imagegen` supplied the [hair-color direction reference](originals/bride-honey-blonde-direction-reference.png), [exact prompt](prompts/hair-color-direction.txt) and [receipt](evidence/imagegen-reference-receipt.json). That generated image is a palette guide only; its face, pose, background/alpha artifacts and canvas are not used in the final foregrounds. Original v01 detailed pose references and all earlier images remain preserved in the adjacent v01 package. Final artwork remains honestly **source-derived**, not independently authored whole-image native art.

[Gallery](index.html), [four revised brides beside approved groom](comparisons/all-native.png), [exact4×](comparisons/all-4x.png), [manifest](manifest.json), [exact scope](evidence/targeted-change.json), [QA](evidence/validation.json). Every pose includes v01/v02/groom comparison PNGs, exact4×, Chapter2 groundskeeper comparison and an unchanged-lobby-background composite. The approved Pavilion presenter remains a craft benchmark.

Reproduce with Pillow:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/recolor.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

No approval/selection registration, main, narrative, gameplay or engine integration changes. Every earlier approved image, historical review, groom PNG, clerk candidate and alternative plumber portrait remains unchanged. All four revisions stay UNSELECTED pending Nate.
''')
 print('Four blonde/green-eyed bride revisions and comparison gallery packaged.')
if __name__=='__main__':main()
