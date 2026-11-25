# Chapter 4 Artwork PMO — B2-10 v03 approval and production stop rule

**Owner decision (2026-11-24):** Nate approves the **v03** upper-salvage scene and authorizes moving on. The approved candidate is `v03/native/CH4-NEW-03-upper-salvage-v03.png`, **314×206**, with exact nearest-neighbor 4× preview. Its originating review commit is `7963f507568a6e6f9a50ffda3755103f9674bdd3` on `art/ch4-b210-upper-salvage-review-20261124`. **APPROVED FOR REGISTRATION, NOT YET REGISTERED/SELECTED BY THIS NOTE.** Preserve exact candidate bytes, provenance, earlier review versions, and source layers.

This owner decision supersedes the `PMO-V02-ART-DIRECTION.md` instruction to keep refining the rack or foreground porcelain. Do **not** make v04 or reopen the rejected stair/rail redraws. Any formal selection, registry update and publication validation remain separate engineering work.

## Owner's broader correction: stop endless micro-revisions

Nate supplied a successful Chapter 4 ballroom/auctioneer scene as an example of an acceptable *main scene*: readable human silhouette and pose, recognizable doors/chair/table/industrial fittings, clear warm-versus-cool material zones, and visual texture that serves the composition. It is detailed but **not busy to the point of confusion** at 314×206. Use that quality of staging and hierarchy alongside the strongest approved Chapter 2 scenes. Do not demand pixel-by-pixel equivalence or maximum apparent detail from every supporting scene.

For all subsequent Chapter 4 art production:

1. **Start at the right level.** Before drafting, choose comparable approved *scene-class* references (Chapter 2 plus approved Chapter 4), establish subject, routes, silhouettes, lighting and focal hierarchy, then create a detailed large reference if useful. The large image is a reference only; construct the deliverable at its final native grid. No image-downscale masquerading as native illustration.
2. **Make the first published candidate selection-ready.** Codex should self-review native size and exact nearest-neighbor 4× before publishing, including a one-second recognition test for gameplay-relevant objects. Put effort into first-pass composition and material character instead of publishing schematic imagery that needs repeated patches.
3. **Simplify by prioritizing, not stripping the room bare.** A few recognizable, convincingly modeled props and clear negative space beat a collection of tiny icons; enough background richness can remain when it recedes behind focal objects. Scene NPCs should stay legible and simpler than their portraits.
4. **Stop when it works.** Do not request or perform microscopic material, palette, rail, trim or prop edits merely because a comparison reveals differences. A good-enough approved scene should advance. Technical QA is necessary but does not itself establish visual quality; likewise, artistic differences from Chapter 2 are not automatically defects.
5. **Use targeted revision only for real blockers:** unreadable route/prop, incorrect story object/state, continuity contradiction, visual focal confusion, broken perspective that changes navigation, or a substantial style mismatch. Prefer one coherent revision covering the blockers. If the underlying idea remains wrong, reconsider the design rather than accumulating v04–v09 patches.
6. **Preserve owner authority.** New candidates remain UNSELECTED until Nate approves. Once approved, keep them byte-identical through registration, verify hashes and runtime mapping, and do not modify unrelated approved art or draft PR #32.

## Immediate workflow

- **Engineering / Claude:** Register the **exact v03** file as B2-10 `CH4-NEW-03` through the established approval / registry workflow; verify SHA-256, canonical mapping and preservation of previous selections. No new artwork changes in this step.
- **Artwork / Codex:** Proceed to consolidated **B2-11** (`docs/138`): `NEW-04` public corridor dry base and the `public_corridor_flood` state references, based on the same geometry. No guest or attendant portraits (voice-only). Show the common base and water variants at native / exact 4× next to the relevant approved Chapter 2 and Chapter 4 scenes. Publish UNSELECTED to review; do not alter canonical main or game integration.

**Production principle:** Strong, coherent first passes; visually legible scenes; decisive acceptance. Do not spend repeated cycles chasing cosmetic perfection in already serviceable art.
