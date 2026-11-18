"""Rebuild review exports from immutable image_gen sources; never draw artwork.

Source rasters and their alpha are retained. Full-frame NEAREST exports are
dimension-correct review derivatives, not proof of native-grid authorship.
"""
from pathlib import Path
from collections import Counter
from html import escape
import hashlib
import json
import subprocess
from PIL import Image

R = Path(__file__).resolve().parent
ROOT = R.parents[4]
BASE = '2a1022ba7d96f9cf887402fc59c8266f81be577c'
BRANCH = 'art/ch3-pavilion-batch01-20261118'
NARRATIVE = '857ffdf1bc9432cf4bbbfd7819f5f430a06d9036'
SOURCE_ROOT = '/Users/MrDashiki/.codex/generated_images/01a1f095-e80e-7773-9e72-40383ff7cd50/'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(name, data):
    (R / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def img(path, size, label):
    w, h = size
    return f'<div class="viewport"><img class="art" src="{path}" width="{w}" height="{h}" data-w="{w}" data-h="{h}" alt="{escape(label)}"></div>'


def link(path, label):
    return f'<a href="{path}">{escape(label)}</a>'


briefs = json.loads((R / 'sources/registered-briefs.json').read_text())
calls = json.loads((R / 'tool-calls.json').read_text())
active = [c for c in calls if c['role'] == 'current candidate source']
assert len(active) == 6
records = []
for b in briefs['records']:
    cid = b['id']
    c = next(c for c in active if c['candidateId'] == cid)
    source = R / 'generation-source' / c['filename']
    original = Image.open(source)
    size = tuple(map(int, b['brief']['dimensions'].split('x')))
    foreground = b['brief']['kind'] == 'portrait'
    mode = 'RGBA' if foreground else 'RGB'
    native = original.convert(mode).resize(size, Image.Resampling.NEAREST)
    candidate = f'candidates/{cid}-v01.png'
    preview = f'previews/{cid}-v01-4x.png'
    native.save(R / candidate)
    native.resize((size[0] * 4, size[1] * 4), Image.Resampling.NEAREST).save(R / preview)
    pixels = list(native.getdata())
    visible = [p[:3] for p in pixels if not foreground or p[3] > 0]
    palette = Counter(visible)
    alpha = Counter(p[3] for p in pixels) if foreground else Counter({255: len(pixels)})
    partial = sum(n for a, n in alpha.items() if 0 < a < 255)
    alpha_info = {'fullyTransparentPixels': alpha[0], 'fullyOpaquePixels': alpha[255],
                  'partialAlphaPixels': partial, 'distinctAlphaValues': len(alpha),
                  'spriteBounds': list(native.getchannel('A').getbbox()) if foreground else None,
                  'hardAlphaRequirement': 'PASS' if not foreground or partial == 0 else 'FAIL — generated partial alpha preserved'}
    records.append({'id': cid, 'catalogueKey': b['catalogueKey'], 'title': b['brief']['title'],
                    'status': 'generated', 'selected': False, 'assetPath': None,
                    'candidate': candidate, 'sha256': sha(R / candidate), 'dimensions': list(size), 'mode': mode,
                    'preview4x': preview, 'previewSha256': sha(R / preview),
                    'source': f'generation-source/{c["filename"]}', 'sourceSha256': sha(source),
                    'originalSourceFilename': c['filename'], 'originalToolPath': SOURCE_ROOT + c['filename'],
                    'sourceDimensions': list(original.size), 'sourceMode': original.mode,
                    'prompt': c['prompt'], 'promptSha256': sha(R / c['prompt']),
                    'referencedImagesInOrder': c['references'],
                    'referenceHashes': [sha(R / p) for p in c['references']],
                    'transparent_background': foreground, 'alpha': alpha_info,
                    'palette': {'visibleRgbColors': len(palette), 'dominant16': [{'rgb': list(k), 'pixels': v} for k, v in palette.most_common(16)],
                                'processing': 'No palette quantization, recoloring or dithering.'},
                    'authoredAtRequestedNativeSize': original.size == size,
                    'processing': 'Full-frame NEAREST sampling to requested review dimensions; RGB conversion for opaque backgrounds, original generated alpha preserved for foregrounds. No crop, blur, paint, sharpening, palette reduction or alpha threshold. Exact 4x NEAREST preview.',
                    'aspectRatioChangePercent': ((size[0] / size[1]) / (original.width / original.height) - 1) * 100})

composites = []
for name, bi, fi in [('attendant', 1, 2), ('presenter', 4, 5)]:
    bg, fg = records[bi], records[fi]
    background = Image.open(R / bg['candidate']).convert('RGBA')
    foreground = Image.open(R / fg['candidate']).convert('RGBA')
    comp = Image.alpha_composite(background, foreground).convert('RGB')
    path = f'composites/{name}-background-foreground.png'
    prev = f'composites/{name}-background-foreground-4x.png'
    comp.save(R / path)
    comp.resize((2256, 1112), Image.Resampling.NEAREST).save(R / prev)
    proofs = []
    for color, label in [((255, 255, 255), 'white'), ((25, 34, 46), 'dark')]:
        proof = Image.new('RGBA', (564, 278), color + (255,))
        proof = Image.alpha_composite(proof, foreground).convert('RGB')
        pp = f'composites/{name}-foreground-on-{label}.png'
        proof.save(R / pp)
        proofs.append({'file': pp, 'sha256': sha(R / pp)})
    composites.append({'character': name, 'backgroundId': bg['id'], 'foregroundId': fg['id'],
                       'file': path, 'sha256': sha(R / path), 'preview4x': prev, 'previewSha256': sha(R / prev),
                       'dimensions': [564, 278], 'method': 'Pillow alpha_composite, same full-canvas anchor; no movement or rescaling between layers.',
                       'edgeProofs': proofs})

for c in calls:
    c['sha256'] = sha(R / 'generation-source' / c['filename'])
    c['sourceDimensions'] = list(Image.open(R / 'generation-source' / c['filename']).size)
    c['originalToolPath'] = SOURCE_ROOT + c['filename']
    c['promptSha256'] = sha(R / c['prompt'])
    c['referenceHashes'] = [sha(R / p) for p in c['references']]
save('generation-records.json', {'tool': 'built-in image_gen.imagegen', 'calls': calls})
save('manifest.json', {'repository': 'InterstellarHarvest/CYOA-storyboard', 'branch': BRANCH,
                       'generationBaseCommit': BASE, 'approvedNarrativeBlob': NARRATIVE,
                       'status': 'generated', 'selected': False, 'gate': 'Nate visual selection; Batch B not started',
                       'catalogueChanges': 'None. Exact catalogue prompts remain unchanged; later owner steering is preserved separately and appended to relevant submissions.',
                       'nativeAuthorshipRequirement': 'NOT MET — tool returned larger rasters. These six dimension-correct review exports were NEAREST sampled. Do not represent them as original native-resolution drawings.',
                       'candidates': records, 'composites': composites})
save('palette.json', {c['id']: c['palette'] for c in records})

hashlines = ['# Six current candidates — generated / unselected\n']
for c in records:
    hashlines.append(f'- `{c["id"]}` — `{c["candidate"]}`\n  SHA-256: `{c["sha256"]}`\n')
(R / 'CANDIDATE_HASHES.md').write_text('\n'.join(hashlines))

css = '''
:root{color-scheme:dark;--bg:#182430;--panel:#233341;--ink:#f4ead5;--line:#586c7b;--accent:#f0ad95;--dim:#bdccd1}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,sans-serif}header,main,footer{max-width:1500px;margin:auto;padding:28px}h1{font-size:clamp(30px,4vw,48px);line-height:1.15}h2{font-size:26px}h3{font-size:19px}.eyebrow{color:var(--accent);letter-spacing:.1em;font-size:12px}.status{border:1px solid var(--accent);padding:6px 12px;display:inline-block}.note{padding:16px;background:#433635;border-left:4px solid var(--accent)}p{max-width:1050px}nav,.links,.toolbar{display:flex;gap:14px;flex-wrap:wrap;align-items:center}a{color:var(--accent);text-underline-offset:3px}.toolbar{position:sticky;top:0;z-index:5;background:#182430f5;padding:12px 28px;border-block:1px solid var(--line)}button{font:inherit;background:var(--panel);color:var(--ink);border:1px solid var(--line);padding:6px 14px;cursor:pointer}button[aria-pressed=true]{background:var(--accent);color:var(--bg)}section{padding:20px 0;border-bottom:1px solid var(--line);scroll-margin-top:100px}.card{padding:18px;border:1px solid var(--line);background:var(--panel);margin:18px 0}.viewport{max-width:100%;overflow:auto;padding:8px;background:repeating-conic-gradient(#344653 0% 25%,#263641 0% 50%) 50%/16px 16px}img{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.grid>div{min-width:0}code,pre{font:12px/1.6 ui-monospace,monospace;overflow-wrap:anywhere}pre{white-space:pre-wrap;max-height:420px;overflow:auto}details{margin:14px 0;border:1px solid var(--line);padding:12px}summary{cursor:pointer;color:var(--accent)}.muted{color:var(--dim);font-size:14px}.hash{display:block;user-select:all}table{border-collapse:collapse;display:block;overflow:auto}td,th{border:1px solid var(--line);padding:8px;text-align:left}a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid #fff;outline-offset:3px}@media(max-width:800px){.grid{grid-template-columns:1fr}header,main,footer{padding:18px}.toolbar{padding:10px}.card{padding:10px}}
'''
(R / 'gallery.css').write_text(css)
parts = ['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 3 Batch A — The People’s Pavilion artwork review</title><link rel="stylesheet" href="gallery.css"><body>',
         '<header><div class="eyebrow">THE ACCEPTABLE ERROR · CHAPTER 3 · BATCH A</div><h1>The People’s Pavilion<br>One Experience Per Person</h1><p class="status">SIX GENERATED CANDIDATES · UNSELECTED</p><p>A distinct Pavilion environment and two new human characters. Latest owner direction calls for a different palette and architecture and prohibits repeating the receptionist. The early reception-like studies are superseded.</p><p class="note"><strong>Technical limitation:</strong> The generator returned larger rasters, despite the native-size prompts. The files below are dimension-correct nearest-neighbor review exports, not verified original native-grid artwork. Foreground alpha is preserved and may include partial transparency. These failures remain visible in QA; no image is approved.</p><nav><a href="#restroom">Restroom set</a><a href="#stage">Verification set</a><a href="#composites">Layer composites</a><a href="#references">Approved references</a><a href="#evidence">QA and provenance</a></nav></header>',
         '<div class="toolbar"><span>View:</span><button data-scale="1" aria-pressed="true">Native dimensions · 1×</button><button data-scale="4" aria-pressed="false">Nearest-neighbor · 4×</button><span class="muted">Images scroll without fractional fit-to-width scaling.</span></div><main>']
for title, anchor, group in [('Real restroom and attendant', 'restroom', records[:3]), ('Human verification and presenter', 'stage', records[3:])]:
    parts.append(f'<section id="{anchor}"><h2>{title}</h2>')
    for c in group:
        parts.append(f'<article class="card candidate" id="{c["id"]}"><h3>{c["id"]} · {escape(c["title"])}</h3><p><code>{escape(c["catalogueKey"])}</code> · {c["dimensions"][0]}×{c["dimensions"][1]} {c["mode"]} · generated / unselected</p>')
        parts.append(img(c['candidate'], c['dimensions'], c['title']))
        parts.append(f'<p><code class="hash">SHA-256 {c["sha256"]}</code></p><div class="links">' + link(c['candidate'], 'Dimension-correct PNG') + link(c['preview4x'], 'Exact 4× PNG') + link(c['source'], 'Untouched generator original') + link(c['prompt'], 'Exact submitted prompt') + '</div>')
        parts.append(f'<p class="muted">Generator original: {c["sourceDimensions"][0]}×{c["sourceDimensions"][1]} {c["sourceMode"]}. {c["palette"]["visibleRgbColors"]:,} visible RGB colors. ' + (f'{c["alpha"]["fullyTransparentPixels"]:,} fully transparent pixels; {c["alpha"]["partialAlphaPixels"]:,} partial-alpha pixels.' if c['mode'] == 'RGBA' else 'Opaque background.') + '</p>')
        parts.append('<details><summary>Catalogue brief and complete submitted prompt</summary><h4>Exact catalogue prompt</h4><pre>' + escape(next(b['brief']['prompt'] for b in briefs['records'] if b['id'] == c['id'])) + '</pre><h4>Complete submission, including global direction and applicable owner steering</h4><pre>' + escape((R / c['prompt']).read_text()) + '</pre></details></article>')
    parts.append('</section>')
parts.append('<section id="composites"><h2>Foreground / background composition proofs</h2><p>Each is a literal full-canvas alpha composition. The backgrounds are independent generation calls with closer perspectives; neither is an enlargement or crop of its main scene.</p>')
for c in composites:
    parts.append(f'<article class="card"><h3>{c["character"].title()} · matching background + idle foreground</h3>' + img(c['file'], c['dimensions'], c['character'] + ' layer composite') + '<div class="links">' + link(c['file'], '1× composite') + link(c['preview4x'], '4× composite') + '</div><details><summary>Foreground edge checks on white and dark backings</summary><div class="grid">')
    for p in c['edgeProofs']:
        parts.append('<div>' + img(p['file'], [564, 278], p['file']) + '</div>')
    parts.append('</div></details></article>')
parts.append('</section><section id="references"><h2>Approved continuity references · unchanged</h2><p>The reception establishes the game family. The warm House and green industrial Biology Park demonstrate chapter-level variation. These six files are byte-exact copies of approved references, not new candidates.</p><div class="grid">')
for r in json.loads((R / 'references/manifest.json').read_text()):
    path = 'references/' + r['file']
    size = Image.open(R / path).size
    parts.append('<div class="card"><h3>' + escape(r['file']) + '</h3>' + img(path, size, 'Approved ' + r['file']) + '<p><code>' + escape(r['sourcePath']) + '</code></p></div>')
parts.append('</div></section><section id="evidence"><h2>QA, exact prompts and immutable sources</h2><p>File dimensions, nearest-neighbor previews, compositing, hashes and source preservation are mechanically checked. Native-grid authorship and strict pixel-sharp alpha are separate requirements and are not silently passed. Read the visual QA notes before selecting.</p><div class="links">')
for path, title in [('manifest.json', 'Six candidates and hashes'), ('CANDIDATE_HASHES.md', 'Copyable SHA-256 list'), ('qa.json', 'Technical QA'), ('browser-qa.json', 'Browser and zoom QA'), ('VISUAL_QA.md', 'Visual QA and issues'), ('palette.json', 'Palette measurements'), ('generation-records.json', 'All original filenames and tool calls'), ('sources/registered-briefs.json', 'Exact catalogue prompts'), ('sources/owner-steering.json', 'Later owner direction'), ('references/manifest.json', 'Approved-reference provenance'), ('PNG_SHA256SUMS.txt', 'Every PNG hash'), ('SOURCE_SHA256SUMS.txt', 'Source and prompt hashes'), ('README.md', 'Package guide')]:
    parts.append(link(path, title))
parts.append('</div><p><code>' + BRANCH + '</code><br>Preparation base <code>' + BASE + '</code><br>Approved narrative blob <code>' + NARRATIVE + '</code></p><details><summary>Superseded studies · provenance only, not selectable</summary><p>The first restroom reused the receptionist appearance; its first background shared the reception styling. Both were retired after explicit owner correction. A later background study was retired after the desk-height composite check. The untouched originals and exact prompts remain available here.</p>')
for c in calls:
    if c['role'] != 'current candidate source':
        parts.append('<p>' + escape(c['reason']) + ' · ' + link('generation-source/' + c['filename'], c['filename']) + ' · ' + link(c['prompt'], 'Exact superseded prompt') + '</p>')
parts.append('</details><p class="note"><strong>Stop at Nate’s visual selection gate.</strong> Nothing selected, approved, integrated or merged. No Batch B, inventory, Focus A or death artwork generated. Narrative, dialogue, checks, branching and approved prior artwork remain unchanged.</p></section></main><footer>Built-in image_gen · independent environment and portrait sources · review only</footer><script>for(const b of document.querySelectorAll("[data-scale]")){b.addEventListener("click",()=>{const s=Number(b.dataset.scale);for(const i of document.querySelectorAll("img.art")){i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;}for(const other of document.querySelectorAll("[data-scale]"))other.setAttribute("aria-pressed",String(other===b));});}</script></body></html>')
(R / 'index.html').write_text('\n'.join(parts))

(R / 'PNG_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(R)}\n' for p in sorted(R.rglob('*.png'))))
source_files = sorted(p for p in R.rglob('*') if p.is_file() and (p.is_relative_to(R / 'sources') or p.is_relative_to(R / 'prompts')))
(R / 'SOURCE_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(R)}\n' for p in source_files))
print(json.dumps({'currentCandidates': len(records), 'toolCalls': len(calls), 'branch': BRANCH, 'hashes': {c['id']: c['sha256'] for c in records}}, indent=2))
