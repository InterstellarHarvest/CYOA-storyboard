# Chapter 4 Artwork PMO — B2-10 v02 targeted refinement directive

**Decision:** `v01` remains **UNSELECTED / NOT SELECTION-READY**. Nate has not approved this asset. Codex's internal rejection at the artistic gate is correct. The single-scene narrative scope, geometry and W.C. panel are sound; do **not** restart composition or revive consolidated-away images.

**Pinned review source:** `art/ch4-b210-upper-salvage-review-20261124` at `ca66bbc5b37a8b4e52805134147f7c96b0a26bfd`, `v01/`. Preserve that package byte-exact. Canonical `main`, approved artwork, game, narrative, draft PR #32 and other batches are off limits.

## Independent PMO visual assessment

At the actual **314×206 native size**, freight-lift doors, the legible `W.C.` three-button panel, the open maintenance hatch and descending stair routes are understandable and compatible. The central floor is usable negative space. Keep these shapes, perspective and camera placement stable.

The **rear right storage rack** remains a row of pale circular/square symbols rather than convincing discarded plumbing. The bowls do not show enough thick rims, receding cavity, underside/outlet, overlap, mounting or weight against shelves. The **front-left nested sinks and pallet** are also too icon-like: form transitions and supported/contact shadows are weak compared with approved Chapter 2 Control Tower and Maintenance Exit. Leaning mirror/partition leaves need more believable thickness, reflection planes and contact. Broad room shading or another palette/noise treatment will not fix the object anatomy. The visual field is generally less dimensional than approved Chapter 4 Service Stairs as well.

## Authorized v02 intervention: repaint existing fixture artwork

1. Work **directly in the native 314×206 pixel grid**. Focus on `v01/layers/material-storage-racks.png` and `v01/layers/material-foreground-sanitary-salvage.png` (and their non-material counterparts or source recipes where required), plus tiny localized contact-shadow corrections at their supports. Preserve the original v01 layer stack. Do not globally reprocess the room or replace its master via image downscaling.
2. Give rear fixtures distinct, plausible three-quarter silhouettes: at least one detached toilet-bowl shape with an oval rim and dark hollow, one dismantled sink with porcelain edge and drain/outlet sockets, and staggered stock with true occlusion. Each object must visibly rest on a shelf; use shelf thickness/brackets and contact shadows, not isolated floating ovals. Keep all fixtures disconnected and **unusable**.
3. Redraw the nested foreground sinks with explicit lip thickness, hollow bowl, faucet holes/drain, underside contours and readable support on the wooden pallet. Limit highlights to physically meaningful glaze edges and ridges. The pallet should carry the fixture weight with shadows, not become decorative grain.
4. Refine the leaning glass/mirror and bathroom partition edges only enough to distinguish reflective glass, chipped enamel and metal framing. Use selective planes, edge breaks, cast shadows and purposeful pixel clusters. No new object types, extra character, hanging stall, crane-only state or environmental storytelling text.
5. **Pixel-lock all geography:** freight-lift doors and sill, W.C. glyphs/three buttons, open maintenance hatch, descending stairs/guardrails, central movement space, architecture/perspective and any already convincing pipes/ducts. Do not move the camera or alter the one-scene consolidation contract.
6. Preserve a replayable construction recipe. If pixels are manually repainted in an editor, preserve the editable layered native source and deterministic assembly; do not silently hand-edit a flattened PNG while leaving a stale generator that overwrites the fix.

## Mandatory visual gate before publication

- Compare **at 314×206**, then at exact 1256×824 nearest-neighbor 4×, alongside *actual approved* Chapter 2 `control_tower.png`, `maintenance_exit.png`, `damaged_walkway.png` and Chapter 4 `service_stairs.png`, `loading_dock.png`. Inspect rack, porcelain and pallet at the same logical scale as comparator objects.
- Judge **form modelling, foreground/midground separation, cluster economy and material character**, not only palette count, technical checks or how richly the source illustration looks. More speckles, soft gradients and blanket shading are specifically rejected.
- If v02 still looks like programming geometry or icons after one genuine native fixture redraw, stop at the quality gate and candidly recommend specialized Aseprite/Krita pixel illustration for those two layers. Do not publish a mere relighting pass as selection-ready.
- If the new object modelling passes, publish **v02 UNSELECTED** on the same art review branch. Include a browser gallery; v01/v02 native and exact4× sheets; *readable, non-overlapping labels* (the v01 `story-object-details-4x` title collides); close crops of rack, nested sinks and mirror; canonical Chapter 2/4 comparisons; source/repair records; source-derived authorship; exact hashes; preservation and browser QA. Do not register or merge.

**Success criterion:** Nate can identify disconnected sinks and toilet bowls as physically supported salvage, with believable volume and layered porcelain, *at native resolution*. The scene should retain Chapter 2's rich but economical pixel clusters without adding a person or increasing the asset count.
