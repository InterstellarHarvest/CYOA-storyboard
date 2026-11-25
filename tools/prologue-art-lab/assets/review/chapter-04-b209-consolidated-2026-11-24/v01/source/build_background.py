"""Native 564x278 geometry and localized prop construction from preserved plates.

Only a generated clean underdrawing has a diagnostic transfer before localized native interpretation. Original room pixels outside the correction
and prop layers are preserved. Palette entries follow the existing material ramps.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import json, hashlib

ROOT = Path(__file__).resolve().parents[1]
SIZE = (564, 278)

def blank():
    return Image.new('RGBA', SIZE)

def save(im, rel):
    im.save(ROOT / rel)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def layer_mask(im):
    return im.getchannel('A').point(lambda a: 255 if a else 0)

def geometry():
    from PIL import ImageFilter
    from collections import Counter
    old = Image.open(ROOT/'references/before-wheel-removed.png').convert('RGBA')
    src = Image.open(ROOT/'originals/NEW-18-clean-room-underdrawing.png').convert('RGB')
    diagnostic = src.resize(SIZE, Image.Resampling.NEAREST)
    save(diagnostic, 'evidence/internal-study/clean-room-direct-transfer-diagnostic.png')
    # Generated underdrawing supplies occluded material/form information only.
    # Interpret it on this grid with the EXISTING room's palette, preserve every
    # unobscured room pixel, then construct threshold and floor continuity here.
    colors = sorted(set(old.convert('RGB').get_flattened_data()))
    palette = Image.new('P',(1,1)); flat=[v for c in colors for v in c]
    palette.putpalette(flat+[0]*(768-len(flat)))
    fitted=diagnostic.quantize(palette=palette,dither=Image.Dither.NONE).convert('RGB')
    # Native low-contrast isolated material islands merge into neighboring planes;
    # preserve dark contours and connected creases, molding and damage.
    pix=list(fitted.get_flattened_data());out=pix[:]
    for y in range(145,277):
        for x in range(1,236):
            i=y*564+x;c=pix[i];near=[pix[i-1],pix[i+1],pix[i-564],pix[i+564]]
            target,n=Counter(near).most_common(1)[0]
            if n>=3 and c not in near and sum((a-b)**2 for a,b in zip(c,target))<900:out[i]=target
    fitted.putdata(out)
    m=Image.new('L',SIZE);d=ImageDraw.Draw(m)
    d.polygon([(35,186),(43,170),(52,162),(59,151),(69,145),(85,147),(94,157),(99,169),(101,198),(87,224),(55,225),(41,203)],fill=255)
    d.polygon([(94,163),(183,161),(196,179),(196,220),(175,242),(107,244),(91,217)],fill=255)
    d.polygon([(22,225),(58,216),(198,219),(222,230),(234,277),(17,277)],fill=255)
    d.rectangle((0,210,80,277),fill=255)
    m=m.filter(ImageFilter.MaxFilter(5));new=old.copy();new.paste(fitted,(0,0),m)
    # Continue door seams and reveal a fully unobstructed floor gap. Coordinates
    # follow the clean reference's extended lower doors and existing upper jamb.
    d=ImageDraw.Draw(new)
    d.polygon([(28,163),(42,163),(42,227),(28,230)],fill=(89,51,57))
    d.line([(31,163),(31,229)],fill=(54,45,49),width=2)
    d.line([(34,163),(34,228)],fill=(185,120,60),width=1)
    # Retain exact approved-review door handles; no doubled underdrawing tails.
    new.paste(old.crop((24,114,43,163)),(24,114))
    d.line([(0,233),(96,221)],fill=(39,37,34),width=2)
    d.line([(0,236),(97,224)],fill=(211,197,164),width=1)
    # A few purposeful floor joints clarify receding boards behind the table;
    # no grain or repeated tiny marks are introduced.
    for pts in [[(0,251),(44,243),(82,239)],[(0,266),(52,254),(92,247)],[(47,277),(82,260),(99,251)]]:
        d.line(pts,fill=(95,81,64),width=1)
    save(m,'masks/NEW-18-occluded-room-reconstruction.png')
    return old,new

def table():
    im=blank();d=ImageDraw.Draw(im)
    # Relocated table begins to the RIGHT of the jamb. Cloth is a newly built
    # native layer, with weight/creases rather than stretched old table pixels.
    d.ellipse((100,222,297,254),fill=(119,115,92))
    d.polygon([(101,239),(295,240),(306,277),(92,277)],fill=(201,187,145))
    for poly,color in [
        ([(103,240),(126,245),(116,278),(93,278)],(164,155,122)),
        ([(128,244),(143,246),(146,278),(118,278)],(227,210,166)),
        ([(148,246),(161,247),(169,278),(149,278)],(164,155,122)),
        ([(170,247),(195,247),(204,278),(174,278)],(242,228,195)),
        ([(197,247),(210,246),(225,278),(207,278)],(164,155,122)),
        ([(215,245),(239,244),(253,278),(230,278)],(227,210,166)),
        ([(244,243),(262,242),(281,278),(259,278)],(164,155,122)),
        ([(269,241),(291,240),(303,278),(286,278)],(227,210,166)),
    ]:d.polygon(poly,fill=color)
    d.ellipse((100,222,297,249),fill=(227,210,166))
    d.ellipse((104,223,293,246),fill=(242,228,195))
    d.line([(111,242),(137,246),(201,247),(261,244),(289,239)],fill=(201,187,145),width=2)
    # Controlled tabletop shadows anchor objects instead of floating them.
    d.ellipse((145,231,247,241),fill=(164,155,122))
    d.ellipse((107,228,147,237),fill=(201,187,145))
    source=Image.open(ROOT/'references/before-wheel-removed.png').convert('RGBA')
    m=Image.new('L',SIZE);md=ImageDraw.Draw(m)
    md.polygon([(80,247),(218,242),(231,277),(80,277)],fill=255)
    part=source.copy();part.putalpha(m);im.alpha_composite(part,(80,0))
    save(m,'masks/source-clean-linen-clusters.png')
    return im

def bucket():
    src=Image.open(ROOT/'references/before-wheel-removed.png').convert('RGBA')
    m=Image.new('L',SIZE);d=ImageDraw.Draw(m)
    # Preserve the actual silver/ice pixel clusters, uniformly translated by42
    # native pixels. Separate handles have open negative space, not wall chips.
    d.polygon([(102,171),(180,171),(177,204),(170,233),(163,239),(117,239),(109,232),(104,208)],fill=255)
    d.polygon([(101,166),(115,166),(122,163),(130,165),(141,164),(151,166),(176,166),(186,170),(184,175),(173,179),(112,179),(103,176)],fill=255)
    d.ellipse((96,181,113,218),fill=255);d.ellipse((100,187,109,211),fill=0)
    d.ellipse((177,181,194,218),fill=255);d.ellipse((181,187,190,211),fill=0)
    d.rectangle((116,236,171,240),fill=255)
    cut=src.copy();cut.putalpha(m);im=blank();im.alpha_composite(cut,(42,0));save(m,'masks/source-bucket-silhouette.png')
    return im

def flowers_and_linen():
    src=Image.open(ROOT/'references/before-wheel-removed.png').convert('RGBA')
    m=Image.new('L',SIZE);d=ImageDraw.Draw(m)
    # Original clustered flower heads/leaves/vase, relocated without scaling.
    d.polygon([(37,186),(44,177),(45,171),(52,164),(59,161),(61,155),(68,150),(81,149),(88,155),(90,162),(96,169),(95,177),(98,186),(98,195),(87,200),(86,222),(59,222),(57,200),(43,197),(38,193)],fill=255)
    cut=src.copy();cut.putalpha(m);im=blank();im.alpha_composite(cut,(42,0))
    save(m,'masks/source-flower-vase-clusters.png')
    d=ImageDraw.Draw(im)
    # Three glasses and layered napkins are separate, deliberately sparse native
    # forms: no displaced bucket fragments or chair pixels enter the tabletop.
    for x,y,h in [(134,207,28),(143,214,24),(153,219,20)]:
        d.polygon([(x,y),(x+7,y+1),(x+7,y+h),(x,y+h-1)],fill=(164,178,156))
        d.rectangle((x+2,y+4,x+5,y+h-2),fill=(201,201,166))
        d.line([(x,y),(x+7,y+1),(x+7,y+h),(x,y+h-1),(x,y)],fill=(74,95,85),width=1)
        d.line([(x+1,y+2),(x+1,y+h-3)],fill=(242,244,214),width=1)
        d.line([(x,y+1),(x+7,y+2)],fill=(242,244,214),width=1)
    for y in [236,233,230]:
        d.polygon([(108,y),(130,y-3),(141,y+1),(117,y+5),(108,y+3)],fill=(164,155,122))
        d.polygon([(108,y-1),(130,y-4),(140,y),(117,y+3),(108,y+2)],fill=(242,228,195))
        d.line([(112,y+2),(135,y-1)],fill=(201,187,145),width=1)
    return im

def wheel():
    im=blank();d=ImageDraw.Draw(im)
    # Four-spoke brass PLUMBING valve. Open inner holes; no source wall tint,
    # nautical pegs, wooden tones or extra permanent foreground prop.
    d.ellipse((123,89,205,170),fill=(78,64,42))
    d.ellipse((125,90,203,168),fill=(185,145,71))
    d.ellipse((128,93,200,165),fill=(233,202,122))
    d.ellipse((132,97,196,161),fill=(124,95,51))
    d.ellipse((135,100,193,158),fill=(0,0,0,0))
    d.arc((126,91,201,166),190,285,fill=(252,229,173),width=2)
    d.arc((129,94,198,163),8,92,fill=(105,83,50),width=2)
    for points in [[(164,98),(164,158)],[(134,130),(194,130)]]:
        d.line(points,fill=(105,83,50),width=6)
        d.line([(x-1,y-1)for x,y in points],fill=(203,165,84),width=4)
        d.line([(x-2,y-2)for x,y in points],fill=(243,217,145),width=1)
    d.regular_polygon((164,130,9),6,rotation=30,fill=(105,83,50))
    d.regular_polygon((163,129,7),6,rotation=30,fill=(233,202,122))
    d.rectangle((161,127,165,132),fill=(78,64,42))
    d.line([(162,170),(162,175)],fill=(105,83,50),width=6)
    d.line([(161,170),(161,175)],fill=(233,202,122),width=2)
    return im

def fender():
    im=blank();d=ImageDraw.Draw(im)
    # A compact spherical bundle, built from overlapping nonradial bands.
    # Muted tan/slate/rust match the approved inspect. No hub or metallic rim.
    cx,cy,r=244,231,17
    disk=Image.new('L',SIZE);dd=ImageDraw.Draw(disk);dd.ellipse((cx-r,cy-r,cx+r,cy+r),fill=255)
    ball=blank();bd=ImageDraw.Draw(ball)
    bd.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(77,75,62))
    bd.ellipse((cx-r+2,cy-r+1,cx+r-2,cy+r-2),fill=(132,116,86))
    # Unequal, off-center paths visibly wrap in several directions.
    bands=[
        ([(223,221),(236,218),(252,221),(264,226)],(172,143,99),(213,188,141)),
        ([(226,239),(236,236),(249,232),(262,222)],(81,96,94),(132,146,140)),
        ([(230,212),(232,225),(240,237),(254,248)],(164,143,106),(215,191,149)),
        ([(243,211),(238,220),(234,234),(236,249)],(87,100,96),(135,146,137)),
        ([(221,232),(234,230),(250,234),(263,240)],(140,78,54),(181,111,77)),
        ([(253,213),(252,228),(246,241),(239,251)],(176,150,105),(220,195,148)),
        ([(229,245),(240,241),(253,237),(264,232)],(94,107,101),(140,151,140)),
        ([(225,217),(236,226),(250,227),(264,220)],(176,151,108),(218,192,146)),
        ([(249,211),(242,220),(240,228),(244,236),(256,245)],(140,78,54),(176,109,77)),
        ([(222,237),(233,242),(248,245),(262,239)],(172,149,109),(213,188,141)),
    ]
    for pts,shadow,light in bands:
        bd.line(pts,fill=shadow,width=5,joint='curve')
        bd.line([(x,y-1)for x,y in pts],fill=light,width=2,joint='curve')
    ball.putalpha(disk);im.alpha_composite(ball)
    # Folded napkin strip visibly travels from the bucket handle to the sphere.
    d=ImageDraw.Draw(im)
    d.polygon([(229,206),(236,207),(245,214),(248,219),(244,221),(238,215),(232,213),(227,211)],fill=(201,187,145))
    d.polygon([(229,207),(234,208),(242,214),(245,219),(243,219),(237,214),(231,212),(228,210)],fill=(242,228,195))
    d.polygon([(230,210),(227,207),(224,210),(226,214),(230,214),(233,217),(236,214),(233,211)],fill=(242,228,195))
    d.line([(229,210),(232,214),(234,213)],fill=(164,155,122),width=1)
    d.polygon([(228,213),(225,217),(226,222),(231,217),(233,214)],fill=(227,210,166))
    return im

def water(base, object_mask):
    im=blank();d=ImageDraw.Draw(im)
    shape=[(0,233),(28,229),(92,221),(98,223),(71,233),(56,239),(84,244),(108,250),(122,259),(133,269),(153,277),(130,277),(114,271),(96,263),(73,256),(47,252),(23,249),(0,250)]
    m=Image.new('L',SIZE);ImageDraw.Draw(m).polygon(shape,fill=255)
    # Select six coherent reflection/shadow ramps from the actual floor underlay.
    pixels=[]
    for y in range(SIZE[1]):
        for x in range(SIZE[0]):
            active=m.getpixel((x,y))and not object_mask.getpixel((x,y))
            c=base.getpixel((x,y))[:3]
            lum=(c[0]*3+c[1]*5+c[2]*2)//10
            wet=(67,84,76)if lum<72 else(83,100,88)if lum<90 else(106,120,102)if lum<111 else(135,145,121)if lum<139 else(162,166,139)if lum<170 else(165,177,153)
            pixels.append(wet+(255,)if active else(0,0,0,0))
    im.putdata(pixels);d=ImageDraw.Draw(im)
    for pts in [[(4,235),(31,231),(58,227),(91,223)],[(1,246),(22,247),(41,251),(53,252)],[(68,252),(82,256),(88,259)],[(109,267),(119,272),(130,276)]]:
        d.line(pts,fill=(179,192,166),width=1)
    # Restrict even edge glints to the wet floor mask and keep cloth opaque.
    im.putalpha(ImageChops.subtract(m,object_mask))
    return im

def main():
    old,room=geometry();save(room,'layers/NEW-18-reconstructed-room.png')
    parts={'table-and-cloth':table(),'silver-bucket':bucket(),'flowers-glasses-napkins':flowers_and_linen()}
    base=room.copy();objects=Image.new('L',SIZE)
    for name,part in parts.items():
        base=Image.alpha_composite(base,part);objects=ImageChops.lighter(objects,layer_mask(part));save(part,f'layers/NEW-18-{name}.png');save(layer_mask(part),f'masks/NEW-18-{name}.png')
    base=base.convert('RGB');save(base,'native/CH4-NEW-18-shared-base-v01.png')
    save(objects,'masks/NEW-18-all-table-props.png')
    delta=ImageChops.difference(old.convert('RGB'),base);difference=ImageChops.lighter(ImageChops.lighter(delta.getchannel('R'),delta.getchannel('G')),delta.getchannel('B')).point(lambda p:255 if p else 0);save(difference,'masks/NEW-18-geometry-correction.png')
    wheel_layer=wheel();fender_layer=fender();water_layer=water(base,objects)
    records=[]
    for name,part in [('wheel-mounted',wheel_layer),('rubber-band-fender',fender_layer),('water-emerging',water_layer)]:
        save(part,f'layers/NEW-18-{name}.png');save(layer_mask(part),f'masks/NEW-18-{name}.png');out=Image.alpha_composite(base.convert('RGBA'),part).convert('RGB');save(out,f'native/CH4-NEW-18-{name}-v01.png');records.append({'name':name,'layer':f'layers/NEW-18-{name}.png','allowedMask':f'masks/NEW-18-{name}.png','changedPixels':sum(p!=q for p,q in zip(base.get_flattened_data(),out.get_flattened_data())),'canonicalFocusId':None,'runtimeBinding':None,'newFlagsOrNodes':False})
    # Removed-wheel state deliberately has identical pixels/bytes to neutral base.
    (ROOT/'native/CH4-NEW-18-wheel-removed-v01.png').write_bytes((ROOT/'native/CH4-NEW-18-shared-base-v01.png').read_bytes())
    for name,part in [('wheel-mounted',wheel_layer),('rubber-band-fender',fender_layer)]:
        combined=Image.alpha_composite(Image.alpha_composite(base.convert('RGBA'),water_layer),part).convert('RGB');save(combined,f'previews/NEW-18-{name}-with-water-native.png')
    door_mask=Image.new('L',SIZE);ImageDraw.Draw(door_mask).polygon([(0,233),(96,221),(98,225),(0,237)],fill=255);save(door_mask,'masks/NEW-18-door-gap.png')
    data={'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'size':list(SIZE),'startingPlate':'references/before-wheel-removed.png','startingSha256':sha(ROOT/'references/before-wheel-removed.png'),'method':'Existing native room retained outside localized reconstruction; missing material/form information comes from the preserved clean-room source and is interpreted within old occluder masks using the existing palette plus native contour/cluster/threshold/floor work. Table/linen/glasses/napkins and props use separate native layers. Exact native bucket clusters translated42px without scaling; open handles kept. Wheel, wrapped spherical rubber-band fender, napkin knot and water are new native-grid localized layers. Generated clean underdrawing is interpreted only within the old occluder mask with existing material palette and native contour/cluster/threshold/floor corrections. No whole-image resize offered as finished art, no blur or procedural gradient. Exact native flower/vase and unobscured cloth clusters also translated without scaling.','bucketTranslationNativePixels':[42,0],'doorThresholdNativeEndpoints':[[0,233],[96,221]],'tableLeftX':92,'doorUnobstructedIntervalX':[0,91],'states':records,'wheelRemovedMatchesBase':True,'baseSha256':sha(ROOT/'native/CH4-NEW-18-shared-base-v01.png')}
    (ROOT/'evidence/background-derivation.json').write_text(json.dumps(data,indent=2)+'\n')
    for p in (ROOT/'native').glob('CH4-NEW-18-*.png'):
        im=Image.open(p);im.resize((2256,1112),Image.Resampling.NEAREST).save(ROOT/'previews'/(p.stem+'-4x.png'))
    print('Native shared geometry and four localized states constructed.')

if __name__=='__main__':main()
