"""Separate QA for source-derived portrait and independently native environments."""
from pathlib import Path
from PIL import Image
from html.parser import HTMLParser
from unittest import mock
import hashlib,json,io,runpy,sys,subprocess,tempfile

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
 for rel,h in baseline['files'].items():check((REVIEW/rel).is_file() and sha(REVIEW/rel)==h,'Preserved earlier bytes: '+rel)
 manifest=json.loads((ROOT/'manifest.json').read_text())
 frozen=json.loads((ROOT/'evidence/frozen-environments.json').read_text())
 for f in frozen['files']:check(sha(REVIEW/f['file'])==f['sha256'],'Frozen v05 environment: '+f['file'])
 for a in manifest['assets']:
  check(a['status']=='UNSELECTED','Unselected status: '+a['id'])
  for key in ['native','preview4x','previous','previousPreview4x','benchmark','detailedReference','comparison','comparison4x']:
   f=a[key];p=ROOT/f['file'];check(sha(p)==f['sha256'],'Image hash '+a['id']+'/'+key)
   with Image.open(p) as im:check(list(im.size)==f['dimensions'] and im.mode==f['mode'],'Dimensions/mode '+a['id']+'/'+key)
  with Image.open(ROOT/a['native']['file']) as im,Image.open(ROOT/a['preview4x']['file']) as four:
   expected=(564,278) if a['id']=='CH4-03' else (314,206)
   check(im.size==expected,'Actual target grid: '+a['id'])
   check(four.size==(im.width*4,im.height*4) and four.mode==im.mode,'Exact4x dimensions/mode: '+a['id'])
   check(four.tobytes()==im.resize(four.size,Image.Resampling.NEAREST).tobytes(),'All exact4x pixels: '+a['id'])
   if a['id']=='CH4-03':check(im.mode=='RGBA' and im.getchannel('A').getextrema()==(0,255),'Transparent portrait cutout')
   else:check(im.mode=='RGB','Opaque scene: '+a['id'])
 # Replay scenes while rejecting every prohibited source-raster operation.
 sys.path.insert(0,str(ROOT/'source'));import scene_tools
 def forbidden(*args,**kwargs):raise AssertionError('Scene raster input/resampling forbidden')
 original_new=Image.new
 def native_new(mode,size,*args,**kwargs):
  check(size==(314,206),'Scene canvas/mask stays native 314x206')
  return original_new(mode,size,*args,**kwargs)
 collected={}
 def capture(self,p):
  b=io.BytesIO();self.im.save(b,format='PNG');collected[Path(p).name]=b.getvalue()
 patches=[mock.patch.object(Image,'open',forbidden),mock.patch.object(Image,'new',native_new),mock.patch.object(scene_tools.Canvas,'save',capture)]
 patches += [mock.patch.object(Image.Image,name,forbidden) for name in ['resize','crop','filter','quantize','transform']]
 for p in patches:p.start()
 try:
  runpy.run_path(str(ROOT/'source/restroom.py'),run_name='__main__')
  runpy.run_path(str(ROOT/'source/ballroom.py'),run_name='__main__')
 finally:
  for p in reversed(patches):p.stop()
 for name,content in collected.items():check(content==(ROOT/'backgrounds'/name).read_bytes(),'Independent room-background exact PNG replay: '+name)
 check(len(collected)==2,'Both native backgrounds replayed separately from derived character assembly')
 # Final hybrid frames are separately replayed with their explicitly allowed
 # source-derived people; never mislabel the full frame as independently native.
 npc_module=runpy.run_path(str(ROOT/'source/scene_people.py'))
 with tempfile.TemporaryDirectory(prefix='ch4-v06-scene-people-') as temp:
  out=Path(temp);(out/'evidence').mkdir();(out/'backgrounds').symlink_to(ROOT/'backgrounds',target_is_directory=True);(out/'detailed').symlink_to(ROOT/'detailed',target_is_directory=True)
  npc_module['main'].__globals__['ROOT']=out;npc_module['main']()
  for name in ['CH4-04-restroom-v02.png','CH4-05-ballroom-v02.png']:
   check((out/'native'/name).read_bytes()==(ROOT/'native'/name).read_bytes(),'Hybrid scene exact NPC-composition replay: '+name)
 npc_derivation=json.loads((ROOT/'evidence/scene-npc-derivation.json').read_text())
 check(not npc_derivation['rejectedCodeFiguresUsed'],'Rejected faceless code figures not used')
 for layer in npc_derivation['layers']:
  check(not layer['independentlyNativeAuthored'],'Honest source-derived actor classification: '+layer['id'])
  check(sha(ROOT/layer['source'])==layer['sourceSha256'] and sha(ROOT/layer['file'])==layer['sha256'],'Actor master/layer provenance: '+layer['id'])
 for a in manifest['assets']:
  check(not a['independentlyAuthoredAtNativeResolution'],'Whole-frame independent-native claim absent: '+a['id'])
 # Authorized derived portrait replay; do not impose the old no-resize restriction.
 module=runpy.run_path(str(ROOT/'source/portrait.py'))
 with tempfile.TemporaryDirectory(prefix='ch4-v06-portrait-') as temp:
  out=Path(temp);(out/'evidence').mkdir();module['main'].__globals__['ROOT']=out;module['main']()
  check((out/'native/CH4-03-auctioneer-source-derived-v06.png').read_bytes()==(ROOT/'native/CH4-03-auctioneer-source-derived-v06.png').read_bytes(),'Authorized portrait derivation exact replay')
 derivation=json.loads((ROOT/'evidence/portrait-derivation.json').read_text())
 check(not derivation['independentlyAuthoredAtNativeResolution'] and derivation['method'].startswith('SOURCE-DERIVED'),'Honest portrait provenance')
 check(sha(ROOT/derivation['source'])==derivation['sourceSha256'],'Preferred source illustration unchanged')
 policy=json.loads((ROOT/'evidence/production-policy-decision.json').read_text())
 check(policy['sourceDerivedPortraitsAuthorized'] and policy['sourceDerivedExceptionDecision']=='AUTHORIZED','Later policy resolves formerly pending exception')
 check(not policy['approvalRecordsChanged'],'Policy authorization does not register artwork approval')
 bg=Image.open(REVIEW/'v05/native/CH4-02-auctioneer-background-v05.png').convert('RGBA');fg=Image.open(ROOT/manifest['assets'][0]['native']['file']).convert('RGBA')
 composite=Image.open(ROOT/manifest['composite']['file'])
 check(composite.tobytes()==Image.alpha_composite(bg,fg).tobytes(),'Composite uses exact frozen background and final foreground')
 for name in ['CH4-03','CH4-04','CH4-05']:
  one=Image.open(ROOT/f'comparisons/{name}-candidate-history-approved.png');four=Image.open(ROOT/f'comparisons/{name}-candidate-history-approved-4x.png')
  check(four.size==(one.width*4,one.height*4) and four.tobytes()==one.resize(four.size,Image.Resampling.NEAREST).tobytes(),'Comparison sheet exact4x '+name)
 class Links(HTMLParser):
  def handle_starttag(self,tag,attrs):
   for key,val in attrs:
    if key not in ['src','href','data-one','data-four','value'] or not val or val.startswith(('#','http:','https:')):continue
    p=(ROOT/val).resolve()
    if p==ROOT/'evidence/validation.json':continue
    check(p.is_relative_to(REVIEW) and p.is_file(),'Gallery dependency: '+val)
 Links().feed((ROOT/'index.html').read_text())
 canonical=json.loads((ROOT/'evidence/canonical-requirements.json').read_text());actual=json.loads((REPO/'story/chapters/chapter-04.wip.json').read_text())['nodes']
 for a in canonical.values():
  for id_,node in a['verbatimNodes'].items():check(actual[id_]==node,'Verbatim canonical node: '+id_)
 changed=subprocess.check_output(['git','diff','--name-only',baseline['baseCommit'],'--','story','assets','docs','.github'],cwd=REPO,text=True).strip()
 check(not changed,'Production assets/workflows/narrative/gameplay/approval paths unchanged')
 report={'passed':True,'checksPassed':len(checks),'artworkApproved':False,'portraitAuthorship':'SOURCE-DERIVED - owner authorized','sceneAuthorship':'HYBRID: independent native backgrounds plus source-derived illustrated NPCs; both replays verified','earlierFilesPreserved':len(baseline['files']),'checks':checks}
 (ROOT/'evidence/validation.json').write_text(json.dumps(report,indent=2)+'\n');print(str(len(checks))+' v06 QA checks passed; all candidates UNSELECTED.')

if __name__=='__main__':main()
