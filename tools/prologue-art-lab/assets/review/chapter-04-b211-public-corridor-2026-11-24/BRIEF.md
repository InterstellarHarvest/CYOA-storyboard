# Chapter 4 B2-11 — Codex art-production brief

**Scope:** `CH4-NEW-04`, one reusable **314×206 opaque public corridor** main scene, plus only the necessary `public_corridor_flood` conditional reference frame(s) with **identical architecture**. The corridor is the new art batch after Nate approved B2-10 v03; do not resurrect retired Chapter 4 assets or run another consolidation audit. All produced PNGs must remain **UNSELECTED** until Nate's visual approval. No runtime, narrative, flag or gameplay changes.

## Read before production

- `docs/129_PERMANENT_PIXEL_ART_PRODUCTION_STANDARD_20261122.md`; `docs/137_CH4_ARTWORK_CONSOLIDATION_PROPOSAL_20261124.md`; `docs/138_CH4_B209_REVISED_PRODUCTION_BRIEF_20261124.md` (B2-11 queue).
- The actual `story/chapters/chapter-04.wip.json` nodes `hotel_stall_public_corridor_walk` (dry) and `hotel_flooded_public_corridor` (flood). Other conditional links should be checked rather than invented.
- [Nate's B2-10 approval and **new anti-micro-revision stop rule**](https://github.com/InterstellarHarvest/CYOA-storyboard/blob/115152a5e42e5877a21bde5ccc0d050608bdda56/tools/prologue-art-lab/assets/review/chapter-04-b210-upper-salvage-2026-11-24/PMO-V03-APPROVAL-AND-STOP-RULE.md). This is now the art-PMO production standard. Reference the strongest approved Chapter 2 and Chapter 4 *main scenes* at native size and exact nearest 4×. Nate's successful auctioneer-room screenshot in the PMO conversation is an additional **positive** composition benchmark (attach it in the Codex session if available), not a new object list for this scene.

## The actual corridor geometry and state

The **dry** route follows the embarrassing stall-crane escape: the player walks away publicly; the hall leads to a **service door/staff lavatory**, **stairs toward collection**, and a **side passage/exit to the outside**. The corridor should look like the same Grand Bellevue institution as the approved lobby, service passage, maintenance, and ballroom—showy surface treatment covering cramped facilities and intrusive technology. At 314×206, make the routes distinct without building a noisy forest of tiny signs. Do not draw the player or a detailed guest portrait in the main scene.

The **flooded** scene is the same exact camera and architecture: water races over hotel carpet and spreads beneath corridor doors; an attendant struggles with a WET FLOOR sign, which falls and floats away; the player sees the **open maintenance hatch**, staff passage and side exit. **One clearly flooded supplemental frame with the fallen/floating sign is probably sufficient**. Add another only for a genuinely distinct story-critical state—not a separate image for each sentence. Minor changes to the hatch/sign/water are allowed; all unchanged dry background pixels and perspective must stay exact. No new guest/attendant portraits; consolidated canon uses voice-only dialogue.

## Visual direction and stop rule

Use **legible silhouettes, physically convincing materials, clear foreground–midground separation, selective warm/cool lighting and purposeful restrained pixel clusters**. Think bureaucratic pseudo-luxury in the spirit of *Brazil*: patched carpet, ornate-yet-cheap doors, concealed ducts, absurd tech, a building pretending everything is in order. Main-scene NPCs are visually simple if any incidental distant bystanders appear; portraits, not 314×206 scenes, carry facial detail.

If generating a detailed large concept reference, **paint/reinterpret the game artwork independently at its native logical grid**. Do not just shrink it or conceal downsampling beneath palette reduction. Preserve accurate `SOURCE-DERIVED` provenance if appropriate, original prompt/source and editable native layer recipe. The first published version should be **selection-worthy** after one internal composition/legibility QA. Do not publish a schematic candidate and rely on six micro-edits later. Only genuine route, story, composition or material-readability failures justify a targeted revision; when a scene works, stop.

## Deliverable and boundaries

Publish a review-only package under `tools/prologue-art-lab/assets/review/chapter-04-b211-public-corridor-2026-11-24/v01/`, with separate native dry master and flooded reference frame(s), 4× nearest previews (1256×824), native/4× before-after and approved-benchmark comparisons, gallery `online.html`, PNG hashes, provenance/prompt/recipe, structural layers and automated/native-browser QA. Commit to `art/ch4-b211-public-corridor-review-20261124`; push only when safely authenticated. If generator access is blocked, report the specific blocker—**do not substitute inferior vector/shape-code illustration and label it finished**.

**Never modify** `main`, `assets/selected`, previously approved sources, narrative/game, PR #32, or other review batches. Do not self-approve, register or deploy the corridor.
