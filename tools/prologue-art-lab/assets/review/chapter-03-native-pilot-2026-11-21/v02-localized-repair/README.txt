OUT OF ORDER — CHAPTER 3 LOCALIZED REPAIR V02
Assessment and first presenter test — Nate review, November 21, 2026.

NEW DIRECTION: maximize useful detail while removing only noise that harms
readability at exact 4x. The v01 reconstructions are not selected. Full-scene
reconstruction is withdrawn. Previous files are historical and unchanged.

Open index.html or standalone-gallery.html. README.md is the GitHub-rendered
review page. The portable HTML embeds every image; keep companion files for
its source/evidence links.

ASSESSMENT FIRST:
Locomotion's original composition, foreground chairs, camera, curtains,
fixtures, stage, signs, 30, doorway, shading and lighting remain protected.
Only six presenter pixels warrant a first localized visual test. A binary
mask and source-coordinate replacement plan were frozen before candidate
creation. Eyes, eyebrows, nose, smile, costume, near hand, gesture and shoes
remain exactly as in the original. There is no demonstrated pit/net/floor/
landing perspective failure requiring a geometry change.

Backstage: no repair justified in this pass; closed 0-pixel edit mask.
Retain cable contours, concrete variation, props, scenery, daylight depth,
EXIT sign and the already-approved attached mechanical clapper exactly.
No Backstage candidate has been produced.

FIRST TEST:
candidate/CH3-LOCOMOTION-presenter-local-v02.png
314x206 RGB, opaque. Exact 4x 1256x824.
SHA-256 8d4b6cef5b7d37f9f612da308fdc7868b7f31a9a4eb8947ed3993af66c7cf2e4
6 changed pixels / 64,684 (0.009276%); 64,678 unchanged.
0 changed pixels outside the predeclared mask.
RGB count 16,885 -> 16,879; no palette target or reduction.

The repair removes a detached copper pixel and joins selected hair/hand
edge shades. It is intentionally subtle. Some joins remain subjective and
can be rejected individually; the original expression and useful detail
remain. This is not a complete presenter or scene polish.

Exact changed coordinates, original RGB, replacement RGB, sampled source
coordinate and rationale are in sources/changed-pixels.csv and repair-plan.
The transparent six-pixel edit layer reconstructs the candidate exactly over
the immutable original. No image generation, global sharpening, posterizing,
resizing to native or palette processing was used. Full-scene original
native-grid authorship remains unresolved; this local repair does not solve
or relabel that provenance.

PRESERVATION:
Starting review commit 32df76cb77dc83edf4737e61bf0889bc43821845.
All 644 preexisting tracked files retain exact SHA-256, including every
approved asset, registry, previous pilot file, receipt, narrative and
workflow. Only this new v02 directory is added. The original sources match
the currently selected canonical main d9b6b91604b72115c5402253f00924665e957727.
No engine files or Chapter 4 files were edited or used as repair inputs.

QA ACTUALLY RUN:
92 pixel, mask, dimension, opacity, link, deterministic replay and
preservation checks: PASS.
Canonical check, storyboard smoke and Chapter 3 narrative: PASS.
Local Chromium and Firefox gallery checks: 26/26 PASS. Browser canvas
comparison independently confirms exactly six different decoded pixels.
Native and exact 4x CSS sizing, all image decoding/hashes, evidence links,
mobile layout and embedded portable HTML were checked.

NOT RUN THIS ITERATION:
Live public Pages deployment; game engine/runtime QA; sync tool self-tests;
the selected-artwork browser regression (its earlier 60 checks are historical,
not a new v02 pass). Approved bytes and sync code did not change.

Publication to the existing remote review branch is authorized by Nate's
standing instruction and is required for each completed review version.
Branch publication means neither selection nor approval. Both approvals
and v01 files remain unchanged. No canonical registration, integration,
main merge, Pages workflow change or Pages deployment is authorized.

STOP FOR NATE REVIEW BEFORE EXPANDING ANY REPAIR.

REPLAY:
python3 repair.py
The repair script is portable with originals/, masks/ and sources/ intact.
python3 validate.py and build_review.py expect this version's original
location inside the storyboard worktree so the whole prior-tree checks
and reference copies can resolve. Browser QA requires installed Playwright
and Chromium/Firefox; set NODE_PATH to its installation before running
node qa-browser.cjs. All browser serving is local and is not a deployment.
