"""Preserve untouched imagegen sources; explicitly label any native-size derivation."""
from pathlib import Path
from PIL import Image
import sys,json,hashlib,shutil
ROOT=Path(__file__).resolve().parent
ident,source_path=sys.argv[1:3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
brief=json.loads((ROOT/'sources/briefs.json').read_text())
item=next(i for i in brief['candidates'] if i['candidateId']==ident)
configs=[c for p in (ROOT/'sources').glob('*generation-config.json') for c in json.loads(p.read_text())]
config=next(c for c in configs if c['candidateId']==ident)
src=Path(source_path);dest=ROOT/'generation-source'/src.name
shutil.copyfile(src,dest)
original=Image.open(dest);target=tuple(item['dimensions'])
assert original.convert('RGBA').getchannel('A').getextrema()==(255,255)
out=original.convert('RGB');derived=out.size!=target
if derived:out=out.resize(target,Image.Resampling.NEAREST)
file=ROOT/f'candidates/{ident}-v01.png';out.save(file)
preview=None
if item['kind']=='scene':
 preview=f'previews/{ident}-v01-4x.png';out.resize((1256,824),Image.Resampling.NEAREST).save(ROOT/preview)
record={'candidateId':ident,'record':item['record'],'tool':'built-in image_gen.imagegen','generationCalls':1,'source':str(dest.relative_to(ROOT)),'originalSourceFilename':src.name,'originalToolPath':str(src),'sourceSha256':sha(dest),'actualSourceDimensions':list(original.size),'actualSourceMode':original.mode,'requestedDimensions':list(target),'exactRequestedSourceDimensionsPassed':not derived,'candidate':str(file.relative_to(ROOT)),'candidateSha256':sha(file),'workingDimensions':list(out.size),'derivedExport':derived,'derivation':'RGB export and nearest-neighbor reduction of this new source to requested logical dimensions; no sharpening, palette filtering, dithering, repainting or crop.' if derived else 'RGB export at the exact returned source dimensions, no resize.','preview4x':preview,'submittedPrompt':config['submittedPrompt'],'submittedPromptSha256':sha(ROOT/config['submittedPrompt']),'cataloguePrompt':item['prompt'],'cataloguePromptSha256':sha(ROOT/item['prompt']),'canonicalDirection':'prompts/canonical-direction.txt','canonicalDirectionSha256':sha(ROOT/'prompts/canonical-direction.txt'),'referencesInOrder':[{'file':p,'sha256':sha(ROOT/p)} for p in config['references']],'transparent_background':False,'originalNativeGridAuthorship':'UNPROVEN: retained source dimensions/derivation do not prove direct grid authorship.','status':'generated','selected':False,'approved':False,'assetPath':None}
p=ROOT/'sources/generation-records.json';records=json.loads(p.read_text()) if p.exists() else []
assert not any(r['candidateId']==ident for r in records),ident
records.append(record);records.sort(key=lambda r:next(i for i,b in enumerate(brief['candidates']) if b['candidateId']==r['candidateId']))
p.write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps({'candidateId':ident,'actualSourceDimensions':list(original.size),'workingDimensions':list(out.size),'derived':derived,'sha256':sha(file)},indent=2))
