# Chapter 4 B2-11 — public corridor approval and gameplay handoff

Nate approved **B2-11 dry v02 plus flooded v04** on **2026-11-25**, after native-resolution and exact nearest-neighbor 4× visual review. The dry master is **APPROVED / SELECTED** as one Chapter 4 scene. The flooded image is **APPROVED / PRESERVED AS A CONDITIONAL REFERENCE ONLY**; it is not another primary scene, Focus ID or runtime dispatch. Both files retain their original bytes and exact SHA-256 hashes. Earlier versions and editable source construction remain intact on the review branch.

**Immutable review source:** `InterstellarHarvest/CYOA-storyboard@6475c943f7383ea796e118c6d84b8760d0ccc12e`, branch `art/ch4-b211-public-corridor-review-20261124`, `tools/prologue-art-lab/assets/review/chapter-04-b211-public-corridor-2026-11-24/`.

| Unit | Selection role | Canonical/path | SHA-256 |
|---|---|---|---|
| `CH4-NEW-04` dry v02 | **APPROVED / SELECTED** | `scenes:grand_bellevue/public_corridor` → `assets/selected/pending-integration/scenes/grand_bellevue/public_corridor.png` | `86da5123204f65c43ed23f418fe0edcf987dbdb3d000821367c36c8f30c390ec` |
| `CH4-NEW-04` flooded v04 | **APPROVED / PRESERVED** | `tools/prologue-art-lab/assets/approved/conditional-production-references/chapter-04/b2-11/CH4-NEW-04-public-corridor-flood-v04.png` | `f802ff0c9aa345147f6039779df8b49403cc96add6be89b13f2ef9396727212f` |

Both PNGs are **314×206 opaque RGB**. The primary is copied from `v02/native/CH4-NEW-04-public-corridor-v02.png`; the preserved state from `v04/native/CH4-NEW-04-public-corridor-flood-v04.png`. Both are honestly **SOURCE-DERIVED**, with large source art used only as a reference for native structural/material construction. No wholly independent whole-frame native-grid authorship is claimed.

## Scene coverage and conditional handling

- `hotel_stall_public_corridor_walk`: dry hotel corridor with left STAFF/service door, recessed collection stairs and bright side exit. No extra guest portrait or new gameplay interaction.
- `hotel_flooded_public_corridor`: the **same** corridor geometry after flooding, with water over carpet, open maintenance hatch, a fallen/floating WET FLOOR sign and a gray-haired attendant at credible adult scale. The attendant is environmental dialogue staging, not a new portrait asset.
- The flooded reference has no dedicated new scene key, Focus ID, flag or runtime binding. **Gameplay PMO** will decide if/when the conditional state is displayed during later Chapter 4 integration without rewriting the authored story, and must preserve the selected dry master as the default. This artwork registration itself introduces no conditional dispatch.

`story/artwork.draft.json` marks `grand_bellevue/public_corridor` `approved`, `assetPath: null`; the suggested eventual engine destination is `art/scenes/grand_bellevue/public_corridor.png`. The selected public preview path is not an engine file path. Story nodes, dialogue, choices, inventory, flags, routes, UI and game integration are unchanged.

## Verification and preservation

The established `tools/sync/register-art.mjs` selected exactly one primary PNG after a successful dry run. Validate with `node tools/sync/check-canon.mjs` and `python3 tools/sync/verify-ch4-b211-selection.py`. The dedicated verifier compares against canonical baseline `5a4290d672e1904b4b5ad361562f05168c328a50`, checks exact selected and conditional PNG hashes/formats, preserves all **200 earlier selections** byte-for-byte and their metadata, confirms all previous art records and narrative/game-facing files are unchanged, and ensures the conditional flood file is *not* an extra selected key. Machine-readable results: `docs/144_CH4_B211_VERIFICATION_20261125.json`.

Do not modify draft PR #32, previously approved sources, main narrative/gameplay, or other reviews as part of this registration. After normal registration PR and publication, **next artwork group: B2-12** (`docs/138`) — bridal dressing room `CH4-NEW-01` and privacy panel Focus A `CH4-NEW-07`, with only required `bridal_privacy_status` supplemental states. New B2-12 candidates remain **UNSELECTED** until Nate's approval; apply the first-pass quality/stop rule rather than endlessly polishing.
