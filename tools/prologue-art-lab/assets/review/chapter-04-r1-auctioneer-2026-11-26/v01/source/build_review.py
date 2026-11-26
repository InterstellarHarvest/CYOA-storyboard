"""Read-only comparisons and explicit technical/artistic gate reports."""
from pathlib import Path
from PIL import Image, ImageDraw, __version__ as pillow_version
import hashlib, json, html, sys, subprocess
R=Path(__file__).resolve().parents[1]
REPO=next(p for p in R.parents if (p/'story/artwork.draft.json').exists())
BASE='2af6606c25ce252752c65aa5c68c87ff84f804ae'
SHA=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,data): (R/name).write_text(json.dumps(data,indent=2)+'\n')
def preview(path):
 im=Image.open(R/path); dest='previews/'+Path(path).stem+'-4x.png'
 im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(R/dest)
 assert Image.open(R/dest).tobytes()==im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).tobytes()
 return dest
def info(path):
 p=R/path; im=Image.open(p); a=im.convert('RGBA').getchannel('A')
 opaque={rgb[:3] for rgb in im.convert('RGBA').get_flattened_data() if rgb[3]==255}
 return {'file':path,'sha256':SHA(p),'dimensions':list(im.size),'mode':im.mode,'rgbaColours':len(set(im.convert('RGBA').get_flattened_data())),'opaqueRGBColours':len(opaque),'alphaValues':sorted(set(a.get_flattened_data())),'partialAlphaPixels':sum(0<v<255 for v in a.get_flattened_data())}
def replay():
 # Independent replay from the explicit paint tape, not rendered reference pixels.
 from PIL import ImageDraw
 tape=json.loads((R/'source/native-paint.json').read_text()); result=Image.new('RGBA',tuple(tape['size']))
 for i,layer in enumerate(tape['layers']):
  im=Image.new('RGBA',result.size); d=ImageDraw.Draw(im)
  for op in layer['commands']:
   if op[0]=='polygon':d.polygon([tuple(p) for p in op[2]],fill=tape['palette'][op[1]])
   elif op[0]=='line':d.line([tuple(p) for p in op[2]],fill=tape['palette'][op[1]],width=op[3])
   else:d.ellipse(op[2],fill=tape['palette'][op[1]])
  assert im.tobytes()==Image.open(R/'layers'/f'{i+1:02d}.png').tobytes()
  result.alpha_composite(im)
 assert result.tobytes()==Image.open(R/'native/CH4-03-R1-construction-study.png').tobytes()
 return {'passed':True,'source':'source/native-paint.json','blankCanvas':[564,278],'layersReplayed':len(tape['layers']),'explicitMarks':sum(len(l['commands'])for l in tape['layers']),'sourceRasterReadDuringReplay':False,'gradientOrResamplingDuringPainting':False,'pixelEquality':True}
def panel(paths,dest):
 ims=[Image.open(R/p).convert('RGBA') for p in paths]; out=Image.new('RGB',(sum(i.width for i in ims),max(i.height for i in ims)),(165,164,150)); x=0
 for im in ims:out.paste(im,(x,0),im);x+=im.width
 out.save(R/dest)
def main():
 refs=json.loads((R/'evidence/references.json').read_text())
 for rec in refs:
  data=subprocess.check_output(['git','show',rec['sourceCommit']+':'+rec['sourcePath']],cwd=REPO)
  assert data==(R/rec['file']).read_bytes();assert SHA(R/rec['file'])==rec['sha256']
 old='references/approved-ch403.png'; new='native/CH4-03-R1-construction-study.png'; bg=Image.open(R/'references/approved-auctioneer-background.png').convert('RGBA')
 for name,p in [('approved',old),('study',new)]:
  comp=bg.copy();comp.alpha_composite(Image.open(R/p).convert('RGBA'));comp.convert('RGB').save(R/'comparisons'/f'{name}-on-approved-background.png')
 panel([old,new],'comparisons/old-study-foreground.png')
 panel(['comparisons/approved-on-approved-background.png','comparisons/study-on-approved-background.png'],'comparisons/old-study-composites.png')
 for label,box in [('face',(270,35,350,123)),('hands',(255,188,365,269))]:
  ims=[Image.open(R/p).crop(box).convert('RGBA') for p in [old,new]]
  out=Image.new('RGBA',(ims[0].width*2,ims[0].height));out.paste(ims[0],(0,0));out.paste(ims[1],(ims[0].width,0));out.save(R/'comparisons'/f'{label}-old-study.png')
 imagepaths=[old,new]+[str(p.relative_to(R))for p in sorted((R/'comparisons').glob('*.png'))]+[r['file']for r in refs if r['file']!=old]
 previews={p:preview(p)for p in imagepaths}
 dump('evidence/replay.json',replay())
 measured=[info(p)for p in [old,new]]
 assert measured[1]['dimensions']==[564,278] and measured[1]['alphaValues']==[0,255]
 dump('evidence/technical-qa.json',{'contractChecksPassed':True,'artisticGatePassed':False,'result':'HELD — method validation study, not a selection-ready replacement','paletteTarget':'Approximately 60–70 deliberate colours; 60 entries designed, 54 visible after opaque layer coverage. No colour padding.','paletteTargetReached':False,'nearestNeighbor4xExact':True,'immutableReferenceCopiesVerified':len(refs),'paintTapeReplayPassed':True,'python':sys.version,'pillow':pillow_version,'assets':measured})
 dump('manifest.json',{'assetId':'CH4-03-R1','status':'UNSELECTED / ARTISTIC GATE FAILED / DO NOT REGISTER','approvedOriginalRemainsSelected':True,'canonicalProductionKey':'hotel_auctioneer:showman (reference only; no registration changes)','newRasterAuthorship':'Independently constructed from blank native canvas using explicit native brush marks; design and pose referenced from approved artwork. No source pixels sampled or resized into the study.','newImageGeneration':False,'generationPrompt':'No new image generation; original source prompt and receipt preserved. See prompts/native-illustration-brief.md.','paintSource':'source/native-paint.json','editableProject':'source/CH4-03-R1-native.ora','baseCommit':BASE,'draftPR32ReadOnlySource':'f320e63934c13e27fd13b9482d0cfba58911362d','approvalStatusChanged':False,'images':measured,'references':'evidence/references.json','artisticAssessment':'ARTISTIC-GATE.md','sourceOriginal':info('originals/approved-style-detailed-original.png')})
 def fig(title,p,caption=''):
  w,h=Image.open(R/p).size
  return f'<section class="figure"><h3>{html.escape(title)}</h3><p>{html.escape(caption)}</p><p><button data-scale="1">Native 1×</button> <button data-scale="4">Exact 4×</button> <a href="{p}">PNG</a></p><div class="viewport"><img src="{p}" data-one="{p}" data-four="{previews[p]}" data-w="{w}" data-h="{h}" width="{w}" height="{h}" alt="{html.escape(title)}"></div></section>'
 parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>CH4-03 R1 — artistic gate held</title><style>body{background:#242923;color:#f1ead7;font:16px system-ui;margin:24px}a{color:#f6d696}h1{font-size:27px}.notice{background:#503a2f;border-left:5px solid #e5bb69;padding:18px;max-width:1000px}article{margin:36px 0}section.figure{border-top:1px solid #6c7163;padding:12px 0}button{background:#e6d8b8;color:#20251f;border:0;padding:8px 16px;cursor:pointer}.viewport{overflow:auto;background:#a5a496;max-width:100%;padding:8px}img{image-rendering:pixelated;image-rendering:crisp-edges;max-width:none;display:block}p{max-width:1050px;line-height:1.5}code{word-break:break-word}</style><h1>CH4-03 R1 — native construction study</h1><p class="notice"><b>UNSELECTED. Artistic gate held.</b> This study meets the canvas and binary-transparency contract, but loses the approved portrait’s likeness, expression and material modeling. It is evidence of the authoring limitation, not a proposed selection-ready replacement. The approved portrait remains untouched.</p><p><a href="ARTISTIC-GATE.md">Artistic assessment and illustrator handoff</a> · <a href="manifest.json">Manifest</a> · <a href="evidence/technical-qa.json">Technical QA</a> · <a href="source/CH4-03-R1-native.ora">Editable OpenRaster project</a> · <a href="source/native-paint.json">Native paint tape</a> · <a href="originals/approved-style-detailed-original.png">Preserved 1788×880 original</a></p><article id="portrait"><h2>Approved original and new study</h2>']
 parts += [fig('Approved CH4-03 — unchanged',old,'The source-derived approved original; partial figure opacity is preserved here.'),fig('Native construction study — visual gate failed',new,'Blank-canvas native construction. 54 visible opaque colours; binary alpha. Do not select.')]
 parts += ['</article><article id="comparison"><h2>Direct comparisons — approved left / study right</h2>']
 for name in ['old-study-foreground','old-study-composites','face-old-study','hands-old-study']:
  parts.append(fig(name.replace('-',' ').title(),'comparisons/'+name+'.png','Exact native pixels, with no interpolation. Side-by-side images use equal native grids.'))
 parts += ['</article><article id="composites"><h2>Composites on unchanged CH4-02</h2>']
 for n in ['approved','study']:parts.append(fig(n.title()+' on approved background','comparisons/'+n+'-on-approved-background.png'))
 parts += ['</article><article id="benchmarks"><h2>Exact approved references</h2><p>Chapter 2 conductor and groundskeeper establish cluster and palette handling; they are mechanical characters, so the human receptionist, Pavilion portraits and later auctioneers supply the facial and costume benchmarks. Bureaucratic is archived following consolidation and is shown only as an approved historical style reference.</p>']
 for rec in refs:
  if rec['file']!=old:parts.append(fig(Path(rec['file']).stem.replace('-',' ').title(),rec['file']))
 parts += ['</article><script>document.querySelectorAll("button[data-scale]").forEach(b=>b.addEventListener("click",()=>{const i=b.closest("section").querySelector("img"),s=Number(b.dataset.scale);i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;i.src=s===4?i.dataset.four:i.dataset.one;}));</script></html>']
 (R/'index.html').write_text('\n'.join(parts)+'\n')
 print(json.dumps({'figures':len(imagepaths),'referenceCopiesVerified':len(refs),'artisticGatePassed':False}))
if __name__=='__main__':main()
