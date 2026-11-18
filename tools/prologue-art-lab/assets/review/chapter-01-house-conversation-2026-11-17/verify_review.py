"""Verify the review delivery's image bytes, integer pixels, local links and scope."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import subprocess
from PIL import Image, ImageChops

R = Path(__file__).resolve().parent
ROOT = R.parents[4]
BASE = 'b3e374b9a12c1bd2e60ec437293a734ffe562d33'
BRANCH_BASE = '1ce7e79641e764d11367d476c7ede9ee0e8614c2'
records = json.loads((R / 'generation-records.json').read_text())['records']


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


results = []
for rec in records:
    native = Image.open(R / rec['candidate'])
    four = Image.open(R / rec['preview4x'])
    original = Image.open(R / rec['source'])
    expected = original.convert('RGB').resize((564, 278), Image.Resampling.NEAREST)
    exact_native = ImageChops.difference(native, expected).getbbox() is None
    exact_four = ImageChops.difference(four, native.resize((2256, 1112), Image.Resampling.NEAREST)).getbbox() is None
    original_untouched = sha(Path(rec['originalToolPath'])) == rec['sourceSha256'] if Path(rec['originalToolPath']).is_file() else None
    checks = {
        'candidate': rec['candidate'], 'nativeSize': list(native.size), 'mode': native.mode,
        'nativeDimensionsPass': native.size == (564, 278), 'opaqueRGBPass': native.mode == 'RGB',
        'previewDimensionsPass': four.size == (2256, 1112), 'sourceSamplingExact': exact_native,
        'every4xPixelExact': exact_four, 'originalToolOutputByteExact': original_untouched,
        'candidateHashPass': sha(R / rec['candidate']) == rec['candidateSha256'],
        'sourceHashPass': sha(R / rec['source']) == rec['sourceSha256'],
        'previewHashPass': sha(R / rec['preview4x']) == rec['previewSha256'],
        'promptHashPass': sha(R / rec['prompt']) == rec['promptSha256'],
        'aspectRatioChangePercent': rec['aspectRatioChangePercent'],
    }
    assert all(v for k, v in checks.items() if k.endswith('Pass') or k in ['sourceSamplingExact', 'every4xPixelExact'])
    assert original_untouched is not False
    results.append(checks)

references = json.loads((R / 'references/manifest.json').read_text())
for name, ref in references.items():
    assert sha(R / 'references' / f'{name}.png') == ref['sha256'] == sha(ROOT / ref['canonicalPath'])
    im = Image.open(R / 'references' / f'{name}.png')
    four = Image.open(R / 'references' / f'{name}-4x.png')
    assert ImageChops.difference(four, im.resize((im.width * 4, im.height * 4), Image.Resampling.NEAREST)).getbbox() is None

for p in (R / 'sources').rglob('*'):
    if p.is_file() and p.relative_to(R / 'sources').parts[0] in ['story', 'docs']:
        relative = p.relative_to(R / 'sources').as_posix()
        pinned = subprocess.check_output(['git', 'show', f'{BASE}:{relative}'], cwd=ROOT)
        assert p.read_bytes() == pinned
        if relative != 'story/artwork.draft.json':
            assert p.read_bytes() == (ROOT / relative).read_bytes()

changes = subprocess.check_output(['git', 'diff', '--name-only', BRANCH_BASE], cwd=ROOT, text=True).splitlines()
prefix = R.relative_to(ROOT).as_posix() + '/'
assert all(p.startswith(prefix) for p in changes), changes
registry = json.loads((ROOT / 'story/artwork.draft.json').read_text())
for room in ['lounge', 'dining']:
    original_brief = json.loads((R / 'sources/registered-briefs.json').read_text())[room]
    assert registry['portraits']['house:idle']['views'][f'house_of_tomorrow/{room}'] == original_brief
    assert registry['portraits']['house:idle']['views'][f'house_of_tomorrow/{room}']['assetPath'] is None
    assert not (ROOT / f'art/portraits/house/{room}_conversation.png').exists()
    assert not (ROOT / f'assets/selected/art/portraits/house/{room}_conversation.png').exists()


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for key, val in attrs:
            if key in ['src', 'href'] and val and not val.startswith(('#', 'http')):
                self.links.append(val)


links = Links()
links.feed((R / 'index.html').read_text())
pending = {'qa.json', 'browser-qa.json'}
for target in links.links:
    assert (R / target).is_file() or target in pending, target

report = {
    'pass': True, 'generationBaseCommit': BASE, 'branchBaseCommit': BRANCH_BASE, 'nativeCandidatesValidated': len(results),
    'images': results, 'approvedReferencesByteExact': True,
    'allReference4xPixelsExact': True, 'sourceSnapshotsMatchPinnedGenerationBase': True,
    'targetBriefsAndChapter1SourcesMatchCurrentBranchBase': True,
    'localGalleryLinksChecked': len(links.links), 'localGalleryLinksPass': True,
    'canonicalTrackedChangesOutsideReview': [], 'productionPathsRemainNullAndAbsent': True,
    'selectedArtworkAndChapter2Preserved': True, 'chapter3AndBatchBConversionsUnchanged': True,
    'artisticApproval': 'none; unselected pending Art Director review',
    'limitation': 'Nearest native export from non-integer-grid generated originals; logical-grid authorship and aesthetic consistency require visual review.',
}
(R / 'qa.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
