# B2-09 v03 — targeted wedding-cake/trolley correction

**UNSELECTED.** Only B2-09 changes. The owner called B2-06/07/08 selection-ready and requested exact preservation; this is not approval/selection registration. [Frozen sibling hashes](evidence/frozen-siblings.json). All ten approved Chapter 4 assets and every previous candidate remain unchanged.

## Method and cause

The existing native material/structure source is editable. The v02 cake silhouette was incomplete; the elevator-panel drawing also failed to respect object occlusion. Upper tiers disappeared, with some cart/frame/caster encroachment from structural/floor painting. This correction reads those frozen native layers, masks the structural layer with the complete cake/trolley silhouette, restores material pixels and paints a small native layer with rounded tiers, warm side planes, flowers/piping, frame and casters. The foreground mover/hand is protected.

No built-in imagegen call, regeneration or whole-group rerender is needed for this existing native-layer edit. No palette conversion or new color is introduced. The result remains **source-derived** through its original reference/native construction provenance. It is not claimed independently authored as a complete new native scene.

[Native comparison](comparisons/B2-09-v02-v03-native.png), [exact4x comparison](comparisons/B2-09-v02-v03-4x.png), [gallery](index.html), [changed pixels](evidence/changed-pixels-4x.png), [exact scope](evidence/targeted-change.json). Only 723 pixels change, all within the protected object mask; every other v02 pixel and the existing palette remain exact. Original detailed reference and crop are preserved for visual inspection. Dimensions 314×206 opaque; exact 4× 1256×824.

## Repeatable safeguard

Story-object protection must clip ALL later structural paint, including wall/elevator geometry and floor/grout passes. Masks must include the whole silhouette: upper tiers/flowers, handles, cloth edges, frame and wheels. Check protected masks against source objects and inspect native/exact4x before publication; hashes/color counts alone cannot detect a lost story object. [Audit](evidence/story-object-audit.json). The four-scene technique is retained; no other scene is rerun here.

Reproduce with the recorded Pillow version:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/restore.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

`source/restore.py` is the exact native edit recipe; no new image-generation prompt exists. Source native/layer/reference inputs are pinned to 62ef2059585de49292bbec2742d3c637d2eae818 and preserved historical files. The targeted object layer, protected mask, clipped structural layer, source palette restriction and before/after previews are included. No narrative, gameplay, production integration, main or approval-record changes.
