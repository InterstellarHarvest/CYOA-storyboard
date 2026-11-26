#!/usr/bin/env python3
"""Chapter 4 artwork closeout verifier (docs/152). Read-only.

Reconciles canonical main against the approved docs/137 consolidation plan without repeating
that audit: the 63 active primary requirements, every one of the 120 node-to-art mappings,
inventory and death art, the preserved conditional / inspection references with their nodes,
the six R1 candidates (deferred), and the integration blockers still present in canon.

  python3 tools/sync/verify-ch4-art-closeout.py               # storyboard checks, writes the report + node map
  python3 tools/sync/verify-ch4-art-closeout.py --game <dir>  # also runs game main's importer + validator read-only

Nothing in story/, assets/ or the game checkout is written. The --game probe copies game main's
convert.js, rules.js and runtime-settings.json into a temporary folder.
"""
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = '8e388e21035004d79280417985ddc98631621e6e'  # main after PR #43 (B2-19)
PR32_REF = 'refs/heads/review/ch4-ch403-assessment-b209-sheet-20261124'
PR32_HEAD = 'f320e63934c13e27fd13b9482d0cfba58911362d'
GAME_MAIN = 'c7a2d3dc7e19b8d574deedec0e5b4b7098daa9a1'  # game main at docs/140 (C1/C2 merged); re-read with --game
REPORT = ROOT / 'docs/152_CH4_ARTWORK_CLOSEOUT_VERIFICATION_20261126.json'
NODE_MAP = ROOT / 'docs/152_CH4_NODE_ART_MAP_20261126.tsv'
OWN = {'docs/152_CH4_ARTWORK_CLOSEOUT_AND_GAMEPLAY_HANDOFF_20261126.md', REPORT.relative_to(ROOT).as_posix(),
       NODE_MAP.relative_to(ROOT).as_posix(), 'tools/sync/verify-ch4-art-closeout.py'}
APPROVED = 'tools/prologue-art-lab/assets/approved'

sys.dont_write_bytecode = True  # importing the consolidation tool must not leave __pycache__ behind
spec = importlib.util.spec_from_file_location('cc', ROOT / 'tools/sync/ch4-consolidation.py')
cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)

EXPECT_DISPOSITIONS = {'RETAIN': 45, 'NEW': 17, 'NEW_RENDERER_EXCEPTION': 1, 'REUSE': 6, 'NARRATIVE': 14, 'RETIRED': 7}
CONTRACT = {'main_scene': ((314, 206), 'opaque'), 'portrait': ((564, 278), 'transparent'),
            'portrait_background': ((564, 278), 'opaque'), 'focus_a': ((564, 278), 'opaque'),
            'inventory_slot': ((96, 96), 'transparent'), 'inventory_inspect': ((565, 451), 'opaque'),
            'fatal_aftermath': ((314, 206), 'opaque')}
# C3 reuse at integration: scene keys that have no record of their own -> the approved scene they reuse.
REUSE_SCENES = {'grand_bellevue/wedding_entry': 'grand_bellevue/ballroom', 'grand_bellevue/refreshment_table': 'grand_bellevue/ballroom',
                'grand_bellevue/bridal_corridor': 'grand_bellevue/service_passage', 'grand_bellevue/freight_lift': 'grand_bellevue/upper_salvage'}
REUSE_BACKGROUNDS = {'grand_bellevue/refreshment_table': 'grand_bellevue/ballroom'}

# Six R1 refinement candidates: DEFERRED - NOT BLOCKING INTEGRATION. The approved bytes stay selected.
R1 = {'CH4-01': ('scenes:grand_bellevue/lobby', '582bcd51de937e5fe124160a8beb74b4ee469f52eeb6d9d0d38b918cfb0d6be0'),
      'CH4-04': ('scenes:grand_bellevue/restroom', None),
      'CH4-05': ('scenes:grand_bellevue/ballroom', None),
      'CH4-B2-03': ('scenes:grand_bellevue/restroom#portraitBackground', '77325aca0d3c61d5b6d1980232fb11fa55156454a26659c6887c4d726a82c377'),
      'CH4-B2-11': ('scenes:grand_bellevue/loading_dock#portraitBackground', None),
      'CH4-03': ('portraits:hotel_auctioneer:showman', '231baf25ffd00511144693927354e73f42cae4f052964a9db0a99323689a0d78')}
R1_STUDIES = [
    ('art/ch4-r1-auctioneer-review-20261126', '6e59549e2ccf4b60e77ba7783987fd26637fcbbe',
     'tools/prologue-art-lab/assets/review/chapter-04-r1-auctioneer-2026-11-26/REVIEW-STATUS.json', 'studySha256',
     'f345448c37a24342440301303314e05be9f19b202b39b3597f1461d857cf451c'),
    ('art/ch4-r1-restroom-material-pilot01-review-20261126', 'e06c93fa0618054a2c4e2b630f6544709db410bd',
     'tools/prologue-art-lab/assets/review/chapter-04-r1-restroom-material-pilot01-2026-11-26/REVIEW-STATUS.json', 'pilotSha256',
     '89b6e60d5999e0297a0f577ff80f5cb530b5f410e9c8e77b2c5082bb9504775e')]

# Every approved Chapter 4 file outside assets/selected: (path under APPROVED, sha256, approval doc, nodes).
REFS = [
    ('conditional-production-references/chapter-04/b2-04/CH4-B2-24-open-v01.png', 'a90e705303261114f882f0f270c195716f1a6e6b7384f6792373bc650c9b204c', '132', ['hotel_chair_stapler_stealth', 'hotel_chair_ring_focus']),
    ('conditional-production-references/chapter-04/b2-04/CH4-B2-25-slipped-v01.png', 'afc5ba21cf2b472a762538ee9bbeb8ae571f64e27815d36a3849fd9ba5dd6846', '132', ['hotel_ring_slips', 'hotel_collection_ring_focus']),
    ('conditional-production-references/chapter-04/b2-04/CH4-B2-25-recovered-v01.png', '6cd99a639036a2ae746d7e7bcaca30a4d3914ebb125a3a59fde62e3a37f7ade1', '132', ['hotel_collection_ring_porter_recovery', 'hotel_collection_ring_stapler_recovery']),
    ('conditional-production-references/chapter-04/b2-07/CH4-B2-37-cleared-v01.png', '97a1485382bfdda21a70258af8be957ace82fa19b0a8e64b3179e14e43ce73df', '135', ['hotel_staff_lavatory_move_boxes']),
    ('conditional-production-references/chapter-04/b2-07/CH4-B2-41-cleared-v01.png', '7eb87b07f2f1390e2e2d278c3f757d66db1e0afd8bcf716821bf9c324eeeb668', '135', ['hotel_staff_lavatory_move_boxes']),
    ('conditional-production-references/chapter-04/b2-07/CH4-B2-37-permit-v01.png', '1e410771e048a01f43ec77ddeee1d61a137338579a428e160e952d674a352c85', '135', ['hotel_staff_lavatory_temporary_use_permit']),
    ('conditional-production-references/chapter-04/b2-07/CH4-B2-41-permit-v01.png', '2bd720955c229d775d9b5f55ecb2bea4b74670c1e00517231e2d771d58e82831', '135', ['hotel_staff_lavatory_temporary_use_permit']),
    ('conditional-production-references/chapter-04/b2-08/CH4-B2-42-relieved-v01.png', '8278a9dbb107cdf62e5883a386626fff9b30d7d933e08e10a81c30bb9703c051', '136', ['hotel_boiler_pressure_relieved']),
    ('conditional-production-references/chapter-04/b2-08/CH4-B2-47-relieved-v01.png', '25b3b3bf50e84fe62510b43cda9072e976ad4c316eea8223ed04a0668d784692', '136', ['hotel_boiler_pressure_relieved']),
    ('conditional-production-references/chapter-04/b2-08/CH4-B2-42-inspection-hold-v01.png', '93f7ab9c125077718aa345b9374ee3368caf2499010ee4862b6e189205c7d482', '136', ['hotel_boiler_dispute_hold']),
    ('conditional-production-references/chapter-04/b2-08/CH4-B2-47-inspection-hold-v01.png', '01e200de1f21d56328dc876166bcc77ecd0bd43ba8ab7fee556f514bfcb2af0f', '136', ['hotel_boiler_dispute_hold']),
    ('conditional-production-references/chapter-04/b2-08/CH4-B2-42-staff-access-v01.png', 'b179c47d6cc0730ba7f88d8c5e8c159be46dca9c99539fce5da4186ddf8efbba', '136', ['hotel_boiler_staff_access']),
    ('conditional-production-references/chapter-04/b2-08/CH4-B2-47-staff-access-v01.png', 'fb67d5ae76b4f91de9995ed6095e396b769e688bbcc3f9e8931ae4a8ec56b7ea', '136', ['hotel_boiler_staff_access']),
    ('conditional-production-references/chapter-04/b2-09/CH4-NEW-18-wheel-mounted-v01.png', 'ba0e7961134a632a522331f57945dd7889f9ae158a27a67e1cadc16cbdf1afc9', '142', ['hotel_commodore_bixby']),
    ('conditional-production-references/chapter-04/b2-09/CH4-NEW-18-wheel-removed-v01.png', 'cc9d19c2413df5b017b72592e3d5c676a84ad0ad91c354093a0a9e0199233e7d', '142', ['hotel_bixby_emergency']),
    ('conditional-production-references/chapter-04/b2-09/CH4-NEW-18-rubber-band-fender-v01.png', '7c4261a915e62c91f394942eac5fe7c0e6f5fc847fcc68b248494cf76c0c850b', '142', ['hotel_bixby_trade']),
    ('conditional-production-references/chapter-04/b2-09/CH4-NEW-18-water-emerging-v01.png', 'b5b1b1d0cc775cc02cfb61447efe12950fe78ca3e6184602b07c42dac9cb6f65', '142', ['hotel_commodore_bixby', 'hotel_bixby_emergency', 'hotel_bixby_trade']),
    ('conditional-production-references/chapter-04/b2-11/CH4-NEW-04-public-corridor-flood-v04.png', 'f802ff0c9aa345147f6039779df8b49403cc96add6be89b13f2ef9396727212f', '144', ['hotel_flooded_public_corridor']),
    ('conditional-production-references/chapter-04/b2-12/CH4-NEW-07-focus-provisional-v02.png', 'b7d8014313519b67d3ebe8c72772ed0d01b4dbbb88748c9e5b0e7f589d669272', '145', ['hotel_bridal_door_focus']),
    ('inspection-references/chapter-04/b2-12/CH4-NEW-07-inspect-locked-v03.png', 'b571f3215be27ab7e86bdb67530a86d33e20ed6a0638842f88227fdbc06ec0e3', '145', ['hotel_bridal_door_focus']),
    ('inspection-references/chapter-04/b2-12/CH4-NEW-07-inspect-provisional-v03.png', 'fa4d465cd6c25b7591ff97caf2713e4b521ef3c2dba6243c5a571685f17660e9', '145', ['hotel_bridal_door_focus']),
    ('visual-design-masters/chapter-04/b2-12/CH4-NEW-07-locked-design-master-565x451-v01.png', '072e30b905014a3856e21190551307eab0b0298dd0624e831f5395951d3b7afb', '145', []),
    ('visual-design-masters/chapter-04/b2-12/CH4-NEW-07-provisional-design-master-565x451-v01.png', 'e546f7eb4d6de3a319548ee7759ab9ca83e415caa7293fb29322ca6f98ef44b3', '145', []),
    ('conditional-production-references/chapter-04/b2-13/CH4-NEW-08-manual-slack-revealed-v01.png', '592bc3e6a237745d9a066fe5d7424d1cb5f520caffbc0af2491eaf76d83bb98d', '147', ['hotel_bridal_gown_motor']),
    ('conditional-production-references/chapter-04/b2-18/restroom-active-leak-main.png', '9a6243310bb7af1958854110af742c603275b2ebf9c889050c6c065737e57279', '150', ['hotel_restroom_plumber']),
    ('conditional-production-references/chapter-04/b2-18/restroom-active-leak-close.png', '35a8f8297da89038a0a7b30596363bfa6ad86e3edc6b02bf0efb360a4dc3a46a', '150', ['hotel_restroom_plumber', 'hotel_wheel_buyer_lead']),
    ('conditional-production-references/chapter-04/b2-18/restroom-contained-main.png', '674cb60c905347e99c95b99ec87dfacc218cf15483abe89bc4e092d40b43ed1a', '150', ['hotel_wheel_return', 'hotel_key_master_cabinet', 'hotel_valve_braced']),
    ('conditional-production-references/chapter-04/b2-18/restroom-flood-onset-main.png', '432ce64f5e7e0420f678774ec8cf2edb02ce745ff532d83b3e1723af9d90fb46', '150', ['hotel_valve_flood']),
    ('conditional-production-references/chapter-04/b2-18/restroom-stall-lifting-main.png', '84976c116d9fc87b6ce8f4cf5d7f316d7185fa308f889df6d1c76eafe6bc525e', '150', ['hotel_stall_lot_claimed', 'hotel_stall_crane_success']),
    ('conditional-production-references/chapter-04/b2-19/lobby-doors-removed.png', 'e2aa3835dca0edf1e76b93df2a3cf628db8dc5ff8f56c1f5df8e6188ea7d218e', '151', ['hotel_auctioneer_arrival']),
    ('conditional-production-references/chapter-04/b2-19/lot61-open.png', '3913c8ad89c0245c31827f1933926ff0d1a00ec9da71f34dfa9818ff222c42b5', '151', ['hotel_lot61_pod_auction', 'hotel_lot61_pod_declined']),
    ('conditional-production-references/chapter-04/b2-19/lot61-packed.png', 'f3c27be75a18007850f8eb9bff7ae71f031063aa44735f9bfbd24bf5d876b558', '151', ['hotel_lot61_pod_escaped']),
    ('retired-selections/chapter-04/CH4-B2-16-v01.png', 'e396db0771247012401cccf3a481d329947381a677c445ccc0a04d61b21f77f3', '137', []),
]
STAFF_PASS = 'pavilion_temporary_staff_pass'
STAFF_PASS_CHOICES = {'collection_show_staff_pass', 'boiler_show_staff_pass'}


class Checks:
    def __init__(self):
        self.items, self.failed = [], []

    def __call__(self, ok, msg, detail=None):
        row = {'ok': bool(ok), 'check': msg}
        if detail is not None:
            row['detail'] = detail
        self.items.append(row)
        if not ok:
            self.failed.append(msg)
            print('FAIL', msg, '' if detail is None else json.dumps(detail)[:400])
        return ok


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git(*a, **kw):
    return subprocess.check_output(['git', *a], cwd=ROOT, **kw)


def png_info(p):
    from PIL import Image
    im = Image.open(p)
    im.load()
    alpha = 'transparent' if im.mode in ('RGBA', 'LA', 'P') and im.getextrema()[-1][0] == 0 else 'opaque'
    return im.size, im.mode, alpha


def preview_key(key):
    cat, lk = key.split(':', 1)
    if cat == 'inventory_slot':
        return 'items:' + lk + '#slot'
    if cat == 'inventory_inspect':
        return 'items:' + lk + '#inspect'
    if cat == 'fatal_aftermath':
        return 'deathScreens:' + lk
    return cc.preview_key(key)


def asset_id(rec):
    m = re.search(r'\b(CH4-(?:B2-|NEW-)?\d+)\b', (rec or {}).get('notes', ''))
    return m.group(1) if m else None


def first_sha(rec):
    m = re.search(r'\b[0-9a-f]{64}\b', (rec or {}).get('notes', ''))
    return m.group(0) if m else None


def strings(v, acc):
    if isinstance(v, dict):
        for k, x in v.items():
            acc.add(k)
            strings(x, acc)
    elif isinstance(v, list):
        for x in v:
            strings(x, acc)
    elif isinstance(v, str):
        acc.add(v)
    return acc


def main(argv):
    game = argv[argv.index('--game') + 1] if '--game' in argv else None
    check = Checks()
    chapter, art, preview = cc.load_canon()
    nodes = chapter['nodes']
    plan = json.loads((ROOT / 'docs/137_CH4_ARTWORK_CONSOLIDATION_PLAN_20261124.json').read_text())['requirements']
    docs_text = {p.name[:3]: p.read_text(encoding='utf-8') for p in sorted((ROOT / 'docs').glob('1[2-5][0-9]_CH4_*.md'))}
    docs_all = '\n'.join(docs_text.values())
    report = {'schema': 'out-of-order-ch4-artwork-closeout-v1', 'base': BASE}

    # 0. Scope: base commit and an additions-only change set.
    head = git('rev-parse', 'HEAD').decode().strip()
    check(subprocess.run(['git', 'merge-base', '--is-ancestor', BASE, 'HEAD'], cwd=ROOT).returncode == 0, 'HEAD descends from canonical base 8e388e2 (B2-19 merged)', head)
    changed = set(git('diff', '--name-only', BASE).decode().split()) | set(git('ls-files', '--others', '--exclude-standard').decode().split())
    check(changed <= OWN, 'Only the closeout document, its report/map and this verifier differ from base', sorted(changed - OWN))
    check(len(nodes) == 120, 'Chapter 4 has 120 nodes', len(nodes))

    # 1. The consolidated requirement set (docs/137), reconciled against current canon.
    from collections import Counter
    disp = Counter(r['disposition'] for r in plan.values())
    check(dict(disp) == EXPECT_DISPOSITIONS and len(plan) == 90, 'docs/137 plan: 90 logical requirements = 45 retain + 17 new + 1 renderer exception + 6 reuse + 14 no-image + 7 retired', dict(disp))
    active = {k: r for k, r in plan.items() if r['disposition'] in ('RETAIN', 'NEW', 'NEW_RENDERER_EXCEPTION')}
    check(len(active) == 63, 'Active primary target = 63 image requirements', len(active))
    rows = []
    for key, r in sorted(active.items()):
        rec = cc.registry_record(art, key)
        pk = preview_key(key)
        pv = preview.get(pk) or {}
        f = ROOT / pv.get('file', '-')
        ok = bool(rec) and rec.get('status') in ('approved', 'integrated') and f.is_file()
        info = {'key': key, 'disposition': r['disposition'], 'assetId': asset_id(rec) or r.get('assetId') or r.get('planId'),
                'status': rec and rec.get('status'), 'file': pv.get('file'), 'sha256': pv.get('sha256')}
        if ok:
            digest = sha(f)
            size, mode, alpha = png_info(f)
            want_size, want_alpha = CONTRACT[key.split(':', 1)[0]]
            ok = digest == pv['sha256'] and first_sha(rec) == digest and tuple(size) == want_size and alpha == want_alpha
            if r['disposition'] == 'RETAIN':
                ok = ok and digest == r['sha256']
            docs = sorted(n for n, t in docs_text.items() if digest in t)
            info.update({'size': list(size), 'mode': mode, 'alpha': alpha, 'approvalDocs': docs})
            ok = ok and bool(docs)
        rows.append(info)
        check(ok, 'Active %s %s: approved, previewed, contract size/alpha, preview = file = first approval SHA%s' % (
            info['assetId'], key, ' = docs/137 SHA' if r['disposition'] == 'RETAIN' else ''), None if ok else info)
    report['activeRequirements'] = rows

    # 1b. Reuse (C3), no-image presentation (C1/C2), retirements.
    for key, r in sorted(plan.items()):
        d = r['disposition']
        cat, lk = key.split(':', 1)
        if d == 'REUSE':
            src = active.get(r['source'])
            rec = cc.registry_record(art, key)
            if cat == 'portrait':
                sp, pose = lk.split(':')
                used = [n for n, x in nodes.items() if x.get('speaker') == sp and x.get('pose') == pose]
                check(src and not used, 'Reuse %s -> %s: approved source; no node still asks for the retired pose' % (key, r['source']), used)
            else:
                check(src is not None and rec is None, 'Reuse %s -> %s: approved source; no record of its own (registered as `reused` at integration, docs/137 C3)' % (key, r['source']))
        elif d == 'NARRATIVE':
            if cat == 'main_scene':
                rec = art['scenes'].get(lk) or {}
                check(rec.get('format') == 'text-led' and rec.get('status') == 'approved' and not rec.get('assetPath') and 'scenes:' + lk not in preview,
                      'No-image %s: text-led record (C1), no image, no preview' % key)
            elif cat == 'portrait':
                sp = lk.split(':')[0]
                vo = [k for k, v in art['portraits'].items() if k.startswith(sp + ':') and v.get('format') == 'voice-only']
                drawn = [k for k in preview if k.startswith('portraits:' + sp + ':')]
                check(len(vo) == 1 and not drawn, 'No-image %s: voice-only record (C2), no portrait image' % key, vo)
            else:
                speakers = {x['speaker'] for x in nodes.values() if x['mode'] == 'dialogue' and x['scene'] == lk}
                voice = {k.split(':')[0] for k, v in art['portraits'].items() if v.get('format') == 'voice-only'}
                bg = (art['scenes'].get(lk) or {}).get('portraitBackground')
                check(speakers <= voice and not bg, 'No-image %s: every dialogue speaker there is voice-only, so no closer background is drawn' % key, sorted(speakers - voice))
        elif d == 'RETIRED':
            if cat == 'portrait':
                rec = art['portraits'].get(lk) or {}
                sp, pose = lk.split(':')
                used = [n for n, x in nodes.items() if x.get('speaker') == sp and x.get('pose') == pose]
                pv = preview.get('portraits:' + lk) or {}
                check(rec.get('status') == 'approved' and rec.get('notes', '').startswith('ARCHIVED') and pv.get('sha256') == r['sha256']
                      and sha(ROOT / pv['file']) == r['sha256'] and not used,
                      'Archived %s (%s): approval, preview and bytes preserved; no active node uses it' % (key, r.get('assetId')))
            else:
                ledger = json.loads((ROOT / 'docs/137_CH4_RETIRED_ARTWORK_LEDGER_20261124.json').read_text())
                check(not (art['scenes'].get(lk) or {}).get('portraitBackground') and 'CH4-B2-16' in json.dumps(ledger)
                      and sha(ROOT / APPROVED / 'retired-selections/chapter-04/CH4-B2-16-v01.png') == r['sha256'],
                      'Retired CH4-B2-16: out of the active registry, ledger record and exact bytes preserved')

    # 2. Node-to-art map for all 120 nodes, as canon resolves today.
    def selected(pk):
        p = preview.get(pk)
        return p and (ROOT / p['file']).is_file() and sha(ROOT / p['file']) == p['sha256']
    refs_by_node = {}
    for path, digest, doc, ns in REFS:
        for n in ns:
            refs_by_node.setdefault(n, []).append(Path(path).stem)
    gaps, tsv = [], ['\t'.join(['node', 'mode', 'scene', 'mainScene', 'speaker', 'portrait', 'background', 'focus', 'endingArt', 'deathPopup', 'conditionalReferences'])]
    for nid, n in nodes.items():
        scene = n['scene']
        srec = art['scenes'].get(scene) or {}
        if srec.get('format') == 'text-led':
            main_art = 'TEXT-LED (C1)'
        elif selected('scenes:' + scene):
            main_art = asset_id(srec) or scene
        elif scene in REUSE_SCENES and selected('scenes:' + REUSE_SCENES[scene]):
            main_art = 'REUSE %s (C3)' % asset_id(art['scenes'][REUSE_SCENES[scene]])
        else:
            main_art = 'GAP'
        speaker = portrait = background = focus = ending = popup = ''
        if n['mode'] == 'dialogue':
            speaker = n['speaker'] + ':' + n['pose']
            prec = art['portraits'].get(speaker) or {}
            if prec.get('format') == 'voice-only':
                portrait, background = 'VOICE-ONLY (C2)', 'none (Narrative B)'
            else:
                portrait = asset_id(prec) if selected('portraits:' + speaker) and not prec.get('notes', '').startswith('ARCHIVED') else 'GAP'
                bkey = cc.background_for(art, scene, speaker, False).split(':', 1)[1]
                if selected('scenes:' + bkey + '#portraitBackground'):
                    background = asset_id(art['scenes'][bkey]['portraitBackground'])
                elif bkey in REUSE_BACKGROUNDS and selected('scenes:' + REUSE_BACKGROUNDS[bkey] + '#portraitBackground'):
                    background = 'REUSE %s (C3)' % asset_id(art['scenes'][REUSE_BACKGROUNDS[bkey]]['portraitBackground'])
                else:
                    background = 'GAP'
        if n['mode'] == 'focus':
            focus = asset_id(art['focus'].get(n['focus'])) if selected('focus:' + n['focus']) else 'GAP'
        if n.get('endingArt'):
            ending = asset_id(art['deathScreens'].get(n['endingArt'])) if selected('deathScreens:' + n['endingArt']) else 'GAP'
            popup = (n.get('deathPopup') or {}).get('id', '') + ('' if (n.get('deathPopup') or {}).get('status') == 'owner-approved' else ' (NOT APPROVED)')
            if 'NOT APPROVED' in popup:
                gaps.append(nid + ': popup')
        row = [nid, n['mode'], scene, main_art, speaker, portrait, background, focus, ending, popup, ', '.join(refs_by_node.get(nid, []))]
        gaps += ['%s: %s' % (nid, c) for c in row if c == 'GAP']
        tsv.append('\t'.join(row))
    check(not gaps, 'All 120 nodes resolve: main scene, portrait + background, Focus A and fatal art each approved, reused (C3) or no-image (C1/C2)', gaps)
    modes = Counter(n['mode'] for n in nodes.values())
    report['nodeMap'] = {'file': NODE_MAP.relative_to(ROOT).as_posix(), 'nodes': len(nodes), 'modes': dict(modes), 'gaps': gaps}

    # 3. Inventory art for every item Chapter 4 references.
    items = json.loads((ROOT / 'story/items.draft.json').read_text())
    referenced = sorted(i for i in strings(nodes, set()) if i in items)
    givers = {}
    manifest = json.loads((ROOT / 'story/storyboard-manifest.json').read_text())
    for c in manifest['chapters']:
        d = json.loads((ROOT / 'story' / c['file']).read_text())
        acc = set()

        def gives(v):
            if isinstance(v, dict):
                g = v.get('give')
                acc.update(g if isinstance(g, list) else [g] if isinstance(g, str) else [])
                [gives(x) for x in v.values()]
            elif isinstance(v, list):
                [gives(x) for x in v]
        gives(d)
        for i in acc:
            givers.setdefault(i, []).append(c['id'])
    item_rows = {}
    for i in referenced:
        rec = art['items'].get(i) or {}
        sides = {}
        for side in ('slot', 'inspect'):
            r = rec.get(side) or {}
            ready = r.get('status') in ('integrated', 'reused') and r.get('assetPath') or (r.get('status') == 'approved' and selected('items:%s#%s' % (i, side)))
            sides[side] = {'status': r.get('status'), 'assetPath': r.get('assetPath'), 'ready': bool(ready)}
        item_rows[i] = {'givenBy': givers.get(i, []), **sides}
        if i == STAFF_PASS:
            continue
        check(sides['slot']['ready'] and sides['inspect']['ready'] and givers.get(i),
              'Item %s: granted by %s; slot and inspect art %s/%s' % (i, givers.get(i), sides['slot']['status'], sides['inspect']['status']))
    sp = item_rows.get(STAFF_PASS, {})
    gated = sorted(n for n, x in nodes.items() for ch in x.get('choices', []) if ch.get('id') in STAFF_PASS_CHOICES)

    def reach(skip):
        seen, stack = {chapter['start']}, [chapter['start']]
        while stack:
            x = stack.pop()
            acc = set()
            for ch in nodes[x].get('choices', []):
                if ch.get('id') not in skip:
                    strings(ch, acc)
            for k in ('use', 'contextAction', 'show', 'scenePickup'):
                strings(nodes[x].get(k), acc)
            for y in acc & set(nodes):
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        return seen
    full = reach(set())
    only_pass = sorted(full - reach(STAFF_PASS_CHOICES))
    check(len(full) == 120, 'All 120 nodes reachable from hotel_entry_dispatch through authored links', 120 - len(full))
    check(sp and not sp['givenBy'] and not sp['slot']['ready'] and len(only_pass) == 5,
          'OPEN DECISION recorded: %s is required by %s but granted by no chapter; its art records are archived pre-reboot prompts; 5 nodes are reachable only with it' % (STAFF_PASS, gated), only_pass)
    report['items'] = item_rows
    report['staffPassDecision'] = {'item': STAFF_PASS, 'gatedChoicesAt': gated, 'nodesOnlyReachableWithIt': only_pass,
                                   'artRecords': {s: (art['items'][STAFF_PASS].get(s) or {}).get('status') for s in ('slot', 'inspect')}}

    # 4. Conditional, inspection, design-master and retired references: exact set, bytes, nodes.
    on_disk = sorted(p.relative_to(ROOT / APPROVED).as_posix() for p in (ROOT / APPROVED).rglob('*') if p.is_file() and 'chapter-04' in p.as_posix())
    check(on_disk == sorted(r[0] for r in REFS), 'Approved Chapter 4 reference tree holds exactly the 33 recorded files', sorted(set(on_disk) ^ {r[0] for r in REFS}))
    for path, digest, doc, ns in REFS:
        p = ROOT / APPROVED / path
        check(p.is_file() and sha(p) == digest and digest in docs_text.get(doc, '') and all(n in nodes for n in ns),
              'Reference %s: SHA-256 %s… matches docs/%s; nodes exist' % (Path(path).name, digest[:12], doc))
    ref_shas = {r[1] for r in REFS}
    ref_keys = [k for k in preview if preview[k]['sha256'] in ref_shas and Path(preview[k]['file']).name != 'bridal_privacy_panel.png']
    # B2-09 wheel-removed intentionally equals the NEW-18 base; no other reference is a selection.
    check(all(preview[k]['sha256'] == 'cc9d19c2413df5b017b72592e3d5c676a84ad0ad91c354093a0a9e0199233e7d' for k in ref_keys),
          'No conditional reference is a canonical selection (only the documented B2-09 wheel-removed = NEW-18 base byte identity)', ref_keys)
    escaped = nodes['hotel_lot61_pod_escaped']
    check(escaped.get('effects', {}).get('set', {}).get('ch4_pod_survived_packing') is True and nodes['fatal_lot61_folded'].get('endingArt') == 'grand_bellevue/folded_for_convenience',
          'B2-19 timing anchors: ch4_pod_survived_packing is set on entry (flag alone must not reveal the case); fatal fold keeps FOLDED FOR CONVENIENCE')
    check(nodes['hotel_stall_porter_protest']['scene'] == 'grand_bellevue/restroom' and selected('scenes:grand_bellevue/restroom#portraitBackground')
          and preview['scenes:grand_bellevue/restroom#portraitBackground']['sha256'] == R1['CH4-B2-03'][1],
          'B2-18 post-lift decision: hotel_stall_porter_protest uses CH4-B2-03 unchanged')

    # 5. Hash integrity: every selection, and no Chapter 4 PNG ever modified in place.
    bad = [k for k, v in preview.items() if not (ROOT / v['file']).is_file() or sha(ROOT / v['file']) != v['sha256']]
    check(len(preview) == 214 and not bad, 'All 214 selected images match their recorded SHA-256', bad)
    ch4_keys = [k for k in preview if 'grand_bellevue' in k or k.startswith('portraits:hotel_') or k.split(':')[1].split('#')[0] in ('lot_53_dispute_ticket', 'wedding_ring_lot31')]
    mism = []
    for k in ch4_keys:
        s = preview[k]['source']
        try:
            blob = git('rev-parse', '%s:%s' % (s['commit'], s['path'])).decode().strip()
        except subprocess.CalledProcessError:
            blob = None
        local = git('hash-object', preview[k]['file']).decode().strip()
        if blob != local:
            mism.append(k)
    check(len(ch4_keys) == 69 and not mism, 'All 69 Chapter 4 selections (63 active + 6 archived portraits) are byte-identical to their immutable review-source blobs', {'count': len(ch4_keys), 'mismatch': mism})
    ch4_paths = [preview[k]['file'] for k in ch4_keys] + [APPROVED + '/' + r[0] for r in REFS]
    modified = git('log', '--diff-filter=M', '--format=%h', BASE, '--', *ch4_paths).decode().split()
    check(not modified, 'No Chapter 4 selected or reference PNG has ever been modified in place on main', modified)
    report['selectionCounts'] = {'all': len(preview), 'chapter4': len(ch4_keys)}

    # 6. R1: six candidates deferred; approved bytes stay selected; failed studies preserved on their branches.
    r1 = {}
    for aid, (pk, want) in R1.items():
        pv = preview.get(pk) or {}
        rec = cc.registry_record(art, {'scenes': 'main_scene', 'portraits': 'portrait'}[pk.split(':')[0]] + ':' + pk.split(':', 1)[1].replace('#portraitBackground', '')) if '#' not in pk else art['scenes'][pk.split(':', 1)[1].split('#')[0]]['portraitBackground']
        ok = selected(pk) and (want is None or pv['sha256'] == want) and asset_id(rec) == aid
        r1[aid] = {'key': pk, 'sha256': pv.get('sha256'), 'status': 'DEFERRED — NOT BLOCKING INTEGRATION; approved original stays selected'}
        check(ok, 'R1 %s stays selected unchanged (%s)' % (aid, pk))
    remote = dict(reversed(l.split('\t')) for l in git('ls-remote', 'origin').decode().splitlines())
    for branch, head_sha, status_path, field, want in R1_STUDIES:
        try:
            st = json.loads(git('show', '%s:%s' % (head_sha, status_path)))
        except subprocess.CalledProcessError:
            st = {}
        check(remote.get('refs/heads/' + branch) == head_sha and st.get(field) == want,
              'Failed R1 study preserved: %s @ %s (%s %s…)' % (branch, head_sha[:7], field, want[:12]))
    report['r1'] = r1

    # 7. Integration blockers still present in canon (not implemented here).
    two_seg = sorted({n['focus'] for n in nodes.values() if n['mode'] == 'focus' and n['focus'].count('/') == 1})
    if_runs = [(nid, i) for nid, n in nodes.items() for i, r in enumerate(n.get('text') if isinstance(n.get('text'), list) else []) if isinstance(r, dict) and 'if' in r]
    fatal = sorted(nid for nid, n in nodes.items() if n.get('deathPopup'))
    no_cards = sorted(nid for nid, n in nodes.items() if not n.get('choices') and not n.get('deathPopup'))
    export = json.loads((ROOT / 'story/death-presentations.export.json').read_text())
    check(len(two_seg) == 3, 'WP-1 still open: 3 two-segment Focus A ids', two_seg)
    check(len(if_runs) == 17, 'WP-2 still open: 17 text runs carry their own `if`', len(if_runs))
    check(len(fatal) == 4 and chapter['development'].get('notForGameplay') is True and not any(e['id'].startswith('chapter-04:') for e in export['entries']),
          'WP-3 still open: 4 fatal popups, all owner-approved with approved art, excluded from the death export while Chapter 4 is notForGameplay', fatal)
    check(len(no_cards) == 3, 'Also open: 3 park-bound endings with no card (Chapter 5 hand-off)', no_cards)
    report['blockersInCanon'] = {'WP-1': two_seg, 'WP-2': ['%s run %d' % x for x in if_runs], 'WP-3': fatal, 'parkExits': no_cards}

    # 8. Draft PR #32 untouched.
    check(remote.get(PR32_REF) == PR32_HEAD, 'Draft PR #32 head unchanged at f320e63', remote.get(PR32_REF))

    # 9. Optional: game main's importer + validator, read-only, on this canon.
    if game:
        report['gameProbe'] = game_probe(Path(game), check)

    NODE_MAP.write_text('\n'.join(tsv) + '\n', encoding='utf-8')
    report['checks'] = check.items
    report['result'] = 'PASS' if not check.failed else 'FAIL'
    REPORT.write_text(json.dumps(report, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    print('%s: %d checks, %d failed' % (report['result'], len(check.items), len(check.failed)))
    return 0 if not check.failed else 1


PROBE = r'''
const fs=require('fs'),path=require('path');const [,,dir,sb,out]=process.argv;
const {convert}=require(path.join(dir,'convert.js'));const Rules=require(path.join(dir,'rules.js'));
const rd=(p)=>JSON.parse(fs.readFileSync(path.join(sb,p),'utf8'));
const manifest=rd('story/storyboard-manifest.json');const chapters={};
manifest.chapters.forEach(c=>{chapters[c.id]=rd(path.join('story',c.file));delete chapters[c.id].development;});
const run=(strip)=>{const ch=JSON.parse(JSON.stringify(chapters));
 if(strip)Object.values(ch).forEach(c=>Object.values(c.nodes).forEach(n=>{delete n.deathPopup;delete n.endingArt;}));
 const settings=JSON.parse(fs.readFileSync(path.join(dir,'runtime-settings.json'),'utf8'));delete settings.pendingArtBindings;
 const missing=new Set();JSON.stringify(ch['chapter-04'],(k,v)=>{if((k==='speaker'||k==='who')&&typeof v==='string'&&v!=='you'&&!settings.cast[v])missing.add(v);return v;});
 if(strip)missing.forEach(id=>{settings.cast[id]={name:id.toUpperCase()};});
 const r=convert({manifest:{chapters:manifest.chapters.map(c=>({id:c.id,title:c.title,file:c.file,status:c.status}))},chapters:ch,items:rd('story/items.draft.json'),artwork:rd('story/artwork.draft.json'),settings,bindings:[]},{mode:'preview'});
 let v=null;if(strip&&r.story)v=Rules.validateStory(r.story,null,{routeMarks:true});
 return {importErrors:r.errors,warnings:r.warnings.filter(w=>/chapter-04|grand_bellevue|hotel_/.test(w)),castMissing:[...missing].sort(),validatorErrors:v?v.errors:null};};
fs.writeFileSync(out,JSON.stringify({raw:run(false),stripped:run(true)}));
'''


def game_probe(g, check):
    gsha = subprocess.check_output(['git', 'rev-parse', 'origin/main'], cwd=g).decode().strip()
    tmp = Path(tempfile.mkdtemp(prefix='ch4-closeout-game-'))
    try:
        for src, dst in (('tools/story-import/convert.js', 'convert.js'), ('game/js/rules.js', 'rules.js'), ('story/runtime-settings.json', 'runtime-settings.json')):
            (tmp / dst).write_bytes(subprocess.check_output(['git', 'show', 'origin/main:' + src], cwd=g))
        (tmp / 'probe.js').write_text(PROBE)
        subprocess.check_call(['node', str(tmp / 'probe.js'), str(tmp), str(ROOT), str(tmp / 'out.json')])
        o = json.loads((tmp / 'out.json').read_text())
    finally:
        shutil.rmtree(tmp)
    raw, st = o['raw'], o['stripped']
    check(gsha == GAME_MAIN, 'Game main unchanged since docs/140 (C1/C2 merged at c7a2d3d)', gsha)
    ch4_fields = sorted(e for e in raw['importErrors'] if 'chapter-04:' in e and 'unsupported field' in e)
    check(len(ch4_fields) == 8 and all('deathPopup' in e or 'endingArt' in e for e in ch4_fields),
          'Game importer: only the 4 fatal nodes are rejected for Chapter 4 node fields (deathPopup/endingArt, WP-3)', ch4_fields)
    check(not st['importErrors'], 'Game importer: with WP-3 fields routed aside and cast names supplied, Chapter 4 imports with no error', st['importErrors'])
    v = st['validatorErrors'] or []
    focus = [e for e in v if 'location/scene/target' in e]
    runs = [e for e in v if 'unknown run key if' in e]
    cards = [e for e in v if 'has no choices' in e]
    echo = [e for e in v if 'say is only echoed in dialogue nodes' in e]
    certain = [e for e in v if 'can make it certain' in e]
    check(len(focus) == 3 and len(runs) == 17 and len(cards) == 3 and len(echo) == 1 and len(certain) == 1 and len(v) == 25,
          'Game validator: exactly the docs/140 set — WP-1 x3, WP-2 x17, park exits x3, Focus echo x1, unmarked certain check x1', v)
    no_record = sorted(re.findall(r'no scene artwork record for (\S+)', ' '.join(raw['warnings'])))
    check(sorted(set(no_record)) == sorted(REUSE_SCENES), 'Game importer: the only scene keys without a record are the 4 C3 reuse keys', no_record)
    check(len(raw['castMissing']) == 21, 'Game runtime settings lack display names for 21 Chapter 4 speakers/voices (routine integration)', raw['castMissing'])
    return {'gameMain': gsha, 'validatorErrors': v, 'castMissing': raw['castMissing'], 'reuseSceneKeys': sorted(set(no_record)),
            'placeholderWarnings': len(raw['warnings'])}


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
