from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
from palette import compact
PACKAGE=Path(__file__).resolve().parents[1];ROOT=PACKAGE/'diagnostics/quantize-only-replay';PREVIOUS=PACKAGE.parent/'v01'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(p):
 im=Image.open(p);return {'file':str(p.relative_to(ROOT)),'sha256':sha(p),'dimensions':list(im.size),'mode':im.mode}
def main():
 for name in ['native','previews','comparisons','evidence']:(ROOT/name).mkdir(parents=True,exist_ok=True)
 assets=[];reports={};bg=Image.open(PREVIOUS/'native/CH4-B2-03-v01.png').convert('RGBA');sheet=Image.new('RGB',(1164,648),'#23382f');draw=ImageDraw.Draw(sheet)
 for i,id_ in enumerate(['CH4-B2-01','CH4-B2-02']):
  source=PREVIOUS/f'native/{id_}-v01.png';im=Image.open(source).convert('RGBA');out,report=compact(im);reports[id_]=report;p=ROOT/f'native/{id_}-palette-v02.png';out.save(p);four=ROOT/f'previews/{id_}-palette-v02-4x.png';out.resize((2256,1112),Image.Resampling.NEAREST).save(four)
  comp=Image.alpha_composite(bg,out);comp.save(ROOT/f'previews/{id_}-composite.png');comp.resize((2256,1112),Image.Resampling.NEAREST).save(ROOT/f'previews/{id_}-composite-4x.png')
  assets.append({'id':id_,'status':'UNSELECTED','selected':False,'native':rec(p),'preview4x':rec(four),'approvedSource':{'commit':'81cf3b5f022510737bdd2d4ba3703e0173d86772','file':str(source.relative_to(ROOT.parent)),'sha256':sha(source)},'method':'Requested native RGB palette treatment only; source-derived; alpha/silhouette/geometry exact'})
  for j,(label,art) in enumerate([('Approved v01 — preserved',im),('v02 palette candidate',out)]):
   x=j*582+9;y=i*324+9;draw.text((x,y),id_+' · '+label,font=ImageFont.load_default(size=14),fill='#f4e2c0');back=Image.alpha_composite(Image.new('RGBA',art.size,'#40574b'),art);sheet.paste(back.convert('RGB'),(x,y+28))
 sheet.save(ROOT/'comparisons/plumbers-v01-v02-native.png');sheet.resize((4656,2592),Image.Resampling.NEAREST).save(ROOT/'comparisons/plumbers-v01-v02-4x.png')
 (ROOT/'evidence/palette-treatment.json').write_text(json.dumps(reports,indent=2)+'\n');(ROOT/'manifest.json').write_text(json.dumps({'title':'B2-01 plumbers — requested compact-palette alternatives v02','status':'UNSELECTED','ownerRequest':'Run the same Chapter1/2 NPC palette cleanser on both plumber portraits','approvedV01Modified':False,'backgroundAndFocusArtModified':False,'sourceDerived':True,'assets':assets,'frozenBackground':{'file':'../v01/native/CH4-B2-03-v01.png','sha256':sha(PREVIOUS/'native/CH4-B2-03-v01.png')}},indent=2)+'\n');print('Two palette alternatives prepared; all approved v01 bytes unchanged.')
if __name__=='__main__':main()
