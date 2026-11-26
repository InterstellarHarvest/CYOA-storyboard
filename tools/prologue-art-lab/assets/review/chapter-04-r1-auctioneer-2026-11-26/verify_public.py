"""Verify committed public bytes and immutable canonical inputs for the R1 package."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from PIL import Image
import argparse, hashlib, json, subprocess
B=Path(__file__).resolve().parent
REPO=next(p for p in B.parents if(p/'story/artwork.draft.json').exists())
BRANCH='art/ch4-r1-auctioneer-review-20261126'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--commit',required=True);ap.add_argument('--out',required=True);args=ap.parse_args()
 out=Path(args.out).resolve();assert not out.is_relative_to(B)
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()==args.commit
 refs=subprocess.check_output(['git','ls-remote','origin','refs/heads/'+BRANCH,'refs/heads/main','refs/pull/32/head'],cwd=REPO,text=True)
 remote={line.split()[1]:line.split()[0]for line in refs.splitlines()};assert remote['refs/heads/'+BRANCH]==args.commit
 paths=subprocess.check_output(['git','ls-tree','-r','--name-only',args.commit,'--',str(B.relative_to(REPO))],cwd=REPO,text=True).splitlines()
 tasks=[{'path':p,'commit':args.commit,'sha256':hashlib.sha256((REPO/p).read_bytes()).hexdigest(),'role':'review-package'}for p in paths]
 r=json.loads((B/'v01/evidence/references.json').read_text());a=json.loads((B/'environment-assessment/manifest.json').read_text())
 for rec in r+a['approvedAssets']+a['benchmarks']:
  tasks.append({'path':rec['sourcePath'],'commit':rec['sourceCommit'],'sha256':rec['sha256'],'role':'immutable-canonical-reference'})
 def verify(task):
  url='https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/'+task['commit']+'/'+task['path']
  data=subprocess.check_output(['curl','--retry','2','--fail','--silent','--show-error','--location','--max-time','90',url]);sha=hashlib.sha256(data).hexdigest();assert sha==task['sha256'],url
  dims=None
  if task['path'].endswith('.png'):
   with Image.open(BytesIO(data))as im:im.load();dims=list(im.size)
  return {**task,'url':url,'publicBytesMatch':True,'dimensions':dims}
 with ThreadPoolExecutor(max_workers=8)as pool:verified=list(pool.map(verify,tasks))
 changed=subprocess.check_output(['git','diff','--name-only','2af6606c25ce252752c65aa5c68c87ff84f804ae',args.commit],cwd=REPO,text=True).splitlines()
 assert all(p.startswith(str(B.relative_to(REPO))+'/')for p in changed)
 report={'passed':True,'commit':args.commit,'branch':BRANCH,'remoteRefsObserved':remote,'allPublicHashesMatch':True,'publicObjectsVerified':len(verified),'pngsDecoded':sum(r['dimensions']is not None for r in verified),'canonicalReferenceCopiesVerified':len(tasks)-len(paths),'onlyNewR1PackageChanged':True,'artisticGatePassed':False,'productionSelectionsChanged':False,'files':verified}
 out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='files'}))
if __name__=='__main__':main()
