from pathlib import Path
from PIL import Image, ImageChops
import json, hashlib, subprocess, tempfile, shutil, sys
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 checks=[]
 def check(label,ok,**detail):
  assert ok,(label,detail);checks.append({'check':label,'passed':True,**detail})
 m=json.loads((ROOT/'manifest.json').read_text());recipes=json.loads((ROOT/'evidence/native-layer-recipes.json').read_text());inventory=json.loads((ROOT/'evidence/authored-semantic-inventory.json').read_text())
 check('Four primary UNSELECTED candidates / no supplemental endings',m['primaryAssetCount']==4 and m['supplementalAssetCount']==0 and len(m['assets'])==4 and m['status']=='UNSELECTED' and not m['ownerApproved'])
 check('Four existing consolidated IDs',[a['id']for a in m['assets']]==['CH4-NEW-14','CH4-NEW-15','CH4-NEW-16','CH4-NEW-17'])
 nodes=json.loads((REPO/'story/chapters/chapter-04.wip.json').read_text())['nodes'];saved=json.loads((ROOT/'evidence/canonical-nodes.json').read_text())
 check('Exact canonical node and choice snapshots',all(nodes[k]==v for k,v in saved.items()))
 for a in m['assets']:
  id=a['id'];im=Image.open(ROOT/a['native']['file']);check(id+' native 314x206 RGB',im.mode=='RGB' and im.size==(314,206));check(id+' native SHA-256',sha(ROOT/a['native']['file'])==a['native']['sha256'])
  for key,scale in [('exact2x',2),('exact4x',4)]:
   f=Image.open(ROOT/a[key]['file']);check(id+' exact nearest '+str(scale)+'x',f.mode=='RGB' and f.size==(314*scale,206*scale) and sha(ROOT/a[key]['file'])==a[key]['sha256'] and ImageChops.difference(f,im.resize(f.size,Image.Resampling.NEAREST)).getbbox() is None)
  out=Image.new('RGBA',im.size)
  for r in recipes[id]:
   layer=Image.open(ROOT/r['file']);check('Binary native layer '+r['file'],layer.mode=='RGBA' and layer.size==im.size and set(layer.getchannel('A').get_flattened_data())<={0,255} and sha(ROOT/r['file'])==r['sha256']);out=Image.alpha_composite(out,layer)
  check(id+' exact layer composition',ImageChops.difference(out.convert('RGB'),im).getbbox() is None)
  for entity in inventory[id]:
   mask=Image.open(ROOT/entity['mask']);check('Authored semantic mask '+entity['entity'],mask.mode=='L' and mask.size==im.size and mask.getbbox() is not None and set(mask.get_flattened_data())<={0,255})
  node=nodes[a['node']]
  check(id+' approved ending/popup mapping',node['end'] and node['endingArt']==a['endingArt']==node['deathPopup']['artRef'] and node['deathPopup']['id']==a['deathPopupId'] and node['deathPopup']['status']=='owner-approved')
  check(id+' artwork not selected or bound',a['status']=='UNSELECTED' and not a['selected'] and not a['ownerApproved'] and a['canonicalAssetPath'] is None and a['runtimeBinding'] is None)
 # These are construction checks, not automated visual recognition of objects.
 # The readable semantics also receive the recorded human visual assessment.
 get=lambda id,name:next(e for e in inventory[id] if name in e['entity'])
 check('Exactly one authored wire hanger',sum('wire clothes hanger'in e['entity'] for e in inventory['CH4-NEW-15'])==1)
 check('Exactly one authored shoe in each case/gown image',all(sum('shoe'in e['entity']for e in inventory[id])==1 for id in ['CH4-NEW-16','CH4-NEW-17']))
 check('No authored shoe in final-occupancy or suit',all(not any('shoe'in e['entity']for e in inventory[id]) for id in ['CH4-NEW-14','CH4-NEW-15']))
 suit=Image.open(ROOT/m['assets'][1]['native']['file']);wire=Image.open(ROOT/'layers/CH4-NEW-15-single-wire-hanger.png');wall=Image.open(ROOT/'layers/CH4-NEW-15-quiet-wall.png')
 visible=[x for x in range(314) if wire.getpixel((x,69))[3] and suit.getpixel((x,69))==wire.getpixel((x,69))[:3]]
 check('Same hanger crossbar visibly survives jacket/trouser compositing',len(visible)>=3,visibleCrossbarPixels=len(visible))
 check('Jacket neckline is actually hollow',suit.getpixel((155,63))==wall.getpixel((155,63))[:3])
 stall=get('CH4-NEW-14','raised empty stall')['bbox'];porcelain=get('CH4-NEW-14','broken floor-level')['bbox'];check('Broken toilet lies well below lifted stall',porcelain[1]>stall[3] and porcelain[3]>=190,verticalGap=porcelain[1]-stall[3],floorDebrisBottom=porcelain[3])
 for r in m['references']:
  blob=subprocess.check_output(['git','show',r['sourceCommit']+':'+r['sourcePath']],cwd=REPO);check('Exact pinned reference '+r['file'],sha(ROOT/r['file'])==r['sha256']==hashlib.sha256(blob).hexdigest())
 for p in(ROOT/'previews').glob('*-4x.png'):
  name=p.name[:-7]+'.png';sources=[d/name for d in[ROOT/'native',ROOT/'references',ROOT/'comparisons']if(d/name).exists()];check('Unique native source '+p.name,len(sources)==1)
  im=Image.open(sources[0]);f=Image.open(p);check('Exact 4x '+p.name,f.size==(im.width*4,im.height*4) and ImageChops.difference(f,im.resize(f.size,Image.Resampling.NEAREST)).getbbox() is None)
 check('All comparison captions fit',all(r['fits']for r in json.loads((ROOT/'evidence/caption-layout.json').read_text())))
 prov=json.loads((ROOT/'evidence/generation-provenance.json').read_text())
 for s in prov['sources']:
  check('Original/prompt preserved '+s['id'],sha(ROOT/s['file'])==s['sha256'] and sha(ROOT/s['prompt'])==s['promptSha256'])
  for r in s['inputs']:check('Generation reference input '+r['path'],sha(ROOT/r['path'])==r['sha256'])
 check('Honest native/source provenance',m['sourceDerivedDesign'] and m['nativeRasterConstructedIndependently'] and not m['referencePixelsTransferred'] and not m['whollyIndependentCreativeDesign'])
 with tempfile.TemporaryDirectory(prefix='b216-native-replay-')as folder:
  t=Path(folder);(t/'source').mkdir();shutil.copyfile(ROOT/'source/build.py',t/'source/build.py');log=subprocess.check_output([sys.executable,str(t/'source/build.py')],text=True)
  check('All four reproduce with NO reference or original images available',not(t/'originals').exists() and not(t/'references').exists() and all(sha(t/a['native']['file'])==a['native']['sha256']for a in m['assets']))
  (ROOT/'evidence/source-isolated-replay.json').write_text(json.dumps({'passed':True,'onlyInput':'source/build.py','referenceImagesAvailable':False,'sourcePixelsTransferred':False,'result':json.loads(log)},indent=2)+'\n')
 count=0;selected=0
 for entry in subprocess.check_output(['git','ls-tree','-r',m.get('preservationBaseline',m['canonicalBaseline'])],cwd=REPO,text=True).splitlines():
  meta,name=entry.split('\t',1);mode,kind,digest=meta.split()
  if kind!='blob':continue
  data=(REPO/name).read_bytes();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==digest,name;count+=1;selected+=int(name.startswith('assets/selected/'))
 check('Every baseline tracked file / selected art unchanged',True,baselineFiles=count,selectedArtFiles=selected)
 check('Dedicated B2-16 review branch',subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()==m['branch'])
 check('No registry, popup, narrative, gameplay or integration changes',not m['registryModified'] and not m['narrativeGameplayOrEngineModified'] and not m['popupCopyModified'] and not m['popupsBakedIntoArtwork'] and m['newCanonicalNodesOrEndings']==0 and not m['nextBatchStarted'])
 report={'passed':True,'status':'UNSELECTED','artisticApproval':False,'checks':checks,'semanticChecksAreAuthoredConstructionChecksNotVisualRecognition':True}
 (ROOT/'evidence/validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':True,'checks':len(checks),'baselineFiles':count,'selectedArtFiles':selected}))
if __name__=='__main__':main()
