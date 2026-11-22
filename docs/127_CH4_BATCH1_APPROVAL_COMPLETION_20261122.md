# Chapter 4 Batch 1 approved artwork completion

Nate approved all five assets **unchanged** on 2026-11-22. All five are **APPROVED and SELECTED**, not integrated. Immutable reviewed source: `3463e20bd366390008fa4f71c087ed5f334f3a31` on `art/ch4-batch01-review-20261121`. The v08 selection-ready MD/JSON are authoritative; historical review files stay unchanged.

Exact selected files are registered through `tools/sync/register-art.mjs`. Canonical public selected paths are below; runtime `assetPath` stays null until Gameplay PMO verifies the engine bindings, following the Chapter 2/docs105 workflow. Suggested engine destinations are recorded separately, not silently bound.

| Asset | Version | Registry key | SHA-256 |
|---|---|---|---|
| CH4-01 | v05 | `scenes:grand_bellevue/lobby` | `582bcd51de937e5fe124160a8beb74b4ee469f52eeb6d9d0d38b918cfb0d6be0` |
| CH4-02 | v05 | `scenes:grand_bellevue/lobby#portraitBackground` | `b2f11966c5b598b1869803f35eb38d00006f346c40a563118c4bdb0eacadf77f` |
| CH4-03 | v08 final review | `portraits:hotel_auctioneer:showman` | `231baf25ffd00511144693927354e73f42cae4f052964a9db0a99323689a0d78` |
| CH4-04 | v07 | `scenes:grand_bellevue/restroom` | `83cf1f0df4d130f24c53c931cae83fd92abef8fdc7e8f80359c5657ce051ce06` |
| CH4-05 | v07 | `scenes:grand_bellevue/ballroom` | `76a290b0f7419927440e0635638183b89a7844b03bc9cec065bc08827dec713c` |

## CH4-01

- Canonical selected PNG: [`assets/selected/pending-integration/scenes/grand_bellevue/lobby.png`](../assets/selected/pending-integration/scenes/grand_bellevue/lobby.png).
- Contract: 314×206 RGB.
- Suggested engine destination, not yet bound: `art/scenes/grand_bellevue/lobby.png`.
- Story-node associations (29): `entry_backstage_exit`, `hotel_lobby_view`, `hotel_auctioneer_arrival`, `hotel_auction_reopen_53`, `hotel_auction_testimonial`, `hotel_auction_bride_ally`, `hotel_auction_dispute_ticket`, `hotel_auction_chair_lot31`, `hotel_chair_vegetation_inspection`, `hotel_chair_examiner_inspection`, `hotel_chair_stapler_stealth`, `hotel_chair_stapler_caught`, `hotel_chair_staff_escort`, `hotel_chair_ring_focus`, `hotel_ring_retrieved`, `hotel_ring_slips`, `hotel_ring_in_pocket`, `hotel_ring_show_bride`, `hotel_bride_ring_handover`, `hotel_bride_ring_bathroom`, `hotel_collection_ring_to_bride`, `hotel_lot61_pod_auction`, `hotel_lot61_pod_escaped`, `fatal_lot61_folded`, `hotel_lot61_pod_declined`, `hotel_ring_inspect_inscription`, `hotel_auctioneer_restroom_inventory`, `hotel_auctioneer_lot14_dispute`, `hotel_auctioneer_lot14_recall`.
- Provenance: Independently native-drawn environment as recorded in v05.
- Immutable source: [tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21/v05/native/CH4-01-lobby-v05.png](https://github.com/InterstellarHarvest/CYOA-storyboard/blob/3463e20bd366390008fa4f71c087ed5f334f3a31/tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21/v05/native/CH4-01-lobby-v05.png).

## CH4-02

- Canonical selected PNG: [`assets/selected/pending-integration/scenes/grand_bellevue/lobby/portraitBackground.png`](../assets/selected/pending-integration/scenes/grand_bellevue/lobby/portraitBackground.png).
- Contract: 564×278 RGB.
- Suggested engine destination, not yet bound: `art/portraits/grand_bellevue/backgrounds/lobby.png`.
- Story-node associations (19): `hotel_auctioneer_arrival`, `hotel_auction_reopen_53`, `hotel_auction_testimonial`, `hotel_auction_bride_ally`, `hotel_auction_dispute_ticket`, `hotel_auction_chair_lot31`, `hotel_chair_vegetation_inspection`, `hotel_chair_examiner_inspection`, `hotel_chair_stapler_caught`, `hotel_chair_staff_escort`, `hotel_ring_show_bride`, `hotel_bride_ring_handover`, `hotel_bride_ring_bathroom`, `hotel_lot61_pod_auction`, `hotel_lot61_pod_escaped`, `hotel_lot61_pod_declined`, `hotel_auctioneer_restroom_inventory`, `hotel_auctioneer_lot14_dispute`, `hotel_auctioneer_lot14_recall`.
- Provenance: Independently native-drawn environment as recorded in v05.
- Immutable source: [tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21/v05/native/CH4-02-auctioneer-background-v05.png](https://github.com/InterstellarHarvest/CYOA-storyboard/blob/3463e20bd366390008fa4f71c087ed5f334f3a31/tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21/v05/native/CH4-02-auctioneer-background-v05.png).

## CH4-03

- Canonical selected PNG: [`assets/selected/pending-integration/portraits/hotel_auctioneer/showman.png`](../assets/selected/pending-integration/portraits/hotel_auctioneer/showman.png).
- Contract: 564×278 RGBA.
- Suggested engine destination, not yet bound: `art/portraits/grand_bellevue/hotel_auctioneer/showman.png`.
- Story-node associations (6): `hotel_auctioneer_arrival`, `hotel_auction_reopen_53`, `hotel_auction_chair_lot31`, `hotel_lot61_pod_auction`, `hotel_auctioneer_restroom_inventory`, `hotel_auctioneer_lot14_dispute`.
- Provenance: SOURCE-DERIVED: preferred original -> premultiplied-alpha Lanczos 564x278 -> cutout cleanup -> targeted near-opaque interior feature contrast cleanup.
- Immutable source: [tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21/v08/native/CH4-03-auctioneer-source-derived-v08.png](https://github.com/InterstellarHarvest/CYOA-storyboard/blob/3463e20bd366390008fa4f71c087ed5f334f3a31/tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21/v08/native/CH4-03-auctioneer-source-derived-v08.png).

## CH4-04

- Canonical selected PNG: [`assets/selected/pending-integration/scenes/grand_bellevue/restroom.png`](../assets/selected/pending-integration/scenes/grand_bellevue/restroom.png).
- Contract: 314×206 RGB.
- Suggested engine destination, not yet bound: `art/scenes/grand_bellevue/restroom.png`.
- Story-node associations (12): `hotel_restroom_entry`, `hotel_restroom_plumber`, `hotel_valve_braced`, `hotel_valve_flood`, `hotel_stall_lot_claimed`, `hotel_wheel_buyer_lead`, `hotel_lot_receipt_study`, `hotel_wheel_return`, `hotel_key_master_cabinet`, `hotel_stall_porter_protest`, `hotel_stall_crane_success`, `fatal_stall_final_occupancy`.
- Provenance: Hybrid native room background with source-derived illustrated NPCs and v07 crispness correction.
- Immutable source: [tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21/v07/native/CH4-04-restroom-v03.png](https://github.com/InterstellarHarvest/CYOA-storyboard/blob/3463e20bd366390008fa4f71c087ed5f334f3a31/tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21/v07/native/CH4-04-restroom-v03.png).

## CH4-05

- Canonical selected PNG: [`assets/selected/pending-integration/scenes/grand_bellevue/ballroom.png`](../assets/selected/pending-integration/scenes/grand_bellevue/ballroom.png).
- Contract: 314×206 RGB.
- Suggested engine destination, not yet bound: `art/scenes/grand_bellevue/ballroom.png`.
- Story-node associations (2): `hotel_wedding_arrival`, `hotel_bridal_organizer`.
- Provenance: Hybrid native room background with source-derived illustrated NPCs and v07 crispness correction.
- Immutable source: [tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21/v07/native/CH4-05-ballroom-v03.png](https://github.com/InterstellarHarvest/CYOA-storyboard/blob/3463e20bd366390008fa4f71c087ed5f334f3a31/tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21/v07/native/CH4-05-ballroom-v03.png).

## Verification and gameplay handoff

The independent verifier checks each registered file against the immutable approved Git blob, owner hash, native contract, exact source object and approved status. It also protects all prior selected metadata/PNGs and canonical narrative/gameplay files. [Machine-readable completion](127_CH4_BATCH1_APPROVAL_COMPLETION_20261122.json) and [verification](127_CH4_BATCH1_VERIFICATION_20261122.json).

Gameplay PMO: pin the published canonical approval revision; copy these exact native selected PNG bytes to the suggested destinations after validating loader conventions; assign runtime assetPath in a separate integration change; retain source-derived portrait provenance; bind only authored logical scenes/pose, preserving later event-state requirements; run importer, pixel/composite and route QA; publish tested game evidence before changing approved to integrated. Do not import 4× previews or regenerate approved images. All narrative, choices, checks, items, flags, chapter readiness and gameplay files remain unchanged.

Batch 2 starts separately from the canonical v08 inventory: five restroom dialogue/control review candidates, all UNSELECTED pending Nate.
