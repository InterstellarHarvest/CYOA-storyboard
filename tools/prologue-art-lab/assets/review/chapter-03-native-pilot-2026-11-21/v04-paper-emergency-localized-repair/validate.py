from pathlib import Path
from PIL import Image,ImageDraw
from html.parser import HTMLParser
import json,hashlib,subprocess,re
B=Path(__file__).resolve().parent;R=B.parents[5];checks=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def check(name,ok):checks.append({'name':name,'pass':bool(ok)});assert ok,name
p=json.loads((B/'sources/repair-plan.json').read_text());s=json.loads((B/'sources/repair-result.json').read_text());m=json.loads((B/'manifest.json').read_text());base=json.loads((B/'sources/preservation-baseline.json').read_text());first=json.loads((B/'sources/pre-edit-declaration.json').read_text())
original=Image.open(B/p['source']).convert('RGB');candidate=Image.open(B/p['candidate']).convert('RGB');check('Original byte-identical to approved source',sha(B/p['source'])==p['baseApprovedSha256']==s['sourceSha256']=='ac0f7c44d267dd54897507ae3b8b02959a5b76f4fcd9d0418b77b8fdb777ba7e');check('Candidate native opaque RGB',candidate.size==(314,206)and Image.open(B/p['candidate']).mode=='RGB'and candidate.convert('RGBA').getchannel('A').getextrema()==(255,255));check('Masks and operations frozen before candidate rendering',first['candidateExisted']is False and first['declaredBeforeRendering']and first['planSha256']==sha(B/'sources/repair-plan.json'))
allowed=Image.open(B/p['unionMask']['file']).convert('L');actualMask=Image.open(B/'masks/effective-change-mask.png').convert('L');check('Declared union hash exact',sha(B/p['unionMask']['file'])==p['unionMask']['sha256']);pts={(x,y)for y in range(206)for x in range(314)if candidate.getpixel((x,y))!=original.getpixel((x,y))};check('Exactly 327 changes',len(pts)==s['changedPixels']==327);check('Every change within predeclared mask',all(allowed.getpixel(q)==255 for q in pts));check('All 64357 other pixels unchanged',sum(original.getpixel((x,y))==candidate.getpixel((x,y))for y in range(206)for x in range(314))==64357);check('Declared union tightly traced at 334 pixels',sum(v==255 for v in allowed.get_flattened_data())==334);check('Effective mask is exactly actual changed coordinates',{(x,y)for y in range(206)for x in range(314)if actualMask.getpixel((x,y))}==pts)
# Validate masks from the declared primitives, independently replaying footprint only.
traced={k:Image.new('L',(314,206),0)for k in p['masks']}
for op in p['operations']:
 d=ImageDraw.Draw(traced[op['region']]);co=op['coordinates'];kind=op['kind']
 if kind=='point':d.point(tuple(co),fill=255)
 elif kind=='line':d.line([tuple(q)for q in co],fill=255,width=op['width'])
 else:d.polygon([tuple(q)for q in co],fill=255)
 check('Original source RGB sample exact '+str(op['sample'])+' '+str(len(checks)),list(original.getpixel(tuple(op['sample'])))==op['rgb'])
for k,v in p['masks'].items():
 mask=Image.open(B/v['file']).convert('L');effective=Image.open(B/'masks'/f'{k}-effective-mask.png').convert('L');check(k+' declaration hash pixels and primitive shape exact',sha(B/v['file'])==v['sha256']and sum(c==255 for c in mask.get_flattened_data())==v['pixels']and mask.tobytes()==traced[k].tobytes());check(k+' actual changed count exact',sum(q in pts for q in[(x,y)for y in range(206)for x in range(314)if mask.getpixel((x,y))])==s['changedPixelsByRegion'][k]);check(k+' effective mask exact',{(x,y)for y in range(206)for x in range(314)if effective.getpixel((x,y))}=={q for q in pts if mask.getpixel(q)})
oldp1=Image.open(B.parent/'v03-paper-emergency-targeted-review/masks/P1-proposed-mask.png').convert('L');check('P1 remains within previously assessed crossing',all(oldp1.getpixel((x,y))==255 for y in range(206)for x in range(314)if traced['P1'].getpixel((x,y))))
for g in p['protectedGuards']:check('Protected context unchanged: '+g['name'],original.crop(g['box']).tobytes()==candidate.crop(g['box']).tobytes())
check('Nose and surrounding upper face unchanged',original.crop((213,109,219,113)).tobytes()==candidate.crop((213,109,219,113)).tobytes());check('Right two-person sign unchanged',original.crop((198,64,227,96)).tobytes()==candidate.crop((198,64,227,96)).tobytes())
receipt=Image.open(B/p['passingReceiptMask']).convert('L');rpts={(x,y)for y in range(206)for x in range(314)if receipt.getpixel((x,y))};check('Passing receipt remains exact',not(pts&rpts));palmOp=next(op for op in p['operations']if op['reason'].startswith('Urgent open stop/leave palm'));palm=Image.new('L',(314,206));ImageDraw.Draw(palm).polygon([tuple(q)for q in palmOp['coordinates']],fill=255);palmpoints={(x,y)for y in range(206)for x in range(314)if palm.getpixel((x,y))};gap=min(max(abs(x-x2),abs(y-y2))for x,y in palmpoints for x2,y2 in rpts);check('Raised palm does not intersect conservative passing-receipt guard',gap>=1);check('Raised palm stays left of plant protected region',max(x for x,y in palmpoints)<=239)
changes=json.loads((B/'sources/changed-pixels.json').read_text());check('Every changed RGB logged, none missing or extra',{(v['x'],v['y'])for v in changes}==pts and all(v['beforeRGB']==list(original.getpixel((v['x'],v['y'])))and v['afterRGB']==list(candidate.getpixel((v['x'],v['y'])))for v in changes));check('Fourteen old-hand edge pixels restored inside hands mask',sum(v['region']=='hands'and v['y']==141 for v in changes)==14)
layer=Image.open(B/'sources/exact-native-edit-layer.png').convert('RGBA');check('Transparent edit layer has 327 opaque cells and zero partial alpha',sum(v==255 for v in layer.getchannel('A').get_flattened_data())==327 and set(layer.getchannel('A').get_flattened_data())=={0,255});check('Edit layer composites exactly to candidate',Image.alpha_composite(original.convert('RGBA'),layer).convert('RGB').tobytes()==candidate.tobytes())
for name,im in [('approved',original),('candidate-v04',candidate)]:check('Exact full-scene 4x '+name,Image.open(B/'previews'/f'paper-emergency-{name}-4x.png').tobytes()==im.resize((1256,824),Image.Resampling.NEAREST).tobytes())
n=Image.open(B/'comparisons/approved-left-candidate-right-native.png');z=Image.open(B/'comparisons/approved-left-candidate-right-4x.png');check('Native pair consists of unchanged original and candidate',n.size==(628,206)and n.crop((0,0,314,206)).tobytes()==original.tobytes()and n.crop((314,0,628,206)).tobytes()==candidate.tobytes());check('Exact full-scene 4x pair',z.size==(2512,824)and z.tobytes()==n.resize((2512,824),Image.Resampling.NEAREST).tobytes())
for key in ['face','hands','P1','attendant','receipt-clearance','desk-contact']:
 n=Image.open(B/'comparisons'/f'{key}-before-after-native.png');z=Image.open(B/'comparisons'/f'{key}-before-after-4x.png');check('Exact crop 4x '+key,z.tobytes()==n.resize((n.width*4,n.height*4),Image.Resampling.NEAREST).tobytes())
changed=[path for path,h in base['files'].items()if not(R/path).is_file()or sha(R/path)!=h];check('All 831 earlier tracked files unchanged',len(base['files'])==831 and not changed);check('Generated unselected, no production path',m['status']=='generated'and m['selection']=='unselected'and m['approved']is False and m['assetPath']is None);check('Actual colors reported without palette cap',len(set(candidate.get_flattened_data()))==s['candidateUniqueRGB']==20133 and s['paletteTarget']is None);h=sha(B/p['candidate']);subprocess.run(['python3',str(B/'repair.py'),'--render'],check=True,capture_output=True);check('Native operation replay reproduces exact PNG hash',sha(B/p['candidate'])==h==s['candidateSha256'])
class H(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.images=[];self.links=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if 'id'in a:self.ids.append(a['id'])
  if t=='img':self.images.append(a)
  if t=='a':self.links.append(a['href'])
h=H();h.feed((B/'index.html').read_text());check('HTML anchors unique',len(h.ids)==len(set(h.ids)))
for im in h.images:check('HTML image exact dimensions '+im['src'],Image.open(B/im['src']).size==(int(im['width']),int(im['height'])))
for link in h.links:
 if link.startswith('#'):check('Anchor '+link,link[1:]in h.ids)
 elif not link.startswith(('http','qa/')):check('Artifact link '+link,(B/link).exists())
shtml=H();shtml.feed((B/'standalone-gallery.html').read_text());check('Portable HTML embeds every preview',len(shtml.images)==len(h.images)and all(im['src'].startswith('data:image/png;base64,')for im in shtml.images))
for link in re.findall(r'\]\(([^)]+)\)',(B/'README.md').read_text()):
 if not link.startswith(('http','qa/')):check('GitHub review artifact link '+link,(B/link).exists())
r={'result':'PASS','checks':checks,'checkCount':len(checks),'changedPixels':327,'changedPixelsByRegion':s['changedPixelsByRegion'],'declaredMaskPixels':334,'outsideMaskChanges':0,'P2Changes':0,'passingReceiptChanges':0,'palmToReceiptChebyshevDistance':gap,'priorTrackedFilesPreserved':831,'previousFilesChanged':changed,'geometryTransforms':0,'sourceAuthorshipLimitationRetained':True};(B/'qa/pixel-and-preservation.json').write_text(json.dumps(r,indent=2));print('PASS',len(checks),'checks;',len(pts),'pixels changed, 0 outside masks;',len(base['files']),'prior files preserved.')
