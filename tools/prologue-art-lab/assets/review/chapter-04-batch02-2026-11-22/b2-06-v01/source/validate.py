from pathlib import Path
from PIL import Image,ImageChops
from html.parser import HTMLParser
import json,hashlib,subprocess,os
ROOT=Path(__file__).resolve().parents[1];REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists());BASE='c6dbbaff7bf0edbda7a8ddff14556588c1eacd73'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 checks=[]
 def check(v,s):
  assert v,s
  checks.append({'check':s,'passed':True})
 m=json.loads((ROOT/'manifest.json').read_text());d=json.loads((ROOT/'evidence/derivation.json').read_text());canon=m['canonicalApprovalBaseline'];nodes=json.loads(subprocess.check_output(['git','show',canon+':story/chapters/chapter-04.wip.json'],cwd=REPO))['nodes'];check(len(m['assets'])==6 and m['status']=='UNSELECTED','Exactly six unselected canonical B2-06 portraits')
 for a in m['assets']:
  id_=a['id'];im=Image.open(ROOT/a['native']['file']);four=Image.open(ROOT/a['preview4x']['file']);source=Image.open(ROOT/a['detailedReference']['file']);check(im.size==(564,278)and im.mode=='RGBA',id_+' native564x278 RGBA');check(sha(ROOT/a['native']['file'])==a['native']['sha256'],id_+' exact native hash');check(source.mode=='RGBA'and source.getchannel('A').getextrema()[0]==0,id_+' generated original retains true alpha');check(sha(ROOT/a['detailedReference']['file'])==a['detailedReference']['sha256'],id_+' source hash')
  check(four.size==(2256,1112)and four.tobytes()==im.resize(four.size,Image.Resampling.NEAREST).tobytes(),id_+' exact4x pixels');check(sha(ROOT/a['preview4x']['file'])==a['preview4x']['sha256'],id_+' preview hash');check(set(im.getchannel('A').get_flattened_data())=={0,255},id_+' binary clean alpha');check(all(p==(0,0,0,0)for p in im.get_flattened_data()if not p[3]),id_+' transparent RGB cleared');box=im.getchannel('A').getbbox();check(box[0]>10 and box[1]>5 and box[2]<554,id_+' complete head/veil/hands and transparent margins');check(a['status']=='UNSELECTED'and not a['selected']and a['sourceDerived']and not a['independentlyAuthoredAtNativeResolution'],id_+' unselected/honest source-derived status')
  who,pose=a['key'].split(':')[1:];check(all(nodes[n].get('speaker')==who and nodes[n].get('pose')==pose and nodes[n]['scene']in a['sceneKeys']for n in a['nodeIds']),id_+' exact authored speaker/pose/node/background mapping')
  for scene,c in a['composites'].items():
   bg=Image.open(ROOT/c['backgroundReference']).convert('RGBA');comp=Image.open(ROOT/c['native']['file']);check(Image.alpha_composite(bg,im).convert('RGB').tobytes()==comp.tobytes(),id_+' exact approved-context composite '+scene);check(Image.open(ROOT/c['preview4x']['file']).tobytes()==comp.resize((2256,1112),Image.Resampling.NEAREST).tobytes(),id_+' exact4x context '+scene)
  check(Image.open(ROOT/f'layers/{id_}-native-foreground.png').tobytes()==im.tobytes(),id_+' editable native master exact')
  check(sha(ROOT/a['effectiveSource']['file'])==a['effectiveSource']['sha256']==next(x['sourceSha256']for x in d['assets']if x['id']==id_),id_+' exact effective source used')
  record=next(x for x in d['assets']if x['id']==id_);alpha=Image.new('L',im.size)
  for name in record['materialMasks']:
   mm=Image.open(ROOT/f'masks/{id_}-{name}.png');part=Image.open(ROOT/f'layers/{id_}-{name}.png');alpha=ImageChops.lighter(alpha,mm);check(part.getchannel('A').tobytes()==mm.tobytes(),id_+' addressable '+name+' layer alpha')
  check(alpha.tobytes()==im.getchannel('A').tobytes(),id_+' semantic material masks cover full silhouette')
  for suffix in ['identity-pavilion','chapter2']:
   sheet=Image.open(ROOT/f'comparisons/{id_}-{suffix}-native.png');check(Image.open(ROOT/f'comparisons/{id_}-{suffix}-4x.png').tobytes()==sheet.resize((sheet.width*4,sheet.height*4),Image.Resampling.NEAREST).tobytes(),id_+' exact4x canonical comparison '+suffix)
 check(set(a['key']for a in m['assets'])=={'portraits:hotel_auctioneer:delighted','portraits:hotel_auctioneer:disappointed','portraits:hotel_auctioneer:bureaucratic','portraits:hotel_porter:alarmed','portraits:hotel_porter:curious','portraits:hotel_porter:relieved'},'Only six exact inventory demands')
 check(next(a for a in m['assets']if a['id']=='CH4-B2-34')['effectiveSource']['file'].endswith('-cutout.png'),'Corrected relieved cutout used, original retained')
 for name,a in m['canonicalBenchmarks'].items():
  check((ROOT/f'references/{name}.png').read_bytes()==subprocess.check_output(['git','show',canon+':'+a['file']],cwd=REPO),'Exact approved benchmark '+name)
 old=0
 for path in subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'tools/prologue-art-lab/assets/review','story','assets/selected','.github','docs'],cwd=REPO,text=True).splitlines():
  if path.startswith('tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/')and Path(path).name in ['AGENTS.md','README.md','SHA256SUMS']:continue
  check((REPO/path).read_bytes()==subprocess.check_output(['git','show',BASE+':'+path],cwd=REPO),'Previous review/canonical file exact '+path);old+=1
 class Links(HTMLParser):
  def handle_starttag(self,t,attrs):
   for k,v in attrs:
    if v=='evidence/validation.json':continue
    if k in ['src','href','data-one','data-four']and v and not v.startswith(('https:','http:','#','data:')):check((ROOT/v).is_file(),'Gallery dependency '+v)
 Links().feed((ROOT/'index.html').read_text())
 paths=[p for folder in ['native','previews','layers','masks','comparisons']for p in(ROOT/folder).glob('*.png')]+[ROOT/'manifest.json',ROOT/'index.html'];before={str(p.relative_to(ROOT)):sha(p)for p in paths}
 for script in ['native_build.py','package.py']:subprocess.run(['python3',str(ROOT/'source'/script)],cwd=REPO,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=subprocess.DEVNULL,check=True)
 check(all(sha(ROOT/p)==s for p,s in before.items()),'Exact deterministic native/gallery replay')
 out={'passed':True,'checksPassed':len(checks),'assets':6,'status':'UNSELECTED','canonicalNodeCount':len(m['storyNodeCoverage']),'sourceDerived':True,'canonicalFilesChanged':0,'historicalAndCanonicalFilesPreserved':old,'replayFilesIdentical':len(before),'integrationPerformed':False,'visualAssessment':'evidence/visual-review.md','checks':checks};(ROOT/'evidence/validation.json').write_text(json.dumps(out,indent=2)+'\n');print(str(len(checks))+' checks passed; six unselected portraits; prior artwork unchanged.')
if __name__=='__main__':main()
