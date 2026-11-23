"""Native contracts, immutable selection preservation, lettering and replay QA."""
from pathlib import Path
from PIL import Image
from html.parser import HTMLParser
import hashlib,json,subprocess,os
ROOT=Path(__file__).resolve().parents[1];REPO=next(p for p in ROOT.parents if (p/'story/artwork.draft.json').exists());BASE='3463e20bd366390008fa4f71c087ed5f334f3a31';OLD='tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 checks=[]
 def check(v,n):
  assert v,n
  checks.append({'check':n,'passed':True})
 m=json.loads((ROOT/'manifest.json').read_text());d=json.loads((ROOT/'evidence/derivation.json').read_text())['assets'];a=m['assets']
 check(len(a)==5 and all(x['status']=='UNSELECTED' and not x['selected'] and x['sourceDerived'] for x in a),'Exactly five unselected source-derived candidates')
 check([x['key'] for x in a]==['portraits:hotel_plumber:worried','portraits:hotel_plumber_assistant:pleased','scenes:grand_bellevue/restroom#portraitBackground','focus:grand_bellevue/restroom/lot_14_receipt','focus:grand_bellevue/restroom/master_isolator'],'Exact canonical B2-01 logical assets')
 for x in a:
  for k in ['native','original','preview4x']:
   p=ROOT/x[k]['file'];check(sha(p)==x[k]['sha256'],x['id']+' '+k+' hash')
  im=Image.open(ROOT/x['native']['file']);four=Image.open(ROOT/x['preview4x']['file'])
  check(im.size==(564,278),x['id']+' actual native564x278')
  extrema=im.convert('RGBA').getchannel('A').getextrema()
  check(im.mode=='RGBA' and extrema[0]==0 if x['kind']=='portrait' else extrema==(255,255),x['id']+' correct alpha contract')
  check(four.size==(2256,1112) and four.tobytes()==im.resize((2256,1112),Image.Resampling.NEAREST).tobytes(),x['id']+' exact nearest4x')
  check(not d[x['id']]['independentlyAuthoredAtNativeResolution'],x['id']+' provenance is source-derived')
 # Every old review-version byte, plus canonical story and selected images, stays untouched.
 preserved=0
 paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,OLD,'story','assets/selected'],cwd=REPO,text=True).splitlines()
 for rel in paths:
  if rel.startswith(OLD+'/'):
   # Root navigation/policy may receive a later owner-decision addendum.
   part=Path(rel).relative_to(OLD).parts[0]
   if part not in ['v01','v02','v03','v04','v05','v06','v07','v08','portrait-study-01','portrait-study-02']:continue
  original=subprocess.check_output(['git','show',BASE+':'+rel],cwd=REPO)
  check((REPO/rel).is_file() and (REPO/rel).read_bytes()==original,'Immutable prior/canonical file '+rel);preserved+=1
 node=json.loads((ROOT/'evidence/canonical-nodes.json').read_text())
 check(a[3]['nodeIds']==['hotel_lot_receipt_study'] and a[4]['nodeIds']==['hotel_key_master_cabinet'],'Focus source nodes exact')
 lettering=d['CH4-B2-04']['nativeLettering']
 check(all(t in node['hotel_lot_receipt_study']['text'] for t in lettering['lines']),'All receipt copy is verbatim canonical')
 check(' '.join(lettering['renderedRows'][-2:])==lettering['lines'][-1],'Exception wraps without lost or invented words')
 sx,sy,ex,ey=lettering['safeTextRectInPaperPlane']
 check(all(sx<=x0<x1<=ex and sy<=y0<y1<=ey for x0,y0,x1,y1 in lettering['glyphBoundsInPaperPlane']),'All receipt text remains inside inset margins')
 check(min(lettering['minimumPaperPlaneMargins'])>=25,'Paper has at least25px planning inset on every side')
 check(len(lettering['paperPlaneQuad'])==4 and d['CH4-B2-05']['nativeLettering']['nativeCapHeightApproximate']>=7,'Perspective and legible close-up plaque cap height recorded')
 check(d['CH4-B2-02']['portraitPropLettering']['text']==['LOT','14'],'Held portrait receipt has readable canonical lot identifier')
 for atlas in ['tiny5-approved-atlas.png','pressstart-approved-atlas.png']:
  check(set(Image.open(ROOT/'fonts'/atlas).convert('RGBA').getchannel('A').get_flattened_data())<={0,255},'Approved bitmap font mask is hard0/255 '+atlas)
 for x in a[:2]:
  bg=Image.open(ROOT/a[2]['native']['file']).convert('RGBA');fg=Image.open(ROOT/x['native']['file']).convert('RGBA');actual=Image.open(ROOT/f'previews/{x["id"]}-composite.png')
  check(actual.tobytes()==Image.alpha_composite(bg,fg).tobytes(),x['id']+' exact two-layer composite')
 class Links(HTMLParser):
  def handle_starttag(self,t,attrs):
   for k,v in attrs:
    if v=='evidence/validation.json':continue
    if k in ['src','href','data-one','data-four'] and v and not v.startswith(('http:','https:','#','data:')):check((ROOT/v).is_file(),'Gallery dependency '+v)
 Links().feed((ROOT/'index.html').read_text())
 selected=[p for dr in ['native','previews','comparisons'] for p in (ROOT/dr).glob('*.png')]+[ROOT/'manifest.json',ROOT/'index.html']
 before={str(p.relative_to(ROOT)):sha(p) for p in selected}
 for script in ['prepare.py','package.py']:subprocess.run(['python3',str(ROOT/'source'/script)],check=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=subprocess.DEVNULL)
 check(all(sha(ROOT/p)==h for p,h in before.items()),'Exact production/composite/gallery replay')
 report={'passed':True,'checksPassed':len(checks),'assets':5,'sourceDerived':True,'selected':False,'historicalAndCanonicalFilesPreserved':preserved,'replayFilesIdentical':len(before),'receiptMarginsPass':True,'objectLetteringPerspectiveAndReadabilityChecked':True,'mainScenesChanged':False,'gameIntegrationPerformed':False,'checks':checks}
 (ROOT/'evidence/validation.json').write_text(json.dumps(report,indent=2)+'\n');print(str(len(checks))+' checks passed; five unselected assets; exact replay and old-art preservation.')
if __name__=='__main__':main()
