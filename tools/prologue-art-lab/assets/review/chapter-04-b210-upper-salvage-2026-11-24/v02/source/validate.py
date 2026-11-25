from pathlib import Path
from PIL import Image,ImageChops
from html.parser import HTMLParser
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];V01=ROOT.parent/'v01';REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists())
BASE='33ec6cec075bbab8ccd5ca1673dcf4b524f41a0e';checks=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(v,n):
    assert v,n
    checks.append({'check':n,'passed':True})
def difference(a,b):
    d=ImageChops.difference(a,b);return ImageChops.lighter(ImageChops.lighter(d.getchannel('R'),d.getchannel('G')),d.getchannel('B'))
def main():
    m=json.loads((ROOT/'manifest.json').read_text());a=m['asset'];im=Image.open(ROOT/a['native']['file']);old=Image.open(V01/'native/CH4-NEW-03-upper-salvage-v01.png');four=Image.open(ROOT/a['preview4x']['file'])
    check(m['status']=='UNSELECTED'and not m['ownerApproved']and m['primaryUnits']==1 and m['supplementalStates']==[],'One unselected scene; no approval or extra states')
    check(len(list((ROOT/'native').glob('*.png')))==1,'No extra native assets')
    check(im.size==(314,206)and im.mode=='RGB','Native314x206 RGB')
    check(four.size==(1256,824)and four.tobytes()==im.resize((1256,824),Image.Resampling.NEAREST).tobytes(),'Exact NN4x export')
    check(sha(ROOT/a['native']['file'])==a['native']['sha256']and sha(ROOT/a['preview4x']['file'])==a['preview4x']['sha256'],'Manifest native/preview hashes')
    d=difference(old,im);allowed=Image.open(ROOT/'masks/authorized-local-repair.png');protected=Image.open(ROOT/'masks/pixel-locked-geography.png')
    check(ImageChops.subtract(d,allowed).getbbox()is None,'Zero pixel changes outside the two authorized fixture regions')
    check(ImageChops.multiply(d,protected).getbbox()is None,'Every visible lift/WC/hatch/stair/rail/duct pixel exact v01')
    for name,box in [('WC full panel',(118,69,141,107)),('central movement floor',(95,125,212,206)),('stairwell and landing',(212,140,314,206)),('upper architecture',(0,0,314,42))]:check(old.crop(box).tobytes()==im.crop(box).tobytes(),name+' entire region exact')
    check((ROOT/'references/v01-before.png').read_bytes()==(V01/'native/CH4-NEW-03-upper-salvage-v01.png').read_bytes(),'Before image exact v01 PNG')
    recipe=json.loads((ROOT/'evidence/repair.json').read_text());result=Image.new('RGBA',(314,206));shared=0
    for rel in recipe['layerOrder']:
        p=ROOT/rel;part=Image.open(p);check(part.mode=='RGBA'and part.size==(314,206),'Native editable layer '+rel)
        check(set(part.getchannel('A').get_flattened_data())<={0,255},'Binary layer transparency '+rel)
        if Path(rel).stem not in recipe['replacedLayers']:check(p.read_bytes()==(V01/rel).read_bytes(),'Shared layer byte-exact '+rel);shared+=1
        result=Image.alpha_composite(result,part)
    check(shared==8,'Only two semantic layers replaced')
    check(result.convert('RGB').tobytes()==im.tobytes(),'Exact layered source assembly')
    check(sha(ROOT/a['native']['file'])==recipe['nativeHash'],'Repair recipe final hash')
    check(sha(V01/'originals/CH4-NEW-03-detailed-reference.png')==recipe['referenceSha256'],'Pinned original detailed concept unchanged')
    for r in json.loads((ROOT/'evidence/benchmark-provenance.json').read_text()):
        data=subprocess.check_output(['git','show',r['sourceCommit']+':'+r['sourcePath']],cwd=REPO);check((ROOT/r['file']).read_bytes()==data,'Exact approved benchmark '+r['file']);check(sha(ROOT/r['file'])==r['sha256'],'Frozen benchmark hash '+r['file'])
    check(a['runtimeBinding']is None and a['newFocusId']is None and a['nodeIds']==json.loads((V01/'manifest.json').read_text())['asset']['nodeIds'],'Canonical three-node coverage and null bindings retained')
    for r in json.loads((ROOT/'evidence/caption-layout.json').read_text()):check(r['fits']and r['textWidth']<r['panelWidth']-8,'Non-overlapping caption '+r['sheet']+'/'+r['caption'])
    pairs=0
    for p in ROOT.rglob('*-4x.png'):
        possible=[p.with_name(p.name.replace('-4x','-native')),ROOT/'native'/p.name.replace('-4x',''),ROOT/'references'/p.name.replace('-4x','')]
        one=next((q for q in possible if q.is_file()),None)
        if one:
            x=Image.open(one);y=Image.open(p);check(y.size==(x.width*4,x.height*4)and y.tobytes()==x.resize(y.size,Image.Resampling.NEAREST).tobytes(),'Exact4x '+str(p.relative_to(ROOT)));pairs+=1
    # The parent index may gain a latest-version link; historical packages,
    # approval records, PMO direction and all canonical files remain immutable.
    index_path=str((ROOT.parent/'README.md').relative_to(REPO));preserved=0;v01_count=0
    for line in subprocess.check_output(['git','ls-tree','-r',BASE],cwd=REPO,text=True).splitlines():
        meta,path=line.split('\t')
        if meta.split()[1]!='blob'or path==index_path:continue
        data=(REPO/path).read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();check(blob==meta.split()[2],'Baseline preserved '+path);preserved+=1
        if path.startswith(str(V01.relative_to(REPO))+'/'):v01_count+=1
    class Links(HTMLParser):
        def __init__(self):super().__init__();self.links=[]
        def handle_starttag(self,t,attrs):self.links +=[v for k,v in attrs if k in['href','src','data-one','data-four']and v and not v.startswith(('#','http'))]
    links=Links();links.feed((ROOT/'index.html').read_text())
    for link in set(links.links):check((ROOT/link).is_file()or link=='evidence/validation.json','Gallery dependency '+link)
    files=list(ROOT.rglob('*.png'))+[ROOT/'manifest.json',ROOT/'index.html',ROOT/'evidence/repair.json'];before={p:sha(p)for p in files}
    for name in['refine_existing.py','package_review.py']:subprocess.run([sys.executable,str(ROOT/'source'/name)],cwd=REPO,check=True,stdout=subprocess.DEVNULL)
    check(all(sha(p)==s for p,s in before.items()),'Deterministic native repair / comparisons / gallery replay')
    out={'technicalPassed':True,'checksPassed':len(checks),'status':'UNSELECTED','ownerApproved':False,'changedNativePixels':m['changedNativePixels'],'unchangedScenePercent':m['unchangedScenePercent'],'geographyPixelExact':True,'outsideAuthorizedChanges':0,'sharedLayersByteExact':shared,'v01FilesByteExact':v01_count,'baselineFilesPreserved':preserved,'exact4xPairs':pairs,'replayedFilesIdentical':len(before),'sourceDerived':True,'canonicalGameplayNarrativeApprovalRecordsChanged':False,'visualAssessment':'evidence/visual-review.md','checks':checks}
    (ROOT/'evidence/validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='checks'}))
if __name__=='__main__':main()
