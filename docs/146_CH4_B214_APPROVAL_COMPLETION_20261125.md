# Chapter 4 B2-14 — bridal lavatory v02 and three seashells v01: approval registration

**Owner approval:** On 2026-11-25, Nate approved **B2-14** after native and exact nearest-neighbour 4× review:
- **CH4-NEW-02 bridal lavatory v02**;
- **CH4-NEW-09 three seashells v01**, unchanged.

Both are **APPROVED / SELECTED**. No pixels were modified, downscaled, re-encoded or regenerated.

**Approved review source:**
- Branch `art/ch4-b214-native-review-20261125`, approved head [`fbad7b3620f0043752868215bea046bccc259e05`](https://github.com/InterstellarHarvest/CYOA-storyboard/commit/fbad7b3620f0043752868215bea046bccc259e05).
- Package root `tools/prologue-art-lab/assets/review/chapter-04-b214-bridal-lavatory-2026-11-25/`.

| Unit | Selection | Canonical key → selected path | SHA-256 | Format | Immutable source |
|---|---|---|---|---|---|
| CH4-NEW-02 bridal lavatory **v02** | **APPROVED / SELECTED** | `scenes:grand_bellevue/bridal_lavatory` → `assets/selected/pending-integration/scenes/grand_bellevue/bridal_lavatory.png` | `85fb565d8c2f79525a95ada44a9f9e3c05e2cee374712e520488c88153ee7480` | 314×206 opaque RGB | [`100debc`](https://github.com/InterstellarHarvest/CYOA-storyboard/commit/100debcb0940f330b7237da93c05e99c6bf7d89e) `v02/native/CH4-NEW-02-bridal-lavatory-v02.png` |
| CH4-NEW-09 three seashells **v01** | **APPROVED / SELECTED** | `focus:grand_bellevue/three_seashells` → `assets/selected/pending-integration/focus/grand_bellevue/three_seashells.png` | `70f35ae3853883b4fe15293ae5e6fd5ede1e721ab54946d2bc7499ce94ac04c6` | 564×278 opaque RGB (Focus A) | [`04a920c`](https://github.com/InterstellarHarvest/CYOA-storyboard/commit/04a920c08f06d1bf62d63eaaf5f52cddd99c38b9) `v01/native/CH4-NEW-09-three-seashells-v01.png` |

Both files are byte-identical at their introducing commit and at the approved review head.

## Superseded and unapproved artwork

- **Lavatory v01 (superseded, historical review artwork).**
  - It is preserved unchanged on the review branch at `v01/native/CH4-NEW-02-bridal-lavatory-v01.png`, SHA-256 `522cc6a4c2e2d45f1aae7b3897a05380b86a2c70fccdba767576aa1520cabc04`, introduced in `04a920c` and identical at `fbad7b3`.
  - It is not selected, not copied into `assets/selected/`, and has no key.
  - The complete v01 and v02 review packages remain on the review branch: the imagegen reference, its prompt, native layers, recipes and public verification receipts.
- **Separate Claude alternatives from the B2-14 agent collision: NOT APPROVED.**
  - Hashes `ebc3287c…` (lavatory) and `8a4f5343…` (seashells).
  - They are not registered, not copied into the repository, and are absent from every selected image. The verifier enforces this.

## Provenance

Both images are honestly **SOURCE-DERIVED**:
- One preserved built-in imagegen reference per image, with its exact prompt.
- Each final raster was constructed separately at native resolution from editable layers and material ramps. No source pixels were transferred.
- Wholly independent native-grid authorship is not claimed.
- v02 refines only the lavatory's materials and lighting over the fixed v01 geometry. Its three shell layers are pixel-identical to v01, so the room matches the unchanged Focus.

## Canonical coverage

**`grand_bellevue/bridal_lavatory`** serves `hotel_seashell_room`, `hotel_seashell_first_attempt`, `hotel_seashell_instructions`, `hotel_seashell_complaint`, `hotel_seashell_second_attempt` and `hotel_seashell_assessment_appeal`. It is also the scene behind the `hotel_seashell_inspect` Focus.
- The room shows a spotless small lavatory with an open marble counter bearing exactly three shells.
- It has no toilet, sink or concealed fixture.
- The bathroom AI stays **voice-only** (`bathroom_ai:neutral`, docs/137 C2): no portrait, face or closer background.

**`grand_bellevue/three_seashells`** is the Focus of `hotel_seashell_inspect` and keeps its four authored choices.
- The shells are smooth, ridged, and "the third".
- No order, mechanism, text or solution is implied. The shells stay props, not inventory items.
- The key has two segments; the engine's three-segment Focus requirement is already tracked in docs/140 and is not addressed here.

Both registry records are `approved`, with `assetPath: null`. Their suggested engine paths are `art/scenes/grand_bellevue/bridal_lavatory.png` and `art/focus/grand_bellevue/three_seashells.png`. The selected preview paths are not engine paths.

No Chapter 4 narrative, choices, flags, items, routes, Focus behavior, engine code, game integration, deployment or draft PR #32 is changed.

## B2-13 status

**B2-13 (AutoFit gown) is not registered on canonical `main`** at base `436e83f`.
- Its review branch `art/ch4-b213-autofit-gown-review-20261125` (head `7a74fc3`) is untouched.
- `focus:grand_bellevue/autofit_gown` remains absent from the registry.
- This registration neither adds nor removes anything for B2-13.

## Workflow and verification

1. Added the two registry records to `story/artwork.draft.json` as `not-started`.
2. Ran `node tools/sync/register-art.mjs` for exactly the two approved PNGs: dry run first, then the real run. It copied the exact bytes, wrote provenance to `story/artwork-preview.json`, and raised both records to `approved`.
3. `node tools/sync/check-canon.mjs` reports OK: 288 art records (70 approved, 140 integrated, 73 not-started, 5 reused) and 205 previewed.
4. `node tools/storyboard/qa-smoke.mjs` passes.
5. `python3 tools/sync/verify-ch4-b214-selection.py` passes 244 checks against canonical base `436e83f43c01b0a64620056d44aabf14c61fb444`. Report: `docs/146_CH4_B214_VERIFICATION_20261125.json`. The checks cover:
   - exact selected hashes and formats;
   - byte identity with both review commits;
   - preservation of superseded v01;
   - absence of the unapproved alternatives;
   - exact provenance metadata;
   - all **203 earlier selections** unchanged, with their bytes;
   - all earlier registry records unchanged;
   - an unchanged `assets/approved/` tree;
   - no narrative or engine-facing change;
   - nothing beyond the registration files changed;
   - an unchanged PR #32 head.

The earlier point-in-time verifiers (`verify-ch4-b2xx-selection.py`) pin their own bases and expect exactly their own additions. Like `verify-ch4-b208` after the consolidation, they are not re-run as regressions.

Next in the docs/138 queue: B2-13 awaits its own approval and registration; then B2-16 (fatal aftermaths). Any new candidates stay **UNSELECTED** until Nate approves them.
