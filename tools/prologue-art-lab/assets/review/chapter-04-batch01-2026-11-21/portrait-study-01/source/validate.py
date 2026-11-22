"""Validate honest study packaging, preservation and presentation, not approval."""
from pathlib import Path
from PIL import Image
from html.parser import HTMLParser
import hashlib, json, subprocess

ROOT=Path(__file__).resolve().parent.parent
REVIEW=ROOT.parent
REPO=next(p for p in REVIEW.parents if (p/'story/artwork.draft.json').exists())

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    checks=[]
    def check(condition,label):
        assert condition,label
        checks.append({'check':label,'passed':True})
    baseline=json.loads((ROOT/'evidence/preservation-baseline.json').read_text())
    for name,expected in baseline['files'].items():
        check((REVIEW/name).is_file() and sha(REVIEW/name)==expected,'Preserved earlier bytes: '+name)
    frozen=json.loads((ROOT/'evidence/frozen-environments.json').read_text())
    for f in frozen['files']:
        check(sha(REVIEW/f['file'])==f['sha256'],'Frozen owner-review PNG: '+f['file'])
    manifest=json.loads((ROOT/'manifest.json').read_text())
    receipt=json.loads((ROOT/'evidence/generation-receipt.json').read_text())
    check(manifest['status']=='UNSELECTED','No artwork selection claimed')
    check(manifest['nativeCandidate'] is None,'No invalid native candidate presented')
    check(not receipt['nativeSizeGatePassed'] and not receipt['nativeAuthorshipProven'],'Failed native output gate explicitly recorded')
    check(not receipt['resized'] and not receipt['nativeCandidateProduced'],'No downsized/native derivative claimed')
    check(not (ROOT/'native').exists(),'No manufactured native asset directory')
    for a in manifest['assets']:
        one=ROOT/a['original']['file'];four=ROOT/a['exact4x']['file']
        check(sha(one)==a['original']['sha256'],'Original hash: '+a['id'])
        check(sha(four)==a['exact4x']['sha256'],'Preview hash: '+a['id'])
        with Image.open(one) as im,Image.open(four) as enlarged:
            check(list(im.size)==a['original']['dimensions'],'Original dimensions: '+a['id'])
            check(enlarged.size==(im.width*4,im.height*4),'Exact 4× dimensions: '+a['id'])
            check(im.mode==enlarged.mode,'Alpha/mode preserved: '+a['id'])
            expected=im.resize(enlarged.size,Image.Resampling.NEAREST)
            check(enlarged.tobytes()==expected.tobytes(),'Every 4× preview pixel exact: '+a['id'])
            if a['id']=='raster-test':
                check(im.size==(1785,881) and im.size!=(564,278),'Test remains actual non-native 1785×881')
                check(sha(one)==receipt['sha256'],'Generated master bytes match original receipt')
            elif a['id']!='frontal-reference':
                check(im.size==(564,278),'v05/approved native raster: '+a['id'])
    sheet=ROOT/'comparisons/native-v05-and-approved.png'
    with Image.open(sheet) as one,Image.open(ROOT/'comparisons/native-v05-and-approved-exact-4x.png') as four:
        check(four.tobytes()==one.resize(four.size,Image.Resampling.NEAREST).tobytes() and four.size==(one.width*4,one.height*4),'Native benchmark sheet exact 4×')
    class Links(HTMLParser):
        def handle_starttag(self,tag,attrs):
            for key,value in attrs:
                if key not in ['src','href','data-one','data-four'] or not value or value.startswith(('#','http:','https:')):continue
                p=(ROOT/value).resolve()
                if p==ROOT/'evidence/validation.json':
                    check(p.parent.is_dir(),'Validation report destination exists; this run writes the self-referenced report')
                else:
                    check(p.is_file() and p.is_relative_to(REVIEW),'Gallery dependency exists: '+value)
    Links().feed((ROOT/'index.html').read_text())
    changed=subprocess.check_output(['git','diff','--name-only',baseline['baseCommit'],'--','story','assets','docs','.github'],cwd=REPO,text=True).strip()
    check(not changed,'Canonical/production/story/assets/docs/workflow paths unchanged')
    report={'passed':True,'packagingChecksPassed':len(checks),'artworkApproved':False,'productionNativeGatePassed':False,'newNativeCandidateExists':False,'frozenEnvironmentPNGsUnchanged':True,'earlierVersionFilesPreserved':len(baseline['files']),'checks':checks}
    (ROOT/'evidence/validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(str(len(checks))+' study preservation/presentation checks passed. New native candidate: NONE; production native gate: FAILED.')

if __name__=='__main__':main()
