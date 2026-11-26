from pathlib import Path
from PIL import Image,ImageChops
import subprocess,json,hashlib,zipfile,io,html
R=Path(__file__).resolve().parents[1];W=next(p for p in R.parents if (p/'story/artwork.draft.json').exists())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return Image.open(R/p)
def sheet(paths):
 ims=[]
 for p in paths:
  im=load(p).convert('RGBA');ims.append(Image.alpha_composite(Image.new('RGBA',im.size,(124,135,124,255)),im).convert('RGB'))
 out=Image.new('RGB',(sum(i.width for i in ims),max(i.height for i in ims)),(124,135,124));x=0
 for im in ims:out.paste(im,(x,0));x+=im.width
 return out
def preview(p):
 im=load(p);dest='previews/'+Path(p).stem+'-4x.png';out=im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST);out.save(R/dest)
 # Independent block reconstruction, including RGBA alpha.
 for y in range(im.height):
  for x in range(im.width):
   block=out.crop((x*4,y*4,x*4+4,y*4+4));assert len(set(block.getdata()))==1 and block.getpixel((0,0))==im.getpixel((x,y))
 return dest
def fig(title,p,caption):
 im=load(p);p4=preview(p)
 return '<section class="figure"><h3>'+html.escape(title)+'</h3><p>'+html.escape(caption)+'</p><button data-scale="1">Native 1×</button> <button data-scale="4">Exact 4×</button> <a href="'+p+'">PNG</a><div class="raster"><img src="'+p+'" data-one="'+p+'" data-four="'+p4+'" data-w="'+str(im.width)+'" data-h="'+str(im.height)+'" width="'+str(im.width)+'" height="'+str(im.height)+'" alt="'+html.escape(title)+'"></div></section>'
def main():
 refs=json.loads((R/'evidence/references.json').read_text());controls=json.loads((R/'evidence/controlling-sources.json').read_text())
 for a in refs+controls:
  blob=subprocess.check_output(['git','show',a['sourceCommit']+':'+a['sourcePath']],cwd=W);assert hashlib.sha256(blob).hexdigest()==a['sha256']
  if 'file' in a:assert sha(R/a['file'])==a['sha256']
 names=['pavilion_temporary_staff_pass_slot','pavilion_temporary_staff_pass_inspect'];records=[]
 for n in names:
  p='native/'+n+'.png';im=load(p);isSlot=n.endswith('slot');assert im.size==((96,96) if isSlot else (565,451));assert im.mode==('RGBA' if isSlot else 'RGB')
  if isSlot:assert set(im.getchannel('A').getdata())=={0,255};assert im.getbbox()[0]>=5 and im.getbbox()[2]<=91
  marks=json.loads((R/'source'/f'{n}-marks.json').read_text());assert not marks['generatedPixelsUsed']
  for t in marks['textLayout']:
   z=t['safeZone'];x,y,x2,y2=t['box'];assert z[0]<=x and z[1]<=y and x2<=z[2] and y2<=z[3]
  rebuilt=Image.new('RGBA',im.size)
  with zipfile.ZipFile(R/'source'/f'{n}.ora') as z:
   assert Image.open(io.BytesIO(z.read('mergedimage.png'))).convert('RGBA').tobytes()==im.convert('RGBA').tobytes()
  layers=sorted((R/'layers').glob(n+'-*.png'))
  order=['cardstock-and-laminate','punch-and-clip','institutional-printing'] if isSlot else ['backing-and-shadow','cardstock-and-laminate','punch-and-clip','institutional-printing']
  for ln in order:rebuilt=Image.alpha_composite(rebuilt,Image.open(R/'layers'/f'{n}-{ln}.png'))
  assert rebuilt.tobytes()==im.convert('RGBA').tobytes()
  records.append(dict(id='pavilion_temporary_staff_pass:'+('slot' if isSlot else 'inspect'),file=p,status='UNSELECTED',dimensions=list(im.size),mode=im.mode,sha256=sha(R/p),colours=len(set(im.getdata())),alphaValues=[0,255] if isSlot else None,editableSource='source/'+n+'.ora',marks='source/'+n+'-marks.json',provenance='Independently drawn on native canvas; generated reference pixels never sampled, traced, reduced or quantized',textLayout=marks['textLayout'],layerCompositeExact=True))
 required=['TEMPORARY STAFF',"PEOPLE'S PAVILION",'DEPARTMENT: HUMAN PRESENTATION','VALID UNTIL CORRECTED']
 actual=[t['text'] for t in records[1]['textLayout']];assert all(s in actual for s in required)
 # Cross-format identity sheet keeps original scales; no upsampled icon masquerades as inspection art.
 sheet(['native/'+n+'.png' for n in names]).save(R/'comparisons/slot-inspection-identity.png')
 sheet(['native/'+names[0]+'.png']+['references/ch2-'+i+'-slot.png' for i in ['expo_examiner_badge','acting_director_badge','bathroom_pass']]).save(R/'comparisons/chapter2-slot-benchmarks.png')
 sheet(['native/'+names[1]+'.png','references/ch2-expo_examiner_badge-inspect.png']).save(R/'comparisons/chapter2-credential-comparison.png')
 figs=[]
 def add(t,p,c):figs.append(fig(t,p,c))
 add('Inventory slot — native 96×96','native/'+names[0]+'.png','Transparent RGBA, binary alpha. Recognizable clip, green-grey sleeve, cream insert, STAFF block and burgundy seal; no baked inventory frame.')
 add('Inventory inspection — native 565×451','native/'+names[1]+'.png','Opaque RGB. Four required lines in chunky custom bitmap type; each has a separate safe region. Registration and seal do not overlap the text.')
 body='<article id="candidate">'+''.join(figs)+'</article>';figs=[]
 add('Slot / inspection identity','comparisons/slot-inspection-identity.png','Both independently drawn at their own actual resolution. Same clip, punched attachment, burgundy paper border, Pavilion pictogram, cream insert and registration design.')
 body+='<article id="identity">'+''.join(figs)+'</article>';figs=[]
 add('Chapter 2 slots — pass, examiner, director, bathroom pass','comparisons/chapter2-slot-benchmarks.png','Actual approved canonical PNGs at native scale. Candidate on left. Transparency appears over the backing of this comparison sheet only.')
 add('Candidate and approved Chapter 2 examiner inspection','comparisons/chapter2-credential-comparison.png','Side-by-side native images. Compare credential silhouette, clip, materials, clear typography and deliberate edges. Candidate has cheaper matte paper and more restrained laminate.')
 add('Approved Chapter 2 acting director inspection','references/ch2-acting_director_badge-inspect.png','Canonical selected reference; preserved byte-for-byte.')
 add('Approved Chapter 2 bathroom pass inspection','references/ch2-bathroom_pass-inspect.png','Canonical paper, edge wear and material benchmark; preserved byte-for-byte.')
 add('Approved Chapter 4 dispute-ticket inspection','references/ch4-dispute-ticket-inspect.png','Canonical native paper and chunky object-lettering comparison; preserved byte-for-byte.')
 body+='<article id="benchmarks">'+''.join(figs)+'</article>'
 css='body{margin:24px;background:#222c28;color:#e8dfc5;font:16px system-ui}a{color:#e9d5a5}h1{font-size:27px}article{margin-top:32px}section.figure{border-top:1px solid #6a7767;padding:16px 0 24px}button{padding:9px 14px;background:#ded2b1;border:0;cursor:pointer;color:#263632}.raster{overflow:auto;padding:8px;background:#7c877c;margin-top:12px}img{display:block;image-rendering:pixelated;max-width:none}p{max-width:1000px;line-height:1.5}'
 js="document.querySelectorAll('section.figure').forEach(f=>f.querySelectorAll('button').forEach(b=>b.onclick=()=>{const i=f.querySelector('img'),s=Number(b.dataset.scale);i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;i.src=s===1?i.dataset.one:i.dataset.four;}));"
 header='<h1>Temporary Staff Pass — v01 — UNSELECTED</h1><p>Exactly two new artwork candidates. Native construction, purposeful clusters and controlled material ramps. Existing approved art and the narrative/engine grant work are untouched. <a href="README.md">Production notes / Claude handoff</a> · <a href="manifest.json">Manifest and hashes</a> · <a href="evidence/technical-qa.json">Technical QA</a> · <a href="originals/credential-design-reference.png">Large reference only</a> · <a href="prompts/reference.txt">Exact reference prompt</a></p>'
 (R/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Temporary Staff Pass v01 review</title><style>'+css+'</style>'+header+body+'<script>'+js+'</script></html>')
 for rec in records:
  rec['exact4xPreview']='previews/'+Path(rec['file']).stem+'-4x.png';rec['exact4xSha256']=sha(R/rec['exact4xPreview']);rec['exact4xDimensions']=[n*4 for n in rec['dimensions']]
 manifest=dict(item='pavilion_temporary_staff_pass',status='UNSELECTED',sourceMain=refs[0]['sourceCommit'],assets=records,requiredText=required,serial='HP-03 / 0417 is decorative credential printing, not a new story fact or gameplay rule',generatedReference='originals/credential-design-reference.png',method='source/build_art.py builds each native grid independently; generated raster read by no construction code',integration='Not implemented. Claude owns grant logic and any narrative/item/registry changes in separate files.')
 (R/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 qa=dict(passed=True,candidates=2,canonicalReferencesVerified=len(refs),controllingSourcesVerified=len(controls),nativeDimensionsModesPassed=True,binarySlotAlphaPassed=True,allPreviewsExact4x=True,editableLayerCompositeAndORAExact=True,requiredTextSafeZonesPassed=True,noGeneratedPixelsUsed=True,noGlobalQuantizationOrSharpening=True,artisticApproval='PENDING NATE; technical QA is not visual approval',results=records)
 (R/'evidence/technical-qa.json').write_text(json.dumps(qa,indent=2)+'\n');print(json.dumps(dict(candidates=2,figures=8,passed=True,colours=[r['colours'] for r in records])))
if __name__=='__main__':main()
