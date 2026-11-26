# Chapter 4 artwork — closeout and gameplay handoff

**Ruling (Nate / Artwork PMO, 2026-11-26):** Chapter 4 artwork is **complete for gameplay integration**. No further artwork is to be generated, and R1 is not resumed.

**What this document is:** a narrow final reconciliation of canonical `main` at [`8e388e2`](https://github.com/InterstellarHarvest/CYOA-storyboard/commit/8e388e21035004d79280417985ddc98631621e6e) (B2-19, PR #43) against the approved consolidation (docs/137). It does not repeat that audit.

**Files:**
- Verifier: `python3 tools/sync/verify-ch4-art-closeout.py --game <out-of-order checkout>` — **PASS, 164 checks**, read-only.
- Report: [152_CH4_ARTWORK_CLOSEOUT_VERIFICATION_20261126.json](152_CH4_ARTWORK_CLOSEOUT_VERIFICATION_20261126.json).
- Node-by-node map: [152_CH4_NODE_ART_MAP_20261126.tsv](152_CH4_NODE_ART_MAP_20261126.tsv).

## 1. Verdict

**Ready for the Gameplay PMO.**
- All 63 active primary requirements are approved and selected.
- All 120 nodes resolve to approved art, an authorized reuse, or an authorized no-image presentation.
- No artwork gap exists inside the consolidated Chapter 4 scope.

| | Item | Effect |
|---|---|---|
| **Integration blockers** (§7A) | WP-1, WP-2 and WP-3, the three park-bound endings, one Focus echo and one unmarked 100% check. These are engine/importer work in the game repository. | Chapter 4 cannot be played until they are done. They are the integration task itself, not artwork. |
| **Open owner decision** (§8) | D-1: the Temporary Staff Pass. Chapter 4 requires it, but no chapter grants it, and its art records are archived pre-reboot prompts. | Does not block starting integration. It must be decided before final route QA. |
| **Optional visual polish** (§6) | The six R1 refinement candidates. | DEFERRED — NOT BLOCKING INTEGRATION. |

## 2. Active coverage: 63 of 63

| Category | Retained | New | Total | Contract |
|---|---:|---:|---:|---|
| Main scenes | 12 | 4 (NEW-01–04) | 16 | 314×206 opaque |
| Speaker portraits | 21 | 2 (NEW-05, NEW-06) | 23 | 564×278 transparent |
| Closer backgrounds | 7 | 1 (NEW-18, renderer exception) | 8 | 564×278 opaque |
| Focus A | 5 | 3 (NEW-07–09) | 8 | 564×278 opaque |
| Inventory slot / inspect | — | 2 + 2 (NEW-10–13) | 4 | 96×96 transparent / 565×451 opaque |
| Fatal aftermaths | — | 4 (NEW-14–17) | 4 | 314×206 opaque |
| **Total** | **45** | **18** | **63** | |

**Per-requirement checks:** for every one of the 63, the verifier confirms:
- the record is `approved`;
- the selected file exists at its contract size and alpha;
- file SHA-256 = preview SHA-256 = the first SHA in the approval note;
- for the 45 retained images, the hash also equals docs/137's;
- the hash appears in its approval record (docs/128–151).

**Not counted as active, and kept distinct:**

| Class | Count | Status |
|---|---:|---|
| Reuse (docs/137 C3) | 6 | Every source is approved. Four scene keys have no record and are registered as `reused` at integration (§7B): `wedding_entry`→CH4-05, `refreshment_table`→CH4-05, `bridal_corridor`→CH4-B2-19, `freight_lift`→CH4-NEW-03. Bixby "commanding" is remapped to "delighted". The refreshment-table background already resolves to NEW-18 through the pose's `portraitBackgroundScene`. |
| Authorized no-image (C1/C2) | 14 | Three `text-led` scenes, six `voice-only` speakers, and five closer backgrounds that are unnecessary because the only speakers there are voice-only. |
| Archived approved records | 7 | Six retired portraits keep their approval, preview and bytes, and no node uses them. CH4-B2-16 is held in the retired ledger and `retired-selections/` (`e396db07…`). |
| Preserved supplemental references | 33 files | 28 conditional, 2 INSPECT, 2 historical design masters and 1 retired selection (§4–§5). None is a canonical selection. |

## 3. Node-to-art mapping (120 nodes)

The TSV lists each node's main scene, portrait, background, Focus, ending art, popup and conditional references, resolved from current canon with the game importer's background rule.

| Layer | Resolved |
|---|---|
| Main scene | 120: 109 approved, 6 on the four C3 reuse keys, 5 text-led (C1) |
| Dialogue (64) | 49 approved portraits on approved backgrounds; 15 voice-only (C2) with no portrait aperture |
| Focus (8) | 8 approved Focus A images |
| Fatal endings (4) | 4 approved aftermaths; all 4 popups `owner-approved` |
| Unresolved | **0** |

**Inventory:** every item Chapter 4 references has slot and inspect art, except the staff pass (§8).

| Item | Granted by | Art |
|---|---|---|
| `wedding_ring_lot31` | Chapter 4 | approved (docs/149) |
| `lot_53_dispute_ticket` | Chapter 4 | approved (docs/149) |
| `red_stapler` | Chapter 1 | integrated |
| `rubber_band_ball` | Chapter 1 | integrated |
| `acting_director_badge` | Chapter 2 | integrated |
| `expo_examiner_badge` | Prologue | integrated |
| `wc_key` | Prologue | reused |

## 4. Conditional references and timing

All are **APPROVED / PRESERVED** references, byte-exact under `tools/prologue-art-lab/assets/approved/`. They carry no keys, Focus IDs, flags or bindings.
- The selected master stays the default.
- Show a reference only through conditions and text beats that already exist, never through a node-entry flag alone.

| Family (record) | Reference → base | Node(s) | Timing |
|---|---|---|---|
| Chair and ring (docs/132) | `CH4-B2-24-open` → Focus `auction_floor/chair_armrest` | `hotel_chair_stapler_stealth`, `hotel_chair_ring_focus` | `ch4_chair_seam_open`: seam open, ring still caught, not yet in inventory |
| | `CH4-B2-25-slipped` → Focus `collection_stairs/chair_armrest` | `hotel_ring_slips`, `hotel_collection_ring_focus` | `ch4_ring_slipped_inside_chair`: ring below the brace, unreachable by fingers |
| | `CH4-B2-25-recovered` → same | `hotel_collection_ring_porter_recovery`, `hotel_collection_ring_stapler_recovery` | after the explicit recovery gives the ring |
| Staff lavatory (docs/135) | `CH4-B2-37-cleared` (scene), `CH4-B2-41-cleared` (background) | `hotel_staff_lavatory_move_boxes` | boxes moved |
| | `CH4-B2-37-permit`, `CH4-B2-41-permit` | `hotel_staff_lavatory_temporary_use_permit` | permit issued |
| Boiler (docs/136) | `CH4-B2-42/47-relieved` | `hotel_boiler_pressure_relieved` | needle in GREEN; outer passage open; inner door and maintenance gate closed |
| | `CH4-B2-42/47-inspection-hold` | `hotel_boiler_dispute_hold` | DO NOT OPERATE tag; RED pressure; lavatory chained |
| | `CH4-B2-42/47-staff-access` | `hotel_boiler_staff_access` | maintenance gate open; RED pressure. Reachable only with the staff pass (§8). |
| Ballroom threshold, on NEW-18 (docs/142) | `wheel-mounted` | `hotel_commodore_bixby` | before the hand-off |
| | `wheel-removed` | `hotel_bixby_emergency` | after he presses the wheel into your hands. Its bytes equal the NEW-18 base, by design. |
| | `rubber-band-fender` | `hotel_bixby_trade` | trade made; the ball stays with him |
| | `water-emerging` | the three Bixby nodes | from the authored "water creeps out beneath the ballroom door"; combinable with the other three |
| Public corridor (docs/144) | `CH4-NEW-04-public-corridor-flood-v04` | `hotel_flooded_public_corridor` | flooded route only; the dry master is the default (`hotel_stall_public_corridor_walk`) |
| Bridal privacy (docs/145) | `CH4-NEW-07-focus-provisional-v02` | `hotel_bridal_door_focus` | the later authorization condition; the locked Focus is the default |
| AutoFit gown (docs/147) | `CH4-NEW-08-manual-slack-revealed-v01` | `hotel_bridal_gown_motor` | inside the node, before the lining is replaced. The node sets `ch4_autofit_release_located`. Never persist an open-lining state. |
| **Restroom, B2-18** (docs/150) | `restroom-active-leak-main` → CH4-04 | `hotel_restroom_plumber` | after the burst |
| | `restroom-active-leak-close` → CH4-B2-03 | `hotel_restroom_plumber`, `hotel_wheel_buyer_lead` | the same burst at the closer camera; buyer lead while the leak is uncontained |
| | `restroom-contained-main` → CH4-04 | `hotel_wheel_return`, `hotel_key_master_cabinet`, `hotel_valve_braced` | contained **and** braced. The braced narration explains the temporary seal; braced-main stays UNSELECTED. |
| | `restroom-flood-onset-main` → CH4-04 | `hotel_valve_flood` | first surge only, before the narrated floating-basket beat |
| | `restroom-stall-lifting-main` → CH4-04 | `hotel_stall_lot_claimed`, `hotel_stall_crane_success` | the empty enclosure lifts on four cables; the toilet stays on the floor |
| | (decision) CH4-B2-03, unchanged | `hotel_stall_porter_protest` | **reuse the approved conversation background**; no post-lift variant (docs/151) |
| **Lobby and Lot 61, B2-19** (docs/151) | `lobby-doors-removed` → CH4-01 | `hotel_auctioneer_arrival` onward | doors stay absent once the workmen remove them during the sale, and on every later lobby visit. The removal itself is narrated. |
| | `lot61-open` → CH4-01 | `hotel_lot61_pod_auction`, `hotel_lot61_pod_declined` | from when the pod is wheeled out and its door opens; while it departs on decline |
| | `lot61-packed` → CH4-01 | `hotel_lot61_pod_escaped` | **only after the authored folding finishes**. The node sets `ch4_pod_survived_packing` on entry, so the flag alone must not reveal the case. |
| | (unchanged) FOLDED FOR CONVENIENCE | `fatal_lot61_folded` | the unsuccessful outcome keeps its fatal illustration; the escape never borrows its shoe or bulge |

**B2-18/B2-19 provenance:** these were derived from the **current approved masters**, not from R1-refined ones, which supersedes docs/138's sequencing note. If an R1 replacement is ever selected, re-derive or re-check them before they are shown over it.

## 5. INSPECT — presentation-only

The docs/145 dual-view handoff is preserved unchanged.
- **The two square INSPECT images** (565×451):
  - `CH4-NEW-07-inspect-locked-v03` `b571f321…`
  - `CH4-NEW-07-inspect-provisional-v03` `fa4d465c…`
  - Both are in `approved/inspection-references/chapter-04/b2-12/`; the superseded v01 design masters stay in `visual-design-masters/`.
  - They belong to a contextual **INSPECT** action on `hotel_bridal_door_focus`. That action is not an inventory item.
- **Opening and closing the overlay must not:**
  - call `Rules.step`;
  - consume a choice;
  - set or clear flags;
  - grant or remove an item;
  - reset dialogue;
  - change eligibility or save data.
- **Closing:** X or Escape returns to the same Focus node and choice set.
- **Validation:** validate in Chromium and Firefox per docs/145. If choices break, keep the existing 564×278 Focus behavior and leave the overlay disabled.
- **Item inspect images** (ticket and ring, docs/149) use the normal inventory inspector. Viewing the ring's inspect image must not set `ch4_ring_inscription_read`; only the authored READ does.

## 6. R1 — DEFERRED, NOT BLOCKING INTEGRATION

The approved originals stay selected. Nothing is replaced, and no further R1 work is authorized.

| Candidate | Selected key | Approved SHA-256 (unchanged) |
|---|---|---|
| CH4-01 lobby | `scenes:grand_bellevue/lobby` | `582bcd51de937e5fe124160a8beb74b4ee469f52eeb6d9d0d38b918cfb0d6be0` |
| CH4-04 restroom | `scenes:grand_bellevue/restroom` | `83cf1f0df4d130f24c53c931cae83fd92abef8fdc7e8f80359c5657ce051ce06` |
| CH4-05 ballroom | `scenes:grand_bellevue/ballroom` | `76a290b0f7419927440e0635638183b89a7844b03bc9cec065bc08827dec713c` |
| CH4-B2-03 restroom background | `scenes:grand_bellevue/restroom#portraitBackground` | `77325aca0d3c61d5b6d1980232fb11fa55156454a26659c6887c4d726a82c377` |
| CH4-B2-11 loading-dock background | `scenes:grand_bellevue/loading_dock#portraitBackground` | `27f69050b10d3e10121f7f2c2860db1418504b00d3848daabde420485b9bcc1f` |
| CH4-03 auctioneer (showman) | `portraits:hotel_auctioneer:showman` | `231baf25ffd00511144693927354e73f42cae4f052964a9db0a99323689a0d78` |

**Preserved evidence** (unselected; never registered):
- **Auctioneer native study and five-environment assessment:** `art/ch4-r1-auctioneer-review-20261126` @ `6e59549`.
  - The study (`f345448c…`) failed its artistic gate.
  - The assessment made no redraws and recommends retaining CH4-01 and CH4-05.
- **Restroom material pilot 01:** `art/ch4-r1-restroom-material-pilot01-review-20261126` @ `e06c93f`.
  - The pilot (`89b6e60d…`) failed its gate on bowl volume and brass modeling.
  - Painting stopped there; B2-11 was never started.

**If R1 is ever reopened:** both gates name the method, an experienced pixel illustrator working from a blank native canvas.

## 7. Remaining engine / importer work (not implemented here)

Confirmed against canon and by running game `main` (`c7a2d3d`, unchanged since docs/140) read-only. The importer and the validator reproduce the docs/140 set exactly.

### A. Blockers: the engine or importer must change

| ID | Gap | Count | docs/140 direction |
|---|---|---:|---|
| WP-1 | Two-segment Focus A ids (`bridal_privacy_panel`, `autofit_gown`, `three_seashells`) | 3 | Accept or normalise the canon ids; do not rename them |
| WP-2 | Text runs with their own `if` | 17 | Generic conditional runs, deterministic in saves, NOTES and replay |
| WP-3 | `deathPopup`/`endingArt` on the four fatal nodes | 4 | Route through `death-presentations.export.json`. All four popups are owner-approved with approved art; the exporter skips Chapter 4 only while it is `notForGameplay`. |
| — | Park-bound endings with no card (`hotel_service_park_exit`, `hotel_bridal_corridor_park_exit`, `hotel_bridal_lavatory_park_exit`) | 3 | Chapter 5 hand-off or the agreed ending presentation |
| — | USE `red_stapler` `say` echo on Focus node `hotel_collection_ring_focus` | 1 | Engine allowance or the agreed presentation |
| — | `focus_free_ring_careful` can reach 100% unmarked | 1 | Mark it `certain`, or cap it, per Gameplay PMO |

### B. Routine integration steps (required, but not blockers)

1. **C3 reuse:** register the four reuse scene keys as `reused` (§2). No new art.
2. **Bindings:**
   - copy the 63 active Chapter 4 selections to their suggested `art/` paths (no node uses the 6 archived portraits);
   - set `assetPath` and item `slotArt`/`inspectArt`;
   - raise the records to `integrated`.
3. **Cast names:** add display names for 21 Chapter 4 speakers and voices to the game's `runtime-settings.json`.
4. **Conditional-state dispatch:** add a generic way to show the §4 references from existing conditions and text beats. Without it, the selected defaults display: legal, but the lobby doors, Lot 61 and the restroom states would not change.
5. **INSPECT overlay:** the presentation-only engine contract in §5.
6. **Lift `notForGameplay`** and update the manifest status, currently "narrative approved · artwork pending · not in game", once the Gameplay PMO accepts the import. Both are left untouched here.

## 8. Open owner decision D-1: Temporary Staff Pass

**The gap:**
- `pavilion_temporary_staff_pass` gates two approved SHOW choices: `collection_show_staff_pass` at `hotel_collection_stairs` and `boiler_show_staff_pass` at `hotel_boiler_pressure_intro`.
- No chapter in the manifest grants it. The rebooted Chapter 3 has no Provisional Employment node, and docs/106 left the grant as an open owner decision.
- Its slot and inspect records are **archived pre-reboot prompts** (`not-started`). No art exists.
- Five approved-art nodes are reachable **only** with it:
  - `hotel_collection_staff_pass`, `hotel_collection_staff_pass_first`, `hotel_collection_staff_pass_recognized` and `hotel_collection_staff_pass_authorized`;
  - `hotel_boiler_staff_access`, which also carries the B2-08 staff-access references.

**Options** (nothing is generated or substituted until Nate chooses):
- **(a) A chapter grants the pass.** Two inventory images become a genuine new requirement: a 96×96 slot and a 565×451 inspect.
- **(b) The pass stays ungrantable.** The two cards show locked (`REQUIRES: TEMPORARY STAFF PASS — NOT IN INVENTORY`, docs/123), no art is needed, and the five nodes remain unreachable authored content.

This is outside the docs/137 scope of 63 images. It does not block starting integration.

> **Addendum, 2026-11-26: D-1 decided, option (a).**
> - **Decision:** Nate approved granting the existing `pavilion_temporary_staff_pass` at the Chapter 3 reboot node `unauthorized_presenter`, immediately after TEMPORARY PRESENTER APPOINTED.
> - **Record:** [docs/153](153_CH3_TEMPORARY_STAFF_PASS_GRANT_20261126.md). It was held until Nate approved the two item images. Both v01 images were then approved and registered (PR #45).
> - **What follows:** the 96×96 slot and 565×451 inspect images become a genuine new item requirement outside the 63. The five Chapter 4 nodes and both SHOW choices are unchanged.
>
> **Correction, same date.** §7A omitted one integration blocker that docs/126 §6 item 1 already recorded: the **Chapter 3 → 4 exit hand-off**.
> - Chapter 4's `hotel_entry_dispatch` routes only on `ch3_exit_route`.
> - None of the seven Chapter 3 reboot endings writes that flag.
> - All seven end in BEGIN AGAIN.
> - Until the Gameplay PMO wires the hand-off, no route enters Chapter 4. The above is unchanged otherwise.

## 9. Hash integrity

- **All 214 selections** match their recorded SHA-256.
- **All 69 Chapter 4 selections** are byte-identical to their immutable review-source blobs, compared by git object identity at each recorded source commit and path.
- **All 33 preserved Chapter 4 reference files** are present exactly, with no extras, and match the hashes in their approval records.
- **No Chapter 4 selected or reference PNG** has ever been modified in place on `main`.
- **The R1 failed studies** are intact at their branch heads.
- **Draft PR #32** is unchanged at `f320e63`.

## 10. Boundaries

**Added:**
- this document;
- its verification JSON and node-map TSV;
- the read-only verifier.

**Not changed:**
- narrative, choices, flags, items or gameplay;
- the engine or the game repository;
- registry records, selections, images or references;
- the manifest status, deployment or draft PR #32.
