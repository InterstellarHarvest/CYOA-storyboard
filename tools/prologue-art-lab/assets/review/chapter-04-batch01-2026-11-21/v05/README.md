# v05 — portrait painting priority; restricted room corrections

All three assets remain UNSELECTED. The portrait preserves v04's frontal identity, proportions, silhouette and low gavel. The lobby/background continue from v04 with only the specified wear, plaster, wall illumination and variation corrections. Earlier versions, canonical selections, story, gameplay, restroom and ballroom are unchanged.

Portrait authoring changes from a flat contour-only substrate to layered native-size pixel-brush painting. Each pigment mark has an explicit anatomical/material path, width/pressure, color and opacity. The writer reconstructs the substrate from blank and paints into its own 564×278 raster; it never reads reference-image pixels. Native pigment mixing is not source-image sampling. There is no broad face lighting field, automatic texture/noise, blur, supersampling, downsampling, palette extraction or whole-image color reduction.

The unchanged v04 detailed frontal study remains the primary character reference. Actual approved receptionist, Pavilion attendant and Pavilion presenter art are displayed for face, hair, hand, cloth, palette and perceived finish comparisons. No new imagegen call was needed in v05; the original built-in generation prompt/receipt and unchanged study remain preserved in v04.

The portrait rebuilds the socket/brow/lid relationship, age folds, cheek/nose/mouth/neck paint, grouped neutral silver locks, gavel grain/bevel, knuckles and wrapped fingers, jacket folds/seams, satin crests and cotton construction. It remains a relatively graphic illustrated candidate; owner review must decide whether its natural detail and character meet the approved-art standard. More marks, native authorship and technical passing do not establish aesthetic quality.

Room scope is checked at the pixel level in `evidence/targeted-change-qa.json`. The lobby changes 2,018 pixels, all within carpet-wear/plaster regions; the curtain/duct, restroom doors and podium are preserved in explicit protected checks. The background changes 15,037 pixels, all within the lamp panel and blank-wall regions; curtain, duct/attachments, door/wood and actual lamp fixture construction remain unchanged. The new weak lamp-panel falloff is a localized illumination correction, not a room-wide procedural art pass. The foreground alpha silhouette matches v04 exactly.

`index.html` prioritizes the portrait and shows v04/v05 comparisons at native and exact 4×, approved human portraits, historical versions and unchanged concepts. `manifest.json` records images, dimensions, hashes, source nodes, source files, method and limitations. `comparison.json` records the actual visual review axes. The gallery links the correction masks/delta proof. `online.html` is an additive publication entry with immutable direct GitHub image links.

Reproduce from this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/lobby.py
PYTHONDONTWRITEBYTECODE=1 python3 source/backdrop.py
PYTHONDONTWRITEBYTECODE=1 python3 source/auctioneer.py
PYTHONDONTWRITEBYTECODE=1 python3 source/targeted_qa.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package_review.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

Native replay forbids image reads, resampling and non-native canvas/mask sizes and reproduces exact candidate bytes. Other QA covers dimensions, alpha, exact exports, prior-version/canonical preservation, allowed corrections and gallery resources. Browser QA covers Chromium/Firefox image loads, comparisons, 1×/4× controls and mobile pixel preservation. QA does not approve the work.

Completed iterations are automatically committed/pushed to the existing review branch under Nate's standing instruction, then remote commit/image bytes and the browser gallery are verified. No approval registration or production/main merge occurs here.
