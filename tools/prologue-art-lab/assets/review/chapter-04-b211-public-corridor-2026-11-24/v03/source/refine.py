"""Native character cluster simplification and exact sign translation only.

The v02 environment, pose, silhouette and size are preserved. No new generated
source, whole-frame processing or independent-authorship claim.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageFilter
from collections import Counter
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];OLD=ROOT.parent/'v02';SIZE=(314,206)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rgb(c):return tuple(bytes.fromhex(c[1:]))
def main():
 src=Image.open(OLD/'layers/state-attendant.png').convert('RGBA');alpha=src.getchannel('A');out=src.copy()
 groups={
 'cloth':(['#21262d','#2d303d','#3d4351','#535c6d','#6e7681'],['#212b37','#29394a','#3d5063','#586b7a']),
 'hair':(['#4b4c4d','#6f706d','#989789','#c7bfa5','#e2d2b0'],['#6f706d','#6f706d','#aaa998','#d0c7ad','#d0c7ad']),
 'skin':(['#573f31','#80543b','#a8754d','#c18e60','#dba97a','#edc69a'],['#795138','#a8754d','#a8754d','#d0a474','#d0a474','#e7c393']),
 'collar':(['#9c9583','#c3baa0','#e6d6b3','#f1dfb7'],['#a99f84','#d7c8a4','#ead7ae','#ead7ae']),
 'shoe':(['#28282a','#4c4a44','#7d715d','#a59071'],['#252b30','#252b30','#59606a','#59606a'])}
 # Deliberate local ramps: preserve material identity while grouping tones.
 mapping={};masks={}
 for name,(original,ramp)in groups.items():
  for i,c in enumerate(original):mapping[rgb(c)]=rgb(ramp[min(i,len(ramp)-1)])
  m=Image.new('L',SIZE);m.putdata([255 if p[3]and p[:3]in[rgb(c)for c in original]else 0 for p in src.get_flattened_data()]);masks[name]=m
 out.putdata([mapping.get(p[:3],p[:3])+(p[3],)if p[3]else(0,0,0,0)for p in src.get_flattened_data()])
 # Repaint broad cloth masses. Keep the silhouette and pointing gesture exact.
 def brush(points,color,region):
  field=Image.new('RGBA',SIZE);ImageDraw.Draw(field).polygon(points,fill=color);field.putalpha(ImageChops.multiply(field.getchannel('A'),region));out.alpha_composite(field)
 cloth=masks['cloth'];interior=alpha.filter(ImageFilter.MinFilter(3));clothInside=ImageChops.multiply(cloth,interior)
 brush([(128,120),(140,124),(146,136),(143,159),(125,160),(128,145),(121,139)],'#3d5063',clothInside)
 brush([(143,122),(155,125),(161,151),(155,162),(145,160),(149,142)],'#29394a',clothInside)
 brush([(127,164),(139,164),(137,184),(131,188),(128,185)],'#29394a',clothInside)
 brush([(144,163),(155,163),(153,187),(145,188),(140,183)],'#29394a',clothInside)
 brush([(131,168),(134,166),(133,182),(131,185)],'#3d5063',clothInside)
 brush([(149,165),(152,166),(150,182),(147,187),(145,185)],'#3d5063',clothInside)
 # Hair is a few large lit/shadowed locks, not many tiny bright strands.
 brush([(133,98),(160,98),(160,119),(133,119)],'#aaa998',masks['hair'])
 brush([(134,104),(141,100),(145,103),(142,108),(140,116),(134,113)],'#6f706d',masks['hair'])
 brush([(139,101),(147,99),(153,101),(150,104),(142,106),(136,108)],'#d0c7ad',masks['hair'])
 brush([(153,106),(160,108),(158,118),(152,119),(151,114)],'#6f706d',masks['hair'])
 # Quiet face planes. Dark eye/mouth pixels and the original contour survive.
 face=Image.new('L',SIZE);ImageDraw.Draw(face).rectangle((136,103,151,115),fill=255);face=ImageChops.multiply(face,masks['skin'])
 brush([(136,103),(151,103),(151,116),(136,116)],'#d0a474',face)
 brush([(136,104),(140,105),(139,110),(142,114),(146,115),(138,116)],'#a8754d',face)
 brush([(142,105),(147,106),(148,110),(145,112),(142,110)],'#e7c393',face)
 # Remove weak isolated interior fabric shade islands, retaining true edges,
 # hands and face features. No blur or lower-resolution resampling is used.
 changed=0;pixels=list(out.get_flattened_data());before=pixels[:];inside=list(clothInside.get_flattened_data())
 for y in range(116,188):
  for x in range(111,161):
   i=y*314+x
   if not inside[i]:continue
   near=[before[j]for j in[i-1,i+1,i-314,i+314]if inside[j]]
   if len(near)<3:continue
   v,n=Counter(near).most_common(1)[0]
   if n>=3 and before[i]not in near:pixels[i]=v;changed+=1
 # Replace tiny interior cloth islands by the surrounding cloth shade. This
 # removes miniature tailoring texture while preserving the broad fold planes.
 seen=set();islands=0;base=pixels[:]
 for y in range(116,188):
  for x in range(111,161):
   seed=y*314+x
   if seed in seen or not inside[seed]:continue
   todo=[seed];seen.add(seed);component=[];around=[];color=base[seed]
   while todo:
    i=todo.pop();component.append(i)
    for j in[i-1,i+1,i-314,i+314]:
     if j<0 or j>=len(base)or not inside[j]:continue
     if base[j]==color:
      if j not in seen:seen.add(j);todo.append(j)
     else:around.append(base[j])
   if len(component)<=3 and around:
    target=Counter(around).most_common(1)[0][0]
    for i in component:pixels[i]=target
    islands+=len(component)
 out.putdata(pixels)
 # Just two eye clusters and one mouth mark retain expression at scene scale.
 fd=ImageDraw.Draw(out);fd.point((140,108),fill='#212b37');fd.line([(144,106),(145,106)],fill='#795138');fd.line([(140,113),(141,113)],fill='#795138')
 out.putalpha(alpha);out.save(ROOT/'layers/state-attendant.png')
 # Translate the entire existing sign, lettering and its immediate wake exactly.
 oldsign=Image.open(OLD/'layers/state-floating-sign.png').convert('RGBA');sign=Image.new('RGBA',SIZE);sign.alpha_composite(oldsign,(34,0));sign.save(ROOT/'layers/state-floating-sign.png')
 recipe=json.loads((OLD/'evidence/repair.json').read_text());names=recipe['floodLayerOrder'];assembled=Image.new('RGBA',SIZE);order=[]
 for n in names:
  path=ROOT/'layers'/(n+'.png')if n in['state-attendant','state-floating-sign']else OLD/'layers'/(n+'.png')
  assembled=Image.alpha_composite(assembled,Image.open(path).convert('RGBA'));order.append(str(path.relative_to(ROOT))if path.is_relative_to(ROOT)else'../v02/layers/'+n+'.png')
 result=assembled.convert('RGB');native=ROOT/'native/CH4-NEW-04-public-corridor-flood-v03.png';result.save(native);result.resize((1256,824),Image.Resampling.NEAREST).save(ROOT/'previews/CH4-NEW-04-public-corridor-flood-v03-4x.png')
 allowed=ImageChops.lighter(alpha,oldsign.getchannel('A'));allowed=ImageChops.lighter(allowed,sign.getchannel('A'));allowed.save(ROOT/'masks/authorized-corrections.png')
 oldbox=oldsign.getchannel('A').getbbox();newbox=sign.getchannel('A').getbbox();charbox=alpha.getbbox()
 record={'status':'UNSELECTED','ownerApproved':False,'sourceDerived':True,'whollyIndependentAuthorshipClaim':False,'baseCommit':'e825c7a8bc97280e55cd1650b50c1f94ec15f272','method':'Native local material-ramp grouping and broad plane/lock/cloth repaint inside exact v02 character silhouette; exact34-pixel rightward sign translation. No new generation, blur or resampling.','characterSilhouetteUnchanged':True,'characterOriginUnchanged':[110,99],'characterHeightUnchanged':94,'nativeMaterialGroups':groups,'isolatedClothShadePixelsMerged':changed,'tinyInteriorClothIslandPixelsMerged':islands,'signTranslation':[34,0],'oldSignBBox':list(oldbox),'newSignBBox':list(newbox),'characterBBox':list(charbox),'bboxHorizontalGap':newbox[0]-charbox[2],'floodLayerOrder':order,'unchangedDryFile':'../v02/native/CH4-NEW-04-public-corridor-v02.png','unchangedDrySha256':sha(OLD/'native/CH4-NEW-04-public-corridor-v02.png'),'finalFloodSha256':sha(native),'originalAttendantSource':'../v02/originals/attendant-illustration-source.png','originalGenerationProvenance':'../v02/evidence/generation-provenance.json'}
 (ROOT/'evidence/repair.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'hash':sha(native),'gap':record['bboxHorizontalGap']}))
if __name__=='__main__':main()
