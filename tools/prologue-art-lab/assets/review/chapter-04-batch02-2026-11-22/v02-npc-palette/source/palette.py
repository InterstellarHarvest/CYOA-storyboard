"""Compact no-dither NPC palette calibrated to approved Chapter2's 50/61 tones.

A requested color treatment, not independent drawing or anatomical revision.
Alpha and geometry are preserved. No gradient/shading is synthesized.
"""
from PIL import Image

def compact(im,colors=64):
 im=im.convert('RGBA');original=list(im.get_flattened_data());samples=[p[:3] for p in original if p[3]>=245]
 sample=Image.new('RGB',(len(samples),1));sample.putdata(samples);q=sample.quantize(colors=colors,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
 raw=q.getpalette();used=sorted(set(q.get_flattened_data()));palette=[tuple(raw[i*3:i*3+3]) for i in used]
 unique={p[:3] for p in original if p[3]};mapping={rgb:min(palette,key=lambda c:(rgb[0]-c[0])**2+(rgb[1]-c[1])**2+(rgb[2]-c[2])**2) for rgb in unique}
 out=Image.new('RGBA',im.size);out.putdata([mapping[p[:3]]+(p[3],) if p[3] else p for p in original]);assert out.getchannel('A').tobytes()==im.getchannel('A').tobytes()
 report={'method':'Opaque-interior weighted median-cut palette fit; every foreground RGB assigned to nearest chosen tone, no dithering or new shading','calibration':'Approved Chapter2 Groundskeeper61 and Courtesy Conductor50 opaque colors; choose conventional64-tone NPC treatment, not a global environment limit','sourceRGBColors':len({p[:3] for p in original if p[3]>=245}),'finalRGBColors':len({p[:3] for p in out.get_flattened_data() if p[3]>=245}),'palette':palette,'alphaExactlyPreserved':True,'anatomyReconstructed':False,'gradientsAdded':False}
 return out,report
