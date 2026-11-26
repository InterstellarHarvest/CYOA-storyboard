"""Non-destructive environment evidence; never creates replacement artwork."""
from pathlib import Path
from PIL import Image
import json, hashlib, html, subprocess
ROOT=Path(__file__).resolve().parent
REPO=next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists())
BASE='2af6606c25ce252752c65aa5c68c87ff84f804ae'
SHA=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
CROPS={'CH4-01':(0,70,108,158),'CH4-04':(0,89,139,190),'CH4-05':(30,107,238,206),'CH4-B2-03':(0,144,251,278),'CH4-B2-11':(187,63,438,256)}
BENCH={'ch2-bureau':'assets/selected/art/scenes/biology_park/conveniences_bureau.png','ch2-control-tower':'assets/selected/art/scenes/biology_park/control_tower.png','ch4-staff-lavatory':'assets/selected/pending-integration/scenes/grand_bellevue/staff_lavatory.png'}
NOTES={
 'CH4-01':'Retain. Optional targeted carpet wear, damage edges and podium/flower accents. Preserve layout, duct lighting, all objects and small NPC.',
 'CH4-04':'Localized basin/faucet planes, worker colour clusters and contact shadows. Preserve both plumbers, fixtures, stalls and exposed toilet.',
 'CH4-05':'Retain. Optional floor-mark and floral/cloth grouping. Preserve tables, chair-carrying workmen, clipboards, all figures and architecture.',
 'CH4-B2-03':'Highest priority: near basin/tap material pilot, then other surfaces only if volume survives. No flat sink reconstruction or global quantization.',
 'CH4-B2-11':'Second material pilot: lift threshold and floor. Preserve all loading-dock objects, light direction and geometry.'}
def main():
 records=json.loads((ROOT/'evidence/approved-inputs.json').read_text()); benchmarks=[]
 for name,path in BENCH.items():
  data=subprocess.check_output(['git','show',BASE+':'+path],cwd=REPO)
  p=ROOT/'references'/f'{name}.png';assert p.read_bytes()==data
  benchmarks.append({'id':name,'file':str(p.relative_to(ROOT)),'sourceCommit':BASE,'sourcePath':path,'sha256':SHA(p),'status':'APPROVED / BENCHMARK / UNCHANGED'})
 for rec in records:
  assert subprocess.check_output(['git','show',BASE+':'+rec['sourcePath']],cwd=REPO)==(ROOT/rec['file']).read_bytes()
  assert SHA(ROOT/rec['file'])==rec['sha256']
 figures=[]
 def export(title,path,caption):
  im=Image.open(ROOT/path); four='previews/'+Path(path).stem+'-4x.png'
  im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/four)
  assert Image.open(ROOT/four).tobytes()==im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).tobytes()
  figures.append({'title':title,'path':path,'four':four,'w':im.width,'h':im.height,'caption':caption})
 for rec in records:
  ident=rec['id'];im=Image.open(ROOT/rec['file']);rec['dimensions']=list(im.size);rec['mode']=im.mode;rec['colours']=len(im.getcolors(im.width*im.height));rec['proposedAction']=NOTES[ident];rec['crop']=CROPS[ident]
  export(ident+' — unchanged approved image',rec['file'],NOTES[ident])
  # All three remain at their own native pixel scale. No resizing to equal widths.
  refs=[im]+[Image.open(ROOT/b['file'])for b in benchmarks[:2]]
  sheet=Image.new('RGB',(sum(i.width for i in refs),max(i.height for i in refs)),(40,45,39));x=0
  for i in refs:sheet.paste(i,(x,0));x+=i.width
  p='comparisons/'+ident+'-chapter2.png';sheet.save(ROOT/p)
  export(ident+' / Chapter 2 Bureau / Control Tower',p,'Left to right, same pixel scale. Different canvas contracts are preserved; no reference is shrunk.')
  p='comparisons/'+ident+'-material-crop.png';im.crop(CROPS[ident]).save(ROOT/p)
  export(ident+' — native material crop',p,'Unmodified crop for inspecting cluster handling. Coordinates are recorded in the manifest.')
 for b in benchmarks:export(b['id']+' — approved benchmark',b['file'],'Exact canonical PNG. Reference only; no replacement proposed.')
 (ROOT/'manifest.json').write_text(json.dumps({'type':'VISUAL ASSESSMENT ONLY','newEnvironmentArtworkCreated':False,'sourceCommit':BASE,'selectionChanges':False,'recommendation':'Prioritize background material pilots; retain main compositions and consider only localized refinements. Await Nate direction.','approvedAssets':records,'benchmarks':benchmarks,'allReferencesExactBytes':True,'all4xExactNearestNeighbor':True,'report':'ASSESSMENT.md','figures':figures},indent=2)+'\n')
 h=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Chapter 4 R1 — five-environment assessment</title><style>body{background:#242923;color:#f1ead7;font:16px system-ui;margin:24px}a{color:#f6d696}h1{font-size:27px}.notice{background:#344335;padding:18px;max-width:1000px}section.figure{border-top:1px solid #6c7163;padding:12px 0}button{background:#e6d8b8;color:#20251f;border:0;padding:8px 16px;cursor:pointer}.viewport{overflow:auto;background:#a5a496;max-width:100%;padding:8px}img{image-rendering:pixelated;image-rendering:crisp-edges;max-width:none;display:block}p{max-width:1050px;line-height:1.5}</style><h1>Chapter 4 R1 — five-environment assessment</h1><p class="notice"><b>Assessment only. No environment artwork was redrawn.</b> All approved PNGs remain selected and unchanged. The two close backgrounds merit material-cluster pilots; the main scenes remain readable and need only optional localized work. No new objects or room designs are proposed.</p><p><a href="ASSESSMENT.md">Full five-image assessment and recommended order</a> · <a href="manifest.json">Hashes, crop coordinates and findings</a></p><article id="assessment"><h2>Five approved images and Chapter 2 comparisons</h2>']
 for i,f in enumerate(figures):
  if i==15:h.append('</article><article id="benchmarks"><h2>Approved Chapter 2 and Chapter 4 benchmarks</h2>')
  h.append(f'<section class="figure"><h3>{html.escape(f["title"])}</h3><p>{html.escape(f["caption"])}</p><p><button data-scale="1">Native 1×</button> <button data-scale="4">Exact 4×</button> <a href="{f["path"]}">PNG</a></p><div class="viewport"><img src="{f["path"]}" data-one="{f["path"]}" data-four="{f["four"]}" data-w="{f["w"]}" data-h="{f["h"]}" width="{f["w"]}" height="{f["h"]}" alt="{html.escape(f["title"])}"></div></section>')
 h.append('</article><script>document.querySelectorAll("button[data-scale]").forEach(b=>b.addEventListener("click",()=>{const i=b.closest("section").querySelector("img"),s=Number(b.dataset.scale);i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;i.src=s===4?i.dataset.four:i.dataset.one;}));</script></html>')
 (ROOT/'index.html').write_text('\n'.join(h)+'\n');print(json.dumps({'approvedPNGsUnchanged':5,'benchmarksUnchanged':3,'figures':len(figures),'newArtworkCreated':False}))
if __name__=='__main__':main()
