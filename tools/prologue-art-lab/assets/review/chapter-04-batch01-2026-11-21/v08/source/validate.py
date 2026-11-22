"""Portrait quality contracts, exact freezes and canonical inventory audit."""
from pathlib import Path
from PIL import Image
from html.parser import HTMLParser
import hashlib,json,runpy,tempfile,subprocess

ROOT=Path(__file__).resolve().parent.parent
REVIEW=ROOT.parent
REPO=next(p for p in ROOT.parents if (p/'story/artwork.draft.json').exists())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 checks=[]
 def check(value,label):
  assert value,label
  checks.append({'check':label,'passed':True})
 baseline=json.loads((ROOT/'evidence/preservation-baseline.json').read_text())
 for rel,h in baseline['files'].items():check((REVIEW/rel).is_file() and sha(REVIEW/rel)==h,'Prior version preserved: '+rel)
 freeze=json.loads((ROOT/'evidence/frozen-preferred-environments.json').read_text())
 check({a['id']:a['preferredReviewVersion'] for a in freeze['assets']}=={'CH4-01':'v05','CH4-02':'v05','CH4-04':'v07','CH4-05':'v07'},'Exact four owner-preferred candidate versions')
 for a in freeze['assets']:
  check(a['status']=='UNSELECTED' and not a['formalSelectionConfirmed'] and a['frozen'],'Freeze is not formal approval: '+a['id'])
  check(sha(ROOT/a['file'])==a['sha256'],'Frozen exact native PNG: '+a['id'])
  with Image.open(ROOT/a['file']) as im,Image.open(ROOT/a['preview4x']['file']) as big:
   check(list(im.size)==a['dimensions'] and im.mode==a['mode'],'Frozen dimensions/mode: '+a['id'])
   check(big.size==(im.width*4,im.height*4) and big.tobytes()==im.resize(big.size,Image.Resampling.NEAREST).tobytes(),'Existing frozen exact4x preview: '+a['id'])
 manifest=json.loads((ROOT/'manifest.json').read_text());portrait=manifest['portrait'];native=ROOT/portrait['native']['file'];im=Image.open(native)
 check(im.size==(564,278) and im.mode=='RGBA','Final transparent 564x278 portrait contract')
 check(im.getchannel('A').getextrema()==(0,255),'Real transparent exterior and painted foreground')
 prior=Image.open(REVIEW/'v06/native/CH4-03-auctioneer-source-derived-v06.png')
 check(im.getchannel('A').tobytes()==prior.getchannel('A').tobytes(),'Exact prior alpha/silhouette retained')
 report=json.loads((ROOT/'evidence/portrait-derivation.json').read_text());regions=report['nativeInteriorCleanup']['eligibleRegions'];pp=prior.load();np=im.load();changed=outside=0
 for y in range(278):
  for x in range(564):
   if pp[x,y]==np[x,y]:continue
   changed+=1
   eligible=0<x<563 and 0<y<277 and pp[x,y][3]>=245 and all(pp[xx,yy][3]>=245 for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]) and any(x0<=x<x1 and y0<=y<y1 for x0,y0,x1,y1 in regions)
   outside+=not eligible
 check(changed==report['nativeInteriorCleanup']['changedPixels'] and outside==0,'Only declared near-opaque native feature regions changed; boundary colors preserved')
 check(not portrait['independentlyAuthoredAtNativeResolution'] and not report['independentlyAuthoredAtNativeResolution'],'Honest source-derived classification')
 check(sha(ROOT/portrait['source']['file'])==portrait['source']['sha256']==report['sourceSha256'],'Preferred source master hash preserved')
 old_path=(ROOT/portrait['source']['file']).resolve().relative_to(REPO).as_posix()
 source_at_preferred_commit=subprocess.check_output(['git','show','2a267beaf182fa6b589d7256ae813de8b168e63a:'+old_path],cwd=REPO)
 check(hashlib.sha256(source_at_preferred_commit).hexdigest()==portrait['source']['sha256'],'Original source exactly matches the owner-specified preferred commit')
 mod=runpy.run_path(str(ROOT/'source/portrait.py'))
 with tempfile.TemporaryDirectory(prefix='ch4-v08-portrait-replay-') as temp:
  out=Path(temp);(out/'evidence').mkdir();mod['main'].__globals__['ROOT']=out;mod['main']()
  check((out/'native'/native.name).read_bytes()==native.read_bytes(),'Exact final source-derived portrait replay')
 for one_rel,four_rel in [(portrait['native']['file'],portrait['preview4x']['file']),(manifest['composite']['file'],manifest['composite4x']['file']),(manifest['comparison']['file'],manifest['comparison4x']['file'])]:
  with Image.open(ROOT/one_rel) as one,Image.open(ROOT/four_rel) as big:check(big.size==(one.width*4,one.height*4) and one.mode==big.mode and big.tobytes()==one.resize(big.size,Image.Resampling.NEAREST).tobytes(),'Every exact4x pixel: '+one_rel)
 bg=Image.open(REVIEW/'v05/native/CH4-02-auctioneer-background-v05.png').convert('RGBA');composite=Image.open(ROOT/manifest['composite']['file']);check(composite.tobytes()==Image.alpha_composite(bg,im).tobytes(),'Composite uses exact frozen background and final foreground')
 selection=json.loads((ROOT/'BATCH1-SELECTION-READY.json').read_text())
 check(len(selection['assets'])==5 and not selection['formalApprovalRegistrationPerformed'] and not selection['productionIntegrationPerformed'],'Five selection-ready candidates; no registry/production action')
 for a in selection['assets']:check(a['status']=='UNSELECTED' and a['canonicalProductionAssetPath'] is None and sha(ROOT/a['native']['file'])==a['native']['sha256'],'Selection-ready exact hash / unselected status: '+a['id'])
 sources=json.loads((ROOT/'evidence/canonical-sources.json').read_text())
 for f in sources['files']:check(sha(ROOT/f['snapshot'])==f['sha256'],'Pinned canonical snapshot hash: '+f['canonicalPath'])
 canon=ROOT/'evidence/canonical';chapter=json.loads((canon/'story__chapters__chapter-04.wip.json').read_text());nodes=chapter['nodes'];registry=json.loads((canon/'story__artwork.draft.json').read_text());inv=json.loads((ROOT/'BATCH2-INVENTORY.json').read_text());assets=inv['assets']
 check(len(nodes)==120 and set(inv['nodeCoverage'])==set(nodes) and all(inv['nodeCoverage'].values()),'Exact120-node inventory coverage, no missing/invented node IDs')
 expected={
  'main_scene':{n['scene'] for n in nodes.values()},
  'portrait':{n['speaker']+':'+n['pose'] for n in nodes.values() if n.get('speaker')},
  'portrait_background':{n['scene'] for n in nodes.values() if n.get('speaker')},
  'focus_a':{n['focus'] for n in nodes.values() if n.get('focus')},
  'fatal_aftermath':{n['endingArt'] for n in nodes.values() if n.get('endingArt')},
 }
 for cat,keys in expected.items():check({a['logicalKey'] for a in assets if a['category']==cat}==keys,'Exact canonical demand set: '+cat)
 groups={g['id'] for g in inv['groups']}|{'BATCH1'}
 for a in assets:
  check(a['group'] in groups and a['artworkStatus']=='UNSELECTED' and all(i in nodes for i in a['nodeIds']),'Planning group/status/source node IDs: '+a['inventoryId'])
  for id_ in a['nodeIds']:
   check(a['inventoryId'] in inv['nodeCoverage'][id_],'Bidirectional node coverage: '+a['inventoryId']+'/'+id_)
   if a['category']=='main_scene':check(nodes[id_]['scene']==a['logicalKey'],'Canonical scene field: '+id_)
   elif a['category']=='portrait':check(nodes[id_]['speaker']+':'+nodes[id_]['pose']==a['logicalKey'],'Canonical speaker/pose: '+id_)
   elif a['category']=='focus_a':check(nodes[id_]['focus']==a['logicalKey'],'Canonical Focus A key: '+id_)
   elif a['category']=='fatal_aftermath':check(nodes[id_]['endingArt']==nodes[id_]['deathPopup']['artRef']==a['logicalKey'] and a['sourceBriefVerbatim']==nodes[id_]['notes'],'Exact fatal artRef and brief: '+id_)
   elif a['category']=='state_family':check(a['canonicalKey'] is None and a['evidence'][id_]['text']==nodes[id_]['text'],'Narrative-derived state evidence, not invented canonical key: '+id_)
  if a['category'] in ['inventory_slot','inventory_inspect']:
   kind=a['category'].split('_',1)[1];record=registry['items'][a['logicalKey']][kind]
   check(a['registryPromptVerbatim']==record['prompt'] and a['registryNotesVerbatim']==record['notes'] and a['suggestedFilename']==record.get('suggestedFilename'),'Exact existing item-art record: '+a['inventoryId'])
 first=inv['recommendedFirstGroup'];check(first['id']=='B2-01' and first['primaryUnits']==5 and first['stateFamilies']==0 and not first['generationStarted'],'Recommended first group is five canonical restroom dialogue/control units; not generated')
 check(len([a for a in assets if a['category'].startswith('inventory_')])==4,'Exactly four new item-art records')
 check(not any(a['logicalKey'] in ['autofit_gown','three_seashells','shutoff_wheel'] for a in assets if a['category'].startswith('inventory_')),'Temporary props not invented as inventory')
 check(not manifest['batch2GenerationStarted'],'Inventory handoff is not unauthorized Batch2 generation')
 class Links(HTMLParser):
  def handle_starttag(self,tag,attrs):
   for key,value in attrs:
    if key not in ['src','href','data-one','data-four'] or not value or value.startswith(('#','http:','https:')):continue
    p=(ROOT/value).resolve()
    if p==ROOT/'evidence/validation.json':continue
    check(p.is_relative_to(REVIEW) and p.is_file(),'Gallery dependency: '+value)
 Links().feed((ROOT/'index.html').read_text())
 protected=subprocess.check_output(['git','diff','--name-only',baseline['baseCommit'],'--','story','assets','docs','.github'],cwd=REPO,text=True).strip();check(not protected,'Production/narrative/gameplay/approval files unchanged')
 result={'passed':True,'checksPassed':len(checks),'artworkApproved':False,'formalSelectionRegistered':False,'frozenEnvironmentCount':4,'frozenEnvironmentsUnchanged':True,'priorFilesPreserved':len(baseline['files']),'portraitInteriorPixelsChanged':changed,'portraitAlphaAndBoundaryPreserved':True,'inventoryCanonicalNodesCovered':120,'batch2GenerationStarted':False,'checks':checks}
 (ROOT/'evidence/validation.json').write_text(json.dumps(result,indent=2)+'\n');print(str(len(checks))+' v08 checks passed; four exact freezes;120/120 inventory nodes;all artwork UNSELECTED.')

if __name__=='__main__':main()
