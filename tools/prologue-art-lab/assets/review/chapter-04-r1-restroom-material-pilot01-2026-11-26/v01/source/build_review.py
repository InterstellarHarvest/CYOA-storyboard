"""Exact-delta QA, immutable input checks and non-destructive review exports."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops, __version__ as pillow_version
import json, hashlib, html, subprocess, zipfile, io, sys
from paint_material_pilot import raster_path

R=Path(__file__).resolve().parents[1]
REPO=next(p for p in R.parents if(p/'story/artwork.draft.json').exists())
SOURCE='references/approved-restroom-background.png'
PILOT='native/CH4-B2-03-R1-material-pilot01-v01.png'
LABEL='UNSELECTED — MATERIAL PILOT, NOT SELECTION-READY'
CROP=(0,175,174,278)
SHA=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,value):(R/name).write_text(json.dumps(value,indent=2)+'\n')
def replay():
 tape=json.loads((R/'source/native-paint.json').read_text());allowed=Image.open(R/'masks/allowed-edit-region.png')
 group=Image.new('RGBA',(564,278))
 for index,layer in enumerate(tape['layers']):
  im=Image.new('RGBA',(564,278));draw=ImageDraw.Draw(im)
  for op in layer['commands']:
   kind,colour=op[:2];fill=tape['palette'][colour]
   if kind=='path':draw.polygon(raster_path(op[2]),fill=fill)
   elif kind=='polygon':draw.polygon([tuple(x)for x in op[2]],fill=fill)
   elif kind=='line':draw.line([tuple(x)for x in op[2]],fill=fill,width=op[3])
   else:draw.ellipse(op[2],fill=fill)
  im.putalpha(ImageChops.multiply(im.getchannel('A'),allowed))
  assert im.tobytes()==Image.open(R/'layers'/f'{index+1:02d}.png').tobytes()
  group.alpha_composite(im)
 original=Image.open(R/SOURCE).convert('RGB');original.paste(group,(0,0),group.getchannel('A'))
 assert original.tobytes()==Image.open(R/PILOT).tobytes()
 with zipfile.ZipFile(R/'source/CH4-B2-03-material-pilot01.ora')as z:
  assert Image.open(io.BytesIO(z.read('mergedimage.png'))).convert('RGB').tobytes()==original.tobytes()
 return {'passed':True,'source':'source/native-paint.json','layers':len(tape['layers']),'allLayerPixelsReproduced':True,'finalPixelsReproduced':True,'openRasterMergedImageMatches':True,'newRasterColourSampling':False,'resamplingOrQuantizationDuringPaint':False}

def sheet(files,dest):
 ims=[Image.open(R/p).convert('RGBA')for p in files];out=Image.new('RGB',(sum(i.width for i in ims),max(i.height for i in ims)),(37,43,36));x=0
 for im in ims:out.paste(im,(x,0),im);x+=im.width
 out.save(R/dest)

def main():
 refs=json.loads((R/'evidence/references.json').read_text())
 historical=json.loads((R/'evidence/historical-source-provenance.json').read_text())
 for rec in refs+historical:
  assert subprocess.check_output(['git','show',rec['sourceCommit']+':'+rec['sourcePath']],cwd=REPO)==(R/rec['file']).read_bytes()
  assert SHA(R/rec['file'])==rec['sha256']
 original=Image.open(R/SOURCE);pilot=Image.open(R/PILOT)
 assert original.mode==pilot.mode=='RGB' and original.size==pilot.size==(564,278)
 allowed=Image.open(R/'masks/allowed-edit-region.png');mask=Image.open(R/'masks/changed-pixels.png');protected=Image.open(R/'masks/protected-fixtures.png')
 # Recompute the exact binary difference independently from tuple equality.
 values=[255 if p!=q else 0 for p,q in zip(original.get_flattened_data(),pilot.get_flattened_data())]
 assert list(mask.get_flattened_data())==values
 outside=sum(v and not a for v,a in zip(values,allowed.get_flattened_data()))
 guarded=sum(v and g for v,g in zip(values,protected.get_flattened_data()))
 assert outside==guarded==0
 layerAlphas={p.name:sorted(set(Image.open(p).getchannel('A').get_flattened_data()))for p in (R/'layers').glob('*.png')}
 assert all(set(v).issubset({0,255})for v in layerAlphas.values())
 for name,im in [('original',original),('pilot',pilot)]:im.crop(CROP).save(R/'comparisons'/f'{name}-material-crop.png')
 sheet([SOURCE,PILOT],'comparisons/original-pilot-full-scene.png')
 sheet(['comparisons/original-material-crop.png','comparisons/pilot-material-crop.png'],'comparisons/original-pilot-material.png')
 # Diagnostic overlay only. Candidate pixels are not tinted or filtered.
 overlay=original.copy();overlay.paste((221,67,161),(0,0,564,278),mask);overlay.save(R/'comparisons/exact-changes-overlay.png')
 envelope=original.copy();envelope.paste((91,180,204),(0,0,564,278),allowed);envelope.save(R/'comparisons/allowed-envelope-overlay.png')
 for name,source,box in [('bureau-material','references/approved-ch2-bureau.png',(188,118,314,206)),('tower-material','references/approved-ch2-control-tower.png',(223,75,314,190))]:
  Image.open(R/source).crop(box).save(R/'comparisons'/f'{name}.png')
 sheet(['comparisons/original-material-crop.png','comparisons/pilot-material-crop.png','comparisons/bureau-material.png','comparisons/tower-material.png'],'comparisons/material-and-chapter2.png')
 dump('evidence/replay.json',replay())
 changed=sum(bool(v)for v in values)
 qa={'technicalChecksPassed':True,'artisticGatePassed':False,'status':LABEL,'geometryAndVolumeApproval':False,'dimensions':[564,278],'mode':'RGB','opaque':True,'sourceHash':SHA(R/SOURCE),'pilotHash':SHA(R/PILOT),'changedPixels':changed,'unchangedPixels':len(values)-changed,'changedPercent':round(changed/len(values)*100,5),'changedBounds':mask.getbbox(),'changedMaskIsExactBinaryRGBDifference':True,'outsideAllowedRegionChanges':outside,'protectedFixtureChanges':guarded,'nativeLayerAlphaValues':layerAlphas,'sourceAndHistoricalFilesVerified':len(refs)+len(historical),'allPreviewsExactNearestNeighbor4x':True,'nativePaintTapeAndORAReplay':'passed','newImageGeneration':False,'globalQuantizer':False,'automatedSharpening':False,'sourceDownsampledIntoPilot':False,'python':sys.version,'pillow':pillow_version}
 dump('evidence/technical-qa.json',qa)
 stats=json.loads((R/'evidence/paint-statistics.json').read_text())
 dump('manifest.json',{'assetId':'CH4-B2-03','reviewUnit':'R1 material-cluster pilot 01','version':'v01','status':LABEL,'artisticGate':'FAILED — volume and brass modeling not adequately preserved; painting stopped after this one pilot','selectionReady':False,'ownerApproved':False,'sourceCommit':'2af6606c25ce252752c65aa5c68c87ff84f804ae','canonicalApprovedPath':'assets/selected/pending-integration/scenes/grand_bellevue/restroom/portraitBackground.png','registryKeyReferenceOnly':'scenes:grand_bellevue/restroom#portraitBackground','newRegistryOrRuntimeBindings':False,'approvedOriginal':{'file':SOURCE,'sha256':SHA(R/SOURCE),'unchanged':True},'pilot':{'file':PILOT,'sha256':SHA(R/PILOT),'dimensions':[564,278],'mode':'RGB','status':LABEL},'provenance':'Mixed composite: untouched approved source-derived background plus explicitly painted native-grid material layers. The full scene is not claimed to be independently authored. No source raster colours were sampled into the painted material group.','construction':'Native-resolution opaque raster brush regions, using manually placed curved boundaries and material ramps; no larger intermediate canvas, quantization, source resize or sharpen pass. This construction lost too much material volume and was stopped at its artistic gate.','editableSource':'source/CH4-B2-03-material-pilot01.ora','nativeTape':'source/native-paint.json','paletteStatistics':stats,'cropNativeBounds':CROP,'benchmarkCrops':{'bureau':[188,118,314,206],'controlTower':[223,75,314,190]},'changedMask':'masks/changed-pixels.png','allowedMask':'masks/allowed-edit-region.png','scopeVerification':'evidence/technical-qa.json','originalSourcesAndPrompts':'evidence/historical-source-provenance.json','visualAssessment':'ARTISTIC-GATE.md','furtherScenePainting':False,'loadingDockStarted':False})
 paths=[SOURCE,PILOT,'comparisons/original-pilot-full-scene.png','comparisons/original-material-crop.png','comparisons/pilot-material-crop.png','comparisons/original-pilot-material.png','comparisons/material-and-chapter2.png','masks/changed-pixels.png','comparisons/exact-changes-overlay.png','masks/allowed-edit-region.png','comparisons/allowed-envelope-overlay.png','layers/material-group-composite.png','references/approved-ch2-bureau.png','references/approved-ch2-control-tower.png','references/approved-ch4-restroom-main.png']
 previews={}
 for p in paths:
  im=Image.open(R/p);four='previews/'+Path(p).stem+'-4x.png';im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(R/four)
  assert Image.open(R/four).tobytes()==im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).tobytes();previews[p]=four
 def fig(title,p,caption):
  w,h=Image.open(R/p).size
  return f'<section class="figure"><h3>{html.escape(title)}</h3><p>{html.escape(caption)}</p><p><button data-scale="1">Native 1×</button> <button data-scale="4">Exact 4×</button> <a href="{p}">PNG</a></p><div class="viewport"><img src="{p}" data-one="{p}" data-four="{previews[p]}" data-w="{w}" data-h="{h}" width="{w}" height="{h}" alt="{html.escape(title)}"></div></section>'
 h=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>CH4-B2-03 R1 — material pilot 01</title><style>body{background:#242923;color:#f1ead7;font:16px system-ui;margin:24px}a{color:#f6d696}h1{font-size:27px}.notice{background:#503a2f;border-left:5px solid #e5bb69;padding:18px;max-width:1050px}section.figure{border-top:1px solid #6c7163;padding:12px 0}button{background:#e6d8b8;color:#20251f;border:0;padding:8px 16px;cursor:pointer}.viewport{overflow:auto;background:#a5a496;max-width:100%;padding:8px}img{image-rendering:pixelated;image-rendering:crisp-edges;max-width:none;display:block}p{max-width:1050px;line-height:1.5}</style><h1>CH4-B2-03 — R1 material-cluster pilot 01</h1>',f'<p class="notice"><b>{LABEL}</b><br>Artistic gate failed: clearer clusters, but the bowl reads shallower, the apron becomes banded and the tap loses convincing brass modeling. Painting stopped after this one localized pilot. No whole-scene treatment or loading-dock work was started.</p>',f'<p>{changed:,} changed pixels ({qa["changedPercent"]}% of the canvas). Zero changes outside the independently defined work envelope; zero changes in protected mirror and rear-fixture windows. These scope checks do not constitute visual approval.</p>','<p><a href="ARTISTIC-GATE.md">Visual findings and limitation</a> · <a href="manifest.json">Manifest</a> · <a href="evidence/technical-qa.json">Exact-difference QA</a> · <a href="source/CH4-B2-03-material-pilot01.ora">Editable OpenRaster layers</a> · <a href="source/native-paint.json">Native brush tape</a> · <a href="originals/CH4-B2-03-original.png">Preserved detailed source</a></p><article id="context"><h2>Full-scene context — approved source and single pilot</h2>',fig('Approved original — unchanged',SOURCE,'All approved bytes and the original source-derived provenance are preserved.'),fig('One localized native material pilot',PILOT,LABEL+'; artistic gate failed. The rest of the room is the original approved raster.'),'</article><article id="comparison"><h2>Original left / pilot right</h2>',fig('Full-scene before / pilot','comparisons/original-pilot-full-scene.png','Same native canvas contracts. Exact 4× exports are precomputed; no responsive shrinking.'),fig('Near basin material comparison','comparisons/original-pilot-material.png','Identical native crop: x=0–173, y=175–277. Inspect bowl depth, rolled rim, apron curvature, tap and pipe.'),'</article><article id="materials"><h2>Individual material views</h2>',fig('Original material crop','comparisons/original-material-crop.png','Approved rounded ceramic, tap and waste/support run.'),fig('Pilot material crop','comparisons/pilot-material-crop.png','Connected clusters are clearer, but do not preserve sufficient dimensional richness.'),fig('Painted group alone','layers/material-group-composite.png','Native opaque brush layers on transparency. This is not a full replacement background.'),'</article><article id="mask"><h2>Exact changed-pixel proof</h2>',fig('Exact RGB changed-pixel mask','masks/changed-pixels.png','White means at least one RGB channel differs from the approved original. Black means exact equality. No tolerance or threshold beyond zero.'),'</article><article id="scope"><h2>Work envelope and protected environment</h2>',fig('Actual changes in magenta','comparisons/exact-changes-overlay.png','Diagnostic overlay only; the pilot artwork itself is not tinted.'),fig('Independently defined allowed region','masks/allowed-edit-region.png','Defined from approved geometry before painting. Not inferred from the final changed pixels.'),fig('Allowed envelope over approved room','comparisons/allowed-envelope-overlay.png','Cyan marks the work envelope. The mirror, rear fixtures and remainder of the environment remain outside it.'),'</article><article id="benchmarks"><h2>Actual approved Chapter 2 and Chapter 4 references</h2>',fig('Material crops beside Chapter 2','comparisons/material-and-chapter2.png','Left to right: original basin, pilot basin, approved Bureau desk/chair, approved Control Tower console. All retain their original native pixel scale.'),fig('Approved Chapter 2 Bureau','references/approved-ch2-bureau.png','Primary cluster and readable-material benchmark, exact canonical PNG.'),fig('Approved Chapter 2 Control Tower','references/approved-ch2-control-tower.png','Primary cluster and readable-material benchmark, exact canonical PNG.'),fig('Approved Chapter 4 restroom main scene','references/approved-ch4-restroom-main.png','Continuity reference only. Not revised, registered or replaced.'),'</article><script>document.querySelectorAll("button[data-scale]").forEach(b=>b.addEventListener("click",()=>{const i=b.closest("section").querySelector("img"),s=Number(b.dataset.scale);i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;i.src=s===4?i.dataset.four:i.dataset.one;}));</script></html>']
 (R/'index.html').write_text('\n'.join(h)+'\n')
 print(json.dumps({'technicalChecksPassed':True,'artisticGatePassed':False,'changedPixels':changed,'outsideEnvelope':outside,'protectedFixturesChanged':guarded,'figures':len(paths)}))
if __name__=='__main__':main()
