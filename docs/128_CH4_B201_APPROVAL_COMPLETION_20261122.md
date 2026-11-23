# Chapter 4 B2-01 v01 approved selection and gameplay handoff

Nate approved all five **unchanged** on 2026-11-22. All are **APPROVED and SELECTED**, not integrated. Immutable authoritative review commit: `81cf3b5f022510737bdd2d4ba3703e0173d86772` on `art/ch4-batch01-review-20261121`. Manifest: `tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/v01/manifest.json`, SHA-256 `ce96a63e20ebabf6e26cf5cabd056bc46448612c6b55f8de52d77d8e184c07d0`. Historical packages and Batch1 approvals stay unchanged.

Registration follows docs/105 and [Batch1 docs/127](127_CH4_BATCH1_APPROVAL_COMPLETION_20261122.md): verify immutable inputs, dry-run register-art, register exact selected PNG bytes, validate canon and preservation, review PR, then publish. Curated selected paths are canonical public copies; runtime assetPath is null until Gameplay PMO integration. Suggested engine destinations use existing conventions without binding the engine.

| Asset | Canonical key | SHA-256 |
|---|---|---|
| CH4-B2-01 — Plumber — worried | `portraits:hotel_plumber:worried` | `cedd81713cbd5ee4bb0a97d869a62c395a1b34ea04ba276fa5ac21c01d5de65d` |
| CH4-B2-02 — Eddie — pleased | `portraits:hotel_plumber_assistant:pleased` | `ac47c23105b70af92b970682b72c266726ddbe9a75e182bdf6a71869568d6eea` |
| CH4-B2-03 — Restroom conversation background | `scenes:grand_bellevue/restroom#portraitBackground` | `77325aca0d3c61d5b6d1980232fb11fa55156454a26659c6887c4d726a82c377` |
| CH4-B2-04 — Lot 14 receipt | `focus:grand_bellevue/restroom/lot_14_receipt` | `af9f7b03eacfe54721e52217b265b7fcdc852b0eb7cf1d0cd1fd7e7f1eef85d3` |
| CH4-B2-05 — Emergency master isolator | `focus:grand_bellevue/restroom/master_isolator` | `ba494521a177b397cc9db901e83046fccc83afcfcebca890b23a0656be042153` |

## CH4-B2-01 — Plumber — worried

- Canonical selected PNG: [`assets/selected/pending-integration/portraits/hotel_plumber/worried.png`](../assets/selected/pending-integration/portraits/hotel_plumber/worried.png).
- Contract: 564×278 RGBA; transparent foreground. Original exact4× preview is2256×1112 nearest-neighbor.
- Suggested engine destination, not yet bound: `art/portraits/grand_bellevue/hotel_plumber/worried.png`.
- Canonical node associations: `hotel_restroom_plumber`.
- Provenance: **SOURCE-DERIVED**, not independent native-grid authorship. [Original processing](https://github.com/InterstellarHarvest/CYOA-storyboard/blob/81cf3b5f022510737bdd2d4ba3703e0173d86772/tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/v01/evidence/derivation.json).
- Immutable native source: [tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/v01/native/CH4-B2-01-v01.png](https://github.com/InterstellarHarvest/CYOA-storyboard/blob/81cf3b5f022510737bdd2d4ba3703e0173d86772/tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/v01/native/CH4-B2-01-v01.png).

## CH4-B2-02 — Eddie — pleased

- Canonical selected PNG: [`assets/selected/pending-integration/portraits/hotel_plumber_assistant/pleased.png`](../assets/selected/pending-integration/portraits/hotel_plumber_assistant/pleased.png).
- Contract: 564×278 RGBA; transparent foreground. Original exact4× preview is2256×1112 nearest-neighbor.
- Suggested engine destination, not yet bound: `art/portraits/grand_bellevue/hotel_plumber_assistant/pleased.png`.
- Canonical node associations: `hotel_wheel_buyer_lead`.
- Provenance: **SOURCE-DERIVED**, not independent native-grid authorship. [Original processing](https://github.com/InterstellarHarvest/CYOA-storyboard/blob/81cf3b5f022510737bdd2d4ba3703e0173d86772/tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/v01/evidence/derivation.json).
- Immutable native source: [tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/v01/native/CH4-B2-02-v01.png](https://github.com/InterstellarHarvest/CYOA-storyboard/blob/81cf3b5f022510737bdd2d4ba3703e0173d86772/tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/v01/native/CH4-B2-02-v01.png).

## CH4-B2-03 — Restroom conversation background

- Canonical selected PNG: [`assets/selected/pending-integration/scenes/grand_bellevue/restroom/portraitBackground.png`](../assets/selected/pending-integration/scenes/grand_bellevue/restroom/portraitBackground.png).
- Contract: 564×278 RGB; opaque. Original exact4× preview is2256×1112 nearest-neighbor.
- Suggested engine destination, not yet bound: `art/portraits/grand_bellevue/backgrounds/restroom.png`.
- Canonical node associations: `hotel_restroom_plumber`, `hotel_wheel_buyer_lead`, `hotel_stall_porter_protest`.
- Provenance: **SOURCE-DERIVED**, not independent native-grid authorship. [Original processing](https://github.com/InterstellarHarvest/CYOA-storyboard/blob/81cf3b5f022510737bdd2d4ba3703e0173d86772/tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/v01/evidence/derivation.json).
- Immutable native source: [tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/v01/native/CH4-B2-03-v01.png](https://github.com/InterstellarHarvest/CYOA-storyboard/blob/81cf3b5f022510737bdd2d4ba3703e0173d86772/tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/v01/native/CH4-B2-03-v01.png).

## CH4-B2-04 — Lot 14 receipt

- Canonical selected PNG: [`assets/selected/pending-integration/focus/grand_bellevue/restroom/lot_14_receipt.png`](../assets/selected/pending-integration/focus/grand_bellevue/restroom/lot_14_receipt.png).
- Contract: 564×278 RGB; opaque. Original exact4× preview is2256×1112 nearest-neighbor.
- Suggested engine destination, not yet bound: `art/focus/grand_bellevue/restroom/lot_14_receipt.png`.
- Canonical node associations: `hotel_lot_receipt_study`.
- Provenance: **SOURCE-DERIVED**, not independent native-grid authorship. [Original processing](https://github.com/InterstellarHarvest/CYOA-storyboard/blob/81cf3b5f022510737bdd2d4ba3703e0173d86772/tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/v01/evidence/derivation.json).
- Immutable native source: [tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/v01/native/CH4-B2-04-v01.png](https://github.com/InterstellarHarvest/CYOA-storyboard/blob/81cf3b5f022510737bdd2d4ba3703e0173d86772/tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/v01/native/CH4-B2-04-v01.png).

## CH4-B2-05 — Emergency master isolator

- Canonical selected PNG: [`assets/selected/pending-integration/focus/grand_bellevue/restroom/master_isolator.png`](../assets/selected/pending-integration/focus/grand_bellevue/restroom/master_isolator.png).
- Contract: 564×278 RGB; opaque. Original exact4× preview is2256×1112 nearest-neighbor.
- Suggested engine destination, not yet bound: `art/focus/grand_bellevue/restroom/master_isolator.png`.
- Canonical node associations: `hotel_key_master_cabinet`.
- Provenance: **SOURCE-DERIVED**, not independent native-grid authorship. [Original processing](https://github.com/InterstellarHarvest/CYOA-storyboard/blob/81cf3b5f022510737bdd2d4ba3703e0173d86772/tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/v01/evidence/derivation.json).
- Immutable native source: [tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/v01/native/CH4-B2-05-v01.png](https://github.com/InterstellarHarvest/CYOA-storyboard/blob/81cf3b5f022510737bdd2d4ba3703e0173d86772/tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/v01/native/CH4-B2-05-v01.png).

## Verification

[Machine-readable selection](128_CH4_B201_APPROVAL_COMPLETION_20261122.json) and [independent results](128_CH4_B201_VERIFICATION_20261122.json) record exact source/copy hashes, native dimensions/alpha,4× pixels, node mappings, previous150 selected previews/bytes, all earlier artwork records and canonical narrative/gameplay/workflow preservation. The read-only verifier stages only committed approved native files; no regeneration, resize, sharpening, lettering or alpha processing is performed during registration.

## Gameplay PMO handoff

Pin the published approval revision. Copy the five exact native selected PNGs to the suggested destinations after validating actual loader conventions. Assign runtime assetPath and promote to integrated only in a separate verified game-integration change. Keep the two transparent foregrounds over the shared opaque restroom background, and use564×278 Focus A (not565×451 item inspection). Preserve the receipt lettering/perspective/margins, single isolator lever and all source-derived provenance. Do not use4× previews as native masters. Run importer, scene/portrait/Focus bindings, route and actual pixel QA; publish game build evidence under docs105. No engine integration or narrative/gameplay change occurred here.

Next production group comes from the existing canonical v08 inventory: B2-02 loading dock and service arrivals (six UNSELECTED assets).
