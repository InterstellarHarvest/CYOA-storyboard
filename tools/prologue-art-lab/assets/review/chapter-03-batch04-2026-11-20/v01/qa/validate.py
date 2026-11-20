from pathlib import Path
import hashlib,json,subprocess
from PIL import Image,ImageChops
P=Path(__file__).resolve().parents[1];R=P.parents[5]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((P/'manifest.json').read_text());a=json.loads((R/'story/artwork.draft.json').read_text())
base=json.loads(subprocess.check_output(['git','show',m['baseMain']+':story/artwork.draft.json'],cwd=R))
def record(d,k):
 g,k=k.split(':',1)
 return d[g][k.split('#')[0]]['portraitBackground'] if '#' in k else d[g][k]
assert len(m['candidates'])==9 and not m['selected'] and not m['approved'] and m['assetPath'] is None
results=[]
for c in m['candidates']:
 p=P/c['file'];im=Image.open(p);dim=tuple(c['dimensions']);assert im.size==dim
 assert sha(p)==c['sha256'];assert c['status']=='generated' and c['selected'] is False and c['approved'] is False and c['assetPath'] is None
 alpha=im.convert('RGBA').getchannel('A').histogram();assert sum(alpha[1:255])==0
 if c['record'].startswith('portraits:'):assert im.mode=='RGBA' and alpha[0]>0
 else:assert im.mode=='RGB' and alpha[0]==0
 preview=Image.open(P/c['preview4x']);assert preview.size==(dim[0]*4,dim[1]*4)
 assert preview.tobytes()==im.resize(preview.size,Image.Resampling.NEAREST).tobytes()
 assert sha(P/c['source']['original'])==c['source']['sha256']
 assert (P/c['prompt']).is_file() and c['registeredPrompt']==record(a,c['record'])['prompt']
 for op in c['operations']:
  if op.get('outsideMaskChanged')==0:
   refs=json.loads((P/'references/approved-sources.json').read_text());old=Image.open(P/refs[op['base']]['reviewFile']).convert('RGB');mask=Image.open(P/op['mask'])
   changed=[]
   for y in range(im.height):
    for x in range(im.width):
     if im.getpixel((x,y))!=old.getpixel((x,y)):
      assert mask.getpixel((x,y))==255;changed.append([x,y])
   assert changed==json.loads((P/op['changedCoordinates']).read_text())
 results.append({'id':c['candidateId'],'result':'PASS','sha256':c['sha256'],'dimensions':dim,'mode':im.mode,'alphaPartial':0,'exact4x':True})
refs=json.loads((P/'references/approved-sources.json').read_text())
for k,r in refs.items():assert sha(P/r['reviewFile'])==r['sha256']==sha(R/r['file'])
# All selected bytes, preview entries, approved narrative and history remain byte-exact.
for path in ['story/artwork-preview.json','story/chapters/chapter-03.reboot-candidate.json','story/archives/chapter-03-pre-reboot-20261118.json','story/storyboard-manifest.json']:
 assert (R/path).read_bytes()==subprocess.check_output(['git','show',m['baseMain']+':'+path],cwd=R)
for line in subprocess.check_output(['git','ls-tree','-r',m['baseMain'],'assets/selected','docs/artwork-history'],cwd=R,text=True).splitlines():
 metadata,path=line.split('\t');digest=metadata.split()[2];data=(R/path).read_bytes();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==digest
# Only nine previously unstarted records may advance; only status/notes change.
newkeys={c['record'] for c in m['candidates']}
for k in newkeys:
 old=record(base,k);current=record(a,k);assert old['status']=='not-started';assert current['status'] in ('not-started','generated')
 if current['status']=='generated':
  restored=dict(current);restored['status']=old['status'];restored['notes']=old['notes'];assert restored==old
  record(a,k)['status']=old['status'];record(a,k)['notes']=old['notes']
assert a==base
inventory=json.loads((P/'inventory.json').read_text());assert len(inventory['nodeCoverage'])==34 and not inventory['missingRegisteredRequirements']
assert all(not n['missingRegistryRequirements'] for n in inventory['nodeCoverage'])
attendant=Image.open(P/m['candidates'][2]['file']);assert attendant.getbbox()[3]==278
initial=Image.open(P/'proofs/D03-initial-seated-cut-before-correction.png')
initial.putdata([p if p[3] else (0,0,0,0) for p in initial.getdata()])
assert attendant.crop((0,0,564,230)).tobytes()==initial.crop((0,0,564,230)).tobytes()
report={'result':'PASS','candidates':results,'approvedReferenceCopies':len(refs),'allSelectedAssetBytesUnchanged':True,'previewRegistryUnchanged':True,'narrativeAndArchiveUnchanged':True,'registryChangesRestrictedToNineUnstartedStatusAndNotes':True,'courtesyPixelsOutsideStateMasksUnchanged':True,'attendantCanvasEdgeAnchored':True,'attendantUpperPortraitPreserved':True,'nativeGridAuthorship':'UNPROVEN; technical validation is not creative approval.'}
(P/'qa/results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
