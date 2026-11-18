"""Validate review packaging, reporting unmet artwork requirements separately."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import subprocess
from PIL import Image, ImageChops

R = Path(__file__).resolve().parent
ROOT = R.parents[4]
BASE = '2a1022ba7d96f9cf887402fc59c8266f81be577c'
EXPECTED = ['CH3-A01-restroom', 'CH3-A02-restroom-bg', 'CH3-A03-attendant-idle',
            'CH3-A04-verification', 'CH3-A05-verification-bg', 'CH3-A06-presenter-idle']
m = json.loads((R / 'manifest.json').read_text())
checks = []


def check(condition, label):
    assert condition, label
    checks.append(label)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def equal(a, b):
    return a.mode == b.mode and a.size == b.size and a.tobytes() == b.tobytes()


check([c['id'] for c in m['candidates']] == EXPECTED, 'Exactly six authorized current candidate IDs, in order')
check(len(list((R / 'candidates').glob('*.png'))) == 6, 'Exactly six selectable candidate PNGs')
check(all(c['status'] == 'generated' and c['selected'] is False and c['assetPath'] is None for c in m['candidates']), 'All generated/unselected; all production assetPath values null')
briefs = json.loads((R / 'sources/registered-briefs.json').read_text())
calls = json.loads((R / 'generation-records.json').read_text())['calls']
for c in m['candidates']:
    native = Image.open(R / c['candidate'])
    original = Image.open(R / c['source'])
    w, h = native.size
    check(list(native.size) == c['dimensions'] and native.mode == c['mode'], c['id'] + ': correct export dimensions and mode')
    check(sha(R / c['candidate']) == c['sha256'] and sha(R / c['source']) == c['sourceSha256'], c['id'] + ': candidate and original hashes')
    check(equal(native, original.convert(native.mode).resize(native.size, Image.Resampling.NEAREST)), c['id'] + ': disclosed full-frame NEAREST export, no other processing')
    check(equal(Image.open(R / c['preview4x']), native.resize((4 * w, 4 * h), Image.Resampling.NEAREST)), c['id'] + ': exact 4x nearest-neighbor expansion')
    if native.mode == 'RGBA':
        alpha = native.getchannel('A')
        check(alpha.getextrema()[0] == 0 and alpha.getbbox() is not None, c['id'] + ': real transparent outside region and visible foreground')
        check(equal(alpha, original.getchannel('A').resize(native.size, Image.Resampling.NEAREST)), c['id'] + ': generated alpha preserved')
    b = next(b for b in briefs['records'] if b['id'] == c['id'])
    prompt = (R / c['prompt']).read_text()
    check(b['brief']['prompt'] in prompt and briefs['direction'] in prompt, c['id'] + ': exact full registered prompt and shared direction retained')

for c in calls:
    check(sha(R / 'generation-source' / c['filename']) == c['sha256'], c['filename'] + ': immutable generation source')
    check(sha(R / c['prompt']) == c['promptSha256'], c['filename'] + ': exact submitted prompt hash')
    check([sha(R / p) for p in c['references']] == c['referenceHashes'], c['filename'] + ': reference bytes and order')
    original = Path(c['originalToolPath'])
    if original.exists():
        check(sha(original) == c['sha256'], c['filename'] + ': byte-exact copy of original tool file')

for c in m['composites']:
    bg = next(r for r in m['candidates'] if r['id'] == c['backgroundId'])
    fg = next(r for r in m['candidates'] if r['id'] == c['foregroundId'])
    actual = Image.open(R / c['file'])
    expected = Image.alpha_composite(Image.open(R / bg['candidate']).convert('RGBA'), Image.open(R / fg['candidate'])).convert('RGB')
    check(equal(actual, expected), c['character'] + ': exact unchanged full-canvas layer composite')
    check(equal(Image.open(R / c['preview4x']), actual.resize((2256, 1112), Image.Resampling.NEAREST)), c['character'] + ': exact composite 4x proof')

for r in json.loads((R / 'references/manifest.json').read_text()):
    check(sha(R / 'references' / r['file']) == r['sha256'] == sha(ROOT / r['sourcePath']), r['file'] + ': approved reference copied unchanged')
for name in ['PNG_SHA256SUMS.txt', 'SOURCE_SHA256SUMS.txt']:
    for line in (R / name).read_text().splitlines():
        expected, path = line.split('  ', 1)
        check(sha(R / path) == expected, name + ': ' + path)

for p in ['story/artwork.draft.json', 'story/chapters/chapter-03.reboot-candidate.json',
          'docs/111_CH3_ARTWORK_PMO_HANDOFF_AND_NARRATIVE_LOCK_20261118.md',
          'docs/112_CH3_ARTWORK_AUDIT_AND_GENERATION_HANDOFF_20261118.md']:
    check((ROOT / p).read_bytes() == (R / 'sources' / p).read_bytes(), 'Authoritative source snapshot unchanged: ' + p)
blob = subprocess.check_output(['git', 'hash-object', 'story/chapters/chapter-03.reboot-candidate.json'], cwd=ROOT, text=True).strip()
check(blob == m['approvedNarrativeBlob'], 'Approved narrative blob remains pinned')
subprocess.run(['git', 'diff', '--exit-code', BASE, '--', 'story', 'assets/selected', 'tools/storyboard'], cwd=ROOT, check=True, stdout=subprocess.PIPE)
checks.append('No narrative, catalogue, selected-artwork or storyboard-viewer changes relative to preparation base')


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []
    def handle_starttag(self, tag, attrs):
        for key, val in attrs:
            if key in ('href', 'src') and val and not val.startswith(('#', 'http')):
                self.paths.append(val)


parser = Links()
parser.feed((R / 'index.html').read_text())
# qa.json is the output being written immediately after these checks.
check(all((R / p).exists() or p == 'qa.json' for p in parser.paths), 'All gallery image, prompt, download and evidence links resolve locally')
failures = []
for c in m['candidates']:
    if not c['authoredAtRequestedNativeSize']:
        failures.append({'id': c['id'], 'requirement': 'Original native-resolution artwork', 'result': 'FAIL',
                         'detail': f'Generator returned {c["sourceDimensions"]}; requested {c["dimensions"]}. Dimension-correct export is resampled.'})
    if c['mode'] == 'RGBA' and c['alpha']['partialAlphaPixels']:
        failures.append({'id': c['id'], 'requirement': 'Pixel-sharp 0/255 alpha', 'result': 'FAIL',
                         'detail': f'{c["alpha"]["partialAlphaPixels"]} partial-alpha pixels in preserved-alpha review export.'})
qa = {'reviewPackageIntegrity': 'PASS', 'artworkRequirements': 'NOT FULLY MET' if failures else 'PASS',
      'creativeApproval': 'NOT GRANTED — Nate selection required', 'checksPassed': len(checks),
      'checks': checks, 'unmetArtworkRequirements': failures,
      'palette': 'Counts and dominant colors measured in palette.json; no numeric palette cap was specified or imposed. No quantization or dithering applied.',
      'visualQA': 'VISUAL_QA.md', 'scope': 'Review package plus isolated Pages overlay workflow only; current public main supplies all existing site content.'}
(R / 'qa.json').write_text(json.dumps(qa, indent=2) + '\n')
print(json.dumps({k: qa[k] for k in ['reviewPackageIntegrity', 'artworkRequirements', 'checksPassed', 'unmetArtworkRequirements']}, indent=2))
