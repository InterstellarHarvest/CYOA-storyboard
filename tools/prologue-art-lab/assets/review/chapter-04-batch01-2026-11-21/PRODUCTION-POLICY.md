# Out of Order — Chapter 4 artwork production policy

## Latest Chapter4 owner decisions — 2026-11-22

B2-01 v01 (five assets from81cf3b5f022510737bdd2d4ba3703e0173d86772) is now APPROVED and SELECTED unchanged, canonical main fde5708e0043972feeae0309e8a1d1836e756dae, docs128, PR21. All ten approved Chapter4 assets stay exact. Later plumber palette alternatives are new UNSELECTED candidates, never automatic replacements.

Nate explicitly requests compact Chapter1/2 NPC color ramps: preserve anatomy, face/hair/hands/fabric detail, but fewer deliberate shade steps, no excessive gradient shading or fine-grained surface noise. New NPCs use a64-tone no-dither fit calibrated to approved Chapter2 references, not a global palette limit for environments. Actual artwork at native/exact4x remains the visual gate. Follow this direction in subsequent batches.

Current new reviews live in the sibling chapter-04-batch02-2026-11-22 package: b2-02-v01 (six loading-dock/service-arrival assets) and v02-npc-palette (both requested plumber alternatives). Publish completed UNSELECTED candidates with originals, prompts, provenance, comparisons, hashes and QA; no narrative/gameplay or engine integration.


## Owner selection — 2026-11-22 (supersedes review-time status below)

Nate approved all five exact Batch1 selections unchanged from v08: CH4-01/02 v05, CH4-03 v08 and CH4-04/05 v07. They are now APPROVED and SELECTED, not integrated. [Canonical registration/closeout](https://github.com/InterstellarHarvest/CYOA-storyboard/blob/ee5948f14144d2bd99b75432e8d58422e8958bf1/docs/127_CH4_BATCH1_APPROVAL_COMPLETION_20261122.md); main commit `ee5948f14144d2bd99b75432e8d58422e8958bf1`, PR20. All five public selected PNGs and registry statuses were verified against immutable owner hashes. [Approval record](BATCH1-APPROVED-20261122.json), [public verification](BATCH1-PUBLIC-VERIFICATION-20261122.json). The old UNSELECTED statements in preserved historical packages describe the review-time state; this later approval supersedes them only for those five exact assets.

New work: [B2-01 five-asset gallery](../chapter-04-batch02-2026-11-22/v01/index.html). New Batch2 candidates remain UNSELECTED. Preserve all approved PNGs and every earlier version. No narrative/gameplay/engine integration.


Owner decision: Nate's policy update in this session supersedes the earlier independent-native-authorship requirement for portraits. **Visual consistency with approved artwork takes priority.** Keep this record with subsequent Chapter 4 review batches; do not reopen the resolved production-method decision.

- Use approved NPC artwork as the primary portrait style reference. Preserve generated originals, exact prompts, input references and hashes.
- Source-derived portraits are authorized: controlled quality-preserving reduction to **564×278**, transparent foreground, targeted final-resolution cleanup as needed, and exact nearest-neighbor **2256×1112** previews. Describe the actual derivation honestly. Never label a source-derived asset independently authored at native resolution.
- Retain face, likeness, anatomy, expression, hair, hands, clothing, proportion and illustration richness. Compare actual artwork with approved NPCs at native size and exact 4×. No arbitrary palette limit or unnecessary simplification.
- Internally compare/refine intermediate attempts, and publish the strongest completed candidate rather than every experiment. Seek owner input only for meaningful creative decisions or final selection.
- Main scenes continue to prioritize correct perspective, coherent lighting, readable composition, rich material rendering, purposeful native-grid detail and simplified small NPCs. Current restroom/ballroom backgrounds are independently drawn at **314×206**; their illustrated NPC layers are source-derived to address Nate's scene-NPC quality feedback. The whole frames are disclosed as hybrid art, with exact **1256×824** previews.
- Publish completed UNSELECTED review candidates, gallery/dependencies, originals, derivation/source, prompts, manifests, hashes, comparisons and QA to `art/ch4-batch01-review-20261121`. Verify remote commit and image accessibility. Review publication does not approve or integrate artwork.
- Preserve every previous candidate. Keep v05 lobby/background and preferred v07 restroom/ballroom exact PNGs and hashes frozen. Do not change main, narrative, gameplay, production assets/workflows or approval records.

## Current production split

**CH4-03:** preferred `portrait-study-02` direction is retained. The independent drawing-code route remains discontinued. The previously proposed source-derived exception is **AUTHORIZED by this later policy**, so it is no longer owner-decision-pending. Prepare the production-resolution candidate from the unchanged preferred original, with disclosed reduction and edge cleanup. Final artwork selection is still **UNSELECTED / Nate's decision pending**.

**CH4-01/02:** frozen v05 owner-review candidates, unchanged and UNSELECTED. Exact hashes are resolved in v08/evidence/frozen-preferred-environments.json.

**CH4-04/05:** preferred v07 restroom/ballroom are now frozen exact owner-review candidates; no cosmetic revisions. Subsequent story-required state art must use separate files and preserve these bases.

The concise [illustrator handoff](v06/CH4-03-ILLUSTRATOR-HANDOFF.md) remains available only if an independently painted version is later commissioned; it is not a prerequisite for the now-authorized source-derived portrait candidate. No commission or external contact has been initiated.

## v06 implementation disclosure — scene NPC quality correction

Nate rejected the blocky code-drawn scene figures and supplied actual approved Pavilion scene-NPC examples. The rejected figure passes are not used. Final environments combine native-drawn room backgrounds with separately generated, cropped/reduced character layers matching those examples. Preserve every character master, prompt, crop/scale/placement recipe and layer hash. Label the resulting full scenes **hybrid / source-derived NPC composites**, never independently native-authored whole frames. This implements the visual-quality priority; it does not register creative approval.
