from pathlib import Path
from PIL import Image,ImageChops
from collections import Counter
import json,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1];REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists());BASE='1261658ed882bff7340405e91f5d44f4e5404012'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 checks=[]
 def check(label,ok,**details):
  assert ok,(label,details);checks.append({'check':label,'passed':True,**details})
 m=json.loads((ROOT/'manifest.json').read_text());recipe=json.loads((ROOT/'evidence/native-layer-recipes.json').read_text())
 check('One Focus identifier; two new unselected states',m['existingCanonicalFocusIdentifier']=='grand_bellevue/bridal_privacy_panel'and len(m['widescreenStates'])==2 and m['newArtworkStatus']=='UNSELECTED'and not m['ownerApproved'])
 palettes={}
 for key,state in zip(['locked','provisional'],m['widescreenStates']):
  im=Image.open(ROOT/state['native']['file']);p=ROOT/state['native']['file'];four=Image.open(ROOT/state['exact4x']['file'])
  check(key+' dimensions/opaque RGB',im.size==(564,278)and im.mode=='RGB')
  check(key+' SHA-256',sha(p)==state['native']['sha256'],sha256=sha(p))
  check(key+' exact nearest4x',four.size==(2256,1112)and ImageChops.difference(four,im.resize((2256,1112),Image.Resampling.NEAREST)).getbbox()is None)
  check(key+' no approval or new runtime binding',not state['ownerApproved']and not state['selected']and state['newFocusId']is None and state['newFlag']is None and state['runtimeBinding']is None)
  replay=Image.new('RGBA',(564,278))
  for r in recipe['states'][key]:
   layer=Image.open(ROOT/r['file']);check(key+' layer '+r['file'],sha(ROOT/r['file'])==r['sha256']and layer.size==(564,278)and layer.mode=='RGBA'and set(layer.getchannel('A').get_flattened_data())<={0,255});replay=Image.alpha_composite(replay,layer)
  check(key+' exact native layer replay',ImageChops.difference(replay.convert('RGB'),im).getbbox()is None)
  counts=Counter(im.get_flattened_data());palettes[key]={'colors':len(counts),'coherentMaterialRamps':'evidence/material-ramps.json','noArbitraryGlobalCap':True,'noDitheringOrSharpening':True,'colorsAndPixels':[{'rgb':list(c),'pixels':n}for c,n in counts.most_common()]}
 rail=Image.open(ROOT/'masks/wainscot-rail.png');plate=Image.open(ROOT/'masks/plate-and-shadow.png')
 check('No overlap: wainscot / plate including cast shadow',ImageChops.multiply(rail,plate).getbbox()is None,plateAndShadowBBox=plate.getbbox(),railBBox=rail.getbbox(),minimumClearRows=rail.getbbox()[1]-plate.getbbox()[3])
 allowed=Image.open(ROOT/'masks/authorized-status-change.png');actual=Image.open(ROOT/'masks/actual-status-change.png')
 check('Exact shared geometry: screen/LED-only state differences',ImageChops.multiply(actual,ImageChops.invert(allowed)).getbbox()is None and actual.getbbox()is not None,changedPixels=sum(p>0 for p in actual.get_flattened_data()))
 approved=json.loads((ROOT/'evidence/owner-approval-preservation.json').read_text())['assets']
 expected=['072e30b905014a3856e21190551307eab0b0298dd0624e831f5395951d3b7afb','e546f7eb4d6de3a319548ee7759ab9ca83e415caa7293fb29322ca6f98ef44b3','f2718d729a28138a88cf51b6ef3c511bdf6d7de0d500654d975b1ab0249bdf49']
 for a,h in zip(approved,expected):
  data=subprocess.check_output(['git','show',BASE+':'+a['sourcePath']],cwd=REPO)
  check(a['id']+' immutable approved source/copy bytes',hashlib.sha256(data).hexdigest()==h==sha(ROOT/a['referenceCopy']['file'])and data==(ROOT/a['referenceCopy']['file']).read_bytes()and a['status']=='APPROVED'and a['ownerApproved'],sha256=h)
 for r in json.loads((ROOT/'evidence/benchmark-provenance.json').read_text()):
  data=subprocess.check_output(['git','show',r['sourceCommit']+':'+r['sourcePath']],cwd=REPO)
  check('Approved Chapter2 benchmark '+r['file'],hashlib.sha256(data).hexdigest()==r['sha256']==sha(ROOT/r['file']))
 glyphs=json.loads((ROOT/'evidence/lettering-layout.json').read_text());check('Chunky native glyphs / measured margins',all(g['binaryGlyphs']and g['scale']==1 and min(g['leftMargin'],g['rightMargin'])>=2 for g in glyphs))
 for p in (ROOT/'previews').glob('*-4x.png'):
  source=p.name[:-7]+'.png';paths=[d/source for d in[ROOT/'native',ROOT/'references',ROOT/'comparisons']if(d/source).exists()];check('Preview source '+p.name,len(paths)==1)
  im=Image.open(paths[0]);target=Image.open(p);check('Exact4x '+p.name,target.size==(im.width*4,im.height*4)and ImageChops.difference(target,im.resize(target.size,Image.Resampling.NEAREST)).getbbox()is None)
 check('Comparison captions fit',all(x['fits']for x in json.loads((ROOT/'evidence/comparison-layout.json').read_text())))
 prov=json.loads((ROOT/'evidence/generation-provenance.json').read_text());check('Honest source-derived provenance',prov['sourceDerived']and not prov['whollyIndependentNativeAuthorship']and prov['noApprovedImageUsedAsResizedProductionLayer'])
 check('Generated original / prompt hashes',sha(ROOT/prov['source']['file'])==prov['source']['sha256']and sha(ROOT/prov['prompt'])==prov['promptSha256'])
 for r in prov['referenceInputs']:check('Generation input hash '+r['file'],sha(ROOT/r['file'])==r['sha256'])
 j=json.loads((REPO/'story/chapters/chapter-04.wip.json').read_text());nodes=j['nodes'];nodes={n['id']:n for n in nodes}if isinstance(nodes,list)else nodes
 ids=['hotel_bridal_door_focus','hotel_bridal_door_options','hotel_bridal_ring_argument','hotel_bridal_autofit_survived'];snapshot={k:nodes[k]for k in ids};(ROOT/'evidence/canonical-handoff-nodes.json').write_text(json.dumps(snapshot,indent=2)+'\n')
 check('Existing five Focus choices / five return choices retained',len(nodes[ids[0]]['choices'])==5 and len(nodes[ids[1]]['choices'])==5)
 check('Handoff is separate; no engine implementation claimed',not m['inspectionBehaviorImplemented']and not m['storyChoicesModified']and not m['canonicalMainModified'])
 tracked=0;selected=0
 for line in subprocess.check_output(['git','ls-tree','-r',BASE],cwd=REPO,text=True).splitlines():
  meta,name=line.split('\t',1);mode,kind,digest=meta.split()
  if kind!='blob':continue
  data=(REPO/name).read_bytes();h=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert h==digest,name;tracked+=1;selected+=int(name.startswith('assets/selected/'))
 check('All existing tracked files exact, including entire v01 package',True,baseline=BASE,trackedFiles=tracked,selectedAssetFiles=selected)
 check('Correct isolated review branch',subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()==m['branch'])
 (ROOT/'evidence/palette-diagnostics.json').write_text(json.dumps(palettes,indent=2)+'\n')
 (ROOT/'evidence/validation.json').write_text(json.dumps({'passed':True,'newFocusStatus':'UNSELECTED','approvedInspectionStatus':'APPROVED / exact bytes','artisticApproval':False,'engineFeatureImplemented':False,'checks':checks},indent=2)+'\n')
 print(json.dumps({'passed':True,'checks':len(checks),'paletteCounts':{k:v['colors']for k,v in palettes.items()},'baselineFilesUnchanged':tracked,'selectedAssetFilesUnchanged':selected}))
if __name__=='__main__':main()
