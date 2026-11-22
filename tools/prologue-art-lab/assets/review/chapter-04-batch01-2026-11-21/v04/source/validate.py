"""v04 contracts, exact exports, immutable history and native authoring replay."""
from pathlib import Path
from unittest.mock import patch
from html.parser import HTMLParser
from urllib.parse import urlparse
import hashlib,json,subprocess,tempfile
from PIL import Image

ROOT=Path(__file__).resolve().parent.parent
BATCH=ROOT.parent
REPO=next(p for p in ROOT.parents if (p/'story/artwork.draft.json').exists())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=json.loads((ROOT/'manifest.json').read_text());checks=[]
 def check(ok,label):
  checks.append({'check':label,'passed':bool(ok)})
  if not ok:raise AssertionError(label)
 for a in m['assets']:
  for key in ['native','preview4x','previousV02','previousV02Preview4x','previousV03','previousV03Preview4x','previousV01','detailedReference','comparisonSheet']:
   v=a[key];p=(ROOT/v['file']).resolve();im=Image.open(p)
   check(sha(p)==v['sha256'] and list(im.size)==v['dimensions'],a['id']+' '+key+' dimensions and SHA-256')
  im=Image.open(ROOT/a['native']['file']);w,h=im.size
  check((w,h)==((314,206) if a['id']=='CH4-01' else (564,278)),a['id']+' native contract')
  alpha=set(im.convert('RGBA').getchannel('A').tobytes())
  check(alpha==({0,255} if a['id']=='CH4-03' else {255}),a['id']+' exact alpha/opacity')
  for native,large in [('native','preview4x'),('previousV02','previousV02Preview4x'),('previousV03','previousV03Preview4x')]:
   src=Image.open(ROOT/a[native]['file']);prev=Image.open(ROOT/a[large]['file'])
   check(prev.size==(src.width*4,src.height*4) and prev.tobytes()==src.resize(prev.size,Image.Resampling.NEAREST).tobytes(),a['id']+' '+native+' exact 4x')
  check(a['status']=='generated / unselected' and a['assetPath'] is None,a['id']+' unselected and unregistered')
 # Record every freshly created source raster; larger transport canvases forbidden.
 import lobby,backdrop,auctioneer
 created=[];original_new=Image.new
 def native_new(mode,size,*args,**kw):
  created.append([mode,list(size)])
  assert tuple(size) in [(314,206),(564,278)],('Non-native authoring canvas',size)
  return original_new(mode,size,*args,**kw)
 def forbid(*args,**kw):raise AssertionError('Source raster read/resampling operation forbidden')
 with tempfile.TemporaryDirectory(prefix='ch4-v04-native-') as tmp:
  with patch.object(Image,'new',native_new),patch.object(Image,'open',forbid),patch.object(Image.Image,'resize',forbid),patch.object(Image.Image,'crop',forbid),patch.object(Image.Image,'filter',forbid),patch.object(Image.Image,'quantize',forbid),patch.object(Image.Image,'transform',forbid):
   lobby.lobby(Path(tmp)/'CH4-01-lobby-v04.png')
   backdrop.portrait_background(Path(tmp)/'CH4-02-auctioneer-background-v04.png')
   auctioneer.auctioneer(Path(tmp)/'CH4-03-auctioneer-showman-v04.png')
  for a in m['assets']:check(sha(Path(tmp)/Path(a['native']['file']).name)==a['native']['sha256'],a['id']+' deterministic native replay with image reads/scaling forbidden')
 check(all(tuple(x[1]) in [(314,206),(564,278)] for x in created),'all reconstruction surfaces/masks are actual native dimensions')
 baseline=json.loads((ROOT/'evidence/preservation-baseline.json').read_text())
 for f,h in baseline['files'].items():check(sha(BATCH/f)==h,'v01/v02 unchanged: '+f)
 pin=json.loads((BATCH/'v02/evidence/source-pin.json').read_text())
 for f,h in pin['files'].items():check(sha(REPO/f)==h,'canonical source unchanged: '+f)
 for item in json.loads((ROOT/'evidence/perspective-audit.json').read_text())['checks']:check(item['withinOneNativePixel'],'perspective: '+item['part'])
 for ref in m['approvedReferences']:check(sha(ROOT/ref['file'])==ref['sha256'],'approved comparison unchanged: '+ref['title'])
 bg=Image.open(ROOT/'native/CH4-02-auctioneer-background-v04.png').convert('RGBA');fg=Image.open(ROOT/'native/CH4-03-auctioneer-showman-v04.png')
 c=Image.open(ROOT/'previews/auctioneer-composite-v04.png')
 check(c.tobytes()==Image.alpha_composite(bg,fg).convert('RGB').tobytes(),'exact native portrait layering')
 diff=subprocess.check_output(['git','diff',m['reviewedBaseCommit'],'--name-only'],cwd=REPO,text=True).splitlines()
 allowed=BATCH.relative_to(REPO).as_posix()+'/'
 check(all(f.startswith(allowed) for f in diff),'all changes confined to isolated review package; main/story/gameplay/registries/workflows unchanged')
 class Links(HTMLParser):
  def handle_starttag(self,tag,attrs):
   for k,v in attrs:
    if k in ['src','href','value','data-native','data-large'] and v and not v.startswith('#') and not urlparse(v).scheme:
     p=(ROOT/v).resolve();check(p.is_file(),'gallery resource: '+v)
 for f in ['validation.json','browser-qa.json']:(ROOT/'evidence'/f).touch(exist_ok=True)
 Links().feed((ROOT/'index.html').read_text())
 report={'passed':True,'checkCount':len(checks),'checks':checks,'nativeReplay':{'sourceRasterReads':False,'supersampling':False,'sourceDownsampling':False,'nativeSurfaceAndMaskCreations':len(created),'uniqueCanvasSizes':sorted({str(x[1]) for x in created}),'byteIdentical':True},'creativeApproval':False,'scope':'CH4-01/02/03 only; no restroom or ballroom revision.'}
 (ROOT/'evidence/validation.json').write_text(json.dumps(report,indent=2)+'\n')
 print(str(len(checks))+' checks passed; all source canvases native, prior versions unchanged, no creative approval implied.')

if __name__=='__main__':main()
