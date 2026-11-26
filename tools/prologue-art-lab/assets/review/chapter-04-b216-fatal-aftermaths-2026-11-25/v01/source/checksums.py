"""Refresh or verify every package file hash; checksum record excludes itself."""
from pathlib import Path
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence/checksums.json'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--verify',action='store_true');args=ap.parse_args()
 records={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(ROOT.rglob('*'))if p.is_file()and p!=OUT and'__pycache__'not in p.parts}
 if args.verify:assert json.loads(OUT.read_text())['files']==records
 else:OUT.write_text(json.dumps({'algorithm':'SHA-256','selfExcluded':'evidence/checksums.json','files':records},indent=2)+'\n')
 print(json.dumps({'files':len(records),'verified':args.verify}))
if __name__=='__main__':main()
