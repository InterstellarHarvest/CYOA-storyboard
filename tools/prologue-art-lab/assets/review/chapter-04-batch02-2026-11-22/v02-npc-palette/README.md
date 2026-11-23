# B2-01 plumber portraits - compact palette v02

**UNSELECTED**. Two NEW UNSELECTED palette alternatives. Approved v01 images remain registered and unchanged. Their character designs/poses guide the new stepped-ramp illustrations; geometry/alpha are not claimed pixel-identical after reillustration. Coherent64-tone final NPC ramps match the reduced-tone Chapter1/2 direction; detail is carried by features, hands, hair, seams and folds rather than gradients or grain.

The approved background, receipt Focus A and master-isolator Focus A are unchanged. Eddie still holds the readable LOT14 receipt. The two internal quantization-only diagnostics are retained as diagnostics, not final review candidates. Source-derived reillustration originals, exact prompts and final palette recipe are preserved.

[Native/exact4x gallery](index.html), [manifest and exact hashes](manifest.json), [comparison PNG](comparisons/plumbers-v01-v02-native.png), [4x comparison](comparisons/plumbers-v01-v02-4x.png).

The built-in image_gen.imagegen tool generated the original illustrations; every source, exact prompt, generation receipt and input benchmark is preserved. Source-derived quality-first workflow: new stepped-ramp source -> nearest564x278 -> binary alpha cleanup -> compact64-tone no-dither fit, then composites on the exact frozen approved background. Never claim independent native-grid authorship. The64-tone NPC target is calibrated to actual Chapter2 references (50/61); environment colors are not forced under the same cap. No mathematical gradients or new anatomical shading are synthesized. Native/4x artistic comparisons matter more than counts.

Approved v01/B1 images are never reprocessed or overwritten. New palette alternatives do not replace an owner selection automatically. Canonical registration is on main at fde5708e0043972feeae0309e8a1d1836e756dae (PR21); runtime assetPath remains null until separate verified game integration, per docs105/127/128. No narrative/gameplay/workflow changes.

Reproduce with the recorded Pillow version:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/prepare.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

Originals/prompts: [generation receipts](evidence/generation-receipts.json); final derivation: [palette treatment](evidence/palette-treatment.json). Source/qa-gallery.cjs exercises every native/exact4x control in Chromium/Firefox. Public file verification compares every published byte to the local package, with its output outside the commit.
