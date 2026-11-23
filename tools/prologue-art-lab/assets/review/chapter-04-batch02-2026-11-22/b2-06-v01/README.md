# Chapter4 B2-06 v01 — Auctioneer and porter expression extensions

Six **UNSELECTED** transparent portrait foregrounds from the exact canonical B2-06 inventory: CH4-B2-31 auctioneer delighted;32 porter alarmed;33 porter curious;34 porter relieved;35 auctioneer disappointed;36 auctioneer bureaucratic. Eight authored nodes, no invented keys, dialogue or story requirements. [Canonical evidence](evidence/canonical-node-evidence.json), [manifest/hashes](manifest.json), [gallery](index.html), [all native](comparisons/all-native.png), [all exact4×](comparisons/all-4x.png).

## Actual production and provenance

Built-in `image_gen.imagegen` generated six detailed portrait references using the exact approved auctioneer/porter identities and approved Pavilion attendant/presenter as human anatomy/clothing benchmarks. A seventh built-in background-extraction edit corrected an unwanted gray halo in the relieved porter reference. Original first source, corrected cutout, exact prompts, input references and generation receipts are all preserved. No CLI/API fallback was used.

The high-resolution artwork is reference material, not a finished native asset. The native recipe fits a coherent local palette using **only opaque character colors**, so invisible background RGB cannot consume detail colors. It constructs a target-grid binary silhouette, removes detached fragments, merges tiny low-contrast surface islands, preserves coherent facial/hand features and material edges, repairs colored boundary fringe, clears hidden RGB and exports separate editable material masks/layers. A selective warm-plane pass quiets isolated skin/hand shade flecks without smoothing coherent wrinkles, dark pupils/brows/creases or white catchlights. Source transfer diagnostics are retained as diagnostics only. This follows the approved B2-04/B2-05 portrait approach, not a new simplified coordinate-drawn figure or broad procedural lighting pass.

Every new image is explicitly **SOURCE-DERIVED**, not independently authored whole-image native-grid artwork. Local64-tone fitting is a portrait production choice calibrated to approved work, never a universal cap or proof of artistic readiness. No dithering, random texture, smooth generated gradients or arbitrary global palette rule is introduced. [Exact derivation and native decisions](evidence/derivation.json), [source recipe](source/native_build.py), [prompts](prompts/), [generation receipts](evidence/generation-receipts.json).

## Identity, context and visual checks

The auctioneer retains normally proportioned elderly anatomy, silver hair/mustache, expressive brows, burgundy formalwear, dark lapels, bow tie, pocket square, gavel and both hands. Expressions remain restrained and recognizable. The porter retains his approved face, gray cap/jacket, open-neck cream shirt, clipboard and pencil; all caps, hands and gestures remain inside the frame. The clipboard uses non-letter ruled bars, not invented readable clues. No ring, staff pass, tag, new document wording or extra character is added.

Auctioneer poses composite over the exact approved lobby portrait background. Curious/relieved porter use the approved service passage. Alarmed porter includes both existing authored lobby and boiler-access contexts. These are review composites, not new backgrounds or runtime bindings. Approved Chapter3 human portraits establish anatomy/costume finish; Chapter2 Bureau/Control Tower establish deliberate cluster/material/light craft. Every candidate includes direct native/exact4× comparisons with both chapters at their actual grids, plus same-identity comparisons. [Visual assessment](evidence/visual-review.md). Technical dimensions/color counts do not establish owner approval.

## Reproduce

Use the Python/Pillow versions recorded in derivation.json:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/native_build.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

B2-05 is APPROVED/SELECTED unchanged on canonical main f068f1005d313a3e2869f332398a97e2e4c772db, PR26, docs/133: four blonde/green-eyed bride v02 PNGs and original clerk v01. All35 prior approved primary Chapter4 images, three conditional B2-04 references, all earlier approvals/reviews and unselected plumber alternatives remain unchanged. No narrative, gameplay, canonical registry, production assetPath or engine integration changes. New B2-06 candidates stay UNSELECTED pending Nate.
