# B2-12 v02 — widescreen Focus and approved INSPECT

Two new564×278 opaque RGB Focus candidates: LOCKED and PROVISIONALLY AUTHORIZED. **Both UNSELECTED.** They share one native composition and differ only inside screen/indicator masks.

Nate has explicitly approved all three v01 images unchanged: dressing room314×206, locked inspection565×451, provisional inspection565×451. Exact reference copies are under `references/`; hashes and pinned source paths are in `evidence/owner-approval-preservation.json`. No canonical registration is performed in this artwork review, and historical v01 review manifests are not rewritten.

The owner finalized two separate views:564×278 Focus with existing choices, and565×451 informational INSPECT. See the exact `OWNER-DIRECTION.md` and the separate `ENGINEERING-HANDOFF.md`. No engine/narrative/gameplay implementation, binding, integration, main merge, PR#32 change or deployment is included.

## Native artwork and source provenance

Built-in `image_gen.imagegen` generated one new widescreen composition reference, using the approved locked panel as object identity, the approved dressing room as architecture/material reference and approved Chapter2 Exposure Dispenser as rendering benchmark. The original and exact prompt/input hashes are preserved. Approved artwork was not regenerated or used as a resized/cropped/recolored production layer.

`source/build_native.py` builds at564×278. Explicit native material masks use source-informed light/colour fields for plaster, door wood and duct surfaces; the diagnostic BOX reference is labeled NOT production. Native layers separately paint the door and jamb profiles/insets, plaster extension and wainscot rail, duct/pipe joints and supports, glass/brass lamp, full brass panel/edge planes/fixings, camera optics and swivel, recessed CRT, three policy pictograms and plaques, physical assistance button and bitmap lettering. This is **SOURCE-DERIVED**, not wholly independent native authorship; the native construction is more than a whole-image downscale or palette transfer.

`source/native_support.py` reuses code/constants from v01 only. No approved image is processed by that helper extraction. Native RGBA layers have binary alpha, masks are editable, material ramps are explicit, and compositing orders/hashes are preserved. No dithering, sharpening, interpolation in enlargement or arbitrary global palette cap is used. Typography is chunky binary5×7 at native scale1, appropriate to the panel's reduced physical size; detailed legibility remains in approved INSPECT.

## Owner correction and visual gate

The owner observed that the first native plate overlapped the wainscot rail. Corrected the wall geometry once: the rail is below the entire plate and its cast shadow, with plaster extended behind it. The conduit reaches the relocated rail. Identical correction in both states; camera, brass plate, badge layout, lighting direction and approved sources remain intact. Pre-correction diagnostics are preserved, clearly NOT current.

Compare actual images at native and exact nearest-neighbor4× against approved Chapter2 Exposure Dispenser and Aid Box. The door, camera/screen, three badges, emergency button, sconce and conduit have distinct silhouettes and material groups. Dark lens/CRT recesses, stepped brass/painted-wood bevels and warm glass establish dimensionality without granular texture. No person, AI face, door handle/keyhole, extra control station or invented story object is present. The plate occupies most of the height and remains separated from architecture. Internal assessment supports publishing this single corrected composition for Nate's visual decision; it is not owner approval.

## Review and replay

Open `index.html` locally or the published immutable `online.html` browser gallery. Exact4× images display at their full raster sizes; wide comparisons scroll. Approved INSPECT and room references retain native dimensions and byte hashes. Comparison sheets show widescreen/approved-square, both new states, same-class Chapter2 benchmarks, the targeted rail correction and the explicit source diagnostic versus native construction.

Python3 + Pillow replay: `python3 source/build_native.py`, `python3 source/package_review.py`, `python3 source/validate.py`. See `evidence/validation.json`, palette diagnostics, browser receipts and public byte verification. Technical checks do not confer artistic approval. The entire pre-existing repository tree, including all v01/source/approved images and approval records, remains unchanged.
