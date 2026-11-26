from pathlib import Path
from PIL import Image,ImageChops
from collections import Counter
import json,hashlib,subprocess,tempfile,shutil,sys
ROOT=Path(__file__).resolve().parents[1];REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists());BASE='436e83f43c01b0a64620056d44aabf14c61fb444'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 checks=[]
 def check(label,ok,**detail):
  assert ok,(label,detail);checks.append({'check':label,'passed':True,**detail})
 m=json.loads((ROOT/'manifest.json').read_text());recipes=json.loads((ROOT/'evidence/native-layer-recipes.json').read_text());identities=json.loads((ROOT/'evidence/shell-identities.json').read_text());ramps=json.loads((ROOT/'evidence/material-ramps.json').read_text());palette={}
 check('Two primary candidates; no invented state assets',len(m['assets'])==2 and m['supplementalAssetCount']==0 and m['status']=='UNSELECTED'and not m['ownerApproved'])
 for a,key,size in zip(m['assets'],['room','focus'],[(314,206),(564,278)]):
  im=Image.open(ROOT/a['native']['file']);four=Image.open(ROOT/a['exact4x']['file']);check(key+' native RGB/dimensions',im.mode=='RGB'and im.size==size)
  check(key+' final hash',sha(ROOT/a['native']['file'])==a['native']['sha256']);check(key+' exact4x',four.size==(size[0]*4,size[1]*4)and ImageChops.difference(four,im.resize(four.size,Image.Resampling.NEAREST)).getbbox()is None)
  out=Image.new('RGBA',size)
  for r in recipes[key]:
   layer=Image.open(ROOT/r['file']);check(key+' layer '+r['file'],sha(ROOT/r['file'])==r['sha256']and layer.size==size and layer.mode=='RGBA'and set(layer.getchannel('A').get_flattened_data())<={0,255});out=Image.alpha_composite(out,layer)
  check(key+' exact compositing replay',ImageChops.difference(im,out.convert('RGB')).getbbox()is None)
  check(key+' unselected/unbound',not a['selected']and not a['ownerApproved']and a['status']=='UNSELECTED'and a['canonicalAssetPath']is None and a['runtimeBinding']is None)
  counts=Counter(im.get_flattened_data());palette[key]={'colors':len(counts),'noGlobalCapImposed':True,'colorsAndPixels':[{'rgb':list(c),'pixels':n}for c,n in counts.most_common()]}
  shells=identities[key];check(key+' exactly three canonical shell identities',[s['kind']for s in shells]==['smooth','ridged','third'])
  masks=[Image.open(ROOT/s['mask'])for s in shells]
  for i,s in enumerate(shells):
   layer=Image.open(ROOT/f'layers/{key}-shell-{s["kind"]}.png');allowed={tuple(bytes.fromhex(h[1:]))for h in ramps['shell']};colours={p[:3]for p in layer.get_flattened_data()if p[3]}
   check(key+' '+s['kind']+' neutral shell material only',colours<=allowed and len(colours)>1 and masks[i].getbbox()is not None and layer.size==size)
   for j in range(i):check(key+' separate shell silhouettes '+str(i)+str(j),ImageChops.multiply(masks[i],masks[j]).getbbox()is None)
 for r in m['references']:
  data=subprocess.check_output(['git','show',BASE+':'+r['sourcePath']],cwd=REPO);check('Canonical reference '+r['file'],hashlib.sha256(data).hexdigest()==r['sha256']==sha(ROOT/r['file']))
 for p in(ROOT/'previews').glob('*-4x.png'):
  name=p.name[:-7]+'.png';sources=[d/name for d in[ROOT/'native',ROOT/'references',ROOT/'comparisons']if(d/name).is_file()];check(p.name+' native source',len(sources)==1)
  im=Image.open(sources[0]);four=Image.open(p);check(p.name+' exact nearest4x',four.size==(im.width*4,im.height*4)and ImageChops.difference(four,im.resize(four.size,Image.Resampling.NEAREST)).getbbox()is None)
 check('Comparison caption margins',all(r['fits']for r in json.loads((ROOT/'evidence/caption-layout.json').read_text())))
 with tempfile.TemporaryDirectory(prefix='b214-native-replay-')as folder:
  t=Path(folder)
  for d in['source','native','previews','layers','masks','evidence']:(t/d).mkdir()
  shutil.copyfile(ROOT/'source/build.py',t/'source/build.py');log=subprocess.check_output([sys.executable,str(t/'source/build.py')],text=True)
  check('Source-isolated native replay: zero reference images available',not(t/'originals').exists()and not(t/'references').exists()and all(sha(t/a['native']['file'])==a['native']['sha256']for a in m['assets']))
  (ROOT/'evidence/source-isolated-replay.json').write_text(json.dumps({'passed':True,'onlyInput':'source/build.py','originalsAndReferencesAvailable':False,'sourcePixelsTransferred':False,'reproducedNativeHashes':{a['id']:sha(t/a['native']['file'])for a in m['assets']},'rendererOutput':json.loads(log)},indent=2)+'\n')
 prov=json.loads((ROOT/'evidence/generation-provenance.json').read_text())
 for s in prov['sources']:
  check('Source original/prompt hash '+s['prompt'],sha(ROOT/s['original']['file'])==s['original']['sha256']and sha(ROOT/s['prompt'])==s['promptSha256'])
  for r in s['inputs']:check('Source input '+r['file'],sha(ROOT/r['file'])==r['sha256'])
 check('Honest provenance',prov['sourceDerivedDesign']and prov['nativeRasterConstructedIndependently']and not prov['sourcePixelsTransferred']and not prov['whollyIndependentCreativeDesign'])
 nodes=json.loads((REPO/'story/chapters/chapter-04.wip.json').read_text())['nodes'];nodes={n['id']:n for n in nodes}if isinstance(nodes,list)else nodes;saved=json.loads((ROOT/'evidence/canonical-nodes.json').read_text())
 check('Exact authored-node snapshot',all(nodes[k]==v for k,v in saved.items()))
 check('Canonical room and Focus mappings',nodes['hotel_seashell_room']['scene']=='grand_bellevue/bridal_lavatory'and nodes['hotel_seashell_inspect']['focus']=='grand_bellevue/three_seashells')
 check('Authored smooth/ridged/ordinary distinction','One is smooth, one ridged'in json.dumps(nodes['hotel_seashell_inspect']))
 check('No source-authored operating instructions exposed','No instructions ever provided'in nodes['hotel_seashell_instructions']['notes'])
 check('No extra gameplay modes/conditions/registration',not m['registryModified']and not m['narrativeGameplayOrEngineModified'])
 architecture=json.loads((ROOT/'evidence/architecture.json').read_text());check('Open counter / no concealed plumbing representation',architecture['openUnderCounter']and architecture['brackets']==2 and architecture['plumbingFixtures']==0 and architecture['textOrInstructions']==0)
 count=0;selected=0
 for entry in subprocess.check_output(['git','ls-tree','-r',BASE],cwd=REPO,text=True).splitlines():
  meta,name=entry.split('\t',1);mode,kind,digest=meta.split()
  if kind!='blob':continue
  data=(REPO/name).read_bytes();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==digest,name;count+=1;selected+=int(name.startswith('assets/selected/'))
 check('All baseline tracked blobs preserved',True,baselineFiles=count,selectedAssetFiles=selected,baseline=BASE)
 check('Isolated art-review branch',subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()==m['branch'])
 (ROOT/'evidence/palette-diagnostics.json').write_text(json.dumps(palette,indent=2)+'\n');(ROOT/'evidence/validation.json').write_text(json.dumps({'passed':True,'status':'UNSELECTED','artisticApproval':False,'nativeWithoutSourcePixels':True,'checks':checks},indent=2)+'\n');print(json.dumps({'passed':True,'checks':len(checks),'paletteCounts':{k:v['colors']for k,v in palette.items()},'baselineFiles':count,'selectedAssetFiles':selected}))
if __name__=='__main__':main()
