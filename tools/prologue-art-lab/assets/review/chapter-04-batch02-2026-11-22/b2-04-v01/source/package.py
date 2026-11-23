"""Publishable review package: seven primary units, three supplemental state frames."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,html
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(rel):
 p=ROOT/rel;im=Image.open(p);return {'file':rel,'sha256':sha(p),'dimensions':list(im.size),'mode':im.mode}
def main():
 inv=json.loads((ROOT/'evidence/inventory-source.json').read_text());plan=json.loads((ROOT/'evidence/state-plan.json').read_text());assets=[]
 titles=['Service passage — Lot31 at collection','Porter — businesslike','Porter — uncertain','Porter — practical','Service-passage conversation background','Auction armrest — ring caught','Collection armrest — ring caught']
 for i,item in enumerate(x for x in inv['assets']if x['category']!='state_family'):
  n=i+19;id_=f'CH4-B2-{n:02}';kind={'main_scene':'scene','portrait':'portrait','portrait_background':'portrait-background','focus_a':'focus'}[item['category']]
  key='scenes:'+item['logicalKey']if kind=='scene'else'portraits:'+item['logicalKey']if kind=='portrait'else'scenes:'+item['logicalKey']+'#portraitBackground'if kind=='portrait-background'else'focus:'+item['logicalKey']
  detailed=f'originals/{id_}-detailed-v02.png'if n==20 else f'originals/{id_}-detailed.png'
  assets.append({'id':id_,'title':titles[i],'key':key,'inventoryId':item['inventoryId'],'kind':kind,'unitType':'primary','nodeIds':item['nodeIds'],'status':'UNSELECTED','selected':False,'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'native':rec(f'native/{id_}-v01.png'),'preview4x':rec(f'previews/{id_}-4x.png'),'detailedReference':rec(detailed),'pixelFriendlySource':rec(f'originals/{id_}-pixel-friendly.png')if n not in[20,21,22]else None,'layers':[str(p.relative_to(ROOT))for p in sorted((ROOT/'layers').glob(id_+'*.png'))],'masks':[str(p.relative_to(ROOT))for p in sorted((ROOT/'masks').glob(id_+'*.png'))]})
  if kind=='portrait':assets[-1]['authoredSceneKeys']=item['sceneKeys']
 for s in plan['states']:
  base=next(a for a in assets if a['id']==s['baseAssetId']);id_=s['id']
  layers=['layers/CH4-B2-24-open-native-object.png']if id_.endswith('open')else['layers/CH4-B2-25-ring-removed.png']+(['layers/CH4-B2-25-slipped-ring.png']if id_.endswith('slipped')else[])
  assets.append({'id':id_,'title':s['title'],'key':None,'baseFocusKey':'focus:'+s['baseFocusKey'],'baseAssetId':s['baseAssetId'],'inventoryId':'state_family:chair_and_ring_states','kind':'focus-state','unitType':'supplemental-state','nodeIds':s['nodeIds'],'status':'UNSELECTED','selected':False,'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'runtimeBindingInstalled':False,'authoredEvidence':s,'native':rec(f'native/{id_}-v01.png'),'preview4x':rec(f'previews/{id_}-4x.png'),'detailedReference':base['detailedReference'],'pixelFriendlySource':base['pixelFriendlySource'],'layers':layers,'masks':['masks/CH4-B2-24-open-allowed.png']if id_.endswith('open')else['masks/CH4-B2-25-states-allowed.png']})
 for p in (ROOT/'references').glob('*.png'):
  im=Image.open(p)
  if im.width>564 or im.height>278:continue
  im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/'previews'/(p.stem+'-4x.png'))
 bg=Image.open(ROOT/'native/CH4-B2-23-v01.png').convert('RGBA')
 for n in[20,21,22]:
  fg=Image.open(ROOT/f'native/CH4-B2-{n}-v01.png').convert('RGBA');c=Image.alpha_composite(bg,fg);c.save(ROOT/f'previews/CH4-B2-{n}-composite.png');c.resize((2256,1112),Image.Resampling.NEAREST).save(ROOT/f'previews/CH4-B2-{n}-composite-4x.png')
  for name,color in [('light','#f0e6ce'),('dark','#182a24')]:Image.alpha_composite(Image.new('RGBA',fg.size,color),fg).save(ROOT/f'previews/CH4-B2-{n}-alpha-{name}.png')
  context='restroom'if n==20 else'lobby';approved=Image.open(ROOT/f'references/approved-{context}-conversation.png').convert('RGBA');c=Image.alpha_composite(approved,fg);c.save(ROOT/f'previews/CH4-B2-{n}-{context}-composite.png');c.resize((2256,1112),Image.Resampling.NEAREST).save(ROOT/f'previews/CH4-B2-{n}-{context}-composite-4x.png')
 font=ImageFont.load_default(size=15);sheet=Image.new('RGB',(1164,1600),'#253b34');d=ImageDraw.Draw(sheet)
 for i,a in enumerate(assets):
  x=10+(i%2)*582;y=10+(i//2)*318;d.text((x,y),a['id']+' '+a['title'],font=font,fill='#f0dfbd');im=Image.open(ROOT/a['native']['file']).convert('RGBA');c=Image.alpha_composite(Image.new('RGBA',im.size,'#40554a'),im);sheet.paste(c.convert('RGB'),(x,y+28))
 sheet.save(ROOT/'comparisons/all-native.png');sheet.resize((4656,6400),Image.Resampling.NEAREST).save(ROOT/'comparisons/all-4x.png')
 for a in assets:
  name='approved-groundkeeper'if a['kind']=='portrait'else'approved-bureau';candidate=Image.open(ROOT/a['native']['file']).convert('RGBA');benchmark=Image.open(ROOT/f'references/{name}.png').convert('RGBA');w=candidate.width+benchmark.width+30;h=max(candidate.height,benchmark.height)+45;im=Image.new('RGBA',(w,h),'#40554a');dr=ImageDraw.Draw(im);dr.text((10,8),a['id']+' UNSELECTED',font=font,fill='#f0dfbd');dr.text((candidate.width+20,8),'Approved Chapter 2',font=font,fill='#f0dfbd');im.alpha_composite(candidate,(10,35));im.alpha_composite(benchmark,(candidate.width+20,35));im=im.convert('RGB');im.save(ROOT/f'comparisons/{a["id"]}-chapter2-native.png');im.resize((w*4,h*4),Image.Resampling.NEAREST).save(ROOT/f'comparisons/{a["id"]}-chapter2-4x.png')
 states=Image.new('RGB',(1740,644),'#253b34');dr=ImageDraw.Draw(states)
 for id_,x,y in [('CH4-B2-24',8,8),('CH4-B2-24-open',588,8),('CH4-B2-25',8,326),('CH4-B2-25-slipped',588,326),('CH4-B2-25-recovered',1168,326)]:
  dr.text((x,y),id_+' UNSELECTED',font=font,fill='#f0dfbd');states.paste(Image.open(ROOT/f'native/{id_}-v01.png'),(x,y+27))
 states.save(ROOT/'comparisons/ring-states-native.png');states.resize((6960,2576),Image.Resampling.NEAREST).save(ROOT/'comparisons/ring-states-4x.png')
 manifest={'title':'Chapter 4 B2-04 — Lot31 and Collection Stairs v01','groupId':'B2-04','status':'UNSELECTED','branch':'art/ch4-batch01-review-20261121','canonicalApprovalBaseline':'2c0f1c5a22c234bc561b12d98009a10883cf66ac','inventorySource':'evidence/inventory-source.json','primaryUnits':7,'stateFamilies':1,'supplementalStateFrames':3,'nativePNGCount':10,'storyNodeCoverage':inv['group']['nodeIds'],'productionIntegrationPerformed':False,'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'assets':assets,'canonicalBenchmarks':json.loads((ROOT/'evidence/canonical-benchmarks.json').read_text()),'stateBindingPlan':'evidence/state-plan.json'}
 (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 def figure(one,four,size,label):
  return '<section class="figure"><p>'+html.escape(label)+'</p><button data-scale="1">Native 1×</button> <button data-scale="4">Exact 4×</button><div class="scroll"><img src="'+one+'" width="'+str(size[0])+'" height="'+str(size[1])+'" data-one="'+one+'" data-four="'+four+'" data-w="'+str(size[0])+'" data-h="'+str(size[1])+'" alt="'+html.escape(label)+'"></div></section>'
 cards=[]
 for a in assets:
  title=a['key']or('Production-only state; base '+a['baseFocusKey']);card='<article id="'+a['id']+'"><h2>'+a['id']+' — '+html.escape(a['title'])+' <b>UNSELECTED</b></h2><p><code>'+html.escape(title)+'</code> · '+', '.join(a['nodeIds'])+'</p>'
  if a['unitType']=='supplemental-state':card+='<p>'+html.escape(a['authoredEvidence']['truth'])+' No runtime binding or canonical state key is installed.</p>'
  card+=figure(a['native']['file'],a['preview4x']['file'],a['native']['dimensions'],'Candidate v01 — '+str(a['native']['dimensions']))
  if a['kind']=='portrait':card+=figure('references/approved-attendant.png','previews/approved-attendant-4x.png',(564,278),'Primary human portrait finish benchmark — approved Pavilion attendant')
  card+=figure('references/approved-bureau.png','previews/approved-bureau-4x.png',(314,206),'Approved Chapter 2 — pixel-cluster and material benchmark')
  if a['kind']=='portrait':card+=figure('previews/'+a['id']+'-composite.png','previews/'+a['id']+'-composite-4x.png',(564,278),'Porter over independently composed service-passage background')
  if a['kind']=='portrait':
   context='restroom'if a['id']=='CH4-B2-20'else'lobby';card+=figure('previews/'+a['id']+'-'+context+'-composite.png','previews/'+a['id']+'-'+context+'-composite-4x.png',(564,278),'Same unselected porter foreground over unchanged approved '+context+' background — authored context reuse')
  if a['kind']in['focus','focus-state']:card+=figure('references/approved-isolator-focus.png','previews/approved-isolator-focus-4x.png',(564,278),'Approved Focus A object-detail benchmark — B2-03')
  if a['unitType']=='supplemental-state':
   base=next(x for x in assets if x['id']==a['baseAssetId']);card+=figure(base['native']['file'],base['preview4x']['file'],base['native']['dimensions'],'Unchanged base Focus candidate — compare the bounded object-state change')
  card+='<p>SHA-256 <code>'+a['native']['sha256']+'</code></p><p><a href="'+a['detailedReference']['file']+'">Detailed reference</a> · <a href="comparisons/'+a['id']+'-chapter2-native.png">Direct Chapter2 native comparison</a> · <a href="comparisons/'+a['id']+'-chapter2-4x.png">Direct exact4× comparison</a></p></article>';cards.append(card)
 header='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>B2-04 v01 — UNSELECTED</title><style>body{margin:0;background:#182a25;color:#eadfc6;font:16px/1.5 system-ui}main{max-width:1320px;margin:auto;padding:24px}h1,h2{line-height:1.2}article,header{background:#253b34;border:1px solid #617365;padding:22px;margin:20px 0}b{color:#ffc77a;font-size:14px}a{color:#c4e5ce}code{overflow-wrap:anywhere;font-size:12px}button{background:#e5d4ac;border:0;padding:8px 12px;margin-bottom:10px;cursor:pointer}.scroll{overflow:auto;background:repeating-conic-gradient(#344b41 0% 25%,#40594d 0% 50%) 0/20px 20px;padding:8px}img{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}.figure{margin:18px 0}p{max-width:1100px}</style><main><header><h1>Chapter 4 B2-04<br>Lot31 and Collection Stairs</h1><p><b>Seven primary assets + three state-family frames — all UNSELECTED pending Nate</b></p><p>B2-03's seven exact PNGs are approved/selected at canonical main <code>2c0f1c5a22c234bc561b12d98009a10883cf66ac</code>, PR24/docs131, verified on GitHub and live Pages. The B2-01 plumber alternatives remain separate/unselected. No narrative, gameplay or engine integration changes.</p><p>Native314×206 main scene; native564×278 portraits, separate closer background and Focus/state frames. Every image has exact4× and direct approved Chapter2 comparisons. Human portraits also have an approved human finish benchmark. Detailed references establish ambition; separate interpretations and native material/structural/letter/object layers produce these SOURCE-DERIVED candidates. No independent native-grid authorship is claimed.</p><p>The existing inventory specifies seven primary units plus a chair/ring state family. The extra frames show an opened seam, a slipped ring beneath the brace, and the empty cavity after explicit recovery. They are review-only production choices; no new Focus state keys or runtime behavior are installed, and conditional states are not represented as sequential pages.</p><p><a href="manifest.json">Manifest, hashes and source nodes</a> · <a href="README.md">Production and prompts</a> · <a href="evidence/state-plan.json">Authored state evidence</a> · <a href="comparisons/all-native.png">All ten at native</a> · <a href="comparisons/ring-states-native.png">Ring-state comparisons</a> · <a href="evidence/validation.json">Technical preservation checks</a> · <a href="evidence/visual-review.md">Visual assessment</a></p></header>'''
 script='''<script>document.querySelectorAll('button[data-scale]').forEach(b=>b.addEventListener('click',()=>{const i=b.closest('section').querySelector('img'),s=Number(b.dataset.scale);i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;}));</script></main></html>'''
 (ROOT/'index.html').write_text(header+''.join(cards)+script);print('Packaged ten UNSELECTED PNGs: seven primary units and three state-family frames.')
if __name__=='__main__':main()
