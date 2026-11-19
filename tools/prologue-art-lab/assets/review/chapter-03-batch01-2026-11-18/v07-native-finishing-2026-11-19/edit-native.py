"""Coordinate-authored finishing on existing 314x206 rasters; no filtering.

Every primitive is specified below at the actual logical grid. These local edits
substantiate native finishing, not original authorship of the inherited scene.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib
import json

ROOT=Path(__file__).resolve().parent
ops=[]
def rgb(c): return tuple(bytes.fromhex(c.lstrip('#')))
def poly(scene,label,points,color): ops.append(dict(scene=scene,label=label,kind='polygon',points=points,color=color))
def rect(scene,label,box,color): ops.append(dict(scene=scene,label=label,kind='rectangle',box=box,color=color))
def line(scene,label,points,color,width=1): ops.append(dict(scene=scene,label=label,kind='line',points=points,color=color,width=width))
def dots(scene,label,points,color): ops.append(dict(scene=scene,label=label,kind='points',points=points,color=color))

# A01: small, fully bounded material planes and edge runs only.
s='A01'
# Structural faces stop at foreground occlusion, above the reception worktop.
rect(s,'center post light face above intercom',(183,42,185,128),'5c7d80')
rect(s,'center post broad face above intercom',(187,42,192,128),'4a6b71')
line(s,'center post recessed edge above intercom',[(194,43),(194,128)],'34545d')
line(s,'left restroom jamb highlight',[(69,72),(69,138)],'5a7a7d')
line(s,'left restroom jamb recessed edge',[(74,73),(74,137)],'35565f')
line(s,'restroom lintel recessed edge',[(79,69),(163,69)],'2f4d55')
# Gate: native cream panel interiors, avoid the steel frame and turnstile.
poly(s,'left gate cream face',[(83,147),(99,147),(99,176),(83,176)],'f4d3a9')
poly(s,'left gate narrow shaded return',[(100,147),(101,147),(101,176),(100,176)],'e8c49c')
rect(s,'right gate cream face',(159,147,165,175),'f0cfa5')
line(s,'left gate top rail controlled highlight',[(81,141),(100,141)],'8a9a96')
# Reception front: three deliberately authored planes within the source silhouette.
poly(s,'counter broad coral plane',[(192,153),(256,153),(260,152),(260,176),(256,178),(193,178)],'de6d58')
poly(s,'counter left coral shaded return',[(179,152),(185,154),(185,175),(179,173)],'c56451')
poly(s,'counter right coral shaded return',[(262,153),(266,151),(266,174),(262,176)],'ce6552')
line(s,'counter toe kick upper light',[(198,181),(254,181)],'678385')
# Preserve the intercom and all other equipment. Small surface/shadow edits only.
line(s,'intercom lowest slot coherent dark run',[(185,138),(192,138)],'49514d')
line(s,'intercom first slot coherent dark run',[(186,133),(193,133)],'49514d')
line(s,'intercom middle slot coherent dark run',[(186,136),(192,136)],'49514d')

# A01 attendant: manually specified face/temple/glasses clusters; same placement.
poly(s,'attendant face base',[(216,102),(221,102),(223,105),(224,110),(226,113),(225,117),(222,119),(216,119),(212,117),(211,113),(211,108)],'efb475')
poly(s,'attendant face light plane',[(217,103),(220,103),(221,105),(221,110),(223,112),(223,115),(220,117),(215,116),(213,112),(214,107)],'f6c38a')
poly(s,'attendant jaw shaded cluster',[(212,114),(214,117),(218,119),(221,119),(222,118),(217,117),(214,114)],'cd925e')
line(s,'attendant warm jaw contour',[(211,114),(212,117),(215,119),(220,120),(223,119),(225,117)],'996d4e')
poly(s,'attendant ear cluster',[(207,112),(209,112),(211,114),(211,116),(209,116),(207,114)],'e4a169')
dots(s,'attendant ear interior',[(208,113),(209,114)],'b57c56')
poly(s,'gray temple deliberate midtone',[(205,106),(207,105),(207,108),(209,108),(209,111),(207,112),(205,111)],'969c96')
line(s,'gray temple narrow highlight',[(205,107),(205,109),(206,110)],'bbc0b5')
line(s,'gray temple lower shade',[(206,112),(208,112),(208,113)],'687778')
line(s,'hair side part',( [(214,99),(218,99),(220,100)]),'756253')
# Thin rectangular frames, two clear lens interiors and one-pixel bridge.
rect(s,'left lens clean warm interior',(212,108,215,109),'efbd82')
rect(s,'right lens clean warm interior',(219,107,222,108),'f2c186')
line(s,'left thin rectangular glasses frame',[(211,107),(215,107),(216,108),(216,109),(215,110),(211,110),(211,108)],'655b4c')
line(s,'right thin rectangular glasses frame',[(218,106),(222,106),(223,107),(223,108),(222,109),(219,109),(218,108),(218,106)],'655b4c')
line(s,'glasses bridge one pixel',[(216,108),(218,108)],'625849')
line(s,'glasses left temple arm',[(207,110),(210,109),(211,109)],'5b5348')
dots(s,'scene-scale eyes',[(214,109),(221,108)],'403e37')
dots(s,'lens restrained highlights',[(212,108),(219,107)],'f9d7a0')
line(s,'nose light cluster',[(218,110),(218,112),(219,112)],'f9cb8d')
dots(s,'nose lower shade',[(220,112)],'bd895b')
line(s,'warm open smile',[(216,114),(217,115),(221,115),(223,113)],'84543c')
line(s,'smile teeth two-pixel cluster',[(218,114),(221,114)],'ffe3ad')
line(s,'lower lip highlight',[(218,116),(221,116)],'eaa774')
# Clothing planes consolidate the local soft shading, preserve outline/hand pose.
poly(s,'attendant left vest flat plane',[(211,124),(214,130),(214,133),(209,134),(207,127),(207,124)],'44656b')
poly(s,'attendant right vest flat plane',[(226,123),(231,126),(232,131),(229,132),(226,132)],'3b5c65')
poly(s,'attendant cream left sleeve plane',[(205,129),(207,131),(207,138),(203,138),(202,136),(203,132)],'f1d7ad')
poly(s,'attendant cream right sleeve plane',[(236,129),(239,134),(239,138),(235,138),(234,134)],'e8cda4')
line(s,'attendant dark tie center',[(220,125),(220,128),(221,130)],'55554d')

# New authored microphone: all visible pixels left of attendant's source silhouette.
line(s,'microphone base shadow',[(197,142),(202,142)],'756f60')
line(s,'microphone base dark plane',[(198,141),(201,141)],'465458')
line(s,'microphone base highlight',[(198,140),(201,140)],'a4aba2')
line(s,'microphone gooseneck dark path',[(200,139),(199,136),(199,133),(199,130),(199,128)],'465458')
line(s,'microphone upper stem glint',[(200,133),(200,131)],'bec3b4')
poly(s,'microphone head capsule',[(198,126),(200,126),(201,127),(200,128),(198,128)],'4c5858')
line(s,'microphone head light face',[(199,127),(200,127)],'c6c9b5')
dots(s,'microphone lower cap pixel',[(199,128)],'899790')

# A04: existing composition/identity unchanged; named native surface repairs.
s='A04'
# Four curtain groups, each an explicit fold face with controlled highlight/shadow.
rect(s,'curtain left fold mid face above camera',(56,71,60,103),'65938c')
rect(s,'curtain left crease above camera',(62,71,63,103),'557f7b')
rect(s,'curtain left highlight face',(67,71,69,135),'83ada0')
rect(s,'curtain before countdown mid face',(120,73,123,125),'629089')
rect(s,'curtain before countdown crease',(127,75,128,125),'4e7876')
rect(s,'curtain after countdown mid face',(194,73,201,126),'62918a')
rect(s,'curtain after countdown crease',(205,73,206,129),'4a7471')
rect(s,'curtain next fold highlight',(209,73,210,130),'78a397')
rect(s,'curtain next fold deep crease',(213,73,214,130),'466c6d')
rect(s,'curtain next fold mid face',(216,73,218,128),'64938c')
# A few clean camera planes and vent runs; every external boundary remains source.
rect(s,'camera stand center metal plane',(37,140,39,166),'a2a399')
line(s,'camera stand narrow side shade',[(42,141),(42,166)],'65716d')
# Platform faceted planes, ring/countdown and outside geometry are unchanged.
rect(s,'platform left center flat facet',(143,143,151,148),'958b85')
rect(s,'platform right center flat facet',(169,143,181,148),'938a84')
rect(s,'platform left narrow shaded facet',(127,142,129,145),'777a74')
rect(s,'platform right narrow shaded facet',(194,142,196,146),'7e8079')
line(s,'platform lower central edge',[(145,150),(181,150)],'5f6b67')
# Presenter costume planes: face, hands, silhouette and full welcoming gesture stay.
poly(s,'presenter left jacket face',[(80,108),(82,107),(84,111),(83,113),(80,113)],'3f5c66')
poly(s,'presenter right jacket face',[(91,111),(94,112),(95,114),(94,116),(91,116)],'3c5963')
poly(s,'presenter left skirt face',[(81,125),(88,125),(88,134),(81,134)],'435e68')
poly(s,'presenter right skirt shade',[(89,125),(95,125),(95,134),(89,134)],'344f59')
line(s,'presenter skirt restrained lower edge',[(82,135),(94,135)],'304d57')
# Existing broad step: two interior edge runs consolidate soft boundary marks.
line(s,'stage coral lip central run',[(87,159),(233,159)],'d2694e')
line(s,'stage lower riser central run',[(87,168),(232,168)],'67716d')

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
reports=[]
for scene,ident in [('A01','CH3-A01-restroom-v07'),('A04','CH3-A04-verification-v07')]:
    source=ROOT/f'references/{scene}-v06.png'
    original=Image.open(source).convert('RGB'); assert original.size==(314,206)
    out=original.copy(); stages=[];scope=Image.new('1',out.size);md=ImageDraw.Draw(scope)
    for op in [o for o in ops if o['scene']==scene]:
        before=out.copy();d=ImageDraw.Draw(out);color=rgb(op['color'])
        if op['kind']=='polygon':
            pts=[tuple(p) for p in op['points']];d.polygon(pts,fill=color);md.polygon(pts,fill=1)
        elif op['kind']=='rectangle':d.rectangle(tuple(op['box']),fill=color);md.rectangle(tuple(op['box']),fill=1)
        elif op['kind']=='line':
            pts=[tuple(p) for p in op['points']];d.line(pts,fill=color,width=op['width']);md.line(pts,fill=1,width=op['width'])
        else:
            for p in op['points']:d.point(tuple(p),fill=color);md.point(tuple(p),fill=1)
        count=sum(a!=b for a,b in zip(before.getdata(),out.getdata()))
        stages.append({**op,'changedPixelsAtThisStep':count})
    # Hard preservation regions include all mandatory letters/digits and control hardware.
    locks=[('RESTROOM sign',(69,38,180,62)),('wall access-control reader',(171,102,180,120)),('turnstile and left metal frame',(102,139,155,183)),('right desktop device absence',(244,127,254,142))] if scene=='A01' else [('PEOPLES PAVILION sign',(67,23,252,44)),('countdown 30 and ring',(132,70,189,121)),('standing microphone',(101,111,113,154)),('presenter face',(83,90,94,103)),('welcoming hand',(108,100,119,109)),('camera body and lens',(8,104,66,134)),('side chair',(251,159,301,197)),('rear exit',(224,77,251,136))]
    lock_results=[]
    for label,box in locks:
        passed=original.crop(box).tobytes()==out.crop(box).tobytes()
        assert passed,(scene,label)
        lock_results.append({'label':label,'box':box,'byteIdenticalToV06':passed})
    file=ROOT/f'candidates/{ident}.png';out.save(file)
    out.resize((1256,824),Image.Resampling.NEAREST).save(ROOT/f'previews/{ident}-4x.png')
    mask=Image.new('RGB',(314,206));m=mask.load();changes=[];unexpected=[]
    for y in range(206):
        for x in range(314):
            a=original.getpixel((x,y));b=out.getpixel((x,y))
            if a!=b:
                changes.append((x,y,a,b));m[x,y]=(244,143,63)
                if not scope.getpixel((x,y)):unexpected.append([x,y])
    mask.save(ROOT/f'diagnostics/{scene}-changed-pixels.png')
    mask.resize((1256,824),Image.Resampling.NEAREST).save(ROOT/f'diagnostics/{scene}-changed-pixels-4x.png')
    scope.convert('RGB').save(ROOT/f'diagnostics/{scene}-declared-scope.png')
    with (ROOT/f'sources/{scene}-changed-pixels.tsv').open('w') as f:
        f.write('x\ty\tbefore_rgb\tafter_rgb\n')
        for x,y,a,b in changes:f.write(f'{x}\t{y}\t{",".join(map(str,a))}\t{",".join(map(str,b))}\n')
    reports.append({'candidateId':ident,'source':f'references/{scene}-v06.png','sourceSha256':digest(source),'candidate':f'candidates/{ident}.png','sha256':digest(file),'dimensions':[314,206],'nativeEditOperations':len(stages),'changedPixels':len(changes),'changedPercent':round(len(changes)/64684*100,2),'unmodifiedPixels':64684-len(changes),'unexpectedChangedPixels':unexpected,'sourceUniqueRGB':len(original.getcolors(64684)),'finishedUniqueRGB':len(out.getcolors(64684)),'authoredEditColors':len({o['color'] for o in stages}),'sourcePixelsRemainingDerived':True,'lockedRegions':lock_results,'operations':stages,'status':'generated/unselected','selected':False,'approved':False,'assetPath':None})
(ROOT/'sources/native-edit-record.json').write_text(json.dumps({'method':'Coordinate-authored native raster primitives, executed by Pillow at 314x206. No resampling of candidates, quantization, sharpening, blur, dithering or automated palette replacement.','generationCalls':0,'originalWholeSceneNativeAuthorship':'UNPROVEN: v06 is source-derived. Only the explicitly logged native finishing edits are substantiated.','candidates':reports},indent=2)+'\n')
print(json.dumps([{k:r[k] for k in ['candidateId','sha256','nativeEditOperations','changedPixels','sourceUniqueRGB','finishedUniqueRGB']} for r in reports],indent=2))
