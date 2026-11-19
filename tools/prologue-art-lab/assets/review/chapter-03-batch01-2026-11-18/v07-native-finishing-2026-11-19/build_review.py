"""Review proofs and validation for the coordinate-authored v07 finishing pass."""
from pathlib import Path
from PIL import Image
import hashlib, json, html

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent
REPO=BASE.parents[4]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2)+'\n')
def image(src,w,h,alt):return f'<div class="viewport"><img class="art" src="{src}" width="{w}" height="{h}" data-w="{w}" data-h="{h}" alt="{html.escape(alt)}"></div>'
pins=json.loads((ROOT/'sources/history-pins.json').read_text())
for p in pins['files']:assert sha(BASE/p['file'])==p['sha256'],p['file']
refs=json.loads((ROOT/'sources/reference-manifest.json').read_text())
for p in refs:
    assert sha(ROOT/p['file'])==p['sha256']
    assert sha(REPO/p['repositoryPath'])==p['sha256']
record=json.loads((ROOT/'sources/native-edit-record.json').read_text())
approved=['prologue-reception.png','chapter-01-foyer.png','chapter-02-groundskeeper.png']
approved_colors={n:len(Image.open(ROOT/'references'/n).convert('RGB').getcolors(64684)) for n in approved}
cards=[];qa=[];manifest=[]
notes={
 'A01':[
 'Restored a small slate/steel gooseneck microphone on the desk, immediately right of the intercom and left of the attendant. The attendant was not translated, scaled or repositioned.',
 'Replaced selected face pixels with thin rectangular glasses, one-pixel bridge, two scene-scale eye marks, gray temple clusters, a warmer jaw contour and a small open smile. Changed selected shirt, vest and tie pixels without changing the seated pose.',
 'Finished the unobstructed center-post faces, selected jamb/lintel runs, gate-panel interiors, reception-counter planes and intercom slot runs. The sign, access reader, turnstile and metal frame remain pixel-identical.',
 'The unwanted right-hand desk device remains absent; that region is pixel-identical to v06. All other architecture retains its framing and object positions.',
 'Face resemblance is a review judgment: the small manually finished face still differs from the A03 portrait. The source-derived shading outside the edit regions remains soft and tonally varied.'
 ],
 'A04':[
 'Finished selected curtain fold faces/creases, camera-stand metal plane/edge, platform front facets, presenter jacket/skirt planes and two central stage-step edge runs. No object was moved, scaled or reframed.',
 "PEOPLE'S PAVILION signage, countdown 30 and ring, standing microphone, presenter face and welcoming hand, camera body/lens, side chair and rear exit are byte-identical to v06 in the locked proof regions.",
 'The presenter identity/gesture, circular platform, curtain/support architecture, seating and framing are retained. The 564×278 A06 foreground remains untouched.',
 'The finish is local. Most of the image, including many antialiased-looking/soft tonal transitions, remains inherited from v06; it is not a full native redraw or full-scene palette normalization.'
 ]}

for r in record['candidates']:
    ident=r['candidateId'];key='A01' if 'A01' in ident else 'A04'
    original=Image.open(ROOT/r['source']).convert('RGB');out=Image.open(ROOT/r['candidate']).convert('RGB')
    assert original.size==out.size==(314,206)
    assert sha(ROOT/r['candidate'])==r['sha256']
    preview=Image.open(ROOT/f'previews/{ident}-4x.png').convert('RGB')
    assert preview.size==(1256,824)
    px=preview.load();src=out.load()
    assert all(px[4*x+dx,4*y+dy]==src[x,y] for y in range(206) for x in range(314) for dx in range(4) for dy in range(4))
    mask=Image.open(ROOT/f'diagnostics/{key}-changed-pixels.png').convert('RGB')
    scope=Image.open(ROOT/f'diagnostics/{key}-declared-scope.png').convert('1')
    changed=[]
    for y in range(206):
        for x in range(314):
            different=original.getpixel((x,y))!=out.getpixel((x,y))
            assert bool(mask.getpixel((x,y))!=(0,0,0))==different
            if different:
                assert scope.getpixel((x,y)),(key,x,y)
                changed.append((x,y))
    assert len(changed)==r['changedPixels']
    before_colors=len({original.getpixel(p) for p in changed})
    after_colors=len({out.getpixel(p) for p in changed})
    pair=Image.new('RGB',(628,206));pair.paste(original,(0,0));pair.paste(out,(314,0))
    pair.save(ROOT/f'comparisons/{key}-v06-v07.png')
    pair.resize((2512,824),Image.Resampling.NEAREST).save(ROOT/f'comparisons/{key}-v06-v07-4x.png')
    density=Image.new('RGB',(1256,206));density.paste(out,(0,0))
    for index,name in enumerate(approved,1):density.paste(Image.open(ROOT/'references'/name).convert('RGB'),(index*314,0))
    density.save(ROOT/f'comparisons/{key}-approved-style.png')
    density.resize((5024,824),Image.Resampling.NEAREST).save(ROOT/f'comparisons/{key}-approved-style-4x.png')
    # Character proofs retain native pixels; scene and portrait crop scales differ
    # deliberately and are explicitly labeled, rather than normalizing faces.
    facebox=(201,96,229,122) if key=='A01' else (73,86,118,139)
    char=Image.new('RGB',((facebox[2]-facebox[0])*2,facebox[3]-facebox[1]))
    char.paste(original.crop(facebox),(0,0));char.paste(out.crop(facebox),(facebox[2]-facebox[0],0))
    char.save(ROOT/f'comparisons/{key}-identity-v06-v07.png')
    char.resize((char.width*8,char.height*8),Image.Resampling.NEAREST).save(ROOT/f'comparisons/{key}-identity-v06-v07-8x.png')
    port=Image.open(ROOT/'references'/('A03-attendant.png' if key=='A01' else 'A06-presenter.png')).convert('RGBA')
    box=(267,41,361,154) if key=='A01' else (131,71,229,155)
    crop=port.crop(box);back=Image.new('RGBA',crop.size,'#23373d');back.alpha_composite(crop);back.convert('RGB').save(ROOT/f'comparisons/{key}-portrait-identity-crop.png')
    if key=='A01':
        micbox=(180,122,208,146)
        mic=out.crop(micbox);mic.save(ROOT/'diagnostics/A01-microphone-closeup.png')
        mic.resize((224,192),Image.Resampling.NEAREST).save(ROOT/'diagnostics/A01-microphone-closeup-8x.png')
        original.crop(micbox).resize((224,192),Image.Resampling.NEAREST).save(ROOT/'diagnostics/A01-microphone-before-8x.png')
    q={
      'candidateId':ident,'dimensions':{'result':'PASS','nativeWorkingGrid':[314,206],'candidateResampled':False},
      'alpha':{'result':'PASS','extrema':list(out.convert('RGBA').getchannel('A').getextrema()),'mode':out.mode},
      'preview':{'result':'PASS','dimensions':[1256,824],'all4x4BlocksMatchSource':True},
      'editScope':{'result':'PASS','operations':r['nativeEditOperations'],'changedPixels':len(changed),'percent':r['changedPercent'],'unexpectedChangedPixels':len(r['unexpectedChangedPixels']),'allLockedRegionsPass':all(p['byteIdenticalToV06'] for p in r['lockedRegions'])},
      'palette':{'beforeUniqueRGB':r['sourceUniqueRGB'],'afterUniqueRGB':r['finishedUniqueRGB'],'changedPixelRegionBeforeUniqueRGB':before_colors,'changedPixelRegionAfterUniqueRGB':after_colors,'authoredColors':r['authoredEditColors'],'fixedLimit':None,'globalQuantization':False,'sharpening':False,'dithering':False,'filtering':False},
      'nativeFinishingEvidence':'PASS: all modified coordinates, final before/after RGB values, primitive definitions and scope masks are supplied. Edits were executed directly on the inherited 314x206 canvas.',
      'originalWholeSceneNativeAuthorship':'UNPROVEN. The unchanged majority remains source-derived. Native finishing is not a claim of original native authorship.',
      'remainingLimitations':notes[key][-1],
      'visualApproval':'PENDING NATE; no technical metric selects or approves a candidate.'
    }
    qa.append(q)
    manifest.append({k:r[k] for k in ['candidateId','candidate','sha256','source','sourceSha256','dimensions','nativeEditOperations','changedPixels','sourceUniqueRGB','finishedUniqueRGB','status','selected','approved','assetPath']})
    title='A01 — Restroom' if key=='A01' else 'A04 — Verification stage'
    cards.append(f'''<article class="candidate" id="{ident}"><h2>{title}</h2><p><strong>{ident}</strong> · Generated / unselected · 314×206</p>
{image(r['candidate'],314,206,title+' native finishing candidate')}<p class="meta">SHA-256: <code>{r['sha256']}</code></p>
<p><a href="{r['candidate']}">314×206 PNG</a> · <a href="previews/{ident}-4x.png">Exact 4× PNG</a> · <a href="sources/{key}-changed-pixels.tsv">Every changed pixel: before/after RGB</a></p>
<h3>v06 → v07</h3><p class="meta">Left: v06. Right: v07. Same framing, native grid and display scale.</p>{image(f'comparisons/{key}-v06-v07.png',628,206,title+' v06 left v07 right')}
<h3>Approved chapter style comparison</h3><p class="meta">Left to right: v07, approved Prologue reception, approved Chapter 1 foyer, selected Chapter 2 groundskeeper. All scenes are 314×206.</p>{image(f'comparisons/{key}-approved-style.png',1256,206,title+' beside earlier chapters')}
<h3>Exact corrections</h3><ul>{''.join('<li>'+html.escape(n)+'</li>' for n in notes[key])}</ul>
<p class="notice">Whole-image RGB colors: <strong>{r['sourceUniqueRGB']:,} → {r['finishedUniqueRGB']:,}</strong>. Changed-pixel region: {before_colors:,} → {after_colors:,} colors. Counts are diagnostic evidence, not a palette target or approval test. Most inherited RGB softness remains.</p>
<h3>Changed-pixel mask</h3><p class="meta">Orange marks the {len(changed):,} changed pixels ({r['changedPercent']}%); black marks pixels identical to v06. No other pixel changed.</p>{image(f'diagnostics/{key}-changed-pixels.png',314,206,title+' exact change mask')}
<h3>Character identity proof</h3><p class="meta">Native scene crops: v06 left / v07 right. The separately linked 8× proof uses exact nearest-neighbor. The portrait crop retains its own native scale; it was not resized to force a likeness comparison.</p>{image(f'comparisons/{key}-identity-v06-v07.png',char.width,char.height,title+' character before and after')}<p><a href="comparisons/{key}-identity-v06-v07-8x.png">8× scene identity proof</a></p>{image(f'comparisons/{key}-portrait-identity-crop.png',crop.width,crop.height,title+' unchanged portrait identity crop')}
</article>''')
write('qa.json',{'nativeFinishing':'PASS for documented local edits; original full-scene native authorship remains unproven.','candidates':qa,'approvedReferenceUniqueRGBColors':approved_colors,'historyPreservation':{'result':'PASS','sourcePin':pins['commit'],'filesChecked':len(pins['files'])},'referencesUnchanged':{'result':'PASS','count':len(refs)},'unchangedPortraits':json.loads((BASE/'v06-314-regeneration-2026-11-19/qa.json').read_text())['unchangedPortraits'],'productionScope':'Narrative, dialogue, game, selected/approved assets, items and production registry unchanged. No approval or integration.'})
write('manifest.json',{'version':'v07','date':'2026-11-19','branch':'art/ch3-pavilion-batch01-20261118','sourcePin':pins['commit'],'method':'Direct native-grid coordinate edits; no image generation or candidate resampling.','generationCalls':0,'status':'generated/unselected','selected':False,'approved':False,'originalNativeAuthorship':'UNPROVEN; source-derived v06 retained except logged native finishing edits.','candidates':manifest,'editRecord':'sources/native-edit-record.json','qa':'qa.json'})
write('sources/provenance.json',{'sourcePin':pins['commit'],'sourceInputs':refs[:2],'inheritedGenerationRecords':'../v06-314-regeneration-2026-11-19/sources/generation-records.json','candidateResampling':False,'manualMeaning':'Codex specified individual coordinates, polygons, line runs and curated RGB colors. Python/Pillow executed those explicit native raster primitives. This was not a human pixel-editor session and was not automated global color quantization.','fullEditSpecification':'edit-native.py','exactPixelDeltas':['sources/A01-changed-pixels.tsv','sources/A04-changed-pixels.tsv'],'generationCalls':0,'studiesGenerated':False,'productionMainSceneResolution':[314,206]})
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 3 — v07 native finishing</title>
<style>*{box-sizing:border-box}body{margin:0;background:#15252a;color:#f3e9d9;font:16px/1.55 system-ui,sans-serif}main{max-width:1380px;margin:auto;padding:24px}h1{font-size:30px;line-height:1.2}h2{font-size:24px}h3{font-size:19px}a{color:#9de0db}code{overflow-wrap:anywhere}nav,.controls{display:flex;gap:12px;flex-wrap:wrap;margin:18px 0}.controls{position:sticky;top:0;background:#15252af5;padding:12px 0;z-index:2}button{font:inherit;padding:9px 16px;border:1px solid #819c9f;background:#25444d;color:inherit;border-radius:4px;cursor:pointer}button[aria-pressed=true]{background:#f4d3ac;color:#17272c}.notice{padding:16px;background:#563e31;border-left:4px solid #f0b984}.viewport{max-width:100%;overflow:auto;background:#091519;border:1px solid #55727a}.viewport img{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}article{border-top:1px solid #55727a;margin-top:36px;padding-top:18px}.meta{color:#c5d5d6;font-size:14px}li{margin:8px 0}.proofs{display:flex;flex-wrap:wrap;gap:24px}.proofs figure{margin:0;max-width:100%}figcaption{margin:8px 0}</style>
<main><h1>Chapter 3 — v07 native pixel finishing</h1><p><strong>Two 314×206 candidates · Generated / unselected</strong></p>
<p>Targeted coordinate-authored finishing on the existing v06 canvases. No new generation, composition replacement, resolution change or global palette filter. A02, A03, A05 and A06 remain unchanged at 564×278.</p>
<p class="notice"><strong>Authorship boundary:</strong> the logged local edits were made directly on the 314×206 grid. The inherited majority remains source-derived, with substantial RGB softness and tonal variation. This does not establish original native-grid authorship of either full scene.</p>
<nav><a href="#CH3-A01-restroom-v07">A01</a><a href="#CH3-A04-verification-v07">A04</a><a href="#microphone">Microphone close-up</a><a href="../v06-314-regeneration-2026-11-19/">Preserved v06 gallery</a><a href="manifest.json">Candidates / hashes</a><a href="qa.json">Technical QA</a></nav>
<div class="controls"><button data-scale="1" aria-pressed="true">1× working grid</button><button data-scale="4" aria-pressed="false">4× nearest-neighbor</button></div><p class="meta">All artwork displays at exact integer scale. Comparison rows scroll; artwork is never shrunk to fit a device.</p>
CARDS
<section id="microphone"><h2>A01 — unobstructed restored microphone</h2><p>The new head, gooseneck, base and small highlights use explicit native pixels beside the intercom. The attendant stays at his v06 position. These fixed 8× crops show the same 28×24 source region.</p><div class="proofs"><figure><figcaption>v06 · microphone missing</figcaption>MIC_BEFORE</figure><figure><figcaption>v07 · microphone restored</figcaption>MIC_AFTER</figure></div></section>
<h2>Palette and pixel-quality inspection</h2><p>The pass consolidates selected material planes and character clusters. It does not chase a mandatory color count. Earlier chapter references contain REF_COLORS unique RGB colors respectively; v07 remains much more tonally varied. See the per-scene counts above and the exact edit specification before judging whether the local finish is an improvement.</p>
<p>No palette study was promoted and no controlled palette-filter experiment was needed for this pass. Remaining soft edges, source-derived shading and scene-scale face likeness are explicitly pending Nate’s judgment.</p>
<h2>Records and review gate</h2><p><a href="sources/native-edit-record.json">Every authored primitive and protected-region result</a> · <a href="edit-native.py">Reproducible native edit specification</a> · <a href="sources/provenance.json">What “manual” means / inherited source provenance</a> · <a href="sources/reference-manifest.json">Reference source paths and hashes</a> · <a href="sources/history-pins.json">All historical hashes</a> · <a href="PNG_SHA256SUMS.txt">PNG checksums</a> · <a href="SOURCE_SHA256SUMS.txt">Package checksums</a> · <a href="browser-qa.json">Local browser verification</a> · <a href="public-browser-qa.json">Public browser verification</a></p><p>All HISTORY_COUNT previous review files are unchanged from commit 025a900. No narrative, gameplay, selected/approved artwork, production registry or portrait was changed. Nothing is selected, approved or integrated; no further artwork batch has begun. Stop for Nate’s Art Director review.</p>
</main><script>document.querySelectorAll('[data-scale]').forEach(b=>b.onclick=()=>{const s=Number(b.dataset.scale);document.querySelectorAll('img.art').forEach(i=>{i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s});document.querySelectorAll('[data-scale]').forEach(n=>n.setAttribute('aria-pressed',String(n===b)));});</script></html>'''
mic_before='<div class="viewport"><img src="diagnostics/A01-microphone-before-8x.png" width="224" height="192" alt="Microphone missing in v06"></div>'
mic_after='<div class="viewport"><img src="diagnostics/A01-microphone-closeup-8x.png" width="224" height="192" alt="Restored microphone visible beside intercom in v07"></div>'
page=page.replace('CARDS','\n'.join(cards)).replace('MIC_BEFORE',mic_before).replace('MIC_AFTER',mic_after).replace('REF_COLORS',', '.join(map(str,approved_colors.values()))).replace('HISTORY_COUNT',str(len(pins['files'])))
(ROOT/'index.html').write_text(page)
(ROOT/'README.md').write_text('''# Chapter 3 v07 — native finishing

Two generated/unselected 314×206 review candidates finished with explicit coordinate-authored raster primitives. No imagegen calls or candidate resizing. Run `python3 edit-native.py`, then `python3 build_review.py`. Run `qa-browser.cjs` and rebuild the package checksum lists afterward.

The edit script, named primitive log, every before/after RGB coordinate, scope masks and protected-region checks substantiate the local native finishing. They do not prove original native-grid authorship of the inherited full scenes. Most RGB softness remains source-derived. Palette counts are diagnostic, not mandatory limits.

A01 restores the unobstructed desk microphone, refines selected glasses/temple/jaw/smile/clothing clusters, and selected architectural material planes. A04 receives local curtain, camera-stand, platform, costume and stage-edge work. Locked required text, countdown, hardware, presenter face and gesture remain unchanged as recorded.

All v01–v06 files, four portraits, approved/selected assets, narrative, gameplay and production registry are unchanged. Nothing approved, registered or integrated. Stop for Nate’s visual review.
''')
pngs=sorted(p for p in ROOT.rglob('*.png') if p.is_file() and 'working' not in p.relative_to(ROOT).parts)
(ROOT/'PNG_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(ROOT).as_posix()}\n' for p in pngs))
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and 'working' not in p.relative_to(ROOT).parts and p.suffix!='.png' and p.name!='SOURCE_SHA256SUMS.txt')
(ROOT/'SOURCE_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(ROOT).as_posix()}\n' for p in files))
print(json.dumps({'historyFilesUnchanged':len(pins['files']),'candidateHashes':{r['candidateId']:r['sha256'] for r in record['candidates']},'nativeFinishing':'documented','originalFullSceneNativeAuthorship':'unproven'},indent=2))
