"""Verify every new package file against the immutable public review commit."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from PIL import Image
import json,hashlib,subprocess,argparse
ROOT=Path(__file__).resolve().parents[1];REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--commit',required=True);ap.add_argument('--out',required=True);args=ap.parse_args();out=Path(args.out).resolve();assert not out.is_relative_to(ROOT)
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip();assert head==args.commit
 remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/art/ch4-b217-ticket-ring-review-20261125'],cwd=REPO,text=True).split()[0];assert remote==head
 paths=sorted(p for p in ROOT.rglob('*')if p.is_file()and'__pycache__'not in p.parts and p.suffix!='.pyc');raw='https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/'+head+'/'
 def verify(p):
  url=raw+p.relative_to(REPO).as_posix();data=subprocess.check_output(['curl','--retry','2','--fail','--silent','--show-error','--location','--max-time','60',url]);digest=hashlib.sha256(data).hexdigest();assert digest==hashlib.sha256(p.read_bytes()).hexdigest(),str(p)
  dimensions=None
  if p.suffix=='.png':
   with Image.open(BytesIO(data))as im:im.load();dimensions=list(im.size)
  return {'file':str(p.relative_to(ROOT)),'sha256':digest,'bytesMatch':True,'decodedDimensions':dimensions,'url':url}
 with ThreadPoolExecutor(max_workers=8)as ex:results=list(ex.map(verify,paths))
 report={'passed':True,'commit':head,'remoteBranchVerified':True,'filesVerified':len(results),'pngsDecoded':sum(x['decodedDimensions']is not None for x in results),'newArtworkStatus':'UNSELECTED','approvedReferenceCopies':'APPROVED / exact bytes','newArtworkOwnerApproved':False,'allBytesMatch':True,'files':results};out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='files'}))
if __name__=='__main__':main()
