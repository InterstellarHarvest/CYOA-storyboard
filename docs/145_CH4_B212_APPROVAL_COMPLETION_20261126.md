# Chapter 4 B2-12 — owner approval, artwork registration and dual-view handoff

**Owner approval:** Nate approved the B2-12 dressing-room v01 and original square inspection design on 2026-11-25; he approved both widescreen Focus v02 states and then approved the two revised square INSPECT v03 states after a lock-icon/text spacing correction. The preferred production set is **five images**: one 314×206 scene, two 564×278 Focus states, and two 565×451 INSPECT states. No sixth gameplay scene or new inventory item is needed.

**Registration model:** Two canonical primary keys are **APPROVED / SELECTED**; three conditional/inspection assets are **APPROVED / PRESERVED**, without new Focus identifiers, item keys or runtime bindings. The two superseded square v01 images remain preserved byte-for-byte as historical approved design masters. The game importer still uses the existing 564×278 Focus A contract; no engine feature or gameplay change is part of this registration.

Review branch: `art/ch4-b212-bridal-privacy-review-20261125`.

| Image | Owner selection | SHA-256 | Canonical/preservation path |
|---|---|---|---|
| CH4-NEW-01 dressing room v01 — 314×206 RGB | **APPROVED / SELECTED** scene `scenes:grand_bellevue/bridal_dressing_room` | `f2718d729a28138a88cf51b6ef3c511bdf6d7de0d500654d975b1ab0249bdf49` | `assets/selected/pending-integration/scenes/grand_bellevue/bridal_dressing_room.png` |
| CH4-NEW-07 locked widescreen Focus v02 — 564×278 RGB | **APPROVED / SELECTED** `focus:grand_bellevue/bridal_privacy_panel` | `d4c260fb9b4c55e647cecb58bb6fed196f9f056fd3cf291f1862889ff8035520` | `assets/selected/pending-integration/focus/grand_bellevue/bridal_privacy_panel.png` |
| CH4-NEW-07 provisional widescreen Focus v02 — 564×278 RGB | **APPROVED / PRESERVED** conditional state | `b7d8014313519b67d3ebe8c72772ed0d01b4dbbb88748c9e5b0e7f589d669272` | `tools/prologue-art-lab/assets/approved/conditional-production-references/chapter-04/b2-12/CH4-NEW-07-focus-provisional-v02.png` |
| CH4-NEW-07 locked INSPECT v03 — 565×451 RGB | **APPROVED / PRESERVED** inspection art | `b571f3215be27ab7e86bdb67530a86d33e20ed6a0638842f88227fdbc06ec0e3` | `tools/prologue-art-lab/assets/approved/inspection-references/chapter-04/b2-12/CH4-NEW-07-inspect-locked-v03.png` |
| CH4-NEW-07 provisional INSPECT v03 — 565×451 RGB | **APPROVED / PRESERVED** inspection art | `fa4d465cd6c25b7591ff97caf2713e4b521ef3c2dba6243c5a571685f17660e9` | `tools/prologue-art-lab/assets/approved/inspection-references/chapter-04/b2-12/CH4-NEW-07-inspect-provisional-v03.png` |

## Immutable source provenance

- Dressing-room v01: [`1261658ed882bff7340405e91f5d44f4e5404012`](https://github.com/InterstellarHarvest/CYOA-storyboard/commit/1261658ed882bff7340405e91f5d44f4e5404012), `tools/prologue-art-lab/assets/review/chapter-04-b212-bridal-privacy-2026-11-25/v01/native/CH4-NEW-01-bridal-dressing-room-v01.png`.
- Both widescreen Focus states: [`a944f9aeff110ddc66301840c2d415f1ba9bc357`](https://github.com/InterstellarHarvest/CYOA-storyboard/commit/a944f9aeff110ddc66301840c2d415f1ba9bc357), `tools/prologue-art-lab/assets/review/chapter-04-b212-bridal-privacy-2026-11-25/v02/native/CH4-NEW-07-focus-{locked,provisional}-v02.png`.
- Both corrected square INSPECT states: [`43490eeabeb4edb619903ecb4836b0da8d9a4446`](https://github.com/InterstellarHarvest/CYOA-storyboard/commit/43490eeabeb4edb619903ecb4836b0da8d9a4446), `tools/prologue-art-lab/assets/review/chapter-04-b212-bridal-privacy-2026-11-25/v03/native/CH4-NEW-07-inspect-{locked,provisional}-v03.png`.
- Earlier approved square v01 image bytes remain separately preserved at `tools/prologue-art-lab/assets/approved/visual-design-masters/chapter-04/b2-12/` with hashes `072e30b905014a3856e21190551307eab0b0298dd0624e831f5395951d3b7afb` (locked) and `e546f7eb4d6de3a319548ee7759ab9ca83e415caa7293fb29322ca6f98ef44b3` (provisional). Their original review package is unchanged. The v03 improvement moves only CRT text/icons, retaining the exact source palette and every pixel outside the CRT content region.
- All artworks retain honest **SOURCE-DERIVED** provenance. Native layers, imagegen references, processing recipes, masks and exact prompts remain pinned in their respective review packages. This registration does not claim wholly independent native authorship.

## Gameplay/UI handoff — explicitly deferred

The canonical node `hotel_bridal_door_focus` already uses scene `grand_bellevue/bridal_dressing_room` and Focus identifier `grand_bellevue/bridal_privacy_panel`, with five approved existing choices, including the conditional wedding-ring action. Use the selected locked widescreen art as the normal Focus A close-up with the story choices visible and usable. Preserve the approved provisional widescreen art for the corresponding later authorization condition; do not add a second Focus key or author a new state transition in the storyboard.

Nate's separate dual-view design is to add a contextual **INSPECT** action that opens the matching 565×451 square image for detailed reading. It is **not an inventory item**. X or Escape must return to the exact same widescreen Focus node and available choice set. Opening and closing the overlay may not invoke `Rules.step`, consume a choice, set/clear flags, grant/remove an item, reset dialogue, change eligibility or alter save data. Extra descriptive text must be informational and consistent with approved narrative, not a new branch. No runtime art binding is made here because the scene-owned 565×451 inspection presentation does not yet have a tested engine contract.

Before Gameplay PMO integrates, validate in Chromium and Firefox: each of five bridal-door choices, ring available/unavailable, previously asked/denied flags, locked/provisional art dispatch, X/Escape, keyboard focus, text and choice scrolling, save/resume, and all existing Focus and inventory inspections. The current inspector intentionally hides cards while open; the old special scene-pickup close commits a choice, so it cannot be reused blindly. If choices break, retain current Focus behavior and do not enable the square overlay. The engine's existing 564×278 Focus contract remains controlling.

No Chapter 4 narrative, item, rule, route, gameplay asset path, engine code, public Pages workflow or draft PR #32 is changed by this registration. No game integration/deployment is authorized here.

## Verification and queue

`node tools/sync/register-art.mjs` was used for exactly the two primary keys, preserving the exact source PNG bytes and registering source ref/commit/path and hashes. The three additional preferred artworks are preserved separately with no runtime binding. `node tools/sync/check-canon.mjs` passes. Run `python3 tools/sync/verify-ch4-b212-selection.py` for pinned image contracts, five approved production choices, historical master preservation, prior-selection preservation, metadata, storyline and engine boundary checks. The verification report is `docs/145_CH4_B212_VERIFICATION_20261126.json`.

B2-12 art is visually complete under Nate's approval. Continue the consolidated Chapter 4 queue at **B2-13** according to `docs/138`, without reopening the retired assets or obsolete B2-09 scope. The separate INSPECT engine feature stays in the deferred integration queue.
