"""Assessment only: exact approved background/foreground alpha compositing."""
from pathlib import Path
from PIL import Image
import hashlib,json
A=Path(__file__).resolve().parents[1]
def main():
 bg=Image.open(A/'references/approved-background.png').convert('RGBA');fg=Image.open(A/'references/approved-porter.png').convert('RGBA')
 out=bg.copy();out.alpha_composite(fg);out.convert('RGB').save(A/'comparisons/approved-porter-over-approved-background.png')
 pair=Image.new('RGB',(1128,278));pair.paste(bg,(0,0));pair.paste(out,(564,0));pair.save(A/'comparisons/background-and-porter.png')
 edge=fg.getchannel('A').crop((529,0,564,278));assert not edge.getbbox()
 files=['references/approved-background.png','references/approved-porter.png','comparisons/approved-porter-over-approved-background.png','comparisons/background-and-porter.png']
 for p in files:
  im=Image.open(A/p);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(A/'previews'/(Path(p).stem+'-4x.png'))
 (A/'manifest.json').write_text(json.dumps({'status':'ASSESSMENT ONLY — NOT A SELECTABLE IMAGE','newArtworkGenerated':False,'artworkModified':False,'method':'Approved foreground at native origin (0,0), alpha-over exact approved background; original alpha retained; previews exact nearest-neighbour 4x.','portraitAlphaBounds':fg.getchannel('A').getbbox(),'examinedEdgeBounds':[529,0,564,278],'foregroundOcclusionPixelsInEdge':0,'judgment':'Edge is visible, not hidden, but peripheral/inconspicuous in the full native portrait composition. No identifiable floor toilet or lifted enclosure is shown there. Recommend reuse.','ownerDecision':'Nate/PMO explicitly permits approved CH4-B2-03 reuse for hotel_stall_porter_protest. No additional image required.','references':'evidence/references.json','images':[{'file':p,'sha256':hashlib.sha256((A/p).read_bytes()).hexdigest()}for p in files]},indent=2)+'\n')
if __name__=='__main__':main()
