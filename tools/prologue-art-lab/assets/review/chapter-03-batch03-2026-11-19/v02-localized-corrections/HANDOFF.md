# Out of Order — Chapter 3 Batch C v02 correction handoff

2026-11-19. Source: `art/ch3-pavilion-batch03-20261119` at `53358b9df78f72e815cd69ee4128b1c86c08818d`.

Eight candidates remain generated/unselected. This pass changes only C01 and C03 through explicit edits on their existing 314×206 grids. It makes no image-generation calls.

- **C01 urgency: 55 changed pixels.** The held object now has a narrow dark handle, tapered silver body, flared dark lip and one-pixel clapper. Its previous pale rectangular footprint and lower shadow are repaired with adjacent same-row curtain pixels. Every existing hand skin pixel is protected. The presenter’s face, pose, sleeve, stage, restroom reveal, two-person sign, loudspeaker, buttons, console and countdown remain unchanged.
- **C03 locomotion: 184 changed pixels.** Two floor-tile courses and receding grout joints distinguish the existing stationary landing beyond the curtain. The existing yellow sill gains a restrained highlight and narrow step face. No floor area is widened, no bridge is added, and the pit remains between the moving surface and escape floor. Conveyor, padded pit, net, camera, stage footprint, signage and doorway remain unchanged. The timed d6 leap is still required by the narrative.
- **C06 excited presenter: retained byte-identical.** Native and enlarged comparison against approved idle shows already raised eyebrows, bright eyes and an open delighted smile. The optional edit was declined to retain likeness, proportions, alpha and anchoring.
- **C02, C04, C05, C07 and B07: retained byte-identical.** Six unchanged candidate PNGs are copied exactly into the v02 set with separately identifiable filenames.

Open `index.html` for native/4× candidate views, all eight v01/v02 comparisons, 8× bell/landing close-ups, changed-pixel overlays, stage continuity and approved-chapter style references. Six portrait composites are byte-identical to v01 at (0,0), scale 1. Original generation records, exact prompts and oversized source files remain linked in immutable v01.

`sources/corrections.json` records source/final hashes and operations. `sources/*-changed-pixels.json` lists every changed coordinate with before/after channel values. Allowed masks, exact changed masks and transparent correction layers are retained for every candidate; unchanged candidates have empty masks. `finish_pixels.py` reproduces the edits; `build_review.py` verifies the outputs and builds the gallery. No global sharpening, enlargement, filtering, quantization or scene-wide redraw is used.

Technical QA passes dimensions, RGB/RGBA modes, binary alpha, exact 4× nearest-neighbor previews, mask containment, complete pixel-coordinate accounting and reconstruction from v01 plus the local layer. Zero unexpected pixels occur outside the edit masks. All 179 v01 files match the source commit’s Git blobs; 324 protected current files and 834 pinned historical Batch A/B review files pass hash verification. Approved artwork, narrative, registry and publication workflows remain unchanged. Browser verification is in `browser-qa.json`.

**Original native-grid authorship remains unresolved/unproven.** These localized edits are authored at native resolution and documented exactly. The inherited illustrations still derive from oversized generation outputs and retain source-derived RGB softness. This finishing pass does not establish original native-grid authorship.

Art Director attention: confirm the seven-pixel-wide bell reads at native size and that the articulated landing still communicates a difficult but plausible jump. No other visual change is proposed.

No Pages deployment, workflow dispatch, PR #13 update/merge, approval registration, integration, production asset paths or Batch D. `main`-only publication remains intact. Stop for Nate’s final visual review.
