# B2-11 v04 — adult doorway scale and clean clusters

Published2026-11-25 on `art/ch4-b211-public-corridor-review-20261124`. **UNSELECTED. Nate's visual approval pending.**

[Browser gallery](https://htmlpreview.github.io/?https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/20e5ba9a75551172bdc40f891f3389ff96bc8593/tools/prologue-art-lab/assets/review/chapter-04-b211-public-corridor-2026-11-24/v04/online.html) · [Full-scene v03/v04 comparison4×](https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/20e5ba9a75551172bdc40f891f3389ff96bc8593/tools/prologue-art-lab/assets/review/chapter-04-b211-public-corridor-2026-11-24/v04/comparisons/v03-v04-flood-4x.png) · [Character detail comparison4×](https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/20e5ba9a75551172bdc40f891f3389ff96bc8593/tools/prologue-art-lab/assets/review/chapter-04-b211-public-corridor-2026-11-24/v04/comparisons/character-sign-4x.png) · [Native flood](https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/20e5ba9a75551172bdc40f891f3389ff96bc8593/tools/prologue-art-lab/assets/review/chapter-04-b211-public-corridor-2026-11-24/v04/native/CH4-NEW-04-public-corridor-flood-v04.png).

Artwork commit `3639fb300a4f471ceb0cc71b636396fa0e7f8f6b`; immutable gallery/package commit `20e5ba9a75551172bdc40f891f3389ff96bc8593`. The final receipt commit preserves the tested package tree.

## Correction

The previous94px character was too short beside the doorway and the source reduction retained excessive shade texture. v04 rebuilds the same gray-haired female hotel attendant in navy work jacket/trousers from a dedicated clean-cluster source. Her native height is132px, with feet at the same193px floor boundary. The existing near STAFF-door leaf edge measures174px;132/174 is about76%. This is an image-scale calibration, not an exact physical-height claim.

Face, hair, hands, collar and structural cloth folds remain readable at native size and exact4×. The new source supplies clean connected material shapes; it is not an enlargement of the rejected94px image, another wrinkle pass or a whole-scene regeneration. The pointing action toward the staff passage and the professional identity remain consistent with `hotel_attendant:professional`. Staff Lavatory/Pavilion are rendering benchmarks, not borrowed character identities.

The v03 floating sign is unchanged, with17px horizontal bounding-box clearance from the new figure and no intersection with a10px expanded character silhouette. Room, doors, hatch, stairs, water, outside view and dry master remain exact. The new foreground figure naturally occludes a different set of room pixels; all composited changes lie inside the union of old/new figure silhouettes.

## Exact files and provenance

- Native flood314×206 RGB SHA256:`f802ff0c9aa345147f6039779df8b49403cc96add6be89b13f2ef9396727212f`.
- Exact1256×824 nearest-neighbor4× SHA256:`399b17c8b61e2ecbde7448cf5c6801cb4fe0479759c03b2955057d5bb0fb7bce`.
- Unchanged dry candidate SHA256:`86da5123204f65c43ed23f418fe0edcf987dbdb3d000821367c36c8f30c390ec`.

SOURCE-DERIVED. Built-in `image_gen` produced the preserved clean-cluster character source; exact prompt, original PNG, input roles and hashes are in [generation provenance](v04/evidence/generation-provenance.json). The132px object interpretation uses coherent material ramps, binary alpha and limited tiny-cloth-island cleanup, without blur or stochastic dithering. Full-image independent native authorship is not claimed. One native figure layer changes;15 other layers remain reused from earlier packages. No new portrait or runtime key is registered.

## Verification

- 73 native/source/preservation checks pass, including exact scene assembly and deterministic replay.
- Native height94→132; foot boundary193 unchanged; door-scale record174; sign gap17;10px silhouette clearance passes.
- Zero changed pixels outside old/new character silhouettes. Dry PNG exact; sign layer exact.
- All94 v01,107 v02 and45 v03 files remain byte-identical;199 approved files and920 protected baseline blobs remain exact.
- Public verification:all52 package files match pinned bytes; all33 PNGs decode.
- Actual public Chromium/Firefox gallery:PASS,18 integer native/exact4× figure checks.
- Canonical main remains `5a4290d672e1904b4b5ad361562f05168c328a50`; PR32 branch remains `f320e63934c13e27fd13b9482d0cfba58911362d`.
- No narrative/gameplay, approved image, selection record, runtime binding or engine integration changes.

[Public bytes](V04-PUBLIC-BYTE-VERIFICATION-20261125.json) · [Public browsers](V04-PUBLIC-BROWSER-VERIFICATION-20261125.json) · [Native QA](v04/evidence/validation.json) · [Visual review](v04/evidence/visual-review.md) · [Method and saved source](v04/README.md).
