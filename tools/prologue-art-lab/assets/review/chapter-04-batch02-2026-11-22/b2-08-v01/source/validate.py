from pathlib import Path
from PIL import Image,ImageChops
from html.parser import HTMLParser
import json,hashlib,subprocess,os
ROOT=Path(__file__).resolve().parents[1];REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists())
BASE='8d32d44c787c09884ca0b3455c34f2a539d34db2'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 checks=[]
 def check(v,s):
  assert v,s
  checks.append({'check':s,'passed':True})
 m=json.loads((ROOT/'manifest.json').read_text());nodes=json.loads((ROOT/'evidence/canonical-node-evidence.json').read_text())['nodes'];allassets=m['assets']+m['supplementalStates'];check(len(m['assets'])==6 and len(m['supplementalStates'])==6,'Exactly six primary demands and six separate conditional references')
 for a in allassets:
  id_=a['id'];im=Image.open(ROOT/a['native']['file']);four=Image.open(ROOT/a['preview4x']['file']);portrait=a['kind']=='portrait';size=(314,206)if id_.startswith('CH4-B2-42')else(564,278)
  check(im.size==size and im.mode==('RGBA'if portrait else'RGB'),id_+' correct native grid/mode');check(sha(ROOT/a['native']['file'])==a['native']['sha256'],id_+' exact manifest hash');check(four.size==(size[0]*4,size[1]*4)and four.tobytes()==im.resize(four.size,Image.Resampling.NEAREST).tobytes(),id_+' exact nearest4x');check(sha(ROOT/a['preview4x']['file'])==a['preview4x']['sha256'],id_+' preview hash');check(a['status']=='UNSELECTED'and not a['selected']and a['sourceDerived']and not a['independentlyAuthoredAtNativeResolution'],id_+' unselected honest provenance')
  if portrait:
   al=im.getchannel('A');box=al.getbbox();check(set(al.get_flattened_data())=={0,255},id_+' binary transparent silhouette');check(all(p==(0,0,0,0)for p in im.get_flattened_data()if not p[3]),id_+' zero hidden RGB');check(box[0]>10 and box[1]>5 and box[2]<554,id_+' head/hands inside margins');src=Image.open(ROOT/a['detailedReference']['file']);check(src.mode=='RGBA'and src.getchannel('A').getextrema()[0]==0,id_+' original true alpha preserved');who,pose=a['key'].split(':')[1:];check(all(nodes[n]['speaker']==who and nodes[n]['pose']==pose for n in a['nodeIds']),id_+' exact speaker pose nodes')
   c=a['composite'];bg=Image.open(ROOT/f'native/{c["backgroundAssetId"]}-v01.png').convert('RGBA');comp=Image.open(ROOT/c['native']['file']);check(comp.tobytes()==Image.alpha_composite(bg,im).convert('RGB').tobytes(),id_+' exact authored-context layered composite');check(Image.open(ROOT/c['preview4x']['file']).tobytes()==comp.resize((2256,1112),Image.Resampling.NEAREST).tobytes(),id_+' composite exact4x')
   if 'serviceComposite'in a:
    c=a['serviceComposite'];bg=Image.open(ROOT/c['backgroundReference']).convert('RGBA');comp=Image.open(ROOT/c['native']['file']);check(comp.tobytes()==Image.alpha_composite(bg,im).convert('RGB').tobytes(),id_+' unchanged approved service-context composite');check(set(a['sceneKeys'])=={'grand_bellevue/boiler_room','grand_bellevue/service_passage'},id_+' exact two authored dialogue contexts')
  elif a in m['assets']:check(all(nodes[n]['scene']=='grand_bellevue/boiler_room'for n in a['nodeIds']),id_+' exact existing scene coverage')
  if a in m['supplementalStates']:
   check(a['canonicalKey']is None and a['runtimeBinding']is None and a['newFocusId']is None,id_+' no invented canonical/runtime IDs');base=Image.open(ROOT/f'native/{a["comparisonBaseId"]}-v01.png');allowed=Image.open(ROOT/a['allowedMask']);pairs=list(zip(base.get_flattened_data(),im.get_flattened_data(),allowed.get_flattened_data()));check(any(x!=y for x,y,_ in pairs),id_+' meaningful state change');check(all(x==y for x,y,k in pairs if not k),id_+' all pixels outside bounded state region exact')
 for n,r in json.loads((ROOT/'evidence/environment-derivation.json').read_text()).items():
  check(r['nativeStructureChangesInsideProtectedObjects']==0,n+' structure preserves complete protected story objects')
  initial=Image.open(ROOT/f'native/{n}-v01.png');face=Image.open(ROOT/f'masks/{n}-gauge-face.png');door=json.loads((ROOT/'evidence/canonical-node-evidence.json').read_text())
  for suffix,state in r['states'].items():
   check(state['outsideAllowedChanges']==0,n+' '+suffix+' bounded object edits')
   if suffix=='relieved':check(state['gauge']['sector']=='GREEN' and state['gauge']['needleTip'][0]<state['gauge']['center'][0],n+' needle physically rotates LEFT into green')
   else:
    check(state['gauge']['sector']=='RED' and state['gauge']['needleTip'][0]>state['gauge']['center'][0],n+' '+suffix+' remains high pressure RED')
    im=Image.open(ROOT/f'native/{n}-{suffix}-v01.png');check(all(a==b for a,b,k in zip(initial.get_flattened_data(),im.get_flattened_data(),face.get_flattened_data())if k),n+' '+suffix+' actual dial pixels unchanged')
 from native_build import LAYOUT
 from shared_native import mask
 for n in[42,47]:
  id_=f'CH4-B2-{n}';im=Image.open(ROOT/f'native/{id_}-v01.png');door=mask(im.size,[LAYOUT[n]['doorRegion']])
  for state in['inspection-hold','staff-access']:
   other=Image.open(ROOT/f'native/{id_}-{state}-v01.png');check(all(a==b for a,b,k in zip(im.get_flattened_data(),other.get_flattened_data(),door.get_flattened_data())if k),id_+' '+state+' lavatory remains exactly closed and chained')
  check(Image.open(ROOT/f'layers/{id_}-native-do-not-operate-tag.png').getchannel('A').getbbox()is not None,id_+' separate authored DO NOT OPERATE tag')
 for name,a in m['canonicalBenchmarks'].items():check((ROOT/f'references/{name}.png').read_bytes()==subprocess.check_output(['git','show',m['canonicalApprovalBaseline']+':'+a['file']],cwd=REPO),'Exact immutable approved benchmark '+name)
 for p in(ROOT/'comparisons').glob('*-native.png'):
  im=Image.open(p);four=Image.open(p.with_name(p.name.replace('-native.png','-4x.png')));check(four.tobytes()==im.resize(four.size,Image.Resampling.NEAREST).tobytes(),'Exact4x direct comparison '+p.name)
 old=0
 for row in subprocess.check_output(['git','ls-tree','-r',BASE,'tools/prologue-art-lab/assets/review','story','assets/selected','.github','docs'],cwd=REPO,text=True).splitlines():
  metadata,path=row.split('\t',1)
  if path.startswith('tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/')and Path(path).name in['AGENTS.md','README.md','SHA256SUMS']:continue
  blob=(REPO/path).read_bytes();digest=hashlib.sha1(b'blob '+str(len(blob)).encode()+b'\0'+blob).hexdigest();check(digest==metadata.split()[2],'Preserved canonical/historical file '+path);old+=1
 class Links(HTMLParser):
  def handle_starttag(self,t,attrs):
   for k,v in attrs:
    if v=='evidence/validation.json':continue
    if k in['src','href','data-one','data-four']and v and not v.startswith(('https:','http:','#','data:')):check((ROOT/v).is_file(),'Gallery dependency '+v)
 Links().feed((ROOT/'index.html').read_text())
 paths=[p for folder in['native','previews','layers','masks','comparisons']for p in(ROOT/folder).glob('*.png')]+[ROOT/'manifest.json',ROOT/'index.html'];before={str(p.relative_to(ROOT)):sha(p)for p in paths}
 for script in['native_build.py','package.py']:subprocess.run(['python3',str(ROOT/'source'/script)],cwd=REPO,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=subprocess.DEVNULL,check=True)
 check(all(sha(ROOT/p)==s for p,s in before.items()),'Deterministic native/gallery replay exact')
 out={'passed':True,'checksPassed':len(checks),'primaryAssets':6,'conditionalReferenceFrames':6,'status':'UNSELECTED','canonicalNodeCount':6,'historicalAndCanonicalFilesPreserved':old,'canonicalFilesChanged':0,'replayFilesIdentical':len(before),'sourceDerived':True,'integrationPerformed':False,'visualAssessment':'evidence/visual-review.md','checks':checks};(ROOT/'evidence/validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='checks'}))
if __name__=='__main__':main()
