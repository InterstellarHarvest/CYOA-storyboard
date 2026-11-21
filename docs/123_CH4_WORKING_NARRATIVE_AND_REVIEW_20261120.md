# Out of Order — Chapter 4 working narrative and public review

**Status:** Story collaboration in progress. This is a review-only checkpoint, not a narrative lock, art approval, or gameplay integration request.

## Creative foundation

- Working title: **Something Old, Something Sold**.
- Place: the Grand Bellevue Hotel beside the People's Pavilion.
- Incident: a wedding is disrupted as the bride's auctioneer father sells hotel furnishings to pay for it; salvage crews collect purchased fixtures during the event.
- Tone: human personalities, physical comedy, absurd escalation, and occasional dangerous decisions, with the protagonist still needing a bathroom.
- Approved as working material by Nate: all seven Chapter 3 transitions, three differentiated entrances, the public/service/wedding first choices, and the initial Public A1 restroom/plumber sequence. Approval is revisable as later branches are written.
- **2026-11-21 expansion, awaiting Nate's review:** the four responses to the Public A1 plumber incident and their early consequences. These are available on the public WIP storyboard but are not yet narrative-approved.

## Source of truth

- Review story JSON: `story/chapters/chapter-04.wip.json`
- Public reader: `tools/storyboard/?review=ch4-wip`
- Prior chapter source: `story/chapters/chapter-03.reboot-candidate.json` (approved blob SHA `857ffdf1bc9432cf4bbbfd7819f5f430a06d9036`)

The review URL appends Chapter 4 to an **in-memory** manifest only; the public default manifest and archived Chapter 3 remain unchanged. The current game does not consume Chapter 4, and the approved Chapter 3 endings still use their existing terminal controls.

## Entry continuity

Require a future gameplay handoff to persist `ch3_exit_route` from the actual Chapter 3 ending. Seven distinct values:

| Chapter 3 ending | Chapter 4 first scene | Shared entry |
| --- | --- | --- |
| `locomotion_fail` | `entry_locomotion_fail` | Loading dock |
| `presenter_help_end` | `entry_presenter_help_end` | Loading dock |
| `paper_problem_end` | `entry_paper_problem_end` | Public lobby |
| `attendant_honest_end` | `entry_attendant_honest_end` | Loading dock |
| `door_dash_fail` | `entry_door_dash_fail` | Public lobby |
| `door_reverse_end` | `entry_door_reverse_end` | Wedding party |
| `backstage_exit` | `entry_backstage_exit` | Direct auctioneer scene |

The fastest-visitor ribbon is **cosmetic only**, not a new inventory item. No edits to Chapter 3 are authorized by this checkpoint.

## Presentation and gameplay contract

Carry forward established Chapter 1–3 conventions:

1. Narrative B: second person, present tense, dialogue-speed typing, paragraph pagination with CONTINUE when long, results append appropriately.
2. Dialogue: an active NPC portrait; spoken NPC pieces are unquoted; stage directions are plain descriptions. Secondary speakers use typed speaker pieces, as in the approved Chapter 3 reboot.
3. Choice cards: `kind: spoken` contains raw words without quote characters (the renderer adds them); `kind: action` is rendered in action ink; `kind: continue` controls pacing. Avoid repeated question banks and point-and-click exploration.
4. Focus A: reserve for meaningful object close-ups, not routine movement.
5. Inventory: SHOW/USE/READ are gated by actual possession. Old items are never silently restored; `wc_key` is an optional USE opportunity in the plumber incident, pending outcome design.
6. Checks: hidden d6 only when fully authored with pass/fail destinations. The risk marker is never added merely because a choice sounds dangerous. The proposed valve-wrench action uses d6 ≥4, with distinct nonfatal successes and failures.
7. Fatal outcomes: require a real ending, complete lead-in, popup title and narrative, art requirement, and RETRY/CHECKPOINT/EXIT. Chapter 4 has **no approved deaths yet**.
8. Retain prior flags, infections/antidotes, inventory, NOTES, and Chapter 3 exit-specific continuity.

## Public A1 expansion awaiting editorial approval (2026-11-21)

- **A1-A / valve wrench:** d6 ≥4. On success the player holds the bare shaft long enough for a temporary seal; on failure the flood worsens and washes toward the wedding. The choice has explicit `pass`, `fail`, and respective results; neither route is a fatal ending.
- **A1-B / maintenance:** a real passage behind the sinks; choices to inspect a two-lever shutoff (Focus A), meet a nervous groom with an empty ring box, or take a service stair to the foreman. Shutting water to the restrooms and shutting it off to the whole hotel have different flags and consequences.
- **A1-C / Lot 14:** Eddie names the wheel's buyer, Commodore Bixby. A receipt close-up exposes an auction exception favoring the bride. The Commodore can be persuaded to return the wheel at the cost of a future bridge-tour obligation, or traded a `rubber_band_ball` as a boat fender, consuming that item. Taking the dispute to the auctioneer remains unwritten.
- **A1-D / Facilities Key:** conditional `wc_key` USE opens the emergency isolation cabinet, shuts down the restrooms' water, and preserves the key. The signed-return tag from earlier chapters gets a quiet callback. No dice roll: existing inventory earns a certain advantage.
- **Shared punch line:** even successful repairs do not deliver a bathroom visit. Salvage workers remove the last toilet as Lot 53. Players can pursue that buyer or take a new service route; unfinished destinations remain marked DRAFT REVIEW STOP.

Proposed state keys (subject to integration audit): `ch4_restroom_leak` (`braced`, `uncontained`, `flooding`, `contained`), `ch4_restroom_water_off`, `ch4_hotel_water_off`, `ch4_plumber_helped`, `ch4_groom_located`, `ch4_knows_wheel_lot_14`, `ch4_valve_wheel_recovered`, `ch4_bixby_expects_bridge`, `ch4_bixby_fender_trade`, `ch4_master_key_recognized`.

## Route-development queue

- Public A1 restroom → plumber: introductory incident approved. The four successor routes are **proposed, not approved**, and need Nate's dialogue/choice review, followed by outcome work for their remaining editorial stops (Lot 53 buyer, ballroom flooding/shutoff, groom and ring, auctioneer dispute).
- Public A2: auctioneer question → unwritten.
- Public A3: help bride → unwritten.
- Service S1/S2/S3: restroom passage, cake rescue, freight lift → unwritten.
- Wedding W1/W2: missing groom, service slip → unwritten.

Any `wip_*` node in the JSON is an explicit **editorial stop**, not an ending or playable consequence. The current working draft has 44 nodes and 13 editorial stops, with one fully authored d6 check. Replace every editorial stop and audit all checks and routes before narrative lock or artwork generation. No new item definition is needed for this batch: both `wc_key` and `rubber_band_ball` already exist.

## Review cadence

After meaningful owner-approved incident batches, update this JSON and the route queue. Keep the review URL current. Do not mark scenes approved for artwork or integrate into the game until the authored routes and owner approval warrant those actions.
