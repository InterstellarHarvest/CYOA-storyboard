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
| Story nodes | 118 |
| Nodes reachable from Chapter 4 entry (including SHOW/USE and d6 outcomes) | 118/118 |
| Broken choice/SHOW/USE/d6 targets | 0 |
| Layout unique placements | 118/118 |
| Fatal endings | 4: FINAL OCCUPANCY, FOLDED FOR CONVENIENCE, PRESSED AND STEAMED, MADE TO MEASURE |
| Explicit nonfatal park exits | 3: service yard, bridal corridor, bridal lavatory |
| Missing-item and exhausted dialogue actions | Gated in WIP JSON; future game UI must display disabled/greyed with explanatory subtitles |
| `PERMANENTLY SATISFIED` incorrectly reused in Ch4 death headings | 0 |

The attached JSON is an **approved narrative draft for review and art prompts**, not evidence of finished gameplay or artwork integration. Some item/used-action cards are currently hidden by the review engine instead of shown disabled; preserving the desired future behavior is a separate gameplay/UI integration requirement.

## Remaining editorial stops — Chapter 4 is not yet complete

These seven nodes are still explicitly marked `DRAFT REVIEW STOP` and require one-node-at-a-time story review with Nate:

1. `wip_auctioneer_question` — auctioneer conversation.
2. `wip_freight_lift` — service-side lift continuation.
3. `wip_stall_crane_ride` — survive the raised stall into upper salvage.
4. `wip_stall_wedding_walk` — wedding-corridor walk.
5. `wip_ballroom_flood` — displaced water entering ballroom.
6. `wip_ballroom_water_off` — whole-hotel water shutoff consequence.
7. `wip_auctioneer_dispute` — Lot 14 safety-equipment auction challenge.

**Suggested next review:** the stall-crane upper-salvage survival continuation, then the two flood branches; each should reconnect to existing restroom obstacles or a nonfatal park exit without dragging the player into wedding duties.

## Canonical source paths

- `story/chapters/chapter-04.wip.json`
- `story/chapter-04.wip-review-layout.json`
- `docs/124_CH4_EXIT_TO_PARK_AND_CH5_PARK_SEED_20261121.md` — park/Chapter 5 boundary rule

No Chapter 5 scenes or artwork were generated in this batch.
