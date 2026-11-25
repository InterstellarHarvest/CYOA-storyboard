from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json,html,subprocess

ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists())
BASE='d82ae25bd39855412797bb2632dc61b1001b940a'
STATES=['wheel-mounted','wheel-removed','rubber-band-fender','water-emerging']
NODES=['hotel_wedding_arrival','hotel_bridal_organizer','hotel_commodore_bixby','hotel_bixby_emergency','hotel_bixby_trade']

def record(rel):
    p=ROOT/rel;im=Image.open(p)
    return {'file':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'dimensions':list(im.size),'mode':im.mode}

def main():
    for p in sorted((ROOT/'native').glob('*.png')):
        im=Image.open(p);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/'previews'/(p.stem+'-4x.png'))
    for p in sorted((ROOT/'references').glob('*.png')):
        im=Image.open(p);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/'previews'/(p.stem+'-4x.png'))
    assets=[]
    for id_,title,kind,key,nodes,f in [
        ('CH4-NEW-05','Commodore Bixby — unchanged single portrait','portrait','portraits:hotel_commodore_bixby:delighted',NODES[2:],'CH4-NEW-05-bixby-reused-v01.png'),
        ('CH4-NEW-06','Wedding organizer — urgent / briskly kind','portrait','portraits:hotel_wedding_organizer:urgent',NODES[:2],'CH4-NEW-06-organizer-urgent-v01.png'),
        ('CH4-NEW-18','Shared ballroom threshold — neutral base','portrait_background','scenes:grand_bellevue/ballroom#portraitBackground',NODES,'CH4-NEW-18-shared-base-v01.png')]:
        assets.append({'id':id_,'title':title,'kind':kind,'proposedCanonicalKey':key,'nodeIds':nodes,'status':'UNSELECTED','selected':False,'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'reusedByteForByte':id_=='CH4-NEW-05','native':record('native/'+f),'preview4x':record('previews/'+Path(f).stem+'-4x.png')})
    conditions={
        'wheel-mounted':('hotel_commodore_bixby','Initial Bixby beat: brass plumbing valve wheel mounted on the silver ice bucket.'),
        'wheel-removed':('hotel_bixby_emergency','After handoff: bucket remains, wheel absent. Identical to neutral shared base; also suitable as organizer context.'),
        'rubber-band-fender':('hotel_bixby_trade','After trade/handoff: wheel absent, approved-design rubber-band sphere tied to bucket with a napkin.'),
        'water-emerging':('hotel_commodore_bixby','Thin water sheet emerges directly at the ballroom door gap. Combinable with any prop state; actual timing deferred.')}
    states=[]
    for name in STATES:
        node,condition=conditions[name];f=f'CH4-NEW-18-{name}-v01.png'
        states.append({'reviewLabel':name,'kind':'supplemental-production-reference','status':'UNSELECTED','selected':False,'canonicalFocusId':None,'canonicalSceneKey':None,'runtimeBinding':None,'newFlags':None,'newNodes':None,'nodeIds':[node],'condition':condition,'implementationBoundary':'Review reference only; no prescribed conditional dispatch, timing, Focus ID or runtime binding. Water may combine with the three prop states.','native':record('native/'+f),'preview4x':record('previews/'+Path(f).stem+'-4x.png'),'allowedMask':None if name=='wheel-removed'else f'masks/NEW-18-{name}.png'})
    comps=[]
    for person,file in [('Bixby','CH4-NEW-05-bixby-reused-v01.png'),('Organizer','CH4-NEW-06-organizer-urgent-v01.png')]:
        for state in STATES:
            bg=Image.open(ROOT/f'native/CH4-NEW-18-{state}-v01.png').convert('RGBA');fg=Image.open(ROOT/'native'/file);im=Image.alpha_composite(bg,fg).convert('RGB');stem=f'{person.lower()}-{state}';im.save(ROOT/f'previews/{stem}-native.png');im.resize((2256,1112),Image.Resampling.NEAREST).save(ROOT/f'previews/{stem}-4x.png');comps.append({'speaker':person,'state':state,'reviewOnly':True,'canonicalTimingOrBindingAssigned':False,'native':record(f'previews/{stem}-native.png'),'preview4x':record(f'previews/{stem}-4x.png')})
    for name in['wheel-mounted','rubber-band-fender']:
        p=ROOT/f'previews/NEW-18-{name}-with-water-native.png';im=Image.open(p);im.resize((2256,1112),Image.Resampling.NEAREST).save(ROOT/f'previews/NEW-18-{name}-with-water-4x.png')
    font=ImageFont.load_default(size=14)
    def sheet(items,stem):
        sizes=[Image.open(ROOT/p).size for _,p in items];w=sum(s[0]+16 for s in sizes)+8;h=max(s[1]for s in sizes)+44;out=Image.new('RGB',(w,h),'#273b36');d=ImageDraw.Draw(out);x=8
        for label,p in items:
            d.text((x,9),label,font=font,fill='#eee2c0');im=Image.open(ROOT/p).convert('RGBA');out.paste(im,(x,36),im);x+=im.width+16
        out.save(ROOT/f'comparisons/{stem}-native.png');out.resize((w*4,h*4),Image.Resampling.NEAREST).save(ROOT/f'comparisons/{stem}-4x.png')
    sheet([('Before: doors obscured','references/before-wheel-removed.png'),('NEW-18: threshold exposed','native/CH4-NEW-18-shared-base-v01.png')],'before-after')
    sheet([(s.replace('-',' '),f'native/CH4-NEW-18-{s}-v01.png')for s in STATES],'four-states')
    sheet([('Bixby / wheel','previews/bixby-wheel-mounted-native.png'),('Bixby / wheel handed over','previews/bixby-wheel-removed-native.png'),('Bixby / rubber-band fender','previews/bixby-rubber-band-fender-native.png'),('Organizer / shared neutral base','previews/organizer-wheel-removed-native.png')],'speaker-composites')
    sheet([('NEW-18 shared threshold','native/CH4-NEW-18-shared-base-v01.png'),('Approved Ch2 Bureau','references/approved-bureau.png'),('Approved Ch2 Tower','references/approved-tower.png'),('Approved CH4-05 ballroom','references/approved-ballroom.png'),('Approved CH4 service background','references/approved-service-background.png')],'background-approved-benchmarks')
    sheet([('NEW-06 organizer','native/CH4-NEW-06-organizer-urgent-v01.png'),('Ch2 cluster benchmark: conductor robot','references/approved-ch2-conductor.png'),('Ch2 material benchmark: groundskeeper robot','references/approved-ch2-groundskeeper.png'),('Approved Pavilion attendant','references/approved-attendant.png'),('Approved Pavilion presenter','references/approved-presenter.png'),('Approved Ch4 engineer','references/approved-engineer.png'),('Identity: approved CH4-05 organizer','references/approved-organizer-scene-crop.png')],'organizer-approved-benchmarks')
    sheet([('NEW-05 exact reused Bixby','native/CH4-NEW-05-bixby-reused-v01.png'),('Approved Ch2 conductor','references/approved-ch2-conductor.png'),('Approved Pavilion attendant','references/approved-attendant.png'),('Approved Ch4 auctioneer','references/approved-auctioneer-delighted.png')],'bixby-approved-benchmarks')
    for name,file in [('before','references/before-wheel-removed.png'),('corrected','native/CH4-NEW-18-shared-base-v01.png'),('water','native/CH4-NEW-18-water-emerging-v01.png')]:
        Image.open(ROOT/file).crop((0,135,115,278)).save(ROOT/f'previews/threshold-{name}-detail-native.png')
    sheet([(name,f'previews/threshold-{name}-detail-native.png')for name in['before','corrected','water']],'threshold-detail')
    for name,file,box in [('before','references/before-fender.png',(172,203,225,259)),('new','native/CH4-NEW-18-rubber-band-fender-v01.png',(215,200,268,256))]:
        Image.open(ROOT/file).crop(box).save(ROOT/f'previews/fender-{name}-detail-native.png')
    sheet([('Previous fender','previews/fender-before-detail-native.png'),('Native wrapped ball + napkin','previews/fender-new-detail-native.png'),('Approved rubber-band ball inspect','references/approved-rubber-band-ball.png')],'fender-before-after')
    # Detail crops are native pixels, never resampled to match source scale.
    for p in (ROOT/'previews').glob('*-detail-native.png'):
        im=Image.open(p);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(p.with_name(p.name.replace('-native','-4x')))
    nodes=json.loads((REPO/'story/chapters/chapter-04.wip.json').read_text())['nodes']
    (ROOT/'evidence/canonical-node-evidence.json').write_text(json.dumps({'sourceCommit':BASE,'nodes':{k:nodes[k]for k in NODES},'canonicalStoryChanged':False,'supplementalBindingsAdded':False},ensure_ascii=False,indent=2)+'\n')
    manifest={'title':'Consolidated Chapter4 B2-09 review v01','branch':'art/ch4-b209-consolidated-review-20261124','canonicalMain':BASE,'draftPR32ReadOnly':'f320e63934c13e27fd13b9482d0cfba58911362d','activeChapterPrimaryTarget':63,'status':'UNSELECTED','primaryUnits':3,'conditionalReferenceFrames':4,'assets':assets,'supplementalStates':states,'composites':comps,'integrationPerformed':False,'selectionRecordsChanged':False,'mainDeploymentPerformed':False,'oldReviewPackageUnchanged':True,'oldStopNoticePreserved':True,'supersededScopeReactivated':False,'nativeContract':[564,278],'method':'Source-derived localized native reconstruction and intentional material/contour/prop layers; original Bixby bytes reused; no independent whole-image native authorship claim.'}
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    def fig(title,one,four):
        w,h=Image.open(ROOT/one).size
        return f'<section class="figure"><h3>{html.escape(title)}</h3><nav><button data-scale="1">Native 1×</button><button data-scale="4">Exact 4×</button><a href="{one}">PNG</a><a href="{four}">4× PNG</a></nav><div class="raster"><img src="{one}" data-one="{one}" data-four="{four}" data-w="{w}" data-h="{h}" width="{w}" height="{h}" alt="{html.escape(title)}"></div></section>'
    body='<article id="overview"><h2>Threshold correction and localized states</h2>'
    for title,stem in [('Before / corrected background','before-after'),('Wheel / removed / fender / water','four-states'),('Door edge, gap and water source','threshold-detail'),('Both speakers over the shared room','speaker-composites'),('Fender correction and approved object identity','fender-before-after')]:body+=fig(title,f'comparisons/{stem}-native.png',f'comparisons/{stem}-4x.png')
    body+='</article>'
    for a in assets:
        body+=f'<article id="{a["id"]}"><h2>{html.escape(a["title"])}</h2><p><strong>UNSELECTED</strong> · {html.escape(a["proposedCanonicalKey"])} · proposed coverage: {html.escape(", ".join(a["nodeIds"]))}</p><p class="hash">SHA-256 {a["native"]["sha256"]}</p>'+fig('Candidate',a['native']['file'],a['preview4x']['file'])
        stem='bixby-approved-benchmarks'if a['id']=='CH4-NEW-05'else'organizer-approved-benchmarks'if a['id']=='CH4-NEW-06'else'background-approved-benchmarks'
        body+=fig('Approved canonical comparisons',f'comparisons/{stem}-native.png',f'comparisons/{stem}-4x.png')
        if a['kind']=='portrait':
            person='bixby'if a['id']=='CH4-NEW-05'else'organizer';used=STATES[:3]if person=='bixby'else['wheel-removed']
            for state in used:body+=fig(f'{person.title()} / {state} — review composite',f'previews/{person}-{state}-native.png',f'previews/{person}-{state}-4x.png')
        body+='</article>'
    for s in states:
        body+=f'<article id="state-{s["reviewLabel"]}"><h2>{s["reviewLabel"]}</h2><p><strong>UNSELECTED supplemental production reference</strong> · {html.escape(s["condition"])} No new canonical Focus ID, scene, flag, node or runtime binding.</p>'+fig('Localized state',s['native']['file'],s['preview4x']['file'])+'</article>'
    for state in['wheel-mounted','rubber-band-fender']:
        body+=fig('Review-only combination: '+state+' + water',f'previews/NEW-18-{state}-with-water-native.png',f'previews/NEW-18-{state}-with-water-4x.png')
    style='body{margin:0;background:#142821;color:#f3e5c7;font:16px/1.5 system-ui,sans-serif}main{padding:22px}header,article{margin-bottom:30px;padding:20px;border:1px solid #65776a}h1,h2,h3{margin:0 0 12px}a{color:#bde1ce;margin-right:16px}nav{display:flex;flex-wrap:wrap;gap:12px;margin:14px 0}button{background:#435d4e;color:#fff1cf;border:1px solid #b0bfa9;padding:10px;cursor:pointer}.raster{overflow:auto;max-width:100%;background:repeating-conic-gradient(#344e41 0 25%,#3c5549 0 50%) 0/12px 12px}.raster img{display:block;image-rendering:pixelated;max-width:none!important}.figure{margin:22px 0;padding:14px;background:#294136;min-width:0}.hash{font:13px monospace;overflow-wrap:anywhere}'
    header='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Consolidated CH4 B2-09 v01</title><style>'+style+'</style><main><header><h1>Consolidated Chapter 4 B2-09 v01</h1><p><strong>Everything UNSELECTED.</strong> Three primary units: exact reused Bixby, one wedding organizer, one shared ballroom-threshold background. Four localized state references. Active chapter target remains63.</p><p>Lower door edges and gap are exposed beside the relocated table; water originates at the threshold. Wheel/fender changes share the same room geometry. The old B2-09 package and STOP notice remain untouched. No commanding portrait, redundant main scene, canonical selection, binding, PR32 merge or deployment.</p><nav><a href="manifest.json">Manifest / hashes</a><a href="README.md">Sources / native method / scope</a><a href="evidence/validation.json">QA</a><a href="evidence/visual-review.md">Visual assessment</a><a href="originals/CH4-NEW-06-organizer-detailed.png">Organizer source</a><a href="originals/NEW-18-clean-room-underdrawing.png">Occluded-room reference</a></nav></header>'
    script='<script>document.querySelectorAll("button[data-scale]").forEach(b=>b.onclick=()=>{const i=b.closest("section.figure").querySelector("img"),s=Number(b.dataset.scale);i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;});</script></main></html>'
    (ROOT/'index.html').write_text(header+body+script)
    print('Consolidated three-unit gallery, localized states and exact4x comparison exports ready.')

if __name__=='__main__':main()
