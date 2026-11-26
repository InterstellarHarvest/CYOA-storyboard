from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, hashlib, html
ROOT=Path(__file__).resolve().parents[1]
BASE='436e83f43c01b0a64620056d44aabf14c61fb444'
BRANCH='art/ch4-b216-fatal-aftermaths-review-20261125'
SPECS=[
 ('CH4-NEW-14','FINAL OCCUPANCY','final-occupancy','fatal_stall_final_occupancy','final_occupancy','occupancy'),
 ('CH4-NEW-15','PRESSED AND STEAMED','pressed-and-steamed','fatal_boiler_pressed_and_steamed','pressed_and_steamed','steam'),
 ('CH4-NEW-16','FOLDED FOR CONVENIENCE','folded-for-convenience','fatal_lot61_folded','folded_for_convenience','case'),
 ('CH4-NEW-17','MADE TO MEASURE','made-to-measure','fatal_bridal_made_to_measure','made_to_measure','gown'),
]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(f):
 im=Image.open(ROOT/f);return {'file':f,'sha256':sha(ROOT/f),'dimensions':list(im.size),'mode':im.mode}
def four(f):
 im=Image.open(ROOT/f);p='previews/'+Path(f).stem+'-4x.png';im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/p);return p
def main():
 assets=[];nodes=json.loads((ROOT/'evidence/canonical-nodes.json').read_text());references=json.loads((ROOT/'evidence/references.json').read_text())
 for id,title,slug,node,key,anchor in SPECS:
  f=f'native/{id}-{slug}-v02.png';im=Image.open(ROOT/f);two=f'previews/{id}-{slug}-v02-2x.png';im.resize((628,412),Image.Resampling.NEAREST).save(ROOT/two)
  assets.append({'id':id,'title':title,'version':'v02','status':'UNSELECTED','ownerApproved':False,'selected':False,'class':'fatal-aftermath','node':node,'endingArt':nodes[node]['endingArt'],'deathPopupId':nodes[node]['deathPopup']['id'],'proposedExistingCanonicalKey':'deathScreens:grand_bellevue/'+key,'canonicalAssetPath':None,'runtimeBinding':None,'native':rec(f),'exact2x':rec(two),'exact4x':rec(four(f)),'sourceDerivedDesign':True,'nativeRasterConstructedIndependently':True,'referencePixelsTransferred':False})
 for r in references:four(r['file'])
 labels=[];font=ImageFont.load_default(size=13)
 def sheet(name,items):
  sizes=[Image.open(ROOT/f).size for label,f in items];widths=[max(w+24,int(font.getlength(label))+24)for(label,f),(w,h)in zip(items,sizes)]
  im=Image.new('RGB',(sum(widths)+8,max(h for w,h in sizes)+54),'#263a32');d=ImageDraw.Draw(im);x=8
  for(label,f),w in zip(items,widths):d.text((x+8,10),label,font=font,fill='#efe3bf');im.paste(Image.open(ROOT/f).convert('RGB'),(x+8,42));labels.append({'label':label,'fits':font.getlength(label)<w-16});x+=w
  p='comparisons/'+name+'-native.png';im.save(ROOT/p);four(p);return p
 # A readable two-by-two master sheet, using actual native images without scaling.
 contact=Image.new('RGB',(680,528),'#263a32');d=ImageDraw.Draw(contact)
 for i,a in enumerate(assets):
  x=16+(i%2)*338;y=12+(i//2)*264;d.text((x,y),a['title'],font=font,fill='#efe3bf');contact.paste(Image.open(ROOT/a['native']['file']),(x,y+32))
 contact.save(ROOT/'comparisons/four-aftermaths-native.png');four('comparisons/four-aftermaths-native.png')
 for i,(a,benchmark)in enumerate(zip(assets,['approved-ch2-compost.png','approved-ch2-reclassified.png','approved-ch2-compost.png','approved-ch2-site-improvement.png'])):
  sheet(a['id']+'-chapter2',[(a['title']+' - UNSELECTED',a['native']['file']),('Approved Chapter 2 aftermath','references/'+benchmark)])
 for a in assets:
  old=next((ROOT.parent/'v01/native').glob(a['id']+'-*.png'));p='references/'+old.name;(ROOT/p).write_bytes(old.read_bytes());four(p)
  sheet(a['id']+'-v01-v02',[('v01 - rejected rendering pass',p),('v02 - UNSELECTED refinement',a['native']['file'])])
 crops=[]
 for label,box in [('sink',(0,90,86,154)),('toilet',(146,120,253,200))]:
  for version in ['v01','v02']:
   source=next((ROOT.parent/version/'native').glob('CH4-NEW-14-*.png'));p=f'comparisons/{label}-{version}-native-crop.png';Image.open(source).crop(box).save(ROOT/p);four(p);crops.append((label+' '+version+' - actual native crop',p))
 sheet('porcelain-detail-v01-v02',crops)
 sheet('hotel-continuity',[(assets[0]['title'],assets[0]['native']['file']),('Approved restroom','references/approved-ch4-restroom.png'),(assets[2]['title'],assets[2]['native']['file']),('Approved lobby','references/approved-ch4-lobby.png')])
 sheet('gown-identity',[(assets[3]['title'],assets[3]['native']['file']),('B2-13 owner-directed gown identity','references/owner-directed-b213-gown.png'),('Approved bridal room','references/approved-ch4-bridal-room.png')])
 (ROOT/'evidence/caption-layout.json').write_text(json.dumps(labels,indent=2)+'\n')
 palette={}
 for a in assets:
  im=Image.open(ROOT/a['native']['file']);colours=sorted(im.getcolors(314*206),reverse=True);palette[a['id']]={'colours':len(colours),'noArbitraryGlobalPaletteLimit':True,'coloursAndPixels':[{'rgb':list(rgb),'pixels':n}for n,rgb in colours]}
 (ROOT/'evidence/palette-diagnostics.json').write_text(json.dumps(palette,indent=2)+'\n')
 m={'title':'Chapter 4 B2-16 v02 - four fatal aftermaths','branch':BRANCH,'canonicalBaseline':BASE,'preservationBaseline':'e7d516687a38bd542f6b1010644b7b5a5f37a2ae','status':'UNSELECTED','ownerApproved':False,'primaryAssetCount':4,'supplementalAssetCount':0,'assets':assets,'references':references,'registryModified':False,'narrativeGameplayOrEngineModified':False,'popupCopyModified':False,'popupsBakedIntoArtwork':False,'newCanonicalNodesOrEndings':0,'nextBatchStarted':False,'provenance':'evidence/generation-provenance.json','nativeLayers':'evidence/native-layer-recipes.json','semanticInventory':'evidence/authored-semantic-inventory.json','nativeRecipe':'source/build.py','sourceDerivedDesign':True,'nativeRasterConstructedIndependently':True,'referencePixelsTransferred':False,'whollyIndependentCreativeDesign':False}
 (ROOT/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 descriptions=[
  'Broken floor-level porcelain and three fallen auction tags below an elevated, empty stall. Four taut lifting cables. No shoe, body, impact or injury.',
  'One ordinary wire hanger carries both the empty tuxedo jacket and the folded matching trousers. Three restrained steam wisps. No boiler, gauges, clipboard, shoe, person or lettering.',
  'One compact metallic briefcase, approximately two shoe-lengths wide, with only a slight asymmetric lid bulge. Exactly one loose shoe; orderly hotel auction context.',
  'The B2-13 gown and wheeled stand identity, re-illustrated at 314×206. Empty lace neckline, absurdly cinched bodice, layered skirt and exactly one abandoned shoe. No wearer or complex machinery.',
 ]
 def fig(label,f):
  im=Image.open(ROOT/f);p='previews/'+Path(f).stem+'-4x.png';return f'<section class="figure"><h3>{html.escape(label)}</h3><nav><button data-scale="1">Native 1×</button><button data-scale="4">Exact 4×</button><a href="{f}">Native PNG</a><a href="{p}">4× PNG</a></nav><div class="raster"><img src="{f}" data-one="{f}" data-four="{p}" data-w="{im.width}" data-h="{im.height}" width="{im.width}" height="{im.height}" alt="{html.escape(label)}"></div></section>'
 css='body{margin:0;background:#172a23;color:#efe5c8;font:16px/1.55 system-ui,sans-serif}main{padding:22px}header,article{padding:20px;border:1px solid #697c6d;margin-bottom:26px}h1,h2,h3{margin:0 0 12px}a{color:#c5dfca;margin-right:14px}nav{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0}button{padding:10px;background:#435e4d;border:1px solid #bacbaa;color:#fff0ca;cursor:pointer}.figure{padding:14px;margin:20px 0;background:#294136}.raster{overflow:auto;max-width:100%;background:#253b32}.raster img{display:block;max-width:none!important;image-rendering:pixelated}p{max-width:1120px}'
 page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 4 B2-16 · Four fatal aftermaths</title><style>'+css+'</style><main><header><h1>Chapter 4 B2-16 · Four fatal aftermaths · v02</h1><p><strong>All four candidates UNSELECTED.</strong> Each image is 314×206 opaque RGB, with exact 2× popup-compatible and nearest-neighbor 4× exports. No visible victim, face, limb, gore, impact or wearer. Titles and popup copy remain separate UI; none is baked into the artwork.</p><p>Detailed generated originals are design references. Final rasters are independently constructed on blank native-grid layers; no source pixels are shrunk, sampled or transferred. Controlled material ramps and clean silhouettes retain readability at 4×.</p><nav>'
 for id,title,slug,node,key,anchor in SPECS:page+=f'<a href="#{anchor}">{title}</a>'
 page+='<a href="#comparisons">Comparisons</a><a href="#benchmarks">Approved benchmarks</a><a href="manifest.json">Manifest / hashes</a><a href="evidence/validation.json">QA</a><a href="README.md">Method / visual assessment</a><a href="evidence/canonical-nodes.json">Exact authored nodes</a><a href="evidence/generation-provenance.json">Sources / prompts</a><a href="source/build.py">Native recipe</a><a href="evidence/native-layer-recipes.json">Editable layers</a></nav></header>'
 for spec,a,desc in zip(SPECS,assets,descriptions):
  page+=f'<article id="{spec[-1]}"><h2>{a["id"]} · {a["title"]}</h2><p>{desc}</p>'+fig(a['title']+' · UNSELECTED',a['native']['file'])+f'<p><a href="{a["exact2x"]["file"]}">Exact 2× export</a> · Canonical node: <code>{a["node"]}</code></p></article>'
 page+='<article id="comparisons"><h2>v01 / v02 and benchmark comparisons</h2><p>v02 rebuilds the basin, tap, trap, broken cistern/bowl/pedestal and ceramic fragments; corrects the left floor/wall intersection; and develops tailoring, satin, metal hardware, leather and gown construction. The close-ups below are pixel-exact crops, not new assets or softened enlargements.</p>'+fig('All four v02 native candidates','comparisons/four-aftermaths-native.png')+fig('Sink and toilet detail · v01 / v02','comparisons/porcelain-detail-v01-v02-native.png')
 for a in assets:page+=fig(a['title']+' · v01 / v02','comparisons/'+a['id']+'-v01-v02-native.png')
 for a in assets:page+=fig(a['title']+' / approved Chapter 2','comparisons/'+a['id']+'-chapter2-native.png')
 page+=fig('Approved hotel environment continuity','comparisons/hotel-continuity-native.png')+fig('Gown and stand identity continuity','comparisons/gown-identity-native.png')+'</article>'
 page+='<article id="benchmarks"><h2>Actual approved Chapter 2 aftermath PNGs</h2>'
 for r in references:
  if 'ch2-' in r['file'] and 'bureau'not in r['file']:page+=fig(Path(r['file']).stem+' · approved bytes',r['file'])
 page+='</article><article id="sources"><h2>Detailed reference originals · not native production artwork</h2><p>The source illustrations are retained without alteration. The final stall is opened to communicate its emptiness; the suit uses a visibly hollow jacket opening, one wire crossbar and folded trousers; the case stays portable; the gown retains the owner-directed identity without the source’s machinery. Original sources and prompts are preserved even where native design choices differ.</p><nav>'
 for a in assets:page+=f'<a href="originals/{a["id"]}-detailed-reference.png">{a["id"]} original</a><a href="prompts/{a["id"]}-reference-prompt.txt">Exact prompt</a>'
 page+='</nav><p>B2-13 is used as the gown identity expressly directed by this brief. Its pinned historical review manifest remains UNSELECTED; this package does not infer or perform registration. All canonical images remain unchanged.</p></article>'
 page+='<script>document.querySelectorAll("button[data-scale]").forEach(b=>b.onclick=()=>{const i=b.closest("section.figure").querySelector("img"),s=Number(b.dataset.scale);i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;});</script></main></html>'
 (ROOT/'index.html').write_text(page)
if __name__=='__main__':main()
