# Chapter 4 B2-17 v01 — Lot 53 Dispute Ticket and Wedding Ring

**Four primary candidates, all UNSELECTED.** This is artwork review only: no selection, registration, merge, deployment, item-rule change, Focus state or runtime binding.

| Asset | Existing item / view | Native contract |
| --- | --- | --- |
| CH4-NEW-10 | lot_53_dispute_ticket / slot | 96×96 transparent RGBA |
| CH4-NEW-11 | lot_53_dispute_ticket / inspect | 565×451 opaque RGB |
| CH4-NEW-12 | wedding_ring_lot31 / slot | 96×96 transparent RGBA |
| CH4-NEW-13 | wedding_ring_lot31 / inspect | 565×451 opaque RGB |

Every primary has an exact nearest-neighbor 4× export. The slot PNGs have binary 0/255 alpha, clean transparent margins, no baked inventory frame, contact shadow or glow. The ring hole is genuinely transparent. The inspection artwork is constructed separately at 565×451; it is neither an enlargement of the slot nor the 564×278 Focus A contract.

## Canonical wording audit

All three proposed ticket phrases are already present in `story/items.draft.json`, in `lot_53_dispute_ticket.description`:

- `LOT 53`
- `LACK OF PRIVACY — CUSTOMER PRESENT`
- `HOLD FOR INSPECTION`

Thus none remains merely draft-proposed wording. The narrative node `hotel_auction_dispute_ticket` confirms the red carbon-copy ticket, formal objection, lack of privacy, stamping/tear-off and right to inspect before departure. It explicitly says the sale is not cancelled. The artwork adds no refund, cancellation, serial number, customer name, date, seal or additional entitlement. `DISPUTE TICKET` is taken from the canonical item name. Line breaks in the reason and stamp change layout only; they preserve the canonical words and em dash.

The ring inscription is exactly `AS IS, WHERE IS.`, including comma and final full stop. It is authored both in `hotel_ring_inspect_inscription` and the item's READ description. That description also specifies a tiny maker's mark. Canon supplies no initials, brand, purity or date, so the illustration uses a small anonymous geometric punch. Its precise decorative shape is an artwork choice for owner review, not a new named manufacturer or item property. No engraving or hallmark is readable in the slot.

Full exact item/node snapshots, registry entries and the field-by-field wording audit are preserved in `evidence/`.

## Identity, materials and lettering

The paper pair shares one landscape salmon-red carbon-copy slip, a torn/perforated pad edge, a thin dark red paper edge, centered lot field, reason area, lower-right inspection stamp and a modest curled lower corner. The icon simplifies long prose into economical ink blocks rather than pseudo-words. The inspection uses only meaningful canonical lettering, with comfortable physical margins. Warm paper planes, a shallow crease, selected fiber bundles, worn stamp edges and the curled reverse distinguish paper from ink and desk.

The ring pair shares the same simple low-domed silver band and one short pale blue ribbon, matching the approved auction/collection armrest PNGs. A wrap, compact knot and two short ends depict one continuous ribbon. No box, gemstones or additional jewelry appears. Coherent cool silver reflections, a narrow warm desk reflection and folded blue textile forms separate the materials. Shared object geometry is rasterized directly into each target canvas, with finer polishing/weave detail reserved for inspection.

Paper lettering uses an editable chunky 5×7 bitmap alphabet with native 2–5 pixel cells projected through a planar homography. Text is physically aligned to the paper, including the stamp; it is not a smooth overlay floating above the object. The smallest inspection text has a 14-pixel local character height. All inspection lettering/stamp pixels remain within the paper mask and the text keeps at least 20 local units of physical edge margin.

Ring glyphs are individually constructed from the same bitmap alphabet, placed by arc distance and oriented to the tangent of the actual inner-wall ellipse. The engraving is on the metal surface, fully clear of the ribbon and maker mark. The phrase is readable in the full native inspection view; the gallery also provides a pixel-exact crop for auditing, without substituting larger typesetting.

## Production and provenance

The built-in `image_gen.imagegen` tool produced four detailed design/material references. The inspection references informed the later slot references so object identity remained consistent. Every original, exact prompt, input role/hash and generation record is preserved. One generated slot-ring reference contains unwanted soft glow; it is retained intact as source evidence, and none is transferred into the binary-alpha native output.

Visual designs are honestly **source-derived**. Final rasters are independently constructed from blank native canvases by `source/build.py`, using explicit material ramps, geometric forms, semantic masks and native bitmap glyph cells. The renderer reads no reference PNG, transfers or samples no reference pixels, and performs no source reduction, sharpening, global palette filter, antialiasing, procedural colour gradient or random-grain pass. Shape curves describe physical forms and lettering placement rather than smoothly interpolated colours.

Editable native RGBA layers, object masks, material ramps, camera/plane geometry, full text/glyph placement and layer-order recipes are included. An isolated replay containing only `build.py` and `chunky-glyphs.json`, without any source/reference images, reproduces all four final PNG hashes. Palette counts are diagnostic; no arbitrary global colour cap is imposed.

## Visual review and verification

The gallery compares slot/inspection pairs at their own actual native dimensions and exact 4×, approved Chapter 2 slots/inspection artwork, approved paper examples and both Chapter 4 ring/armrest images. Main inspection views and lettering crops were visually checked for phrase accuracy, margins, text orientation, silver/ribbon identity and silhouette clarity. Technical success does not constitute Nate's artistic approval.

148 verification checks pass: native dimensions/modes/hashes, exact 4×, binary-alpha layers and slot margins, empty ring hole, on-surface lettering, no ribbon occlusion, exact canonical wording, curved glyph orientation, shared object geometry, canonical reference bytes, prompt/input hashes, source-only replay and preservation of all 679 baseline tracked files, including 205 selected-art files.

With Python 3 and Pillow, run:

```
python3 source/build.py
python3 source/package.py
python3 source/validate.py
```

`index.html` is local. Published `online.html` pins dependencies to an immutable artwork commit. Native/4× controls display full integer raster dimensions and scroll wide images; checkerboard is gallery CSS rather than baked artwork. Public byte verification and Chromium/Firefox receipts are stored outside frozen v01.

## Gameplay handoff boundaries

The existing item IDs and slot/inspect keys are recorded only as proposed mappings. No registry paths or runtime asset bindings are assigned. The ticket's existing give/read/use behavior and the ring's existing READ/inscription flag remain authoritative. Inspection pixels do not authorize automatically setting `ch4_ring_inscription_read`, transferring the ring or creating a new reveal state. No additional Focus artwork, conditional inventory image, item, fee or rule is introduced.

Canonical baseline: `6a88153f1a41759def5d8e02fd04789db860ec1b`. Dedicated sole-producer worktree: `_worktrees/CYOA-ch4-b217-ticket-ring-20261125`; branch: `art/ch4-b217-ticket-ring-review-20261125`. No other agent or batch package is used for production. Narrative, gameplay, registry selections, approved artwork, main and PR #32 are untouched. Stop after publication at Nate's visual approval gate.
