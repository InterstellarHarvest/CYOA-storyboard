# Chapter 4 B2-05 v01 — Bride and auction clerk

Five **UNSELECTED** transparent portraits: bride determined / hopeful / grateful / helpful, plus the precise auction clerk. Exact canonical inventory and six authored nodes are preserved in [node evidence](evidence/canonical-node-evidence.json). No added dialogue, props, items, characters, story modes or runtime bindings. The approved lobby conversation background is reused byte-exact, never repainted.

## Production and provenance

Built-in `image_gen.imagegen` generated five detailed character references using approved Pavilion attendant/presenter artwork as the primary style inputs and the approved groom as local wardrobe context. The four bride poses retain one design. [Exact prompts](prompts/) and [generation receipts](evidence/generation-receipts.json) preserve all input references and saved originals. No external CLI/API generation fallback was used.

The high-resolution artwork is reference material. A direct native transfer is retained only as a diagnostic. Following the approved B2-04 portrait method, `source/native_build.py` constructs the 564×278 foreground through a local coherent palette fit, protected face/hand/prop regions, selective native low-contrast cluster merging, binary silhouette construction, detached-fragment removal, native contour fringe repair, zero hidden RGB and separate editable skin/hair/fabric/object masks and layers. Source colors are retained intelligently: broad material classification must not recolor anatomy, stipple faces or turn red tickets brown. Rare pale-blue ribbon and silver-band material ramps are explicitly preserved in the grateful pose. This is more than a resize or global color-count exercise; visual comparison remains the gate.

All exports are explicitly **SOURCE-DERIVED**, not independently authored whole-image native-grid artwork. Local 64-tone fitting follows the approved portrait studies, with extra rare-object material ramps where necessary. It is not a universal cap. No dithering, smooth gradient synthesis or random noise is added. [Exact derivation](evidence/derivation.json).

The bride's hopeful pose has no ring in her hands: the player still owns it. Grateful receives the silver ring and pale-blue ribbon. Helpful carries no key: the organizer holds it in the story. The male clerk holds the authored red carbon-copy ticket pad and ordinary stamp; paper contains non-letter form bars, not invented clue text. The actual inspection artwork and inventory images remain separate later groups.

Every candidate has direct native/exact4× comparisons with approved Chapter 2 groundskeeper and Pavilion presenter, plus a composite over the unchanged approved lobby background. Bureau, Control Tower and Pavilion attendant benchmarks are also preserved. Native exports are564×278 RGBA; exact4× exports2256×1112. [Gallery](index.html), [all native](comparisons/all-native.png), [manifest/hashes](manifest.json), [visual assessment](evidence/visual-review.md).

## Reproduce

Use the recorded Pillow version in `evidence/derivation.json`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/native_build.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

All B2-04 approvals and earlier artwork/history remain byte-exact. Main's B2-04 completion is8a5b91f4effabda5e6ebb5f53f317850931db68b, PR25, docs/132. Seven primary images are approved/selected; three supplemental states are approved/preserved conditional references only. No new Focus IDs or state bindings. Alternative B2-01 plumber portraits remain UNSELECTED; original v01 approvals stay selected. This review alters no canonical story file, selected image, narrative, gameplay or engine integration.
