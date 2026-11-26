"""Hash the whole review package, including assessment and publication receipts."""
from pathlib import Path
import argparse,json,hashlib
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'PACKAGE-SHA256.json'
ap=argparse.ArgumentParser();ap.add_argument('--verify',action='store_true');args=ap.parse_args()
files={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.rglob('*')) if p.is_file() and p!=OUT and '__pycache__' not in p.parts and p.suffix!='.pyc'}
if args.verify:assert json.loads(OUT.read_text())['files']==files
else:OUT.write_text(json.dumps({'algorithm':'SHA-256','selfExcluded':OUT.name,'files':files},indent=2)+'\n')
print(json.dumps({'files':len(files),'verified':args.verify}))
