"""Retain untouched built-in output and an explicitly derived working donor."""
from pathlib import Path
from PIL import Image
import argparse,json,hashlib,shutil
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=argparse.ArgumentParser();p.add_argument('--id',required=True);p.add_argument('--source',required=True);a=p.parse_args()
cfg=json.loads((ROOT/'sources/generation-config.json').read_text());c=next(c for c in cfg['sources'] if c['candidateId']==a.id)
source=Path(a.source);dest=ROOT/'generation-source'/source.name
if dest.exists():assert dest.read_bytes()==source.read_bytes()
else:shutil.copyfile(source,dest)
raw=Image.open(dest);target=tuple(c['requestedDimensions']);native=raw.convert('RGBA' if c['kind']=='foreground' else 'RGB')
if native.size!=target:native=native.resize(target,Image.Resampling.NEAREST)
(ROOT/'donors').mkdir(exist_ok=True);out=ROOT/f'donors/{a.id}-native-donor.png';native.save(out)
native.resize((target[0]*4,target[1]*4),Image.Resampling.NEAREST).save(ROOT/f'previews/{a.id}-donor-4x.png')
prompt=ROOT/c['submittedPrompt']
r={'candidateId':a.id,'tool':'built-in image_gen.imagegen','originalFilename':source.name,'originalSourcePath':str(source),'source':str(dest.relative_to(ROOT)),'sourceSha256':sha(dest),'actualSourceDimensions':list(raw.size),'actualSourceMode':raw.mode,'actualAlphaExtrema':list(raw.convert('RGBA').getchannel('A').getextrema()),'requestedDimensions':list(target),'workingDonor':str(out.relative_to(ROOT)),'workingDonorSha256':sha(out),'workingDonorDimensions':list(native.size),'workingDonorAlphaValues':sorted(set(native.convert('RGBA').getchannel('A').getdata())),'submittedPrompt':c['submittedPrompt'],'submittedPromptSha256':sha(prompt),'transparentBackgroundRequested':c['transparent_background'],'references':[{'file':f,'sha256':sha(ROOT/f)} for f in c['references']],'generationCalls':1,'status':'source donor only; not an approved or selected artwork','derivation':'Untouched original retained. '+('Source-size nearest-neighbor transfer to target grid; no sharpening, global quantization, dithering or alpha threshold.' if raw.size!=target else 'Source already has requested dimensions; no size transform.'),'originalNativeGridAuthorship':'UNPROVEN; source dimensions and target export alone do not demonstrate original pixel-grid authorship.'}
rp=ROOT/'sources/generation-records.json';records=json.loads(rp.read_text()) if rp.exists() else [];records=[x for x in records if x['candidateId']!=a.id];records.append(r);rp.write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps({k:r[k] for k in ['candidateId','source','actualSourceDimensions','workingDonor','sourceSha256']},indent=2))
