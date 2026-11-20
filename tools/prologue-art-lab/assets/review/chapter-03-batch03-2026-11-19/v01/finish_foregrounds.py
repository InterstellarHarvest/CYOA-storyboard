"""Manually traced native silhouettes; no blanket alpha cutoff or source overwrite."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
R=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
common_left=[(142,277),(143,264),(132,263),(123,260),(115,255),(111,249),(111,239),(114,226),(117,214),(121,196),(125,181),(133,170),(150,163),(166,159),(170,154),(170,150),(160,151),(148,148),(140,141),(136,132),(136,122),(143,114),(145,106),(147,98),(150,90),(157,82),(166,77)]
configs=[
('CH3-C06-presenter-excited','references/A06-presenter.png',[(175,74),(193,74),(199,78),(201,82),(208,83),(214,88),(216,93),(217,101),(216,106),(222,111),(226,119),(227,125),(224,132),(219,139),(211,145),(203,151),(205,156),(224,165),(240,179),(256,189),(267,180),(278,169),(284,158),(292,153),(300,147),(307,144),(310,146),(309,151),(313,153),(324,152),(327,154),(332,155),(336,158),(337,162),(333,165),(328,169),(319,174),(312,178),(305,181),(296,180),(288,191),(277,204),(265,216),(254,222),(245,224),(236,220),(231,220),(228,235),(234,253),(240,277)]+common_left,[(147,221),(151,225),(154,231),(147,230)]),
('CH3-C07-presenter-alarmed','references/A06-presenter.png',[(174,74),(190,74),(198,78),(200,82),(208,84),(214,90),(218,98),(218,105),(216,108),(222,113),(226,120),(227,125),(224,132),(219,139),(211,145),(203,151),(205,156),(224,165),(240,177),(263,184),(288,180),(291,171),(291,163),(296,157),(301,149),(306,142),(310,139),(313,141),(316,140),(319,142),(321,146),(324,149),(323,157),(321,161),(321,169),(318,176),(313,182),(308,187),(300,191),(298,197),(285,207),(273,213),(258,215),(244,212),(231,208),(227,231),(234,253),(240,277)]+common_left,[(147,221),(151,225),(154,231),(147,230)]),
('CH3-B07-attendant-alarmed','references/A03-attendant.png',[(294,43),(313,43),(323,47),(328,49),(334,56),(337,60),(339,66),(340,74),(340,82),(342,88),(344,94),(343,101),(341,108),(338,114),(336,121),(332,128),(333,132),(341,138),(356,143),(361,144),(362,137),(370,139),(372,130),(375,121),(378,114),(382,112),(386,113),(389,112),(392,115),(395,117),(397,123),(399,126),(401,132),(401,141),(399,149),(396,154),(395,160),(394,170),(397,178),(399,185),(402,192),(405,201),(408,211),(411,223),(410,233),(407,241),(402,247),(394,248),(387,248),(380,244),(374,236),(370,234),(369,248),(367,262),(234,262),(226,258),(223,252),(222,243),(221,234),(223,224),(226,214),(230,205),(233,194),(235,183),(239,171),(242,161),(247,154),(255,148),(264,142),(282,136),(295,133),(297,128),(293,123),(286,119),(283,113),(279,108),(276,103),(273,98),(270,94),(269,87),(268,79),(270,70),(273,63),(276,57),(282,51),(289,46)],[])
]
records=[]
for ident,ref,points,hole in configs:
 src=Image.open(R/f'donors/{ident}-native-donor.png').convert('RGBA');baseline=Image.open(R/ref).convert('RGBA')
 mask=Image.new('L',src.size);d=ImageDraw.Draw(mask);d.polygon(points,fill=255)
 if hole:d.polygon(hole,fill=0)
 # Exact transparent voids remain voids. This is not a guessed 127/128 alpha
 # threshold: the hand-traced contour determines the native opaque boundary.
 for y in range(src.height):
  for x in range(src.width):
   if src.getpixel((x,y))[3]==0:mask.putpixel((x,y),0)
 out=src.copy();out.putalpha(mask)
 # Remove an unrequested generated lapel microphone by transferring only the
 # approved jacket pixels at its footprint; costume/nametag remain familiar.
 if 'presenter' in ident:
  repair=Image.new('L',src.size);ImageDraw.Draw(repair).polygon([(179,183),(185,181),(188,187),(188,192),(183,196),(177,193)],fill=255)
  for y in range(181,197):
   for x in range(177,189):
    if repair.getpixel((x,y)) and mask.getpixel((x,y)):out.putpixel((x,y),baseline.getpixel((x,y)))
  repair.save(R/f'masks/{ident}-costume-repair.png')
 assert set(out.getchannel('A').getdata())=={0,255}
 # Every opaque pixel retains the generated RGB except the documented small
 # approved-costume transfer. Transparent RGB is cleared for clean transport.
 for y in range(out.height):
  for x in range(out.width):
   if out.getpixel((x,y))[3]==0:out.putpixel((x,y),(0,0,0,0))
 dest=R/f'candidates/{ident}-v01.png';out.save(dest);mask.save(R/f'masks/{ident}-native-silhouette.png')
 out.resize((2256,1112),Image.Resampling.NEAREST).save(R/f'previews/{ident}-v01-4x.png')
 bounds=list(out.getchannel('A').getbbox());basebounds=list(baseline.getchannel('A').getbbox())
 assert bounds[1]==basebounds[1] and bounds[3]==basebounds[3],(ident,bounds,basebounds)
 rows=[]
 for y in range(out.height):
  runs=[];start=None
  for x in range(out.width+1):
   value=x<out.width and mask.getpixel((x,y))>0
   if value and start is None:start=x
   if not value and start is not None:runs.append([start,x-1]);start=None
  if runs:rows.append({'y':y,'runs':runs})
 (R/f'sources/{ident}-matte-row-runs.json').write_text(json.dumps(rows,separators=(',',':'))+'\n')
 records.append({'candidateId':ident,'file':str(dest.relative_to(R)),'sha256':sha(dest),'reference':ref,'referenceSha256':sha(R/ref),'dimensions':[564,278],'mode':'RGBA','alphaValues':[0,255],'nativeMatte':'Explicit manually traced polygon plus source exact transparent voids; no blanket opacity threshold, feathering, gradient mask or scenery.','silhouettePoints':points,'transparentHole':hole,'bounds':bounds,'approvedBounds':basebounds,'topAndBottomAnchorsExact':True,'compositeAnchor':[0,0],'compositeScale':1,'wholeCharacterResized':False,'wholeCharacterTranslated':False,'derivation':'Original generated donor transferred to requested canvas as separately documented. Matte is intentionally authored on the logical grid. Native-grid source authorship remains unproven. Identity/costume likeness requires Art Director visual selection.','status':'generated','selected':False,'approved':False,'assetPath':None})
(R/'sources/foreground-assembly.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps([{'id':r['candidateId'],'sha256':r['sha256'],'bounds':r['bounds']} for r in records],indent=2))
