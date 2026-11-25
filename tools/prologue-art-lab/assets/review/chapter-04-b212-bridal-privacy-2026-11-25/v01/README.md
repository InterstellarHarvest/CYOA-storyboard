# Chapter 4 B2-12 v01 — owner review

**UNSELECTED. No artwork approval, registration or engine integration is implied.**

Two primary candidates and one conditional reference follow the pinned `BRIEF.md` at `9f49416c9dd2e8b02e84b04a6c4ed1f4bc5e65b5`:

| Candidate | Native PNG | Contract |
| --- | --- | --- |
| CH4-NEW-01 Bridal dressing room | `native/CH4-NEW-01-bridal-dressing-room-v01.png` | 314×206 opaque RGB |
| CH4-NEW-07 Privacy panel, locked | `native/CH4-NEW-07-bridal-privacy-panel-v01.png` | 565×451 opaque RGB, explicit review brief |
| Provisional authorization reference | `native/CH4-NEW-07-provisional-authorized-v01.png` | Same 565×451 geometry; screen and LED only |

`manifest.json` records exact SHA-256 hashes, source-derived provenance, proposed canonical keys and existing story-node associations. These are review records only. Canonical paths and runtime bindings remain null.

## Review

Open `index.html` locally or the published `online.html` through the repository's existing HTML preview service. Native images display at their actual pixel dimensions. Exact4× images use nearest-neighbor pixels and no responsive rescaling; wide comparisons scroll horizontally. Direct comparison PNGs are in `comparisons/` at native and exact4×. Approved Chapter2 and Chapter4 PNGs in `references/` retain their canonical bytes and actual dimensions.

Judge the scene at314×206 first: empty gown, deliberately narrow waist, steel stand with grounded H-base and three visible casters, closed handle-less bathroom door and adjacent privacy hardware. White satin/lace, velvet, tarnished steel/brass, green painted wood and aged cream plaster remain distinguishable. There are no people, AI faces, mannequins, bathroom fixtures, shells, abandoned shoes or fatal-aftermath illustrations. The mirror reflects only empty room/light. The cool window and warm sconces provide coherent light direction.

The closeup exposes a swivel camera, recessed CRT, red locked indicator, closed lock, visual-ID/bride-only/groom-exclusion badges and physical emergency-assistance button. Its provisional state substitutes green authorization and an open lock. It is a conditional production reference for the existing AutoFit-survival outcome; no new flags, Focus IDs, scene keys or dispatch have been invented. The main-room bathroom door remains closed; later lavatory artwork is outside this batch.

## Dimension boundary

The invoked brief explicitly requests **565×451** for Focus A, including a second explicit instruction for readable lettering. Existing approved Focus artwork and the current runtime contract use **564×278** (`docs/105`, lines174–178). These review images follow the brief's565×451 dimensions. They are **not asserted compatible with current Focus runtime**. No engine or registry change, crop, stretch, alternate runtime image or dimension migration is included. Resolve the conflicting contract before separate registration/integration. See `evidence/dimension-contract.json`.

## Authoring and provenance

**SOURCE-DERIVED; not wholly independently authored at native resolution.** Three built-in image-generation originals and their exact prompts are preserved. The detailed room establishes composition/material relationships; a separately generated pixel-friendly study informs the scene's shade grouping; the closeup source informs physical panel material and light. The first generation's exact reference-attachment list was not retained; it is not reconstructed from guesses. The other two calls' explicit input lists and hashes are recorded.

`source/build_native.py` constructs at the final314×206 and565×451 grids. Source-derived BOX diagnostic fields are explicitly labeled **NOT production**. Semantic native masks assign material-specific colour ramps, remove isolated tiny material islands and retain useful grouped light observations. Final-grid structural layers separately construct door leaf/insets, duct flange/vent profiles, wall moldings, rolling steel rack/joints/casters, empty wooden hanger, gown seams/fold paths and lace groups, main-scene privacy icons, Focus plate thickness/screws, camera optics/swivel, CRT depth, policy pictograms, button and binary bitmap lettering. Source fields and native structural construction are both disclosed; the result is not presented as independently painted from a blank canvas.

Native RGBA layer PNGs and L-mode semantic masks are editable. `evidence/native-layer-recipes.json` contains exact compositing orders and hashes. `evidence/material-ramps.json` records coherent material ramps, without an arbitrary global palette cap. `evidence/lettering-layout.json` records chunky5×7 glyph construction, native glyph scale and measured margins. No antialiasing, dithering, smooth final gradients or interpolated enlargement is used. `source/build_native.py` and `source/package_review.py` replay the assets, previews, comparisons and manifests using Python3 + Pillow.

## One complete artistic gate

See `evidence/visual-review.md`. The complete first pass was compared directly with actual approved Ch2 Bureau/Control Tower and Ch4 Lobby/Ballroom/Staff Lavatory/Public Corridor at native and exact4×, plus actual approved Focus examples. One coherent internal correction restored green lower-wall materials, gave the lamp a native brass/glass frame, removed the source button inscription behind the rebuilt button and widened policy-label margins. Stop at this completed pass; no cosmetic revision cycle or next batch has started.

## Verification and boundaries

`evidence/validation.json` verifies native dimensions/opacity, exact4× pixel identity, native layer replay, conditional state masks, lettering margins, source/benchmark hashes, source-node associations and byte preservation of every baseline tracked file. `evidence/qa-canon.json` and `evidence/qa-smoke.txt` record unchanged canonical checks. Browser evidence records actual decoded images and integer-size controls in Chromium and Firefox. Public receipts live outside the frozen v01 package after publication.

Canonical `main`, `assets/selected`, all prior review versions and plumber alternatives, production records, narrative/gameplay/runtime files and PR#32 are untouched. B2-13 AutoFit gown and B2-14 lavatory/seashell closeups remain future work. Nate's visual approval is the next gate; registration and integration are separate.
