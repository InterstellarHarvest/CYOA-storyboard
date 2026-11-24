from pathlib import Path
from PIL import Image,ImageChops
from html.parser import HTMLParser
import json,hashlib,subprocess,os
ROOT=Path(__file__).resolve().parents[1];REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists())
BASE='f6840e5d69f70435f88ce9ece720583566fce8e2'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 checks=[]
 def check(v,s):
  assert v,s
  checks.append({'check':s,'passed':True})
 m=json.loads((ROOT/'manifest.json').read_text());nodes=json.loads((ROOT/'evidence/canonical-node-evidence.json').read_text())['nodes'];allassets=m['assets']+m['supplementalStates'];check(len(m['assets'])==5 and len(m['supplementalStates'])==4,'Exactly five primary demands and four separate conditional references')
 for a in allassets:
  id_=a['id'];im=Image.open(ROOT/a['native']['file']);four=Image.open(ROOT/a['preview4x']['file']);portrait=a['kind']=='portrait';size=(314,206)if id_.startswith('CH4-B2-37')else(564,278)
  check(im.size==size and im.mode==('RGBA'if portrait else'RGB'),id_+' correct native grid/mode');check(sha(ROOT/a['native']['file'])==a['native']['sha256'],id_+' exact manifest hash');check(four.size==(size[0]*4,size[1]*4)and four.tobytes()==im.resize(four.size,Image.Resampling.NEAREST).tobytes(),id_+' exact nearest4x');check(sha(ROOT/a['preview4x']['file'])==a['preview4x']['sha256'],id_+' preview hash');check(a['status']=='UNSELECTED'and not a['selected']and a['sourceDerived']and not a['independentlyAuthoredAtNativeResolution'],id_+' unselected honest provenance')
  if portrait:
   al=im.getchannel('A');box=al.getbbox();check(set(al.get_flattened_data())=={0,255},id_+' binary transparent silhouette');check(all(p==(0,0,0,0)for p in im.get_flattened_data()if not p[3]),id_+' zero hidden RGB');check(box[0]>10 and box[1]>5 and box[2]<554,id_+' head/hands inside margins');src=Image.open(ROOT/a['detailedReference']['file']);check(src.mode=='RGBA'and src.getchannel('A').getextrema()[0]==0,id_+' original true alpha preserved');who,pose=a['key'].split(':')[1:];check(all(nodes[n]['speaker']==who and nodes[n]['pose']==pose for n in a['nodeIds']),id_+' exact speaker pose nodes')
   c=a['composite'];bg=Image.open(ROOT/f'native/{c["backgroundAssetId"]}-v01.png').convert('RGBA');comp=Image.open(ROOT/c['native']['file']);check(comp.tobytes()==Image.alpha_composite(bg,im).convert('RGB').tobytes(),id_+' exact authored-context layered composite');check(Image.open(ROOT/c['preview4x']['file']).tobytes()==comp.resize((2256,1112),Image.Resampling.NEAREST).tobytes(),id_+' composite exact4x')
  elif a in m['assets']:check(all(nodes[n]['scene']=='grand_bellevue/staff_lavatory'for n in a['nodeIds']),id_+' exact existing scene coverage')
  if a in m['supplementalStates']:
   check(a['canonicalKey']is None and a['runtimeBinding']is None and a['newFocusId']is None,id_+' no invented canonical/runtime IDs');base=Image.open(ROOT/f'native/{a["comparisonBaseId"]}-v01.png');allowed=Image.open(ROOT/a['allowedMask']);pairs=list(zip(base.get_flattened_data(),im.get_flattened_data(),allowed.get_flattened_data()));check(any(x!=y for x,y,_ in pairs),id_+' meaningful state change');check(all(x==y for x,y,k in pairs if not k),id_+' all pixels outside bounded state region exact')
 for n,r in json.loads((ROOT/'evidence/environment-derivation.json').read_text()).items():
  check(r['floorStructureChangesInsideStoryProtection']==0,n+' structure cannot overwrite protected story objects');check(r['permitOutsideAllowedChanges']==0,n+' permit patch bounded');im=Image.open(ROOT/f'native/{n}-cleared-v01.png');red=Image.open(ROOT/f'masks/{n}-red-story-ribbon.png');check(sum(bool(k)for k in red.get_flattened_data())>8,n+' rare red ribbon explicitly protected');check(any(r>g*1.5 and r>b*1.3 for (r,g,b),k in zip(im.get_flattened_data(),red.get_flattened_data())if k),n+' ribbon red survives final material pass')
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
 out={'passed':True,'checksPassed':len(checks),'primaryAssets':5,'conditionalReferenceFrames':4,'status':'UNSELECTED','canonicalNodeCount':3,'historicalAndCanonicalFilesPreserved':old,'canonicalFilesChanged':0,'replayFilesIdentical':len(before),'sourceDerived':True,'integrationPerformed':False,'visualAssessment':'evidence/visual-review.md','checks':checks};(ROOT/'evidence/validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='checks'}))
if __name__=='__main__':main()
