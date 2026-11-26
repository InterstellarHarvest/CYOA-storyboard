"""Exact native CRT-content edit, using approved native source and bitmap glyphs.

No regeneration, resizing, source reduction or resampling of production images.
Both states share text/row geometry. Original source-derived provenance remains.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageFont
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
FONT=json.loads((ROOT/'source/bitmap-glyphs.json').read_text())
SIZE=(565,451);CONTENT=(289,106,421,163);TEXT_BOX=(285,105,425,139);ICON_ZONE=(341,145,369,163);CROP=(264,84,440,183)
BG='#182e2a';LAYOUT=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def text(d,lines,ink):
 x0,y0,x1,y1=TEXT_BOX;scale=2;gap=4;height=28+gap;y=y0+(y1-y0-height)//2
 boxes=[]
 for line in lines:
  w=(len(line)*6-1)*scale;x=x0+(x1-x0-w)//2;boxes.append([x,y,x+w,y+14]);start=x
  for ch in line:
   for j,row in enumerate(FONT[ch]):
    for i,b in enumerate(row):
     if b=='1':d.rectangle((x+i*2,y+j*2,x+i*2+1,y+j*2+1),fill=ink)
   x+=12
  y+=18
 return boxes
def change_mask(a,b):
 d=ImageChops.difference(a,b);return ImageChops.lighter(ImageChops.lighter(d.getchannel('R'),d.getchannel('G')),d.getchannel('B')).point(lambda p:255 if p else 0)
def main():
 allowed=Image.new('L',SIZE);ImageDraw.Draw(allowed).rectangle(CONTENT,fill=255);allowed.save(ROOT/'masks/authorized-crt-content.png')
 artifacts=[];crops={}
 for state in ['locked','provisional']:
  source='references/approved-inspect-'+state+'-v01.png';before=Image.open(ROOT/source).convert('RGB')
  patch=Image.new('RGBA',SIZE);d=ImageDraw.Draw(patch);d.rectangle(CONTENT,fill=BG)
  lines=['LOCKED','BRIDE ONLY']if state=='locked'else['PROVISIONAL','AUTHORIZED'];ink='#b2d3bd'if state=='locked'else'#bad6a0'
  boxes=text(d,lines,ink)
  icon=Image.new('RGBA',SIZE);g=ImageDraw.Draw(icon)
  if state=='locked':
   g.arc((351,147,359,158),180,360,fill=ink,width=2)
   g.line([(351,151),(351,155)],fill=ink,width=2);g.line([(358,151),(358,155)],fill=ink,width=2)
  else:
   g.arc((353,146,363,156),180,350,fill=ink,width=2)
   g.line([(353,150),(353,155)],fill=ink,width=2)
  g.rectangle((349,154,361,162),fill=ink);g.rectangle((354,157,355,160),fill=BG)
  patch=Image.alpha_composite(patch,icon);patch.save(ROOT/f'layers/{state}-crt-content.png');icon.save(ROOT/f'layers/{state}-icon-only.png')
  result=Image.alpha_composite(before.convert('RGBA'),patch).convert('RGB');f=f'native/CH4-NEW-07-inspect-{state}-v03.png';result.save(ROOT/f)
  result.resize((2260,1804),Image.Resampling.NEAREST).save(ROOT/f'previews/CH4-NEW-07-inspect-{state}-v03-4x.png')
  actual=change_mask(before,result);actual.save(ROOT/f'masks/{state}-actual-changes.png')
  ib=icon.getchannel('A').getbbox();textbottom=max(b[3]for b in boxes);gap=ib[1]-textbottom
  LAYOUT.append({'state':state,'textBox':list(TEXT_BOX),'textLineInkBounds':boxes,'textHorizontalCenter':355,'textNativeScale':2,'lineGap':4,'iconZone':list(ICON_ZONE),'iconInkBounds':list(ib),'iconBody':[349,154,361,162],'iconBodyCenterX':355,'clearRowsBelowText':gap,'oldTextFirstRowY':117,'newTextFirstRowY':boxes[0][1],'oldSecondLineLastRowY':150,'newSecondLineLastRowY':boxes[1][3]-1,'layoutSameAcrossStates':True})
  artifacts.append({'state':state,'file':f,'sha256':sha(ROOT/f),'dimensions':list(result.size),'mode':result.mode,'status':'UNSELECTED','ownerApproved':False,'source':source,'sourceSha256':sha(ROOT/source),'patch':f'layers/{state}-crt-content.png','patchSha256':sha(ROOT/f'layers/{state}-crt-content.png'),'actualChangeMask':f'masks/{state}-actual-changes.png','changedPixels':sum(v>0 for v in actual.get_flattened_data()),'outsideAuthorizedPixels':sum(v>0 for v in ImageChops.multiply(actual,ImageChops.invert(allowed)).get_flattened_data()),'sourceDerived':True,'newImageGeneration':False,'runtimeBinding':None})
  for label,im in [('before',before),('after',result)]:
   p=f'closeups/{state}-{label}-crt-native.png';crops[(state,label)]=p;crop=im.crop(CROP);crop.save(ROOT/p);crop.resize((crop.width*4,crop.height*4),Image.Resampling.NEAREST).save(ROOT/f'previews/{state}-{label}-crt-native-4x.png')
 for p in (ROOT/'references').glob('*.png'):
  im=Image.open(p);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/'previews'/(p.stem+'-4x.png'))
 font=ImageFont.load_default(size=13)
 def sheet(name,states):
  width=225;height=145;out=Image.new('RGB',(width*2+12,height*len(states)+12),'#263a32');d=ImageDraw.Draw(out)
  for row,state in enumerate(states):
   for col,label in enumerate(['before','after']):
    x=col*width+8;y=row*height+8;caption=('v01 APPROVED'if label=='before'else'v03 UNSELECTED')+' / '+state
    assert font.getlength(caption)<width-8
    d.text((x,y),caption,font=font,fill='#efe3bf');out.paste(Image.open(ROOT/crops[(state,label)]),(x+18,y+33))
  p=f'comparisons/{name}-native.png';out.save(ROOT/p);out.resize((out.width*4,out.height*4),Image.Resampling.NEAREST).save(ROOT/f'previews/{name}-native-4x.png')
 sheet('both-states-crt-before-after',['locked','provisional']);sheet('locked-crt-before-after',['locked']);sheet('provisional-crt-before-after',['provisional'])
 (ROOT/'evidence/layout.json').write_text(json.dumps(LAYOUT,indent=2)+'\n')
 manifest={'title':'B2-12 v03 INSPECT alternatives - separate lock icon row','branch':'art/ch4-b212-bridal-privacy-review-20261125','preservationBaseline':'a944f9aeff110ddc66301840c2d415f1ba9bc357','newArtworkStatus':'UNSELECTED','ownerApproved':False,'newAssets':artifacts,'unchangedApprovedReferences':json.loads((ROOT/'evidence/reference-provenance.json').read_text()),'sourceDerived':True,'whollyIndependentNativeAuthorship':False,'newImageGeneration':False,'method':'Existing editable native screen-content layer replaced with original bitmap glyphs and a dedicated lock-icon row. Text moves up11px. No other pixels change. Palette exact; no new colors or image resampling. Original source-derived illustration provenance retained.','sourceIllustrationCommit':'ce8cc78f7683c99d96399091ab92cc3ac52e4f05','approvedSquareSourceCommit':'1261658ed882bff7340405e91f5d44f4e5404012','authorizedEditBoxInclusive':list(CONTENT),'closeupCropBoxExclusive':list(CROP),'sharedLayout':'evidence/layout.json','productionRegistrationPerformed':False,'gameplayOrNarrativeChanged':False,'approvedV01OrV02Modified':False}
 (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps({'assets':artifacts,'layout':LAYOUT}))
if __name__=='__main__':main()
