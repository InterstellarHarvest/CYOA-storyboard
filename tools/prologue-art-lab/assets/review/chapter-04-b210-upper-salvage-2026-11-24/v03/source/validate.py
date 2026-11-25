"""Check the owner-directed combination, preservation and deterministic replay."""
from pathlib import Path
from PIL import Image,ImageChops
from html.parser import HTMLParser
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];V02=ROOT.parent/'v02';V01=ROOT.parent/'v01'
REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists())
BASE='29a23f13ca8824bae3868b46c2afb19f075f7651';checks=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(v,n):
    assert v,n
    checks.append({'check':n,'passed':True})
def diff(a,b):
    d=ImageChops.difference(a,b);return ImageChops.lighter(ImageChops.lighter(d.getchannel('R'),d.getchannel('G')),d.getchannel('B'))
def main():
    m=json.loads((ROOT/'manifest.json').read_text());a=m['asset'];im=Image.open(ROOT/a['native']['file']);old=Image.open(V02/'native/CH4-NEW-03-upper-salvage-v02.png');four=Image.open(ROOT/a['preview4x']['file'])
    check(m['status']=='UNSELECTED'and not m['ownerApproved']and m['primaryUnits']==1 and m['supplementalStates']==[],'One unselected scene; no new state or approval')
    check(len(list((ROOT/'native').glob('*.png')))==1,'Single native asset')
    check(im.size==(314,206)and im.mode=='RGB','Native RGB314x206')
    check(four.size==(1256,824)and four.tobytes()==im.resize((1256,824),Image.Resampling.NEAREST).tobytes(),'Exact nearest-neighbor1256x824')
    check(sha(ROOT/a['native']['file'])==a['native']['sha256']and sha(ROOT/a['preview4x']['file'])==a['preview4x']['sha256'],'Manifest hashes exact')
    delta=diff(old,im);allowed=Image.open(ROOT/'masks/authorized-local-repair.png');protected=Image.open(ROOT/'masks/pixel-locked-geography.png')
    check(ImageChops.subtract(delta,allowed).getbbox()is None,'Zero changed pixels outside authorized rack')
    check(ImageChops.multiply(delta,protected).getbbox()is None,'Existing visible route and rail pixels exact')
    for title,box in [('Whole foreground and left room',(0,0,212,206)),('Whole lower stairwell',(203,140,314,206)),('Upper architecture',(0,0,314,42))]:check(old.crop(box).tobytes()==im.crop(box).tobytes(),title+' pixel exact v02')
    for name in ['material-descending-stairwell.png','material-guardrails.png']:
        p=ROOT/'layers'/name
        check(p.read_bytes()==(V01/'layers'/name).read_bytes()==(V02/'layers'/name).read_bytes(),'Original restored layer byte-exact '+name)
    check((ROOT/'layers/material-foreground-sanitary-salvage.png').read_bytes()==(V02/'layers/material-foreground-sanitary-salvage.png').read_bytes(),'New foreground layer preserved byte-exact v02')
    recipe=json.loads((ROOT/'evidence/repair.json').read_text());assembled=Image.new('RGBA',(314,206));shared=0
    for rel in recipe['layerOrder']:
        part=Image.open(ROOT/rel)
        check(part.size==(314,206)and part.mode=='RGBA'and set(part.getchannel('A').get_flattened_data())<={0,255},'Editable native binary-alpha layer '+rel)
        if Path(rel).stem not in recipe['replacedLayers']:
            check((ROOT/rel).read_bytes()==(V02/rel).read_bytes(),'Shared layer exact '+rel);shared+=1
        assembled=Image.alpha_composite(assembled,part)
    check(shared==9 and assembled.convert('RGB').tobytes()==im.tobytes(),'One changed layer; exact native layer assembly')
    check(recipe['nativeHash']==sha(ROOT/a['native']['file'])and recipe['referenceSha256']==sha(V01/'originals/CH4-NEW-03-detailed-reference.png'),'Final hash and original source provenance')
    for r in json.loads((ROOT/'evidence/benchmark-provenance.json').read_text()):
        data=subprocess.check_output(['git','show',r['sourceCommit']+':'+r['sourcePath']],cwd=REPO)
        check((ROOT/r['file']).read_bytes()==data and sha(ROOT/r['file'])==r['sha256'],'Actual approved benchmark '+r['file'])
    check(a['runtimeBinding']is None and a['newFocusId']is None and a['nodeIds']==json.loads((V01/'manifest.json').read_text())['asset']['nodeIds'],'Three canonical story nodes retained; no new bindings')
    for r in json.loads((ROOT/'evidence/caption-layout.json').read_text()):check(r['fits']and r['textWidth']<r['panelWidth']-8,'Caption fits '+r['sheet']+'/'+r['caption'])
    pairs=0
    for p in ROOT.rglob('*-4x.png'):
        candidates=[p.with_name(p.name.replace('-4x','-native')),ROOT/'native'/p.name.replace('-4x',''),ROOT/'references'/p.name.replace('-4x','')]
        one=next((q for q in candidates if q.is_file()),None)
        if one:
            x=Image.open(one);y=Image.open(p);check(y.size==(x.width*4,x.height*4)and y.tobytes()==x.resize(y.size,Image.Resampling.NEAREST).tobytes(),'Exact4x '+str(p.relative_to(ROOT)));pairs+=1
    # Historical packages and every canonical file are unchanged. Only the
    # parent latest-review index may receive a new link after publication.
    index=str((ROOT.parent/'README.md').relative_to(REPO));preserved=0;versions={'v01':0,'v02':0}
    for line in subprocess.check_output(['git','ls-tree','-r',BASE],cwd=REPO,text=True).splitlines():
        meta,path=line.split('\t')
        if meta.split()[1]!='blob'or path==index:continue
        data=(REPO/path).read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert blob==meta.split()[2],path
        preserved+=1
        for version in versions:
            if path.startswith(str((ROOT.parent/version).relative_to(REPO))+'/'):versions[version]+=1
    check(True,'All '+str(preserved)+' baseline blobs preserved; historical v01/v02 immutable')
    class Links(HTMLParser):
        def __init__(self):super().__init__();self.links=[]
        def handle_starttag(self,t,attrs):self.links +=[v for k,v in attrs if k in['href','src','data-one','data-four']and v and not v.startswith(('#','http'))]
    links=Links();links.feed((ROOT/'index.html').read_text())
    for link in set(links.links):check((ROOT/link).is_file()or link=='evidence/validation.json','Gallery dependency '+link)
    files=list(ROOT.rglob('*.png'))+[ROOT/'manifest.json',ROOT/'index.html',ROOT/'evidence/repair.json'];before={p:sha(p)for p in files}
    for name in ['refine_existing.py','package_review.py']:subprocess.run([sys.executable,str(ROOT/'source'/name)],cwd=REPO,check=True,stdout=subprocess.DEVNULL)
    check(all(sha(p)==s for p,s in before.items()),'Deterministic native assembly and review-gallery replay')
    report={'technicalPassed':True,'checksPassed':len(checks),'status':'UNSELECTED','ownerApproved':False,'changedNativePixelsFromV02':m['changedNativePixels'],'unchangedScenePercentFromV02':m['unchangedScenePercent'],'outsideRackChanges':0,'originalStairsAndRailsByteExact':True,'v02ForegroundByteExact':True,'sharedLayersByteExact':shared,'historicalFilesByteExact':versions,'baselineFilesPreserved':preserved,'exact4xPairs':pairs,'replayedFilesIdentical':len(before),'sourceDerived':True,'stairsPerspectiveClaim':'Original owner-accepted fallback, not corrected perspective','canonicalGameplayNarrativeApprovalRecordsChanged':False,'checks':checks}
    (ROOT/'evidence/validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='checks'}))
if __name__=='__main__':main()
