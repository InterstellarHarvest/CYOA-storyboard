from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops
import json, hashlib, html

ROOT=Path(__file__).resolve().parents[1]
V1=ROOT.parent/'v01'
BASE='436e83f43c01b0a64620056d44aabf14c61fb444'
PARENT='da17468f1ca8f1b0aaa61b6ce7f981336edaa6ce'
BRANCH='art/ch4-b214-native-review-20261125'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(f):
    im=Image.open(ROOT/f)
    return {'file':f,'sha256':sha(ROOT/f),'dimensions':list(im.size),'mode':im.mode}
def four(f):
    im=Image.open(ROOT/f);out='previews/'+Path(f).stem+'-4x.png'
    im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/out)
    return out

def main():
    native='native/CH4-NEW-02-bridal-lavatory-v02.png'
    old='references/lavatory-v01-UNCHANGED.png'
    focus='references/seashells-v01-UNCHANGED.png'
    (ROOT/old).write_bytes((V1/'native/CH4-NEW-02-bridal-lavatory-v01.png').read_bytes())
    (ROOT/focus).write_bytes((V1/'native/CH4-NEW-09-three-seashells-v01.png').read_bytes())
    for f in (ROOT/'references').glob('*.png'):four(str(f.relative_to(ROOT)))
    refs=[r for r in json.loads((V1/'evidence/benchmark-provenance.json').read_text()) if (ROOT/r['file']).exists()]
    (ROOT/'evidence/benchmark-provenance.json').write_text(json.dumps(refs,indent=2)+'\n')
    font=ImageFont.load_default(size=13);labels=[]
    def sheet(name,items):
        sizes=[Image.open(ROOT/f).size for label,f in items]
        widths=[max(w+24,int(font.getlength(label))+24)for(label,f),(w,h)in zip(items,sizes)]
        out=Image.new('RGB',(sum(widths)+8,max(h for w,h in sizes)+54),'#263a32');d=ImageDraw.Draw(out);x=8
        for(label,f),w in zip(items,widths):
            d.text((x+8,10),label,font=font,fill='#efe3bf');out.paste(Image.open(ROOT/f).convert('RGB'),(x+8,42))
            labels.append({'caption':label,'fits':font.getlength(label)<w-16});x+=w
        p='comparisons/'+name+'-native.png';out.save(ROOT/p);four(p);return p
    before=sheet('lavatory-v01-v02',[('v01 - preserved',old),('v02 - UNSELECTED',native)])
    ch2=sheet('lavatory-chapter2',[('B2-14 v02 - UNSELECTED',native),('Approved Chapter 2 Bureau','references/approved-ch2-bureau.png'),('Approved Chapter 2 Control Tower','references/approved-ch2-control-tower.png')])
    hotel=sheet('hotel-continuity',[('B2-14 v02 lavatory',native),('Approved B2-12 dressing room','references/approved-b212-dressing-room.png')])
    pair=sheet('frozen-focus-continuity',[('Refined room only',native),('v01 Focus - unchanged',focus)])
    previous=Image.open(ROOT/old);current=Image.open(ROOT/native)
    delta=ImageChops.difference(previous,current).convert('L').point(lambda v:255 if v else 0)
    # RGB differences may theoretically cancel in luminance; use per-channel max.
    bands=ImageChops.difference(previous,current).split()
    delta=ImageChops.lighter(ImageChops.lighter(bands[0],bands[1]),bands[2]).point(lambda v:255 if v else 0)
    delta.save(ROOT/'masks/v01-v02-changed-pixels.png')
    (ROOT/'evidence/change-region.json').write_text(json.dumps({'changedPixels':sum(v==255 for v in delta.get_flattened_data()),'totalPixels':314*206,'bbox':delta.getbbox(),'shellGeometryAndOpaquePixelsPreserved':True,'counterTopPolygon':[[94,94],[220,94],[242,104],[72,104]],'floorVanishingPoint':[157,65],'roomBoundaries':{'near':[22,8,292,185],'back':[67,27,247,145]}},indent=2)+'\n')
    (ROOT/'evidence/caption-layout.json').write_text(json.dumps(labels,indent=2)+'\n')
    original=rec('originals/lavatory-detailed-reference.png')
    provenance={'sourceDerivedDesign':True,'nativeRasterConstructedIndependently':True,'sourcePixelsTransferred':False,'whollyIndependentCreativeDesign':False,'newImageGeneration':False,'referenceTool':'Built-in image_gen.imagegen, inherited v01 reference','referenceOriginal':original,'referencePrompt':'source/lavatory-reference-prompt.txt','referencePromptSha256':sha(ROOT/'source/lavatory-reference-prompt.txt'),'referenceGenerationRecordCommit':PARENT,'referenceGenerationRecord':'../v01/evidence/generation-provenance.json','nativeParent':'v01/source/build.py','nativeParentSha256':sha(ROOT/'source/base_native.py'),'nativeMethod':'Native material-specific illustration over fixed v01 geometry. source/refine.py paints surfaces and light directly at 314x206; source/base_native.py reproduces the original shell layers. No large image is read, resized, sharpened or sampled by either renderer.','changes':['Modeled plaster moldings and fixed raised wall paneling','Perspective-correct individual tiles with grout and broken warm reflections','Stone slab arris, sparse mineral veins and contact shadows','Folded duct seams, fasteners, grille lips and support shadows','Milky lamp glass with warm local plaster illumination','Clean repaired joints and minor old metal coating wear']}
    (ROOT/'evidence/provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    m={'title':'B2-14 v02 - bridal lavatory material and lighting refinement','status':'UNSELECTED','ownerApproved':False,'selected':False,'branch':BRANCH,'canonicalBaseline':BASE,'preservationBaseline':PARENT,'primaryAssetCount':1,'focusRevised':False,'assets':[{'id':'CH4-NEW-02','label':'Bridal lavatory','version':'v02','status':'UNSELECTED','ownerApproved':False,'selected':False,'native':rec(native),'exact4x':rec(four(native)),'proposedCanonicalKey':'scenes:grand_bellevue/bridal_lavatory','runtimeBinding':None,'canonicalAssetPath':None,'nodes':['hotel_seashell_room'],'sourceDerivedDesign':True,'nativeRasterConstructedIndependently':True,'sourcePixelsTransferred':False}],'unchangedFocus':rec(focus),'unchangedPreviousRoom':rec(old),'references':refs,'newRuntimeModes':0,'registryModified':False,'narrativeGameplayOrEngineModified':False,'constraints':{'visibleOrConcealedPlumbingFixture':False,'additionalTechnology':False,'npcOrAiFace':False,'decorativeClutter':False,'shellCount':3,'shellArrangementChanged':False,'counterPlacementChanged':False,'perspectiveChanged':False}}
    (ROOT/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    def fig(title,f):
        im=Image.open(ROOT/f);p='previews/'+Path(f).stem+'-4x.png'
        return f'<section class="figure"><h3>{html.escape(title)}</h3><nav><button data-scale="1">Native 1×</button><button data-scale="4">Exact 4×</button><a href="{f}">Native PNG</a><a href="{p}">4× PNG</a></nav><div class="raster"><img src="{f}" data-one="{f}" data-four="{p}" data-w="{im.width}" data-h="{im.height}" width="{im.width}" height="{im.height}" alt="{html.escape(title)}"></div></section>'
    css='body{margin:0;background:#172a23;color:#efe5c8;font:16px/1.55 system-ui,sans-serif}main{padding:22px}header,article{padding:20px;border:1px solid #697c6d;margin-bottom:26px}h1,h2,h3{margin:0 0 12px}a{color:#c5dfca;margin-right:14px}nav{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0}button{padding:10px;background:#435e4d;border:1px solid #bacbaa;color:#fff0ca;cursor:pointer}.figure{padding:14px;margin:20px 0;background:#294136}.raster{overflow:auto;max-width:100%;background:#253b32}.raster img{display:block;max-width:none!important;image-rendering:pixelated}p{max-width:1120px}'
    head='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>B2-14 v02 · Bridal lavatory</title><style>'+css+'</style><main><header><h1>B2-14 v02 · Bridal lavatory</h1><p><strong>One revised candidate · UNSELECTED.</strong> 314×206 opaque RGB. Fixed composition, room perspective, counter position and exact original shell layers. Both v01 images are preserved; the separate seashell Focus is not revised.</p><p>A cohesive native material-and-lighting pass: dimensional moldings and paneling, perspective-correct tile/grout and restrained reflections, modeled stone thickness and bracket shadows, folded duct seams and fasteners, warm lamp illumination, clean repaired architectural joints. No new fixture, technology, person, AI face or decorative object.</p><nav><a href="#room">v02</a><a href="#comparisons">Before / after</a><a href="#benchmarks">Canonical benchmarks</a><a href="manifest.json">Manifest / hashes</a><a href="evidence/validation.json">QA</a><a href="README.md">Method / assessment</a><a href="source/refine.py">Editable native recipe</a><a href="evidence/native-layer-recipes.json">Native layers</a><a href="evidence/provenance.json">Provenance</a><a href="originals/lavatory-detailed-reference.png">Preserved reference original</a></nav><p>Controls use actual native or pre-exported nearest-neighbor 4× rasters at integer dimensions. Wide comparisons scroll horizontally. Technical validation does not confer artistic approval.</p></header>'
    body='<article id="room"><h2>CH4-NEW-02 · v02 · UNSELECTED</h2>'+fig('Spotless lavatory - native material refinement',native)+'</article>'
    body+='<article id="comparisons"><h2>Before / after and hotel continuity</h2>'+fig('v01 preserved / v02 candidate',before)+fig('Approved Chapter 2 comparison',ch2)+fig('Approved dressing-room continuity',hotel)+fig('Refined room / unchanged three-seashell Focus',pair)+'</article>'
    body+='<article id="benchmarks"><h2>Actual approved canonical PNGs · unchanged</h2>'
    for r in refs:body+=fig(r['role'],r['file'])
    body+='</article><article id="shells"><h2>Separate Focus · v01 · unchanged reference only</h2><p>This is an exact copy for continuity review. It is not a revised or additional candidate.</p>'+fig('Original three-seashell Focus - unchanged',focus)+'</article>'
    script='<script>document.querySelectorAll("button[data-scale]").forEach(b=>b.onclick=()=>{const i=b.closest("section.figure").querySelector("img"),s=Number(b.dataset.scale);i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;});</script></main></html>'
    (ROOT/'index.html').write_text(head+body+script)

if __name__=='__main__':main()
