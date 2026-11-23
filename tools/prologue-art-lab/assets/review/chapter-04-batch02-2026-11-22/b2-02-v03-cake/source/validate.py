from pathlib import Path
from PIL import Image
from html.parser import HTMLParser
import hashlib,json,subprocess,os
ROOT=Path(__file__).resolve().parents[1];REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists());BASE='62ef2059585de49292bbec2742d3c637d2eae818';OLD=ROOT.parent/'b2-02-v02-pixel'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 checks=[]
 def check(v,label):
  assert v,label
  checks.append({'check':label,'passed':True})
 m=json.loads((ROOT/'manifest.json').read_text());report=json.loads((ROOT/'evidence/targeted-change.json').read_text());base=Image.open(OLD/'native/CH4-B2-09-v02.png').convert('RGB');new=Image.open(ROOT/m['native']['file']);mask=Image.open(ROOT/'masks/cake-and-trolley-protected.png');hand=Image.open(ROOT/'masks/foreground-hand-preserved.png')
 check(m['assetId']=='CH4-B2-09'and m['status']=='UNSELECTED'and not m['formalApprovalRegistered'],'Only B2-09 revised, unselected')
 check(new.size==(314,206)and new.mode=='RGB','Native opaque314x206');check(sha(ROOT/m['native']['file'])==m['native']['sha256'],'Final native SHA256')
 four=Image.open(ROOT/m['preview4x']['file']);check(four.size==(1256,824)and four.tobytes()==new.resize(four.size,Image.Resampling.NEAREST).tobytes(),'Exact4x nearest preview')
 diff=[(i%314,i//314)for i,(a,b)in enumerate(zip(base.get_flattened_data(),new.get_flattened_data()))if a!=b];check(len(diff)==report['changedPixels']==723,'Exact723-pixel targeted change');check(all(mask.getpixel(p)==255 for p in diff),'Zero changes outside protected cake/trolley silhouette');check(all(base.getpixel((x,y))==new.getpixel((x,y))for y in range(206)for x in range(314)if hand.getpixel((x,y))),'Foreground hand unchanged')
 check(set(base.get_flattened_data())==set(new.get_flattened_data()),'Exact existing64-color scene palette retained')
 structure=Image.open(OLD/'layers/CH4-B2-09-native-structure.png').convert('RGBA');safe=Image.open(ROOT/'layers/native-structure-object-safe.png');paint=Image.open(ROOT/'layers/native-cake-and-trolley.png');under=Image.open(OLD/'layers/CH4-B2-09-material-underpainting.png').convert('RGBA')
 check(all(safe.getpixel((x,y))[3]==0 for y in range(206)for x in range(314)if mask.getpixel((x,y))),'Structural paint excluded from complete story object')
 check(all(safe.getpixel((x,y))==structure.getpixel((x,y))for y in range(206)for x in range(314)if not mask.getpixel((x,y))),'Structural layer exact outside story-object mask')
 check(Image.alpha_composite(Image.alpha_composite(under,safe),paint).convert('RGB').tobytes()==new.tobytes(),'Exact final composition from protected native layers')
 # These semantic anchor regions supplement, never replace, native visual review.
 for name,p in [('bouquet',(161,92)),('upper tier',(163,98)),('middle tier',(163,105)),('base tier',(164,116)),('near caster',(161,138)),('far caster',(180,135))]:check(mask.getpixel(p)==255 and paint.getpixel(p)[3]==255,'Protected/readable native object anchor '+name)
 frozen=json.loads((ROOT/'evidence/frozen-siblings.json').read_text())
 for a in frozen['assets']:
  for key in['native','preview4x']:check(sha(ROOT/a[key]['file'])==a[key]['sha256'],'Exact frozen sibling '+a['id']+' '+key)
  check(a['status']=='UNSELECTED','Selection-ready assessment is not approval '+a['id'])
 roots=['tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21','tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22','story','assets/selected','.github','docs'];preserved=0
 for rel in subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,*roots],cwd=REPO,text=True).splitlines():
  if rel.startswith(roots[1]+'/')and Path(rel).relative_to(roots[1]).parts[0]not in['v01','b2-02-v01','v02-npc-palette','b2-02-v02-pixel']:continue
  check((REPO/rel).read_bytes()==subprocess.check_output(['git','show',BASE+':'+rel],cwd=REPO),'Previous/canonical file exact '+rel);preserved+=1
 class Links(HTMLParser):
  def handle_starttag(self,t,attrs):
   for k,v in attrs:
    if v=='evidence/validation.json':continue
    if k in['href','src','data-one','data-four']and v and not v.startswith(('https:','http:','#','data:')):check((ROOT/v).is_file(),'Gallery dependency '+v)
 Links().feed((ROOT/'index.html').read_text())
 files=[p for n in['native','previews','layers','masks','comparisons']for p in(ROOT/n).glob('*.png')]+[ROOT/'manifest.json',ROOT/'index.html'];before={str(p.relative_to(ROOT)):sha(p)for p in files}
 for script in['restore.py','package.py']:subprocess.run(['python3',str(ROOT/'source'/script)],env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),check=True,stdout=subprocess.DEVNULL)
 check(all(sha(ROOT/p)==h for p,h in before.items()),'Exact deterministic targeted edit/gallery replay')
 result={'passed':True,'checksPassed':len(checks),'revisedAsset':'CH4-B2-09','changedPixels':len(diff),'outsideProtectedObjectChanges':0,'otherThreeScenesUnchanged':True,'paletteUnchanged':True,'approvedAndHistoricalFilesPreserved':preserved,'replayFilesIdentical':len(before),'artworkApproved':False,'status':'UNSELECTED','checks':checks};(ROOT/'evidence/validation.json').write_text(json.dumps(result,indent=2)+'\n');print(str(len(checks))+' checks passed; only723 cake/trolley pixels change.')
if __name__=='__main__':main()
