# CH4-B2-03 — R1 material-cluster pilot 01

**UNSELECTED — MATERIAL PILOT, NOT SELECTION-READY.**

The one localized pilot failed its artistic gate: the bowl lost concavity, the
apron became banded and the tap lost convincing brass modeling. Painting stopped;
no scene-wide conversion or loading-dock work followed.

Open `index.html` locally or `online.html` through the public browser viewer.
See [ARTISTIC-GATE.md](ARTISTIC-GATE.md) for visual findings and the method limit,
and [manifest.json](manifest.json) for scope, hashes and honest mixed provenance.

The native material group was painted separately, then composited over an exact
copy of the approved source-derived background. Only the group has new native
paint authorship; the complete scene is not described as independently authored.
No new imagegen call was made. Historical originals, prompt and receipts are
preserved as exact blobs from the approved B2-01 source commit.

Editable sources: `source/CH4-B2-03-material-pilot01.ora`, `layers/*.png`,
`source/native-paint.json`, and `source/paint_material_pilot.py`.
The masks include an independently defined allowed work envelope, protected
fixture windows, semantic paint coverage and an exact final RGB difference mask.

Reproduce with Python 3 and Pillow:

```sh
python3 source/paint_material_pilot.py
python3 source/build_review.py
```

The review builder checks immutable source blobs, exact changed-pixel locality,
native tape replay, OpenRaster merged pixels and exact nearest-neighbour 4×.
These technical checks remain separate from the failed artistic gate.
Publication receipts are kept outside this frozen version directory.
