# Out of Order — Chapter 4 Narrative Closeout Audit

**Owner:** Nate, Chapter 4 Narrative PMO  
**Checkpoint:** November 21, 2026 (Eastern)  
**Chapter:** *Something Old, Something Sold*  
**Review:** https://interstellarharvest.github.io/CYOA-storyboard/tools/storyboard/?review=ch4-wip

## 1. Narrative state

**All previously identified Chapter 4 editorial stops are now authored and owner-approved.** The storyboard is the canonical *narrative and artwork-prompt source*, not proof that this chapter is playable or illustrated. No Chapter 5 narrative was created.

The protagonist is always seeking a working toilet. The wedding is incidental venue scenery; the bride, groom, organizer, and auctioneer are useful only when they offer bathroom directions, conditional access, an inventory interaction, a hazard, or a way out. No wedding-reunion, ceremony-management, or family-help quest remains.

## 2. Static route audit

| Test | Result |
| --- | --- |
| Chapter 4 nodes | **120** |
| Nodes reachable from chapter entry, counting SHOW/USE/d6 edges | **120/120** |
| Story targets missing | **0** |
| Review timeline placements | **120 unique / 120 nodes** |
| DRAFT REVIEW STOP / `wip_` nodes | **0** |
| Duplicate choice IDs | **0** (smart-door return hub now uses its own IDs) |
| Nonterminal nodes without any possible path to a safe exit | **0** |
| Explicit fatal endings | **4** |
| Distinct nonfatal park exits | **3** |
| Authored hidden d6 checks | **8** |

The seven Chapter 4 arrival variants are keyed to the seven intended Chapter 3 reboot endings. All Chapter 4 safe ends set `ch4_exit_park_approached` and a distinct `ch4_exit_route`. There is no early player-facing clue about fried animals or prototype security plants: those are exclusive to the opening of Chapter 5.

## 3. Fatal endings and odds

| Fatal title | Trigger and odds | Art/pop-up status |
| --- | --- | --- |
| **FINAL OCCUPANCY** | Lose crane grip: raw d6 **1–3 fatal**, 4–6 survive | Unique approved popup and aftermath brief; PNG pending |
| **FOLDED FOR CONVENIENCE** | Enter Lot 61 pod: raw d6 **1–4 fatal**, 5–6 survive | Unique approved popup and normal-sized compressed case + loose shoe brief; PNG pending |
| **PRESSED AND STEAMED** | Operate boiler pressure wheel: raw d6 **1–4 fatal**, 5–6 survive | Unique approved popup and one steaming jacket-and-trousers hanger brief; PNG pending |
| **MADE TO MEASURE** | Wear AutoFit bridal gown: raw d6 **1–4 fatal**, 5–6 survive; examining manual-slack tab adds **+1**, making raw 1–3 fatal | Unique approved popup and cinched gown + shoe brief; PNG pending |

Each fatal node has `end:true`, a unique `deathPopup.id`, exactly one incident-specific popup title and narrative, and an `artRef`. The inappropriate phrase `PERMANENTLY SATISFIED` does **not** appear in Chapter 4 popup titles or narrative.

## 4. Items and inspection dependencies

- **New Chapter 4 inventory:** `lot_53_dispute_ticket` and `wedding_ring_lot31` may be awarded on their approved branches. Both persist unless an explicit transfer removes the ring.
- **Prior-chapter items reused:** vegetation credential, Examiner Badge, Temporary Staff Pass, Red Stapler, and optional rubber band ball. Inspections and SHOW/USE actions retain their d6 consequences or shortcut effects.
- **Inspection-gated non-items:** reading the Lot 14 receipt sets `ch4_knows_wheel_lot_14`; citing it unlocks the short correction/recall path. Reading the wedding-ring inscription sets `ch4_ring_inscription_read`. The gown's separate manual-slack inspection sets `ch4_autofit_release_located` and grants only the approved nonstacking +1.
- **Not inventory items:** recalled shutoff wheel (temporary story prop), three seashells (remain on their counter), and the worn wedding gown (temporary costume).
- **Six inventory slots:** game integration must handle an award when all slots are occupied. This cannot be proven by the narrative graph alone; do not silently add a seventh slot or lose an awarded item.

Item and exhausted dialogue choices must remain visible but disabled, with **REQUIRES / NOT IN INVENTORY / ALREADY ATTEMPTED** subtitles, according to Nate's UI rule. The review/game engine may currently hide choices on failed `if` predicates; correcting this is a gameplay/UI integration task, not another narrative branch.

## 5. Key narrative route checks

- Public restroom → plumber/valve → crane stall, auction or dignified corridor exit.
- Crane success → Upper Salvage: clerk → staff lavatory, hatch → maintenance, stairs → dock. Crane failure → FINAL OCCUPANCY.
- Flooded public corridor → staff lavatory, maintenance, or parkward exit.
- Isolating all water → no hydraulic toilet function → staff, boiler, or exit. The earlier water-shutoff effects persist.
- Lot 14 dispute → receipt-gated safety-wheel recall; direct buyer and water-control alternatives remain. Correction connects to the existing plumber return, never a wedding task.
- Lot 31 chair and Collection Stairs → optional ring/stapler/pass routes, plus toilet directions and established hazards. Groom offers a concise bridal-lavatory clue, no escort or reunion.
- Bridal organizer → outer dressing-room door only; smart inner door, identification checks and ring refusal; gown inspection and optional fatal AutoFit attempt; survival reaches the empty three-seashell lavatory with pending registration fee.
- Seashell complaint, intuitive-use dead end, second attempt and appeal all converge on return options or the park-bound nonfatal departure. There is never a working toilet in this room.
- Freight lift W.C. is Warehouse Collection; choices reconnect to salvage clerk, maintenance, or parkward exit without replaying the crane-riding scene.

## 6. Outstanding integration checks — not missing narrative

1. **Chapter 3 → 4 exit flag handoff.** Chapter 4 expects `ch3_exit_route` set to one of seven reboot IDs. `story/chapters/chapter-03.reboot-candidate.json` contains those seven ending node IDs, but its endings do not themselves write `ch3_exit_route`; `story/chapters/chapter-03.draft.json` appears to retain earlier exit IDs. Gameplay PMO must confirm which Chapter 3 asset is shipped and set the required route flag before Chapter 4 dispatch. Do not change Chapter 3 narrative from this PMO.
2. **Inventory capacity and conditional card presentation.** Verify that six-slot inventory can accept the optional Chapter 4 ring/ticket via an explicit item replacement flow when full, and that locked/previously attempted action cards remain visible with subtitles.
3. **Chapter 4 → 5 transition.** Three nonfatal Chapter 4 endings physically head toward the park. The engine must map them into Chapter 5 when that chapter exists; no Chapter 5 wildlife/plant hazard reveal belongs in Chapter 4.
4. **Art asset production.** All artwork, portrait/scene/Focus A assets, and four fatal aftermath PNGs are pending the separate Chapter 4 Artwork PMO; approved text and art briefs must not be mistaken for completed images.
5. **Playable QA after integration.** This audit verifies JSON navigation and logic statically; hidden d6 probabilities, choice rendering, append-not-replace narration, text typing, CONTINUE pacing, conditionals, inventory, and the death popup must be exercised in the actual game engine later.

## 7. Handoff status

**Chapter 4 Narrative PMO node closure: complete, pending Nate's final review of the published storyboard and separate art/gameplay integration.** Do not invent more wedding business to fill space. The next creative PMOs may focus on Chapter 4 artwork and Chapter 5 park narrative, with the Chapter 5 seed constrained by `docs/124_CH4_EXIT_TO_PARK_AND_CH5_PARK_SEED_20261121.md`.

Canonical source paths:

- `story/chapters/chapter-04.wip.json`
- `story/chapter-04.wip-review-layout.json`
- `docs/124_CH4_EXIT_TO_PARK_AND_CH5_PARK_SEED_20261121.md`
- `docs/125_CH4_BRIDAL_PRIVACY_AND_SEASHELL_AUDIT_20261121.md`
