from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from collections import Counter
import json,hashlib,html

ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists())
CANON='6334b895333dd2d78332cf9f1d834e619468f932'
BRANCH_BASE='60c0569856eec3c5319dcac060875054ac2e955a'
NODES=['hotel_upper_salvage_arrival','hotel_upper_salvage_clerk_directions','hotel_freight_wc_misunderstanding']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def record(rel):
    p=ROOT/rel;im=Image.open(p)
    return {'file':rel,'sha256':sha(p),'dimensions':list(im.size),'mode':im.mode}
def metrics(im):
    im=im.convert('RGB');pixels=list(im.get_flattened_data());w,h=im.size;counts=Counter(pixels);seen=set();sizes=[]
    for i,c in enumerate(pixels):
        if i in seen:continue
        todo=[i];seen.add(i);n=0
        while todo:
            k=todo.pop();n+=1;x,y=k%w,k//w
            for v in([k-1]if x else[])+([k+1]if x<w-1 else[])+([k-w]if y else[])+([k+w]if y<h-1 else[]):
                if v not in seen and pixels[v]==c:seen.add(v);todo.append(v)
        sizes.append(n)
    return {'colors':len(counts),'uniqueColorsUsedOnce':sum(n==1 for n in counts.values()),'fourConnectedColorComponents':len(sizes),'singlePixelComponents':sum(n==1 for n in sizes),'pixelsInClustersOf4OrMore':sum(n for n in sizes if n>=4),'pixelCount':w*h,'diagnosticOnly':'Counts are not artistic approval or an arbitrary palette limit.'}
def main():
    candidate='native/CH4-NEW-03-upper-salvage-v01.png';preview='previews/CH4-NEW-03-upper-salvage-v01-4x.png'
    # Resized sources are diagnostics only; the final master is constructed by
    # native_scene + native_materials, never loaded from these PNGs.
    for name in ['detailed','material']:
        im=Image.open(ROOT/f'originals/CH4-NEW-03-{name}-reference.png').convert('RGB').resize((314,206),Image.Resampling.NEAREST)
        im.save(ROOT/f'evidence/internal-study/{name}-direct-resize-DIAGNOSTIC.png')
    refs=json.loads((ROOT/'evidence/canonical-benchmarks.json').read_text());all_metrics={}
    for a in refs:
        p=ROOT/a['file'];im=Image.open(p);im.resize((1256,824),Image.Resampling.NEAREST).save(ROOT/f'previews/{p.stem}-4x.png');all_metrics[p.stem]=metrics(im)
    all_metrics['CH4-NEW-03']=metrics(Image.open(ROOT/candidate))
    (ROOT/'evidence/palette-and-clusters.json').write_text(json.dumps(all_metrics,indent=2)+'\n')
    font=ImageFont.load_default(size=13)
    def sheet(items,stem):
        sizes=[Image.open(ROOT/p).size for _,p in items];w=sum(a+16 for a,b in sizes)+8;h=max(b for a,b in sizes)+42;out=Image.new('RGB',(w,h),'#283d35');d=ImageDraw.Draw(out);x=8
        for title,p in items:
            d.text((x,8),title,font=font,fill='#f1e5c7');im=Image.open(ROOT/p);out.paste(im,(x,34));x+=im.width+16
        out.save(ROOT/f'comparisons/{stem}-native.png');out.resize((w*4,h*4),Image.Resampling.NEAREST).save(ROOT/f'comparisons/{stem}-4x.png')
    sheet([('CH4-NEW-03 candidate',candidate)]+[(p['file'].split('/')[-1][:-4],p['file'])for p in refs[:3]],'chapter2')
    sheet([('CH4-NEW-03 candidate',candidate)]+[(p['file'].split('/')[-1][:-4],p['file'])for p in refs[3:]],'chapter4')
    sheet([('Reference resize: DIAGNOSTIC','evidence/internal-study/detailed-direct-resize-DIAGNOSTIC.png'),('Native structural underpainting','evidence/internal-study/native-structural-underpainting.png'),('Final native interpretation',candidate)],'production-process')
    details=[('W.C. / three buttons',(116,67,142,109)),('Open pipework hatch',(142,82,208,125)),('Detached nested sinks',(24,135,83,182)),('Descending stair opening',(212,138,314,206))]
    items=[]
    for title,box in details:
        name=title.split()[0].replace('.','').replace('/','')
        file=f'previews/detail-{name}-native.png';im=Image.open(ROOT/candidate).crop(box);im.save(ROOT/file);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/file.replace('-native','-4x'));items.append((title,file))
    sheet(items,'story-object-details')
    nodes=json.loads((REPO/'story/chapters/chapter-04.wip.json').read_text())['nodes']
    (ROOT/'evidence/canonical-node-evidence.json').write_text(json.dumps({'canonicalCommit':CANON,'nodes':{n:nodes[n]for n in NODES},'futureReuseSceneKeys':['grand_bellevue/upper_salvage','grand_bellevue/freight_lift'],'runtimeBindingsAssigned':False,'noMandatorySuspendedStall':True,'noPeople':True},ensure_ascii=False,indent=2)+'\n')
    for name in ['generation-receipt','material-generation-receipt']:
        p=ROOT/f'evidence/{name}.json';d=json.loads(p.read_text());d['originalSha256']=sha(ROOT/d['preservedOriginal']);d['originalDimensions']=list(Image.open(ROOT/d['preservedOriginal']).size);p.write_text(json.dumps(d,indent=2)+'\n')
    manifest={'title':'Chapter4 B2-10 / CH4-NEW-03 upper salvage v01','branch':'art/ch4-b210-upper-salvage-review-20261124','reviewBaseCommit':BRANCH_BASE,'canonicalBaseline':CANON,'mainObservedAtStart':'b8a8e4ea3c6d13141b2e33d281ba864c3b2aec42','status':'UNSELECTED','selected':False,'primaryUnits':1,'supplementalStates':[],'asset':{'id':'CH4-NEW-03','proposedCanonicalKey':'scenes:grand_bellevue/upper_salvage','kind':'main-scene','native':record(candidate),'preview4x':record(preview),'nodeIds':NODES,'sourceDerived':True,'whollyIndependentAuthorshipClaim':False,'method':'Independent native structural silhouettes and pixel painting on a blank314x206 canvas; separate source-guided discrete material-cluster interpretation within those native layers; critical lettering and object sockets protected. No resized source used as finished master.','assembly':'evidence/material-interpretation.json','sourceRecipe':['source/native_scene.py','source/native_materials.py'],'exactText':'W.C.','newFocusId':None,'runtimeBinding':None},'benchmarks':refs,'provenance':'SOURCE-DERIVED hybrid native reconstruction; no source RGB pasted into master; no claim of wholly independent artwork.','approvalOrIntegrationPerformed':False,'canonicalFilesChanged':False,'visualAssessment':'evidence/visual-review.md','visualQualityGatePassed':False,'selectionReady':False,'qualityGateDisposition':'Native construction and technical review complete; illustration finish remains below strongest Chapter2 benchmark. Publish transparently as an unselected limitation review, not a selection-ready asset.','internalVisualConcern':'Rear-rack fixtures remain more schematic than the richest Chapter2 object modelling; owner visual approval is required. No technical check constitutes visual selection.'}
    (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    def fig(title,one,four):
        w,h=Image.open(ROOT/one).size
        return f'<section class="figure"><h3>{html.escape(title)}</h3><nav><button data-scale="1">Native 1×</button><button data-scale="4">Exact 4×</button><a href="{one}">PNG</a><a href="{four}">4× PNG</a></nav><div class="raster"><img src="{one}" data-one="{one}" data-four="{four}" data-w="{w}" data-h="{h}" width="{w}" height="{h}" alt="{html.escape(title)}"></div></section>'
    body='<article id="CH4-NEW-03"><h2>Single reusable scene — UNSELECTED</h2>'+fig('Candidate',candidate,preview)+f'<p class="hash">SHA-256 {manifest["asset"]["native"]["sha256"]}</p><p>One scene for all three canonical nodes. No clerk/protagonist, suspended stall, separate freight-lift image, extra state, new Focus ID or runtime binding. VISUAL GATE NOT FULLY MET: rear-rack fixture modelling remains more schematic than the strongest Chapter2 reference. This is a limitation review, not a selection-ready image; technical correctness does not establish approval.</p></article>'
    body+='<article id="comparisons"><h2>Actual native and exact4× comparisons</h2>'
    for title,stem in [('Chapter2 pixel-art benchmarks','chapter2'),('Chapter4 architectural continuity','chapter4'),('W.C., hatch, sinks and downward stairs','story-object-details'),('Production evidence — not extra candidates','production-process')]:body+=fig(title,f'comparisons/{stem}-native.png',f'comparisons/{stem}-4x.png')
    body+='</article><article id="benchmarks"><h2>Approved benchmarks individually</h2>'
    for a in refs:
        stem=Path(a['file']).stem;body+=fig(stem,a['file'],f'previews/{stem}-4x.png')
    body+='</article>'
    style='body{margin:0;background:#142820;color:#efe5c8;font:16px/1.5 system-ui,sans-serif}main{padding:22px}header,article{padding:20px;border:1px solid #647466;margin-bottom:26px}h1,h2,h3{margin:0 0 12px}a{color:#bce0c9;margin-right:16px}nav{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0}button{padding:10px;background:#435e4d;border:1px solid #b7c8ac;color:#f4e9ca;cursor:pointer}.figure{padding:14px;margin:20px 0;background:#294136}.raster{overflow:auto;max-width:100%;background:#253b32}.raster img{display:block;max-width:none!important;image-rendering:pixelated}.hash{font:13px monospace;overflow-wrap:anywhere}'
    header='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CH4 B2-10 upper salvage v01</title><style>'+style+'</style><main><header><h1>Chapter4 B2-10 · Upper salvage mezzanine v01</h1><p><strong>One UNSELECTED scene,314×206 RGB. VISUAL GATE NOT FULLY MET; not selection-ready.</strong> Freight lift and W.C. panel at left; open maintenance hatch at back; service stairs descend at right. Disconnected sanitary salvage is stored clear of the routes. Exact4× exports are1256×824.</p><p>SOURCE-DERIVED: native structural drawing and source-guided material clusters. Detailed references and diagnostic reductions are preserved, never offered as final artwork. No canonical main, selected PNG, narrative/gameplay, binding or draft PR32 change.</p><nav><a href="manifest.json">Manifest / hashes</a><a href="README.md">Method / limitations</a><a href="evidence/validation.json">QA</a><a href="evidence/visual-review.md">Visual assessment</a><a href="originals/CH4-NEW-03-detailed-reference.png">Detailed source</a><a href="originals/CH4-NEW-03-material-reference.png">Material study source</a><a href="comparisons/chapter2-4x.png">Direct Chapter2 4× comparison</a></nav></header>'
    script='<script>document.querySelectorAll("button[data-scale]").forEach(b=>b.onclick=()=>{const i=b.closest("section.figure").querySelector("img"),s=Number(b.dataset.scale);i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;});</script></main></html>'
    (ROOT/'index.html').write_text(header+body+script)
    print('Single-scene review gallery, six benchmarks, process/detail comparisons and metrics ready.')
if __name__=='__main__':main()
