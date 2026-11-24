"""Verify exact pinned v01 B2-06 approval, associations and preservation."""
from pathlib import Path
from io import BytesIO
from PIL import Image
import copy, hashlib, json, subprocess

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / 'docs/134_CH4_B206_APPROVAL_COMPLETION_20261123.json'
def digest(data): return hashlib.sha256(data).hexdigest()
def blob(commit, path): return subprocess.check_output(['git', 'show', commit + ':' + path], cwd=ROOT)
def main():
    d = json.loads(DOC.read_text()); checks = []
    def check(value, label):
        assert value, label
        checks.append({'check': label, 'passed': True})
    base = d['canonicalBase']; source = d['approvalSourceCommit']
    catalog = json.loads((ROOT / 'story/artwork.draft.json').read_text())
    previews = json.loads((ROOT / 'story/artwork-preview.json').read_text())['images']
    nodes = json.loads((ROOT / 'story/chapters/chapter-04.wip.json').read_text())['nodes']
    for a in d['assets']:
        sm = a['sourceManifest']; raw = blob(source, sm['path'])
        check(digest(raw) == sm['sha256'], 'Pinned source manifest ' + a['id'])
        m = json.loads(raw)
        item = m if 'assetId' in m else next(x for x in m['assets'] if x['id'] == a['id'])
        original = blob(source, a['source']['path']); registered = (ROOT / a['canonicalSelectedPath']).read_bytes()
        check(digest(original) == digest(registered) == a['sha256'] == item['native']['sha256'], 'Exact owner/source/selected PNG ' + a['id'])
        native = Image.open(BytesIO(registered))
        check(list(native.size) == a['dimensions'] and native.mode == a['mode'], 'Native dimensions/mode ' + a['id'])
        alpha = native.convert('RGBA').getchannel('A').getextrema()
        check(alpha[0] == 0 if a['kind'] == 'portrait' else alpha == (255, 255), 'Alpha contract ' + a['id'])
        large_bytes = blob(source, a['approvedPreview4x']['path']); large = Image.open(BytesIO(large_bytes))
        check(digest(large_bytes) == a['approvedPreview4x']['sha256'] and large.size == (native.width*4, native.height*4) and large.tobytes() == native.resize(large.size, Image.Resampling.NEAREST).tobytes(), 'Exact approved 4x preview ' + a['id'])
        p = previews[a['registryKey']]
        check(p['file'] == a['canonicalSelectedPath'] and p['sha256'] == a['sha256'] and p['source'] == a['source'], 'Selected mapping/provenance ' + a['id'])
        group, key = a['registryKey'].split(':', 1)
        record = catalog[group][key.split('#')[0]]['portraitBackground'] if '#' in key else catalog[group][key]
        check(record['status'] == 'approved' and record['assetPath'] is None and record['suggestedFilename'] == a['suggestedEngineDestination'], 'Approved/selected without integration ' + a['id'])
        check('SOURCE-DERIVED' in record['notes'], 'Honest authorship provenance ' + a['id'])
        check(a['storyNodeIds'] == item['nodeIds'] and all(n in nodes for n in a['storyNodeIds']), 'Pinned story associations ' + a['id'])
        for nid in a['storyNodeIds']:
            n = nodes[nid]
            check(n.get('speaker') + ':' + n.get('pose') == key if group == 'portraits' else n.get('focus') == key if group == 'focus' else n.get('scene') == key.split('#')[0], 'Canonical node mapping ' + a['id'] + ':' + nid)
    for path in subprocess.check_output(['git','ls-tree','-r','--name-only',base,'docs','tools/prologue-art-lab/assets/approved/conditional-production-references'],cwd=ROOT,text=True).splitlines():
        if path == 'docs/103_RETROACTIVE_ARTWORK_APPROVAL_LEDGER.md': continue
        check((ROOT / path).read_bytes() == blob(base,path), 'Previous approval/supplemental reference exact ' + path)
    for a in d['assets']:
        _,key = a['registryKey'].split(':',1)
        check(catalog['portraits'][key]['portraitBackgroundScene'] == a['portraitBackgroundScene'], 'Exact approved default dialogue context ' + a['id'])
        check(all(nodes[n]['scene'] in a['sceneKeys'] for n in a['storyNodeIds']), 'Every authored scene context retained ' + a['id'])
    check(source == 'f6840e5d69f70435f88ce9ece720583566fce8e2' and all(a['version']=='v01' for a in d['assets']), 'Exact owner-pinned source and six v01 versions')
    old = json.loads(blob(base, 'story/artwork-preview.json'))['images']
    for key, p in old.items():
        check(previews[key] == p and (ROOT / p['file']).read_bytes() == blob(base, p['file']), 'Prior selected metadata and bytes ' + key)
    check(len(previews) == len(old) + 6, 'Exactly six new selections')
    reduced = copy.deepcopy(catalog)
    for a in reversed(d['assets']):
        group, key = a['registryKey'].split(':', 1)
        if '#' in key: del reduced[group][key.split('#')[0]]['portraitBackground']
        else: del reduced[group][key]
    check(reduced == json.loads(blob(base, 'story/artwork.draft.json')), 'All previous artwork records unchanged')
    for path in subprocess.check_output(['git','ls-tree','-r','--name-only',base,'story','.github'], cwd=ROOT, text=True).splitlines():
        if path in ['story/artwork.draft.json','story/artwork-preview.json']: continue
        check((ROOT / path).read_bytes() == blob(base, path), 'Narrative/gameplay/workflow unchanged ' + path)
    ledger = 'docs/103_RETROACTIVE_ARTWORK_APPROVAL_LEDGER.md'
    check((ROOT / ledger).read_bytes().startswith(blob(base, ledger)), 'Previous approval ledger preserved')
    report = {'passed': True, 'checksPassed': len(checks), 'registeredAssets': 6, 'previousSelectionsPreserved': len(old), 'allSixApprovedAndSelected': True, 'sourceCommit': source, 'baseCommit': base, 'integrationPerformed': False, 'checks': checks}
    (ROOT / 'docs/134_CH4_B206_VERIFICATION_20261123.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'{len(checks)} checks passed; six approved/selected; {len(old)} prior selections preserved; no integration.')
if __name__ == '__main__': main()
