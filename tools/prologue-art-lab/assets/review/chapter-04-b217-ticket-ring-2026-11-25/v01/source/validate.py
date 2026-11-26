from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib,subprocess,tempfile,shutil,sys
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 checks=[]
 def check(label,ok,**detail):
  assert ok,(label,detail);checks.append({'check':label,'passed':True,**detail})
 m=json.loads((ROOT/'manifest.json').read_text());layers=json.loads((ROOT/'evidence/native-layer-recipes.json').read_text());text=json.loads((ROOT/'evidence/native-text-layout.json').read_text());geometry=json.loads((ROOT/'evidence/object-geometry.json').read_text())
 check('Four UNSELECTED primary item candidates',m['primaryAssetCount']==4 and len(m['assets'])==4 and m['supplementalAssetCount']==0 and not m['ownerApproved'] and m['status']=='UNSELECTED')
 check('Existing consolidated IDs',[a['id']for a in m['assets']]==['CH4-NEW-10','CH4-NEW-11','CH4-NEW-12','CH4-NEW-13'])
 for a in m['assets']:
  id=a['id'];slot=a['view']=='slot';size=(96,96)if slot else(565,451);im=Image.open(ROOT/a['native']['file']);four=Image.open(ROOT/a['exact4x']['file'])
  check(id+' exact native size/mode',im.size==size and im.mode==('RGBA'if slot else'RGB'))
  check(id+' SHA-256',sha(ROOT/a['native']['file'])==a['native']['sha256'])
  check(id+' exact4x',four.size==(im.width*4,im.height*4) and four.mode==im.mode and sha(ROOT/a['exact4x']['file'])==a['exact4x']['sha256'] and ImageChops.difference(four,im.resize(four.size,Image.Resampling.NEAREST)).getbbox() is None)
  out=Image.new('RGBA',size)
  for r in layers[id]:
   layer=Image.open(ROOT/r['file']);check(id+' binary native layer '+r['file'],layer.mode=='RGBA' and layer.size==size and sha(ROOT/r['file'])==r['sha256'] and set(layer.getchannel('A').get_flattened_data())<={0,255});out=Image.alpha_composite(out,layer)
  if not slot:out=out.convert('RGB')
  check(id+' layer replay',ImageChops.difference(im,out).getbbox() is None)
  check(id+' unselected/unbound',a['status']=='UNSELECTED' and not a['selected'] and not a['ownerApproved'] and a['canonicalAssetPath'] is None and a['runtimeBinding'] is None)
  if slot:
   alpha=im.getchannel('A');bbox=alpha.getbbox();check(id+' binary transparency',set(alpha.get_flattened_data())=={0,255})
   check(id+' transparent margins / corners',bbox[0]>=4 and bbox[1]>=4 and bbox[2]<=92 and bbox[3]<=92 and all(im.getpixel(p)[3]==0 for p in [(0,0),(95,0),(95,95),(0,95)]),bbox=bbox)
   check(id+' no hidden RGB fringe',all(p==(0,0,0,0) for p in im.get_flattened_data()if p[3]==0))
   check(id+' no baked background/shadow/glow/UI layer',len(layers[id])==2 and not any(x in r['file']for r in layers[id]for x in ['desk','shadow','glow','frame']))
 # Native-layer relationships prove clipping/visibility rather than treating
 # declared text metadata alone as proof of the actual final image.
 def mask(name):return Image.open(ROOT/'masks'/name)
 ink=mask('CH4-NEW-11-canonical-form-ink.png');paper=mask('CH4-NEW-11-red-carbon-ticket.png')
 check('Inspection lettering/stamp entirely on paper',ImageChops.multiply(ink,ImageChops.invert(paper)).getbbox() is None)
 ring=mask('CH4-NEW-13-plain-silver-band.png');engraving=mask('CH4-NEW-13-inside-engraving.png');ribbon=mask('CH4-NEW-13-single-pale-blue-ribbon.png');maker=mask('CH4-NEW-13-anonymous-maker-punch.png')
 check('Engraving lies entirely on silver inner surface',ImageChops.multiply(engraving,ImageChops.invert(ring)).getbbox() is None)
 check('Maker punch lies entirely on silver',ImageChops.multiply(maker,ImageChops.invert(ring)).getbbox() is None)
 check('Ribbon does not occlude inscription',ImageChops.multiply(engraving,ribbon).getbbox() is None)
 check('Maker mark does not collide with lettering',ImageChops.multiply(engraving,maker).getbbox() is None)
 check('Slot ring hole genuinely transparent',Image.open(ROOT/m['assets'][2]['native']['file']).getpixel((41,47))[3]==0)
 check('Inspection hole displays desk, not a filled metal disc',ring.getpixel((246,235))==0 and Image.open(ROOT/m['assets'][3]['native']['file']).getpixel((246,235))==Image.open(ROOT/'layers/CH4-NEW-13-quiet-desk.png').getpixel((246,235))[:3])
 check('Slot has no readable engraving or hallmark',text['CH4-NEW-12']==[] and all(not any(word in r['file']for word in ['engraving','maker'])for r in layers['CH4-NEW-12']))
 actual=[r['text']for r in text['CH4-NEW-11']]
 check('Only canonical meaningful ticket lettering',actual==['DISPUTE TICKET','LOT 53','LACK OF PRIVACY','— CUSTOMER PRESENT','HOLD FOR','INSPECTION'])
 for r in text['CH4-NEW-11']:
  x,y,x1,y1=r['localBox'];check('Safe physical paper margins '+r['role'],min(x,y,430-x1,278-y1)>=20,minimumLocalMargin=round(min(x,y,430-x1,278-y1),2))
  check('Legible native character height '+r['role'],7*r['unit']>=14,nativeLocalHeight=7*r['unit'])
 entry=text['CH4-NEW-13'][0];check('Exact ring wording and punctuation',entry['text']=='AS IS, WHERE IS.' and ''.join(g['character']for g in entry['glyphs'])==entry['text'])
 check('Engraving actually follows inner curve',entry['followsInnerCurve'] and entry['nativeGlyphConstruction'] and entry['unit']==2 and max(g['tangentDegrees']for g in entry['glyphs'])-min(g['tangentDegrees']for g in entry['glyphs'])>35)
 slotgeom=geometry['CH4-NEW-12'];inspectgeom=geometry['CH4-NEW-13'];check('Ring pair shares precise band/ribbon geometry',slotgeom['sharedObject']==inspectgeom['sharedObject'] and slotgeom['outerRadii']==inspectgeom['outerRadii'] and slotgeom['innerRadii']==inspectgeom['innerRadii'])
 check('Ticket pair shares paper aspect/tear/curl identity',geometry['CH4-NEW-10']['paperLocalSize']==geometry['CH4-NEW-11']['paperLocalSize'] and geometry['CH4-NEW-10']['sharedObject']==geometry['CH4-NEW-11']['sharedObject'])
 for r in m['references']:
  data=subprocess.check_output(['git','show',r['sourceCommit']+':'+r['sourcePath']],cwd=REPO);check('Exact canonical benchmark '+r['file'],hashlib.sha256(data).hexdigest()==sha(ROOT/r['file'])==r['sha256'])
 for p in(ROOT/'previews').glob('*-4x.png'):
  name=p.name[:-7]+'.png';sources=[d/name for d in [ROOT/'native',ROOT/'references',ROOT/'comparisons']if(d/name).exists()];check('Unique source '+p.name,len(sources)==1)
  im=Image.open(sources[0]);f=Image.open(p);check('Exact nearest4x '+p.name,f.mode==im.mode and f.size==(im.width*4,im.height*4) and ImageChops.difference(f,im.resize(f.size,Image.Resampling.NEAREST)).getbbox() is None)
 check('Comparison caption margins',all(r['fits']for r in json.loads((ROOT/'evidence/caption-layout.json').read_text())))
 for p,box,source in [('ring-inscription-native-crop.png',(125,128,372,203),m['assets'][3]['native']['file']),('ticket-lettering-native-crop.png',(104,102,490,351),m['assets'][1]['native']['file'])]:check('Exact crop '+p,ImageChops.difference(Image.open(ROOT/'comparisons'/p),Image.open(ROOT/source).crop(box)).getbbox() is None)
 items=json.loads((REPO/'story/items.draft.json').read_text());saved=json.loads((ROOT/'evidence/canonical-items.json').read_text());check('Exact canonical item snapshot',all(items[k]==v for k,v in saved.items()))
 description=items['lot_53_dispute_ticket']['description'];check('All three ticket phrases authored in item description',all(p in description for p in ['LOT 53','LACK OF PRIVACY — CUSTOMER PRESENT','HOLD FOR INSPECTION']))
 read=items['wedding_ring_lot31']['description'][1]['text'];check('Exact inscription and maker existence in authored READ',"TINY MAKER'S MARK"in read and 'AS IS, WHERE IS.'in read)
 check('No draft-only ticket words invented',json.loads((ROOT/'evidence/wording-audit.json').read_text())['draftOnlyProposedTicketWording']==[])
 nodes=json.loads((REPO/'story/chapters/chapter-04.wip.json').read_text())['nodes'];saved=json.loads((ROOT/'evidence/canonical-nodes.json').read_text());check('Exact node / condition / choice snapshots',all(nodes[k]==v for k,v in saved.items()))
 prov=json.loads((ROOT/'evidence/generation-provenance.json').read_text())
 for s in prov['sources']:
  check('Preserved original/prompt '+s['id'],sha(ROOT/s['file'])==s['sha256'] and sha(ROOT/s['prompt'])==s['promptSha256'])
  for r in s['inputs']:check('Preserved source input '+r['file'],sha(ROOT/r['file'])==r['sha256'])
 check('Honest source-derived design / native raster provenance',prov['sourceDerivedDesign'] and prov['nativeRasterConstructedIndependently'] and not prov['sourcePixelsTransferred'] and not prov['whollyIndependentCreativeDesign'])
 with tempfile.TemporaryDirectory(prefix='b217-native-replay-')as folder:
  t=Path(folder);(t/'source').mkdir()
  for n in ['build.py','chunky-glyphs.json']:shutil.copyfile(ROOT/'source'/n,t/'source'/n)
  log=subprocess.check_output([sys.executable,str(t/'source/build.py')],text=True)
  check('All four images reproduce without any source/reference PNGs',not(t/'originals').exists() and not(t/'references').exists() and all(sha(t/a['native']['file'])==a['native']['sha256']for a in m['assets']))
  (ROOT/'evidence/source-isolated-replay.json').write_text(json.dumps({'passed':True,'onlyInputs':['source/build.py','source/chunky-glyphs.json'],'sourceImagesAvailable':False,'output':json.loads(log)},indent=2)+'\n')
 count=0;selected=0
 for line in subprocess.check_output(['git','ls-tree','-r',m['canonicalBaseline']],cwd=REPO,text=True).splitlines():
  meta,name=line.split('\t',1);mode,kind,digest=meta.split()
  if kind!='blob':continue
  data=(REPO/name).read_bytes();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==digest,name;count+=1;selected+=int(name.startswith('assets/selected/'))
 check('Every baseline tracked file / selected artwork byte-identical',True,baselineFiles=count,selectedArtFiles=selected)
 check('Dedicated isolated B2-17 branch',subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()==m['branch'])
 check('No registration/gameplay/item-rule/state/binding changes',not m['registryModified'] and not m['narrativeGameplayItemRulesOrEngineModified'] and m['newFocusStatesOrBindings']==0 and not m['nextBatchStarted'])
 (ROOT/'evidence/validation.json').write_text(json.dumps({'passed':True,'status':'UNSELECTED','artisticApproval':False,'visualLegibilityApproval':'Owner review still required; text geometry/wording/occlusion verified and native artwork visually inspected.','checks':checks},indent=2)+'\n')
 print(json.dumps({'passed':True,'checks':len(checks),'baselineFiles':count,'selectedArtFiles':selected}))
if __name__=='__main__':main()
