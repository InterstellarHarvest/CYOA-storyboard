# B2-19 v01 — three UNSELECTED conditional-state candidates

Use the browser gallery `index.html` or its pinned public `online.html` entry.
Read [RECONCILIATION.md](RECONCILIATION.md) for the minimum states, node timing,
approved fatal-art reuse and the explicit PMO resolution of the B2-18 hold.

The three 314×206 RGB images are: both restroom leaves removed; open Lot 61 pod;
compact empty case after successful escape. Both Lot 61 images inherit the removed
doors. Motion and departure are narrated, avoiding redundant variations. The
existing approved fatal illustration remains unchanged and handles the fatal path.

The approved lobby is the source plate, not a reconstruction. Local native event
layers preserve its exterior door frames, central pier, lighting and room detail.
The pod toilet reuses approved native CH4-04 pixels with a semantic cutout, at 1:1
scale. New metalwork/case shapes are painted at the actual native grid. Imagegen
provided only a form/light reference; no generated pixels are resized into the
states. Its noncanonical OUT OF ORDER label is excluded. The canonical warning
stays in narration; the native booth has a small warning pictogram only.

No global recolouring, palette reduction, sharpen pass, new characters or elaborate
removal machinery. Protected source figures and furniture are unchanged. The exact
RGB difference masks include only door removal and actual object/shadow occlusion.

Editable files: `layers/*.png`, `source/native-event-marks.json`, `source/*.ora`.
Python 3 / Pillow reproduce the native states and review exports:

```sh
python3 source/build_states.py
python3 source/build_review.py
```

The assessment in `../porter-assessment/` alpha-composites exact approved images.
It is not new selectable artwork. The porter does not occlude the far-right edge;
it is inconspicuous in the native composition, and PMO explicitly accepts reuse.

All new states remain UNSELECTED. No canonical registrations, story, gameplay,
engine, main, PR #32 or deployment changes. Public verification receipts are kept
outside this frozen version folder.
