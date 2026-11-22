"""Exact exports/replay and NPC-only scope preservation; not creative approval."""
from pathlib import Path
from PIL import Image,ImageDraw
from html.parser import HTMLParser
import hashlib,json,runpy,tempfile,subprocess

ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT.parent/'v06'
REPO=next(p for p in ROOT.parents if (p/'story/artwork.draft.json').exists())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 checks=[]
 def check(value,label):
  assert value,label
  checks.append({'check':label,'passed':True})
 baseline=json.loads((ROOT/'evidence/preservation-baseline.json').read_text())
 for rel,expected in baseline['files'].items():check((ROOT.parent/rel).is_file() and sha(ROOT.parent/rel)==expected,'Earlier file preserved: '+rel)
 m=json.loads((ROOT/'manifest.json').read_text());d=json.loads((ROOT/'evidence/npc-derivation.json').read_text());old=json.loads((BASE/'evidence/scene-npc-derivation.json').read_text())
 for layer,prior in zip(d['layers'],old['layers']):
  check(layer['position']==prior['position'] and layer['nativeSpriteSize']==prior['nativeSpriteSize'] and layer['sourceCropAbsolute']==prior['sourceCropAbsolute'],'Actor scale/placement/crop unchanged: '+layer['id'])
  check(sha(ROOT/layer['source'])==layer['sourceSha256'],'Original master unchanged: '+layer['id'])
  check(sha(ROOT/layer['file'])==layer['sha256'],'Final actor hash: '+layer['id'])
  im=Image.open(ROOT/layer['file']);check(set(im.getchannel('A').get_flattened_data())<={0,255},'Crisp native alpha coverage: '+layer['id'])
  check(not layer['independentlyNativeAuthored'],'Honest source-derived classification: '+layer['id'])
 # Reproduce derivation independently into a disposable directory, preserving
 # original input location and never mutating the reviewed output files.
 mod=runpy.run_path(str(ROOT/'source/derive.py'))
 with tempfile.TemporaryDirectory(prefix='ch4-v07-replay-') as tmp:
  out=Path(tmp);mod['main'].__globals__['ROOT']=out;mod['main']()
  for layer in d['layers']:check((out/layer['file']).read_bytes()==(ROOT/layer['file']).read_bytes(),'Exact actor replay: '+layer['id'])
  for name in ['CH4-04-restroom-v03.png','CH4-05-ballroom-v03.png']:check((out/'native'/name).read_bytes()==(ROOT/'native'/name).read_bytes(),'Exact complete scene replay: '+name)
 scopes=[]
 for a in m['assets']:
  one=Image.open(ROOT/a['native']['file']);prev=Image.open(ROOT/a['previous']['file']);four=Image.open(ROOT/a['preview4x']['file'])
  check(one.size==(314,206) and one.mode=='RGB','Native scene contract: '+a['id'])
  check(four.size==(1256,824) and four.tobytes()==one.resize((1256,824),Image.Resampling.NEAREST).tobytes(),'Every exact4x pixel: '+a['id'])
  check(a['status']=='UNSELECTED','No selection claimed: '+a['id'])
  for key in ['native','preview4x','previous','previous4x','benchmark','benchmark4x','comparison','comparison4x','background']:
   check(sha(ROOT/a[key]['file'])==a[key]['sha256'],'Manifest hash '+a['id']+'/'+key)
  room='restroom' if a['id']=='CH4-04' else 'ballroom';mask=Image.new('1',(314,206),0)
  for layer in d['layers']:
   if layer['room']!=room:continue
   for key in ['file','previousFile']:
    im=Image.open(ROOT/layer[key]);alpha=im.getchannel('A').point(lambda v:255 if v else 0);mask.paste(1,tuple(layer['position'])+(layer['position'][0]+im.width,layer['position'][1]+im.height),alpha)
  changed=outside=0;delta=Image.new('RGB',(314,206),'#182b29');mp=mask.load();dp=delta.load();newp=one.load();oldp=prev.load()
  for y in range(206):
   for x in range(314):
    if newp[x,y]!=oldp[x,y]:changed+=1;outside+=not mp[x,y];dp[x,y]=(235,180,95)
  check(outside==0,'All changed pixels stay within old/new NPC coverage: '+a['id'])
  mask.convert('L').save(ROOT/'evidence'/(a['id']+'-npc-only-mask.png'));delta.save(ROOT/'evidence'/(a['id']+'-changed-pixels.png'))
  scopes.append({'id':a['id'],'changedPixels':changed,'changedPixelsOutsideNPCAlpha':outside,'backgroundAndShadowPixelsOutsideNPCsUnchanged':True,'mask':'evidence/'+a['id']+'-npc-only-mask.png','delta':'evidence/'+a['id']+'-changed-pixels.png'})
 (ROOT/'evidence/scope-qa.json').write_text(json.dumps({'passed':True,'scope':'NPC pixels only; exact union of old/new alpha coverage','assets':scopes,'auctioneerUnchanged':True,'frozenV05EnvironmentsUnchanged':True},indent=2)+'\n')
 for key in ['preservedAuctioneer','frozenLobby','frozenPortraitBackground']:check(sha(ROOT/m[key]['file'])==m[key]['sha256'],'Exact preservation: '+key)
 a=Image.open(ROOT/m['npcComparison']['file']);b=Image.open(ROOT/m['npcComparison4x']['file']);check(b.size==(a.width*4,a.height*4) and b.tobytes()==a.resize(b.size,Image.Resampling.NEAREST).tobytes(),'NPC comparison exact4x')
 class Links(HTMLParser):
  def handle_starttag(self,tag,attrs):
   for key,value in attrs:
    if key not in ['src','href','data-one','data-four'] or not value or value.startswith(('#','http:','https:')):continue
    p=(ROOT/value).resolve()
    if p==ROOT/'evidence/validation.json':continue
    check(p.is_relative_to(ROOT.parent) and p.is_file(),'Gallery dependency: '+value)
 Links().feed((ROOT/'index.html').read_text())
 protected=subprocess.check_output(['git','diff','--name-only',baseline['baseCommit'],'--','story','assets','docs','.github'],cwd=REPO,text=True).strip();check(not protected,'Canonical/production/narrative/gameplay/approval paths unchanged')
 report={'passed':True,'checksPassed':len(checks),'artworkApproved':False,'sourceDerived':True,'scopeProof':scopes,'earlierFilesPreserved':len(baseline['files']),'checks':checks}
 (ROOT/'evidence/validation.json').write_text(json.dumps(report,indent=2)+'\n');print(str(len(checks))+' v07 checks passed; zero changes outside NPC alpha.')

if __name__=='__main__':main()
