# Auctioneer restart — approved NPC style first

**UNSELECTED fresh style candidate.** Nate directed a restart using the two approved Pavilion NPCs as the style references: simply an old man with a gavel and the suit. The detailed auctioneer drawing and all previous auctioneer versions were excluded from the generation inputs. Only the approved Pavilion attendant and Pavilion presenter were supplied to built-in `image_gen.imagegen`.

The fresh illustration uses cleaner contours, broad sculpted silver hair, a normally proportioned elderly face, a restrained expression, burgundy formalwear and a natural chest-height gavel grip. The intended finish is the approved NPCs' illustrated face, hair, hand and clothing treatment, rather than reducing a highly rendered concept painting. It is a fresh character construction, not a small-mark pass over v05. Owner review must decide whether it fits the existing NPC family. The head has a slight tilt; the face and torso face the viewer.

[Open the gallery](index.html), [view the exact prompt](prompts/approved-npcs-only.txt), or [inspect the generation receipt](evidence/generation-receipt.json). The original generated PNG is preserved unchanged at `generated/CH4-03-auctioneer-fresh-style-original.png`.

The tool returned **1788×880 RGBA**, despite the requested 564×278 canvas. This is a style-review candidate, not a production-ready native asset. The gallery deliberately includes a **source-derived layout diagnostic** at 564×278 so the design can be compared at the approved NPCs' display scale. That diagnostic is a nearest-neighbor resize, is labelled source-derived in its file name/PNG metadata/manifest/gallery, and is never described as independent native-grid authoring. Its exact 4× preview is an inspection export only. No production/native directory or asset registration is created. The full original and its exact 4× export are also supplied. Repeating a size request does not prove native authorship.

The comparison PNG places the fresh source-derived layout, approved attendant, approved presenter and preserved v05 portrait side by side. The three existing images are pasted at their true native size. Only the new panel is rescaled for this diagnostic, explicitly labelled. This allows style and character review without presenting a resized image as finished game art.

CH4-01 lobby and CH4-02 background remain frozen at v05 with their exact hashes. All v01–v05 files and the previous method study remain unchanged. Everything new remains UNSELECTED. No main, narrative, gameplay, approval registry, production workflow, restroom or ballroom changes are part of this publication.

Reproduce presentation exports from the unchanged original, not the stochastic generative call:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/package_review.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

The `.py` files package and validate presentation only; they do not draw the portrait. Input hashes, prompt, receipt, original output, diagnostic provenance, comparisons, exact 4× previews and browser QA are preserved. Publication is to `art/ch4-batch01-review-20261121` under Nate's standing instruction. This publication does not approve the character or satisfy the unresolved independent native-grid production contract.
