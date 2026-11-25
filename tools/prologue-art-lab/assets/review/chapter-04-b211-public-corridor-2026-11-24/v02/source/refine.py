"""One targeted owner-review correction, preserving the v01 room and sources.

SOURCE-DERIVED: local yard material reconstruction and a generated scene-NPC
source with controlled reduction/cluster cleanup; native projected doors/hatch.
No claim of wholly independent native authorship; no whole-scene resize.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
from collections import Counter
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];OLD=ROOT.parent/'v01';SIZE=(314,206)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rgba(p):return Image.open(p).convert('RGBA')
def blank():return Image.new('RGBA',SIZE)
def mask(points):
 m=Image.new('L',SIZE);ImageDraw.Draw(m).polygon(points,fill=255);return m
def rgb(c):return tuple(bytes.fromhex(c[1:]))
def fit(im,palette):
 colors=[rgb(c)for c in palette];out=im.convert('RGBA');data=[]
 for c in out.get_flattened_data():
  data.append(min(colors,key=lambda p:sum((a-b)**2 for a,b in zip(c[:3],p)))+(255,)if c[3]>=128 else(0,0,0,0))
 out.putdata(data);return out
def main():
 oldrecipe=json.loads((OLD/'evidence/native-construction.json').read_text());drynames=oldrecipe['dryLayerOrder']
 # Preserve all existing dry material/architectural layers except the hatch.
 for p in(OLD/'layers').glob('*.png'):(ROOT/'layers'/p.name).write_bytes(p.read_bytes())
 # New side-exit view: preserve the established jamb and rebuild recognizable
 # loading-yard forms inside it. Source-informed shade clusters are disclosed.
 guide=Image.open(OLD/'originals/CH4-NEW-04-pixel-friendly-study.png').convert('RGB').resize(SIZE,Image.Resampling.NEAREST)
 palette=['#27362f','#3a483c','#64715a','#969779','#b3af8a','#c2d8d2','#a6c5d1','#b9d9e3','#e4e1cd','#d2c4a6','#bca786','#a28b6c','#81705a','#615647','#4d4c40','#4c5951','#708678','#9aa99b','#74603a','#a3864e','#c8a263','#d8bb79','#c6bea7','#dcd0b2']
 yard=fit(guide.convert('RGBA'),palette);aperture=mask([(271,49),(307,26),(307,190),(271,172)]);yard.putalpha(aperture);d=ImageDraw.Draw(yard)
 # Deliberate canopy lip, supports, louver and paving perspective, rather than
 # the v01 blank beige panel and isolated X that looked like a mystery door.
 d.line([(280,88),(295,83),(306,84)],fill='#81705a')
 d.line([(281,91),(298,86),(307,88)],fill='#615647')
 d.line([(288,90),(288,129)],fill='#81705a');d.line([(289,91),(289,128)],fill='#d2c4a6')
 d.polygon([(274,103),(281,101),(281,110),(274,112)],fill='#615647')
 for y in[104,106,108,110]:d.line([(275,y),(280,y-1)],fill='#9aa99b')
 for pts in[[(273,145),(305,151)],[(273,158),(307,168)],[(277,174),(307,183)],[(288,136),(280,176)]]:d.line(pts,fill='#bca786')
 # The aperture mask restores jamb pixels, including the diagonal threshold.
 yard.putalpha(aperture)
 # A real right-hand jamb replaces the remaining v01 beige strip/X fragment.
 d=ImageDraw.Draw(yard);jamb=[(308,24),(313,20),(313,201),(308,192)];d.polygon(jamb,fill='#3a483c');d.line([(309,25),(309,192)],fill='#969779');d.line([(312,23),(312,197)],fill='#27362f')
 d.line([(310,69),(310,75)],fill='#64715a');d.line([(310,158),(310,166)],fill='#b3af8a')
 yard.save(ROOT/'layers/repair-side-exit-yard.png')
 # One coherent left-wall perspective. Project every door edge, inset and
 # molding toward the same vanishing point; vertical jambs remain vertical.
 VP=(205,115);wall=blank();d=ImageDraw.Draw(wall)
 wallpts=[(126,68),(163,88),(163,138),(126,153)];d.polygon(wallpts,fill='#81705a')
 d.polygon([(127,70),(139,77),(139,146),(127,152)],fill='#a28b6c')
 d.polygon([(139,77),(163,88),(163,138),(139,146)],fill='#81705a')
 d.polygon([(126,108),(163,111),(163,138),(126,153)],fill='#4c5c48')
 d.line([(126,108),(163,111)],fill='#969779');d.line([(126,110),(163,113)],fill='#27362f')
 d.line([(126,151),(163,137)],fill='#7c8469');d.line([(126,153),(163,139)],fill='#27362f')
 doorrecords=[]
 def door(x0,x1,top,bottom):
  def point(x,y):return(round(x),round(VP[1]+(y-VP[1])*(VP[0]-x)/(VP[0]-x0)))
  def quad(xa,xb,ya,yb):return[point(xa,ya),point(xb,ya),point(xb,yb),point(xa,yb)]
  outer=quad(x0,x1,top,bottom);d.polygon(outer,fill='#241f1b')
  leaf=quad(x0+2,x1-1,top+3,bottom-2);d.polygon(leaf,fill='#554132')
  d.polygon(quad(x0+2,(x0+x1)/2,top+3,bottom-2),fill='#72563e')
  d.line([outer[0],outer[1],outer[2]],fill='#af8d66');d.line([outer[0],outer[3]],fill='#241f1b',width=2)
  d.line([point(x0+2,top+4),point(x0+2,bottom-3)],fill='#907055')
  for va,vb in[(0.13,0.46),(0.59,0.89)]:
   q=quad(x0+3,x1-2,top+(bottom-top)*va,top+(bottom-top)*vb)
   d.polygon(q,fill='#3c2d24');d.line(q[:3],fill='#241f1b');d.line([q[3],q[2]],fill='#907055')
   # Native connected wood highlights and grain within each inset plane.
   yA=top+(bottom-top)*va;yB=top+(bottom-top)*vb
   d.line([point(x0+4,yA+2),point(x0+4,yB-3)],fill='#554132')
   if x1-x0>10:
    d.line([point(x0+5,yA+3),point(x0+5,yA+8)],fill='#72563e')
    d.line([point(x0+6,yB-7),point(x0+6,yB-3)],fill='#554132')
  hx,hy=point(x1-2,top+(bottom-top)*0.61);d.line([(hx-1,hy),(hx+1,hy)],fill='#c8a263');d.point((hx,hy+2),fill='#74603a')
  doorrecords.append({'nearX':x0,'farX':x1,'nearTop':top,'nearBottom':bottom,'corners':outer,'vanishingPoint':list(VP)})
 door(131,144,77,150);door(151,159,88,141)
 wall.save(ROOT/'layers/repair-far-door-perspective.png')
 # The closed and open hatch share exactly the same fixed frame and hinge.
 hinge=[(87,120),(87,172)];frame=[hinge[0],(111,119),(111,160),hinge[1]]
 hatch=blank();d=ImageDraw.Draw(hatch);d.polygon(frame,fill='#27362f')
 d.polygon([(89,122),(109,121),(109,158),(89,169)],fill='#64715a')
 d.polygon([(91,124),(107,123),(107,156),(91,166)],fill='#4c5c48')
 d.line([frame[0],frame[1],frame[2]],fill='#b3af8a');d.line([(89,122),(109,121)],fill='#969779')
 for y in[126,158]:d.rectangle((86,y,88,y+4),fill='#74603a');d.line([(87,y),(87,y+4)],fill='#c8a263')
 d.rectangle((106,139,108,145),fill='#3a483c');d.line([(107,141),(107,144)],fill='#c8a263')
 for pts in[[(91,166),(94,163),(94,166)],[(101,161),(104,159),(104,161)]]:d.polygon(pts,fill='#a3864e')
 hatch.save(ROOT/'layers/08-hatch-closed.png')
 opened=blank();d=ImageDraw.Draw(opened)
 opening=[(89,122),(109,121),(109,158),(89,169)];d.polygon(opening,fill='#1f2a29')
 d.polygon([(89,122),(93,125),(93,164),(89,169)],fill='#34423e')
 d.line([(93,125),(107,124)],fill='#647065');d.line([(107,124),(107,157)],fill='#34423e')
 d.line([(102,128),(102,151),(107,149)],fill='#74603a',width=3);d.line([(101,128),(101,150),(106,148)],fill='#c8a263')
 d.line([(96,130),(96,157)],fill='#647065',width=2);d.line([(95,131),(95,157)],fill='#a5ad94')
 # The outer free edge is closer to camera and taller. The anchored hinge
 # edge never moves; top and bottom attach to their matching frame corners.
 leaf=[hinge[0],(72,113),(72,181),hinge[1]];d.polygon(leaf,fill='#27362f')
 d.polygon([(86,122),(75,118),(75,177),(86,168)],fill='#4c5c48')
 d.polygon([(85,125),(78,122),(78,171),(85,165)],fill='#3a483c')
 d.line([(72,113),(72,181),(87,172)],fill='#969779');d.line([(74,116),(74,178)],fill='#64715a')
 d.line([(78,135),(85,136)],fill='#64715a');d.line([(78,157),(85,155)],fill='#27362f',width=2)
 d.line([(75,145),(75,151)],fill='#c8a263')
 for y in[126,158]:d.rectangle((86,y,88,y+4),fill='#74603a');d.line([(87,y),(87,y+4)],fill='#c8a263')
 opened.save(ROOT/'layers/state-hatch-open.png')
 # Rich source illustration replaces the schematic tiny person. Controlled
 # quality-preserving reduction is explicit source-derived NPC production.
 src=ROOT/'originals/attendant-illustration-source.png';figure=rgba(src);alpha=figure.getchannel('A');bbox=alpha.point(lambda p:255 if p>=128 else 0).getbbox();figure=figure.crop(bbox)
 height=94;width=round(figure.width*height/figure.height);small=figure.resize((width,height),Image.Resampling.NEAREST)
 charpal=['#21262d','#2d303d','#3d4351','#535c6d','#6e7681','#4b4c4d','#6f706d','#989789','#c7bfa5','#e2d2b0','#573f31','#80543b','#a8754d','#c18e60','#dba97a','#edc69a','#9c9583','#c3baa0','#e6d6b3','#f1dfb7','#28282a','#4c4a44','#7d715d','#a59071']
 small=fit(small,charpal)
 # Merge only isolated weak interior shade islands; keep eyes, fingers and
 # silhouette intact. This is cleanup of the illustration, not a geometry redraw.
 pixels=list(small.get_flattened_data());oldpixels=pixels[:];quiet=0
 for y in range(1,height-1):
  for x in range(1,width-1):
   i=y*width+x;c=oldpixels[i]
   if c[3]==0:continue
   near=[oldpixels[j]for j in[i-1,i+1,i-width,i+width]]
   if any(p[3]==0 for p in near):continue
   q,n=Counter(near).most_common(1)[0]
   if n>=3 and c not in near and sum((a-b)**2 for a,b in zip(c[:3],q[:3]))<1200:pixels[i]=q;quiet+=1
 small.putdata(pixels)
 small.save(ROOT/'diagnostics/attendant-native-source-derived.png')
 attendant=blank();attendant.alpha_composite(small,(110,99));attendant.save(ROOT/'layers/state-attendant.png')
 water=rgba(ROOT/'layers/state-water.png');d=ImageDraw.Draw(water)
 d.line([(128,194),(142,196),(156,193)],fill='#344e4d');d.line([(130,196),(143,197),(155,195)],fill='#90a399')
 water.save(ROOT/'layers/state-water.png')
 newdry=drynames+['repair-side-exit-yard','repair-far-door-perspective']
 def assemble(names):
  out=blank()
  for n in names:out=Image.alpha_composite(out,rgba(ROOT/'layers'/(n+'.png')))
  return out.convert('RGB')
 dry=assemble(newdry);floodnames=newdry+['state-water','state-hatch-open','state-attendant','state-floating-sign'];flood=assemble(floodnames)
 paths={}
 for state,im in[('dry',dry),('flood',flood)]:
  name='CH4-NEW-04-public-corridor'+('-flood'if state=='flood'else'')+'-v02';p=ROOT/'native'/(name+'.png');im.save(p);im.resize((1256,824),Image.Resampling.NEAREST).save(ROOT/'previews'/(name+'-4x.png'));paths[state]=sha(p)
 # Authorized correction areas for exact before/after checks against v01.
 drymask=Image.new('L',SIZE);d=ImageDraw.Draw(drymask);d.polygon(wallpts,fill=255);d.line([(126,153),(163,139)],fill=255);d.polygon(frame,fill=255);d.rectangle((85,115,112,173),fill=255);drymask=ImageChops.lighter(drymask,aperture);ImageDraw.Draw(drymask).polygon(jamb,fill=255);drymask.save(ROOT/'masks/dry-correction-authorized.png')
 statemask=Image.new('L',SIZE)
 for n in floodnames[len(newdry):]:statemask=ImageChops.lighter(statemask,rgba(ROOT/'layers'/(n+'.png')).getchannel('A'))
 statemask.save(ROOT/'masks/flood-authorized.png')
 floodrepair=drymask.copy()
 for n in['state-hatch-open','state-attendant']:
  floodrepair=ImageChops.lighter(floodrepair,rgba(OLD/'layers'/(n+'.png')).getchannel('A'))
  floodrepair=ImageChops.lighter(floodrepair,rgba(ROOT/'layers'/(n+'.png')).getchannel('A'))
 ImageDraw.Draw(floodrepair).rectangle((124,192,160,198),fill=255)
 floodrepair.save(ROOT/'masks/flood-correction-authorized.png')
 record={'sourceDerived':True,'whollyIndependentAuthorshipClaim':False,'baseReviewCommit':'e650f02a1d803069ae142557cfc134edab77dafd','method':'Four owner-requested corrections: local source-informed yard material reconstruction; native door-plane projection to common VP; fixed-frame/hinged-leaf hatch; generated illustrated scene-NPC source with controlled reduction, local ramp and cluster cleanup. No whole-scene resize or general palette/shading pass.','retainedSource':'../v01/originals/CH4-NEW-04-pixel-friendly-study.png','retainedSourceSha256':sha(OLD/'originals/CH4-NEW-04-pixel-friendly-study.png'),'attendantSource':'originals/attendant-illustration-source.png','attendantSourceSha256':sha(src),'attendantCrop':list(bbox),'attendantNativeSize':[width,height],'attendantOrigin':[110,99],'attendantPalette':charpal,'attendantReduction':'nearest-neighbor object-only source reduction, coherent gray-hair/navy-uniform ramps and weak-interior-cluster cleanup; binary alpha >=128','attendantQuietInteriorPixels':quiet,'yardPalette':palette,'doorProjection':doorrecords,'hatch':{'fixedFrame':frame,'hingeEdge':hinge,'openLeaf':leaf,'aperture':opening,'freeEdgeIsNearerAndTaller':True},'dryLayerOrder':newdry,'floodLayerOrder':floodnames,'hashes':paths,'canonicalAttendant':{'speaker':'hotel_attendant','pose':'professional','node':'hotel_flooded_public_corridor','distinctFrom':'hotel_wedding_assistant','sceneAction':'points screen left toward staff passage after sign floats away','visualDesignChoices':'older woman, short gray bob, navy work jacket and trousers; these are art-direction choices, not additional canonical facts'},'status':'UNSELECTED'}
 (ROOT/'evidence/repair.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(paths))
if __name__=='__main__':main()
