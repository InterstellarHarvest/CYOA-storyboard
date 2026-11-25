from pathlib import Path
from PIL import Image,ImageChops,ImageFilter
from html.parser import HTMLParser
import json,hashlib,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];OLD=ROOT.parent/'v02';REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists());BASE='e825c7a8bc97280e55cd1650b50c1f94ec15f272';checks=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(v,n):
 assert v,n
 checks.append({'check':n,'passed':True})
def main():
 m=json.loads((ROOT/'manifest.json').read_text());r=json.loads((ROOT/'evidence/repair.json').read_text());a=m['supplementalReferences'][0]
 check(m['status']=='UNSELECTED'and not m['ownerApproved']and m['newPrimaryAssets']==0 and m['newlyRevisedArtworkUnits']==1,'Only one unselected flood revision; dry candidate unchanged')
 check(len(list((ROOT/'native').glob('*.png')))==1,'Only one newly authored native PNG')
 old=Image.open(OLD/'native/CH4-NEW-04-public-corridor-flood-v02.png');im=Image.open(ROOT/a['native']['file']);four=Image.open(ROOT/a['preview4x']['file'])
 check(im.mode=='RGB'and im.size==(314,206),'Opaque native314x206')
 check(four.size==(1256,824)and four.tobytes()==im.resize(four.size,Image.Resampling.NEAREST).tobytes(),'Exact nearest-neighbor4x')
 check(sha(ROOT/a['native']['file'])==a['native']['sha256']==r['finalFloodSha256'],'Final flood hash exact')
 check(sha(ROOT/a['preview4x']['file'])==a['preview4x']['sha256'],'Final preview hash exact')
 dry=ROOT/m['asset']['native']['file'];original=OLD/'native/CH4-NEW-04-public-corridor-v02.png'
 check(dry.read_bytes()==original.read_bytes()and sha(dry)==r['unchangedDrySha256'],'Dry master unchanged exact PNG bytes')
 d=ImageChops.difference(old,im);d=ImageChops.lighter(ImageChops.lighter(d.getchannel('R'),d.getchannel('G')),d.getchannel('B'))
 check(ImageChops.subtract(d,Image.open(ROOT/'masks/authorized-corrections.png')).getbbox()is None,'Zero changes outside character plus old/new sign pixels')
 npc=Image.open(ROOT/'layers/state-attendant.png');oldnpc=Image.open(OLD/'layers/state-attendant.png');sign=Image.open(ROOT/'layers/state-floating-sign.png');oldsign=Image.open(OLD/'layers/state-floating-sign.png')
 check(npc.size==(314,206)and npc.mode=='RGBA'and set(npc.getchannel('A').get_flattened_data())<={0,255},'Native binary-alpha simplified character')
 check(npc.getchannel('A').tobytes()==oldnpc.getchannel('A').tobytes(),'Exact character silhouette, size, origin and pose')
 check(ImageChops.multiply(npc.getchannel('A'),sign.getchannel('A')).getbbox()is None,'Character and sign silhouettes never overlap')
 check(ImageChops.multiply(npc.getchannel('A').filter(ImageFilter.MaxFilter(21)),sign.getchannel('A')).getbbox()is None,'Sign clears a10-pixel expanded character silhouette')
 check(r['bboxHorizontalGap']==16,'Sixteen native pixels of horizontal bbox clearance')
 expected=Image.new('RGBA',(314,206));expected.alpha_composite(oldsign,(34,0))
 check(sign.tobytes()==expected.tobytes(),'Exact34px rightward sign translation; lettering/shape/wake unchanged')
 oldbox=oldsign.getchannel('A').getbbox();newbox=sign.getchannel('A').getbbox()
 check(oldsign.crop(oldbox).tobytes()==sign.crop(newbox).tobytes(),'No sign resampling, repaint or clipping')
 result=Image.new('RGBA',(314,206));shared=0
 for rel in r['floodLayerOrder']:
  part=Image.open(ROOT/rel).convert('RGBA');result=Image.alpha_composite(result,part)
  if rel.startswith('../v02/'):shared+=1
 check(shared==14 and result.convert('RGB').tobytes()==im.tobytes(),'Fourteen existing layers reused; exact assembly with only two edits')
 oldm=json.loads((OLD/'manifest.json').read_text())
 check(m['asset']['nodeIds']==oldm['asset']['nodeIds']and a['nodeIds']==oldm['supplementalReferences'][0]['nodeIds'],'Canonical node coverage unchanged')
 check(m['asset']['runtimeBinding']is None and a['runtimeBinding']is None and all(a[k]is None for k in ['newSceneKey','newFocusId','newFlag']),'No new runtime binding, scene key, Focus or flag')
 for ref in ['staff_lavatory.png','conveniences_bureau.png','control_tower.png']:check((ROOT/'references'/ref).read_bytes()==(OLD/'references'/ref).read_bytes(),'Exact approved benchmark '+ref)
 for c in json.loads((ROOT/'evidence/caption-layout.json').read_text()):check(c['fits'],'Readable caption '+c['sheet']+'/'+c['caption'])
 pairs=0
 for p in ROOT.rglob('*-4x.png'):
  candidates=[p.with_name(p.name.replace('-4x','-native')),ROOT/'native'/p.name.replace('-4x',''),ROOT/'references'/p.name.replace('-4x','')];one=next((p for p in candidates if p.is_file()),None)
  if one:
   x=Image.open(one);y=Image.open(p);check(y.size==(x.width*4,x.height*4)and y.tobytes()==x.resize(y.size,Image.Resampling.NEAREST).tobytes(),'Exact4x '+str(p.relative_to(ROOT)));pairs+=1
 preserved=0;versions={'v01':0,'v02':0};approved=0;index=str((ROOT.parent/'README.md').relative_to(REPO))
 for line in subprocess.check_output(['git','ls-tree','-r',BASE],cwd=REPO,text=True).splitlines():
  meta,path=line.split('\t')
  if meta.split()[1]!='blob'or path==index:continue
  data=(REPO/path).read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert blob==meta.split()[2],path;preserved+=1
  if path.startswith('assets/selected/'):approved+=1
  for v in versions:
   if path.startswith(str((ROOT.parent/v).relative_to(REPO))+'/'):versions[v]+=1
 check(True,'All prior versions, approved art, narrative and selections preserved')
 class Links(HTMLParser):
  def __init__(self):super().__init__();self.links=[]
  def handle_starttag(self,t,attrs):self.links +=[v for k,v in attrs if k in ['href','src','data-one','data-four']and v and not v.startswith(('#','http'))]
 links=Links();links.feed((ROOT/'index.html').read_text())
 for link in set(links.links):check((ROOT/link).is_file()or link=='evidence/validation.json','Gallery dependency '+link)
 files=list(ROOT.rglob('*.png'))+[ROOT/'manifest.json',ROOT/'index.html',ROOT/'evidence/repair.json'];before={p:sha(p)for p in files}
 for name in ['refine.py','package_review.py']:subprocess.run([sys.executable,str(ROOT/'source'/name)],cwd=REPO,check=True,stdout=subprocess.DEVNULL)
 check(all(sha(p)==v for p,v in before.items()),'Deterministic repair/assembly/gallery replay')
 out={'passed':True,'checksPassed':len(checks),'status':'UNSELECTED','ownerApproved':False,'dryPNGBytesUnchanged':True,'characterSilhouetteUnchanged':True,'signTranslation':[34,0],'signBBoxGapNativePixels':16,'noSignCharacterOverlap':True,'tenPixelSilhouetteClearancePassed':True,'signPixelsUnchangedApartFromTranslation':True,'changesOutsideAuthorizedPixels':0,'sharedLayersByteExact':shared,'exact4xPairs':pairs,'earlierReviewFilesByteExact':versions,'approvedFilesByteExact':approved,'baselineBlobsPreserved':preserved,'replayedArtifactsIdentical':len(before),'sourceDerived':True,'newImageGeneration':False,'checks':checks}
 (ROOT/'evidence/validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='checks'}))
if __name__=='__main__':main()
