"""Presentation packaging only: no drawing/reconstruction of portrait artwork.

Preserve masters. The only resampling operation is exact 4x nearest-neighbor.
Comparison sheets paste source pixels one-for-one onto an external checker.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib, json, html

ROOT = Path(__file__).resolve().parent.parent
REVIEW = ROOT.parent
PREVIEWS = ROOT / 'previews'
COMPARISONS = ROOT / 'comparisons'

ITEMS = [
    ('raster-test', 'Fresh raster method test', 'generated/CH4-03-raster-method-test-original.png', 'SOURCE-SIZED TEST — NOT NATIVE', 'New raster construction; failed native-size gate. Not a game-asset candidate.'),
    ('frontal-reference', 'Primary detailed frontal reference', '../v04/detailed/CH4-03-front-reference-v04.png', 'DETAILED REFERENCE', 'Unchanged original character guide; not native game artwork.'),
    ('v05-auctioneer', 'Preserved v05 auctioneer', '../v05/native/CH4-03-auctioneer-showman-v05.png', 'UNSELECTED — NATIVE 564×278', 'Earlier coordinate/brush portrait; no further marks or changes.'),
    ('receptionist', 'Approved receptionist', '../v02/references/portraits__receptionist__receptionist_idle.png', 'APPROVED REFERENCE — NATIVE 564×278', 'Compare eyes, cheek/mouth planes, hair masses, contour hierarchy and cloth.'),
    ('pavilion-attendant', 'Approved Pavilion attendant', '../v04/references/pavilion_attendant_idle.png', 'APPROVED REFERENCE — NATIVE 564×278', 'Compare natural anatomy, hand integration and dimensional fabric folds.'),
    ('pavilion-presenter', 'Approved Pavilion presenter', '../v04/references/pavilion_presenter_idle.png', 'APPROVED REFERENCE — NATIVE 564×278', 'Compare expressive face, hair construction, gesture, tailoring and palette.'),
]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def record(relative):
    path = (ROOT / relative).resolve()
    result = {'file': relative, 'sha256': digest(path)}
    if path.suffix == '.png':
        with Image.open(path) as im:
            result.update(dimensions=list(im.size), mode=im.mode)
            if im.mode == 'RGBA':
                result['alphaExtrema'] = list(im.getchannel('A').getextrema())
    return result

def checker(size):
    im = Image.new('RGB', size, '#233132')
    d = ImageDraw.Draw(im)
    for y in range(0, size[1], 8):
        for x in range(0, size[0], 8):
            if (x//8 + y//8) % 2:
                d.rectangle((x, y, x+7, y+7), fill='#304140')
    return im

def sheet(ids, filename, columns):
    selected = [next(item for item in ITEMS if item[0] == id_) for id_ in ids]
    images = [Image.open(ROOT / item[2]).convert('RGBA') for item in selected]
    w, h = max(im.width for im in images), max(im.height for im in images)
    cellw, cellh = w+24, h+70
    out = Image.new('RGB', (columns*cellw, ((len(images)+columns-1)//columns)*cellh), '#172426')
    d = ImageDraw.Draw(out)
    font = ImageFont.load_default(size=14)
    for i, (item, im) in enumerate(zip(selected, images)):
        x, y = (i % columns)*cellw+12, (i // columns)*cellh+12
        d.text((x, y), item[1]+' — '+str(im.width)+'×'+str(im.height), font=font, fill='#f3e7ce')
        d.text((x, y+20), item[3], font=font, fill='#e5b775')
        backing = checker(im.size)
        # Alpha-composite for display only. Masters and exact4x preserve alpha.
        backing.paste(im, (0, 0), im)
        out.paste(backing, (x, y+46))
    path = COMPARISONS / filename
    out.save(path)
    return path

def main():
    PREVIEWS.mkdir(exist_ok=True)
    COMPARISONS.mkdir(exist_ok=True)
    assets = []
    for id_, title, relative, label, note in ITEMS:
        with Image.open(ROOT / relative) as im:
            im.resize((im.width*4, im.height*4), Image.Resampling.NEAREST).save(PREVIEWS/(id_+'-exact-4x.png'))
        assets.append({'id': id_, 'title': title, 'classification': label, 'note': note, 'original': record(relative), 'exact4x': record('previews/'+id_+'-exact-4x.png')})
    benchmarks = sheet(['v05-auctioneer','receptionist','pavilion-attendant','pavilion-presenter'], 'native-v05-and-approved.png', 2)
    with Image.open(benchmarks) as im:
        im.resize((im.width*4, im.height*4), Image.Resampling.NEAREST).save(COMPARISONS/'native-v05-and-approved-exact-4x.png')
    sheet(['raster-test','frontal-reference'], 'raster-test-and-frontal-reference-1to1.png', 2)
    sheet(['raster-test','frontal-reference','v05-auctioneer','receptionist','pavilion-attendant','pavilion-presenter'], 'all-six-original-pixels.png', 2)
    old = json.loads((REVIEW/'v05/manifest.json').read_text())
    source = next(a for a in old['assets'] if a['id'] == 'CH4-03')
    frozen = json.loads((ROOT/'evidence/frozen-environments.json').read_text())
    manifest = {
        'study': 'CH4-03 portrait-specific reconstruction study 01',
        'status': 'UNSELECTED', 'baseCommit': 'a89702d9aac81183398fb70bbc97ab4d700e54f6',
        'publicationBranch': 'art/ch4-batch01-review-20261121',
        'nativeContract': {'dimensions': [564,278], 'alpha': 'transparent foreground', 'satisfiedByNewStudy': False},
        'nativeCandidate': None,
        'decision': 'Stop further portrait revisions after failed method test; proposed layered native raster workflow is in METHOD-DECISION.md.',
        'method': 'One fresh built-in raster generation from four visual references, not v05. Returned master preserved byte-for-byte; no resize/crop into native asset. Only exact4x presentation enlargement and one-for-one comparison pasting.',
        'nativeAuthorshipProven': False, 'pillowVersion': Image.__version__,
        'sourceNodeIds': source['sourceNodeIds'], 'canonicalRequirements': '../v02/evidence/canonical-requirements.json',
        'referenceInputOrder': ['frontal-reference','receptionist','pavilion-attendant','pavilion-presenter'],
        'assets': assets, 'frozenEnvironments': frozen,
        'comparisons': [record(p.relative_to(ROOT).as_posix()) for p in sorted(COMPARISONS.glob('*.png'))],
        'prompt': record('prompts/native-raster-reconstruction.txt'),
        'receipt': record('evidence/generation-receipt.json'),
        'knownLimitations': ['Native-size generation failed: 1785×881 returned, 564×278 requested.', 'Internal image-model authorship is unobservable; prompt instructions do not prove native construction.', 'The source-sized test is more painterly than the approved NPCs; no new native-size aesthetic comparison is possible.', 'The saved original makes export packaging replayable; the stochastic generative call is not bit-for-bit replayable.', 'This is not a completed new native portrait review version or an artwork approval.'],
    }
    (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    comparison = {
        'creativeApproval': False, 'nativeCandidateProduced': False,
        'visualAssessments': [
            {'against': 'v05 auctioneer', 'finding': 'The raster test models cheeks/jowls, sockets/lids, mouth/mustache, sculpted silver hair, cloth folds and the two-hand gavel hold more naturally. It changes the underlying anatomy. V05 remains flatter and diagrammatic. This comparison is of original pixels at different source resolutions, not proof of improvement at native size.'},
            {'against': 'primary frontal reference', 'finding': 'The test follows the elderly frontal identity and material treatment very closely. Large-scale transitions and construction are stronger; close resemblance also raises a style concern because the study remains painterly rather than demonstrating native NPC cluster craft.'},
            {'against': 'approved receptionist', 'finding': 'The receptionist achieves facial expression, grouped hair volume, selective contours and clothing distinction at 564×278. The source-sized test has not demonstrated the same economy and finish at this grid.'},
            {'against': 'approved Pavilion attendant', 'finding': 'The attendant integrates natural hands, neck, shoulders and cloth folds at native size. The test gives a more credible gavel hold than v05, but how it would survive native reconstruction is unresolved.'},
            {'against': 'approved Pavilion presenter', 'finding': 'The presenter combines readable gesture, lively facial anatomy, hair masses and controlled suit shading. The test is more realistic and may diverge in style; no equivalence claim is made.'},
        ],
        'nativeComparisonVerdict': 'NOT AVAILABLE for the new test; no valid native candidate exists.',
        'exact4xVerdict': 'Exact nearest-neighbor inspection exports preserve source pixels; they do not cure the failed native-size output.',
        'decision': 'Use a layered direct-native raster illustrator workflow before further portrait revisions. Do not incrementally repaint v05.'
    }
    (ROOT/'comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
    cards = []
    for a in assets:
        original, four = a['original'], a['exact4x']
        w,h = original['dimensions']
        cards.append(f'''<article id="{a['id']}" class="art-card"><h2>{html.escape(a['title'])}</h2><p class="tag">{html.escape(a['classification'])}</p><p>{html.escape(a['note'])}</p><p>Actual raster: {w}×{h}. <span class="scale-label">Original pixels · 1×</span></p><div class="actions"><button class="scale" data-target="{a['id']}" data-scale="1">1× original pixels</button><button class="scale" data-target="{a['id']}" data-scale="4">Exact 4×</button><a href="{original['file']}">Original PNG</a><a href="{four['file']}">4× PNG</a></div><div class="viewport checker"><img class="artwork" data-target="{a['id']}" src="{original['file']}" data-one="{original['file']}" data-four="{four['file']}" data-width="{w}" data-height="{h}" width="{w}" height="{h}" alt="{html.escape(a['title'])}; {html.escape(a['classification'])}" loading="eager"></div><details><summary>Original SHA-256</summary><code>{original['sha256']}</code></details></article>''')
    freeze_cards = []
    for f in frozen['files']:
        rel='../'+f['file']
        freeze_cards.append(f'<p><a href="{rel}">{html.escape(Path(f["file"]).name)}</a><br><code>{f["sha256"]}</code></p>')
    comparison_links = ''.join(f'<li><a href="{p.relative_to(ROOT).as_posix()}">{html.escape(p.stem)}</a> · original pixels; no reduction</li>' for p in sorted(COMPARISONS.glob('*.png')))
    assessments = ''.join(f'<li><strong>{html.escape(a["against"])}:</strong> {html.escape(a["finding"])}</li>' for a in comparison['visualAssessments'])
    page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CH4 auctioneer · reconstruction method study 01</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#152326;color:#eee5d3;font:16px/1.55 system-ui,sans-serif}main{max-width:1480px;margin:auto;padding:28px}h1{font-size:clamp(1.6rem,3vw,2.5rem);line-height:1.2}h2{font-size:1.35rem}a{color:#a7dcca}button{background:#304b4d;color:#fff3dd;border:1px solid #71827a;padding:8px 14px;border-radius:5px;cursor:pointer}button:focus-visible,a:focus-visible{outline:3px solid #efd69a}.notice,.art-card,.panel{padding:22px;background:#203236;border:1px solid #486060;border-radius:9px;margin:24px 0}.notice{border-left:5px solid #edb56b}.tag{color:#edc180;font-weight:700}.actions{display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin:15px 0}.viewport{max-width:100%;max-height:720px;overflow:auto;border:1px solid #526767;isolation:isolate}.checker{background-color:#2a3939;background-image:linear-gradient(45deg,#384b48 25%,transparent 25%),linear-gradient(-45deg,#384b48 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#384b48 75%),linear-gradient(-45deg,transparent 75%,#384b48 75%);background-size:16px 16px;background-position:0 0,0 8px,8px -8px,-8px 0}.artwork{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}code{overflow-wrap:anywhere;font-size:.82em}li{margin:.8em 0}details{margin-top:12px}footer{padding:24px 0;color:#b4c6c0}@media(max-width:600px){main{padding:12px}.notice,.art-card,.panel{padding:14px}}
</style></head><body><main><header><p>Out of Order · Chapter 4 · CH4-03</p><h1>Portrait reconstruction method study 01</h1><p class="tag">UNSELECTED · Method decision, not a completed v06</p></header>
<section class="notice" id="decision"><h2>The native-size gate failed</h2><p>One fresh raster test returned <strong>1785×881</strong>, despite the explicit <strong>564×278</strong> request. It is preserved as a source-sized study. It has not been shrunk, cropped or filtered into a native asset. <strong>No new native portrait candidate is claimed.</strong></p><p>The current coordinate construction has reached diminishing returns. This raster test improves anatomical modeling at its larger resolution, but cannot establish the approved NPC standard on the required grid. Further illustration revisions stop here.</p><p>Proposed next method: direct layered raster illustration on a blank 564×278 canvas, with fresh anatomy, native painting stages and reproducible layer exports. <a href="METHOD-DECISION.md">Read the method assessment and concrete production proposal</a>.</p><p><a href="evidence/generation-receipt.json">Measured output receipt</a> · <a href="prompts/native-raster-reconstruction.txt">Exact built-in generation prompt</a> · <a href="manifest.json">Manifest / hashes</a> · <a href="comparison.json">Visual findings</a></p></section>
<nav><a href="#raster-test">Raster test</a> · <a href="#frontal-reference">Frontal reference</a> · <a href="#v05-auctioneer">v05</a> · <a href="#receptionist">Receptionist</a> · <a href="#pavilion-attendant">Attendant</a> · <a href="#pavilion-presenter">Presenter</a> · <a href="#frozen">Frozen rooms</a></nav>
<section class="panel" id="comparison-files"><h2>Direct comparison PNGs</h2><p>All source pixels are displayed one-for-one. The large study is deliberately not fitted into a 564×278 box. Only v05 and the approved references qualify for native-size comparison. Their exact 4× sheet is also supplied.</p><ul>__COMPARISON_LINKS__</ul></section>
__CARDS__
<section class="panel" id="visual-findings"><h2>Actual artwork assessment</h2><ul>__ASSESSMENTS__</ul><p><strong>Unresolved:</strong> a new independently authored native portrait with benchmark-quality eyes, hair, fabric and gavel grip. Exact scaling and source polish do not satisfy that requirement.</p></section>
<section class="panel" id="frozen"><h2>Frozen v05 owner-review environments</h2><p>CH4-01 and CH4-02 are preserved exactly. Both remain UNSELECTED; no approval registration or further room edits occurred.</p>__FROZEN__<p><a href="evidence/frozen-environments.json">Freeze record</a> · <a href="evidence/preservation-baseline.json">v01–v05 preservation baseline</a> · <a href="evidence/validation.json">Study validation</a> · <a href="../v05/index.html">Preserved v05 gallery</a></p></section>
<footer>Publication branch: art/ch4-batch01-review-20261121. Main, narrative, gameplay, production workflows, artwork approval registries, restroom and ballroom are unchanged. <a href="README.md">Study notes</a></footer></main><script>
document.querySelectorAll('.scale').forEach(button=>button.addEventListener('click',()=>{const img=document.querySelector('.artwork[data-target="'+button.dataset.target+'"]'),scale=Number(button.dataset.scale);img.src=scale===4?img.dataset.four:img.dataset.one;img.width=Number(img.dataset.width)*scale;img.height=Number(img.dataset.height)*scale;img.closest('article').querySelector('.scale-label').textContent=scale===4?'Exact nearest-neighbor · 4×':'Original pixels · 1×';}));
</script></body></html>'''
    page=page.replace('__COMPARISON_LINKS__',comparison_links).replace('__CARDS__','\n'.join(cards)).replace('__ASSESSMENTS__',assessments).replace('__FROZEN__','\n'.join(freeze_cards))
    (ROOT/'index.html').write_text(page)

if __name__ == '__main__':
    main()
