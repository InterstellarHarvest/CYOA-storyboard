# Chapter 4 B2-10 — owner-approved upper salvage v03 registration

Nate approved **B2-10 v03 / CH4-NEW-03** on **2026-11-24** after native-resolution and exact-nearest-neighbor 4× review. The upper-salvage mezzanine scene is **APPROVED / SELECTED** on this registration branch, pending normal PR and canonical-main publication. **No pixels have been modified, downscaled, re-encoded or regenerated.** Earlier review versions and source-derived editable layers remain on the art review branch.

| Field | Exact approved selection |
|---|---|
| Canonical artwork key | `scenes:grand_bellevue/upper_salvage` |
| Asset ID | `CH4-NEW-03` — upper salvage mezzanine |
| Selected PNG | `assets/selected/pending-integration/scenes/grand_bellevue/upper_salvage.png` |
| SHA-256 | `1030e04f9b32d2c0fc4394e9f00a4a70ba162db1c9eeed4f2772068cf9ce3207` |
| Format | 314×206 opaque RGB PNG |
| Immutable source commit | `7963f507568a6e6f9a50ffda3755103f9674bdd3` |
| Source branch | `art/ch4-b210-upper-salvage-review-20261124` |
| Exact source path | `tools/prologue-art-lab/assets/review/chapter-04-b210-upper-salvage-2026-11-24/v03/native/CH4-NEW-03-upper-salvage-v03.png` |
| Provenance | SOURCE-DERIVED; native-layer reinterpretation; no claim of fully independent whole-frame native authorship |
| Owner decision and production stop rule | `tools/prologue-art-lab/assets/review/chapter-04-b210-upper-salvage-2026-11-24/PMO-V03-APPROVAL-AND-STOP-RULE.md` at review commit `115152a5e42e5877a21bde5ccc0d050608bdda56` |

## Canonical coverage and reuse

One image covers `hotel_upper_salvage_arrival`, `hotel_upper_salvage_clerk_directions`, and `hotel_freight_wc_misunderstanding`. Its shared geography includes freight-lift doors with the W.C. three-button panel, a dark open hatch, descending service stairs, and disconnected bathroom fixtures on racks/pallets. The salvage clerk is **voice-only**. There is **no separate freight-lift scene, clerk portrait, interactive usable toilet or conditional variant**.

The art registry status is `approved`, not `integrated`. `assetPath` stays `null`; the future engine destination suggested in the registry is `art/scenes/grand_bellevue/upper_salvage.png`. The selected public preview path is **not an instruction to change the game importer**. No story JSON, flags, choices, UI, runtime, Focus IDs or gameplay bindings are changed by artwork registration.

## Preservation and publication check

`node tools/sync/register-art.mjs` registered one exact source PNG after a successful dry run. Run `node tools/sync/check-canon.mjs` and `python3 tools/sync/verify-ch4-b210-selection.py` in the registration branch. The verifier compares against canonical baseline `b8a8e4ea3c6d13141b2e33d281ba864c3b2aec42` to ensure all **199 earlier selected PNGs and metadata** remain unchanged, the exact new image hash and provenance are pinned, no other registry records are touched, and no narrative or engine integration files change. See adjacent `143_CH4_B210_VERIFICATION_20261124.json` after running it.

Do not merge unrelated draft PR #32, rewrite approved art, or deploy as part of registration without separate authorization. The PMO's next art batch is **B2-11 public corridor dry base and flood states**, per docs/138 and the updated owner stop rule. Every new B2-11 candidate remains **UNSELECTED** until Nate reviews it.
