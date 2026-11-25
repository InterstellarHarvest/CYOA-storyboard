"""Localized v01 fixture refinement in the approved B2-02 source-derived style.

No frame-wide tonal guide, palette fit or new geometry pass. Existing native
fixtures use a reference underpainting, local ramps and explicit native repair
clusters; source-defined contours are retained and provenance is disclosed.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
from collections import Counter
import importlib.util,json,hashlib,argparse,sys
sys.dont_write_bytecode=True

ROOT=Path(__file__).resolve().parents[1];SIZE=(314,206)
PORCELAIN=['#303b38','#526965','#756b52','#8b826c','#a39472','#b3aa8c','#c5b994','#dfd6b5','#e8dcbc','#f3e9c8']
COLORS=[tuple(bytes.fromhex(c[1:]))for c in PORCELAIN]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def polygon_mask(points):
    m=Image.new('L',SIZE);ImageDraw.Draw(m).polygon(points,fill=255);return m
def material_patch(guide,mask):
    out=Image.new('RGBA',SIZE);raw=list(guide.get_flattened_data());mp=list(mask.get_flattened_data());fitted=[]
    for c,a in zip(raw,mp):fitted.append(min(COLORS,key=lambda p:sum((v-w)**2 for v,w in zip(c,p)))+(255,)if a else(0,0,0,0))
    # A source underpainting informs object anatomy, then connected native shade
    # groups replace isolated weak texture. Dark sockets/glaze edges are retained.
    src=fitted[:];changed=0
    for y in range(1,205):
        for x in range(1,313):
            i=y*314+x;c=src[i]
            if not c[3]or sum(c[:3])<250 or sum(c[:3])>650:continue
            near=[src[n]for n in[i-1,i+1,i-314,i+314]if src[n][3]]
            if not near:continue
            target,n=Counter(near).most_common(1)[0]
            if n>=3 and c not in near and sum((a-b)**2 for a,b in zip(c[:3],target[:3]))<1500:fitted[i]=target;changed+=1
    out.putdata(fitted);return out,changed

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo-root');args=ap.parse_args()
    repo=Path(args.repo_root).resolve()if args.repo_root else next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists())
    v01=repo/'tools/prologue-art-lab/assets/review/chapter-04-b210-upper-salvage-2026-11-24/v01'
    for folder in['native','previews','layers','masks','evidence','diagnostics','comparisons']:(ROOT/folder).mkdir(exist_ok=True)
    srcpath=v01/'originals/CH4-NEW-03-detailed-reference.png';guide=Image.open(srcpath).convert('RGB').resize(SIZE,Image.Resampling.NEAREST);guide.save(ROOT/'diagnostics/reference-transfer-NOT-FINAL.png')
    shifted=Image.new('RGB',SIZE);shifted.paste(guide,(0,2))
    parts=json.loads((v01/'evidence/material-interpretation.json').read_text())['finalLayerOrder']
    # Rear: keep one sink, one disconnected angled pan and one partition.
    rack=Image.new('RGBA',SIZE);d=ImageDraw.Draw(rack)
    d.rectangle((212,47,313,137),fill='#30483d');d.rectangle((217,49,307,135),fill='#385349')
    for x in[212,308]:d.rectangle((x,46,x+3,139),fill='#344440');d.line([(x,47),(x,136)],fill='#657770')
    # Retained shelving is quieter. Three rows are structure, not extra stock.
    for y in[65,89,118,137]:
        d.rectangle((215,y,307,y+3),fill='#263d35');d.line([(216,y),(306,y)],fill='#657770')
    d.polygon([(277,96),(299,92),(307,133),(284,136)],fill='#263d35')
    d.polygon([(279,97),(298,94),(304,131),(286,133)],fill='#4b6857')
    d.line([(279,97),(286,132)],fill='#829477');d.line([(300,95),(306,132)],fill='#647c63')
    d.rectangle((282,108,284,111),fill='#788a80')
    sinkmask=polygon_mask([(222,46),(224,43),(229,42),(245,42),(248,46),(250,53),(247,58),(225,58),(222,55)])
    bowlmask=polygon_mask([(221,78),(223,72),(227,67),(232,66),(236,68),(239,73),(237,79),(235,82),(241,82),(242,85),(222,85)])
    sink,cs=material_patch(guide,sinkmask)
    # Reuse approved Chapter4 NATIVE porcelain modelling as a style source,
    # without its cistern/room/floor. No scaling of this native fragment.
    approved_path=ROOT/'references/ch4-restroom-bowl-style.png'
    approved=Image.open(approved_path).convert('RGB');crop=approved.crop((266,121,291,142))
    local=Image.new('L',crop.size);ImageDraw.Draw(local).polygon([(5,1),(19,1),(22,3),(24,7),(22,11),(16,13),(16,17),(20,20),(5,20),(8,17),(8,13),(2,11),(0,7),(2,3)],fill=255)
    bowlguide=Image.new('RGB',SIZE);bowlguide.paste(crop,(224,68));bowlmask=Image.new('L',SIZE);bowlmask.paste(local,(224,68));bowl,cb=material_patch(bowlguide,bowlmask)
    # Native support/contact corrections and true detached outlet, not a ring icon.
    d.line([(224,64),(248,64)],fill='#223732')
    d.line([(223,88),(242,88)],fill='#263d35')
    rack.alpha_composite(sink,(0,6));rack.alpha_composite(bowl);d=ImageDraw.Draw(rack)
    d.line([(224,61),(228,64),(245,64)],fill='#c5b994')
    d.polygon([(244,79),(248,79),(251,82),(251,85),(247,86),(244,83)],fill='#a39472')
    d.ellipse((247,81,251,85),fill='#756b52');d.line([(247,81),(250,81)],fill='#dfd6b5');d.point((249,83),fill='#303b38')
    # Foreground: retain original partition/mirror/pallet layers and footprint.
    spec=importlib.util.spec_from_file_location('preserved_native',v01/'source/native_scene.py');n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n)
    fore=Image.open(v01/'layers/material-foreground-sanitary-salvage.png').convert('RGBA')
    oldfixture=Image.new('RGBA',SIZE);od=ImageDraw.Draw(oldfixture)
    n.basin(od,28,153,50,25);n.basin(od,32,139,39,25)
    od.polygon([(73,171),(76,167),(78,167),(77,172)],fill='#7d8270')
    original_basin=n.basin;n.basin=lambda *a,**k:None
    backing=n.foreground_storage();n.basin=original_basin
    fore.paste(backing,(0,0),oldfixture.getchannel('A'))
    frontmask=polygon_mask([(28,147),(38,144),(41,138),(47,136),(66,136),(73,139),(77,149),(82,150),(83,156),(80,165),(80,176),(76,181),(42,182),(33,179),(30,171),(29,160)])
    foreground,cfront=material_patch(shifted,frontmask)
    d=ImageDraw.Draw(fore)
    d.polygon([(32,178),(72,176),(84,181),(77,185),(39,188),(27,183)],fill='#5e513e')
    fore.alpha_composite(foreground);d=ImageDraw.Draw(fore)
    # Physically meaningful native edge/cavity/socket repairs. No new noise.
    d.line([(35,175),(43,178),(62,178),(77,176)],fill='#c5b994')
    d.line([(34,169),(42,172),(61,172),(76,169)],fill='#dfd6b5')
    d.point((60,156),fill='#303b38');d.point((59,155),fill='#dfd6b5')
    # A few existing glaze clusters stay sharp; never a blanket highlight pass.
    d.line([(44,139),(61,138)],fill='#e8dcbc')
    # Lower rack edge already meets the stair landing: retain its exact pixels.
    oldrack=Image.open(v01/'layers/material-storage-racks.png').convert('RGBA')
    rack.paste(oldrack.crop((0,140,314,206)),(0,140))
    replacements={'material-storage-racks':rack,'material-foreground-sanitary-salvage':fore}
    protected=Image.new('L',SIZE)
    for target in['material-freight-lift','material-wc-three-button-panel','material-open-maintenance-hatch','material-descending-stairwell','material-guardrails','material-ceiling-duct-and-lights']:
        idx=next(i for i,p in enumerate(parts)if Path(p).stem==target);visible=Image.open(v01/parts[idx]).getchannel('A')
        for p in parts[idx+1:]:visible=ImageChops.subtract(visible,Image.open(v01/p).getchannel('A'))
        protected=ImageChops.lighter(protected,visible)
    result=Image.new('RGBA',SIZE)
    for rel in parts:
        name=Path(rel).stem
        if name in replacements:
            im=replacements[name]
            # Restore exact v01 foreground colors wherever an already visible
            # route is protected; replacements cannot reveal or cover it.
            old=Image.open(v01/rel).convert('RGBA');im.paste(old,(0,0),protected);im.save(ROOT/rel)
        else:(ROOT/rel).write_bytes((v01/rel).read_bytes());im=Image.open(v01/rel).convert('RGBA')
        result=Image.alpha_composite(result,im)
    result=result.convert('RGB');out=ROOT/'native/CH4-NEW-03-upper-salvage-v02.png';result.save(out);result.resize((1256,824),Image.Resampling.NEAREST).save(ROOT/'previews/CH4-NEW-03-upper-salvage-v02-4x.png')
    allowed=Image.new('L',SIZE);d=ImageDraw.Draw(allowed);d.rectangle((0,77,94,202),fill=255);d.rectangle((212,42,313,139),fill=255);allowed=ImageChops.subtract(allowed,protected)
    protected.save(ROOT/'masks/pixel-locked-geography.png');allowed.save(ROOT/'masks/authorized-local-repair.png')
    m=Image.new('L',SIZE);m.paste(sinkmask,(0,6));m.save(ROOT/'masks/rear-sink.png');bowlmask.save(ROOT/'masks/rear-bowl.png');frontmask.save(ROOT/'masks/nested-sinks.png')
    (ROOT/'evidence/repair.json').write_text(json.dumps({'sourceDerived':True,'whollyIndependentAuthorshipClaim':False,'baseVersion':'v01','method':'Localized version of approved B2-02 material/structure workflow: detailed-reference fixture underpainting, local material ramps and connected-cluster selection, native object silhouette masks, edge/socket/underside/support painting; source-defined contours retained. No whole-scene relighting/palette pass or master replacement.','reference':'../v01/originals/CH4-NEW-03-detailed-reference.png','referenceSha256':sha(srcpath),'approvedBowlReference':{'file':'references/ch4-restroom-bowl-style.png','canonicalSourcePath':'assets/selected/pending-integration/scenes/grand_bellevue/restroom.png','sha256':sha(approved_path),'nativeCrop':[266,121,291,142]},'nativePalette':PORCELAIN,'sourceFigureTranslation':{'foreground':[0,2],'rearSink':[0,6],'rearBowlNativeCrop':{'sourceCrop':[266,121,291,142],'targetOrigin':[224,68],'noScaling':True}},'replacedLayers':list(replacements),'layerOrder':parts,'quietPixelsMerged':cs+cb+cfront,'nativeHash':sha(out),'status':'UNSELECTED'},indent=2)+'\n')
    print(sha(out))
if __name__=='__main__':main()
