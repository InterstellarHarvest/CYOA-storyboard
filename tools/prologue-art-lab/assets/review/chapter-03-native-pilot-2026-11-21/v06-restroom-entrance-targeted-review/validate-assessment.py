"""Verify source identity, exact previews, closed masks and preservation."""
from pathlib import Path
from PIL import Image
from html.parser import HTMLParser
import base64
import hashlib
import json
import re
import subprocess

B = Path(__file__).resolve().parent
R = B.parents[5]
m = json.loads((B / 'manifest.json').read_text())
a = json.loads((B / 'assessment/targeted-assessment.json').read_text())
baseline = json.loads((B / 'sources/preservation-baseline.json').read_text())
checks = []

def check(name, value):
    checks.append({'name': name, 'pass': bool(value)})
    assert value, name

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

key = 'scenes:pavilion_reboot/restroom_entrance'
expected = '117dd9d00b6c9d32b4b153f71aaf51c2546ade70b803d45a748728f8d1a1f8b4'
source = m['approvedSource']
im = Image.open(B / m['approvedOriginal'])
check('Exact approved A01 hash', expected == source['sha256'] == sha(B / m['approvedOriginal']))
check('Pinned A01 source commit', source['source']['commit'] == 'a87155bfadad42e0deae3bee2e749963d1459a4b')
check('Approved original matches independently downloaded source', (B / m['approvedOriginal']).read_bytes() == (B / m['baselineSourceRemoteVerified']).read_bytes())
check('Matches latest fetched main bytes', subprocess.check_output(['git', 'show', baseline['verifiedMain'] + ':' + source['file']], cwd=R) == (B / m['approvedOriginal']).read_bytes())
preview = json.loads((R / 'story/artwork-preview.json').read_text())['images']
record = json.loads((R / 'story/artwork.draft.json').read_text())['scenes']['pavilion_reboot/restroom_entrance']
check('Canonical A01 remains unchanged and approved', preview[key] == source and record['status'] == 'approved' and record['assetPath'] is None)
check('Native contract opaque RGB 314x206', im.size == (314, 206) and im.mode == 'RGB' and im.convert('RGBA').getchannel('A').getextrema() == (255, 255))
check('Palette count descriptive only and accurate', m['metrics']['uniqueRGB'] == len(set(im.get_flattened_data())) == 17503)
check('KEEP without new candidate or defect', m['recommendation'] == a['recommendation'] == 'KEEP' and not a['meaningfulDefectsDemonstrated'] and not m['candidateProduced'] and not (B / 'candidate').exists())
check('No artwork changes claimed or made', m['artworkPixelsChanged'] == a['artworkPixelsChanged'] == 0 and json.loads((B / 'sources/changed-pixels.json').read_text()) == [])
repair = Image.open(B / 'masks/proposed-repair-mask.png')
protected = Image.open(B / 'masks/protected-pixels.png')
check('Closed native repair mask', repair.size == im.size and repair.mode == 'L' and repair.getextrema() == (0, 0))
check('Every original pixel protected', protected.size == im.size and protected.mode == 'L' and protected.getextrema() == (255, 255) and m['protectedArtworkPixels'] == 64684)
check('Original native-grid authorship limitation retained', 'unresolved/unproven' in a['nativeGridAuthorshipLimitation'])
old = json.loads((B / 'sources/historical-v09-edit-record.json').read_text())
check('Earlier microphone correction source preserved', old['sha256'] == expected and old['changedPixels'] == 59 and old['changedBounds'] == [196, 123, 203, 143])
mic = (196, 123, 203, 143)
check('Earlier microphone region unchanged', im.crop(mic).tobytes() == Image.open(R / source['file']).crop(mic).tobytes())
check('All region decisions KEEP', len(a['regions']) == 6 and all(r['action'] == 'KEEP' for r in a['regions']))
for region in a['regions']:
    p = B / 'assessment' / (region['id'] + '-native.png')
    check('Native source crop ' + region['id'], Image.open(p).tobytes() == im.crop(region['box']).tobytes())
for ref in m['references']:
    check('Reference exact hash ' + ref['reviewFile'], sha(B / ref['reviewFile']) == ref['sha256'])
    if ref['canonicalAtVerifiedMain']:
        check('Reference unchanged from main ' + ref['reviewFile'], subprocess.check_output(['git', 'show', baseline['verifiedMain'] + ':' + ref['file']], cwd=R) == (B / ref['reviewFile']).read_bytes())
    else:
        check('Selected Paper v04 matches pinned source blob', subprocess.check_output(['git', 'show', ref['source']['commit'] + ':' + ref['source']['path']], cwd=R) == (B / ref['reviewFile']).read_bytes())
check('Paper canonical preview remains v03', preview['scenes:pavilion_reboot/paper_emergency']['sha256'] == 'ac0f7c44d267dd54897507ae3b8b02959a5b76f4fcd9d0418b77b8fdb777ba7e')
receipt = json.loads((B / 'sources/paper-v04-selection-receipt.json').read_text())
check('Paper v04 creative approval preserved separately', receipt['approved'] and receipt['selected'] and not receipt['canonicalRegistrationPerformed'] and receipt['selectedFile']['sha256'] == '93a48082124600b1afeb45e5ea54856bf253e858e55111295e9d9c26919bc978')
for path in (B / 'previews').glob('*-4x.png'):
    name = path.name.removesuffix('-4x.png')
    original = B / ('originals/' + name + '.png' if name == 'approved-restroom-entrance' else 'references/' + name + '.png')
    native = Image.open(original)
    check('Exact 4x preview ' + path.name, Image.open(path).tobytes() == native.resize((native.width * 4, native.height * 4), Image.Resampling.NEAREST).tobytes())
for folder in ['assessment', 'comparisons']:
    for path in (B / folder).glob('*-4x.png'):
        native = Image.open(path.with_name(path.name.replace('-4x.png', '-native.png')))
        big = Image.open(path)
        check('Exact 4x diagnostic ' + folder + '/' + path.name, big.size == (native.width * 4, native.height * 4) and big.tobytes() == native.resize(big.size, Image.Resampling.NEAREST).tobytes())
bg = Image.open(B / 'references/restroom-close-background.png').convert('RGBA')
fg = Image.open(B / 'references/attendant-idle.png').convert('RGBA')
check('Diagnostic composite uses unchanged aligned layers', Image.open(B / 'assessment/approved-conversation-composite-native.png').tobytes() == Image.alpha_composite(bg, fg).tobytes())
pair = Image.open(B / 'comparisons/approved-left-protected-guide-right-native.png')
check('Native pair left panel is exact original', pair.size == (628, 206) and pair.crop((0, 0, 314, 206)).tobytes() == im.tobytes())

class HTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images, self.links, self.ids = [], [], []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'img':
            self.images.append(attrs)
        if tag == 'a':
            self.links.append(attrs['href'])

h = HTML()
h.feed((B / 'index.html').read_text())
check('Unique HTML anchors', len(h.ids) == len(set(h.ids)))
for item in h.images:
    check('Gallery image contract ' + item['src'], Image.open(B / item['src']).size == (int(item['width']), int(item['height'])))
for link in h.links:
    if link.startswith('#'):
        check('Gallery anchor ' + link, link[1:] in h.ids)
    elif not link.startswith(('http', 'qa/')):
        check('Local evidence link ' + link, (B / link).is_file())
portable = HTML()
portable.feed((B / 'standalone-gallery.html').read_text())
check('Portable gallery same image count', len(portable.images) == len(h.images))
check('Portable image bytes exact', all(p['src'].startswith('data:image/png;base64,') and base64.b64decode(p['src'].split(',', 1)[1]) == (B / n['src']).read_bytes() for p, n in zip(portable.images, h.images)))
for link in re.findall(r'\]\(([^)]+)\)', (B / 'README.md').read_text()):
    if not link.startswith(('http', 'qa/')):
        check('README evidence link ' + link, (B / link).is_file())
changed = [f for f, expected in baseline['files'].items() if sha(R / f) != expected]
check('All pre-existing tracked files byte-identical', len(baseline['files']) == 1037 and not changed)
check('Review starts at prior published head', baseline['commit'] == 'aaba261a1522f5ddd9c663ebed8fa19bb4c49054')
check('No registration/integration/deployment', not any(m[k] for k in ['registrationPerformed', 'integrationPerformed', 'mergePerformed', 'pagesDeploymentPerformed', 'chapter4Changes']))
report = {'result': 'PASS', 'checkCount': len(checks), 'checks': checks,
          'priorTrackedFilesPreserved': len(baseline['files']), 'priorFilesChanged': changed,
          'approvedA01Sha256': expected, 'recommendation': 'KEEP', 'candidateProduced': False,
          'artworkPixelsChanged': 0, 'proposedRepairMaskPixels': 0, 'protectedPixels': 64684,
          'registrationPerformed': False, 'canonicalA01Unchanged': True, 'paperCanonicalStillV03': True}
(B / 'qa/preservation.json').write_text(json.dumps(report, indent=2) + '\n')
print('PASS:', len(checks), 'checks;', len(baseline['files']), 'prior files unchanged; A01 KEEP, zero edits.')
