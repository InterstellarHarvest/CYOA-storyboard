# Chapter 4 B2-17 — dispute ticket and wedding ring v01: approval registration

**Owner approval:** On 2026-11-26, Nate approved **all four B2-17 v01 candidates** without changes.
- All four are **APPROVED / SELECTED** on the existing item art records for `lot_53_dispute_ticket` and `wedding_ring_lot31`.
- No pixels were modified, downscaled, re-encoded or regenerated.

**Approved review source:**
- Branch `art/ch4-b217-ticket-ring-review-20261125`, final review head [`302c9c5304d555b50aa252200c45c30726123a46`](https://github.com/InterstellarHarvest/CYOA-storyboard/commit/302c9c5304d555b50aa252200c45c30726123a46).
- Pinned review gallery at [`c29eb9f`](https://htmlpreview.github.io/?https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/c29eb9f73a659f9ad7ca40f5819521aebf86a5ae/tools/prologue-art-lab/assets/review/chapter-04-b217-ticket-ring-2026-11-25/v01/online.html).
- All four natives were introduced in [`e350a13`](https://github.com/InterstellarHarvest/CYOA-storyboard/commit/e350a13794113ad7269074698fd021d10de957d3) at `tools/prologue-art-lab/assets/review/chapter-04-b217-ticket-ring-2026-11-25/v01/native/`.
- They are byte-identical at `e350a13`, `c29eb9f` and `302c9c5`, and they match the v01 review manifest.

| ID | Canonical key → selected path | Native format | SHA-256 |
|---|---|---|---|
| CH4-NEW-10 Dispute ticket, slot | `items:lot_53_dispute_ticket#slot` → `assets/selected/pending-integration/items/lot_53_dispute_ticket/slot.png` | 96×96 RGBA, transparent | `21543ddb40788ee4f994601b37397caa3173a082b851e569cccf79484c9741cd` |
| CH4-NEW-11 Dispute ticket, inspection | `items:lot_53_dispute_ticket#inspect` → `assets/selected/pending-integration/items/lot_53_dispute_ticket/inspect.png` | 565×451 RGB, opaque | `493004874154a0037559aa3eb4393eb60d73fac4977577699245eb9154393eed` |
| CH4-NEW-12 Wedding ring, slot | `items:wedding_ring_lot31#slot` → `assets/selected/pending-integration/items/wedding_ring_lot31/slot.png` | 96×96 RGBA, transparent | `e3a1d25cf2343302a6df8c660341879fa1e6a90f43629ac0706e50d2ba3e1ebe` |
| CH4-NEW-13 Wedding ring, inspection | `items:wedding_ring_lot31#inspect` → `assets/selected/pending-integration/items/wedding_ring_lot31/inspect.png` | 565×451 RGB, opaque | `298d8e45f371f7cc3f95e14928cf153fbe1af50f1bfac941a569c4f844a067e8` |

These are the first item images in `assets/selected/pending-integration/`. The path comes from the key, through `register-art.mjs`.

## Records

**All four records already existed** as `not-started` draft records from the Chapter 4 WIP. No record was added.
- `register-art.mjs` raised each to `approved`.
- Each record's `notes` now begins with the owner approval, the immutable source commit, the approved review head and the SHA-256. The earlier draft note follows verbatim under "Earlier draft note, superseded by this approval". This keeps the docs/137 ring-inscription corrections.
- Title, kind, dimensions, prompt, `suggestedFilename` and `assetPath` (`null`) are unchanged.

**What the art shows:**
- **Ticket:** a salmon-red carbon-copy slip with the lettering `DISPUTE TICKET`, `LOT 53`, `LACK OF PRIVACY — CUSTOMER PRESENT` and a `HOLD FOR INSPECTION` stamp. Every phrase is canonical item wording (`items.draft.json` name and description). No serial, date, name, seal, refund or new entitlement appears.
- **Ring:** a plain silver band with one pale blue ribbon, matching the approved auction and collection armrest Focus images. The inspection view carries the inner engraving exactly `AS IS, WHERE IS.` and an anonymous geometric maker punch. Nothing is legible in the slot.
- Both slots use binary 0/255 alpha with no baked frame, shadow or glow. The ring hole is transparent.

## Gameplay handoff (not performed here)

Gameplay integration is a separate Gameplay PMO task. When it happens:
- Copy the selected PNGs to the records' suggested engine paths:
  - `art/items/grand_bellevue/lot_53_dispute_ticket_slot.png`
  - `art/items/grand_bellevue/lot_53_dispute_ticket_inspect.png`
  - `art/items/grand_bellevue/wedding_ring_lot31_slot.png`
  - `art/items/grand_bellevue/wedding_ring_lot31_inspect.png`
- Set `slotArt` and `inspectArt` in `story/items.draft.json`; both are `null` today. Then raise the records to `integrated` through the normal batch and `game-integration.json` flow.
- Item behavior stays as authored:
  - The ticket keeps its give/read/use rules and `read` mark.
  - The ring keeps its READ effect (`ch4_ring_inscription_read`) and its two-state description.
- Showing the inspection image must **not** set the inscription flag automatically, transfer the ring or create a new reveal state. The flag is set only by the authored READ.
- No conditional inventory image, additional Focus art, item, fee or rule is introduced.
- The open Chapter 4 engine items in docs/140 are unaffected and remain the Gameplay PMO's.

No Chapter 4 narrative, choices, flags, items, item rules, Focus behavior, engine code, game integration, deployment or draft PR #32 is changed.

## Preservation

- All **210 earlier selections** are unchanged, with their bytes. This includes B2-13 (`autofit_gown`), B2-14 (`bridal_lavatory`, `three_seashells`) and the four B2-16 death screens.
- Approved supplemental and conditional references are unchanged.
- The full v01 review package stays on the review branch at `302c9c5`: originals, exact prompts, layers, masks, `source/build.py`, evidence, comparisons and public receipts. It is not copied into `main`.

## Provenance

All four images are **SOURCE-DERIVED**:
- Four preserved built-in imagegen design and material references with their exact prompts.
- The final rasters were separately constructed on blank native canvases from geometry, material ramps, semantic masks and native bitmap glyphs.
- The renderer reads no reference image. A source-only replay reproduces all four hashes.
- Wholly independent creative authorship is not claimed.

## QA tooling adjustment

`tools/storyboard/qa-smoke.mjs`, the Pages publish gate, asserted that these four item records stay `not-started`.
- It now asserts that they are `approved` with `assetPath: null`: approved storyboard art, not integrated.
- No other tooling changes.

## Workflow and verification

1. Read the four PNGs from the review head. Confirmed them against the manifest, the approval hashes and all three review commits.
2. Ran `node tools/sync/register-art.mjs` for each PNG: four dry runs, then four real runs. It copied the exact bytes, wrote provenance to `story/artwork-preview.json`, and raised each record `not-started` → `approved`.
3. Wrote the approval provenance notes on the four records.
4. `node tools/sync/check-canon.mjs` reports OK: 293 art records (79 approved, 140 integrated, 69 not-started, 5 reused) and 214 previewed.
5. Every CI step passes locally:
   - `qa-sync`, both Chapter 3 suites, `qa-smoke`, the death-export check and `qa-static`;
   - storyboard `qa-browser` 26/26, `qa-timeline` 136/136 and `qa-artwork-preview` 64/64;
   - art-lab `qa-pages-site` 70/70 and `qa-browser` 106/106.
6. `python3 tools/sync/verify-ch4-b217-selection.py` passes against canonical base `301ab75a62500a83b20dfee292b1a7460e01e405`, which includes B2-13, B2-14 and B2-16. Report: `docs/149_CH4_B217_VERIFICATION_20261126.json`. The checks cover:
   - exact bytes and formats, with binary slot alpha;
   - manifest agreement and identity with all three review commits;
   - exact provenance metadata;
   - only status and notes changed on the four existing records, with earlier notes kept verbatim;
   - exactly four new selections;
   - all 210 earlier selections unchanged, including B2-13, B2-14 and B2-16;
   - approved references unchanged;
   - the review package kept on its branch;
   - canonical ticket wording and the ring inscription;
   - unchanged narrative, item-rule and runtime files;
   - only registration files changed;
   - an unchanged PR #32 head.

**Next in the docs/138 queue: R1**, the refinement redraws of CH4-01, CH4-04, CH4-05, CH4-B2-03 and CH4-B2-11. They stay UNSELECTED until Nate picks replacements, and the approved PNGs stay selected meanwhile. B2-18/B2-19 state families follow from the R1-refined masters.
