"""Add a read-only online-gallery entry pinned to the committed v05 art package."""
from pathlib import Path
from urllib.parse import urlparse
import argparse,re,json,hashlib
ROOT=Path(__file__).resolve().parent.parent
REPO=next(p for p in ROOT.parents if (p/'story/artwork.draft.json').exists())

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--asset-commit',required=True);args=ap.parse_args()
 raw='https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/'+args.asset_commit+'/'
 blob='https://github.com/InterstellarHarvest/CYOA-storyboard/blob/'+args.asset_commit+'/'
 def rewrite(m):
  attr,value=m.group(1),m.group(2)
  if not value or value.startswith('#') or urlparse(value).scheme:return m.group(0)
  target=(ROOT/value).resolve();assert target.is_file() and target.is_relative_to(ROOT.parent),value
  return attr+'="'+(raw if target.suffix=='.png' else blob)+target.relative_to(REPO).as_posix()+'"'
 text=re.sub(r'\b(src|href|data-native|data-large|value)="([^"\n]*)"',rewrite,(ROOT/'index.html').read_text())
 (ROOT/'online.html').write_text(text)
 (ROOT/'evidence/online-provenance.json').write_text(json.dumps({'assetCommit':args.asset_commit,'onlineGallery':'online.html','sha256':hashlib.sha256(text.encode()).hexdigest(),'note':'Absolute PNG/dependency URLs pin the preserved source-art commit. The final publication commit adds this browser entry without changing art pixels.'},indent=2)+'\n')

if __name__=='__main__':main()
