from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil,html
ROOT=Path(__file__).resolve().parents[1];OLD=ROOT.parent/'b2-02-v01';REPO=next(p for p in ROOT.parents if (p/'story/artwork.draft.json').exists())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(rel):
 p=ROOT/rel;im=Image.open(p);return {'file':rel,'sha256':sha(p),'dimensions':list(im.size),'mode':im.mode}
def main():
 for n in['references','references/detailed','references/v01','previews','comparisons']:(ROOT/n).mkdir(parents=True,exist_ok=True)
 old=json.loads((OLD/'manifest.json').read_text());reports=json.loads((ROOT/'evidence/native-reconstruction.json').read_text());assets=[]
 for a in old['assets'][:4]:
  id_=a['id'];source=OLD/'originals'/(id_+('-worker-corrected.png'if id_.endswith('07')else'-workers-corrected.png'if id_.endswith('08')else'-original.png'));shutil.copyfile(source,ROOT/f'references/detailed/{id_}-reference.png');shutil.copyfile(OLD/a['native']['file'],ROOT/f'references/v01/{id_}-v01.png');shutil.copyfile(OLD/a['preview4x']['file'],ROOT/f'previews/{id_}-v01-4x.png')
  assets.append({'id':id_,'title':a['title'],'key':a['key'],'nodeIds':a['nodeIds'],'status':'UNSELECTED','selected':False,'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'native':rec(f'native/{id_}-v02.png'),'preview4x':rec(f'previews/{id_}-4x.png'),'previousNative':rec(f'references/v01/{id_}-v01.png'),'detailedReference':rec(f'references/detailed/{id_}-reference.png'),'pixelFriendlySource':rec(f'originals/{id_}-pixel-friendly.png'),'directTransferDiagnostic':rec(f'diagnostics/{id_}-direct-transfer-diagnostic.png'),'nativeLayers':[str(p.relative_to(ROOT))for p in sorted((ROOT/'layers').glob(id_+'*.png'))],'nativeMasks':[str(p.relative_to(ROOT))for p in sorted((ROOT/'masks').glob(id_+'*.png'))]})
 for name in ['approved-bureau','approved-tower','approved-lobby','approved-restroom']:
  shutil.copyfile(OLD/'references'/(name+'.png'),ROOT/'references'/(name+'.png'));im=Image.open(ROOT/'references'/(name+'.png'));im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/'previews'/(name+'-4x.png'))
 retained=[]
 for a in old['assets'][4:]:
  shutil.copyfile(OLD/a['native']['file'],ROOT/'references'/(a['id']+'-retained-v01.png'));shutil.copyfile(OLD/a['preview4x']['file'],ROOT/'previews'/(a['id']+'-retained-v01-4x.png'));retained.append({'id':a['id'],'status':'UNSELECTED','role':'Retained v01 candidate, not revised in this four-main-scene pass','native':rec('references/'+a['id']+'-retained-v01.png'),'preview4x':rec('previews/'+a['id']+'-retained-v01-4x.png'),'originalPath':'../b2-02-v01/'+a['native']['file']})
 def sheet(name,rows):
  cols=max(len(row)for row in rows);im=Image.new('RGB',(338*cols,242*len(rows)),'#22372f');d=ImageDraw.Draw(im)
  for y,row in enumerate(rows):
   for x,(label,rel)in enumerate(row):
    xx=x*338+12;yy=y*242+10;d.text((xx,yy),label,font=ImageFont.load_default(size=13),fill='#ecdfc1');art=Image.open(ROOT/rel).convert('RGB');assert art.size==(314,206);im.paste(art,(xx,yy+24))
  im.save(ROOT/'comparisons'/(name+'-native.png'));im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/'comparisons'/(name+'-4x.png'))
 sheet('v01-v02',[[('Preserved v01 '+a['title'],a['previousNative']['file']),('Native v02 '+a['title'],a['native']['file'])]for a in assets])
 sheet('canonical',[[('v02 Loading Dock',assets[2]['native']['file']),('Chapter2 Control Tower','references/approved-tower.png')],[('v02 Service Stairs',assets[3]['native']['file']),('Chapter2 Bureau','references/approved-bureau.png')],[('v02 Loading Lane',assets[0]['native']['file']),('Chapter4 approved lobby','references/approved-lobby.png')],[('v02 Service Alley',assets[1]['native']['file']),('Chapter2 Bureau','references/approved-bureau.png')]])
 sheet('native-construction',[[('Transfer diagnostic ONLY',a['directTransferDiagnostic']['file']),('Material underpainting','layers/'+a['id']+'-material-underpainting.png'),('Final native construction',a['native']['file'])]for a in assets])
 manifest={'title':'B2-02 v02 - four-scene native pixel-art reinterpretation','status':'UNSELECTED','branch':'art/ch4-batch01-review-20261121','standardCommit':'cc2afd6def0bc41d9a193456eff95d2ce3cb488a','standard':'docs/129_PERMANENT_PIXEL_ART_PRODUCTION_STANDARD_20261122.md','previousReviewCommit':'b3abaae4238b87bdc27f444637b83a2c549838f9','sourceDerived':True,'pipeline':'Detailed reference -> separate pixel-friendly source -> diagnostic native transfer -> semantic material masks/ramps and selected cluster reconstruction -> native geometry/light-plane/object-edge painting -> isolated native region layers -> exact4x','paletteCountsAreDiagnosticOnly':True,'assets':assets,'retainedCandidates':retained,'narrativeOrGameplayChanged':False,'approvedAssetsModified':False}
 (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 def card(label,one,four,note='',id_=''):
  art=Image.open(ROOT/one);w,h=art.size;return f'<article id="{id_}"><h2>{html.escape(label)}</h2><p>{note}</p><div class="controls"><button data-scale="1">Native1x</button><button data-scale="4">Exact4x</button><a href="{one}">PNG</a> · <a href="{four}">4x PNG</a></div><div class="strip"><img class="art" src="{one}" data-one="{one}" data-four="{four}" data-w="{w}" data-h="{h}" width="{w}" height="{h}" alt="{html.escape(label)}"></div></article>'
 cards=[]
 for a in assets:
  note='<strong>UNSELECTED</strong> · 314x206 opaque · source-derived native reconstruction<br>Canonical <code>'+a['key']+'</code><br>SHA256 <code>'+a['native']['sha256']+'</code><br><a href="'+a['detailedReference']['file']+'">Original detailed reference</a> · <a href="'+a['pixelFriendlySource']['file']+'">Separate pixel-friendly source</a> · <a href="'+a['directTransferDiagnostic']['file']+'">Transfer diagnostic, not a candidate</a>'
  cards.append(card('v02 '+a['title'],a['native']['file'],a['preview4x']['file'],note,a['id']))
 for a in assets:cards.append(card('Preserved v01 '+a['title'],a['previousNative']['file'],'previews/'+a['id']+'-v01-4x.png','Historical candidate unchanged; this is the earlier reduced-illustration treatment.'))
 for name,title in [('approved-bureau','Approved Chapter2 Bureau'),('approved-tower','Approved Chapter2 Control Tower'),('approved-lobby','Approved Chapter4 lobby'),('approved-restroom','Approved Chapter4 restroom')]:cards.append(card(title,'references/'+name+'.png','previews/'+name+'-4x.png','Canonical comparison reference, exact bytes preserved.'))
 for a in retained:cards.append(card(a['id']+' - retained v01 candidate',a['native']['file'],a['preview4x']['file'],'<strong>UNSELECTED</strong>. Retained without cosmetic revision; not represented as a newly approved asset.'))
 style='''<style>*{box-sizing:border-box}html{color-scheme:dark}body{margin:0;background:#172824;color:#ecdfc1;font:16px/1.55 system-ui}main{max-width:1320px;padding:24px;margin:auto}a{color:#bfdfc9}h1{font-size:29px}h2{font-size:21px}article,section{margin:22px 0;padding:18px;background:#22372f;border:1px solid #5a705c;min-width:0}button{font:inherit;padding:8px 14px;color:#f3e7cc;background:#405b49;border:1px solid #8ca286;cursor:pointer}.controls,nav{display:flex;flex-wrap:wrap;gap:12px;align-items:center}.strip{overflow:auto;max-width:100%;padding:10px;background:#11221c;margin-top:12px}img.art{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}code{font-size:12px;overflow-wrap:anywhere}@media(max-width:600px){main{padding:10px}article,section{padding:10px}h1{font-size:23px}}</style>'''
 header='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>B2-02 v02 native pixel-art reinterpretation</title>'''+style+'''<main><header><h1>Chapter4 B2-02 v02 · native pixel-art reinterpretation</h1><p><strong>Four revised main scenes - UNSELECTED</strong></p><p>Chapter2 supplies the pixel-cluster craft benchmark. The preserved detailed sources supply composition, perspective, materials, light and story ambition. Both matter. The final314x206 images are built through separate pixel-friendly interpretations, semantic material/occlusion masks, selected cluster cleanup and native architecture/light-plane/object-edge painting. A direct transfer is retained only as a diagnostic.</p></header><nav><a href="manifest.json">Manifest/hashes</a><a href="README.md">Method and limits</a><a href="evidence/native-reconstruction.json">Native guides/layers</a><a href="evidence/palette-diagnostics.json">Palette/cluster diagnostics</a><a href="evidence/visual-qa.json">Visual comparison notes</a><a href="evidence/validation.json">Technical QA</a><a href="comparisons/v01-v02-native.png">v01/v02 PNG</a><a href="comparisons/v01-v02-4x.png">v01/v02 exact4x</a><a href="comparisons/canonical-native.png">Canonical comparison PNG</a><a href="comparisons/canonical-4x.png">Canonical exact4x</a><a href="comparisons/native-construction-native.png">Native construction stages</a></nav><section><h2>What to inspect</h2><p>Judge native size first, then exact4x: intentional clusters and stable edges; readable architecture/objects; distinct plaster, wood, velvet, steel, piano and stone; stepped light/shadow; simple scene-NPC silhouettes. Color counts and passing file checks do not establish visual approval.</p><p>Dock and stairs established the treatment first. The four layouts retain the shipping staircase, sofa/trolley, chandelier hoist/padded crate, two piano workers plus foreman, cake trolley and door/stair geometry. Floor perspective and light/shadow regions are constructed on the final grid, not copied photographic grain. Material masks and individual NPC-region layers are saved for targeted revision.</p><p>The foreman and portrait background remain their exact v01 files, shown below as retained UNSELECTED candidates; this pass does not flatten them to main-scene detail. Approved B2-01 v01 artwork and the two separate plumber palette alternatives are unchanged. No narrative, gameplay, approval registration or engine integration changes.</p><p><a href="https://github.com/InterstellarHarvest/CYOA-storyboard/blob/cc2afd6def0bc41d9a193456eff95d2ce3cb488a/docs/129_PERMANENT_PIXEL_ART_PRODUCTION_STANDARD_20261122.md">Permanent owner standard and artwork hierarchy</a> (canonical main, PR22).</p></section>'''
 script='''<script>document.querySelectorAll('button[data-scale]').forEach(b=>b.addEventListener('click',()=>{const i=b.closest('article').querySelector('img'),s=Number(b.dataset.scale);i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;}));</script></main></html>'''
 (ROOT/'index.html').write_text(header+''.join(cards)+script)
 (ROOT/'README.md').write_text('''# B2-02 v02 — four-scene native pixel-art reinterpretation

All four revisions are **UNSELECTED**. This follows Nate's permanent standard and final hierarchy in canonical docs129/PR22. Main scenes314x206; portraits/backgrounds and Focus564x278 retain their own richer detail requirements. No universal palette-count target is imposed.

## Actual production method

1. Preserve the original detailed concepts and all historical native PNGs unchanged.
2. Built-in image_gen.imagegen makes a **separate pixel-friendly interpretation**, guided primarily by approved Chapter2 Bureau/Control Tower. Prompts, inputs and receipts are retained; this source is not called finished art.
3. A nearest target-grid transfer is saved as a **diagnostic underpainting only**.
4. At314x206, authored semantic masks distinguish floor, wall, steel, wood/copper, occluded props and NPC regions. Material-specific ramps are selected; quiet one/two-pixel low-contrast texture components are merged while structural seams, lights, hardware, brick, features and object contours are protected.
5. A separate native RGBA construction layer rebuilds elevator panel geometry, perspective floor grout, explicit light/shadow planes and wear clusters, beam/duct edges, stairs/rail silhouettes or piano keys/rim, exterior drainage and threshold details. These are target-grid drawing decisions beyond palette fitting; the JSON guide and transparent layer expose them for correction.
6. NPC regions are saved as separate editable layers. Tiny figures use clothing/pose/cap and concise skin/hand clusters, not portrait-level anatomy. Final opaque native PNGs and exact1256x824 nearest4x views are exported.

**SOURCE-DERIVED native reinterpretation**, not independently authored whole-image native art. Some source-defined object contours remain; the method is neither a complete manual repaint nor a direct resize/quantization-only finish. No blur, unsharp filter, gradient synthesis or dithering is used in this pass. Scripts and layers make the actual work reproducible; visual approval remains Nate's decision.

## Review material

[Gallery](index.html), [manifest/hashes](manifest.json), [v01/v02](comparisons/v01-v02-native.png), [exact4x](comparisons/v01-v02-4x.png), [canonical comparisons](comparisons/canonical-native.png), [canonical4x](comparisons/canonical-4x.png), [native construction stages](comparisons/native-construction-native.png). Detailed source originals, pixel-friendly sources, masks, layers, prompts, generation receipts and diagnostics are preserved. Palette/component counts are diagnostic evidence only.

The exact v01 foreman and background remain UNSELECTED retained candidates. No portrait/background cosmetic rework or silent approval occurs here. All ten approved Chapter4 PNGs, the two plumber palette alternatives and every prior review version remain unchanged. No narrative/gameplay or engine integration.

Reproduce with the recorded Pillow version:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/native_rebuild.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```
''')
 print('Consolidated four-scene review packaged.')
if __name__=='__main__':main()
