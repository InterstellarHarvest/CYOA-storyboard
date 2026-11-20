"""Bounded, deterministic native-grid pixel edits. No generation or image filtering."""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json, shutil

ROOT = Path(__file__).resolve().parent
V01 = ROOT.parent / 'v01'
PIN = '53358b9df78f72e815cd69ee4128b1c86c08818d'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name, data): (ROOT / name).write_text(json.dumps(data, indent=2) + '\n')
for d in ['candidates', 'previews', 'masks', 'layers', 'sources', 'comparisons', 'composites']:
    (ROOT / d).mkdir(exist_ok=True)
source = json.loads((V01 / 'manifest.json').read_text())
records = []
for candidate in source['candidates']:
    ident = candidate['candidateId']
    before_file = V01 / candidate['file']
    assert digest(before_file) == candidate['sha256']
    before = Image.open(before_file)
    after = before.copy()
    allowed = Image.new('1', before.size)
    ad = ImageDraw.Draw(allowed)
    operations = []
    if ident == 'CH3-C01-urgency':
        # Rows explicitly cover only the old bell/stem and immediate shadow repair.
        ad.rectangle((111, 99, 113, 102), fill=1)
        for y in range(103, 108): ad.line((110, y, 116, y), fill=1)
        ad.rectangle((109, 108, 116, 109), fill=1)
        ad.point((109, 106), fill=1); ad.point((109, 107), fill=1)
        # Finger/hand RGB is protected independently of the allowed object region.
        hand = {(x,y) for y in range(101,108) for x in range(105,116)
                if (lambda c: c[0] > c[1]+25 and c[1] > c[2]+15)(before.getpixel((x,y))[:3])}
        # Erase old pale block and lower rectangular shadow using the adjacent
        # same-row curtain tone, keeping its vertical material rhythm.
        for y in range(103,110):
            for x in range(108,117):
                if allowed.getpixel((x,y)) and (x,y) not in hand:
                    after.putpixel((x,y), before.getpixel((117,y)))
        palette = {'D':(57,76,80), 'L':(245,239,211),
                   'M':(190,198,184), 'S':(124,147,143)}
        rows = {
            99:(112,'D'),100:(112,'D'),101:(112,'D'),102:(112,'D'),
            103:(111,'DDD'),104:(110,'DLLSD'),105:(110,'DLMSD'),
            106:(109,'DLMMSSD'),107:(109,'DLLMMMD'),108:(109,'DDDDDDD'),
            109:(112,'D'),
        }
        for y,(left,row) in rows.items():
            for dx,letter in enumerate(row):
                p=(left+dx,y)
                if p not in hand:
                    assert allowed.getpixel(p)
                    after.putpixel(p,palette[letter])
        assert all(before.getpixel(p)==after.getpixel(p) for p in hand)
        operations = [
            'Redraw only the existing held bell: narrow dark handle, tapered silver body, flared dark lip and one-pixel clapper.',
            'Repair the old pale rectangular bell/shadow footprint from the adjacent same-row curtain pixels.',
            'All existing skin pixels in the hand region remain exact; presenter pose and face are untouched.',
        ]
        write('sources/bell-edit-spec.json', {'rows': {str(y):[x,row] for y,(x,row) in rows.items()},
            'palette':palette,'protectedHandPixels':[list(p) for p in sorted(hand)],
            'repairSource':'v01 pixel (117,y), same row; only allowed bell/shadow footprint'})
    elif ident == 'CH3-C03-locomotion':
        # The landing exists in v01. These line segments articulate its top
        # plane/threshold without changing width, curtain, pit, belt or net.
        segments = [
            # Parallel grout courses recede into the opening.
            ((224,132),(256,132),(130,122,112)),
            ((228,137),(258,137),(130,122,112)),
            # Two perspective joints; no arrows or painted easy path.
            ((235,129),(234,132),(137,128,116)),
            ((234,133),(232,137),(137,128,116)),
            ((232,138),(230,141),(137,128,116)),
            ((247,129),(248,132),(137,128,116)),
            ((248,133),(250,137),(137,128,116)),
            ((250,138),(252,141),(137,128,116)),
            # Existing yellow sill gains a crisp top highlight and a slim
            # stationary vertical face at exactly its existing front edge.
            ((226,142),(257,142),(245,207,134)),
            ((227,144),(258,144),(116,110,104)),
            ((228,145),(257,145),(151,137,120)),
            # Short return edge ties the sill to the fixed portal jamb.
            ((258,140),(258,143),(89,101,99)),
        ]
        draw = ImageDraw.Draw(after)
        for p,q,color in segments:
            ad.line((*p,*q),fill=1,width=1)
            draw.line((*p,*q),fill=color,width=1)
        operations = [
            'Add two restrained tile courses and receding grout joints on the existing stationary floor inside the curtain opening.',
            'Clarify the existing yellow threshold with a one-pixel highlight, narrow step face and short fixed-jamb return.',
            'Do not widen the landing or span the padded pit; conveyor, pit, net and challenge geography remain unchanged.',
        ]
        write('sources/landing-edit-spec.json', {'segments':segments,
            'meaning':'Existing fixed landing beyond curtain; no new bridge, jump arrow or enlarged escape surface.'})
    else:
        operations = ['Retained byte-identical from v01.']
        if ident == 'CH3-C06-presenter-excited':
            operations += ['Optional facial edit declined after native/close comparison: v01 already has raised brows, bright eyes and an open delighted smile. Retain likeness and exact anchors.']
    pixels = []
    for y in range(before.height):
        for x in range(before.width):
            a,b=before.getpixel((x,y)),after.getpixel((x,y))
            if a!=b:
                assert allowed.getpixel((x,y)),(ident,x,y)
                pixels.append({'x':x,'y':y,'before':list(a),'after':list(b)})
    final = ROOT / 'candidates' / f'{ident}-v02.png'
    if pixels: after.save(final)
    else: shutil.copyfile(before_file,final)
    changed = Image.new('1',before.size)
    for p in pixels: changed.putpixel((p['x'],p['y']),1)
    allowed.convert('L').save(ROOT/'masks'/f'{ident}-allowed.png')
    changed.convert('L').save(ROOT/'masks'/f'{ident}-changed.png')
    overlay=Image.new('RGBA',before.size)
    for p in pixels:overlay.putpixel((p['x'],p['y']),tuple(p['after'][:3])+(255,))
    overlay.save(ROOT/'layers'/f'{ident}-correction.png')
    after.resize((after.width*4,after.height*4),Image.Resampling.NEAREST).save(ROOT/'previews'/f'{ident}-v02-4x.png')
    coords=f'sources/{ident}-changed-pixels.json'
    write(coords,{'candidateId':ident,'coordinates':'zero-based x,y; before/after channel values','pixels':pixels})
    records.append({**{k:candidate[k] for k in ['candidateId','record','kind','dimensions','carryForward']},
        'sourceCommit':PIN,'sourceFile':'../v01/'+candidate['file'],'sourceSha256':candidate['sha256'],
        'file':str(final.relative_to(ROOT)),'sha256':digest(final),
        'status':'generated','selected':False,'approved':False,'assetPath':None,
        'changedPixels':len(pixels),'byteIdenticalToV01':not pixels,'operations':operations,
        'allowedMask':f'masks/{ident}-allowed.png','changedMask':f'masks/{ident}-changed.png',
        'correctionLayer':f'layers/{ident}-correction.png','changedCoordinates':coords})
write('sources/corrections.json',records)
print(json.dumps({r['candidateId']:{'changedPixels':r['changedPixels'],'sha256':r['sha256']} for r in records},indent=2))
