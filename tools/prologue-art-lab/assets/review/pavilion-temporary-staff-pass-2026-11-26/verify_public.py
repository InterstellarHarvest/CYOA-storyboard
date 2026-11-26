"""Verify every committed package byte publicly, plus pinned canonical inputs."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess, hashlib, json, argparse, io, time
from PIL import Image

ROOT=Path(__file__).resolve().parent
REPO=next(p for p in ROOT.parents if (p/'story/artwork.draft.json').exists())
PREFIX=ROOT.relative_to(REPO).as_posix()
BASE='89cf0adf09dfadba27bb82f87201160f68818b46'
BRANCH='art/pavilion-temporary-staff-pass-review-20261126'
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def sha(b):return hashlib.sha256(b).hexdigest()
def check(item):
    commit,path,expected=item
    url='https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/'+commit+'/'+path
    for attempt in range(4):
        try:
            # System curl uses the platform trust store; do not disable TLS checks.
            data=subprocess.check_output(['curl','--fail','--silent','--show-error','--location','--max-time','90',url])
            assert sha(data)==expected,(path,'SHA-256 mismatch')
            dimensions=None
            if path.endswith('.png'):
                im=Image.open(io.BytesIO(data));im.load();dimensions=list(im.size)
            return {'commit':commit,'path':path,'sha256':expected,'bytes':len(data),'dimensions':dimensions,'passed':True}
        except Exception:
            if attempt==3:raise
            time.sleep(attempt+1)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--commit',required=True);ap.add_argument('--out',required=True);args=ap.parse_args()
    assert git('merge-base',BASE,args.commit).decode().strip()==BASE
    changed=git('diff','--name-only',BASE,args.commit).decode().splitlines()
    assert changed and all(p.startswith(PREFIX+'/') for p in changed),changed
    remote=git('ls-remote','origin','refs/heads/'+BRANCH).decode().split()[0]
    assert remote==args.commit,(remote,args.commit)
    paths=git('ls-tree','-r','--name-only',args.commit,'--',PREFIX).decode().splitlines()
    jobs=[(args.commit,p,sha(git('show',args.commit+':'+p))) for p in paths]
    refs=[]
    for folder in ['v01']:
        for r in json.loads((ROOT/folder/'evidence/references.json').read_text()):refs.append((r['sourceCommit'],r['sourcePath'],r['sha256']))
    refs += [(r['sourceCommit'],r['sourcePath'],r['sha256']) for r in json.loads((ROOT/'v01/evidence/controlling-sources.json').read_text())]
    for c,p,h in refs:assert sha(git('show',c+':'+p))==h
    with ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(check,jobs+refs))
    report={'passed':True,'commit':args.commit,'remoteBranch':BRANCH,'baseMain':BASE,'packageFiles':len(jobs),'immutableCanonicalInputs':len(refs),'packageOnlyDiff':True,'allPublicBytesAndHashesVerified':True,'results':results}
    Path(args.out).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='results'}))
if __name__=='__main__':main()
