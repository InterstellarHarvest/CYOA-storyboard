# Chapter 3 — Narrative Lock and Artwork PMO Handoff

**Owner ruling (Nate): 2026-11-18.** Chapter 3 is **approved as currently authored for artwork generation**. This replaces the earlier pending prose-review gate in docs/110. The approval does **not** declare art complete, activate Chapter 3 in the public storyboard manifest, merge the draft branch, or authorize changes to the game. Future wording/choice changes remain possible by separate owner ruling; artwork should stay pinned to the exact current script until such a change.

## Approved narrative source

- Source: `story/chapters/chapter-03.reboot-candidate.json`, content blob SHA `857ffdf1bc9432cf4bbbfd7819f5f430a06d9036`, on review branch `story/ch3-reboot-20261118` (draft PR #5).
- 34 reachable new Chapter 3 nodes, 28 authored route variants (includes optional inherited-item variants), seven unique living endpoints, two approved hidden d6 checks, and three conditional inherited-item actions.
- `wc_key` SHOW, `family_portrait_photo` SHOW, `red_stapler` USE (consumes stapler) are approved. The held `timing_clicker` adds +1 only to the locomotion check, never consumed there.
- All surviving paths leave the People's Pavilion without restroom access, and the alleged Original remains an **unexplained record datum**, never an established embodied other person.
- `story/archives/chapter-03-pre-reboot-20261118.json` preserves the previous 62-node discarded Chapter 3 verbatim, SHA-256 `02beb009b667f6930408850db91ca078262df6807ecc7236d044a3a4dc0dcbe1`. Its choices, old images and popup briefs are historical only.
- Public manifest `story/storyboard-manifest.json` still marks legacy Chapter 3 `archived`. Only explicit `?review=ch3-reboot` in the isolated preview viewer opens the approved reboot candidate.

## Canonical asset inventory from the approved script

### Fourteen distinct scene IDs requiring new visual briefs (reuse a master only if the scene remains visually truthful)

1. `pavilion_reboot/arrival`
2. `pavilion_reboot/restroom_entrance`
3. `pavilion_reboot/human_verification_stage`
4. `pavilion_reboot/urgency_stage`
5. `pavilion_reboot/locomotion_stage`
6. `pavilion_reboot/backstage`
7. `pavilion_reboot/exterior_exit`
8. `pavilion_reboot/surprise_stage`
9. `pavilion_reboot/service_exit`
10. `pavilion_reboot/record_printer`
11. `pavilion_reboot/record_scanner`
12. `pavilion_reboot/paper_emergency`
13. `pavilion_reboot/exit_vestibule`
14. `pavilion_reboot/courtesy_stage`

### Human portraits

- `pavilion_attendant`: `idle`, `alarmed`, `quiet` (three consistent poses).
- `pavilion_presenter`: `idle`, `excited`, `alarmed`, `relieved` (four consistent poses).
- They appear in nine speaker/scene combinations: attendant at restroom entrance, record printer, record scanner, service exit and courtesy stage; presenter at human-verification stage, urgency stage, surprise stage and service exit. Plan the requisite close-POV portrait backgrounds for each relevant view; don't assume one generic background or a scaled scene will match the shot.
- The visitor and machine voices do not yet require separately authored speaker portrait IDs. Ask the owner before expanding the cast.

### Not needed

- **Zero fatal endings; zero Chapter 3 death-popup illustrations.** Every one of the seven `end:true` Chapter 3 nodes is surviving; the review viewer previously mislabeled them fatal and has been corrected on the review branch. Treat `deathPopup`/approved fatal story content, not `end:true` alone, as the fatal signal.
- **Zero newly authored Focus A close-ups** in the locked script; propose one only if it materially helps an existing interaction and obtain approval before making new nodes/requirements.
- **Zero new Chapter 3 inventory items or item illustrations.** Reuse previously selected Facilities Key, House Family Photo, Red Swangline Stapler and Timing Clicker art. Do not revive the 16 obsolete `pavilion_*` inventory definitions.

## Art direction and constraints

- **Mood:** funny, human and physically ridiculous first; unsettling institutional assumptions underneath. Real, functioning restroom and human faces, not endless anonymous records offices. Slightly wrong retro-futurist Exposition, industrial cool-grey family; no brass/gold glamour or sterile sci-fi polish.
- **Never show the protagonist's face.** The House photograph shows only their torso/lap, no head. No image should assert the existence or appearance of an embodied Original.
- **Scenes:** author pixel art at exactly **314×206 logical pixels**. Presentation may use 4× nearest-neighbor; avoid destructive resampling/blur.
- **Portraits:** **564×278** portrait images at native size; human foreground transparent RGBA over a matching, tighter, genuinely closer portrait background. Not a blurred enlargement of the 314×206 scene and not a much wider panoramic background.
- **Item inspect** spec (only if later approved): 565×451, but no new inspector art is required in this handoff.
- Existing game's shell/portraits and Chapters 1–2 selected artwork are locked. Do not redraw or replace them; maintain family resemblance and the chosen camera language.

## Production and review workflow

1. Read this handoff, docs/109–110, approved candidate JSON, the public artwork catalogue and approved style references. Map each scene/pose to its source nodes and camera requirement. Avoid treating old Chapter 3 descriptions as current prompts.
2. **Quarantine legacy art calls:** preserve all old `pavilion/*` scene/focus/death/Registrar records and provenance, but mark them clearly archived/retired/unused using existing schema-compatible metadata. Do not invent new status enum values or delete historical records.
3. Author **new** `pavilion_reboot/*` artwork records and exact prompts in an isolated artwork branch/review package, with dimensions, visual continuity, per-state dependencies, and source node references. Do not silently generate from the old `pavilion/*` prompts.
4. Generate in small coherent batches (suggest first: real restroom entrance + attendant + human-verification presenter views), produce a public gallery with native and 4× nearest views and exact prompt/sha provenance, and ask Nate to choose/approve. **Selection constitutes artwork approval**; do not keep selected images marked unfinished.
5. After approval, register selected source hashes/status in the public storyboard artwork metadata and preserve existing approved art untouched. Production `assetPath` is set only when gameplay integration is actually confirmed; no invented asset paths.
6. Handoff to Claude Gameplay PMO for engine mapping/import and full runtime QA only after art selections and narrative/source pins are ready. Gameplay `main` is a separate production decision.

## Verification and handoff safety

- `node tools/storyboard/qa-ch3-reboot-candidate.mjs` — PASS: 34 nodes, 28 authored route variants, seven living endpoints, two checks, three item actions, complete preview timeline groups.
- `node tools/storyboard/qa-smoke.mjs` — PASS; `node tools/sync/check-canon.mjs` — OK; `node tools/sync/qa-sync.mjs` — PASS 22/22. These tests check the draft graph and existing active storyboard; they are **not** a playable Chapter 3 engine import or an art completeness proof.
- The review viewer's `FATAL ENDING` misclassification is corrected on the isolated review branch to distinguish `SURVIVING ENDING`. Preserve that fix and do not commission fatal art based on legacy red node labels.
- No direct changes to public `main`, gameplay repo or Chapters 1–2 are authorized by this handoff.
