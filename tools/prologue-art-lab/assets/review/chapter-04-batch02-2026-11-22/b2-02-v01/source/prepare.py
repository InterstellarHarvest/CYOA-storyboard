"""B2-02 source-derived target-grid preparation, never native-authorship claims."""
from pathlib import Path
from PIL import Image,ImageFilter,ImageDraw,ImageFont
import json,hashlib,shutil
from palette import compact
ROOT=Path(__file__).resolve().parents[1];REPO=next(p for p in ROOT.parents if (p/'story/artwork.draft.json').exists());OLD=REPO/'tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21';B201=ROOT.parent/'v01'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(rel):
 p=ROOT/rel;im=Image.open(p);return {'file':rel,'sha256':sha(p),'dimensions':list(im.size),'mode':im.mode}
def main():
 for d in ['native','previews','comparisons','references','evidence']:(ROOT/d).mkdir(exist_ok=True)
 refs={'approved-lobby.png':OLD/'v05/native/CH4-01-lobby-v05.png','approved-restroom.png':OLD/'v07/native/CH4-04-restroom-v03.png','approved-auctioneer.png':OLD/'v08/native/CH4-03-auctioneer-source-derived-v08.png','approved-attendant.png':B201/'references/approved-attendant.png','approved-presenter.png':B201/'references/approved-presenter.png','approved-receptionist.png':OLD/'v04/references/receptionist__receptionist_idle.png','approved-groundkeeper.png':OLD/'v04/references/groundskeeper__groundskeeper_idle.png','approved-conductor.png':OLD/'v04/references/courtesy_conductor__courtesy_conductor_talking.png','approved-tower.png':B201/'references/approved-tower.png','approved-bureau.png':B201/'references/approved-bureau.png','approved-pavilion-exterior.png':REPO/'assets/selected/pending-integration/scenes/pavilion_reboot/exterior_exit.png'}
 for name,source in refs.items():shutil.copyfile(source,ROOT/'references'/name)
 inv=OLD/'v08/BATCH2-INVENTORY.json';m=json.loads(inv.read_text());group=next(g for g in m['groups'] if g['id']=='B2-02');inventory=[a for a in m['assets'] if a['group']=='B2-02'];allnodes=json.loads((REPO/'story/chapters/chapter-04.wip.json').read_text())['nodes'];(ROOT/'evidence/canonical-nodes.json').write_text(json.dumps({k:allnodes[k] for k in group['nodeIds']},indent=2)+'\n');(ROOT/'evidence/inventory-source.json').write_text(json.dumps({'sourceCommit':'3463e20bd366390008fa4f71c087ed5f334f3a31','file':str(inv.relative_to(REPO)),'sha256':sha(inv),'group':group,'assets':inventory},indent=2)+'\n')
 assets=[];methods={}
 for index,item in enumerate(inventory):
  id_='CH4-B2-'+str(index+6).zfill(2);kind={'main_scene':'scene','portrait':'portrait','portrait_background':'portrait-background'}[item['category']];size=tuple(item['dimensions']);original=f'originals/{id_}-original.png'
  if id_=='CH4-B2-10':
   im=Image.open(ROOT/original).convert('RGBA').resize(size,Image.Resampling.NEAREST);im.putalpha(im.getchannel('A').point(lambda a:255 if a>=128 else 0));im,method=compact(im);method['sourceDerived']=True;method['nativeTransfer']='Nearest target-grid transfer of newly generated stepped-cluster art; binary cutout alpha; no smooth gradients or sharpening';method['sourceGeometryModifiedAtNative']=False
  else:
   im=Image.open(ROOT/original).convert('RGB').resize(size,Image.Resampling.LANCZOS);method={'sourceDerived':True,'nativeTransfer':'Controlled Lanczos reduction of new composed illustration, then restrained native edge clarification (UnsharpMask radius0.45,60%,threshold3); no palette cap on environment','independentlyAuthoredAtNativeResolution':False}
   # Scoped requested staging corrections. Every other reduced pixel is retained.
   if id_ in ['CH4-B2-07','CH4-B2-08']:
    before=im.copy();file='originals/'+id_+('-worker-corrected.png' if id_.endswith('07') else '-workers-corrected.png');edited=Image.open(ROOT/file).convert('RGB').resize(size,Image.Resampling.LANCZOS)
    box=(59,94,96,154) if id_.endswith('07') else (212,91,247,115);im.paste(edited.crop(box),box);diff=[(i%size[0],i//size[0]) for i,(a,b) in enumerate(zip(before.get_flattened_data(),im.get_flattened_data())) if a!=b];assert all(box[0]<=x<box[2] and box[1]<=y<box[3] for x,y in diff);method['stagingCorrection']={'file':file,'nativeBox':box,'changedPixels':len(diff),'outsideBoxChangesBeforeFinish':0,'reason':'Match the exact authored worker count/description'}
   im=im.filter(ImageFilter.UnsharpMask(radius=.45,percent=60,threshold=3))
  native=f'native/{id_}-v01.png';im.save(ROOT/native);four=f'previews/{id_}-4x.png';im.resize((size[0]*4,size[1]*4),Image.Resampling.NEAREST).save(ROOT/four)
  key='scenes:'+item['logicalKey'] if kind=='scene' else 'portraits:'+item['logicalKey'] if kind=='portrait' else 'scenes:'+item['logicalKey']+'#portraitBackground'
  assets.append({'id':id_,'title':item['logicalKey'].split('/')[-1].replace('_',' ').title(),'key':key,'inventoryId':item['inventoryId'],'kind':kind,'nodeIds':item['nodeIds'],'status':'UNSELECTED','selected':False,'sourceDerived':True,'native':rec(native),'preview4x':rec(four),'original':rec(original),'prompt':f'prompts/{id_}.txt'});methods[id_]=method
 bg=Image.open(ROOT/assets[5]['native']['file']).convert('RGBA');fg=Image.open(ROOT/assets[4]['native']['file']).convert('RGBA');c=Image.alpha_composite(bg,fg);c.save(ROOT/'previews/foreman-composite.png');c.resize((2256,1112),Image.Resampling.NEAREST).save(ROOT/'previews/foreman-composite-4x.png')
 for label,color in [('light','#f0e6ce'),('dark','#182a24')]:Image.alpha_composite(Image.new('RGBA',(564,278),color),fg).save(ROOT/f'previews/foreman-alpha-{label}.png')
 for name in refs:
  im=Image.open(ROOT/'references'/name);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/'previews'/(Path(name).stem+'-4x.png'))
 sheet=Image.new('RGB',(1164,972),'#23382f');d=ImageDraw.Draw(sheet)
 for i,a in enumerate(assets):
  x=(i%2)*582+9;y=(i//2)*324+9;d.text((x,y),a['id']+' '+a['title'],font=ImageFont.load_default(size=15),fill='#f1dfc0');im=Image.open(ROOT/a['native']['file']).convert('RGBA');back=Image.alpha_composite(Image.new('RGBA',im.size,'#40574b'),im);sheet.paste(back.convert('RGB'),(x,y+29))
 sheet.save(ROOT/'comparisons/B2-02-all-native.png');sheet.resize((4656,3888),Image.Resampling.NEAREST).save(ROOT/'comparisons/B2-02-all-4x.png')
 (ROOT/'evidence/derivation.json').write_text(json.dumps({'pillowVersion':Image.__version__,'allSourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'assets':methods},indent=2)+'\n');(ROOT/'manifest.json').write_text(json.dumps({'title':'Chapter4 B2-02 Loading dock and service arrivals v01','groupId':'B2-02','status':'UNSELECTED','branch':'art/ch4-batch01-review-20261121','inventorySource':'evidence/inventory-source.json','storyNodeCoverage':group['nodeIds'],'productionIntegrationPerformed':False,'sourceDerived':True,'assets':assets,'references':{name:rec('references/'+name) for name in refs}},indent=2)+'\n');print('Prepared six B2-02 candidates and foreman composite.')
if __name__=='__main__':main()
