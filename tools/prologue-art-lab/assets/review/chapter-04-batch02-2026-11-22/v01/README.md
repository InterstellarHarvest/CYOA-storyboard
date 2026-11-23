# Chapter 4 B2-01 — Restroom dialogue and controls v01

Five **UNSELECTED** review candidates, independently separate from the five approved Batch 1 selections. No engine integration or narrative changes. [Gallery](index.html), [manifest/exact hashes](manifest.json), [native comparison](comparisons/B2-01-all-native.png), [exact4× comparison](comparisons/B2-01-all-4x.png).

- CH4-B2-01: `hotel_plumber:worried`, transparent564×278.
- CH4-B2-02: `hotel_plumber_assistant:pleased`, transparent564×278.
- CH4-B2-03: shared `grand_bellevue/restroom` portrait background, opaque564×278.
- CH4-B2-04: `grand_bellevue/restroom/lot_14_receipt`, opaque564×278 Focus A.
- CH4-B2-05: `grand_bellevue/restroom/master_isolator`, opaque564×278 Focus A.

Built-in **image_gen.imagegen** produced the original illustrations from approved Pavilion portraits, approved Chapter4 architecture and approved Chapter2/reception environmental rendering references. [Originals](originals/), [exact prompts](prompts/), [tool receipts](evidence/generation-receipts.json), [input references/hashes](manifest.json). All final images are **SOURCE-DERIVED**, not independently authored at native resolution. Foregrounds use premultiplied-alpha Lanczos reduction, disconnected cutout/fringe cleanup and restrained near-opaque interior contrast retention, preserving anatomy. Room/Focus art uses controlled opaque reduction of newly composed close cameras, never an enlarged scene crop. No global palette cap. [Full derivation](evidence/derivation.json).

Nate’s final lettering direction is applied to portrait/inspection objects: approved Tiny5/Press Start bitmap atlases, binary glyph masks and nearest-pixel perspective mapping onto paper/plaque planes. The full receipt copy is canonical, including its wrapped exception; deliberate inset margins keep it clear of all four damaged edges. Eddie’s held receipt shows only readable LOT14, with full content in the close-up. Cabinet lettering is enlarged and perspective-aligned. The new background’s top plaque reads WATER; original main scenes and their markings are untouched.

Focus A is **564×278 opaque**, verified against canonical docs105, artwork helpers and a read-only inspection of actual game `ART_CLASS.focus` (recorded in evidence/dimension-contract.json). The565×451 item inspector is separate. Canonical nodes, the pinned v08 inventory and every unchanged approved reference are preserved. Both portraits are composed on the new shared background; light/dark transparency previews are retained.

Reproduce with the recorded Pillow version:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/prepare.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

Native lettering is deterministic using bundled copies of already-approved project bitmap font atlases/mappings. No smooth system-font dependency in the artwork. Gallery labels use ordinary browser UI text. `source/qa-gallery.cjs` checks native/exact4× images and controls in Chromium/Firefox; `source/prepare_online.py` pins public gallery dependencies to an immutable artwork commit. No production Pages workflow change.

Batch1 approvals: canonical main `ee5948f14144d2bd99b75432e8d58422e8958bf1`, PR20. Runtime paths remain unbound until Gameplay PMO integration; all exact approved bytes are preserved. Full closeout: docs/127 in that commit. Historical review statuses remain unchanged; the later owner approval supersedes them.
