"""Verify actual native PNGs, exact scaling, authored mappings and preservation."""
from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1];REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=json.loads((ROOT/'manifest.json').read_text());inv=json.loads((ROOT/'evidence/inventory-source.json').read_text());plan=json.loads((ROOT/'evidence/state-plan.json').read_text());nodes=json.loads((ROOT/'evidence/canonical-nodes.json').read_text());checks=[]
 def check(v,label):
  assert v,label;checks.append({'check':label,'passed':True})
 primary=[a for a in m['assets']if a['unitType']=='primary'];states=[a for a in m['assets']if a['unitType']=='supplemental-state']
 check(len(primary)==7 and len(states)==3 and m['status']=='UNSELECTED','Seven primary demands plus three UNSELECTED state frames')
 check({a['inventoryId']for a in primary}=={a['inventoryId']for a in inv['assets']if a['category']!='state_family'},'Exact canonical primary inventory demands')
 check(sorted({n for a in m['assets']for n in a['nodeIds']})==sorted(m['storyNodeCoverage'])==sorted(inv['group']['nodeIds']),'Exact21-node source coverage')
 check(len(list((ROOT/'native').glob('*.png')))==10,'Exactly ten native PNG candidates')
 for a in m['assets']:
  check(a['status']=='UNSELECTED'and a['selected']is False,'No owner selection inferred '+a['id'])
  im=Image.open(ROOT/a['native']['file']);four=Image.open(ROOT/a['preview4x']['file']);size=[314,206]if a['kind']=='scene'else[564,278]
  check(list(im.size)==a['native']['dimensions']==size and im.mode==a['native']['mode'],'Native dimensions/mode '+a['id'])
  check(sha(ROOT/a['native']['file'])==a['native']['sha256']and sha(ROOT/a['preview4x']['file'])==a['preview4x']['sha256'],'Manifest native/preview hashes '+a['id'])
  alpha=im.convert('RGBA').getchannel('A');check(alpha.getextrema()==(0,255)and im.mode=='RGBA'if a['kind']=='portrait'else alpha.getextrema()==(255,255),'Alpha contract '+a['id'])
  if a['kind']=='portrait':check(alpha.getbbox()[1]>4 and alpha.crop((0,0,564,1)).getextrema()==(0,0),'Complete cap with top transparency margin '+a['id'])
  check(four.size==(im.width*4,im.height*4)and four.tobytes()==im.resize(four.size,Image.Resampling.NEAREST).tobytes(),'Exact4x nearest pixels '+a['id'])
  check(a['sourceDerived']and not a['independentlyAuthoredAtNativeResolution']and a['layers']and a['masks'],'Honest editable source-derived provenance '+a['id'])
  check(sha(ROOT/a['detailedReference']['file'])==a['detailedReference']['sha256'],'Detailed source pinned '+a['id'])
  check((ROOT/f'comparisons/{a["id"]}-chapter2-native.png').is_file()and(ROOT/f'comparisons/{a["id"]}-chapter2-4x.png').is_file(),'Direct native/exact4x Chapter2 comparison '+a['id'])
  for n in a['nodeIds']:check(n in nodes,'Authored node exists '+a['id']+':'+n)
  if a['unitType']=='primary':
   group,key=a['key'].split(':',1)
   for n in a['nodeIds']:
    node=nodes[n];check(node.get('speaker','')+':'+node.get('pose','')==key if group=='portraits'else node.get('focus')==key if group=='focus'else node.get('scene')==key.split('#')[0],'Exact authored association '+a['id']+':'+n)
  else:check(a['key']is None and a['runtimeBindingInstalled']is False,'State frame has no invented canonical/runtime binding '+a['id'])
 for name,b in m['canonicalBenchmarks'].items():check(sha(ROOT/f'references/{name}.png')==b['sha256'],'Exact canonical approved reference '+name)
 bg=Image.open(ROOT/'native/CH4-B2-23-v01.png').convert('RGBA')
 for n in[20,21,22]:
  fg=Image.open(ROOT/f'native/CH4-B2-{n}-v01.png');composite=Image.open(ROOT/f'previews/CH4-B2-{n}-composite.png');check(composite.tobytes()==Image.alpha_composite(bg,fg).tobytes(),'Independent scene/foreground composite '+str(n))
  context='restroom'if n==20 else'lobby';approved=Image.open(ROOT/f'references/approved-{context}-conversation.png').convert('RGBA');c=Image.open(ROOT/f'previews/CH4-B2-{n}-{context}-composite.png');check(c.tobytes()==Image.alpha_composite(approved,fg).tobytes(),'Exact approved alternate dialogue context '+str(n))
 recon=json.loads((ROOT/'evidence/native-reconstruction.json').read_text());protect=Image.open(ROOT/'masks/CH4-B2-19-complete-story-objects.png')
 for layer in ['floor-structure','architecture']:
  alpha=Image.open(ROOT/f'layers/CH4-B2-19-{layer}.png').getchannel('A');check(ImageChops.multiply(alpha,protect).getbbox()is None,'Architecture/floor pass preserves complete object silhouettes '+layer)
 check(recon['primary']['CH4-B2-19']['nativeStructuralPixelsChanged']>0,'Native scene structure beyond material fitting')
 for a in states:
  report=recon['states'][a['id']];base=Image.open(ROOT/f'native/{a["baseAssetId"]}-v01.png');im=Image.open(ROOT/a['native']['file']);allowed=Image.open(ROOT/report['allowedMask']);points=[i for i,(x,y)in enumerate(zip(base.getdata(),im.getdata()))if x!=y]
  check(points and len(points)==report['changedPixels']and not any(allowed.getpixel((i%564,i//564))==0 for i in points)and report['outsideAllowedChanges']==0,'Actual state change is bounded; outside pixels exact '+a['id'])
 source=nodes['hotel_collection_ring_focus']['text'];check(any(t.get('if')=={'flag':'ch4_ring_slipped_inside_chair'}for t in source if isinstance(t,dict))and any(t.get('if')==plan['baseCollectionCondition']for t in source if isinstance(t,dict)),'Exact authored caught/slipped conditions')
 check(all('wedding_ring_lot31'in nodes[n]['effects']['give']for n in ['hotel_collection_ring_porter_recovery','hotel_collection_ring_stapler_recovery']),'Recovered state follows explicit inventory grant')
 check(all(s['canonicalKey']is None for s in plan['states']),'No Focus states falsely installed as pages or new runtime keys')
 freeze=json.loads((ROOT/'evidence/frozen-history.json').read_text());base=freeze['baseReviewCommit'];mutable={'README.md','AGENTS.md'}
 for rel,digest in freeze['files'].items():
  if rel in mutable:
   original=subprocess.check_output(['git','show',base+':'+str((ROOT.parent/rel).relative_to(REPO))],cwd=REPO);check((ROOT.parent/rel).read_bytes().endswith(original),'Previous index/guidance text preserved '+rel)
  else:check(sha(ROOT.parent/rel)==digest,'Historical bytes preserved '+rel)
 for path in subprocess.check_output(['git','ls-tree','-r','--name-only',base,'story','assets/selected','.github'],cwd=REPO,text=True).splitlines():
  check((REPO/path).read_bytes()==subprocess.check_output(['git','show',base+':'+path],cwd=REPO),'Canonical narrative/gameplay/selected registry unchanged '+path)
 report={'passed':True,'checksPassed':len(checks),'primaryAssets':7,'supplementalStateFrames':3,'nativePNGCount':10,'status':'UNSELECTED','historicalFilesPreserved':len(freeze['files']),'canonicalFilesChanged':0,'integrationPerformed':False,'visualAssessment':'evidence/visual-review.md','checks':checks}
 (ROOT/'evidence/validation.json').write_text(json.dumps(report,indent=2)+'\n');print(f'{len(checks)} technical/preservation checks passed; ten UNSELECTED frames; no canonical changes.')
if __name__=='__main__':main()
