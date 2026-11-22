"""Package a fresh generated style candidate. This script does not draw art.

The 564x278 layout is an explicitly source-derived diagnostic, not a native
reconstruction. Source bytes are preserved. Inspection enlargements are NN4x.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin
import hashlib,json,html

ROOT=Path(__file__).resolve().parent.parent
REVIEW=ROOT.parent
ORIGINAL='generated/CH4-03-auctioneer-fresh-style-original.png'
DIAG='diagnostics/CH4-03-layout-only-source-derived-564x278.png'
COMPOSITE='diagnostics/CH4-03-over-frozen-v05-layout-only.png'
ITEMS=[
 ('fresh','Fresh auctioneer','SOURCE-DERIVED LAYOUT ONLY',DIAG,'previews/fresh-layout-exact-4x.png'),
 ('attendant','Approved Pavilion attendant','APPROVED REFERENCE - NATIVE','../v04/references/pavilion_attendant_idle.png','previews/attendant-exact-4x.png'),
 ('presenter','Approved Pavilion presenter','APPROVED REFERENCE - NATIVE','../v04/references/pavilion_presenter_idle.png','previews/presenter-exact-4x.png'),
 ('v05','Preserved v05 auctioneer','UNSELECTED - EARLIER NATIVE','../v05/native/CH4-03-auctioneer-showman-v05.png','previews/v05-exact-4x.png'),
]

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def rec(relative):
 p=ROOT/relative;im=Image.open(p)
 return {'file':relative,'sha256':sha(p),'dimensions':list(im.size),'mode':im.mode}

def checker(size):
 im=Image.new('RGB',size,'#293a39');d=ImageDraw.Draw(im)
 for y in range(0,size[1],8):
  for x in range(0,size[0],8):
   if (x//8+y//8)%2:d.rectangle((x,y,x+7,y+7),fill='#3a4e49')
 return im

def metadata():
 info=PngImagePlugin.PngInfo()
 info.add_text('Classification','SOURCE-DERIVED STYLE/LAYOUT DIAGNOSTIC ONLY; NOT INDEPENDENT NATIVE ART')
 info.add_text('SourceSHA256',sha(ROOT/ORIGINAL))
 info.add_text('Operation','Nearest-neighbor resize of generated original to 564x278 for layout comparison only')
 return info

def main():
 for directory in ['diagnostics','previews','comparisons']:(ROOT/directory).mkdir(exist_ok=True)
 original=Image.open(ROOT/ORIGINAL)
 diagnostic=original.resize((564,278),Image.Resampling.NEAREST)
 diagnostic.save(ROOT/DIAG,pnginfo=metadata())
 original.resize((original.width*4,original.height*4),Image.Resampling.NEAREST).save(ROOT/'previews/generated-original-exact-4x.png')
 background=Image.open(REVIEW/'v05/native/CH4-02-auctioneer-background-v05.png').convert('RGBA')
 Image.alpha_composite(background,diagnostic).save(ROOT/COMPOSITE,pnginfo=metadata())
 Image.open(ROOT/COMPOSITE).resize((2256,1112),Image.Resampling.NEAREST).save(ROOT/'previews/composite-layout-exact-4x.png',pnginfo=metadata())
 assets=[]
 for id_,title,label,one,four in ITEMS:
  im=Image.open(ROOT/one)
  im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/four,pnginfo=metadata() if id_=='fresh' else None)
  assets.append({'id':id_,'title':title,'classification':label,'one':rec(one),'exact4x':rec(four)})
 sheet=Image.new('RGB',(1176,752),'#18272a');d=ImageDraw.Draw(sheet);font=ImageFont.load_default(size=14)
 d.text((12,12),'STYLE REVIEW ONLY - new auctioneer panel is source-derived; not native authorship',font=font,fill='#eec38e')
 for i,a in enumerate(assets):
  x=(i%2)*588+12;y=(i//2)*348+52
  d.text((x,y),a['title'],font=font,fill='#f4e7cd');d.text((x,y+20),a['classification'],font=font,fill='#eac58e')
  im=Image.open(ROOT/a['one']['file']).convert('RGBA');back=checker(im.size);back.paste(im,(0,0),im);sheet.paste(back,(x,y+46))
 sheet.save(ROOT/'comparisons/fresh-style-vs-approved-and-v05.png',pnginfo=metadata())
 sheet.resize((sheet.width*4,sheet.height*4),Image.Resampling.NEAREST).save(ROOT/'comparisons/fresh-style-vs-approved-and-v05-exact-4x.png',pnginfo=metadata())
 receipt=json.loads((ROOT/'evidence/generation-receipt.json').read_text())
 old=json.loads((REVIEW/'v05/manifest.json').read_text());canonical=next(a for a in old['assets'] if a['id']=='CH4-03')
 manifest={'id':'CH4-03','review':'Portrait study 02 — approved NPC style restart','status':'UNSELECTED','branch':'art/ch4-batch01-review-20261121','baseCommit':'f5bea5cc033676865d45d20ca9c3ac9842f7585d','method':'Fresh built-in image generation with ONLY approved Pavilion attendant and presenter. No high-detail auctioneer reference or prior auctioneer image was an input. Code packages presentation only.','original':rec(ORIGINAL),'originalExact4x':rec('previews/generated-original-exact-4x.png'),'layoutDiagnostic':{'classification':'SOURCE-DERIVED; NOT A NATIVE RECONSTRUCTION','operation':'Nearest-neighbor resize for style/layout review only','image':rec(DIAG),'nativeAuthorshipProven':False},'nativeCandidate':None,'productionReady':False,'inputReferences':receipt['inputReferences'],'prompt':'prompts/approved-npcs-only.txt','receipt':'evidence/generation-receipt.json','sourceNodeIds':canonical['sourceNodeIds'],'canonicalRequirements':'../v02/evidence/canonical-requirements.json','comparisonAssets':assets,'compositeLayoutDiagnostic':rec(COMPOSITE),'compositeExact4x':rec('previews/composite-layout-exact-4x.png'),'comparisonSheets':[rec('comparisons/fresh-style-vs-approved-and-v05.png'),rec('comparisons/fresh-style-vs-approved-and-v05-exact-4x.png')],'frozenEnvironments':json.loads((ROOT/'evidence/frozen-environments.json').read_text()),'pillowVersion':Image.__version__,'knownLimitations':['Original returned 1788x880 instead of requested 564x278. Independent native-grid production remains unresolved.','Layout image and composite use resized source pixels and are diagnostic only.','The face has a slight head tilt while face/torso look toward the viewer.','Style similarity and selection are for Nate to judge; no approval is claimed.','Generative call is stochastic; preserved-master presentation exports are reproducible.']}
 (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 findings={'status':'UNSELECTED','newConstruction':True,'generationReferences':['approved Pavilion attendant','approved Pavilion presenter'],'excludedInputs':['high-detail auctioneer drawing','v01-v05 auctioneer','previous raster method study'],'visualFindings':{'face':'A restrained skeptical elderly expression, clearer lids/cheeks/mouth and less mechanically concentric modeling than v05; slight head tilt.','hair':'Broad overlapping silver locks, selective lighter ridges and darker roots in the approved NPC illustration family.','handsAndGavel':'One hand wraps around a compact gavel handle; fingers, cuff and second hand form a more coherent pose.','costume':'Burgundy jacket uses weight-bearing illustrated folds; dark satin lapels, ivory shirt and bow tie have separate shapes and values.','paletteAndStyle':'Warmer simple skin planes and controlled contour/shadow shapes follow the Pavilion references rather than the earlier highly rendered auctioneer study.','remainingReview':'Nate should judge whether the face, expression, suit, gavel grip and overall level of illustration fit the approved NPCs. Source-sized polish and a resized diagnostic do not prove native production readiness.'},'comparisonClassification':'The new panel is source-derived layout; three other panels are actual native PNGs.','nativeProductionReady':False}
 (ROOT/'comparison.json').write_text(json.dumps(findings,indent=2)+'\n')
 cards=[]
 for a in assets:
  id_,one,four=a['id'],a['one']['file'],a['exact4x']['file']
  cards.append(f'<article id="{id_}"><h2>{html.escape(a["title"])}</h2><p class="tag">{a["classification"]}</p><div class="actions"><button class="scale" data-target="{id_}" data-scale="1">1× layout / native</button><button class="scale" data-target="{id_}" data-scale="4">Exact 4×</button><a href="{one}">PNG</a><a href="{four}">4× PNG</a></div><div class="viewport checker"><img class="artwork" data-target="{id_}" src="{one}" data-one="{one}" data-four="{four}" data-width="564" data-height="278" width="564" height="278" alt="{html.escape(a["title"])} — {a["classification"]}"></div></article>')
 def full_card(id_,title,one,four,label):
  im=Image.open(ROOT/one);w,h=im.size
  return f'<article id="{id_}"><h2>{title}</h2><p class="tag">{label} · {w}×{h}</p><div class="actions"><button class="scale" data-target="{id_}" data-scale="1">Original pixels</button><button class="scale" data-target="{id_}" data-scale="4">Exact 4×</button><a href="{one}">PNG</a><a href="{four}">4× PNG</a></div><div class="viewport checker"><img class="artwork" data-target="{id_}" src="{one}" data-one="{one}" data-four="{four}" data-width="{w}" data-height="{h}" width="{w}" height="{h}" alt="{title} — {label}"></div></article>'
 page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Auctioneer restart · approved NPC style</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#152428;color:#f0e6d4;font:16px/1.55 system-ui,sans-serif}main{max-width:1480px;margin:auto;padding:28px}h1{font-size:clamp(1.8rem,3vw,2.6rem);line-height:1.2}h2{font-size:1.25rem}.intro,.notes,article{background:#203438;border:1px solid #4a6563;padding:20px;border-radius:8px;margin:18px 0}.tag{font-weight:700;color:#e9c08c}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.grid article{margin:0;min-width:0}.actions{display:flex;flex-wrap:wrap;align-items:center;gap:14px;margin:14px 0}button{background:#355450;color:#fff1d6;padding:8px 13px;border:1px solid #829184;border-radius:4px;cursor:pointer}a{color:#addacb}.viewport{overflow:auto;max-width:100%;max-height:720px;border:1px solid #59716b}.artwork{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}.checker{background-color:#293a39;background-image:linear-gradient(45deg,#3a4e49 25%,transparent 25%),linear-gradient(-45deg,#3a4e49 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#3a4e49 75%),linear-gradient(-45deg,transparent 75%,#3a4e49 75%);background-size:16px 16px;background-position:0 0,0 8px,8px -8px,-8px 0}code{overflow-wrap:anywhere}li{margin:10px 0}button:focus-visible,a:focus-visible{outline:3px solid #edc792}@media(max-width:900px){.grid{grid-template-columns:1fr}}@media(max-width:600px){main{padding:12px}.intro,.notes,article{padding:14px}}
</style></head><body><main><header><p>Out of Order · Chapter 4 · CH4-03</p><h1>A fresh auctioneer in the approved NPC style</h1><p class="tag">UNSELECTED · Portrait study 02</p></header><section class="intro"><p>New character, generated from <strong>only the approved Pavilion attendant and presenter</strong>: an elderly man in burgundy formalwear, holding a gavel. The detailed auctioneer drawing and every prior auctioneer portrait were excluded from the input images.</p><p>The three-way style comparison is the focus. The new panel below is a <strong>source-derived layout preview</strong> at 564×278; it is not independently authored native artwork. The untouched generated original is 1788×880 and remains available below. Exact 4× exports preserve the displayed pixels.</p><p><a href="comparisons/fresh-style-vs-approved-and-v05.png">Direct comparison PNG</a> · <a href="comparisons/fresh-style-vs-approved-and-v05-exact-4x.png">Exact 4× comparison PNG</a> · <a href="prompts/approved-npcs-only.txt">Exact prompt</a> · <a href="evidence/generation-receipt.json">Two-reference receipt</a></p></section><section class="grid">__CARDS__</section>__COMPOSITE____ORIGINAL__<section class="notes" id="review-notes"><h2>Review focus</h2><p>Compare the face, silver hair, expression, gavel grip, suit folds and palette with the two approved NPCs. The new illustration uses the same kind of designed contours and color planes rather than reducing the earlier highly detailed drawing. The slight head tilt and the overall character are for owner review.</p><p>Native production remains unresolved: the tool returned a larger original. The resized layout and composite are explicitly source-derived diagnostics, not finished native assets. No approval or integration has occurred.</p><p><strong>Frozen environments:</strong> v05 lobby and portrait background remain byte-for-byte unchanged. Every previous candidate and review package is preserved. No main, narrative, gameplay, production workflow, restroom or ballroom changes.</p><p><a href="evidence/frozen-environments.json">Frozen PNG hashes</a> · <a href="evidence/validation.json">Validation</a> · <a href="manifest.json">Manifest and hashes</a> · <a href="comparison.json">Visual findings</a> · <a href="README.md">Production notes</a> · <a href="../v05/index.html">Preserved v05 gallery</a></p></section></main><script>
document.querySelectorAll('.scale').forEach(b=>b.addEventListener('click',()=>{const i=document.querySelector('.artwork[data-target="'+b.dataset.target+'"]'),s=Number(b.dataset.scale);i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.width)*s;i.height=Number(i.dataset.height)*s;}));
</script></body></html>'''
 page=page.replace('__CARDS__','\n'.join(cards)).replace('__COMPOSITE__',full_card('composite','Layout over the frozen v05 background',COMPOSITE,'previews/composite-layout-exact-4x.png','SOURCE-DERIVED COMPOSITE ONLY')).replace('__ORIGINAL__',full_card('original','Untouched generated original',ORIGINAL,'previews/generated-original-exact-4x.png','UNSELECTED · ORIGINAL OUTPUT; NOT NATIVE'))
 (ROOT/'index.html').write_text(page)

if __name__=='__main__':main()
