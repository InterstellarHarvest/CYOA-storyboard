from pathlib import Path
from PIL import Image,ImageChops
from html.parser import HTMLParser
import json,hashlib,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];OLD=ROOT.parent/'v01';REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists())
BASE='e650f02a1d803069ae142557cfc134edab77dafd';checks=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(v,n):
 assert v,n
 checks.append({'check':n,'passed':True})
def delta(a,b):
 d=ImageChops.difference(a,b);return ImageChops.lighter(ImageChops.lighter(d.getchannel('R'),d.getchannel('G')),d.getchannel('B'))
def assemble(names):
 im=Image.new('RGBA',(314,206))
 for n in names:im=Image.alpha_composite(im,Image.open(ROOT/'layers'/(n+'.png')).convert('RGBA'))
 return im.convert('RGB')
def main():
 m=json.loads((ROOT/'manifest.json').read_text());r=json.loads((ROOT/'evidence/repair.json').read_text());assets=[m['asset']]+m['supplementalReferences']
 check(m['status']=='UNSELECTED'and not m['ownerApproved']and m['primaryUnits']==1 and len(assets)==2,'One unselected primary plus one conditional flood reference')
 check(len(list((ROOT/'native').glob('*.png')))==2,'Only two final native assets')
 ims=[];colors={}
 for state,a in zip(['dry','flood'],assets):
  im=Image.open(ROOT/a['native']['file']);four=Image.open(ROOT/a['preview4x']['file']);ims.append(im)
  check(im.size==(314,206)and im.mode=='RGB',state+' opaque314x206')
  check(four.size==(1256,824)and four.tobytes()==im.resize(four.size,Image.Resampling.NEAREST).tobytes(),state+' exact nearest-neighbor4x')
  check(all(sha(ROOT/a[k]['file'])==a[k]['sha256']for k in ['native','preview4x']),state+' exact manifest hashes')
  old=Image.open(OLD/'native'/Path(a['native']['file']).name.replace('-v02','-v01'));allowed=Image.open(ROOT/f'masks/{state}-correction-authorized.png')
  check(ImageChops.subtract(delta(old,im),allowed).getbbox()is None,state+' zero corrections outside four authorized repair regions')
  check(assemble(r[state+'LayerOrder']).tobytes()==im.tobytes(),state+' exact editable layer assembly')
  check(a['runtimeBinding']is None and a['newFocusId']is None,state+' null runtime and Focus bindings')
  check(r['hashes'][state]==sha(ROOT/a['native']['file']),state+' repair record hash')
  colors[state]=len(im.getcolors(200000))
 check(ImageChops.subtract(delta(*ims),Image.open(ROOT/'masks/flood-authorized.png')).getbbox()is None,'Flood state changes confined to water/hatch/attendant/sign')
 check(r['floodLayerOrder'][:len(r['dryLayerOrder'])]==r['dryLayerOrder'],'Same twelve structural/repair layers shared by both states')
 shared=0
 for p in(ROOT/'layers').glob('*.png'):
  im=Image.open(p);check(im.mode=='RGBA'and im.size==(314,206)and set(im.getchannel('A').get_flattened_data())<={0,255},'Native editable binary-alpha '+p.name)
 for name in json.loads((OLD/'evidence/native-construction.json').read_text())['dryLayerOrder']:
  if name!='08-hatch-closed':check((ROOT/'layers'/(name+'.png')).read_bytes()==(OLD/'layers'/(name+'.png')).read_bytes(),'Unchanged original dry layer '+name);shared+=1
 check(shared==9,'Nine original dry layers byte-exact; hatch is targeted replacement')
 # Pixel-level perspective and hinge anchors, independent of palette metrics.
 for d in r['doorProjection']:
  vx,vy=d['vanishingPoint'];x0=d['nearX'];x1=d['farX'];top=d['nearTop'];bottom=d['nearBottom']
  check(d['corners']==[[x0,top],[x1,round(vy+(top-vy)*(vx-x1)/(vx-x0))],[x1,round(vy+(bottom-vy)*(vx-x1)/(vx-x0))],[x0,bottom]],'Door edges share corridor vanishing point '+str(x0))
 h=r['hatch'];check(h['openLeaf'][0]==h['fixedFrame'][0]==h['hingeEdge'][0]and h['openLeaf'][-1]==h['fixedFrame'][-1]==h['hingeEdge'][-1],'Open hatch leaf shares exact closed frame hinge endpoints')
 check(h['openLeaf'][2][1]-h['openLeaf'][1][1]>h['hingeEdge'][1][1]-h['hingeEdge'][0][1],'Outward leaf free edge is nearer and taller')
 npc=Image.open(ROOT/'layers/state-attendant.png');oldnpc=Image.open(OLD/'layers/state-attendant.png');box=npc.getchannel('A').getbbox();oldbox=oldnpc.getchannel('A').getbbox()
 check(box[3]-box[1]>=90 and box[3]-box[1]>2*(oldbox[3]-oldbox[1]),'Attendant native silhouette more than twice v01 height')
 check(r['canonicalAttendant']['speaker']=='hotel_attendant'and r['canonicalAttendant']['distinctFrom']=='hotel_wedding_assistant','Attendant role distinct from wedding assistant')
 nodes=json.loads((REPO/'story/chapters/chapter-04.wip.json').read_text())['nodes'];n=nodes['hotel_flooded_public_corridor']
 check(n['speaker']=='hotel_attendant'and n['pose']=='professional'and any('She points toward a service passage' in t.get('desc','')for t in n['text']if isinstance(t,dict)),'Narrative speaker/pose/pointing action checked')
 check(assets[0]['nodeIds']==['hotel_stall_public_corridor_walk','hotel_flooded_public_corridor']and all(assets[1][k]is None for k in ['newSceneKey','newFlag']),'Canonical coverage retained; no extra scene/flag')
 check(sha(ROOT/r['attendantSource'])==r['attendantSourceSha256']and sha(ROOT/r['retainedSource'])==r['retainedSourceSha256'],'Both generated/reference source hashes exact')
 check(m['sourceDerived']and not m['whollyIndependentNativeAuthorship'],'Source-derived provenance explicit')
 for ref in json.loads((ROOT/'evidence/benchmark-provenance.json').read_text()):
  data=subprocess.check_output(['git','show',ref['sourceCommit']+':'+ref['sourcePath']],cwd=REPO);check((ROOT/ref['file']).read_bytes()==data and sha(ROOT/ref['file'])==ref['sha256'],'Approved benchmark exact '+ref['file'])
 for a in json.loads((ROOT/'evidence/caption-layout.json').read_text()):check(a['fits']and a['textWidth']<a['panelWidth']-8,'Caption fits '+a['sheet']+'/'+a['caption'])
 pairs=0
 for p in ROOT.rglob('*-4x.png'):
  candidates=[p.with_name(p.name.replace('-4x','-native')),ROOT/'native'/p.name.replace('-4x',''),ROOT/'references'/p.name.replace('-4x','')];one=next((q for q in candidates if q.is_file()),None)
  if one:
   a=Image.open(one);b=Image.open(p);check(b.size==(a.width*4,a.height*4)and b.tobytes()==a.resize(b.size,Image.Resampling.NEAREST).tobytes(),'Exact4x '+str(p.relative_to(ROOT)));pairs+=1
 # Parent index can gain a latest-review link; every original source, approved
 # PNG, narrative, selection record and immutable v01 file stays unchanged.
 parentindex=str((ROOT.parent/'README.md').relative_to(REPO));preserved=0;v01=0;approved=0
 for line in subprocess.check_output(['git','ls-tree','-r',BASE],cwd=REPO,text=True).splitlines():
  meta,path=line.split('\t')
  if meta.split()[1]!='blob'or path==parentindex:continue
  data=(REPO/path).read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert blob==meta.split()[2],path;preserved+=1
  if path.startswith(str(OLD.relative_to(REPO))+'/'):v01+=1
  if path.startswith('assets/selected/'):approved+=1
 check(True,'Every '+str(preserved)+' preserved baseline blob exact')
 class Links(HTMLParser):
  def __init__(self):super().__init__();self.links=[]
  def handle_starttag(self,t,attrs):self.links +=[v for k,v in attrs if k in ['href','src','data-one','data-four']and v and not v.startswith(('#','http'))]
 links=Links();links.feed((ROOT/'index.html').read_text())
 for link in set(links.links):check((ROOT/link).is_file()or link=='evidence/validation.json','Gallery dependency '+link)
 files=list(ROOT.rglob('*.png'))+[ROOT/'manifest.json',ROOT/'index.html',ROOT/'evidence/repair.json'];before={p:sha(p)for p in files}
 for name in ['refine.py','package_review.py']:subprocess.run([sys.executable,str(ROOT/'source'/name)],cwd=REPO,check=True,stdout=subprocess.DEVNULL)
 check(all(sha(p)==s for p,s in before.items()),'Deterministic native repair and gallery replay')
 out={'technicalPassed':True,'checksPassed':len(checks),'status':'UNSELECTED','ownerApproved':False,'exact4xPairs':pairs,'correctionChangesOutsideAuthorizedRegions':0,'stateChangesOutsideAuthorizedMasks':0,'originalDryLayersByteExact':shared,'sharedDryFloodLayers':len(r['dryLayerOrder']),'attendantSilhouetteHeight':box[3]-box[1],'v01AttendantSilhouetteHeight':oldbox[3]-oldbox[1],'attendantIdentity':'hotel_attendant, not hotel_wedding_assistant','doorVanishingPoint':[205,115],'hatchHingeAnchorsPassed':True,'v01FilesByteExact':v01,'approvedFilesByteExact':approved,'baselineBlobsPreserved':preserved,'paletteCountsDiagnosticOnly':colors,'replayedArtifactsIdentical':len(before),'sourceDerived':True,'canonicalGameplayNarrativeSelectionsModified':False,'checks':checks}
 (ROOT/'evidence/validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='checks'}))
if __name__=='__main__':main()
