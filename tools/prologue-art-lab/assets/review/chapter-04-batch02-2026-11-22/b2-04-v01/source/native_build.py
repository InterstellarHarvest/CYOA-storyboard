"""SOURCE-DERIVED native construction for seven B2-04 demands and three state frames.
Generated concepts/interpretations are references, not native-authorship claims.
All writes stay within this new review package; no approved image is edited.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,hashlib
from shared_native import save,mask,quiet_clusters,materialize,portrait
from materials import RAMP,nearest
import pixel_text
import block_letters
ROOT=Path(__file__).resolve().parents[1]
SIZE=(564,278)
def delta(a,b):
 points=[(i%a.width,i//a.width)for i,(x,y)in enumerate(zip(a.getdata(),b.getdata()))if x!=y]
 return {'changedPixels':len(points),'changedBounds':[min(x for x,y in points),min(y for x,y in points),max(x for x,y in points)+1,max(y for x,y in points)+1]if points else None}
def apply(base,layer):return Image.alpha_composite(base.convert('RGBA'),layer).convert('RGB')
def letter(text,quad,scale=2,color='#27342f'):
 layer=Image.new('RGBA',(block_letters.measure(text,scale)+4,5*scale+2));block_letters.draw(layer,text,(2,1),scale=scale,color=color)
 return pixel_text.project(layer,quad,size=SIZE)
def scene():
 id_='CH4-B2-19';size=(314,206);src=Image.open(ROOT/f'originals/{id_}-pixel-friendly.png').convert('RGB');under=src.resize(size,Image.Resampling.NEAREST);save(under,f'diagnostics/{id_}-direct-transfer.png')
 polys=[[(197,36),(242,39),(258,67),(284,67),(286,189),(273,192),(269,198),(203,198),(196,184),(190,174),(193,129)],[(184,84),(209,87),(213,106),(206,115),(210,146),(215,163),(194,198),(164,198),(163,188),(141,199),(117,199),(117,187),(157,127),(163,105),(176,98)],[(67,98),(116,98),(116,117),(141,117),(143,130),(156,130),(155,178),(119,179),(119,172),(81,165),(67,154)],[(0,148),(29,157),(31,206),(0,206)],[(197,188),(219,187),(232,191),(257,186),(262,196),(249,204),(210,205),(197,199)],[(128,50),(159,48),(160,85),(128,85)]]
 protect=mask(size,polys);floor=mask(size,[[(0,127),(68,123),(147,135),(314,183),(314,206),(0,206)]]);floor=ImageChops.subtract(floor,protect)
 save(protect,f'masks/{id_}-complete-story-objects.png');save(floor,f'masks/{id_}-floor.png')
 out=materialize(under)
 for y in range(206):
  for x in range(314):
   if protect.getpixel((x,y)):continue
   c=under.getpixel((x,y));r,g,b=c
   if 85<x<201 and y<104 and r>g and g>b and r>110:out.putpixel((x,y),nearest(c,RAMP['plaster']))
   elif floor.getpixel((x,y))and r>=g*.9 and b<=r and max(c)-min(c)<135:out.putpixel((x,y),nearest(c,RAMP['floor']if min(c)<150 else RAMP['cream']))
 out,pruned=quiet_clusters(out,protect,threshold=500)
 people=[[(184,85),(208,87),(214,107),(206,115),(210,149),(215,164),(195,198),(164,198),(162,186),(140,199),(117,199),(118,186),(157,128),(163,106),(177,98)],[(259,70),(280,70),(285,86),(282,109),(268,116),(255,105)]]
 for i,p in enumerate(people):
  pm=mask(size,[p]);npc=under.quantize(colors=48,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB');out.paste(npc,(0,0),pm);layer=Image.new('RGBA',size);layer.paste(npc,(0,0),pm);save(layer,f'layers/{id_}-npc-{i}.png');save(pm,f'masks/{id_}-npc-{i}.png')
 save(out,f'layers/{id_}-material-underpainting.png');before=out.copy();structure=Image.new('RGBA',size);d=ImageDraw.Draw(structure)
 # Native perspective grout and drain construction, clipped behind full props.
 for y in [139,155,176,201]:d.line((0,y,313,y),fill=RAMP['floor'][1]+(255,))
 for x in [6,75,146,223,307]:d.line([(72,124),(x,205)],fill=RAMP['floor'][1]+(255,))
 structure.putalpha(ImageChops.multiply(structure.getchannel('A'),floor))
 architecture=Image.new('RGBA',size);ad=ImageDraw.Draw(architecture)
 # Rebuild the louver's selected edge planes on the target grid.
 for y in [14,20,26,32,38,44]:ad.line((106,y,144,y-7),fill=RAMP['steel'][2]+(255,))
 ad.line((201,34,201,85),fill=RAMP['steel'][3]+(255,));ad.line((203,35,203,85),fill=RAMP['ink'][0]+(255,))
 architecture.putalpha(ImageChops.subtract(architecture.getchannel('A'),protect));out=apply(apply(out,structure),architecture)
 protected_changes=sum(a!=b and m>0 for a,b,m in zip(before.getdata(),out.getdata(),protect.getdata()))
 save(structure,f'layers/{id_}-floor-structure.png');save(architecture,f'layers/{id_}-architecture.png')
 # Independently authored short native signs, on their actual object planes.
 signage=Image.new('RGBA',size);sd=ImageDraw.Draw(signage)
 sd.polygon([(229,10),(272,5),(272,19),(229,24)],fill='#d4c6a3',outline='#34413c')
 text='BOILER';tw=block_letters.measure(text,1);block_letters.draw(signage,text,(230+(42-tw)//2,12),scale=1,color='#202c2d')
 sd.rectangle((131,55,157,81),fill='#c5b18c',outline='#34413c');tw=block_letters.measure('STAFF',1);block_letters.draw(signage,'STAFF',(132+(24-tw)//2,58),scale=1,color='#202c2d')
 sd.rectangle((133,68,155,77),fill='#894a4f');tw=block_letters.measure('SOLD',1);block_letters.draw(signage,'SOLD',(134+(20-tw)//2,70),scale=1,color='#f3e9c8')
 # No arrow is painted or left visible beneath SOLD.
 out=apply(out,signage);save(signage,f'layers/{id_}-native-lettering.png');save(signage.getchannel('A'),f'masks/{id_}-lettering.png')
 return out,{'method':'Separate generated pixel-friendly source; native semantic material/cluster decisions, perspective/architecture and lettering construction','quietSurfacePixelsMerged':pruned,'nativeStructuralPixelsChanged':delta(before,out)['changedPixels'],'structuralPassChangesInsideProtectedMask':protected_changes,'protectedStoryPolygons':polys,'shortNativeSigns':['BOILER','STAFF','SOLD'],'smallNPCs':'Separate gray uniform/head/hand clusters, no portrait-level anatomy'}
def closeup(id_):
 src=Image.open(ROOT/f'originals/{id_}-pixel-friendly.png').convert('RGB');under=src.resize(SIZE,Image.Resampling.NEAREST);save(under,f'diagnostics/{id_}-direct-transfer.png')
 # Richer Focus/background palettes than scene NPCs.128 is a local choice,
 # never a universal limit or a substitute for the visual quality comparison.
 out=under.quantize(colors=128,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB');out,pruned=quiet_clusters(out,threshold=500)
 if id_.endswith('24'):
  # Rare story colors receive their own material ramp, rather than losing the
  # pale BLUE ribbon in a palette dominated by wood and red upholstery.
  ribbon=mask(SIZE,[[(343,135),(368,137),(384,166),(413,186),(434,216),(416,223),(386,193),(363,176),(353,159)]])
  blue=[(38,71,88),(65,103,125),(91,139,165),(125,177,201),(164,207,223),(199,226,234)]
  for y in range(278):
   for x in range(564):
    c=under.getpixel((x,y))
    if ribbon.getpixel((x,y))and c[2]>c[0]*1.1 and c[1]>c[0]*1.05:out.putpixel((x,y),nearest(c,blue))
  save(ribbon,f'masks/{id_}-blue-ribbon-material.png')
  silver=mask(SIZE,[[(313,141),(325,135),(348,136),(362,146),(369,158),(365,170),(343,172),(318,160)]])
  ramp=[(40,44,49),(64,74,85),(99,113,126),(143,153,164),(184,196,205),(219,225,228),(241,242,233)]
  for y in range(135,173):
   for x in range(312,370):
    c=under.getpixel((x,y))
    if silver.getpixel((x,y))and min(c)>40 and max(c)-min(c)<75 and not(c[2]-c[0]>40 and c[1]-c[0]>20):out.putpixel((x,y),nearest(c,ramp))
  save(silver,f'masks/{id_}-silver-band-material.png')
 save(out,f'layers/{id_}-material-underpainting.png');layer=Image.new('RGBA',SIZE);d=ImageDraw.Draw(layer)
 if id_.endswith('23'):
  # Rebuild this plaque, including removing every formerly visible arrow tip.
  d.polygon([(150,51),(216,40),(216,115),(150,125)],fill='#d4bf95')
  d.polygon([(151,115),(216,105),(216,115),(151,125)],fill='#bba67d')
  for text,q in [('STAFF',[(162,56),(204,49),(204,60),(162,67)]),('LAVATORY',[(152,76),(213,66),(213,77),(152,87)])]:layer=Image.alpha_composite(layer,letter(text,q))
  d=ImageDraw.Draw(layer);d.polygon([(157,96),(209,82),(214,104),(162,118)],fill='#8e3034',outline='#612b2d')
  layer=Image.alpha_composite(layer,letter('SOLD',[(164,98),(206,87),(209,102),(167,113)],color='#f3e9c8'))
  # Boiler-access lettering uses the physical plaque plane, leaving its rim.
  d=ImageDraw.Draw(layer);d.polygon([(453,22),(555,6),(555,25),(453,42)],fill='#c5b18c')
  layer=Image.alpha_composite(layer,letter('BOILER ACCESS',[(457,23),(551,9),(551,23),(457,37)],scale=2))
  # Native crate hardware and calm wall repair edges, away from chair contours.
  d=ImageDraw.Draw(layer);d.line((218,247,237,247),fill='#b4bfb1');d.line((218,248,218,254),fill='#344b4a');d.rectangle((220,248,221,249),fill='#cec29e')
 elif id_.endswith('24'):
  # Native tack shank and stepped silver catch-light, preserving object shape.
  d.line((255,126,265,128),fill='#d5a345');d.point((256,125),fill='#f6e6aa')
  d.line((321,155,328,159),fill='#d6dbca');d.line((328,159,338,162),fill='#92a29a')
 elif id_.endswith('25'):
  # Native brace bevel/grain and loose-tack shank; the deep cavity stays empty.
  d.line((276,144,289,149),fill='#ac8758');d.line((294,151,307,156),fill='#8c6946');d.line((313,158,325,163),fill='#69503a')
  d.line((246,114,252,119),fill='#d5a345');d.point((247,113),fill='#eed17a')
 out=apply(out,layer);save(layer,f'layers/{id_}-native-details.png');save(layer.getchannel('A'),f'masks/{id_}-native-details.png')
 return out,{'method':'Separate pixel-friendly interpretation, source-informed native material/quiet-cluster decisions and native physical-detail/letter layer','quietSurfacePixelsMerged':pruned,'nativeDetailPixels':sum(a>0 for a in layer.getchannel('A').getdata()),'lettering':['STAFF','LAVATORY','SOLD','BOILER ACCESS']if id_.endswith('23')else[],'ringEngravingReadable':False}
def state_frames(primary):
 reports={};base=primary['CH4-B2-24'];layer=Image.new('RGBA',SIZE);d=ImageDraw.Draw(layer)
 # The existing loose fold is lifted a few pixels; ring/ribbon are retained.
 d.polygon([(304,134),(324,129),(344,130),(362,135),(372,143),(370,150),(357,141),(338,138),(310,143)],fill='#251c19')
 d.polygon([(302,130),(324,124),(344,125),(361,130),(370,138),(358,135),(342,131),(325,132),(304,137)],fill='#64202c')
 d.line([(306,131),(325,126),(344,127),(359,132)],fill='#a83c43',width=2)
 allowed=mask(SIZE,[[(298,119),(349,119),(377,139),(379,154),(303,151)]])
 layer.putalpha(ImageChops.multiply(layer.getchannel('A'),allowed));opened=apply(base,layer)
 save(layer,'layers/CH4-B2-24-open-native-object.png');save(allowed,'masks/CH4-B2-24-open-allowed.png')
 reports['CH4-B2-24-open']={'baseAssetId':'CH4-B2-24','allowedMask':'masks/CH4-B2-24-open-allowed.png',**delta(base,opened),'outsideAllowedChanges':sum(a!=b and not m for a,b,m in zip(base.getdata(),opened.getdata(),allowed.getdata()))}
 result={'CH4-B2-24-open':opened}
 base=primary['CH4-B2-25'];remove=Image.new('RGBA',SIZE);d=ImageDraw.Draw(remove)
 # Remove the upper caught ring in a bounded native object region, retain and
 # reconstruct its blue ribbon as an empty loop under the existing cloth flap.
 d.polygon([(305,118),(317,111),(337,112),(352,120),(355,133),(346,143),(318,141),(305,132)],fill='#081318')
 d.polygon([(308,128),(320,133),(341,138),(350,135),(346,143),(318,141)],fill='#0b171d')
 d.polygon([(332,107),(341,109),(355,121),(357,129),(350,132),(347,122),(338,116)],fill='#527b8e')
 d.line([(335,109),(343,113),(351,123)],fill='#8db8ca',width=2);d.line([(348,123),(351,130)],fill='#35596d',width=2)
 removed=apply(base,remove);save(remove,'layers/CH4-B2-25-ring-removed.png')
 allowed=mask(SIZE,[[(302,104),(344,104),(360,118),(362,146),(302,146)],[(350,189),(401,189),(401,223),(350,223)]])
 # The supplement is clipped to these actual object regions. Geometry outside
 # them, and all approved/historical PNGs, stays byte/pixel exact.
 remove.putalpha(ImageChops.multiply(remove.getchannel('A'),allowed));removed=apply(base,remove)
 recovered=removed.copy();ring=Image.new('RGBA',SIZE);rd=ImageDraw.Draw(ring)
 rd.ellipse((359,207,394,214),fill='#061016');rd.ellipse((360,193,391,210),fill='#405763');rd.ellipse((362,194,390,208),fill='#809aa6');rd.ellipse((364,195,387,202),fill='#101f26');rd.arc((361,193,391,209),0,165,fill='#bacfd2',width=2);rd.arc((363,195,389,208),10,160,fill='#576f80',width=2)
 # Reapply the existing brace/front-frame pixels wherever they occlude the
 # deeper ring. Dark cavity pixels permit the silver band to remain visible.
 occluder=Image.new('L',SIZE)
 for y in range(189,224):
  for x in range(350,402):
   if max(base.getpixel((x,y)))>65:occluder.putpixel((x,y),255)
 ring.putalpha(ImageChops.multiply(ImageChops.subtract(ring.getchannel('A'),occluder),allowed));slipped=apply(removed,ring)
 save(ring,'layers/CH4-B2-25-slipped-ring.png');save(occluder,'masks/CH4-B2-25-brace-front-occlusion.png');save(allowed,'masks/CH4-B2-25-states-allowed.png')
 for id_,im in [('CH4-B2-25-slipped',slipped),('CH4-B2-25-recovered',recovered)]:
  reports[id_]={'baseAssetId':'CH4-B2-25','allowedMask':'masks/CH4-B2-25-states-allowed.png',**delta(base,im),'outsideAllowedChanges':sum(a!=b and not m for a,b,m in zip(base.getdata(),im.getdata(),allowed.getdata()))}
  result[id_]=im
 return result,reports
def main():
 primary={};reports={}
 for n in range(19,26):
  id_=f'CH4-B2-{n:02}';im,r=scene()if n==19 else portrait(id_)if n in[20,21,22]else closeup(id_)
  primary[id_]=im;reports[id_]=r
 states,state_reports=state_frames(primary)
 for id_,im in {**primary,**states}.items():
  save(im,f'native/{id_}-v01.png');save(im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST),f'previews/{id_}-4x.png')
  r=reports.get(id_,state_reports.get(id_));r.update(sourceDerived=True,independentlyAuthoredAtNativeResolution=False,nativeSize=list(im.size),nativeColors=len(im.getcolors(im.width*im.height)),pillowVersion=Image.__version__)
 (ROOT/'evidence/native-reconstruction.json').write_text(json.dumps({'primary':reports,'states':state_reports},indent=2)+'\n');print('Constructed seven primary UNSELECTED assets plus three bounded object-state frames.')
if __name__=='__main__':main()
