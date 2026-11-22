"""Verify the requested room-only corrections and unchanged portrait silhouette."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
ROOT=Path(__file__).resolve().parent.parent

def run():
 report={'passed':True,'assets':[]}
 for id,stem in [('CH4-01','lobby'),('CH4-02','auctioneer-background')]:
  old=Image.open(ROOT.parent/'v04/native'/f'{id}-{stem}-v04.png').convert('RGB')
  new=Image.open(ROOT/'native'/f'{id}-{stem}-v05.png').convert('RGB')
  allowed=Image.new('1',old.size,0);d=ImageDraw.Draw(allowed)
  if id=='CH4-01':
   d.polygon([(172,153),(196,153),(202,179),(201,205),(153,205),(150,181)],fill=1)
   # Includes the old removed plaster chip at native column 245.
   for r in [(90,77,133,143),(138,76,153,97),(208,76,245,145),(278,76,304,145)]:d.rectangle(r,fill=1)
  else:
   for r in [(114,134,330,234),(465,64,553,213)]:d.rectangle(r,fill=1)
  op,np,mp=old.load(),new.load(),allowed.load();changed=[];outside=[]
  delta=Image.new('RGB',old.size,'#172024');dp=delta.load()
  for y in range(old.height):
   for x in range(old.width):
    if op[x,y]!=np[x,y]:
     changed.append([x,y]);dp[x,y]=(232,190,115)
     if not mp[x,y]:outside.append([x,y])
  assert not outside,(id,'outside requested correction mask',outside[:10])
  maskFile=f'evidence/{id}-allowed-correction-mask.png';deltaFile=f'evidence/{id}-changed-pixels.png'
  allowed.save(ROOT/maskFile);delta.save(ROOT/deltaFile)
  protected=[]
  if id=='CH4-01':
   for name,r in [('duct and ceiling',(0,0,249,77)),('paired restroom doors',(149,88,228,150)),('podium',(0,115,64,174))]:
    same=old.crop(r).tobytes()==new.crop(r).tobytes();assert same,name;protected.append({'region':name,'unchanged':same})
  else:
   for name,r in [('curtain',(0,0,309,130)),('duct and its attachments',(268,0,564,54)),('door and wood',(0,130,114,278))]:
    same=old.crop(r).tobytes()==new.crop(r).tobytes();assert same,name;protected.append({'region':name,'unchanged':same})
   # The fixture is repainted identically after the corrected wall illumination.
   fixture=Image.new('1',old.size,0);f=ImageDraw.Draw(fixture)
   f.polygon([(480,80),(518,80),(513,129),(486,129)],fill=1)
   f.ellipse((480,76,518,84),fill=1);f.ellipse((495,71,504,77),fill=1)
   for r in [(495,116,505,152),(489,130,511,133),(493,134,507,136),(496,153,504,155)]:f.rectangle(r,fill=1)
   fp=fixture.load();same=all(op[x,y]==np[x,y] for y in range(old.height) for x in range(old.width) if fp[x,y]);assert same,'lamp fixture changed';protected.append({'region':'lamp fixture silhouette and construction','unchanged':same})
  report['assets'].append({'id':id,'changedPixels':len(changed),'outsideAllowedMask':0,'allowedMask':maskFile,'deltaImage':deltaFile,'protected':protected})
 oldfg=Image.open(ROOT.parent/'v04/native/CH4-03-auctioneer-showman-v04.png')
 newfg=Image.open(ROOT/'native/CH4-03-auctioneer-showman-v05.png')
 same=oldfg.getchannel('A').tobytes()==newfg.getchannel('A').tobytes();assert same
 report['portraitSilhouette']={'matchesV04Exactly':same,'note':'Frontal composition and opaque silhouette retained; actual skin/hair/costume painting is revised.'}
 (ROOT/'evidence/targeted-change-qa.json').write_text(json.dumps(report,indent=2)+'\n')
 return report

if __name__=='__main__':print(json.dumps(run(),indent=2))
