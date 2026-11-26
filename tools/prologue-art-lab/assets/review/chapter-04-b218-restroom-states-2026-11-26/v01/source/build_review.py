"""Validate native states, exact locality and editable sources; export review only."""
from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib,subprocess,zipfile,io,html
R=Path(__file__).resolve().parents[1];REPO=next(p for p in R.parents if(p/'story/artwork.draft.json').exists())
SHA=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
MAP={
 'restroom-active-leak-main':{'title':'Active leak — main','nodes':['hotel_restroom_plumber'],'condition':'After the metallic snap and violent-jet description; not before the burst.','beat':'Uncontained jet and ricochet; actors retain approved repair staging.'},
 'restroom-active-leak-close':{'title':'Active leak — dialogue background','nodes':['hotel_restroom_plumber','hotel_wheel_buyer_lead'],'condition':'Burst text beat, then ch4_restroom_leak=uncontained on buyer/maintenance choices.','beat':'Closer view of same leak; no new main-scene binding.'},
 'restroom-braced-main':{'title':'Temporarily braced — dribble remains','nodes':['hotel_valve_braced'],'condition':'ch4_restroom_leak=braced; ch4_plumber_helped=true from existing d6 pass.','beat':'Thin dribble, temporary seal, residual wet floor. Existing wrench/repair pose retained.'},
 'restroom-contained-main':{'title':'Contained — wet floor, no flow','nodes':['hotel_wheel_return','hotel_key_master_cabinet'],'condition':'ch4_restroom_leak=contained; ch4_restroom_water_off=true. Maintenance isolator branches also set this condition, in their existing scenes.','beat':'Shared no-flow reference; wheel fitting/key/lever operations are narrated, not separate background variants.'},
 'restroom-flood-onset-main':{'title':'Flood — initial surge','nodes':['hotel_valve_flood'],'condition':'ch4_restroom_leak=flooding from existing d6 fail.','beat':'Onset only, before the narrated floating-basket beat; not a depiction of Eddie floating while kneeling.'},
 'restroom-stall-lifting-main':{'title':'Stall lifting — toilet stays grounded','nodes':['hotel_stall_lot_claimed','hotel_stall_crane_success','hotel_stall_porter_protest'],'condition':'Authored lift event; no new flag assigned. Overlay can accompany either braced or contained water condition.','beat':'Closed enclosure partly through the hatch, four cables; floor toilet retained. No protagonist shown.'},
}
def dump(n,v):(R/n).write_text(json.dumps(v,indent=2)+'\n')
def sheet(paths,dest,cols=None):
 ims=[Image.open(R/p).convert('RGB')for p in paths]
 if cols:
  w=max(i.width for i in ims);h=max(i.height for i in ims);out=Image.new('RGB',(w*cols,h*((len(ims)+cols-1)//cols)),(38,43,36))
  for k,im in enumerate(ims):out.paste(im,((k%cols)*w,(k//cols)*h))
 else:
  out=Image.new('RGB',(sum(i.width for i in ims),max(i.height for i in ims)),(38,43,36));x=0
  for im in ims:out.paste(im,(x,0));x+=im.width
 out.save(R/dest)
def main():
 refs=json.loads((R/'evidence/references.json').read_text())
 for rec in refs:
  assert (R/rec['file']).read_bytes()==subprocess.check_output(['git','show',rec['sourceCommit']+':'+rec['sourcePath']],cwd=REPO)
  assert SHA(R/rec['file'])==rec['sha256']
 records=json.loads((R/'evidence/native-state-build.json').read_text());figures=[]
 def add(title,p,caption):
  im=Image.open(R/p);four='previews/'+Path(p).stem+'-4x.png';im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(R/four)
  assert Image.open(R/four).tobytes()==im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).tobytes()
  f={'title':title,'path':p,'four':four,'w':im.width,'h':im.height,'caption':caption};figures.append(f);return f
 mainbase='references/approved-CH4-04.png';closebase='references/approved-CH4-B2-03.png'
 mains=[mainbase]+[r['file']for r in records if r['name']!='restroom-active-leak-close']
 sheet(mains,'comparisons/main-state-progression.png',cols=3)
 progression=add('Restroom states — 3×2 native sheet','comparisons/main-state-progression.png','Row 1: approved base, active leak, braced. Row 2: contained, flood onset, lifting over contained. Braced/contained are alternatives; the sheet is not a new story sequence.')
 checks=[]
 for rec in records:
  rec.update(MAP[rec['name']]);rec.update({'runtimeBinding':None,'focusId':None,'newStoryFlag':None})
  base=Image.open(R/rec['base']).convert('RGB');out=Image.open(R/rec['file']);assert out.size==base.size and out.mode=='RGB'
  changed=Image.open(R/rec['changedMask']);allowed=Image.open(R/rec['allowedMask'])
  exact=[255 if a!=b else 0 for a,b in zip(base.get_flattened_data(),out.get_flattened_data())]
  assert exact==list(changed.get_flattened_data());assert sum(bool(v)for v in exact)==rec['changedPixels']
  assert not ImageChops.multiply(changed,ImageChops.invert(allowed)).getbbox()
  if out.size==(314,206):assert not ImageChops.multiply(changed,Image.open(R/'masks/main-source-figures-protected.png')).getbbox()
  if 'stall' in rec['name']:assert not ImageChops.multiply(changed,Image.open(R/'masks/toilet-grounded-protected.png')).getbbox()
  comp=base.convert('RGBA')
  for name in rec['layers']:comp.alpha_composite(Image.open(R/'layers'/f'{name}.png'))
  assert comp.convert('RGB').tobytes()==out.tobytes()
  with zipfile.ZipFile(R/rec['editableSource'])as z:assert Image.open(io.BytesIO(z.read('mergedimage.png'))).tobytes()==out.tobytes()
  pair='comparisons/'+rec['name']+'-before-after.png';sheet([rec['base'],rec['file']],pair)
  rec['comparison']=pair;rec['paletteRGBColours']=len(out.getcolors(out.width*out.height))
  rec['sha256']=SHA(R/rec['file']);checks.append({'name':rec['name'],'dimensions':list(out.size),'opaqueRGB':True,'sha256':rec['sha256'],'changedPixels':rec['changedPixels'],'exactDifferenceMask':True,'outsideAllowedChanges':0,'sourceFiguresProtected':True if out.width==314 else'no figures in background','layerCompositeExact':True,'openRasterCompositeExact':True})
  add(rec['title'],rec['file'],rec['condition']+' '+rec['beat'])
  add(rec['title']+' — approved left / state right',pair,'Both views retain their native contracts; exact 4× exports use nearest-neighbour only.')
  add(rec['title']+' — exact changed pixels',rec['changedMask'],'White = any RGB change from approved master. Black = exact equality. No tolerance; unrelated pixels outside the allowed mask remain untouched.')
 add('Approved closer background — reused before burst and for porter',closebase,'Nearest lifting bay is outside this closer view. No redundant stall-removal dialogue background is needed.')
 for character in ['approved-plumber-worried','approved-assistant-pleased']:
  comp=Image.open(R/'native/restroom-active-leak-close.png').convert('RGBA');comp.alpha_composite(Image.open(R/'references'/f'{character}.png').convert('RGBA'))
  file='comparisons/'+character+'-leak-composite.png';comp.convert('RGB').save(R/file)
  add(character+' — approved foreground over leak background',file,'Layering check only. Exact approved character PNG, including its original alpha; no portrait revision or alternative selection.')
 add('Lift overlay composability over temporary brace','comparisons/lifting-over-braced-proof.png','Comparison proof only, not a seventh candidate or a runtime binding. The same lifted enclosure accompanies either water outcome.')
 add('Approved Chapter 2 Bureau','references/approved-ch2-bureau.png','Actual canonical PNG, primary pixel-cluster and material-readability benchmark.')
 add('Approved Chapter 2 Control Tower','references/approved-ch2-control-tower.png','Actual canonical PNG, primary pixel-cluster and material-readability benchmark.')
 sheet(['references/approved-ch2-bureau.png',mainbase,'native/restroom-active-leak-main.png','native/restroom-flood-onset-main.png','references/approved-ch2-control-tower.png','native/restroom-stall-lifting-main.png'],'comparisons/chapter2-state-context.png',cols=3)
 add('Chapter 2 / master / conditional-state context','comparisons/chapter2-state-context.png','Row 1: Bureau, approved restroom, leak. Row 2: flood, Control Tower, lift. Same native scale; no enlargement or shrink-to-fit in this sheet.')
 dump('evidence/technical-qa.json',{'passed':True,'candidateCount':len(records),'immutableMastersVerified':len(refs),'allNativeContractsAndRGBModesPassed':True,'exactNearestNeighbor4x':True,'exactChangedPixelMasksPassed':True,'zeroOutsideAllowedChanges':True,'editableLayerAndORACompositesExact':True,'generatedReferencePixelsUsed':False,'productionOrStoryFilesChanged':False,'runtimeDispatchImplemented':False,'results':checks})
 dump('manifest.json',{'status':'UNSELECTED','reviewFamily':'B2-18/B2-19 — restroom conditional states only','canonicalBaseCommit':'2af6606c25ce252752c65aa5c68c87ff84f804ae','R1ProductionSuspended':True,'refinementDependencySupersededByOwnerForThisReview':True,'authoritativeMasters':['CH4-04 approved v07','CH4-B2-03 approved B2-01 v01'],'failedR1PixelsUsed':False,'newCandidates':records,'references':'evidence/references.json','canonicalNodeExtract':'evidence/canonical-nodes.json','reconciliation':'RECONCILIATION.md','sourceProvenance':'Source-derived approved raster masters plus native event overlays and integer relocation of approved enclosure pixels; no generated high-resolution image is reduced into a state. Water uses deliberate translucent layers, final outputs are opaque RGB.','newGeneration':'Built-in imagegen edit for reference only; exact prompt and source preserved in prompts/stall-reference.txt and originals/raised-stall-imagegen-reference.png.','generationReceipt':'evidence/generation-receipt.json','newFocusIds':False,'newRuntimeBindings':False,'newFlagsOrNodes':False,'lobbyOrLot61ProductionStarted':False,'canonicalContinuityConcern':'Restroom/fatal nodes leave toilet grounded; later hotel_upper_salvage_arrival says it is inside suspended stall. Current art follows the explicit restroom moment. No story edit or invented transport event.'})
 # Figure lookup preserves one row per artifact and makes browser QA exhaustive.
 bypath={f['path']:f for f in figures}
 def fig(path):
  f=bypath[path];return f'<section class="figure"><h3>{html.escape(f["title"])}</h3><p>{html.escape(f["caption"])}</p><p><button data-scale="1">Native 1×</button> <button data-scale="4">Exact 4×</button> <a href="{f["path"]}">PNG</a></p><div class="viewport"><img src="{f["path"]}" data-one="{f["path"]}" data-four="{f["four"]}" data-w="{f["w"]}" data-h="{f["h"]}" width="{f["w"]}" height="{f["h"]}" alt="{html.escape(f["title"])}"></div></section>'
 h=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Chapter 4 — restroom conditional states</title><style>body{background:#242923;color:#f1ead7;font:16px system-ui;margin:24px}a{color:#f6d696}h1{font-size:27px}.notice{background:#344335;border-left:5px solid #d8b969;padding:18px;max-width:1100px}.concern{background:#503e2f;padding:14px;max-width:1100px}section.figure{border-top:1px solid #6c7163;padding:12px 0}button{background:#e6d8b8;color:#20251f;border:0;padding:8px 16px;cursor:pointer}.viewport{overflow:auto;background:#a5a496;max-width:100%;padding:8px}img{image-rendering:pixelated;image-rendering:crisp-edges;max-width:none;display:block}p,table{max-width:1150px;line-height:1.5}td,th{text-align:left;border-bottom:1px solid #6c7163;padding:9px;vertical-align:top}code{word-break:break-word}</style><h1>Chapter 4 — restroom conditional-state family</h1><p class="notice"><b>Six UNSELECTED candidates.</b> Approved CH4-04 and CH4-B2-03 are the masters. R1 is suspended; neither failed study is used. Local event layers preserve the existing room, fixtures and source figures. No registration, narrative, gameplay, runtime dispatch or deployment changes.</p><p><a href="RECONCILIATION.md">Full story/state reconciliation</a> · <a href="manifest.json">Manifest and node mappings</a> · <a href="evidence/technical-qa.json">Hashes and exact-mask QA</a> · <a href="VISUAL-REVIEW.md">Visual review and limits</a> · <a href="originals/raised-stall-imagegen-reference.png">Generated reference only</a> · <a href="prompts/stall-reference.txt">Exact imagegen prompt</a></p><p class="concern"><b>Continuity issue for PMO:</b> the restroom lift/fatal nodes leave the toilet on the floor; the later mezzanine arrival says it is inside the suspended stall. These candidates follow the explicit restroom moment. No canon was changed. The flood reference captures onset before Eddie floats past; subsequent motion stays in narration.</p><table><thead><tr><th>Reference</th><th>Story coverage</th><th>Scope</th></tr></thead><tbody>']
 for rec in records:h.append('<tr><td>'+html.escape(rec['title'])+'</td><td>'+html.escape(', '.join(rec['nodes']))+'</td><td>'+html.escape(rec['beat'])+'</td></tr>')
 h+=['</tbody></table><article id="progression"><h2>Base and state progression</h2>',fig('comparisons/main-state-progression.png'),'</article>']
 for rec in records:
  aid='dialogue'if rec['name'].endswith('close')else'lifting'if'stall'in rec['name']else rec['name']
  h+=['<article id="'+aid+'"><h2>'+html.escape(rec['title'])+'</h2>',fig(rec['file']),fig(rec['comparison']),fig(rec['changedMask']),'<p><a href="'+rec['editableSource']+'">Editable native OpenRaster</a> · <a href="'+rec['allowedMask']+'">Allowed edit mask</a></p></article>']
 h+=['<article id="reuse"><h2>Reuse and composability</h2>',fig(closebase),fig('comparisons/approved-plumber-worried-leak-composite.png'),fig('comparisons/approved-assistant-pleased-leak-composite.png'),fig('comparisons/lifting-over-braced-proof.png'),'<p>The approved master-isolator Focus artwork is reused; key/lever operation remains in the existing authored Focus node. No second close-up or empty-bay state is invented.</p></article><article id="benchmarks"><h2>Approved Chapter 2 benchmarks</h2>',fig('references/approved-ch2-bureau.png'),fig('references/approved-ch2-control-tower.png'),fig('comparisons/chapter2-state-context.png'),'</article><script>document.querySelectorAll("button[data-scale]").forEach(b=>b.addEventListener("click",()=>{const i=b.closest("section").querySelector("img"),s=Number(b.dataset.scale);i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;i.src=s===4?i.dataset.four:i.dataset.one;}));</script></html>']
 (R/'index.html').write_text('\n'.join(h)+'\n');print(json.dumps({'candidates':len(records),'figures':len(figures),'technicalPassed':True}))
if __name__=='__main__':main()
