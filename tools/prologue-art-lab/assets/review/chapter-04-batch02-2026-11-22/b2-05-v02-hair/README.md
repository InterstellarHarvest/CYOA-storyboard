# B2-05 v02 — honey-blonde bride, targeted color revision

Four **UNSELECTED** revised bride portraits: determined, hopeful, grateful and helpful. Nate requested a clearly different hair color from the approved dark-brown-haired groom. Honey blonde is the new direction. The exact v01 clerk remains separate, unchanged and unselected.

## Exact scope

`source/recolor.py` starts from the four v01 PNGs at immutable review commit9afe76fe17dcb02633b82261a6c69457891da50f. Individually authored native hair silhouette polygons plus a warm-hair color predicate select only the existing hair clusters. Ear/earring exclusion boxes preserve anatomy. An eight-step honey-blonde ramp replaces chestnut shades; original ink, transparency, silhouette, face/brows/expression, gown/veil, hands and props are preserved. No new shapes, texture, gradients or dithering. All pixels outside the final hair masks are byte-identical; alpha is entirely unchanged. Exact source/final hashes and changed-pixel maps are retained.

Built-in `image_gen.imagegen` supplied the [hair-color direction reference](originals/bride-honey-blonde-direction-reference.png), [exact prompt](prompts/hair-color-direction.txt) and [receipt](evidence/imagegen-reference-receipt.json). That generated image is a palette guide only; its face, pose, background/alpha artifacts and canvas are not used in the final foregrounds. Original v01 detailed pose references and all earlier images remain preserved in the adjacent v01 package. Final artwork remains honestly **source-derived**, not independently authored whole-image native art.

[Gallery](index.html), [four revised brides beside approved groom](comparisons/all-native.png), [exact4×](comparisons/all-4x.png), [manifest](manifest.json), [exact scope](evidence/targeted-change.json), [QA](evidence/validation.json). Every pose includes v01/v02/groom comparison PNGs, exact4×, Chapter2 groundskeeper comparison and an unchanged-lobby-background composite. The approved Pavilion presenter remains a craft benchmark.

Reproduce with Pillow:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/recolor.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

No approval/selection registration, main, narrative, gameplay or engine integration changes. Every earlier approved image, historical review, groom PNG, clerk candidate and alternative plumber portrait remains unchanged. All four revisions stay UNSELECTED pending Nate.
