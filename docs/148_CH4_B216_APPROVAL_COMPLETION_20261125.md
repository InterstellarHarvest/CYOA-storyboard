# Chapter 4 B2-16 — four fatal aftermath illustrations v02: approval registration

**Owner approval:** On 2026-11-25, Nate approved **all four B2-16 v02 fatal aftermath illustrations** without further changes.
- All four are **APPROVED / SELECTED** as canonical `deathScreens` records.
- No pixels were modified, downscaled, re-encoded or regenerated.

**Approved review source:**
- Branch `art/ch4-b216-fatal-aftermaths-review-20261125`, approved head [`0fbecaa28d3127faeb553b7847d13121834806a7`](https://github.com/InterstellarHarvest/CYOA-storyboard/commit/0fbecaa28d3127faeb553b7847d13121834806a7).
- Package `tools/prologue-art-lab/assets/review/chapter-04-b216-fatal-aftermaths-2026-11-25/v02/`.
- All four natives were introduced in [`56fe286`](https://github.com/InterstellarHarvest/CYOA-storyboard/commit/56fe286e427bba9020d9e38be326ca1d82ce400e). They are byte-identical at the approved head and match the v02 review manifest.

| ID | Canonical key → selected path | Fatal node | SHA-256 |
|---|---|---|---|
| CH4-NEW-14 FINAL OCCUPANCY | `deathScreens:grand_bellevue/final_occupancy` → `assets/selected/pending-integration/deathScreens/grand_bellevue/final_occupancy.png` | `fatal_stall_final_occupancy` | `e65d321cac76af8e03dd57ba5cbe3aa2d7db454669b0dd36631c61e51e475b7a` |
| CH4-NEW-15 PRESSED AND STEAMED | `deathScreens:grand_bellevue/pressed_and_steamed` → `assets/selected/pending-integration/deathScreens/grand_bellevue/pressed_and_steamed.png` | `fatal_boiler_pressed_and_steamed` | `f0cb0816a5639977634ef21b7d1d57ccfa136c5ef575aa2bb9fd006fc8097e56` |
| CH4-NEW-16 FOLDED FOR CONVENIENCE | `deathScreens:grand_bellevue/folded_for_convenience` → `assets/selected/pending-integration/deathScreens/grand_bellevue/folded_for_convenience.png` | `fatal_lot61_folded` | `30490a4259b363879dc126e273dcc07bb979d96ad4f6534dd75cb7e3901ddc07` |
| CH4-NEW-17 MADE TO MEASURE | `deathScreens:grand_bellevue/made_to_measure` → `assets/selected/pending-integration/deathScreens/grand_bellevue/made_to_measure.png` | `fatal_bridal_made_to_measure` | `d244595dd545551268143fc6a94e0d9d641d3825324b16db7791b5f0118b21bc` |

All four are 314×206 opaque RGB.

## Records and coverage

**Records.**
- The four `deathScreens` records did not exist on `main`. They were added as `death-screen` records at 314×206 and raised to `approved` by `register-art.mjs`.
- `assetPath` is `null`. The suggested engine paths are `art/deaths/<id>.png`, matching Chapter 2.

**Coverage.** Each record's id is exactly the existing `deathPopup.artRef` and `endingArt` of its fatal node, so no node is edited.
- **FINAL OCCUPANCY:** the restroom after the raised stall is craned away through the ceiling hatch, leaving the broken floor-level toilet, porcelain fragments and lot tags.
- **PRESSED AND STEAMED:** an immaculately pressed, steaming, empty black suit on a hanger; no shoe.
- **FOLDED FOR CONVENIENCE:** Lot Sixty-One as a closed aluminium case, with exactly one shoe.
- **MADE TO MEASURE:** the fitted, empty AutoFit gown on its stand, with exactly one shoe.
- None of the four shows a victim, face, limbs, gore or impact.

**These are aftermath illustrations only.**
- The popup title, description, BEGIN AGAIN button, frame and background remain engine UI. None is baked into the art, and none of them is modified.
- `story/death-presentations.export.json` is unchanged, and `export-death-presentations.mjs --check` passes.
- The game importer does not yet consume Chapter 4 `deathPopup`/`endingArt` fields (docs/140). No death-popup behavior, narrative, gameplay, engine, game integration, deployment or draft PR #32 is changed.

## Superseded v01 (historical review artwork)

Nate rejected v01 for lost detail, especially the sink and toilet. All four v01 natives are preserved unchanged on the review branch, introduced in `1fdf2ce` and identical at `0fbecaa`. None is selected.

| ID | v01 SHA-256 |
|---|---|
| CH4-NEW-14 | `a079f2dd91f2cdfaf9f13d7caa754ae909c6f2e4c24587e033c7edf7e8a66dc9` |
| CH4-NEW-15 | `36f62d19b207626f8fdf11901e43a292316f3880c4e60cbdd26dedd2c65ca3cd` |
| CH4-NEW-16 | `4f64b7a41755553bd8d03a11568678ace298f81e08ebb7661ad3f105d05906db` |
| CH4-NEW-17 | `1ed8f23a9dc93b7324a1cf9a4baf4ee06f98082d9b1d405e94897df5e17c919b` |

## Provenance

All four images are **SOURCE-DERIVED**:
- They use preserved imagegen originals and exact prompts.
- The final rasters were separately constructed at native resolution from binary RGBA layers, semantic masks and material ramps.
- The renderer reads no source image. No source pixels were transferred, reduced, sharpened or quantized.
- Wholly independent creative authorship is not claimed. All sources, layers, recipes and public receipts remain on the review branch.

## QA tooling adjustment

Two QA assertions fixed the death-art catalogue at exactly nine records. As with PR #34 for growing Chapter 4 approvals, they now require exactly the nine earlier records plus **exactly these four** `grand_bellevue/` death records. Any other Chapter 4 death record still fails.
- `tools/storyboard/qa-smoke.mjs`, which is the Pages publish gate.
- `tools/storyboard/qa-browser.js`.

No other tooling changes.

## Workflow and verification

1. Added four registry records as `not-started`.
2. Ran `node tools/sync/register-art.mjs` for each PNG: four dry runs, then four real runs. It copied the exact bytes, wrote provenance, and raised the records to `approved`.
3. `node tools/sync/check-canon.mjs` reports OK: 293 art records (75 approved, 140 integrated, 73 not-started, 5 reused) and 210 previewed.
4. All non-browser CI steps pass locally: `qa-sync`, both Chapter 3 suites, `qa-smoke`, the death-export check and `qa-static`. Local `qa-browser.js` passes 26/26.
5. `python3 tools/sync/verify-ch4-b216-selection.py` passes against canonical base `6a88153f1a41759def5d8e02fd04789db860ec1b`, which includes B2-13 and B2-14. Report: `docs/148_CH4_B216_VERIFICATION_20261125.json`. The checks cover:
   - exact bytes and formats;
   - v02 manifest agreement and identity with both review commits;
   - v01 preserved and not selected;
   - exact provenance and records;
   - fatal nodes and popup copy unchanged and correctly mapped;
   - exactly four new selections;
   - all **206 earlier selections** unchanged, with their bytes, including B2-13 and B2-14;
   - all earlier records and approved supplemental references unchanged;
   - only the registration and QA-count files changed;
   - no narrative, popup or engine-facing change;
   - an unchanged PR #32 head.

Next in the docs/138 queue: B2-17 (dispute ticket and ring item art), then R1 refinements. New candidates stay **UNSELECTED** until Nate approves them.
