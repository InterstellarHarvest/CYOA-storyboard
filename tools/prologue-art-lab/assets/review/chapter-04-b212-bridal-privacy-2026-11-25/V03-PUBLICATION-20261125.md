# B2-12 v03 — INSPECT lock-row alternatives

**Both565×451 alternatives remain UNSELECTED pending Nate's explicit approval.** Existing v01 INSPECT/dressing room and newly approved v02 widescreen artwork are preserved unchanged. No canonical registration, narrative/gameplay/runtime change, main merge, PR#32 change or deployment is included.

[Public browser gallery](https://htmlpreview.github.io/?https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/bf2ebf97a5e06f04bb3cc09e333dd63cd3c293f0/tools/prologue-art-lab/assets/review/chapter-04-b212-bridal-privacy-2026-11-25/v03/online.html) · [Native before/after close-ups](https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/bf2ebf97a5e06f04bb3cc09e333dd63cd3c293f0/tools/prologue-art-lab/assets/review/chapter-04-b212-bridal-privacy-2026-11-25/v03/comparisons/both-states-crt-before-after-native.png) · [Exact4× before/after close-ups](https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/bf2ebf97a5e06f04bb3cc09e333dd63cd3c293f0/tools/prologue-art-lab/assets/review/chapter-04-b212-bridal-privacy-2026-11-25/v03/previews/both-states-crt-before-after-native-4x.png).

- Branch: `art/ch4-b212-bridal-privacy-review-20261125`.
- Preservation baseline: `a944f9aeff110ddc66301840c2d415f1ba9bc357`.
- Native alternatives, layers and recipes: `63617fd0327cfa4018175377a75f99838598e861`.
- Immutable gallery and public verification: `bf2ebf97a5e06f04bb3cc09e333dd63cd3c293f0`.
- Main unchanged: `13ea9b57ee3b5c670a3ab0ff0f160896559ce2ef`.
- PR#32 unchanged: `f320e63934c13e27fd13b9482d0cfba58911362d`.

## Exact new files

| State | SHA-256 | Changed native pixels |
| --- | --- | --- |
| locked | `b571f3215be27ab7e86bdb67530a86d33e20ed6a0638842f88227fdbc06ec0e3` | 2187 |
| provisional | `fa4d465cd6c25b7591ff97caf2713e4b521ef3c2dba6243c5a571685f17660e9` | 2931 |

Native565×451 opaque RGB; exact nearest-neighbor4×2260×1804. Only pixels within the existing CRT-content rectangle `[289,106,421,163]` inclusive are edited. All surrounding pixels, CRT glass accents, bezel, status LED, brass frame, lighting and material treatment are exact. Each image retains the exact original29-colour palette.

The centered text block starts11 native pixels higher; its line gap is4 pixels. Both states use the same text box, icon zone and lock-body anchor. Dedicated lock-row spacing is9 clear native rows below the locked text and8 below provisional text; the one-pixel difference is the different shackle silhouette within the same icon zone. Closed and open shackles connect appropriately to the same-position body. No divider or new glass styling was added.

## Approved source bytes preserved

| Protected reference | Unchanged SHA-256 |
| --- | --- |
| APPROVED INSPECT source | `072e30b905014a3856e21190551307eab0b0298dd0624e831f5395951d3b7afb` |
| APPROVED INSPECT source | `e546f7eb4d6de3a319548ee7759ab9ca83e415caa7293fb29322ca6f98ef44b3` |
| Newly APPROVED widescreen - protected | `d4c260fb9b4c55e647cecb58bb6fed196f9f056fd3cf291f1862889ff8035520` |
| Newly APPROVED widescreen - protected | `b7d8014313519b67d3ebe8c72772ed0d01b4dbbb88748c9e5b0e7f589d669272` |

These are owner-approved references, not re-registrations. Historical review manifests retain their original review-time labels. Reference copies are exact; all original v01/v02 files remain untouched.

## Verification

- All62 targeted checks pass: dimensions/opacity, SHA-256, exact source palette, binary editable patch alpha, exact native layer replay, actual/authorized difference masks, zero outside-content changes, shared text/body anchors, clear icon spacing, exact176×99 crops and nearest-neighbor4× previews.
- All927 pre-existing tracked files remain byte-for-byte unchanged, including every v01/v02/source/history file and200 selected-asset files. Canonical story/approval/runtime files are unchanged.
- Local Chromium and Firefox pass all20 figure checks at native and exact4×, with full comparisons/alternatives inspected.
- At public commit `bf2ebf97a5e06f04bb3cc09e333dd63cd3c293f0`, all67 package files match local bytes and all47 PNGs decode; remote branch verified. See `V03-PUBLIC-BYTE-VERIFICATION.json`.
- Actual public gallery passes all20 figure checks in Chromium and Firefox. Native/4× dimensions are exact integer raster dimensions with pixelated rendering. Public combined close-ups were visually inspected; screenshots and report are in `public-browser-v03/`.
- This receipt and public verification evidence are outside the frozen v03 package. No reviewed artwork is modified after publication verification.

## Provenance and review boundary

No new image generation or high-resolution reduction. Existing native bitmap glyphs and localized editable raster layers are used for the correction; original SOURCE-DERIVED illustration provenance remains accurate. `v03/source/OWNER-REQUEST.txt`, `source/build.py`, glyph data, patches, actual masks and layout measurements preserve the exact request and reproducible method. Original image-generation sources/prompts/layers stay in immutable v01 history.

Review the two v03 alternatives against the approved v01 close-ups. They offer clearer separation of display text and status icons while preserving the object. They do not replace an approved image until Nate explicitly selects them through the separate workflow. Approved widescreen v02 remains unchanged; no INSPECT engine behavior is implemented or changed here.
