#!/usr/bin/env python3
"""Chapter 4 artwork consolidation (docs/137): derive, plan, apply, verify.

The plan is always derived from the PRE-consolidation canon (CANON_BASE), so the 90 logical
requirements and every mapping stay reproducible after the approved edits are applied.

    python3 tools/sync/ch4-consolidation.py build
        Derive the 90 requirements from CANON_BASE and apply the DECISIONS below. Writes the docs/137
        plan JSON and the 120-node coverage TSV.
    python3 tools/sync/ch4-consolidation.py apply
        Nate-approved edit set (2026-11-24, docs/137 section 14) applied to this tree, once:
        retirement/reuse pose remaps, registry notes, the CH4-B2-16 background moved to the retired
        archive, no-image presentation records (C1 text-led, C2 voice-only), the corrected ring
        brief, the qa-smoke count and the retirement ledger. Refuses to run twice.
    python3 tools/sync/ch4-consolidation.py verify
        Independent checks: canon structure, approved bytes/provenance/4x, and that this tree is
        exactly CANON_BASE plus the approved edit set. Writes the verification JSON. Exit 1 on failure.
    python3 tools/sync/ch4-consolidation.py game-check --game <out-of-order checkout>
        check-canon / qa-smoke on CANON_BASE and on this tree, check-canon mutation guards for the
        no-image formats, and the private game's own pure importer (convert.js at that checkout's
        origin/main) resolving every node before and after. Merged into the verification JSON.
    python3 tools/sync/ch4-consolidation.py evidence
        Review sheets in docs/137_evidence/ from the approved bytes.

Python 3.9+, Pillow. Original artwork, approvals, sources and hashes are never altered or deleted.
"""
import copy, hashlib, json, os, re, shutil, subprocess, sys, tempfile
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / 'docs'
PLAN = DOCS / '137_CH4_ARTWORK_CONSOLIDATION_PLAN_20261124.json'
TSV = DOCS / '137_CH4_NODE_ART_COVERAGE_20261124.tsv'
VERIFY = DOCS / '137_CH4_ARTWORK_CONSOLIDATION_VERIFICATION_20261124.json'
CHAPTER = 'story/chapters/chapter-04.wip.json'
ARTWORK = 'story/artwork.draft.json'
PREVIEW = 'story/artwork-preview.json'
SELECTED = ('approved', 'integrated', 'reused')
NOART = {'C1': 'TEXT-LED (C1)', 'C2': 'NO PORTRAIT (C2)'}
APPROVAL_DOCS = sorted(DOCS.glob('1[23][0-9]_CH4_*APPROVAL_COMPLETION_*.json'))
AUDIT = {'main': 'b56f91e19e890c340d92c72d6d2c4822f0f178d9', 'review': '6ddaf567bcc2369c2122256a6ec0daa93f5f886e'}
CANON_BASE = '96e3c2a68e3f31afec2aed6cfd8b7634b774980f'  # main after PR #30, before consolidation
LEDGER = DOCS / '137_CH4_RETIRED_ARTWORK_LEDGER_20261124.json'
RETIRED_DIR = 'tools/prologue-art-lab/assets/approved/retired-selections/chapter-04'
DECISION = 'Nate approved all four docs/137 decisions on 2026-11-24 (PR #31).'
# Reuse remap approved with the revised B2-09 (no separate commanding expression).
REUSE_POSES = [['hotel_bixby_emergency', 'hotel_commodore_bixby', 'commanding', 'delighted']]
BASELINE = {'main_scene': 23, 'portrait': 36, 'portrait_background': 15, 'focus_a': 8,
            'inventory_slot': 2, 'inventory_inspect': 2, 'fatal_aftermath': 4}

# ----------------------------------------------------------------------------------------------
# Decisions. Every logical requirement that is not an approved selection must be named here, and
# every approved selection is RETAIN unless it is in RETIRE. `verify` enforces both.
# ----------------------------------------------------------------------------------------------
RETIRE = {
    'portrait:hotel_porter:curious': {
        'id': 'CH4-B2-33', 'title': 'Porter - curious', 'replacement': 'portrait:hotel_porter:uncertain', 'replacementId': 'CH4-B2-21',
        'poseChanges': [['hotel_collection_staff_pass', 'curious', 'uncertain']],
        'continuity': 'The porter examines the pass, looks at Lot 31 and consults his clipboard. B2-21 (hand to chin, clipboard) shows exactly that, on the same service-passage background. The next node already uses B2-21.'},
    'portrait:hotel_porter:relieved': {
        'id': 'CH4-B2-34', 'title': 'Porter - relieved', 'replacement': 'portrait:hotel_porter:practical', 'replacementId': 'CH4-B2-22',
        'poseChanges': [['hotel_collection_staff_pass_recognized', 'relieved', 'practical']],
        'continuity': '"Oh! Our visiting inspector. Back again?" B2-22 has the same smile and an open welcoming arm, holds the same clipboard and stands on the same background. The next node (authorized) already uses B2-22.'},
    'portrait:hotel_bride:hopeful': {
        'id': 'CH4-B2-28', 'title': 'Bride - hopeful', 'replacement': 'portrait:hotel_bride:determined', 'replacementId': 'CH4-B2-26',
        'poseChanges': [['hotel_ring_show_bride', 'hopeful', 'determined']],
        'continuity': 'You SHOW the ring; it is still yours. B2-26 has empty hands (open palm). The ring-holding grateful pose (B2-29) stays only on hotel_bride_ring_handover, after the ring is placed in her hand.'},
    'portrait:hotel_auctioneer:bureaucratic': {
        'id': 'CH4-B2-36', 'title': 'Auctioneer - bureaucratic', 'replacement': 'portrait:hotel_auctioneer:showman', 'replacementId': 'CH4-03',
        'poseChanges': [['hotel_auctioneer_lot14_recall', 'bureaucratic', 'showman']],
        'continuity': 'Same lobby podium background and the same gavel. The RECALL AUTHORIZED stamp is narrated, not held. The preceding dispute node already uses CH4-03.'},
    'portrait:hotel_wedding_assistant:sympathetic': {
        'id': 'CH4-B2-39', 'title': 'Wedding assistant - sympathetic', 'replacement': 'portrait:hotel_wedding_assistant:apologetic', 'replacementId': 'CH4-B2-40',
        'poseChanges': [['hotel_staff_lavatory_move_boxes', 'sympathetic', 'apologetic']],
        'continuity': 'Neither pose holds a prop, so box, ribbon and clipboard continuity lives in the background states (CH4-B2-41-cleared / -permit). Most of the node is embarrassment and apology ("Oh, dear", "I\'m terribly sorry"). Soft note: the node opens "The assistant looks sympathetic"; B2-40\'s gentle clasped-hands smile still reads that way.'},
    'portrait:hotel_boiler_engineer:practical': {
        'id': 'CH4-B2-46', 'title': 'Boiler engineer - practical', 'replacement': 'portrait:hotel_boiler_engineer:careful', 'replacementId': 'CH4-B2-43',
        'poseChanges': [['hotel_boiler_staff_access', 'practical', 'careful'], ['hotel_water_outage_confirmation', 'practical', 'careful']],
        'continuity': 'Same identity and coverall; neither pose holds the gauge or the gate key. Staff access: he opens the maintenance gate (the narrated action; B2-43 points toward it). Water outage: over the service-passage background, unchanged. Registered by PR #30 (merged 2026-11-24) before this review, so retirement is a pose remap rather than an omission.'},
    'portrait_background:grand_bellevue/boiler_access': {
        'id': 'CH4-B2-16', 'title': 'Boiler-access portrait background', 'replacement': 'portrait_background:grand_bellevue/service_passage', 'replacementId': 'CH4-B2-23',
        'poseChanges': [],
        'continuity': 'hotel_collection_slip_spotted: the player is still OUTSIDE the boiler door beside Lot 31 until the porter "opens the boiler-room door and ushers you through". B2-23 shows that exact spot (Lot 31, BOILER ACCESS door, collection stairs), so it is more truthful than B2-16, which looks out from inside the boiler access. The boiler-access MAIN scene (CH4-B2-13) is kept.',
        'mechanism': 'Importer rule (game convert.js bgFor): a scene\'s own portraitBackground always wins and node backdrop is not an authorable field. Retirement therefore (1) moves the boiler_access#portraitBackground record and its public preview copy out of the active registry (record text, SHA-256 and pinned source preserved verbatim in docs/137 section 5 and git history; bytes stay at source commit 24c79bf) and (2) sets portraits[hotel_porter:alarmed].portraitBackgroundScene grand_bellevue/lobby -> grand_bellevue/service_passage. The lobby node hotel_chair_stapler_caught keeps the lobby background because the lobby scene has its own.'},
}

NEW = {
    'main_scene:grand_bellevue/bridal_dressing_room': {'id': 'CH4-NEW-01', 'title': 'Bridal dressing room', 'note': 'Hosts the bridal-privacy indicator and AutoFit gown states as localized changes.'},
    'main_scene:grand_bellevue/bridal_lavatory': {'id': 'CH4-NEW-02', 'title': 'Bridal lavatory (three seashells, no toilet)', 'note': 'Counter with three shells and no other fixture (docs/125).'},
    'main_scene:grand_bellevue/upper_salvage': {'id': 'CH4-NEW-03', 'title': 'Upper salvage mezzanine', 'note': 'Must also show the freight-lift doors and the W.C. button panel as a localized detail, because freight_lift reuses this image. The hatch and service stairs are visible (B/C/D exits).'},
    'main_scene:grand_bellevue/public_corridor': {'id': 'CH4-NEW-04', 'title': 'Public corridor (reusable dry base)', 'note': 'The dry base. Flooding is the public_corridor_flood state family, derived from this master.'},
    'portrait:hotel_commodore_bixby:delighted': {'id': 'CH4-NEW-05', 'title': 'Commodore Bixby (one reusable expression)', 'note': 'Miniature naval cap, green auction paddle in pocket. Empty hands: the brass wheel and ice bucket are environment props, never held in the portrait (he hands the wheel away in hotel_bixby_emergency / hotel_bixby_trade). Also serves the commanding node.'},
    'portrait:hotel_wedding_organizer:urgent': {'id': 'CH4-NEW-06', 'title': 'Wedding organizer', 'note': 'One distinct portrait; must match the organizer already drawn in the approved ballroom scene CH4-05 (navy suit, clipboard).'},
    'focus_a:grand_bellevue/bridal_privacy_panel': {'id': 'CH4-NEW-07', 'title': 'Bridal privacy panel (Focus A)', 'note': ''},
    'focus_a:grand_bellevue/autofit_gown': {'id': 'CH4-NEW-08', 'title': 'AutoFit gown (Focus A)', 'note': 'Motor and manual-slack detail as localized states.'},
    'focus_a:grand_bellevue/three_seashells': {'id': 'CH4-NEW-09', 'title': 'Three seashells (Focus A)', 'note': ''},
    'inventory_slot:lot_53_dispute_ticket': {'id': 'CH4-NEW-10', 'title': 'Lot 53 dispute ticket - slot', 'note': '96x96 slot record already exists (not-started).'},
    'inventory_inspect:lot_53_dispute_ticket': {'id': 'CH4-NEW-11', 'title': 'Lot 53 dispute ticket - inspection', 'note': '565x451 inspect record already exists (not-started).'},
    'inventory_slot:wedding_ring_lot31': {'id': 'CH4-NEW-12', 'title': 'Wedding ring - slot', 'note': ''},
    'inventory_inspect:wedding_ring_lot31': {'id': 'CH4-NEW-13', 'title': 'Wedding ring - inspection', 'note': 'The record note says "do not reveal any inscription", but hotel_ring_inspect_inscription and items.draft already author AS IS, WHERE IS. That note is stale (v08 canonicalRegistryGaps); decide how the inscription is revealed before production.'},
    'fatal_aftermath:grand_bellevue/final_occupancy': {'id': 'CH4-NEW-14', 'title': 'Final Occupancy', 'note': 'Popup ch4_final_occupancy unchanged.'},
    'fatal_aftermath:grand_bellevue/pressed_and_steamed': {'id': 'CH4-NEW-15', 'title': 'Pressed and Steamed', 'note': 'Popup unchanged; the hanger artwork is not part of B2-08.'},
    'fatal_aftermath:grand_bellevue/folded_for_convenience': {'id': 'CH4-NEW-16', 'title': 'Folded for Convenience', 'note': 'Popup unchanged.'},
    'fatal_aftermath:grand_bellevue/made_to_measure': {'id': 'CH4-NEW-17', 'title': 'Made to Measure', 'note': 'Popup unchanged.'},
}

# Not in Nate's 17. The current renderer cannot show the organizer or Bixby without it (section 7).
RENDERER_EXCEPTION = {
    'portrait_background:grand_bellevue/ballroom': {
        'id': 'CH4-NEW-18', 'title': 'Ballroom / reception closer background (shared)',
        'note': 'Required by the current renderer for 5 dialogue nodes (organizer x2, Bixby x3). Every layered speaker draws over a 564x278 opaque background for its scene, and the approved alternative CH4-02 is lobby-specific: it shows the auction podium and the framed piano lot that are in the LOBBY scene CH4-01. Reusing it in the ballroom would be untruthful. One shared ballroom/reception background also serves refreshment_table (reuse). If Nate rules CH4-02 acceptable here, this drops out and the active target returns to 62.'},
}

REUSE = {
    'main_scene:grand_bellevue/wedding_entry': {'source': 'main_scene:grand_bellevue/ballroom', 'truth': '"hurries you into the reception hall": the ballroom is the reception hall. The side-entrance moment is narrated.'},
    'main_scene:grand_bellevue/refreshment_table': {'source': 'main_scene:grand_bellevue/ballroom', 'truth': '"At the edge of the reception". The wheel-on-ice-bucket boat and the water creeping under the ballroom door are localized prop/water treatments (B2-09 revised concept), not a unique scene.'},
    'main_scene:grand_bellevue/bridal_corridor': {'source': 'main_scene:grand_bellevue/service_passage', 'truth': '"return to the corridor. The service passage leads back toward the staff lavatory". The same passage is already the approved scene for hotel_bride_service_shortcut and hotel_wedding_service_shortcut, which lead to the bridal room.'},
    'main_scene:grand_bellevue/freight_lift': {'source': 'main_scene:grand_bellevue/upper_salvage', 'truth': 'The lift ride is narrated; the node ends with you "on the mezzanine... The lift remains behind you". NEW-03 must show the lift doors and the W.C. panel.'},
    'portrait:hotel_commodore_bixby:commanding': {'source': 'portrait:hotel_commodore_bixby:delighted', 'truth': 'Same man, same costume. Neither node shows him holding the wheel; he "pulls the wheel free... and presses it into your hands" (narrated).'},
    'portrait_background:grand_bellevue/refreshment_table': {'source': 'portrait_background:grand_bellevue/ballroom', 'truth': 'The refreshment table is at the edge of the reception in the ballroom.'},
}

NARRATIVE = {
    'main_scene:grand_bellevue/arrival': {'constraint': 'C1', 'why': 'Router line after Chapter 3 ("You leave the People\'s Pavilion behind"). A text-led transition.'},
    'main_scene:grand_bellevue/forecourt': {'constraint': 'C1', 'why': 'Two short exterior arrivals across the courtyard. No approved exterior shows glass doors and flowers; loading_lane shows a staircase being removed (a different beat).'},
    'main_scene:grand_bellevue/courtyard': {'constraint': 'C1', 'why': 'Two END CHAPTER 4 park-bound departures. Text-led.'},
    'portrait:bridal_door_ai:neutral': {'constraint': 'C2', 'why': 'Machine voice: no anthropomorphic portrait. The privacy panel (NEW-07) is the device.'},
    'portrait:bathroom_ai:neutral': {'constraint': 'C2', 'why': 'Machine voice: no anthropomorphic portrait.'},
    'portrait:hotel_lift_voice:neutral': {'constraint': 'C2', 'why': 'Machine voice: no anthropomorphic portrait.'},
    'portrait:hotel_salvage_clerk:practical': {'constraint': 'C2', 'why': 'Minor exchange; environmental storytelling in NEW-03.'},
    'portrait:hotel_wedding_guest:curious': {'constraint': 'C2', 'why': 'Minor exchange (one line).'},
    'portrait:hotel_attendant:professional': {'constraint': 'C2', 'why': 'Minor exchange; the floating WET FLOOR sign is environmental.'},
    'portrait_background:grand_bellevue/bridal_dressing_room': {'constraint': 'C2', 'why': 'Only speaker is the door AI (no portrait), so nothing is drawn over it.'},
    'portrait_background:grand_bellevue/bridal_lavatory': {'constraint': 'C2', 'why': 'Only speaker is the bathroom AI (no portrait).'},
    'portrait_background:grand_bellevue/freight_lift': {'constraint': 'C2', 'why': 'Only speaker is the lift voice (no portrait).'},
    'portrait_background:grand_bellevue/upper_salvage': {'constraint': 'C2', 'why': 'Only speaker is the salvage clerk (no portrait).'},
    'portrait_background:grand_bellevue/public_corridor': {'constraint': 'C2', 'why': 'Only speakers are the guest and attendant (no portraits).'},
}

REFINE = {
    'CH4-01': 'main_scene:grand_bellevue/lobby', 'CH4-04': 'main_scene:grand_bellevue/restroom', 'CH4-05': 'main_scene:grand_bellevue/ballroom',
    'CH4-B2-03': 'portrait_background:grand_bellevue/restroom', 'CH4-B2-11': 'portrait_background:grand_bellevue/loading_dock',
}

# The 12 localized-state families (v08 BATCH2-INVENTORY, unchanged). base = the approved or planned master.
STATE_FAMILIES = [
    {'family': 'lobby_door_removal', 'base': 'CH4-01', 'nodes': ['hotel_auctioneer_arrival', 'hotel_restroom_entry'], 'refs': [], 'dependsOnRefinement': True},
    {'family': 'restroom_active_leak', 'base': 'CH4-04 (+CH4-B2-03)', 'nodes': ['hotel_restroom_plumber'], 'refs': [], 'dependsOnRefinement': True},
    {'family': 'restroom_braced_or_contained', 'base': 'CH4-04 (+CH4-B2-03)', 'nodes': ['hotel_valve_braced', 'hotel_wheel_return', 'hotel_key_master_cabinet'], 'refs': [], 'dependsOnRefinement': True},
    {'family': 'restroom_flood', 'base': 'CH4-04', 'nodes': ['hotel_valve_flood'], 'refs': [], 'dependsOnRefinement': True},
    {'family': 'stall_lifting_and_removed', 'base': 'CH4-04', 'nodes': ['hotel_stall_lot_claimed', 'hotel_stall_crane_success', 'hotel_stall_public_corridor_walk'], 'refs': [], 'dependsOnRefinement': True},
    {'family': 'chair_and_ring_states', 'base': 'CH4-B2-24 / CH4-B2-25', 'nodes': ['hotel_chair_stapler_stealth', 'hotel_chair_ring_focus', 'hotel_ring_slips', 'hotel_collection_ring_focus', 'hotel_collection_ring_porter_recovery', 'hotel_collection_ring_stapler_recovery'], 'refs': ['CH4-B2-24-open', 'CH4-B2-25-recovered', 'CH4-B2-25-slipped'], 'dependsOnRefinement': False},
    {'family': 'staff_boxes_attempt', 'base': 'CH4-B2-37 / CH4-B2-41', 'nodes': ['hotel_staff_lavatory_storage', 'hotel_staff_lavatory_move_boxes'], 'refs': ['CH4-B2-37-cleared', 'CH4-B2-37-permit', 'CH4-B2-41-cleared', 'CH4-B2-41-permit'], 'dependsOnRefinement': False},
    {'family': 'boiler_pressure_state', 'base': 'CH4-B2-42 / CH4-B2-47', 'nodes': ['hotel_boiler_pressure_intro', 'hotel_boiler_pressure_relieved'], 'refs': ['CH4-B2-42-relieved', 'CH4-B2-42-inspection-hold', 'CH4-B2-42-staff-access', 'CH4-B2-47-relieved', 'CH4-B2-47-inspection-hold', 'CH4-B2-47-staff-access'], 'dependsOnRefinement': False, 'note': 'Red/green pressure plus the inspection-hold and staff-bypass stagings are all covered by the six B2-08 references.'},
    {'family': 'lot61_open_and_packed', 'base': 'CH4-01 (lobby)', 'nodes': ['hotel_lot61_pod_auction', 'hotel_lot61_pod_escaped', 'hotel_lot61_pod_declined'], 'refs': [], 'dependsOnRefinement': True},
    {'family': 'bridal_privacy_status', 'base': 'CH4-NEW-07 / CH4-NEW-01', 'nodes': ['hotel_bridal_door_focus', 'hotel_bridal_autofit_survived'], 'refs': [], 'dependsOnRefinement': False},
    {'family': 'gown_motor_manual_slack', 'base': 'CH4-NEW-08', 'nodes': ['hotel_bridal_gown_focus', 'hotel_bridal_gown_motor', 'hotel_bridal_autofit_survived'], 'refs': [], 'dependsOnRefinement': False},
    {'family': 'public_corridor_flood', 'base': 'CH4-NEW-04', 'nodes': ['hotel_stall_public_corridor_walk', 'hotel_flooded_public_corridor'], 'refs': [], 'dependsOnRefinement': False},
]

CONSTRAINTS = {
    'C1': {'title': 'Every node draws a scene image',
           'evidence': 'game/js/story-flow.js (main 3a8e07a) line 169 always calls G.setSceneArt for v.scene; convert.js reports a scene key with no record as a DEV PLACEHOLDER (an error in an approved build). Text-led exteriors therefore still need something in the scene aperture.',
           'smallestFallback': 'Game-side presentation rule: a node whose scene key is registered as text-led keeps the previous scene image (for the Chapter 4 opening that is Chapter 3\'s last image, which matches "You leave the People\'s Pavilion behind"). Needs a separately authorized engine change. Interim alternative with no engine work: reused records pointing arrival/forecourt at CH4-B2-06 loading lane and courtyard at CH4-B2-07 service alley. Not recommended: it adds movers and a sofa the text never mentions.',
           'affects': ['main_scene:grand_bellevue/arrival', 'main_scene:grand_bellevue/forecourt', 'main_scene:grand_bellevue/courtyard']},
    'C2': {'title': 'A dialogue node must be led by a speaker with a portrait',
           'evidence': 'game/js/rules.js line 1788: "speaker X is an incidental voice (no portrait): it may only speak in say runs"; stage.js chapterArtKeys throws "No registered portrait for speaker". Incidental voices (docs/104 section 4) may only speak inside another speaker\'s conversation. Chapter 4 has 15 dialogue nodes led by the six portrait-less speakers (door AI 6, bathroom AI 4, lift voice 1, salvage clerk 2, guest 1, attendant 1).',
           'smallestFallback': 'Recommended: a generic engine extension so an incidental voice may lead a dialogue node, presented as Narrative B (no portrait aperture) with the voice\'s NAME: label (the docs/104 section 4 label machinery already exists). No canon or narrative change. Alternative (canon edit, needs approval): switch those 15 nodes to narrative mode with {say, who} runs, wording unchanged. Not recommended: produce 6 portraits and 5 backgrounds (11 images).',
           'affects': sorted([k for k, v in NARRATIVE.items() if v['constraint'] == 'C2'])},
    'C3': {'title': 'Reuse cannot bind before the source art is integrated',
           'evidence': 'convert.js artRecord: a pending binding (runtime-settings pendingArtBindings) accepts only an "approved" record whose first notes SHA-256 equals the bound file. A "reused" record must carry a real art/ assetPath (the reception and wc_key precedent).',
           'smallestFallback': 'Register reuse as status "reused" with the source\'s art/ assetPath at integration time (existing mechanism, no new keys). Bixby commanding can instead change its node pose to delighted, like the retirements. Until then the storyboard records the reuse in docs/137 only.',
           'affects': sorted(REUSE)},
}


# ----------------------------------------------------------------------------------------------
def rd(p, root=ROOT):
    return json.loads((Path(root) / p).read_text(encoding='utf-8'))


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(*args, cwd=ROOT):
    return subprocess.check_output(['git', *args], cwd=cwd)


def colors(img):
    """Distinct visible RGBA values (fully transparent pixels ignored)."""
    raw = img.convert('RGBA').tobytes()
    return len({raw[i:i + 4] for i in range(0, len(raw), 4) if raw[i + 3]})


def registry_record(art, key):
    cat, lk = key.split(':', 1)
    if cat == 'main_scene':
        return art['scenes'].get(lk)
    if cat == 'portrait_background':
        sc = art['scenes'].get(lk)
        return sc.get('portraitBackground') if isinstance(sc, dict) else None
    if cat == 'portrait':
        return art['portraits'].get(lk)
    if cat == 'focus_a':
        return art['focus'].get(lk)
    if cat == 'fatal_aftermath':
        return art['deathScreens'].get(lk)
    if cat.startswith('inventory_'):
        return (art['items'].get(lk) or {}).get(cat.split('_', 1)[1])
    return None


def preview_key(key):
    cat, lk = key.split(':', 1)
    return {'main_scene': 'scenes:' + lk, 'portrait_background': 'scenes:' + lk + '#portraitBackground',
            'portrait': 'portraits:' + lk, 'focus_a': 'focus:' + lk}.get(cat)


def asset_id(rec):
    m = re.search(r'(CH4-(?:B2-)?\d+)\b', (rec or {}).get('notes', ''))
    return m.group(1) if m else None


def walk(v, fn):
    fn(v)
    if isinstance(v, dict):
        for x in v.values():
            walk(x, fn)
    elif isinstance(v, list):
        for x in v:
            walk(x, fn)


def derive(chapter, art):
    """The logical requirements, exactly as the v08 inventory counts them."""
    req = {}

    def add(cat, lk, nid):
        r = req.setdefault(cat + ':' + lk, {'category': cat, 'logicalKey': lk, 'nodeIds': []})
        if nid and nid not in r['nodeIds']:
            r['nodeIds'].append(nid)
    gives = {}
    for nid, n in chapter['nodes'].items():
        add('main_scene', n['scene'], nid)
        if n['mode'] == 'dialogue':
            add('portrait', n['speaker'] + ':' + n['pose'], nid)
            add('portrait_background', n['scene'], nid)
        if n['mode'] == 'focus':
            add('focus_a', n['focus'], nid)
        if n.get('endingArt'):
            add('fatal_aftermath', n['endingArt'], nid)
        def grant(v):
            if isinstance(v, dict) and isinstance(v.get('give'), list):
                for iid in v['give']:
                    if nid not in gives.setdefault(iid, []):
                        gives[iid].append(nid)
        walk(n, grant)
    for iid, rec in art['items'].items():
        for side in ('slot', 'inspect'):
            if 'grand_bellevue' in (((rec or {}).get(side) or {}).get('suggestedFilename') or ''):
                add('inventory_' + side, iid, None)
                req['inventory_' + side + ':' + iid]['nodeIds'] = gives.get(iid, [])
    return req


def classify(req, art, preview):
    out = {}
    for key, r in req.items():
        rec = registry_record(art, key)
        approved = bool(rec) and rec.get('status') in SELECTED
        row = dict(r)
        row['registryStatus'] = rec.get('status') if rec else None
        if approved:
            pk = preview_key(key)
            p = preview.get(pk) if pk else None
            row.update({'assetId': asset_id(rec), 'selectedFile': p and p['file'], 'sha256': p and p['sha256']})
            if key in RETIRE:
                d = RETIRE[key]
                row.update({'disposition': 'RETIRED', 'replacement': d['replacement'], 'replacementId': d['replacementId']})
            else:
                row['disposition'] = 'RETAIN'
            if row['assetId'] in REFINE:
                row['refinementFlag'] = True
        elif key in NEW:
            row.update({'disposition': 'NEW', 'planId': NEW[key]['id'], 'title': NEW[key]['title'], 'brief': NEW[key]['note']})
        elif key in RENDERER_EXCEPTION:
            d = RENDERER_EXCEPTION[key]
            row.update({'disposition': 'NEW_RENDERER_EXCEPTION', 'planId': d['id'], 'title': d['title'], 'brief': d['note']})
        elif key in REUSE:
            row.update({'disposition': 'REUSE', 'source': REUSE[key]['source'], 'truth': REUSE[key]['truth'], 'constraint': 'C3'})
        elif key in NARRATIVE:
            row.update({'disposition': 'NARRATIVE', 'constraint': NARRATIVE[key]['constraint'], 'why': NARRATIVE[key]['why']})
        else:
            row['disposition'] = 'UNDECIDED'
        out[key] = row
    return out


def resolve(plan, key, depth=0):
    """What a requirement finally shows after consolidation: an approved id, a plan id or a note."""
    r = plan[key]
    d = r['disposition']
    if d == 'RETAIN':
        return r['assetId']
    if d == 'RETIRED':
        return resolve(plan, r['replacement'], depth + 1)
    if d in ('NEW', 'NEW_RENDERER_EXCEPTION'):
        return r['planId']
    if d == 'REUSE':
        return resolve(plan, r['source'], depth + 1)
    if d == 'NARRATIVE':
        return NOART[r['constraint']]
    return '??'


def background_for(art, scene, speaker_pose, proposed):
    """Game convert.js bgFor: the scene's own portraitBackground first, else the pose's portraitBackgroundScene."""
    sc = art['scenes'].get(scene) or {}
    retired_bg = proposed and scene == 'grand_bellevue/boiler_access'
    if isinstance(sc.get('portraitBackground'), dict) and not retired_bg:
        return 'portrait_background:' + scene
    via = (art['portraits'].get(speaker_pose) or {}).get('portraitBackgroundScene')
    if proposed and speaker_pose == 'hotel_porter:alarmed':
        via = 'grand_bellevue/service_passage'
    if via and isinstance((art['scenes'].get(via) or {}).get('portraitBackground'), dict):
        return 'portrait_background:' + via
    return 'portrait_background:' + scene


def proposed_pose(nid, pose):
    for d in RETIRE.values():
        for n, old, new in d['poseChanges']:
            if n == nid and old == pose:
                return new
    for n, _, old, new in REUSE_POSES:
        if n == nid and old == pose:
            return new
    return pose


def coverage(chapter, art, plan, proposed=True):
    """Node coverage. proposed=True: base canon projected through the decisions (the plan);
    proposed=False: what this tree's canon resolves to as-is (after `apply`)."""
    fam = {}
    for f in STATE_FAMILIES:
        for n in f['nodes']:
            fam.setdefault(n, []).append(f['family'])
    rows = []
    for nid, n in chapter['nodes'].items():
        row = {'node': nid, 'mode': n['mode'], 'scene': n['scene'],
               'mainScene': resolve(plan, 'main_scene:' + n['scene'])}
        if n['mode'] == 'dialogue':
            sp = n['speaker'] + ':' + n['pose']
            new_sp = n['speaker'] + ':' + (proposed_pose(nid, n['pose']) if proposed else n['pose'])
            row['speaker'] = sp
            row['portraitNow'] = plan['portrait:' + sp].get('assetId') or resolve(plan, 'portrait:' + sp)
            row['portrait'] = resolve(plan, 'portrait:' + new_sp)
            if row['portrait'] == NOART['C2']:
                row['background'] = 'none (Narrative B; C2)'
                row['backgroundNow'] = row['background']
            else:
                bnow = background_for(art, n['scene'], sp, False)
                bnew = background_for(art, n['scene'], new_sp, proposed)
                row['backgroundNow'] = plan[bnow].get('assetId') or resolve(plan, bnow) if bnow in plan else '??'
                row['background'] = resolve(plan, bnew) if bnew in plan else '??'
        if n['mode'] == 'focus':
            row['focus'] = resolve(plan, 'focus_a:' + n['focus'])
        if n.get('endingArt'):
            row['endingArt'] = resolve(plan, 'fatal_aftermath:' + n['endingArt'])
            row['deathPopup'] = (n.get('deathPopup') or {}).get('id')
        if fam.get(nid):
            row['stateFamilies'] = fam[nid]
        rows.append(row)
    return rows


def load_canon(root=ROOT, base=False):
    """This tree's canon, or (base=True) the pre-consolidation canon at CANON_BASE."""
    if base:
        get = lambda rel: json.loads(git('show', CANON_BASE + ':' + rel))
        return get(CHAPTER), get(ARTWORK), get(PREVIEW)['images']
    return rd(CHAPTER, root), rd(ARTWORK, root), rd(PREVIEW, root)['images']


def counts(plan):
    c = {}
    for r in plan.values():
        c[r['disposition']] = c.get(r['disposition'], 0) + 1
    return c


# ----------------------------------------------------------------------------------------------
def build():
    chapter, art, preview = load_canon(base=True)
    req = derive(chapter, art)
    plan = classify(req, art, preview)
    rows = coverage(chapter, art, plan)
    c = counts(plan)
    approved = c.get('RETAIN', 0) + c.get('RETIRED', 0)
    base = CANON_BASE
    out = {
        'schema': 'out-of-order-ch4-artwork-consolidation-v1',
        'title': 'Chapter 4 artwork consolidation - proposed inventory, mappings and coverage',
        'status': 'APPROVED by Nate 2026-11-24 (PR #31) and applied by tools/sync/ch4-consolidation.py apply. Derived from the pre-consolidation canon CANON_BASE so every mapping stays reproducible.',
        'canonicalBase': base,
        'auditCheckpoints': AUDIT,
        'derivedBy': 'tools/sync/ch4-consolidation.py build',
        'counts': {
            'logicalRequirements': len(plan),
            'byCategory': {k: sum(1 for r in plan.values() if r['category'] == k) for k in BASELINE},
            'approvedPrimaryOnMain': approved,
            'retainedApproved': c.get('RETAIN', 0),
            'retired': c.get('RETIRED', 0),
            'newPrimary': c.get('NEW', 0),
            'newRendererException': c.get('NEW_RENDERER_EXCEPTION', 0),
            'reuse': c.get('REUSE', 0),
            'narrativeOrPresentation': c.get('NARRATIVE', 0),
            'activePrimaryTarget': c.get('RETAIN', 0) + c.get('NEW', 0),
            'activePrimaryWithRendererException': c.get('RETAIN', 0) + c.get('NEW', 0) + c.get('NEW_RENDERER_EXCEPTION', 0),
            'stateFamilies': len(STATE_FAMILIES),
            'supplementalReferencesPreserved': sum(len(f['refs']) for f in STATE_FAMILIES),
            'nodes': len(chapter['nodes']),
        },
        'retirements': [dict(retire=k, **v) for k, v in RETIRE.items()],
        'reuse': [dict(requirement=k, sourceResolvesTo=resolve(plan, v['source']), **v) for k, v in REUSE.items()],
        'narrativeOrPresentation': [dict(requirement=k, **v) for k, v in NARRATIVE.items()],
        'newPrimary': [dict(requirement=k, **v) for k, v in NEW.items()],
        'rendererException': [dict(requirement=k, **v) for k, v in RENDERER_EXCEPTION.items()],
        'refinementFlags': [{'id': i, 'requirement': k} for i, k in REFINE.items()],
        'stateFamilies': STATE_FAMILIES,
        'rendererConstraints': CONSTRAINTS,
        'requirements': plan,
        'nodeCoverage': rows,
    }
    PLAN.write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    cols = ['node', 'mode', 'scene', 'mainScene', 'speaker', 'portraitNow', 'portrait', 'backgroundNow', 'background', 'focus', 'endingArt', 'deathPopup', 'stateFamilies']
    lines = ['\t'.join(cols)]
    for r in rows:
        lines.append('\t'.join(','.join(r[c]) if isinstance(r.get(c), list) else str(r.get(c, '')) for c in cols))
    TSV.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps(out['counts'], indent=1))


# ----------------------------------------------------------------------------------------------
class Checks:
    def __init__(self):
        self.items = []

    def __call__(self, ok, label, detail=None):
        self.items.append({'check': label, 'passed': bool(ok), **({'detail': detail} if detail is not None else {})})
        if not ok:
            print('FAIL', label, detail if detail is not None else '')
        return ok

    @property
    def failed(self):
        return [c for c in self.items if not c['passed']]


def live_file(r):
    """Where an approved selection's bytes live now (CH4-B2-16 moved to the retired archive by `apply`)."""
    p = ROOT / r['selectedFile']
    if not p.exists() and r.get('assetId') == 'CH4-B2-16':
        p = ROOT / RETIRED_DIR / 'CH4-B2-16-v01.png'
    return p


def verify_applied(check, report, b_ch, b_art, b_pv, chapter, art, preview):
    """This tree must be exactly CANON_BASE plus the approved edit set (and nothing else)."""
    diffs = []
    for nid in b_ch['nodes']:
        b, p = b_ch['nodes'][nid], chapter['nodes'][nid]
        diffs += [[nid, k, b.get(k), p.get(k)] for k in sorted(set(b) | set(p)) if b.get(k) != p.get(k)]
    expect = [[n, 'pose', o, w] for d in RETIRE.values() for n, o, w in d['poseChanges']] + [[n, 'pose', o, w] for n, _, o, w in REUSE_POSES]
    check(sorted(diffs) == sorted(expect) and {k: v for k, v in b_ch.items() if k != 'nodes'} == {k: v for k, v in chapter.items() if k != 'nodes'},
          'Chapter 4 differs from CANON_BASE only in 8 pose fields (7 retirements + Bixby commanding -> delighted); text, choices, flags, items, d6, endings untouched', diffs)
    report['poseChanges'] = diffs
    for rel in ('story/items.draft.json', 'story/storyboard-manifest.json', 'story/chapters/prologue-00.draft.json', 'story/chapters/chapter-01.draft.json',
                'story/chapters/chapter-02.draft.json', 'story/chapters/chapter-03.draft.json', 'story/death-presentations.export.json',
                'story/game-integration.json', 'story/sync-contract.json', 'story/storyboard-layout.json'):
        check(git('show', CANON_BASE + ':' + rel) == (ROOT / rel).read_bytes(), 'Byte-identical to CANON_BASE: ' + rel)
    exp = copy.deepcopy(b_art)
    for k, d in RETIRE.items():
        if k.startswith('portrait:'):
            rec = registry_record(exp, k)
            cur = registry_record(art, k)
            check(cur['notes'] == retired_prefix(d) + rec['notes'] and {x: y for x, y in cur.items() if x != 'notes'} == {x: y for x, y in rec.items() if x != 'notes'}
                  and re.search(r'SHA-256[^0-9a-f]{0,3}([0-9a-f]{64})', cur['notes']).group(1) == re.search(r'SHA-256[^0-9a-f]{0,3}([0-9a-f]{64})', rec['notes']).group(1),
                  'Retired %s: archived (viewer Archived filter) with its approval, fields and first SHA-256 unchanged' % d['id'])
            rec['notes'] = cur['notes']
    exp['scenes']['grand_bellevue/boiler_access'].pop('portraitBackground')
    check(art['scenes']['grand_bellevue/boiler_access']['notes'].startswith(b_art['scenes']['grand_bellevue/boiler_access']['notes'] + ' CH4-B2-16 closer background RETIRED'),
          'Boiler-access scene keeps its original notes; retirement appended')
    exp['scenes']['grand_bellevue/boiler_access']['notes'] = art['scenes']['grand_bellevue/boiler_access']['notes']
    exp['portraits']['hotel_porter:alarmed']['portraitBackgroundScene'] = 'grand_bellevue/service_passage'
    for k, rec in no_image_records(b_ch).items():
        cat, lk = k.split(':', 1)
        (exp['scenes'] if cat == 'main_scene' else exp['portraits'])[lk] = rec
    for side, b in RING_BRIEF.items():
        exp['items']['wedding_ring_lot31'][side].update(b)
    check(exp == art, 'Artwork registry = CANON_BASE + exactly the approved edits (retirement notes, B2-16 out, alarmed background scene, 9 no-image records, ring brief)')
    ring = art['items']['wedding_ring_lot31']
    check(all(ring[side]['status'] == 'not-started' and ring[side]['assetPath'] is None and {k: ring[side][k] for k in b} == b for side, b in RING_BRIEF.items())
          and 'AS IS, WHERE IS.' in ring['inspect']['prompt'] and not ring['inspect']['notes'].startswith('CH4 WORKING DRAFT'),
          'Ring brief matches the approved inscription reveal (AS IS, WHERE IS.); art stays unproduced')
    ledger = json.loads(LEDGER.read_text(encoding='utf-8'))
    led = {e['id']: e for e in ledger['retired']}
    check(sorted(led) == sorted(d['id'] for d in RETIRE.values()) and all(led[d['id']]['originalRecordVerbatim'] == registry_record(b_art, k) for k, d in RETIRE.items()),
          'Ledger holds all 7 retired records verbatim from CANON_BASE')
    bpk = 'scenes:grand_bellevue/boiler_access#portraitBackground'
    kept = ROOT / RETIRED_DIR / 'CH4-B2-16-v01.png'
    check(kept.exists() and sha(kept.read_bytes()) == b_pv[bpk]['sha256'] == 'e396db0771247012401cccf3a481d329947381a677c445ccc0a04d61b21f77f3'
          and sha(git('show', b_pv[bpk]['source']['commit'] + ':' + b_pv[bpk]['source']['path'])) == b_pv[bpk]['sha256'],
          'CH4-B2-16 exact bytes preserved in the retired archive and at its pinned source commit')
    check(preview == {k: v for k, v in b_pv.items() if k != bpk}, 'Preview registry = CANON_BASE minus only the CH4-B2-16 entry; every other entry identical')
    bad = [k for k, v in preview.items() if sha((ROOT / v['file']).read_bytes()) != v['sha256']]
    check(not bad, 'Every selected file matches its preview SHA (%d)' % len(preview), bad)
    base_files = set(git('ls-tree', '-r', '--name-only', CANON_BASE, '--', 'assets/selected').decode().split('\n')) - {''}
    now_files = {str(p.relative_to(ROOT)) for p in (ROOT / 'assets/selected').rglob('*') if p.is_file() and p.name != '.DS_Store'}
    check(base_files - now_files == {b_pv[bpk]['file']} and not now_files - base_files, 'Selected package = CANON_BASE minus the one retired CH4-B2-16 copy')
    hist = [h for h in git('diff', '--name-status', CANON_BASE, '--', 'tools/prologue-art-lab/assets', 'docs').decode().split('\n') if h]
    bad = [h for h in hist if not h.startswith('A') and not h.split('\t')[-1].startswith(('docs/136_CH4_B208_APPROVAL_COMPLETION_20261124.md', 'docs/103_'))]
    check(not bad, 'No review package, approval record or art-lab asset modified or deleted (additions only; docs/103 and docs/136 annotated)', bad)
    ni = no_image_records(b_ch)
    check(len(ni) == 9 and sum(r['format'] == 'text-led' for r in ni.values()) == 3 and sum(r['format'] == 'voice-only' for r in ni.values()) == 6,
          '9 approved no-image presentation records: 3 text-led scenes (C1), 6 voice-only speakers (C2)')
    check(all(registry_record(art, k)['assetPath'] is None and preview_key(k) not in preview for k in ni), 'No-image records carry no assetPath and no preview')


def verify_core(check):
    chapter, art, preview = load_canon()
    nodes = chapter['nodes']
    stored = json.loads(PLAN.read_text(encoding='utf-8'))
    report = {}

    b_ch, b_art, b_pv = load_canon(base=True)
    report['canonicalBase'] = CANON_BASE
    check(subprocess.run(['git', 'merge-base', '--is-ancestor', CANON_BASE, 'HEAD'], cwd=ROOT).returncode == 0, 'CANON_BASE %s is an ancestor of this branch' % CANON_BASE[:7])

    # Narrative structure ----------------------------------------------------------------------
    check(len(nodes) == 120, '120 Chapter 4 nodes', len(nodes))
    dests = []

    def collect(v):
        if isinstance(v, dict):
            for k in ('to', 'pass', 'fail'):
                if isinstance(v.get(k), str):
                    dests.append(v[k])
    for n in nodes.values():
        walk(n.get('choices'), collect)
        walk(n.get('show'), collect)
        walk(n.get('use'), collect)
    missing = sorted({d for d in dests if d not in nodes})
    check(not missing, 'Every choice / SHOW / USE / pass / fail destination resolves (%d links)' % len(dests), missing)
    reachable, todo = set(), [chapter['start']]
    while todo:
        x = todo.pop()
        if x in reachable or x not in nodes:
            continue
        reachable.add(x)
        found = []
        for f in ('choices', 'show', 'use'):
            walk(nodes[x].get(f), lambda v: isinstance(v, dict) and [found.append(v[k]) for k in ('to', 'pass', 'fail') if isinstance(v.get(k), str)])
        todo.extend(found)
    check(len(reachable) == 120, 'All 120 nodes reachable from hotel_entry_dispatch (ignoring conditions)', sorted(set(nodes) - reachable))
    dev = chapter['development']
    entry = nodes[chapter['start']]['choices']
    exits = [c['if']['flagIs'][1] for c in entry if c.get('if', {}).get('flagIs', [None])[0] == dev['chapter3ExitFlagRequired']]
    check(exits == dev['chapter3ExitIds'] and len(exits) == 7 and all(c['to'] in nodes for c in entry),
          'Seven Chapter 3 entry routes: dispatch keys on ch3_exit_route and each lands on an existing node', exits)
    dice = []
    walk(chapter, lambda v: isinstance(v, dict) and isinstance(v.get('check'), dict) and dice.append(v['check']))
    check(len(dice) == 8 and all(d.get('sides') == 6 for d in dice), 'Hidden d6 checks present (8 x d6)', [d['id'] for d in dice])
    report['d6'] = {'count': len(dice), 'sha256': sha(json.dumps(dice, sort_keys=True).encode())}
    fatal = [nid for nid, n in nodes.items() if n.get('endingArt')]
    check(len(fatal) == 4 and all(nodes[f].get('end') and all(k in (nodes[f].get('deathPopup') or {}) for k in ('id', 'title', 'description', 'button')) for f in fatal),
          'Four fatal endings: end=true with a complete deathPopup (id/title/description/button)', fatal)
    export = rd('story/death-presentations.export.json')
    ex_ids = json.dumps(export)
    check(all(nodes[f]['deathPopup']['id'] in ex_ids or nodes[f]['deathPopup']['title'] in ex_ids for f in fatal) or True,
          'Death-presentation export inspected (Chapter 4 is notForGameplay; export coverage reported, not required)',
          {f: (nodes[f]['deathPopup']['id'] in ex_ids) for f in fatal})
    items = rd('story/items.draft.json')
    used = set()

    def items_in(v):
        if isinstance(v, dict):
            for k in ('give', 'take', 'hasItem', 'item', 'notHasItem', 'has', 'hasAll', 'hasAny'):
                x = v.get(k)
                if isinstance(x, str):
                    used.add(x)
                elif isinstance(x, list):
                    used.update(i for i in x if isinstance(i, str))
    for n in nodes.values():
        walk(n, items_in)
        for f in ('show', 'use'):
            used.update((n.get(f) or {}).keys())
    check(used and all(i in items for i in used), 'Every item Chapter 4 gives, takes, tests, SHOWs or USEs exists in items.draft.json', sorted(used))
    check(all(dev.get(k) for k in ('approvedItemCardsOnChair', 'approvedItemCardsAtBoiler', 'approvedItemCardAtGroom')), 'Approved item-gated card rules present in development metadata')

    # Requirements & plan ----------------------------------------------------------------------
    req = derive(b_ch, b_art)
    plan = classify(req, b_art, b_pv)
    cat = {k: sum(1 for r in plan.values() if r['category'] == k) for k in BASELINE}
    check(cat == BASELINE and len(plan) == 90, 'Independent derivation = 90 logical requirements (23 scenes, 36 poses, 15 backgrounds, 8 Focus, 4 item, 4 fatal)', cat)
    check(not [k for k, r in plan.items() if r['disposition'] == 'UNDECIDED'], 'Every requirement has exactly one disposition', [k for k, r in plan.items() if r['disposition'] == 'UNDECIDED'])
    dead = [k for k in list(RETIRE) + list(NEW) + list(RENDERER_EXCEPTION) + list(REUSE) + list(NARRATIVE) if k not in plan]
    check(not dead, 'No decision names a requirement that canon does not have', dead)
    overlap = [k for k in plan if sum(k in d for d in (RETIRE, NEW, RENDERER_EXCEPTION, REUSE, NARRATIVE)) > 1]
    check(not overlap, 'No requirement is decided twice', overlap)
    check(stored['requirements'] == plan and stored['nodeCoverage'] == coverage(b_ch, b_art, plan),
          'Committed plan JSON equals a fresh derivation from CANON_BASE (rebuild if this fails)')
    c = counts(plan)
    report['counts'] = c
    check(c.get('RETAIN', 0) + c.get('RETIRED', 0) == 52, 'Approved primary Chapter 4 selections on main = 52 (46 at audit + 6 B2-08 via PR #30)', c)
    check(c.get('RETIRED') == 7 and c.get('RETAIN') == 45, '7 retirements, 45 approved retained')
    check(c.get('NEW', 0) + c.get('NEW_RENDERER_EXCEPTION', 0) + c.get('RETAIN', 0) == 63, 'Approved active primary target = 63 (45 retained + 17 new + CH4-NEW-18)')
    check(c.get('NEW') == 17, '17 genuinely new primary images (Nate\'s list)', c.get('NEW'))
    check(c.get('REUSE', 0) + c.get('NARRATIVE', 0) + c.get('NEW_RENDERER_EXCEPTION', 0) == 21, '21 remaining demands resolved without Nate\'s 17 (reuse + narrative + 1 renderer exception)')

    # Approved selections: bytes, contracts, provenance, 4x ------------------------------------
    approvals = {}
    for f in APPROVAL_DOCS:
        d = json.loads(f.read_text(encoding='utf-8'))
        for a in d['assets']:
            approvals[a['id']] = (f.name, a, d)
    check(len(approvals) == 52, 'Approval records docs/127-136 name 52 primary assets', len(approvals))
    contracts = {'main_scene': ((314, 206), 'opaque'), 'portrait_background': ((564, 278), 'opaque'),
                 'portrait': ((564, 278), 'transparent'), 'focus_a': ((564, 278), 'opaque')}
    fourx = srcok = 0
    color = {}
    for key, r in plan.items():
        if r['disposition'] not in ('RETAIN', 'RETIRED'):
            continue
        aid = r['assetId']
        raw = live_file(r).read_bytes()
        im = Image.open(BytesIO(raw))
        size, alpha = contracts[r['category']]
        a_ext = im.convert('RGBA').getchannel('A').getextrema()
        ok_alpha = a_ext == (255, 255) if alpha == 'opaque' else a_ext[0] == 0
        check(im.size == size and ok_alpha, 'Native %s %dx%d %s: %s' % (aid, size[0], size[1], alpha, key))
        doc, a, d = approvals.get(aid, (None, {}, {}))
        check(sha(raw) == r['sha256'] == a.get('sha256'), 'Selected bytes = preview SHA = approval record SHA: %s (%s)' % (aid, doc))
        src = a.get('source') or {}
        try:
            blob = git('show', src['commit'] + ':' + src['path'])
            srcok += check(sha(blob) == sha(raw), 'Pinned source blob identical: %s @ %s' % (aid, src['commit'][:7]))
        except Exception as e:  # blobless clone offline
            check(False, 'Pinned source blob readable: %s' % aid, str(e)[:200])
        p4 = a.get('approvedPreview4x')
        if p4:
            big_raw = git('show', src['commit'] + ':' + p4['path'])
            big = Image.open(BytesIO(big_raw))
            nn = im.resize((im.width * 4, im.height * 4), Image.NEAREST)
            fourx += check(sha(big_raw) == p4['sha256'] and big.size == nn.size and big.convert('RGBA').tobytes() == nn.convert('RGBA').tobytes(),
                           'Approved exact 4x preview = nearest-neighbour 4x of native: %s' % aid)
        if aid in REFINE:
            color[aid] = colors(im)
    report['fourX'] = {'checked': fourx, 'noRecordedPreview': [k for k, (f, a, d) in approvals.items() if not a.get('approvedPreview4x')]}
    report['sourceBlobsIdentical'] = srcok
    supp = []
    for f in APPROVAL_DOCS:
        for s in json.loads(f.read_text(encoding='utf-8')).get('supplementalReferences') or []:
            supp.append(s)
    sup_files = {p.name: p for p in (ROOT / 'tools/prologue-art-lab/assets/approved/conditional-production-references/chapter-04').rglob('*.png')}
    sup_ok = [s['id'] for s in supp if any(n.startswith(s['id'] + '-v') and sha(p.read_bytes()) == s['sha256'] for n, p in sup_files.items())]
    check(len(supp) == 13 and len(sup_ok) == 13 and len(sup_files) == 13, '13 approved supplemental references preserved byte-exact (7 earlier + 6 B2-08)', sup_ok)
    fam_refs = sorted(r for f in STATE_FAMILIES for r in f['refs'])
    check(fam_refs == sorted(s['id'] for s in supp), 'Every supplemental reference is assigned to exactly one state family')
    check(len(STATE_FAMILIES) == 12 and all(n in nodes for f in STATE_FAMILIES for n in f['nodes']), '12 state families, every listed node exists')

    # Retirements: physical truth rules -------------------------------------------------------
    for k, d in RETIRE.items():
        r, rep = plan[k], plan[d['replacement']]
        check(r['disposition'] == 'RETIRED' and rep['disposition'] == 'RETAIN' and rep['assetId'] == d['replacementId'] and r['assetId'] == d['id'],
              'Retire %s -> %s: both approved; replacement retained' % (d['id'], d['replacementId']))
        if k.startswith('portrait:'):
            check(k.split(':')[1] == d['replacement'].split(':')[1], 'Same character: %s / %s' % (d['id'], d['replacementId']))
            for nid, old, new in d['poseChanges']:
                check(b_ch['nodes'][nid]['pose'] == old and nodes[nid]['pose'] == new and nodes[nid]['speaker'] == k.split(':')[1],
                      'Node %s: %s:%s -> %s' % (nid, k.split(':')[1], old, new))
            check(sorted(n for n, o, _ in d['poseChanges']) == sorted(r['nodeIds']), 'Pose remap covers every node of %s' % d['id'], r['nodeIds'])
    grateful = [nid for nid, n in nodes.items() if n.get('speaker') == 'hotel_bride' and n['pose'] == 'grateful']
    handed = []
    walk(nodes, lambda v: None)
    for nid, n in nodes.items():
        hit = []
        walk(n, lambda v: isinstance(v, dict) and 'wedding_ring_lot31' in (v.get('take') or []) and hit.append(1))
        if hit:
            handed.append(nid)
    check(grateful == ['hotel_bride_ring_handover'] and handed == ['hotel_bride_ring_handover'],
          'Ring rule: the ring-holding grateful bride appears only where the ring is handed over', {'grateful': grateful, 'ringTaken': handed})
    rows = coverage(b_ch, b_art, plan)
    byn = {r['node']: r for r in rows}
    now = {r['node']: r for r in coverage(chapter, art, plan, proposed=False)}
    keys = ('mainScene', 'portrait', 'background', 'focus', 'endingArt')
    drift = [n for n in byn if any(byn[n].get(k) != now[n].get(k) for k in keys)]
    check(not drift, 'Applied canon resolves every node exactly as the approved plan (main scene, portrait, background, Focus, ending)', drift)
    check(byn['hotel_collection_slip_spotted']['background'] == 'CH4-B2-23' and byn['hotel_collection_slip_spotted']['backgroundNow'] == 'CH4-B2-16',
          'B2-16 -> B2-23 resolves through the importer background rule for hotel_collection_slip_spotted')
    check(byn['hotel_chair_stapler_caught']['background'] == byn['hotel_chair_stapler_caught']['backgroundNow'] == 'CH4-02',
          'Alarmed porter keeps the lobby background in the lobby (hotel_chair_stapler_caught)')
    check(byn['hotel_collection_slip_unnoticed']['mainScene'] == byn['hotel_collection_slip_spotted']['mainScene'] == 'CH4-B2-13',
          'Boiler-access MAIN scene CH4-B2-13 kept on both slip nodes')
    changed_rows = [r['node'] for r in rows if 'portrait' in r and (r['portraitNow'] != r['portrait'] or r['backgroundNow'] != r['background'])]
    expect = sorted(n for d in RETIRE.values() for n, _, _ in d['poseChanges']) + ['hotel_collection_slip_spotted']
    check(sorted(changed_rows) == sorted(expect), 'Exactly the 8 retirement nodes change presentation among approved art', sorted(changed_rows))
    verify_applied(check, report, b_ch, b_art, b_pv, chapter, art, preview)

    # Coverage ---------------------------------------------------------------------------------
    unresolved = [r['node'] for r in rows if '??' in json.dumps(r)]
    check(len(rows) == 120 and not unresolved, 'All 120 nodes have a resolved main scene and, where shown, portrait/background/focus/ending', unresolved)
    c2 = [r['node'] for r in rows if r.get('portrait') == NOART['C2']]
    check(len(c2) == 15, 'Dialogue nodes led by portrait-less speakers (constraint C2) = 15', c2)
    report['c2Nodes'] = c2
    c1 = [r['node'] for r in rows if r['mainScene'] == NOART['C1']]
    report['c1Nodes'] = c1
    check(len(c1) == 5, 'Text-led scene nodes (constraint C1) = 5', c1)
    for f in fatal:
        check(byn[f]['endingArt'] in [v['id'] for v in NEW.values()], 'Fatal %s -> %s' % (f, byn[f]['endingArt']))
    check(not any(k.startswith('portrait:hotel_commodore_bixby') and plan[k]['disposition'] == 'RETAIN' for k in plan) and
          not list((ROOT / 'assets/selected').rglob('*bixby*')), 'B2-09 paused: no Bixby art registered or selected')

    # Diagnostics -----------------------------------------------------------------------------
    bench = {p.name: colors(Image.open(p)) for p in sorted((ROOT / 'assets/selected/art/scenes/biology_park').glob('*.png'))}
    report['colorDiagnostics'] = {'refinementFlags': color, 'chapter2SceneBenchmarks': {'count': len(bench), 'min': min(bench.values()), 'max': max(bench.values())},
                                  'otherChapter4Approved': {plan[k]['assetId']: colors(Image.open(live_file(plan[k]))) for k in plan
                                                            if plan[k]['disposition'] in ('RETAIN', 'RETIRED') and plan[k]['category'] in ('main_scene', 'portrait_background') and plan[k]['assetId'] not in REFINE}}
    check(all(color[i] > 10 * max(bench.values()) for i in color), 'All five refinement flags exceed 10x the Chapter 2 scene colour ceiling (diagnostic only)', color)
    return report


def verify():
    check = Checks()
    report = verify_core(check)
    old = json.loads(VERIFY.read_text(encoding='utf-8')) if VERIFY.exists() else {}
    out = {'schema': 'out-of-order-ch4-consolidation-verification-v1', 'tool': 'tools/sync/ch4-consolidation.py verify',
           'result': 'PASS' if not check.failed else 'FAIL', 'passed': len(check.items) - len(check.failed), 'failed': len(check.failed),
           'report': report, 'checks': check.items}
    if 'gameCheck' in old:
        out['gameCheck'] = old['gameCheck']
    VERIFY.write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    print('verify: %d passed, %d failed' % (out['passed'], out['failed']))
    return 0 if not check.failed else 1


# ----------------------------------------------------------------------------------------------
RING_BRIEF = {
    'slot': {
        'prompt': 'Draft brief, not approved art: small simple silver wedding band with one strand of pale blue ribbon caught around it; understated 1960s styling on a transparent 96×96 slot canvas. No legible lettering at slot scale.',
        'notes': 'CH4 DRAFT BRIEF — not yet requested, generated, selected or approved. Corrected 2026-11-24 (docs/137 NEW-12, Nate): the inscription reveal is already approved canon (hotel_ring_inspect_inscription and the wedding_ring_lot31 read text): AS IS, WHERE IS. Nothing is legible at 96×96, and the slot never shows other wording.'},
    'inspect': {
        'prompt': "Draft brief, not approved art: close-up of the simple silver wedding band with its loose pale blue ribbon, the inner curve turned toward the viewer, showing a tiny maker's mark and the engraving AS IS, WHERE IS. as fine lettering that follows the curve (exactly those words, capitals and punctuation; no other words). Keep the engraving small, so the unread description ('too small to read at a glance') stays true while the approved words are correct wherever the pixels resolve them. 565×451 item-inspect view, restrained 1960s palette, no ornate jewelry or ring box.",
        'notes': "CH4 DRAFT BRIEF — not yet requested, generated, selected or approved. Corrected 2026-11-24 (docs/137 NEW-13, Nate): replaces the stale 'Inscription not authored yet'. Canon reveals the engraving in hotel_ring_inspect_inscription and the item's read text (beneath a tiny maker's mark: AS IS, WHERE IS.). The text reveal stays authoritative; the art never shows any other wording."},
}


VOICE_TITLES = {'bridal_door_ai': 'Bridal door AI', 'bathroom_ai': 'Bathroom AI', 'hotel_lift_voice': 'Freight-lift voice',
                'hotel_salvage_clerk': 'Salvage clerk', 'hotel_wedding_guest': 'Wedding guest', 'hotel_attendant': 'Hotel attendant'}


def no_image_records(chapter):
    """C1 / C2 owner-approved presentation records: they carry no image and must never get one."""
    nodes = chapter['nodes']
    out = {}
    for k, v in NARRATIVE.items():
        cat, lk = k.split(':', 1)
        if cat == 'main_scene':
            ids = [n for n, x in nodes.items() if x['scene'] == lk]
            out[k] = {
                'title': lk.split('/')[1].replace('_', ' ').capitalize() + ' — text-led transition',
                'kind': 'scene', 'status': 'approved', 'format': 'text-led', 'assetPath': None, 'suggestedFilename': None,
                'prompt': 'NO IMAGE. Owner-approved text-led transition: the previous scene image stays on screen (docs/137 section 8, C1). Do not commission artwork for this key.',
                'notes': 'OWNER APPROVED NO-IMAGE PRESENTATION — Nate, 2026-11-24 (docs/137 C1). ' + v['why'] + ' Nodes: ' + ', '.join(ids) + '. The game keeps the previous scene image once its generic text-led capability is integrated.'}
        elif cat == 'portrait':
            sid = lk.split(':')[0]
            ids = [n for n, x in nodes.items() if x.get('speaker') == sid and x['mode'] == 'dialogue']
            out[k] = {
                'title': VOICE_TITLES[sid] + ' — voice only',
                'kind': 'portrait', 'status': 'approved', 'format': 'voice-only', 'assetPath': None, 'suggestedFilename': None,
                'prompt': 'NO IMAGE. Owner-approved voice-only speaker: leads dialogue in Narrative B with its NAME: label and no portrait aperture (docs/137 section 8, C2). Do not commission a portrait or a closer background.',
                'notes': 'OWNER APPROVED NO-IMAGE PRESENTATION — Nate, 2026-11-24 (docs/137 C2). ' + v['why'] + ' Leads: ' + ', '.join(ids) + '.'}
    return out


def retired_prefix(d):
    """The viewer's retiredArt convention (Chapter 3 precedent): Archived filter, DO NOT GENERATE. The original
    approval notes follow unchanged, so the first SHA-256 in the notes is still the approved selection."""
    nodes = ', '.join(n for n, _, _ in d['poseChanges'])
    return ('ARCHIVED / RETIRED / UNUSED — CHAPTER 4 CONSOLIDATION (docs/137; Nate, 2026-11-24). Approved image kept as history: '
            + nodes + ' now use ' + d['replacementId'] + '. Do not generate, re-select or import. Original approval record follows: ')


def apply_edits(root, ledger=False):
    """The Nate-approved edit set. In the real tree it runs once (`apply`); game-check never needs it."""
    root = Path(root)
    ch = rd(CHAPTER, root)
    art = rd(ARTWORK, root)
    pv = rd(PREVIEW, root)
    if art['portraits']['hotel_porter:alarmed'].get('portraitBackgroundScene') != 'grand_bellevue/lobby':
        raise SystemExit('apply: the consolidation is already applied to ' + str(root))
    base_art = copy.deepcopy(art)
    for k, d in RETIRE.items():
        for nid, old, new in d['poseChanges']:
            assert ch['nodes'][nid]['pose'] == old, nid
            ch['nodes'][nid]['pose'] = new
        if k.startswith('portrait:'):
            rec = registry_record(art, k)
            rec['notes'] = retired_prefix(d) + rec['notes']
    for nid, sid, old, new in REUSE_POSES:
        assert ch['nodes'][nid]['speaker'] == sid and ch['nodes'][nid]['pose'] == old, nid
        ch['nodes'][nid]['pose'] = new
    # CH4-B2-16: out of the active registry. Record verbatim in the ledger; bytes to the retired archive.
    sc = art['scenes']['grand_bellevue/boiler_access']
    removed = sc.pop('portraitBackground')
    pk = 'scenes:grand_bellevue/boiler_access#portraitBackground'
    prev = pv['images'].pop(pk)
    src = root / prev['file']
    dst = root / RETIRED_DIR / 'CH4-B2-16-v01.png'
    dst.parent.mkdir(parents=True, exist_ok=True)
    data = src.read_bytes()
    assert sha(data) == prev['sha256']
    dst.write_bytes(data)
    src.unlink()
    for d in (src.parent, src.parent.parent):
        if d.is_dir() and not any(p.name != '.DS_Store' for p in d.iterdir()):
            shutil.rmtree(d)
    sc['notes'] += (' CH4-B2-16 closer background RETIRED FROM ACTIVE COVERAGE — Nate, 2026-11-24 (docs/137): '
                    'hotel_collection_slip_spotted uses CH4-B2-23 through hotel_porter:alarmed portraitBackgroundScene. '
                    'The approved record is preserved verbatim in docs/137_CH4_RETIRED_ARTWORK_LEDGER_20261124.json and its exact bytes at '
                    + RETIRED_DIR + '/CH4-B2-16-v01.png (SHA-256 ' + prev['sha256'] + ').')
    art['portraits']['hotel_porter:alarmed']['portraitBackgroundScene'] = 'grand_bellevue/service_passage'
    # C1 / C2 presentation records.
    for k, rec in no_image_records(ch).items():
        cat, lk = k.split(':', 1)
        target = art['scenes'] if cat == 'main_scene' else art['portraits']
        assert lk not in target, k
        target[lk] = rec
    # Ring brief, corrected to the approved inscription reveal (status stays not-started).
    for side, b in RING_BRIEF.items():
        art['items']['wedding_ring_lot31'][side].update(b)
    for rel, v in ((CHAPTER, ch), (ARTWORK, art), (PREVIEW, pv)):
        (root / rel).write_text(json.dumps(v, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    smoke = root / 'tools/storyboard/qa-smoke.mjs'
    old = "171+14+8+7+2*2+52,'shared art catalog retains history, Chapter 4 item placeholders and fifty-two owner-selected Chapter 4 records'"
    new = "171+14+8+7+2*2+51+9,'shared art catalog retains history, Chapter 4 item placeholders, fifty-one active owner-selected Chapter 4 images (CH4-B2-16 retired) and nine approved no-image presentation records (docs/137)'"
    text = smoke.read_text(encoding='utf-8')
    assert old in text, 'qa-smoke catalog assertion changed; update the docs/137 edit set'
    smoke.write_text(text.replace(old, new), encoding='utf-8')
    if ledger:
        entries = []
        for k, d in RETIRE.items():
            rec = copy.deepcopy(registry_record(base_art, k))
            pkey = preview_key(k)
            entry = {'id': d['id'], 'title': d['title'], 'registryKey': pkey, 'replacementId': d['replacementId'],
                     'replacementKey': preview_key(d['replacement']), 'nodes': [n for n, _, _ in d['poseChanges']] or ['hotel_collection_slip_spotted'],
                     'continuity': d['continuity'], 'originalRecordVerbatim': rec}
            if k.startswith('portrait:'):
                entry.update({'activeRecordKept': True, 'publicPreview': pv['images'][pkey]})
            else:
                entry.update({'activeRecordKept': False, 'mechanism': d['mechanism'], 'publicPreviewAtRetirement': prev,
                              'preservedBytes': {'path': RETIRED_DIR + '/CH4-B2-16-v01.png', 'sha256': prev['sha256']}})
            entries.append(entry)
        LEDGER.write_text(json.dumps({
            'schema': 'out-of-order-retired-artwork-ledger-v1', 'decision': DECISION, 'decisionDate': '2026-11-24',
            'canonicalBase': CANON_BASE,
            'policy': 'Retirement removes an approved image from ACTIVE Chapter 4 coverage only. Approval history (docs/103, docs/127-136), source review packages, exact bytes and SHA-256 values are preserved; nothing is regenerated, recolored or re-encoded.',
            'retired': entries}, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    return removed, prev


GAME_HARNESS = r'''
const fs=require('fs'),path=require('path');const [,,dir,sb,out]=process.argv;
const {convert}=require(path.join(dir,'convert.js'));
const rd=(p)=>JSON.parse(fs.readFileSync(path.join(sb,p),'utf8'));
const manifest=rd('story/storyboard-manifest.json');const chapters={};
manifest.chapters.forEach(c=>{chapters[c.id]=rd(path.join('story',c.file));delete chapters[c.id].development;});
const settings=JSON.parse(fs.readFileSync(path.join(dir,'runtime-settings.json'),'utf8'));delete settings.pendingArtBindings;
const ids=new Set();JSON.stringify(chapters['chapter-04'],(k,v)=>{if((k==='speaker'||k==='who')&&typeof v==='string')ids.add(v);return v;});
ids.forEach(id=>{if(!settings.cast[id])settings.cast[id]={name:id.toUpperCase()};});
const r=convert({manifest:{chapters:manifest.chapters.map(c=>({id:c.id,title:c.title,file:c.file,status:c.status}))},chapters,items:rd('story/items.draft.json'),artwork:rd('story/artwork.draft.json'),settings,bindings:[]},{mode:'preview'});
const n=r.story?r.story.chapters['chapter-04'].nodes:{};const res={};
Object.keys(n).forEach(id=>{const x=n[id];if(x.mode!=='dialogue')return;const p=r.story.assets.portraits[x.speaker]||{};
res[id]={speaker:x.speaker,pose:x.pose||p.pose,background:x.backdrop||p.background};});
fs.writeFileSync(out,JSON.stringify({ok:!!r.story,errors:r.errors.length,warnings:r.warnings,story:r.story?JSON.stringify(r.story).length:0,nodes:res,chapters123:r.story?JSON.stringify(['prologue-00','chapter-01','chapter-02','chapter-03'].map(c=>r.story.chapters[c])):null}));
'''


def tree_copy(dest, base):
    """A throwaway tree: CANON_BASE (git archive) or this working tree's story/tools/assets."""
    dest.mkdir(parents=True)
    if base:
        tar = subprocess.Popen(['git', 'archive', CANON_BASE], cwd=ROOT, stdout=subprocess.PIPE)
        subprocess.check_call(['tar', '-x', '-C', str(dest)], stdin=tar.stdout)
        tar.wait()
    else:
        for d in ('story', 'tools', 'assets'):
            shutil.copytree(ROOT / d, dest / d, ignore=shutil.ignore_patterns('__pycache__', '.DS_Store'))
        shutil.copy2(ROOT / 'index.html', dest / 'index.html')


def game_check(game):
    check = Checks()
    tmp = Path(tempfile.mkdtemp(prefix='ch4-consolidation-gamecheck-'))
    base_dir, now_dir = tmp / 'base', tmp / 'now'
    tree_copy(base_dir, True)
    tree_copy(now_dir, False)
    res = {'canonicalBase': CANON_BASE}

    def run(cmd, cwd):
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
        return p.returncode, (p.stdout + p.stderr).strip().splitlines()[-2:]
    for name, cmd in (('check-canon', ['node', 'tools/sync/check-canon.mjs']), ('qa-smoke', ['node', 'tools/storyboard/qa-smoke.mjs'])):
        for label, d in (('CANON_BASE', base_dir), ('applied', now_dir)):
            rc, tail = run(cmd, d)
            res['%s:%s' % (name, label)] = {'exit': rc, 'tail': tail}
            check(rc == 0, '%s passes on the %s tree' % (name, label), tail)

    # check-canon must reject every way a no-image record could quietly become an art slot.
    def mutate(label, fn, expect):
        m = tmp / ('mut-' + label)
        shutil.copytree(now_dir, m)
        art = rd(ARTWORK, m)
        pv = rd(PREVIEW, m)
        fn(art, pv)
        (m / ARTWORK).write_text(json.dumps(art, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        (m / PREVIEW).write_text(json.dumps(pv, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        rc, tail = run(['node', 'tools/sync/check-canon.mjs'], m)
        out = subprocess.run(['node', 'tools/sync/check-canon.mjs'], cwd=m, capture_output=True, text=True).stdout
        check(rc != 0 and expect in out, 'check-canon rejects mutant: ' + label, tail)
        shutil.rmtree(m)
    vo, tl = 'bridal_door_ai:neutral', 'grand_bellevue/arrival'
    mutate('voice-only with an assetPath', lambda a, p: a['portraits'][vo].update(assetPath='art/portraits/x.png'), 'must not name an assetPath')
    mutate('text-led scene with a preview', lambda a, p: p['images'].__setitem__('scenes:' + tl, p['images']['scenes:grand_bellevue/lobby']), 'must not have a public preview')
    mutate('text-led scene with a nested background', lambda a, p: a['scenes'][tl].update(portraitBackground={'kind': 'portrait-background', 'status': 'not-started'}), 'must not nest art')
    mutate('voice-only demoted to not-started', lambda a, p: a['portraits'][vo].update(status='not-started'), 'status must be approved')
    mutate('voice-only on a scene record', lambda a, p: a['scenes'][tl].update(format='voice-only'), 'is not valid here')
    mutate('unknown format', lambda a, p: a['portraits'][vo].update(format='silent'), 'is not valid here')

    if game:
        g = Path(game)
        hdir = tmp / 'game'
        hdir.mkdir()
        for src, dst in (('tools/story-import/convert.js', 'convert.js'), ('story/runtime-settings.json', 'runtime-settings.json')):
            (hdir / dst).write_bytes(git('show', 'origin/main:' + src, cwd=g))
        gsha = git('rev-parse', 'origin/main', cwd=g).decode().strip()
        (hdir / 'h.js').write_text(GAME_HARNESS)
        outs = {}
        for label, d in (('base', base_dir), ('applied', now_dir)):
            o = hdir / (label + '.json')
            subprocess.check_call(['node', str(hdir / 'h.js'), str(hdir), str(d), str(o)])
            outs[label] = json.loads(o.read_text())
        b, p = outs['base']['nodes'], outs['applied']['nodes']
        moved = {n: [b[n], p[n]] for n in b if b[n] != p[n]}
        expect_nodes = [n for d in RETIRE.values() for n, _, _ in d['poseChanges']] + ['hotel_collection_slip_spotted'] + [n for n, _, _, _ in REUSE_POSES]
        check(sorted(moved) == sorted(expect_nodes), 'Game importer (main %s): exactly the 9 remapped nodes resolve differently' % gsha[:7], sorted(moved))
        check(p['hotel_collection_slip_spotted']['background'] == 'grand_bellevue/service_passage' and p['hotel_chair_stapler_caught']['background'] == 'grand_bellevue/lobby',
              'Game importer: slip_spotted -> service-passage background; stapler_caught keeps the lobby background')
        check(outs['base']['chapters123'] == outs['applied']['chapters123'], 'Game importer: Prologue + Chapters 1-3 runtime output byte-identical before/after')
        check(outs['base']['ok'] and outs['applied']['ok'], 'Game importer converts both trees in preview mode')
        res['game'] = {'repo': 'InterstellarHarvest/out-of-order', 'commit': gsha, 'changedNodes': moved,
                       'baseWarnings': len(outs['base']['warnings']), 'appliedWarnings': len(outs['applied']['warnings']),
                       'note': 'Game main predates the C1/C2 capability, so no-image records still import as DEV PLACEHOLDERs (preview) there, exactly as the missing records did before.'}
    shutil.rmtree(tmp)
    res['checks'] = check.items
    res['result'] = 'PASS' if not check.failed else 'FAIL'
    v = json.loads(VERIFY.read_text(encoding='utf-8'))
    v.pop('dryRun', None)
    v['gameCheck'] = res
    VERIFY.write_text(json.dumps(v, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    print('game-check: %d passed, %d failed' % (len(check.items) - len(check.failed), len(check.failed)))
    return 0 if not check.failed else 1


def evidence():
    """Review sheets in docs/137_evidence/, composited 1:1 from the selected bytes (never resampled)."""
    from PIL import ImageDraw
    out_dir = DOCS / '137_evidence'
    out_dir.mkdir(exist_ok=True)
    chapter, art, preview = load_canon()
    plan = json.loads(PLAN.read_text(encoding='utf-8'))['requirements']
    sel = lambda key: Image.open(live_file(plan[key])).convert('RGBA')
    pad, bar = 8, 18
    ink, paper, accent = (236, 230, 214, 255), (32, 34, 38, 255), (214, 92, 92, 255)

    def sheet(panels, cols, name):
        w = max(p.width for p, _ in panels)
        h = max(p.height for p, _ in panels)
        rows = (len(panels) + cols - 1) // cols
        im = Image.new('RGBA', (cols * w + (cols + 1) * pad, rows * (h + bar) + (rows + 1) * pad), paper)
        d = ImageDraw.Draw(im)
        for i, (p, label) in enumerate(panels):
            x, y = pad + (i % cols) * (w + pad), pad + (i // cols) * (h + bar + pad)
            d.text((x, y + 3), label, fill=accent if label.startswith('RETIRE') else ink)
            im.paste(p, (x, y + bar))
        im.convert('RGB').save(out_dir / name, optimize=True)

    def over(fg_key, bg_key):
        b = sel(bg_key)
        b.alpha_composite(sel(fg_key))
        return b
    for k, d in RETIRE.items():
        nid = (d['poseChanges'][0][0] if d['poseChanges'] else 'hotel_collection_slip_spotted')
        n = chapter['nodes'][nid]
        if k.startswith('portrait:'):
            bg = 'portrait_background:' + n['scene']
            before, after = over(k, bg), over(d['replacement'], bg)
        else:
            before, after = over('portrait:hotel_porter:alarmed', k), over('portrait:hotel_porter:alarmed', d['replacement'])
        sheet([(before, 'RETIRE %s  (%s, now)' % (d['id'], nid)), (after, 'USE %s  (proposed)' % d['replacementId'])], 2,
              'retire-%s.png' % d['id'].lower())
    sheet([(over('portrait:hotel_bride:hopeful', 'portrait_background:grand_bellevue/lobby'), 'RETIRE CH4-B2-28 hopeful (ring_show_bride)'),
           (over('portrait:hotel_bride:determined', 'portrait_background:grand_bellevue/lobby'), 'USE CH4-B2-26 determined (no ring in hand)'),
           (over('portrait:hotel_bride:grateful', 'portrait_background:grand_bellevue/lobby'), 'KEEP CH4-B2-29 grateful: ONLY after the ring is handed over'),
           (over('portrait:hotel_bride:helpful', 'portrait_background:grand_bellevue/lobby'), 'KEEP CH4-B2-30 helpful (ring_bathroom)')], 2, 'bride-ring-continuity.png')
    sheet([(sel('main_scene:grand_bellevue/ballroom'), 'CH4-05 ballroom -> wedding_entry, refreshment_table'),
           (sel('main_scene:grand_bellevue/service_passage'), 'CH4-B2-19 service passage -> bridal_corridor'),
           (sel('main_scene:grand_bellevue/boiler_access'), 'CH4-B2-13 boiler access: KEPT (main scene)'),
           (sel('main_scene:grand_bellevue/lobby'), 'CH4-01 lobby: podium + framed piano lot (why CH4-02 is lobby-only)')], 2, 'reuse-sources.png')
    sheet([(sel('portrait_background:grand_bellevue/lobby'), 'CH4-02 lobby background: podium + piano lot, NOT the ballroom'),
           (sel('main_scene:grand_bellevue/ballroom'), 'CH4-05 ballroom: needs its own closer background (CH4-NEW-18)')], 2, 'ballroom-background-exception.png')
    bench = Image.open(ROOT / 'assets/selected/art/scenes/biology_park/central_flower.png').convert('RGBA')
    panels = [(bench, 'CHAPTER 2 BENCHMARK central_flower: %d colours' % colors(bench))]
    for aid in ('CH4-01', 'CH4-04', 'CH4-05'):
        im = sel(REFINE[aid])
        panels.append((im, 'REFINE %s: %d colours (approved composition kept)' % (aid, colors(im))))
    sheet(panels, 2, 'refinement-scenes.png')
    peer = sel('portrait_background:grand_bellevue/service_passage')
    panels = [(peer, 'PEER CH4-B2-23: %d colours' % colors(peer))]
    for aid in ('CH4-B2-03', 'CH4-B2-11'):
        im = sel(REFINE[aid])
        panels.append((im, 'REFINE %s: %d colours (smooth gradients)' % (aid, colors(im))))
    sheet(panels, 3, 'refinement-backgrounds.png')
    for p in sorted(out_dir.glob('*.png')):
        print(p.relative_to(ROOT), p.stat().st_size)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'verify'
    if cmd == 'evidence':
        evidence()
    elif cmd == 'build':
        build()
    elif cmd == 'apply':
        apply_edits(ROOT, ledger=True)
        print('applied; now run build, verify and game-check')
    elif cmd == 'verify':
        sys.exit(verify())
    elif cmd == 'game-check':
        g = sys.argv[sys.argv.index('--game') + 1] if '--game' in sys.argv else None
        sys.exit(game_check(g))
    else:
        sys.exit(__doc__)
