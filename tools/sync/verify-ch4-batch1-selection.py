"""Read-only verification of Nate's five unchanged Chapter 4 selections."""
from pathlib import Path
from PIL import Image
import hashlib,json,subprocess

ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/'docs/127_CH4_BATCH1_APPROVAL_COMPLETION_20261122.json'
def digest(b):return hashlib.sha256(b).hexdigest()
def git_blob(commit,path):return subprocess.check_output(['git','show',commit+':'+path],cwd=ROOT)
def main():
 d=json.loads(DOC.read_text());checks=[]
 def check(value,label):
  assert value,label
  checks.append({'check':label,'passed':True})
 source=d['approvalSourceCommit'];base=d['canonicalBase']
 source_manifest=json.loads(git_blob(source,d['sourceSelectionManifest']['file']))
 check(digest(git_blob(source,d['sourceSelectionManifest']['file']))==d['sourceSelectionManifest']['sha256'],'Pinned authoritative selection manifest')
 catalog=json.loads((ROOT/'story/artwork.draft.json').read_text());previews=json.loads((ROOT/'story/artwork-preview.json').read_text())['images']
 for i,a in enumerate(d['assets']):
  original=git_blob(source,a['source']['path']);registered=ROOT/a['canonicalSelectedPath']
  check(digest(original)==digest(registered.read_bytes())==a['sha256']==source_manifest['assets'][i]['native']['sha256'],'Exact owner/source/registered PNG hash '+a['id'])
  with Image.open(registered) as im:
   check(list(im.size)==a['dimensions'] and im.mode==a['mode'],'Native dimensions/mode '+a['id'])
   alpha=im.convert('RGBA').getchannel('A').getextrema()
   check(alpha[0]==0 if a['id']=='CH4-03' else alpha==(255,255),'Alpha contract '+a['id'])
  p=previews[a['registryKey']]
  check(p['sha256']==a['sha256'] and p['file']==a['canonicalSelectedPath'] and p['source']==a['source'],'Registered selected provenance '+a['id'])
  group,key=a['registryKey'].split(':',1)
  if '#portraitBackground' in key:record=catalog[group][key.split('#')[0]]['portraitBackground']
  else:record=catalog[group][key]
  check(record['status']=='approved' and record['assetPath'] is None and record['suggestedFilename']==a['suggestedEngineDestination'],'Approved/selected without game integration '+a['id'])
  check(a['storyNodeIds'] and a['selectionStatus']=='SELECTED','Exact story associations '+a['id'])
  if a['id']=='CH4-03':check('SOURCE-DERIVED' in record['notes'] and not source_manifest['assets'][i]['independentlyAuthoredAtNativeResolution'],'Source-derived portrait provenance explicit')
 old_preview=json.loads(git_blob(base,'story/artwork-preview.json'))['images']
 for k,p in old_preview.items():
  check(previews[k]==p,'Previous selected metadata preserved '+k)
  check((ROOT/p['file']).read_bytes()==git_blob(base,p['file']),'Previous selected PNG bytes preserved '+k)
 check(len(previews)==len(old_preview)+5,'Exactly five new selections')
 old_catalog=json.loads(git_blob(base,'story/artwork.draft.json'))
 reduced=json.loads(json.dumps(catalog))
 for k in ['grand_bellevue/lobby','grand_bellevue/restroom','grand_bellevue/ballroom']:del reduced['scenes'][k]
 del reduced['portraits']['hotel_auctioneer:showman']
 check(reduced==old_catalog,'All earlier artwork records unchanged')
 for path in subprocess.check_output(['git','ls-tree','-r','--name-only',base,'story','.github'],cwd=ROOT,text=True).splitlines():
  if path in ['story/artwork.draft.json','story/artwork-preview.json']:continue
  check((ROOT/path).read_bytes()==git_blob(base,path),'Canonical narrative/gameplay/workflow unchanged '+path)
 ledger=ROOT/'docs/103_RETROACTIVE_ARTWORK_APPROVAL_LEDGER.md'
 check(ledger.read_bytes().startswith(git_blob(base,str(ledger.relative_to(ROOT)))),'Prior approval ledger prefix preserved')
 report={'passed':True,'checksPassed':len(checks),'registeredAssets':5,'previousSelectionsPreserved':len(old_preview),'allFiveApprovedAndSelected':True,'sourceCommit':source,'baseCommit':base,'integrationPerformed':False,'checks':checks}
 (ROOT/'docs/127_CH4_BATCH1_VERIFICATION_20261122.json').write_text(json.dumps(report,indent=2)+'\n')
 print(str(len(checks))+' checks passed; five approved/selected, no integration.')
if __name__=='__main__':main()
