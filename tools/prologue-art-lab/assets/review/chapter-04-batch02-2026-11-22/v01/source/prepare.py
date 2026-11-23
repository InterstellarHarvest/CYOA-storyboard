"""Disclosed source-derived production reduction and exact native lettering.

No asset is claimed independently authored on the target grid. Portraits retain
source anatomy; cleanup affects alpha debris, contaminated edges and local
contrast, not construction. All prior selected artwork stays untouched.
"""
from pathlib import Path
from PIL import Image,ImageFilter,ImageDraw,ImageFont
from collections import deque
import json,hashlib,shutil
from pixel_text import draw as pixel_draw,measure as pixel_measure,project
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'story/artwork.draft.json').exists())
OLD=REPO/'tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(im,rel):
 p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True);im.save(p)
def rec(rel):
 p=ROOT/rel;im=Image.open(p);return {'file':rel,'sha256':sha(p),'dimensions':list(im.size),'mode':im.mode}
def portrait(src):
 im=Image.open(src).convert('RGBA').convert('RGBa').resize((564,278),Image.Resampling.LANCZOS).convert('RGBA');raw=im.copy();p=im.load();w,h=im.size
 for y in range(h):
  for x in range(w):
   if p[x,y][3]<=40:p[x,y]=(0,0,0,0)
 seen=set();parts=[]
 for y in range(h):
  for x in range(w):
   if not p[x,y][3] or (x,y) in seen:continue
   q=deque([(x,y)]);seen.add((x,y));part=[]
   while q:
    u,v=q.popleft();part.append((u,v))
    for xx,yy in [(u-1,v),(u+1,v),(u,v-1),(u,v+1)]:
     if 0<=xx<w and 0<=yy<h and p[xx,yy][3] and (xx,yy) not in seen:seen.add((xx,yy));q.append((xx,yy))
   parts.append(part)
 parts.sort(key=len,reverse=True)
 for part in parts[1:]:
  for x,y in part:p[x,y]=(0,0,0,0)
 edge=im.copy();ep=edge.load();fringe=0
 for y in range(1,h-1):
  for x in range(1,w-1):
   r,g,b,a=p[x,y]
   if not a or max(r,g,b)-min(r,g,b)<100 or not any(p[u,v][3]==0 for u,v in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]):continue
   near=[((u-x)**2+(v-y)**2,u,v) for v in range(max(1,y-3),min(h-1,y+4)) for u in range(max(1,x-3),min(w-1,x+4)) if p[u,v][3]>=245 and all(p[uu,vv][3]>200 for uu,vv in [(u-1,v),(u+1,v),(u,v-1),(u,v+1)])]
   if near:
    _,u,v=min(near);rgb=p[u,v][:3]
    if sum((c-d)**2 for c,d in zip((r,g,b),rgb))>70**2:ep[x,y]=rgb+(a,);fringe+=1
 sharp=edge.convert('RGB').filter(ImageFilter.UnsharpMask(radius=.55,percent=75,threshold=2));s=sharp.load();before=edge.copy();q=before.load();changed=0
 for y in range(1,h-1):
  for x in range(1,w-1):
   if q[x,y][3]>=245 and all(q[u,v][3]>=245 for u,v in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]):
    rgb=s[x,y];changed+=rgb!=q[x,y][:3];ep[x,y]=rgb+(q[x,y][3],)
 return edge,{'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'reduction':'Premultiplied RGBa Lanczos to564x278; no crop/repose','alphaCleanup':'<=40 alpha and disconnected debris removed; original interior alpha retained','fringeColorPixelsRepaired':fringe,'interiorFinish':{'filter':'UnsharpMask','radius':.55,'percent':75,'threshold':2,'nearOpaqueInteriorOnly':True,'pixelsChanged':changed,'alphaUnchangedDuringFinish':True},'sourceDimensions':list(Image.open(src).size),'changedPixelsFromRawReduction':sum(a!=b for a,b in zip(raw.get_flattened_data(),edge.get_flattened_data()))}
def main():
 for d in ['native','previews','comparisons','references','evidence','fonts']:(ROOT/d).mkdir(exist_ok=True)
 refs={'approved-restroom.png':OLD/'v07/native/CH4-04-restroom-v03.png','approved-attendant.png':OLD/'v04/references/pavilion_attendant_idle.png','approved-presenter.png':OLD/'v04/references/pavilion_presenter_idle.png','approved-bureau.png':REPO/'assets/selected/art/scenes/biology_park/conveniences_bureau.png','approved-tower.png':REPO/'assets/selected/art/scenes/biology_park/control_tower.png','approved-reception-background.png':REPO/'assets/selected/art/portraits/receptionist/reception_background.png','plumber-identity.png':OLD/'v06/detailed/NPC-plumbers-original.png'}
 for name,path in refs.items():shutil.copyfile(path,ROOT/'references'/name)
 allnodes=json.loads((REPO/'story/chapters/chapter-04.wip.json').read_text())['nodes'];relevant=['hotel_restroom_plumber','hotel_wheel_buyer_lead','hotel_lot_receipt_study','hotel_key_master_cabinet','hotel_stall_porter_protest']
 (ROOT/'evidence/canonical-nodes.json').write_text(json.dumps({k:allnodes[k] for k in relevant},indent=2)+'\n')
 inventory=OLD/'v08/BATCH2-INVENTORY.json';shutil.copyfile(inventory,ROOT/'evidence/canonical-v08-inventory.json')
 contracts={'focusDimensions':[564,278],'focusAlpha':'opaque','portraitDimensions':[564,278],'portraitAlpha':'transparent','backgroundDimensions':[564,278],'authority':['docs/105_CANONICAL_SYNC_PIPELINE.md#Owner/Story Director dimension resolution','tools/sync/lib.mjs contractFor','docs/108_CHAPTER_02_ARTWORK_COMPLETION_AND_GAMEPLAY_HANDOFF_20261117.md'],'notItemInspectDimensions':[565,451],'actualRuntimeEvidence':{'repository':'InterstellarHarvest/out-of-order','commit':'d849da779667b3bcde5dedf2e7d5a7601d8b4b6e','file':'game/js/stage.js','lines':'147-168','focus':'focus: { size: [564, 278], scale: 1 }','inspect':'inspect: { size: [565, 451] }','readOnlyInspection':True},'narrativeModified':False}
 (ROOT/'evidence/dimension-contract.json').write_text(json.dumps(contracts,indent=2)+'\n')
 assets=[];derivation={}
 specs=[('CH4-B2-01','Plumber — worried','portrait','portraits:hotel_plumber:worried',['hotel_restroom_plumber']),('CH4-B2-02','Eddie — pleased','portrait','portraits:hotel_plumber_assistant:pleased',['hotel_wheel_buyer_lead']),('CH4-B2-03','Restroom conversation background','portrait-background','scenes:grand_bellevue/restroom#portraitBackground',['hotel_restroom_plumber','hotel_wheel_buyer_lead','hotel_stall_porter_protest']),('CH4-B2-04','Lot 14 receipt','focus','focus:grand_bellevue/restroom/lot_14_receipt',['hotel_lot_receipt_study']),('CH4-B2-05','Emergency master isolator','focus','focus:grand_bellevue/restroom/master_isolator',['hotel_key_master_cabinet'])]
 for id_,title,kind,key,nodes in specs:
  source=ROOT/f'originals/{id_}-original.png'
  if kind=='portrait':im,report=portrait(source)
  else:im=Image.open(source).convert('RGB').resize((564,278),Image.Resampling.LANCZOS);report={'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'sourceDimensions':list(Image.open(source).size),'reduction':'Lanczos to opaque564x278; newly generated close composition, not an enlargement of approved scene'}
  if id_=='CH4-B2-02':
   layer=Image.new('RGBA',(30,45),(0,0,0,0));ImageDraw.Draw(layer).rectangle((3,2,26,17),fill='#e3cfa8')
   pixel_draw(layer,'LOT',(6,3),1,'#343a30');pixel_draw(layer,'14',(10,11),1,'#343a30')
   quad=[(241,182),(269,179),(276,223),(253,228)];overlay=project(layer,quad)
   im=Image.alpha_composite(im,overlay)
   report['portraitPropLettering']={'text':['LOT','14'],'font':'approved Tiny5 integer bitmap','planeQuad':quad,'method':'Perspective-projected top receipt inset, no changes to fingers; full receipt copy belongs to the Focus A asset','minimumNativeCapHeight':5}
  if id_=='CH4-B2-03':
   before=im.copy();edited=Image.open(ROOT/'originals/CH4-B2-03-label-cleanup.png').convert('RGB').resize((564,278),Image.Resampling.LANCZOS)
   box=(209,104,247,118);im.paste(edited.crop(box),box)
   changed=[(i%564,i//564) for i,(a,b) in enumerate(zip(before.get_flattened_data(),im.get_flattened_data())) if a!=b]
   assert all(box[0]<=x<box[2] and box[1]<=y<box[3] for x,y in changed)
   label=Image.new('RGBA',(38,12),(0,0,0,0));pixel_draw(label,'WATER',(4,3),1,'#253c31');im=Image.alpha_composite(im.convert('RGBA'),project(label,[(209,104),(247,104),(247,118),(209,118)])).convert('RGB')
   report['readablePortraitContextLabel']={'text':'WATER','font':'approved Tiny5 bitmap; 5px cap height','planeQuad':[(209,104),(247,104),(247,118),(209,118)],'mainSceneUnchanged':True}
   report['nativeLabelCleanup']={'method':'Use only the imagegen-edited blank upper cabinet plaque, retaining every other reduced pixel exactly','box':box,'changedPixels':len(changed),'outsideBoxChanges':0,'source':'originals/CH4-B2-03-label-cleanup.png'}
  if id_=='CH4-B2-04':
   # Exact canonical receipt copy, native final lettering on generated blank paper.
   canonical=['LOT 14 — BRASS WATER SHUTOFF WHEEL.','BUYER — COMMODORE E. BIXBY.','PURCHASE PRICE — 12.00.','DECLARED PURPOSE — NAVAL DECORATION.','ALL SALES FINAL','CATALOGUING ERRORS REQUIRE ORIGINAL RECEIPT.']
   rows=[(canonical[0],52,26,2,'#393d32'),(canonical[1],52,52,2,'#393d32'),(canonical[2],52,78,2,'#393d32'),(canonical[3],52,104,2,'#393d32'),(canonical[4],52,138,3,'#8a4635'),('CATALOGUING ERRORS REQUIRE',52,173,2,'#393d32'),('ORIGINAL RECEIPT.',52,189,2,'#393d32')]
   safe=(46,22,466,202);bounds=[];layer=Image.new('RGBA',(480,224),(0,0,0,0))
   for text,x,y,scale,color in rows:
    assert text in allnodes['hotel_lot_receipt_study']['text']
    box=pixel_draw(layer,text,(x,y),scale,color);assert safe[0]<=box[0] and safe[1]<=box[1] and box[2]<=safe[2] and box[3]<=safe[3];bounds.append(box)
   quad=[(42,29),(516,25),(516,251),(38,254)]
   im=Image.alpha_composite(im.convert('RGBA'),project(layer,quad)).convert('RGB')
   report['nativeLettering']={'method':'Approved Tiny5 bitmap atlas; hard 0/255 glyphs, integer clusters; nearest-pixel homography aligns text to the receipt plane','sourceNode':'hotel_lot_receipt_study','lines':canonical,'renderedRows':[t for t,*_ in rows],'safeTextRectInPaperPlane':safe,'glyphBoundsInPaperPlane':bounds,'paperPlaneSize':[480,224],'paperPlaneQuad':quad,'minimumPaperPlaneMargins':[52,26,40,25],'exceptionWrap':'Only line wrapping changes; exact canonical phrase is preserved.','minimumNativeCapHeight':10,'paletteCap':False}
  if id_=='CH4-B2-05':
   before=im.copy();layer=Image.new('RGBA',(128,28),'#dbc99e')
   for text,y in [('EMERGENCY',3),('WATER ISOLATION',16)]:pixel_draw(layer,text,((128-pixel_measure(text,1,'pressstart'))//2,y),1,'#23382f','pressstart')
   quad=[(306,38),(423,35),(424,60),(306,64)];im=Image.alpha_composite(im.convert('RGBA'),project(layer,quad)).convert('RGB')
   changed=[(i%564,i//564) for i,(a,b) in enumerate(zip(before.get_flattened_data(),im.get_flattened_data())) if a!=b]
   plate=(305,34,425,65);assert all(plate[0]<=x<plate[2] and plate[1]<=y<plate[3] for x,y in changed)
   report['nativeLettering']={'method':'Approved Press Start bitmap glyphs; nearest-pixel homography follows the actual enamel plaque perspective; bevel/hardware untouched','text':['EMERGENCY','WATER ISOLATION'],'planeSize':[128,28],'planeQuad':quad,'changedBounds':plate,'outsideLabelChanges':0,'nativeCapHeightApproximate':7,'glyphMaskAlpha':[0,255]}
  native=f'native/{id_}-v01.png';save(im,native);four=f'previews/{id_}-4x.png';save(im.resize((2256,1112),Image.Resampling.NEAREST),four)
  derivation[id_]=report
  assets.append({'id':id_,'title':title,'kind':kind,'key':key,'nodeIds':nodes,'status':'UNSELECTED','selected':False,'sourceDerived':True,'original':rec(f'originals/{id_}-original.png'),'native':rec(native),'preview4x':rec(four),'provenance':'evidence/derivation.json','prompt':f'prompts/{id_}.txt'})
 bg=Image.open(ROOT/assets[2]['native']['file']).convert('RGBA')
 for a in assets[:2]:
  fg=Image.open(ROOT/a['native']['file']).convert('RGBA');composite=Image.alpha_composite(bg,fg);rel=f'previews/{a["id"]}-composite.png';save(composite,rel);save(composite.resize((2256,1112),Image.Resampling.NEAREST),rel.replace('.png','-4x.png'))
  for label,color in [('light','#efe5ce'),('dark','#152727')]:save(Image.alpha_composite(Image.new('RGBA',(564,278),color),fg),f'previews/{a["id"]}-alpha-{label}.png')
 for rel in ['references/approved-attendant.png','references/approved-presenter.png','references/approved-restroom.png','references/approved-bureau.png','references/approved-tower.png','references/approved-reception-background.png']:
  im=Image.open(ROOT/rel);save(im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST),'previews/'+Path(rel).stem+'-4x.png')
 (ROOT/'evidence/derivation.json').write_text(json.dumps({'pillowVersion':Image.__version__,'sourceModified':False,'allSourceDerived':True,'assets':derivation},indent=2)+'\n')
 manifest={'title':'Chapter 4 B2-01 — Restroom dialogue and controls v01','status':'UNSELECTED','branch':'art/ch4-batch01-review-20261121','canonicalInventoryCommit':'3463e20bd366390008fa4f71c087ed5f334f3a31','inventorySha256':sha(inventory),'contract':'564x278 native; transparent foregrounds; opaque background and Focus A; exact2256x1112 NN previews','productionIntegrationPerformed':False,'batch1ApprovedUnchanged':True,'assets':assets,'references':{n:rec('references/'+n) for n in refs}}
 (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print('Prepared five source-derived UNSELECTED assets, both composites and exact4x views.')
if __name__=='__main__':main()
