"""Preservation/provenance and presentation QA; no claim of native authorship."""
from pathlib import Path
from PIL import Image
from html.parser import HTMLParser
import hashlib,json,subprocess

ROOT=Path(__file__).resolve().parent.parent
REVIEW=ROOT.parent
REPO=next(p for p in REVIEW.parents if (p/'story/artwork.draft.json').exists())

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 checks=[]
 def check(value,label):
  assert value,label
  checks.append({'check':label,'passed':True})
 baseline=json.loads((ROOT/'evidence/preservation-baseline.json').read_text())
 for name,expected in baseline['files'].items():
  check((REVIEW/name).is_file() and sha(REVIEW/name)==expected,'Earlier file preserved: '+name)
 frozen=json.loads((ROOT/'evidence/frozen-environments.json').read_text())
 for f in frozen['files']:check(sha(REVIEW/f['file'])==f['sha256'],'Frozen v05 environment unchanged: '+f['file'])
 receipt=json.loads((ROOT/'evidence/generation-receipt.json').read_text());m=json.loads((ROOT/'manifest.json').read_text())
 check(receipt['inputCount']==2,'Exactly two generation reference images')
 check(not receipt['highDetailAuctioneerReferenceUsed'] and not receipt['previousAuctioneerUsedAsInput'],'No detailed or previous auctioneer supplied')
 check([Path(f['file']).name for f in receipt['inputReferences']]==['pavilion_attendant_idle.png','pavilion_presenter_idle.png'],'Approved Pavilion style references only')
 for f in receipt['inputReferences']:check(sha(ROOT/f['file'])==f['sha256'],'Generation reference hash: '+f['file'])
 original=ROOT/receipt['originalFile']
 check(sha(original)==receipt['sha256'],'Original generated PNG bytes preserved')
 with Image.open(original) as im:
  check(im.size==(1788,880) and im.mode=='RGBA','Actual original dimensions/transparency recorded')
  check(im.getchannel('A').getextrema()==(0,255),'Genuine transparent background exists')
  with Image.open(ROOT/'diagnostics/CH4-03-layout-only-source-derived-564x278.png') as diag:
   check(diag.tobytes()==im.resize((564,278),Image.Resampling.NEAREST).tobytes(),'Layout diagnostic explicitly follows recorded source-derived operation')
   check('SOURCE-DERIVED' in diag.info['Classification'],'Diagnostic PNG contains non-native provenance label')
 check(m['status']=='UNSELECTED' and not m['productionReady'] and m['nativeCandidate'] is None,'No approval or production/native completion claimed')
 check(not (ROOT/'native').exists(),'Source-derived diagnostic not placed under native assets')
 pairs=[(m['original'],m['originalExact4x']),(m['compositeLayoutDiagnostic'],m['compositeExact4x'])]+[(a['one'],a['exact4x']) for a in m['comparisonAssets']]+[(m['comparisonSheets'][0],m['comparisonSheets'][1])]
 for a,b in pairs:
  check(sha(ROOT/a['file'])==a['sha256'] and sha(ROOT/b['file'])==b['sha256'],'Manifest hashes: '+a['file'])
  with Image.open(ROOT/a['file']) as one,Image.open(ROOT/b['file']) as four:
   check(four.size==(one.width*4,one.height*4) and four.mode==one.mode,'Exact4x dimensions/mode: '+a['file'])
   check(four.tobytes()==one.resize(four.size,Image.Resampling.NEAREST).tobytes(),'Every exact4x pixel: '+a['file'])
 class Links(HTMLParser):
  def handle_starttag(self,tag,attrs):
   for k,v in attrs:
    if k not in ['src','href','data-one','data-four'] or not v or v.startswith(('#','http:','https:')):continue
    p=(ROOT/v).resolve()
    if p==ROOT/'evidence/validation.json':continue
    check(p.is_relative_to(REVIEW) and p.is_file(),'Gallery dependency: '+v)
 Links().feed((ROOT/'index.html').read_text())
 changed=subprocess.check_output(['git','diff','--name-only',baseline['baseCommit'],'--','story','assets','docs','.github'],cwd=REPO,text=True).strip()
 check(not changed,'Canonical and production paths unchanged')
 result={'passed':True,'checksPassed':len(checks),'newPortraitGenerated':True,'generationReferences':'approved Pavilion attendant and presenter only','nativeAuthorshipProven':False,'productionReady':False,'artworkApproved':False,'earlierFilesPreserved':len(baseline['files']),'checks':checks}
 (ROOT/'evidence/validation.json').write_text(json.dumps(result,indent=2)+'\n')
 print(str(len(checks))+' preservation/provenance/presentation checks passed; fresh source-sized style candidate remains UNSELECTED.')

if __name__=='__main__':main()
