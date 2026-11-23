"""Package seven unselected canonical B2-03 demands without changing canon."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,html
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(rel):
 p=ROOT/rel;im=Image.open(p);return {'file':rel,'sha256':sha(p),'dimensions':list(im.size),'mode':im.mode}
def main():
 inventory=json.loads((ROOT/'evidence/inventory-source.json').read_text());assets=[]
 titles=['Maintenance walkway','Boiler access','Groom — nervous','Groom — relieved','Boiler access conversation background','Maintenance conversation background','Central water isolation — two levers']
 for index,item in enumerate(inventory['assets']):
  n=index+12;id_=f'CH4-B2-{n:02}';kind={'main_scene':'scene','portrait':'portrait','portrait_background':'portrait-background','focus_a':'focus'}[item['category']]
  key=('scenes:'+item['logicalKey']if kind=='scene'else'portraits:'+item['logicalKey']if kind=='portrait'else'scenes:'+item['logicalKey']+'#portraitBackground'if kind=='portrait-background'else'focus:'+item['logicalKey'])
  assets.append({'id':id_,'title':titles[index],'key':key,'inventoryId':item['inventoryId'],'kind':kind,'nodeIds':item['nodeIds'],'status':'UNSELECTED','selected':False,'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'native':rec(f'native/{id_}-v01.png'),'preview4x':rec(f'previews/{id_}-4x.png'),'detailedReference':rec(f'originals/{id_}-detailed.png'),'pixelFriendlySource':rec(f'originals/{id_}-pixel-friendly.png')if n not in [14,15]else None,'layers':[str(p.relative_to(ROOT))for p in sorted((ROOT/'layers').glob(id_+'*.png'))],'masks':[str(p.relative_to(ROOT))for p in sorted((ROOT/'masks').glob(id_+'*.png'))]})
 for p in (ROOT/'references').glob('*.png'):
  im=Image.open(p);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/'previews'/(p.stem+'-4x.png'))
 bg=Image.open(ROOT/'native/CH4-B2-17-v01.png').convert('RGBA')
 for n in [14,15]:
  fg=Image.open(ROOT/f'native/CH4-B2-{n}-v01.png').convert('RGBA');c=Image.alpha_composite(bg,fg);c.save(ROOT/f'previews/CH4-B2-{n}-composite.png');c.resize((2256,1112),Image.Resampling.NEAREST).save(ROOT/f'previews/CH4-B2-{n}-composite-4x.png')
  for name,color in [('light','#f0e6ce'),('dark','#182a24')]:Image.alpha_composite(Image.new('RGBA',fg.size,color),fg).save(ROOT/f'previews/CH4-B2-{n}-alpha-{name}.png')
 sheet=Image.new('RGB',(1164,1284),'#253b34');d=ImageDraw.Draw(sheet);font=ImageFont.load_default(size=15)
 for i,a in enumerate(assets):
  x=10+(i%2)*582;y=10+(i//2)*318;d.text((x,y),a['id']+' '+a['title'],font=font,fill='#f0dfbd');im=Image.open(ROOT/a['native']['file']).convert('RGBA');back=Image.alpha_composite(Image.new('RGBA',im.size,'#40554a'),im);sheet.paste(back.convert('RGB'),(x,y+28))
 sheet.save(ROOT/'comparisons/all-native.png');sheet.resize((4656,5136),Image.Resampling.NEAREST).save(ROOT/'comparisons/all-4x.png')
 # Direct native comparisons keep both candidate and benchmark pixels unscaled.
 for a in assets:
  name='approved-groundkeeper'if a['kind']=='portrait'else'approved-tower'if a['id']=='CH4-B2-13'else'approved-bureau'
  candidate=Image.open(ROOT/a['native']['file']).convert('RGBA');benchmark=Image.open(ROOT/f'references/{name}.png').convert('RGBA');w=candidate.width+benchmark.width+30;h=max(candidate.height,benchmark.height)+45
  im=Image.new('RGBA',(w,h),'#40554a');dr=ImageDraw.Draw(im);dr.text((10,8),a['id']+' UNSELECTED',font=font,fill='#f0dfbd');dr.text((candidate.width+20,8),'Approved Chapter 2',font=font,fill='#f0dfbd');im.alpha_composite(candidate,(10,35));im.alpha_composite(benchmark,(candidate.width+20,35));im=im.convert('RGB');im.save(ROOT/f'comparisons/{a["id"]}-chapter2-native.png');im.resize((w*4,h*4),Image.Resampling.NEAREST).save(ROOT/f'comparisons/{a["id"]}-chapter2-4x.png')
 manifest={'title':'Chapter 4 B2-03 — Maintenance access and water isolation v01','groupId':'B2-03','status':'UNSELECTED','branch':'art/ch4-batch01-review-20261121','canonicalApprovalBaseline':'9fa1f19629956d279f98a118d4280734096f9d56','inventorySource':'evidence/inventory-source.json','storyNodeCoverage':inventory['group']['nodeIds'],'productionIntegrationPerformed':False,'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'assets':assets,'canonicalBenchmarks':json.loads((ROOT/'evidence/canonical-benchmarks.json').read_text())}
 (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 def img(rel,w,h,**attrs):return '<img src="'+rel+'" width="'+str(w)+'" height="'+str(h)+'" '+ ' '.join(k.replace('_','-')+'="'+html.escape(str(v))+'"'for k,v in attrs.items())+'>'
 def figure(one,four,size,label):
  return '<section class="figure"><p>'+label+'</p><button data-scale="1">Native 1×</button> <button data-scale="4">Exact 4×</button><div class="scroll">'+img(one,*size,data_one=one,data_four=four,data_w=size[0],data_h=size[1],alt=label)+'</div></section>'
 cards=[]
 for a in assets:
  name='approved-groundkeeper'if a['kind']=='portrait'else'approved-tower'if a['id']=='CH4-B2-13'else'approved-bureau';ref=Image.open(ROOT/f'references/{name}.png')
  card='<article id="'+a['id']+'"><h2>'+a['id']+' — '+html.escape(a['title'])+' <b>UNSELECTED</b></h2><p><code>'+html.escape(a['key'])+'</code> · '+', '.join(a['nodeIds'])+'</p>'
  card+=figure(a['native']['file'],a['preview4x']['file'],a['native']['dimensions'],'Candidate v01 — '+str(a['native']['dimensions']))
  if a['kind']=='portrait':card+=figure('references/approved-attendant.png','previews/approved-attendant-4x.png',(564,278),'Primary human portrait finish benchmark — approved Pavilion attendant')
  card+=figure('references/'+name+'.png','previews/'+name+'-4x.png',ref.size,'Approved Chapter 2 — '+name.replace('approved-',''))
  if a['kind']=='portrait':card+=figure('previews/'+a['id']+'-composite.png','previews/'+a['id']+'-composite-4x.png',(564,278),'Candidate composited over independent maintenance background')
  card+='<p>SHA-256 <code>'+a['native']['sha256']+'</code></p><p><a href="'+a['detailedReference']['file']+'">Detailed reference</a> · <a href="comparisons/'+a['id']+'-chapter2-native.png">Direct native comparison</a> · <a href="comparisons/'+a['id']+'-chapter2-4x.png">Direct exact4× comparison</a></p></article>';cards.append(card)
 header='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Chapter 4 B2-03 — UNSELECTED v01</title><style>body{margin:0;background:#182a25;color:#eadfc6;font:16px/1.5 system-ui}main{max-width:1320px;margin:auto;padding:24px}h1,h2{line-height:1.2}article,header{background:#253b34;border:1px solid #617365;padding:22px;margin:20px 0}b{color:#ffc77a;font-size:14px}a{color:#c4e5ce}code{overflow-wrap:anywhere;font-size:12px}button{background:#e5d4ac;border:0;padding:8px 12px;margin-bottom:10px;cursor:pointer}.scroll{overflow:auto;background:repeating-conic-gradient(#344b41 0% 25%,#40594d 0% 50%) 0/20px 20px;padding:8px}img{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}.figure{margin:18px 0}p{max-width:1100px}</style><main><header><h1>Chapter 4 B2-03<br>Maintenance access and water isolation</h1><p><b>Seven v01 candidates — UNSELECTED, awaiting Nate</b></p><p>B2-02 is approved and selected at canonical main <code>9fa1f19629956d279f98a118d4280734096f9d56</code>. The B2-01 plumber alternatives remain a separate unapproved decision. No narrative, gameplay or engine integration changes.</p><p>Review each candidate at native and exact4× alongside approved Chapter2. Main scenes314×206; portraits, independent backgrounds and Focus564×278. Detailed sources establish composition; separate interpretations and native material/structural/letter layers establish these source-derived candidates. This is not a claim of independent native-grid authorship. Palette counts are diagnostic, not approval.</p><p><a href="manifest.json">Manifest, hashes and canonical nodes</a> · <a href="README.md">Production/provenance</a> · <a href="comparisons/all-native.png">All seven at native size</a> · <a href="evidence/validation.json">Technical validation</a> · <a href="evidence/visual-review.md">Visual review</a></p></header>'''
 script='''<script>document.querySelectorAll('button[data-scale]').forEach(b=>b.addEventListener('click',()=>{const i=b.closest('section').querySelector('img'),s=Number(b.dataset.scale);i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;}));</script></main></html>'''
 (ROOT/'index.html').write_text(header+''.join(cards)+script)
 print('Packaged seven UNSELECTED candidates, paired references, composites and gallery.')
if __name__=='__main__':main()
