"""Owner-directed combination: v02 foreground, fuller rack, original stairs restored.

Localized source-derived porcelain; original stairs and rails are untouched.
No previous package is written. No room-wide processing or generation.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import importlib.util,json,hashlib,sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];V02=ROOT.parent/'v02';V01=ROOT.parent/'v01';SIZE=(314,206)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return Image.open(p).convert('RGBA')
def main():
    spec=importlib.util.spec_from_file_location('v02_methods',V02/'source/refine_existing.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    src=V01/'originals/CH4-NEW-03-detailed-reference.png';guide=Image.open(src).convert('RGB').resize(SIZE,Image.Resampling.NEAREST)
    rack=load(V01/'layers/material-storage-racks.png');d=ImageDraw.Draw(rack)
    # Original fuller rack rhythm: two top porcelain stacks, middle pans and
    # loose fittings, original lower mirrors and leaning partition leaves.
    # Clear only old white icon silhouettes; keep native rack/partition depth.
    for box in [(218,42,300,64),(218,68,275,88)]:d.rectangle(box,fill='#385349')
    for y in [65,89]:
        d.rectangle((215,y,307,y+3),fill='#263d35');d.line([(216,y),(306,y)],fill='#657770')
    left=load(V02/'layers/material-storage-racks.png').crop((220,48,253,65));rack.alpha_composite(left,(220,48))
    shifted=Image.new('RGB',SIZE);shifted.paste(guide,(0,8))
    mask=v.polygon_mask([(267,45),(269,43),(275,43),(278,42),(289,44),(295,48),(296,51),(294,54),(294,62),(289,64),(276,64),(274,60),(271,59),(271,55),(268,54)])
    right,n1=v.material_patch(shifted,mask);rack.alpha_composite(right)
    # A native source pan, kept identical to the recent approved-style repair.
    bowl=load(V02/'layers/material-storage-racks.png').crop((223,68,253,89));rack.alpha_composite(bowl,(222,68))
    # Side-stored second ceramic piece: the reference gives a genuinely angled
    # back, convex belly and disconnected pipe, rather than another ring icon.
    mask2=v.polygon_mask([(247,69),(249,66),(256,65),(262,67),(266,70),(266,75),(263,80),(260,83),(251,84),(249,81),(247,77)])
    piece,n2=v.material_patch(guide,mask2);rack.alpha_composite(piece)
    d=ImageDraw.Draw(rack)
    # Top fittings and their wooden tray; restrained, legible connected clusters.
    d.polygon([(253,59),(268,58),(273,60),(270,64),(254,64)],fill='#90734a');d.line([(254,59),(268,59)],fill='#b18e56')
    d.line([(254,58),(254,51),(257,49),(260,50)],fill='#344440',width=4);d.line([(254,57),(254,51),(257,50),(260,51)],fill='#a5b3a1')
    d.line([(262,58),(262,54),(265,53),(267,54)],fill='#344440',width=3);d.line([(262,57),(263,54),(266,54)],fill='#788a80')
    # Disconnected outlet rests beside the pans and shares the local glaze ramp.
    d.polygon([(263,81),(266,77),(271,77),(275,80),(275,85),(271,88),(266,87)],fill='#b3aa8c')
    d.polygon([(266,81),(268,79),(271,79),(273,81),(272,85),(268,86),(266,84)],fill='#303b38')
    d.line([(267,79),(271,78),(273,80)],fill='#dfd6b5');d.line([(267,87),(273,87)],fill='#263d35')
    # Contact shadows beneath porcelain, not a global outline/highlight pass.
    d.line([(224,64),(249,64)],fill='#263d35');d.line([(275,64),(295,64)],fill='#263d35')
    d.line([(223,88),(244,88)],fill='#263d35');d.line([(249,86),(260,86)],fill='#263d35')
    # Retain old lower shelf mirrors and all feet at the deck boundary.
    oldrack=load(V01/'layers/material-storage-racks.png');rack.paste(oldrack.crop((0,140,314,206)),(0,140))

    # Owner-directed fallback: the attempts at new stair geometry were rejected.
    # Restore the original native stairwell AND rails byte-for-byte, without
    # claiming that their remaining perspective ambiguity has been corrected.
    parts=json.loads((V02/'evidence/repair.json').read_text())['layerOrder']
    replacements={'material-storage-racks':rack}
    # Lift, hatch and duct remain exact even where repair regions meet them.
    protect=Image.new('L',SIZE)
    for name in ['material-freight-lift','material-wc-three-button-panel','material-open-maintenance-hatch','material-ceiling-duct-and-lights','material-descending-stairwell','material-guardrails']:
        idx=next(i for i,p in enumerate(parts)if Path(p).stem==name);vis=load(V02/parts[idx]).getchannel('A')
        for p in parts[idx+1:]:vis=ImageChops.subtract(vis,load(V02/p).getchannel('A'))
        protect=ImageChops.lighter(protect,vis)
    assembled=Image.new('RGBA',SIZE)
    for rel in parts:
        if Path(rel).stem in replacements:
            im=replacements[Path(rel).stem];im.paste(load(V02/rel),(0,0),protect);im.save(ROOT/rel)
        else:(ROOT/rel).write_bytes((V02/rel).read_bytes());im=load(V02/rel)
        assembled=Image.alpha_composite(assembled,im)
    im=assembled.convert('RGB');out=ROOT/'native/CH4-NEW-03-upper-salvage-v03.png';im.save(out);im.resize((1256,824),Image.Resampling.NEAREST).save(ROOT/'previews/CH4-NEW-03-upper-salvage-v03-4x.png')
    allowed=Image.new('L',SIZE);d=ImageDraw.Draw(allowed);d.rectangle((212,42,313,139),fill=255);allowed=ImageChops.subtract(allowed,protect);allowed.save(ROOT/'masks/authorized-local-repair.png');protect.save(ROOT/'masks/pixel-locked-geography.png')
    (ROOT/'evidence/repair.json').write_text(json.dumps({'sourceDerived':True,'whollyIndependentAuthorshipClaim':False,'baseVersion':'v02','method':'Combine exact v02 foreground with fuller v01 rack layout and localized reference-derived porcelain, native shelves/contacts/fittings. Original v01/v02 stairwell and rail layers restored unchanged after owner rejected reconstruction attempts. No full-frame tonal/palette pass.','reference':'../v01/originals/CH4-NEW-03-detailed-reference.png','referenceSha256':sha(src),'nativePalette':v.PORCELAIN,'replacedLayers':list(replacements),'layerOrder':parts,'quietPixelsMerged':n1+n2,'nativeHash':sha(out),'status':'UNSELECTED','v02ForegroundByteExact':True,'stairsDisposition':'Owner-requested fallback to exact original v01/v02 stairs and rails. Perspective ambiguity remains; do not claim a new perspective correction.'},indent=2)+'\n')
    print(sha(out))
if __name__=='__main__':main()
