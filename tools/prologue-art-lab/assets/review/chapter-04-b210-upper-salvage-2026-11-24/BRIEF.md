# Codex production directive — Chapter 4 B2-10 / CH4-NEW-03

Nate has approved and registered the preceding consolidated B2-09. The canonical baseline is `6334b895333dd2d78332cf9f1d834e619468f932`. You are the pixel-art production agent for **one reusable B2-10 main scene only**, using the public storyboard as the source of narrative truth. Work on branch `art/ch4-b210-upper-salvage-review-20261124`; publish candidates **UNSELECTED**. Do not alter `main`, `assets/selected/`, `story/`, `story/artwork.draft.json`, `story/artwork-preview.json`, game integration, any approved PNG, or draft PR #32.

Read in full: `docs/129_PERMANENT_PIXEL_ART_PRODUCTION_STANDARD_20261122.md`, `docs/138_CH4_B209_REVISED_PRODUCTION_BRIEF_20261124.md` (B2-10 queue), and relevant narrative nodes `hotel_upper_salvage_arrival`, `hotel_upper_salvage_clerk_directions`, `hotel_freight_wc_misunderstanding` in `story/chapters/chapter-04.wip.json`. These nodes converge on the same visual space.

## Single image contract

- ID: `CH4-NEW-03`; future canonical scene key `scenes:grand_bellevue/upper_salvage`.
- **314×206 opaque RGB native pixel art** (actual logical pixels, not softened or antialiased), and an **exact 1256×824 nearest-neighbor 4× review**.
- Show a cramped hotel **upper salvage mezzanine** with **freight-lift doors and a clear W.C. panel**, dismantled sanitary fixtures (sinks, mirrors, toilet bowls, bathroom partitions) stacked bureaucratically, an open maintenance hatch leading into pipework, and service stairs descending toward the loading dock. Industrial rails, grilles, exposed duct, bent brackets and cheap painted-over paneling should fit the established Grand Bellevue material language: *Brazil* (1985) absurdist institutional glamour barely concealing rundown engineering; never spotless luxury or overt steampunk.
- Preserve credible geography so the freight-lift entry, hatch route and stair route are all legible in ONE reusable composition. The lift's W.C. button means **Warehouse Collection**, not a usable water closet. The exact letters `W.C.` must read at native size and align with perspective, but avoid any other tiny unreadable prose. It is enough to show a panel next to or just inside the freight lift doors. No misleading functioning toilet in this scene.
- **No drawn salvage clerk portrait**: he is approved as voice-only. **No mandatory suspended stall** in the base image: one route arrives by crane inside a suspended stall, another by freight lift, so the shared base must remain truthful to BOTH. Do not add the protagonist, their face or any new character. Conditional stall accents are NOT authorized in this batch.
- Avoid a second upper-salvage scene or separate freight-lift PNG: docs/137 consolidated those nodes to this one master. No new flags, Focus IDs, portraits or runtime bindings.

## Visual standard and method

- Before generating, inspect **actual approved Chapter 2 native images and their exact 4×**: `assets/selected/art/scenes/biology_park/control_tower.png`, `damaged_walkway.png`, `maintenance_exit.png`. Also compare Chapter 4 selected `assets/selected/pending-integration/scenes/grand_bellevue/service_stairs.png`, `loading_dock.png`, `lobby.png`. Match Chapter 2's **high detail through deliberately placed broad connected pixel clusters**, restrained local palettes and material-specific shadow shapes; not its subject matter.
- You MAY use a large, richly detailed imagegen illustration as an **independent composition/material reference**. Do NOT shrink that large source to 314×206 and call it final. Deliberately REINTERPRET on a blank native grid using independently shaped silhouettes, structural masks, selective native pixel painting, clear contours and controlled palette/texture clusters. The approach used to simplify NPCs in later Chapter 4 passes applies to objects and any figures at scene scale. Portrait rendering is not the target here.
- Preserve the large source, exact prompt, intermediate diagnostic, editable semantic layers/masks and assembly recipe. Mark honest provenance **SOURCE-DERIVED** unless truly authored natively. Do not fake a claim of wholly independent native authorship. Reject attempts that look like automatic reductions, gray smears, over-dithered noise or flat mechanical polygons compared with Chapter 2.
- Pixel grid: no half-res sampling or post-hoc sharpening that introduces many near-duplicate colours; exact4× must be a mathematically exact nearest-neighbor export. Need not impose an arbitrary 64-colour global palette on main scenes; use a reasoned local/material palette comparable to approved scenes, and log counts and cluster findings.

## One-cycle production and quality gate

1. Inspect storyboard data and canonical Chapter 2/4 pixels. Sketch compositional geography; ensure lift/hatch/stairs are distinct and W.C. reads correctly.
2. Generate a richly detailed source reference with the built-in image-generation capability, if available. Treat only as reference. Create the 314×206 master with deliberate native-grid structural/artistic reconstruction, not a resize. Preserve layered source.
3. Produce `v01` in `tools/prologue-art-lab/assets/review/chapter-04-b210-upper-salvage-2026-11-24/`, with native PNG, exact4× preview, source/provenance/recipe, comparison sheets against approved Chapter 2 and Chapter 4, a browser review gallery, validation JSON and README.
4. Critique at **actual 314×206** before publishing. If readability/style falls below Chapter 2, refine internally (v01b or study) until truly selection-worthy; never label an unready draft as ready. Preserve diagnostics explicitly.
5. Commit and push ONLY the isolated review branch. Verify published hashes and gallery if permitted. Leave everything **UNSELECTED**, do not register or merge without Nate's later approval.

Final report: concise link to gallery and 4× comparison, exact review branch/commit, honest provenance, checks run, any unresolved visual weakness. Do not ask Nate aesthetic questions you can resolve from these canonical refs. No extra art beyond this one scene.
