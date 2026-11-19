"""Honest, non-destructive packaging of two fresh imagegen main-scene outputs."""
from pathlib import Path
from PIL import Image
import hashlib
import html
import json
import shutil

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent
REPO = BASE.parents[4]
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def put(name, data):
    (ROOT/name).write_text(json.dumps(data, indent=2)+'\n')
pins = json.loads((ROOT/'sources/history-pins.json').read_text())
for item in pins['files']:
    assert sha(BASE/item['file']) == item['sha256'], item['file']
refs = json.loads((ROOT/'sources/reference-manifest.json').read_text())
for item in refs:
    assert sha(ROOT/item['file']) == item['sha256']
    assert sha(REPO/item['repositoryPath']) == item.get('repositorySourceSha256',item['sha256'])
records = json.loads((ROOT/'sources/generation-records.json').read_text())
visual = json.loads((ROOT/'sources/visual-inspection.json').read_text())
candidates = []
qa = []
for record in records:
    ident = record['candidateId']
    source = ROOT/record['source']
    assert sha(source) == record['sourceSha256']
    original = Image.open(source)
    assert list(original.size) == record['actualSourceDimensions']
    working = original.convert('RGB')
    derived = working.size != (314,206)
    if derived:
        working = working.resize((314,206), Image.Resampling.NEAREST)
    candidate = ROOT/f'candidates/{ident}.png'
    working.save(candidate)
    preview = working.resize((1256,824), Image.Resampling.NEAREST)
    preview.save(ROOT/f'previews/{ident}-4x.png')
    assert preview.tobytes() == working.resize((1256,824), Image.Resampling.NEAREST).tobytes()
    # Check every preview block, not only a sampled subset.
    pixels = preview.load()
    for y in range(206):
        for x in range(314):
            expected = working.getpixel((x,y))
            assert all(pixels[4*x+dx,4*y+dy] == expected for dx in range(4) for dy in range(4))
    old_name = 'previous-A01-v04.png' if 'A01' in ident else 'previous-A04-v04.png'
    old = Image.open(ROOT/'references'/old_name).convert('RGB')
    assert old.size == (314,206)
    pair = Image.new('RGB',(628,206)); pair.paste(old,(0,0)); pair.paste(working,(314,0))
    pair.save(ROOT/f'comparisons/{ident}-previous-current.png')
    pair.resize((2512,824),Image.Resampling.NEAREST).save(ROOT/f'comparisons/{ident}-previous-current-4x.png')
    density = Image.new('RGB',(1256,206)); density.paste(working,(0,0))
    for i,name in enumerate(['prologue-reception.png','chapter-01-foyer.png','chapter-02-groundskeeper.png'],1):
        ref=Image.open(ROOT/'references'/name).convert('RGB'); assert ref.size == (314,206)
        density.paste(ref,(i*314,0))
    density.save(ROOT/f'comparisons/{ident}-approved-density.png')
    density.resize((5024,824),Image.Resampling.NEAREST).save(ROOT/f'comparisons/{ident}-approved-density-4x.png')
    item = {
        'id':ident, 'baseId':'CH3-A01-restroom' if 'A01' in ident else 'CH3-A04-verification',
        'candidate':f'candidates/{ident}.png','sha256':sha(candidate),'dimensions':[314,206],
        'preview4x':f'previews/{ident}-4x.png','previewSha256':sha(ROOT/f'previews/{ident}-4x.png'),
        'source':record['source'],'sourceSha256':sha(source),'actualSourceDimensions':list(original.size),
        'derivedExport':derived,'derivation':'RGB conversion; nearest-neighbor reduction of the fresh generated raster to 314x206. No sharpening, inking, palette quantization, blur or automatic pixelation to conceal the source size.' if derived else 'RGB export at returned source size; no resize.',
        'previousComparison':f'comparisons/{ident}-previous-current.png',
        'approvedDensityComparison':f'comparisons/{ident}-approved-density.png',
        'status':'generated','selected':False,'approved':False,'assetPath':None,
        'prompt':record['prompt']
    }
    candidates.append(item)
    qa.append({
        'candidateId':ident,
        'freshGeneration':{'result':'PASS','evidence':record['source'],'referencesExclude628Study':True},
        'requestedSourceSize':{'result':'FAIL' if derived else 'PASS','requested':[314,206],'actual':list(original.size)},
        'originalNativeGridAuthorship':{'result':'UNPROVEN / NOT PASSED','reason':'No source-editor/grid authorship evidence. A dimensionally correct derived export cannot certify deliberate 314-grid authorship.'},
        'workingDimensions':{'result':'PASS','size':list(working.size)},
        'alpha':{'result':'PASS' if original.convert('RGBA').getchannel('A').getextrema()==(255,255) else 'FAIL','requirement':'opaque main scene','sourceAlphaExtrema':list(original.convert('RGBA').getchannel('A').getextrema()),'workingAlphaExtrema':[255,255]},
        'preview':{'result':'PASS','size':list(preview.size),'scale':4,'all4x4BlocksExactlyEqualWorkingPixels':True},
        'palette':{'sourceUniqueRGB':len(original.convert('RGB').getcolors(original.width*original.height)),'workingUniqueRGB':len(working.getcolors(314*206)),'quantizationApplied':False,'fixedPaletteLimit':None,'assessment':'Measured, not a pass claim. Native cluster quality, shading and remaining antialiasing/tonal softness require visual judgment.'},
        'visualInspection':visual[ident],
        'productionReady':False
    })
put('manifest.json',{'version':'v06','date':'2026-11-19','sourcePin':pins['commit'],'branch':'art/ch3-pavilion-batch01-20261118','tool':'built-in image_gen.imagegen','generationCalls':len(records)+len(json.loads((ROOT/'sources/initial-attempts/generation-records.json').read_text())),'currentCandidates':2,'initialAttempts':'sources/initial-attempts/generation-records.json','status':'generated','selected':False,'approved':False,'canonicalMainSceneSize':[314,206],'portraitSizeStill':[564,278],'628Studies':'Archived unchanged; not selected for production. No 628 artwork used as input to these generations.','candidates':candidates})
reference_palettes={name:len(Image.open(ROOT/'references'/name).convert('RGB').getcolors(314*206)) for name in ['prologue-reception.png','chapter-01-foyer.png','chapter-02-groundskeeper.png']}
put('qa.json',{'technicalRequirementOverall':'NOT PASSED: native-grid authorship unproven; see per-candidate source sizes.','candidates':qa,'approvedReferenceUniqueRGBColors':reference_palettes,'paletteInterpretation':'Counts describe tonal variety only, not an approval rule or automatic style test. No output was palette-filtered.','historyPreservation':{'result':'PASS','pin':pins['commit'],'filesChecked':len(pins['files'])},'referenceIntegrity':{'result':'PASS','referencesChecked':len(refs)},'unchangedPortraits':[{'id':i['id'],'file':'../v04/'+i['candidate'],'sha256':i['sha256'],'dimensions':i['dimensions']} for i in json.loads((BASE/'v04/manifest.json').read_text())['candidates'] if i['id'] not in ['CH3-A01-restroom','CH3-A04-verification']],'scope':'Only two main-scene review candidates. No narrative, gameplay, selected assets, production registry, portrait changes or approvals.'})

def art(src,w,h,alt):
    return f'<div class="viewport"><img class="art" src="{src}" width="{w}" height="{h}" data-w="{w}" data-h="{h}" alt="{html.escape(alt)}"></div>'
cards=[]
for item,q in zip(candidates,qa):
    ident=item['id']; title='A01 — Restroom' if 'A01' in ident else 'A04 — Verification stage'
    notes=''.join('<li>'+html.escape(n)+'</li>' for n in q['visualInspection']['observations'])
    prompt=html.escape((ROOT/item['prompt']).read_text())
    srcsize='×'.join(map(str,item['actualSourceDimensions']))
    cards.append(f'''<article class="candidate" id="{ident}"><h2>{title}</h2><p><strong>{ident}</strong> · Generated / unselected</p>
<p class="notice">Returned source: <strong>{srcsize}</strong>. Working export: <strong>314×206</strong>{' (derived from this fresh generation)' if item['derivedExport'] else ''}. Original native-grid authorship remains unproven.</p>
{art(item['candidate'],314,206,title+' fresh working export')}<p class="meta">Working SHA-256: <code>{item['sha256']}</code></p>
<p><a href="{item['candidate']}">314×206 PNG</a> · <a href="{item['preview4x']}">Exact 4× PNG</a> · <a href="{item['source']}">Untouched generator source ({srcsize})</a></p>
<h3>Previous 314 version → fresh generation</h3><p class="meta">Left: v04. Right: v06. Each cell is 314×206 at 1×; the 4× control applies exact integer dimensions. No 628 experiment is used.</p>
{art(item['previousComparison'],628,206,title+' previous v04 left and fresh v06 right')}
<p><a href="comparisons/{ident}-previous-current-4x.png">Side-by-side 4× PNG</a></p>
<h3>Pixel-density comparison</h3><p class="meta">Left to right: fresh Chapter 3, approved Prologue reception, approved Chapter 1 foyer, selected Chapter 2 groundskeeper. Same logical dimensions and display scale.</p>
{art(item['approvedDensityComparison'],1256,206,title+' beside approved earlier chapter scenes')}
<p><a href="comparisons/{ident}-approved-density-4x.png">Density comparison 4× PNG</a></p>
<h3>Inspection notes</h3><ul>{notes}</ul><p class="meta">Palette: {q['palette']['workingUniqueRGB']} unique RGB colors in the working export; no quantization. Pixel-density matching remains an Art Director judgment.</p>
<details><summary>Exact submitted prompt</summary><pre>{prompt}</pre></details></article>''')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 3 — two fresh 314 scenes / v06</title>
<style>*{box-sizing:border-box}body{margin:0;background:#15252a;color:#f3e9d9;font:16px/1.55 system-ui,sans-serif}main{max-width:1380px;margin:auto;padding:24px}h1{font-size:30px;line-height:1.2}h2{font-size:24px}h3{font-size:19px}a{color:#9de0db}code{overflow-wrap:anywhere}nav,.controls{display:flex;flex-wrap:wrap;gap:12px;margin:18px 0}.controls{position:sticky;top:0;background:#15252af5;padding:12px 0;z-index:2}button{font:inherit;padding:9px 16px;border:1px solid #819c9f;background:#25444d;color:inherit;border-radius:4px;cursor:pointer}button[aria-pressed=true]{background:#f4d3ac;color:#17272c}.notice{padding:16px;background:#563e31;border-left:4px solid #f0b984}.viewport{max-width:100%;overflow:auto;background:#091519;border:1px solid #55727a}.art{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}article{border-top:1px solid #55727a;margin-top:36px;padding-top:18px}.meta{color:#c5d5d6;font-size:14px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#0c1c20;padding:18px;font-size:13px}li{margin:8px 0}.characters{display:flex;gap:16px;flex-wrap:wrap}.characters figure{margin:0;max-width:100%}figcaption{margin:8px 0}</style>
<main><h1>Chapter 3 — fresh main scenes at original density</h1><p><strong>314×206 main scenes retained across the game. Two new candidates · generated / unselected.</strong></p>
<p>Fresh restroom and verification-stage illustrations, guided primarily by the selected Prologue–Chapter 2 scenes for detail density, line weight and shading. The 628 study remains archived and is not selected for production.</p>
<p class="notice"><strong>Technical limit:</strong> source dimensions and derivation are disclosed for each scene below. A 314×206 export and a correct 4× preview do not demonstrate native-grid authorship. No sharpening, palette filtering, extra outline edits or automatic pixelation pass was applied to conceal oversized sources.</p>
<nav><a href="#CH3-A01-restroom-v06">A01 restroom</a><a href="#CH3-A04-verification-v06">A04 verification</a><a href="../v04/">Previous six-candidate set</a><a href="../v05-628-regeneration/">Archived 628 study</a><a href="manifest.json">Candidate hashes / provenance</a><a href="qa.json">Technical QA</a></nav>
<div class="controls"><button data-scale="1" aria-pressed="true">1× native-size export</button><button data-scale="4" aria-pressed="false">4× nearest-neighbor review</button></div>
<p class="meta">Every image uses exact integer dimensions. Large images scroll within their container; mobile views never shrink the artwork to fractional scale.</p>
CARDS
<h2>Character identity references — unchanged portraits</h2><p>A02, A03, A05 and A06 remain byte-for-byte unchanged at 564×278. These portraits guide recognizable small scene figures; they were not regenerated. <a href="../v04/#composites">Existing portrait composite proofs</a>.</p><div class="characters"><figure><figcaption>Male attendant identity</figcaption>ATTENDANT</figure><figure><figcaption>Female presenter identity</figcaption>PRESENTER</figure></div>
<h2>Review gate</h2><p>Nate’s Art Director review is required for the two new scenes, their density match, small character identities and agreement with the unchanged portrait architecture. No new candidate is selected, approved or integrated. No next batch has begun.</p>
<h2>Records</h2><p><a href="sources/generation-records.json">Fresh generation records</a> · <a href="sources/initial-attempts/generation-records.json">Retained initial attempts</a> · <a href="sources/reference-manifest.json">Reference source paths and hashes</a> · <a href="sources/brief-provenance.json">Owner decision and registered briefs</a> · <a href="sources/history-pins.json">Preserved earlier hashes</a> · <a href="PNG_SHA256SUMS.txt">PNG checksums</a> · <a href="SOURCE_SHA256SUMS.txt">Package checksums</a> · <a href="browser-qa.json">Browser QA</a></p><p class="meta">Four generation calls: two initial attempts retained for provenance, then one density-focused regeneration per scene. All HISTORY_COUNT earlier review files match source commit 2efd2a5. Narrative, gameplay, approved/selected artwork and production registry remain unchanged.</p>
</main><script>document.querySelectorAll('[data-scale]').forEach(b=>b.onclick=()=>{const scale=Number(b.dataset.scale);document.querySelectorAll('img.art').forEach(i=>{i.width=Number(i.dataset.w)*scale;i.height=Number(i.dataset.h)*scale});document.querySelectorAll('[data-scale]').forEach(n=>n.setAttribute('aria-pressed',String(n===b)));});</script></html>'''
page=page.replace('CARDS','\n'.join(cards)).replace('HISTORY_COUNT',str(len(pins['files']))).replace('ATTENDANT',art('references/attendant-identity.png',564,278,'Unchanged attendant identity')).replace('PRESENTER',art('references/presenter-identity.png',564,278,'Unchanged presenter identity'))
(ROOT/'index.html').write_text(page)
(ROOT/'README.md').write_text('''# Chapter 3 v06 — two fresh 314×206 main scenes

Built-in imagegen was used for two initial attempts and one targeted density regeneration per scene (four calls total). See `sources/generation-records.json` and `sources/initial-attempts/generation-records.json` for exact prompts, references, actual source sizes and hashes. The two current candidates remain generated/unselected. Native-grid limitations are explicit in `qa.json` and the gallery.

The original 314×206 contract is retained. The 628 study remains archived, unchanged, unselected and excluded from the new generation inputs. A02/A03/A05/A06 remain unchanged at 564×278. No narrative, gameplay, selected artwork or production registry edits; no approval or next batch.

`python3 build_review.py` exports dimensionally correct working images and exact 4× previews, side-by-side previous/new comparisons, and same-scale comparisons with approved earlier chapters. It never sharpens, quantizes or adds outlines. If a returned source is oversized, its reduction is explicitly identified as a derived export, not native-grid authorship.

Run `qa-browser.cjs`, then rebuild to include its report and screenshots in checksum lists.
''')
pngs=sorted(p for p in ROOT.rglob('*.png') if p.is_file())
(ROOT/'PNG_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(ROOT).as_posix()}\n' for p in pngs))
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and p.suffix!='.png' and p.name!='SOURCE_SHA256SUMS.txt')
(ROOT/'SOURCE_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(ROOT).as_posix()}\n' for p in files))
print(json.dumps({'candidates':[{'id':i['id'],'sha256':i['sha256'],'sourceSize':i['actualSourceDimensions']} for i in candidates],'historicalFilesUnchanged':len(pins['files'])},indent=2))
