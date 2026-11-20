# Chapter 3 Batch D — unselected review-gallery publication proposal

The nine remaining active Chapter 3 artwork requirements now have generated candidates. This proposal publishes their review package through the existing protected `main` Pages workflow so Nate can review native images, exact 4× previews, composites, continuity references, prompts, originals, derivations and SHA-256 hashes.

- Immutable complete gallery source: `InterstellarHarvest/CYOA-storyboard@3931c496c13c691c8afa3c5206d4f56196c372fc`, branch `art/ch3-pavilion-batch04-20261120`.
- Exact candidate/original source commit recorded in the nine generated catalogue entries: `4fc277651c7d05163817d9ab99d0fc3fcf522d47`. Candidate bytes are unchanged between these commits.
- Package: `tools/prologue-art-lab/assets/review/chapter-03-batch04-2026-11-20/v01/`.
- Proposed gallery after a separate merge and successful main deployment: https://interstellarharvest.github.io/CYOA-storyboard/tools/prologue-art-lab/assets/review/chapter-03-batch04-2026-11-20/v01/.
- [Inventory, hashes, QA and Art Director questions](120_CH3_BATCH_D_GENERATION_AND_REVIEW_20261120.md). [Publication validation](121_CH3_BATCH_D_PUBLICATION_VALIDATION_20261120.json).

Only nine previously `not-started` records advance to `generated`, with exact source commit/path/hash provenance and null production paths. No selected preview entry is added. Twenty approved active Chapter 3 images are reused; all selected artwork, historical packages, narrative and the private game remain unchanged.

The workflow sparse-checks out the pinned package and runs a trusted helper from main. It validates all 111 package files/checksums, nine candidate PNG contracts, generated/unselected flags, source and reference hashes, 34-node coverage and QA receipts, then stages identical bytes. Gallery Python/JavaScript files are data and are never executed by the publication workflow. Deployment provenance is written outside immutable `v01`.

All prior workflow bytes remain identical after removing the two Batch D environment pins and its checkout/staging steps. Main-only triggers, `refs/heads/main` job guard, permissions, environment and Batch A/B/C pins remain unchanged. The draft PR is a reviewable publication proposal; it does not merge, dispatch Pages, deploy directly from an art branch, approve candidates, or integrate gameplay.

Image QA, canonical drift, Chapter 3 briefs/narrative, sync 22/22, storyboard smoke, gallery Chromium/Firefox checks, storyboard browser 24/24, selected-art browser 60/60 and repaired Prologue built-site browser 70/70 pass. The actual main build step plus pinned-package staging helper passes locally. Original native-grid authorship remains unproven and is explicitly documented; technical passing is not visual approval.
