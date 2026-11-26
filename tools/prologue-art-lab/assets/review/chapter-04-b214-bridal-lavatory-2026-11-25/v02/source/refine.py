"""One native material-and-lighting refinement. No large raster is read.

The immutable v01 recipe supplies the fixed room geometry and exact shells.
All new surfaces are painted at 314x206 with explicit material colour groups.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib
import base_native as B

ROOT = Path(__file__).resolve().parents[1]
B.ROOT = ROOT
C = B.c
W, H = 314, 206
EXTRA = {
    'plaster_warm': '#dbc09a', 'plaster_glaze': '#d6bd99',
    'plaster_repair': '#c3ae90', 'green_half': '#526b58',
    'green_recess': '#354f43', 'green_glint': '#809078',
    'stone_lit': '#e4d6b7', 'stone_half': '#cec0a4',
    'lamp_gold': '#f5d89b', 'lamp_core': '#fff0c7',
    'metal_half': '#7d8b75', 'metal_shadow': '#384d42',
}

def poly(d, points, colour): d.polygon(points, fill=colour)
def stroke(d, points, colour, width=1): d.line(points, fill=colour, width=width)

def walls(d, im):
    # Original perspective and room silhouette, with all surfaces still spotless.
    d.rectangle((0, 0, 313, 205), fill=C('cream', 2))
    poly(d, [(22,8),(292,8),(247,27),(67,27)], C('cream',3))
    poly(d, [(22,8),(67,27),(67,145),(22,185)], C('cream',2))
    d.rectangle((67,27,247,145), fill=C('cream',3))
    poly(d, [(247,27),(292,8),(292,185),(247,145)], C('cream',1))
    # Trowelled plaster / renewed paint, not speckled grime. Larger interlocking
    # clusters follow the wall's construction and light rather than random noise.
    poly(d, [(69,39),(89,39),(89,43),(119,43),(129,52),(130,61),(144,72),(149,86),(69,86)], EXTRA['plaster_glaze'])
    poly(d, [(72,42),(93,43),(105,49),(111,57),(121,68),(123,77),(127,85),(73,85)], EXTRA['plaster_warm'])
    poly(d, [(80,51),(92,49),(100,51),(108,57),(111,67),(119,73),(120,82),(85,82),(78,76)], C('cream',4))
    poly(d, [(92,55),(101,53),(106,57),(109,68),(105,74),(96,74),(90,66)], C('cream',5))
    poly(d, [(155,43),(180,43),(180,45),(211,45),(211,47),(236,47),(236,79),(226,79),(226,81),(193,81),(193,79),(163,79),(163,74),(155,74)], EXTRA['plaster_glaze'])
    poly(d, [(27,29),(31,31),(31,84),(37,85),(37,88),(26,92)], EXTRA['plaster_repair'])
    poly(d, [(262,43),(277,36),(278,80),(265,78)], C('cream',2))
    poly(d, [(279,35),(283,32),(283,87),(279,86)], C('cream',1))
    # A repaired cornice joint, sealed and painted over; no flaking dirty wall.
    stroke(d, [(225,37),(225,40),(228,40),(228,43)], EXTRA['plaster_repair'])
    stroke(d, [(226,37),(226,39),(229,39),(229,42)], EXTRA['plaster_glaze'])
    stroke(d, [(34,26),(37,28),(37,31)], C('cream',1))
    stroke(d, [(35,26),(38,28),(38,31)], C('cream',3))
    # The rail stays exactly above the counter as in v01. Raised paneling is
    # architectural millwork; no door, hatch, cupboard or concealed fixture.
    poly(d, [(22,100),(67,88),(247,88),(292,100),(292,185),(247,145),(67,145),(22,185)], C('green',2))
    poly(d, [(22,100),(67,88),(67,145),(22,185)], C('green',1))
    poly(d, [(247,88),(292,100),(292,185),(247,145)], C('green',1))
    poly(d, [(69,94),(112,94),(120,110),(132,126),(132,140),(69,140)], EXTRA['green_half'])
    stroke(d, [(22,100),(67,88),(247,88),(292,100)], C('brass',3))
    stroke(d, [(23,102),(67,90),(247,90),(291,102)], C('green',0))
    stroke(d, [(23,104),(67,92),(247,92),(291,104)], C('green',3))
    # Back wall: long uninterrupted inset, clearly fixed molding, no split doors.
    stroke(d, [(74,117),(74,135),(239,135),(239,117)], C('green',0))
    stroke(d, [(76,118),(76,133),(237,133),(237,118)], C('green',3))
    stroke(d, [(78,120),(78,131),(235,131)], EXTRA['green_recess'])
    stroke(d, [(78,131),(125,131)], EXTRA['green_half'])
    # Side-wall panel shapes share the existing perspective, not front-on boxes.
    stroke(d, [(28,107),(60,98),(60,141),(28,168),(28,107)], C('green',0))
    stroke(d, [(30,108),(58,100),(58,140),(30,163)], C('green',3))
    stroke(d, [(32,111),(55,104),(55,139),(32,158)], EXTRA['green_recess'])
    stroke(d, [(254,98),(286,107),(286,168),(254,141),(254,98)], C('green',0))
    stroke(d, [(256,100),(284,108),(284,163),(256,140)], C('green',3))
    stroke(d, [(258,104),(281,111),(281,158),(258,139)], EXTRA['green_recess'])
    # Baseboard with thickness and a narrow clean floor contact shadow.
    stroke(d, [(23,176),(67,139),(247,139),(291,176)], C('green',0), 2)
    stroke(d, [(23,178),(67,141),(247,141),(291,178)], C('green',3))
    stroke(d, [(23,181),(67,143),(247,143),(291,181)], EXTRA['green_recess'])
    stroke(d, [(22,184),(67,145),(247,145),(292,184)], C('green',0), 2)

def floor(d, im):
    # Every tile is projected through the original VP(157,65). Flat categorical
    # shade groups, clipped to the unchanged floor; no gradient or dithering.
    floor_mask=Image.new('L',(W,H));md=ImageDraw.Draw(floor_mask)
    footprint=[(67,146),(247,146),(292,186),(292,205),(22,205),(22,186)]
    md.polygon(footprint,fill=255)
    painting=Image.new('RGBA',(W,H));q=ImageDraw.Draw(painting)
    def xat(x,y): return round(157+(x-157)*(y-65)/81)
    rows=[146,155,169,188,214];xs=[67,103,139,175,211,247]
    shades=[[2,3,2,2,1],[2,2,3,2,2],[2,3,2,2,2],[3,2,2,3,2]]
    for row,(y0,y1) in enumerate(zip(rows,rows[1:])):
        for col,(x0,x1) in enumerate(zip(xs,xs[1:])):
            a,b=xat(x0,y0),xat(x1,y0);e,f=xat(x0,y1),xat(x1,y1)
            tone=C('stone',shades[row][col]);p=[(a,y0),(b,y0),(f,y1),(e,y1)]
            poly(q,p,tone)
            # Readable stone-cut variation at edges; individual tiles, no grid
            # filled with a repeated noise texture.
            if (row,col) in [(0,1),(1,3),(2,0),(2,3),(3,1)]:
                poly(q,[(a+3,y0+2),(b-4,y0+2),(b-8,y0+4),(a+6,y0+4)],EXTRA['stone_half'])
            if (row,col) in [(1,1),(2,2),(3,4)]:
                poly(q,[(e+4,y1-3),(f-4,y1-3),(f-8,y1-6),(e+9,y1-6)],EXTRA['stone_half'])
            stroke(q,[(a,y0),(b,y0),(f,y1)],C('stone',1))
            stroke(q,[(a+1,y0+1),(b-1,y0+1)],EXTRA['stone_half'])
    # Softly stepped reflected lamp light broken by the physical tile seams.
    for points,col in [
        ([(105,148),(109,148),(109,153),(104,153)],EXTRA['stone_half']),
        ([(102,157),(108,157),(108,160),(105,161),(105,167),(100,167)],C('stone',3)),
        ([(103,158),(105,158),(105,164),(102,164)],EXTRA['stone_lit']),
        ([(95,172),(105,172),(103,180),(99,180),(98,186),(93,186)],EXTRA['stone_half']),
        ([(97,173),(100,173),(99,181),(96,181)],C('stone',3)),
        ([(86,192),(98,192),(95,198),(91,198),(89,205),(84,205)],EXTRA['stone_half'])]: poly(q,points,col)
    # Directional skirting shadows stay close to surfaces. No puddles/footprints.
    poly(q,[(67,146),(247,146),(250,149),(65,149)],C('stone',1))
    stroke(q,[(247,147),(292,187)],C('stone',0))
    stroke(q,[(67,147),(24,186)],C('stone',1))
    # Grout is the final tile construction layer so adjoining tile fills cannot
    # paint over the shared vertical seams. All lines share the original VP.
    for x in xs:
        stroke(q,[(xat(x,146),146),(xat(x,214),214)],C('stone',1))
        stroke(q,[(xat(x,147)+1,147),(xat(x,214)+1,214)],EXTRA['stone_half'])
    for y in rows[1:-1]:
        stroke(q,[(xat(67,y),y),(xat(247,y),y)],C('stone',1))
        stroke(q,[(xat(67,y+1),y+1),(xat(247,y+1),y+1)],EXTRA['stone_half'])
    painting.putalpha(floor_mask);im.alpha_composite(painting)

def cornices(d, im):
    # Stepped plaster crown molding and finely modeled original decorative field.
    for pts in [[(23,12),(66,30),(247,30),(291,12)],[(23,15),(66,33),(247,33),(291,15)]]:
        stroke(d,pts,C('cream',1));stroke(d,[(x,y-1)for x,y in pts],C('cream',4))
    for pts in [[(75,51),(81,51),(83,47),(139,47)],[(174,47),(230,47),(234,51),(240,51)],[(75,52),(75,80),(81,80),(84,84),(231,84),(235,80),(240,80),(240,52)]]:
        stroke(d,[(x+1,y+1)for x,y in pts],C('cream',1))
        stroke(d,pts,C('cream',2))
        stroke(d,[(x-1,y-1)for x,y in pts],C('cream',4))
    # Shadowed fillet at each wall's near edge, then lit inner rebate.
    for pts in [[(29,31),(58,44),(58,84),(29,94)],[(258,44),(284,31),(284,92),(258,83)]]:
        stroke(d,[(x+1,y+1)for x,y in pts],C('cream',0))
        stroke(d,pts,C('cream',1))
        stroke(d,[(x-1,y-1)for x,y in pts],C('cream',3))
    stroke(d,[(32,35),(54,45),(54,81),(32,89)],C('cream',3))
    stroke(d,[(261,46),(280,37),(280,86),(261,80)],C('cream',2))
    # Painted-over hairline stress only where crown and wall join; clean finish.
    stroke(d,[(69,37),(70,41),(73,43)],EXTRA['plaster_repair'])
    stroke(d,[(70,37),(71,40),(74,42)],EXTRA['plaster_glaze'])

def duct(d, im):
    # Same ventilation trunk and grille. Faces, folded seams and support contacts
    # are actual native forms; no new technology or additions to the silhouette.
    poly(d,[(68,35),(254,32),(254,40),(240,44),(71,44)],C('cream',2))
    poly(d,[(70,36),(251,33),(249,38),(240,40),(70,40)],C('cream',1))
    poly(d,[(56,18),(68,12),(254,12),(272,6),(272,28),(255,34),(67,39),(55,33)],C('steel',1))
    poly(d,[(68,14),(254,14),(254,18),(68,19)],C('steel',3))
    poly(d,[(68,19),(254,18),(254,29),(68,34)],C('steel',2))
    poly(d,[(68,30),(254,26),(254,30),(68,35)],EXTRA['metal_half'])
    poly(d,[(68,35),(254,30),(254,33),(68,38)],EXTRA['metal_shadow'])
    poly(d,[(57,20),(66,16),(66,34),(56,31)],C('steel',2))
    poly(d,[(255,14),(270,8),(270,26),(255,31)],C('steel',2))
    poly(d,[(257,16),(268,11),(268,25),(257,29)],EXTRA['metal_half'])
    stroke(d,[(68,14),(253,14),(270,7)],C('steel',4))
    stroke(d,[(68,36),(254,31),(270,26)],C('steel',0))
    # Sheet joints: bright folded edge against a dark recessed seam.
    for x in [97,132,193,224]:
        y=round(34-(x-68)*4/186)
        stroke(d,[(x,17),(x,y)],C('steel',1))
        stroke(d,[(x+1,18),(x+1,y-1)],C('steel',3))
    stroke(d,[(58,21),(64,18)],C('steel',3))
    stroke(d,[(58,30),(64,33)],C('steel',1))
    # Two old coating scuffs underneath the fresh wiped-down metal surface.
    poly(d,[(121,25),(126,25),(126,26),(129,26),(129,28),(123,28),(123,27),(121,27)],C('steel',1))
    stroke(d,[(122,24),(126,24)],C('steel',3))
    poly(d,[(229,22),(232,22),(232,23),(235,23),(235,25),(230,25)],C('steel',1))
    # Grille depth: each lip has a lit upper edge and a dark opening beneath.
    B.bevel(d,(148,15,182,31),C('steel',0),C('steel',3),C('steel',0))
    stroke(d,[(149,16),(181,16)],C('steel',4))
    for y in [18,22,26,30]:
        stroke(d,[(151,y),(179,y)],C('steel',3))
        stroke(d,[(152,y+1),(179,y+1)],C('steel',1))
    for x,y in [(82,13),(113,0),(209,0),(239,13)]:
        poly(d,[(x+2,y+1),(x+5,y+1),(x+5,35),(x+8,37),(x+5,41),(x+1,39)],C('steel',0))
        poly(d,[(x,y),(x+3,y),(x+3,35),(x+6,36),(x+5,39),(x,37)],C('steel',1))
        stroke(d,[(x,y),(x,34),(x+2,37)],C('steel',3))
        stroke(d,[(x+2,y+2),(x+2,34)],EXTRA['metal_shadow'])
        for yy in ([y+5,30] if y>0 else [5,20,31]):
            d.rectangle((x,yy,x+1,yy+1),fill=C('steel',0));d.point((x,yy),fill=C('steel',4))

def lamp_and_frame(d, im):
    # Original lamp footprint and direction; milky glass, brass cage, cast shadow.
    poly(d,[(103,55),(110,60),(111,74),(107,81),(102,79)],C('cream',1))
    poly(d,[(105,57),(109,61),(109,73),(105,78)],C('cream',2))
    poly(d,[(99,55),(105,55),(107,59),(106,76),(102,79),(98,76)],C('brass',1))
    d.ellipse((99,51,103,55),fill=C('brass',3))
    stroke(d,[(100,51),(102,51)],EXTRA['lamp_gold'])
    poly(d,[(96,57),(99,54),(105,55),(107,58),(105,60),(97,60)],C('brass',2))
    stroke(d,[(97,57),(100,55),(104,56)],C('brass',4))
    stroke(d,[(97,59),(105,59)],C('brass',0))
    d.rectangle((99,60,104,71),fill=C('brass',3))
    d.rectangle((99,60,102,70),fill=EXTRA['lamp_gold'])
    d.rectangle((100,61,101,69),fill=EXTRA['lamp_core'])
    stroke(d,[(104,60),(104,71)],C('brass',1))
    B.bevel(d,(98,72,105,75),C('brass',2),C('brass',4),C('brass',0))
    stroke(d,[(99,73),(103,73)],C('brass',3))
    d.rectangle((101,76,103,79),fill=C('brass',1));d.point((101,76),fill=C('brass',4))
    # Original doorway boundaries; more convincing varnished edge / rebate.
    d.rectangle((0,0,21,205),fill=C('green',0));d.rectangle((292,0,313,205),fill=C('green',0))
    d.rectangle((12,0,16,205),fill=C('green',1));stroke(d,[(13,0),(13,205)],EXTRA['green_recess'])
    stroke(d,[(18,0),(18,205)],C('brass',2));stroke(d,[(19,0),(19,205)],C('brass',0))
    stroke(d,[(21,0),(21,205)],C('green',3))
    d.rectangle((298,0,303,205),fill=C('green',1));stroke(d,[(300,0),(300,205)],EXTRA['green_recess'])
    stroke(d,[(294,0),(294,205)],C('brass',2));stroke(d,[(295,0),(295,205)],C('brass',0))

def counter_details(d, im):
    # Top/back silhouette remains [(94,94),(220,94),(242,104),(72,104)].
    # Marble only within that slab; veins are sparse branching mineral features.
    poly(d,[(94,95),(124,95),(117,99),(89,99)],C('stone',4))
    poly(d,[(170,95),(194,95),(203,99),(173,99)],EXTRA['stone_lit'])
    poly(d,[(207,96),(219,96),(232,102),(216,102)],EXTRA['stone_half'])
    stroke(d,[(84,102),(95,100),(103,100),(110,97),(116,97),(122,95)],C('stone',2))
    stroke(d,[(88,102),(97,101),(104,101)],C('stone',4))
    stroke(d,[(177,95),(182,97),(192,98),(199,101),(209,102),(218,101)],C('stone',2))
    stroke(d,[(194,98),(202,97),(208,97)],C('stone',2))
    stroke(d,[(179,95),(184,96)],C('stone',4))
    stroke(d,[(211,98),(218,99),(226,99)],C('stone',3))
    # Lit arris / bullnose / shadow face: same six-pixel thickness, more volume.
    stroke(d,[(73,104),(241,104)],C('stone',4))
    stroke(d,[(74,105),(241,105)],EXTRA['stone_lit'])
    stroke(d,[(73,106),(241,106)],C('stone',2))
    stroke(d,[(73,108),(241,108)],C('stone',1))
    stroke(d,[(74,109),(240,109)],C('stone',0))
    stroke(d,[(73,110),(241,110)],C('brass',2))
    stroke(d,[(78,110),(130,110)],C('brass',4))
    for pts in [[(94,106),(100,107),(108,107)],[(166,106),(173,107),(180,107)],[(221,106),(225,107),(234,107)]]:stroke(d,pts,C('stone',1))
    # Counter/wall and bracket attachment shadows are geometric, not random marks.
    poly(d,[(78,111),(235,111),(233,115),(222,119),(116,119),(91,116)],C('green',1))
    stroke(d,[(85,111),(231,111)],C('green',0),2)
    for x in [100,218]:
        poly(d,[(x+3,113),(x+9,115),(x+9,129),(x+5,131),(x+4,126)],C('green',1))
        stroke(d,[(x+4,113),(x+6,116),(x+6,127)],C('green',0))
        d.rectangle((x,112,x+3,127),fill=C('brass',1))
        stroke(d,[(x,112),(x+2,113),(x+2,125)],C('brass',3))
        stroke(d,[(x+2,121),(x+7,113)],C('brass',2),2)
        stroke(d,[(x+2,119),(x+6,113)],C('brass',4))
        stroke(d,[(x+1,126),(x+3,126)],C('brass',0));d.point((x+1,125),fill=C('brass',4))

def main():
    for sub in ['layers','native','previews','masks','evidence']:(ROOT/sub).mkdir(exist_ok=True)
    a=B.Art('room',(W,H))
    a.add('plaster-and-paneling',walls)
    a.add('projected-stone-tiles',floor)
    a.add('architectural-moldings',cornices)
    a.add('modeled-original-duct',duct)
    a.add('original-lamp-and-doorframe',lamp_and_frame)
    a.add('original-counter-geometry',B.counter)
    a.add('stone-edge-and-bracket-modeling',counter_details)
    B.add_shells(a,[(113,100,20,13,'smooth'),(157,100,21,13,'ridged'),(201,100,20,13,'third')])
    a.save('CH4-NEW-02-bridal-lavatory-v02')
    (ROOT/'evidence/native-layer-recipes.json').write_text(json.dumps(B.RECIPES,indent=2)+'\n')
    (ROOT/'evidence/material-ramps.json').write_text(json.dumps({'base':B.P,'refinement':EXTRA},indent=2)+'\n')
    (ROOT/'evidence/shell-identities.json').write_text(json.dumps(B.SHELLS,indent=2)+'\n')
    p=ROOT/'native/CH4-NEW-02-bridal-lavatory-v02.png'
    image=Image.open(p)
    print(json.dumps({'file':str(p.relative_to(ROOT)),'sha256':B.sha(p),'size':list(image.size),'colours':len(image.getcolors(W*H)),'status':'UNSELECTED'}))

if __name__=='__main__':main()
