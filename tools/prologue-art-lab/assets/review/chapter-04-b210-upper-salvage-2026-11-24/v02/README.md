# B2-10 v02 — modest refinement of the published scene

One314×206 RGB candidate, exact1256×824 nearest-neighbor preview, **UNSELECTED** pending Nate. [Gallery](index.html) · [v01/v02](comparisons/v01-v02-native.png) · [Quick-glance4×](comparisons/quick-glance-4x.png) · [Manifest/hash](manifest.json).

The established v01 composition is retained. This follows Nate's latest request to refine the existing batch toward the earlier Chapter4 main-scene pixel-art improvements. It does not use the rejected generic-bowl redraw or restart the room. The historical v01 hold and every v01 file remain unchanged.

## Limited changes

- Replace repetitive rack fixture symbols with a sink, a detached toilet bowl and one quiet partition. The stock is supported by its shelves and has less competing edge/contrast density.
- Preserve the original concept's angled nested sink anatomy, then interpret its porcelain at native resolution with coherent local ramps, silhouette masks and selective rim/socket/underside/contact repairs. It is the existing scene's fixture design, rather than a new generic bowl design.
- Use the **actual approved Chapter4 restroom's native bowl fragment** as a model/style source for the rear bowl. Crop `(266,121,291,142)` is transferred at native size, without scaling, with the cistern/room/floor excluded; a detached outlet is illustrated. The frozen approved source and its hash are preserved. Approval of that source does not approve this new composite.
- Retain the mirror/partition treatment around the foreground. Where sink occlusion changes, the original native backing supplies the newly exposed surface. The mirror comparison is provided for inspection; no full mirror or room repaint is claimed.

Eight other semantic layers are copied byte-for-byte from v01. Lift and sill, W.C. glyphs/three buttons, hatch, stairwell/guardrails, ductwork, architecture and central movement floor remain pixel-exact. Only the two fixture layers and their local supports are changed. No general relighting, whole-scene palette fitting, blur, sharpening or new image generation.

## Honest provenance and editable source

This is **SOURCE-DERIVED**, following the localized material/structure approach used in the approved B2-02 pixel pass. Some reference-defined object contours are retained. It is not a claim of wholly independent hand-painted native authorship.

`source/refine_existing.py` preserves the room, builds native fixture masks and rack/support geometry, interprets only the localized original-reference porcelain underpainting, quiets weak isolated texture, and paints selective native contour/socket/contact corrections. A frozen native approved-art fragment supplies the rear bowl modelling. The original detailed source, exact prompts and historical recipes remain preserved in `../v01/`; no new prompt/generation is claimed. [Repair provenance and layer order](evidence/repair.json), `layers/`, `masks/`, `references/` and the diagnostic underpainting make the derivation explicit.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/refine_existing.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package_review.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

The final layer order is recorded in the repair JSON. All PNG layers are editable at314×206; transparent masks are binary. Reproduction uses frozen v01 inputs and the frozen approved reference, not whatever production source might be selected later.

## Review gate

The native before/after shows meaningful improvement in foreground sink volume and recognizable stock, with less rack clutter. The quick-glance sheet includes actual approved Chapter2 Control Tower/Maintenance Exit and Chapter4 Service Stairs; further comparisons include Damaged Walkway/Loading Dock. Crops retain identical native scale, with caption widths measured to prevent overlap.

This is a modest refinement for **owner visual review**, not formal approval or integration. Small rear stock remains deliberately simpler than foreground porcelain so the routes dominate. Technical QA checks exact dimensions/scaling, unchanged geography, bounded edits, frozen sources, layer replay and byte-for-byte historical preservation. Those checks do not substitute for Nate's decision.

No canonical main, selected/approved PNG, narrative, gameplay, binding, draft PR32, other batch or deployment changes. No new Focus IDs, flags, scenes, portraits or state variants.
