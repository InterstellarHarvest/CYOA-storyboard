"""Precise native hair and iris palette edit. Every other RGBA pixel stays exact to v01."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];OLD=ROOT.parent/'b2-05-v01'
# Hand-authored native silhouette regions follow existing hair locks; ear/face,
# brows, veil and hairline skin are excluded. The warm-hair color predicate
# further excludes cream fabric, transparent pixels and original dark ink.
POLYGONS={
26:[[(219,62),(220,52),(227,43),(241,39),(248,34),(258,31),(267,33),(278,35),(283,41),(292,43),(296,49),(302,52),(309,58),(311,65),(308,70),(300,72),(295,68),(293,60),(292,54),(282,51),(275,50),(271,49),(273,56),(273,60),(269,63),(267,61),(270,59),(270,54),(268,51),(263,49),(259,50),(257,52),(257,59),(258,62),(262,64),(258,66),(254,65),(251,62),(250,67),(249,73),(249,82),(249,90),(247,91),(245,88),(241,87),(236,87),(234,90),(235,94),(238,97),(243,99),(247,99),(250,102),(251,109),(249,117),(240,118),(232,115),(226,109),(222,103),(221,96),(223,91),(219,87),(217,80),(217,72)],[(298,72),(299,76),(302,79),(304,84),(304,88),(301,90),(299,87),(297,83),(297,78)]],
28:[[(225,62),(226,54),(234,44),(245,39),(253,34),(261,32),(271,34),(276,37),(284,36),(292,40),(297,46),(302,48),(311,55),(316,59),(317,65),(315,69),(307,70),(303,67),(301,61),(299,56),(295,53),(286,51),(280,50),(282,56),(282,59),(279,63),(273,63),(276,60),(279,59),(278,55),(275,52),(270,51),(266,52),(263,57),(263,60),(266,63),(270,64),(266,66),(263,66),(260,63),(259,69),(255,75),(254,82),(255,91),(252,91),(248,88),(242,88),(241,91),(243,95),(248,98),(251,99),(255,102),(257,109),(257,115),(253,118),(245,118),(237,115),(230,110),(227,103),(226,96),(227,90),(222,85),(222,77),(223,67)],[(306,74),(308,79),(311,83),(315,84),(317,88),(315,91),(311,91),(310,87),(308,85)]],
29:[[(239,62),(239,53),(246,43),(256,37),(266,33),(275,32),(281,34),(285,35),(291,33),(298,36),(302,39),(306,41),(310,45),(313,47),(319,51),(325,54),(329,59),(329,64),(328,68),(322,71),(318,69),(315,63),(312,59),(309,54),(304,51),(299,50),(289,48),(290,53),(290,58),(288,62),(284,63),(284,61),(287,60),(287,54),(284,51),(280,50),(275,52),(272,56),(272,60),(273,63),(277,65),(274,67),(270,65),(269,62),(268,69),(267,75),(266,82),(266,88),(268,91),(267,93),(263,91),(259,89),(254,89),(254,93),(257,96),(261,98),(266,100),(271,103),(273,109),(274,115),(269,119),(260,119),(250,115),(243,109),(240,102),(240,94),(237,88),(236,82),(236,75),(237,68)],[(318,72),(320,77),(326,80),(329,84),(330,87),(327,90),(323,89),(321,85),(320,80)]],
30:[[(208,62),(209,52),(217,44),(227,38),(237,34),(244,32),(250,33),(259,35),(264,40),(274,44),(279,48),(285,51),(289,55),(289,62),(288,66),(284,70),(277,70),(275,65),(274,61),(270,56),(267,53),(260,51),(256,51),(254,51),(255,57),(253,60),(248,63),(247,61),(251,59),(251,55),(249,52),(245,51),(241,52),(238,55),(237,59),(238,62),(243,64),(240,66),(236,65),(232,62),(231,68),(229,73),(228,80),(229,89),(228,92),(224,90),(221,88),(217,88),(216,91),(217,94),(221,97),(225,99),(228,101),(231,104),(232,112),(231,117),(225,119),(217,117),(210,113),(205,107),(203,101),(204,95),(201,90),(202,85),(203,76),(206,68)],[(281,72),(284,78),(286,82),(289,85),(288,89),(284,92),(282,89),(282,84),(280,79)]]}
RAMP=[(66,52,34),(91,70,39),(119,92,49),(149,118,63),(180,148,84),(205,176,109),(227,204,144),(244,226,173)]
THRESHOLDS=[42,56,68,82,96,111,128]
EAR_BOXES={26:(234,87,248,100),28:(240,88,253,102),29:(253,89,269,103),30:(216,88,230,102)}
FACE_CORES={26:(253,70,294,108),28:(258,70,308,111),29:(269,70,318,111),30:(233,70,280,110)}
# Explicit native iris-rim pixels; white/catchlight and dark pupil pixels are preserved.
IRIS_POINTS={
26:[(262,79),(262,80),(263,80),(265,78),(266,78),(265,79),(266,79),(265,80),(266,80),(287,74),(287,75),(287,76),(287,77),(285,77),(286,77),(283,76),(283,77)],
28:[(267,79),(267,80),(268,81),(270,79),(270,80),(270,81),(271,79),(271,80),(289,74),(291,74),(291,75),(291,76),(291,77),(290,78),(291,78)],
29:[(279,81),(279,82),(279,83),(281,81),(282,81),(281,82),(282,82),(281,83),(301,75),(301,76),(303,73),(304,73),(304,75),(304,76)],
30:[(250,81),(250,82),(251,82),(253,79),(254,79),(254,80),(254,81),(254,82),(272,77),(272,78),(273,79),(275,76),(275,77),(275,78),(275,79)]}
GREEN_RAMP=[(36,82,55),(60,126,79),(104,164,110)]
def lum(c):return (c[0]*2126+c[1]*7152+c[2]*722)/10000
def main():
 records=[]
 for n,polys in POLYGONS.items():
  id_=f'CH4-B2-{n}';old=Image.open(OLD/f'native/{id_}-v01.png').convert('RGBA');out=old.copy();area=Image.new('L',old.size);d=ImageDraw.Draw(area)
  for poly in polys:d.polygon(poly,fill=255)
  # Preserve complete ears/earrings including their dark anatomical outlines.
  d.rectangle(EAR_BOXES[n],fill=0)
  d.rectangle(FACE_CORES[n],fill=0)
  mask=Image.new('L',old.size);layer=Image.new('RGBA',old.size);difference=Image.new('RGB',old.size,'#27392f');count=0
  for y in range(28,123):
   for x in range(195,333):
    r,g,b,a=old.getpixel((x,y))
    if not(a and area.getpixel((x,y))and 60<r<190 and r>g*1.23 and g>b*1.12):continue
    c=RAMP[sum(lum((r,g,b))>v for v in THRESHOLDS)];out.putpixel((x,y),c+(a,));mask.putpixel((x,y),255);layer.putpixel((x,y),c+(a,));difference.putpixel((x,y),(241,207,120));count+=1
  iris_mask=Image.new('L',old.size);iris_layer=Image.new('RGBA',old.size);iris_count=0
  for x,y in IRIS_POINTS[n]:
   c=old.getpixel((x,y));r,g,b,a=c
   # Keep all original dark pupils, catchlights and eye whites exact.
   if not(a and 55<max(r,g,b)<175 and r>g*1.1 and g>b*1.02):continue
   col=GREEN_RAMP[0 if lum(c)<55 else 1 if lum(c)<85 else 2]+(a,)
   out.putpixel((x,y),col);iris_mask.putpixel((x,y),255);iris_layer.putpixel((x,y),col);difference.putpixel((x,y),(122,218,164));iris_count+=1
  allowed=ImageChops.lighter(mask,iris_mask);allowed.save(ROOT/f'masks/{id_}-allowed-hair-and-irises.png');iris_mask.save(ROOT/f'masks/{id_}-irises-only.png');iris_layer.save(ROOT/f'layers/{id_}-green-irises.png')
  mask.save(ROOT/f'masks/{id_}-hair-only.png');area.save(ROOT/f'masks/{id_}-hair-silhouette-region.png');layer.save(ROOT/f'layers/{id_}-blonde-hair.png');out.save(ROOT/f'native/{id_}-v02.png');out.resize((2256,1112),Image.Resampling.NEAREST).save(ROOT/f'previews/{id_}-4x.png');difference.save(ROOT/f'evidence/{id_}-changed-pixels.png');difference.resize((2256,1112),Image.Resampling.NEAREST).save(ROOT/f'evidence/{id_}-changed-pixels-4x.png')
  outside=sum(a!=b and not m for a,b,m in zip(old.get_flattened_data(),out.get_flattened_data(),allowed.get_flattened_data()));assert outside==0
  records.append({'id':id_,'changedHairPixels':count,'changedIrisPixels':iris_count,'changedPixelsTotal':count+iris_count,'outsideHairAndIrisMaskChanges':outside,'alphaUnchanged':old.getchannel('A').tobytes()==out.getchannel('A').tobytes(),'baseFile':str((OLD/f'native/{id_}-v01.png').relative_to(ROOT.parent)),'baseSha256':hashlib.sha256((OLD/f'native/{id_}-v01.png').read_bytes()).hexdigest(),'finalSha256':hashlib.sha256((ROOT/f'native/{id_}-v02.png').read_bytes()).hexdigest(),'nativeHairPolygons':polys,'preservedEarBox':EAR_BOXES[n]})
 (ROOT/'evidence/targeted-change.json').write_text(json.dumps({'baseCommit':'9afe76fe17dcb02633b82261a6c69457891da50f','status':'UNSELECTED','edit':'Honey-blonde hair and green irises in four bride poses only','method':'Imagegen hair-color direction reference; native 8-step hair palette and explicit 3-step green iris-rim edit; original pupils, whites, catchlights, anatomy, alpha and every other pixel preserved','ramp':RAMP,'thresholds':THRESHOLDS,'greenIrisRamp':GREEN_RAMP,'priorHairOnlyCommit':'97ccd2b8a0943374453c7a4a56af1868cb559c3f','assets':records,'groomModified':False,'clerkModified':False,'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False},indent=2)+'\n');print([(r['id'],r['changedHairPixels'],r['changedIrisPixels'])for r in records])
if __name__=='__main__':main()
