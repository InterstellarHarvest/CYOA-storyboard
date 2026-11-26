#!/usr/bin/env python3
"""Verifier for the owner-approved Temporary Staff Pass grant in the Chapter 3 reboot (docs/153). Read-only.

  python3 tools/sync/verify-ch3-staff-pass-grant.py

Checks, against canonical base 89cf0ad (docs/152 merged):
  - scope: only the approved story edit, the two locked QA pins, the item text, the two restored
    art briefs, docs/153 and the dated docs/152 addendum differ;
  - unauthorized_presenter: every earlier word, run order, choice and target preserved; the only new
    content is one printer run and an arrival `give` of the existing item;
  - every other Chapter 3 node, Chapter 4, the obsolete pre-reboot Chapter 3 and its archive are unchanged;
  - grant scope: the item is given only there and taken nowhere;
  - routes: a state-tracking search (flags, items, both outcomes of every check) from every Chapter 2
    hand-off through Chapter 3 shows which endings hold the pass, then from every Chapter 3 ending into
    Chapter 4 (with ch3_exit_route, the pending docs/126 hand-off) shows the five pass-gated nodes become
    reachable exactly on the two endings after the appointment.
"""
import json
import subprocess
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = '89cf0adf09dfadba27bb82f87201160f68818b46'
ITEM = 'pavilion_temporary_staff_pass'
NODE = 'unauthorized_presenter'
CH3 = 'story/chapters/chapter-03.reboot-candidate.json'
CH4 = 'story/chapters/chapter-04.wip.json'
CH2 = 'story/chapters/chapter-02.draft.json'
PRINTER_RUN = {'desc': "An administrative printer rattles and ejects a card: TEMPORARY STAFF. PEOPLE'S PAVILION. "
                       "DEPARTMENT: HUMAN PRESENTATION. VALID UNTIL CORRECTED. You pocket it. Apparently, you have been hired again."}
PASS_ONLY = ['hotel_boiler_staff_access', 'hotel_collection_staff_pass', 'hotel_collection_staff_pass_authorized',
             'hotel_collection_staff_pass_first', 'hotel_collection_staff_pass_recognized']
EXPECTED_FILES = {CH3, 'story/items.draft.json', 'story/artwork.draft.json', 'tools/storyboard/qa-smoke.mjs',
                  'tools/storyboard/qa-ch3-reboot-candidate.mjs', 'tools/sync/verify-ch3-staff-pass-grant.py',
                  'docs/152_CH4_ARTWORK_CLOSEOUT_AND_GAMEPLAY_HANDOFF_20261126.md',
                  'docs/153_CH3_TEMPORARY_STAFF_PASS_GRANT_20261126.md', 'docs/153_CH3_TEMPORARY_STAFF_PASS_GRANT_VERIFICATION_20261126.json'}
REPORT = ROOT / 'docs/153_CH3_TEMPORARY_STAFF_PASS_GRANT_VERIFICATION_20261126.json'
STATE_CAP = 400000


class Checks:
    def __init__(self):
        self.items, self.failed = [], []

    def __call__(self, ok, msg, detail=None):
        self.items.append({'ok': bool(ok), 'check': msg, **({'detail': detail} if detail is not None else {})})
        if not ok:
            self.failed.append(msg)
            print('FAIL', msg, '' if detail is None else json.dumps(detail)[:500])


def git(*a):
    return subprocess.check_output(['git', *a], cwd=ROOT)


def now(p):
    return json.loads((ROOT / p).read_text(encoding='utf-8'))


def base(p):
    return json.loads(git('show', BASE + ':' + p))


# --- A small interpreter of the storyboard's own route semantics -------------------------------------
def holds(cond, flags, inv):
    if cond is None:
        return True
    if not isinstance(cond, dict):
        raise ValueError('unsupported condition %r' % (cond,))
    for k, v in cond.items():
        vs = v if isinstance(v, list) and k != 'flagIs' else [v]
        if k == 'flag':
            ok = all(flags.get(x) not in (None, False) for x in vs)
        elif k == 'notFlag':
            ok = all(flags.get(x) in (None, False) for x in vs)
        elif k == 'flagIs':
            ok = flags.get(v[0]) == v[1]
        elif k == 'has':
            ok = all(x in inv for x in vs)
        else:
            raise ValueError('unsupported condition operator ' + k)
        if not ok:
            return False
    return True


def apply(fx, flags, inv):
    flags, inv = dict(flags), set(inv)
    for k, v in (fx or {}).items():
        if k == 'set':
            flags.update(v)
        elif k == 'give':
            inv.update(v)
        elif k == 'take':
            inv.difference_update(v)
        elif k == 'mark':
            pass
        else:
            raise ValueError('unsupported effect ' + k)
    return flags, inv


def tested(chapter):
    """The flags and items any condition or item action of this chapter can test."""
    flags, items = {'__via_appointment'}, {ITEM}

    def walk(v, in_if=False):
        if isinstance(v, dict):
            for k, x in v.items():
                if in_if and k in ('flag', 'notFlag'):
                    flags.update(x if isinstance(x, list) else [x])
                elif in_if and k == 'flagIs':
                    flags.add(x[0])
                elif in_if and k == 'has':
                    items.update(x if isinstance(x, list) else [x])
                walk(x, in_if or k == 'if')
        elif isinstance(v, list):
            for x in v:
                walk(x, in_if)
    for n in chapter['nodes'].values():
        walk(n)
        for verb in ('show', 'use'):
            items.update((n.get(verb) or {}).keys())
    return flags, items


def explore(chapter, flags0, inv0, start=None):
    """Every reachable (node, flags, items) state. Returns visited states and terminal states.
    State is projected onto the flags and items some condition tests, which is exact for reachability."""
    nodes = chapter['nodes']
    tf, ti = tested(chapter)
    key = lambda n, f, i: (n, frozenset((k, v) for k, v in f.items() if k in tf), frozenset(x for x in i if x in ti))
    seen, terminals = set(), []
    q = deque()

    def arrive(nid, f, i, via):
        f, i = apply(nodes[nid].get('effects'), f, i)
        if nid == NODE:
            f['__via_appointment'] = True
        k = key(nid, f, i)
        if k not in seen:
            seen.add(k)
            q.append((nid, f, i))
    arrive(start or chapter['start'], dict(flags0), set(inv0), None)
    while q:
        if len(seen) > STATE_CAP:
            raise RuntimeError('state cap exceeded')
        nid, f, i = q.popleft()
        n = nodes[nid]
        outs = []
        for ch in n.get('choices', []):
            if not holds(ch.get('if'), f, i):
                continue
            outs.append(ch)
        for verb in ('show', 'use'):
            for item, act in (n.get(verb) or {}).items():
                if item in i and holds(act.get('if'), f, i):
                    outs.append(act)
        if not outs:
            terminals.append((nid, f, i))
        for o in outs:
            f1, i1 = apply(o.get('effects'), f, i)
            if o.get('restart') or o.get('chapter'):
                terminals.append((nid, f1, i1))
                continue
            branches = [o] if 'check' not in o else [o.get('pass') or {}, o.get('fail') or {}]
            for b in branches:
                f2, i2 = apply(b.get('effects') if b is not o else None, f1, i1)
                if b.get('to'):
                    arrive(b['to'], f2, i2, nid)
    return seen, terminals


def main():
    check = Checks()
    report = {'schema': 'out-of-order-ch3-staff-pass-grant-v1', 'base': BASE, 'item': ITEM, 'node': NODE}

    # 1. Scope.
    changed = set(git('diff', '--name-only', BASE).decode().split()) | set(git('ls-files', '--others', '--exclude-standard').decode().split())
    check(changed <= EXPECTED_FILES, 'Only the approved files differ from base 89cf0ad', sorted(changed - EXPECTED_FILES))
    for p in ('story/chapters/chapter-03.draft.json', 'story/archives/chapter-03-pre-reboot-20261118.json', CH4, CH2,
              'story/storyboard-manifest.json', 'story/artwork-preview.json', 'story/death-presentations.export.json',
              'story/sync-contract.json', 'story/storyboard-layout.json'):
        check(git('rev-parse', BASE + ':' + p) == git('hash-object', p), 'Unchanged: ' + p)
    sel = git('diff', '--name-only', BASE, '--', 'assets', 'tools/prologue-art-lab/assets').decode().split()
    check(not sel, 'No image, selection or reference changed', sel)

    # 2. The node edit.
    b3, n3 = base(CH3), now(CH3)
    bn, nn = b3['nodes'][NODE], n3['nodes'][NODE]
    others = [k for k in set(b3['nodes']) | set(n3['nodes']) if k != NODE and b3['nodes'].get(k) != n3['nodes'].get(k)]
    check(not others and {k: v for k, v in b3.items() if k != 'nodes'} == {k: v for k, v in n3.items() if k != 'nodes'},
          'Every other Chapter 3 node and the chapter header are unchanged', others)
    check(nn.get('effects') == {'give': [ITEM]} and 'effects' not in bn, 'The appointment gives exactly the existing item on arrival')
    check({k: v for k, v in nn.items() if k not in ('effects', 'text')} == {k: v for k, v in bn.items() if k != 'text'},
          'Mode, scene, speaker, pose and both choices (ids, text, targets) unchanged')
    bt, nt = bn['text'], nn['text']
    split_ok = (len(nt) == len(bt) + 2 and nt[:4] == bt[:4] and nt[5] == PRINTER_RUN
                and nt[4]['desc'] + ' ' + nt[6]['desc'] == bt[4]['desc'] and nt[4]['desc'].endswith('TEMPORARY PRESENTER APPOINTED.'))
    check(split_ok, 'Text: earlier runs identical; the last run is split exactly after TEMPORARY PRESENTER APPOINTED. and rejoins to the original; one printer run inserted there')
    for line in ('TEMPORARY STAFF', "PEOPLE'S PAVILION", 'DEPARTMENT: HUMAN PRESENTATION', 'VALID UNTIL CORRECTED'):
        check(line in PRINTER_RUN['desc'], 'Printed credential line present: ' + line)
    choices = [c['id'] for c in nn['choices']]
    check(choices == ['start_presenter_demonstration', 'free_real_presenter'], 'Grant precedes both appointment choices', choices)

    # 3. Item record and art briefs.
    bi, ni = base('story/items.draft.json'), now('story/items.draft.json')
    check({k: v for k, v in bi.items() if k != ITEM} == {k: v for k, v in ni.items() if k != ITEM}, 'Every other item record unchanged')
    check({k: v for k, v in bi[ITEM].items() if k != 'description'} == {k: v for k, v in ni[ITEM].items() if k != 'description'},
          'Item keeps its id, name, null art fields and READ mark; only the description changes', ni[ITEM]['description'])
    ba, na = base('story/artwork.draft.json'), now('story/artwork.draft.json')
    na_items = {k: v for k, v in na['items'].items() if k != ITEM}
    check({k: v for k, v in ba.items() if k != 'items'} == {k: v for k, v in na.items() if k != 'items'} and na_items == {k: v for k, v in ba['items'].items() if k != ITEM},
          'Every other artwork record unchanged')
    for side, dim in (('slot', '96x96'), ('inspect', '565x451')):
        o, r = ba['items'][ITEM][side], na['items'][ITEM][side]
        check(r['status'] == 'not-started' and r['assetPath'] is None and r['dimensions'] == dim and r['suggestedFilename'] == o['suggestedFilename']
              and r['notes'].startswith('ACTIVE ITEM BRIEF') and r['notes'].endswith(o['notes']) and 'ARCHIVED' not in r['notes'].split(o['notes'])[0],
              'Art brief %s restored: active, not-started, no image, same contract and path; archived note kept verbatim as history' % side)

    # 4. Grant scope across the canon.
    m = now('story/storyboard-manifest.json')
    givers, takers = [], []

    def scan(cid, v, nid=None):
        if isinstance(v, dict):
            if ITEM in (v.get('give') or []):
                givers.append(cid + ':' + str(nid))
            if ITEM in (v.get('take') or []):
                takers.append(cid + ':' + str(nid))
            for k, x in v.items():
                scan(cid, x, nid)
        elif isinstance(v, list):
            for x in v:
                scan(cid, x, nid)
    for c in m['chapters']:
        for nid, n in now('story/' + c['file'])['nodes'].items():
            scan(c['id'], n, nid)
    check(givers == ['chapter-03:' + NODE] and not takers, 'Granted only at chapter-03:unauthorized_presenter; no authored rule takes it', {'give': givers, 'take': takers})

    # 5. Routes: Chapter 2 hand-offs -> Chapter 3 -> Chapter 4.
    c2, c4 = now(CH2), now(CH4)
    handoffs = {nid: n['effects']['set'] for nid, n in c2['nodes'].items() if 'chapter3_entry_group' in json.dumps(n.get('effects'))}
    prior = set()
    for c in m['chapters'][:3]:
        scan_give = []

        def g(v):
            if isinstance(v, dict):
                prior.update(v.get('give') or [])
                [g(x) for x in v.values()]
            elif isinstance(v, list):
                [g(x) for x in v]
        g(now('story/' + c['file']))
    prior.discard(ITEM)
    ch3_ends = {}
    for h, fl in sorted(handoffs.items()):
        for inv0 in (set(), prior):
            _, terms = explore(n3, fl, inv0)
            for nid, f, i in terms:
                e = ch3_ends.setdefault(nid, {'withPass': 0, 'withoutPass': 0, 'viaAppointment': 0, 'violations': 0})
                has = ITEM in i
                e['withPass' if has else 'withoutPass'] += 1
                e['viaAppointment'] += bool(f.get('__via_appointment'))
                e['violations'] += has != bool(f.get('__via_appointment'))
    report['chapter3Endings'] = ch3_ends
    check(len(handoffs) == 5 and len(ch3_ends) == 7, 'Explored all 7 Chapter 3 endings from all 5 Chapter 2 hand-offs', sorted(ch3_ends))
    check(all(e['violations'] == 0 for e in ch3_ends.values()), 'At every Chapter 3 ending: the pass is held if and only if the route went through the appointment')
    with_pass = sorted(k for k, e in ch3_ends.items() if e['withPass'])
    check(with_pass == ['backstage_exit', 'presenter_help_end'] and ch3_ends['presenter_help_end']['withoutPass'] == 0,
          'Pass reaches exactly the two endings after the appointment (presenter_help_end always; backstage_exit only via the demonstration)', with_pass)
    ch4 = {}
    for end in sorted(ch3_ends):
        for label, inv0 in (('pass only', {ITEM}), ('everything else, no pass', prior)):
            seen, _ = explore(c4, {'ch3_exit_route': end}, inv0)
            reached = {s[0] for s in seen}
            ch4['%s | %s' % (end, label)] = {'nodes': len(reached), 'passOnlyNodesReached': sorted(set(PASS_ONLY) & reached)}
    report['chapter4Reachability'] = ch4
    for end in ('presenter_help_end', 'backstage_exit'):
        r = ch4[end + ' | pass only']['passOnlyNodesReached']
        check(r == sorted(PASS_ONLY), 'Ch3 %s -> Ch4 holding the pass: all 5 pass-gated nodes reachable' % end, r)
    for k, v in ch4.items():
        if k.endswith('no pass'):
            check(not v['passOnlyNodesReached'], 'Without the pass (%s): the 5 nodes stay unreachable' % k.split(' |')[0], v['passOnlyNodesReached'])

    report['checks'] = check.items
    report['result'] = 'PASS' if not check.failed else 'FAIL'
    REPORT.write_text(json.dumps(report, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    print('%s: %d checks, %d failed' % (report['result'], len(check.items), len(check.failed)))
    return 0 if not check.failed else 1


if __name__ == '__main__':
    sys.exit(main())
