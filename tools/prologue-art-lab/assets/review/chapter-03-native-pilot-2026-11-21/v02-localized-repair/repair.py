"""Six predeclared native-pixel edits to a byte-verified copy of approved art.
No generation, resampling to native size, sharpening, quantization or filtering.
All replacements are exact RGB samples from the same immutable original.
"""
from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib,csv
B=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 plan=json.loads((B/'sources/repair-plan.json').read_text());p=B/'originals/approved-locomotion.png';assert sha(p)==plan['sourceSha256'];assert sha(B/plan['maskFile'])==plan['maskSha256']
 original=Image.open(p).convert('RGB');candidate=original.copy();allowed=Image.open(B/plan['maskFile']).convert('L');layer=Image.new('RGBA',original.size)
 changes=[]
 for op in plan['operations']:
  at=tuple(op['at']);assert allowed.getpixel(at)==255;before=original.getpixel(at);after=original.getpixel(tuple(op['sample']));assert list(before)==op['beforeRGB'] and list(after)==op['afterRGB']
  candidate.putpixel(at,after);layer.putpixel(at,after+(255,));changes.append({'x':at[0],'y':at[1],'beforeRGB':list(before),'afterRGB':list(after),'sampleX':op['sample'][0],'sampleY':op['sample'][1],'reason':op['defect']})
 effective=Image.new('L',original.size);actual=[]
 for y in range(206):
  for x in range(314):
   if original.getpixel((x,y))!=candidate.getpixel((x,y)):
    assert allowed.getpixel((x,y))==255;effective.putpixel((x,y),255);actual.append([x,y])
 assert len(actual)==6 and set(map(tuple,actual))=={tuple(o['at'])for o in plan['operations']}
 c=B/'candidate/CH3-LOCOMOTION-presenter-local-v02.png';candidate.save(c);effective.save(B/'masks/effective-change-mask.png');layer.save(B/'sources/presenter-six-pixel-edit-layer.png')
 for name,im in [('locomotion-approved',original),('locomotion-presenter-candidate-v02',candidate)]:im.resize((1256,824),Image.Resampling.NEAREST).save(B/'previews'/f'{name}-4x.png')
 pair=Image.new('RGB',(628,206));pair.paste(original,(0,0));pair.paste(candidate,(314,0));pair.save(B/'comparisons/locomotion-approved-left-candidate-right-native.png');pair.resize((2512,824),Image.Resampling.NEAREST).save(B/'comparisons/locomotion-approved-left-candidate-right-4x.png')
 for label,box in [('presenter',(68,81,118,158)),('hair-face',(74,85,97,105)),('open-hand',(101,99,117,111))]:
  old=original.crop(box);new=candidate.crop(box);pair=Image.new('RGB',(old.width*2,old.height));pair.paste(old,(0,0));pair.paste(new,(old.width,0));pair.save(B/'comparisons'/f'{label}-before-after-native.png');pair.resize((pair.width*4,pair.height*4),Image.Resampling.NEAREST).save(B/'comparisons'/f'{label}-before-after-4x.png')
  mask=effective.crop(box);mask.resize((mask.width*4,mask.height*4),Image.Resampling.NEAREST).save(B/'masks'/f'{label}-changed-pixels-4x.png')
  overlay=candidate.convert('RGBA')
  for at in actual:overlay.putpixel(tuple(at),(255,20,60,255))
  overlay.crop(box).resize(((box[2]-box[0])*4,(box[3]-box[1])*4),Image.Resampling.NEAREST).save(B/'comparisons'/f'{label}-change-locator-4x.png')
 (B/'sources/changed-pixels.json').write_text(json.dumps(changes,indent=2))
 with (B/'sources/changed-pixels.csv').open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(changes[0]));w.writeheader();w.writerows(changes)
 stats={'status':'generated','selection':'unselected','approved':False,'assetPath':None,'dimensions':[314,206],'mode':candidate.mode,'changedPixels':len(actual),'totalPixels':314*206,'unchangedPixels':314*206-len(actual),'changedScenePercent':len(actual)/(314*206)*100,'changesOutsideAllowedMask':0,'approvedOriginalSha256':sha(p),'candidateSha256':sha(c),'originalUniqueRGB':len(set(original.get_flattened_data())),'candidateUniqueRGB':len(set(candidate.get_flattened_data())),'partialAlphaPixels':0,'geometryTransforms':0,'paletteTarget':None,'filters':[],'nativeAuthorshipLimitation':'The inherited original full-scene native-grid authorship remains unresolved. The six documented replacements are native-pixel edits; they do not establish original scene authorship.','identityAssessment':'Eyes, eyebrows, nose, mouth, body, costume, near hand, gesture, legs and shoes are pixel-identical. Only three hair edge points, one outer cheek/hair fringe and two open-hand edge points change. No scale or pose change.','remainingLimit':'The result is intentionally subtle. Two contour joins are judgment calls and could be preferred in their original form. All source-derived softness elsewhere remains; no claim of a completed presenter or scene polish.'}
 (B/'sources/repair-result.json').write_text(json.dumps(stats,indent=2));print(json.dumps(stats,indent=2))
if __name__=='__main__':main()
