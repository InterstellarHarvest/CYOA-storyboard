from pathlib import Path
from PIL import Image
from html.parser import HTMLParser
import json,hashlib,re
B=Path(__file__).resolve().parent;R=B.parents[5];checks=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def check(name,value):checks.append({'name':name,'pass':bool(value)});assert value,name
m=json.loads((B/'manifest.json').read_text());a=json.loads((B/'assessment/targeted-assessment.json').read_text());base=json.loads((B/'sources/preservation-baseline.json').read_text());registry=json.loads((R/'story/artwork-preview.json').read_text())['images']
im=Image.open(B/'originals/approved-paper-emergency.png');check('Approved native 314x206 opaque RGB',im.size==(314,206)and im.mode=='RGB'and im.convert('RGBA').getchannel('A').getextrema()==(255,255));check('Canonical approved PNG copied byte-identically',sha(B/'originals/approved-paper-emergency.png')==registry[m['canonicalArtKey']]['sha256']==m['approvedSource']['sha256']=='ac0f7c44d267dd54897507ae3b8b02959a5b76f4fcd9d0418b77b8fdb777ba7e')
check('Approved native pixel data unchanged',im.tobytes()==Image.open(R/registry[m['canonicalArtKey']]['file']).tobytes());check('Exact approved 4x pixel blocks',Image.open(B/'previews/paper-emergency-approved-4x.png').tobytes()==im.resize((1256,824),Image.Resampling.NEAREST).tobytes());check('No artwork candidate produced',m['candidateProduced']is False and not(B/'candidate').exists()and not(B/'candidates').exists());check('Review material remains generated/unselected',m['status']=='generated'and m['selection']=='unselected'and m['approved']is False and m['assetPath']is None)
check('Zero active edit mask pixels',not any(Image.open(B/'masks/active-edit-mask.png').get_flattened_data()));check('All 64684 original pixels protected',set(Image.open(B/'masks/active-protected-pixels.png').get_flattened_data())=={255});check('Empty changed pixel log',json.loads((B/'sources/changed-pixels.json').read_text())==[]and len((B/'sources/changed-pixels.csv').read_text().splitlines())==1)
lock=Image.open(B/'masks/protected-objects.png').convert('L');union=Image.new('L',(314,206),0)
for p in m['proposals']:
 mask=Image.open(B/p['maskFile']).convert('L');check(p['id']+' mask exact dimensions binary',mask.size==(314,206)and set(mask.get_flattened_data())<={0,255});check(p['id']+' declared count and hash exact',sum(v==255 for v in mask.get_flattened_data())==p['maskPixels']and sha(B/p['maskFile'])==p['maskSha256']);check(p['id']+' mask does not touch protected hardware or identity',not any(x and y for x,y in zip(mask.get_flattened_data(),lock.get_flattened_data())));check(p['id']+' proposal not applied',p['applyNow']is False);check(p['id']+' exact 4x mask export',Image.open(B/'masks'/f'{p["id"]}-proposed-mask-4x.png').tobytes()==mask.resize((1256,824),Image.Resampling.NEAREST).tobytes())
 for y in range(206):
  for x in range(314):
   if mask.getpixel((x,y)):union.putpixel((x,y),255)
check('Proposed union equals exact component union',union.tobytes()==Image.open(B/'masks/proposed-mask-union.png').tobytes())
for r in a['regions']:
 native=Image.open(B/'assessment'/f'{r["id"]}-original-native.png');crop=im.crop(r['box']);check('Approved crop unchanged '+r['id'],native.tobytes()==crop.tobytes());check('Exact 4x crop '+r['id'],Image.open(B/'assessment'/f'{r["id"]}-original-4x.png').tobytes()==native.resize((native.width*4,native.height*4),Image.Resampling.NEAREST).tobytes());pair=Image.open(B/'comparisons'/f'{r["id"]}-original-left-markup-right-native.png');big=Image.open(B/'comparisons'/f'{r["id"]}-original-left-markup-right-4x.png');check('Exact matching-scale diagnostic pair '+r['id'],big.tobytes()==pair.resize((pair.width*4,pair.height*4),Image.Resampling.NEAREST).tobytes())
native=Image.open(B/'comparisons/original-left-assessment-right-native.png');big=Image.open(B/'comparisons/original-left-assessment-right-4x.png');check('Native original versus diagnostic pair at matching scale',native.size==(628,206)and native.crop((0,0,314,206)).tobytes()==im.tobytes());check('Exact full-scene 4x diagnostic comparison',big.size==(2512,824)and big.tobytes()==native.resize((2512,824),Image.Resampling.NEAREST).tobytes())
for r in m['references']:check('Approved reference exact '+r['key'],sha(B/r['reviewFile'])==r['sha256'])
changed=[p for p,h in base['files'].items()if not(R/p).is_file()or sha(R/p)!=h];check('All 730 earlier tracked files preserved',len(base['files'])==730 and not changed)
for path in ['assets/selected/pending-integration/scenes/pavilion_reboot/backstage.png','assets/selected/pending-integration/scenes/pavilion_reboot/locomotion_stage.png','tools/prologue-art-lab/assets/review/chapter-03-native-pilot-2026-11-21/v02-localized-repair/candidate/CH3-LOCOMOTION-presenter-local-v02.png']:check('Explicit no-change guard '+path,sha(R/path)==base['files'][path])
class H(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.images=[];self.links=[]
 def handle_starttag(self,t,attrs):
  d=dict(attrs)
  if 'id'in d:self.ids.append(d['id'])
  if t=='img':self.images.append(d)
  if t=='a':self.links.append(d['href'])
h=H();h.feed((B/'index.html').read_text());check('HTML anchors unique',len(h.ids)==len(set(h.ids)))
for v in h.images:check('HTML image dimensions '+v['src'],Image.open(B/v['src']).size==(int(v['width']),int(v['height'])))
for p in h.links:
 if p.startswith('#'):check('HTML anchor '+p,p[1:]in h.ids)
 elif not p.startswith('http')and not p.startswith('qa/'):check('Source or evidence link '+p,(B/p).exists())
s=H();s.feed((B/'standalone-gallery.html').read_text());check('Portable gallery embeds every image',len(h.images)==len(s.images)and all(v['src'].startswith('data:image/png;base64,')for v in s.images))
for p in re.findall(r'\]\(([^)]+)\)',(B/'README.md').read_text()):
 if not p.startswith(('http','qa/')):check('GitHub review link '+p,(B/p).exists())
r={'result':'PASS','checkCount':len(checks),'checks':checks,'priorTrackedFilesPreserved':len(base['files']),'priorFilesChanged':changed,'artworkPixelsChanged':0,'candidateProduced':False,'activeEditMaskPixels':0,'proposedMasksInactive':True,'proposalCounts':{p['id']:p['maskPixels']for p in m['proposals']},'sourceNativeGridAuthorshipLimitationRetained':True,'generatedUnselected':True};(B/'qa/preservation-and-masks.json').write_text(json.dumps(r,indent=2));print('PASS',len(checks),'checks; 0 artwork pixels changed;',len(base['files']),'prior files preserved.')
