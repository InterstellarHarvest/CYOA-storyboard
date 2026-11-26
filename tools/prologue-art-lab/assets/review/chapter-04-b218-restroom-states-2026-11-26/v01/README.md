# Chapter 4 B2-18 — restroom conditional-state family v01

**Six UNSELECTED production references; no registration or integration.**

The current PMO instruction suspends R1 and supersedes the old dependency on
refined masters. Approved CH4-04 and CH4-B2-03 remain authoritative. Neither failed
R1 study is used, modified or selected.

## Contents

- Main scene: active leak, temporarily braced/dribbling, contained/no-flow,
  flood onset, nearest stall lifting over the contained wet floor.
- One active-leak closer background using approved CH4-B2-03.
- Base/state comparisons, a main progression sheet, Chapter 2 references,
  approved-portrait composites and exact nearest-neighbour 4× exports.
- Exact changed-pixel masks, declared allowed regions, protected figure/toilet
  masks, native event layers, six editable OpenRaster projects and build scripts.

Read [RECONCILIATION.md](RECONCILIATION.md) before interpreting the states. It
identifies which beats need images, which use narration or approved Focus reuse,
and the existing toilet-location contradiction in the later mezzanine scene.
The flood reference is deliberately the onset before the floating-basket beat.
No fully removed-bay or extra dialogue-background variant is invented.

## Source method and reproducibility

The state outputs are source-derived composites of exact approved native masters
and localized native event layers. The existing room is not independently redrawn.
Water uses a small set of explicit translucent brush colours and connected native
marks. The lifted enclosure uses integer-translated approved door/frame pixels,
with only revealed wall, hatch and cables constructed at native resolution.

The built-in imagegen tool supplied one staging reference, preserved with its
exact prompt and receipt. No generated pixels are resized, sampled or pasted into
the state outputs. No global palette reduction, sharpening or architecture
repaint occurs. Full-scene PNGs are opaque RGB; water layers retain intentional
transparency so original grout and material shading remain visible.

```sh
python3 source/build_states.py
python3 source/build_review.py
```

Python 3 and Pillow are required. `source/native-event-marks.json` records the
new marks; source-box translations and the exposed-wall plate are explicit in
`source/build_states.py`. `layers/*.png` and `source/*.ora` are editable native
sources. QA recomposes every output, checks OpenRaster merged pixels, measures
exact RGB differences and verifies all approved source blobs.

Open `index.html` locally or the pinned `online.html` public browser entry.
Public byte and browser receipts are stored outside this frozen version folder.
Stop for Nate's review before producing the lobby-door or Lot 61 families.
