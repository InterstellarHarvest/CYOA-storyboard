"""NPC-only before/after review with exact final-pixel 4x exports."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib

ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT.parent/'v06'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(rel):
 p=ROOT/rel;im=Image.open(p)
 return {'file':rel,'dimensions':list(im.size),'mode':im.mode,'sha256':sha(p)}
def four(src,dst):
 im=Image.open(ROOT/src);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/dst)
def backing(size):
 im=Image.new('RGB',size,'#263b38');d=ImageDraw.Draw(im)
 for y in range(0,size[1],8):
  for x in range(0,size[0],8):
   if (x//8+y//8)%2:d.rectangle((x,y,x+7,y+7),fill='#3a5047')
 return im

def main():
 for n in ['previews','comparisons']:(ROOT/n).mkdir(exist_ok=True)
 d=json.loads((ROOT/'evidence/npc-derivation.json').read_text());font=ImageFont.load_default(size=12)
 board=Image.new('RGB',(456,372),'#1b2e2c');draw=ImageDraw.Draw(board)
 for i,l in enumerate(d['layers']):
  x=(i%3)*152+8;y=(i//3)*124+8;draw.text((x,y),l['id'].replace('-and-chair',''),font=font,fill='#efdcb5')
  for col,label,key in [(0,'v06','previousFile'),(1,'v07','file')]:
   xx=x+col*72;draw.text((xx,y+16),label,font=font,fill='#bbd7be')
   im=Image.open(ROOT/l[key]).convert('RGBA');bg=backing(im.size);bg.paste(im,(0,0),im);board.paste(bg,(xx,y+32))
 for i,(title,rel,box) in enumerate([('Approved presenter','../v06/references/approved-pavilion-urgency_stage.png',(73,85,114,154)),('Approved attendant','../v06/references/approved-pavilion-courtesy_stage.png',(199,91,242,145))]):
  x=i*152+8;y=256;draw.text((x,y),title,font=font,fill='#efdcb5');im=Image.open(ROOT/rel).crop(box);board.paste(im,(x,y+24))
 board.save(ROOT/'comparisons/NPC-v06-v07-approved.png');four('comparisons/NPC-v06-v07-approved.png','comparisons/NPC-v06-v07-approved-4x.png')
 assets=[];cards=[]
 for number,name,title,approved in [(4,'restroom','Restroom','courtesy_stage'),(5,'ballroom','Ballroom','urgency_stage')]:
  id_='CH4-0'+str(number);native='native/'+id_+'-'+name+'-v03.png';old='../v06/native/'+id_+'-'+name+'-v02.png';preview='previews/'+id_+'-candidate-4x.png';old4='previews/'+id_+'-v06-4x.png';bench='../v06/references/approved-pavilion-'+approved+'.png';bench4='../v06/references/approved-pavilion-'+approved+'-4x.png'
  four(native,preview);four(old,old4)
  sheet=Image.new('RGB',(676,254),'#1b2e2c');sd=ImageDraw.Draw(sheet)
  for j,(label,rel) in enumerate([('v06',old),('v07 - NPC crispness only',native)]):
   x=12+j*338;sd.text((x,10),label,font=font,fill='#efdcb5');sheet.paste(Image.open(ROOT/rel),(x,34))
  comparison='comparisons/'+id_+'-v06-v07.png';sheet.save(ROOT/comparison);four(comparison,comparison.replace('.png','-4x.png'))
  asset={'id':id_,'title':title,'status':'UNSELECTED','authorship':'HYBRID: preserved native background plus source-derived NPC art','native':rec(native),'preview4x':rec(preview),'previous':rec(old),'previous4x':rec(old4),'benchmark':rec(bench),'benchmark4x':rec(bench4),'comparison':rec(comparison),'comparison4x':rec(comparison.replace('.png','-4x.png')),'background':rec('../v06/backgrounds/'+id_+'-'+name+'-background-v02.png')}
  assets.append(asset)
  panels=[]
  for role,label,one,big in [('previous','v06',old,old4),('candidate','v07 - UNSELECTED',native,preview),('benchmark','Approved scene NPC style',bench,bench4)]:
   panels.append(f'<div class="column"><h3>{label}</h3><div class="viewport"><img class="art {role}" data-target="{id_}" data-one="{one}" data-four="{big}" src="{one}" width="314" height="206" alt="{title} {label}"></div></div>')
  cards.append(f'<article id="{id_}"><h2>{title}</h2><div class="actions"><button class="scale" data-target="{id_}" data-scale="1">Native 1×</button><button class="scale" data-target="{id_}" data-scale="4">Exact 4×</button><a href="{native}">Candidate PNG</a><a href="{comparison}">Before/after PNG</a><a href="{comparison.replace(".png","-4x.png")}">4× before/after PNG</a></div><div class="grid">{"".join(panels)}</div></article>')
 manifest={'review':'Chapter 4 v07 — scene NPC crispness correction','status':'UNSELECTED','branch':'art/ch4-batch01-review-20261121','baseCommit':'314a1134c507a6670f05dd2228cc534e5299ca4e','policy':'../PRODUCTION-POLICY.md','sourceDerived':True,'assets':assets,'npcDerivation':'evidence/npc-derivation.json','npcComparison':rec('comparisons/NPC-v06-v07-approved.png'),'npcComparison4x':rec('comparisons/NPC-v06-v07-approved-4x.png'),'preservedAuctioneer':rec('../v06/native/CH4-03-auctioneer-source-derived-v06.png'),'frozenLobby':rec('../v05/native/CH4-01-lobby-v05.png'),'frozenPortraitBackground':rec('../v05/native/CH4-02-auctioneer-background-v05.png'),'sourcePrompts':['../v06/prompts/scene-plumbers-style.txt','../v06/prompts/scene-ballroom-people-style.txt','../v06/prompts/scene-porters-style.txt'],'processingBrief':'prompts/NPC-native-cleanup-v07.txt','knownLimitations':['Native sprite sizes remain 25-60px wide and 46-74px tall; fourfold display does not add information.','Some one-pixel source texture is more visible after crisp sampling. Owner review must judge the balance of clarity and illustration quality.','No independent native authorship is claimed for the source-derived NPCs or hybrid complete scenes.'],'pillowVersion':Image.__version__}
 (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 4 v07 · crisper scene NPCs</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#15282a;color:#f0e6d2;font:16px/1.55 system-ui,sans-serif}main{max-width:1400px;margin:auto;padding:28px}h1{font-size:clamp(1.8rem,3vw,2.5rem);line-height:1.2}h2{font-size:1.35rem}h3{font-size:1rem}.panel,article{padding:22px;border:1px solid #4d6c62;border-radius:8px;background:#203936;margin:24px 0}.tag{font-weight:700;color:#e9c389}.actions{display:flex;gap:15px;align-items:center;flex-wrap:wrap;margin:15px 0}button{background:#34594e;color:#f8ebd0;border:1px solid #90a18b;padding:8px 13px;border-radius:4px;cursor:pointer}a{color:#addfca}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.column{min-width:0}.viewport{max-width:100%;max-height:850px;overflow:auto;border:1px solid #5c7b6b}.art{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}button:focus-visible,a:focus-visible{outline:3px solid #ecd298}@media(max-width:1000px){.grid{grid-template-columns:1fr}}@media(max-width:600px){main{padding:12px}.panel,article{padding:14px}}
</style></head><body><main><header><p>Out of Order · Chapter 4</p><h1>Crisper scene NPCs at native size and 4×</h1><p class="tag">v07 · ALL CANDIDATES UNSELECTED</p></header><section class="panel intro"><p>The 4× exports were already exact nearest-neighbor. The softness was in v06's reduced NPC pixels. This revision uses sharper source samples for face/hand features, controlled body reduction and crisp native silhouette coverage. It retains the source-derived illustrations and their detail.</p><p><strong>Scope:</strong> scene NPC pixels only. Positions, scale, poses, contact shadows, room backgrounds, auctioneer and frozen v05 environments are preserved.</p><p><a href="evidence/npc-derivation.json">Exact derivation / feature regions</a> · <a href="evidence/scope-qa.json">Changed-pixel proof</a> · <a href="manifest.json">Manifest and hashes</a> · <a href="evidence/validation.json">QA</a> · <a href="../PRODUCTION-POLICY.md">Production policy</a></p></section><section class="panel" id="npc-detail"><h2>Actual NPC pixels: v06 / v07 / approved examples</h2><div class="actions"><button id="npc-native">Native 1× sheet</button><button id="npc-four">Exact 4× sheet</button><a href="comparisons/NPC-v06-v07-approved.png">Native comparison PNG</a><a href="comparisons/NPC-v06-v07-approved-4x.png">Exact 4× comparison PNG</a></div><div class="viewport"><img class="art npc-sheet" src="comparisons/NPC-v06-v07-approved-4x.png" data-one="comparisons/NPC-v06-v07-approved.png" data-four="comparisons/NPC-v06-v07-approved-4x.png" width="1824" height="1488" alt="Final NPC before/after pixels beside the exact approved scene examples"></div></section>__CARDS__<section class="panel"><h2>Preserved files and provenance</h2><p>No new artwork generation or character redesign. Every original, prompt, earlier candidate and review remains unchanged. Final scenes remain hybrid/source-derived NPC composites. Native resolution and exact scaling do not establish artistic approval.</p><p><a href="../v06/index.html">Preserved v06 gallery and auctioneer</a> · <a href="../v06/evidence/scene-npc-generation-receipts.json">Original character generation records</a> · <a href="prompts/NPC-native-cleanup-v07.txt">Processing brief</a> · <a href="README.md">Review notes</a></p><p>Main, production assets/workflows, narrative, gameplay and approval records are unchanged.</p></section></main><script>
document.querySelectorAll('.scale').forEach(b=>b.addEventListener('click',()=>{const a=document.getElementById(b.dataset.target),s=Number(b.dataset.scale);a.querySelectorAll('.previous,.candidate,.benchmark').forEach(i=>{i.src=s===4?i.dataset.four:i.dataset.one;i.width=314*s;i.height=206*s;});}));
function sheet(s){const i=document.querySelector('.npc-sheet');i.src=s===4?i.dataset.four:i.dataset.one;i.width=456*s;i.height=372*s;}document.getElementById('npc-native').onclick=()=>sheet(1);document.getElementById('npc-four').onclick=()=>sheet(4);
</script></body></html>'''
 (ROOT/'index.html').write_text(page.replace('__CARDS__','\n'.join(cards)))

if __name__=='__main__':main()
