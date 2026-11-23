from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];OLD=ROOT.parent/'b2-02-v02-pixel'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(rel):
 p=ROOT/rel;im=Image.open(p);return {'file':rel,'sha256':sha(p),'dimensions':list(im.size),'mode':im.mode}
def main():
 for n in['references','comparisons','previews','evidence']:(ROOT/n).mkdir(exist_ok=True)
 for src,dst in[(OLD/'native/CH4-B2-09-v02.png','references/CH4-B2-09-v02.png'),(OLD/'previews/CH4-B2-09-4x.png','previews/CH4-B2-09-v02-4x.png'),(OLD/'references/detailed/CH4-B2-09-reference.png','references/CH4-B2-09-detailed-reference.png'),(OLD/'references/approved-bureau.png','references/approved-bureau.png'),(OLD/'previews/approved-bureau-4x.png','previews/approved-bureau-4x.png')]:shutil.copyfile(src,ROOT/dst)
 before=Image.open(ROOT/'references/CH4-B2-09-v02.png');after=Image.open(ROOT/'native/CH4-B2-09-v03.png');region=(145,84,185,143)
 for name,im in[('v02',before),('v03',after)]:
  crop=im.crop(region);crop.save(ROOT/f'previews/cake-{name}-native.png');crop.resize((crop.width*4,crop.height*4),Image.Resampling.NEAREST).save(ROOT/f'previews/cake-{name}-4x.png')
 ref=Image.open(ROOT/'references/CH4-B2-09-detailed-reference.png');ref.crop((round(region[0]*ref.width/314),round(region[1]*ref.height/206),round(region[2]*ref.width/314),round(region[3]*ref.height/206))).save(ROOT/'references/detailed-cake-crop.png')
 sheet=Image.new('RGB',(676,250),'#22362d');d=ImageDraw.Draw(sheet)
 for x,label,im in[(12,'B2-09 v02 - preserved',before),(350,'B2-09 v03 - cake restored',after)]:d.text((x,10),label,font=ImageFont.load_default(size=14),fill='#f3e3c4');sheet.paste(im,(x,34))
 sheet.save(ROOT/'comparisons/B2-09-v02-v03-native.png');sheet.resize((2704,1000),Image.Resampling.NEAREST).save(ROOT/'comparisons/B2-09-v02-v03-4x.png')
 change=json.loads((ROOT/'evidence/targeted-change.json').read_text())
 manifest={'title':'B2-09 Service Stairs v03 - targeted wedding-cake/trolley restoration','status':'UNSELECTED','assetId':'CH4-B2-09','key':'scenes:grand_bellevue/service_stairs','nodeIds':['hotel_maintenance_dock_exit'],'baseCommit':'62ef2059585de49292bbec2742d3c637d2eae818','base':rec('references/CH4-B2-09-v02.png'),'native':rec('native/CH4-B2-09-v03.png'),'preview4x':rec('previews/CH4-B2-09-v03-4x.png'),'originalDetailedReference':rec('references/CH4-B2-09-detailed-reference.png'),'sourceDerived':True,'method':'Targeted native restoration/painting from existing editable material/structural layers; no new generated artwork or whole-scene rerender','changedPixels':change['changedPixels'],'changedBounds':change['changedBounds'],'outsideProtectedObjectChanges':0,'paletteChanged':False,'otherScenesModified':False,'formalApprovalRegistered':False,'integrationPerformed':False,'processingSource':'source/restore.py','scopeEvidence':'evidence/targeted-change.json','frozenSiblings':'evidence/frozen-siblings.json'}
 (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 def card(id_,title,one,four,note):
  im=Image.open(ROOT/one);w,h=im.size
  return f'<article id="{id_}"><h2>{title}</h2><p>{note}</p><div class="controls"><button data-scale="1">Native 1×</button><button data-scale="4">Exact 4×</button><a href="{one}">PNG</a> · <a href="{four}">4× PNG</a></div><div class="strip"><img class="art" src="{one}" data-one="{one}" data-four="{four}" data-w="{w}" data-h="{h}" width="{w}" height="{h}" alt="{title}"></div></article>'
 cards=card('current','B2-09 v03 - restored cake and trolley','native/CH4-B2-09-v03.png','previews/CH4-B2-09-v03-4x.png','UNSELECTED. Same 314×206 scene and existing 64-color palette. Only the protected cake/trolley silhouette changes.')+card('previous','Preserved B2-09 v02','references/CH4-B2-09-v02.png','previews/CH4-B2-09-v02-4x.png','Unchanged historical candidate; the elevator paint obscured the upper cake tiers.')+card('crop-current','v03 cake/trolley crop','previews/cake-v03-native.png','previews/cake-v03-4x.png','Exact native crop; same pixels as the full scene, shown at 1× or exact 4×.')+card('crop-previous','v02 crop','previews/cake-v02-native.png','previews/cake-v02-4x.png','Compare the tier silhouette, flowers, icing, trolley cloth/frame and visible casters.')+card('difference','Changed-pixel map','evidence/changed-pixels.png','evidence/changed-pixels-4x.png','Gold marks the 723 changed pixels. Zero changes outside the complete protected object mask; foreground hand unchanged.')+card('canonical','Approved Chapter 2 Bureau - craft benchmark','references/approved-bureau.png','previews/approved-bureau-4x.png','Approved canonical reference, exact bytes preserved. Material ramps and deliberate native clusters remain the visual standard.')
 style='''<style>*{box-sizing:border-box}html{color-scheme:dark}body{margin:0;background:#172824;color:#eddfc1;font:16px/1.55 system-ui}main{max-width:1200px;padding:24px;margin:auto}a{color:#c0e1cb}h1{font-size:29px}h2{font-size:21px}article,section{background:#22362d;padding:18px;margin:22px 0;border:1px solid #5f715e;min-width:0}.controls,nav{display:flex;gap:12px;flex-wrap:wrap;align-items:center}button{font:inherit;padding:8px 14px;background:#405b49;color:#f3e7cb;border:1px solid #8fa386;cursor:pointer}.strip{overflow:auto;max-width:100%;padding:10px;background:#11231c;margin-top:12px}img.art{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}code{font-size:12px;overflow-wrap:anywhere}@media(max-width:600px){main{padding:10px}article,section{padding:10px}h1{font-size:23px}}</style>'''
 header='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>B2-09 v03 targeted cake restoration</title>'''+style+'''<main><header><h1>B2-09 v03 · wedding cake and trolley restoration</h1><p><strong>UNSELECTED - B2-09 only</strong></p><p>One targeted native correction. B2-06, B2-07 and B2-08 remain their exact v02 files and are not registered approved/selected. All approved art and historical reviews remain unchanged.</p></header><nav><a href="manifest.json">Manifest/hash</a><a href="README.md">Method</a><a href="evidence/targeted-change.json">Exact changed region</a><a href="evidence/validation.json">QA</a><a href="evidence/story-object-audit.json">Story-object audit</a><a href="comparisons/B2-09-v02-v03-native.png">Direct comparison PNG</a><a href="comparisons/B2-09-v02-v03-4x.png">Exact 4× comparison PNG</a><a href="references/CH4-B2-09-detailed-reference.png">Preserved detailed reference</a><a href="references/detailed-cake-crop.png">Original reference cake/trolley crop</a></nav><section><h2>Correction and preservation</h2><p>The v02 object mask missed the upper tiers and some trolley pixels. Elevator-panel and floor/structure paint covered them. The new full silhouette clips that structural paint, restores the existing material underpainting and refines the tiers, icing, bouquet, trolley frame and casters on the native grid. The foreground mover’s hand stays in front.</p><p>No generation, group rerender, global palette conversion, architecture/light changes or new colors. The 723 changed pixels are confined to the object, within x152–183/y88–140. Exact 64-color palette retained. Native 314×206 and exact 1256×824 preview.</p><p>Structural/material passes must protect every complete story-object silhouette, including tops, overhangs, handles and wheels. A source-to-final object audit supplements file/scale checks. Technical success does not approve the image.</p></section>'''
 script='''<script>document.querySelectorAll('button[data-scale]').forEach(b=>b.addEventListener('click',()=>{const i=b.closest('article').querySelector('img'),s=Number(b.dataset.scale);i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;}));</script></main></html>'''
 (ROOT/'index.html').write_text(header+cards+script)
 (ROOT/'README.md').write_text('''# B2-09 v03 — targeted wedding-cake/trolley correction

**UNSELECTED.** Only B2-09 changes. The owner called B2-06/07/08 selection-ready and requested exact preservation; this is not approval/selection registration. [Frozen sibling hashes](evidence/frozen-siblings.json). All ten approved Chapter 4 assets and every previous candidate remain unchanged.

## Method and cause

The existing native material/structure source is editable. The v02 cake silhouette was incomplete; the elevator-panel drawing also failed to respect object occlusion. Upper tiers disappeared, with some cart/frame/caster encroachment from structural/floor painting. This correction reads those frozen native layers, masks the structural layer with the complete cake/trolley silhouette, restores material pixels and paints a small native layer with rounded tiers, warm side planes, flowers/piping, frame and casters. The foreground mover/hand is protected.

No built-in imagegen call, regeneration or whole-group rerender is needed for this existing native-layer edit. No palette conversion or new color is introduced. The result remains **source-derived** through its original reference/native construction provenance. It is not claimed independently authored as a complete new native scene.

[Native comparison](comparisons/B2-09-v02-v03-native.png), [exact4x comparison](comparisons/B2-09-v02-v03-4x.png), [gallery](index.html), [changed pixels](evidence/changed-pixels-4x.png), [exact scope](evidence/targeted-change.json). Only 723 pixels change, all within the protected object mask; every other v02 pixel and the existing palette remain exact. Original detailed reference and crop are preserved for visual inspection. Dimensions 314×206 opaque; exact 4× 1256×824.

## Repeatable safeguard

Story-object protection must clip ALL later structural paint, including wall/elevator geometry and floor/grout passes. Masks must include the whole silhouette: upper tiers/flowers, handles, cloth edges, frame and wheels. Check protected masks against source objects and inspect native/exact4x before publication; hashes/color counts alone cannot detect a lost story object. [Audit](evidence/story-object-audit.json). The four-scene technique is retained; no other scene is rerun here.

Reproduce with the recorded Pillow version:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/restore.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

`source/restore.py` is the exact native edit recipe; no new image-generation prompt exists. Source native/layer/reference inputs are pinned to 62ef2059585de49292bbec2742d3c637d2eae818 and preserved historical files. The targeted object layer, protected mask, clipped structural layer, source palette restriction and before/after previews are included. No narrative, gameplay, production integration, main or approval-record changes.
''')
 print('Small B2-09-only review packaged.')
if __name__=='__main__':main()
