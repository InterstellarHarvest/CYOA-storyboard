"""B2-11 native/state/provenance/preservation and reproducible assembly QA."""
from pathlib import Path
from PIL import Image,ImageChops
from html.parser import HTMLParser
import json,hashlib,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists())
BASE='e4f46f2300bad7e946dea0ffd917d9c3b339b7b8';MAIN='5a4290d672e1904b4b5ad361562f05168c328a50';checks=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(v,n):
 assert v,n
 checks.append({'check':n,'passed':True})
def diff(a,b):
 d=ImageChops.difference(a,b);return ImageChops.lighter(ImageChops.lighter(d.getchannel('R'),d.getchannel('G')),d.getchannel('B'))
def assemble(names):
 im=Image.new('RGBA',(314,206))
 for n in names:im=Image.alpha_composite(im,Image.open(ROOT/'layers'/(n+'.png')).convert('RGBA'))
 return im.convert('RGB')
def main():
 m=json.loads((ROOT/'manifest.json').read_text());r=json.loads((ROOT/'evidence/native-construction.json').read_text());a=m['asset'];state=m['supplementalReferences'][0]
 check(m['status']=='UNSELECTED'and not m['ownerApproved']and m['primaryUnits']==1 and len(m['supplementalReferences'])==1,'One unselected primary and one conditional reference')
 check(len(list((ROOT/'native').glob('*.png')))==2,'Exactly two final native PNGs')
 colors={};images=[]
 for title,asset in [('dry',a),('flood',state)]:
  im=Image.open(ROOT/asset['native']['file']);four=Image.open(ROOT/asset['preview4x']['file']);images.append(im)
  check(im.size==(314,206)and im.mode=='RGB',title+' opaque native314x206 RGB')
  check(four.size==(1256,824)and four.tobytes()==im.resize(four.size,Image.Resampling.NEAREST).tobytes(),title+' exact nearest-neighbor4x')
  for k in ['native','preview4x']:check(sha(ROOT/asset[k]['file'])==asset[k]['sha256'],title+' '+k+' SHA256')
  colors[title]=len(im.getcolors(200000));check(asset['runtimeBinding']is None and asset['newFocusId']is None,title+' no runtime/Focus binding')
 check(state['newSceneKey']is None and state['newFlag']is None,'Conditional reference introduces no scene key or flag')
 dry,flood=images;delta=diff(dry,flood);allow=Image.open(ROOT/'masks/flood-authorized.png')
 check(ImageChops.subtract(delta,allow).getbbox()is None,'Zero state changes outside floor/hatch/attendant/sign masks')
 check(assemble(r['dryLayerOrder']).tobytes()==dry.tobytes(),'Exact dry structural assembly')
 check(assemble(r['floodLayerOrder']).tobytes()==flood.tobytes(),'Exact shared-base plus local state assembly')
 check(r['floodLayerOrder'][:len(r['dryLayerOrder'])]==r['dryLayerOrder'],'All ten architecture/route/material layers shared identically')
 for p in (ROOT/'layers').glob('*.png'):
  im=Image.open(p);check(im.size==(314,206)and im.mode=='RGBA'and set(im.getchannel('A').get_flattened_data())<={0,255},'Native binary-alpha editable layer '+p.name)
 check(sha(ROOT/a['native']['file'])==r['dryHash']and sha(ROOT/state['native']['file'])==r['floodHash'],'Construction hashes exact')
 check(sha(ROOT/r['source'])==r['sourceSha256'],'Pixel-friendly reference source exact')
 for x in m['sources']:check(sha(ROOT/x['file'])==x['sha256'],'Preserved source hash '+x['file'])
 for p in m['prompts']:check((ROOT/p).is_file(),'Original source prompt '+p)
 guide=Image.open(ROOT/'diagnostics/source-transfer-NOT-FINAL.png')
 check(guide.tobytes()!=dry.tobytes(),'Final differs from explicit source-transfer diagnostic')
 sourceDelta=sum(p!=q for p,q in zip(guide.get_flattened_data(),dry.get_flattened_data()))
 check(m['sourceDerived']and not m['whollyIndependentNativeAuthorship']and not r['whollyIndependentAuthorshipClaim'],'Source-derived provenance; no independent authorship claim')
 for ref in json.loads((ROOT/'evidence/benchmark-provenance.json').read_text()):
  data=subprocess.check_output(['git','show',ref['sourceCommit']+':'+ref['sourcePath']],cwd=REPO)
  check((ROOT/ref['file']).read_bytes()==data and sha(ROOT/ref['file'])==ref['sha256'],'Actual approved canonical benchmark '+ref['file'])
 for x in json.loads((ROOT/'evidence/caption-layout.json').read_text()):check(x['fits']and x['textWidth']<x['panelWidth']-8,'Caption fits '+x['sheet']+'/'+x['caption'])
 pairs=0
 for p in ROOT.rglob('*-4x.png'):
  candidates=[p.with_name(p.name.replace('-4x','-native')),ROOT/'native'/p.name.replace('-4x',''),ROOT/'references'/p.name.replace('-4x','')]
  one=next((q for q in candidates if q.is_file()),None)
  if one:
   x=Image.open(one);y=Image.open(p);check(y.size==(x.width*4,x.height*4)and y.tobytes()==x.resize(y.size,Image.Resampling.NEAREST).tobytes(),'Exact4x '+str(p.relative_to(ROOT)));pairs+=1
 preserved=0;approved=0
 for line in subprocess.check_output(['git','ls-tree','-r',BASE],cwd=REPO,text=True).splitlines():
  meta,path=line.split('\t')
  if meta.split()[1]!='blob':continue
  data=(REPO/path).read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert blob==meta.split()[2],path;preserved+=1
  if path.startswith('assets/selected/'):approved+=1
 check(True,'All '+str(preserved)+' post-main-merge blobs byte-exact, including '+str(approved)+' approved files')
 check(subprocess.run(['git','merge-base','--is-ancestor',MAIN,BASE],cwd=REPO).returncode==0,'Canonical main incorporated into review baseline')
 nodebytes=subprocess.check_output(['git','show',MAIN+':story/chapters/chapter-04.wip.json'],cwd=REPO);nodes=json.loads(nodebytes)['nodes'];pinned=json.loads((ROOT/'evidence/canonical-nodes.json').read_text())
 check(all(pinned[k]==nodes[k]for k in a['nodeIds']),'Exact canonical dry/flood nodes')
 check(nodes[a['nodeIds'][0]]['scene']==nodes[a['nodeIds'][1]]['scene']=='grand_bellevue/public_corridor','One existing canonical corridor scene')
 check(len(nodes[a['nodeIds'][0]]['choices'])==len(nodes[a['nodeIds'][1]]['choices'])==3,'Existing three-route choices preserved in both states')
 class Links(HTMLParser):
  def __init__(self):super().__init__();self.links=[]
  def handle_starttag(self,t,attrs):self.links +=[v for k,v in attrs if k in ['href','src','data-one','data-four']and v and not v.startswith(('#','http'))]
 parser=Links();parser.feed((ROOT/'index.html').read_text())
 for link in set(parser.links):check((ROOT/link).is_file()or link=='evidence/validation.json','Gallery dependency '+link)
 files=list(ROOT.rglob('*.png'))+[ROOT/'manifest.json',ROOT/'index.html',ROOT/'evidence/native-construction.json'];before={p:sha(p)for p in files}
 for name in ['native_scene.py','package_review.py']:subprocess.run([sys.executable,str(ROOT/'source'/name)],cwd=REPO,check=True,stdout=subprocess.DEVNULL)
 check(all(sha(p)==digest for p,digest in before.items()),'Deterministic native layers/state/gallery replay')
 out={'technicalPassed':True,'checksPassed':len(checks),'status':'UNSELECTED','ownerApproved':False,'primaryUnits':1,'supplementalReferences':1,'exact4xPairs':pairs,'stateChangesOutsideAuthorizedMasks':0,'sharedStructuralLayers':len(r['dryLayerOrder']),'floodChangedNativePixels':m['floodChangedNativePixels'],'floodUnchangedPercent':m['floodUnchangedPercent'],'paletteCountsDiagnosticOnly':colors,'sourceTransferDifferentNativePixels':sourceDelta,'replayedFilesIdentical':len(before),'postMainMergeBaseline':BASE,'canonicalMain':MAIN,'preservedBaselineBlobs':preserved,'approvedFilesByteExact':approved,'canonicalNarrativeGameplaySelectionsModified':False,'sourceDerived':True,'visualAssessment':'evidence/visual-review.md','checks':checks}
 (ROOT/'evidence/validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='checks'}))
if __name__=='__main__':main()
