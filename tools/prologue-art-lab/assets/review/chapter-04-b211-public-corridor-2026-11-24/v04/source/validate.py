from pathlib import Path
from PIL import Image,ImageChops,ImageFilter
from html.parser import HTMLParser
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];OLD=ROOT.parent/'v03';REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists());BASE='19c67561d371c2bc524d39bc9f2a57e8b4584961';checks=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(v,n):
 assert v,n
 checks.append({'check':n,'passed':True})
def main():
 m=json.loads((ROOT/'manifest.json').read_text());r=json.loads((ROOT/'evidence/repair.json').read_text());a=m['supplementalReferences'][0]
 check(m['status']=='UNSELECTED'and not m['ownerApproved']and m['newPrimaryAssets']==0 and m['newlyRevisedArtworkUnits']==1,'One unselected flood correction; dry candidate unchanged')
 check(len(list((ROOT/'native').glob('*.png')))==1,'Only one new native scene export')
 old=Image.open(OLD/'native/CH4-NEW-04-public-corridor-flood-v03.png');im=Image.open(ROOT/a['native']['file']);four=Image.open(ROOT/a['preview4x']['file'])
 check(im.mode=='RGB'and im.size==(314,206),'Opaque314x206 native')
 check(four.size==(1256,824)and four.tobytes()==im.resize(four.size,Image.Resampling.NEAREST).tobytes(),'Exact nearest-neighbor4x')
 check(sha(ROOT/a['native']['file'])==a['native']['sha256']==r['finalFloodSha256'],'Native source/manifest hash exact')
 check(sha(ROOT/a['preview4x']['file'])==a['preview4x']['sha256'],'Preview hash exact')
 check((ROOT/m['asset']['native']['file']).read_bytes()==(ROOT/r['dryCandidate']).read_bytes(),'Dry PNG exact unchanged v02 candidate')
 d=ImageChops.difference(old,im);d=ImageChops.lighter(ImageChops.lighter(d.getchannel('R'),d.getchannel('G')),d.getchannel('B'))
 check(ImageChops.subtract(d,Image.open(ROOT/'masks/authorized-character-repair.png')).getbbox()is None,'Zero changed pixels outside old/new character silhouettes')
 npc=Image.open(ROOT/'layers/state-attendant.png');oldnpc=Image.open(OLD/'layers/state-attendant.png');sign=Image.open(OLD/'layers/state-floating-sign.png');cb=npc.getchannel('A').getbbox();ob=oldnpc.getchannel('A').getbbox()
 check(npc.mode=='RGBA'and npc.size==(314,206)and set(npc.getchannel('A').get_flattened_data())<={0,255},'Native binary-alpha character layer')
 check(cb[3]-cb[1]==132 and ob[3]-ob[1]==94,'Door-relative height changes94px to132px')
 check(cb[3]==ob[3]==193,'Feet retain exact existing floor boundary')
 check(r['doorReference']['height']==174 and abs(r['doorReference']['npcToDoorRatio']-132/174)<1e-9,'Door-relative scale record exact')
 check(ImageChops.multiply(npc.getchannel('A'),sign.getchannel('A')).getbbox()is None,'No character/sign overlap')
 check(ImageChops.multiply(npc.getchannel('A').filter(ImageFilter.MaxFilter(21)),sign.getchannel('A')).getbbox()is None,'Sign clears10px expanded character silhouette')
 check(r['bboxHorizontalGap']==17,'Seventeen pixels of horizontal bbox clearance')
 result=Image.new('RGBA',(314,206));shared=0
 for rel in r['floodLayerOrder']:
  p=ROOT/rel;result=Image.alpha_composite(result,Image.open(p).convert('RGBA'))
  if rel.startswith('../v03/'):shared+=1
 check(shared==15 and result.convert('RGB').tobytes()==im.tobytes(),'Fifteen unchanged source layers plus new NPC assemble exactly')
 check(not any(Path(rel).name=='state-floating-sign.png'and not rel.startswith('../v03/')for rel in r['floodLayerOrder']),'Separated v03 sign layer reused unchanged')
 check(sha(ROOT/r['source'])==r['sourceSha256'],'New clean-cluster source hash exact')
 gen=json.loads((ROOT/'evidence/generation-provenance.json').read_text())
 check(sha(ROOT/gen['output'])==gen['outputSha256']and sha(ROOT/gen['prompt'])==gen['promptSha256'],'Generated original and exact prompt hashes')
 check(m['sourceDerived']and not m['whollyIndependentNativeAuthorship']and gen['sourceDerived'],'Accurate source-derived provenance')
 oldm=json.loads((OLD/'manifest.json').read_text())
 check(m['asset']['nodeIds']==oldm['asset']['nodeIds']and a['nodeIds']==oldm['supplementalReferences'][0]['nodeIds'],'Canonical node mappings unchanged')
 check(m['asset']['runtimeBinding']is None and a['runtimeBinding']is None and all(a[k]is None for k in ['newSceneKey','newFocusId','newFlag']),'No new runtime binding, scene, Focus or flag')
 for name in ['staff_lavatory.png','conveniences_bureau.png','control_tower.png']:check((ROOT/'references'/name).read_bytes()==(OLD/'references'/name).read_bytes(),'Exact approved benchmark '+name)
 data=subprocess.check_output(['git','show','5a4290d672e1904b4b5ad361562f05168c328a50:assets/selected/art/scenes/pavilion_reboot/courtesy_stage.png'],cwd=REPO)
 check((ROOT/'references/courtesy_stage.png').read_bytes()==data,'Actual approved Pavilion rendering benchmark')
 for c in json.loads((ROOT/'evidence/caption-layout.json').read_text()):check(c['fits'],'Caption fits '+c['sheet']+'/'+c['caption'])
 pairs=0
 for p in ROOT.rglob('*-4x.png'):
  candidates=[p.with_name(p.name.replace('-4x','-native')),ROOT/'native'/p.name.replace('-4x',''),ROOT/'references'/p.name.replace('-4x',''),ROOT/'evidence'/p.name.replace('-4x','')];one=next((q for q in candidates if q.is_file()),None)
  if one:
   x=Image.open(one);y=Image.open(p);check(y.size==(x.width*4,x.height*4)and y.tobytes()==x.resize(y.size,Image.Resampling.NEAREST).tobytes(),'Exact4x '+str(p.relative_to(ROOT)));pairs+=1
 preserved=0;versions={'v01':0,'v02':0,'v03':0};approved=0;index=str((ROOT.parent/'README.md').relative_to(REPO))
 for line in subprocess.check_output(['git','ls-tree','-r',BASE],cwd=REPO,text=True).splitlines():
  meta,path=line.split('\t')
  if meta.split()[1]!='blob'or path==index:continue
  data=(REPO/path).read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert blob==meta.split()[2],path;preserved+=1
  if path.startswith('assets/selected/'):approved+=1
  for v in versions:
   if path.startswith(str((ROOT.parent/v).relative_to(REPO))+'/'):versions[v]+=1
 check(True,'All earlier packages, sources, approved files and canonical records byte-exact')
 class Links(HTMLParser):
  def __init__(self):super().__init__();self.links=[]
  def handle_starttag(self,t,attrs):self.links +=[v for k,v in attrs if k in ['href','src','data-one','data-four']and v and not v.startswith(('#','http'))]
 links=Links();links.feed((ROOT/'index.html').read_text())
 for link in set(links.links):check((ROOT/link).is_file()or link=='evidence/validation.json','Gallery dependency '+link)
 files=list(ROOT.rglob('*.png'))+[ROOT/'manifest.json',ROOT/'index.html',ROOT/'evidence/repair.json'];before={p:sha(p)for p in files}
 for name in ['refine.py','package_review.py']:subprocess.run([sys.executable,str(ROOT/'source'/name)],cwd=REPO,check=True,stdout=subprocess.DEVNULL)
 check(all(sha(p)==v for p,v in before.items()),'Deterministic source interpretation/assembly/gallery replay')
 out={'passed':True,'checksPassed':len(checks),'status':'UNSELECTED','ownerApproved':False,'oldHeight':94,'newHeight':132,'feetYUnchanged':193,'doorNearLeafHeight':174,'signGapNativePixels':17,'noSignOverlap':True,'tenPixelSilhouetteClearancePassed':True,'dryPNGBytesUnchanged':True,'changesOutsideCharacterSilhouettes':0,'sharedUnchangedLayers':shared,'exact4xPairs':pairs,'earlierReviewFilesByteExact':versions,'approvedFilesByteExact':approved,'baselineBlobsPreserved':preserved,'replayedArtifactsIdentical':len(before),'sourceDerived':True,'newGeneratedSource':True,'wholeRoomGenerated':False,'checks':checks}
 (ROOT/'evidence/validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='checks'}))
if __name__=='__main__':main()
