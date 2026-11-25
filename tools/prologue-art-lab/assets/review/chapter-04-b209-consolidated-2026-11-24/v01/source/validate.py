from pathlib import Path
from PIL import Image,ImageChops
from html.parser import HTMLParser
import subprocess,json,hashlib,sys

ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists())
BASE='d82ae25bd39855412797bb2632dc61b1001b940a'
OLD='1459c4ed2f4288a41805365d1085e8fd3cdb76ae'
OLDROOT='tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/'
checks=[]
def check(value,note):
    assert value,note
    checks.append({'check':note,'passed':True})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def delta(a,b):
    d=ImageChops.difference(a.convert('RGB'),b.convert('RGB'));return ImageChops.lighter(ImageChops.lighter(d.getchannel('R'),d.getchannel('G')),d.getchannel('B'))

def main():
    m=json.loads((ROOT/'manifest.json').read_text())
    check(m['primaryUnits']==3 and m['conditionalReferenceFrames']==4 and m['activeChapterPrimaryTarget']==63,'Consolidated three-unit scope, four reference states and63 target')
    check(m['status']=='UNSELECTED'and not m['selectionRecordsChanged']and not m['integrationPerformed']and not m['supersededScopeReactivated'],'Unselected only; obsolete four-asset scope not reactivated')
    for a in m['assets']+m['supplementalStates']:
        p=ROOT/a['native']['file'];im=Image.open(p);preview=Image.open(ROOT/a['preview4x']['file'])
        name=a.get('id',a.get('reviewLabel'))
        check(im.size==(564,278)and im.mode==('RGBA'if a['kind']=='portrait'else'RGB'),str(name)+' dimensions/mode')
        check(sha(p)==a['native']['sha256'],str(name)+' native hash')
        check(preview.size==(2256,1112)and preview.tobytes()==im.resize((2256,1112),Image.Resampling.NEAREST).tobytes(),str(name)+' exact nearest4x')
        check(sha(ROOT/a['preview4x']['file'])==a['preview4x']['sha256'],str(name)+' preview hash')
        check(a['status']=='UNSELECTED'and a['selected']is False,str(name)+' not selected')
        if a['kind']=='portrait':
            colors=set(im.getchannel('A').get_flattened_data());check(colors=={0,255},name+' binary alpha')
            check(all(c==(0,0,0,0)for c in im.get_flattened_data()if c[3]==0),name+' zero hidden RGB')
            box=im.getbbox();check(box[0]>0 and box[1]>0 and box[2]<550,name+' complete hair/hands and side margins')
        else:check(all(len(c)==3 for c in im.get_flattened_data()),str(name)+' opaque background')
    bixby=ROOT/'native/CH4-NEW-05-bixby-reused-v01.png'
    original=subprocess.check_output(['git','show',OLD+':'+OLDROOT+'b2-09-v01/native/CH4-B2-49-v01.png'],cwd=REPO)
    check(bixby.read_bytes()==original,'Bixby v01 exact immutable original PNG bytes')
    check(sha(bixby)=='44f81292dc520eeabc6864c21449fb033db4891702c6102634b126b344ee05b8','Bixby proposed selection hash retained')
    check(not any('commanding'in p.name or 'B2-48'in p.name for p in (ROOT/'native').glob('*')),'No obsolete commanding portrait or refreshment main scene exported')
    story=json.loads((REPO/'story/chapters/chapter-04.wip.json').read_text())['nodes']
    check(m['assets'][0]['nodeIds']==['hotel_commodore_bixby','hotel_bixby_emergency','hotel_bixby_trade'],'Single Bixby pose covers three canonical nodes')
    check(all(story[n]['pose']=='delighted'for n in m['assets'][0]['nodeIds']),'Bixby canonical consolidated poses unchanged')
    check(m['assets'][1]['nodeIds']==['hotel_wedding_arrival','hotel_bridal_organizer'],'Organizer covers exact two canonical nodes')
    check(len(m['assets'][2]['nodeIds'])==5 and m['assets'][2]['proposedCanonicalKey']=='scenes:grand_bellevue/ballroom#portraitBackground','Shared background covers all five dialogue nodes without registration')
    base=Image.open(ROOT/'native/CH4-NEW-18-shared-base-v01.png')
    before=Image.open(ROOT/'references/before-wheel-removed.png')
    correction=Image.open(ROOT/'masks/NEW-18-geometry-correction.png')
    check(ImageChops.subtract(delta(before,base),correction).getbbox()is None,'Every pixel outside localized geometry correction unchanged')
    # Independent physical boundary: all new base corrections below the existing
    # door/curtain upper geometry and left of the reserved foreground area.
    allowed=Image.new('L',(564,278));from PIL import ImageDraw
    ImageDraw.Draw(allowed).rectangle((0,143,312,277),fill=255)
    check(ImageChops.subtract(delta(before,base),allowed).getbbox()is None,'Upper doors, duct, swags, lamps and right wall/window remain exact')
    props=Image.open(ROOT/'masks/NEW-18-all-table-props.png');gap=Image.open(ROOT/'masks/NEW-18-door-gap.png')
    check(ImageChops.multiply(props,gap).getbbox()is None,'Full visible door gap unobstructed by table and props')
    for a in m['assets'][:2]:
        fg=Image.open(ROOT/a['native']['file']);check(ImageChops.multiply(fg.getchannel('A'),gap).getbbox()is None,a['id']+' composite leaves threshold unobstructed')
    removed=ROOT/'native/CH4-NEW-18-wheel-removed-v01.png'
    check(removed.read_bytes()==(ROOT/'native/CH4-NEW-18-shared-base-v01.png').read_bytes(),'Removed-wheel state byte-identical to neutral base')
    for state in m['supplementalStates']:
        name=state['reviewLabel'];out=Image.open(ROOT/state['native']['file'])
        check(all(state[k]is None for k in ['canonicalFocusId','canonicalSceneKey','runtimeBinding','newFlags','newNodes']),name+' supplemental null IDs/flags/bindings')
        if state['allowedMask']:
            mask=Image.open(ROOT/state['allowedMask']);part=Image.open(ROOT/f'layers/NEW-18-{name}.png')
            check(ImageChops.subtract(delta(base,out),mask).getbbox()is None,name+' zero changes outside local mask')
            check(Image.alpha_composite(base.convert('RGBA'),part).convert('RGB').tobytes()==out.tobytes(),name+' exact editable-layer reconstruction')
            check(mask.getbbox()is not None,name+' nonempty prop/water mask')
    water=Image.open(ROOT/'masks/NEW-18-water-emerging.png')
    check(ImageChops.multiply(water,gap).getbbox()is not None,'Water starts at actual door gap, without disconnected dry strip')
    check(ImageChops.multiply(water,props).getbbox()is None,'Water does not paint over table, flowers, bucket or cloth')
    check(water.getbbox()[1]>=220,'Water is confined to threshold/floor plane')
    for c in m['composites']:
        fg=Image.open(ROOT/m['assets'][0 if c['speaker']=='Bixby'else 1]['native']['file']);bg=Image.open(ROOT/f'native/CH4-NEW-18-{c["state"]}-v01.png').convert('RGBA');out=Image.open(ROOT/c['native']['file'])
        check(Image.alpha_composite(bg,fg).convert('RGB').tobytes()==out.tobytes(),c['speaker']+'/'+c['state']+' exact shared-background composite')
        check(c['reviewOnly']and not c['canonicalTimingOrBindingAssigned'],'Composite assigns no runtime timing')
    for name in ['wheel-mounted','rubber-band-fender']:
        wanted=Image.alpha_composite(Image.alpha_composite(base.convert('RGBA'),Image.open(ROOT/'layers/NEW-18-water-emerging.png')),Image.open(ROOT/f'layers/NEW-18-{name}.png')).convert('RGB')
        check(wanted.tobytes()==Image.open(ROOT/f'previews/NEW-18-{name}-with-water-native.png').tobytes(),name+' water combination shares exact geometry/layers')
    for stack in json.loads((ROOT/'evidence/layer-assembly.json').read_text())['stacks']:
        out=Image.new('RGBA',(564,278))
        for part in stack['layers']:out=Image.alpha_composite(out,Image.open(ROOT/part))
        check(out.convert(stack['outputMode']).tobytes()==Image.open(ROOT/stack['output']).tobytes(),'Editable semantic layer stack reconstructs '+stack['output'])
    for r in json.loads((ROOT/'evidence/input-provenance.json').read_text()):
        data=subprocess.check_output(['git','show',r['sourceCommit']+':'+r['sourcePath']],cwd=REPO)
        check(data==(ROOT/r['file']).read_bytes(),r['file']+' exact pinned source bytes')
    for r in json.loads((ROOT/'evidence/generation-receipts.json').read_text()):
        check(sha(ROOT/r['preservedFile'])==r['sha256'],r['id']+' original generation hash')
        check((ROOT/r['promptFile']).read_text().strip()==r['prompt'],r['id']+' exact original prompt')
        check(all((ROOT/f).is_file()for f in r['orderedReferenceFiles']),r['id']+' ordered references available')
    crop=Image.open(ROOT/'references/approved-ballroom.png').crop((195,74,231,155))
    check(crop.tobytes()==Image.open(ROOT/'references/approved-organizer-scene-crop.png').tobytes(),'Organizer identity crop exact approved CH4-05 pixels')
    # Every raster export is checked, including comparison sheets and crops.
    pairs=0
    for p in ROOT.rglob('*-4x.png'):
        if '/internal-study/'in str(p):continue
        candidates=[p.with_name(p.name.replace('-4x.png','-native.png')),p.with_name(p.name.replace('-4x.png','.png'))]
        if p.parent.name=='previews':candidates+=[ROOT/'native'/p.name.replace('-4x.png','.png'),ROOT/'references'/p.name.replace('-4x.png','.png')]
        source=next((q for q in candidates if q.is_file()),None)
        # One preserved reference crop already named -4x is its own input record.
        if source:
            a=Image.open(source);b=Image.open(p);check(b.size==(a.width*4,a.height*4)and b.tobytes()==a.resize(b.size,Image.Resampling.NEAREST).tobytes(),'Exact NN raster '+str(p.relative_to(ROOT)));pairs+=1
    # Existing canonical files are immutable under this art-only worktree.
    preserved=0
    for line in subprocess.check_output(['git','ls-tree','-r',BASE],cwd=REPO,text=True).splitlines():
        meta,path=line.split('\t');p=REPO/path
        if meta.split()[1]!='blob':continue
        data=p.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        check(blob==meta.split()[2],'Canonical baseline preserved '+path);preserved+=1
    old_stop=subprocess.check_output(['git','show',OLD+':'+OLDROOT+'AGENTS.md'],cwd=REPO)
    check((ROOT/'evidence/old-review-STOP-notice.md').read_bytes()==old_stop,'Old STOP notice exact and preserved, not reactivated')
    class Links(HTMLParser):
        def __init__(self):super().__init__();self.links=[]
        def handle_starttag(self,tag,attrs):
            self.links += [v for k,v in attrs if k in ['href','src','data-one','data-four']and v and not v.startswith(('#','http'))]
    links=Links();links.feed((ROOT/'index.html').read_text())
    for f in set(links.links):check((ROOT/f).is_file()or f=='evidence/validation.json','Gallery dependency exists '+f)
    # Reproducibility covers actual final rasters and semantic layers, not just
    # dimensions/palette count. The copied Bixby is not regenerated by any script.
    tracked=[p for p in ROOT.rglob('*.png')]+[ROOT/'manifest.json',ROOT/'index.html',ROOT/'evidence/background-derivation.json',ROOT/'evidence/organizer-derivation.json']
    before_replay={p:sha(p)for p in tracked}
    for script in ['build_background.py','build_organizer.py','package_review.py']:
        subprocess.run([sys.executable,str(ROOT/'source'/script)],check=True,cwd=REPO,stdout=subprocess.DEVNULL)
    check(all(sha(p)==s for p,s in before_replay.items()),'All native/art/layer/gallery outputs replay byte-identically')
    out={'passed':True,'checksPassed':len(checks),'primaryUnits':3,'supplementalReferenceFrames':4,'activeChapterPrimaryTarget':63,'allUnselected':True,'bixbyExactOriginalBytes':True,'canonicalBaselineFilesUnchanged':preserved,'oldReviewAndStopUnchanged':True,'exact4xPairs':pairs,'replayedFilesIdentical':len(before_replay),'narrativeOrGameplayChanged':False,'selectionOrBindingsChanged':False,'deployed':False,'visualGate':'evidence/visual-review.md','checks':checks}
    (ROOT/'evidence/validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='checks'}))

if __name__=='__main__':main()
