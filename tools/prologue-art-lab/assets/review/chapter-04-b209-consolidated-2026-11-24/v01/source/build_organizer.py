"""One source-derived organizer, with native material/contour construction.

No Bixby image is regenerated. The preserved candidate remains byte-for-byte.
"""
from pathlib import Path
from PIL import Image, ImageDraw
from collections import Counter
import hashlib, json, platform

ROOT=Path(__file__).resolve().parents[1]
SIZE=(564,278)

def save(im,rel):im.save(ROOT/rel)

def quiet_clusters(image,eligible):
    src=list(image.get_flattened_data());out=src[:];seen=set();changed=0;w,h=image.size
    for i,c in enumerate(src):
        if i in seen:continue
        q=[i];seen.add(i);component=[];neighbors=[]
        while q:
            k=q.pop();component.append(k);x,y=k%w,k//w
            for n in ([k-1]if x else[])+([k+1]if x<w-1 else[])+([k-w]if y else[])+([k+w]if y<h-1 else[]):
                if src[n]==c:
                    if n not in seen:seen.add(n);q.append(n)
                else:neighbors.append(src[n])
        if len(component)>2 or not neighbors or not all(eligible[k]for k in component):continue
        target,n=Counter(neighbors).most_common(1)[0]
        if n>=3 and sum((a-b)**2 for a,b in zip(c,target))<1100:
            for k in component:out[k]=target
            changed+=len(component)
    image.putdata(out);return image,changed

def main():
    path=ROOT/'originals/CH4-NEW-06-organizer-detailed.png';source=Image.open(path).convert('RGBA')
    source_alpha=source.getchannel('A').point(lambda a:255 if a>=128 else 0);box=source_alpha.getbbox();crop=source.crop(box)
    height=266;width=round(crop.width*height/crop.height);left=300;top=12
    draft=Image.new('RGBA',SIZE);draft.paste(crop.resize((width,height),Image.Resampling.NEAREST),(left,top))
    save(draft,'evidence/internal-study/organizer-direct-transfer-diagnostic.png')
    alpha=draft.getchannel('A').point(lambda a:255 if a>=160 else 0);ap=list(alpha.get_flattened_data());rgb=draft.convert('RGB');raw=list(rgb.get_flattened_data())
    opaque=[c for c,a in zip(raw,ap)if a];strip=Image.new('RGB',(len(opaque),1));strip.putdata(opaque)
    palette=strip.quantize(colors=64,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    fitted=rgb.quantize(palette=palette,dither=Image.Dither.NONE).convert('RGB')
    # Target-grid material masks preserve eyes, brows, mouth, hair locks, natural
    # fingers and the THREE board clips. Quiet isolated cloth/paper flecks only.
    fp=list(fitted.get_flattened_data());eligible=[];categories=[]
    for i,c in enumerate(fp):
        x,y=i%564,i//564;r,g,b=c
        if not ap[i]:category='clear'
        elif y<116 and r>g*1.12 and r>75 and not(r>160 and g>112):category='auburn-hair'
        elif r>145 and r>g*1.12 and g>b*1.12:category='skin-and-hands'
        elif r>175 and g>160 and b>120:category='ivory-paper-and-collar'
        elif max(c)-min(c)<55 and max(c)<180:category='slate-suit-and-board-edges'
        else:category='contours-and-clip-details'
        categories.append(category)
        eligible.append(bool(ap[i])and category in['slate-suit-and-board-edges','ivory-paper-and-collar']and y>115)
    fitted,merged=quiet_clusters(fitted,eligible)
    # Native contour cleanup removes detached alpha islands and retains all
    # connected curl/finger edges. No soft halo or partly transparent interior.
    clean=ap[:];detached=0
    for y in range(1,277):
        for x in range(1,563):
            i=y*564+x
            if ap[i]and not any(ap[n]for n in[i-1,i+1,i-564,i+564]):clean[i]=0;detached+=1
    final=Image.new('RGBA',SIZE);final.putdata([c+(255,)if a else(0,0,0,0)for c,a in zip(fitted.get_flattened_data(),clean)])
    # Explicit native construction decisions are applied after the diagnostic
    # transfer: discreet tailoring replaces an unrequested blank source badge.
    correction=Image.new('RGBA',SIZE);d=ImageDraw.Draw(correction)
    d.polygon([(367,157),(393,151),(396,160),(391,166),(386,169),(371,174)],fill=(81,80,84))
    # Restrict corrections to the actual character silhouette.
    correction.putalpha(Image.frombytes('L',SIZE,bytes(255 if a and b else 0 for a,b in zip(correction.getchannel('A').get_flattened_data(),clean))))
    final=Image.alpha_composite(final,correction)
    for i,a in enumerate(correction.getchannel('A').get_flattened_data()):
        if a:categories[i]='slate-suit-and-board-edges'
    save(correction,'layers/NEW-06-native-tailoring-correction.png')
    save(final,'native/CH4-NEW-06-organizer-urgent-v01.png')
    save(final.resize((2256,1112),Image.Resampling.NEAREST),'previews/CH4-NEW-06-organizer-urgent-v01-4x.png')
    save(final,'layers/NEW-06-complete-native-foreground.png');save(final.getchannel('A'),'masks/NEW-06-binary-silhouette.png')
    for name in sorted(set(categories)-{'clear'}):
        m=Image.new('L',SIZE);m.putdata([255 if category==name and a else 0 for category,a in zip(categories,clean)])
        part=final.copy();part.putalpha(m);save(m,f'masks/NEW-06-{name}.png');save(part,f'layers/NEW-06-{name}.png')
    records={'sourceDerived':True,'independentlyAuthoredAtNativeResolution':False,'source':'originals/CH4-NEW-06-organizer-detailed.png','sourceSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'sourceSilhouetteBox':box,'composition':{'left':left,'top':top,'height':height,'width':width,'uniformNearestDiagnosticTransfer':True},'method':'Detailed source -> native diagnostic -> opaque-only coherent64-tone fitting -> material-specific protected clusters -> isolated cloth/paper cluster reconstruction -> native silhouette and tailoring correction -> disjoint editable material layers. Diagnostic reduction and palette fit alone are not the final artwork. Face/hair/hands/three clips remain protected; no whole-image independent native authorship claim.','sourcePaletteFit':64,'nativeColors':len(set(c for c in final.get_flattened_data()if c[3])),'quietMaterialPixelsMerged':merged,'detachedAlphaPixelsRemoved':detached,'binaryAlpha':True,'python':platform.python_version(),'pillow':Image.__version__,'characterReference':'references/approved-organizer-scene-crop.png','nativeCanvas':list(SIZE),'finalSha256':hashlib.sha256((ROOT/'native/CH4-NEW-06-organizer-urgent-v01.png').read_bytes()).hexdigest()}
    (ROOT/'evidence/organizer-derivation.json').write_text(json.dumps(records,indent=2)+'\n')
    print('Single organizer native foreground, editable semantic layers and exact4x ready.')

if __name__=='__main__':main()
