from pathlib import Path
from PIL import Image
import json,hashlib,subprocess
P=Path(__file__).resolve().parents[1];R=P.parents[5];V=P.parent/'v01'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((P/'manifest.json').read_text());old=json.loads((V/'manifest.json').read_text());result=[]
for c in m['candidates']:
 im=Image.open(P/c['file']);assert sha(P/c['file'])==c['sha256'];assert tuple(c['dimensions'])==im.size
 assert c['status']=='generated' and not c['selected'] and not c['approved'] and c['assetPath'] is None
 if c['retainedUnchanged']:
  assert c['sha256']==next(x['sha256'] for x in old['candidates'] if x['record']==c['record']);continue
 assert im.size==(564,278);assert sha(P/c['source']['original'])==c['source']['sha256']
 alpha=im.convert('RGBA').getchannel('A').histogram();assert sum(alpha[1:255])==0
 portrait=c['record'].startswith('portraits:');assert im.mode==('RGBA' if portrait else 'RGB');assert (alpha[0]>0)==portrait
 preview=Image.open(P/c['preview4x']);assert preview.size==(2256,1112);assert preview.tobytes()==im.resize(preview.size,Image.Resampling.NEAREST).tobytes()
 if portrait:
  assert im.getbbox()[3]==278 and 20<=im.getbbox()[1]<=35
  op=c['operations'][0];assert op['forcedBoundingBoxStretch'] is False
  ow,oh=op['original'];w,h=op['roundedRaster'];assert abs((w/ow)/(h/oh)-1)<.002
 result.append({'id':c['candidateId'],'result':'PASS','sha256':c['sha256'],'dimensions':list(im.size),'mode':im.mode,'partialAlpha':0,'exact4x':True})
assert len(result)==3 and sum(c['retainedUnchanged'] for c in m['candidates'])==6
for line in (V/'SHA256SUMS.txt').read_text().splitlines():
 digest,file=line.split('  ',1);assert sha(V/file)==digest
for scope in ['assets/selected','story/artwork-preview.json','story/chapters/chapter-03.reboot-candidate.json','story/archives']:
 assert not subprocess.check_output(['git','diff','3931c496c13c691c8afa3c5206d4f56196c372fc','--',scope],cwd=R)
for line in subprocess.check_output(['git','ls-tree','-r','3931c496c13c691c8afa3c5206d4f56196c372fc',str(V.relative_to(R))],cwd=R,text=True).splitlines():
 meta,file=line.split('\t');b=(R/file).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==meta.split()[2]
report={'result':'PASS','revised':result,'sixOtherCandidatesByteIdentical':True,'entireV01PackageByteIdentical':True,'approvedAssetBytesAndPreviewRegistryUnchanged':True,'narrativeAndArchivesUnchanged':True,'uniformPortraitExportNoBoundingBoxStretch':True,'portraitWaistAnchoredAtCanvasBottom':True,'nativeGridAuthorship':'unproven; larger immutable originals and derived operations documented'}
(P/'qa/results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
