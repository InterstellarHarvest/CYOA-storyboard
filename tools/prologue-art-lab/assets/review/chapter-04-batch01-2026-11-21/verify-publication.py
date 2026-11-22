"""Verify published review files and every HTML/manifest-referenced image.

Read-only HTTP checks. Output must be outside this committed review package.
Usage: python3 verify-publication.py --commit SHA --out /tmp/ch4-publication.json
"""
from pathlib import Path
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, unquote
import argparse,hashlib,json,subprocess,time

ROOT=Path(__file__).resolve().parent
REPO=next(p for p in ROOT.parents if (p/'story/artwork.draft.json').exists())
PREFIX=ROOT.relative_to(REPO).as_posix()

def fetch(url):
 for attempt in range(3):
  try:
   # Use the platform curl trust store; do not disable TLS certificate validation.
   result=subprocess.check_output(['curl','--fail','--silent','--show-error','--location','--connect-timeout','15','--max-time','45','--write-out','\n__CH4_HTTP__%{http_code}\t%{content_type}',url])
   body,metadata=result.rsplit(b'\n__CH4_HTTP__',1)
   status,mime=metadata.decode().split('\t',1)
   return int(status),mime,body
  except Exception:
   if attempt==2:raise
   time.sleep(1+attempt)

class Links(HTMLParser):
 def __init__(self,base,targets):super().__init__();self.base=base;self.targets=targets
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if not v or k not in ['src','href','data-native','data-large','value']:continue
   u=urlparse(v)
   if u.scheme or u.netloc or not u.path:continue
   p=(self.base/unquote(u.path)).resolve()
   if not p.is_relative_to(ROOT):raise ValueError('Reference outside review package: '+v)
   if p.is_dir():p=p/'index.html'
   if not p.is_file():raise FileNotFoundError(p)
   self.targets.add(p)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--commit',required=True);ap.add_argument('--out',required=True);ap.add_argument('--version',default='v03');args=ap.parse_args()
 out=Path(args.out).resolve()
 assert not out.is_relative_to(ROOT),'Remote report must not change the verified package'
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
 assert head==args.commit,'Verify the checked-out commit'
 branch='art/ch4-batch01-review-20261121'
 remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/'+branch],cwd=REPO,text=True).strip()
 assert remote.split()[0]==head,'Remote branch must equal the intended commit'
 targets=set(ROOT.rglob('*.html'))
 for p in sorted(targets):Links(p.parent,targets).feed(p.read_text())
 # Include all image contract files and originals, not just currently visible HTML.
 targets.update(p for p in ROOT.rglob('*.png') if '__pycache__' not in p.parts)
 targets.update(ROOT.rglob('manifest.json'))
 targets.add(ROOT/'SHA256SUMS')
 raw='https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/'+head+'/'
 def check(p):
  url=raw+p.relative_to(REPO).as_posix();status,mime,body=fetch(url)
  expected=hashlib.sha256(p.read_bytes()).hexdigest();actual=hashlib.sha256(body).hexdigest()
  assert status==200 and actual==expected,'Remote bytes differ: '+url
  if p.suffix=='.png':assert body.startswith(b'\x89PNG\r\n\x1a\n'),'Invalid PNG: '+url
  return {'path':p.relative_to(ROOT).as_posix(),'url':url,'status':status,'mime':mime,'sha256':actual,'byteMatch':True}
 results=[]
 with ThreadPoolExecutor(max_workers=6) as pool:
  jobs={pool.submit(check,p):p for p in targets}
  for job in as_completed(jobs):
   results.append(job.result())
   if len(results)%15==0:print('Verified',len(results),'/',len(targets),'remote files',flush=True)
 gallery='https://raw.githack.com/InterstellarHarvest/CYOA-storyboard/'+head+'/'+PREFIX+'/'+args.version+'/index.html'
 mirror={'url':gallery,'available':False}
 try:
  status,mime,body=fetch(gallery)
  mirror.update(status=status,mime=mime,available=status==200 and 'text/html' in mime and body==(ROOT/args.version/'index.html').read_bytes())
 except Exception as exc:mirror['error']=str(exc)
 report={'remoteBranch':branch,'commit':head,'remoteRefVerified':True,'filesVerified':len(results),'imagesVerified':sum(r['path'].endswith('.png') for r in results),'allBytesMatch':True,'browserGallery':mirror,'files':sorted(results,key=lambda r:r['path'])}
 out.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k!='files'},indent=2))

if __name__=='__main__':main()
