# Out of Order — Chapter 4 bridal privacy and seashell publication audit

**Checkpoint:** November 21, 2026 (US Eastern)  
**Owner:** Nate — Chapter 4 Narrative PMO  
**Working title:** *Something Old, Something Sold*  
**Review URL:** https://interstellarharvest.github.io/CYOA-storyboard/tools/storyboard/?review=ch4-wip

## Scope of this approved batch

- Resolved the former `wip_bride_find_wedding_organizer`: organizer unlocks only the outer dressing room and leaves. The protagonist is seeking a toilet, not volunteering to repair the wedding.
- Resolved bride-authorized staff corridor and wedding-side service corridor into brief, practical route junctions with staff-lavatory, organizer, and parkward options.
- Added bridal privacy AI door inspection, conditional definition-of-bride dialogue, false bridal claim, emergency override denial, and ring-show denial. Ring possession never opens the door. Item SHOW stays visible but locked with explanatory subtitle when absent in future engine UI.
- Added gown Focus A inspection: AutoFit motor, tensioned neckline, explicit manufacturer's warning. Separate inspection of the manual-slack tab sets `ch4_autofit_release_located` and grants a **nonstacking +1** to the hidden dress d6.
- Dress attempt: hidden d6 base **1–4 fatal, 5–6 survive** (`need: 5`), with inspected manual slack **1–3 fatal, 4–6 survive**. Fourth fatal ending is `MADE TO MEASURE`, with a single unique death-popup title and narrative. Artwork is **not generated**.
- Survival grants provisional bride registration, a **pending** fee, and bathroom-door entry. Temporary gown is not a six-slot inventory item.
- The bridal lavatory has **only three seashells on a counter** and no toilet. Inspect/attempt/use instructions, single missing-toilet complaint, circular second-attempt certification, assessment appeal, and clean exit are now authored. The owner removed the proposed extra demonstration request.
- All living exits described in this batch head **toward the park**. Fried animals and dangerous prototype security plants belong exclusively to **opening Chapter 5**; none are foreshadowed in Chapter 4 exits.
- Added the previously approved ring inscription inspection to actual gameplay links, setting `ch4_ring_inscription_read` for the short optional groom callback. The ring remains an item until explicitly handed away.

## Editorial and navigation QA

| Check | Result |
| --- | --- |
| Story nodes | 120 |
| Nodes reachable from Chapter 4 entry (including SHOW/USE and d6 outcomes) | 120/120 |
| Broken choice/SHOW/USE/d6 targets | 0 |
| Layout unique placements | 120/120 |
| Fatal endings | 4: FINAL OCCUPANCY, FOLDED FOR CONVENIENCE, PRESSED AND STEAMED, MADE TO MEASURE |
| Explicit nonfatal park exits | 3: service yard, bridal corridor, bridal lavatory |
| Missing-item and exhausted dialogue actions | Gated in WIP JSON; future game UI must display disabled/greyed with explanatory subtitles |
| `PERMANENTLY SATISFIED` incorrectly reused in Ch4 death headings | 0 |

The attached JSON is an **approved narrative draft for review and art prompts**, not evidence of finished gameplay or artwork integration. Some item/used-action cards are currently hidden by the review engine instead of shown disabled; preserving the desired future behavior is a separate gameplay/UI integration requirement.

## Remaining editorial stops — Chapter 4 is not yet complete

This one node is still explicitly marked `DRAFT REVIEW STOP` and requires one-node-at-a-time story review with Nate:

1. `wip_freight_lift` — service-side lift continuation.

**Suggested next review:** the freight lift. It should reconnect to existing restroom obstacles or a nonfatal park exit without dragging the player into wedding duties.

### Approved subsequent node — Upper Salvage

`wip_stall_crane_ride` is retired and replaced with `hotel_upper_salvage_arrival` plus `hotel_upper_salvage_clerk_directions`. There are exactly three choices: **B** ask the salvage clerk about installed toilets (connect to `hotel_staff_lavatory_storage`); **C** take the maintenance hatch (connect to `hotel_pipe_tunnel`); **D** take the service stairs to the loading dock (connect to `hotel_maintenance_dock_exit`). No manifest-inspection puzzle or extra roll. The previously approved crane d6 and fatal outcome remain unchanged. The clerk's short floor-plan joke is published.

### Approved subsequent node — Dignified Walk

`wip_stall_wedding_walk` is retired and replaced by `hotel_stall_public_corridor_walk`, which keeps the player fully dressed and has exactly three choices: **A** staff lavatory, **B** collection stairs, **C** nonfatal service-yard park exit. A guest has one brief joke. No wedding obligation, dice, item, or additional fee.

### Approved subsequent node — Flooded Public Corridor

`wip_flooded_hotel_corridor` is retired and replaced by `hotel_flooded_public_corridor`. An attendant briefly reclassifies the flood as a temporary water feature; the player can **A** reach the staff lavatory, **B** use the maintenance hatch, or **C** leave via the service-yard park exit. Set `ch4_flooded_corridor_reached`. No extra dice, wedding task, or inventory.

### Approved subsequent node — Whole-Hotel Water Shutoff

`wip_hotel_water_off` is retired and replaced by `hotel_water_outage_confirmation`. The engineer distinguishes mechanically operational toilets from hydraulically operable ones and notes that access is a separate issue. The player may **A** try the sold staff lavatory, **B** the engineers' lavatory beyond the boiler, or **C** leave through the loading dock toward the park. All existing water-off flags persist, and `ch4_hotel_water_outage_confirmed` is set. No new dice, item, or wedding involvement.

### Approved subsequent node — Auctioneer's Restroom Inventory

`wip_auctioneer_question` is retired and replaced by `hotel_auctioneer_restroom_inventory`. The auctioneer mistakes an urgent request to use a toilet for a live product demonstration; the player may **A** enter the still-open public restroom, **B** try the staff lavatory, or **C** take the service corridor to the loading dock. The initial bride–father argument has been trimmed to a single bathroom-door sale joke. Set `ch4_auctioneer_restroom_inventory_asked`. No new dice, item, or fee.

### Approved subsequent node — Lot 14 Cataloguing Recall

`wip_auctioneer_dispute` is retired and replaced with `hotel_auctioneer_lot14_dispute` and `hotel_auctioneer_lot14_recall`. The receipt's old bride-objection clause is replaced with a cataloguing-error requirement. A conditional **CITE LOT 14 RECEIPT** action requires `ch4_knows_wheel_lot_14` from Focus A inspection and recalls the plumbing wheel; other choices return to Commodore Bixby or use the maintenance controls. The recalled wheel is a temporary story prop and returns through the existing plumber repair node. No new dice, fees, or wedding roles.

## Subsequent owner directive — wedding is superficial only

Nate requested an additional trim after bridal and seashell publication. Previously approved mechanical consequences, items, and bathroom routes remain. All surviving dialogue choices must prioritize finding a toilet, escaping a hazard, or leaving the hotel. Explicit groom-search tasks, wedding reunion, explaining hotel problems to the family, and ceremony logistics were removed or rewritten. Optional ring return to the bride remains because it grants useful staff-corridor permission. The organizer is only a keyholder to the private bathroom. Wedding guests, cake, flowers, and auctioneer family ties are incidental scenery and occasional punchlines.

A direct parkward exit now appears at the loading-dock foreman, sharing the existing service-yard end node rather than creating an additional unique ending.

## Canonical source paths

- `story/chapters/chapter-04.wip.json`
- `story/chapter-04.wip-review-layout.json`
- `docs/124_CH4_EXIT_TO_PARK_AND_CH5_PARK_SEED_20261121.md` — park/Chapter 5 boundary rule

No Chapter 5 scenes or artwork were generated in this batch.
