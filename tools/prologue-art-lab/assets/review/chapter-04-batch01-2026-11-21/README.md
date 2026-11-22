# Chapter 4 Batch 1 artwork review

Latest: [v07 scene NPC crispness correction](v07/index.html). Face/hand sampling and native cutout cleanup address v06 softness at4x. Only scene NPC pixels change; poses, scale, placement, room backgrounds, auctioneer and frozen v05 environments are preserved. Source-derived processing is fully recorded. All candidates remain **UNSELECTED**.

Preserved complete package: [v06 auctioneer and resumed environments](v06/index.html). The preferred auctioneer is a source-derived 564×278 candidate under Nate's revised [production policy](PRODUCTION-POLICY.md). Restroom/ballroom v02 use native-drawn room backgrounds plus illustrated source-derived NPCs matching the exact owner-supplied approved Pavilion scene examples; rejected code figures are not used. All methods, originals, prompts, layers and derivations are disclosed. Frozen v05 lobby/background and all earlier versions remain unchanged. Everything remains **UNSELECTED**.

Preserved preferred character study: [portrait study 02 — approved NPC style restart](portrait-study-02/index.html). A fresh old man with gavel and burgundy formalwear, generated using **only the approved Pavilion attendant and presenter**. No high-detail auctioneer drawing or previous auctioneer was a generation input. Original output and explicitly source-derived size-matched style diagnostics are preserved. **UNSELECTED; not a completed native production asset.** The v05 lobby/background remain frozen unchanged.

Previous portrait work: [reconstruction method study 01](portrait-study-01/index.html). The fresh built-in raster test is preserved at its returned **1785×881** resolution; it failed the requested 564×278 native-size gate. It is a source-sized method test, **not a completed v06 or a new native candidate**. No downsampled substitute was made. [The method assessment](portrait-study-01/METHOD-DECISION.md) documents the visual comparison and proposes direct layered native raster illustration before further portrait revisions. All artwork remains UNSELECTED.

**CH4-01 and CH4-02 are frozen at v05 for owner review.** Their exact native PNGs and hashes are preserved in [the freeze record](portrait-study-01/evidence/frozen-environments.json); no further edits or approval registration have occurred. All v01–v05 package files remain unchanged.

Latest gallery: [v05/index.html](v05/index.html) — priority native pixel-brush portrait painting plus mask-restricted carpet/plaster/lamp/wall corrections to the v04 room base. Actual approved human NPCs and the unchanged frontal study are the portrait references; their rendering standard is not claimed to be automatically achieved. All CH4-01/02/03 candidates remain UNSELECTED. [v05 production notes](v05/README.md). Previous galleries remain unchanged: [v04](v04/index.html), [v03](v03/index.html), [v02](v02/index.html), [full v01 batch](v01/index.html).

v05 adds explicit layered native pigment brush marks for the frontal character, rather than another broad face-lighting pass. Marks mix only with the reconstructed native canvas, with no reference raster sampling or image rescaling. Room edits have changed-pixel masks/protected-region proof; the portrait's alpha silhouette matches v04. No new imagegen call was needed: the preserved v04 frontal study remains the primary guide.

v04 adds one new detailed frontal character-reference generation; its original PNG, prompt and receipt are preserved. Native portrait pixels are independently illustrated with explicit material/anatomical ramps, not extracted from that reference. The hotel lighting is retained selectively with material/construction illustration and perspective corrections. Historical method descriptions below refer to their earlier versions; v04's exact sources and limitations are in its manifest and production notes.

Online-preview entry: [v02/online.html](v02/online.html). This additive copy uses absolute image URLs pinned to the verified artifact commit, so a read-only HTML preview can render the gallery without interpreting relative image paths. `prepare-online-gallery.py` regenerates it. The original galleries and candidate bytes remain unchanged. GitHub displays HTML as source; the publication handoff supplies a tested browser-preview link when available.

Nate requested more detail after viewing v01: “too simple and not detailed enough compared to ch2 stuff imo.” He clarified that the portrait should carry more detail and the main scene should look less simplistic. v02 revises CH4-01 lobby, CH4-02 close background and CH4-03 showman first. CH4-04 restroom and CH4-05 hall remain preserved v01 candidates; they have not been revised or selected.

All images are generated/unselected. These are initial reconstruction candidates, with a documented quality gap versus Chapter 2, especially natural materials and face/cloth modeling. No approval, registration, gameplay change, public-main merge or deployment occurred.

## Provenance and workflow

Branch: `art/ch4-batch01-review-20261121`.
Canonical main pinned after fetch: `d9b6b91604b72115c5402253f00924665e957727`.

Stage A used built-in `image_gen.imagegen`, six calls, including the corrected empty portrait background. Every original detailed image remains unchanged, including the initial close reference with an unwanted person. Full prompts and generation receipts are retained. No fallback CLI/API was used.

Stage B was independently coordinate-authored directly at 314×206 (main scenes) and 564×278 (portrait layers), using Python/Pillow ImageDraw from a blank canvas. The editable `.py` files are the native sources. They never load source raster pixels. This is not a resized or palette-reduced reference. It is also not claimed to be image-model-generated native artwork.

Stage C scene previews are exact 1256×824 nearest-neighbor presentation exports. The main-scene NPCs remain small simple figures; no facial detail was added to room figures. The transparent portrait is separately authored.

Pinned main has no Chapter 4 artwork registry records or registered prompt fields. The complete relevant canonical source nodes are preserved verbatim in each version’s `evidence/canonical-requirements.json`, alongside the owner’s exact production brief. The artwork registry was not edited to fabricate source prompts.

## Quality review

The galleries contain four actual approved Chapter 2 environments, selected Chapter 1 artwork (v01), and the exact approved reception scene/portrait pair. Those production reception files were found in the playable checkout and verified byte-identical to the canonical selected images: 314×206 scene, opaque 564×278 background and transparent 564×278 foreground.

Comparison covers pixel size, detail density, silhouette, clusters, architectural edges, object readability, NPC scale and simplicity, and native/4× appearance. No color-count quota substitutes for artistic judgment. v02 still has flatter architectural surfaces and more angular portrait anatomy than the approved references. Later door removal, flooding, pod and stall/crane incidents are not claimed to be literally depicted by the establishing entry-state art.

## Validation

v01: 126 image/source/preservation/link checks pass. Gallery: 10 browser checks pass in Chromium and Firefox. Canonical storyboard smoke, canonical drift and sync QA (23 checks) pass.

v02: see `v02/evidence/validation.json` and `v02/evidence/browser-qa.json` for exact current results. Native replay disables raster open, resize, crop, filter, quantize and transform, and reconstructs the candidate PNG bytes exactly. This verifies the submitted native drawing pipeline, not artistic merit. Browser checks load the gallery under a GitHub Pages style prefix, decode images, exercise benchmark/1×/4× controls, and preserve native pixels on mobile.

Each version’s `manifest.json` records native/reference/preview dimensions and SHA-256. `SHA256SUMS` covers the entire final package except itself and ignored Python caches.

To rebuild v02, run from its `source/` folder:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 lobby.py
PYTHONDONTWRITEBYTECODE=1 python3 backdrop.py
PYTHONDONTWRITEBYTECODE=1 python3 auctioneer.py
PYTHONDONTWRITEBYTECODE=1 python3 package_review.py
PYTHONDONTWRITEBYTECODE=1 python3 validate.py
```

Browser verification requires Playwright and installed Chromium/Firefox. `qa-gallery.cjs` supports `PLAYWRIGHT_CHROMIUM_EXECUTABLE` and `PLAYWRIGHT_FIREFOX_EXECUTABLE` for existing browser installations.

Stop for Nate’s creative selection of the lobby and portrait standard before extending the revision to the remaining rooms or registering any approved candidates.

## Standing publication instruction — owner authorized November 21, 2026

Every completed artwork review version must be committed and pushed to its corresponding remote review branch automatically, including unselected candidates. Continue on `art/ch4-batch01-review-20261121` for this batch and establish its own remote tracking branch. Preserve every previous candidate and version, the native PNGs, exact 4× scene previews, unchanged detailed references, comparison images, prompts, manifests, hashes, QA and complete HTML gallery dependencies.

After pushing, verify the remote branch commit and accessibility of every referenced image. Return the exact commit SHA, clickable GitHub gallery/source and PNG comparison links, and a browser-rendered gallery when available. A local-only package is not a completed publication handoff. `verify-publication.py` in this directory audits raw GitHub files against the committed local image bytes and checks a read-only browser-gallery mirror; its remote verification report is written outside the package to avoid changing the commit being verified.

Review-branch publication does not approve artwork. Do not mark unselected candidates approved/integrated, merge them into main, replace approved selections, change narrative/gameplay files or modify the production Pages workflow to host the review. Creative selection remains Nate’s decision. This standing authorization requires no further publication request for subsequent review versions.
