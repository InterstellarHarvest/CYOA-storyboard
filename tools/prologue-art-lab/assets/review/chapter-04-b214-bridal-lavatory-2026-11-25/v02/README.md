# B2-14 v02 — bridal lavatory refinement

**One revised primary candidate, CH4-NEW-02. UNSELECTED.** The 314×206 RGB room and its exact 1256×824 nearest-neighbor preview are under `native/` and `previews/`. The separately authored three-seashell Focus is unchanged; its exact v01 bytes appear only as a continuity reference. Both v01 images and the entire v01 package are frozen.

## Artistic scope

The original doorway, wall/floor geometry, VP(157,65), counter polygon, lamp, duct and shell placement remain fixed. The native shell layers and all their opaque pixels are exact matches to v01. The counter still spans the same polygon and six-pixel front thickness; its face is modeled with a lit arris, shadow edge, sparse mineral veins and stronger bracket/contact shadows.

Fixed architectural moldings now have lit faces, recessed fillets and consistent shadows. Green paneling is architectural millwork without handles, hinges or concealed compartments. The floor has individual projected tile surfaces, recessed grout, thin bevel lights and broken warm lamp reflections. Duct faces, folded seams, support fasteners, grille lips and contact shadows communicate its sheet-metal construction. The original sconce has warm milky glass and a small, shaped area of illumination. Clean sealed joints and limited coating wear suggest an old institution maintained by cosmetic renewal rather than a dirty bathroom.

The room remains deliberately empty: one narrow open counter and exactly three shells. No toilet, sink, concealed fixture, NPC, AI face, additional technology or clutter is added. There are no labels, operating clues, shell-order signals or successful states. The original smooth/ridged/ordinary distinction remains exact.

## Method and provenance

This is one cohesive material-and-lighting illustration pass in the existing native source, not a new generated scene or global palette/shading filter. `source/base_native.py` is the exact archived v01 renderer. `source/refine.py` paints the revised surfaces directly on blank 314×206 layers and reuses its deterministic shell construction. Explicit material ramps and categorical clusters replace photographic gradients. Neither renderer reads the detailed reference, samples pixels from it, reduces it, sharpens it or quantizes it.

The original built-in imagegen reference, exact prompt and canonical benchmark inputs are preserved. Its creative/design influence is explicitly **source-derived**; only the final raster construction is independent at native resolution. No new image generation was necessary for this refinement. An isolated replay containing only the two renderer scripts reproduces the final PNG without access to reference images. Editable native RGBA layers, masks, recipe order, material ramps and hashes are included.

## Visual comparison and limitations

`comparisons/` holds v01/v02, canonical Bureau/Control Tower and approved B2-12 dressing-room comparisons, plus continuity with the unchanged Focus. Every sheet has an exact 4× export. At native size, the room is intentionally much emptier than the Bureau and Control Tower; their material separation, edge construction and directional lighting guide the refinement rather than their density of props. At 4×, grout and moldings form stable lines, stone veins remain sparse and shells stay readable. The fine-grained machinery, furniture and foliage of those benchmarks are not imported into this room.

The revised counter's material is more developed than the frozen Focus counter. The shared cream stone, green/gilt wall, lamp direction and shell layout retain continuity; the Focus has not been changed to force an exact finish match. Nate's visual decision remains the approval gate. Technical checks and colour counts do not establish artistic approval.

## Reproduction and verification

Run from any directory with Python 3 and Pillow:

```
python3 source/refine.py
python3 source/package.py
python3 source/validate.py
```

`evidence/validation.json` records native RGB size, exact 4×, layer replay, shell preservation, exact v01/Focus and canonical reference bytes, source-isolated replay and preservation of all 770 prior tracked files, including 202 selected-art files. Palette diagnostics report 42 colours without treating this as an artistic score or an arbitrary limit. `masks/v01-v02-changed-pixels.png` and its record disclose the altered region.

`index.html` is a local gallery. Published `online.html` pins dependencies to an immutable artwork commit. Both galleries display full integer native or exact 4× rasters with horizontal scrolling. Public byte and Chromium/Firefox receipts are stored outside frozen v02.

No registry, binding, selected asset, narrative, gameplay, engine, canonical main or PR #32 changes are made. No subsequent artwork batch begins before Nate's review.
