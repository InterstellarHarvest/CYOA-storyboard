"""Package final candidates and comparisons. Does not author native scenes."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json,html

ROOT=Path(__file__).resolve().parent.parent
REVIEW=ROOT.parent
ASSETS=[
 ('CH4-03','Auctioneer — preferred style','native/CH4-03-auctioneer-source-derived-v06.png','SOURCE-DERIVED PORTRAIT · 564×278','../portrait-study-02/diagnostics/CH4-03-layout-only-source-derived-564x278.png','Preferred study diagnostic','../v04/references/pavilion_attendant_idle.png','Pavilion attendant','../portrait-study-02/generated/CH4-03-auctioneer-fresh-style-original.png'),
 ('CH4-04','Public restroom','native/CH4-04-restroom-v02.png','HYBRID SCENE · SOURCE-DERIVED NPCs · 314×206','../v01/native/CH4-04-restroom-v01.png','Preserved v01','../v02/references/scenes__biology_park__conveniences_bureau.png','Chapter 2 Bureau','detailed/CH4-04-reference-v02.png'),
 ('CH4-05','Ballroom','native/CH4-05-ballroom-v02.png','HYBRID SCENE · SOURCE-DERIVED NPCs · 314×206','../v01/native/CH4-05-ballroom-v01.png','Preserved v01','../v02/references/scenes__biology_park__control_tower.png','Chapter 2 Control Tower','detailed/CH4-05-reference-v02.png'),
]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def record(rel):
 p=ROOT/rel
 with Image.open(p) as im:
  r={'file':rel,'dimensions':list(im.size),'mode':im.mode,'sha256':sha(p)}
  r['alphaExtrema']=list(im.getchannel('A').getextrema()) if im.mode=='RGBA' else [255,255]
 return r
def checker(size):
 im=Image.new('RGB',size,'#263a38');d=ImageDraw.Draw(im)
 for y in range(0,size[1],8):
  for x in range(0,size[0],8):
   if (x//8+y//8)%2:d.rectangle((x,y,x+7,y+7),fill='#3b5048')
 return im
def four(src,dst):
 im=Image.open(ROOT/src);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/dst)
def sheet(items,dst,columns=2):
 ims=[Image.open(ROOT/r).convert('RGBA') for _,r in items];w=max(i.width for i in ims);h=max(i.height for i in ims)
 im=Image.new('RGB',(columns*(w+24),((len(ims)+columns-1)//columns)*(h+58)),'#1a2b2b');d=ImageDraw.Draw(im);font=ImageFont.load_default(size=14)
 for i,((title,_),art) in enumerate(zip(items,ims)):
  x=i%columns*(w+24)+12;y=i//columns*(h+58)+12;d.text((x,y),title,font=font,fill='#f1dfb8')
  b=checker(art.size);b.paste(art,(0,0),art);im.paste(b,(x,y+34))
 im.save(ROOT/dst);four(dst,dst.replace('.png','-4x.png'))

def main():
 for name in ['previews','comparisons']:(ROOT/name).mkdir(exist_ok=True)
 portrait=Image.open(ROOT/ASSETS[0][2]).convert('RGBA')
 bg=Image.open(REVIEW/'v05/native/CH4-02-auctioneer-background-v05.png').convert('RGBA')
 Image.alpha_composite(bg,portrait).save(ROOT/'previews/auctioneer-over-frozen-v05.png')
 four('previews/auctioneer-over-frozen-v05.png','previews/auctioneer-over-frozen-v05-4x.png')
 # Inspection mattes expose cutout fringe without modifying the foreground.
 mattes=[]
 for name,color in [('dark','#182727'),('light','#f4e9cb')]:
  im=Image.new('RGBA',portrait.size,color);im=Image.alpha_composite(im,portrait);rel='previews/portrait-alpha-'+name+'.png';im.save(ROOT/rel);four(rel,rel.replace('.png','-4x.png'));mattes.append((name,rel))
 approvals=[('Pavilion attendant','../v04/references/pavilion_attendant_idle.png'),('Pavilion presenter','../v04/references/pavilion_presenter_idle.png'),('Receptionist','../v02/references/portraits__receptionist__receptionist_idle.png')]
 for title,path in approvals:four(path,'previews/approved-'+title.lower().replace(' ','-')+'-4x.png')
 refs=[('Bureau','../v02/references/scenes__biology_park__conveniences_bureau.png'),('Control Tower','../v02/references/scenes__biology_park__control_tower.png'),('Spore Garden','../v02/references/scenes__biology_park__spore_garden.png'),('Tour Tram','../v02/references/scenes__biology_park__tour_tram.png')]
 for title,path in refs:four(path,'previews/approved-'+title.lower().replace(' ','-')+'-4x.png')
 # Actual final scene-pixel crops against the exact scene NPC examples supplied
 # by Nate. This is an inspection sheet, not a new character-art derivative.
 npc_panels=[('New plumbers','native/CH4-04-restroom-v02.png',(24,117,134,189)),('New musicians','native/CH4-05-ballroom-v02.png',(48,70,141,133)),('New organizer','native/CH4-05-ballroom-v02.png',(194,76,233,157)),('New porters','native/CH4-05-ballroom-v02.png',(243,78,307,139)),('Approved presenter','references/approved-pavilion-urgency_stage.png',(73,85,114,154)),('Approved attendant','references/approved-pavilion-courtesy_stage.png',(199,91,242,145))]
 npc_sheet=Image.new('RGB',(480,280),'#1a2b2b');nd=ImageDraw.Draw(npc_sheet);font=ImageFont.load_default(size=13)
 for i,(label,rel,box) in enumerate(npc_panels):
  x=(i%3)*160+12;y=(i//3)*140+12;nd.text((x,y),label,font=font,fill='#f1dfb8')
  art=Image.open(ROOT/rel).crop(box).convert('RGB');npc_sheet.paste(art,(x,y+30))
 npc_sheet.save(ROOT/'comparisons/scene-npcs-vs-approved.png');four('comparisons/scene-npcs-vs-approved.png','comparisons/scene-npcs-vs-approved-4x.png')
 sheets=[];assets=[]
 requirements=json.loads((ROOT/'evidence/canonical-requirements.json').read_text())
 for id_,title,native,method,prior,priorLabel,benchmark,benchmarkLabel,detail in ASSETS:
  preview='previews/'+id_+'-candidate-4x.png';old4='previews/'+id_+'-previous-4x.png';four(native,preview);four(prior,old4)
  if id_=='CH4-03':
   panels=[('v06 - source-derived, cleaned',native),('Preferred study - NN diagnostic',prior),('Approved Pavilion attendant',approvals[0][1]),('Approved Pavilion presenter',approvals[1][1])]
  else:panels=[('v02 - native room + derived NPCs',native),('Preserved v01',prior),('Approved Chapter 2 Bureau',refs[0][1]),('Approved Chapter 2 Control Tower',refs[1][1])]
  comparison='comparisons/'+id_+'-candidate-history-approved.png';sheet(panels,comparison);sheets.extend([record(comparison),record(comparison.replace('.png','-4x.png'))])
  assets.append({'id':id_,'title':title,'status':'UNSELECTED','method':method,'native':record(native),'preview4x':record(preview),'previous':record(prior),'previousPreview4x':record(old4),'benchmark':record(benchmark),'detailedReference':record(detail),'comparison':record(comparison),'comparison4x':record(comparison.replace('.png','-4x.png')),'sourceNodeIds':requirements[id_]['sourceNodeIds'],'canonicalRequirements':'evidence/canonical-requirements.json','independentlyAuthoredAtNativeResolution':False,'backgroundIndependentlyAuthoredAtNativeResolution':id_!='CH4-03','editableSource':['source/portrait.py'] if id_=='CH4-03' else ['source/'+('restroom' if id_=='CH4-04' else 'ballroom')+'.py','source/scene_tools.py','source/scene_people.py']})
 frozen=json.loads((REVIEW/'portrait-study-02/evidence/frozen-environments.json').read_text());(ROOT/'evidence/frozen-environments.json').write_text(json.dumps(frozen,indent=2)+'\n')
 manifest={'review':'Chapter 4 v06 — quality-first auctioneer; resumed environments v02','status':'UNSELECTED','branch':'art/ch4-batch01-review-20261121','canonicalMain':'d9b6b91604b72115c5402253f00924665e957727','baseCommit':'2a267beaf182fa6b589d7256ae813de8b168e63a','policy':'../PRODUCTION-POLICY.md','sourceDerivedPortraitException':'AUTHORIZED by Nate; final selection pending','assets':assets,'approvedPortraitReferences':[record(p) for _,p in approvals],'approvedChapter2References':[record(p) for _,p in refs],'frozenEnvironments':frozen,'composite':record('previews/auctioneer-over-frozen-v05.png'),'composite4x':record('previews/auctioneer-over-frozen-v05-4x.png'),'comparisons':sheets,'portraitDerivation':'evidence/portrait-derivation.json','environmentGenerationReceipts':'evidence/environment-generation-receipts.json','sceneNPCGenerationReceipts':'evidence/scene-npc-generation-receipts.json','sceneNPCDerivation':'evidence/scene-npc-derivation.json','backgrounds':[record('backgrounds/CH4-04-restroom-background-v02.png'),record('backgrounds/CH4-05-ballroom-background-v02.png')],'sceneNPCReferences':[record('references/approved-pavilion-courtesy_stage.png'),record('references/approved-pavilion-urgency_stage.png')],'pillowVersion':Image.__version__,'knownLimitations':['All candidates remain unselected; technical QA does not establish artistic approval.','The portrait is honestly source-derived under the revised policy, not an independently authored native reconstruction.','Native room writers simplify the architectural studies into material clusters; illustrated NPCs are separately source-derived. Fine surface nuance is less extensive than the large studies.','The restroom reference shows four basins; native reconstruction intentionally corrects this to three.','Only entry/pre-flood restroom and establishing ballroom are depicted; no active crane/flood or private bridal lavatory.','The optional independent-illustrator handoff is archival and no longer blocks the authorized portrait workflow.']}
 (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 cards=[]
 for a,spec in zip(assets,ASSETS):
  id_,title,native,method,prior,priorLabel,benchmark,benchmarkLabel,detail=spec;w,h=a['native']['dimensions']
  if id_=='CH4-03':options=approvals[:2];bench4='previews/approved-pavilion-attendant-4x.png'
  else:options=refs;bench4='previews/approved-'+benchmarkLabel.replace('Chapter 2 ','').lower().replace(' ','-')+'-4x.png'
  opts=''.join('<option value="'+p+'" data-four="previews/approved-'+name.lower().replace(' ','-')+'-4x.png"'+(' selected' if p==benchmark else '')+'>'+name+'</option>' for name,p in options)
  columns=[]
  for role,label,one,four_ in [('candidate','Candidate - UNSELECTED',native,a['preview4x']['file']),('previous',priorLabel,prior,a['previousPreview4x']['file']),('benchmark',benchmarkLabel,benchmark,bench4)]:
   columns.append(f'<div class="column"><h3 class="{role}-label">{label}</h3><div class="viewport checker"><img class="{role} art" data-target="{id_}" data-one="{one}" data-four="{four_}" data-width="{w}" data-height="{h}" src="{one}" width="{w}" height="{h}" alt="{title}: {label}"></div></div>')
  note=('The original preferred illustration is reduced using premultiplied-alpha Lanczos; only cutout-edge specks are cleaned. Face, hair, hands, suit, expression and pose are retained. Source-derived under the recorded policy, not independently native-authored.' if id_=='CH4-03' else 'Hybrid scene: independently native-drawn room background plus source-derived illustrated people matching the owner-supplied approved Pavilion scene NPCs. Compare actual face/hair/hand/cloth finish, perspective, lighting and human scale.')
  cards.append(f'''<article id="{id_}"><h2>{html.escape(title)}</h2><p class="tag">{method} · UNSELECTED</p><p>{note}</p><div class="actions"><button class="scale" data-target="{id_}" data-scale="1">Native 1×</button><button class="scale" data-target="{id_}" data-scale="4">Exact 4×</button><label>Approved benchmark <select class="benchmark-select" data-target="{id_}">{opts}</select></label><a href="{native}">Candidate PNG</a><a href="{a['comparison']['file']}">Comparison PNG</a><a href="{a['comparison4x']['file']}">4× comparison PNG</a></div><div class="comparisons">{''.join(columns)}</div><details><summary>Unchanged detailed reference / generation source</summary><p><a href="{detail}">Original PNG</a> — {a['detailedReference']['dimensions'][0]}×{a['detailedReference']['dimensions'][1]}; preserved unchanged.</p><div class="viewport"><img class="art" src="{detail}" width="{a['detailedReference']['dimensions'][0]}" height="{a['detailedReference']['dimensions'][1]}" alt="Preserved detailed reference for {title}" loading="lazy"></div></details></article>''')
 page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 4 v06 · auctioneer and environments</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#15262a;color:#eee4d1;font:16px/1.55 system-ui,sans-serif}main{max-width:1840px;margin:auto;padding:28px}h1{font-size:clamp(1.7rem,3vw,2.5rem);line-height:1.2}h2{font-size:1.4rem}h3{font-size:1rem}.intro,article,.panel{padding:22px;background:#20373a;border:1px solid #4a6863;border-radius:8px;margin:24px 0}.tag{font-weight:700;color:#edc48d}.actions{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin:15px 0}button,select{padding:8px 12px;background:#355751;color:#fff1d4;border:1px solid #91a18c;border-radius:4px}button{cursor:pointer}a{color:#b0e1cc}.comparisons{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.column{min-width:0}.viewport{overflow:auto;max-width:100%;max-height:850px;border:1px solid #58756b}.art{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}.checker{background-color:#263a38;background-image:linear-gradient(45deg,#3b5048 25%,transparent 25%),linear-gradient(-45deg,#3b5048 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#3b5048 75%),linear-gradient(-45deg,transparent 75%,#3b5048 75%);background-size:16px 16px;background-position:0 0,0 8px,8px -8px,-8px 0}details{margin-top:18px}code{overflow-wrap:anywhere}button:focus-visible,a:focus-visible,select:focus-visible{outline:3px solid #edd49a}@media(max-width:1000px){.comparisons{grid-template-columns:1fr}}@media(max-width:600px){main{padding:12px}.intro,article,.panel{padding:14px}}
</style></head><body><main><header><p>Out of Order · Chapter 4 · Batch 1</p><h1>Auctioneer v06 · restroom and ballroom v02</h1><p class="tag">ALL CANDIDATES UNSELECTED</p></header><section class="intro"><p>The preferred auctioneer is now a production-resolution, transparently <strong>source-derived</strong> candidate under Nate's revised quality-first policy. The environments combine native-authored room backgrounds with separately illustrated source-derived NPCs. The complete frames are honestly labelled hybrid art; rejected code-drawn people are not used.</p><p><strong>Frozen:</strong> v05 lobby and portrait background are unchanged owner-review candidates. Preferred direction does not register artwork approval.</p><p><a href="../PRODUCTION-POLICY.md">Recorded production policy</a> · <a href="evidence/production-policy-decision.json">Exception authorized; selection pending</a> · <a href="evidence/portrait-derivation.json">Portrait derivation / edge cleanup</a> · <a href="evidence/scene-visual-qa.json">Perspective / human-scale / visual QA</a> · <a href="evidence/scene-npc-derivation.json">Scene NPC derivation</a> · <a href="comparisons/scene-npcs-vs-approved.png">Scene NPC comparison PNG</a> · <a href="manifest.json">Manifest and hashes</a> · <a href="evidence/validation.json">Validation</a></p></section><nav><a href="#CH4-03">Auctioneer</a> · <a href="#composite">Frozen-background composite</a> · <a href="#CH4-04">Restroom</a> · <a href="#CH4-05">Ballroom</a> · <a href="#frozen">Frozen files</a></nav>__PORTRAIT__<section class="panel" id="composite"><h2>Auctioneer over the frozen v05 background</h2><p>Foreground candidate composited over the exact preserved background; only this review preview is newly exported.</p><div class="actions"><a href="previews/auctioneer-over-frozen-v05.png">Native composite PNG</a><a href="previews/auctioneer-over-frozen-v05-4x.png">Exact 4× composite PNG</a><a href="previews/portrait-alpha-dark-4x.png">Dark-matte edge check</a><a href="previews/portrait-alpha-light-4x.png">Light-matte edge check</a></div><div class="viewport"><img class="art composite" src="previews/auctioneer-over-frozen-v05.png" width="564" height="278" alt="Candidate auctioneer over unchanged frozen v05 background"></div></section>__ROOMS__<section class="panel" id="frozen"><h2>Preserved owner-review files</h2><p><a href="../v05/native/CH4-01-lobby-v05.png">Frozen v05 lobby PNG</a> · <a href="../v05/native/CH4-02-auctioneer-background-v05.png">Frozen v05 portrait-background PNG</a> · <a href="evidence/frozen-environments.json">Exact hashes</a></p><p><a href="../portrait-study-02/index.html">Preferred original study, prompt and provenance</a> · <a href="../v05/index.html">Preserved v05 gallery</a> · <a href="CH4-03-ILLUSTRATOR-HANDOFF.md">Optional independent illustrator handoff</a> · <a href="README.md">Production notes</a></p><p>No main, production assets/workflows, narrative, gameplay or approval records have changed. The former independent-portrait block does not prevent the authorized source-derived workflow or environment production.</p></section></main><script>
document.querySelectorAll('.scale').forEach(b=>b.addEventListener('click',()=>{const a=document.getElementById(b.dataset.target),s=Number(b.dataset.scale);a.dataset.scale=s;a.querySelectorAll('.candidate,.previous,.benchmark').forEach(i=>{i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.width)*s;i.height=Number(i.dataset.height)*s;});}));
document.querySelectorAll('.benchmark-select').forEach(select=>select.addEventListener('change',()=>{const a=document.getElementById(select.dataset.target),i=a.querySelector('.benchmark'),o=select.selectedOptions[0],s=Number(a.dataset.scale||1);i.dataset.one=o.value;i.dataset.four=o.dataset.four;i.src=s===4?i.dataset.four:i.dataset.one;a.querySelector('.benchmark-label').textContent=o.textContent;}));
</script></body></html>'''
 page=page.replace('__PORTRAIT__',cards[0]).replace('__ROOMS__','\n'.join(cards[1:]));(ROOT/'index.html').write_text(page)

if __name__=='__main__':main()
