"""Package a fresh imagegen result; never claim resampling proves native authorship."""
from pathlib import Path
from PIL import Image
import hashlib
import json
import html

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent
ID = 'CH3-A01-restroom-628-v05'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_json(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2) + '\n')

record = json.loads((ROOT/'sources/generation-record.json').read_text())
source = ROOT/record['source']
assert digest(source) == record['sourceSha256']
raw = Image.open(source)
assert list(raw.size) == record['actualSourceDimensions']
pins = json.loads((ROOT/'sources/history-pins.json').read_text())
for old in pins['files']:
    assert digest(BASE/old['file']) == old['sha256'], old['file']
for ref, expected in zip(record['referencesInOrder'], record['referenceHashes']):
    assert digest(ROOT/ref) == expected

for folder in ['candidates', 'previews', 'comparisons']:
    (ROOT/folder).mkdir(exist_ok=True)
working = raw.convert('RGB').resize((628, 412), Image.Resampling.NEAREST)
candidate = ROOT/f'candidates/{ID}.png'
working.save(candidate)
preview = working.resize((1256, 824), Image.Resampling.NEAREST)
preview.save(ROOT/f'previews/{ID}-2x.png')
previous = Image.open(BASE/'v04/candidates/CH3-A01-restroom-v04.png').convert('RGB')
previous.resize((1256, 824), Image.Resampling.NEAREST).save(ROOT/'comparisons/previous-v04-4x.png')

# Independent crops for face/outline inspection, with coordinates recorded below.
fresh_crop = [410, 184, 488, 282]
previous_crop = [198, 75, 251, 143]
working.crop(fresh_crop).resize((312, 392), Image.Resampling.NEAREST).save(ROOT/'comparisons/fresh-attendant-detail-4x.png')
previous.crop(previous_crop).resize((212, 272), Image.Resampling.NEAREST).save(ROOT/'comparisons/previous-attendant-detail-4x.png')
assert preview.tobytes() == working.resize((1256,824), Image.Resampling.NEAREST).tobytes()
assert preview.resize((628,412), Image.Resampling.NEAREST).tobytes() == working.tobytes()
rgba = working.convert('RGBA')
qa = {
    'candidateId': ID, 'status': 'generated/unselected',
    'freshGeneration': {'result':'PASS', 'generationCalls':1, 'evidence':'Untouched new imagegen output with two design references; previous candidate is used only as a comparison.'},
    'requestedSourceDimensions': {'result':'FAIL', 'requested':[628,412], 'returned':list(raw.size)},
    'originalNativeGridAuthorship': {'result':'UNPROVEN / REQUIREMENT NOT PASSED', 'reason':'Imagegen returned a larger RGB raster. The 628x412 working export is a nearest-neighbor reduction of this new output; it is not evidence of directly authored 628x412 pixel clusters.'},
    'workingExportDimensions': {'result':'PASS', 'dimensions':list(working.size), 'mode':working.mode},
    'previewDimensions': {'result':'PASS','dimensions':list(preview.size),'scale':2,'method':'Pillow NEAREST; every output 2x2 block exactly equals its source pixel'},
    'alpha': {'result':'PASS', 'requirement':'Opaque environment', 'extrema':list(rgba.getchannel('A').getextrema())},
    'palette': {'sourceUniqueRGBColors':len(raw.convert('RGB').getcolors(raw.width*raw.height)), 'workingUniqueRGBColors':len(working.getcolors(working.width*working.height)), 'quantizationApplied':False, 'assessment':'No numeric palette limit in this trial. Numerous tonal values remain; deliberate native clustering and lack of antialiasing cannot be certified.'},
    'historyPreservation': {'result':'PASS','pin':pins['commit'],'filesChecked':len(pins['files'])},
    'referenceIntegrity': {'result':'PASS','referencesChecked':len(record['referencesInOrder'])},
    'visualInspection': {'result':'REVIEW REQUIRED', 'observations':[
        'Same restroom/bench/counter layout and cream/coral/slate-blue materials; fresh drawing, so small contours and proportions vary.',
        'Seated male attendant retains dark side-part hair with gray temples, rectangular glasses, cream shirt, dark tie and teal vest; exact face correspondence remains for Nate to judge.',
        'Desktop contactless gadget absent; slotted intercom/microphone and wall gate reader retained.',
        'RESTROOM sign readable; visible sinks, mirrors, pipes, bin, stalls and gate retained. No occupied stall, protagonist face or embodied Original.',
        'Thin contours replace the prior hand-inked outline treatment. Fine tonal variation/softness remains in the generated source; this is not a certified native pixel-art pass.'
    ]},
    'comparisonCrops': {'fresh':{'source':f'candidates/{ID}.png','box':fresh_crop,'scale':4}, 'previous':{'source':'../v04/candidates/CH3-A01-restroom-v04.png','box':previous_crop,'scale':4},'note':'Independent face crops, not registered pixel-difference proofs.'},
    'scope': {'otherFiveCandidatesChanged':False,'productionContractChanged':False,'narrativeChanged':False,'approved':False,'integrated':False}
}
write_json('qa.json', qa)
manifest = {
    'title':'Chapter 3 / A01 fresh regeneration / 628 trial',
    'candidateId':ID, 'status':'generated', 'selected':False, 'approved':False, 'assetPath':None,
    'workingFile':f'candidates/{ID}.png','sha256':digest(candidate),
    'workingDimensions':[628,412], 'preview':f'previews/{ID}-2x.png',
    'generation':record, 'derivation':{'input':record['source'],'operation':'RGB conversion + nearest-neighbor reduction of the NEW generation to 628x412; no old image enlargement, sharpening, thresholding, repainting or palette quantization.', 'output':f'candidates/{ID}.png'},
    'technicalRequirementPassed':False, 'qa':'qa.json', 'previousSixCandidateGallery':'../v04/',
    'canonicalSceneDimensionsStill':[314,206]
}
write_json('manifest.json',manifest)
prompt = (ROOT/record['prompt']).read_text()
page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 3 — fresh A01 / 628 trial</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#15252a;color:#f3e9d9;font:16px/1.55 system-ui,sans-serif}main{max-width:1360px;margin:auto;padding:24px}h1{font-size:28px;line-height:1.2}h2{font-size:21px}a{color:#9de0db}code{overflow-wrap:anywhere}button{font:inherit;padding:9px 16px;border:1px solid #819c9f;background:#25444d;color:inherit;border-radius:4px;cursor:pointer}button[aria-pressed=true]{background:#f4d3ac;color:#17272c}nav,.controls{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0}.notice{padding:16px;background:#563e31;border-left:4px solid #f0b984}.viewport{overflow:auto;max-width:100%;background:#0a1519;border:1px solid #55727a}.viewport img{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}.details{display:flex;gap:24px;flex-wrap:wrap}.details figure{margin:0;max-width:100%}figcaption{margin:8px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#0c1c20;padding:18px;font-size:13px}table{border-collapse:collapse;width:100%}td,th{padding:10px;border-bottom:1px solid #55727a;text-align:left;vertical-align:top}.meta{font-size:14px;color:#c5d5d6}.candidate{margin:24px 0}li{margin:6px 0}</style>
<main><h1>Chapter 3 — fresh restroom regeneration</h1>
<p><strong>CH3-A01-restroom-628-v05 · Generated / unselected</strong></p>
<p>A new drawing requested at 628×412, keeping the established restroom composition and attendant design. This is a one-image size trial. The other five candidates remain in the previous gallery.</p>
<p class="notice"><strong>Native-source requirement remains unmet.</strong> The generator returned SOURCE_SIZE, despite the 628×412 request. The displayed 628×412 working image is a nearest-neighbor reduction of that <em>new</em> generation. It is not an enlargement of the old 314×206 scene, and it does not demonstrate original native-grid authorship.</p>
<nav><a href="../v04/">Previous six-candidate gallery</a><a href="manifest.json">Manifest + hashes</a><a href="qa.json">Technical / visual QA</a><a href="SOURCE_FILE">Untouched new generator output</a><a href="prompts/CH3-A01-restroom-628-v05.txt">Exact submitted prompt</a></nav>
<section class="candidate"><h2>Compare at the same display size</h2><p>Switch between the new 628×412 working image at 2× and the previous 314×206 image at 4×. Both occupy exactly 1256×824 display pixels. Images scroll; they never shrink to fit.</p>
<div class="controls"><button data-view="new2" aria-pressed="true">Fresh generation · 2×</button><button data-view="old4" aria-pressed="false">Previous v04 · 4×</button><button data-view="new1" aria-pressed="false">Fresh generation · 1×</button></div>
<p id="view-label" class="meta">Fresh generation · 628×412 working export · 2× nearest-neighbor preview</p>
<div class="viewport"><img id="scene" src="previews/CH3-A01-restroom-628-v05-2x.png" width="1256" height="824" alt="Freshly generated restroom with seated male attendant; no desktop contactless device"></div>
<p class="meta">Working PNG SHA-256: <code>CANDIDATE_HASH</code></p></section>
<h2>What changed</h2><ul><li>Freshly drawn room and small seated attendant; the composition, cream/coral/slate-blue palette, outfit and reassuring expression are retained, with small drawing differences.</li><li>Desktop contactless device remains absent. Intercom, microphone and wall gate reader remain.</li><li>Thin generated contours replace the previous 314-grid outline edits. No sharpening, extra inking or palette reduction was applied.</li><li>628×412 working export and exact 2× preview replace the previous 314×206 / 4× presentation for this trial.</li></ul>
<h2>Attendant outline details</h2><p>Independent crops at 4× their respective working grids. These are detail aids, not aligned pixel-difference proofs.</p><div class="details"><figure><figcaption>Fresh generation · 628-grid working export</figcaption><div class="viewport"><img src="comparisons/fresh-attendant-detail-4x.png" width="312" height="392" alt="Fresh attendant face detail"></div></figure><figure><figcaption>Previous v04 · 314-grid</figcaption><div class="viewport"><img src="comparisons/previous-attendant-detail-4x.png" width="212" height="272" alt="Previous attendant face detail"></div></figure><figure><figcaption>Identity reference used for generation · 1×</figcaption><div class="viewport"><img src="../v03/candidates/CH3-A03-attendant-idle-v03.png" width="564" height="278" alt="Established male attendant portrait identity"></div></figure></div>
<h2>Validation and selection</h2><table><tr><th>Check</th><th>Result</th></tr><tr><td>Fresh generation / historical preservation</td><td>Pass · one new tool call; all HISTORY_COUNT earlier review files unchanged.</td></tr><tr><td>Working size / opaque alpha / 2× blocks</td><td>Pass · 628×412 RGB; fully opaque; every preview 2×2 block matches its working pixel.</td></tr><tr><td>Requested generator source size</td><td>Fail · SOURCE_SIZE returned.</td></tr><tr><td>Original 628-grid authorship / deliberate clusters</td><td>Unproven · larger generated raster was reduced; tonal variation and some softness remain.</td></tr><tr><td>Palette</td><td>COLOR_COUNT unique RGB colors in the working image; no quantization or invented palette limit.</td></tr><tr><td>Selection / production</td><td>Pending Nate. No approval, gameplay integration or canonical dimension change.</td></tr></table>
<p>For selection: judge whether the fresh 628 working image at 2× improves the attendant and contours enough to pursue this direction. A future 628-grid rule is only a proposal; this output does not establish that the generator can author that grid directly.</p>
<h2>Provenance</h2><p class="meta">Original source filename: <code>exec-c4c735d2-5d99-4b45-adb4-73b8f388a906.png</code><br>Source SHA-256: <code>SOURCE_HASH</code></p><p><a href="sources/generation-record.json">Generation record + reference hashes</a> · <a href="sources/brief-provenance.json">Registered prompt / authorized size override</a> · <a href="sources/history-pins.json">Preserved historical hashes</a> · <a href="PNG_SHA256SUMS.txt">PNG checksums</a> · <a href="SOURCE_SHA256SUMS.txt">Package checksums</a> · <a href="browser-qa.json">Browser checks</a></p>
<details><summary>Exact generation prompt</summary><pre>PROMPT_TEXT</pre></details>
</main><script>
const views={new2:['previews/CH3-A01-restroom-628-v05-2x.png',1256,824,'Fresh generation · 628×412 working export · 2× nearest-neighbor preview'],old4:['comparisons/previous-v04-4x.png',1256,824,'Previous v04 · 314×206 candidate · 4× nearest-neighbor preview'],new1:['candidates/CH3-A01-restroom-628-v05.png',628,412,'Fresh generation · 628×412 working export · 1×']};
document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>{const [src,w,h,label]=views[b.dataset.view],img=document.querySelector('#scene');img.src=src;img.width=w;img.height=h;document.querySelector('#view-label').textContent=label;document.querySelectorAll('[data-view]').forEach(n=>n.setAttribute('aria-pressed',String(n===b)));});
</script></html>'''
for token, value in {'SOURCE_SIZE':f'{raw.width}×{raw.height}', 'SOURCE_FILE':record['source'], 'CANDIDATE_HASH':digest(candidate), 'SOURCE_HASH':digest(source), 'HISTORY_COUNT':str(len(pins['files'])), 'COLOR_COUNT':str(qa['palette']['workingUniqueRGBColors']), 'PROMPT_TEXT':html.escape(prompt)}.items():
    page=page.replace(token,value)
(ROOT/'index.html').write_text(page)
(ROOT/'README.md').write_text(f'''# A01 fresh regeneration / 628 working trial

Generated/unselected. One new imagegen call requested 628×412. Actual untouched output: {raw.width}×{raw.height}.

The 628×412 working PNG is a nearest-neighbor reduction of this new generation, not an enlargement of the previous candidate. Its 2× preview is exactly 1256×824. Native-grid authorship remains unproven; requested source dimensions failed. See `qa.json` and `manifest.json`.

Candidate: {ID}
SHA-256: {digest(candidate)}

Earlier {len(pins['files'])} review files are preserved and checked against commit {pins['commit']}. Other five candidates, narrative, production assets and canonical scene dimensions are unchanged. No approval or integration.

Rebuild with Python 3 + Pillow: `python3 build_review.py`. Run `qa-browser.cjs`, then rebuild to include browser reports/screenshots in checksum lists.
''')
pngs=sorted(p for p in ROOT.rglob('*.png') if p.is_file())
(ROOT/'PNG_SHA256SUMS.txt').write_text(''.join(f'{digest(p)}  {p.relative_to(ROOT).as_posix()}\n' for p in pngs))
sources=sorted(p for p in ROOT.rglob('*') if p.is_file() and p.suffix != '.png' and p.name not in ['SOURCE_SHA256SUMS.txt'])
(ROOT/'SOURCE_SHA256SUMS.txt').write_text(''.join(f'{digest(p)}  {p.relative_to(ROOT).as_posix()}\n' for p in sources))
print(json.dumps({'candidateId':ID,'sha256':digest(candidate),'sourceSize':raw.size,'workingSize':working.size,'historicalFilesUnchanged':len(pins['files']),'nativeAuthorship':'UNPROVEN'},indent=2))
