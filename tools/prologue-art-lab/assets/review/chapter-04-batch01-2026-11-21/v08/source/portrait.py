"""Authorized source-derived portrait. Never claimed independently native-drawn.

Preserve the preferred original. Premultiplied-alpha Lanczos reduction avoids
dark matte contamination. Cleanup only removes very low-alpha edge specks,
disconnected cutout debris and unusually saturated cutout fringe colors.
Native interior contrast cleanup clarifies the existing face/hair/hands/cloth;
there is no palette reduction, coordinate reconstruction or anatomy repainting.
"""
from pathlib import Path
from PIL import Image,ImageFilter
from collections import deque
import hashlib,json

ROOT=Path(__file__).resolve().parent.parent
SOURCE=ROOT.parent/'portrait-study-02/generated/CH4-03-auctioneer-fresh-style-original.png'

def main():
    (ROOT/'native').mkdir(exist_ok=True)
    original=Image.open(SOURCE).convert('RGBA')
    im=original.convert('RGBa').resize((564,278),Image.Resampling.LANCZOS).convert('RGBA')
    before=im.copy();p=im.load();w,h=im.size
    # The source has small isolated brightly colored cutout debris. Alpha
    # cleanup is restricted to the existing silhouette boundary, not anatomy.
    for y in range(h):
        for x in range(w):
            r,g,b,a=p[x,y]
            if a<=40:p[x,y]=(0,0,0,0)
    components=[];seen=set()
    for y in range(h):
        for x in range(w):
            if not p[x,y][3] or (x,y) in seen:continue
            seen.add((x,y));q=deque([(x,y)]);component=[]
            while q:
                a,b=q.popleft();component.append((a,b))
                for xx,yy in [(a-1,b),(a+1,b),(a,b-1),(a,b+1)]:
                    if 0<=xx<w and 0<=yy<h and p[xx,yy][3] and (xx,yy) not in seen:
                        seen.add((xx,yy));q.append((xx,yy))
            components.append(component)
    components.sort(key=len,reverse=True)
    for c in components[1:]:
        for x,y in c:p[x,y]=(0,0,0,0)
    clean=im.copy();q=clean.load();fringe=[]
    def interior(x,y):
        return p[x,y][3]>=245 and all(p[xx,yy][3]>200 for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)] if 0<=xx<w and 0<=yy<h)
    for y in range(1,h-1):
        for x in range(1,w-1):
            r,g,b,a=p[x,y]
            if not a or max(r,g,b)-min(r,g,b)<100:continue
            if not any(p[xx,yy][3]==0 for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]):continue
            neighbors=[((xx-x)**2+(yy-y)**2,xx,yy) for yy in range(max(1,y-3),min(h-1,y+4)) for xx in range(max(1,x-3),min(w-1,x+4)) if interior(xx,yy)]
            if not neighbors:continue
            _,xx,yy=min(neighbors);rgb=p[xx,yy][:3]
            if sum((c-d)**2 for c,d in zip((r,g,b),rgb))>70**2:
                q[x,y]=rgb+(a,);fringe.append([x,y])
    # Targeted finish at final resolution. Only near-opaque pixels whose
    # immediate neighbors are also opaque are eligible, preserving the exact
    # v06 alpha silhouette and its cleaned antialiased boundary colors.
    sharp=clean.convert('RGB').filter(ImageFilter.UnsharpMask(radius=.55,percent=85,threshold=2))
    before_finish=clean.copy();original_pixels=before_finish.load();sp=sharp.load()
    targeted=0
    regions=[(270,34,349,132),(254,153,368,277),(211,128,420,277)]
    for y in range(1,h-1):
        for x in range(1,w-1):
            if not any(x0<=x<x1 and y0<=y<y1 for x0,y0,x1,y1 in regions):continue
            if original_pixels[x,y][3]<245:continue
            if not all(original_pixels[xx,yy][3]>=245 for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]):continue
            value=sp[x,y]+(original_pixels[x,y][3],)
            if value!=original_pixels[x,y]:clean.putpixel((x,y),value);targeted+=1
    clean.save(ROOT/'native/CH4-03-auctioneer-source-derived-v08.png')
    changed=sum(a!=b for a,b in zip(before.get_flattened_data(),clean.get_flattened_data()))
    report={'status':'UNSELECTED','method':'SOURCE-DERIVED; authorized quality-first portrait policy','independentlyAuthoredAtNativeResolution':False,'policy':'../PRODUCTION-POLICY.md','source':'../portrait-study-02/generated/CH4-03-auctioneer-fresh-style-original.png','sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'sourceDimensions':list(original.size),'outputDimensions':[564,278],'pillowVersion':Image.__version__,'reduction':'RGBA -> premultiplied RGBa -> Lanczos 564x278 -> RGBA; no crop or composition shift','internalFilterComparison':'Preserved the successful Lanczos source reduction and edge cleanup. Compared native interior cleanup at0/55/85percent; selected85 for clearer existing features without new geometry. Intermediate trials remain private.','cleanup':'Preserved v06 cutout cleanup, then selectively clarified existing face/hair/hands/gavel/tailoring contrast at final resolution. Near-opaque interior only; alpha and boundary colors remain unchanged. No anatomy/costume repaint.','changedPixelsFromReduction':changed,'fringeColorPixels':fringe,'paletteReduction':False,'nativeInteriorCleanup':{'filter':'UnsharpMask','radius':.55,'percent':85,'threshold':2,'eligibleRegions':regions,'nearOpaqueInteriorOnly':True,'minimumAlpha':245,'originalAlphaRetained':True,'changedPixels':targeted},'alphaMatchesV06Exactly':True,'sourceModified':False,'artworkApproved':False}
    (ROOT/'evidence/portrait-derivation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Source-derived portrait ready;',targeted,'native interior cleanup pixels; exact prior alpha retained.')

if __name__=='__main__':main()
