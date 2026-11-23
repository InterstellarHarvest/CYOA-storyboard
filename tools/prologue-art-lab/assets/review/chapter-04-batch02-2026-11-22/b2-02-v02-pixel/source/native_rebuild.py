"""Source-derived native reinterpretation with semantic masks and raster painting.

Large concepts are never final assets. A second pixel-friendly interpretation
is only a structural underpainting. Material ramps, low-contrast cluster
selection, explicit architecture/floor construction and NPC marks are authored
at314x206 and exported as separate transparent layers. No native-only authorship
claim; no blur/unsharp/dither or gradient synthesis.
"""
from pathlib import Path
from PIL import Image,ImageDraw
from collections import deque,Counter
import json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];SIZE=(314,206)
# Material-specific ramps chosen for the hotel and approved Chapter2 relationships.
RAMP={
 'ink':['#202c2d','#303b38','#424b43'],
 'plaster':['#625e50','#81765e','#a19477','#bbae8c','#cec29e','#e0d4b0'],
 'floor':['#4b5150','#626662','#777b72','#909184','#a7a38f','#bcb59e','#d4c9a9'],
 'green':['#263c37','#3c5146','#4d6252','#677761','#88927a','#acb198'],
 'steel':['#344b4a','#526965','#718681','#92a29a','#b4bfb1','#d6dbca'],
 'gold':['#5c4230','#886035','#ad7d3a','#d5a345','#eed17a','#f6e6aa'],
 'copper':['#4c3a2b','#79513a','#a46b43','#c78953','#e3b778'],
 'wood':['#473a2d','#69503a','#8c6946','#ac8758','#c5a574','#dfc493'],
 'red':['#3e3035','#65383e','#894a4f','#a86362','#c18777','#dfb095'],
 'brick':['#64493c','#855c46','#a77758','#c29870','#dbc098'],
 'piano':['#20282b','#303538','#45484b','#626367','#92928a'],
 'skin':['#634936','#9a6747','#c28d5c','#e4b67f','#f0cf9e'],
 'cream':['#756b52','#a39472','#c5b994','#dfd6b5','#f3e9c8'],
 'navy':['#303f4b','#465766','#637382','#8b9799'],
 'foliage':['#25443b','#4a6848','#6f8c4d','#96aa5e','#c1c88b'],
 'sky':['#6c9ec4','#8fc0db','#b8d9df','#e0e8d4']}
def rgb(h):return tuple(bytes.fromhex(h[1:]))
RAMP={k:[rgb(c)for c in v]for k,v in RAMP.items()}
def nearest(p,colors):return min(colors,key=lambda c:(p[0]-c[0])**2+(p[1]-c[1])**2+(p[2]-c[2])**2)
def classify(p):
 r,g,b=p
 if max(p)<67:return'ink'
 if min(p)>210:return'cream'
 if b>r*1.13 and b>g*1.04:return'sky'if max(p)>170 and min(p)>110 else'navy'
 if g>r*1.12 and g>b*1.1:return'foliage'
 if g>r*1.025 and b>r*.88:return'steel'
 if g>r*1.015 and g>b*1.1:return'green'
 if r>g*1.25 and r>b*1.3:
  return'red'if b>g*.72 else'gold'if g>100 else'wood'
 if r>g*1.1 and g>b*1.18:return'cream'
 return'floor'
def mask(poly):
 m=Image.new('1',SIZE);ImageDraw.Draw(m).polygon(poly,fill=1);return m
# Polygons are interpreted on the target grid, not pixel-color tracing.
GUIDES={
 '08':{
 'floor':[(0,123),(314,121),(314,206),(0,206)],
 'wall':[(0,28),(313,27),(313,122),(0,129)],
 'steel':[(214,24),(314,24),(314,63),(217,62)],
 'people': [[(199,109),(209,109),(213,123),(221,130),(220,137),(211,136),(211,166),(202,174),(190,172),(191,153),(193,134),(190,125)],[(223,96),(237,96),(241,111),(216,112),(216,106)],[(255,102),(269,103),(271,116),(283,130),(282,140),(274,142),(280,172),(263,174),(255,166),(253,143),(244,136),(242,126),(249,122)]],
 'objects': [[(0,63),(34,62),(44,84),(63,83),(73,130),(143,139),(146,173),(132,189),(0,206)],[(178,124),(212,113),(245,109),(256,119),(260,147),(250,151),(249,164),(183,166),(178,152)]],
 'doors':[(122,72,161,122),(171,72,207,122)],'vpoint':(168,117),
 'floorBands':[125,133,145,161,182,205],
 'repairs':[('line',[(12,18),(210,18)],'steel',3),('line',[(18,30),(209,30)],'green',1),('line',[(250,43),(250,61)],'steel',1),('line',[(287,45),(287,61)],'steel',1)],
 'faces':[(204,117),(230,102),(264,111)]},
 '09':{
 'floor':[(118,112),(257,112),(257,180),(286,206),(68,206),(114,176)],
 'wall':[(0,0),(314,0),(314,206),(257,206),(256,43),(116,43),(116,185),(0,206)],
 'steel':[(45,0),(85,0),(120,44),(109,57),(49,24)],
 'people':[[(141,98),(153,98),(154,108),(163,119),(158,125),(154,143),(144,147),(136,142),(139,125),(137,113)],[(219,96),(231,96),(235,109),(239,117),(235,121),(233,146),(219,145),(217,123),(206,114),(205,105)]],
 'objects':[[(116,72),(141,77),(145,95),(143,109),(165,100),(174,111),(181,126),(180,134),(156,140),(141,131),(126,160),(114,159)],[(233,99),(259,90),(260,120),(234,120)]],
 'doors':[(156,78,183,113),(194,78,220,113)],'vpoint':(183,99),
 'floorBands':[114,122,134,150,168,179,190,204],
 'repairs':[('line',[(112,46),(256,46)],'steel',2),('line',[(116,49),(256,49)],'green',1)],
 'faces':[(149,103),(225,101)]}}
GUIDES['06']={
 'floor':[(0,164),(51,132),(82,119),(314,139),(314,206),(0,206)],
 'wall':[(108,0),(314,0),(314,142),(179,143),(113,78)],
 'steel':[(136,0),(314,0),(314,33),(136,58)],
 'people':[[(133,79),(143,80),(151,94),(146,107),(134,109),(127,98)],[(154,113),(164,113),(166,120),(173,122),(171,132),(165,139),(165,158),(151,163),(137,162),(140,150),(151,134),(150,122)],[(236,111),(245,114),(248,125),(260,147),(260,154),(247,155),(235,139),(229,133),(231,123)],[(257,100),(265,100),(268,118),(267,138),(256,139),(255,121),(250,113)]],
 'objects':[[(0,125),(37,125),(42,154),(33,206),(0,206)],[(82,70),(120,62),(179,68),(181,139),(149,154),(80,153)],[(119,73),(159,83),(239,122),(239,146),(181,145),(142,123),(117,122)],[(204,146),(264,145),(275,173),(210,174)]],
 'doors':[],'vpoint':(70,113),'floorBands':[136,148,165,185,205],
 'repairs':[('line',[(190,72),(190,93)],'green',0),('line',[(299,55),(299,143)],'steel',1),('line',[(121,65),(177,69)],'steel',4)],'faces':[(139,83),(160,118),(243,117),(261,105)]}
GUIDES['07']={
 'floor':[(0,160),(61,140),(91,137),(185,149),(314,169),(314,206),(0,206)],
 'wall':[(100,0),(314,0),(314,178),(185,157),(100,122)],
 'steel':[(128,20),(314,0),(314,41),(131,65)],
 'people':[[(77,100),(87,102),(93,121),(90,136),(80,152),(60,153),(62,134),(69,119),(69,107)],[(131,101),(144,104),(148,122),(151,132),(151,141),(146,149),(151,171),(131,175),(111,168),(114,159),(126,138),(124,122)],[(234,96),(245,99),(245,110),(249,124),(244,138),(242,150),(230,160),(206,166),(205,158),(224,139),(227,122),(226,108)]],
 'objects':[[(0,138),(29,139),(35,182),(0,195)],[(77,112),(127,109),(129,148),(75,153)],[(138,99),(213,96),(230,107),(231,137),(146,150),(140,135)]],
 'doors':[],'vpoint':(66,118),'floorBands':[144,157,176,205],
 'repairs':[('line',[(187,75),(187,99)],'steel',4),('line',[(269,66),(269,171)],'green',0)],'faces':[(83,106),(140,107),(240,103)]}
GUIDES['08']['hands']=[(214,126),(214,133),(249,125),(279,135),(219,107)]
GUIDES['09']['hands']=[(159,121),(210,106),(233,118)]
GUIDES['06']['hands']=[(169,123),(145,93),(235,134),(253,110)]
GUIDES['07']['hands']=[(147,141),(228,136),(87,125)]
def rebuild(id_):
 key=id_[-2:];g=GUIDES[key];src=Image.open(ROOT/f'originals/{id_}-pixel-friendly.png').convert('RGB');under=src.resize(SIZE,Image.Resampling.NEAREST);(ROOT/'diagnostics').mkdir(exist_ok=True);under.save(ROOT/f'diagnostics/{id_}-direct-transfer-diagnostic.png')
 # Masks isolate semantic surfaces and keep material edits from damaging figures/props.
 masks={name:mask(poly)for name,poly in [('floor',g['floor']),('wall',g['wall']),('steel',g['steel'])]};occ=Image.new('1',SIZE);od=ImageDraw.Draw(occ)
 for p in g['objects']+g['people']:od.polygon(p,fill=1)
 masks['objects']=occ;people=Image.new('1',SIZE);pd=ImageDraw.Draw(people)
 for p in g['people']:pd.polygon(p,fill=1)
 masks['people']=people
 material_masks={}
 if key=='08':
  material_masks['wood']=mask([(0,145),(43,145),(43,206),(0,206)])
  material_masks['gold']=mask([(53,70),(107,70),(126,133),(57,143)])
  material_masks['copper']=mask([(0,0),(31,0),(115,69),(107,73),(22,37),(0,59)])
 elif key=='09':
  material_masks['wood']=mask([(115,108),(141,108),(141,158),(115,158)])
  material_masks['copper']=mask([(17,0),(31,0),(42,42),(22,42)])
 if key=='06':
  material_masks['wood']=mask([(118,73),(160,83),(239,123),(239,145),(181,145),(142,123),(116,122)])
  material_masks['copper']=mask([(144,0),(159,0),(157,62),(146,68)])
 if key=='07':
  material_masks['copper']=mask([(103,0),(115,0),(113,109),(104,115)])
 for name,m in material_masks.items():masks['material-'+name]=m
 for i,p in enumerate(g['people']):masks['person-'+str(i)]=mask(p)
 for name,m in masks.items():(ROOT/'masks').mkdir(exist_ok=True);m.convert('L').point(lambda p:255 if p else 0).save(ROOT/f'masks/{id_}-{name}.png')
 out=Image.new('RGB',SIZE);p=under.load();o=out.load();fm=masks['floor'].load();wm=masks['wall'].load();sm=masks['steel'].load();om=occ.load();pm=people.load();categories={};cache={}
 for y in range(206):
  for x in range(314):
   c=p[x,y];kind=classify(c)
   # Region constraints choose materially appropriate ramps, with dark seams retained.
   if not om[x,y]:
    if fm[x,y]:kind='floor' if max(c)-min(c)<58 else kind
    elif sm[x,y]:kind='steel' if max(c)-min(c)<65 else kind
    elif wm[x,y] and c[0]>c[1] and c[0]-c[2]<100:kind='plaster' if c[0]>110 else kind
   if pm[x,y]:
    skin_area=any(abs(x-u)<=5 and abs(y-v)<=6 for u,v in g['faces'])or any(abs(x-u)<=3 and abs(y-v)<=3 for u,v in g['hands'])
    if skin_area and c[0]>c[1]*1.17 and c[1]>c[2]*1.12 and c[0]>110:kind='skin'
    elif c[0]>150 and c[1]>135 and c[2]>100 and max(c)-min(c)<100:kind='cream'
    elif c[1]>c[0]*.86 and c[1]>c[2]*1.15 and c[0]<170:kind='green'
    elif c[0]>c[1]*1.15 and c[1]>c[2]*1.15:kind='wood'
   for material_,mm in material_masks.items():
    if mm.getpixel((x,y)) and c[0]>c[1]*1.12 and c[1]>c[2]*1.12 and not pm[x,y]:kind=material_
   k=(kind,c)
   if k not in cache:cache[k]=nearest(c,RAMP[kind])
   o[x,y]=cache[k];categories[x,y]=kind
 # Prune low-contrast one/two-pixel texture components, not structural seams.
 # Bright hardware, lights, skin marks and lettering are protected semantically.
 initial=out.copy();ip=initial.load();pruned=0;seen=set()
 for y in range(206):
  for x in range(314):
   if (x,y)in seen:continue
   c=ip[x,y];q=deque([(x,y)]);seen.add((x,y));component=[]
   while q:
    u,v=q.popleft();component.append((u,v))
    for a,b in[(u-1,v),(u+1,v),(u,v-1),(u,v+1)]:
     if 0<=a<314 and 0<=b<206 and(a,b)not in seen and ip[a,b]==c:seen.add((a,b));q.append((a,b))
   if len(component)>2:continue
   if any(pm[u,v] or categories[u,v]in['gold','skin','cream','ink','brick'] for u,v in component):continue
   for u,v in component:
    neighbors=[ip[a,b] for b in range(max(0,v-1),min(206,v+2))for a in range(max(0,u-1),min(314,u+2))if(a,b)not in component]
    candidates=[n for n in neighbors if sum((a-b)**2 for a,b in zip(c,n))<4200]
    if candidates:o[u,v]=Counter(candidates).most_common(1)[0][0];pruned+=1
 material=out.copy();material.save(ROOT/f'layers/{id_}-material-underpainting.png')
 # Native structural reconstruction. The transparent layer is independent of color fitting.
 layer=Image.new('RGBA',SIZE);d=ImageDraw.Draw(layer)
 for x0,y0,x1,y1 in g['doors']:
  d.rectangle((x0,y0,x1,y1),fill=RAMP['green'][0]+(255,));d.rectangle((x0+1,y0+1,x1-1,y1-1),fill=RAMP['green'][2]+(255,));d.rectangle((x0+3,y0+3,x1-3,y1-2),fill=RAMP['green'][1]+(255,))
  mid=(x0+x1)//2;d.rectangle((mid+1,y0+4,x1-4,y1-3),fill=RAMP['green'][2]+(255,));d.line((mid,y0+3,mid,y1-1),fill=RAMP['green'][0]+(255,));d.line((x0+3,y0+3,x1-3,y0+3),fill=RAMP['green'][3]+(255,))
  d.polygon([(mid-4,y0+5),(mid+2,y0+5),(mid+2,y0+12),(mid-4,y0+9)],fill=RAMP['green'][3]+(255,))
 # Repaint the floor as discrete perspective/light planes before rebuilding grout.
 # This replaces old sampled floor microtexture and conflicting source grid lines.
 floor=Image.new('RGBA',SIZE);fd=ImageDraw.Draw(floor);fd.polygon(g['floor'],fill=RAMP['floor'][3]+(255,))
 if key=='08':
  planes=[([(150,123),(173,123),(207,206),(161,206)],5),([(277,121),(314,121),(314,181),(248,164)],5),([(133,123),(143,123),(156,206),(139,206)],4),([(0,183),(128,184),(157,206),(0,206)],2)]
  shadows=[[(179,151),(250,151),(277,174),(207,178),(181,169)],[(191,171),(210,170),(220,177),(192,177)]]
 elif key=='09':
  planes=[([(165,113),(175,113),(180,179),(166,179)],5),([(199,113),(207,113),(239,180),(224,180)],4),([(117,163),(257,163),(257,181),(117,181)],2)]
  shadows=[[(139,141),(152,141),(165,149),(144,149)],[(218,144),(235,145),(245,152),(218,150)],[(152,133),(179,132),(183,138),(157,141)]]
 if key in['06','07']:
  planes=[([(40,160),(65,140),(115,143),(180,206),(61,206)],4),([(176,155),(235,156),(314,185),(314,206),(260,206)],2)]
  shadows=[[(135,160),(167,157),(184,168),(150,173)],[(226,150),(260,150),(278,159),(240,164)]] if key=='06' else [[(109,165),(146,165),(169,176),(129,182)],[(203,158),(242,152),(264,162),(218,171)],[(63,150),(126,147),(143,158),(80,162)]]
 for poly,tone in planes:fd.polygon(poly,fill=RAMP['floor'][tone]+(255,))
 for poly in shadows:fd.polygon(poly,fill=RAMP['floor'][1]+(255,))
 # Purposeful tile wear follows grout/traffic rather than repeating noise.
 wear=[([(148,160),(154,160),(156,163),(152,165),(147,164)],4),([(181,183),(190,182),(194,185),(189,187),(182,186)],2),([(256,193),(265,194),(263,197),(257,198),(254,196)],4),([(119,147),(125,146),(128,148),(125,150)],3)] if key=='08' else [([(179,150),(185,150),(187,153),(181,154)],4),([(196,169),(202,168),(207,171),(200,173)],3),([(124,164),(129,164),(132,166),(125,167)],4)]
 for poly,tone in wear:fd.polygon(poly,fill=RAMP['floor'][tone]+(255,))
 fp=floor.load()
 for y in range(206):
  for x in range(314):
   if not fm[x,y]or om[x,y]:fp[x,y]=(0,0,0,0)
 layer=Image.alpha_composite(layer,floor)
 grout=Image.new('RGBA',SIZE);gd=ImageDraw.Draw(grout);vp=g['vpoint']
 for y in g['floorBands']:gd.line((0,y,313,y),fill=RAMP['floor'][1]+(255,))
 for x in [-260,-140,-10,90,190,305,450,650]:gd.line((vp[0],vp[1],x,206),fill=RAMP['floor'][1]+(255,))
 gp=grout.load()
 for y in range(206):
  for x in range(314):
   if not fm[x,y]or om[x,y]:gp[x,y]=(0,0,0,0)
 layer=Image.alpha_composite(layer,grout);d=ImageDraw.Draw(layer)
 for _,points,material_,tone in g['repairs']:d.line(points,fill=RAMP[material_][tone]+(255,),width=1)
 # Native step edges/rail silhouettes are explicit structural clusters, not sampled texture.
 if key=='09':
  for x0,y,x1 in [(116,181,262),(104,189,272),(85,200,283)]:d.line((x0,y,x1,y),fill=RAMP['gold'][3]+(255,));d.line((x0,y+2,x1,y+2),fill=RAMP['green'][0]+(255,))
  d.line((0,100,112,177),fill=RAMP['green'][0]+(255,),width=3);d.line((0,98,111,175),fill=RAMP['green'][4]+(255,))
 elif key=='08':
  # Piano rim and keys are rebuilt at native size for readable lacquer/ivory distinction.
  d.line((184,127,251,125),fill=RAMP['gold'][3]+(255,));d.line((184,129,252,128),fill=RAMP['piano'][0]+(255,))
  for x in range(182,197,3):d.rectangle((x,141,x+1,142),fill=RAMP['cream'][4]+(255,))
  # Purposeful woodgrain/fastener clusters follow the foreground crate's plank directions.
  for x,y in [(4,157),(11,161),(24,159),(8,190),(24,186)]:d.line((x,y,x+5,y+1),fill=RAMP['wood'][1]+(255,))
 else:
  # New native drainage/threshold/fastener clusters support the exterior perspective.
  if key=='06':
   d.line((58,133,136,205),fill=RAMP['steel'][0]+(255,),width=2)
   for x,y in[(63,139),(76,151),(89,163),(102,175),(115,187),(128,199)]:d.line((x-2,y+1,x+1,y-1),fill=RAMP['steel'][3]+(255,))
   for x0,y,x1 in[(213,153,265),(216,160,269),(219,167,272)]:d.line((x0,y,x1,y-4),fill=RAMP['steel'][4]+(255,))
  else:
   d.polygon([(31,184),(47,184),(42,192),(26,192)],fill=RAMP['steel'][0]+(255,))
   for x in[30,34,38,42]:d.line((x+4,185,x,191),fill=RAMP['steel'][3]+(255,))
   d.line((222,161,263,166),fill=RAMP['steel'][3]+(255,))
 layer.save(ROOT/f'layers/{id_}-native-structure.png');out=Image.alpha_composite(out.convert('RGBA'),layer).convert('RGB')
 # Keep individual simplified NPC silhouettes as editable native layers; small faces remain clusters.
 for n,poly in enumerate(g['people']):
  mm=masks['person-'+str(n)].convert('L').point(lambda p:255 if p else 0);npc=Image.new('RGBA',SIZE);npc.paste(out,(0,0),mm);npc.save(ROOT/f'layers/{id_}-npc-{n}.png')
 before=Image.alpha_composite(material.convert('RGBA'),layer).convert('RGB');native_changed=sum(a!=b for a,b in zip(material.get_flattened_data(),before.get_flattened_data()))
 return out,{'source':'originals/'+id_+'-pixel-friendly.png','sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'targetGrid':[314,206],'diagnosticOnly':'diagnostics/'+id_+'-direct-transfer-diagnostic.png','nativeSemanticMasks':list(masks),'materialRamps':RAMP,'quietSurfaceSingletonsMerged':pruned,'nativeStructuralPixelsChangedBeyondMaterialMapping':native_changed,'nativeReconstruction':(['Elevator panel geometry and inset/cast-shadow ramps']if g['doors']else['Native service-frame, ramp and drainage geometry'])+['Floor planes, light/shadow regions, tile wear and grout rebuilt from documented vanishing point through semantic masks','Duct/beam edges and scene-specific hardware/step/piano clusters painted at target grid','NPC regions exported as independent native layers with face/hand-specific material masks'],'structureLayer':'layers/'+id_+'-native-structure.png','guide':g,'newGradients':False,'dithering':False,'paletteIsDiagnosticNotApproval':True}
def main():
 for n in['native','previews','layers','masks','diagnostics','evidence']:(ROOT/n).mkdir(exist_ok=True)
 reports={}
 for key in ['06','07','08','09']:
  id_='CH4-B2-'+key;im,report=rebuild(id_);im.save(ROOT/f'native/{id_}-v02.png');im.resize((1256,824),Image.Resampling.NEAREST).save(ROOT/f'previews/{id_}-4x.png');report['nativeRGBColors']=len(im.getcolors(314*206));reports[id_]=report
 (ROOT/'evidence/native-reconstruction.json').write_text(json.dumps(reports,indent=2)+'\n');print('Native material/structure reconstruction complete.')
if __name__=='__main__':main()
