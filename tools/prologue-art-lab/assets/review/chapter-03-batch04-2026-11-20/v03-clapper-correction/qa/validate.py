from pathlib import Path
from PIL import Image
import json,hashlib,subprocess
P=Path(__file__).resolve().parents[1];R=P.parents[5];baseline='57ecd94f1f7eb840d186d7b5afae79a60063511d'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((P/'manifest.json').read_text());prior=json.loads((P.parent/'v02-close-camera-corrections/manifest.json').read_text())
contract=json.loads((P/'mask-contract.json').read_text());proof=json.loads((P/'pixel-change-verification.json').read_text())
old=Image.open(P/contract['source']).convert('RGB');new=Image.open(P/'candidates/CH3-D05-backstage-v03.png')
assert new.size==(314,206) and new.mode=='RGB';assert sha(P/'inputs/edit-mask.png')==contract['maskSha256']
allowed=Image.open(P/'inputs/edit-mask.png');effective=Image.open(P/'inputs/effective-edit-mask.png');changed=[]
for y in range(206):
 for x in range(314):
  assert effective.getpixel((x,y)) in (0,255) and allowed.getpixel((x,y)) in (0,255)
  if effective.getpixel((x,y)):assert allowed.getpixel((x,y))
  if old.getpixel((x,y))!=new.getpixel((x,y)):
   assert allowed.getpixel((x,y)) and effective.getpixel((x,y));changed.append([x,y])
assert changed==json.loads((P/'proofs/changed-coordinates.json').read_text())
assert len(changed)==proof['changedPixels']==1287 and proof['outsideAllowedMaskChanged']==proof['outsideEffectiveMaskChanged']==0
assert new.crop((0,122,314,206)).tobytes()==old.crop((0,122,314,206)).tobytes()
regions={'exit':(135,47,210,135),'cables':(0,0,122,105),'sandwich_and_carton':(0,124,83,206),'power_cable_and_outlet':(289,126,314,169),'floor':(0,164,314,206),'original_cabinet_and_casters':(239,122,290,165)}
for label,box in regions.items():assert new.crop(box).tobytes()==old.crop(box).tobytes(),label
assert len(m['candidates'])==9 and not m['selected'] and not m['approved'] and m['assetPath'] is None
retained=[]
for c in m['candidates']:
 assert c['status']=='generated' and not c['selected'] and not c['approved'] and c['assetPath'] is None
 f=P/c['file'];im=Image.open(f);assert sha(f)==c['sha256'] and list(im.size)==c['dimensions']
 original=next(p for p in prior['candidates'] if p['record']==c['record'])
 if c['retainedFromPreviousReview']:
  assert c['sha256']==original['sha256'];retained.append(c['candidateId'])
 else:
  assert c['candidateId']=='CH3-D05-backstage';assert c['sha256']==proof['correctedSha256'];assert c['replacesUnselectedSha256']==original['sha256']
 zoom=Image.open(P/c['preview4x']);assert zoom.tobytes()==im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).tobytes()
 alpha=im.convert('RGBA').getchannel('A').histogram();assert sum(alpha[1:255])==0
assert len(retained)==8
for version in ['v01','v02-close-camera-corrections']:
 V=P.parent/version
 for line in subprocess.check_output(['git','ls-tree','-r',baseline,str(V.relative_to(R))],cwd=R,text=True).splitlines():
  meta,f=line.split('\t');b=(R/f).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==meta.split()[2]
for scope in ['story','assets/selected','docs/artwork-history']:
 for line in subprocess.check_output(['git','ls-tree','-r',baseline,scope],cwd=R,text=True).splitlines():
  meta,f=line.split('\t');b=(R/f).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==meta.split()[2]
receipt=json.loads((P/'generation-receipts.json').read_text())
for r in receipt:assert sha(P/r['file'])==r['sha256'] and sha(P/r['prompt'])==r['promptSha256']
report={'result':'PASS','correctedSha256':proof['correctedSha256'],'changedPixels':len(changed),'changedPercent':round(100*len(changed)/(314*206),3),'outsideAllowedMaskChanged':0,'outsideEffectiveMaskChanged':0,'protectedRegions':list(regions),'eightRetainedCandidatesByteIdentical':retained,'entireV01AndV02PackagesByteIdentical':True,'canonicalRegistryAndPreviewRegistryByteIdentical':True,'allApprovedArtworkByteIdentical':True,'narrativeAndArchivesByteIdentical':True,'nativeDimensions':[314,206],'mode':'RGB','partialAlpha':0,'exact4x':True,'allNineRemainGeneratedUnselected':True,'nativeGridAuthorship':'unresolved / unproven; larger generator originals and masked derived export documented'}
(P/'qa/results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
