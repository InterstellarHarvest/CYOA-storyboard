from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,subprocess,html
ROOT=Path(__file__).resolve().parents[1];REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists())
CANON='ac2916cf077d960ee17fef5678649d594b1581d6';BASE='f6840e5d69f70435f88ce9ece720583566fce8e2'
INV='tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21/v08/BATCH2-INVENTORY.json'
CASES=[(37,'main_scene:grand_bellevue/staff_lavatory','Staff lavatory — boxed-in entry'),(38,'portrait:hotel_wedding_assistant:busy','Wedding assistant — busy'),(39,'portrait:hotel_wedding_assistant:sympathetic','Wedding assistant — sympathetic'),(40,'portrait:hotel_wedding_assistant:apologetic','Wedding assistant — apologetic'),(41,'portrait_background:grand_bellevue/staff_lavatory','Staff lavatory — closer entry background')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(rel):
 p=ROOT/rel;i=Image.open(p);return {'file':rel,'sha256':sha(p),'dimensions':list(i.size),'mode':i.mode}
def key(d):
 return 'portraits:'+d['logicalKey']if d['category']=='portrait'else 'scenes:'+d['logicalKey']+('#portraitBackground'if d['category']=='portrait_background'else'')
def main():
 inv=json.loads((REPO/INV).read_text());group=next(g for g in inv['groups']if g['id']=='B2-07');nodes=json.loads(subprocess.check_output(['git','show',CANON+':story/chapters/chapter-04.wip.json'],cwd=REPO))['nodes'];assets=[];states=[]
 for num,inventory,title in CASES:
  id_=f'CH4-B2-{num}';d=next(a for a in inv['assets']if a['inventoryId']==inventory)
  assets.append({'id':id_,'title':title,'version':'v01','inventoryId':inventory,'key':key(d),'kind':d['category'],'nodeIds':d['nodeIds'],'status':'UNSELECTED','selected':False,'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'native':rec(f'native/{id_}-v01.png'),'preview4x':rec(f'previews/{id_}-4x.png'),'detailedReference':rec(f'originals/{id_}-detailed.png'),'pixelFriendlyReference':rec(f'originals/{id_}-pixel-friendly.png')if num in[37,41]else None,'processingSource':'source/native_build.py','prompt':f'prompts/{id_}-detailed.txt'})
 for num in[37,41]:
  for state,node,condition in [('cleared','hotel_staff_lavatory_move_boxes','After the boxes are removed and the closed seat is visible for the first time: red ribbon and LOT58 tag remain. The assistant later replaces one box; this reference does not prescribe that timing.'),('permit','hotel_staff_lavatory_temporary_use_permit','Final authored beat after the SOLD ribbon is removed, lid raised and assistant places the clipboard on the seat. No use or flushing occurs.')]:
   id_=f'CH4-B2-{num}-{state}';states.append({'id':id_,'baseAssetId':f'CH4-B2-{num}','version':'v01','kind':'conditional-production-reference','status':'UNSELECTED','selected':False,'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'condition':condition,'nodeIds':[node],'canonicalKey':None,'runtimeBinding':None,'newFocusId':None,'implementationBoundary':'Conditional reference only. A later authorized gameplay/integration task must decide timing; do not infer flag dispatch, new nodes, modes or canonical IDs.','native':rec(f'native/{id_}-v01.png'),'preview4x':rec(f'previews/{id_}-4x.png'),'allowedMask':f'masks/CH4-B2-{num}-'+('entry-box-occluder.png'if state=='cleared'else'permit-toilet-allowed.png'),'sourceReference':rec(f'originals/CH4-B2-{num}-'+('permit-reference.png'if state=='permit'else'pixel-friendly.png')),'comparisonBaseId':f'CH4-B2-{num}'+(''if state=='cleared'else'-cleared')})
 for num,bg in[(38,'CH4-B2-41'),(39,'CH4-B2-41-cleared'),(40,'CH4-B2-41-permit')]:
  id_=f'CH4-B2-{num}';fg=Image.open(ROOT/f'native/{id_}-v01.png');back=Image.open(ROOT/f'native/{bg}-v01.png').convert('RGBA');c=Image.alpha_composite(back,fg).convert('RGB');one=f'previews/{id_}-composite-native.png';four=f'previews/{id_}-composite-4x.png';c.save(ROOT/one);c.resize((2256,1112),Image.Resampling.NEAREST).save(ROOT/four);a=next(a for a in assets if a['id']==id_);a['composite']={'backgroundAssetId':bg,'native':rec(one),'preview4x':rec(four),'reviewOnly':True}
 refs=json.loads((ROOT/'evidence/canonical-benchmarks.json').read_text())
 for name in refs:
  im=Image.open(ROOT/f'references/{name}.png');im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/f'previews/{name}-4x.png')
 font=ImageFont.load_default(size=14)
 def sheet(items,out):
  sizes=[Image.open(ROOT/p).size for _,p in items];w=sum(s[0]+14 for s in sizes)+10;h=max(s[1]for s in sizes)+40;s=Image.new('RGB',(w,h),'#293e37');d=ImageDraw.Draw(s);x=10
  for title,p in items:
   d.text((x,8),title.replace('—','-'),font=font,fill='#f1e2bd');im=Image.open(ROOT/p).convert('RGBA');s.paste(im,(x,30),im);x+=im.width+14
  s.save(ROOT/f'comparisons/{out}-native.png');s.resize((w*4,h*4),Image.Resampling.NEAREST).save(ROOT/f'comparisons/{out}-4x.png')
 for a in assets:
  id_=a['id'];sheet([(id_,a['native']['file']),('Approved Chapter2 Bureau','references/approved-bureau.png'),('Approved Chapter2 Tower','references/approved-tower.png')],id_+'-chapter2')
  if a['kind']=='portrait':sheet([(id_,a['native']['file']),('Approved Pavilion presenter','references/approved-presenter.png'),('Approved Pavilion attendant','references/approved-attendant.png'),('Approved Chapter4 bride','references/approved-bride.png')],id_+'-portraits')
 sheet([(a['id'],a['native']['file'])for a in assets if a['kind']=='portrait'],'assistant-poses')
 for n in[37,41]:sheet([('Entry boxes',f'native/CH4-B2-{n}-v01.png'),('Closed / sealed',f'native/CH4-B2-{n}-cleared-v01.png'),('Open / permit clipboard',f'native/CH4-B2-{n}-permit-v01.png')],f'CH4-B2-{n}-states')
 sheet([(a['id'],a['native']['file'])for a in assets],'all-primary')
 m={'title':'Chapter4 B2-07 v01 — Staff lavatory used as storage','groupId':'B2-07','status':'UNSELECTED','branch':'art/ch4-batch01-review-20261121','canonicalApprovalBaseline':CANON,'reviewPreservationBaseline':BASE,'inventorySource':INV,'primaryUnits':5,'supplementalReferenceFrames':4,'storyNodeCoverage':group['nodeIds'],'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'productionIntegrationPerformed':False,'assets':assets,'supplementalStates':states,'canonicalBenchmarks':refs,'method':'Detailed built-in imagegen references; separate environment pixel-friendly interpretation; target-grid material/cluster/structure/lettering and occlusion construction; protected source-derived portrait palettes/anatomy/silhouettes; bounded state-object references.'};(ROOT/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 (ROOT/'evidence/canonical-node-evidence.json').write_text(json.dumps({'canonicalCommit':CANON,'inventorySource':INV,'group':group,'storyFile':'story/chapters/chapter-04.wip.json','nodes':{k:nodes[k]for k in group['nodeIds']},'runtimeBindingsChanged':False},ensure_ascii=False,indent=2)+'\n')
 def fig(title,one,four):
  w,h=Image.open(ROOT/one).size
  return f'<section class="figure"><h3>{html.escape(title)}</h3><nav><button data-scale="1">Native 1×</button><button data-scale="4">Exact 4×</button><a href="{one}">PNG</a><a href="{four}">4× PNG</a></nav><div class="raster"><img src="{one}" data-one="{one}" data-four="{four}" data-w="{w}" data-h="{h}" width="{w}" height="{h}" alt="{html.escape(title)}"></div></section>'
 style=(ROOT.parent/'b2-06-v01/index.html').read_text().split('<style>')[1].split('</style>')[0];body=''
 for a in assets+states:
  id_=a['id'];primary=a in assets;title=a.get('title',id_+' — conditional reference');note='Exact canonical inventory demand.'if primary else a['condition'];body+=f'<article id="{id_}"><h2>{html.escape(title)}</h2><p><strong>UNSELECTED</strong> · {html.escape(note)}</p><p class="hash">SHA-256 {a["native"]["sha256"]}</p>'+fig('New candidate',a['native']['file'],a['preview4x']['file'])
  ref='approved-presenter'if a['kind']=='portrait'else'approved-bureau';body+=fig('Approved benchmark: '+ref,f'references/{ref}.png',f'previews/{ref}-4x.png')
  if primary:
   body+=f'<p>Canonical node coverage: {html.escape(", ".join(a["nodeIds"]))}. <a href="{a["detailedReference"]["file"]}">Detailed reference</a> · <a href="{a["prompt"]}">Exact prompt</a> · <a href="comparisons/{id_}-chapter2-native.png">Chapter2 comparison PNG</a> · <a href="comparisons/{id_}-chapter2-4x.png">Exact4× comparison PNG</a></p>'
   if a['kind']=='portrait':body+=fig('Approved Pavilion attendant','references/approved-attendant.png','previews/approved-attendant-4x.png')+fig('Approved Chapter4 bride','references/approved-bride.png','previews/approved-bride-4x.png')+fig('Chapter2 cluster/material benchmark','references/approved-bureau.png','previews/approved-bureau-4x.png')+fig('Paired authored-context composite',a['composite']['native']['file'],a['composite']['preview4x']['file'])+f'<p><a href="comparisons/{id_}-portraits-native.png">Human NPC comparison PNG</a> · <a href="comparisons/{id_}-portraits-4x.png">Exact4× PNG</a></p>'
   else:
    n=37 if id_.endswith('37')else 41;rr='approved-restroom'if n==37 else'approved-restroom-background';body+=fig('Approved same-hotel room finish',f'references/{rr}.png',f'previews/{rr}-4x.png')+f'<p><a href="comparisons/CH4-B2-{n}-states-native.png">Entry/reveal/permit comparison PNG</a> · <a href="comparisons/CH4-B2-{n}-states-4x.png">Exact4× states</a></p>'
  else:body+='<p>Conditional production reference only; no new canonical key, Focus ID, narrative node, gameplay mode or runtime binding.</p>'
  body+='</article>'
 header='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>B2-07 v01 — Storage lavatory</title><style>'+style+'</style><main><header><h1>Chapter4 B2-07 v01 · Staff lavatory used as storage</h1><p><strong>Five primary UNSELECTED candidates and four conditional reference frames.</strong> Boxed-in actual toilet, closer room background and wedding assistant busy/sympathetic/apologetic. The revealed sealed lid and final permit clipboard are authored story beats, preserved as separate references without new runtime IDs or bindings.</p><p>Rich detailed references, separate environment pixel interpretation, protected native material/structure/lettering layers and source-derived portraits. Native and exact nearest-neighbor4× views; all old approved artwork stays exact. No narrative/gameplay/engine integration.</p><nav><a href="manifest.json">Manifest/hashes</a><a href="README.md">Method and boundaries</a><a href="evidence/validation.json">QA/preservation</a><a href="evidence/visual-review.md">Visual review</a><a href="comparisons/all-primary-native.png">All five native PNG</a><a href="comparisons/assistant-poses-native.png">Three expressions PNG</a><a href="evidence/canonical-node-evidence.json">Canonical evidence</a></nav></header>'
 script='<script>document.querySelectorAll("button[data-scale]").forEach(b=>b.onclick=()=>{const i=b.closest("section.figure").querySelector("img"),s=Number(b.dataset.scale);i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;});</script></main></html>'
 (ROOT/'index.html').write_text(header+body+script)
 print('B2-07 gallery, direct comparisons, provenance and canonical mappings prepared.')
if __name__=='__main__':main()
