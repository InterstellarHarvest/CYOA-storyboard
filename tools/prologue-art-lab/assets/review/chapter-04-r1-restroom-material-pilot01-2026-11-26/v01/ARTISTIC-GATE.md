# R1 material-cluster pilot 01 — artistic gate failed

2026-11-26. **UNSELECTED — MATERIAL PILOT, NOT SELECTION-READY.**

This is the single authorized localized pilot. Painting stopped after its first
native/4× comparison showed loss of volume and material character. It is published
as diagnostic review evidence, not a replacement recommendation. The approved
CH4-B2-03 remains selected and unchanged. No loading-dock work was started.

## Actual comparison

| Material/form | Improvement | Remaining loss relative to the approved original |
| --- | --- | --- |
| Ceramic bowl | Larger connected regions, clearly stepped edges | The interior reads as a shallow dish. The transition from the back wall to the rounded well is insufficiently modeled; outlining the opening does not preserve its concavity. |
| Rolled rim and apron | Continuous lip highlight and distinct underside | The lip becomes too uniform; broad apron bands and isolated glazing accents read as illustrated strips rather than the original glazed, convex ceramic. |
| Brass tap | Crosshead, stem and spout remain recognizable, with a concise ramp | The contour is too heavy and the broad reflection strips flatten the cylinder. The result reads as a graphic green-bronze tap rather than convincing aged brass. Small contour differences inside the allowed envelope also weaken fidelity to the original. |
| Supporting pipe/shadow | Visible diagonal run, coupling and contact separation | The simplified shadow and metal stripes do not fully retain the subtle depth of the original fitting beneath the apron. |
| Full-scene fit | The existing room remains intact outside the work envelope | The cleaner but flatter target group looks conspicuously schematic beside the untouched rear basins and the room's richer lighting. |

At native size the main material identities remain legible, but the basin looks
shallower and the tap looks more diagrammatic. At 4× the clusters are easier to
identify, yet the same losses become more obvious. The actual approved Chapter 2
Bureau and Control Tower demonstrate that economical clusters can retain form;
this pilot has not achieved that balance.

**Conclusion:** clearer pixels and fewer material colours do not compensate for
lost volume. Do not extend this treatment across the restroom, transfer it to
CH4-B2-11, or replace the approved background.

## Construction and limitations

Six editable native raster layers contain 105 explicit brush/path marks. Curved
boundaries were rasterized directly at 564×278 with flat material colours and
binary layer coverage. The painted group uses 32 visible RGB colours. It is not
a quantized or sharpened copy of the source, and no larger working image was
shrunk into the pilot.

However, the path-based construction still simplifies the internal form too much.
It is a method limitation, not a reason to add more mechanical contours, texture
marks or palette entries. Further work should use direct native raster painting
by an experienced pixel illustrator, with the original ceramic/tap modeling held
as the reference and the work envelope locked. The first acceptance test should
be the untextured bowl's concavity and the tap's cylindrical reflections at native
size; wear comes after that. The OpenRaster project, source plate and masks are
provided for such a handoff.

## Exact scope proof

- Approved source SHA-256:
  `77325aca0d3c61d5b6d1980232fb11fa55156454a26659c6887c4d726a82c377`.
- 10,450 pixels differ, within native bounds `x=[0,160), y=[180,278)`.
- The exact changed-pixel mask is white wherever any RGB channel differs, with
  no perceptual tolerance. Black pixels are byte-equal RGB values.
- Zero changed pixels lie outside the independently defined work envelope.
- Zero changes occur in the protected mirror and rear-fixture windows.
- The full-scene colour count remains high because everything outside the small
  pilot is the unchanged approved source; no global palette operation occurred.
- The mask verifies locality, not preservation of all form within the painted
  region. The latter failed the visual gate above.

## Preservation and PMO disposition

CH4-01 and CH4-05 are unchanged. CH4-03 is deferred; its failed study is not
selected or reused. CH4-04 is only a continuity reference. CH4-B2-11 is not started.
All historical reviews, original imagegen sources, prompts and approved hashes
remain intact. No main, canonical registry, narrative, gameplay, engine file or
draft PR #32 is modified. The gallery is a read-only review publication, with
native and exact nearest-neighbour 4× exports and public verification receipts.
