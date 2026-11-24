# Chapter 4: player speaker correction, main reconciliation, B2-09 v02 disposition

**Status:** review-branch work on PR #31, still a draft. Nate's decisions of 2026-11-24:
- approve the speaker correction;
- defer the integration gaps ([docs/140](140_CH4_GAMEPLAY_INTEGRATION_WORK_PACKAGE_20261124.md));
- preferred merge order is #31 then game #25, but **neither merge is authorized yet**;
- no publishing, deployment, artwork selection or new B2-09 generation.

## 1. Player speaker correction: who `visitor` → `you`

**Audit** ([machine-readable](139_CH4_PLAYER_SPEAKER_AUDIT_20261124.json)): Chapter 4 contains **97** `visitor` values. Every one is the `who` of a `{say, who}` run in a node's text, and there is no other use of `visitor` in Chapter 4.
- **96** are all-caps player lines (Chapter 4's player voice), each spoken to the node's NPC or to the scene's voice.
- **1** is lower case: "Can you get it out?" in `hotel_collection_ring_porter_recovery` (text run 3). It follows your own line about the manifest, is addressed to the porter, and he answers it ("We'd better."), so it is the player. It is kept in lower case exactly as authored.
- The two narration mentions of "visitor" (the Chapter 3 badge text *FASTEST SATISFIED VISITOR*) are not speaker ids and are untouched.

**Change:** 97 × `"who": "visitor"` → `"who": "you"` (`tools/sync/ch4-consolidation.py apply-speaker`). The diff is exactly those 97 lines. No wording, capitals, choices, conditions, flags, items, dice or endings changed. `verify` replays it from the audit and requires equality.

**Chapter 3 is unaffected:**
- `story/chapters/chapter-03*.json` are byte-identical to main.
- In the game's importer, Chapter 3 keeps its NPC `visitor` (9 lines, cast name "VISITOR"). Chapter 4 now has 0 `visitor` and 97 `you` runs.

**Rendering (game PR #25 branch, Chromium + Firefox, local verification):**
- The corrected player lines render in the player's Choices face in the dialogue box. Per docs/84 the box never labels the player.
- NOTES shows them under **YOU:**. The lower-case line is the player too.
- An NPC `visitor` in the same conversation is still labelled **VISITOR:** in the box and in NOTES.
- No page errors.

## 2. Storyboard main merged into PR #31

`main` 38bdb99 (PR #28: 29 Chapter 3 artwork reconciliations) was merged into the branch as **e2c9e76** (history-preserving merge commit). There were **no textual conflicts**. The four overlapping files combine orthogonal changes:

| File | Main (PR #28) | This PR | Result |
|---|---|---|---|
| `story/artwork.draft.json` | 29 Chapter 3 records → `integrated` with production paths | Chapter 4 consolidation edits | Both kept. `verify`: registry = main + exactly the approved Chapter 4 edits |
| `story/artwork-preview.json` | Chapter 3 previews re-sourced to the game build | CH4-B2-16 entry retired | Both kept. Preview = main minus only CH4-B2-16 |
| `tools/storyboard/qa-artwork-preview.js` | +1 Chapter 3 filter check; provenance accepts the renamed repo | NO IMAGE checks | 64 checks (62 + 2) |
| `tools/storyboard/qa-smoke.mjs` | Integrated provenance accepts `out-of-order` | Catalog count 264 | No count drift from main (main 256; this PR −1 + 9 = 264) |

**Chapter 3 preserved** (`verify`): all **29** selections (defined as main's own QA defines them) keep their record (status `integrated`, 29 production `assetPath`s, approval notes), preview, SHA-256 bytes and `story/game-integration.json` exactly as main.

**Chapter 4 preserved:**
- The 90 requirements and every disposition derive identically at 96e3c2a and 38bdb99 (PR #28 changed no Chapter 4 record).
- Approvals, 7 retirements, 9 no-image records, active target 63 and the docs/138 scope are all unchanged.

**No hash changes. Changed expectations:** none from the merge. The only count change on the branch is the approved one (catalog 256 → 264; selected previews 197 → 196).

## 3. B2-09 v02 (review branch `b896f50`): asset-by-asset disposition

This package was produced under the superseded four-asset brief. Everything stays exactly as published and **UNSELECTED**. Nothing was deleted, overwritten or selected.

The review branch now carries a dated **STOP** notice at the top of its `AGENTS.md` and `README.md` (commit 1459c4e, documentation only) suspending automatic continuation.

Inspected natively and at 4×, against approved CH4-05, CH4-02, the Chapter 4 portraits and docs/129.

| Asset | Superseded role | Disposition under docs/138 | Why |
|---|---|---|---|
| **CH4-B2-49 v01** Bixby delighted | delighted portrait | **REUSE candidate for NEW-05, unchanged.** Present for Nate's selection; no new generation. | Meets every canon detail: miniature naval cap, green auction paddle in his pocket, **empty hands** (the wheel is never held). The broad, open gesture can also carry the emergency line. 53 colours (approved Chapter 4 portraits: median 62). Same identity as the B2-48 figure. |
| **CH4-B2-50 v01** Bixby commanding (whistle) | commanding portrait | **REDUNDANT.** Preserve; do not select. | The revised brief has one Bixby expression. |
| **CH4-B2-51-emergency v02** | emergency state of the refreshment background | **REUSE candidate as the NEW-18 neutral base.** | Pixel diff vs B2-51: it differs **only** in the wheel region (wheel removed, bucket kept). The ornate **ballroom double doors** are in view, and the architecture matches CH4-05 (duct, swags, green wainscot, sconces). So it works as the shared ballroom-threshold background for the organizer and Bixby, with no prop that would be wrong for the organizer's nodes or after the hand-off. |
| **CH4-B2-51 v01** (wheel on bucket) | primary background | **REVISE in role:** keep as a localized state for `hotel_commodore_bixby` only, never as the base. | Its base plate **bakes in the wheel boat**, so it would always be visible, including for the organizer and after the wheel is handed over. 148 colours (approved backgrounds 123–172). |
| **CH4-B2-51-trade v02** | trade state | **REUSE candidate as the `hotel_bixby_trade` localized state** (the rubber-band fender tied on). | It differs from the emergency plate only around the bucket. |
| *(missing)* water under the ballroom door | — | **The one new localized state to derive** from the neutral base: a thin water sheet from the door's gap. Every other pixel stays identical. | Canon: water creeps "from beneath the ballroom door" (`hotel_commodore_bixby`), and a guest slips on it (`hotel_bixby_emergency`). **No B2-51 plate shows any water.** |
| **CH4-B2-48 v02** refreshment alcove scene | main scene | **REDUNDANT.** Preserve; do not select. | `refreshment_table` reuses approved CH4-05 (docs/137). **Defect found:** a translucent red rectangle around the chair legs (a leftover plate or mask, like v01's wheel-mask bug), also present in B2-48-trade. 157 colours. |
| **CH4-B2-48-emergency / -trade v02** | main-scene states | **REDUNDANT.** Preserve as reference only. | They are states of a redundant scene. Their slip and fender staging can guide the water and fender states. |
| *(none exists)* Wedding organizer, NEW-06 | — | **NEW generation needed** (after approval). | No candidate exists in any package. It must match the organizer drawn in CH4-05. |

**Recommendation for B2-09 (avoids duplicate production):**
- Select or approve from what exists: **B2-49** as NEW-05, **B2-51-emergency** as the NEW-18 base, and **B2-51 / B2-51-trade** as localized states.
- Produce only **two** new things: the **organizer portrait** (NEW-06) and the **water-under-door state** of the NEW-18 base.
- Registration keys follow docs/138 (for example `scenes:grand_bellevue/ballroom#portraitBackground`), at selection time only.
- Nothing is selected or generated until Nate says so.

## 4. Validation (local, 2026-11-24, branch c56e5b7)

**New failures: none.**
- `ch4-consolidation.py verify`: **302/302**. That covers main + edits exactly, the 29 Chapter 3 selections unchanged, the 90 requirements identical at both bases, and the 97-line speaker audit replay.
- `game-check`: **14/14** against main 38bdb99. The game importer resolves exactly the 9 remapped nodes differently, and Prologue–Chapter 3 output is byte-identical.
- check-canon, qa-smoke (264), death export, qa-static, qa-sync, qa-ch3-reference-supersession, qa-ch3-integration-state, qa-ch3-reboot-candidate, qa-ch3-artwork-briefs, qa-legacy-render: PASS.
- Browser (Chromium + Firefox): storyboard 26/26, artwork preview **64/64**, timeline 136/136.
- **Pages build**, emulated locally (every step of `pages.yml` except configure / upload / deploy, with sparse pinned gallery checkouts): **PASS on this branch and on main**. Site 2,056 files on both; previews 197 → 196, as approved.

**Known and expected:**
- All nine `verify-ch4-*-selection.py` scripts fail on **untouched main too**. They are point-in-time PR verifiers, so these are not regressions. On this branch b208 stops at the intended CH4-B2-46 remap.
