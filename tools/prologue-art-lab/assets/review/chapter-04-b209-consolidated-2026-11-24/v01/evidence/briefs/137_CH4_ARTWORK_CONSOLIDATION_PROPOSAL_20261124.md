# Chapter 4 artwork consolidation — proposal for Nate's approval

**Status: APPROVED by Nate on 2026-11-24 and APPLIED on this review branch (§14).** Not merged or deployed. §1–§13 are the proposal exactly as approved; §14 records what was implemented and how it was validated. The game-engine capabilities (C1/C2) are a separate game PR.

- Machine-readable plan: [137_CH4_ARTWORK_CONSOLIDATION_PLAN_20261124.json](137_CH4_ARTWORK_CONSOLIDATION_PLAN_20261124.json)
- Node-by-node coverage (all 120 nodes, now → proposed): [137_CH4_NODE_ART_COVERAGE_20261124.tsv](137_CH4_NODE_ART_COVERAGE_20261124.tsv)
- Verification and dry-run results: [137_CH4_ARTWORK_CONSOLIDATION_VERIFICATION_20261124.json](137_CH4_ARTWORK_CONSOLIDATION_VERIFICATION_20261124.json)
- Tool: [`tools/sync/ch4-consolidation.py`](../tools/sync/ch4-consolidation.py) — `build` / `verify` / `dry-run --game <checkout>` / `evidence`
- Review sheets: [`docs/137_evidence/`](137_evidence/), composited 1:1 from the selected bytes

## 1. The decision

Approving all four items lets the next agent run the approval-time edit set (§11) and resume production with the revised B2-09 (§10).

1. **Approve the seven retirements in §4.** Six are portrait pose remaps; every approval, byte and record is kept. The seventh, CH4-B2-16, takes its closer background out of the *active* registry; its record and SHA are preserved verbatim (§5).
2. **Approve one renderer-required background beyond your 17: CH4-NEW-18, a shared ballroom/reception closer background (§7.1).** The current renderer cannot show the organizer or Bixby without it, and the approved alternative CH4-02 is lobby-specific. If you would rather rule CH4-02 acceptable in the ballroom, the target stays at 62.
3. **Choose how portrait-less voices and text-led exteriors are presented (§8, C1/C2).** The recommendation is a small, generic game-engine change, authorized separately in the game repo. The alternatives are listed.
4. **Confirm the revised B2-09 scope (§10).** It supersedes the "Automatic next group" paragraph of docs/136.

## 2. Verified state (Phase A)

| Item | Audit checkpoint | Verified now (2026-11-24) |
|---|---|---|
| Canonical `main` | `b56f91e` | **`96e3c2a`**: PR #30 merged 17:42Z, registering all six B2-08 primaries **including CH4-B2-46** and six references. Pages run 45451489365 green. |
| Review branch `art/ch4-batch01-review-20261121` | `6ddaf56` | `6ddaf56`, unchanged |
| Open PRs | — | #28 (Chapter 3 reconciliation draft, unrelated) |
| Game `out-of-order` main | — | `3a8e07a` (PR #22, Chapter 3 gameplay). Chapter 4 is `notForGameplay`. |

Discrepancies with the audit, and how this proposal handles them:

- **B2-08 is already registered, CH4-B2-46 included** (PR #30, merged while this review was being prepared). So "omit B2-46 from registration" can no longer apply. B2-46 is retired the same way as the other portraits: a pose remap, approval preserved. Approved primaries on main are now **52** (46 + 6), as the audit projected.
- **docs/136 "Automatic next group" still instructs the old four-asset B2-09** (refreshment-table scene and background, Bixby delighted *and* commanding). §10 supersedes it. No Bixby art exists on any branch.
- The audit's Library files (four ChatGPT links) **could not be opened here**. Every number below was re-derived from the repository by the tool. Where my per-item split differs from the audit, I say so (§3).
- Observation only, not added to your refinement list: **CH4-02** (lobby background) has 689 colours, against 123–172 for the other approved Chapter 4 backgrounds.

## 3. Before / after

| | Count | Source |
|---|---:|---|
| Original logical primary requirements | **90** | 23 scenes + 36 speaker poses + 15 dialogue backgrounds + 8 Focus A + 4 item images + 4 fatal (identical to the v08 BATCH2-INVENTORY) |
| Approved primary selections on main | **52** | 46 at audit + 6 B2-08 |
| Proposed retirements | **7** | §4 |
| Approved retained | **45** | |
| Genuinely new primary art (your list) | **17** | §9 |
| Renderer-required exception | **1** | CH4-NEW-18, §7.1 |
| Resolved by reuse | **6** | §6 |
| Resolved by narrative / presentation | **14** | §7 |
| Localized-state families | **12** | §9.3; 13 approved references preserved |
| **Active primary target** | **62** (45 + 17), or **63** with NEW-18 | vs 90: −31% (62) / −30% (63) |
| Remaining new production | **17**, or **18** with NEW-18 | vs 38 unproduced: −55% / −53% |

The audit split the 21 demands that need no new art as **9 reuse / 12 narrative**. My independent split is **6 reuse / 14 narrative / 1 renderer exception**. The boundary moves because the current renderer cannot reuse a ballroom background that doesn't exist yet, and because five closer backgrounds become unnecessary once their only speakers carry no portrait. The active count changes only through NEW-18.

## 4. Retirements (awaiting approval)

All seven were checked against the story text and the actual pixels. In each case the replacement is the same character (or the same location) and is already approved and in use on the neighbouring nodes.

| Retire | → Replacement | Affected node(s) | Physical continuity | Sheet |
|---|---|---|---|---|
| CH4-B2-33 Porter curious | CH4-B2-21 uncertain | `hotel_collection_staff_pass` | He examines the pass and consults his clipboard; B2-21 is hand-to-chin with the clipboard. The next node already uses B2-21. | [sheet](137_evidence/retire-ch4-b2-33.png) |
| CH4-B2-34 Porter relieved | CH4-B2-22 practical | `hotel_collection_staff_pass_recognized` | "Our visiting inspector. Back again?" Same smile, welcoming arm, clipboard. The next node already uses B2-22. | [sheet](137_evidence/retire-ch4-b2-34.png) |
| CH4-B2-28 Bride hopeful | CH4-B2-26 determined | `hotel_ring_show_bride` | You *show* the ring; it is still yours. B2-26 has empty hands. The ring-holding grateful pose (B2-29) stays only on `hotel_bride_ring_handover`, the one node that takes the ring (verified). | [sheet](137_evidence/retire-ch4-b2-28.png), [ring continuity](137_evidence/bride-ring-continuity.png) |
| CH4-B2-36 Auctioneer bureaucratic | CH4-03 showman | `hotel_auctioneer_lot14_recall` | Same podium background and gavel. The RECALL AUTHORIZED stamp is narrated. The preceding dispute node already uses CH4-03. | [sheet](137_evidence/retire-ch4-b2-36.png) |
| CH4-B2-39 Wedding assistant sympathetic | CH4-B2-40 apologetic | `hotel_staff_lavatory_move_boxes` | Neither pose holds a prop, so the boxes, ribbon and clipboard live in the B2-07 background states. Soft note: the node opens "The assistant looks sympathetic"; B2-40's gentle clasped-hands smile still reads that way, and the rest of the node is apology. | [sheet](137_evidence/retire-ch4-b2-39.png) |
| CH4-B2-46 Boiler engineer practical | CH4-B2-43 careful | `hotel_boiler_staff_access`, `hotel_water_outage_confirmation` | Same identity. Neither pose holds the gauge or the key; the gate opening is narrated. The service-passage background is unchanged. | [sheet](137_evidence/retire-ch4-b2-46.png) |
| CH4-B2-16 Boiler-access closer background | CH4-B2-23 service-passage background | `hotel_collection_slip_spotted` | You are still **outside** the boiler door beside Lot 31 until the porter "opens the boiler-room door and ushers you through". B2-23 shows exactly that spot, which is *more* truthful than B2-16 (the view from inside). **The boiler-access main scene CH4-B2-13 is kept.** | [sheet](137_evidence/retire-ch4-b2-16.png) |

**Mechanism** (applied only on approval: `apply_proposal` in the tool; full edit set in §11):

- **Portraits:** change the 7 `pose` fields on the 7 nodes above. Each retired record stays `approved` with its preview and bytes, plus an appended note "RETIRED FROM ACTIVE CHAPTER 4 COVERAGE". The note goes after the first SHA, so the importer's approved-SHA rule is unaffected. Reverting = restoring 7 pose strings.
- **CH4-B2-16:** in the game importer (`convert.js` `bgFor`), a scene's own `portraitBackground` always wins, and `backdrop` is not an authorable node field. So the record must leave `scenes[grand_bellevue/boiler_access]`, and `portraits[hotel_porter:alarmed].portraitBackgroundScene` changes from `grand_bellevue/lobby` to `grand_bellevue/service_passage`. The lobby node `hotel_chair_stapler_caught` keeps the lobby background, because the lobby scene has its own (proved by the game importer, §12). The public preview copy leaves `assets/selected/`, and `qa-smoke`'s pinned active-catalog count goes from 52 to 51 Chapter 4 records.

## 5. CH4-B2-16 record, preserved verbatim

Nothing is lost. The bytes stay at the immutable source commit, the approval stays in docs/131 and docs/103, and this is the exact record that would leave the active registry:

```json
{"title": "Boiler access conversation background", "kind": "portrait-background", "status": "approved", "dimensions": "564x278", "assetPath": null,
 "suggestedFilename": "art/portraits/grand_bellevue/backgrounds/boiler_access.png",
 "prompt": "Exact owner-selected B2-03 v01 CH4-B2-16; preserve existing approved PNG bytes. Authoritative source manifest and production provenance pinned in docs/131.",
 "notes": "OWNER APPROVED AND SELECTED UNCHANGED — Nate, 2026-11-23; B2-03 v01 CH4-B2-16. SOURCE-DERIVED native interpretation, not independent native-grid authorship. Exact source 24c79bff8d33b5997ccb6b7aa7bb86293afef291:tools/prologue-art-lab/assets/review/chapter-04-batch02-2026-11-22/b2-03-v01/native/CH4-B2-16-v01.png; SHA-256 e396db0771247012401cccf3a481d329947381a677c445ccc0a04d61b21f77f3. Manifest, masks, material/structural/letter layers, detailed sources and prompts are pinned in docs/131. Not integrated; runtime assetPath remains null. The two B2-01 plumber alternatives remain separate and unapproved; earlier v01 approvals remain selected."}
```

Public preview `assets/selected/pending-integration/scenes/grand_bellevue/boiler_access/portraitBackground.png`, SHA-256 `e396db07…f77f3`.

## 6. Reuse (6)

| Demand | Uses | Nodes | Why it's truthful |
|---|---|---|---|
| Scene `wedding_entry` | CH4-05 ballroom | `entry_door_reverse_end` | "hurries you into the reception hall": the ballroom *is* the reception. |
| Scene `refreshment_table` | CH4-05 ballroom | 3 Bixby nodes | "At the edge of the reception". The wheel-on-ice-bucket boat and the water under the door are localized prop/water treatments. |
| Scene `bridal_corridor` | CH4-B2-19 service passage | `hotel_bridal_corridor_exit` | "The service passage leads back toward the staff lavatory". This passage is already the approved scene of both shortcuts to the bridal room. |
| Scene `freight_lift` | CH4-NEW-03 upper salvage | `hotel_freight_wc_misunderstanding` | The ride is narrated; you end "on the mezzanine… The lift remains behind you". **NEW-03 must show the lift doors and the W.C. panel.** |
| Portrait Bixby commanding | CH4-NEW-05 Bixby | `hotel_bixby_emergency` | Same man; he never holds the wheel in either portrait. |
| Background `refreshment_table` | CH4-NEW-18 ballroom background | 3 Bixby nodes | Same room. |

[Reuse source sheet](137_evidence/reuse-sources.png). How reuse is registered is constraint C3 (§8).

## 7. Narrative / presentation (14) and the one exception

| Demand | Constraint | Reason |
|---|---|---|
| Scenes `arrival`, `forecourt`, `courtyard` | C1 | Short exterior arrivals (3 nodes) and park-bound departures (2 nodes): text-led transitions. No approved exterior matches (no glass doors and flowers; loading lane shows a staircase being removed). |
| Portraits `bridal_door_ai`, `bathroom_ai`, `hotel_lift_voice` | C2 | Machine voices: no anthropomorphic portrait. |
| Portraits `hotel_salvage_clerk`, `hotel_wedding_guest`, `hotel_attendant` | C2 | Minor exchanges; environmental storytelling in NEW-03 and NEW-04. |
| Backgrounds `bridal_dressing_room`, `bridal_lavatory`, `freight_lift`, `upper_salvage`, `public_corridor` | C2 | The only speakers there have no portrait, so nothing is drawn over a closer background. |

### 7.1 Exception: CH4-NEW-18, the ballroom / reception closer background

Five dialogue nodes take place in the ballroom: the organizer ×2 and Bixby ×3. Every layered speaker draws over a 564×278 opaque background for its scene, and none exists for the ballroom. The approved CH4-02 shows the lobby auction podium and the framed piano lot that are in the lobby scene CH4-01 ([sheet](137_evidence/ballroom-background-exception.png)), so it would place the organizer in the lobby. One shared background covers both the ballroom and the refreshment table. **Recommended: approve it as the 18th new image.**

## 8. Renderer constraints (verified against game main `3a8e07a`)

**C1 — every node draws a scene image.** `story-flow.js:169` always calls `setSceneArt` for the node's scene; a scene key without a record becomes a DEV PLACEHOLDER (an error in an approved build). Affects 5 nodes.
- *Recommended fallback:* a game-side rule that a text-led scene keeps the previous image. For the chapter opening that is Chapter 3's last image, which matches "You leave the People's Pavilion behind." Needs separate engine authorization.
- *Interim alternative, no engine work:* `reused` records pointing arrival/forecourt at CH4-B2-06 and courtyard at CH4-B2-07. Not recommended: it adds movers and a sofa the text never mentions.

**C2 — a dialogue node must be led by a speaker with a portrait.** `rules.js:1788` rejects an incidental voice leading a node, and `stage.js` `chapterArtKeys` throws without a portrait. Affects **15 nodes**: door AI 6, bathroom AI 4, lift voice 1, clerk 2, guest 1, attendant 1.
- *Recommended fallback:* a generic engine extension that lets an incidental voice lead a dialogue node, presented as Narrative B (no portrait aperture) with its NAME: label. The label machinery from docs/104 §4 already exists. No canon change.
- *Alternative (canon edit, needs approval):* switch the 15 nodes to narrative mode with `{say, who}` runs, wording unchanged.
- *Not recommended:* drawing 6 portraits and 5 backgrounds.

**C3 — reuse cannot bind before integration.** The pending binding accepts only an `approved` record whose first notes SHA matches the bound file. A `reused` record needs a real `art/` assetPath; that is the existing reception and `wc_key` precedent.
- *Fallback:* register reuse as `reused` at integration time; no new keys. Bixby commanding can instead take the pose remap used for the retirements.
- Until then the reuse lives in this record only. No new scene IDs, Focus keys, flags or runtime bindings are introduced anywhere.

## 9. Remaining artwork workload

### 9.1 New primary art: 17 (+1)

| ID | Requirement | Brief constraints |
|---|---|---|
| NEW-01 | Bridal dressing room (scene) | Hosts the privacy-indicator and AutoFit states as localized changes. |
| NEW-02 | Bridal lavatory (scene) | Counter, three shells, **no** toilet or concealed fixture. |
| NEW-03 | Upper salvage mezzanine (scene) | Must also show the **freight-lift doors and W.C. panel**, the hatch and the service stairs. |
| NEW-04 | Public corridor (scene) | Dry reusable base; flooding is a state family. |
| NEW-05 | Commodore Bixby (portrait, one expression) | Cap and green paddle; **empty hands**. The wheel and bucket are environment props only. |
| NEW-06 | Wedding organizer (portrait) | Must match the organizer already drawn in CH4-05. |
| NEW-07 | Bridal privacy panel (Focus A) | |
| NEW-08 | AutoFit gown (Focus A) | Motor and manual-slack as states. |
| NEW-09 | Three seashells (Focus A) | |
| NEW-10/11 | Lot 53 dispute ticket — slot / inspection | Records exist (not-started). |
| NEW-12/13 | Wedding ring — slot / inspection | Decide the inscription reveal first: the record note says "do not reveal", but `hotel_ring_inspect_inscription` authors AS IS, WHERE IS. |
| NEW-14–17 | Final Occupancy · Pressed and Steamed · Folded for Convenience · Made to Measure | Popups and outcomes unchanged; never the protagonist's face. |
| **NEW-18** | Ballroom/reception closer background | §7.1 |

### 9.2 Quality refinement: 5 approved images (flag only; nothing overwritten)

| Asset | Colours | Benchmark |
|---|---:|---|
| CH4-01 Lobby | 2,542 | Chapter 2 scenes: 58–64 (28 measured) |
| CH4-04 Restroom | 2,524 | |
| CH4-05 Ballroom | 3,669 | |
| CH4-B2-03 Restroom background | 49,487 | Other approved Chapter 4 backgrounds: 123–172 |
| CH4-B2-11 Loading-dock background | 83,600 | |

[Scene sheet](137_evidence/refinement-scenes.png) · [background sheet](137_evidence/refinement-backgrounds.png).
- **Requirement:** native redraws that keep each approved composition, layout, materials, objects and humor, published as an **unselected** review batch. The approved PNGs stay selected until you pick replacements. Counts are diagnostic, not rejection.
- **Sequencing:** six state families derive from CH4-01 and CH4-04 (§9.3), so produce them from the refined masters to avoid doing them twice.

### 9.3 Localized-state families: 12

| Family | Base | Status |
|---|---|---|
| chair_and_ring_states | B2-24 / B2-25 | **Covered**: 3 approved references |
| staff_boxes_attempt | B2-37 / B2-41 | **Covered**: 4 approved references |
| boiler_pressure_state (+ inspection hold, staff bypass) | B2-42 / B2-47 | **Covered**: 6 approved references |
| lobby_door_removal · lot61_open_and_packed | CH4-01 | To derive **after** lobby refinement |
| restroom_active_leak · braced_or_contained · flood · stall_lifting_and_removed | CH4-04 (+B2-03) | To derive **after** restroom refinement |
| bridal_privacy_status | NEW-07 / NEW-01 | With B2-12 |
| gown_motor_manual_slack | NEW-08 | With B2-13 |
| public_corridor_flood | NEW-04 | With B2-11 |

Any flattened runtime PNGs must be derived reproducibly from approved native masters and masks. Timing is left to integration, with no new nodes, flags or keys.

## 10. B2-09 is paused; revised scope

**This supersedes the "Automatic next group" paragraph of docs/136.** Do not start the old four-asset B2-09.

The revised B2-09, once you approve this proposal:
- **NEW-05:** Bixby, one portrait.
- **NEW-18:** the shared ballroom/reception background (if approved).
- **NEW-06:** the organizer, who shares that background (natural to batch together).
- The localized wheel-and-bucket treatment on the existing ballroom.
- No commanding portrait and no refreshment-table scene.

Suggested order after that: B2-10 upper salvage (NEW-03) → B2-11 corridor (NEW-04) → B2-12 dressing room and privacy panel (NEW-01/07) → B2-13 gown (NEW-08) → B2-14 lavatory and shells (NEW-02/09) → fatal ×4 → items ×4 → refinement batch → restroom/lobby state families.

## 11. Approval-time edit set (exactly what "yes" applies)

Implemented in `apply_proposal()` and proven on a throwaway copy by `dry-run`:

1. `story/chapters/chapter-04.wip.json`: 7 `pose` values (table in §4). No other byte.
2. `story/artwork.draft.json`:
   - Append the retirement note to 6 portrait records.
   - Move `scenes[grand_bellevue/boiler_access].portraitBackground` out (§5).
   - Set `portraits[hotel_porter:alarmed].portraitBackgroundScene = grand_bellevue/service_passage`.
3. `story/artwork-preview.json` and `assets/selected/…/boiler_access/portraitBackground.png`: drop the one CH4-B2-16 preview.
4. `tools/storyboard/qa-smoke.mjs`: active Chapter 4 count 52 → 51.
5. docs/103 ledger line and a docs/137 completion record. Then the normal PR → check-canon → Pages flow.

Fully reversible with `git revert`. Nothing in any review package, approval document or source commit is touched.

## 12. Validation (all actually run on this branch, 2026-11-24)

| Check | Result |
|---|---|
| `ch4-consolidation.py verify` | **PASS 266/266.** 90 requirements re-derived; 120 nodes reachable, all links resolve; 7 Chapter 3 entry routes; 8 hidden d6; 4 fatal endings with complete popups; every item and item-gated card present; 52 approved: native size, alpha contract, selected = preview = approval SHA, 52/52 pinned source blobs identical, 47/47 exact-4× previews = nearest-neighbour ×4 (Batch 1's 5 have no recorded 4× preview); 13 supplemental references byte-exact; ring rule; B2-16 → B2-23 through the importer rule; B2-13 main scene kept; exactly 8 nodes change presentation; no story/assets/viewer byte differs from `96e3c2a`. |
| `ch4-consolidation.py dry-run --game <out-of-order>` | **PASS 21/21.** check-canon and qa-smoke pass on base *and* proposed trees. Proposed Chapter 4 differs **only** in the 7 pose fields. Chapters 1–3, Prologue, items, manifest, death export and game-integration are byte-identical. The **game's own importer** (`convert.js` @ `3a8e07a`) resolves exactly the 8 retirement nodes differently, puts slip_spotted on the service-passage background, keeps stapler_caught on the lobby, and gives byte-identical Prologue + Chapters 1–3 runtime output. |
| `check-canon.mjs` | PASS (RESULT: OK) |
| `qa-smoke.mjs` | PASS (256 art records) |
| `export-death-presentations.mjs --check` | PASS (6 popup records) |
| `prologue-art-lab/qa/qa-static.mjs` | PASS |
| `qa-sync.mjs`, `qa-ch3-reference-supersession.mjs`, `qa-ch3-reboot-candidate.mjs`, `qa-ch3-artwork-briefs.mjs`, `qa-legacy-render.mjs` | PASS |
| `qa-browser.js` (Chromium + Firefox) | PASS 26/26 |
| `qa-artwork-preview.js` (Chromium + Firefox) | PASS 60/60 |
| `verify-ch4-b208-selection.py` | PASS (407 checks) |
| `verify-ch4-batch1…b207-selection.py` | **FAIL as expected.** Point-in-time PR verifiers assert "exactly N new selections" against their own base, so they fail on every later commit. Not a regression. |
| Not run | `qa-timeline.js` (no viewer change); game browser suites (Chapter 4 is not importable for gameplay yet). |

## 13. Carried-over open items (not changed here)

- Inline speaker tags without portraits: `hotel_second_porter`, `autofit_system`, and `hotel_service_foreman` (which differs from `hotel_salvage_foreman`). From v08 `inlineSpeakerQuestions`; all are incidental voices, and C2 doesn't apply because they never lead a node.
- The stale ring-inscription art note (NEW-13).

## 14. Approval and implementation (2026-11-24)

**Nate's decision:**
- approve all four items in §1;
- the active production target is **63** (45 retained + 17 new + CH4-NEW-18);
- C1 and C2 are to be built as a separate, reviewable game-engine PR;
- B2-09 is revised as in §10 / [docs/138](138_CH4_B209_REVISED_PRODUCTION_BRIEF_20261124.md);
- mark docs/136's old next group superseded and correct the ring brief;
- keep the five refinement candidates selected until replacements are reviewed;
- preserve every original, approval, source and hash.

**Applied on this branch** (`python3 tools/sync/ch4-consolidation.py apply`, then build / verify / game-check):

| Change | Detail |
|---|---|
| `chapter-04.wip.json` | **8 `pose` values only**: the 7 retirements of §4, plus `hotel_bixby_emergency` commanding → delighted (one Bixby expression). No text, choice, flag, item, d6 or ending changes. |
| Six retired portraits | Remain `approved` with their bytes, previews and full approval notes. Their notes are now prefixed with the viewer's existing archive convention (`ARCHIVED / RETIRED / UNUSED — CHAPTER 4 CONSOLIDATION …`, Chapter 3 precedent), so they move to the **Archived** filter. The original notes follow unchanged and the first SHA-256 is still the approved one. |
| CH4-B2-16 | The record leaves `scenes[grand_bellevue/boiler_access]`. It is preserved verbatim in the [retired-artwork ledger](137_CH4_RETIRED_ARTWORK_LEDGER_20261124.json), with its exact bytes **moved, not deleted**, to `tools/prologue-art-lab/assets/approved/retired-selections/chapter-04/CH4-B2-16-v01.png` (SHA-256 `e396db07…f77f3`, also intact at source commit `24c79bf`). `hotel_porter:alarmed.portraitBackgroundScene` is now `grand_bellevue/service_passage`. |
| **No-image presentation records** | 3 `format: "text-led"` scenes (arrival, forecourt, courtyard) and 6 `format: "voice-only"` speakers (door AI, bathroom AI, lift voice, salvage clerk, wedding guest, attendant). They are `approved` with no path, preview or nested art. `check-canon` rejects any image on them (6 mutation tests), `register-art` refuses them, and the viewer labels them NO IMAGE. They are the canonical signal the game's C1/C2 capability consumes. |
| Ring brief | `wedding_ring_lot31` slot and inspect briefs now match the approved reveal: a tiny maker's mark and **AS IS, WHERE IS.**, small enough that the unread description stays true. Status stays `not-started`. |
| qa-smoke | Catalog count 256 → 264 (−1 CH4-B2-16, +9 no-image records), plus a voice-only assertion. |
| docs | docs/136 "Automatic next group" marked SUPERSEDED (original kept, struck through). A docs/103 ledger entry. [docs/138](138_CH4_B209_REVISED_PRODUCTION_BRIEF_20261124.md) revised B2-09 brief and queue. |

**Not changed:**
- CH4-01, CH4-04, CH4-05, CH4-B2-03 and CH4-B2-11 stay selected.
- No review package, approval record, source file or hash is modified or deleted. `verify` checks this: the only non-additions under docs/ and the art-lab assets are the two annotations.
- Reuse scene keys (C3) still bind at integration.

**Validation of the applied branch:** see the PR and the [verification JSON](137_CH4_ARTWORK_CONSOLIDATION_VERIFICATION_20261124.json).

**Follow-up (2026-11-24):** player speaker correction, merge of storyboard main 38bdb99 (PR #28), B2-09 v02 disposition and validation are in [docs/139](139_CH4_SPEAKER_CORRECTION_MAIN_RECONCILIATION_AND_B209_V02_DISPOSITION_20261124.md). The deferred Chapter 4 integration gaps are in [docs/140](140_CH4_GAMEPLAY_INTEGRATION_WORK_PACKAGE_20261124.md).
