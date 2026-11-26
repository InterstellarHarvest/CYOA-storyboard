from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,html
ROOT=Path(__file__).resolve().parents[1]
BASE='6a88153f1a41759def5d8e02fd04789db860ec1b'
BRANCH='art/ch4-b217-ticket-ring-review-20261125'
SPECS=[('CH4-NEW-10','Lot 53 Dispute Ticket — slot','dispute-ticket-slot','lot_53_dispute_ticket','slot','ticket-slot'),('CH4-NEW-11','Lot 53 Dispute Ticket — inspection','dispute-ticket-inspection','lot_53_dispute_ticket','inspect','ticket-inspect'),('CH4-NEW-12','Wedding Ring — slot','wedding-ring-slot','wedding_ring_lot31','slot','ring-slot'),('CH4-NEW-13','Wedding Ring — inspection','wedding-ring-inspection','wedding_ring_lot31','inspect','ring-inspect')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(f):
 im=Image.open(ROOT/f);return {'file':f,'sha256':sha(ROOT/f),'dimensions':list(im.size),'mode':im.mode}
def four(f):
 im=Image.open(ROOT/f);p='previews/'+Path(f).stem+'-4x.png';im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/p);return p
def main():
 assets=[];refs=json.loads((ROOT/'evidence/references.json').read_text());nodes=json.loads((ROOT/'evidence/canonical-nodes.json').read_text())
 for id,label,slug,item,kind,anchor in SPECS:
  f=f'native/{id}-{slug}-v01.png';assets.append({'id':id,'label':label,'version':'v01','itemId':item,'view':kind,'status':'UNSELECTED','ownerApproved':False,'selected':False,'proposedExistingCanonicalKey':'items:'+item+':'+kind,'canonicalAssetPath':None,'runtimeBinding':None,'native':rec(f),'exact4x':rec(four(f)),'sourceDerivedDesign':True,'nativeRasterConstructedIndependently':True,'sourcePixelsTransferred':False,'nodeCoverage':[k for k,v in nodes.items()if item in json.dumps(v)]})
 for r in refs:four(r['file'])
 font=ImageFont.load_default(size=13);labels=[]
 def paste(base,img,xy):
  image=img.convert('RGBA');base.paste(image,xy,image.getchannel('A'))
 def sheet(name,items):
  items=[(label.replace('—','-').replace('·','/'),f)for label,f in items]
  sizes=[Image.open(ROOT/f).size for label,f in items];widths=[max(w+24,int(font.getlength(label))+24)for(label,f),(w,h)in zip(items,sizes)]
  im=Image.new('RGB',(sum(widths)+8,max(h for w,h in sizes)+54),'#34443e');d=ImageDraw.Draw(im);x=8
  for(label,f),w in zip(items,widths):
   d.text((x+8,10),label,font=font,fill='#efe3bf');paste(im,Image.open(ROOT/f),(x+8,42));labels.append({'label':label,'fits':font.getlength(label)<w-16});x+=w
  p='comparisons/'+name+'-native.png';im.save(ROOT/p);four(p);return p
 # The primary images retain their own native sizes; slots are never enlarged to
 # masquerade as inspection sources. Only the separate 4x exports magnify them.
 contact=Image.new('RGB',(760,1080),'#34443e');d=ImageDraw.Draw(contact)
 for i,a in enumerate(assets):
  x=16 if i%2==0 else 177;y=16+(i//2)*535;d.text((x,y),a['id']+' · '+a['view'],font=font,fill='#efe3bf');paste(contact,Image.open(ROOT/a['native']['file']),(x,y+36))
 contact.save(ROOT/'comparisons/four-assets-native.png');four('comparisons/four-assets-native.png')
 sheet('ticket-pair-identity',[('Slot — actual 96x96',assets[0]['native']['file']),('Inspection — actual 565x451',assets[1]['native']['file'])])
 sheet('ring-pair-identity',[('Slot — actual 96x96',assets[2]['native']['file']),('Inspection — actual 565x451',assets[3]['native']['file'])])
 sheet('slot-benchmarks',[(assets[0]['label'],assets[0]['native']['file']),(assets[2]['label'],assets[2]['native']['file']),('Approved Chapter 2 seed','references/approved-ch2-seed-slot.png'),('Approved Chapter 2 antidote','references/approved-ch2-antidote-slot.png'),('Approved paper slot','references/approved-claim-ticket-slot.png')])
 sheet('ticket-inspection-benchmarks',[('Ticket — UNSELECTED',assets[1]['native']['file']),('Approved paper inspection','references/approved-claim-ticket-inspect.png'),('Approved Chapter 2 item inspection','references/approved-ch2-antidote-inspect.png')])
 sheet('ring-inspection-benchmarks',[('Ring — UNSELECTED',assets[3]['native']['file']),('Approved Chapter 2 metal inspection','references/approved-ch2-seed-inspect.png')])
 sheet('ring-armrest-continuity',[('Ring inspection candidate',assets[3]['native']['file']),('Approved auction armrest','references/approved-ch4-auction-armrest.png'),('Approved collection armrest','references/approved-ch4-collection-armrest.png')])
 # Pixel-exact inspection crops make the curve and stamp easy to audit, but the
 # actual wording remains legible in the full native production inspection PNG.
 Image.open(ROOT/assets[3]['native']['file']).crop((125,128,372,203)).save(ROOT/'comparisons/ring-inscription-native-crop.png');four('comparisons/ring-inscription-native-crop.png')
 Image.open(ROOT/assets[1]['native']['file']).crop((104,102,490,351)).save(ROOT/'comparisons/ticket-lettering-native-crop.png');four('comparisons/ticket-lettering-native-crop.png')
 (ROOT/'evidence/caption-layout.json').write_text(json.dumps(labels,indent=2)+'\n')
 palette={}
 for a in assets:
  im=Image.open(ROOT/a['native']['file']);counts=sorted(im.getcolors(565*451),reverse=True)
  palette[a['id']]={'coloursIncludingTransparency':len(counts),'noArbitraryGlobalPaletteLimit':True,'colours':[{'pixel':list(rgb),'count':n}for n,rgb in counts]}
 (ROOT/'evidence/palette-diagnostics.json').write_text(json.dumps(palette,indent=2)+'\n')
 m={'title':'Chapter 4 B2-17 v01 — Dispute Ticket and Wedding Ring','branch':BRANCH,'canonicalBaseline':BASE,'status':'UNSELECTED','ownerApproved':False,'primaryAssetCount':4,'supplementalAssetCount':0,'assets':assets,'references':refs,'registryModified':False,'narrativeGameplayItemRulesOrEngineModified':False,'newFocusStatesOrBindings':0,'nextBatchStarted':False,'wordingAudit':'evidence/wording-audit.json','nativeTextLayout':'evidence/native-text-layout.json','nativeLayers':'evidence/native-layer-recipes.json','sourceDerivedDesign':True,'nativeRasterConstructedIndependently':True,'sourcePixelsTransferred':False,'whollyIndependentCreativeDesign':False,'inspectionCanvasContract':'565x451 opaque RGB; item-inspect, not 564x278 Focus A','slotContract':'96x96 transparent RGBA, binary alpha, no UI frame or shadow/glow; ring hole transparent'}
 (ROOT/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 def fig(label,f):
  im=Image.open(ROOT/f);p='previews/'+Path(f).stem+'-4x.png';return f'<section class="figure"><h3>{html.escape(label)}</h3><nav><button data-scale="1">Native 1×</button><button data-scale="4">Exact 4×</button><a href="{f}">Native PNG</a><a href="{p}">4× PNG</a></nav><div class="raster"><img src="{f}" data-one="{f}" data-four="{p}" data-w="{im.width}" data-h="{im.height}" width="{im.width}" height="{im.height}" alt="{html.escape(label)}"></div></section>'
 css='body{margin:0;background:#172a23;color:#efe5c8;font:16px/1.55 system-ui,sans-serif}main{padding:22px}header,article{padding:20px;border:1px solid #697c6d;margin-bottom:26px}h1,h2,h3{margin:0 0 12px}a{color:#c5dfca;margin-right:14px}nav{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0}button{padding:10px;background:#435e4d;border:1px solid #bacbaa;color:#fff0ca;cursor:pointer}.figure{padding:14px;margin:20px 0;background:#294136}.raster{overflow:auto;max-width:100%;background-color:#4b5750;background-image:linear-gradient(45deg,#606d62 25%,transparent 25%),linear-gradient(-45deg,#606d62 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#606d62 75%),linear-gradient(-45deg,transparent 75%,#606d62 75%);background-size:16px 16px;background-position:0 0,0 8px,8px -8px,-8px 0}.raster img{display:block;max-width:none!important;image-rendering:pixelated}p{max-width:1120px}'
 page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 4 B2-17 · Ticket and Wedding Ring · v01</title><style>'+css+'</style><main><header><h1>Chapter 4 B2-17 · Ticket and Wedding Ring · v01</h1><p><strong>Four candidates · all UNSELECTED.</strong> Slot images are true 96×96 transparent RGBA with binary alpha. Independent inspection images are 565×451 opaque RGB. Each has an exact nearest-neighbor 4× export. Checkerboard is gallery CSS, never part of the PNG.</p><p>All three ticket phrases are confirmed in the canonical item description: LOT 53; LACK OF PRIVACY — CUSTOMER PRESENT; HOLD FOR INSPECTION. No draft-only wording remains. The ring reads exactly <strong>AS IS, WHERE IS.</strong> along its inner curve, with a tiny anonymous maker punch above it. Slot art reveals no readable engraving.</p><p>Paper type is a chunky native bitmap construction projected onto the paper plane. Ring glyphs are individually placed on the inner-curve tangent. Neither font is a smoothed generated texture. The four detailed imagegen references are preserved; final rasters are separately constructed at native sizes without reference-pixel transfer.</p><nav>'
 for id,label,slug,item,kind,anchor in SPECS:page+=f'<a href="#{anchor}">{id}</a>'
 page+='<a href="#comparisons">Identity / comparisons</a><a href="#lettering">Lettering</a><a href="#benchmarks">Canonical art</a><a href="manifest.json">Manifest / hashes</a><a href="evidence/validation.json">QA</a><a href="evidence/wording-audit.json">Canonical wording audit</a><a href="README.md">Method / scope</a><a href="source/build.py">Native recipe</a><a href="evidence/native-layer-recipes.json">Editable native layers</a><a href="evidence/generation-provenance.json">Imagegen sources / prompts</a></nav></header>'
 descriptions=['Red paper, perforated tear-off edge, lot code, form structure and a compact inspection stamp. No baked inventory frame, background, glow or contact shadow.','One red carbon-copy ticket, generous physical margins, canonical reason wording and stamped inspection hold. Ordinary paperwork; no invented names, serials, dates, cancellation or refund rights.','One plain silver band and one pale blue ribbon, matching the approved armrest object. Open transparent hole, no readable inscription or maker mark, ring box, stone or additional jewelry.','The same silver band and ribbon, independently modeled at inspection size. Exact inscription follows the inner curve; the anonymous maker mark carries no invented initials, brand or purity number.']
 for spec,a,desc in zip(SPECS,assets,descriptions):page+=f'<article id="{spec[-1]}"><h2>{a["id"]} · {html.escape(a["label"])}</h2><p>{desc}</p>'+fig(a['label']+' · UNSELECTED',a['native']['file'])+'</article>'
 page+='<article id="comparisons"><h2>Native / exact 4× identity and quality comparisons</h2>'+fig('All four candidates at their actual native dimensions','comparisons/four-assets-native.png')
 for n,label in [('ticket-pair-identity','Ticket pair — separate native illustrations'),('ring-pair-identity','Ring pair — same object, separate native illustrations'),('slot-benchmarks','Approved inventory-slot benchmarks'),('ticket-inspection-benchmarks','Paper / Chapter 2 inspection benchmarks'),('ring-inspection-benchmarks','Metal / Chapter 2 inspection benchmark'),('ring-armrest-continuity','Approved Chapter 4 ring identity')]:page+=fig(label,'comparisons/'+n+'-native.png')
 page+='</article><article id="lettering"><h2>Canonical lettering — exact native crops</h2><p>These crops contain the actual inspection pixels. No larger replacement text or caption is inserted into the artwork. Readability must also hold in the full native inspection views above.</p>'+fig('AS IS, WHERE IS. — actual inner-curve pixels','comparisons/ring-inscription-native-crop.png')+fig('Ticket wording / margins — actual paper pixels','comparisons/ticket-lettering-native-crop.png')+'</article>'
 page+='<article id="benchmarks"><h2>Actual approved canonical PNGs · unchanged</h2>'
 for r in refs:page+=fig(r['role'],r['file'])
 page+='</article><article id="sources"><h2>Detailed references · not production rasters</h2><nav>'
 for a in assets:page+=f'<a href="originals/{a["id"]}-reference.png">{a["id"]} original</a><a href="prompts/{a["id"]}-reference-prompt.txt">Exact prompt</a>'
 page+='</nav><p>The generated slot ring reference includes unwanted soft glow. It is preserved as a reference artifact; the native output transfers none of it and has strictly binary transparency. No generated source is reduced into a finished asset. Creative design is disclosed as source-derived. Nothing is selected, registered, merged, bound to gameplay or deployed.</p></article><script>document.querySelectorAll("button[data-scale]").forEach(b=>b.onclick=()=>{const i=b.closest("section.figure").querySelector("img"),s=Number(b.dataset.scale);i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;});</script></main></html>'
 (ROOT/'index.html').write_text(page)
if __name__=='__main__':main()
