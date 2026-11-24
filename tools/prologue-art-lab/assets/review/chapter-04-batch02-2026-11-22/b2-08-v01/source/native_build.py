"""SOURCE-DERIVED B2-08; no approved images are edited.
Separate native material/structure/sign/gauge/state layers preserve story truth.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,subprocess,sys,math,hashlib
from shared_native import mask,quiet_clusters
from materials import nearest
import block_letters,pixel_text
ROOT=Path(__file__).resolve().parents[1]
RAMPS={
 'gold':['#3f3022','#65452b','#8b6031','#b27e38','#d49f4e','#edc579','#ffe4a1'],
 'steel':['#222c34','#34434f','#4c5d68','#6b7d85','#95a1a1','#c5cdba'],
 'green':['#243a35','#354c40','#4e624b','#6d7c58','#92936c','#b3ae84'],
 'floor':['#333b3c','#4c5554','#6a716c','#8e9182','#b5ad92','#d4c6a4'],
 'plaster':['#695a49','#927956','#b99b6d','#d9ba88','#eed5a4','#ffebbc']}
RAMPS={k:[tuple(bytes.fromhex(c[1:]))for c in v]for k,v in RAMPS.items()}
LAYOUT={42:{'size':(314,206),'gauge':(63,36,17,19),'plate':[(33,69),(81,72),(81,85),(33,82)],'doorLabel':[(116,45),(148,50),(148,59),(116,54)],'boilerLabel':[(192,57),(203,57),(203,65),(192,65)],'innerLabel':[(120,87),(141,87),(141,97),(120,97)],'gate':(178,108,221,149),'wheel':[(31,91),(76,90),(99,113),(99,164),(78,183),(31,183)],'doorRegion':[(111,61),(151,64),(151,170),(111,174)],'npc':[(264,69),(296,69),(309,112),(305,169),(310,183),(265,183),(263,123),(250,113),(250,97)],'floor':[(81,205),(174,150),(224,147),(274,104),(314,143),(314,206)]},
47:{'size':(564,278),'gauge':(100,49,23,28),'plate':[(49,99),(127,103),(127,124),(49,120)],'doorLabel':[(188,69),(244,77),(244,94),(188,86)],'boilerLabel':[(321,92),(348,92),(348,104),(321,104)],'innerLabel':[(186,140),(226,140),(226,165),(186,165)],'gate':(292,169,377,243),'wheel':[(46,135),(129,133),(157,176),(157,229),(125,263),(47,263)],'doorRegion':[(174,88),(249,100),(249,249),(174,268)],'npc':None,'floor':[(244,278),(287,248),(382,245),(449,204),(564,201),(564,278)]}}
def save(im,rel):im.save(ROOT/rel)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def apply(a,b):return Image.alpha_composite(a.convert('RGBA'),b).convert('RGB')
def diff(a,b):return sum(x!=y for x,y in zip(a.get_flattened_data(),b.get_flattened_data()))
def textplane(lines,quad,size,scale=1,color='#29332c',back=None):
 widths=[block_letters.measure(t,s)for t,s in lines];h=sum(5*s for _,s in lines)+2*(len(lines)-1)+6;w=max(widths)+6;im=Image.new('RGBA',(w,h),back or(0,0,0,0));y=3
 for t,s in lines:
  tw=block_letters.measure(t,s);block_letters.draw(im,t,((w-tw)//2,y),scale=s,color=color);y+=5*s+2
 return pixel_text.project(im,quad,size=size)
def gauge(num,relieved=False):
 size=LAYOUT[num]['size'];cx,cy,rx,ry=LAYOUT[num]['gauge'];im=Image.new('RGBA',size);d=ImageDraw.Draw(im);b=(cx-rx,cy-ry,cx+rx,cy+ry)
 # Deliberate native dial construction replaces the guide's erroneous
 # recolored high-pressure needle. The relieved needle physically points LEFT.
 d.ellipse(b,fill='#e7d4a7',outline='#313a34');d.arc((cx-rx+2,cy-ry+2,cx+rx-2,cy+ry-2),180,269,fill='#557d56',width=3 if num==42 else 4);d.arc((cx-rx+2,cy-ry+2,cx+rx-2,cy+ry-2),270,360,fill='#b64e36',width=3 if num==42 else 4)
 for a in range(185,356,15):
  t=math.radians(a);p=(round(cx+(rx-2)*math.cos(t)),round(cy+(ry-2)*math.sin(t)));q=(round(cx+(rx-5)*math.cos(t)),round(cy+(ry-5)*math.sin(t)));d.line((p,q),fill='#333b32')
 theta=math.radians(228 if relieved else 317);p=(round(cx+(rx-6)*math.cos(theta)),round(cy+(ry-6)*math.sin(theta)));d.line((cx,cy,*p),fill='#29362f',width=2 if num==42 else 3);d.line((cx,cy,*p),fill='#436645'if relieved else'#993d30');d.ellipse((cx-2,cy-2,cx+2,cy+2),fill='#26332e');d.point((cx-1,cy-1),fill='#e1c882')
 return im,{'center':[cx,cy],'needleTip':list(p),'sector':'GREEN'if relieved else'RED','rotationDegrees':228 if relieved else 317}
def material(under,num,protect,write_masks=True):
 out=under.quantize(colors=96 if num==42 else 128,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB');sz=under.size;steel=Image.new('L',sz);green=Image.new('L',sz);plaster=Image.new('L',sz);gold=Image.new('L',sz)
 for y in range(sz[1]):
  for x in range(sz[0]):
   if num==42 and x>245 and y>65:continue
   r,g,b=under.getpixel((x,y));key=None
   if r>g*1.14 and g>b*1.45 and r>85:key='gold'
   elif b>r*1.04 and max(r,g,b)-min(r,g,b)<90:key='steel'
   elif g>r*.93 and g>b*1.1 and r<160:key='green'
   elif (89<x<174 and y<91 if num==42 else 140<x<287 and y<160)and r>g*1.05 and g>b*1.1:key='plaster'
   if key:
    out.putpixel((x,y),nearest((r,g,b),RAMPS[key]));{'gold':gold,'steel':steel,'green':green,'plaster':plaster}[key].putpixel((x,y),255)
 if write_masks:
  for k,im in [('steel',steel),('green',green),('plaster',plaster),('gold',gold)]:save(im,f'masks/CH4-B2-{num}-{k}-material.png')
 out,n=quiet_clusters(out,protect,threshold=500);return out,n
def opened_gate(base,num):
 sz=base.size
 # Source-informed object reconstruction, clipped to gate/leaf/chain footprint.
 # The successful guide preserves actual walkway depth and boiler skirt.
 under=Image.open(ROOT/f'originals/CH4-B2-{num}-staff-access-reference.png').convert('RGB').resize(sz,Image.Resampling.NEAREST)
 protect=mask(sz,[LAYOUT[num]['wheel'],LAYOUT[num]['doorRegion']]);native,_=material(under,num,protect,False)
 polys=[[(171,99),(231,99),(248,108),(248,159),(171,156)]]if num==42 else[[(282,159),(402,159),(422,173),(422,253),(282,250)]]
 allowed=mask(sz,polys);layer=native.convert('RGBA');layer.putalpha(allowed)
 # A few target-grid hinge/edge highlights retain physical attachments.
 d=ImageDraw.Draw(layer)
 if num==42:d.line((224,109,227,110),fill='#edce8f');d.point((225,142),fill='#edce8f')
 else:d.line((378,173,382,175),fill='#edce8f');d.line((377,230,381,231),fill='#b78a46')
 layer.putalpha(ImageChops.multiply(layer.getchannel('A'),allowed));return apply(base,layer),layer,allowed
def environment(num):
 id_=f'CH4-B2-{num}';s=LAYOUT[num];size=s['size'];src=Image.open(ROOT/f'originals/{id_}-pixel-friendly.png').convert('RGB');under=src.resize(size,Image.Resampling.NEAREST);save(under,f'diagnostics/{id_}-direct-transfer.png')
 polys=[s['wheel'],s['doorRegion']]
 if s['npc']:polys.append(s['npc'])
 gx,gy,grx,gry=s['gauge'];polys.append([(gx-grx-8,gy-gry-8),(gx+grx+8,gy-gry-8),(gx+grx+8,gy+gry+8),(gx-grx-8,gy+gry+8)]);x0,y0,x1,y1=s['gate'];polys.append([(x0-3,y0-6),(x1+5,y0-6),(x1+5,y1+3),(x0-3,y1+3)])
 protect=mask(size,polys);save(protect,f'masks/{id_}-complete-story-objects.png');out,merged=material(under,num,protect);save(out,f'layers/{id_}-material-underpainting.png');before=out.copy();floor=ImageChops.subtract(mask(size,[s['floor']]),protect);save(floor,f'masks/{id_}-floor.png')
 structure=Image.new('RGBA',size);d=ImageDraw.Draw(structure)
 if num==42:a,b=(205,205),(273,108)
 else:a,b=(407,277),(484,201)
 d.line((*a,*b),fill='#202f31',width=3 if num==42 else 5);d.line((a[0]-2,a[1],b[0]-1,b[1]),fill='#98a59b')
 for i in range(0,48):
  t=i/48;x=round(a[0]+(b[0]-a[0])*t);y=round(a[1]+(b[1]-a[1])*t)
  if i%(2 if t<.5 else 3)==0:d.line((x-1,y,x+1,y+1),fill='#b2b7a6')
 structure.putalpha(ImageChops.multiply(structure.getchannel('A'),floor));out=apply(out,structure);save(structure,f'layers/{id_}-native-drain-structure.png')
 # Author readable inset bitmap plates on their actual physical planes.
 signs=Image.new('RGBA',size)
 for lines,q,bg in [([('HIGH-PRESSURE',1),('STEAM',2 if num==47 else 1)],s['plate'],'#cda256'),([("ENGINEERS'",1),('LAVATORY',1)],s['doorLabel'],'#decb9d'),([('BOILER',1),('THREE',1)],s['boilerLabel'],'#d7c59a')]:signs=Image.alpha_composite(signs,textplane(lines,q,size,back=bg))
 out=apply(out,signs);save(signs,f'layers/{id_}-native-bitmap-plates.png');red,red_info=gauge(num);out=apply(out,red);save(red,f'layers/{id_}-native-red-gauge.png');save(red.getchannel('A'),f'masks/{id_}-gauge-face.png');primary=out.copy()
 # Success uses only a bounded door-object source. Correct the main study's
 # wrong hinge direction through separate native right-hinged leaf construction.
 state_src=Image.open(ROOT/f'originals/{id_}-relieved-reference.png').convert('RGB').resize(size,Image.Resampling.NEAREST);state_src,_=material(state_src,num,protect,False)
 doorpolys=[[(112,64),(150,68),(150,169),(112,174)]]if num==42 else[[(174,90),(263,89),(263,266),(174,268)]]
 allowed=mask(size,doorpolys);patch=state_src.convert('RGBA');patch.putalpha(allowed)
 if num==42:
  ld=ImageDraw.Draw(patch);steel=RAMPS['steel'];poly=[(148,67),(165,59),(165,177),(148,168)];ld.polygon(poly,fill=steel[1],outline=steel[4]);ld.polygon([(150,70),(163,64),(163,173),(150,166)],fill=steel[2]);ld.polygon([(152,80),(161,76),(161,117),(152,121)],fill='#b7b9a0',outline=steel[0])
  for yy in range(81,117,4):ld.line((152,yy,161,yy+6),fill=steel[1]);ld.line((152,yy+5,161,yy-1),fill=steel[1])
  for yy in[144,149,154]:ld.line((152,yy,162,yy-3),fill=steel[4]);ld.line((152,yy+1,162,yy-2),fill=steel[0])
  ld.line([(159,129),(162,128),(162,139),(160,140)],fill='#e4dbc0');ld.line((148,68,148,167),fill='#d0cba8')
  leaf=mask(size,[poly]);allowed=ImageChops.lighter(allowed,leaf);patch.putalpha(ImageChops.lighter(patch.getchannel('A'),leaf))
 patch.putalpha(ImageChops.multiply(patch.getchannel('A'),allowed))
 relieved=apply(primary,patch);save(patch,f'layers/{id_}-native-open-lavatory-passage.png')
 plaque=textplane([('SANITATION',1),('CLEARANCE',1),('PENDING',1)],s['innerLabel'],size,back='#d8b36c');relieved=apply(relieved,plaque);allowed=ImageChops.lighter(allowed,plaque.getchannel('A'))
 green,green_info=gauge(num,True);relieved=apply(relieved,green);allowed=ImageChops.lighter(allowed,green.getchannel('A'));save(green,f'layers/{id_}-native-green-gauge.png');save(plaque,f'layers/{id_}-inner-closed-door-plate.png')
 steam=Image.new('RGBA',size);sd=ImageDraw.Draw(steam)
 # Discrete overhead relief plume, far from the viewpoint/player. No explosion.
 pts=[(208,18),(210,14),(208,10),(209,6),(207,1)]if num==42 else[(159,18),(162,13),(159,9),(161,5),(159,0)];sd.line(pts,fill='#b9c6bd',width=2 if num==42 else 3);sd.line([(x+1,y)for x,y in pts],fill='#dde2cd');relieved=apply(relieved,steam);allowed=ImageChops.lighter(allowed,steam.getchannel('A'));save(steam,f'layers/{id_}-native-overhead-relief-steam.png');save(allowed,f'masks/{id_}-relieved-allowed.png')
 staff,gate_layer,gate_allowed=opened_gate(primary,num);save(gate_layer,f'layers/{id_}-native-open-maintenance-gate.png');save(gate_allowed,f'masks/{id_}-staff-access-allowed.png');hold=staff.copy()
 tag=Image.new('RGBA',size);td=ImageDraw.Draw(tag)
 if num==42:q=[(61,137),(82,141),(80,161),(59,157)];td.line((65,132,68,140),fill='#ccb986')
 else:q=[(104,193),(150,198),(148,229),(101,225)];td.line((113,185,118,198),fill='#ccb986')
 tag=Image.alpha_composite(tag,textplane([('DO NOT',1),('OPERATE',1)],q,size,color='#702e2a',back='#e8d7aa'));hold=apply(hold,tag);hold_allowed=ImageChops.lighter(gate_allowed,tag.getchannel('A'));save(tag,f'layers/{id_}-native-do-not-operate-tag.png');save(hold_allowed,f'masks/{id_}-inspection-hold-allowed.png')
 ims={id_:primary,id_+'-relieved':relieved,id_+'-inspection-hold':hold,id_+'-staff-access':staff};states={}
 for suffix,im,m in [('relieved',relieved,allowed),('inspection-hold',hold,hold_allowed),('staff-access',staff,gate_allowed)]:states[suffix]={'changedPixels':diff(primary,im),'outsideAllowedChanges':sum(a!=b and not c for a,b,c in zip(primary.get_flattened_data(),im.get_flattened_data(),m.get_flattened_data())),'allowedMask':f'masks/{id_}-{suffix}-allowed.png','gauge':green_info if suffix=='relieved'else red_info}
 report={'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'nativeSize':list(size),'localBasePalette':96 if num==42 else 128,'quietClustersMerged':merged,'nativeStructureChangesInsideProtectedObjects':sum(a!=b and m for a,b,m in zip(before.get_flattened_data(),apply(before,structure).get_flattened_data(),protect.get_flattened_data())),'sourcePixelFriendly':{'file':f'originals/{id_}-pixel-friendly.png','sha256':sha(ROOT/f'originals/{id_}-pixel-friendly.png')},'relievedObjectReference':{'file':f'originals/{id_}-relieved-reference.png','sha256':sha(ROOT/f'originals/{id_}-relieved-reference.png')},'initialGauge':red_info,'states':states,'nativeCorrections':['Physically rotate needle into green; do not merely recolor a red-pointing needle.','Keep existing right-hand lavatory-door hinges; main reference left-swing is not transferred.','Inner door remains closed; inspection/staff bypass does not open lavatory.','Readable inset perspective bitmap plates; separate open gate/tag/steam layers.']}
 return ims,report
def main():
 subprocess.run([sys.executable,str(ROOT/'source/portrait_native.py')],check=True);reports={}
 for num in[42,47]:
  ims,r=environment(num);reports[f'CH4-B2-{num}']=r
  for id_,im in ims.items():save(im,f'native/{id_}-v01.png');save(im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST),f'previews/{id_}-4x.png')
 (ROOT/'evidence/environment-derivation.json').write_text(json.dumps(reports,indent=2)+'\n');print('Six primary B2-08 assets and six bounded conditional references constructed, all UNSELECTED.')
if __name__=='__main__':main()
