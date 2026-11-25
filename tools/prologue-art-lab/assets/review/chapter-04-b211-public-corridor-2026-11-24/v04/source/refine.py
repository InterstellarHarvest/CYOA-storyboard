"""Door-relative adult scale and a dedicated clean-cluster NPC source.

Only the source-derived attendant changes. The existing v03 room/sign and all
earlier packages remain unchanged; no independent native authorship claim.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageFilter
from collections import Counter
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];OLD=ROOT.parent/'v03';SIZE=(314,206)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 path=ROOT/'originals/attendant-clean-cluster-source.png';source=Image.open(path).convert('RGBA');a=source.getchannel('A');box=a.point(lambda p:255 if p>=128 else 0).getbbox()
 crop=source.crop(box);height=132;width=round(crop.width*height/crop.height);native=crop.resize((width,height),Image.Resampling.NEAREST)
 palette=['#222530','#34384a','#4d536b','#68738a','#5f5b60','#968980','#c2b29c','#e1ccaa','#754b38','#b67750','#dca071','#edc39a','#9e8c76','#caba9b','#ebd9b6','#2a2931','#50464b','#8e7161']
 colors=[tuple(bytes.fromhex(c[1:]))for c in palette];pixels=[]
 for p in native.get_flattened_data():pixels.append(min(colors,key=lambda c:sum((x-y)**2 for x,y in zip(p[:3],c)))+(255,)if p[3]>=128 else(0,0,0,0))
 native.putdata(pixels)
 # Remove only tiny interior cloth islands from the source reduction. Hair,
 # skin, fingers, eyes and silhouette remain intact. No blur or dither is used.
 cloth=set(colors[:4]);inside=native.getchannel('A').filter(ImageFilter.MinFilter(3));inside=list(inside.get_flattened_data());seen=set();before=pixels[:];merged=0
 for seed,c in enumerate(before):
  if seed in seen or not inside[seed]or c[:3]not in cloth:continue
  todo=[seed];seen.add(seed);component=[];around=[]
  while todo:
   i=todo.pop();component.append(i);x=i%width;y=i//width
   for nx,ny in[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if not(0<=nx<width and 0<=ny<height):continue
    j=ny*width+nx
    if not inside[j]or before[j][:3]not in cloth:continue
    if before[j]==c:
     if j not in seen:seen.add(j);todo.append(j)
    else:around.append(before[j])
  if len(component)<=2 and around:
   q=Counter(around).most_common(1)[0][0]
   for i in component:pixels[i]=q
   merged+=len(component)
 native.putdata(pixels);native.save(ROOT/'evidence/attendant-native.png');native.resize((width*4,height*4),Image.Resampling.NEAREST).save(ROOT/'previews/attendant-native-4x.png')
 origin=(90,61);layer=Image.new('RGBA',SIZE);layer.alpha_composite(native,origin);layer.save(ROOT/'layers/state-attendant.png')
 oldrecipe=json.loads((OLD/'evidence/repair.json').read_text());order=[];result=Image.new('RGBA',SIZE)
 for rel in oldrecipe['floodLayerOrder']:
  if rel=='layers/state-attendant.png':p=ROOT/'layers/state-attendant.png';record='layers/state-attendant.png'
  else:
   p=(OLD/rel).resolve();record='../v03/'+rel
  result=Image.alpha_composite(result,Image.open(p).convert('RGBA'));order.append(record)
 flood=result.convert('RGB');out=ROOT/'native/CH4-NEW-04-public-corridor-flood-v04.png';flood.save(out);flood.resize((1256,824),Image.Resampling.NEAREST).save(ROOT/'previews/CH4-NEW-04-public-corridor-flood-v04-4x.png')
 oldchar=Image.open(OLD/'layers/state-attendant.png');allowed=ImageChops.lighter(oldchar.getchannel('A'),layer.getchannel('A'));allowed.save(ROOT/'masks/authorized-character-repair.png')
 sign=Image.open(OLD/'layers/state-floating-sign.png');cb=layer.getchannel('A').getbbox();sb=sign.getchannel('A').getbbox()
 record={'status':'UNSELECTED','ownerApproved':False,'sourceDerived':True,'whollyIndependentNativeAuthorship':False,'baseCommit':'19c67561d371c2bc524d39bc9f2a57e8b4584961','method':'New dedicated clean-cluster identity-preserving source; object-only nearest-neighbor reduction, coherent material ramps, binary alpha and removal of tiny interior cloth islands. Final scene assembled from unchanged prior room/sign layers. Not a resize of the previous94-pixel figure or whole scene.','source':'originals/attendant-clean-cluster-source.png','sourceSha256':sha(path),'sourceCrop':list(box),'nativeSize':[width,height],'origin':list(origin),'feetBottomY':193,'oldHeight':94,'newHeight':132,'doorReference':{'description':'Near vertical edge of existing blue STAFF door leaf','top':[18,24],'bottom':[18,198],'height':174,'npcToDoorRatio':132/174},'palette':palette,'tinyClothIslandPixelsMerged':merged,'characterBBox':list(cb),'unchangedSignBBox':list(sb),'bboxHorizontalGap':sb[0]-cb[2],'signBytesUnchanged':True,'floodLayerOrder':order,'dryCandidate':'../v03/references/CH4-NEW-04-public-corridor-v02.png','finalFloodSha256':sha(out),'canonicalIdentity':'hotel_attendant:professional; gray bob/navy work jacket and trousers; points toward staff passage'}
 (ROOT/'evidence/repair.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'hash':sha(out),'size':[width,height],'origin':origin,'gap':record['bboxHorizontalGap']}))
if __name__=='__main__':main()
