"""Targeted native cake/trolley restoration from the editable v02 layers.

No image generation, group rerender, global palette conversion or new colors.
Clip structural paint against the complete story-object silhouette, restore
material underpainting there, and refine readable tier/icing/frame clusters.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];OLD=ROOT.parent/'b2-02-v02-pixel';SIZE=(314,206)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 for n in['native','previews','layers','masks','evidence','comparisons','references']:(ROOT/n).mkdir(exist_ok=True)
 base=Image.open(OLD/'native/CH4-B2-09-v02.png').convert('RGB');under=Image.open(OLD/'layers/CH4-B2-09-material-underpainting.png').convert('RGBA');oldstructure=Image.open(OLD/'layers/CH4-B2-09-native-structure.png').convert('RGBA');palette=set(base.get_flattened_data())
 def color(c):
  rgb=tuple(bytes.fromhex(c[1:]));return min(palette,key=lambda p:sum((a-b)**2 for a,b in zip(p,rgb)))+(255,)
 # Tight semantic silhouette: bouquet, three widening cake tiers, trolley/frame/casters.
 polys=[[(160,89),(163,88),(166,89),(168,90),(170,92),(170,95),(169,97),(158,98),(157,95),(157,92)],[(158,95),(169,95),(170,100),(173,101),(174,106),(176,109),(177,113),(180,116),(181,119),(183,120),(183,123),(150,124),(150,118),(152,116),(152,111),(154,108),(154,104),(156,101),(157,99)],[(151,122),(159,122),(160,123),(181,121),(182,130),(181,134),(176,136),(165,137),(162,140),(159,140),(158,136),(151,135)],[(177,132),(181,131),(183,134),(182,137),(179,138),(177,135)]]
 protect=Image.new('L',SIZE,0);md=ImageDraw.Draw(protect)
 for p in polys:md.polygon(p,fill=255)
 # Preserve the mover/foreground hand over the object exactly as v02.
 mover=[(148,109),(151,109),(152,114),(155,116),(157,117),(159,119),(161,119),(161,121),(159,123),(155,121),(153,119),(150,118),(148,115)]
 person=Image.new('L',SIZE,0);ImageDraw.Draw(person).polygon(mover,fill=255);pm=protect.load();personp=person.load()
 for y in range(206):
  for x in range(314):
   if personp[x,y]:pm[x,y]=0
 protect.save(ROOT/'masks/cake-and-trolley-protected.png');person.save(ROOT/'masks/foreground-hand-preserved.png')
 # The v02 mistake: panel drawing ignored object occlusion and covered upper tiers.
 clipped=oldstructure.copy();cp=clipped.load();overpaint=0
 for y in range(206):
  for x in range(314):
   if pm[x,y]:
    if cp[x,y][3]:overpaint+=1
    cp[x,y]=(0,0,0,0)
 clipped.save(ROOT/'layers/native-structure-object-safe.png')
 restored=Image.alpha_composite(under,clipped);restored.convert('RGB').save(ROOT/'references/material-restoration-before-refinement.png')
 # Native layer decisions: rounded tier shoulders, warm side planes and piped icing.
 layer=Image.new('RGBA',SIZE);d=ImageDraw.Draw(layer)
 dark=color('#756b52');shade=color('#c5b994');mid=color('#dfd6b5');light=color('#f3e9c8');creamshadow=color('#a39472');gold=color('#ad7d3a');metal=color('#526965');ink=color('#303b38');leaf=color('#677761')
 tiers=[([(159,96),(168,96),(170,98),(169,101),(158,101),(156,99),(157,97)],(158,96,169,96)),([(157,101),(170,101),(173,103),(173,108),(171,110),(155,110),(153,108),(154,104)],(156,101,171,101)),([(154,110),(173,110),(177,113),(178,118),(176,121),(153,121),(151,118),(151,114)],(154,110,174,110))]
 for i,(poly,rim)in enumerate(tiers):
  d.polygon(poly,fill=mid);right=max(p[0]for p in poly);top=min(p[1]for p in poly);bottom=max(p[1]for p in poly)
  d.polygon([(right-2,top+2),(right,top+3),(right,bottom-1),(right-2,bottom)],fill=shade)
  d.line(rim,fill=light,width=1);d.line((min(p[0]for p in poly)+2,bottom,right-2,bottom),fill=creamshadow)
 # Bouquet: three flower heads and small leaves, not a miniature portrait texture.
 for x,y in[(159,93),(168,94),(165,90)]:d.polygon([(x-2,y),(x,y-1),(x+1,y),(x,y+2)],fill=leaf)
 for x,y in[(161,92),(165,91),(168,94)]:
  d.line((x-1,y,x+1,y),fill=light);d.line((x,y-1,x,y+1),fill=light);d.point((x,y),fill=shade)
 # Distinct piped rows/garlands reinforce the tiered wedding-cake silhouette.
 for x,y in[(159,99),(163,100),(167,99),(157,107),(162,108),(168,107),(155,113),(161,113),(167,113),(173,114)]:
  d.line((x-1,y,x+1,y),fill=light);d.point((x,y-1),fill=light)
 for x,y in[(155,116),(160,117),(165,117),(170,116)]:d.line([(x,y),(x+1,y+1),(x+2,y+1),(x+3,y)],fill=light)
 d.line((152,122,179,121),fill=light);d.line((154,123,180,122),fill=dark)
 # Restore trolley cloth/frame and the two visible casters without repainting the floor.
 d.line((160,124,160,133),fill=creamshadow);d.line((173,124,173,131),fill=shade)
 d.line((153,134,179,132),fill=metal);d.line((153,135,179,133),fill=dark)
 for x,y in[(161,138),(180,135)]:
  d.line((x,y-3,x,y-1),fill=metal);d.rectangle((x-1,y-1,x+1,y+1),fill=ink);d.point((x,y),fill=gold)
 # Hard clipping is the invariant: every new object pixel stays inside its protected silhouette.
 alpha=layer.getchannel('A');alpha=Image.composite(alpha,Image.new('L',SIZE,0),protect);layer.putalpha(alpha);layer.save(ROOT/'layers/native-cake-and-trolley.png')
 final=Image.alpha_composite(restored,layer).convert('RGB');new=list(final.get_flattened_data());old=list(base.get_flattened_data());diff=[(i%314,i//314)for i,(a,b)in enumerate(zip(old,new))if a!=b];assert diff and all(pm[x,y]for x,y in diff)
 assert set(final.get_flattened_data())<=palette,'No new scene colors'
 final.save(ROOT/'native/CH4-B2-09-v03.png');final.resize((1256,824),Image.Resampling.NEAREST).save(ROOT/'previews/CH4-B2-09-v03-4x.png')
 difference=Image.new('RGB',SIZE,'#172624');dp=difference.load()
 for x,y in diff:dp[x,y]=(243,213,116)
 difference.save(ROOT/'evidence/changed-pixels.png');difference.resize((1256,824),Image.Resampling.NEAREST).save(ROOT/'evidence/changed-pixels-4x.png')
 bbox=[min(x for x,y in diff),min(y for x,y in diff),max(x for x,y in diff)+1,max(y for x,y in diff)+1]
 report={'status':'UNSELECTED','baseCommit':'62ef2059585de49292bbec2742d3c637d2eae818','baseFile':'../b2-02-v02-pixel/native/CH4-B2-09-v02.png','baseSha256':sha(OLD/'native/CH4-B2-09-v02.png'),'method':'Read existing v02 native material/structure layers; clip structure against complete story-object silhouette; restore the cake/trolley and paint targeted tier/icing/frame clusters at314x206 using only existing scene colors','imageGenerationUsed':False,'wholeSceneRegenerated':False,'paletteExactlyRestrictedToV02':True,'v02ColorCount':len(palette),'v03ColorCount':len(set(new)),'changedPixels':len(diff),'changedBounds':bbox,'outsideProtectedObjectChanges':0,'foregroundHandPixelsUnchanged':all(base.getpixel((x,y))==final.getpixel((x,y))for y in range(206)for x in range(314)if personp[x,y]),'structuralPixelsPreviouslyCoveringStoryObject':overpaint,'cause':'Incomplete cake/trolley object silhouette and unconditionally drawn elevator panel obscured upper tiers; floor/structure painting also encroached on cart/frame','masks':{'cakeAndTrolley':polys,'preserveForegroundHand':mover},'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False}
 (ROOT/'evidence/targeted-change.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k]for k in['changedPixels','changedBounds','outsideProtectedObjectChanges','v03ColorCount','structuralPixelsPreviouslyCoveringStoryObject']},indent=2))
if __name__=='__main__':main()
