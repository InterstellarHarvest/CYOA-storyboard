from pathlib import Path
from PIL import Image
from html.parser import HTMLParser
import json,hashlib,subprocess,os
ROOT=Path(__file__).resolve().parents[1];REPO=next(p for p in ROOT.parents if (p/'story/artwork.draft.json').exists());BASE='81cf3b5f022510737bdd2d4ba3703e0173d86772'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 checks=[]
 def check(v,label):
  assert v,label
  checks.append({'check':label,'passed':True})
 m=json.loads((ROOT/'manifest.json').read_text());pal='palette' in ROOT.name;assets=m['assets'];check(len(assets)==(2 if pal else 6),'Exact requested candidate count')
 for a in assets:
  check(a['status']=='UNSELECTED' and not a['selected'],'New candidate unselected '+a['id']);native=ROOT/a['native']['file'];im=Image.open(native);big=Image.open(ROOT/a['preview4x']['file']);size=(564,278) if a['kind']!='scene' else (314,206)
  check(im.size==size and sha(native)==a['native']['sha256'],'Native dimensions/hash '+a['id']);alpha=im.convert('RGBA').getchannel('A');check(alpha.getextrema()==(0,255) if a['kind']=='portrait' else alpha.getextrema()==(255,255),'Alpha contract '+a['id']);check(big.size==(size[0]*4,size[1]*4) and big.tobytes()==im.resize(big.size,Image.Resampling.NEAREST).tobytes(),'Exact nearest4x '+a['id'])
  if a['kind']=='portrait':check(len({p[:3] for p in im.convert('RGBA').get_flattened_data() if p[3]>=245})==64 and set(alpha.get_flattened_data())=={0,255},'Compact64-tone deliberate foreground and hard pixel cutout '+a['id'])
 # Every image/record in prior immutable review packages and canonical story stays intact.
 old_roots=['tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21','tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/v01','story','assets/selected'];preserved=0
 for path in subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,*old_roots],cwd=REPO,text=True).splitlines():
  old=old_roots[0]
  if path.startswith(old+'/') and Path(path).relative_to(old).parts[0] not in ['v01','v02','v03','v04','v05','v06','v07','v08','portrait-study-01','portrait-study-02']:continue
  check((REPO/path).read_bytes()==subprocess.check_output(['git','show',BASE+':'+path],cwd=REPO),'Immutable previous file '+path);preserved+=1
 if pal:
  prior=json.loads((ROOT.parent/'v01/manifest.json').read_text())['assets'];check(all(sha(ROOT.parent/'v01'/a['native']['file'])==a['native']['sha256'] for a in prior),'All five approved v01 native PNG hashes unchanged')
  bg=Image.open(ROOT.parent/'v01/native/CH4-B2-03-v01.png').convert('RGBA')
  for a in assets:check(Image.open(ROOT/f'previews/{a["id"]}-composite.png').tobytes()==Image.alpha_composite(bg,Image.open(ROOT/a['native']['file']).convert('RGBA')).tobytes(),'Exact composition on frozen approved background '+a['id'])
 else:
  inv=json.loads((ROOT/'evidence/inventory-source.json').read_text());nodes=json.loads((ROOT/'evidence/canonical-nodes.json').read_text());check([a['inventoryId']for a in assets]==inv['group']['inventoryIds'],'Exact canonical B2-02 inventory membership');check(set(nodes)==set(inv['group']['nodeIds']) and len(nodes)==7,'Canonical seven-node coverage')
  for a,item in zip(assets,inv['assets']):check(a['nodeIds']==item['nodeIds'],'Exact inventory/node mapping '+a['id'])
  fg=Image.open(ROOT/assets[4]['native']['file']).convert('RGBA');bg=Image.open(ROOT/assets[5]['native']['file']).convert('RGBA');check(Image.open(ROOT/'previews/foreman-composite.png').tobytes()==Image.alpha_composite(bg,fg).tobytes(),'Foreman exact two-layer composite')
 class Links(HTMLParser):
  def handle_starttag(self,t,attrs):
   for k,v in attrs:
    if v=='evidence/validation.json':continue
    if k in ['src','href','data-one','data-four'] and v and not v.startswith(('https:','http:','#','data:')):check((ROOT/v).is_file(),'Gallery dependency '+v)
 Links().feed((ROOT/'index.html').read_text())
 files=[p for name in ['native','previews','comparisons']for p in (ROOT/name).glob('*.png')]+[ROOT/'manifest.json',ROOT/'index.html'];before={str(p.relative_to(ROOT)):sha(p)for p in files}
 for script in ['prepare.py','package.py']:subprocess.run(['python3',str(ROOT/'source'/script)],env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),check=True,stdout=subprocess.DEVNULL)
 check(all(sha(ROOT/p)==h for p,h in before.items()),'Exact reproducible native/preview/composite/gallery replay')
 report={'passed':True,'checksPassed':len(checks),'candidateCount':len(assets),'selected':False,'sourceDerived':True,'priorFilesPreserved':preserved,'replayFilesIdentical':len(before),'canonicalNarrativeChanged':False,'approvedPNGModified':False,'checks':checks};(ROOT/'evidence/validation.json').write_text(json.dumps(report,indent=2)+'\n');print(str(len(checks))+' checks passed for '+ROOT.name)
if __name__=='__main__':main()
