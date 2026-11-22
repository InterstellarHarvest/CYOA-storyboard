"""Validate delivery contracts and replay native authoring with raster reads forbidden."""
from pathlib import Path
from unittest.mock import patch
import importlib, hashlib, json, sys, tempfile, subprocess
from PIL import Image

ROOT=Path(__file__).resolve().parent.parent
REPO=next(p for p in ROOT.parents if (p/'story/artwork.draft.json').exists())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=json.loads((ROOT/'manifest.json').read_text());checks=[]
 def check(ok,label):
  checks.append({'check':label,'passed':bool(ok)})
  if not ok:raise AssertionError(label)
 for r in m['assets']:
  for key in ['native','detailedReference','preview4x']:
   v=r[key]
   if not v:continue
   p=ROOT/v['file'];im=Image.open(p)
   check(digest(p)==v['sha256'],r['id']+' '+key+' SHA-256')
   check(list(im.size)==v['dimensions'],r['id']+' '+key+' dimensions')
  im=Image.open(ROOT/r['native']['file'])
  check(im.size==((564,278) if r['id'] in ['CH4-02','CH4-03'] else (314,206)),r['id']+' native contract')
  values=set(im.convert('RGBA').getchannel('A').getdata())
  check(values==({0,255} if r['id']=='CH4-03' else {255}),r['id']+' binary transparency / opacity')
  if r['preview4x']:
   large=Image.open(ROOT/r['preview4x']['file'])
   check(large.size==(1256,824) and large.tobytes()==im.resize((1256,824),Image.Resampling.NEAREST).tobytes(),r['id']+' exact 4x NEAREST')
 # Native reconstruction cannot access source raster pixels even accidentally.
 import reconstruct, auctioneer
 def forbidden(*a,**k):raise AssertionError('Forbidden raster read/resampling during native authoring')
 with tempfile.TemporaryDirectory(prefix='ch4-native-replay-') as tmp:
  reconstruct.OUT=Path(tmp)
  with patch.object(Image,'open',forbidden),patch.object(Image.Image,'resize',forbidden),patch.object(Image.Image,'crop',forbidden),patch.object(Image.Image,'quantize',forbidden),patch.object(Image.Image,'filter',forbidden),patch.object(Image.Image,'transform',forbidden):
   reconstruct.lobby();reconstruct.portrait_background();reconstruct.restroom();reconstruct.ballroom()
   auctioneer.auctioneer(Path(tmp)/'CH4-03-auctioneer-showman-v01.png')
  for r in m['assets']:
   p=Path(tmp)/Path(r['native']['file']).name
   check(p.read_bytes()==(ROOT/r['native']['file']).read_bytes(),r['id']+' deterministic blank-canvas replay with raster reads and resampling disabled')
 for r in m['approvedReferences']:
  check(digest(REPO/r['canonicalPath'])==r['sha256'] and digest(ROOT/r['reviewCopy'])==r['sha256'],'approved reference unchanged: '+r['canonicalPath'])
 pin=json.loads((ROOT/'evidence/source-pin.json').read_text())
 for f,h in pin['files'].items():check(digest(REPO/f)==h,'canonical source preserved: '+f)
 diff=subprocess.check_output(['git','diff',m['baseCommit'],'--name-only'],cwd=REPO,text=True).splitlines()
 allowed=str(ROOT.relative_to(REPO).parent)+'/'
 check(all(f.startswith(allowed) for f in diff),'all tracked canonical files outside this review package unchanged from pinned main')
 check(all(r['assetPath'] is None and r['status']=='generated / unselected' for r in m['assets']),'no candidate approval/integration registration')
 bg=Image.open(ROOT/'native/CH4-02-auctioneer-background-v01.png').convert('RGBA');fg=Image.open(ROOT/'native/CH4-03-auctioneer-showman-v01.png')
 composite=Image.open(ROOT/'previews/auctioneer-composite-v01.png')
 check(composite.tobytes()==Image.alpha_composite(bg,fg).convert('RGB').tobytes(),'portrait composition is exact layered native foreground/background')
 from html.parser import HTMLParser
 class Links(HTMLParser):
  def handle_starttag(self,tag,attrs):
   for k,v in attrs:
    if k in ['href','src'] and v and not v.startswith(('#','http:','https:','data:')):check((ROOT/v).is_file(),'gallery local resource: '+v)
 # Validation file itself is created below, so allow it during link verification.
 (ROOT/'evidence/validation.json').touch(exist_ok=True)
 Links().feed((ROOT/'index.html').read_text())
 report={'passed':True,'checks':checks,'checkCount':len(checks),'artisticApproval':False,'nativeGridAuthorship':'All five replay byte-for-byte with Image.open/resize/crop/filter/quantize/transform disabled. This establishes the submitted coordinate-source pipeline, not artistic merit.'}
 (ROOT/'evidence/validation.json').write_text(json.dumps(report,indent=2)+'\n')
 print(f'{len(checks)} checks passed. Native-grid replay and contracts verified; creative approval pending.')

if __name__=='__main__':main()
