"""Technical and preservation checks, not a substitute for visual review."""
from pathlib import Path
from PIL import Image
import json,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1];REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=json.loads((ROOT/'manifest.json').read_text());inv=json.loads((ROOT/'evidence/inventory-source.json').read_text());checks=[]
 def check(v,label):
  assert v,label;checks.append({'check':label,'passed':True})
 check(len(m['assets'])==7 and m['status']=='UNSELECTED','Exactly seven UNSELECTED candidates')
 check({a['inventoryId']for a in m['assets']}==set(inv['group']['inventoryIds']),'Exact canonical group demands')
 check(sorted(set(n for a in m['assets']for n in a['nodeIds']))==sorted(m['storyNodeCoverage'])==sorted(inv['group']['nodeIds']),'Exact11-node story coverage')
 reconstruction=json.loads((ROOT/'evidence/native-reconstruction.json').read_text())
 for a in m['assets']:
  check(a['status']=='UNSELECTED'and a['selected']is False,'No owner selection inferred '+a['id'])
  n=ROOT/a['native']['file'];p=ROOT/a['preview4x']['file'];im=Image.open(n);four=Image.open(p)
  check(sha(n)==a['native']['sha256']and sha(p)==a['preview4x']['sha256'],'Manifest PNG hashes '+a['id'])
  check(list(im.size)==a['native']['dimensions']==([314,206]if a['kind']=='scene'else[564,278]),'Native dimensions '+a['id'])
  alpha=im.convert('RGBA').getchannel('A').getextrema()
  check(im.mode=='RGBA'and alpha==(0,255)if a['kind']=='portrait'else alpha==(255,255),'Alpha contract '+a['id'])
  check(four.size==(im.width*4,im.height*4)and four.tobytes()==im.resize(four.size,Image.Resampling.NEAREST).tobytes(),'Exact nearest4x pixels '+a['id'])
  check(a['sourceDerived']and not a['independentlyAuthoredAtNativeResolution']and a['layers']and a['masks'],'Source-derived editable provenance '+a['id'])
  r=reconstruction[a['id']]
  if a['kind']=='scene':check(r['nativeStructuralPixelsChanged']>0 and r['structuralPassChangesInsideProtectedMask']==0,'Separate native structure protects complete story objects '+a['id'])
  check((ROOT/f'comparisons/{a["id"]}-chapter2-native.png').is_file()and(ROOT/f'comparisons/{a["id"]}-chapter2-4x.png').is_file(),'Direct Chapter2 native/4x comparisons '+a['id'])
 for name,b in m['canonicalBenchmarks'].items():check(sha(ROOT/f'references/{name}.png')==b['sha256'],'Exact approved Chapter2 benchmark '+name)
 bg=Image.open(ROOT/'native/CH4-B2-17-v01.png').convert('RGBA')
 for n in [14,15]:
  fg=Image.open(ROOT/f'native/CH4-B2-{n}-v01.png');c=Image.open(ROOT/f'previews/CH4-B2-{n}-composite.png');check(c.tobytes()==Image.alpha_composite(bg,fg).tobytes(),'Independent foreground/background composite '+str(n))
 freeze=json.loads((ROOT/'evidence/frozen-history.json').read_text())
 # Root indexes are append-only current-status guidance; immutable version
 # packages, approval receipts and every earlier image must stay byte-exact.
 mutable={'README.md','AGENTS.md'}
 for rel,digest in freeze['files'].items():
  if rel in mutable:continue
  check(sha(ROOT.parent/rel)==digest,'Historical bytes preserved '+rel)
 base=freeze['baseReviewCommit']
 for path in subprocess.check_output(['git','ls-tree','-r','--name-only',base,'story','assets/selected','.github'],cwd=REPO,text=True).splitlines():
  data=subprocess.check_output(['git','show',base+':'+path],cwd=REPO);check((REPO/path).read_bytes()==data,'Canonical narrative/gameplay/selected registry unchanged '+path)
 text=reconstruction['CH4-B2-18']['lettering']['text']
 check(text==['RESTROOMS','ENTIRE HOTEL','LOT NINETEEN — TWO MATCHING','DECORATIVE LEVERS'],'Full exact canonical isolator wording')
 report={'passed':True,'checksPassed':len(checks),'assets':7,'status':'UNSELECTED','historicalFilesPreserved':len(freeze['files'])-2,'canonicalFilesChanged':0,'integrationPerformed':False,'visualAssessment':'evidence/visual-review.md','checks':checks}
 (ROOT/'evidence/validation.json').write_text(json.dumps(report,indent=2)+'\n');print(f'{len(checks)} technical/preservation checks passed; seven UNSELECTED; no canonical changes.')
if __name__=='__main__':main()
