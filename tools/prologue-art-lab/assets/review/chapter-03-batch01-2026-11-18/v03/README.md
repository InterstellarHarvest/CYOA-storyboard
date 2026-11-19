# Chapter 3 Batch A v03 correction review

Six generated/unselected candidates, pinned to v02 commit `32273a2839e3a941530a153b69fb9a508e92f57b`. Open index.html for native/4x PNGs, six v02/v03 comparisons, before/after composites and white/dark silhouette proofs. Exact scope and offsets are in CHANGELOG.md; visual results and remaining concerns are in VISUAL_QA.md.

A01/A04/A05 are byte-identical carry-forwards. A02 changes only its declared device/shadow polygon. A03 moves +44/0; A06 moves -44/+29. Every visible sprite pixel survives unchanged at scale 1. No generation, face replacement, palette conversion, alpha threshold or global filtering is used.

Original native-grid authorship remains unproven. The soft source-derived RGB variation from v02 is retained honestly. A01's tiny device remains as an explicit continuity concern pending Nate's separate approval for a narrow correction.

Reproduce with Node and pngjs 7.0.0: `node edit-native.mjs` (`PNG_CODEC` may point to an existing installation). Package/independently validate using Python 3/Pillow: `python3 build_review.py`. Browser QA uses the existing Playwright 1.56.1 workflow; `PLAYWRIGHT_MODULE` and `GALLERY_URL` can choose an installation/server. Every historical review file is pinned in sources/history-pins.json. Pixel comparisons prove native edit scope; rgba translation and color/detail multiset checks prove lossless sprites. qa.json and browser-qa.json record results. PNG_SHA256SUMS.txt and SOURCE_SHA256SUMS.txt cover new package files.

Publish only with the existing isolated review-overlay Pages workflow, retaining public main content and restoring its branch protection after deployment. No main merge, canonical narrative/items change, production artwork import, approval, integration or Batch B generation. Stop after publishing for Nate's selection.
