from pathlib import Path
from PIL import Image
from html.parser import HTMLParser
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;R=B.parents[5];checks=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def check(name,ok):checks.append({'name':name,'pass':bool(ok)});assert ok,name
plan=json.loads((B/'sources/repair-plan.json').read_text());first=json.loads((B/'sources/assessment-first.json').read_text());stats=json.loads((B/'sources/repair-result.json').read_text());base=json.loads((B/'sources/preservation-baseline.json').read_text());assessment=json.loads((B/'assessment/targeted-assessment.json').read_text())
check('Assessment and mask fixed before candidate exists',first['candidateExistsAtAssessment'] is False and first['repairPlanSha256']==sha(B/'sources/repair-plan.json') and first['assessmentSha256']==sha(B/'assessment/targeted-assessment.json'))
check('Predeclared mask hash unchanged',sha(B/plan['maskFile'])==plan['maskSha256'])
original=Image.open(B/'originals/approved-locomotion.png').convert('RGB');candidate=Image.open(B/'candidate/CH3-LOCOMOTION-presenter-local-v02.png').convert('RGB');allowed=Image.open(B/plan['maskFile']).convert('L');effective=Image.open(B/'masks/effective-change-mask.png').convert('L')
check('Candidate and original 314x206 RGB',candidate.size==original.size==(314,206) and Image.open(B/'candidate/CH3-LOCOMOTION-presenter-local-v02.png').mode=='RGB')
check('Opaque candidate',candidate.convert('RGBA').getchannel('A').getextrema()==(255,255))
actual={(x,y)for y in range(206)for x in range(314)if candidate.getpixel((x,y))!=original.getpixel((x,y))};points={tuple(o['at'])for o in plan['operations']};permit={(x,y)for y in range(206)for x in range(314)if allowed.getpixel((x,y))==255}
check('Exactly six changed pixels',len(actual)==6);check('Actual changes equal predeclared six coordinates',actual==points==permit);check('Zero changes outside mask',all(allowed.getpixel(p)==255 for p in actual));check('64678 unmasked pixels exactly preserved',sum(candidate.getpixel((x,y))==original.getpixel((x,y))for y in range(206)for x in range(314))==64678)
check('Effective mask equals predeclared mask',effective.tobytes()==allowed.tobytes())
for o in plan['operations']:check('Source sample and replacement exact '+str(o['at']),list(candidate.getpixel(tuple(o['at'])))==o['afterRGB']==list(original.getpixel(tuple(o['sample']))) and list(original.getpixel(tuple(o['at'])))==o['beforeRGB'])
check('Original canonical source SHA-256',sha(B/'originals/approved-locomotion.png')=='be99d790754951bcbcd1c26b94a94ff4e84280f5385735951b0f024b322e13c5')
check('Original Backstage SHA-256',sha(B/'originals/approved-backstage.png')=='aa90896023a59454887e9b3bd5b1745cb8b95a5d9737829119abddd9176f4889')
check('No Backstage repair allowed',not any(Image.open(B/'masks/backstage-proposed-repair-mask.png').get_flattened_data()) and assessment['backstage']['estimatedRepairScope']['nativePixels']==0)
check('No Backstage candidate produced',len(list((B/'candidate').glob('*.png')))==1)
layer=Image.open(B/'sources/presenter-six-pixel-edit-layer.png').convert('RGBA');check('Six opaque edit-layer pixels, all other alpha zero',sum(a==255 for a in layer.getchannel('A').get_flattened_data())==6 and set(layer.getchannel('A').get_flattened_data())=={0,255})
check('Transparent edit layer reconstructs candidate exactly',Image.alpha_composite(original.convert('RGBA'),layer).convert('RGB').tobytes()==candidate.tobytes())
for name,im in [('locomotion-approved',original),('locomotion-presenter-candidate-v02',candidate),('backstage-approved',Image.open(B/'originals/approved-backstage.png'))]:check('Exact 4x preview '+name,Image.open(B/'previews'/f'{name}-4x.png').convert('RGB').tobytes()==im.convert('RGB').resize((1256,824),Image.Resampling.NEAREST).tobytes())
native=Image.open(B/'comparisons/locomotion-approved-left-candidate-right-native.png');big=Image.open(B/'comparisons/locomotion-approved-left-candidate-right-4x.png');check('Matching native comparison halves exact',native.size==(628,206) and native.crop((0,0,314,206)).tobytes()==original.tobytes() and native.crop((314,0,628,206)).tobytes()==candidate.tobytes());check('Matching 4x comparison exact',big.size==(2512,824) and big.tobytes()==native.resize((2512,824),Image.Resampling.NEAREST).tobytes())
for name in ['presenter','hair-face','open-hand']:
 n=Image.open(B/'comparisons'/f'{name}-before-after-native.png');q=Image.open(B/'comparisons'/f'{name}-before-after-4x.png');check('Exact 4x cropped comparison '+name,q.tobytes()==n.resize((n.width*4,n.height*4),Image.Resampling.NEAREST).tobytes())
for v in assessment['locomotion']['protected']:
 x0,y0,x1,y1=v['box'];actualIn={(x,y)for y in range(y0,y1)for x in range(x0,x1)if candidate.getpixel((x,y))!=original.getpixel((x,y))};check('Protected detail context: '+v['name'],actualIn<=points)
changed=[p for p,h in base['files'].items()if not(R/p).is_file()or sha(R/p)!=h];check('All 644 prior tracked files unchanged',len(base['files'])==644 and not changed)
check('Candidate color count reported without palette target',len(set(candidate.get_flattened_data()))==stats['candidateUniqueRGB']==16879 and stats['paletteTarget']is None)
check('Candidate hash exact',sha(B/'candidate/CH3-LOCOMOTION-presenter-local-v02.png')==stats['candidateSha256'])
before=stats['candidateSha256'];subprocess.run(['python3',str(B/'repair.py')],check=True,capture_output=True);check('Deterministic replay yields same PNG hash',sha(B/'candidate/CH3-LOCOMOTION-presenter-local-v02.png')==before)
class H(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.images=[];self.links=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if 'id'in a:self.ids.append(a['id'])
  if t=='img':self.images.append(a)
  if t=='a':self.links.append(a['href'])
h=H();h.feed((B/'index.html').read_text());check('Unique HTML anchors',len(h.ids)==len(set(h.ids)))
for i in h.images:check('HTML image and declared dimensions '+i['src'],Image.open(B/i['src']).size==(int(i['width']),int(i['height'])))
for link in h.links:
 if link.startswith('#'):check('Anchor '+link,link[1:]in h.ids)
 elif not link.startswith('http')and not link.startswith('qa/'):check('Source link '+link,(B/link).exists())
s=H();s.feed((B/'standalone-gallery.html').read_text());check('Portable gallery embeds every image',len(s.images)==len(h.images)and all(i['src'].startswith('data:image/png;base64,')for i in s.images))
report={'result':'PASS','checks':checks,'checkCount':len(checks),'changedPixels':6,'unchangedPixels':64678,'outsideMaskChanges':0,'preservedPreexistingFiles':len(base['files']),'previousFilesChanged':changed,'backstagePixelsEdited':0,'geometryPixelsEdited':0,'imageGenerationUsed':False,'narrativeRegistryGameplayWorkflowChanges':0,'candidateStatus':'generated/unselected','sourceAuthorshipLimitationRetained':True}
(B/'qa/pixel-and-preservation.json').write_text(json.dumps(report,indent=2));print('PASS',len(checks),'checks; 6 changed pixels, 0 outside mask;',len(base['files']),'earlier files preserved')
