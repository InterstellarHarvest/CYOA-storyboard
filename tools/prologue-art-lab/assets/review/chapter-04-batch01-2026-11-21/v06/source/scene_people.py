"""Hybrid scene assembly: native room backgrounds, SOURCE-DERIVED NPC layers.

The rejected code figures are not used. Generated originals and source cells
are preserved; alpha-bounds crop, proportional premultiplied Lanczos reduction,
limited cutout cleanup and placement are explicitly recorded. No independent
native authorship is claimed for characters or the complete hybrid frame.
"""
from pathlib import Path
from PIL import Image,ImageDraw,PngImagePlugin
from collections import deque
import hashlib,json

ROOT=Path(__file__).resolve().parent.parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def prepare(source,cell,height):
    im=Image.open(ROOT/source).convert('RGBA');tile=im.crop(cell)
    box=tile.getchannel('A').point(lambda a:255 if a>96 else 0).getbbox()
    assert box,'Empty actor cell'
    # Two source pixels of padding preserve the anti-aliased cutout boundary.
    box=(max(0,box[0]-2),max(0,box[1]-2),min(tile.width,box[2]+2),min(tile.height,box[3]+2))
    crop=tile.crop(box);width=round(crop.width*height/crop.height)
    im=crop.convert('RGBa').resize((width,height),Image.Resampling.LANCZOS).convert('RGBA')
    p=im.load();before=im.copy()
    for y in range(height):
        for x in range(width):
            if p[x,y][3]<=40:p[x,y]=(0,0,0,0)
    # Saturated artificial fringe is corrected only on the perimeter. Meaningful
    # skin/hair/fabric/hand pixels remain the actual reduced illustration.
    fixed=im.copy();q=fixed.load()
    for y in range(1,height-1):
        for x in range(1,width-1):
            r,g,b,a=p[x,y]
            if not a or max(r,g,b)-min(r,g,b)<110:continue
            if not any(p[xx,yy][3]==0 for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]):continue
            near=[((xx-x)**2+(yy-y)**2,xx,yy) for yy in range(max(1,y-2),min(height-1,y+3)) for xx in range(max(1,x-2),min(width-1,x+3)) if p[xx,yy][3]>=245 and max(p[xx,yy][:3])-min(p[xx,yy][:3])<100]
            if near:
                _,xx,yy=min(near);q[x,y]=p[xx,yy][:3]+(a,)
    changed=sum(a!=b for a,b in zip(before.get_flattened_data(),fixed.get_flattened_data()))
    return fixed,{'source':source,'sourceSha256':sha(ROOT/source),'cell':list(cell),'alphaBoundsWithinCell':list(box),'sourceCropAbsolute':[cell[0]+box[0],cell[1]+box[1],cell[0]+box[2],cell[1]+box[3]],'nativeSpriteSize':[width,height],'operation':'Alpha-bounds crop; proportional premultiplied-alpha Lanczos; alpha<=40 cleared; saturated cutout-perimeter cleanup only.','cutoutCleanupPixelCount':changed,'independentlyNativeAuthored':False}

def main():
    (ROOT/'npc').mkdir(exist_ok=True);(ROOT/'native').mkdir(exist_ok=True)
    definitions=[
        ('plumber','restroom','detailed/NPC-plumbers-original.png',(0,0,894,880),58,55,127),
        ('assistant','restroom','detailed/NPC-plumbers-original.png',(894,0,1788,880),46,110,119),
        ('pianist','ballroom','detailed/NPC-ballroom-people-original.png',(0,0,618,848),57,69,73),
        ('musician','ballroom','detailed/NPC-ballroom-people-original.png',(618,0,1236,848),55,120,75),
        ('organizer','ballroom','detailed/NPC-ballroom-people-original.png',(1236,0,1854,848),74,213,80),
        ('porters-and-chair','ballroom','detailed/NPC-porters-original.png',(0,0,1312,1199),55,274,81),
    ]
    rooms={name:Image.open(ROOT/f'backgrounds/CH4-0{4 if name=="restroom" else 5}-{name}-background-v02.png').convert('RGBA') for name in ['restroom','ballroom']}
    records=[]
    for name,room,source,cell,height,center,top in definitions:
        sprite,rec=prepare(source,cell,height);left=round(center-sprite.width/2)
        path=ROOT/'npc'/(name+'-source-derived.png');sprite.save(path)
        # Local floor contact shadow uses native pixels; no projected source floor.
        shadow=Image.new('RGBA',(314,206),(0,0,0,0));d=ImageDraw.Draw(shadow)
        d.ellipse((left+2,top+height-2,left+sprite.width-2,top+height+1),fill=(54,65,45,75))
        rooms[room]=Image.alpha_composite(rooms[room],shadow)
        rooms[room].alpha_composite(sprite,(left,top))
        rec.update(id=name,room=room,file=path.relative_to(ROOT).as_posix(),sha256=sha(path),position=[left,top],groundY=top+height,status='UNSELECTED')
        records.append(rec)
    for name,im in rooms.items():
        info=PngImagePlugin.PngInfo();info.add_text('Authorship','HYBRID: independent native background with source-derived illustrated NPCs; not independently authored whole-frame art')
        im.convert('RGB').save(ROOT/f'native/CH4-0{4 if name=="restroom" else 5}-{name}-v02.png',pnginfo=info)
    report={'status':'UNSELECTED','wholeFrameAuthorship':'HYBRID / SOURCE-DERIVED NPC COMPOSITE','backgroundAuthorship':'Independently drawn directly at 314x206, with separate forbidden-operation replay','characterAuthorship':'Source-derived from generated art matching the exact owner-supplied approved Pavilion scene NPCs and portraits','rejectedCodeFiguresUsed':False,'paletteReduction':False,'sharpening':False,'pillowVersion':Image.__version__,'layers':records}
    (ROOT/'evidence/scene-npc-derivation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Hybrid scenes assembled with',len(records),'source-derived actor layers; no code-drawn figures.')

if __name__=='__main__':main()
