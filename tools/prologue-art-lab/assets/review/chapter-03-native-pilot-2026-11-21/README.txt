OUT OF ORDER — TWO-SCENE NATIVE PIXEL-ART RECONSTRUCTION PILOT
Nate review — November 21, 2026 (America/New_York)

BOTH CANDIDATES ARE GENERATED / UNSELECTED.
This package authorizes no approval, reapproval, registration, replacement,
gameplay integration, public Pages deployment or next reconstruction batch.
Paper Emergency is excluded.

Open index.html for the gallery with native and exact 4x matching-scale
comparisons, 8x detail crops, approved Chapter 2 and Reception references,
large conceptual references, hashes and imperfections.
standalone-gallery.html embeds all preview images for portable viewing;
keep the companion files to use its evidence/source/QA links.

Base: latest canonical main verified before work,
d9b6b91604b72115c5402253f00924665e957727.
Isolated local storyboard branch: art/ch3-native-pilot-20261121.
Only this new review directory is added. No files previously tracked by the
base commit were changed; all 493 retain their SHA-256 checksums.

The two candidates are directly constructed at 314x206 from native integer
polygons, lines and glyphs using Python/Pillow. No generated/reference image
is read by reconstruct.py. No downsampling to native size, sharpening,
posterization, random texture or automatic palette-reduction step occurs.
Only previews/crops use enlargement: exact 4x and 8x NEAREST.

This is coordinate-authored procedural art. The complete primitive logs,
canvas/palette/font definition, Python source and semantic RGBA layers are
preserved. Deterministic rebuilding reproduces both candidate hashes.
That supports native construction of these two rasters; it does not claim
hand-painted authorship or prove artistic quality. The built-in imagegen
large references remain of unresolved original native-grid authorship.
They are conceptual references only, preserved unchanged, with exact prompts
and tool output filenames/receipts. They are not final candidates.

COLOR COUNTS (exact RGB, no arbitrary 64-color limit):
Backstage: old 25,215; candidate 45.
Locomotion: old 16,885; candidate 36.
Inspected Chapter 2 scenes: 62–64; Reception scene: 868; Chapter 1 foyer: 210.
The gallery includes exact counts and hashes for every selected comparison.
All candidate PNGs are opaque RGB, 314x206. Enlargements are 1256x824.

WHAT TO EVALUATE:
Backstage: broader concrete planes and cleaner cables, scenery, props and
attached clapper. The EXIT sign has moved from the leaf to above the door
for native readability; evaluate this composition change. Props are more
geometric than Chapter 2. Clapper paddles need a final silhouette judgment.
Locomotion: moving belt left, centered padded pit, sparse net spanning it,
stationary landing behind/right. Architecture, signs and 30 remain. Evaluate
net height/contact, landing width, console overlap and the simpler presenter.
Both images are cleaner but flatter. Do not adopt this as the remaining
chapter's standard without evaluating that tradeoff visually.

QA ACTUALLY RUN:
- 110 image/link/source/preservation checks: PASS.
- Deterministic native rebuild, exact 4x/8x pixels, dimensions, opacity: PASS.
- All 493 preexisting tracked files byte-unchanged: PASS.
- Canonical check, sync QA, storyboard smoke: PASS.
- Chapter 3 narrative, artwork briefs, prepare briefs --check: PASS.
- Local gallery Chromium + Firefox: 22/22 PASS, including mobile dimensions.
- Existing selected-artwork browser regression: 60/60 PASS.
Browser snapshots and complete logs/results are under qa/.
An initial gallery run stopped on an overly broad QA selector; it was fixed
and the complete gallery checks then passed in both browsers.

NOT RUN: live Pages deployment, gameplay/engine runtime QA, user study.
No engine files or main-menu assets were accessed or edited in this pilot.

FILES:
candidates/                  Two unselected native PNGs.
approved/                    Byte-identical current selected comparison PNGs.
references/                  Read-only copies of approved style/identity refs.
concept-references/          Large built-in imagegen conceptual references.
previews/                    Exact 4x exports.
closeups/                    Matching-coordinate exact 8x analytical crops.
sources/                     Native scene operation logs and semantic layers.
history/first-native-draft/  Preserved earlier local draft (not an alternative
                            selection or an older canonical approval).
reconstruct.py              Editable native drawing source.
manifest.json               Candidate status, metrics, provenance and limits.
preservation-baseline.json  SHA-256 of all 493 starting tracked files.
generation-prompts.json     Exact built-in concept-reference prompts.
generation-receipts.json    Actual built-in output filenames/receipt metadata.
validate.py                 Pixel, hash and preservation checks.
qa-gallery.cjs              Local gallery browser checks.
qa/                         Actual validation results, logs and screenshots.

REPRODUCE:
python3 reconstruct.py
python3 validate.py

Browser QA requires Playwright with Chromium/Firefox installed. Set NODE_PATH
to the directory containing the installed playwright package, then run
node qa-gallery.cjs. The gallery is tested through a local HTTP server with
the /CYOA-storyboard/ project prefix; this is not a public deployment.

build_gallery.py derives the review package from the pinned repository and
constructs its comparison metadata. The repository base and its approved
assets must be available to rebuild the comparison copies and baseline.
