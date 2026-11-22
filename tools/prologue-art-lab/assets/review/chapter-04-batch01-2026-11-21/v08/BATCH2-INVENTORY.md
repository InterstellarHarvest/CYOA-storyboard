# Chapter 4 Batch 2 artwork inventory

Canonical main: `622ad879dfe187ff2683ae7072515ed740522243`. All **120/120 nodes** are covered by source references. This is planning, not art approval, registry insertion or new production work.

Explicit demands: **23 scene keys, 36 speaker/pose keys across 18 primary speakers, 15 dialogue locations, 8 Focus A keys, 4 new inventory-art records and 4 fatal aftermaths**. Three base scenes, the lobby portrait background and auctioneer showman have Batch 1 review candidates. Logical keys do not imply one new bitmap each: reuse and state layers may resolve several demands.

## Recommended first production group

**B2-01 — Public restroom dialogue and controls**: five units, all from explicit existing demands:

- `portrait` — `hotel_plumber:worried`. Nodes: `hotel_restroom_plumber`.
- `portrait` — `hotel_plumber_assistant:pleased`. Nodes: `hotel_wheel_buyer_lead`.
- `portrait_background` — `grand_bellevue/restroom`. Nodes: `hotel_restroom_plumber`, `hotel_wheel_buyer_lead`, `hotel_stall_porter_protest`.
- `focus_a` — `grand_bellevue/restroom/lot_14_receipt`. Nodes: `hotel_lot_receipt_study`.
- `focus_a` — `grand_bellevue/restroom/master_isolator`. Nodes: `hotel_key_master_cabinet`.

Use frozen v07 restroom geometry, the high-resolution plumber/assistant masters for character continuity, approved Pavilion portraits as the finish benchmark, and a separately authored closer 564×278 background. Do not enlarge tiny scene sprites into portraits. Lot14 receipt text and the red cabinet lever come directly from their Focus A nodes. This group establishes the next dialogue pair and actionable clues without changing any frozen environment. No Batch2 generation has started.

## Manageable follow-on groups

| Group | Scope | Primary units / state families |
|---|---|---|
| B2-01 | Public restroom dialogue and controls | 5 / 0 |
| B2-02 | Loading dock and service arrivals | 6 / 0 |
| B2-03 | Maintenance access and water isolation | 7 / 0 |
| B2-04 | Lot 31 and Collection Stairs | 7 / 1 |
| B2-05 | Bride and auction clerk | 5 / 0 |
| B2-06 | Auctioneer and porter expression extensions | 6 / 0 |
| B2-07 | Staff lavatory used as storage | 5 / 1 |
| B2-08 | Boiler pressure-test room | 6 / 1 |
| B2-09 | Commodore Bixby and the wheel | 4 / 0 |
| B2-10 | Upper salvage and freight lift | 6 / 0 |
| B2-11 | Public corridor, dry and flooded | 4 / 1 |
| B2-12 | Organizer and bridal privacy access | 6 / 1 |
| B2-13 | AutoFit gown inspection | 1 / 1 |
| B2-14 | Three-seashell lavatory | 4 / 0 |
| B2-15 | Hotel approaches and park-bound exits | 5 / 0 |
| B2-16 | Four fatal aftermaths | 4 / 0 |
| B2-17 | Ticket and ring inventory/inspection | 4 / 0 |
| B2-18 | Public restroom event-state derivatives | 0 / 5 |
| B2-19 | Lot 61 pod event states | 0 / 1 |

Larger families have explicit review slices rather than an oversized image dump: B2-04A is the five-unit passage/porter kit; B2-04B is the two Focus A views with ring-state variants. B2-18A covers leak/braced/flood; B2-18B covers door removal and stall lift/removal. Reuse/overlays may reduce PNG counts without dropping authored visual differences.

## Main scene keys

| Logical key | Group | Source nodes / status |
|---|---|---|
| `grand_bellevue/arrival` | B2-15 | 1 nodes; UNPRODUCED_LOGICAL_DEMAND; see JSON for every node ID |
| `grand_bellevue/loading_lane` | B2-02 | 1 nodes; UNPRODUCED_LOGICAL_DEMAND; see JSON for every node ID |
| `grand_bellevue/service_alley` | B2-02 | 2 nodes; UNPRODUCED_LOGICAL_DEMAND; see JSON for every node ID |
| `grand_bellevue/forecourt` | B2-15 | 2 nodes; UNPRODUCED_LOGICAL_DEMAND; see JSON for every node ID |
| `grand_bellevue/wedding_entry` | B2-15 | 1 nodes; UNPRODUCED_LOGICAL_DEMAND; see JSON for every node ID |
| `grand_bellevue/lobby` | BATCH1 | 29 nodes; FROZEN_PREFERRED_UNSELECTED; see JSON for every node ID |
| `grand_bellevue/loading_dock` | B2-02 | 3 nodes; UNPRODUCED_LOGICAL_DEMAND; see JSON for every node ID |
| `grand_bellevue/ballroom` | BATCH1 | 2 nodes; FROZEN_PREFERRED_UNSELECTED; see JSON for every node ID |
| `grand_bellevue/restroom` | BATCH1 | 12 nodes; FROZEN_PREFERRED_UNSELECTED; see JSON for every node ID |
| `grand_bellevue/maintenance` | B2-03 | 9 nodes; UNPRODUCED_LOGICAL_DEMAND; see JSON for every node ID |
| `grand_bellevue/service_stairs` | B2-02 | 1 nodes; UNPRODUCED_LOGICAL_DEMAND; see JSON for every node ID |
| `grand_bellevue/refreshment_table` | B2-09 | 3 nodes; UNPRODUCED_LOGICAL_DEMAND; see JSON for every node ID |
| `grand_bellevue/service_passage` | B2-04 | 15 nodes; UNPRODUCED_LOGICAL_DEMAND; see JSON for every node ID |
| `grand_bellevue/boiler_access` | B2-03 | 2 nodes; UNPRODUCED_LOGICAL_DEMAND; see JSON for every node ID |
| `grand_bellevue/staff_lavatory` | B2-07 | 3 nodes; UNPRODUCED_LOGICAL_DEMAND; see JSON for every node ID |
| `grand_bellevue/boiler_room` | B2-08 | 5 nodes; UNPRODUCED_LOGICAL_DEMAND; see JSON for every node ID |
| `grand_bellevue/bridal_dressing_room` | B2-12 | 14 nodes; UNPRODUCED_LOGICAL_DEMAND; see JSON for every node ID |
| `grand_bellevue/bridal_corridor` | B2-15 | 1 nodes; UNPRODUCED_LOGICAL_DEMAND; see JSON for every node ID |
| `grand_bellevue/courtyard` | B2-15 | 2 nodes; UNPRODUCED_LOGICAL_DEMAND; see JSON for every node ID |
| `grand_bellevue/bridal_lavatory` | B2-14 | 7 nodes; UNPRODUCED_LOGICAL_DEMAND; see JSON for every node ID |
| `grand_bellevue/upper_salvage` | B2-10 | 2 nodes; UNPRODUCED_LOGICAL_DEMAND; see JSON for every node ID |
| `grand_bellevue/public_corridor` | B2-11 | 2 nodes; UNPRODUCED_LOGICAL_DEMAND; see JSON for every node ID |
| `grand_bellevue/freight_lift` | B2-10 | 1 nodes; UNPRODUCED_LOGICAL_DEMAND; see JSON for every node ID |

## Exact portrait speaker/pose keys

| Logical key | Group | Source nodes / status |
|---|---|---|
| `hotel_auctioneer:showman` | BATCH1 | `hotel_auctioneer_arrival`, `hotel_auction_reopen_53`, `hotel_auction_chair_lot31`, `hotel_lot61_pod_auction`, `hotel_auctioneer_restroom_inventory`, `hotel_auctioneer_lot14_dispute` |
| `hotel_salvage_foreman:annoyed` | B2-02 | `hotel_service_foreman` |
| `hotel_wedding_organizer:urgent` | B2-12 | `hotel_wedding_arrival`, `hotel_bridal_organizer` |
| `hotel_plumber:worried` | B2-01 | `hotel_restroom_plumber` |
| `hotel_plumber_assistant:pleased` | B2-01 | `hotel_wheel_buyer_lead` |
| `hotel_commodore_bixby:delighted` | B2-09 | `hotel_commodore_bixby`, `hotel_bixby_trade` |
| `hotel_commodore_bixby:commanding` | B2-09 | `hotel_bixby_emergency` |
| `hotel_porter:businesslike` | B2-04 | `hotel_stall_porter_protest`, `hotel_collection_ring_stapler_recovery` |
| `hotel_auctioneer:delighted` | B2-06 | `hotel_auction_testimonial`, `hotel_lot61_pod_escaped` |
| `hotel_bride:determined` | B2-05 | `hotel_auction_bride_ally` |
| `hotel_auction_clerk:precise` | B2-05 | `hotel_auction_dispute_ticket`, `hotel_chair_examiner_inspection` |
| `hotel_porter:uncertain` | B2-04 | `hotel_chair_vegetation_inspection`, `hotel_collection_staff_pass_first` |
| `hotel_porter:alarmed` | B2-06 | `hotel_chair_stapler_caught`, `hotel_collection_slip_spotted` |
| `hotel_porter:practical` | B2-04 | `hotel_chair_staff_escort`, `hotel_chair_staff_escort_loading`, `hotel_collection_ring_porter_recovery`, `hotel_collection_porters_groom_clue`, `hotel_collection_staff_pass_authorized` |
| `hotel_bride:hopeful` | B2-05 | `hotel_ring_show_bride` |
| `hotel_bride:grateful` | B2-05 | `hotel_bride_ring_handover` |
| `hotel_bride:helpful` | B2-05 | `hotel_bride_ring_bathroom` |
| `hotel_porter:curious` | B2-06 | `hotel_collection_staff_pass` |
| `hotel_porter:relieved` | B2-06 | `hotel_collection_staff_pass_recognized` |
| `hotel_wedding_assistant:busy` | B2-07 | `hotel_staff_lavatory_storage` |
| `hotel_wedding_assistant:sympathetic` | B2-07 | `hotel_staff_lavatory_move_boxes` |
| `hotel_wedding_assistant:apologetic` | B2-07 | `hotel_staff_lavatory_temporary_use_permit` |
| `hotel_boiler_engineer:careful` | B2-08 | `hotel_boiler_pressure_intro` |
| `hotel_boiler_engineer:pleased` | B2-08 | `hotel_boiler_pressure_relieved` |
| `hotel_boiler_engineer:defeated` | B2-08 | `hotel_boiler_dispute_hold` |
| `hotel_boiler_engineer:practical` | B2-08 | `hotel_boiler_staff_access`, `hotel_water_outage_confirmation` |
| `hotel_groom:nervous` | B2-03 | `hotel_boiler_groom_encounter`, `hotel_groom_directions_to_lavatory`, `hotel_groom_leave_behind` |
| `hotel_groom:relieved` | B2-03 | `hotel_groom_show_ring` |
| `hotel_auctioneer:disappointed` | B2-06 | `hotel_lot61_pod_declined` |
| `bridal_door_ai:neutral` | B2-12 | `hotel_bridal_door_knock`, `hotel_bridal_criteria`, `hotel_bridal_false_claim`, `hotel_bridal_emergency_override`, `hotel_bridal_ring_argument`, `hotel_bridal_gown_camera` |
| `bathroom_ai:neutral` | B2-14 | `hotel_seashell_instructions`, `hotel_seashell_complaint`, `hotel_seashell_second_attempt`, `hotel_seashell_assessment_appeal` |
| `hotel_salvage_clerk:practical` | B2-10 | `hotel_upper_salvage_arrival`, `hotel_upper_salvage_clerk_directions` |
| `hotel_wedding_guest:curious` | B2-11 | `hotel_stall_public_corridor_walk` |
| `hotel_attendant:professional` | B2-11 | `hotel_flooded_public_corridor` |
| `hotel_auctioneer:bureaucratic` | B2-06 | `hotel_auctioneer_lot14_recall` |
| `hotel_lift_voice:neutral` | B2-10 | `hotel_freight_wc_misunderstanding` |

## Portrait-background contexts

| Logical key | Group | Source nodes / status |
|---|---|---|
| `grand_bellevue/lobby` | BATCH1 | 19 dialogue nodes; FROZEN_PREFERRED_UNSELECTED |
| `grand_bellevue/loading_dock` | B2-02 | 1 dialogue nodes; PLANNED_DIALOGUE_CONTEXT |
| `grand_bellevue/ballroom` | B2-12 | 2 dialogue nodes; PLANNED_DIALOGUE_CONTEXT |
| `grand_bellevue/restroom` | B2-01 | 3 dialogue nodes; PLANNED_DIALOGUE_CONTEXT |
| `grand_bellevue/refreshment_table` | B2-09 | 3 dialogue nodes; PLANNED_DIALOGUE_CONTEXT |
| `grand_bellevue/service_passage` | B2-04 | 9 dialogue nodes; PLANNED_DIALOGUE_CONTEXT |
| `grand_bellevue/boiler_access` | B2-03 | 1 dialogue nodes; PLANNED_DIALOGUE_CONTEXT |
| `grand_bellevue/staff_lavatory` | B2-07 | 3 dialogue nodes; PLANNED_DIALOGUE_CONTEXT |
| `grand_bellevue/boiler_room` | B2-08 | 4 dialogue nodes; PLANNED_DIALOGUE_CONTEXT |
| `grand_bellevue/maintenance` | B2-03 | 4 dialogue nodes; PLANNED_DIALOGUE_CONTEXT |
| `grand_bellevue/bridal_dressing_room` | B2-12 | 6 dialogue nodes; PLANNED_DIALOGUE_CONTEXT |
| `grand_bellevue/bridal_lavatory` | B2-14 | 4 dialogue nodes; PLANNED_DIALOGUE_CONTEXT |
| `grand_bellevue/upper_salvage` | B2-10 | 2 dialogue nodes; PLANNED_DIALOGUE_CONTEXT |
| `grand_bellevue/public_corridor` | B2-11 | 2 dialogue nodes; PLANNED_DIALOGUE_CONTEXT |
| `grand_bellevue/freight_lift` | B2-10 | 1 dialogue nodes; PLANNED_DIALOGUE_CONTEXT |

## Explicit Focus A close-ups

| Logical key | Group | Source nodes / status |
|---|---|---|
| `grand_bellevue/maintenance/water_isolator` | B2-03 | `hotel_isolator_panel` |
| `grand_bellevue/restroom/lot_14_receipt` | B2-01 | `hotel_lot_receipt_study` |
| `grand_bellevue/restroom/master_isolator` | B2-01 | `hotel_key_master_cabinet` |
| `grand_bellevue/auction_floor/chair_armrest` | B2-04 | `hotel_chair_ring_focus` |
| `grand_bellevue/collection_stairs/chair_armrest` | B2-04 | `hotel_collection_ring_focus` |
| `grand_bellevue/bridal_privacy_panel` | B2-12 | `hotel_bridal_door_focus` |
| `grand_bellevue/autofit_gown` | B2-13 | `hotel_bridal_gown_focus` |
| `grand_bellevue/three_seashells` | B2-14 | `hotel_seashell_inspect` |

## New inventory slot art

| Logical key | Group | Source nodes / status |
|---|---|---|
| `lot_53_dispute_ticket` | B2-17 | `hotel_auction_dispute_ticket`, `hotel_boiler_pressure_intro` |
| `wedding_ring_lot31` | B2-17 | `hotel_ring_retrieved`, `hotel_ring_in_pocket`, `hotel_ring_show_bride`, `hotel_bride_ring_handover`, `hotel_collection_ring_porter_recovery`, `hotel_collection_ring_stapler_recovery`, `hotel_collection_ring_in_pocket`, `hotel_boiler_groom_encounter`, `hotel_bridal_door_focus`, `hotel_bridal_emergency_override`, `hotel_ring_inspect_inscription`, `hotel_bridal_door_options` |

## New inspection art

| Logical key | Group | Source nodes / status |
|---|---|---|
| `lot_53_dispute_ticket` | B2-17 | `hotel_auction_dispute_ticket`, `hotel_boiler_pressure_intro` |
| `wedding_ring_lot31` | B2-17 | `hotel_ring_retrieved`, `hotel_ring_in_pocket`, `hotel_ring_show_bride`, `hotel_bride_ring_handover`, `hotel_collection_ring_porter_recovery`, `hotel_collection_ring_stapler_recovery`, `hotel_collection_ring_in_pocket`, `hotel_boiler_groom_encounter`, `hotel_bridal_door_focus`, `hotel_bridal_emergency_override`, `hotel_ring_inspect_inscription`, `hotel_bridal_door_options` |

## Fatal aftermath illustrations

| Logical key | Group | Source nodes / status |
|---|---|---|
| `grand_bellevue/final_occupancy` | B2-16 | `fatal_stall_final_occupancy` |
| `grand_bellevue/pressed_and_steamed` | B2-16 | `fatal_boiler_pressed_and_steamed` |
| `grand_bellevue/folded_for_convenience` | B2-16 | `fatal_lot61_folded` |
| `grand_bellevue/made_to_measure` | B2-16 | `fatal_bridal_made_to_measure` |

## Narrative-derived scene/focus state families

| Logical key | Group | Source nodes / status |
|---|---|---|
| `lobby_door_removal` | B2-18 | Removal in progress / doorless entrance. Separate state layer/file over the frozen lobby, not a cosmetic rewrite. Sources: `hotel_auctioneer_arrival`, `hotel_restroom_entry` |
| `restroom_active_leak` | B2-18 | Burst copper pipe, spray and airborne towels during the authored dialogue sequence; timing/state-layer representation is a production proposal. Sources: `hotel_restroom_plumber` |
| `restroom_braced_or_contained` | B2-18 | Braced/dripping or contained water states. Reuse compatible frames when no visible distinction is necessary. Sources: `hotel_valve_braced`, `hotel_wheel_return`, `hotel_key_master_cabinet` |
| `restroom_flood` | B2-18 | Flooded room, floating towel basket/Eddie and open service escape. Preserve entry-state geometry. Sources: `hotel_valve_flood` |
| `stall_lifting_and_removed` | B2-18 | Closed stall lifts through the ceiling; a later missing-enclosure view. No invented protagonist face or nudity. Sources: `hotel_stall_lot_claimed`, `hotel_stall_crane_success`, `hotel_stall_public_corridor_walk` |
| `chair_and_ring_states` | B2-04 | Focus/prop variants for loosened seam, caught ring, deeper slipped ring and recovered ring. Use the exact conditional flag text; do not mandate whole-room repaints. Sources: `hotel_chair_stapler_stealth`, `hotel_chair_ring_focus`, `hotel_ring_slips`, `hotel_collection_ring_focus`, `hotel_collection_ring_porter_recovery`, `hotel_collection_ring_stapler_recovery` |
| `staff_boxes_attempt` | B2-07 | Boxes and storage obstruction are authored. If a single base carries both pages, no extra bitmap is required. Sources: `hotel_staff_lavatory_storage`, `hotel_staff_lavatory_move_boxes` |
| `boiler_pressure_state` | B2-08 | Authored pressure test/relief can use gauge/steam overlays or reuse. No invented explosion state or global power failure. Sources: `hotel_boiler_pressure_intro`, `hotel_boiler_pressure_relieved` |
| `lot61_open_and_packed` | B2-19 | Open booth with actual toilet/warning; packing phase; escaped compact case. Fatal case/shoe artwork is a separate exact aftermath brief. Sources: `hotel_lot61_pod_auction`, `hotel_lot61_pod_escaped`, `hotel_lot61_pod_declined` |
| `bridal_privacy_status` | B2-12 | Locked bride-only panel versus green/provisional authorization and opened door. Prefer a state layer; ring never opens this door. Sources: `hotel_bridal_door_focus`, `hotel_bridal_autofit_survived` |
| `gown_motor_manual_slack` | B2-13 | Lining/motor/cables/manual-slack detail, safety clue and authorized fitting result. The motor inspection is narrative, not an invented ninth Focus A key; no new gown inventory item or player portrait is implied. Sources: `hotel_bridal_gown_focus`, `hotel_bridal_gown_motor`, `hotel_bridal_autofit_survived` |
| `public_corridor_flood` | B2-11 | Dry corridor versus flooded carpet/WET FLOOR sign. The authored scene key is shared. Sources: `hotel_stall_public_corridor_walk`, `hotel_flooded_public_corridor` |

## Evidence, reuse and unresolved mappings

- Every inventory row has exact node IDs and canonical evidence fields; state families additionally preserve the relevant narrative text. [Machine-readable inventory](BATCH2-INVENTORY.json), [120-node coverage table](BATCH2-NODE-COVERAGE.tsv), [canonical snapshots](evidence/canonical-sources.json).
- Portraits: 564×278 transparent foreground plus opaque location context; Focus A: established 564×278 convention. Inventory: existing registry explicitly specifies 96×96 slot and 565×451 inspection. Fatal aftermaths: existing project 314×206 standard; runtime/approval integration remains separate.
- AI/voice entries are not instructions to invent human bodies or unapproved hardware. Inline-only tags do not create new pose requirements.
- Existing ticket/ring art briefs are labelled draft/review-only in the registry. They are inventoried, not generated or silently approved. The ring engraving is already authored in the current narrative/item text; the older art note is stale.
- Do not make inventory art for the temporary wheel, seashells or gown. Reuse existing prior-chapter carried-item art where referenced.

- `hotel_second_porter`: Second existing porter identity can supply inline dialogue if a visible portrait is needed; pose remains unspecified.
- `hotel_service_foreman`: Likely alias of primary hotel_salvage_foreman; record the canonical tag mismatch rather than creating a second foreman.
- `autofit_system`: Machine voice can reuse gown/mechanism context; no invented human.

## Exact fatal art constraints

### FINAL OCCUPANCY

Owner-approved fatal lead-in and popup copy. Planned aftermath illustration only: broken porcelain toilet beneath the raised empty stall, scattered auction tags, perhaps an abandoned shoe. Do not show the player's face; no death art generated yet. Engine popup uses the standard RETRY/CHECKPOINT/EXIT controls when integrated.

### PRESSED AND STEAMED

Owner-approved fatal outcome with d6 1–4, no modifiers. Illustration ONLY: a steaming tuxedo jacket and matching trousers together on a single wire clothes hanger, as though freshly steam-pressed. Simple, immediately absurd visual. No boiler, gauge, clipboard, shoe, text, person, face, or gore in the artwork. No image generated yet. Popup has exactly one incident-specific heading and its narrative beside art; future engine has RETRY/CHECKPOINT/EXIT controls.

### FOLDED FOR CONVENIENCE

Owner-approved fatal lead-in/popup copy and specific art brief. Future aftermath image must show a NORMAL-SIZED BRIEFCASE-SIZED folded metallic case or compact suit-like case, with only SLIGHT asymmetrical bulging to imply the body compressed inside and ONE loose shoe lying off to the side as if it fell out. No oversized packing container, exposed corpse, gore, or visible face. The ordinary case size is essential to the joke. No artwork generated yet. Engine popup uses standard RETRY/CHECKPOINT/EXIT controls when integrated. Hidden d6 roll is fatal on 1–4, escape on 5–6; no modifiers approved.

### MADE TO MEASURE

Owner-approved fourth Chapter 4 fatal ending; art deferred. A white gown hanging on its stand, absurdly cinched bodice, one abandoned shoe beneath. No face, body details, gore, or complex machinery. One popup title and one narrative, no unrelated title.

## Guardrails

- No wedding-management errands or new story nodes.
- No Chapter5 fried-animal/security-plant imagery on Chapter4 exits.
- Three seashells remain on a bare counter; no toilet, button, hose or hidden fixture.
- Ring never unlocks bride-only door.
- Keep fatal images to their exact incident-specific briefs.
- Use approved Chapter2 environmental rendering and Pavilion/human NPC portrait finish; small scene NPCs remain simpler but recognizable.
