# Chapter 3 Batch A v02 correction review

Six generated/unselected corrections, derived from pinned v01 commit `99b74b63a3407aafe7a468c2915291c997563700`. Open index.html for native and 4x views, six v01/v02 comparisons, composite comparisons, white/dark silhouette proofs, exact edit prompts, original source filenames and hashes. The original v01 gallery remains one directory above, completely unchanged.

Native files are under candidates/, previews under previews/, composites under composites/, and original tool edits under generation-source/. The built-in image_gen tool supplied six targeted edits. Full edit prompts and ordered reference hashes are in prompts/ and sources/edits.json. Raw tool files remain immutable.

These are DERIVED native realizations. The generator returned larger rasters. realize.mjs discloses pixel-center transfer into the native canvas, followed by hand-specified repair-plate painting, a shared native bitmap countdown family, and manually traced foreground silhouettes/contour inks with fixed integer anchors. Candidate outputs are not merely the transfer-only studies; those studies remain separately labelled under construction-guides/. No global palette quantization, blur, dithering or source-alpha threshold is used. A palette-reduction experiment was rejected during inspection and is not a review candidate.

The entire image has NOT been redrawn pixel by pixel at native resolution. Original-native authorship and wholly deliberate native pixel-cluster shading therefore remain unproven. Fine RGB tonal variation from the tool renders remains. Correct dimensions and local native work do not override this failure.

Strict binary alpha, head/bottom clearance, the native 30 digits, exact 4x pixels, literal composites and v01 preservation are validated in qa.json. Hand-authored silhouettes and future pose anchors are supplied in sources/silhouettes.json. The final presenter silhouette replaces a large bad halo in the generated edit; it is not extracted by alpha threshold. Only idle poses exist.

Rebuild with Node and pngjs 7.0.0 (`PNG_CODEC` may point to its installation): `node realize.mjs`. Then use Python 3/Pillow: `python3 build_review.py`. Browser QA uses the established Playwright 1.56.1 pipeline; `PLAYWRIGHT_MODULE` and `GALLERY_URL` can select a local installation and server. Rebuilding never edits v01 or protected canonical files. PNG_SHA256SUMS.txt and SOURCE_SHA256SUMS.txt cover the new package.

Publication uses the existing review overlay Pages workflow, building the current public site from main and adding this isolated review package only. No public-main commit, narrative/gameplay/item change, approval or integration is authorized. Stop at Nate's selection gate; no Batch B generation.
