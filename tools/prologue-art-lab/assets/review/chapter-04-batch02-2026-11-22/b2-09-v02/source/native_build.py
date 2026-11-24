"""Source-derived B2-09 native interpretation, never edits approved artwork.
Detailed concepts -> separate pixel-friendly source -> semantic native paint,
protected props/figures, structure/water and conditional object construction.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,hashlib,subprocess,sys
from shared_native import mask,quiet_clusters
from materials import nearest
ROOT=Path(__file__).resolve().parents[1]
RAMPS={
 'gold':['#443a29','#695332','#95733d','#bd9551','#dfbb71','#f3d991','#fff0b7'],
 'silver':['#333e3c','#57635e','#7f8980','#a7afa1','#cbd0bd','#e2e4d0','#fbf2d5'],
 'linen':['#77735c','#a49b7a','#c9bb91','#e3d2a6','#f2e4c3','#fff2d7'],
 'wood':['#3d3930','#5f5140','#826b4e','#a08761','#bca17a','#d3b78d','#e6cca4'],
 'plaster':['#787360','#a39b80','#bcb194','#d3c5a4','#e7d7b5','#f6e8c8'],
 'steel':['#273e3b','#425a50','#60756a','#829185','#acb7a4','#d0d9bd'],
 'red':['#362d31','#593339','#7c3b43','#9c4b52','#ba6b69','#d69b89'],
 'water':['#536f6c','#829c95','#b4c7bc','#e3e9d2']}
RAMPS={k:[tuple(bytes.fromhex(c[1:]))for c in v]for k,v in RAMPS.items()}
LAYOUT={48:{'size':(314,206),'wheel':[(128,70),(154,70),(168,77),(169,109),(128,109)],'bucket':[(129,101),(169,101),(170,130),(130,130)],'table':[(79,116),(180,116),(192,174),(170,181),(77,181)],'chair':[(63,112),(90,111),(112,152),(114,188),(62,188)],'npc':[(230,37),(258,35),(276,47),(277,108),(270,132),(270,171),(276,190),(211,191),(211,182),(221,165),(217,117),(203,104),(185,94),(184,79),(205,77),(221,82),(224,59)],'floor':[(0,151),(63,148),(82,155),(199,145),(314,126),(314,206),(0,206)],'ball':(172,119,11)},
51:{'size':(564,278),'wheel':[(96,81),(174,79),(197,110),(197,179),(98,179)],'bucket':[(98,165),(196,165),(198,244),(99,244)],'table':[(18,226),(218,221),(233,278),(17,278)],'chair':[(0,206),(17,207),(34,247),(67,269),(67,278),(0,278)],'npc':None,'floor':[(0,213),(62,213),(214,225),(485,204),(564,207),(564,278),(0,278)],'ball':(200,220,22)}}
def save(im,rel):im.save(ROOT/rel)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def apply(a,b):return Image.alpha_composite(a.convert('RGBA'),b).convert('RGB')
def delta(a,b):return sum(x!=y for x,y in zip(a.get_flattened_data(),b.get_flattened_data()))
def interpret(under,num,protect,save_masks=False,extra_npc=None,wheel_present=True):
 s=LAYOUT[num];sz=s['size'];out=under.quantize(colors=96 if num==48 else 128,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB');bucket=mask(sz,[s['bucket']]);table=mask(sz,[s['table']]);wheel=mask(sz,[s['wheel']]);floor=ImageChops.subtract(mask(sz,[s['floor']]),protect);npc=mask(sz,[s['npc']])if s['npc']else Image.new('L',sz);ms={k:Image.new('L',sz)for k in RAMPS}
 if extra_npc is not None:npc=ImageChops.lighter(npc,extra_npc)
 lamp=mask(sz,[[(159,46),(177,46),(178,75),(159,75)]]if num==48 else[[(250,67),(278,67),(282,118),(250,118)]])
 if save_masks:save(lamp,f'masks/CH4-B2-{num}-lamp-material-protection.png')
 for y in range(sz[1]):
  for x in range(sz[0]):
   if npc.getpixel((x,y)):continue
   r,g,b=under.getpixel((x,y));key=None
   if lamp.getpixel((x,y)):
    if r>g*1.1 and g>b*1.2:key='gold'
   elif bucket.getpixel((x,y))and max(r,g,b)-min(r,g,b)<75:key='silver'
   elif table.getpixel((x,y))and r>g*.98 and g>b*1.1 and r>115:key='linen'
   elif wheel_present and wheel.getpixel((x,y))and ((r>g*1.15 and g>b*1.35)or(r>g*1.06 and g>b*1.55 and r>190)if num==48 else r>g*1.1 and g>b*1.2):key='gold'
   elif floor.getpixel((x,y))and r>g and g>b:key='wood'
   elif r>g*1.4 and b>g*.72:key='red'
   elif g>r*.95 and b>r*.8 and max(r,g,b)-min(r,g,b)<80:key='steel'
   elif (75<x<224 and 38<y<101 if num==48 else 205<x<480 and 55<y<161)and r>g*1.04 and g>b*1.1 and r>120:key='plaster'
   if key:out.putpixel((x,y),nearest((r,g,b),RAMPS[key]));ms[key].putpixel((x,y),255)
 if num==48:
  # A separate local scene-figure fit preserves silhouette/color while keeping
  # miniature faces/clothes simpler than the64-tone portrait foregrounds.
  small=under.quantize(colors=40,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB');out.paste(small,(0,0),npc)
 if save_masks:
  for k,m in ms.items():save(m,f'masks/CH4-B2-{num}-{k}-material.png')
 out,merged=quiet_clusters(out,ImageChops.lighter(protect,npc),threshold=500);return out,merged
def ball_layer(num):
 size=LAYOUT[num]['size'];cx,cy,r=LAYOUT[num]['ball'];im=Image.new('RGBA',size);shade=Image.new('RGBA',(2*r+3,2*r+3));d=ImageDraw.Draw(shade);R=r+1;clip=Image.new('L',shade.size);ImageDraw.Draw(clip).ellipse((1,1,2*r+1,2*r+1),fill=255)
 d.ellipse((1,1,2*r+1,2*r+1),fill='#666654');d.ellipse((2,2,2*r-2,2*r-2),fill='#999681');d.polygon([(1,R),(R,1),(R+3,R),(R-2,2*r+1)],fill='#bdb39a')
 # Source-informed native rubber bands follow deliberate wrapped paths from
 # the exact approved inspect reference; never paste a tiny downsampled ball.
 bands=[([(-.9,-.25),(-.4,-.65),(.3,-.8),(.8,-.35)],'#cdbd98',.22),([(-.55,-.85),(-.2,-.3),(.4,.15),(.85,.65)],'#6f8583',.18),([(-.8,.65),(-.55,0),(-.15,-.6),(.2,-.95)],'#a0674c',.15),([(-.9,.2),(-.4,.1),(.15,.35),(.75,.8)],'#bfb394',.22),([(-.6,.85),(-.1,.5),(.4,-.1),(.7,-.65)],'#506b6e',.18),([(-.85,-.6),(-.25,-.35),(.3,-.2),(.85,-.35)],'#d6c7a5',.19),([(-.1,.95),(.5,.45),(.55,-.2),(.25,-.85)],'#98664f',.14),([(-.95,.0),(-.45,.5),(.2,.65),(.8,.25)],'#cab99a',.18),([(-.4,-.9),(.2,-.55),(.65,.0),(.65,.65)],'#85928c',.13)]
 for points,color,width in (bands[:5]if num==48 else bands):
  pts=[(round(R+x*r),round(R+y*r))for x,y in points];w=max(1,round(r*width));d.line(pts,fill='#4e5145',width=w+2,joint='curve');d.line(pts,fill=color,width=w,joint='curve')
 shade.putalpha(clip);im.alpha_composite(shade,(cx-r-1,cy-r-1));nd=ImageDraw.Draw(im)
 # The authored tie is a length of ivory NAPKIN, never rope or a new item.
 if num==48:pts=[(167,114),(170,111),(175,111),(176,113)]
 else:pts=[(192,193),(196,194),(200,198),(202,201)]
 nd.line(pts,fill='#8d8870',width=3 if num==48 else 5);nd.line([(x,y-1)for x,y in pts],fill='#eee2c3',width=2 if num==48 else 3);save(im,f'layers/CH4-B2-{num}-native-rubber-fender-and-napkin.png');return im
def environment(num):
 id_=f'CH4-B2-{num}';s=LAYOUT[num];sz=s['size'];pixel_file=f'originals/{id_}-pixel-friendly-readability.png'if num==48 else f'originals/{id_}-pixel-friendly.png';under=Image.open(ROOT/pixel_file).convert('RGB').resize(sz,Image.Resampling.NEAREST);save(under,f'diagnostics/{id_}-direct-transfer.png');polys=[s['wheel'],s['bucket'],s['table'],s['chair']]
 if s['npc']:polys.append(s['npc'])
 protect=mask(sz,polys);save(protect,f'masks/{id_}-complete-story-objects.png');floor=ImageChops.subtract(mask(sz,[s['floor']]),protect);save(floor,f'masks/{id_}-floor.png');out,merged=interpret(under,num,protect,True);save(out,f'layers/{id_}-native-material-underpainting.png');before=out.copy()
 structure=Image.new('RGBA',sz);d=ImageDraw.Draw(structure)
 # Selected native parquet edge planes follow the source's floor perspective;
 # all later floor work is clipped behind full props, handles, chair and shoes.
 lines=[]if num==48 else[(238,265,303,265),(309,245,374,245),(405,271,466,271),(478,232,532,232)]
 for line in lines:d.line(line,fill='#756145')
 structure.putalpha(ImageChops.multiply(structure.getchannel('A'),floor));out=apply(out,structure);save(structure,f'layers/{id_}-native-parquet-edges.png')
 details=Image.new('RGBA',sz);dd=ImageDraw.Draw(details)
 if num==48:
  dd.line((136,128,159,128),fill='#d5daca');dd.line((136,126,158,126),fill='#65736b');dd.point((132,114),fill='#e6e8d4');dd.point((168,114),fill='#e6e8d4')
  dd.line((174,13,174,31),fill='#8da291');dd.point((175,15),fill='#d5d8ba');dd.point((175,29),fill='#d5d8ba')
 else:
  dd.line((113,240,173,240),fill='#dae0ca');dd.line((114,238,173,238),fill='#65736b');dd.point((102,187),fill='#eef0dc');dd.point((192,187),fill='#eef0dc')
  dd.line((366,24,366,49),fill='#9bab95');dd.point((368,27),fill='#e1e4c7');dd.point((368,46),fill='#e1e4c7')
 out=apply(out,details);save(details,f'layers/{id_}-native-silver-duct-details.png')
 if num==48:
  wear=Image.new('RGBA',sz);wd=ImageDraw.Draw(wear);wd.line([(146,36),(146,39),(144,41)],fill='#a39b80');wd.polygon([(184,49),(187,51),(186,56),(183,55)],fill='#a39b80');wd.polygon([(178,21),(181,22),(180,24),(177,24)],fill='#60756a');out=apply(out,wear);save(wear,f'layers/{id_}-sparse-connected-wear.png')
 primary=out.copy();wheel_allowed=mask(sz,[s['wheel']]);clean_file=f'originals/{id_}-wheel-removed-readability-reference.png'if num==48 else f'originals/{id_}-wheel-removed-reference.png';clean=Image.open(ROOT/clean_file).convert('RGB').resize(sz,Image.Resampling.NEAREST);clean,_=interpret(clean,num,protect,wheel_present=False);remove=clean.convert('RGBA');remove.putalpha(wheel_allowed);empty=apply(primary,remove);save(remove,f'layers/{id_}-wheel-handoff-object.png');save(wheel_allowed,f'masks/{id_}-wheel-handoff-allowed.png')
 trade_layer=ball_layer(num);trade=apply(empty,trade_layer);trade_allowed=ImageChops.lighter(wheel_allowed,trade_layer.getchannel('A'));save(trade_allowed,f'masks/{id_}-trade-allowed.png')
 emergency=empty.copy();emergency_allowed=wheel_allowed.copy()
 if num==48:
  # Exact authored final emergency beat: changed Bixby, one slipping guest,
  # a second drill chair and shallow advancing water. No extra cast appears.
  src=Image.open(ROOT/'originals/CH4-B2-48-emergency-readability-reference.png').convert('RGB').resize(sz,Image.Resampling.NEAREST)
  ep=[[(229,35),(263,35),(283,55),(285,130),(282,192),(219,192),(219,170),(224,134),(222,111),(218,101),(196,100),(192,92),(194,82),(209,79),(222,82),(225,61)],[(169,90),(186,90),(194,102),(211,103),(217,96),(226,96),(228,107),(218,114),(216,143),(221,162),(217,170),(203,171),(193,182),(176,181),(177,161),(163,150),(157,143),(156,135),(163,128),(163,111)],[(113,126),(132,125),(143,148),(161,155),(165,190),(157,192),(118,191)]]
  guide,_=interpret(src,num,protect,extra_npc=mask(sz,ep[:2]),wheel_present=False)
  # Local facial clusters retain the slipping guest's small eye/open mouth;
  # a whole-room palette fit otherwise spends those rare colors on plaster.
  facebox=(179,96,195,115);face=src.crop(facebox);paint=face.quantize(colors=8,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
  for yy in range(paint.height):
   for xx in range(paint.width):
    r,g,b=face.getpixel((xx,yy))
    if r>140 and g<r*.63 and b>r*.4:paint.putpixel((xx,yy),(128,66,54))
  local=Image.new('RGBA',sz);local.paste(paint,facebox[:2]);fm=Image.new('L',sz);ImageDraw.Draw(fm).rectangle((179,96,194,114),fill=255);fm=ImageChops.multiply(fm,mask(sz,ep[:2]));local.putalpha(fm);guide=apply(guide,local);save(local,f'layers/{id_}-guest-native-face-clusters.png');save(fm,f'masks/{id_}-guest-face-protection.png')
  em=ImageChops.lighter(mask(sz,ep),mask(sz,[s['npc']]));water=Image.new('L',sz)
  for y in range(sz[1]):
   for x in range(sz[0]):
    r,g,b=src.getpixel((x,y))
    if floor.getpixel((x,y))and min(r,g,b)>90 and max(r,g,b)-min(r,g,b)<55 and b>r*.9 and g>r*.92:water.putpixel((x,y),255)
  em=ImageChops.lighter(em,water);patch=guide.convert('RGBA');patch.putalpha(em);emergency=apply(emergency,patch);emergency_allowed=ImageChops.lighter(emergency_allowed,em);save(patch,f'layers/{id_}-emergency-figures-chairs-water.png');save(water,f'masks/{id_}-advancing-shallow-water.png')
 save(emergency_allowed,f'masks/{id_}-emergency-allowed.png');ims={id_:primary,id_+'-emergency':emergency,id_+'-trade':trade};states={}
 for name,im,allowed in [('emergency',emergency,emergency_allowed),('trade',trade,trade_allowed)]:states[name]={'changedPixels':delta(primary,im),'outsideAllowedChanges':sum(a!=b and not c for a,b,c in zip(primary.get_flattened_data(),im.get_flattened_data(),allowed.get_flattened_data())),'allowedMask':f'masks/{id_}-{name}-allowed.png','wheelMounted':False,'rubberFenderAttached':name=='trade'}
 return ims,{'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'nativeSize':list(sz),'localBasePalette':96 if num==48 else 128,'quietSurfacePixelsMerged':merged,'nativeStructureChangesInsideProtectedObjects':sum(a!=b and m for a,b,m in zip(before.get_flattened_data(),apply(before,structure).get_flattened_data(),protect.get_flattened_data())),'states':states,'sourcePixelFriendly':{'file':pixel_file,'sha256':sha(ROOT/pixel_file)},'cleanWheelReference':{'file':clean_file,'sha256':sha(ROOT/clean_file)},'wheelPolicy':'Temporary Lot14 brass plumbing valve wheel, no inventory art/ID or nautical replacement','rubberFenderMethod':'Native sphere/band/napkin illustration studied from exact approved inspect artwork, not a resized inspect PNG','initialWheelMounted':True,'stateMaterialCorrection':'v02: removed-wheel source regions never inherit the mounted brass-wheel material mask; other material/figure/fixture decisions unchanged'}
def main():
 subprocess.run([sys.executable,str(ROOT/'source/portrait_native.py')],check=True);reports={}
 for n in[48,51]:
  ims,r=environment(n);reports[f'CH4-B2-{n}']=r
  for id_,im in ims.items():
   version='v02'if id_=='CH4-B2-48'or id_.endswith(('-emergency','-trade'))else'v01';save(im,f'native/{id_}-{version}.png');save(im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST),f'previews/{id_}-4x.png')
 (ROOT/'evidence/environment-derivation.json').write_text(json.dumps(reports,indent=2)+'\n');print('Four B2-09 primary assets and four conditional beat references constructed, all UNSELECTED.')
if __name__=='__main__':main()
