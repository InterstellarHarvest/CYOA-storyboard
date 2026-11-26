from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1];REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists());BASE='a944f9aeff110ddc66301840c2d415f1ba9bc357'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 checks=[]
 def check(label,ok,**details):
  assert ok,(label,details);checks.append({'check':label,'passed':True,**details})
 m=json.loads((ROOT/'manifest.json').read_text());layout=json.loads((ROOT/'evidence/layout.json').read_text());allowed=Image.open(ROOT/'masks/authorized-crt-content.png')
 check('Exactly two unselected INSPECT alternatives',len(m['newAssets'])==2 and m['newArtworkStatus']=='UNSELECTED'and not m['ownerApproved'])
 palette_counts={}
 for a,l in zip(m['newAssets'],layout):
  before=Image.open(ROOT/a['source']);after=Image.open(ROOT/a['file']);patch=Image.open(ROOT/a['patch']);actual=Image.open(ROOT/a['actualChangeMask'])
  check(a['state']+'565x451 opaque RGB',after.size==(565,451)and after.mode=='RGB')
  check(a['state']+' hashes',sha(ROOT/a['file'])==a['sha256']and sha(ROOT/a['source'])==a['sourceSha256']and sha(ROOT/a['patch'])==a['patchSha256'])
  check(a['state']+' exact source palette',set(before.get_flattened_data())==set(after.get_flattened_data()))
  palette_counts[a['state']]=len(set(after.get_flattened_data()))
  check(a['state']+' exact native patch replay',ImageChops.difference(Image.alpha_composite(before.convert('RGBA'),patch).convert('RGB'),after).getbbox()is None)
  check(a['state']+' binary native alpha',patch.size==after.size and patch.mode=='RGBA'and set(patch.getchannel('A').get_flattened_data())<={0,255})
  d=ImageChops.difference(before,after);real=ImageChops.lighter(ImageChops.lighter(d.getchannel('R'),d.getchannel('G')),d.getchannel('B')).point(lambda p:255 if p else 0)
  check(a['state']+' actual mask exact',ImageChops.difference(real,actual).getbbox()is None)
  check(a['state']+' ZERO surrounding/CRT-style/light changes',ImageChops.multiply(real,ImageChops.invert(allowed)).getbbox()is None and a['outsideAuthorizedPixels']==0,changedPixels=a['changedPixels'])
  check(a['state']+' clear separate icon row',l['clearRowsBelowText']>=8 and l['iconInkBounds'][1]>=l['iconZone'][1]and l['iconInkBounds'][3]<=l['iconZone'][3],clearRows=l['clearRowsBelowText'])
  check(a['state']+' centered text',all((b[0]+b[2])/2==355 for b in l['textLineInkBounds']))
  check(a['state']+' no approval/runtime binding',not a['ownerApproved']and a['runtimeBinding']is None)
  for when,im in [('before',before),('after',after)]:
   crop=Image.open(ROOT/f'closeups/{a["state"]}-{when}-crt-native.png');check(a['state']+' exact unscaled '+when+' crop',crop.size==(176,99)and ImageChops.difference(crop,im.crop(tuple(m['closeupCropBoxExclusive']))).getbbox()is None)
 check('Identical layout boxes and body anchor across states',all(layout[0][k]==layout[1][k]for k in ['textBox','textHorizontalCenter','textNativeScale','lineGap','iconZone','iconBody','iconBodyCenterX','newTextFirstRowY','newSecondLineLastRowY']))
 for p in(ROOT/'previews').glob('*-4x.png'):
  name=p.name[:-7]+'.png';sources=[d/name for d in[ROOT/'native',ROOT/'references',ROOT/'closeups',ROOT/'comparisons']if(d/name).is_file()];check(p.name+' native source exists',len(sources)==1)
  im=Image.open(sources[0]);four=Image.open(p);check(p.name+' exact nearest4x',four.size==(im.width*4,im.height*4)and ImageChops.difference(four,im.resize(four.size,Image.Resampling.NEAREST)).getbbox()is None)
 for r in m['unchangedApprovedReferences']:
  data=subprocess.check_output(['git','show',r['sourceCommit']+':'+r['sourcePath']],cwd=REPO);check(r['file']+' APPROVED / immutable source bytes',hashlib.sha256(data).hexdigest()==r['sha256']==sha(ROOT/r['file'])and data==(ROOT/r['file']).read_bytes()and r['status']=='APPROVED')
 count=0;selected=0
 for line in subprocess.check_output(['git','ls-tree','-r',BASE],cwd=REPO,text=True).splitlines():
  meta,name=line.split('\t',1);mode,kind,digest=meta.split()
  if kind!='blob':continue
  data=(REPO/name).read_bytes();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==digest,name;count+=1;selected+=int(name.startswith('assets/selected/'))
 check('Entire baseline unchanged: v01, approved v02, all history and canonical files',True,baselineFiles=count,selectedFiles=selected)
 check('Honest original source-derived provenance / no new generation',m['sourceDerived']and not m['whollyIndependentNativeAuthorship']and not m['newImageGeneration'])
 check('Correct isolated review branch',subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()==m['branch'])
 report={'passed':True,'newCandidates':'UNSELECTED','artisticApproval':False,'paletteCounts':palette_counts,'allSurroundingPixelsExact':True,'approvedV01AndV02Exact':True,'checks':checks}
 (ROOT/'evidence/validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':True,'checks':len(checks),'palettes':palette_counts,'baselineFiles':count,'surroundingPixelsChanged':0}))
if __name__=='__main__':main()
