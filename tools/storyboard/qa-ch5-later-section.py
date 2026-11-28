#!/usr/bin/env python3
"""State and route audit for the isolated Chapter 5 later-park authoring section.

This audits the authored JSON, not the private game runtime. Run from any cwd.
"""
import itertools
import json
import subprocess
from collections import Counter
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'story/review/chapter-05-later-park'
chapter = json.loads((BASE / 'later-park.section.json').read_text())
items = json.loads((ROOT / 'story/items.draft.json').read_text())
items.update(json.loads((BASE / 'items.additions.json').read_text()))
art = json.loads((BASE / 'artwork.additions.json').read_text())
contract = json.loads((ROOT / 'story/sync-contract.json').read_text())
nodes = chapter['nodes']
checks = 0

def require(condition, message):
    global checks
    checks += 1
    if not condition: raise AssertionError(message)

def allowed(level):
    return set(contract['runtimeFields'].get(level, [])) | set(contract['storyboardOnlyFields'].get(level, []))

def permitted(condition, flags, held, marks):
    if not condition: return True
    require(len(condition) == 1, 'one understood condition operator')
    op, value = next(iter(condition.items()))
    if op == 'flagIs': return flags.get(value[0]) == value[1]
    if op in ('item', 'itemNot'):
        result = value[0] in held and (len(value) == 1 or (value[0], value[1]) in marks)
        return not result if op == 'itemNot' else result
    raise AssertionError('unsupported condition ' + op)

def apply(effects, flags, held):
    flags, held = dict(flags), set(held)
    require(set(effects or {}) <= {'set', 'give'}, 'section uses only scoped flag updates and the single pickup')
    for key, value in (effects or {}).get('set', {}).items():
        require(key.startswith('ch5_later_') or key == 'ch5_exit_route', 'no earlier state overwritten: ' + key)
        flags[key] = value
    for item_id in (effects or {}).get('give', []):
        require(item_id == 'ch5_foam_release_cartridge', 'only approved cartridge granted')
        require(item_id not in held, 'no duplicate pickup')
        held.add(item_id)
    return flags, held

def render_text(text, flags, held, marks):
    output = []
    for block in text if isinstance(text, list) else [text]:
        if isinstance(block, str): output.append(block)
        elif permitted(block.get('if'), flags, held, marks):
            output.append(block.get('text') or block.get('say') or block.get('desc') or '')
    return '\n'.join(output)

require(chapter['development']['notForGameplay'] is True, 'not eligible for gameplay import')
require('Preserve earlier material' in chapter['development']['ownerPlacementDecision'], 'explicit preservation decision recorded')
require(set(chapter) <= allowed('chapter'), 'chapter field contract')
require(chapter['start'] == 'later_park_arrival', 'section starts after earlier property-return area')
require(not {'park_edge', 'shrub_discovery', 'wire_follow', 'squirrel_inspection'} & set(nodes), 'older opening not replaced')

rolls = []
for nid, n in nodes.items():
    require(set(n) <= allowed('node'), nid + ': node field contract')
    require(n['scene'] in art['scenes'], nid + ': scene brief exists')
    require(len({c['id'] for c in n.get('choices', [])}) == len(n.get('choices', [])), nid + ': unique local choice IDs')
    require(bool(n.get('end')) != bool(n.get('choices')), nid + ': terminal or has onward choices')
    for c in n.get('choices', []):
        require(set(c) <= allowed('choice'), nid + ': choice field contract')
        for key in ['to', 'pass', 'fail']:
            target = c.get(key)
            if isinstance(target, dict): target = target.get('to')
            if target: require(target in nodes, nid + ': target ' + target)
        if c.get('check'):
            rolls.append(c['check']['id'])
            require(c['check']['sides'] == 6 and c['check']['need'] == 3, nid + ': approved d6 threshold')
    if n.get('deathPopup'):
        p = n['deathPopup']
        require(n.get('end') is True, nid + ': fatal is terminal')
        require(p['artRef'] == n['endingArt'], nid + ': shared fatal-art reference')
        require(art['deathScreens'][p['artRef']]['dimensions'] == '314x206', nid + ': native death dimensions')
        require(bool(p['title']) and bool(p['description']), nid + ': popup copy present')
require(len(rolls) == len(set(rolls)) == 3, 'three independent authored hidden checks')
require(len([n for n in nodes.values() if n.get('deathPopup')]) == 2, 'two later-section fatal presentations')
require(len([n for n in nodes.values() if n.get('end') and not n.get('deathPopup')]) == 2, 'two later-section nonfatal exits')
require('security_park/dont_whiz' in art['deathScreens'], 'earlier electric-shrub art direction carried in sidecar')
require(all(r['status'] == 'not-started' and r.get('assetPath') is None for group in art.values() for r in group.values() if 'status' in r), 'no production artwork selected or integrated')

base_items = set(json.loads((ROOT / 'story/items.draft.json').read_text()))
optional = ['rubber_band_ball', 'pavilion_temporary_staff_pass', 'acting_director_badge', 'expo_examiner_badge']
sentinels = {'ch4_bridal_registration_fee_pending': True, 'spore_infected': True, 'thorn_infected': True, 'ch4_exit_route': 'bridal_lavatory_departure', 'ch5_property_claim_resolved': True, 'ch5_property_return_result': 'damaged', 'ch5_gate_passed': True}
overall_reached = set()
overall_ends = Counter()
contexts = 0
state_visits = 0

for presence in itertools.product([False, True], repeat=len(optional)):
    for badge_read in [False, True]:
        contexts += 1
        # Include many surviving original items to prove no six-item capacity clamp or unrelated loss.
        original = (base_items - set(optional)) | {item for item, present in zip(optional, presence) if present}
        marks = frozenset({('expo_examiner_badge', 'read')} if badge_read and 'expo_examiner_badge' in original else set())
        visiting = set()
        @lru_cache(None)
        def visit(nid, flag_json, item_tuple):
            global state_visits
            state_visits += 1
            require((nid, flag_json, item_tuple) not in visiting, 'no narrative loop')
            visiting.add((nid, flag_json, item_tuple))
            overall_reached.add(nid)
            n = nodes[nid]
            flags, held = apply(n.get('effects'), json.loads(flag_json), set(item_tuple))
            require(all(flags.get(k) == v for k, v in sentinels.items()), nid + ': prior state preserved')
            require(original <= held, nid + ': original inventory retained')
            if nid == 'rear_restroom':
                require(flags.get('ch5_later_foam_triggered') is True, 'no foam in unvisited restroom')
                require(flags.get('ch5_later_foam_discharge') == 'stopped', 'nozzle stopped before rear restroom')
                require(flags.get('ch5_later_local_shutdown') is True, 'local shutdown completed')
                require(flags.get('ch5_later_foam_expanding') is True, 'stopped discharge does not remove existing foam')
            if nid == 'depot_early':
                require(flags.get('ch5_later_foam_triggered') is False, 'early depot has no fabricated foam event')
                require(flags.get('ch5_later_local_shutdown') is False, 'early depot does not receive unvisited shutdown')
                require('demonstrator' not in render_text(n['text'], flags, held, marks).lower(), 'early depot prose has no demonstrator')
            if nid == 'depot_late':
                require(flags.get('ch5_later_foam_triggered') is True, 'late depot follows actual foam event')
            if nid == 'shutdown_help':
                rendered = render_text(n['text'], flags, held, marks)
                if flags.get('ch5_later_foam_discharge') == 'stopped': require('releases one final white lump' not in rendered, 'stopped nozzle does not spray again')
            if n.get('end'):
                if nid == 'dispatch_gate_exit': require(flags.get('ch5_later_dispatch_connection_observed') is True, 'dispatch clue is earned')
                if nid == 'service_gate_exit': require(not flags.get('ch5_later_dispatch_connection_observed'), 'service exit has no unvisited dispatch clue')
                require(held - original <= {'ch5_foam_release_cartridge'}, 'no incidental prop grants')
                result = Counter({nid: 1})
            else:
                choices = [c for c in n['choices'] if permitted(c.get('if'), flags, held, marks)]
                require(bool(choices), nid + ': at least one available choice')
                result = Counter()
                for c in choices:
                    cf, ci = apply(c.get('effects'), flags, held)
                    if c.get('check'):
                        for raw in range(1, 7):
                            branch = c['pass'] if raw >= c['check']['need'] else c['fail']
                            bf, bi = apply(branch.get('effects'), cf, ci)
                            result.update(visit(branch['to'], json.dumps(bf, sort_keys=True), tuple(sorted(bi))))
                    else:
                        result.update(visit(c['to'], json.dumps(cf, sort_keys=True), tuple(sorted(ci))))
            visiting.remove((nid, flag_json, item_tuple))
            return result
        terminals = visit(chapter['start'], json.dumps(sentinels, sort_keys=True), tuple(sorted(original)))
        require(terminals['service_gate_exit'] > 0 and terminals['dispatch_gate_exit'] > 0, 'both exits reachable for each optional-item configuration')
        overall_ends.update(terminals)

require(overall_reached == set(nodes), 'every later-section node is state-reachable')
require(set(overall_ends) == {'service_gate_exit', 'dispatch_gate_exit', 'fatal_fence', 'fatal_foam'}, 'only approved later-section endings')

legacy_source = '2f0f3e124ce7054ab8ce6720848043109f67605e'
legacy_manifest = json.loads((BASE / 'preserved-records.json').read_text())
require(legacy_manifest['sourceCommit'] == legacy_source, 'immutable earlier source recorded')
require(len(legacy_manifest['files']) == 51, 'all 51 earlier source records listed')
preserved = 0
for entry in legacy_manifest['files']:
    name, expected = entry['path'], entry['gitBlob']
    require((ROOT / name).is_file(), 'preserved earlier record exists: ' + name)
    actual = subprocess.check_output(['git', 'hash-object', '--', name], cwd=ROOT, text=True).strip()
    require(actual == expected, 'earlier record is byte-identical: ' + name)
    preserved += 1

result = {'ok': True, 'scope': 'authored later-park section, not game runtime or whole Chapter 5', 'nodes': len(nodes), 'choices': sum(len(n.get('choices', [])) for n in nodes.values()), 'hidden_checks': len(rolls), 'fatal_presentations': 2, 'nonfatal_exits': 2, 'inventory_mark_contexts': contexts, 'distinct_context_state_visits': state_visits, 'assertions': checks, 'preserved_earlier_records': preserved, 'preserved_source_commit': legacy_source, 'terminal_paths_with_raw_dice_multiplicity': dict(sorted(overall_ends.items())), 'note': 'Path counts are enumeration counts, not player probabilities or scenario samples.'}
print(json.dumps(result, indent=2))
if '--write' in __import__('sys').argv:
    (BASE / 'audit-results.json').write_text(json.dumps(result, indent=2) + '\n')
