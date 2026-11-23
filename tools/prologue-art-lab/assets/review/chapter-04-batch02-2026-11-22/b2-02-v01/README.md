# B2-02 - Loading dock and service arrivals v01

**UNSELECTED**. Six NEW UNSELECTED candidates: four main scenes, one transparent detailed foreman portrait and one matching empty conversation background. All are disclosed source-derived production exports. Main-scene NPCs remain simpler and properly scaled; the detailed foreman uses the compact Chapter1/2-style stepped palette. No invented story nodes or engine integration.

The canonical seven-node group covers loading lane, service alley, loading dock, service stairs and the annoyed salvage foreman. The truck/staircase, sofa/trolley, chandelier hoist/padded container, two piano workers plus foreman, cake trolley and side gate follow their source nodes. The dialogue background contains no NPC. The side-gate view shows ordinary park vegetation only, no future-chapter hazard or bathroom sign. Internal staging corrections preserve all other reduced pixels before the recorded native finish.

[Native/exact4x gallery](index.html), [manifest and exact hashes](manifest.json), [comparison PNG](comparisons/B2-02-all-native.png), [4x comparison](comparisons/B2-02-all-4x.png).

The built-in image_gen.imagegen tool generated the original illustrations; every source, exact prompt, generation receipt and input benchmark is preserved. Source-derived quality-first workflow: new composed environment sources -> controlled native transfer/finish; foreman -> nearest564x278, binary cutout and compact64-tone no-dither fit. Main scenes314x206, opaque background564x278, foreground564x278 transparent. Never claim independent native-grid authorship. The64-tone NPC target is calibrated to actual Chapter2 references (50/61); environment colors are not forced under the same cap. No mathematical gradients or new anatomical shading are synthesized. Native/4x artistic comparisons matter more than counts.

Approved v01/B1 images are never reprocessed or overwritten. New palette alternatives do not replace an owner selection automatically. Canonical registration is on main at fde5708e0043972feeae0309e8a1d1836e756dae (PR21); runtime assetPath remains null until separate verified game integration, per docs105/127/128. No narrative/gameplay/workflow changes.

Reproduce with the recorded Pillow version:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/prepare.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

Originals/prompts: [generation receipts](evidence/generation-receipts.json); final derivation: [derivation](evidence/derivation.json). Source/qa-gallery.cjs exercises every native/exact4x control in Chromium/Firefox. Public file verification compares every published byte to the local package, with its output outside the commit.
