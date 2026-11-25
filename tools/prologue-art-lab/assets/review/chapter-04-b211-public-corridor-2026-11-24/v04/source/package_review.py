from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
import json,hashlib,html
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(rel):
 im=Image.open(ROOT/rel);return {'file':rel,'sha256':sha(ROOT/rel),'dimensions':list(im.size),'mode':im.mode}
def main():
 dry='references/CH4-NEW-04-public-corridor-v02.png';before='references/CH4-NEW-04-public-corridor-flood-v03.png';after='native/CH4-NEW-04-public-corridor-flood-v04.png'
 for p in(ROOT/'references').glob('*.png'):
  im=Image.open(p);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/'previews'/(p.stem+'-4x.png'))
 layout=[];font=ImageFont.load_default(size=13)
 def sheet(items,name):
  sizes=[Image.open(ROOT/p).size for t,p in items];widths=[max(w+16,int(font.getlength(t))+16)for(t,p),(w,h)in zip(items,sizes)];im=Image.new('RGB',(sum(widths)+8,max(h for w,h in sizes)+44),'#283d35');d=ImageDraw.Draw(im);x=8
  for(t,p),width in zip(items,widths):
   d.text((x+4,8),t,font=font,fill='#f0e4c4');im.paste(Image.open(ROOT/p).convert('RGB'),(x+4,36));layout.append({'sheet':name,'caption':t,'textWidth':font.getlength(t),'panelWidth':width,'fits':font.getlength(t)<width-8});x+=width
  im.save(ROOT/f'comparisons/{name}-native.png');im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/f'comparisons/{name}-4x.png')
 sheet([('v03 flood -94px NPC',before),('v04 adult scale / clean clusters',after)],'v03-v04-flood')
 items=[]
 for v,f in[('v03',before),('v04',after)]:
  n=f'previews/{v}-character-sign-native.png';im=Image.open(ROOT/f).crop((84,56,224,202));im.save(ROOT/n);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/n.replace('-native','-4x'));items.append((v+' character / sign',n))
 sheet(items,'character-sign')
 sheet([('v04 flood',after),('Approved Staff Lavatory','references/staff_lavatory.png'),('Approved Ch2 Bureau','references/conveniences_bureau.png')],'canonical-benchmarks')
 (ROOT/'evidence/caption-layout.json').write_text(json.dumps(layout,indent=2)+'\n')
 a=Image.open(ROOT/before);b=Image.open(ROOT/after);n=sum(p!=q for p,q in zip(a.get_flattened_data(),b.get_flattened_data()));d=ImageChops.difference(a,b);ImageChops.lighter(ImageChops.lighter(d.getchannel('R'),d.getchannel('G')),d.getchannel('B')).point(lambda p:255 if p else 0).save(ROOT/'masks/actual-changes.png')
 old=json.loads((ROOT.parent/'v03/manifest.json').read_text());m={'title':'B2-11 v04 — adult doorway scale and clean-cluster attendant','branch':old['branch'],'preservationBaseline':'19c67561d371c2bc524d39bc9f2a57e8b4584961','status':'UNSELECTED','ownerApproved':False,'primaryUnits':1,'newPrimaryAssets':0,'newlyRevisedArtworkUnits':1,'asset':{**old['asset'],'native':rec(dry),'preview4x':rec('previews/CH4-NEW-04-public-corridor-v02-4x.png'),'unchangedFromV02':True},'supplementalReferences':[{**old['supplementalReferences'][0],'native':rec(after),'preview4x':rec('previews/CH4-NEW-04-public-corridor-flood-v04-4x.png')}],'sourceDerived':True,'whollyIndependentNativeAuthorship':False,'newImageGeneration':True,'wholeRoomRegenerated':False,'methodRecord':'evidence/repair.json','nativeLayerRecipe':'source/refine.py','originalSource':'originals/attendant-clean-cluster-source.png','originalGenerationProvenance':'evidence/generation-provenance.json','changesFromV03':n,'dryCandidateBytesUnchanged':True,'narrativeGameplayBindingsModified':False,'productionSelectionsModified':False}
 (ROOT/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 def fig(title,one,four):
  w,h=Image.open(ROOT/one).size
  return f'<section class="figure"><h3>{html.escape(title)}</h3><nav><button data-scale="1">Native 1×</button><button data-scale="4">Exact 4×</button><a href="{one}">PNG</a><a href="{four}">4× PNG</a></nav><div class="raster"><img src="{one}" data-one="{one}" data-four="{four}" data-w="{w}" data-h="{h}" width="{w}" height="{h}" alt="{html.escape(title)}"></div></section>'
 css='body{margin:0;background:#142820;color:#efe5c8;font:16px/1.5 system-ui,sans-serif}main{padding:22px}header,article{padding:20px;border:1px solid #647466;margin-bottom:26px}h1,h2,h3{margin:0 0 12px}a{color:#bce0c9;margin-right:16px}nav{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0}button{padding:10px;background:#435e4d;border:1px solid #b7c8ac;color:#f4e9ca;cursor:pointer}.figure{padding:14px;margin:20px 0;background:#294136}.raster{overflow:auto;max-width:100%;background:#253b32}.raster img{display:block;max-width:none!important;image-rendering:pixelated}code{overflow-wrap:anywhere}'
 body='<article id="flood"><h2>v04 flood reference · UNSELECTED</h2>'+fig('v04 flood',after,'previews/CH4-NEW-04-public-corridor-flood-v04-4x.png')+'</article><article id="dry"><h2>Unchanged v02 dry candidate · UNSELECTED</h2>'+fig('Dry master unchanged',dry,'previews/CH4-NEW-04-public-corridor-v02-4x.png')+'</article><article id="comparisons"><h2>Before / after</h2>'
 for title,name in[('Full flood before / after','v03-v04-flood'),('NPC and sign detail','character-sign'),('Approved scene benchmarks','canonical-benchmarks')]:body+=fig(title,f'comparisons/{name}-native.png',f'comparisons/{name}-4x.png')
 body+='</article><article id="benchmarks"><h2>Actual approved references</h2>'
 for n in['staff_lavatory','conveniences_bureau','control_tower','courtesy_stage']:body+=fig(n,'references/'+n+'.png','previews/'+n+'-4x.png')
 body+='</article>'
 header='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>B2-11 v04 attendant scale and clarity</title><style>'+css+'</style><main><header><h1>B2-11 v04 · adult scale, clean clusters</h1><p><strong>Everything UNSELECTED.</strong> Only the flood reference is revised. The dry master, room, hatch, doors, water, sign and earlier versions stay exact.</p><p>The same gray-haired hotel attendant is rebuilt from a new clean-cluster source at132 native pixels tall, up from94, with feet fixed at the existing floor line. The existing nearby STAFF door leaf is174 pixels at its near edge. Face, hands, hair and tailoring retain purposeful connected shapes without speckled shade texture. The v03 sign is unchanged and remains17 pixels clear of the new character bounding box.</p><nav><a href="manifest.json">Manifest / hashes</a><a href="README.md">Method</a><a href="evidence/validation.json">QA / preservation</a><a href="evidence/repair.json">Native repair recipe</a><a href="evidence/generation-provenance.json">Source provenance</a><a href="source/attendant-clean-cluster-prompt.txt">Exact prompt</a><a href="originals/attendant-clean-cluster-source.png">Clean source original</a><a href="comparisons/character-sign-4x.png">NPC / sign4× comparison</a></nav></header>'
 script='<script>document.querySelectorAll("button[data-scale]").forEach(b=>b.onclick=()=>{const i=b.closest("section.figure").querySelector("img"),s=Number(b.dataset.scale);i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;});</script></main></html>'
 (ROOT/'index.html').write_text(header+body+script);print(json.dumps({'changedPixels':m['changesFromV03'],'status':'UNSELECTED'}))
if __name__=='__main__':main()
