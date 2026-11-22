# v04 — native illustrated detail and front-facing auctioneer

Scope: CH4-01 lobby, CH4-02 close background, CH4-03 foreground. All remain UNSELECTED. Every earlier review version and all approved source bytes are preserved; restroom/ballroom and production/story/gameplay/main are untouched.

The owner's later direction changes the auctioneer's old profile: he now faces forward, has ordinary proportions and a restrained older-man expression, and holds his gavel low. Human portrait detail and palette are compared directly with the approved receptionist, Pavilion attendant and Pavilion presenter. Those approved assets are read-only references, not pixel inputs. Burgundy/charcoal/ivory, warm skin and shaded silver hair are explicit material ramps; no global color quota or palette reduction is imposed.

One new built-in imagegen call produced a detailed frontal study using the approved human NPCs as style/proportion references. Its original PNG, exact prompt and receipt are retained. The hotel references and old profile concept are unchanged. No imagegen CLI/API fallback was used.

The native sources draw on blank 314×206 / 564×278 canvases. The foreground uses explicitly placed color clusters and anatomical/construction marks, with no mathematical face lighting or smoothing. Environmental v03 light is retained selectively, with illustrated seams/folds, chips, stains, slab cracks/corners, carpet wear, wood grain/dents, petals/urns, metal collars/fasteners/tarnish. Source raster sampling, supersampling, high-resolution source filtering and downsampling are prohibited in authoring. Only final presentation/export reads PNGs for exact 4× NEAREST and lossless composites.

The floor/window/ceiling perspective uses a shared (182,112) vanishing point, with floor clipping at the left-wall boundary and corrected podium long edges. A numeric audit of actual authored endpoints is in `evidence/perspective-audit.json`; tolerance is one native pixel for raster rounding. This is an illustration audit, not a building engineering model.

`index.html` shows v03/v04/v02 native and exact 4× rows, three-version comparison PNGs, v01, original and frontal concepts, actual approved Chapter 2/reception art, and the approved human NPCs. Native art must be judged at 1× first. `online.html` is an additive browser-preview copy with immutable direct GitHub image links, generated at publication time.

Known artistic limitations remain in `comparison.json` and each gallery card. The result is still stylized, and owner review must decide whether its surface rendering, facial identity/detail, hands, palette and finish meet the approved-art standard. Native authorship and technical passing do not establish aesthetic approval.

Reproduce from this version directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/lobby.py
PYTHONDONTWRITEBYTECODE=1 python3 source/backdrop.py
PYTHONDONTWRITEBYTECODE=1 python3 source/auctioneer.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package_review.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

Validation disables image reads/resampling and rejects non-native authoring canvases/masks, replays exact native bytes, checks dimensions/alpha/exports, verifies preserved history and canonical sources, audits perspective, and checks gallery dependencies. Browser QA tests Chromium/Firefox, every image, three-version native/4× controls, approved comparisons and mobile pixel preservation. QA results and screenshots are retained in `evidence/`.

Per standing authorization, this completed review is committed/pushed to `art/ch4-batch01-review-20261121`, then its remote SHA/image bytes and browser gallery are checked. No creative selection is implied by publication. Stop for Nate's review before any approval registration or restroom/ballroom revision.
