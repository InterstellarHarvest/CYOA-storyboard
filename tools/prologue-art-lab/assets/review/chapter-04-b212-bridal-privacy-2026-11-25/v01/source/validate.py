"""Verify exact deliverables, compositing, conditions and baseline preservation."""
from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists())
BASE='9f49416c9dd2e8b02e84b04a6c4ed1f4bc5e65b5'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=json.loads((ROOT/'manifest.json').read_text());checks=[]
 def check(label,ok,**details):
  assert ok,(label,details);checks.append({'check':label,'passed':True,**details})
 check('Two unselected primary candidates and one unselected conditional reference',len(m['primaryAssets'])==2 and len(m['supplementalReferences'])==1 and m['status']=='UNSELECTED' and not m['ownerApproved'])
 recipes=json.loads((ROOT/'evidence/native-layer-recipes.json').read_text())
 for a,key,size in [(m['primaryAssets'][0],'room',(314,206)),(m['primaryAssets'][1],'panel-locked',(565,451)),(m['supplementalReferences'][0],'panel-provisional',(565,451))]:
  p=ROOT/a['native']['file'];im=Image.open(p);four=Image.open(ROOT/a['preview4x']['file']);expected=im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST)
  check(a['id']+' dimensions / opaque RGB',im.size==size and im.mode=='RGB',dimensions=list(im.size))
  check(a['id']+' manifest hash',sha(p)==a['native']['sha256'],sha256=sha(p))
  check(a['id']+' exact4x',four.size==expected.size and four.mode=='RGB' and ImageChops.difference(four,expected).getbbox()is None)
  out=Image.new('RGBA',size)
  for rec in recipes[key]:
   layer=Image.open(ROOT/rec['file']);check(rec['file']+' layer hash',sha(ROOT/rec['file'])==rec['sha256'])
   check(rec['file']+' native layer grid / binary alpha',layer.size==size and layer.mode=='RGBA' and set(layer.getchannel('A').get_flattened_data())<={0,255})
   out=Image.alpha_composite(out,layer)
  check(a['id']+' exact native layer replay',ImageChops.difference(out.convert('RGB'),im).getbbox()is None)
  check(a['id']+' no selection/binding',not a['ownerApproved'] and not a['selected'] and a['runtimeBinding']is None and a['canonicalAssetPath']is None)
 allowed=Image.open(ROOT/'masks/panel-authorized-status-change.png');actual=Image.open(ROOT/'masks/panel-actual-status-change.png')
 outside=ImageChops.multiply(actual,ImageChops.invert(allowed))
 check('Conditional reference changes only screen / LED; shared geometry exact',outside.getbbox()is None and actual.getbbox()is not None,changedPixels=sum(p>0 for p in actual.get_flattened_data()))
 variant=m['supplementalReferences'][0];check('No supplemental Focus ID, new flag or runtime binding',variant['newFocusId']is None and variant['newFlag']is None and variant['runtimeBinding']is None and variant['proposedCanonicalKey']is None)
 glyphs=json.loads((ROOT/'evidence/lettering-layout.json').read_text())
 check('Chunky binary pixel lettering / deliberate horizontal margins',all(x['binaryGlyphs']and x['scale']==2 and min(x['leftMargin'],x['rightMargin'])>=4 for x in glyphs),minimumSideMargin=min(min(x['leftMargin'],x['rightMargin'])for x in glyphs))
 check('Comparison labels fit',all(r['fits']for r in json.loads((ROOT/'evidence/caption-layout.json').read_text())))
 for p in (ROOT/'previews').glob('*-4x.png'):
  stem=p.name[:-7]+'.png';options=list((ROOT/'native').glob(stem))+list((ROOT/'references').glob(stem))+list((ROOT/'diagnostics').glob(stem))+list((ROOT/'comparisons').glob(stem))
  check('Preview has native source '+p.name,len(options)==1)
  im=Image.open(options[0]);four=Image.open(p);check('ExactNN preview '+p.name,ImageChops.difference(four,im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST)).getbbox()is None)
 benchmarks=json.loads((ROOT/'evidence/benchmark-provenance.json').read_text())
 for r in benchmarks:
  data=subprocess.check_output(['git','show',r['sourceCommit']+':'+r['sourcePath']],cwd=REPO)
  check('Canonical benchmark '+r['file'],hashlib.sha256(data).hexdigest()==r['sha256']==sha(ROOT/r['file']))
 sources=json.loads((ROOT/'evidence/generation-provenance.json').read_text())
 for r in sources['sources']:
  check('Original source '+r['file'],sha(ROOT/r['file'])==r['sha256']and sha(ROOT/r['prompt'])==r['promptSha256'])
  for f,h in r['inputHashes'].items():check('Retained reference input '+f,sha(ROOT/f)==h)
 check('Honest source-derived provenance',m['sourceDerived']and not m['whollyIndependentNativeAuthorship']and sources['sourceDerived']and not sources['whollyIndependentNativeAuthorship'])
 chapter=json.loads((REPO/'story/chapters/chapter-04.wip.json').read_text());nodes=chapter['nodes'];nodes={n['id']:n for n in nodes}if isinstance(nodes,list)else nodes
 saved=json.loads((ROOT/'evidence/canonical-nodes.json').read_text())
 check('Canonical node excerpts exactly match unchanged narrative',all(nodes[n]==v for n,v in saved.items()))
 for a in m['primaryAssets']+m['supplementalReferences']:check(a['id']+' existing node associations',all(n in nodes for n in a['canonicalNodes']))
 check('Provisional outcome uses existing flag', 'ch4_provisional_bride_registered'in json.dumps(nodes['hotel_bridal_autofit_survived']))
 check('Documented review/runtime size mismatch; no compatibility assertion',json.loads((ROOT/'evidence/dimension-contract.json').read_text())['futureIntegrationNeedsDimensionResolution']is True)
 # Every pre-existing tracked blob is immutable; only this new review package may exist.
 tree=subprocess.check_output(['git','ls-tree','-r',BASE],cwd=REPO,text=True).splitlines();count=0;selected=0
 for line in tree:
  meta,name=line.split('\t',1);mode,kind,digest=meta.split()
  if kind!='blob':continue
  path=REPO/name;data=path.read_bytes();actualhash=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  assert digest==actualhash,('Baseline changed',name);count+=1;selected+=int(name.startswith('assets/selected/'))
 check('Every baseline tracked file unchanged',True,baselineCommit=BASE,filesVerified=count,selectedFilesVerified=selected)
 check('Branch remains isolated review',subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()==m['branch'])
 report={'passed':True,'status':'UNSELECTED','ownerApproved':False,'artisticApproval':False,'dimensionsFollowExplicitReviewBrief':True,'currentFocusRuntimeCompatible':False,'checks':checks}
 (ROOT/'evidence/validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':True,'checks':len(checks),'baselineFiles':count,'selectedFiles':selected,'currentFocusRuntimeCompatible':False}))
if __name__=='__main__':main()
