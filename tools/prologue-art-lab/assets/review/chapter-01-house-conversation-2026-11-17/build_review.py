"""Package existing image_gen renders; only RGB/nearest-neighbor export, no drawn art."""
from pathlib import Path
import hashlib
import html
import json
import subprocess
from PIL import Image

R = Path(__file__).resolve().parent
ROOT = R.parents[4]
BASE = 'b3e374b9a12c1bd2e60ec437293a734ffe562d33'
BRANCH_BASE = '1ce7e79641e764d11367d476c7ede9ee0e8614c2'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save_json(name, value):
    (R / name).write_text(json.dumps(value, indent=2) + '\n')


def picture(path, width, height, alt):
    return f'<div class="scroll"><img class="zoomable" src="{path}" width="{width}" height="{height}" data-width="{width}" data-height="{height}" alt="{html.escape(alt)}"></div>'


def link(path, label):
    return f'<a href="{path}">{html.escape(label)}</a>'


originals = {
    ('A', 'lounge', 1): 'exec-c1234f69-f3d2-4834-9535-73b96895f531.png',
    ('B', 'dining', 1): 'exec-9f5295cf-03da-4082-9c2d-80e5d562394a.png',
    ('A', 'lounge', 2): 'exec-41845ef0-a757-4b1f-9b5f-d0f1db32445f.png',
    ('B', 'dining', 2): 'exec-744b13c8-b818-4503-b775-afa34aa4c50f.png',
}
records = []
for (letter, room, version), filename in originals.items():
    prefix = f'{letter}-{room}'
    source = f'generation-source/{prefix}-v{version:02}.png'
    candidate = f'candidates/{prefix}-conversation-v{version:02}.png'
    prompt = f'prompts/{prefix}-v{version:02}.txt'
    preview = f'previews/{prefix}-conversation-v{version:02}-4x.png'
    im = Image.open(R / source)
    export = im.convert('RGB').resize((564, 278), Image.Resampling.NEAREST)
    export.save(R / candidate)
    export.resize((2256, 1112), Image.Resampling.NEAREST).save(R / preview)
    refs = ['references/foyer-conversation.png', 'references/gallery-conversation.png', f'references/{room}-scene.png'] if version == 1 else [f'candidates/{prefix}-conversation-v01.png', 'references/foyer-conversation.png', 'references/gallery-conversation.png']
    record = {
        'artworkId': f'portraits:house:idle#views:house_of_tomorrow/{room}',
        'usedBy': 'comfort_offer' if room == 'lounge' else 'dinner_arrival',
        'version': version,
        'reviewRole': 'current review candidate' if version == 2 else 'superseded scale study; retained for provenance',
        'approval': 'unselected; pending Art Director review',
        'tool': 'built-in image_gen.imagegen',
        'source': source, 'sourceSha256': sha(R / source), 'sourceDimensions': list(im.size),
        'originalToolPath': '/Users/MrDashiki/.codex/generated_images/01a1ec38-b54e-7282-8f94-36ccf07b29ed/' + filename,
        'prompt': prompt, 'promptSha256': sha(R / prompt),
        'referencedImagesInOrder': refs,
        'referenceHashes': [sha(R / p) for p in refs],
        'transparent_background': False,
        'candidate': candidate, 'candidateSha256': sha(R / candidate),
        'candidateDimensions': [564, 278], 'candidateMode': 'RGB',
        'preview4x': preview, 'previewSha256': sha(R / preview),
        'processing': 'Full-frame RGB export and NEAREST sampling to 564x278; exact 4x NEAREST preview. No crop, compositing, palette quantization, dithering, sharpening or painted pixels.',
        'aspectRatioChangePercent': ((564 / 278) / (im.width / im.height) - 1) * 100,
        'intendedProductionPath': f'art/portraits/house/{room}_conversation.png',
        'productionPathPopulated': False,
    }
    records.append(record)

save_json('generation-records.json', {'canonicalBaseCommit': BASE, 'toolCalls': 4, 'independentFirstRenders': 2, 'focusedScaleCorrections': 2, 'records': records})
current = [x for x in records if x['version'] == 2]
save_json('manifest.json', {'repository': 'InterstellarHarvest/CYOA-storyboard', 'generationBaseCommit': BASE, 'branchBaseCommit': BRANCH_BASE, 'branch': 'agent/ch01-house-conversation-art-20261117', 'status': 'unselected; pending Art Director review', 'candidates': current, 'productionRegistration': 'Not performed; both canonical assetPath values remain null.'})

limitations = '''# Visual comparison and limitations

Both v02 candidates remain unselected pending Art Director review. These are technical production candidates, not approval decisions.

## Shared House design

The approved foyer and gallery PNGs were used directly as image-generation references. Both candidates retain a tall ivory rounded housing, brown woven grille, tiny upper-right black camera dot, lower-left green circular lamp, and lower-right ribbed thumbwheel. They mount directly against a peach wall with a shallow shadow. There are no posts, people, hands, separate sprites, captions or interface elements. The v02 housings are approximately 168x216 logical pixels, close to the approved gallery's approximately 170x218 housing; the approved foyer's housing is slightly taller, approximately 170x236. These bounds are visual estimates, not segmentation measurements.

## Lounge versus approved lounge scene

The new close view retains the garden daylight at left, peach wall/coral trim, warm cabinet and a cropped empty mint recliner at the lower right. The intercom occupies the center at conversational scale. The original main scene remains wider and shows the full recliner and room. Only a sliver of coral appears at the lower-left corner; its separation from the nearby trim/rug is visually ambiguous at this crop.

## Dining versus approved dining scene

The close view retains the garden-window edge, warm serving cabinets and coral pot, an empty white plate and cup at the lower table rim, and two visibly empty mint chair backs. The full main scene establishes four settings; this intentionally tight portrait shows only the near setting and two cropped chair backs. The complete four-place table and all four chairs are outside this framing. No food is visible. Room perspective is reinterpreted for the closer intercom view; furniture locations are consistent cues, not a pixel registration of the main scene.

## Pixel fidelity and generation limits

All four tool-returned originals are preserved byte-exact. The tool returned 1784x882, 1786x881, 1788x880 and 1785x881 RGB renders rather than the requested 2256x1112 integer-grid output. Native candidates use full-frame NEAREST sampling to exactly 564x278. This introduces a small aspect-ratio adjustment (current v02 candidates under 0.15% in magnitude; archived lounge v01 approximately 0.302%; see generation records) and cannot prove that the original was authored on a strict logical pixel grid. No blur or interpolation filter was applied. Four-times PNGs are verified pixel-for-pixel expansions of each native export; the gallery also uses integer CSS dimensions and pixelated image rendering.

The generated grille weave, housing bevels, wall shading and edge highlights are newly rendered rather than byte-identical reproductions of approved pixels. Grille texture is denser and less regular than the source in places, and the wall retains gentle tonal shading. Hard stepped contours remain visible at native resolution and 4x, but microtexture consistency requires Art Director review. No palette reduction or smoothing was applied to disguise these differences. v01 files are archived scale studies, not additional selected options.

## Scope

Only this review directory is added relative to branch base 1ce7e79, preserving the concurrently published final Chapter 2 Batch 8 approvals. Generation source b3e374b remains pinned in sources/; all Chapter 1 target briefs and approved references are unchanged between those revisions. No canonical registry, selected artwork, gameplay, dialogue conversion, choices, flags, inventory, routes, workflows, Chapter 3 files or existing approved PNGs are changed. Batch B branch 004758e is not merged, copied or edited. Production paths remain empty. No review approval is inferred from generating, committing or publishing these files.
'''
(R / 'ARTWORK_CONTINUITY_REVIEW.md').write_text(limitations)
hashes = '# Current review candidates — unselected\n\n'
for x in current:
    hashes += f"- `{x['candidate']}`\n  - SHA-256: `{x['candidateSha256']}`\n"
(R / 'CANDIDATE_HASHES.md').write_text(hashes)
(R / 'README.md').write_text('''# Chapter 1 House lounge and dining conversation artwork

Both v02 images are unselected and await Art Director review. Production paths and the canonical artwork registry are unchanged.

Open index.html for the native 564x278 candidates, integer 4x controls, downloadable exact 2256x1112 PNGs, comparisons with both approved House portraits and corresponding main scenes, exact prompts, original generation outputs, all hashes and limitations. v01 scale studies are retained in the history section.

The package follows the public storyboard's tools/prologue-art-lab/assets/review convention. Branch: agent/ch01-house-conversation-art-20261117. Generation source: b3e374b9a12c1bd2e60ec437293a734ffe562d33. Branch base: 1ce7e79641e764d11367d476c7ede9ee0e8614c2, preserving the concurrent final Chapter 2 Batch 8 approvals. Chapter 1 target briefs and references did not change. Batch B conversion commit 004758e stays on its existing branch. No public-main merge or Pages workflow is performed.

Generation used the built-in image_gen tool, two initial renders and one focused scale correction per image. Exact submitted prompts are under prompts/. References are copied byte-exact from assets/selected/, with original hashes and source paths in references/manifest.json. Complete authoritative briefs and relevant source snapshots are under sources/.

Only RGB and nearest-neighbor dimension export are applied to generated originals. Rebuild with Python 3 and Pillow: python3 build_review.py. Validate with python3 verify_review.py. Read qa.json, browser-qa.json and ARTWORK_CONTINUITY_REVIEW.md for evidence and limitations. Candidate hashes are in CANDIDATE_HASHES.md; PNG_SHA256SUMS.txt covers all image files.

Stop for Art Director approval. Registration and game integration belong to the subsequent approved workflow.
''')

css = '''
:root{color-scheme:dark;--bg:#1e2829;--panel:#293536;--ink:#f4ecdc;--muted:#c3ceca;--line:#5c716a;--accent:#d1e8ab}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,sans-serif}header,main,footer{max-width:1500px;margin:auto;padding:28px}h1{font-size:clamp(30px,4vw,48px);line-height:1.15;margin:12px 0}h2{font-size:26px;margin:0 0 12px}h3{font-size:18px;margin:0 0 12px}p{max-width:1000px}.eyebrow{color:var(--accent);letter-spacing:.12em;font-size:12px;text-transform:uppercase}.status{display:inline-block;border:1px solid var(--accent);padding:4px 10px;color:var(--accent)}a{color:var(--accent);text-underline-offset:3px}nav{display:flex;flex-wrap:wrap;gap:16px}.toolbar{position:sticky;top:0;z-index:10;padding:12px 28px;background:#1e2829f5;border-block:1px solid var(--line);display:flex;align-items:center;gap:12px;flex-wrap:wrap}button{font:inherit;padding:6px 14px;border:1px solid var(--line);background:var(--panel);color:var(--ink);cursor:pointer}button[aria-pressed=true]{background:var(--accent);color:var(--bg)}section{padding:26px 0;border-bottom:1px solid var(--line);scroll-margin-top:100px}.card{padding:20px;background:var(--panel);border:1px solid var(--line);margin:18px 0}.scroll{overflow:auto;max-width:100%;background:#151d1d;padding:12px;border:1px solid #455654}img{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}.pair{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}figure{margin:0;min-width:0}figcaption,.muted{font-size:14px;color:var(--muted);margin:10px 0}code,pre{font:13px/1.6 ui-monospace,monospace;overflow-wrap:anywhere}pre{white-space:pre-wrap;max-height:460px;overflow:auto}details{border:1px solid var(--line);padding:12px;margin-top:18px}summary{cursor:pointer;color:var(--accent)}.links{display:flex;gap:16px;flex-wrap:wrap;font-size:14px;margin:12px 0}.hash{display:block;user-select:all}.note{border-left:3px solid var(--accent);padding-left:14px}a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid #f4cd91;outline-offset:3px}@media(max-width:800px){.pair{grid-template-columns:1fr}header,main,footer{padding:18px}.toolbar{padding:10px 18px}.card{padding:12px}}
'''
(R / 'gallery.css').write_text(css)
parts = ['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>House conversation artwork — Art Director review</title><link rel="stylesheet" href="gallery.css"><body>',
         '<header><div class="eyebrow">The Acceptable Error · Chapter 1 · Presentation Batch B artwork</div><h1>The House, in conversation</h1><p class="status">UNSELECTED · PENDING ART DIRECTOR REVIEW</p><p>Two complete environmental portrait candidates. Native 564×278 RGB; exact nearest-neighbor 4× previews. The production artwork paths remain empty.</p><nav><a href="#lounge">Lounge</a><a href="#dining">Dining</a><a href="#approved">Approved House views</a><a href="#history">Generation history</a><a href="#evidence">Validation and sources</a></nav></header>',
         '<div class="toolbar"><span>Inspect every image at:</span><button data-scale="1" aria-pressed="true">Native 1×</button><button data-scale="4" aria-pressed="false">Nearest 4×</button><span class="muted">Larger images scroll horizontally. No fit-to-width scaling.</span></div><main>']
for x in current:
    room = 'lounge' if 'lounge' in x['candidate'] else 'dining'
    name = room.title()
    parts.append(f'<section id="{room}"><h2>{name} conversation · v02</h2><p><code>{x["artworkId"]}</code> · used by <code>{x["usedBy"]}</code></p><article class="card candidate" data-room="{room}"><h3>Current review candidate · unselected</h3>')
    parts.append(picture(x['candidate'], 564, 278, f'{name}: flush ivory House intercom with empty room cues'))
    parts.append(f'<p><code class="hash">SHA-256 {x["candidateSha256"]}</code><code>{x["candidate"]}</code></p><div class="links">' + link(x['candidate'], 'Native PNG') + link(x['preview4x'], 'Exact 4× PNG') + link(x['source'], 'Original generation output') + link(x['prompt'], 'Exact correction prompt') + '</div></article>')
    parts.append('<h3>Room continuity comparison</h3><div class="pair"><figure>' + picture(f'references/{room}-scene.png', 314, 206, f'Approved {room} main scene') + f'<figcaption>Approved {room} main scene · 314×206 · untouched source</figcaption></figure><figure>' + picture(x['candidate'], 564, 278, f'{name} conversation candidate') + '<figcaption>New tight conversation view · 564×278 · unselected</figcaption></figure></div>')
    desc = 'Garden daylight, peach wall, coral trim, warm cabinet, and cropped empty mint recliner. The speaker remains flush against the wall.' if room == 'lounge' else 'Empty white plate, cup and tabletop rim, two vacant mint chair backs, warm serving cabinet and garden edge. The full four-place table is established by the main scene; this close view shows one setting.'
    parts.append(f'<p>{desc}</p><details><summary>Authoritative registered brief and exact submitted correction prompt</summary><pre>{html.escape((R / x["prompt"]).read_text())}</pre></details></section>')

parts.append('<section id="approved"><h2>Compare with both approved House views</h2><p>These copied references remain approved and unchanged. All four portraits share the same logical canvas dimensions; the scale controls apply equally.</p><div class="pair">')
for f, label in [('foyer-conversation', 'Approved foyer conversation'), ('gallery-conversation', 'Approved portrait-gallery conversation'), ('../candidates/A-lounge-conversation-v02', 'New lounge candidate · unselected'), ('../candidates/B-dining-conversation-v02', 'New dining candidate · unselected')]:
    src = f'references/{f}.png'
    parts.append('<figure>' + picture(src, 564, 278, label) + f'<figcaption>{label}</figcaption></figure>')
parts.append('</div><p>The housing silhouette and control layout are consistent. Grille weave, pixel shading and bevel highlights are newly rendered; inspect their consistency with the approved sources before selecting.</p></section>')
parts.append('<section id="history"><h2>Generation history and original outputs</h2><p>Two independent first renders, then one focused enlargement per room. Earlier scale studies remain immutable provenance; none of these files has been selected.</p>')
for x in records:
    label = x['candidate'].split('/')[-1]
    parts.append(f'<details><summary>{label} · {x["reviewRole"]}</summary>' + picture(x['candidate'], 564, 278, label) + '<div class="links">' + link(x['source'], 'Unmodified original PNG') + link(x['prompt'], 'Exact generation prompt') + link(x['candidate'], 'Native export') + link(x['preview4x'], 'Exact 4× PNG') + f'</div><p>Original {x["sourceDimensions"][0]}×{x["sourceDimensions"][1]}; native 564×278 RGB. Full-frame NEAREST sampling; no crop or smoothing.</p><pre>{html.escape((R / x["prompt"]).read_text())}</pre></details>')
parts.append('</section><section id="evidence"><h2>Technical evidence and limitations</h2><p class="note">The generator did not return an exact integer logical grid. Native exports use nearest-neighbor sampling; original renders are preserved. Exact 4× pixel expansion is verified. This does not establish artistic approval or prove the originals used a uniform logical pixel density.</p><div class="links">')
for path, label in [('ARTWORK_CONTINUITY_REVIEW.md', 'Visual comparison and limitations'), ('manifest.json', 'Current candidates and hashes'), ('generation-records.json', 'All generation records'), ('CANDIDATE_HASHES.md', 'Candidate SHA-256 hashes'), ('PNG_SHA256SUMS.txt', 'Every PNG hash'), ('qa.json', 'Dimension, pixels, hashes and scope checks'), ('browser-qa.json', 'Browser gallery checks'), ('references/manifest.json', 'Approved reference provenance'), ('sources/registered-briefs.json', 'Authoritative registered briefs'), ('sources/provenance.json', 'Branch and source provenance'), ('README.md', 'Review package guide')]:
    parts.append(link(path, label))
parts.append('</div><p>Generation source <code>' + BASE + '</code>; branch base <code>' + BRANCH_BASE + '</code>, preserving concurrent final Chapter 2 Batch 8 approvals. Chapter 1 briefs and references are unchanged. No changes to story, gameplay, Chapter 3, approved artwork, production paths, selected-art previews or workflows. Batch B conversions remain on their existing branch at <code>004758e</code>.</p><p><strong>STOP FOR ART DIRECTOR APPROVAL.</strong> Selection, registration and integration are subsequent work.</p></section></main><footer>Generated with the built-in image_gen tool. Candidates remain unselected. All artwork shown is local to this immutable review package.</footer><script>for(const button of document.querySelectorAll("[data-scale]")){button.addEventListener("click",()=>{const scale=Number(button.dataset.scale);for(const image of document.querySelectorAll(".zoomable")){image.width=Number(image.dataset.width)*scale;image.height=Number(image.dataset.height)*scale;}for(const b of document.querySelectorAll("[data-scale]"))b.setAttribute("aria-pressed",String(b===button));});}</script></body></html>')
(R / 'index.html').write_text('\n'.join(parts))
(R / 'PNG_SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(R)}\n' for p in sorted(R.rglob('*.png'))))
print(json.dumps({'reviewDirectory': str(R.relative_to(ROOT)), 'currentCandidateHashes': {x['candidate']: x['candidateSha256'] for x in current}, 'pngCount': len(list(R.rglob('*.png')))}, indent=2))
