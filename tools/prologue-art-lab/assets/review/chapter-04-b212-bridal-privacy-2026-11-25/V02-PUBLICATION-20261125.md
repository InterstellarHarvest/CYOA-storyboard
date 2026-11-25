# B2-12 v02 — widescreen Focus / approved INSPECT publication

**New widescreen candidates UNSELECTED. Existing v01 dressing room and inspection images APPROVED and preserved unchanged.** No canonical registration, gameplay implementation, merge or deployment is included.

[One browser review gallery](https://htmlpreview.github.io/?https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/00ab5cd03adb9a9f5b32d5ff9ee25584f4edd687/tools/prologue-art-lab/assets/review/chapter-04-b212-bridal-privacy-2026-11-25/v02/online.html) · [Matching widescreen states, exact4×](https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/00ab5cd03adb9a9f5b32d5ff9ee25584f4edd687/tools/prologue-art-lab/assets/review/chapter-04-b212-bridal-privacy-2026-11-25/v02/previews/focus-states-native-4x.png) · [Locked Focus / approved inspection, exact4×](https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/00ab5cd03adb9a9f5b32d5ff9ee25584f4edd687/tools/prologue-art-lab/assets/review/chapter-04-b212-bridal-privacy-2026-11-25/v02/previews/locked-focus-approved-inspect-native-4x.png) · [Chapter2 Focus comparison, exact4×](https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/00ab5cd03adb9a9f5b32d5ff9ee25584f4edd687/tools/prologue-art-lab/assets/review/chapter-04-b212-bridal-privacy-2026-11-25/v02/previews/chapter2-focus-benchmarks-native-4x.png) · [Wainscot correction, exact4×](https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/00ab5cd03adb9a9f5b32d5ff9ee25584f4edd687/tools/prologue-art-lab/assets/review/chapter-04-b212-bridal-privacy-2026-11-25/v02/previews/wainscot-correction-native-4x.png).

- Review branch: `art/ch4-b212-bridal-privacy-review-20261125`.
- Baseline / immutable approved v01 source: `1261658ed882bff7340405e91f5d44f4e5404012`.
- New artwork, source, prompt, native layers and handoff: `34041ed69236865fcafc0adc828f4201c6815134`.
- Frozen gallery/package verified at: `00ab5cd03adb9a9f5b32d5ff9ee25584f4edd687`.
- Main remains `13ea9b57ee3b5c670a3ab0ff0f160896559ce2ef`.
- PR#32 remains `f320e63934c13e27fd13b9482d0cfba58911362d`; untouched.

## New review candidates — 564×278 RGB

| State | SHA-256 |
| --- | --- |
| locked | `d4c260fb9b4c55e647cecb58bb6fed196f9f056fd3cf291f1862889ff8035520` |
| provisionally authorized | `b7d8014313519b67d3ebe8c72772ed0d01b4dbbb88748c9e5b0e7f589d669272` |

Both frames share exact geometry. Differences are confined to the screen/LED: locked/red/closed lock versus provisional/green/open lock. They are two state frames of the existing privacy-panel Focus, not extra Focus IDs or runtime bindings. Exact nearest-neighbor4× exports are2256×1112.

## Approved v01 bytes — preserved

| Approved reference | Unchanged SHA-256 |
| --- | --- |
| CH4-NEW-07-inspect-locked | `072e30b905014a3856e21190551307eab0b0298dd0624e831f5395951d3b7afb` |
| CH4-NEW-07-inspect-provisional | `e546f7eb4d6de3a319548ee7759ab9ca83e415caa7293fb29322ca6f98ef44b3` |
| CH4-NEW-01 | `f2718d729a28138a88cf51b6ef3c511bdf6d7de0d500654d975b1ab0249bdf49` |

The inspection PNGs remain565×451; the dressing room remains314×206. Exact copies and pinned original paths are recorded in `v02/evidence/owner-approval-preservation.json`. Historical v01 manifests and artwork remain unchanged; the current owner decision is recorded separately, without canonical registration.

## Owner correction and quality gate

The first native widescreen pass overlapped the wainscot rail. Reconstructed the lower plaster field and moved the rail below the plate and its cast shadow, identically in both states. The native plate/shadow bounding box is `[221,22,417,265]`; the rail begins at269, leaving four clear native rows after the shadow. Actual pixel masks verify zero intersection. The door, camera, brass plate, policy icons, physical button, sconce and conduit remain readable at native and exact4×.

Compared directly against actual approved Chapter2 Exposure Dispenser and Aid Box at564×278 and exact4×. Native side contexts remain substantial; no people, humanoid AI, invented door hardware or narrative props. Large reference guides light/materials, while panel/fixture forms and native profiles are separately painted. The whole work is honestly SOURCE-DERIVED, not claimed wholly independent. One new built-in imagegen source, exact prompt/input hashes, diagnostic, editable layers/masks, coherent ramps and recipe are preserved. Neither approved inspection image was resized/cropped/recolored into a production layer.

## Verification

- All86 targeted package checks pass:564×278 opaque RGB, SHA-256, exact nearest-neighbor4×, binary layer alpha, exact native compositing replay, status-only differences, rail/shadow clearance, lettering margins, source hashes, approved/reference preservation and existing canonical node/choice associations.
- Both new images use34 colours; no arbitrary global cap, dither, smooth-gradient/sharpening pass or isolated grain field. Colour counts are diagnostic, not artistic approval.
- All806 pre-existing tracked files remain byte-exact, including all v01/history and200 selected-asset files. No production/story/gameplay record changes were made.
- Canonical and storyboard smoke checks pass without changing canonical files.
- Local Chromium and Firefox pass all28 figure checks at native and exact4×.
- Public package: all102 files match bytes and all71 PNGs decode at `00ab5cd03adb9a9f5b32d5ff9ee25584f4edd687`; branch SHA verified. See `V02-PUBLIC-BYTE-VERIFICATION.json`.
- Public gallery: both browsers pass all28 native/4× checks; actual screenshots preserved in `public-browser-v02/` and visually inspected. An initial decode request failed; fresh-browser diagnostics decoded all14 gallery images with no failed responses, and the complete unchanged-gallery rerun passed. No artwork modification was needed for delivery.
- Public receipts live outside frozen `v02/`; its reviewed tree stays unchanged after verification.

## Separate engineering handoff

`v02/ENGINEERING-HANDOFF.md` defines contextual informational INSPECT from `hotel_bridal_door_focus` / `grand_bellevue/bridal_privacy_panel`. It lists all five existing choices, conditions, return-hub and ring behavior, plus required keyboard/focus/save-resume/state tests. Inspection must never call `Rules.step`, replay entry effects, mutate flags/inventory, consume a choice or restart dialogue. X/Escape returns to the exact previous widescreen presentation/choices. Existing inventory-inspection or scene-pickup behavior must be verified before any reuse. **Do not activate a feature that cannot preserve choices.**

This is a handoff only, not engine implementation or evidence of current runtime support. Canonical main, narrative/gameplay, runtime bindings and PR#32 remain untouched; no deployment. Recommendation: use this one widescreen composition for normal interaction and retain the exact approved detailed images for INSPECT, subject to Nate selecting the new Focus frames and separate engineering validation.
