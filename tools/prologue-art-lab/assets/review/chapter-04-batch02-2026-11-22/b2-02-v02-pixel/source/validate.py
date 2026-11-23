from pathlib import Path
from PIL import Image
from collections import Counter,deque
from html.parser import HTMLParser
import hashlib,json,subprocess,os
ROOT=Path(__file__).resolve().parents[1];REPO=next(p for p in ROOT.parents if (p/'story/artwork.draft.json').exists());BASE='b3abaae4238b87bdc27f444637b83a2c549838f9'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stats(path):
 im=Image.open(path).convert('RGB');px=im.load();w,h=im.size;seen=set();small=large=0
 for y in range(h):
  for x in range(w):
   if(x,y)in seen:continue
   c=px[x,y];q=[(x,y)];seen.add((x,y));n=0
   while q:
    u,v=q.pop();n+=1
    for a,b in[(u-1,v),(u+1,v),(u,v-1),(u,v+1)]:
     if 0<=a<w and 0<=b<h and(a,b)not in seen and px[a,b]==c:seen.add((a,b));q.append((a,b))
   if n<=2:small+=1
   if n>=12:large+=1
 return {'RGBColors':len(im.getcolors(w*h)),'oneOrTwoPixelColorComponents':small,'componentsAtLeast12Pixels':large,'note':'Diagnostic only: semantic highlights/lettering/foliage can legitimately form small components; these counts do not establish art approval.'}
def main():
 checks=[]
 def check(v,label):
  assert v,label
  checks.append({'check':label,'passed':True})
 m=json.loads((ROOT/'manifest.json').read_text());reports=json.loads((ROOT/'evidence/native-reconstruction.json').read_text());a=m['assets'];check([x['id']for x in a]==['CH4-B2-06','CH4-B2-07','CH4-B2-08','CH4-B2-09'],'Only four requested main scenes revised')
 diagnostics={}
 for x in a:
  id_=x['id'];p=ROOT/x['native']['file'];im=Image.open(p);big=Image.open(ROOT/x['preview4x']['file']);check(im.size==(314,206)and im.mode=='RGB','Native opaque contract '+id_);check(sha(p)==x['native']['sha256'],'Native manifest hash '+id_);check(big.size==(1256,824)and big.tobytes()==im.resize(big.size,Image.Resampling.NEAREST).tobytes(),'Exact nearest4x '+id_);check(x['status']=='UNSELECTED'and not x['selected']and x['sourceDerived']and not x['independentlyAuthoredAtNativeResolution'],'Honest source-derived/unselected status '+id_)
  r=reports[id_];check(r['nativeStructuralPixelsChangedBeyondMaterialMapping']>100 and not r['newGradients']and not r['dithering'],'Meaningful native structure stage beyond palette fitting '+id_);layer=Image.open(ROOT/r['structureLayer']);under=Image.open(ROOT/f'layers/{id_}-material-underpainting.png');check(Image.alpha_composite(under.convert('RGBA'),layer).convert('RGB').tobytes()==im.tobytes(),'Final rebuilds exactly from native material/structure layers '+id_)
  check(im.tobytes()!=Image.open(ROOT/x['directTransferDiagnostic']['file']).convert('RGB').tobytes(),'Direct transfer is not delivered as final '+id_)
  for rel in x['nativeMasks']:check(Image.open(ROOT/rel).size==(314,206)and set(Image.open(ROOT/rel).get_flattened_data())<={0,255},'Native binary semantic mask '+rel)
  diagnostics[id_]={'previousV01':stats(ROOT/x['previousNative']['file']),'transferDiagnostic':stats(ROOT/x['directTransferDiagnostic']['file']),'nativeV02':stats(p)}
 for name in ['approved-bureau','approved-tower','approved-lobby','approved-restroom']:diagnostics[name]=stats(ROOT/'references'/(name+'.png'))
 (ROOT/'evidence/palette-diagnostics.json').write_text(json.dumps({'notAnApprovalTest':True,'materialRampsAreNotUniversalPaletteCaps':True,'images':diagnostics},indent=2)+'\n')
 # Historical packages, their exact foreman/background and approved sources stay intact.
 prefixes=['tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21','tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22','story','assets/selected'];preserved=0
 for rel in subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,*prefixes],cwd=REPO,text=True).splitlines():
  if rel.startswith(prefixes[0]+'/')and Path(rel).relative_to(prefixes[0]).parts[0]not in['v01','v02','v03','v04','v05','v06','v07','v08','portrait-study-01','portrait-study-02']:continue
  if rel.startswith(prefixes[1]+'/')and Path(rel).relative_to(prefixes[1]).parts[0]not in['v01','v02-npc-palette','b2-02-v01']:continue
  check((REPO/rel).read_bytes()==subprocess.check_output(['git','show',BASE+':'+rel],cwd=REPO),'Immutable prior/canonical file '+rel);preserved+=1
 for x in m['retainedCandidates']:check(sha(ROOT/x['native']['file'])==sha(ROOT/x['originalPath'])==x['native']['sha256'],'Retained exact v01 candidate '+x['id'])
 prior=json.loads((ROOT.parent/'b2-02-v01/manifest.json').read_text())
 for new,old in zip(a,prior['assets'][:4]):check(new['key']==old['key']and new['nodeIds']==old['nodeIds'],'Canonical mappings unchanged '+new['id'])
 class Links(HTMLParser):
  def handle_starttag(self,t,attrs):
   for k,v in attrs:
    if v=='evidence/validation.json':continue
    if k in['src','href','data-one','data-four']and v and not v.startswith(('http:','https:','#','data:')):check((ROOT/v).is_file(),'Gallery dependency '+v)
 Links().feed((ROOT/'index.html').read_text())
 files=[p for n in['native','previews','comparisons','layers','masks']for p in(ROOT/n).glob('*.png')]+[ROOT/'manifest.json',ROOT/'index.html'];before={str(p.relative_to(ROOT)):sha(p)for p in files}
 for n in['native_rebuild.py','package.py']:subprocess.run(['python3',str(ROOT/'source'/n)],env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),check=True,stdout=subprocess.DEVNULL)
 check(all(sha(ROOT/p)==h for p,h in before.items()),'Exact native/layer/mask/gallery replay')
 report={'passed':True,'checksPassed':len(checks),'revisedMainScenes':4,'status':'UNSELECTED','sourceDerived':True,'retainedPriorFiles':preserved,'replayFilesIdentical':len(before),'nativeConstructionBeyondResizeAndPalette':True,'approvedArtModified':False,'narrativeOrGameplayChanged':False,'artisticApproval':False,'checks':checks};(ROOT/'evidence/validation.json').write_text(json.dumps(report,indent=2)+'\n');print(str(len(checks))+' checks passed; four source-derived native reconstructions, no approvals/integration.')
if __name__=='__main__':main()
