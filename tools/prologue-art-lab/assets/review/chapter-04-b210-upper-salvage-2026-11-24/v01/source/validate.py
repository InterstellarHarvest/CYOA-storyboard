from pathlib import Path
from PIL import Image,ImageColor
from html.parser import HTMLParser
import ast,subprocess,hashlib,json,sys
import native_scene,native_materials

ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists())
BASE='60c0569856eec3c5319dcac060875054ac2e955a'
checks=[]
def check(v,n):
    assert v,n
    checks.append({'check':n,'passed':True})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    m=json.loads((ROOT/'manifest.json').read_text());a=m['asset'];im=Image.open(ROOT/a['native']['file']);four=Image.open(ROOT/a['preview4x']['file'])
    check(m['primaryUnits']==1 and len(list((ROOT/'native').glob('*.png')))==1 and m['supplementalStates']==[],'Exactly one scene, no extra candidate or conditional state')
    check(m['status']=='UNSELECTED'and not m['selected']and not m['approvalOrIntegrationPerformed'],'Unselected, no registration or integration')
    check(m['visualQualityGatePassed']is False and m['selectionReady']is False,'Unmet visual gate explicitly disclosed, not concealed by technical QA')
    check('VISUAL GATE NOT FULLY MET'in(ROOT/'index.html').read_text(),'Gallery explicitly states illustration limitation and not selection-ready')
    check(im.size==(314,206)and im.mode=='RGB','Native314x206 opaque RGB contract')
    check(four.size==(1256,824)and four.mode=='RGB'and four.tobytes()==im.resize((1256,824),Image.Resampling.NEAREST).tobytes(),'Mathematically exact1256x824 NN preview')
    check(sha(ROOT/a['native']['file'])==a['native']['sha256'],'Native manifest hash')
    check(sha(ROOT/a['preview4x']['file'])==a['preview4x']['sha256'],'4x manifest hash')
    check(a['nodeIds']==['hotel_upper_salvage_arrival','hotel_upper_salvage_clerk_directions','hotel_freight_wc_misunderstanding'],'Exact three-node canonical coverage')
    check(a['proposedCanonicalKey']=='scenes:grand_bellevue/upper_salvage'and a['runtimeBinding']is None and a['newFocusId']is None,'Proposed key only; no runtime or Focus binding')
    assembly=json.loads((ROOT/'evidence/native-assembly.json').read_text());material=json.loads((ROOT/'evidence/material-interpretation.json').read_text())
    original=Image.new('RGBA',(314,206));final=Image.new('RGBA',(314,206))
    for src,painted in zip(assembly['layers'],material['finalLayerOrder']):
        x=Image.open(ROOT/src);y=Image.open(ROOT/painted)
        check(x.size==y.size==(314,206)and x.mode==y.mode=='RGBA','Native editable layer '+src)
        check(x.getchannel('A').tobytes()==y.getchannel('A').tobytes(),'Material pass preserves native silhouette '+src)
        check(set(y.getchannel('A').get_flattened_data())<={0,255},'No partly transparent layer pixels '+painted)
        original=Image.alpha_composite(original,x);final=Image.alpha_composite(final,y)
    check(original.convert('RGB').tobytes()==Image.open(ROOT/assembly['output']).tobytes(),'Blank-grid structural underpainting replay')
    check(final.convert('RGB').tobytes()==im.tobytes(),'Final semantic layer assembly exact')
    check(sha(ROOT/a['native']['file'])==material['finalSha256'],'Final layer recipe hash')
    check(all(v==255 for v in final.getchannel('A').get_flattened_data()),'Whole native master opaque before RGB export')
    check(a['sourceDerived']and not a['whollyIndependentAuthorshipClaim'],'Honest hybrid source-derived provenance')
    # This assertion concerns the structural builder only. The separate material
    # interpreter explicitly reads a source for its tonal guide, as documented.
    tree=ast.parse((ROOT/'source/native_scene.py').read_text())
    check(not any(isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr=='open'for n in ast.walk(tree)),'Independent native structural builder opens no raster')
    glyphs=assembly['wcLettering']['glyphs'];ink=ImageColor.getrgb(native_scene.P['ink'])
    check(''.join(g['character']for g in glyphs)=='W.C.','Exact native W.C. letters and two periods')
    for g in glyphs:check(all(im.getpixel(tuple(p))==ink for p in g['pixels']),'Native bitmap glyph preserved '+g['character'])
    x0,y0,x1,y1=assembly['wcLettering']['panelBounds'];check(original.convert('RGB').crop((x0,y0,x1+1,y1+1)).tobytes()==im.crop((x0,y0,x1+1,y1+1)).tobytes(),'Whole frontal three-button panel remains exact native painting')
    for p in material['protectedNativeSocketPixels']:check(original.convert('RGB').getpixel(tuple(p))==im.getpixel(tuple(p)),'Protected native drain/faucet socket '+str(p))
    allowed={ImageColor.getrgb(c)for c in native_scene.P.values()}
    allowed.update(ImageColor.getrgb(c)for keys,colors in native_materials.GROUPS.values()for c in colors)
    check(set(im.get_flattened_data())<=allowed,'All final colors belong to explicit native/material ramps; no photographic near-duplicate colors')
    for ref in json.loads((ROOT/'evidence/canonical-benchmarks.json').read_text()):
        raw=subprocess.check_output(['git','show',ref['sourceCommit']+':'+ref['sourcePath']],cwd=REPO)
        check((ROOT/ref['file']).read_bytes()==raw,'Exact approved benchmark '+ref['file'])
        check(sha(ROOT/ref['file'])==ref['sha256'],'Approved reference hash '+ref['file'])
        stem=Path(ref['file']).stem;one=Image.open(ROOT/ref['file']);p=Image.open(ROOT/f'previews/{stem}-4x.png')
        check(p.tobytes()==one.resize((1256,824),Image.Resampling.NEAREST).tobytes(),'Approved benchmark exact4x '+stem)
    for name in ['generation-receipt','material-generation-receipt']:
        r=json.loads((ROOT/f'evidence/{name}.json').read_text());check(sha(ROOT/r['preservedOriginal'])==r['originalSha256'],name+' original exact hash')
        check((ROOT/r['promptFile']).is_file()and all((ROOT/f).is_file()for f in r['orderedReferences']),name+' prompt and ordered inputs retained')
    pairs=0
    for p in ROOT.rglob('*-4x.png'):
        candidates=[p.with_name(p.name.replace('-4x.png','-native.png')),p.with_name(p.name.replace('-4x.png','.png'))]
        if p.parent.name=='previews':candidates += [ROOT/'native'/p.name.replace('-4x.png','.png'),ROOT/'references'/p.name.replace('-4x.png','.png')]
        src=next((q for q in candidates if q.is_file()),None)
        if src:
            one=Image.open(src);p4=Image.open(p);check(p4.size==(one.width*4,one.height*4)and p4.tobytes()==one.resize(p4.size,Image.Resampling.NEAREST).tobytes(),'Exact4x export '+str(p.relative_to(ROOT)));pairs+=1
    # Includes the immutable parent BRIEF and every selected PNG/story/registry.
    preserved=0
    for line in subprocess.check_output(['git','ls-tree','-r',BASE],cwd=REPO,text=True).splitlines():
        metadata,path=line.split('\t')
        if metadata.split()[1]!='blob':continue
        blob=(REPO/path).read_bytes();digest=hashlib.sha1(b'blob '+str(len(blob)).encode()+b'\0'+blob).hexdigest();check(digest==metadata.split()[2],'Baseline file preserved '+path);preserved+=1
    class Links(HTMLParser):
        def __init__(self):super().__init__();self.links=[]
        def handle_starttag(self,t,attrs):self.links +=[v for k,v in attrs if k in['href','src','data-one','data-four']and v and not v.startswith(('#','http'))]
    parser=Links();parser.feed((ROOT/'index.html').read_text())
    for f in set(parser.links):check((ROOT/f).is_file()or f=='evidence/validation.json','Gallery dependency '+f)
    # Repeat only after implementation changes; every final raster and recipe
    # must reproduce byte-identically, including preserved diagnostic studies.
    files=[p for p in ROOT.rglob('*.png')]+[ROOT/'index.html',ROOT/'manifest.json',ROOT/'evidence/native-assembly.json',ROOT/'evidence/material-interpretation.json',ROOT/'evidence/palette-and-clusters.json']
    before={p:sha(p)for p in files}
    for script in ['native_scene.py','native_materials.py','package_review.py']:subprocess.run([sys.executable,str(ROOT/'source'/script)],cwd=REPO,check=True,stdout=subprocess.DEVNULL)
    check(all(sha(p)==s for p,s in before.items()),'Complete native/material/export/gallery replay byte-identical')
    report={'technicalPassed':True,'checksPassed':len(checks),'primaryUnits':1,'supplementalStates':0,'allUnselected':True,'nativeSize':[314,206],'exact4xSize':[1256,824],'baselineFilesUnchanged':preserved,'exact4xPairs':pairs,'replayedFilesIdentical':len(before),'sourceDerived':True,'visualQualityGatePassed':False,'selectionReady':False,'visualLimitation':'Rear-rack fixture modelling more schematic than strongest approved Chapter2 art; see visual-review.md. Technical pass does not change that disposition.','narrativeGameplaySelectionsChanged':False,'checks':checks}
    (ROOT/'evidence/validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='checks'}))
if __name__=='__main__':main()
