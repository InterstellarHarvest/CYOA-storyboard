# Chapter 4 B2-13 — AutoFit gown v01: approval record and registration

**Owner approval:** Nate approved **both B2-13 v01 images** in the Chapter 4 Artwork PMO conversation on **2026-11-25, before B2-14 production began**.
- The AutoFit gown Focus is **APPROVED / SELECTED**.
- The closer manual-slack discovery image is **APPROVED / PRESERVED** as a supplemental reference.
- Registration happened after B2-14 (docs/146, merge `8fc6d19`), so this record is the first canonical registration of an approval that already existed.
- No pixels were modified, downscaled, re-encoded or regenerated.

**Approved review source:**
- Branch `art/ch4-b213-autofit-gown-review-20261125`, approved head [`7a74fc38c1b0533e01425738433ff7be0c917b4e`](https://github.com/InterstellarHarvest/CYOA-storyboard/commit/7a74fc38c1b0533e01425738433ff7be0c917b4e).
- Both images were introduced in [`144a2a6`](https://github.com/InterstellarHarvest/CYOA-storyboard/commit/144a2a6b53408c495a8ee9a51a79f1be719fe462) at `tools/prologue-art-lab/assets/review/chapter-04-b213-autofit-gown-2026-11-25/v01/native/`. They are byte-identical at the approved head.

| Image | Owner decision | Canonical / preservation path | SHA-256 | Format |
|---|---|---|---|---|
| `CH4-NEW-08-autofit-gown-v01.png` | **APPROVED / SELECTED** `focus:grand_bellevue/autofit_gown` | `assets/selected/pending-integration/focus/grand_bellevue/autofit_gown.png` | `0e1a0d3cd73c087416a7e9a2502ae263a597f7da77476e4cd0219dd504d48095` | 564×278 opaque RGB (Focus A) |
| `CH4-NEW-08-manual-slack-revealed-v01.png` | **APPROVED / PRESERVED** supplemental reference for `hotel_bridal_gown_motor` | `tools/prologue-art-lab/assets/approved/conditional-production-references/chapter-04/b2-13/CH4-NEW-08-manual-slack-revealed-v01.png` | `592bc3e6a237745d9a066fe5d7424d1cb5f520caffbc0af2491eaf76d83bb98d` | 564×278 opaque RGB |

## Correction to docs/146

docs/146 (B2-14 registration) wrongly said B2-13 "awaits its own approval and registration". B2-13 had already been approved and awaited **registration only**.

A dated correction was added to docs/146 on 2026-11-25 in two places: under its "B2-13 status" heading and after its closing line. The change is additions only; every original line is kept, so the record of what was written stays intact. docs/146's statement that B2-13 was not *registered* at base `436e83f` was accurate.

## Coverage and boundaries

**`focus:grand_bellevue/autofit_gown`** is the Focus of the existing node `hotel_bridal_gown_focus`, which keeps its four choices: examine motor, try on, hold to camera, leave alone.
- The image shows the whole empty gown on its rolling stand, with the brass motor, geared drum and routed cables under parted outer lace.
- A small maker plate and safety pictogram appear. The inner lining still conceals the manual-slack release.
- There is no wearer, mannequin, protagonist or fatal aftermath.
- The key has two segments; the engine's three-segment Focus requirement is already tracked in docs/140 and is not addressed here.

**The manual-slack image** is a closer camera on the same garment, showing the lining lifted, the brass MANUAL SLACK tab, the NOT AN EMERGENCY STOP warning and slightly slack cables.
- It depicts a moment inside the authored narrative node `hotel_bridal_gown_motor`, before the lining is replaced. That node sets `ch4_autofit_release_located`.
- It is preserved reference art with **no Focus key, flag, mode change, choice or runtime binding**.
- The motor node stays narrative mode. Discovering the tab does not switch the motor off or guarantee survival.
- Any later presentation is a separate, authorized Gameplay PMO decision. It must not persist an open-lining state.

The registry record is `approved` with `assetPath: null`; its suggested engine path is `art/focus/grand_bellevue/autofit_gown.png`.

No Chapter 4 narrative, choices, flags, items, routes, Focus behavior, engine code, game integration, deployment or draft PR #32 is changed.

## Provenance

Both images are **SOURCE-DERIVED**:
- One preserved built-in imagegen reference and its exact prompt.
- The native rasters were separately constructed on blank 564×278 canvases from authored geometry and material layers. No reference pixels were transferred.
- The closer view re-rasterizes the shared geometry; it is not an enlarged crop.
- Wholly independent creative authorship is not claimed.
- The original reference, prompt, layers, masks, recipes and public verification receipts remain on the review branch.

## Workflow and verification

1. Added one registry record, `grand_bellevue/autofit_gown`, as `not-started`.
2. Ran `node tools/sync/register-art.mjs` for the primary PNG: dry run first, then the real run. It copied the exact bytes, wrote provenance to `story/artwork-preview.json`, and raised the record to `approved`.
3. Copied the supplemental byte-for-byte into the approved conditional-reference folder, following the B2-07/B2-11/B2-12 precedent.
4. `node tools/sync/check-canon.mjs` reports OK: 289 art records (71 approved, 140 integrated, 73 not-started, 5 reused) and 206 previewed.
5. `node tools/storyboard/qa-smoke.mjs` passes.
6. `python3 tools/sync/verify-ch4-b213-selection.py` passes against canonical base `8fc6d196846a25f3a303a1a7ed53d120e07f13df`, which includes the completed B2-14 registration. Report: `docs/147_CH4_B213_VERIFICATION_20261125.json`. The checks cover:
   - exact bytes and formats, and identity with both review commits;
   - exactly one new selection with exact provenance;
   - no key for the supplemental;
   - one added registry record and nothing else;
   - node structure intact, with the motor node still narrative;
   - all **205 earlier selections** unchanged, with their bytes, including B2-14;
   - existing approved references unchanged, with only the B2-13 reference added;
   - only registration files changed;
   - docs/146 keeps every line and gains only the dated correction;
   - no narrative or engine-facing change;
   - an unchanged PR #32 head.

Next in the docs/138 queue: B2-16 (four fatal aftermaths). Its candidates stay **UNSELECTED** until Nate approves them.
