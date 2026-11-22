"""Source-derived NPC crispness correction, not independently native authorship.

Originals/crops, sprite sizes, placement, room backgrounds and shadows are
identical to v06. This changes only reduction and native-resolution cleanup.
The portrait is deliberately not regenerated or altered in this revision.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,PngImagePlugin
import hashlib,json

ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT.parent/'v06'
# Native rectangles select existing facial/hand information from the same
# original artwork. They do not draw replacement eyes/limbs or change anatomy.
FEATURES={
 'plumber':[(13,5,32,20),(0,1,15,24)],
 'assistant':[(14,5,30,20),(0,10,22,29)],
 'pianist':[(6,0,17,13),(21,10,31,21),(4,23,13,32)],
 'musician':[(10,0,25,14),(0,8,8,17),(19,28,25,37)],
 'organizer':[(7,0,22,18),(3,27,14,38),(20,25,27,35)],
 'porters-and-chair':[(8,0,23,14),(38,0,54,14),(17,26,27,37),(36,25,47,37)],
}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def prepare(layer):
    src=Image.open(BASE/layer['source']).convert('RGBA').crop(layer['sourceCropAbsolute'])
    w,h=layer['nativeSpriteSize'];nearest=src.resize((w,h),Image.Resampling.NEAREST)
    area=src.convert('RGBa').resize((w,h),Image.Resampling.LANCZOS).convert('RGBA')
    # Prefilter at twice the target grid, then retain distinct native samples.
    twice=src.convert('RGBa').resize((w*2,h*2),Image.Resampling.LANCZOS).convert('RGBA')
    body=twice.resize((w,h),Image.Resampling.NEAREST)
    result=body.convert('RGB').filter(ImageFilter.UnsharpMask(radius=.5,percent=110,threshold=3))
    result.putalpha(area.getchannel('A'))
    p=result.load();n=nearest.load();a=area.load()
    for y in range(h):
        for x in range(w):
            if a[x,y][3]<150:p[x,y]=(0,0,0,0);continue
            if any(x0<=x<x1 and y0<=y<y1 for x0,y0,x1,y1 in FEATURES[layer['id']]):
                # Retain sampled facial/hand contrast with a small stabilizing
                # area contribution. No palette cap or color-count reduction.
                rgb=tuple(round(n[x,y][k]*.88+a[x,y][k]*.12) for k in range(3))
            else:rgb=p[x,y][:3]
            edge=x==0 or y==0 or x==w-1 or y==h-1 or any(a[xx,yy][3]<150 for xx,yy in [(max(0,x-1),y),(min(w-1,x+1),y),(x,max(0,y-1)),(x,min(h-1,y+1))])
            if max(rgb)-min(rgb)>110 and edge:rgb=a[x,y][:3]
            p[x,y]=rgb+(255,)
    return result

def main():
    for d in ['native','npc','evidence']:(ROOT/d).mkdir(exist_ok=True)
    old=json.loads((BASE/'evidence/scene-npc-derivation.json').read_text())
    rooms={name:Image.open(BASE/f'backgrounds/CH4-0{4 if name=="restroom" else 5}-{name}-background-v02.png').convert('RGBA') for name in ['restroom','ballroom']}
    records=[]
    for layer in old['layers']:
        sprite=prepare(layer);left,top=layer['position'];w,h=sprite.size;room=layer['room']
        path=ROOT/'npc'/(layer['id']+'-source-derived.png');sprite.save(path)
        shadow=Image.new('RGBA',(314,206),(0,0,0,0));d=ImageDraw.Draw(shadow)
        d.ellipse((left+2,top+h-2,left+w-2,top+h+1),fill=(54,65,45,75))
        rooms[room]=Image.alpha_composite(rooms[room],shadow);rooms[room].alpha_composite(sprite,(left,top))
        records.append({'id':layer['id'],'room':room,'status':'UNSELECTED','source':'../v06/'+layer['source'],'sourceSha256':sha(BASE/layer['source']),'sourceCropAbsolute':layer['sourceCropAbsolute'],'nativeSpriteSize':[w,h],'position':[left,top],'groundY':layer['groundY'],'featureRectangles':FEATURES[layer['id']],'file':path.relative_to(ROOT).as_posix(),'sha256':sha(path),'previousFile':'../v06/'+layer['file'],'previousSha256':layer['sha256'],'independentlyNativeAuthored':False})
    for room,im in rooms.items():
        meta=PngImagePlugin.PngInfo();meta.add_text('Authorship','HYBRID: preserved native background and source-derived illustrated NPCs; NPC-only crispness correction')
        im.convert('RGB').save(ROOT/f'native/CH4-0{4 if room=="restroom" else 5}-{room}-v03.png',pnginfo=meta)
    report={'status':'UNSELECTED','method':'SOURCE-DERIVED NPC reduction and native-pixel cleanup','nativeAuthorshipClaim':False,'pillowVersion':Image.__version__,'sourceArtworkRegenerated':False,'previousArtworkChanged':False,'sourceCropSpriteSizePoseAndPlacementChanged':False,'nativeSilhouetteCoverageChanged':True,'backgroundsChanged':False,'portraitChanged':False,'reduction':{'body':'Premultiplied-alpha Lanczos to 2x native size; nearest sample to native; native RGB unsharp radius0.5/110percent/threshold3','faceAndHands':'Declared native feature rectangles use 88percent nearest source sample +12percent premultiplied area color','alpha':'Native pixel coverage from area alpha >=150; opaque interior and clear exterior','fringeCleanup':'Saturated perimeter contamination uses stable area color','paletteLimit':None,'finalPreview':'Exact4x nearest-neighbor of the FINAL native PNG; no interpolation'},'internalAlternativesCompared':['v06 area reduction','direct nearest sampling','box reduction','area reduction with stronger sharpening','2x prefilter and nearest','selected feature-aware native treatment'],'layers':records}
    (ROOT/'evidence/npc-derivation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Six NPC layers corrected; backgrounds, placement, scale and portrait preserved.')

if __name__=='__main__':main()
