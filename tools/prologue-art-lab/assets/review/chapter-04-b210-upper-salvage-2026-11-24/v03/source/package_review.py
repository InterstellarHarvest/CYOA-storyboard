from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
import json,hashlib,html

ROOT=Path(__file__).resolve().parents[1];V01=ROOT.parent/'v01'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(rel):
    p=ROOT/rel;im=Image.open(p);return {'file':rel,'sha256':sha(p),'dimensions':list(im.size),'mode':im.mode}
def main():
    for p in(ROOT/'references').glob('*.png'):
        im=Image.open(p);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/'previews'/(p.stem+'-4x.png'))
    before='references/v02-before.png';original='references/v01-before.png';after='native/CH4-NEW-03-upper-salvage-v03.png'
    font=ImageFont.load_default(size=13);layout=[]
    def sheet(items,name):
        dims=[Image.open(ROOT/p).size for title,p in items]
        widths=[max(w+16,int(font.getlength(title))+16)for(title,p),(w,h)in zip(items,dims)]
        canvas=Image.new('RGB',(sum(widths)+8,max(h for w,h in dims)+44),'#283d35');d=ImageDraw.Draw(canvas);x=8
        for(title,p),width in zip(items,widths):
            d.text((x+4,8),title,font=font,fill='#f0e4c4');im=Image.open(ROOT/p);canvas.paste(im,(x+4,36));layout.append({'sheet':name,'caption':title,'textWidth':font.getlength(title),'panelWidth':width,'fits':font.getlength(title)<=width-8});x+=width
        canvas.save(ROOT/f'comparisons/{name}-native.png');canvas.resize((canvas.width*4,canvas.height*4),Image.Resampling.NEAREST).save(ROOT/f'comparisons/{name}-4x.png')
    sheet([('v01 original rack',original),('v02 quieter rack',before),('v03 fuller rack',after)],'v01-v02-v03')
    sheet([('v02',before),('v03',after),('Ch2 Control Tower','references/ch2-control-tower.png'),('Ch2 Maintenance Exit','references/ch2-maintenance-exit.png'),('Ch4 Service Stairs','references/ch4-service-stairs.png')],'quick-glance')
    sheet([('v03',after),('Ch2 Damaged Walkway','references/ch2-damaged-walkway.png'),('Ch4 Loading Dock','references/ch4-loading-dock.png')],'additional-benchmarks')
    for name,box in [('rack',(210,41,314,140)),('sinks',(24,133,90,190)),('stairs',(203,108,314,206))]:
        items=[]
        for version,file in ([('v01',original),('v02',before),('v03',after)] if name=='rack' else [('v02',before),('v03',after)]):
            rel=f'previews/{version}-{name}-native.png';im=Image.open(ROOT/file).crop(box);im.save(ROOT/rel);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/rel.replace('-native','-4x'));items.append((version+' '+name,rel))
        sheet(items,name+'-before-after')
    (ROOT/'evidence/caption-layout.json').write_text(json.dumps(layout,indent=2)+'\n')
    a=Image.open(ROOT/before);b=Image.open(ROOT/after);delta=ImageChops.difference(a,b);mask=ImageChops.lighter(ImageChops.lighter(delta.getchannel('R'),delta.getchannel('G')),delta.getchannel('B')).point(lambda p:255 if p else 0);mask.save(ROOT/'masks/actual-changes.png')
    changes=sum(p!=q for p,q in zip(a.get_flattened_data(),b.get_flattened_data()))
    manifest={'title':'Chapter4 B2-10 v03 — fuller rack, original stairs','branch':'art/ch4-b210-upper-salvage-review-20261124','preservationBaseline':'29a23f13ca8824bae3868b46c2afb19f075f7651','baseReviewCommit':'29a23f13ca8824bae3868b46c2afb19f075f7651','canonicalBaseline':'6334b895333dd2d78332cf9f1d834e619468f932','status':'UNSELECTED','ownerApproved':False,'primaryUnits':1,'supplementalStates':[],'asset':{'id':'CH4-NEW-03','proposedCanonicalKey':'scenes:grand_bellevue/upper_salvage','native':rec(after),'preview4x':rec('previews/CH4-NEW-03-upper-salvage-v03-4x.png'),'nodeIds':['hotel_upper_salvage_arrival','hotel_upper_salvage_clerk_directions','hotel_freight_wc_misunderstanding'],'runtimeBinding':None,'newFocusId':None},'sourceDerived':True,'independentlyAuthoredWholeImage':False,'targetedVisualImprovement':'Owner-requested combination: exact v02 foreground sinks, fuller v01 rack arrangement reinterpreted with the recent local porcelain treatment. Original stairwell and rails restored exactly, per owner fallback. Perspective ambiguity is documented rather than claimed fixed. Everything outside the rack stays pixel-exact v02.','comparisonBaseVersion':'v02','changedNativePixels':changes,'unchangedScenePercent':round(100*(1-changes/(314*206)),3),'noGeneralRelightingOrPalettePass':True,'newImageGeneration':False,'approvedProductionFilesChanged':False,'gameplayNarrativeBindingsChanged':False,'repairRecipe':'source/refine_existing.py','provenance':'Original detailed concept used only for localized fixture underpainting/ramp interpretation; native mask/edge/socket/contact repairs and a native-to-native approved bowl fragment. Some reference-defined contours remain. No wholly independent native authorship claim.'}
    (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    def fig(title,one,four):
        w,h=Image.open(ROOT/one).size
        return f'<section class="figure"><h3>{html.escape(title)}</h3><nav><button data-scale="1">Native 1×</button><button data-scale="4">Exact 4×</button><a href="{one}">PNG</a><a href="{four}">4× PNG</a></nav><div class="raster"><img src="{one}" data-one="{one}" data-four="{four}" data-w="{w}" data-h="{h}" width="{w}" height="{h}" alt="{html.escape(title)}"></div></section>'
    css='body{margin:0;background:#142820;color:#efe5c8;font:16px/1.5 system-ui,sans-serif}main{padding:22px}header,article{padding:20px;border:1px solid #647466;margin-bottom:26px}h1,h2,h3{margin:0 0 12px}a{color:#bce0c9;margin-right:16px}nav{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0}button{padding:10px;background:#435e4d;border:1px solid #b7c8ac;color:#f4e9ca;cursor:pointer}.figure{padding:14px;margin:20px 0;background:#294136}.raster{overflow:auto;max-width:100%;background:#253b32}.raster img{display:block;max-width:none!important;image-rendering:pixelated}code{overflow-wrap:anywhere}'
    body='<article id="CH4-NEW-03"><h2>One UNSELECTED v03 candidate</h2>'+fig('v03 candidate',after,'previews/CH4-NEW-03-upper-salvage-v03-4x.png')+fig('v02 — preserved unchanged',before,'previews/v02-before-4x.png')+fig('v01 — original preserved',original,'previews/v01-before-4x.png')+f'<p>SHA-256 <code>{manifest["asset"]["native"]["sha256"]}</code>. {manifest["unchangedScenePercent"]}% of full-scene pixels remain exact v02. Original stairs and rails are restored unchanged; no new perspective fix is claimed.</p></article>'
    body+='<article id="comparisons"><h2>Native and exact4× comparison sheets</h2>'
    for title,name in [('v01 / v02 / v03','v01-v02-v03'),('Quick-glance full scenes','quick-glance'),('Additional Chapter2/4 benchmarks','additional-benchmarks'),('Rack: before / after','rack-before-after'),('Foreground: unchanged v02 / v03','sinks-before-after'),('Stairs: original restored unchanged','stairs-before-after')]:body+=fig(title,f'comparisons/{name}-native.png',f'comparisons/{name}-4x.png')
    body+='</article><article id="benchmarks"><h2>Actual approved references</h2>'
    refs=json.loads((ROOT/'evidence/benchmark-provenance.json').read_text())
    for ref in refs:
        p=Path(ref['file']);body+=fig(p.stem,ref['file'],'previews/'+p.stem+'-4x.png')
    body+='</article>'
    header='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>B2-10 v03 fuller rack, original stairs</title><style>'+css+'</style><main><header><h1>Chapter4 B2-10 v03 · fuller rack, original stairs</h1><p><strong>Everything UNSELECTED. Nate’s visual approval is pending.</strong> Same314×206 scene: exact v02 foreground sinks plus a fuller, locally refined rack. The owner requested fallback to the original stairs and rails; both are restored byte-for-byte. Their remaining perspective ambiguity is not presented as corrected. Lift/W.C., hatch, duct, architecture and central floor are unchanged.</p><p>SOURCE-DERIVED localized material/structure workflow used in the earlier Chapter4 main-scene improvements. No whole-room shading/palette pass or new image generation. Rejected stair redraws are excluded.</p><nav><a href="manifest.json">Manifest / hashes</a><a href="README.md">Method and scope</a><a href="evidence/validation.json">QA / preservation</a><a href="evidence/visual-review.md">Visual assessment</a><a href="comparisons/quick-glance-4x.png">Quick-glance 4× PNG</a><a href="../v01/originals/CH4-NEW-03-detailed-reference.png">Preserved concept source</a></nav></header>'
    script='<script>document.querySelectorAll("button[data-scale]").forEach(b=>b.onclick=()=>{const i=b.closest("section.figure").querySelector("img"),s=Number(b.dataset.scale);i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;});</script></main></html>'
    (ROOT/'index.html').write_text(header+body+script)
    print(json.dumps({'changedPixels':changes,'unchangedPercent':manifest['unchangedScenePercent'],'status':'UNSELECTED'}))
if __name__=='__main__':main()
