"""Explicit native-pixel Paper Emergency repair. No image generation or global filters.
--prepare freezes traced masks and source-sampled drawing operations before rendering.
--render applies only those operations and validates every pixel outside the union.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,csv,sys
B=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
SRC='originals/approved-paper-emergency.png';DEST='candidate/CH3-B06-paper-emergency-local-v04.png'

def prepare():
 if (B/'sources/repair-plan.json').exists()or(B/DEST).exists():raise SystemExit('Frozen review already exists; copy to a new version to revise. Use --render for exact replay.')
 im=Image.open(B/SRC).convert('RGB');assert sha(B/SRC)=='ac0f7c44d267dd54897507ae3b8b02959a5b76f4fcd9d0418b77b8fdb777ba7e'
 ops=[]
 def add(group,kind,coordinates,sample,reason,width=None):
  v={'region':group,'kind':kind,'coordinates':coordinates,'sample':list(sample),'rgb':list(im.getpixel(sample)),'reason':reason}
  if width:v['width']=width
  ops.append(v)
 # P1: short shadow follows the main moving strip's existing lower/right edge.
 shadow=[(167,182),(166,183),(165,184),(164,185),(163,185),(162,186),(161,186),(160,187),(159,187),(158,188),(157,188),(156,188)]
 for i,p in enumerate(shadow):add('P1','point',p,(167,185)if i<5 else(165,186),'Contact shadow on the returning loop beneath the continuous front strip.')
 for p in [(166,182),(165,183),(164,184),(163,184),(162,185),(161,185),(160,186),(159,186),(158,187),(157,187)]:add('P1','point',p,(165,183),'Retain a narrow lit paper edge above the contact shadow; do not alter ribbon geometry.')
 # Face: preserve head, spectacles, eyes, brows and nose; remove the upturned smile.
 for p in [(217,113),(218,113),(217,114),(218,114),(223,114),(224,114)]:add('face','point',p,(217,112),'Restore only former smile-corner pixels inside the mouth repair shape.')
 add('face','polygon',[(219,112),(222,112),(224,114),(223,117),(219,117),(217,115)],(220,114),'Urgent open mouth outer lip; scale and surrounding face retained.')
 add('face','polygon',[(219,113),(222,113),(223,114),(222,116),(219,116),(218,115)],(223,113),'Small shaded open-mouth cavity, matching the alarmed portrait design cue.')
 add('face','line',[(219,113),(221,113)],(221,113),'Preserve an economical upper-teeth highlight; no portrait downsampling.',1)
 add('face','point',(222,114),(221,113),'One upper-tooth highlight follows the mouth angle.')
 add('face','line',[(220,117),(222,117)],(219,118),'Warm lower-lip boundary retains existing face color family.',1)
 # Trace the OLD clasped hands explicitly, including their antialiased skin fringe.
 old_rows={133:(221,224),134:(219,225),135:(218,226),136:(215,228),137:(214,230),138:(214,230),139:(214,230),140:(215,230),141:(216,229)}
 for y,(x0,x1)in old_rows.items():
  for x in range(x0,x1+1):
   if y==141:sample=(233,141)
   elif y<136:sample=(213,132)if x<222 else(230,132)
   else:sample=(213,132)if x<222 else(230,132)
   add('hands','point',(x,y),sample,'Remove the traced old clasp only; restore vest behind it or the previously hand-occluded counter edge.')
 # Selected vest fold/light remains local to the former hand footprint.
 add('hands','line',[(225,134),(224,138),(225,140)],(230,132),'Local vest fold behind the separated hands; no torso rescale.',1)
 add('hands','line',[(221,134),(220,136)],(213,132),'Vest shading continues within removed-hand footprint.',1)
 # Left/viewer-left forearm braces naturally on the original counter.
 add('hands','polygon',[(210,136),(215,136),(219,138),(218,140),(211,140)],(208,138),'Cream braced forearm within the original sleeve footprint.')
 add('hands','line',[(211,139),(215,139),(217,140)],(232,134),'Preserve a warm sleeve crease/underside.',1)
 add('hands','polygon',[(216,136),(219,136),(221,137),(224,138),(224,139),(221,140),(216,140),(214,139)],(222,136),'One braced hand, visibly separate from the raised hand; no new control.')
 add('hands','line',[(216,139),(220,140),(223,139)],(215,137),'Braced-hand underside and floor/counter contact cue within original hand area.',1)
 add('hands','line',[(217,137),(219,137),(221,138)],(224,138),'Small light cluster on braced hand; retain useful volume.',1)
 # Raised right sleeve: bent elbow at original desk placement, not a reaching grab.
 sleeve=[(232,132),(234,127),(238,126),(241,129),(241,134),(239,138),(236,140),(233,138)]
 add('hands','polygon',sleeve,(232,134),'Bent sleeve under the raised stop palm; maintain cream shirt and existing scale.')
 add('hands','polygon',[(235,129),(238,128),(240,130),(239,134),(237,138),(235,137),(234,133)],(235,134),'Warm sleeve midtone and bent forearm volume.')
 add('hands','line',[(237,130),(238,133),(236,137)],(235,139),'Cream light cluster along raised forearm.',1)
 add('hands','line',[(234,133),(234,136),(236,139)],(232,134),'Local elbow fold, retained clothing palette.',1)
 # Palm is BELOW the passing receipt and LEFT of the plant, not intersecting either.
 palm=[(236,121),(237,120),(238,121),(239,124),(239,127),(238,130),(235,131),(233,128),(233,125),(234,124),(235,126),(235,122)]
 add('hands','polygon',palm,(215,137),'Urgent open stop/leave palm outline; no contact with an unseen person.')
 add('hands','polygon',[(236,122),(237,121),(238,123),(238,128),(237,130),(235,130),(234,128),(234,126),(236,128)],(222,136),'Small palm/finger skin mass at the existing character scale.')
 add('hands','line',[(236,123),(236,126)],(224,138),'One finger-plane highlight; avoid portrait-level finger detail.',1)
 add('hands','point',(237,127),(219,135),'Palm midtone retains volume.')
 add('hands','line',[(235,131),(238,130)],(208,138),'Narrow cream cuff under the skin wrist, clearly attached to sleeve.',1)
 # Predeclare masks by tracing the intended old/new shapes, never a rectangular NPC box.
 masks={k:Image.new('L',(314,206),0)for k in ['P1','face','hands']}
 for op in ops:
  d=ImageDraw.Draw(masks[op['region']]);co=op['coordinates'];kind=op['kind']
  if kind=='point':d.point(tuple(co),fill=255)
  elif kind=='line':d.line([tuple(p)for p in co],fill=255,width=op['width'])
  elif kind=='polygon':d.polygon([tuple(p)for p in co],fill=255)
 union=Image.new('L',(314,206),0)
 for key,mask in masks.items():
  mask.save(B/'masks'/f'{key}-declared-mask.png')
  for y in range(206):
   for x in range(314):
    if mask.getpixel((x,y)):union.putpixel((x,y),255)
 union.save(B/'masks/declared-repair-union.png')
 # Exact protected object/identity guards; old-hand skin occlusion is not visible desk art.
 guards=[{'name':'P2 right floor loop and fold','box':[224,169,278,199]}, {'name':'Restroom and two-person signs','box':[0,0,202,169]}, {'name':'Cream printer/feed unit','box':[184,130,202,148]}, {'name':'Gooseneck microphone','box':[194,122,203,140]}, {'name':'Plant including left leaf tips','box':[242,108,273,145]}, {'name':'Visible counter/desk top and fascia','box':[199,142,270,184]}, {'name':'Brush heads shafts and ceiling mounts','box':[227,24,314,111]}, {'name':'Hair outline and hairstyle','box':[206,97,230,104]}, {'name':'Glasses eyes and upper face','box':[206,103,230,112]}, {'name':'Name badge','box':[226,128,232,131]}]
 paper_guard=Image.new('L',(314,206),0);ImageDraw.Draw(paper_guard).polygon([(229,116),(250,96),(260,94),(258,101),(237,118),(230,124),(229,122)],fill=255);paper_guard.save(B/'masks/protected-passing-receipt.png')
 for y in range(206):
  for x in range(314):assert not(paper_guard.getpixel((x,y))and union.getpixel((x,y))),(x,y,'passing receipt')
 for g in guards:
  x0,y0,x1,y1=g['box'];assert not any(union.getpixel((x,y))for y in range(y0,y1)for x in range(x0,x1)),g['name']
 plan={'date':'2026-11-22','baseApprovedSha256':sha(B/SRC),'source':SRC,'candidate':DEST,'status':'generated','selection':'unselected','approved':False,'assetPath':None,'method':'Explicit native-coordinate point/line/polygon operations; source-sampled colors only; no image generation or global filtering','operations':ops,'masks':{k:{'file':f'masks/{k}-declared-mask.png','sha256':sha(B/'masks'/f'{k}-declared-mask.png'),'pixels':sum(v==255 for v in masks[k].get_flattened_data())}for k in masks},'unionMask':{'file':'masks/declared-repair-union.png','sha256':sha(B/'masks/declared-repair-union.png'),'pixels':sum(v==255 for v in union.get_flattened_data())},'protectedGuards':guards,'passingReceiptMask':'masks/protected-passing-receipt.png','P2Decision':'KEEP','P1Decision':'Moving strip passes in front of lower returning loop; one continuous receipt, no new branch','gestureDecision':'Raised stop palm below passing receipt and left of plant; opposite hand braces on original counter; no player or implied grab','geometryTransforms':0,'remainingLimits':'Counter-braced hand does not depict a literal button press; no new emergency control is invented. Pose/expression remain review choices. Inherited full-scene native-grid authorship remains unresolved.'}
 (B/'sources/repair-plan.json').write_text(json.dumps(plan,indent=2));(B/'sources/pre-edit-declaration.json').write_text(json.dumps({'candidateExisted':(B/DEST).exists(),'planSha256':sha(B/'sources/repair-plan.json'),'sourceSha256':sha(B/SRC),'declaredBeforeRendering':True},indent=2));print('Prepared masks',[(k,v['pixels'])for k,v in plan['masks'].items()],'union',plan['unionMask']['pixels'])

def render():
 plan=json.loads((B/'sources/repair-plan.json').read_text());assert sha(B/'sources/repair-plan.json')==json.loads((B/'sources/pre-edit-declaration.json').read_text())['planSha256'];assert sha(B/plan['source'])==plan['baseApprovedSha256'];original=Image.open(B/plan['source']).convert('RGB');candidate=original.copy();d=ImageDraw.Draw(candidate)
 for k,v in plan['masks'].items():assert sha(B/v['file'])==v['sha256']
 for op in plan['operations']:
  co=op['coordinates'];rgb=tuple(op['rgb']);assert original.getpixel(tuple(op['sample']))==rgb
  if op['kind']=='point':d.point(tuple(co),fill=rgb)
  elif op['kind']=='line':d.line([tuple(p)for p in co],fill=rgb,width=op['width'])
  else:d.polygon([tuple(p)for p in co],fill=rgb)
 allowed=Image.open(B/plan['unionMask']['file']).convert('L');effective=Image.new('L',(314,206),0);layer=Image.new('RGBA',(314,206));changed=[];masks={k:Image.open(B/v['file']).convert('L')for k,v in plan['masks'].items()};counts={k:0 for k in masks}
 for y in range(206):
  for x in range(314):
   before=original.getpixel((x,y));after=candidate.getpixel((x,y))
   if before!=after:
    assert allowed.getpixel((x,y))==255,(x,y);region=next(k for k,mask in masks.items()if mask.getpixel((x,y)));counts[region]+=1;effective.putpixel((x,y),255);layer.putpixel((x,y),after+(255,));changed.append({'x':x,'y':y,'region':region,'beforeRGB':list(before),'afterRGB':list(after)})
 for g in plan['protectedGuards']:assert candidate.crop(g['box']).tobytes()==original.crop(g['box']).tobytes(),g['name']
 receipt=Image.open(B/plan['passingReceiptMask']).convert('L');assert all(candidate.getpixel((x,y))==original.getpixel((x,y))for y in range(206)for x in range(314)if receipt.getpixel((x,y)))
 candidate.save(B/plan['candidate']);effective.save(B/'masks/effective-change-mask.png');layer.save(B/'sources/exact-native-edit-layer.png');(B/'sources/changed-pixels.json').write_text(json.dumps(changed,indent=2))
 with(B/'sources/changed-pixels.csv').open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=['x','y','region','beforeRGB','afterRGB']);w.writeheader();w.writerows(changed)
 for name,im in [('approved',original),('candidate-v04',candidate)]:im.resize((1256,824),Image.Resampling.NEAREST).save(B/'previews'/f'paper-emergency-{name}-4x.png')
 pair=Image.new('RGB',(628,206));pair.paste(original,(0,0));pair.paste(candidate,(314,0));pair.save(B/'comparisons/approved-left-candidate-right-native.png');pair.resize((2512,824),Image.Resampling.NEAREST).save(B/'comparisons/approved-left-candidate-right-4x.png')
 for name,box in [('face',(206,98,232,122)),('hands',(201,118,246,143)),('P1',(149,177,174,194)),('attendant',(199,94,247,145))]:
  old=original.crop(box);new=candidate.crop(box);out=Image.new('RGB',(old.width*2,old.height));out.paste(old,(0,0));out.paste(new,(old.width,0));out.save(B/'comparisons'/f'{name}-before-after-native.png');out.resize((out.width*4,out.height*4),Image.Resampling.NEAREST).save(B/'comparisons'/f'{name}-before-after-4x.png');out.resize((out.width*8,out.height*8),Image.Resampling.NEAREST).save(B/'comparisons'/f'{name}-before-after-8x.png')
 total=len(changed);stats={'status':'generated','selection':'unselected','approved':False,'assetPath':None,'dimensions':[314,206],'mode':'RGB','alpha':'opaque','sourceSha256':sha(B/plan['source']),'candidateSha256':sha(B/plan['candidate']),'changedPixels':total,'changedPixelsByRegion':counts,'unchangedPixels':314*206-total,'changedPercent':total/(314*206)*100,'outsideDeclaredMaskChanges':0,'P2Changes':0,'passingReceiptChanges':0,'protectedGuardChanges':0,'originalUniqueRGB':len(set(original.get_flattened_data())),'candidateUniqueRGB':len(set(candidate.get_flattened_data())),'paletteTarget':None,'noGlobalFilters':True,'geometryTransforms':0};(B/'sources/repair-result.json').write_text(json.dumps(stats,indent=2));print(json.dumps(stats,indent=2))
if __name__=='__main__':
 if '--prepare'in sys.argv:prepare()
 if '--render'in sys.argv:render()
