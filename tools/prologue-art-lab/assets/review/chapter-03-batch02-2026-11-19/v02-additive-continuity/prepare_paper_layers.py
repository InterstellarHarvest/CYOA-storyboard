"""Reproduce the recorded transparent paper transfers; no alpha thresholding."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for r in json.loads((ROOT/'sources/paper-layer-generation-records.json').read_text()):
 source=ROOT/r['source'];assert sha(source)==r['sourceSha256']
 im=Image.open(source).convert('RGBA').resize((314,206),Image.Resampling.NEAREST)
 if r['layerId']=='B02-paper-layer':
  part=im.crop((50,102,283,206)).resize((233,64),Image.Resampling.NEAREST)
  im=Image.new('RGBA',(314,206));im.alpha_composite(part,(63,142))
 d=ImageDraw.Draw(im)
 for box in [(201,96,234,122),(202,122,245,142),(69,38,180,62),(202,67,231,92)]:d.rectangle((box[0],box[1],box[2]-1,box[3]-1),fill=(0,0,0,0))
 dest=ROOT/r['workingLayer'];im.save(dest);assert sha(dest)==r['workingLayerSha256']
print('Two transparent addition layers reproduced with their recorded hashes')
