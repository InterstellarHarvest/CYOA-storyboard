# Chapter4 B2-11 v02 — targeted correction publication

Published2026-11-25 on `art/ch4-b211-public-corridor-review-20261124`. **UNSELECTED. Nate's visual approval pending.**

[Browser gallery](https://htmlpreview.github.io/?https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/4cd05a374964bd3b499ba0637f5ddd0bc11f2517/tools/prologue-art-lab/assets/review/chapter-04-b211-public-corridor-2026-11-24/v02/online.html) · [Dry before/after4×](https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/4cd05a374964bd3b499ba0637f5ddd0bc11f2517/tools/prologue-art-lab/assets/review/chapter-04-b211-public-corridor-2026-11-24/v02/comparisons/dry-v01-v02-4x.png) · [Flood before/after4×](https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/4cd05a374964bd3b499ba0637f5ddd0bc11f2517/tools/prologue-art-lab/assets/review/chapter-04-b211-public-corridor-2026-11-24/v02/comparisons/flood-v01-v02-4x.png) · [Staff Lavatory comparison4×](https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/4cd05a374964bd3b499ba0637f5ddd0bc11f2517/tools/prologue-art-lab/assets/review/chapter-04-b211-public-corridor-2026-11-24/v02/comparisons/staff-lavatory-benchmark-4x.png).

Artwork commit `b67e45d6367a697f8b9b349d0ee91baff64d7daf`; immutable public-gallery commit `4cd05a374964bd3b499ba0637f5ddd0bc11f2517`. The final receipt commit adds no changes to the tested v02 package.

## Owner-requested corrections

1. Recognizable loading-yard view with canopy, building wall, louver, paving and actual jamb replaces the blank beige side-exit plane and isolated X.
2. Far doors share a205,115 vanishing point for head, base and panel edges, while their jambs remain vertical.
3. Closed/open hatch share the same fixed frame and left hinge endpoints; the outward leaf has a nearer/taller free edge and a visible recessed pipe opening.
4. Larger, illustrated scene attendant: 94 native pixels tall instead of 43, with readable hair, face, hands, uniform and shoes.

The owner corrected the initial study's resemblance to the wedding assistant before publication. Canon was rechecked: `hotel_flooded_public_corridor` uses `hotel_attendant:professional`; she loses the WET FLOOR sign and points toward the staff passage. The final gray-haired woman in a navy work jacket/trousers is distinct from `hotel_wedding_assistant`. Staff Lavatory is a detail benchmark only. The earlier lookalike source and exact prompt are retained as **rejected source material, not a candidate**. Age/hair/uniform are art-direction choices, not added canonical facts. The final sign stays fallen and floating.

## Exact assets

| Role | Native PNG SHA-256 |
|---|---|
| CH4-NEW-04 dry | `86da5123204f65c43ed23f418fe0edcf987dbdb3d000821367c36c8f30c390ec` |
| Flood conditional reference | `eda5fa7da5c2ed85c4333993c6b9b0503d3f36ab72078fa831ffa50f8bf6d358` |

314×206 opaque RGB; exact1256×824 nearest-neighbor4×. Paths, preview hashes and existing node mappings are in [v02/manifest.json](v02/manifest.json). One primary and one conditional reference; no extra portrait, scene key, Focus ID, flag or runtime binding.

SOURCE-DERIVED. Original room sources stay preserved in v01. Native door/hatch geometry and local material/yard reconstruction are reproducible. The final scene-NPC source was generated with built-in `image_gen`, then processed at object size with coherent material ramps, binary transparency and limited weak-cluster cleanup. No whole-scene resize or independent-native-authorship claim. Original generated PNGs, exact prompts, repair geometry and editable layers are retained in v02.

## Verification

- 158 targeted checks pass, including local-change boundaries, projected door corners, fixed hinge anchors, source hashes and deterministic replay.
- All corrections stay within the four intended repair regions and small foot-contact area. Dry/flood state differences stay inside their localized state masks.
- Nine original dry layers remain byte-identical. Twelve structural/repair layers are shared by the dry and flooded frames.
- All94 v01 files and199 approved files remain exact; all756 protected baseline blobs are preserved.
- Public verification:all107 v02 files byte-identical to the pinned commit; all85 PNGs decode.
- Actual public Chromium/Firefox gallery:PASS, 36 figure checks with integer native and exact4× controls.
- Canonical main remains `5a4290d672e1904b4b5ad361562f05168c328a50`; PR32 branch remains `f320e63934c13e27fd13b9482d0cfba58911362d`.
- Narrative, gameplay, production selections, approved artwork, engine integration and PR32 are unchanged.

Receipts: [public bytes](V02-PUBLIC-BYTE-VERIFICATION-20261125.json), [public browsers](V02-PUBLIC-BROWSER-VERIFICATION-20261125.json), [native QA](v02/evidence/validation.json), [source/identity provenance](v02/evidence/generation-provenance.json), [flood4× browser screenshot](v02-public-browser-20261125/firefox-flood-4x.png).
