"""Build v02 close-camera/proportion review exports; never changes v01 or approved art."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,html,subprocess
P=Path(__file__).resolve().parent; V=P.parent/'v01'; R=P.parents[5]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,d:p.write_text(json.dumps(d,indent=2)+'\n')
old=json.loads((V/'manifest.json').read_text());new=json.loads(json.dumps(old));new['title']='Chapter 3 Batch D — v02 close cameras and attendant proportions';new['version']='v02-close-camera-corrections';new['historicalReview']='../v01/index.html';new.pop('candidateSourceCommit',None)
new['correctionScope']=['D02 independently authored tighter service close camera','D03 newly drawn natural proportions with uniform export, no forced silhouette-bounds stretching','D09 independently authored tighter courtesy close camera']
revised={'CH3-D02-service-exit-bg','CH3-D03-attendant-quiet','CH3-D09-courtesy-stage-bg'}
for c in new['candidates']:
 ident=c['candidateId'];prior=c['sha256'];c['candidateSourceCommit']='4fc277651c7d05163817d9ab99d0fc3fcf522d47';c['retainedUnchanged']=ident not in revised
 if c['retainedUnchanged']:
  for k in ['file','preview4x','comparison','prompt']:c[k]='../v01/'+c[k]
  c['source']['original']='../v01/'+c['source']['original'];c['reviewVersion']='v01 retained';continue
 source=P/'originals'/f'{ident}-v02-generator.png'
 if ident.startswith('CH3-D09'):source=P/'originals/CH3-D09-wall-correction-generator.png'
 original=Image.open(source);c['operations']=[]
 if ident.startswith('CH3-D03'):
  # Preserve the new drawing's aspect ratio; fit a natural waist anchor with transparent canvas padding.
  # Uniform nominal scale 264/881, integer rounding only; no crop/bbox stretching.
  factor=264/original.height;size=(round(original.width*factor),264)
  im=Image.new('RGBA',(564,278),(0,0,0,0));sprite=original.convert('RGBA').resize(size,Image.Resampling.NEAREST)
  alpha=sprite.getchannel('A').point(lambda x:255 if x>=128 else 0);sprite.putalpha(alpha)
  bbox=alpha.getbbox();left=318-round((bbox[0]+bbox[2])/2);offset=(left,278-size[1]);im.paste(sprite,offset)
  im.putdata([p if p[3] else (0,0,0,0) for p in im.getdata()])
  c['operations']=[{'operation':'uniform nearest-neighbor export and transparent-canvas translation','original':list(original.size),'uniformNominalScale':factor,'roundedRaster':size,'placement':offset,'alphaThreshold':128,'forcedBoundingBoxStretch':False,'resampling':'NEAREST'}]
  c['knownLimitations']=['New drawing preserves costume and identity references, but face/hand anatomy still needs Art Director review. Uniform scale and position differ intentionally from v01; no aspect-ratio warping.','Original native-grid authorship remains unproven; larger generator original is preserved.']
 else:
  im=original.convert('RGB').resize((564,278),Image.Resampling.NEAREST)
  c['operations']=[{'operation':'nearest-neighbor logical export from independently generated close view','original':list(original.size),'to':[564,278],'notDerivedFromMainScenePixels':True}]
  c['knownLimitations']=['Independently generated close view changes the camera; confirm object scale/geography against the unchanged main.','Original native-grid authorship remains unproven; source-derived softness remains.']
  if ident.startswith('CH3-D09'):c['operations'].append({'operation':'image_gen precise correction removes invented filing cabinet; wall/stripe continue behind it','prompt':'prompts/CH3-D09-wall-correction.txt','input':'originals/CH3-D09-courtesy-stage-bg-v02-generator.png','result':'originals/CH3-D09-wall-correction-generator.png'})
 c['file']=f'candidates/{ident}-v02.png';im.save(P/c['file']);c['sha256']=sha(P/c['file']);c['replacesUnselectedSha256']=prior;c['dimensions']=[564,278];c['mode']=im.mode
 c['preview4x']=f'proofs/{ident}-4x.png';im.resize((2256,1112),Image.Resampling.NEAREST).save(P/c['preview4x'])
 c['prompt']=f'prompts/{ident}-v02.txt';c['source']={'tool':'image_gen built-in','original':str(source.relative_to(P)),'sha256':sha(source),'dimensions':list(original.size),'mode':original.mode};c['reviewVersion']='v02';c['candidateSourceCommit']=None
 hist=im.convert('RGBA').getchannel('A').histogram();c['alphaValidation']={'transparent':hist[0],'opaque':hist[255],'partial':sum(hist[1:255])};c['comparison']=f'proofs/{ident}-comparison.png'
 if ident.startswith('CH3-D02'):c['constraints']='Tight service conversation shot: no ceiling or interior floor, cropped left cabinet/pipes and right open door; same location serves both humans.'
 if ident.startswith('CH3-D03'):c['constraints']='Natural taller neck/torso; same identity/costume, compassionate expression, low hands; waist reaches canvas bottom; uniform export only.'
 if ident.startswith('CH3-D09'):c['constraints']='Tight desk-side courtesy conversation shot: cropped shutter/rail/door sliver left, cropped pictogram/poster above; existing intercom/mic lower left, no ceiling/floor.'

def load(ident):return Image.open(P/next(c['file'] for c in new['candidates'] if c['candidateId']==ident)).convert('RGBA')
approved=json.loads((V/'references/approved-sources.json').read_text())
bg=load('CH3-D02-service-exit-bg');man=load('CH3-D03-attendant-quiet');woman=load('CH3-D04-presenter-relieved')
def composite(name,b,f,occlusion=None):
 im=b.copy();im.alpha_composite(f)
 if occlusion:im.paste(b.crop(occlusion),occlusion[:2])
 im.convert('RGB').save(P/'proofs'/name)
composite('service-attendant.png',bg,man);composite('service-presenter.png',bg,woman)
printer=Image.open(V/approved['scenes:pavilion_reboot/record_printer#portraitBackground']['reviewFile']).convert('RGBA');composite('printer-attendant.png',printer,man,(0,263,564,278))
alarmed=Image.open(V/approved['portraits:pavilion_attendant:alarmed']['reviewFile']).convert('RGBA');composite('courtesy-attendant.png',load('CH3-D09-courtesy-stage-bg'),alarmed)

for c in new['candidates']:
 if c['retainedUnchanged']:continue
 prior=next(x for x in old['candidates'] if x['candidateId']==c['candidateId'])
 shots=[('v01 unselected — history',V/prior['file']),('v02 corrected — unselected',P/c['file'])]
 if 'D03' in c['candidateId']:shots.append(('Approved idle — unchanged',V/approved['portraits:pavilion_attendant:idle']['reviewFile']))
 else:
  ident='CH3-D01-service-exit' if 'D02' in c['candidateId'] else 'CH3-D08-courtesy-stage'
  shots.append(('Companion main — unchanged',V/next(x['file'] for x in old['candidates'] if x['candidateId']==ident)))
 sheet=Image.new('RGB',(600,320*len(shots)),(28,36,42));d=ImageDraw.Draw(sheet)
 for i,(title,f) in enumerate(shots):
  im=Image.open(f).convert('RGBA');d.text((15,i*320+8),title,fill='white');sheet.paste(im,(15,i*320+30),im)
 sheet.save(P/c['comparison'])
write(P/'manifest.json',new)
esc=html.escape;cards=[]
contexts={'CH3-D02-service-exit-bg':['service-presenter.png','service-attendant.png'],'CH3-D03-attendant-quiet':['service-attendant.png','printer-attendant.png'],'CH3-D09-courtesy-stage-bg':['courtesy-attendant.png']}
for c in new['candidates']:
 if c['retainedUnchanged']:continue
 extras=''.join('<figure><img src="proofs/'+f+'" width="564" height="278"><figcaption>'+esc(f)+'</figcaption></figure>' for f in contexts[c['candidateId']])
 cards.append('<article id="'+c['candidateId']+'"><h2>'+c['candidateId']+'</h2><p>'+esc(c['constraints'])+'</p><h3>Native 564×278</h3><figure class="checker"><img class="native" src="'+c['file']+'" width="564" height="278"></figure>'+extras+'<details><summary>Exact 4× nearest-neighbor</summary><div class="scroll"><img class="preview4x" src="'+c['preview4x']+'" width="2256" height="1112"></div></details><details open><summary>v01 / v02 / approved or main comparison</summary><img class="comparison" src="'+c['comparison']+'"></details><p>SHA-256 <code>'+c['sha256']+'</code></p><p><a href="'+c['prompt']+'">Exact prompt</a> · <a href="'+c['source']['original']+'">Immutable generator original</a></p><p>'+esc(' '.join(c['knownLimitations']))+'</p></article>')
retained=''.join('<li><a href="../v01/#'+c['candidateId']+'">'+c['candidateId']+' — exact v01 bytes</a></li>' for c in new['candidates'] if c['retainedUnchanged'])
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Batch D v02 — closer cameras and natural proportions</title><style>body{background:#18242a;color:#eee6d6;font:16px/1.5 system-ui;max-width:1160px;margin:auto;padding:24px}a{color:#9de0d7}article{border-top:2px solid #587878;margin-top:32px;padding-top:18px}img{image-rendering:pixelated;vertical-align:top}.native,.preview4x{max-width:none}.comparison{max-width:100%;height:auto}figure{margin:12px 0;max-width:100%;width:fit-content;overflow:auto}.checker{background:repeating-conic-gradient(#536064 0 25%,#334249 0 50%) 50%/16px 16px}.scroll{overflow:auto}code{overflow-wrap:anywhere}summary{padding:12px;background:#26383f;cursor:pointer}details{margin:12px 0}</style></head><body><h1>Chapter 3 Batch D — v02</h1><p><strong>Three corrections · generated / unselected · no approval or gameplay integration</strong></p><p>The service and courtesy conversation backgrounds are independently re-authored close views with no ceiling or room-wide floor. The quiet attendant is redrawn with a taller natural neck/torso and exported uniformly, without fitting his silhouette into an old bounding box. One shared service background serves both humans.</p><p><a href="../v01/">Unchanged historical v01 gallery</a> · <a href="manifest.json">All nine current mappings and hashes</a> · <a href="qa/results.json">Image/preservation QA</a> · <a href="qa/browser-results.json">Browser QA</a> · <a href="SHA256SUMS.txt">Package checksums</a></p><p>Native-grid authorship remains unproven. Larger generator originals and exact derived-export operations are preserved. Native images are shown at exact size; 4× previews scroll.</p>'''+''.join(cards)+'<h2>Six retained candidates</h2><ul>'+retained+'</ul></body></html>'
(P/'index.html').write_text(page)
print('Built three revised images; six v01 candidates retained byte-identically.')
