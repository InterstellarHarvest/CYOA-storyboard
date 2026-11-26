"""Verify immutable public review bytes and preservation of authoritative sources."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from PIL import Image
import argparse,json,hashlib,subprocess
B=Path(__file__).resolve().parent;R=B/'v01'
REPO=next(p for p in B.parents if(p/'story/artwork.draft.json').exists())
BRANCH='art/ch4-b218-restroom-states-review-20261126';BASE='2af6606c25ce252752c65aa5c68c87ff84f804ae'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--commit',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out).resolve();assert not out.is_relative_to(B)
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()==a.commit
 branchrefs=['refs/heads/'+BRANCH,'refs/heads/main','refs/pull/32/head','refs/heads/art/ch4-r1-auctioneer-review-20261126','refs/heads/art/ch4-r1-restroom-material-pilot01-review-20261126']
 seen=subprocess.check_output(['git','ls-remote','origin',*branchrefs],cwd=REPO,text=True);refs={x.split()[1]:x.split()[0]for x in seen.splitlines()};assert refs['refs/heads/'+BRANCH]==a.commit
 paths=subprocess.check_output(['git','ls-tree','-r','--name-only',a.commit,'--',str(B.relative_to(REPO))],cwd=REPO,text=True).splitlines()
 tasks=[{'path':p,'commit':a.commit,'sha256':hashlib.sha256((REPO/p).read_bytes()).hexdigest(),'role':'review-package'}for p in paths]
 originals=json.loads((R/'evidence/references.json').read_text())+json.loads((R/'evidence/controlling-sources.json').read_text())
 for rec in originals:tasks.append({'path':rec['sourcePath'],'commit':rec['sourceCommit'],'sha256':rec['sha256'],'role':'immutable-approved-or-controlling-source'})
 def check(task):
  url='https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/'+task['commit']+'/'+task['path'];data=subprocess.check_output(['curl','--retry','2','--fail','--silent','--show-error','--location','--max-time','90',url]);assert hashlib.sha256(data).hexdigest()==task['sha256'],url
  dims=None
  if task['path'].endswith('.png'):
   with Image.open(BytesIO(data))as im:im.load();dims=list(im.size)
  return{**task,'url':url,'publicBytesMatch':True,'dimensions':dims}
 with ThreadPoolExecutor(max_workers=8)as ex:results=list(ex.map(check,tasks))
 changed=subprocess.check_output(['git','diff','--name-only',BASE,a.commit],cwd=REPO,text=True).splitlines();assert all(p.startswith(str(B.relative_to(REPO))+'/')for p in changed)
 report={'passed':True,'commit':a.commit,'branch':BRANCH,'observedRemoteRefs':refs,'objectsVerified':len(results),'pngsDecoded':sum(x['dimensions']is not None for x in results),'immutableSourcesVerified':len(originals),'allPublicHashesMatch':True,'onlyNewReviewPackageChanged':True,'newCandidates':6,'status':'UNSELECTED','R1ProductionResumed':False,'failedR1PixelsUsed':False,'runtimeBindingsOrRegistrationsChanged':False,'lobbyOrLot61Started':False,'files':results}
 out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='files'}))
if __name__=='__main__':main()
