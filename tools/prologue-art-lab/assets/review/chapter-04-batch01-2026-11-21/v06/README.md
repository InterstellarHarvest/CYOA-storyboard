# Chapter 4 v06 — quality-first portrait and resumed environments

All candidates remain **UNSELECTED**. [Open the gallery](index.html). Nate's [revised production policy](../PRODUCTION-POLICY.md) explicitly authorizes source-derived portraits, prioritizes consistency with approved NPCs and supersedes the former independent-native-only restriction. The preferred direction is `portrait-study-02`; no old auctioneer design is reused.

## CH4-03 — source-derived 564×278 foreground

The unchanged 1788×880 preferred illustration is reduced with premultiplied-alpha Lanczos and limited native cutout-edge cleanup. Lanczos was selected after internal comparison with bicubic and box reduction; only the strongest final is published. No palette limit, global repainting, sharpening or additional wrinkle pass is used. Cleanup removes low-alpha/disconnected cutout specks and saturated perimeter contamination; anatomy, expression, tilted head, hair, hands/gavel, jacket, lapels and pocket square are retained. [Exact derivation](evidence/portrait-derivation.json).

This is **source-derived**, not independently authored at native resolution. It is now an authorized production-resolution candidate, not an approved/integrated asset. Native/4× comparisons include the preferred diagnostic and actual approved Pavilion attendant/presenter, with receptionist also preserved as a reference. The foreground is composited over the exact frozen v05 background; dark/light matte checks inspect silhouette edges. The original illustration, two-reference generation prompt, provenance and previous comparisons remain untouched in `portrait-study-02`.

The optional [illustrator handoff](CH4-03-ILLUSTRATOR-HANDOFF.md) remains available for an independently painted alternative. The former production exception is recorded as **authorized by the later policy**, not owner-decision-pending. Only final selection remains pending.

## CH4-04/05 — native room backgrounds with illustrated source-derived NPCs

Restroom and ballroom v02 each have a fresh detailed architectural study generated with the frozen hotel lobby and actual approved Chapter 2 Bureau/Control Tower as visual references. Their originals, exact prompts and [generation receipts](evidence/environment-generation-receipts.json) are preserved. Room backgrounds are independently drawn from blank 314×206 canvases and never open/resize reference rasters. Nate rejected the code-drawn figures, so final frames combine those backgrounds with separately generated illustrated NPCs matching the actual approved Pavilion scene characters and portraits. Their original atlases, exact prompts, crop/scale/placement recipes and layer hashes are preserved. The final scenes are **hybrid / source-derived NPC composites**, not independently authored whole-frame art. [NPC derivation](evidence/scene-npc-derivation.json).

The restroom has three basins, fresh towels, three stall modules with two doors closed and the nearest open, a readable tank/seat/bowl, bare valve spindle, keyed cabinet, service access and a closed ceiling hatch wider than the full nearest stall footprint. It depicts entry/pre-flood state. The study's extra basin is deliberately corrected. Following Nate's scale feedback, both plumbers are rebuilt as adult kneeling/crouching figures at different depths; their size is tied to the camera height, sinks and ground plane rather than a fixed tiny sprite.

The ballroom has a distinct open parquet floor, raised piano platform and two musicians, dimensional service access with workers carrying a chair, an organizer/clipboards, side tables, heavy faded drapery, improvised wedding bunting, intrusive jointed metal ducts and a restroom-direction pictogram. No bridal lavatory is depicted. Standing figures also use adult proportions against the doors/ground plane. Scene NPCs now retain actual illustrated faces, hair, hands and clothing folds at scene scale, following the approved scene-NPC examples; the rejected faceless code figures are not used.

Direct comparisons include preserved v01 images and actual approved Chapter 2 Bureau/Control Tower, with Spore Garden/Tour Tram benchmark selectors. Native and exact 4× views are provided. [Visual/perspective QA](evidence/scene-visual-qa.json) records composition, lighting, materials, person scale and known limits. Native detail is necessarily less extensive than the large studies; owner review still determines artistic approval.

## Preservation, replay and publication

The v05 lobby/background PNGs and hashes are frozen exactly. All v01–v05 files and both portrait-study packages remain unchanged. Narrative, gameplay, main, production assets/workflows and approval records are untouched. The fetched canonical main is `d9b6b91604b72115c5402253f00924665e957727`; relevant Chapter 4 requirements match the checkout and are preserved verbatim.

Rebuild from this directory with the Pillow version recorded in the manifest:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/portrait.py
PYTHONDONTWRITEBYTECODE=1 python3 source/restroom.py
PYTHONDONTWRITEBYTECODE=1 python3 source/ballroom.py
PYTHONDONTWRITEBYTECODE=1 python3 source/scene_people.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package_review.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

Validation separately checks authorized portrait derivation and forbids raster reads/resampling/non-native canvases during room-background replay and separately replays the disclosed source-derived actor composition. Exact native replay, 4× pixels, alpha/composite, source hashes, earlier-version preservation, canonical requirements and gallery resources are checked. Browser QA covers all comparisons, benchmark selection, image decode and mobile pixel preservation. Passing QA does not approve art.

Completed candidates, references, prompts, source, manifests, comparisons, hashes, QA and gallery are published on `art/ch4-batch01-review-20261121` under standing authorization. Remote verification reports stay outside the package so they do not change the commit being verified. No production GitHub Pages workflow is modified.
