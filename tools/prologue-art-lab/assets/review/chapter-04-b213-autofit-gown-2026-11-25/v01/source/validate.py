from pathlib import Path
from PIL import Image,ImageChops
from collections import Counter
import json,hashlib,subprocess,tempfile,shutil,sys
ROOT=Path(__file__).resolve().parents[1];REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists());BASE='436e83f43c01b0a64620056d44aabf14c61fb444'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 checks=[]
 def check(label,ok,**details):
  assert ok,(label,details);checks.append({'check':label,'passed':True,**details})
 m=json.loads((ROOT/'manifest.json').read_text());recipe=json.loads((ROOT/'evidence/native-layer-recipes.json').read_text());palettes={}
 check('One primary / one supplemental, both unselected',m['primaryAssetCount']==1 and m['supplementalReferenceCount']==1 and m['status']=='UNSELECTED'and not m['ownerApproved'])
 for a,key in[(m['primary'],'default'),(m['supplementalReferences'][0],'manual-slack')]:
  im=Image.open(ROOT/a['native']['file']);four=Image.open(ROOT/a['exact4x']['file'])
  check(key+'564x278 opaque RGB',im.size==(564,278)and im.mode=='RGB')
  check(key+' SHA-256',sha(ROOT/a['native']['file'])==a['native']['sha256'])
  check(key+' exact nearest4x',four.size==(2256,1112)and ImageChops.difference(four,im.resize((2256,1112),Image.Resampling.NEAREST)).getbbox()is None)
  out=Image.new('RGBA',(564,278))
  for r in recipe['states'][key]:
   layer=Image.open(ROOT/r['file']);check(key+' layer '+r['file'],sha(ROOT/r['file'])==r['sha256']and layer.size==(564,278)and layer.mode=='RGBA'and set(layer.getchannel('A').get_flattened_data())<={0,255});out=Image.alpha_composite(out,layer)
  check(key+' exact native layer replay',ImageChops.difference(out.convert('RGB'),im).getbbox()is None)
  check(key+' remains unselected/unbound',a['status']=='UNSELECTED'and not a['ownerApproved']and not a['selected']and a['canonicalAssetPath']is None and a['runtimeBinding']is None)
  counts=Counter(im.get_flattened_data());palettes[key]={'colors':len(counts),'globalCapImposed':False,'constantColourMaterialRamps':'evidence/native-palette-ramps.json','colorsAndPixels':[{'rgb':list(c),'pixels':n}for c,n in counts.most_common()]}
 # Geometry changes are localized in the shared world-registration diagnostic;
 # the supplemental production frame is a separate closer native camera.
 wide=Image.open(ROOT/m['primary']['native']['file']);world=Image.open(ROOT/'diagnostics/manual-slack-world-registration-NOT-candidate.png');diff=ImageChops.difference(wide,world);actual=ImageChops.lighter(ImageChops.lighter(diff.getchannel('R'),diff.getchannel('G')),diff.getchannel('B')).point(lambda v:255 if v else 0)
 saved=Image.open(ROOT/'masks/actual-manual-slack-change.png');allowed=Image.open(ROOT/'masks/authorized-manual-slack-change.png')
 check('World-coordinate difference mask exact',ImageChops.difference(actual,saved).getbbox()is None)
 check('Only lining/cables change in shared geometry',ImageChops.multiply(actual,ImageChops.invert(allowed)).getbbox()is None and actual.getbbox()is not None,changedWorldPixels=sum(v>0 for v in actual.get_flattened_data()))
 out=Image.new('RGBA',(564,278))
 for r in recipe['states']['manual-slack-world-diagnostic']:out=Image.alpha_composite(out,Image.open(ROOT/r['file']))
 check('World diagnostic layer replay exact',ImageChops.difference(out.convert('RGB'),world).getbbox()is None)
 # Meaningful reproducibility gate: no source/reference PNG exists in replay.
 with tempfile.TemporaryDirectory(prefix='b213-native-replay-')as folder:
  t=Path(folder)
  for d in ['source','native','previews','layers','masks','diagnostics','evidence']:(t/d).mkdir()
  for f in ['build_native.py','bitmap-glyphs.json']:shutil.copyfile(ROOT/'source'/f,t/'source'/f)
  log=subprocess.check_output([sys.executable,str(t/'source/build_native.py')],text=True)
  check('Independent native construction with NO original/reference images available',not(t/'originals').exists()and not(t/'references').exists()and all(sha(t/a['native']['file'])==a['native']['sha256']for a in[m['primary']]+m['supplementalReferences']))
  isolated={'passed':True,'inputFiles':['source/build_native.py','source/bitmap-glyphs.json'],'originalAndReferenceImagesAvailable':False,'sourcePixelsTransferred':False,'nativeHashesReproduced':{a['native']['file']:sha(t/a['native']['file'])for a in[m['primary']]+m['supplementalReferences']},'rendererResult':json.loads(log)}
 (ROOT/'evidence/source-isolated-replay.json').write_text(json.dumps(isolated,indent=2)+'\n')
 text=json.loads((ROOT/'evidence/lettering-layout.json').read_text());default=[t for t in text if t['view']=='default'];close=[t for t in text if t['view']=='manual-slack']
 check('Default labels subordinate / no manual solution in primary',all(t['text']in['AUTOFIT','BRIDAL','SYSTEM']and t['font']=='3x5'for t in default)and len(default)==3 and not m['primary']['releaseSolutionRevealed'])
 check('Default recipe excludes discovery layers',not any('revealed'in r['file']or'close-'in r['file']or'manual-slack-inner'in r['file']for r in recipe['states']['default']))
 check('Closer supplement contains full tab and warning text',{'MANUAL','SLACK','NOT AN','EMERGENCY','STOP'}<={t['text']for t in close})
 check('Meaningful native lettering stays inside its physical labels',all(t['binaryGlyphs']and t['inkBox'][0]>=t['box'][0]and t['inkBox'][1]>=t['box'][1]and t['inkBox'][2]<=t['box'][2]and t['inkBox'][3]<=t['box'][3]for t in text))
 for r in m['references']:
  data=subprocess.check_output(['git','show',BASE+':'+r['sourcePath']],cwd=REPO);check('Approved benchmark exact '+r['file'],hashlib.sha256(data).hexdigest()==r['sha256']==sha(ROOT/r['file']))
 for p in(ROOT/'previews').glob('*-4x.png'):
  name=p.name[:-7]+'.png';sources=[d/name for d in[ROOT/'native',ROOT/'references',ROOT/'comparisons']if(d/name).is_file()];check(p.name+' source exists',len(sources)==1)
  im=Image.open(sources[0]);four=Image.open(p);check(p.name+' exact nearest4x',four.size==(im.width*4,im.height*4)and ImageChops.difference(four,im.resize(four.size,Image.Resampling.NEAREST)).getbbox()is None)
 check('Comparison labels fit',all(x['fits']for x in json.loads((ROOT/'evidence/caption-layout.json').read_text())))
 prov=json.loads((ROOT/'evidence/generation-provenance.json').read_text());check('Original source/prompt exact',sha(ROOT/prov['source']['file'])==prov['source']['sha256']and sha(ROOT/prov['prompt'])==prov['promptSha256'])
 for r in prov['inputs']:check('Generation input exact '+r['file'],sha(ROOT/r['file'])==r['sha256'])
 check('Honest source-derived design / independent native raster provenance',m['sourceDerivedDesign']and m['nativeRasterIndependentlyConstructed']and not m['sourcePixelsTransferred']and not m['wholeArtworkWhollyIndependentOfReferences'])
 j=json.loads((REPO/'story/chapters/chapter-04.wip.json').read_text());nodes=j['nodes'];nodes={n['id']:n for n in nodes}if isinstance(nodes,list)else nodes;saved=json.loads((ROOT/'evidence/canonical-nodes.json').read_text())
 check('Canonical narrative snapshot exact',all(nodes[k]==v for k,v in saved.items()))
 check('Intended Focus is authored but unregistered',nodes['hotel_bridal_gown_focus']['focus']=='grand_bellevue/autofit_gown'and 'grand_bellevue/autofit_gown'not in json.loads((REPO/'story/artwork.draft.json').read_text()).get('focus',{}))
 choice=next(c for c in nodes['hotel_bridal_gown_focus']['choices']if c['id']=='gown_examine_motor');check('Existing discovery eligibility unchanged',choice['if']=={'notFlag':'ch4_autofit_release_located'}and choice['to']=='hotel_bridal_gown_motor')
 check('One authored press/loosen sequence; motor node remains narrative',nodes['hotel_bridal_gown_motor']['mode']=='narrative'and nodes['hotel_bridal_gown_motor']['effects']['set']['ch4_autofit_release_located']is True and 'You press the tab'in json.dumps(nodes['hotel_bridal_gown_motor']))
 supp=m['supplementalReferences'][0];check('No extra Focus, flag, mode or runtime binding',supp['newFocusId']is None and supp['newFlag']is None and supp['runtimeBinding']is None and supp['existingNodeMode']=='narrative')
 count=0;selected=0
 for line in subprocess.check_output(['git','ls-tree','-r',BASE],cwd=REPO,text=True).splitlines():
  meta,name=line.split('\t',1);mode,kind,digest=meta.split()
  if kind!='blob':continue
  data=(REPO/name).read_bytes();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==digest,name;count+=1;selected+=int(name.startswith('assets/selected/'))
 check('Every baseline tracked blob unchanged',True,baselineFiles=count,selectedAssetFiles=selected,baselineCommit=BASE)
 check('Correct isolated art-review branch',subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()==m['branch'])
 (ROOT/'evidence/palette-diagnostics.json').write_text(json.dumps(palettes,indent=2)+'\n');report={'passed':True,'status':'UNSELECTED','artisticApproval':False,'nativeRasterConstructedWithoutSourcePixels':True,'checks':checks};(ROOT/'evidence/validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':True,'checks':len(checks),'palettes':{k:v['colors']for k,v in palettes.items()},'baselineFiles':count,'selectedAssetFiles':selected}))
if __name__=='__main__':main()
