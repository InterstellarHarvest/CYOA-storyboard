"""Build diagnostics and a portable assessment; never write approved artwork."""
from pathlib import Path
from PIL import Image, ImageDraw
from html import escape
import base64
import hashlib
import json
import re

B = Path(__file__).resolve().parent
R = B.parents[5]
source = json.loads((B / 'sources/approved-source.json').read_text())
refs = json.loads((B / 'sources/references.json').read_text())
baseline = json.loads((B / 'sources/preservation-baseline.json').read_text())
im = Image.open(B / 'originals/approved-restroom-entrance.png').convert('RGB')
assert im.size == (314, 206)
assert hashlib.sha256((B / 'originals/approved-restroom-entrance.png').read_bytes()).hexdigest() == source['sha256']

def write_json(p, value):
    (B / p).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def save_native_and_4x(image, folder, stem):
    image.save(B / folder / (stem + '-native.png'))
    image.resize((image.width * 4, image.height * 4), Image.Resampling.NEAREST).save(B / folder / (stem + '-4x.png'))

def pair_image(left, right):
    result = Image.new('RGB', (left.width + right.width, max(left.height, right.height)), '#e8e2d5')
    result.paste(left.convert('RGB'), (0, 0))
    result.paste(right.convert('RGB'), (left.width, 0))
    return result

regions = [
    {'id': 'face', 'name': 'Attendant face, glasses and hair', 'box': [201, 94, 235, 122],
     'finding': 'The dark glasses, swept dark/gray hair, cheek and smiling mouth identify the same attendant as the approved idle portrait. The reassuring expression fits real_restroom, attendant_greeting and the explicit smile in attendant_refusal. At native and exact 4×, inherited softness does not hide identity or expression. Do not copy the emergency expression into this greeting state.'},
    {'id': 'hands-costume', 'name': 'Hands, costume, seated silhouette and desk contact', 'box': [201, 120, 245, 146],
     'finding': 'The joined hands read as a quiet clasp; cream sleeves, teal vest, tie and pale badge remain distinct. Forearms terminate at the desktop and the chair back supports the seated reading. The counter deliberately occludes the lower body; absent feet are not evidence of floating. No detached hand, collision or distracting silhouette break is demonstrated.'},
    {'id': 'microphone', 'name': 'Approved v09 gooseneck microphone correction', 'box': [190, 119, 208, 146],
     'finding': 'Retain the explicitly authored capsule/head, small background gap, one-pixel curved stem and compact desktop base. The cool dark microphone remains separate from the brown chair and cream equipment. The tiny geometry is deliberate and independently documented in the v09 edit record; smoothing or thickening would undo the accepted correction.'},
    {'id': 'desk-equipment', 'name': 'Desk layout, existing cream unit and plant', 'box': [177, 106, 273, 189],
     'finding': 'The existing cream slotted unit remains on the left, microphone beside it, attendant centered and potted plant at the far right. Their silhouettes and desktop contacts are separate. The cream unit becomes the paper source in Record Printer; do not delete that established equipment or add back the separate unwanted desktop device. No printer/plant overlap is present.'},
    {'id': 'door-signs', 'name': 'Restroom doorway, two-person pictograms and reader', 'box': [63, 34, 231, 185],
     'finding': 'RESTROOM and both two-person pictograms read clearly. The teal jamb, inner sink/stall sightline, gate and green/red reader stay distinct. The warm tilework, steel pipes and ceiling fixtures explain a real working restroom. The sign glyphs need no cleanup. Reader color changes and visitor movement are successive narrated events, not reasons to repaint this reusable establishing image.'},
    {'id': 'floor-contacts', 'name': 'Architecture, bench, floor and equipment perspective', 'box': [0, 137, 314, 206],
     'finding': 'Door posts, bench supports, gate pedestal and desk plinth have visible floor contacts. The desk front, narrow top plane, wall tiles and receding floor joints form a coherent stylized view. No demonstrated skew, floating furniture or contact error warrants a new perspective correction.'},
]
for region in regions:
    region['action'] = 'KEEP'
    save_native_and_4x(im.crop(region['box']), 'assessment', region['id'])

protected = [
    {'name': 'Attendant identity and calm seated pose', 'box': [201, 94, 245, 144]},
    {'name': 'Exact v09 microphone repair bounds', 'box': [196, 123, 203, 143]},
    {'name': 'Existing cream feed unit at left', 'box': [180, 130, 199, 144]},
    {'name': 'Plant and clear separation from feed unit', 'box': [241, 108, 271, 146]},
    {'name': 'Counter top, front, corner shading and plinth', 'box': [174, 140, 273, 190]},
    {'name': 'Restroom sign, two-person figures and door architecture', 'box': [63, 34, 179, 185]},
    {'name': 'Wall pictogram, fixtures and warm material shading', 'box': [180, 34, 261, 133]},
    {'name': 'Bench and floor contacts', 'box': [0, 136, 69, 206]},
    {'name': 'Right doorway, daylight and exterior depth', 'box': [271, 69, 314, 175]},
]
layer = Image.new('RGBA', im.size)
draw = ImageDraw.Draw(layer)
for item in protected:
    x0, y0, x1, y1 = item['box']
    draw.rectangle((x0, y0, x1 - 1, y1 - 1), outline=(35, 211, 132, 220))
guide = Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB')
save_native_and_4x(guide, 'assessment', 'protected-detail-guide')
save_native_and_4x(pair_image(im, guide), 'comparisons', 'approved-left-protected-guide-right')

# Construction traces are descriptive, never an imposed calibration or repair mask.
architecture = [[(65, 66), (65, 185)], [(171, 65), (171, 185)], [(180, 34), (180, 139)],
                [(261, 40), (261, 109)], [(68, 65), (169, 65)], [(69, 181), (168, 181)],
                [(188, 51), (259, 51)]]
depth = [[(75, 71), (94, 88)], [(75, 101), (93, 104)],
         [(48, 204), (78, 174)], [(97, 205), (105, 177)], [(130, 205), (130, 179)],
         [(181, 205), (168, 185)], [(229, 205), (204, 186)], [(288, 205), (264, 185)]]
contacts = [[(0, 185), (15, 185)], [(52, 187), (65, 187)], [(103, 182), (117, 182)],
            [(182, 187), (265, 187)], [(207, 141), (238, 141)], [(249, 143), (261, 143)]]
layer = Image.new('RGBA', im.size)
draw = ImageDraw.Draw(layer)
for lines, color in [(architecture, (52, 206, 233, 225)), (depth, (255, 182, 66, 235)), (contacts, (224, 99, 214, 235))]:
    for line in lines:
        draw.line(line, fill=color, width=1)
perspective = Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB')
save_native_and_4x(perspective, 'assessment', 'perspective-construction')
write_json('assessment/perspective-guides.json', {
    'cyan': {'meaning': 'Visible architectural edges', 'lines': architecture},
    'amber': {'meaning': 'Approximate depth/floor traces', 'lines': depth},
    'magenta': {'meaning': 'Floor support and desktop contact traces', 'lines': contacts},
    'finding': 'No demonstrated perspective defect requiring correction.',
    'limitation': 'Approximate diagnostic traces, not a recovered camera or proof of one exact vanishing point. Inherited stylization is not by itself a geometric defect.'})

Image.new('L', im.size, 0).save(B / 'masks/proposed-repair-mask.png')
Image.new('L', im.size, 255).save(B / 'masks/protected-pixels.png')
write_json('sources/changed-pixels.json', [])
for name in ['record-printer', 'paper-emergency-canonical-v03', 'paper-emergency-selected-v04']:
    other = Image.open(B / 'references' / (name + '.png')).convert('RGB')
    save_native_and_4x(pair_image(im, other), 'comparisons', 'restroom-left-' + name + '-right')
    for label, box in [('attendant', (201, 94, 245, 144)), ('desk-layout', (177, 106, 273, 189))]:
        save_native_and_4x(pair_image(im.crop(box), other.crop(box)), 'comparisons', label + '-restroom-left-' + name + '-right')

background = Image.open(B / 'references/restroom-close-background.png').convert('RGBA')
portrait = Image.open(B / 'references/attendant-idle.png').convert('RGBA')
composite = Image.alpha_composite(background, portrait)
save_native_and_4x(composite, 'assessment', 'approved-conversation-composite')

assessment = {
    'recommendation': 'KEEP', 'approvedArtKey': 'scenes:pavilion_reboot/restroom_entrance',
    'approvedVersion': 'A01 v09 microphone final', 'source': source,
    'meaningfulDefectsDemonstrated': [], 'regions': regions, 'protected': protected,
    'proposedRepairMaskPixels': 0, 'artworkPixelsChanged': 0, 'candidateProduced': False,
    'maskPolicy': 'All 64,684 artwork pixels protected. Black = no proposed edits. Context rectangles only locate details; they are not edit masks.',
    'perspectiveFinding': 'No demonstrated perspective or grounding defect. Construction traces are approximate inspection aids, not recovered camera calibration. The seated figure is occluded by the desk; no visible feet are required.',
    'microphoneFinding': 'The original approved 59-pixel v09 correction remains byte-identical. Its [196,123,203,143] bounds are protected, as is the full scene. No thickening, straightening, deletion or reconstruction.',
    'deviceFinding': 'Preserve existing left cream feed equipment and right plant. Keep the unwanted extra desktop device absent. Do not transfer the closer background intercom footprint onto the main scene.',
    'continuityFindings': [
        'Record Printer reuses the establishing architecture and desk, adding receipt activity from the left unit. Matching-coordinate scene and crop comparisons are included.',
        'Paper Emergency v04 is now Nate-selected/approved, with urgent face and hand repairs; its separate Claude registration is still pending. The canonical preview remains v03. Both are shown and clearly labeled; do not propagate either emergency pose into A01.',
        'The approved close background uses an independent camera: matching tile/teal/coral/cream materials, doorway/gate, left intercom, gooseneck microphone and right plant. Different device scale and framing are not exact-coordinate continuity errors.',
        'The idle portrait and main attendant agree on swept gray/dark hair, glasses, cream shirt, teal vest, tie, badge and reassuring clasped-hands pose. An unmodified same-size layer composite demonstrates the approved conversation pairing.'
    ],
    'narrativeFinding': 'Reassuring seated attendant fits the establishing/greeting/refusal states. door_choices uses the separately approved alarmed portrait; no full-scene expression replacement is needed. Visitor motion, reader turns red and the bench sign are narrated beats, not requirements to cram new figures or tiny text into A01.',
    'manualFinishFinding': 'No manual finish is justified by a demonstrated readability defect at native or exact 4×. Reopen only for a specific overlap or pixel problem identified in visual review.',
    'nativeGridAuthorshipLimitation': 'Original full-scene native-grid authorship remains unresolved/unproven. The historical localized microphone edit is coordinate-authored; that does not prove the inherited scene. High color count and source-derived softness alone do not justify alteration.'}
write_json('assessment/targeted-assessment.json', assessment)

def metrics(path):
    image = Image.open(B / path)
    alpha = image.convert('RGBA').getchannel('A')
    values = list(alpha.get_flattened_data())
    return {'dimensions': list(image.size), 'mode': image.mode,
            'uniqueRGB': len(set(image.convert('RGB').get_flattened_data())),
            'alphaExtrema': list(alpha.getextrema()), 'transparentPixels': values.count(0),
            'partialAlphaPixels': sum(0 < a < 255 for a in values)}

manifest = {
    'schema': 'out-of-order-targeted-quality-assessment-v1', 'date': '2026-11-22',
    'version': 'v06 assessment only; not new A01 artwork', 'assessmentStatus': 'generated/unselected; awaiting Nate visual review',
    'approvedArtworkStatus': 'approved, unchanged', 'recommendation': 'KEEP',
    'artDirection': 'Maximum useful detail, minimum unnecessary pixel noise.',
    'reviewBranch': 'art/ch3-native-pilot-20261121', 'startingReviewCommit': baseline['commit'],
    'verifiedMain': baseline['verifiedMain'], 'approvedSource': source,
    'approvedOriginal': 'originals/approved-restroom-entrance.png', 'references': refs,
    'metrics': metrics('originals/approved-restroom-entrance.png'),
    'referenceMetrics': {r['reviewFile']: metrics(r['reviewFile']) for r in refs},
    'candidateProduced': False, 'artworkPixelsChanged': 0, 'proposedRepairMaskPixels': 0,
    'protectedArtworkPixels': 64684, 'changedPixelList': 'sources/changed-pixels.json',
    'nativeGridAuthorshipLimitation': assessment['nativeGridAuthorshipLimitation'],
    'noGenerationNoFiltering': True, 'registrationPerformed': False, 'integrationPerformed': False,
    'mergePerformed': False, 'pagesDeploymentPerformed': False, 'chapter4Changes': False,
    'priorTrackedFilesProtected': len(baseline['files']),
    'baselineSourceRemoteVerified': 'sources/source-a87155b-A01-v09.png',
    'historicalLabelRule': 'Copied historical v09 generated/unselected labels describe its earlier review. The later Batch A ledger approves these exact bytes; this assessment leaves that approval intact.',
    'prompts': 'sources/brief.txt and sources/review-direction.txt; no image generation invoked.'}
write_json('manifest.json', manifest)

css = '''*{box-sizing:border-box}body{margin:0;background:#f1eee6;color:#293d43;font:16px/1.6 system-ui,sans-serif}main{max-width:1400px;margin:auto;padding:30px}h1{font-size:36px;line-height:1.2}p{max-width:1120px}a{color:#17616d}.notice{background:#e2ece3;padding:18px;border-left:5px solid #367c6c}.scroll{overflow:auto;padding-bottom:16px}.pair{display:flex;gap:22px;width:max-content}figure{margin:0;flex:none}figcaption{font-size:13px;padding:6px 0}img{display:block;max-width:none;image-rendering:pixelated}summary{cursor:pointer;font-weight:650;padding:10px 0}code{font-size:12px;overflow-wrap:anywhere}.facts{background:#eef0e8;padding:14px;font-size:13px;overflow-wrap:anywhere}button{font:inherit;padding:5px 12px}section{background:#fffdf8;padding:22px;border:1px solid #c9d2ca;margin:24px 0;border-radius:6px}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:10px 8px;border-bottom:1px solid #cad3cc;vertical-align:top;font-size:14px}@media(max-width:700px){main{padding:14px}h1{font-size:28px}}'''
def image(p, label):
    w, h = Image.open(B / p).size
    return f'<figure><figcaption>{escape(label)} · {w}×{h}</figcaption><img src="{p}" width="{w}" height="{h}" alt="{escape(label)}"></figure>'
def pair(a, b, la, lb):
    return '<div class="scroll"><div class="pair">' + image(a, la) + image(b, lb) + '</div></div>'
def enlarged(body, title='Exact 4× views'):
    return '<details class="four"><summary>' + escape(title) + '</summary>' + body + '</details>'
def single(p, label):
    return '<div class="scroll">' + image(p, label) + '</div>'

h = [f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Restroom Entrance A01 preservation-first assessment</title><style>{css}</style><main>',
     '<p>OUT OF ORDER · CHAPTER 3 · RESTROOM ENTRANCE TARGETED ASSESSMENT · NOVEMBER 22, 2026</p><h1>Restroom Entrance · approved A01 v09</h1>',
     '<p><strong>Maximum useful detail, minimum unnecessary pixel noise.</strong> This v06 package assesses the currently approved A01. It does not create a new artwork version.</p>',
     '<p class="notice"><strong>Recommendation: KEEP.</strong> No meaningful defect is demonstrated at native or exact 4× size. Protect the attendant, corrected microphone, existing desk layout, equipment separation, signs and architectural depth. <strong>Zero artwork pixels changed; no candidate and no open repair mask.</strong> Existing approval stays intact.</p>',
     '<p><a href="#regions">Region findings</a> · <a href="#guides">Protection and perspective</a> · <a href="#continuity">Continuity</a> · <a href="#qa">Evidence and QA</a> · <a href="README.md">GitHub review page</a></p>',
     '<p><button id="expand" type="button">Open exact 4× views</button> <button id="collapse" type="button">Close enlarged views</button></p>',
     pair('originals/approved-restroom-entrance.png', 'assessment/protected-detail-guide-native.png', 'Approved A01 v09 · native, unchanged', 'Protected-detail guide · diagnostic only'),
     enlarged(pair('previews/approved-restroom-entrance-4x.png', 'assessment/protected-detail-guide-4x.png', 'Approved original · exact 4×', 'Protected guide · exact 4×')),
     '<p><a href="comparisons/approved-left-protected-guide-right-native.png">Direct native comparison PNG</a> · <a href="comparisons/approved-left-protected-guide-right-4x.png">Direct exact 4× comparison PNG</a></p>',
     '<section id="regions"><h2>Specific region findings</h2><p>All listed regions: KEEP. These rectangles are inspection windows; no region is authorized for repair.</p><table><thead><tr><th>Region</th><th>Finding</th><th>Action</th></tr></thead><tbody>']
for item in regions:
    h.append('<tr><td>' + escape(item['name']) + '</td><td>' + escape(item['finding']) + '</td><td>KEEP</td></tr>')
h.append('</tbody></table>')
for item in regions:
    h.append('<h3>' + escape(item['name']) + '</h3>' + single('assessment/' + item['id'] + '-native.png', 'Unchanged approved native crop') + enlarged(single('assessment/' + item['id'] + '-4x.png', 'Same approved crop · exact 4×')))
h += ['</section><section id="guides"><h2>Protect the accepted corrections and geometry</h2><p>Green outlines locate successful details. All 64,684 source pixels are protected, including areas between these outlines. Cyan traces architectural edges, amber traces depth/floor direction, and magenta marks support/desktop contacts. These are approximate review guides, not a recovered camera model or edit masks. No new geometric correction is justified.</p>',
      enlarged(single('assessment/protected-detail-guide-4x.png', 'Protected detail locations · exact 4×') + single('assessment/perspective-construction-4x.png', 'Perspective and contact traces · exact 4×'), 'Protected-detail and perspective guides at exact 4×'),
      '<ul>' + ''.join('<li>' + escape(p['name']) + '</li>' for p in protected) + '</ul>',
      '<p>' + escape(assessment['microphoneFinding']) + '</p><p>' + escape(assessment['deviceFinding']) + '</p>',
      '<p><a href="masks/proposed-repair-mask.png">Proposed repair mask: all black, 0 pixels</a> · <a href="masks/protected-pixels.png">Protected mask: all white, 64,684 pixels</a> · <a href="sources/changed-pixels.json">Changed pixels: empty list</a> · <a href="assessment/perspective-guides.json">Exact guide coordinates and limitations</a></p>',
      '<p>No manual finish is justified by a demonstrated readability defect. No palette reduction, sharpening, downsampling or full-scene reconstruction was performed.</p></section>',
      '<section id="continuity"><h2>Narrative and cross-scene continuity</h2><p>' + escape(assessment['narrativeFinding']) + '</p>']
for text in assessment['continuityFindings']:
    h.append('<p>' + escape(text) + '</p>')
for name, label in [('record-printer', 'Approved Record Printer'), ('paper-emergency-selected-v04', 'Nate-selected Paper Emergency v04 · registration pending'), ('paper-emergency-canonical-v03', 'Historical Paper Emergency v03 · still canonical until Claude registration')]:
    h.append('<h3>' + escape(label) + '</h3>' + pair('originals/approved-restroom-entrance.png', 'references/' + name + '.png', 'Restroom Entrance · native', label + ' · native'))
    h.append(enlarged(pair('previews/approved-restroom-entrance-4x.png', 'previews/' + name + '-4x.png', 'Restroom Entrance · exact 4×', label + ' · exact 4×'), 'Matching-scale exact 4× scene comparison'))
    for crop in ['attendant', 'desk-layout']:
        h.append(enlarged(single('comparisons/' + crop + '-restroom-left-' + name + '-right-4x.png', 'Restroom left / reference right · same crop coordinates'), crop + ' continuity at exact 4×'))
h += ['<h3>Approved conversation layers · independent close camera</h3>',
      pair('references/restroom-close-background.png', 'references/attendant-idle.png', 'Approved A02 close background · native', 'Approved A03 idle portrait · native, separate transparent layer'),
      single('assessment/approved-conversation-composite-native.png', 'Diagnostic pairing of unchanged approved layers · native; not a registered asset'),
      enlarged(single('previews/restroom-close-background-4x.png', 'Approved close background · exact 4×') + single('assessment/approved-conversation-composite-4x.png', 'Diagnostic approved-layer pairing · exact 4×'), 'Closer view and portrait pairing at exact 4×'),
      '<p>The larger intercom in the close camera is already approved. Do not import its footprint, a new device or portrait facial microdetail into A01. The scene-scale greeting is already readable.</p></section>',
      '<section id="qa"><h2>Source contracts, preservation and QA</h2><div class="facts"><strong>Record:</strong> <code>scenes:pavilion_reboot/restroom_entrance</code><br><strong>Approved source:</strong> A01 v09 microphone final<br><strong>Source commit:</strong> <code>' + source['source']['commit'] + '</code><br><strong>SHA-256:</strong> <code>' + source['sha256'] + '</code><br><strong>Native:</strong> 314×206, opaque RGB. Exact 4×: 1256×824.<br><strong>Unique RGB colors:</strong> ' + str(manifest['metrics']['uniqueRGB']) + ' (descriptive, no palette target).<br><strong>Changed artwork pixels:</strong> 0 / 64,684. Candidate: none. Proposed repair mask: 0.</div>',
      '<p>' + escape(assessment['nativeGridAuthorshipLimitation']) + '</p>',
      '<p><a href="manifest.json">Manifest, sources and color/opacity metrics</a> · <a href="assessment/targeted-assessment.json">Complete findings</a> · <a href="qa/preservation.json">Byte and mask validation</a> · <a href="qa/results.json">Checks actually run and not run</a> · <a href="qa/browser.json">Browser QA</a> · <a href="sources/narrative-excerpts.json">Exact narrative excerpts</a> · <a href="sources/approved-ledger-excerpt.md">Current approval evidence</a> · <a href="sources/historical-v09-edit-record.json">Historical microphone edit record</a> · <a href="sources/historical-v09-qa.json">Historical microphone QA</a> · <a href="sources/paper-v04-selection-receipt.json">Paper v04 owner selection receipt</a></p>',
      '<p>All ' + str(len(baseline['files'])) + ' pre-existing tracked files remain byte-identical. All earlier candidates, approval records, canonical registries and production paths remain unchanged. No Chapter 4 change.</p>',
      '<p><strong>Stop for Nate’s visual review.</strong> No canonical registration, gameplay integration, merge or public Pages deployment.</p></section></main><script>document.getElementById("expand").onclick=()=>document.querySelectorAll("details.four").forEach(d=>d.open=true);document.getElementById("collapse").onclick=()=>document.querySelectorAll("details").forEach(d=>d.open=false);</script></html>']
html = '\n'.join(h)
(B / 'index.html').write_text(html)
portable = re.sub(r'src="([^"]+)"', lambda m: 'src="data:image/png;base64,' + base64.b64encode((B / m[1]).read_bytes()).decode() + '"', html)
(B / 'standalone-gallery.html').write_text(portable)

readme = '''# Restroom Entrance A01 targeted assessment

**Recommendation: KEEP the approved A01 v09 unchanged.** No meaningful defect is demonstrated at native or exact 4×. Zero artwork pixels changed. No candidate; the proposed repair mask is closed (0 pixels). This v06 package is an assessment version, not a new artwork version.

[Portable browser gallery](standalone-gallery.html) · [HTML assessment](index.html) · [Full findings](assessment/targeted-assessment.json) · [Manifest](manifest.json) · [Actual QA](qa/results.json)

![Approved original left, protected guide right, native](comparisons/approved-left-protected-guide-right-native.png)

[Direct native comparison](comparisons/approved-left-protected-guide-right-native.png) · [Direct exact 4× comparison](comparisons/approved-left-protected-guide-right-4x.png) · [Original exact 4×](previews/approved-restroom-entrance-4x.png)

## Findings and protection

- Reassuring smile, glasses, hair, clasped hands, cream shirt, teal vest, tie and badge fit the entrance dialogue and approved idle portrait. No expression or silhouette repair is justified.
- Preserve the earlier v09 microphone correction exactly: head, background gap, curved stem and desktop base. The copied historical edit record documents its 59-pixel correction; this assessment changes none of those pixels.
- Keep the left cream feed unit, centered attendant, right plant and counter geometry. Do not restore the separate unwanted desktop device or create a printer/plant overlap.
- RESTROOM, both two-person pictograms, doorway, reader, gate, interior fixtures, daylight and bench remain readable and grounded.
- No demonstrated wall, floor, furniture or equipment perspective error. The desk occludes the seated lower body; no visible feet are needed. Construction guides are approximate traces, not camera calibration.

[Protected-detail guide](assessment/protected-detail-guide-4x.png) · [Perspective/contact guide](assessment/perspective-construction-4x.png) · [Guide coordinates](assessment/perspective-guides.json) · [Closed repair mask](masks/proposed-repair-mask.png) · [Empty changed-pixel list](sources/changed-pixels.json)

## Continuity

Record Printer keeps the establishing layout and adds receipt activity at the left unit. Paper Emergency's urgent pose belongs to that later event; do not transfer it into the reassuring entrance image. The gallery shows both Nate-selected v04 (separate Claude registration pending) and historical v03 (still canonical), clearly labeled.

The approved portrait background is an independent close camera with consistent materials, doorway/gate, left intercom, microphone and right plant. Its larger intercom footprint is not a missing device to restore into A01. The unmodified approved background and idle portrait are shown separately and in a diagnostic composite; neither layer is edited.

No manual finish is presently justified by a demonstrated native/4× readability defect. Large palette and source-derived softness are not reasons to repaint successful details.

## Source and checks

Approved source: `a87155bfadad42e0deae3bee2e749963d1459a4b`, `CH3-A01-restroom-v09.png`.

SHA-256: `117dd9d00b6c9d32b4b153f71aaf51c2546ade70b803d45a748728f8d1a1f8b4`.

314×206 opaque RGB; exact 4× 1256×824. Original full-scene native-grid authorship remains unresolved/unproven. The earlier localized microphone authorship does not establish inherited full-scene authorship. No filtering, palette limit or image generation.

[Preservation evidence](qa/preservation.json) · [Actual QA / exclusions](qa/results.json) · [Current approval evidence](sources/approved-ledger-excerpt.md) · [Historical microphone correction](sources/historical-v09-edit-record.json) · [Narrative excerpts](sources/narrative-excerpts.json)

Stop for Nate's visual review. No canonical registration, gameplay integration, merge, public Pages deployment or Chapter 4 change.
'''
(B / 'README.md').write_text(readme)
print('Restroom Entrance: KEEP; 0 edits; 0 mask pixels;', manifest['metrics']['uniqueRGB'], 'colors;', len(baseline['files']), 'prior files protected.')
