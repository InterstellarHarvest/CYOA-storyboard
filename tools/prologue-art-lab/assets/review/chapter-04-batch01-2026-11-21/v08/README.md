# Chapter4 v08 — final auctioneer review, exact Batch1 freeze, Batch2 inventory

All artwork remains **UNSELECTED**. The four preferred environment candidates are frozen exactly: CH4-01/02 **v05** and CH4-04/05 **v07**. Their existing PNGs, exact hashes, manifest paths, canonical logical keys and provenance are resolved in [the freeze record](evidence/frozen-preferred-environments.json). No cosmetic environment revision or replacement export was made.

The auctioneer retains the preferred `portrait-study-02` design from commit `2a267beaf182fa6b589d7256ae813de8b168e63a`. The unchanged 1788×880 original is reduced using the authorized quality-first **source-derived** workflow to 564×278 transparent RGBA. The successful v06 cutout cleanup is retained, then existing facial/hair/hand/gavel/tailoring contrast is clarified selectively at final resolution. This uses no new character generation, coordinate reconstruction, palette quota or anatomical repaint. The final alpha channel and silhouette match v06 exactly; near-transparent boundary colors are preserved. [Processing source](source/portrait.py), [exact derivation](evidence/portrait-derivation.json), [original generation prompt](../portrait-study-02/prompts/approved-npcs-only.txt), [unchanged original provenance](../portrait-study-02/evidence/generation-receipt.json).

[Open the final portrait gallery](index.html). Native and exact4× views compare actual artwork with approved Pavilion attendant/presenter, the preferred diagnostic and the unchanged original. The final foreground is composited over the exact frozen CH4-02 v05 background, with dark/light alpha-edge checks. Only the strongest internally compared finish is published; no processing trials are review candidates.

Deliverables:

- [Batch1 selection-ready summary](BATCH1-SELECTION-READY.md), including all five exact hashes and repository paths. Formal registry approval and production integration are separate; no canonical production `assetPath` is fabricated where no CH4 registry record exists.
- [Batch2 onward artwork inventory](BATCH2-INVENTORY.md), [full JSON](BATCH2-INVENTORY.json) and [120-node coverage table](BATCH2-NODE-COVERAGE.tsv). Explicit scene, speaker/pose, Focus A, existing item-art and fatal `artRef` demands are extracted from current canonical sources. Narrative-derived state families, reuse options and unresolved inline/voice mappings are labelled separately.
- Recommended first group **B2-01 — Public restroom dialogue and controls**, five units: closer background; plumber worried; assistant pleased; Lot14 receipt Focus A; emergency cabinet/master isolator Focus A. No Batch2 artwork generation has started.

The canonical snapshot is current public main `622ad879dfe187ff2683ae7072515ed740522243`. Its Chapter4 has the same 120 approved nodes as this checkout. The only relevant-file difference from this review branch is an unrelated Chapter3 approval-note update in the artwork registry. [Source file hashes/snapshots](evidence/canonical-sources.json) preserve current evidence; canonical files are not edited.

Reproduce from this directory with the recorded Pillow version:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/portrait.py
PYTHONDONTWRITEBYTECODE=1 python3 source/inventory.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package_review.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

QA checks final dimensions/alpha, exact4× pixels, exact replay, interior-only cleanup, silhouette/boundary preservation, frozen hashes, every earlier-version byte, canonical snapshot hashes, exact inventory key sets and node coverage, and gallery dependencies. Browser QA checks portrait/approved comparisons, composite, frozen-file1×/4× controls and mobile pixel preservation. Technical passing does not register art approval.

Publication stays on `art/ch4-batch01-review-20261121`. Preserve all older files. No production, narrative, gameplay, approval-record or main changes. Remote verification reports are stored outside the package so they do not change the commit being verified.
