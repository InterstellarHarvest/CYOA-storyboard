"""Read-only remote-byte verification; report outside the reviewed package."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,subprocess,argparse
ROOT=Path(__file__).resolve().parents[1];REPO=next(p for p in ROOT.parents if (p/'story/artwork.draft.json').exists())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--commit',required=True);ap.add_argument('--out',required=True);args=ap.parse_args();out=Path(args.out).resolve();assert not out.is_relative_to(ROOT)
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip();assert head==args.commit
 remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/art/ch4-batch01-review-20261121'],cwd=REPO,text=True).split()[0];assert remote==head
 paths=sorted(p for p in ROOT.parent.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
 raw='https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/'+head+'/'
 def check(p):
  url=raw+p.relative_to(REPO).as_posix();data=subprocess.check_output(['curl','--retry','2','--fail','--silent','--show-error','--location','--max-time','45',url]);digest=hashlib.sha256(data).hexdigest();assert digest==hashlib.sha256(p.read_bytes()).hexdigest(),str(p)
  if p.suffix=='.png':assert data.startswith(b'\x89PNG\r\n\x1a\n')
  return {'file':str(p.relative_to(ROOT.parent)),'sha256':digest,'bytesMatch':True,'url':url}
 with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(check,paths))
 report={'passed':True,'remoteBranch':'art/ch4-batch01-review-20261121','commit':head,'remoteRefVerified':True,'filesVerified':len(results),'pngsVerified':sum(x['file'].endswith('.png') for x in results),'allBytesMatch':True,'files':results};out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='files'},indent=2))
if __name__=='__main__':main()
