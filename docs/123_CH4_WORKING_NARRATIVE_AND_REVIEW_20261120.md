# Out of Order — Chapter 4 working narrative and public review

**Status:** Story collaboration in progress. This is a review-only checkpoint, not a narrative lock, art approval, or gameplay integration request.

## Creative foundation

- Working title: **Something Old, Something Sold**.
- Place: the Grand Bellevue Hotel beside the People's Pavilion.
- Incident: a wedding is disrupted as the bride's auctioneer father sells hotel furnishings to pay for it; salvage crews collect purchased fixtures during the event.
- Tone: human personalities, physical comedy, absurd escalation, and occasional dangerous decisions, with the protagonist still needing a bathroom.
- Approved as working material by Nate: all seven Chapter 3 transitions, three differentiated entrances, the public/service/wedding opening choices, the Public A1 plumber introduction, the A1-A valve outcomes, the last-stall crane incident, the porter protest, three short Lot 53 dialogue branches, Lot 31 chair auction, four conditional item interactions, Focus A, both ring-retrieval outcomes, and the trimmed ring-in-pocket scene with its three successor choices. Approval remains revisable as later branches are written.
- **2026-11-21 checkpoint:** the bride's ring recognition dialogue, optional ring READ/engraving, all four next dialogue choices, and their immediate replies/consequences are approved. The missing-groom and private-bathroom follow-through scenes remain **editorial stops** pending review.

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
- **Unapproved proposals retained in WIP — A1-B / maintenance:** a real passage behind sinks, two-lever shutoff, nervous groom and empty ring box, service stair, different water outcomes.
- **Unapproved proposals retained in WIP — A1-C / Lot 14:** Eddie, Commodore Bixby, receipt, future bridge tour or rubber-band-ball trade.
- **Unapproved proposal retained in WIP — A1-D / Facilities Key:** optional `wc_key` cabinet shortcut.

State keys remain provisional until integration. New approved items for WIP review: `lot_53_dispute_ticket` and `wedding_ring_lot31` (no artwork). The ring inscription's **bride exchange and future groom reassurance line are approved**, but the groom scene and route connections still require review. Other A1 state keys from the original proposal remain unchanged.

## Route-development queue

- **Next to review:** choose one downstream follow-through after the now-complete bride exchanges at `hotel_ring_show_bride`: service-passage groom search, groom-known return, staff-corridor permission, ballroom wedding organizer/private-lavatory lead, or the future groom payoff. Each ends in a clearly labeled `wip_bride_*` editorial stop for collaborative node-by-node development.
- Public A1-A success → crane stall → porter protest → auction → ring is approved through pass/fail; crane-ride, calm wedding walk, bride-groom question, bride-ring involvement, and chair-collection continuations still need review.
- Other plumber successors A1-B, A1-C, and A1-D remain unapproved narrative proposals; review before calling them locked story.
- Public A2: auctioneer question → unwritten.
- Public A3: help bride → unwritten.
- Service S1/S2/S3: restroom passage, cake rescue, freight lift → unwritten.
- Wedding W1/W2: missing groom, service slip → unwritten.

Any `wip_*` node in the JSON is an explicit **editorial stop**, not an ending or playable consequence. The current working draft has **78 nodes, 26 editorial stops, and three authored hidden d6 checks**. Replace every editorial stop and audit all checks, item gating, inventory, and routes before narrative lock or artwork generation.

## Review cadence

After meaningful owner-approved incident batches, update this JSON and the route queue. Keep the review URL current. Do not mark scenes approved for artwork or integrate into the game until the authored routes and owner approval warrant those actions.
