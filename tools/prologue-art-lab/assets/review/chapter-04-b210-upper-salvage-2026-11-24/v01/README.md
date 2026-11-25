# Chapter4 B2-10 / CH4-NEW-03 — upper salvage v01

**Visual gate not fully met — not selection-ready.** One **UNSELECTED**314×206 opaque RGB candidate and exact1256×824 nearest-neighbor preview. Proposed future key `scenes:grand_bellevue/upper_salvage`; no registration or runtime binding is performed. [Gallery](index.html) · [manifest / hashes](manifest.json) · [Chapter2 native comparison](comparisons/chapter2-native.png) · [Chapter2 exact4×](comparisons/chapter2-4x.png).

## Authority and scope

The exact parent [BRIEF.md](../BRIEF.md) is the controlling production directive, pinned at review base `60c0569856eec3c5319dcac060875054ac2e955a`. Canonical story/art baseline is `6334b895333dd2d78332cf9f1d834e619468f932`; remote main was observed at `b8a8e4ea3c6d13141b2e33d281ba864c3b2aec42` (subsequent smoke-count repair). No merge from main is needed for this art-only branch. Docs129/138 and all three required narrative nodes were read in full. [Pinned node evidence](evidence/canonical-node-evidence.json), [composition plan](evidence/composition-plan.json).

The lift, open maintenance hatch and descending service stairs are distinct in one shared room. The lift's native `W.C.` label belongs to its three-button panel; it means Warehouse Collection. Dismantled sinks, mirrors, stored toilet bowls and partition leaves are supported as salvage, with loose outlets and no connected/usable toilet. The central floor stays open. No clerk, protagonist, character, suspended stall, conditional crane accent, extra state, separate freight-lift image, new Focus ID or flag is produced.

The voice-only clerk/voice and actual dialogue are untouched. Main, selected/approved PNGs, narrative, gameplay, integration and draft PR32 are unchanged. This package stops at B2-10's visual-review gate; it does not start another group.

## Actual native production method — SOURCE-DERIVED

1. Inspected actual approved Chapter2 Control Tower, Damaged Walkway and Maintenance Exit at native and exact4×. Also inspected approved Chapter4 Service Stairs, Loading Dock and Lobby at both scales. Exact copies/hashes are preserved in `references/` and [benchmark provenance](evidence/canonical-benchmarks.json).
2. Planned independent native route geography before generation. Built-in `image_gen.imagegen` produced two preserved large references: composition/material concept, then a material study. Both exact prompts, ordered inputs and original PNGs are archived. The references establish form/material ambition; they are not the final image.
3. `native_scene.py` starts with a blank314×206 RGBA canvas and reads **no reference raster**. Its independent native silhouettes/planes construct the architecture, floor, lift, hatch, shelves, disconnected sanitary objects, duct, lamps, descending stairwell, guardrails and chunky bitmap W.C. panel. Every polygon, curve, contour, rim/cavity, drain/faucet hole and material ramp is defined at the actual grid. Ten structural layers and masks are editable. No half-resolution sample, blur, antialias filter or post-sharpening is used.
4. The forms-only studies were internally rejected for flat rendering. The final is a **hybrid source-derived interpretation**: `native_materials.py` derives a full-native-grid tonal guide from the material reference and uses it to choose discrete material-ramp shades inside the independently drawn layers. The native depth planes remain dominant; source RGB is never pasted into the master. Isolated guide grain is suppressed. Native silhouettes, contours, W.C. panel and critical drain/faucet sockets are protected. This reference-guided shade interpretation is explicitly disclosed, not claimed as wholly independent artwork or manual authorship of every final pixel. [Material method and final layer order](evidence/material-interpretation.json).
5. Final foreground/architecture is assembled from the ten material-interpreted native layers. The final is not a resized source, a palette-reduced source offered as finished artwork, or the initial forms-only study. Direct-resize diagnostics and rejected studies are labeled under `evidence/internal-study/`. [Production process comparison](comparisons/production-process-native.png).

Only coherent local ramps are used; there is no arbitrary global64-color rule. [Actual palette/component measurements](evidence/palette-and-clusters.json) are diagnostic, not approval. W.C. uses explicit native bitmap glyphs on a frontal rear-wall panel, with three buttons below. No other tiny pseudo-text appears in the finished scene.

## Visual assessment and limitation

The final geography and story objects read at actual314×206; at4× the edges remain hard and connected rather than blurred. Native metal, cream porcelain, leaning glass, wood and painted/plaster surfaces have distinct ramps and contact/depth groups. Main-scene detail is deliberately quieter than the detailed reference.

**Remaining visual limitation:** rear-rack sanitary fixtures are more schematic than Chapter2's strongest object modelling. This concern is carried prominently into the gallery/manifest for Nate; the package does not claim aesthetic approval or automatic selection readiness. The pure coordinate studies were not promoted as candidates. [Detailed internal assessment](evidence/visual-review.md).

## Reproduce and verify

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/native_scene.py
PYTHONDONTWRITEBYTECODE=1 python3 source/native_materials.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package_review.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

[Native structural assembly](evidence/native-assembly.json) records the underpainting; [final material assembly](evidence/material-interpretation.json) records the production layer stack/hash. All finished semantic layers are `layers/material-*.png`; structural masks are under `masks/`. Both stacks remain editable. Original references/prompts remain untouched.

The gallery uses actual integer-size native and4× PNGs with horizontal scrolling for wide comparisons. It never fractionally shrinks4× to fit. Technical QA verifies dimensions/mode, exact scaling, native lettering, semantic layer reconstruction, palette membership, reference/source hashes, story scope, deterministic replay and preservation of the baseline. Public byte verification and real Chromium/Firefox controls are recorded after publication. Technical passes do not constitute Nate's approval.

The available coordinate/native-material workflow has not reproduced the richest Chapter2 fixture modelling. A further wrinkle/highlight/material-shading pass is not the proposed remedy. Practical handoff: a pixel illustrator can repaint the existing native porcelain/rack layers at314×206 using the approved Chapter2 files, retaining the three-route geometry and exact W.C. bitmap. Publish a later version only after its actual form modelling passes that comparison. No replacement selection or policy exception is assumed here.
