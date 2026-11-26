# Chapter4 B2-13 v01 — AutoFit gown

**One primary Focus candidate and one supplemental discovery reference. Everything new UNSELECTED.** Both are564×278 opaque RGB, with exact2256×1112 nearest-neighbor4× exports. Intended future key: `focus:grand_bellevue/autofit_gown`; no production registry entry or runtime binding is changed.

The wide primary shows the entire empty gown on its steel rolling stand: alarmingly narrow corset waist, broad satin skirt, asymmetric lace swags, three visible casters, brass motor/geared drum and thin routed cables. The maker's label and safety pictogram are physically small. Inner lining conceals the release solution. The closer supplemental resolves MANUAL SLACK and NOT AN EMERGENCY STOP while showing loosened cables. It depicts a moment inside the authored motor node before the lining is replaced. See `CONDITION-AND-INTEGRATION-HANDOFF.md` for exact conditions and why a single supplemental is sufficient.

## Controlling references

- Canonical baseline: `436e83f43c01b0a64620056d44aabf14c61fb444`, including completed B2-12 registration.
- `docs/129_PERMANENT_PIXEL_ART_PRODUCTION_STANDARD_20261122.md`.
- `docs/138_CH4_B209_REVISED_PRODUCTION_BRIEF_20261124.md`.
- `docs/145_CH4_B212_APPROVAL_COMPLETION_20261126.md`.
- Exact authored gown/motor/camera/try/survival nodes copied to `evidence/canonical-nodes.json`.
- Approved B2-12 dressing room and Focus, plus actual approved Chapter2 Exposure Dispenser, Aid Box and Bureau. Exact canonical bytes/hashes are in `references/` and `evidence/benchmark-provenance.json`.

## Authoring method and provenance

Built-in `image_gen.imagegen` produced one detailed composition/material reference, preserved in `originals/` with the exact prompt and input hashes. It uses the approved room for garment/stand identity, approved Chapter2 Focus for pixel/material quality, and approved hotel Focus for palette/light continuity. It is a design reference only.

`source/build_native.py` independently constructs the actual raster on blank564×278 canvases. It reads no reference PNG, samples no reference colour/pixel, transfers no image fragment, and does no source-image reduction or tracing. The renderer's only external input is the bitmap glyph JSON. Layers contain hand-authored geometric silhouettes, constant-colour material regions, stepped wood/brass/steel profiles, rounded satin fold bands, localized cutwork lace/embroidery, collar/cable routes, mechanical parts and binary lettering. Curves describe object geometry, not smooth mathematical colour gradients. No dithering, artificial sharpening, antialiased illustration or arbitrary global palette cap is used.

The closer camera re-rasterizes the same authored world geometry directly at final resolution with a denser curve sampling grid and selected native fastener highlights. It is not an enlarged raster crop. Native layer orders, exact hashes, material ramps, semantic masks and lettering bounds are preserved. A source-derived reduction appears only in explicitly labeled diagnostics/comparisons and never enters production rendering.

**Honest provenance:** visual design is SOURCE-DERIVED from approved artwork and the generated reference; the finished native raster is independently constructed with zero source-pixel transfer. We do not claim a wholly independent creative design or that the reference was itself native art. An isolated replay with only the drawing recipe and glyph data verifies reproduction without source images.

## Text hierarchy and first-pass visual gate

Nate clarified: text need not be readable in the wider scene; a closer dress/mechanism view handles detailed lettering. The primary therefore uses a small maker plate and safety pictogram instead of large text boards. The same two-image scope provides a closer motor-discovery reference for readable release/warning text.

Direct native/4× comparisons use actual approved Chapter2 object art and B2-12 continuity. The gown/stand silhouette, narrow waist and complete hem/casters remain legible. Satin fold masses, stepped shadows, lace cutwork, brass motor, recessed gear and painted steel are distinct. The closeup retains the same construction, cable routes, lamp/paneling and exposed mechanism. There are no people, mannequin, AI face, worn garment or fatality.

One coherent internal correction resolved lace occlusion of labels and strengthened bodice/lace construction. The owner's subsequent text-hierarchy clarification reduced the wide labels and moved the one discovery reference to a closer native camera. No new reference-generation cycle or extra production image was added. This final pair is the owner-review proposal; technical compliance and internal visual assessment do not confer approval.

## Review, replay and preservation

`index.html` is local; published `online.html` pins dependencies to immutable artwork bytes. Native and4× controls display actual integer raster dimensions with horizontal scrolling. `comparisons/` and their separate4× exports show Chapter2 quality, approved-room continuity and the two candidates. Source/world diagnostics are clearly marked NOT production/candidate.

Python3 + Pillow replay: `python3 source/build_native.py`, `python3 source/package_review.py`, `python3 source/validate.py`. QA records dimensions, palette diagnostics, hashes, binary native layers, exact compositing/4×, source-isolated replay, concealment, authored conditions, node snapshots, zero changes outside the world-state masks and preservation of every baseline blob. Browser verification covers Chromium and Firefox; public receipts live outside frozen v01 after publication.

All approved artwork/hashes, selection records, historical alternatives, narrative, gameplay, engine code and PR#32 remain untouched. Canonical main is not modified. No registry entry or bindings are created. B2-14 and later production do not start before Nate reviews B2-13.
