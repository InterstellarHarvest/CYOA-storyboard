# v07 — NPC crispness at native size and exact 4×

**UNSELECTED.** This is an NPC-only correction to the v06 restroom/ballroom composites. The preferred auctioneer, all room backgrounds, poses, scale, positions, contact shadows, frozen v05 lobby/background and every earlier review remain unchanged.

The previous 4× exports were already exact nearest-neighbor. The blur came from the NPC source reduction itself. Internal comparison covered area reduction, direct nearest, box, sharpening and two-stage sampling. The selected treatment retains sharper source information in declared face/hand regions, uses a 2× prefilter followed by native nearest sampling and light local-contrast restoration for body/clothing, and replaces soft fractional-alpha silhouettes with native pixel coverage. Parameters, feature rectangles, crop coordinates and source hashes are explicit in [npc-derivation.json](evidence/npc-derivation.json). There is no palette quota, new design, invented facial linework or return to code-drawn figures.

[Open the gallery](index.html) or the [exact 4× NPC before/after comparison](comparisons/NPC-v06-v07-approved-4x.png). Original NPC masters and generation prompts remain unchanged in v06. This revision introduces no new image-generation call; Python/Pillow performs the disclosed authorized source-derived processing and final-resolution cleanup. Native samples are displayed one-for-one, and every 4× export repeats final pixels exactly.

The figures remain limited by their actual 25–60px widths and 46–74px heights. Sharper sampling makes some one-pixel source texture more conspicuous. Compare actual faces/hands/hair/clothing and the approved scene NPCs before judging the balance; technical passing is not creative approval.

Reproduce from this directory with the Pillow version recorded in the manifest:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/derive.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package_review.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

QA checks exact replay, preserved crop/placement/scale, source hashes, transparent sprites, opaque final scenes, final-pixel nearest-neighbor 4× exports, every prior-version byte, and changed-pixel scope outside old/new NPC alpha. Browser QA checks the native/4× controls, comparison sheet, image decode and mobile pixel preservation. Publication is to `art/ch4-batch01-review-20261121`; remote verification reports stay outside the reviewed package.

No main, production, narrative, gameplay or approval records are modified. All candidates remain UNSELECTED for Nate.
