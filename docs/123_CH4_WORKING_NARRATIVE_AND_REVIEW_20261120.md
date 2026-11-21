# Out of Order — Chapter 4 working narrative and public review

**Status:** Story collaboration in progress. This is a review-only checkpoint, not a narrative lock, art approval, or gameplay integration request.

## Creative foundation

- Working title: **Something Old, Something Sold**.
- Place: the Grand Bellevue Hotel beside the People's Pavilion.
- Incident: a wedding is disrupted as the bride's auctioneer father sells hotel furnishings to pay for it; salvage crews collect purchased fixtures during the event.
- Tone: human personalities, physical comedy, absurd escalation, and occasional dangerous decisions, with the protagonist still needing a bathroom.
- Approved as working material by Nate: all seven Chapter 3 transitions, three differentiated entrances, the public/service/wedding opening choices, the Public A1 plumber introduction, the A1-A valve outcomes, the last-stall crane incident, the porter protest, three short Lot 53 dialogue branches, Lot 31 chair auction, four conditional item interactions, Focus A, both ring-retrieval outcomes, and the trimmed ring-in-pocket scene with its three successor choices. Approval remains revisable as later branches are written.
- **2026-11-21 checkpoint:** the bride's ring recognition dialogue, optional ring READ/engraving, all four reply branches, and the complete Collection Stairs and Lot 58 staff-lavatory incident batch are approved. The actual missing-groom encounter and wedding-organizer/private-lavatory scenes remain **editorial stops** pending review.

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
5. Inventory: SHOW/USE/READ are gated by actual possession. Old items are never silently restored. **Nate-approved future UI requirement:** on Lot 31, display all four conditional SHOW/USE cards even when the item is absent, locked with a small REQUIRES / NOT IN INVENTORY subtitle. The current game engine hides unavailable item actions, so this is *not* an implemented feature of the WIP JSON. The public review JSON records it as an engine-presentation requirement.
   - The **Collection Stairs** Staff Pass action has the same visible-but-locked requirement if the player lacks `pavilion_temporary_staff_pass`. This is an engine integration requirement; the current review JSON retains `if.has` gating, not a simulated disabled-card UI. Story-state alternatives (such as a previously escorted chair) stay context-gated.
6. Checks: hidden d6 only when fully authored with pass/fail destinations. The risk marker is never added merely because a choice sounds dangerous. Approved checks: bare valve d6 ≥4; Red Stapler upholstery tampering d6 ≥4 to go **unnoticed** (both outcomes open the seam); careful ring retrieval d6 ≥4, with +1 if vegetation inspection was allowed, +2 if examiner inspection paused the auction, and automatic success when the seam is already open.
7. Fatal outcomes: require a real ending, complete lead-in, popup title and narrative, art requirement, and RETRY/CHECKPOINT/EXIT. Chapter 4 has **no approved deaths yet**.
8. Retain prior flags, infections/antidotes, inventory, NOTES, and Chapter 3 exit-specific continuity.

## Public A1 / auction approval status (2026-11-21)

- **Approved — A1-A valve wrench:** d6 ≥4. Success braces the bare shaft long enough for a temporary seal; failure makes the flood worse. Two context-specific next choices on each outcome.
- **Approved — success → last stall:** player enters and reaches for their belt, but a crane raises the stall walls/door/latch before they unzip. The fully dressed player is exposed to wedding guests. They can protest, grab the rising stall (unwritten continuation), or walk calmly past guests (unwritten continuation).
- **Approved — protest → Lot 53:** the porter claims only the stall was lifted; the auctioneer mistakes the complaint for an offer. Three short spoken branches: (A) self-cleaning product demonstrator comic misunderstanding and flag; (B) bride ally, pointing to the blue delivery ledger and required countersignature; (C) red carbon **Lot 53 Dispute Ticket** with temporary inspection-hold value. They converge at Lot 31.
- **Approved — Lot 31:** auction of the bridal suite chair last seen carried by the missing groom. A silver wedding ring, bound by pale blue ribbon, glints in the upholstery. Three normal directions: examine, ask bride about groom (editorial stop), or follow the chair to collection (editorial stop).
- **Approved — four item-dependent chair actions:** SHOW Acting Director of Vegetation credential (botanical inspection); SHOW Temporary Examiner Badge (inspection pause); USE Red Swangline Stapler (unseen d6 roll, failed stealth damages upholstery but still opens seam); SHOW Temporary Staff Pass (one authorized collection escort). All require possession; none is consumed here.
- **Approved — Focus A ring retrieval:** detailed upholstery/tack/ribbon close-up, with three player choices: carefully extract, involve the bride (editorial stop), or follow to collection (editorial stop). Successful extraction (or already-open seam) grants `wedding_ring_lot31`. Failed extraction drops the ring inside the chair, requiring pursuit to collection; it is not a death or permanent loss.
- **Approved — ring in pocket:** concise second-person narrative: a thread on cuff, ring securely acquired, bride asks a porter about missing groom, porter reassures her only that the chair is accounted for. Three next cards: SHOW ring to bride (requires possession), keep ring and seek groom, keep ring and look for another restroom. The latter two outcomes remain DRAFT REVIEW STOP.
- **Approved — show bride dialogue:** she recognizes the silver band and blue ribbon, asks where it came from, rebukes her father's attempt to auction the 'matching accessory', and asks whether the player has seen the missing groom. Merely SHOWing the ring **does not** transfer it. All four next reply branches (five contextual cards) and their immediate exchanges have been reviewed and approved:
  1. **Help find the groom / reveal he's behind the boilers:** show only the unlocated `NO, BUT I'LL HELP YOU FIND HIM.` or known `YES. HE'S HIDING BEHIND THE BOILERS.` card based on `ch4_groom_located`. The former gets the service-passage/collection-stairs lead and `ch4_groom_search_lead`; the latter lets the bride know his location (`ch4_bride_knows_groom_location`) and asks you to bring him back. No roll; ring stays in inventory. Future search/reunion scenes remain editorial stops.
  2. **Explicit ring handover:** `PLACE THE RING IN THE BRIDE'S HAND.` is an item-gated action. The approved grateful exchange includes auctioneer jokes and a request to tell the groom she wants him back. Only this branch **takes** `wedding_ring_lot31`, sets `ch4_ring_returned_to_bride`, grants `ch4_bride_ally`, and authorizes staff corridors with `ch4_bride_service_permission`. Does not automatically find the groom; next passage is an editorial stop.
  3. **Request a bathroom:** the bride recognizes the stall incident, explains that a private lavatory lies beyond the bridal dressing room upstairs, and directs the player to the wedding organizer in the ballroom for its key. Sets `ch4_knows_bridal_dressing_lavatory` and `ch4_knows_organizer_has_lavatory_key`. No immediate lavatory access or staff authorization; ring stays in inventory, no roll. Wedding-organizer scene is not yet authored.
  4. **Mention `AS IS, WHERE IS`:** show only if `ch4_ring_inscription_read` is true, after READ in inventory. The bride recognizes her nervous groom's auction joke, laughs, understands that he still intends to marry her, and asks for reassurance to be passed along. Sets `ch4_bride_reassured_by_inscription` and `ch4_groom_fears_auctioneer`; keeps the ring, no roll. **Approved future groom line:** `SHE SAID SHE HASN'T CHANGED HER MIND. AS IS, WHERE IS.` should reassure him **without a persuasion roll** when this flag is present; the groom interaction itself has not been authored/approved yet.
- **Approved — inventory READ ring:** ring description reveals the engraved `AS IS, WHERE IS.` after READ, followed by the auction-terms/wedding-vow joke. No dice or consumption. Item read mark and `ch4_ring_inscription_read` state persist for later conditional dialogue; no art is approved or generated.
- **Approved — Collection Stairs:** after the bride's unlocated-groom clue, short Narrative B passage features two porters struggling with Lot 31, a crushed boutonnière, `ATTACHED GENTLEMAN — NOT INCLUDED` delivery slip, suspicious cough at BOILER ACCESS, and a SOLD sticker covering the staff-lavatory arrow. All four successor cards are approved:
  1. **Ask the porters about the groom:** short dialogue confirms he entered the boiler passage to avoid the bride's father. The groom was briefly classified as an accessory; the porters apologize for the crate, then insist the chair is purchased. Set `ch4_groom_trail_confirmed`; no roll, ring retained. Converge at the yet-unwritten groom encounter.
  2. **Slip past the chair:** hidden d6 ≥4 to enter unnoticed, set `ch4_boiler_entry_unnoticed`. On 1–3, the porters catch the player still attached to the chair's upholstery, pin a **NOT INCLUDED** tag on the coat, and usher the player through the same door; set `ch4_boiler_entry_spotted` and `ch4_not_included_tag` for possible future callbacks. Both outcomes retain the ring, reach the boiler route, and are **not deaths**. No modifiers are approved for this check.
  3. **SHOW Temporary Staff Pass:** item gated, unconsumed, no roll. If `ch4_lot31_staff_escort` was set, porters recognize the earlier visiting inspector; otherwise they ask why a People's Pavilion pass applies and conclude all hotel staff are temporary. In either variant the porter writes **TEMPORARY** under NAME and **OFFICIAL** under PURPOSE on his clipboard, granting `ch4_maintenance_access_authorized`. Then converge on the boiler route.
  4. **Investigate sold staff lavatory:** a wedding assistant is storing approximately three hundred wedding favors on and around the only toilet. The auctioneer sold the room as extra wedding storage, though the fixture was sold separately as **Lot 58**. The assistant points to a private lavatory beyond the bridal dressing room, with its key held by the wedding organizer in the ballroom. Set `ch4_staff_lavatory_sold_for_storage`, `ch4_knows_bridal_dressing_lavatory`, and `ch4_knows_organizer_has_lavatory_key`. Player can ask for the boxes to be moved, seek the organizer, or return to the groom route. Reuse a shorter recognition if this private-lavatory clue was already learned elsewhere; the current entry path only gives the clue here.
- **Approved — staff lavatory / Lot 58 continuation:** the helpful assistant moves boxes; a red ribbon and tag reveal `LOT 58 — STAFF TOILET`, already sold for collection after the ceremony and not to be tested. Set `ch4_lot58_toilet_sold_separately`. Player can defy the tag, seek the organizer, or return to the boilers. Defiance reveals **bureaucratic Catch-22**, not the discarded physical shipping clamp or wedding-bells interruption: Temporary Use Permit needs a verified flush, but testing requires the very permit. The assistant offers an exception form for the wedding organizer to sign. Set `ch4_lot58_permit_paradox`; no roll, no inventory consumption, and the toilet remains unused. Two next cards: ask where the organizer is, or leave paperwork and return to the groom route.
- **Unapproved proposals retained in WIP — A1-B / maintenance:** a real passage behind sinks, two-lever shutoff, nervous groom and empty ring box, service stair, different water outcomes.
- **Unapproved proposals retained in WIP — A1-C / Lot 14:** Eddie, Commodore Bixby, receipt, future bridge tour or rubber-band-ball trade.
- **Unapproved proposal retained in WIP — A1-D / Facilities Key:** optional `wc_key` cabinet shortcut.

State keys remain provisional until integration. New approved items for WIP review: `lot_53_dispute_ticket` and `wedding_ring_lot31` (no artwork). The ring inscription's **bride exchange and future groom reassurance line are approved**, but the groom scene and route connections still require review. Other A1 state keys from the original proposal remain unchanged.

## Route-development queue

- **Next to review:** write the shared missing-groom encounter at `wip_collection_boiler_groom_encounter`, accounting for the porter clue, quiet/spotted d6 outcomes, NOT INCLUDED tag, staff authorization, and return from the lavatory. Or select the wedding organizer at `wip_bride_find_wedding_organizer`. Do not silently connect to the existing unapproved `hotel_groom_pipe_hideout` proposal until that dialogue is reviewed with Nate. The groom-known, bride ally/staff-corridor, and inscription-reassurance continuations remain editorial stops.
- Public A1-A success → crane stall → porter protest → auction → ring is approved through pass/fail; crane-ride, calm wedding walk, bride-groom question, bride-ring involvement, and chair-collection continuations still need review.
- Other plumber successors A1-B, A1-C, and A1-D remain unapproved narrative proposals; review before calling them locked story.
- Public A2: auctioneer question → unwritten.
- Public A3: help bride → unwritten.
- Service S1/S2/S3: restroom passage, cake rescue, freight lift → unwritten.
- Wedding W1/W2: missing groom, service slip → unwritten.

Any `wip_*` node in the JSON is an explicit **editorial stop**, not an ending or playable consequence. The current working draft has **89 nodes, 26 editorial stops, and four authored hidden d6 checks**. Replace every editorial stop and audit all checks, item gating, inventory, and routes before narrative lock or artwork generation.

## Review cadence

After meaningful owner-approved incident batches, update this JSON and the route queue. Keep the review URL current. Do not mark scenes approved for artwork or integrate into the game until the authored routes and owner approval warrant those actions.
