from pathlib import Path
from PIL import Image
from html.parser import HTMLParser
import json,hashlib,subprocess,os
ROOT=Path(__file__).resolve().parents[1];OLD=ROOT.parent/'b2-05-v01';REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists());BASE='9afe76fe17dcb02633b82261a6c69457891da50f'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 checks=[]
 def check(v,label):
  assert v,label
  checks.append({'check':label,'passed':True})
 m=json.loads((ROOT/'manifest.json').read_text());report=json.loads((ROOT/'evidence/targeted-change.json').read_text());check(len(m['assets'])==4 and m['status']=='UNSELECTED','Exactly four unselected bride hair/iris color revisions');cores={26:(253,70,294,108),28:(258,70,308,111),29:(269,70,318,111),30:(233,70,280,110)}
 for a in m['assets']:
  id_=a['id'];n=int(id_.split('-')[-1]);old=Image.open(OLD/f'native/{id_}-v01.png');new=Image.open(ROOT/a['native']['file']);mask=Image.open(ROOT/a['allowedMask']);r=next(x for x in report['assets']if x['id']==id_);check(new.size==(564,278)and new.mode=='RGBA',id_+' native564x278 RGBA');check(sha(ROOT/a['native']['file'])==a['native']['sha256']==r['finalSha256'],id_+' final hash');check(sha(OLD/f'native/{id_}-v01.png')==r['baseSha256'],id_+' exact pinned v01 base');check(new.getchannel('A').tobytes()==old.getchannel('A').tobytes(),id_+' exact original alpha/silhouette')
  diff=[i for i,(x,y)in enumerate(zip(old.get_flattened_data(),new.get_flattened_data()))if x!=y];check(len(diff)==r['changedPixelsTotal'],id_+' exact changed-pixel count');check(all(mask.getpixel((i%564,i//564))for i in diff),id_+' zero changes outside native hair-and-iris masks');iris=Image.open(ROOT/a['irisMask']);box=cores[n];check(all(old.getpixel((x,y))==new.getpixel((x,y))for y in range(box[1],box[3])for x in range(box[0],box[2])if not iris.getpixel((x,y))),id_+' facial features/eyebrows exact except requested iris colors');check(sum(bool(v)for v in iris.get_flattened_data())==r['changedIrisPixels']>0,id_+' explicit green iris pixel count');check(all(old.getpixel((i%564,i//564))==new.getpixel((i%564,i//564))for i,pix in enumerate(old.get_flattened_data())if max(pix[:3])<=55 or min(pix[:3])>=175),id_+' all dark pupil pixels and white/catchlight pixels unchanged');check(old.crop(tuple(r['preservedEarBox'])).tobytes()==new.crop(tuple(r['preservedEarBox'])).tobytes(),id_+' complete ear/earring unchanged');check(old.crop((0,123,564,278)).tobytes()==new.crop((0,123,564,278)).tobytes(),id_+' neck/lower veil/gown/hands/props unchanged')
  layer=Image.open(ROOT/a['hairLayer']);eyelayer=Image.open(ROOT/a['irisLayer']);check(Image.alpha_composite(Image.alpha_composite(old,layer),eyelayer).tobytes()==new.tobytes(),id_+' exact original plus blonde hair and green iris layers');four=Image.open(ROOT/a['preview4x']['file']);check(four.size==(2256,1112)and four.tobytes()==new.resize(four.size,Image.Resampling.NEAREST).tobytes(),id_+' exact nearest4x');check(sha(ROOT/a['preview4x']['file'])==a['preview4x']['sha256'],id_+' preview hash');bg=Image.open(ROOT/'references/approved-lobby-background.png').convert('RGBA');check(Image.alpha_composite(bg,new).convert('RGB').tobytes()==Image.open(ROOT/a['composite']['file']).tobytes(),id_+' exact approved-background composite')
  check(a['status']=='UNSELECTED'and not a['selected']and a['sourceDerived'],id_+' pending owner selection/honest provenance')
 for name in ['approved-groom','approved-groundskeeper','approved-presenter','approved-lobby-background']:
  check((ROOT/f'references/{name}.png').read_bytes()==(OLD/f'references/{name}.png').read_bytes(),'Exact unchanged approved reference '+name)
 check((ROOT/'references/CH4-B2-27-v01.png').read_bytes()==(OLD/'native/CH4-B2-27-v01.png').read_bytes(),'Clerk retained byte-exact v01, not revised or selected')
 # Git's content comparison includes working-tree bytes, not only the index.
 protected=['story','assets/selected','docs','.github','tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21']
 protected +=[str(p.relative_to(REPO))for p in ROOT.parent.iterdir()if p.is_dir()and p!=ROOT and p.name!='b2-05-v02-hair']
 check(not subprocess.check_output(['git','diff','--name-only',BASE,'--',*protected],cwd=REPO,text=True),'Every prior version, approval, story/gameplay/workflow file unchanged')
 archive='tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/b2-05-v02-hair'
 for path in subprocess.check_output(['git','ls-tree','-r','--name-only','97ccd2b8a0943374453c7a4a56af1868cb559c3f',archive],cwd=REPO,text=True).splitlines():
  check((REPO/path).read_bytes()==subprocess.check_output(['git','show','97ccd2b8a0943374453c7a4a56af1868cb559c3f:'+path],cwd=REPO),'Exact preserved first hair-only study '+path)
 class Links(HTMLParser):
  def handle_starttag(self,t,attrs):
   for k,v in attrs:
    if v=='evidence/validation.json':continue
    if k in ['href','src','data-one','data-four']and v and not v.startswith(('https:','http:','#','data:')):check((ROOT/v).is_file(),'Gallery dependency '+v)
 Links().feed((ROOT/'index.html').read_text())
 outputs=[p for d in ['native','previews','layers','masks','comparisons']for p in(ROOT/d).glob('*.png')]+[ROOT/'manifest.json',ROOT/'index.html'];before={str(p.relative_to(ROOT)):sha(p)for p in outputs}
 for script in ['recolor.py','package.py']:subprocess.run(['python3',str(ROOT/'source'/script)],cwd=REPO,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),check=True,stdout=subprocess.DEVNULL)
 check(all(sha(ROOT/p)==h for p,h in before.items()),'Byte-identical deterministic hair edit/gallery replay')
 result={'passed':True,'checksPassed':len(checks),'status':'UNSELECTED','revisedBridePoses':4,'changedHairPixels':sum(a['changedHairPixels']for a in report['assets']),'changedIrisPixels':sum(a['changedIrisPixels']for a in report['assets']),'outsideHairAndIrisMaskChanges':0,'faceExceptIrisAndEarChecksPassed':True,'allOriginalAlphaUnchanged':True,'clerkAndGroomUnchanged':True,'priorApprovalsAndReviewsUnchanged':True,'replayFilesIdentical':len(before),'integrationPerformed':False,'checks':checks};(ROOT/'evidence/validation.json').write_text(json.dumps(result,indent=2)+'\n');print(str(len(checks))+' checks passed; four hair/iris color revisions, all other pixels unchanged.')
if __name__=='__main__':main()
