from pathlib import Path
from PIL import Image, ImageChops
from collections import Counter
import json, hashlib, subprocess, tempfile, shutil, sys
ROOT=Path(__file__).resolve().parents[1];V1=ROOT.parent/'v01'
REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    checks=[]
    def check(label,ok,**details):
        assert ok,(label,details);checks.append({'check':label,'passed':True,**details})
    m=json.loads((ROOT/'manifest.json').read_text());a=m['assets'][0]
    check('Exactly one UNSELECTED lavatory candidate',m['primaryAssetCount']==1 and len(m['assets'])==1 and a['id']=='CH4-NEW-02' and a['status']=='UNSELECTED' and not a['selected'] and not a['ownerApproved'])
    im=Image.open(ROOT/a['native']['file']);four=Image.open(ROOT/a['exact4x']['file'])
    check('314x206 opaque RGB',im.size==(314,206) and im.mode=='RGB')
    check('Native PNG SHA-256',sha(ROOT/a['native']['file'])==a['native']['sha256'])
    check('Exact nearest-neighbor 4x',four.size==(1256,824) and ImageChops.difference(four,im.resize(four.size,Image.Resampling.NEAREST)).getbbox() is None)
    layers=json.loads((ROOT/'evidence/native-layer-recipes.json').read_text())['room'];out=Image.new('RGBA',im.size)
    for r in layers:
        layer=Image.open(ROOT/r['file']);check('Native binary RGBA layer '+r['file'],layer.mode=='RGBA' and layer.size==im.size and set(layer.getchannel('A').get_flattened_data())<={0,255} and sha(ROOT/r['file'])==r['sha256']);out=Image.alpha_composite(out,layer)
    check('Exact native layer compositing',ImageChops.difference(out.convert('RGB'),im).getbbox() is None)
    for kind in ['smooth','ridged','third']:
        p='layers/room-shell-'+kind+'.png'
        check('Exact original '+kind+' shell layer',sha(ROOT/p)==sha(V1/p))
        old=Image.open(V1/p);mask=old.getchannel('A');difference=ImageChops.difference(im,Image.open(V1/'native/CH4-NEW-02-bridal-lavatory-v01.png'))
        check('Final opaque '+kind+' shell pixels unchanged',all(ImageChops.multiply(band,mask).getbbox() is None for band in difference.split()))
        p='masks/room-shell-'+kind+'.png';check('Exact '+kind+' silhouette/position mask',sha(ROOT/p)==sha(V1/p))
    freeze=json.loads((ROOT/'evidence/v01-freeze.json').read_text())
    for p,digest in freeze['files'].items():assert sha(REPO/p)==digest,p
    check('Every historical v01 package file unchanged',True,files=len(freeze['files']))
    check('Separate Focus exact PNG unchanged',sha(ROOT/m['unchangedFocus']['file'])==sha(V1/'native/CH4-NEW-09-three-seashells-v01.png')=='70f35ae3853883b4fe15293ae5e6fd5ede1e721ab54946d2bc7499ce94ac04c6')
    check('Previous room exact PNG unchanged',sha(ROOT/m['unchangedPreviousRoom']['file'])=='522cc6a4c2e2d45f1aae7b3897a05380b86a2c70fccdba767576aa1520cabc04')
    for r in m['references']:
        blob=subprocess.check_output(['git','show',r['sourceCommit']+':'+r['sourcePath']],cwd=REPO)
        check('Exact canonical benchmark '+r['file'],hashlib.sha256(blob).hexdigest()==r['sha256']==sha(ROOT/r['file']))
    for p in(ROOT/'previews').glob('*-4x.png'):
        name=p.name[:-7]+'.png';sources=[q/name for q in[ROOT/'native',ROOT/'references',ROOT/'comparisons']if(q/name).exists()]
        check('Unique source '+p.name,len(sources)==1);s=Image.open(sources[0]);f=Image.open(p)
        check('Exact 4x '+p.name,f.size==(s.width*4,s.height*4) and ImageChops.difference(f,s.resize(f.size,Image.Resampling.NEAREST)).getbbox() is None)
    with tempfile.TemporaryDirectory(prefix='b214-v02-native-replay-')as folder:
        t=Path(folder);(t/'source').mkdir()
        for name in ['base_native.py','refine.py']:shutil.copyfile(ROOT/'source'/name,t/'source'/name)
        result=subprocess.check_output([sys.executable,str(t/'source/refine.py')],text=True)
        check('Reproducible with no source/reference PNGs available',not(t/'originals').exists() and not(t/'references').exists() and sha(t/a['native']['file'])==a['native']['sha256'])
        (ROOT/'evidence/source-isolated-replay.json').write_text(json.dumps({'passed':True,'onlyInputs':['source/base_native.py','source/refine.py'],'referenceImagesAvailable':False,'result':json.loads(result)},indent=2)+'\n')
    prov=json.loads((ROOT/'evidence/provenance.json').read_text())
    check('Original reference/prompt preserved',sha(ROOT/prov['referenceOriginal']['file'])==sha(V1/'originals/lavatory-detailed-reference.png')==prov['referenceOriginal']['sha256'] and sha(ROOT/prov['referencePrompt'])==prov['referencePromptSha256']==sha(V1/'source/lavatory-reference-prompt.txt'))
    check('Honest source-derived design / independent native raster',prov['sourceDerivedDesign'] and prov['nativeRasterConstructedIndependently'] and not prov['sourcePixelsTransferred'] and not prov['whollyIndependentCreativeDesign'])
    check('Exact inherited native recipe',sha(ROOT/'source/base_native.py')==sha(V1/'source/build.py'))
    check('Comparison captions stay within margins',all(x['fits'] for x in json.loads((ROOT/'evidence/caption-layout.json').read_text())))
    check('No registration/bindings/gameplay changes',not m['focusRevised'] and not m['registryModified'] and not m['narrativeGameplayOrEngineModified'] and m['newRuntimeModes']==0 and a['runtimeBinding'] is None and a['canonicalAssetPath'] is None)
    # All already committed files, including canonical artwork and every old
    # review package, must still match the exact parent commit tree.
    count=0;selected=0
    for entry in subprocess.check_output(['git','ls-tree','-r',m['preservationBaseline']],cwd=REPO,text=True).splitlines():
        meta,name=entry.split('\t',1);mode,kind,digest=meta.split()
        if kind!='blob':continue
        data=(REPO/name).read_bytes();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==digest,name
        count+=1;selected+=int(name.startswith('assets/selected/'))
    check('All prior tracked files/approved artwork byte-identical',True,baselineFiles=count,selectedArtFiles=selected)
    check('Existing production owner isolated branch',subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()==m['branch'])
    colours=Counter(im.get_flattened_data())
    (ROOT/'evidence/palette-diagnostics.json').write_text(json.dumps({'colourCount':len(colours),'noArbitraryGlobalCap':True,'colours':[{'rgb':list(k),'pixels':v}for k,v in colours.most_common()]},indent=2)+'\n')
    report={'passed':True,'status':'UNSELECTED','artisticApproval':False,'checks':checks}
    (ROOT/'evidence/validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'passed':True,'checks':len(checks),'colours':len(colours),'baselineFiles':count,'selectedArtFiles':selected}))
if __name__=='__main__':main()
