from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
import json,hashlib,html
ROOT=Path(__file__).resolve().parents[1];OLD=ROOT.parent/'v01'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(rel):
 im=Image.open(ROOT/rel);return {'file':rel,'sha256':sha(ROOT/rel),'dimensions':list(im.size),'mode':im.mode}
def main():
 dry='native/CH4-NEW-04-public-corridor-v02.png';flood='native/CH4-NEW-04-public-corridor-flood-v02.png'
 beforeDry='references/v01-CH4-NEW-04-public-corridor-v01.png';beforeFlood='references/v01-CH4-NEW-04-public-corridor-flood-v01.png'
 refs=json.loads((ROOT/'evidence/benchmark-provenance.json').read_text())
 for p in(ROOT/'references').glob('*.png'):
  im=Image.open(p);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/'previews'/(p.stem+'-4x.png'))
 font=ImageFont.load_default(size=13);captions=[]
 def sheet(items,name):
  dims=[Image.open(ROOT/p).size for t,p in items];widths=[max(w+16,int(font.getlength(t))+16)for(t,p),(w,h)in zip(items,dims)]
  im=Image.new('RGB',(sum(widths)+8,max(h for w,h in dims)+44),'#283d35');d=ImageDraw.Draw(im);x=8
  for(t,p),width in zip(items,widths):
   d.text((x+4,8),t,font=font,fill='#f0e4c4');im.paste(Image.open(ROOT/p).convert('RGB'),(x+4,36));captions.append({'sheet':name,'caption':t,'textWidth':font.getlength(t),'panelWidth':width,'fits':font.getlength(t)<=width-8});x+=width
  im.save(ROOT/f'comparisons/{name}-native.png');im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/f'comparisons/{name}-4x.png')
 sheet([('v01 dry',beforeDry),('v02 dry',dry)],'dry-v01-v02')
 sheet([('v01 flood',beforeFlood),('v02 flood',flood)],'flood-v01-v02')
 sheet([('v02 dry',dry),('v02 flood',flood)],'dry-flood')
 sheet([('v02 flood',flood),('Approved Staff Lavatory','references/staff_lavatory.png'),('Approved Ch4 Lobby','references/lobby.png')],'staff-lavatory-benchmark')
 sheet([('v02 dry',dry),('Ch2 Bureau','references/conveniences_bureau.png'),('Ch2 Control Tower','references/control_tower.png')],'chapter2-benchmarks')
 sheet([('v02 dry',dry),('Ch4 Service Stairs','references/service_stairs.png'),('Ch2 Maintenance Exit','references/maintenance_exit.png')],'additional-benchmarks')
 for name,box,before,after in [('yard',(253,20,314,204),beforeDry,dry),('far-doors',(125,67,164,155),beforeDry,dry),('hatch',(69,111,115,184),beforeFlood,flood),('attendant',(107,95,166,200),beforeFlood,flood)]:
  items=[]
  for version,file in [('v01',before),('v02',after)]:
   p=f'previews/{version}-{name}-native.png';im=Image.open(ROOT/file).crop(box);im.save(ROOT/p);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/p.replace('-native','-4x'));items.append((version+' '+name,p))
  sheet(items,name+'-before-after')
 (ROOT/'evidence/caption-layout.json').write_text(json.dumps(captions,indent=2)+'\n')
 changes={}
 for state,before,after in [('dry',beforeDry,dry),('flood',beforeFlood,flood)]:
  a=Image.open(ROOT/before);b=Image.open(ROOT/after);delta=ImageChops.difference(a,b);m=ImageChops.lighter(ImageChops.lighter(delta.getchannel('R'),delta.getchannel('G')),delta.getchannel('B')).point(lambda p:255 if p else 0);m.save(ROOT/f'masks/{state}-actual-corrections.png');changes[state]=sum(p!=q for p,q in zip(a.get_flattened_data(),b.get_flattened_data()))
 manifest={'title':'Chapter4 B2-11 v02 — side exit, door perspective, hatch and attendant','branch':'art/ch4-b211-public-corridor-review-20261124','preservationBaseline':'e650f02a1d803069ae142557cfc134edab77dafd','canonicalMain':'5a4290d672e1904b4b5ad361562f05168c328a50','status':'UNSELECTED','ownerApproved':False,'primaryUnits':1,'asset':{'id':'CH4-NEW-04','proposedCanonicalKey':'scenes:grand_bellevue/public_corridor','native':rec(dry),'preview4x':rec('previews/CH4-NEW-04-public-corridor-v02-4x.png'),'nodeIds':['hotel_stall_public_corridor_walk','hotel_flooded_public_corridor'],'runtimeBinding':None,'newFocusId':None},'supplementalReferences':[{'label':'public_corridor_flood','role':'Conditional production reference only','condition':'Water over carpet; open maintenance hatch; attendant; fallen floating WET FLOOR sign','nodeIds':['hotel_flooded_public_corridor'],'native':rec(flood),'preview4x':rec('previews/CH4-NEW-04-public-corridor-flood-v02-4x.png'),'runtimeBinding':None,'newFocusId':None,'newSceneKey':None,'newFlag':None}],'sourceDerived':True,'whollyIndependentNativeAuthorship':False,'methodRecord':'evidence/repair.json','nativeLayerRecipe':'source/refine.py','generationProvenance':'evidence/generation-provenance.json','attendantOriginal':rec('originals/attendant-illustration-source.png'),'prompt':'source/attendant-prompt.txt','changesFromV01':changes,'wholeSceneRegenerated':False,'narrativeGameplayBindingsModified':False,'productionSelectionsModified':False}
 (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 def fig(title,one,four):
  w,h=Image.open(ROOT/one).size
  return f'<section class="figure"><h3>{html.escape(title)}</h3><nav><button data-scale="1">Native 1×</button><button data-scale="4">Exact 4×</button><a href="{one}">PNG</a><a href="{four}">4× PNG</a></nav><div class="raster"><img src="{one}" data-one="{one}" data-four="{four}" data-w="{w}" data-h="{h}" width="{w}" height="{h}" alt="{html.escape(title)}"></div></section>'
 css='body{margin:0;background:#142820;color:#efe5c8;font:16px/1.5 system-ui,sans-serif}main{padding:22px}header,article{padding:20px;border:1px solid #647466;margin-bottom:26px}h1,h2,h3{margin:0 0 12px}a{color:#bce0c9;margin-right:16px}nav{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0}button{padding:10px;background:#435e4d;border:1px solid #b7c8ac;color:#f4e9ca;cursor:pointer}.figure{padding:14px;margin:20px 0;background:#294136}.raster{overflow:auto;max-width:100%;background:#253b32}.raster img{display:block;max-width:none!important;image-rendering:pixelated}code{overflow-wrap:anywhere}'
 body='<article id="dry"><h2>CH4-NEW-04 · v02 dry master · UNSELECTED</h2>'+fig('v02 dry corridor',dry,'previews/CH4-NEW-04-public-corridor-v02-4x.png')+'</article>'
 body+='<article id="flood"><h2>Localized flood · v02 reference · UNSELECTED</h2>'+fig('v02 flood reference',flood,'previews/CH4-NEW-04-public-corridor-flood-v02-4x.png')+'</article>'
 body+='<article id="comparisons"><h2>Native / exact4× before and after</h2>'
 for title,name in [('Dry: v01 / v02','dry-v01-v02'),('Flood: v01 / v02','flood-v01-v02'),('Common architecture: dry / flood','dry-flood'),('Approved Staff Lavatory comparison','staff-lavatory-benchmark'),('Approved Chapter2 comparison','chapter2-benchmarks'),('Other approved environments','additional-benchmarks'),('Side exit / yard','yard-before-after'),('Far door perspective','far-doors-before-after'),('Hatch construction','hatch-before-after'),('Attendant scale and detail','attendant-before-after')]:body+=fig(title,f'comparisons/{name}-native.png',f'comparisons/{name}-4x.png')
 body+='</article><article id="benchmarks"><h2>Actual approved canonical references</h2>'
 for ref in refs:
  p=Path(ref['file']);body+=fig(p.stem,ref['file'],'previews/'+p.stem+'-4x.png')
 body+='</article>'
 head='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>B2-11 v02 targeted repair</title><style>'+css+'</style><main><header><h1>Chapter4 B2-11 v02 · targeted owner corrections</h1><p><strong>Everything UNSELECTED. Nate’s visual approval is pending.</strong> Same314×206 room and exact1256×824 nearest-neighbor4×. Original v01 remains unchanged.</p><p>Recognizable loading-yard exit and right jamb; far doors projected to the shared corridor vanishing point; a fixed hatch frame and hinged outward leaf; a distinct94-pixel gray-haired hotel attendant in a navy work jacket and trousers, pointing toward the staff passage. The approved Staff Lavatory is a rendering benchmark only.</p><p>SOURCE-DERIVED localized rendering and scene-character production. The generated attendant source is reduced with a controlled material ramp and native cluster cleanup; independent native authorship is not claimed. No whole-room regeneration, extra portrait, runtime binding or approval change.</p><nav><a href="manifest.json">Manifest / hashes</a><a href="README.md">Method / scope</a><a href="evidence/validation.json">QA / preservation</a><a href="evidence/visual-review.md">Visual assessment</a><a href="evidence/repair.json">Geometry / layer recipe</a><a href="evidence/generation-provenance.json">Generation provenance</a><a href="source/attendant-prompt.txt">Attendant prompt</a><a href="originals/attendant-illustration-source.png">Attendant original</a><a href="../v01/originals/CH4-NEW-04-pixel-friendly-study.png">Preserved room source</a></nav></header>'
 script='<script>document.querySelectorAll("button[data-scale]").forEach(b=>b.onclick=()=>{const i=b.closest("section.figure").querySelector("img"),s=Number(b.dataset.scale);i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;});</script></main></html>'
 (ROOT/'index.html').write_text(head+body+script);print(json.dumps(changes))
if __name__=='__main__':main()
