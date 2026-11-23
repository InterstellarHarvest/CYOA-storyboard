# B2-02 v02 — four-scene native pixel-art reinterpretation

All four revisions are **UNSELECTED**. This follows Nate's permanent standard and final hierarchy in canonical docs129/PR22. Main scenes314x206; portraits/backgrounds and Focus564x278 retain their own richer detail requirements. No universal palette-count target is imposed.

## Actual production method

1. Preserve the original detailed concepts and all historical native PNGs unchanged.
2. Built-in image_gen.imagegen makes a **separate pixel-friendly interpretation**, guided primarily by approved Chapter2 Bureau/Control Tower. Prompts, inputs and receipts are retained; this source is not called finished art.
3. A nearest target-grid transfer is saved as a **diagnostic underpainting only**.
4. At314x206, authored semantic masks distinguish floor, wall, steel, wood/copper, occluded props and NPC regions. Material-specific ramps are selected; quiet one/two-pixel low-contrast texture components are merged while structural seams, lights, hardware, brick, features and object contours are protected.
5. A separate native RGBA construction layer rebuilds elevator panel geometry, perspective floor grout, explicit light/shadow planes and wear clusters, beam/duct edges, stairs/rail silhouettes or piano keys/rim, exterior drainage and threshold details. These are target-grid drawing decisions beyond palette fitting; the JSON guide and transparent layer expose them for correction.
6. NPC regions are saved as separate editable layers. Tiny figures use clothing/pose/cap and concise skin/hand clusters, not portrait-level anatomy. Final opaque native PNGs and exact1256x824 nearest4x views are exported.

**SOURCE-DERIVED native reinterpretation**, not independently authored whole-image native art. Some source-defined object contours remain; the method is neither a complete manual repaint nor a direct resize/quantization-only finish. No blur, unsharp filter, gradient synthesis or dithering is used in this pass. Scripts and layers make the actual work reproducible; visual approval remains Nate's decision.

## Review material

[Gallery](index.html), [manifest/hashes](manifest.json), [v01/v02](comparisons/v01-v02-native.png), [exact4x](comparisons/v01-v02-4x.png), [canonical comparisons](comparisons/canonical-native.png), [canonical4x](comparisons/canonical-4x.png), [native construction stages](comparisons/native-construction-native.png). Detailed source originals, pixel-friendly sources, masks, layers, prompts, generation receipts and diagnostics are preserved. Palette/component counts are diagnostic evidence only.

The exact v01 foreman and background remain UNSELECTED retained candidates. No portrait/background cosmetic rework or silent approval occurs here. All ten approved Chapter4 PNGs, the two plumber palette alternatives and every prior review version remain unchanged. No narrative/gameplay or engine integration.

Reproduce with the recorded Pillow version:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/native_rebuild.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```
