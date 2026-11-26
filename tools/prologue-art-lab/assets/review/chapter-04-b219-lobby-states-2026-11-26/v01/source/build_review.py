from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib,html,zipfile,io,subprocess
R=Path(__file__).resolve().parents[1];B=R.parent;A=B/'porter-assessment';REPO=next(p for p in R.parents if(p/'story/artwork.draft.json').exists())
SHA=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
MAP={
 'lobby-doors-removed':{'title':'Restroom doors removed','nodes':['hotel_auctioneer_arrival','hotel_restroom_entry'],'beat':'Persistent doorless lobby after the removal. The first leaf being carried away is narrated, not a separate frame.'},
 'lot61-open':{'title':'Lot 61 — open convenience pod','nodes':['hotel_lot61_pod_auction','hotel_lot61_pod_declined'],'beat':'After presentation/entrance reveal; reuse while decline/departure begins. No closed, occupied or moving-porters variants.'},
 'lot61-packed':{'title':'Lot 61 — compact case after escape','nodes':['hotel_lot61_pod_escaped'],'beat':'After folding finishes. The survived flag is set before the text sequence; do not reveal the case merely at node entry. Empty escape case: no shoe, no occupied bulge.'}}
def dump(path,obj):path.write_text(json.dumps(obj,indent=2)+'\n')
def sheet(paths,dest,cols=None):
 ims=[Image.open(R/p).convert('RGBA')for p in paths]
 if cols:
  w=max(i.width for i in ims);h=max(i.height for i in ims);out=Image.new('RGB',(w*cols,h*((len(ims)+cols-1)//cols)),(38,44,37))
  for k,im in enumerate(ims):out.paste(im,((k%cols)*w,(k//cols)*h),im)
 else:
  out=Image.new('RGB',(sum(i.width for i in ims),max(i.height for i in ims)),(38,44,37));x=0
  for im in ims:out.paste(im,(x,0),im);x+=im.width
 out.save(R/dest)
def main():
 refs=json.loads((R/'evidence/references.json').read_text());arefs=json.loads((A/'evidence/references.json').read_text())
 for root,records in [(R,refs),(A,arefs)]:
  for rec in records:
   assert (root/rec['file']).read_bytes()==subprocess.check_output(['git','show',rec['sourceCommit']+':'+rec['sourcePath']],cwd=REPO)
   assert SHA(root/rec['file'])==rec['sha256']
 original=Image.open(R/'references/approved-lobby.png');records=json.loads((R/'evidence/native-build.json').read_text());qa=[];figures=[]
 def add(title,path,caption):
  im=Image.open(R/path);four='previews/'+Path(path).stem+'-4x.png';im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(R/four)
  assert Image.open(R/four).tobytes()==im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).tobytes()
  f={'title':title,'path':path,'four':four,'w':im.width,'h':im.height,'caption':caption};figures.append(f);return f
 add('Porter over approved restroom background','../porter-assessment/comparisons/approved-porter-over-approved-background.png','ASSESSMENT ONLY. The far-right edge is not occluded, but is peripheral in the complete native portrait. PMO explicitly permits reuse; no new selectable image.')
 add('Approved background / approved porter composite','../porter-assessment/comparisons/background-and-porter.png','Same native origin, original alpha, no artwork edits. PMO reuse decision resolves the B2-18 hold.')
 add('Approved porter foreground — unchanged','../porter-assessment/references/approved-porter.png','Exact approved hotel_porter:businesslike. No portrait regeneration, palette or opacity correction.')
 allpaths=['references/approved-lobby.png']+[r['file']for r in records];sheet(allpaths,'comparisons/lobby-state-progression.png',cols=2)
 add('Lobby conditional progression — 2×2 native sheet','comparisons/lobby-state-progression.png','Row 1: approved master, doors removed. Row 2: open pod, compact escape case. Declining the demonstration does not lead to the packed state.')
 add('Approved CH4-01 — unchanged','references/approved-lobby.png','Authoritative master. All later state layers preserve its original composition, characters, fixtures and lighting outside actual event regions.')
 protected=Image.open(R/'masks/figures-furniture-protected.png')
 for rec in records:
  rec.update(MAP[rec['name']]);out=Image.open(R/rec['file']);assert out.mode=='RGB'and out.size==(314,206)
  mask=Image.open(R/rec['changedMask']);allowed=Image.open(R/rec['allowedMask']);exact=[255 if a!=b else 0 for a,b in zip(original.get_flattened_data(),out.get_flattened_data())]
  assert exact==list(mask.get_flattened_data());assert not ImageChops.multiply(mask,ImageChops.invert(allowed)).getbbox();assert not ImageChops.multiply(mask,protected).getbbox()
  comp=original.convert('RGBA')
  for n in rec['layers']:comp.alpha_composite(Image.open(R/'layers'/f'{n}.png'))
  assert comp.convert('RGB').tobytes()==out.tobytes()
  with zipfile.ZipFile(R/rec['editableSource'])as z:assert Image.open(io.BytesIO(z.read('mergedimage.png'))).tobytes()==out.tobytes()
  pair='comparisons/'+rec['name']+'-before-after.png';sheet(['references/approved-lobby.png',rec['file']],pair);rec['comparison']=pair;rec['paletteRGBColours']=len(out.getcolors(out.width*out.height))
  add(rec['title'],rec['file'],rec['beat']+' UNSELECTED.')
  add(rec['title']+' — approved left / state right',pair,'Exact native contracts; nearest-neighbour 4×. Object occlusion is an event change, not a repaint of the master.')
  add(rec['title']+' — exact RGB change mask',rec['changedMask'],'White = any changed RGB pixel against approved CH4-01; black = exact equality. No perceptual tolerance. Allowed masks and editable layers are linked below.')
  qa.append({'name':rec['name'],'sha256':SHA(R/rec['file']),'dimensions':[314,206],'mode':'RGB','changedPixels':sum(bool(v)for v in exact),'outsideAllowedChanges':0,'protectedFigureFurnitureChanges':0,'layerCompositeExact':True,'openRasterMergedPixelsExact':True})
 # Compare objects at their actual native grids; the aftermath uses another camera.
 Image.open(R/'references/approved-folded-aftermath.png').crop((112,121,243,180)).save(R/'comparisons/approved-case-detail.png')
 Image.open(R/'native/lot61-packed.png').crop((174,180,218,203)).save(R/'comparisons/new-case-detail.png')
 sheet(['comparisons/approved-case-detail.png','comparisons/new-case-detail.png'],'comparisons/case-identity.png')
 add('Approved FOLDED FOR CONVENIENCE — unchanged','references/approved-folded-aftermath.png','Fatal artwork is reused for the fatal branch. Its loose shoe and slight occupied bulge are not copied into the escape state.')
 add('Case design comparison — different camera scales','comparisons/case-identity.png','Approved death close-view left / empty lobby escape case right. No resizing. Compare gray steel, bevelled lid, two brass clasps and central dark handle; do not infer world scale from different camera crops.')
 add('Approved Chapter 2 Bureau','references/approved-ch2-bureau.png','Exact canonical benchmark for restrained clusters and object readability.')
 add('Approved Chapter 2 Control Tower','references/approved-ch2-control-tower.png','Exact canonical benchmark for equipment/metal planes and useful native detail.')
 sheet(['references/approved-ch2-bureau.png','native/lot61-open.png','references/approved-ch2-control-tower.png','native/lot61-packed.png'],'comparisons/chapter2-context.png',cols=2)
 add('Chapter 2 / B2-19 native context','comparisons/chapter2-context.png','Bureau / open pod; Control Tower / compact case. All images retain their actual native pixel scale.')
 dump(R/'evidence/technical-qa.json',{'passed':True,'candidateCount':3,'dimensionsAndOpaqueRGBPassed':True,'allExactNearestNeighbor4xPassed':True,'immutableInputsVerified':len(refs)+len(arefs),'exactRGBMasksPassed':True,'zeroOutsideAllowedChanges':True,'editableLayersAndORAExact':True,'generatedReferencePixelsUsed':False,'globalRecolouringOrQuantization':False,'results':qa})
 dump(R/'manifest.json',{'status':'UNSELECTED','family':'B2-19 lobby doors and Lot 61','canonicalBaseCommit':'3785e87506c4218a360cf7a309b2fbe690cc4546','authoritativeMaster':'CH4-01 approved lobby','masterSHA256':SHA(R/'references/approved-lobby.png'),'newCandidates':records,'runtimeBindingsAdded':False,'FocusIdsAdded':False,'flagsOrModesAdded':False,'sourceMethod':'Exact approved native lobby plus native event layers; the pod toilet is an integer native pixel copy from approved CH4-04. Packed case independently drawn on native grid using approved fatal case as design reference. Generated reference pixels are not used.','generatedReferenceReceipt':'evidence/generation-receipt.json','referenceLabelExcluded':'Generated OUT OF ORDER label was not canonical; native image has only a warning pictogram, canonical wording stays in narration.','reconciliation':'RECONCILIATION.md','B218Resolution':'Approved CH4-B2-03 reused for hotel_stall_porter_protest per explicit PMO decision; no background modifications. Assessment only in ../porter-assessment/.','continuityBlockers':[]})
 lookup={f['path']:f for f in figures}
 def fig(path):
  f=lookup[path];return f'<section class="figure"><h3>{html.escape(f["title"])}</h3><p>{html.escape(f["caption"])}</p><p><button data-scale="1">Native 1×</button> <button data-scale="4">Exact 4×</button> <a href="{f["path"]}">PNG</a></p><div class="viewport"><img src="{f["path"]}" data-one="{f["path"]}" data-four="{f["four"]}" data-w="{f["w"]}" data-h="{f["h"]}" width="{f["w"]}" height="{f["h"]}" alt="{html.escape(f["title"])}"></div></section>'
 h=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Chapter 4 B2-19 — lobby doors and Lot 61</title><style>body{background:#242923;color:#f1ead7;font:16px system-ui;margin:24px}a{color:#f6d696}h1{font-size:27px}.notice{background:#344335;border-left:5px solid #d8b969;padding:18px;max-width:1100px}section.figure{border-top:1px solid #6c7163;padding:12px 0}button{background:#e6d8b8;color:#20251f;border:0;padding:8px 16px;cursor:pointer}.viewport{overflow:auto;background:#a5a496;max-width:100%;padding:8px}img{image-rendering:pixelated;image-rendering:crisp-edges;max-width:none;display:block}p,table{max-width:1150px;line-height:1.5}td,th{text-align:left;border-bottom:1px solid #6c7163;padding:9px;vertical-align:top}</style><h1>Chapter 4 B2-19 — lobby door removal and Lot 61</h1><p class="notice"><b>Three UNSELECTED conditional-state candidates.</b> Approved CH4-01 is unchanged. Doors stay removed in both pod states. B2-18 PMO decision: reuse the approved restroom dialogue background with the approved porter; the assessment below creates no selectable artwork. No main, registration, narrative, gameplay, engine or deployment changes.</p><p><a href="RECONCILIATION.md">Minimum-state/node mapping and PMO handoff</a> · <a href="manifest.json">Manifest and hashes</a> · <a href="evidence/technical-qa.json">Exact-mask QA</a> · <a href="../porter-assessment/ASSESSMENT.md">Porter reuse assessment</a> · <a href="originals/pod-imagegen-reference.png">Generated reference only</a> · <a href="prompts/pod-reference.txt">Exact reference prompt</a></p><table><thead><tr><th>State</th><th>Authored coverage</th><th>Timing / reuse</th></tr></thead><tbody>']
 for rec in records:h.append('<tr><td>'+html.escape(rec['title'])+'</td><td>'+html.escape(', '.join(rec['nodes']))+'</td><td>'+html.escape(rec['beat'])+'</td></tr>')
 h+=['</tbody></table><article id="assessment"><h2>B2-18 porter/background assessment — PMO reuse accepted</h2>',fig('../porter-assessment/comparisons/approved-porter-over-approved-background.png'),fig('../porter-assessment/comparisons/background-and-porter.png'),fig('../porter-assessment/references/approved-porter.png'),'</article><article id="progression"><h2>Approved base and minimum states</h2>',fig('comparisons/lobby-state-progression.png'),fig('references/approved-lobby.png'),'</article>']
 for rec in records:h+=['<article id="'+rec['name']+'"><h2>'+html.escape(rec['title'])+'</h2>',fig(rec['file']),fig(rec['comparison']),fig(rec['changedMask']),'<p><a href="'+rec['editableSource']+'">Editable native OpenRaster</a> · <a href="'+rec['allowedMask']+'">Allowed edit region</a></p></article>']
 h+=['<article id="case-identity"><h2>Approved case identity and fatal reuse</h2>',fig('references/approved-folded-aftermath.png'),fig('comparisons/case-identity.png'),'</article><article id="benchmarks"><h2>Actual approved Chapter 2 comparisons</h2>',fig('references/approved-ch2-bureau.png'),fig('references/approved-ch2-control-tower.png'),fig('comparisons/chapter2-context.png'),'</article><script>document.querySelectorAll("button[data-scale]").forEach(b=>b.addEventListener("click",()=>{const i=b.closest("section").querySelector("img"),s=Number(b.dataset.scale);i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;i.src=s===4?i.dataset.four:i.dataset.one;}));</script></html>']
 (R/'index.html').write_text('\n'.join(h)+'\n');print(json.dumps({'candidates':3,'figures':len(figures),'technicalPassed':True,'assessment':'PMO reuse accepted; no new selectable image'}))
if __name__=='__main__':main()
