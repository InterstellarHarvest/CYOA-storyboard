"""Independent source, exact-grid, coverage, mask and preservation validation."""
from pathlib import Path
from PIL import Image, ImageChops
from html.parser import HTMLParser
import base64
import csv
import hashlib
import json
import subprocess

B=Path(__file__).resolve().parent;R=B.parents[5]
M=json.loads((B/'manifest.json').read_text());base=json.loads((B/'sources/preservation-baseline.json').read_text())
P=json.loads((R/'story/artwork-preview.json').read_text())['images'];A=json.loads((R/'story/artwork.draft.json').read_text())
C=json.loads((R/'story/chapters/chapter-03.reboot-candidate.json').read_text())['nodes']
matrix=json.loads((B/'chapter-03-completion-matrix.json').read_text());F=json.loads((B/'assessment/scene-findings.json').read_text())
pairings=json.loads((B/'assessment/portrait-composite-findings.json').read_text());checks=[]
def check(name,value):
    checks.append({'name':name,'pass':bool(value)});assert value,name
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def same(a,b):return a.mode==b.mode and a.size==b.size and a.tobytes()==b.tobytes()

keys={'scenes:'+k for k in A['scenes']if k.startswith('pavilion_reboot/')}
check('Exactly all 14 active Chapter 3 scene keys',len(keys)==14 and{r['key']for r in matrix}==keys and len(matrix)==14)
check('Six requested new assessments exact',set(M['newDetailedAssessments'])=={'human_verification_stage','urgency_stage','record_printer','courtesy_stage','arrival','exit_vestibule'})
check('All six new recommendations KEEP',all(F[n]['recommendation']=='KEEP'for n in M['newDetailedAssessments']))
check('No new candidate or artwork/portrait edits',M['newCandidates']==M['artworkPixelsChanged']==M['portraitPixelsChanged']==0 and not(B/'candidate').exists()and json.loads((B/'sources/changed-pixels.json').read_text())==[])
for row in matrix:
    name=row['key'].split('/')[-1];im=Image.open(B/'approved'/(name+'.png'));canonical=P[row['key']]
    check('Exact canonical source '+name,row['canonicalSha256']==canonical['sha256']==sha(B/'approved'/(name+'.png'))and row['canonicalSource']==canonical['source'])
    check('Source bytes match latest main '+name,subprocess.check_output(['git','show',base['mainCommit']+':'+canonical['file']],cwd=R)==(B/'approved'/(name+'.png')).read_bytes())
    record=A['scenes'][row['key'].split(':',1)[1]]
    check('Approved status and null path untouched '+name,record['status']=='approved'and record['assetPath']is None and row['canonicalStatus']=='approved'and row['productionAssetPath']is None)
    check('Opaque native RGB contract '+name,im.size==(314,206)and im.mode=='RGB'and im.convert('RGBA').getchannel('A').getextrema()==(255,255))
    big=Image.open(B/'previews'/(name+'-4x.png'));check('Exact 4x source blocks '+name,same(big,im.resize((1256,824),Image.Resampling.NEAREST)))
    mask=Image.open(B/row['repairMask']);check('Closed zero repair mask '+name,mask.mode=='L'and mask.size==(314,206)and mask.getextrema()==(0,0))
    check('Perspective/continuity findings present '+name,len(F[name]['perspective'])>60 and len(F[name]['continuity'])>60 and not F[name]['demonstratedNewDefects']and row['manualTouchupRecommendation']=='None demonstrated')
    for guide in ['protected','perspective','focus']:
        native=Image.open(B/'assessment'/(name+'-'+guide+'-native.png'));big=Image.open(B/'assessment'/(name+'-'+guide+'-4x.png'))
        check('Exact 4x '+name+' '+guide,same(big,native.resize((native.width*4,native.height*4),Image.Resampling.NEAREST)))
    native=Image.open(B/'comparisons'/(name+'-approved-left-protected-right-native.png'));big=Image.open(B/'comparisons'/(name+'-approved-left-protected-right-4x.png'))
    check('Native comparison exact original left '+name,native.size==(628,206)and same(native.crop((0,0,314,206)),im))
    check('Exact 4x comparison '+name,same(big,native.resize((2512,824),Image.Resampling.NEAREST)))
check('CSV and JSON have same 14 keys',{r['key']for r in csv.DictReader((B/'chapter-03-completion-matrix.csv').open())}==keys)

actual_pairs={}
for node,n in C.items():
    if n.get('speaker')in ['pavilion_attendant','pavilion_presenter']:
        k=(n['scene'].split('/')[-1],n['speaker']+':'+n.get('pose','idle'));actual_pairs.setdefault(k,[]).append(node)
check('15 pairings cover all 20 dialogue nodes',len(pairings)==15 and sum(len(p['nodes'])for p in pairings)==20 and{(p['scene'],p['portrait'])for p in pairings}==set(actual_pairs))
for p in pairings:
    check('Exact dialogue coverage '+p['id'],p['nodes']==actual_pairs[(p['scene'],p['portrait'])])
    bg=Image.open(B/p['backgroundFile']);fg=Image.open(B/p['foregroundFile'])
    check('Approved layer byte hashes '+p['id'],sha(B/p['backgroundFile'])==p['background']['sha256']and sha(B/p['foregroundFile'])==p['foreground']['sha256'])
    check('Original layer source metadata '+p['id'],p['background']==P['scenes:pavilion_reboot/'+p['scene']+'#portraitBackground']and p['foreground']==P['portraits:'+p['portrait']])
    check('Portrait canvas alpha contract '+p['id'],bg.size==fg.size==(564,278)and bg.mode in ['RGB','RGBA']and bg.convert('RGBA').getchannel('A').getextrema()==(255,255)and fg.mode=='RGBA'and not p['partialAlphaPixels']and fg.getchannel('A').getextrema()==(0,255))
    composite=Image.open(B/p['native']);check('Composite exact untransformed approved layers '+p['id'],same(composite,Image.alpha_composite(bg.convert('RGBA'),fg)))
    check('Composite exact 4x '+p['id'],same(Image.open(B/p['fourX']),composite.resize((2256,1112),Image.Resampling.NEAREST)))
    check('Portrait no edit and KEEP '+p['id'],p['recommendation']=='KEEP'and p['pixelsChanged']==0 and not p['portraitModificationAuthorized'])

for ref in M['crossChapterReferences']:
    check('Approved cross-chapter reference '+ref['key'],ref['sha256']==sha(B/ref['reviewFile'])==P[ref['key']]['sha256'])
    im=Image.open(B/ref['reviewFile']);big=Image.open(B/'previews'/(Path(ref['reviewFile']).stem+'-4x.png'))
    check('Reference exact 4x '+ref['key'],same(big,im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST)))
for a in json.loads((B/'assessment/unselected-alternatives.json').read_text()):
    check('Historical unselected alternative exact '+a['version']+' '+a['key'],sha(R/a['file'])==a['sha256']and('unselected'in a['status']or'not selected'in a['status']))
pr=json.loads((B/'sources/paper-pr18-snapshot.json').read_text());paper=next(r for r in matrix if r['key'].endswith('/paper_emergency'))
check('Paper canonical main remains v03',paper['canonicalSha256']==P[paper['key']]['sha256']=='ac0f7c44d267dd54897507ae3b8b02959a5b76f4fcd9d0418b77b8fdb777ba7e')
check('Paper v04 selected and published reference exact',sha(B/'references/paper-emergency-selected-v04.png')==paper['selectedSupersedingArtwork']['sha256']=='93a48082124600b1afeb45e5ea54856bf253e858e55111295e9d9c26919bc978')
check('PR18 remains draft open/unmerged, separate registration done on branch',pr['number']==18 and pr['state']=='open'and pr['draft']and not pr['merged']and pr['headCommit']=='3768b174e544600c3a88e3ae8b18c0fb35982ac4'and pr['selectedPreviewOnRegistrationBranch']['sha256']==paper['selectedSupersedingArtwork']['sha256'])
v=json.loads((B/'assessment/exit-vestibule-resolution.json').read_text());check('Vestibule uncertainty resolved without speculative geometry',v['previous']=='UNCERTAIN'and v['recommendation']=='KEEP'and not v['newGeometryProposed']and len(v['evidence'])==5)
a01=Image.open(B/'approved/restroom_entrance.png');b02=Image.open(B/'approved/record_printer.png');courtesy=Image.open(B/'approved/courtesy_stage.png')
check('Record Printer changes confined to receipt area versus A01',ImageChops.difference(a01,b02).getbbox()==(111,138,195,205))
check('Courtesy exact protected right desk half',same(a01.crop((180,0,314,206)),courtesy.crop((180,0,314,206))))
stage=Image.open(B/'approved/human_verification_stage.png');sign=(64,21,249,49)
check('Shared Pavilion sign byte-identical all four stage states',all(same(stage.crop(sign),Image.open(B/'approved'/(n+'.png')).crop(sign))for n in ['urgency_stage','locomotion_stage','surprise_stage']))
check('Unresolved source authorship retained','unresolved/unproven'in M['nativeGridAuthorshipLimitation'])

class HTML(HTMLParser):
    def __init__(self):super().__init__();self.images=[];self.links=[];self.ids=[]
    def handle_starttag(self,t,a):
        a=dict(a)
        if'id'in a:self.ids.append(a['id'])
        if t=='img':self.images.append(a)
        if t=='a':self.links.append(a['href'])
h=HTML();h.feed((B/'index.html').read_text());portable=HTML();portable.feed((B/'standalone-gallery.html').read_text())
check('Unique gallery anchors',len(h.ids)==len(set(h.ids)))
for i in h.images:check('Gallery image dimensions '+i['src'],Image.open(B/i['src']).size==(int(i['width']),int(i['height'])))
for link in h.links:
    if link.startswith('#'):check('Gallery anchor '+link,link[1:]in h.ids)
    elif not link.startswith(('http','qa/')):check('Gallery evidence link '+link,(B/link).is_file())
check('Portable same image count',len(portable.images)==len(h.images))
check('All embedded images byte-identical',all(p['src'].startswith('data:image/png;base64,')and base64.b64decode(p['src'].split(',',1)[1])==(B/n['src']).read_bytes()for p,n in zip(portable.images,h.images)))
changed=[p for p,old in base['files'].items()if sha(R/p)!=old]
check('All 1137 prior tracked files preserved',len(base['files'])==1137 and not changed)
check('Review starts from latest checked known heads',base['reviewCommit']=='9ba1028821ad83759d3c809ca74775758a4d6aef'and base['mainCommit']=='d9b6b91604b72115c5402253f00924665e957727')
check('No registration/integration/merge/deployment/Chapter4 changes',not any(M[k]for k in ['registrationPerformedByThisTask','integrationPerformed','mergePerformed','pagesDeploymentPerformed','chapter4Changes']))
report={'result':'PASS','checkCount':len(checks),'checks':checks,'priorTrackedFilesPreserved':len(base['files']),'priorFilesChanged':changed,'sceneCount':14,'newAssessments':6,'portraitPairs':15,'dialogueNodes':20,'artworkPixelsChanged':0,'portraitPixelsChanged':0,'newCandidates':0,'allRepairMasksClosed':True,'paperCanonicalStillV03':True,'pr18Merged':False,'registrationPerformedByThisTask':False}
(B/'qa/preservation.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS:',len(checks),'checks;',len(base['files']),'prior files unchanged; 14 scenes, 15 composites; zero edits.')
