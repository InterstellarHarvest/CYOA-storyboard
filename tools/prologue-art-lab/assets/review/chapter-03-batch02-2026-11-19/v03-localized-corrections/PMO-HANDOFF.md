# Chapter 3 Batch B v03 — Art Director review

Branch: `art/ch3-pavilion-batch02-20261119`.
Source commit: `2699abbd651817961b76d87fa0d4c78a57b04bc5`.
Published deployment commit is recorded in `deployment-provenance.json`.

Public gallery: https://interstellarharvest.github.io/CYOA-storyboard/tools/prologue-art-lab/assets/review/chapter-03-batch02-2026-11-19/v03-localized-corrections/

All six candidates remain **generated / unselected**. No registry, narrative, game, approved artwork or prior review file is modified. B01 is byte-identical to v02. No Batch C.

- B02: removed the added right-hand printer by rebuilding on the unchanged A01 v09 base. Original plant/counter restored. Receipt now feeds from the lower slot of the existing left cream desk unit. Microphone, attendant and chair pixels stay exact.
- B03: removed the right-hand printer and restored A02's plant. The same existing left slotted housing now emits a short receipt. Microphone unchanged; approved A03 remains at (0,0), scale 1.
- B04/B05: narrow the door openings locally to four/seven clear pixels respectively, matching the different camera scales. Transfer each existing handle to the near-closed leaf. Keep reader/indicator hardware unchanged. The document is engaged under the roller; the intake arrow points into the reader. Green admits the document, not a person.
- B06: rebuild from approved A01 with the sole existing left printer housing. Remove rectangular attendant exclusion. Use a hand-traced binary silhouette, separate exact microphone/chair silhouettes, and natural foreground receipt layers. Fewer ribbons climb the original plant; jointed ceiling supports and contacting brush bristles carry the paper toward the original right exit. No room architecture is rerendered.

The existing cream unit plausibly serves as the printer housing, so no alternative location or broader architectural change is needed. A01 v09 itself remains unchanged.

Inspection and QA:

- Four opaque 314×206 mains; two opaque 564×278 close backgrounds. Exact main previews are 1256×824 nearest neighbor.
- Allowed-edit masks include both removal of old overlays and addition of new ones. Every v02→v03 changed pixel has a coordinate record; unexpected changes outside these masks are zero.
- Traced attendant mask covers 1,036 native pixels, microphone 101, chair 87. All are exact in B02/B06. The former rectangular background is not protected: 324 paper pixels can now occupy it outside the actual body silhouette.
- B02 and B03 original plant regions are fully byte-identical to approved bases. B06 retains the same plant underneath natural paper occlusion. The generated replacement plant is excluded by manual object traces.
- Both A03 composites preserve every opaque foreground pixel, binary alpha and anchor/scale.
- All 245 prior Batch B package files, 455 Batch A historical files, 179 canonical historical review files and 140 selected/story/authority files pass pinned hash verification.

Native-grid limitation remains: all inherited source limitations persist. One new built-in imagegen call produced only a transparent addition donor at **1548×1016**, preserved unchanged. Only new objects were transferred to the logical grid. Source-derived paper/brush shading remains; no claim of original native-grid authorship is made. The hand-authored native work consists of explicit paper contours/marks, sampling-based door repairs, handle transfer, intake arrows, mount caps, object tracing and compositing. No global palette reduction, recoloring, sharpening, scene resizing or crude alpha thresholding.

Art Director attention: confirm the left housing reads convincingly as the same printer in both scales; inspect plant/paper folds and silhouette occlusion in B06; confirm the paired scanner intake and narrow openings communicate document-only admission. These are visual selection questions, not automatic QA approvals.

All exact hashes: `CANDIDATE_HASHES.md`. Masks, source prompt, raw original filename/dimensions/hash, per-pixel coordinates and technical results are linked in the gallery. Public browser verification follows deployment.
