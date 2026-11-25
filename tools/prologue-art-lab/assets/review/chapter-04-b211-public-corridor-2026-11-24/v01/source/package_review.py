from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
import json,hashlib,html
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(rel):
 p=ROOT/rel;im=Image.open(p);return {'file':rel,'sha256':sha(p),'dimensions':list(im.size),'mode':im.mode}
def main():
 dry='native/CH4-NEW-04-public-corridor-v01.png';flood='native/CH4-NEW-04-public-corridor-flood-v01.png'
 refs=json.loads((ROOT/'evidence/benchmark-provenance.json').read_text())
 for r in refs:
  p=ROOT/r['file'];im=Image.open(p);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/'previews'/(p.stem+'-4x.png'))
 font=ImageFont.load_default(size=13);layout=[]
 def sheet(items,name):
  dims=[Image.open(ROOT/p).size for t,p in items];widths=[max(w+16,int(font.getlength(t))+16)for(t,p),(w,h)in zip(items,dims)]
  canvas=Image.new('RGB',(sum(widths)+8,max(h for w,h in dims)+44),'#283d35');d=ImageDraw.Draw(canvas);x=8
  for(t,p),width in zip(items,widths):
   d.text((x+4,8),t,font=font,fill='#f0e4c4');canvas.paste(Image.open(ROOT/p).convert('RGB'),(x+4,36));layout.append({'sheet':name,'caption':t,'textWidth':font.getlength(t),'panelWidth':width,'fits':font.getlength(t)<=width-8});x+=width
  canvas.save(ROOT/f'comparisons/{name}-native.png');canvas.resize((canvas.width*4,canvas.height*4),Image.Resampling.NEAREST).save(ROOT/f'comparisons/{name}-4x.png')
 sheet([('Dry corridor',dry),('Flood: same architecture',flood)],'dry-flood')
 sheet([('B2-11 dry',dry),('Ch2 Bureau','references/conveniences_bureau.png'),('Ch2 Control Tower','references/control_tower.png')],'chapter2-benchmarks')
 sheet([('B2-11 dry',dry),('Ch4 Lobby','references/lobby.png'),('Ch4 Service Stairs','references/service_stairs.png')],'chapter4-benchmarks')
 sheet([('Flood reference',flood),('Ch2 Maintenance Exit','references/maintenance_exit.png'),('Ch4 Staff Lavatory','references/staff_lavatory.png')],'state-benchmarks')
 sheet([('SOURCE TRANSFER - diagnostic','diagnostics/source-transfer-NOT-FINAL.png'),('Native interpretation',dry)],'source-native')
 for name,box in [('staff-hatch',(10,60,114,174)),('stairs',(163,55,236,154)),('water-sign',(119,161,188,205))]:
  items=[]
  for title,p in [('dry',dry),('flood',flood)]:
   dest=f'previews/{title}-{name}-native.png';im=Image.open(ROOT/p).crop(box);im.save(ROOT/dest);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/dest.replace('-native','-4x'));items.append((title+' '+name,dest))
  sheet(items,name+'-states')
 (ROOT/'evidence/caption-layout.json').write_text(json.dumps(layout,indent=2)+'\n')
 a=Image.open(ROOT/dry);b=Image.open(ROOT/flood);d=ImageChops.difference(a,b);changed=ImageChops.lighter(ImageChops.lighter(d.getchannel('R'),d.getchannel('G')),d.getchannel('B')).point(lambda p:255 if p else 0);changed.save(ROOT/'masks/flood-actual-changes.png')
 n=sum(p!=q for p,q in zip(a.get_flattened_data(),b.get_flattened_data()))
 recipe=json.loads((ROOT/'evidence/native-construction.json').read_text())
 manifest={'title':'Chapter4 B2-11 v01 — public corridor and localized flood','branch':'art/ch4-b211-public-corridor-review-20261124','canonicalMain':'5a4290d672e1904b4b5ad361562f05168c328a50','reviewBranchOriginalHead':'7fc6b9e','postMainMergeBaseline':'e4f46f2300bad7e946dea0ffd917d9c3b339b7b8','status':'UNSELECTED','ownerApproved':False,'primaryUnits':1,'asset':{'id':'CH4-NEW-04','proposedCanonicalKey':'scenes:grand_bellevue/public_corridor','native':rec(dry),'preview4x':rec('previews/CH4-NEW-04-public-corridor-v01-4x.png'),'nodeIds':['hotel_stall_public_corridor_walk','hotel_flooded_public_corridor'],'runtimeBinding':None,'newFocusId':None},'supplementalReferences':[{'label':'public_corridor_flood','role':'Conditional production reference only','condition':'Flooded public corridor: water over carpet, open hatch, attendant, fallen floating WET FLOOR sign','nodeIds':['hotel_flooded_public_corridor'],'native':rec(flood),'preview4x':rec('previews/CH4-NEW-04-public-corridor-flood-v01-4x.png'),'runtimeBinding':None,'newFocusId':None,'newSceneKey':None,'newFlag':None}],'floodChangedNativePixels':n,'floodUnchangedPercent':round(100*(1-n/(314*206)),3),'sourceDerived':True,'whollyIndependentNativeAuthorship':False,'methodRecord':'evidence/native-construction.json','nativeLayerRecipe':'source/native_scene.py','sources':[rec('originals/CH4-NEW-04-detailed-reference.png'),rec('originals/CH4-NEW-04-pixel-friendly-study.png')],'prompts':['source/detailed-reference-prompt.txt','source/pixel-friendly-prompt.txt'],'generationTool':'Built-in image_gen; two retained source studies','sourceTransferDiagnosticIsNotProduction':True,'productionSelectionsModified':False,'narrativeGameplayBindingsModified':False,'approvalPending':'Nate visual selection'}
 (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 def fig(title,one,four):
  w,h=Image.open(ROOT/one).size
  return f'<section class="figure"><h3>{html.escape(title)}</h3><nav><button data-scale="1">Native 1×</button><button data-scale="4">Exact 4×</button><a href="{one}">PNG</a><a href="{four}">4× PNG</a></nav><div class="raster"><img src="{one}" data-one="{one}" data-four="{four}" data-w="{w}" data-h="{h}" width="{w}" height="{h}" alt="{html.escape(title)}"></div></section>'
 css='body{margin:0;background:#142820;color:#efe5c8;font:16px/1.5 system-ui,sans-serif}main{padding:22px}header,article{padding:20px;border:1px solid #647466;margin-bottom:26px}h1,h2,h3{margin:0 0 12px}a{color:#bce0c9;margin-right:16px}nav{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0}button{padding:10px;background:#435e4d;border:1px solid #b7c8ac;color:#f4e9ca;cursor:pointer}.figure{padding:14px;margin:20px 0;background:#294136}.raster{overflow:auto;max-width:100%;background:#253b32}.raster img{display:block;max-width:none!important;image-rendering:pixelated}code{overflow-wrap:anywhere}'
 body='<article id="dry"><h2>CH4-NEW-04 · dry master · UNSELECTED</h2>'+fig('Dry corridor',dry,'previews/CH4-NEW-04-public-corridor-v01-4x.png')+f'<p>SHA-256 <code>{manifest["asset"]["native"]["sha256"]}</code></p></article>'
 body+='<article id="flood"><h2>Localized flood · supplemental reference · UNSELECTED</h2>'+fig('Flood reference',flood,'previews/CH4-NEW-04-public-corridor-flood-v01-4x.png')+f'<p>Same camera and architecture. {manifest["floodUnchangedPercent"]}% of scene pixels stay exact; all changes confined to floor, hatch, attendant and sign. No new scene key, Focus ID, flag or runtime binding.</p></article>'
 body+='<article id="comparisons"><h2>Native / exact4× comparisons</h2>'
 for title,name in [('Dry / flood','dry-flood'),('Chapter2 benchmarks','chapter2-benchmarks'),('Chapter4 benchmarks','chapter4-benchmarks'),('Flood and approved environments','state-benchmarks'),('Source diagnostic / native interpretation','source-native'),('Staff door and hatch states','staff-hatch-states'),('Collection stairs unchanged','stairs-states'),('Water and floating sign','water-sign-states')]:body+=fig(title,f'comparisons/{name}-native.png',f'comparisons/{name}-4x.png')
 body+='</article><article id="benchmarks"><h2>Actual approved canonical references</h2>'
 for ref in refs:
  p=Path(ref['file']);body+=fig(p.stem,ref['file'],'previews/'+p.stem+'-4x.png')
 body+='</article>'
 header='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>B2-11 v01 public corridor review</title><style>'+css+'</style><main><header><h1>Chapter4 B2-11 v01 · public corridor</h1><p><strong>Everything UNSELECTED. Nate’s visual approval is pending.</strong> One dry314×206 scene plus one conditional flooded reference, each with exact1256×824 nearest-neighbor4×. Main incorporated at <code>5a4290d672e1904b4b5ad361562f05168c328a50</code>.</p><p>Staff door, recessed collection stair and bright side exit retain the same perspective in both frames. The flooded state adds shallow water over carpet, an open maintenance hatch, a simplified attendant and the floating WET FLOOR sign.</p><p>SOURCE-DERIVED native structural/material interpretation. Reference-informed local shading is disclosed; not wholly independent authorship. No simple downscale is presented as the final image. Main, approved artwork, narrative/gameplay and PR32 are unchanged.</p><nav><a href="manifest.json">Manifest / hashes</a><a href="README.md">Method / scope</a><a href="evidence/validation.json">QA / preservation</a><a href="evidence/visual-review.md">Visual assessment</a><a href="source/detailed-reference-prompt.txt">Detailed prompt</a><a href="source/pixel-friendly-prompt.txt">Style-study prompt</a><a href="originals/CH4-NEW-04-detailed-reference.png">Detailed original</a><a href="originals/CH4-NEW-04-pixel-friendly-study.png">Pixel-friendly original</a><a href="comparisons/dry-flood-4x.png">Dry / flood4× PNG</a></nav></header>'
 script='<script>document.querySelectorAll("button[data-scale]").forEach(b=>b.onclick=()=>{const i=b.closest("section.figure").querySelector("img"),s=Number(b.dataset.scale);i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;});</script></main></html>'
 (ROOT/'index.html').write_text(header+body+script)
 print(json.dumps({'status':'UNSELECTED','primary':1,'supplemental':1,'floodChanges':n,'floodUnchangedPercent':manifest['floodUnchangedPercent']}))
if __name__=='__main__':main()
