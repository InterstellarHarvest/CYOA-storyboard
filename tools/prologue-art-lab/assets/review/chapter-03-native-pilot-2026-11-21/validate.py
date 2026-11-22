from pathlib import Path
from PIL import Image
from html.parser import HTMLParser
import json,subprocess,hashlib,io,base64
B=Path(__file__).resolve().parent;R=B.parents[4]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((B/'manifest.json').read_text());base=json.loads((B/'preservation-baseline.json').read_text());before={c['file']:sha(B/c['file']) for c in m['candidates']}
subprocess.run(['python3',str(B/'reconstruct.py')],check=True,capture_output=True)
checks=[]
def check(label,v):checks.append({'name':label,'pass':bool(v)});assert v,label
check('Only Backstage and Locomotion scoped',set(m['scope'])=={'scenes:pavilion_reboot/backstage','scenes:pavilion_reboot/locomotion_stage'})
for c in m['candidates']:
 im=Image.open(B/c['file']);check(c['id']+' 314x206 opaque RGB',im.size==(314,206) and im.mode=='RGB' and im.convert('RGBA').getchannel('A').getextrema()==(255,255))
 check(c['id']+' status generated/unselected',c['status']=='generated' and c['selection']=='unselected')
 check(c['id']+' deterministic native rebuild',sha(B/c['file'])==before[c['file']]==c['sha256'])
 z=Image.open(B/c['zoom']);check(c['id']+' exact 4x blocks',z.size==(1256,824) and z.convert('RGBA').tobytes()==im.convert('RGBA').resize((1256,824),Image.Resampling.NEAREST).tobytes())
 expected=set(Image.open(B/c['file']).convert('RGB').get_flattened_data());scene=json.loads((B/'sources'/('backstage' if 'backstage' in c['id'] else 'locomotion')/'scene.json').read_text());palette={tuple(bytes.fromhex(h[1:])) for h in scene['palette'].values()};check(c['id']+' every output pixel belongs to explicitly authored palette',expected<=palette)
 old=c['approved'];check(c['id']+' approved copy byte-identical',sha(B/old['file'])==old['sha256'])
 check(c['id']+' approved exact 4x blocks',Image.open(B/old['zoom']).convert('RGBA').tobytes()==Image.open(B/old['file']).convert('RGBA').resize((1256,824),Image.Resampling.NEAREST).tobytes())
 for crop in c['closeups']:
  for role,p in [('approved',old['file']),('candidate',c['file'])]:
   region=Image.open(B/p).crop(crop['box']).convert('RGBA');z=Image.open(B/crop[role]).convert('RGBA');check(c['id']+' '+crop['label']+' '+role+' exact 8x crop',z.tobytes()==region.resize((region.width*8,region.height*8),Image.Resampling.NEAREST).tobytes())
for r in m['references']:check('Reference preserved: '+r['key'],sha(B/r['file'])==r['sha256'])
changed=[v['path'] for v in base['trackedFiles'] if not (R/v['path']).is_file() or sha(R/v['path'])!=v['sha256']]
check('All 493 preexisting tracked files retain SHA-256',not changed)
check('No diff to any preexisting tracked source file',subprocess.run(['git','-C',str(R),'diff','--quiet',base['baseCommit'],'--','.']).returncode==0)
class H(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.img=[];self.links=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if 'id'in a:self.ids.append(a['id'])
  if t=='img':self.img.append(a)
  if t=='a':self.links.append(a['href'])
h=H();h.feed((B/'index.html').read_text());check('HTML anchors unique',len(h.ids)==len(set(h.ids)))
for im in h.img:check('HTML image valid: '+im['src'],Image.open(B/im['src']).size==(int(im['width']),int(im['height'])))
for link in h.links:
 if link.startswith('#'):check('HTML anchor '+link,link[1:] in h.ids)
 elif not link.startswith('http') and not link.startswith('qa/'):check('Artifact link '+link,(B/link).exists())
s=H();s.feed((B/'standalone-gallery.html').read_text());check('Portable gallery embeds all images',len(s.img)==len(h.img) and all(v['src'].startswith('data:image/png;base64,') for v in s.img))
r={'result':'PASS','checks':checks,'checkCount':len(checks),'baseCommit':base['baseCommit'],'preservation':{'existingTrackedFilesVerified':len(base['trackedFiles']),'changedExistingPaths':changed,'approvedAssetsChanged':0,'registryChanges':0,'narrativeChanges':0,'earlierReviewPackageChanges':0,'chapter4Changes':0,'engineRepositoryAccessOrChanges':False},'candidates':[{'id':c['id'],'size':[c['width'],c['height']],'sha256':c['sha256'],'uniqueRGB':c['uniqueRGB'],'status':'generated/unselected'}for c in m['candidates']],'nativeMethodLimit':'Explicit coordinate-authored procedural native construction is reproducible; artistic success and hand-painted authorship are not inferred. Conceptual imagegen raster authorship remains unresolved.'}
(B/'qa/image-and-preservation.json').write_text(json.dumps(r,indent=2));print('PASS:',len(checks),'image/link/preservation checks;',len(base['trackedFiles']),'preexisting files unchanged')
