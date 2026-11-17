# Presentation-mode audit — Prologue to Chapter 3 (2026-11-17)

**Scope:** whether each scene uses the right gameplay surface (Narrative B, NPC dialogue, Focus A), whether player speech and actions are selectable rather than narrated, where the new **single-choice conversational beat** fits, and what art each correction would need. An authoring and presentation audit, **not** a rewrite.
**Source of truth:** public storyboard after the Chapter 3 approval sync (main `066ea36`, docs/106). Engine behaviour was read from the game at the PR #2 stack head `a15b240` (`game/js/rules.js`, `story-flow.js`, `stage.js`, `tools/story-import/convert.js`) and docs/72 §2–3.
**Status:** Batch 1 (Chapter 1, below) is on branch `agent/presentation-audit-ch01-20261117`, **not merged**. Chapter 2 unchanged (locked). Chapter 3 unchanged beyond docs/106, pending the Story & Creative Director's prose.

## 1. What the engine already supports (verified in code, no extension needed)

| Need | Supported by | Notes |
|---|---|---|
| NPC dialogue with portrait | `mode: 'dialogue'`, `speaker`, `pose` (or the House's per-scene complete **views**) | The importer and validator reject `speaker`/`pose` on non-dialogue nodes (`rules.js` "speaker is for dialogue nodes only"). |
| NPC speech vs stage directions | `text` runs: plain string = the speaker's speech; `{desc}` = direction; `{say, who}` = another speaker | Dialogue speech is never quoted; narration (B) quotes speech. |
| Player speech vs action on cards | `kind: 'spoken'` (card drawn in quotes, `stage.js:647`) vs `kind: 'action'` (action ink `#8e2c1f`) | Authored card text never contains quotes. |
| Mixed speech + action | The card carries one kind; its **echo** `say` may be runs mixing `{act}` and `{say}` | Echo only in dialogue nodes. |
| **Single-choice beat** | A dialogue node whose only card is one `spoken`/`action`/mixed choice to the next node | Already used: Prologue `reception_key_discrepancy`, Chapter 1 `orientation_*`. The echo lands in the transcript, then the NPC replies. |
| Paginated narration | Presentation-only CONTINUE between paragraph groups in B; paged CONTINUE in Focus A | Not authored. |
| Focus A | `mode: 'focus'` + `focus` id, usually an excursion closed with `back` | A `focus` field on a **narrative** node is inert at runtime. |
| SHOW in dialogue | Only authored `show` entries; none means nothing happens | Converting a node to dialogue adds no unauthored interaction. |

## 2. Counts

**Nodes by presentation mode** (storyboard data; Chapter 1 shown before → after Batch 1):

| Chapter | Nodes | Narrative B | Dialogue | Focus A | Spoken cards | Action cards | CONTINUE | System |
|---|---|---|---|---|---|---|---|---|
| Prologue | 29 | 13 | 16 | 0 | 8 | 14 | 20 | 0 |
| Chapter 1 | 36 | 33 → 32 | 2 → 3 | 1 | 5 → 0 | 39 → 44 | 12 | 1 |
| Chapter 2 | 99 | 91 | 2 | 6 | 0 | 80 | 58 | 10 |
| Chapter 3 | 62 | 62 | 0 | 0 | 0 | 58 | 27 | 10 |

Chapter 3 also carries six `focus` references and two `speaker` fields on narrative nodes; both are inert (and `speaker` is invalid) until those nodes change mode.

| Measure | Prologue | Ch 1 | Ch 2 | Ch 3 | Total |
|---|---|---|---|---|---|
| Suspected incorrectly presented scenes | 0 | 7 (1 fixed) | 0 | 11 | **18** |
| Mis-typed choice cards | 0 | 5 (fixed) | 0 | 0 | **5** |
| Potential **new** single-choice beats | 1 | 1 | 0 | 5 | **7** (+2 existing beats to re-word) |
| Potential missing NPC portraits | 0 | 0 portraits; 2 House views if Batch 3 is approved | 0 | 2 (Attendant, Mrs. Pruitt) | **2 portraits + 2 views** |

The Chapter 1 spoken-card count falls to 0 because Batch 1 only fixes typography: those five cards were reported actions shown in quotes. Batch 2 restores real player speech once the Story Director supplies the wording.

## 3. Overall assessment

**Recurring, but concentrated.** The Prologue and Chapter 2 are presented correctly. The Prologue's two NPC encounters are full dialogue with portraits, stage directions, and spoken, action and branching cards. Chapter 2 is machine- and environment-driven, and its two NPC beats already use dialogue. The problem sits in the two chapters drafted later around a talking institution:

- **Chapter 1:** the House is a conversational NPC in about 20 nodes, but only 2 use dialogue mode. Its lines elsewhere sit as quoted narration. Its five `spoken` cards were stage directions ("ASK WHERE THE BATHROOM IS."), which the renderer wraps in quotes.
- **Chapter 3:** every node is Narrative B. Conversations with the Attendant, the Original and the Registrar are written as `Name:` transcripts inside narration, including the player's own lines ("You: Can I use it?"). That is exactly the passive pattern the owner described.

A constraint shapes Chapter 1: approved scene-state art relies on some House nodes staying narrative (`plant_adoption` pedestal overlay, `portrait_print` album on the cabinet). Converting them would hide integrated art, so they stay Narrative B.

## 4. Findings

Confidence: H high, M medium, L low. Art impact: **none** (no new art), **view** (existing integrated portrait/view), **new** (art call required).

### Prologue

| Node | Current | Recommended | Issue | Proposed correction | Art | Conf |
|---|---|---|---|---|---|---|
| `drone_intercepts` | Dialogue, CONTINUE only | Dialogue + single beat | After "Your position has also been discontinued, along with 499,999 others." a generic CONTINUE stands where the protagonist would react | Replace the CONTINUE with one player card; wording from the Story Director (placeholder intent: a stunned spoken reaction). Destination unchanged | none (drone portrait integrated) | M |
| `signed_ / disputed_ / declined_response`, `reception_*` replies | Dialogue, CONTINUE | Keep | CONTINUE closes the NPC's reply to a choice the player just made; a further beat would be forced | None | none | H |
| `expo_property_counter` … `expo_donated` | B with quoted clerk | Keep B | The clerk is incidental; player speech is already selectable (two spoken cards) and narrated per the B rule | None | none | H |
| `reception_key_discrepancy` | Dialogue, one action card | Keep | Already a correct single-choice beat | None | none | H |

### Chapter 1 (House of Tomorrow)

| Node | Current | Recommended | Issue | Proposed correction | Art | Conf |
|---|---|---|---|---|---|---|
| `welcome_home` | Dialogue; 2 `spoken` cards | Dialogue; cards as action (done) → spoken wording (Batch 2) | Cards describe actions but render in quotes | **Batch 1:** kind → action. **Batch 2:** spoken lines, e.g. "YES, PUT MY THINGS AWAY." / "I'LL KEEP MY THINGS." (placeholders) | none | H |
| `orientation_refusal` | B with the House's quoted reply | **Dialogue** (done) | The House answers the player's refusal: continuous conversation | **Batch 1:** dialogue in the integrated foyer view; same words as desc runs + speech | view | H |
| `orientation_storage` | B; 1 `spoken` card | Keep B; card as action (done) | The hatch and arm are a physical event (B is right); the card was mis-typed | **Batch 1:** kind → action. **Batch 2:** spoken "WHERE IS THE BATHROOM?" (placeholder) as a single beat | none | H |
| `dinner_arrival` | B; `spoken` "ANSWER FOR MARTIN." | B, card as action (done); dialogue if Batch 3 | Mis-typed card; the House directly asks a question at the table | **Batch 1:** kind → action. **Batch 3:** dialogue with a dining view | new (dining view) | M |
| `foyer_attempt` | B; House speech; 5 conditional choices | Dialogue | A sustained exchange about leaving; choices are replies to the House | Convert to dialogue (foyer view exists); keep all five conditional cards, effects and destinations | view | M |
| `dinner_redirect` | B; House announcement + door lock | Dialogue or keep | Short announcement plus physical lock; borderline | Owner choice; foyer view exists | view | L |
| `comfort_offer`, `refused_both`, `refreshments` | B; House questions | Dialogue (Batch 3) | The House asks and the player answers; lounge/dining have no House view | Convert only if the owner commissions lounge + dining House views | new (2 views) | M |
| `storage_reclaimed`, `martin_*`, `wardrobe_passage`, `chair_*`, `bathroom_*`, `showroom_reset`, `portrait_intro` | B with House lines | Keep B | Ambient announcements over physical events or reveals; the art carries the moment | None | none | H |
| `plant_adoption`, `portrait_print` | B | **Keep B** | Approved scene-state art (pedestal; album on cabinet) needs the scene, not a portrait | None | none | H |
| `portrait_before_album` | Dialogue, CONTINUE | Dialogue + single beat | "Now then! Shall we continue?" is a question answered by a generic CONTINUE | One player card (wording from the Story Director) → `bathroom_arrival` | none | M |
| `album_closeup` | Focus A | Keep | Correct | None | none | H |

Branches, flags, items and checks: none touched by any Chapter 1 proposal.

### Chapter 2 (Biology Park) — locked, report only

| Node | Current | Recommended | Issue | Proposed correction | Art | Conf |
|---|---|---|---|---|---|---|
| All 99 | B 91 / dialogue 2 / Focus A 6 | Keep | Environment and machinery dominate; the groundskeeper and Courtesy Conductor already use dialogue; the antidote kits use Focus A correctly | **None** | none | H |
| `gardener_choices` | B after `gardener_arrival` dialogue | Keep (observation) | The portrait drops while the player answers the machine; acceptable because all three choices are physical | None this pass | none | L |
| `gardener_promotion` | B | Keep (observation) | Machine speech ("Congratulations! You are now Acting Director…") is unquoted in narration; it may be printed card text | Clarify with the Story Director only if Chapter 2 is reopened | none | L |

No Chapter 2 art is affected and its art queue is not reopened.

### Chapter 3 (People's Pavilion) — plan only, pending the Story Director's prose

| Node | Current | Recommended | Issue | Proposed correction | Art | Conf |
|---|---|---|---|---|---|---|
| `human` | B; transcript "Attendant: … / You: Can I use it? / Attendant: …" | B intro → **dialogue** with the Attendant + **single beat** | The player's line is scripted into narration | Keep the sign/plaque/pipe narration in B; Attendant exchange in dialogue; single spoken card **"CAN I USE IT?"** (approved words); the three route choices unchanged | **new** (Attendant portrait) | H |
| `satisfy` | B; transcript "Attendant: … / You: I haven't used the toilet. / …" | Same treatment | Same | Single spoken card **"I HAVEN'T USED THE TOILET."** (approved words) before "That isn't what the transcript says."; A/C choices, item and check unchanged | new (same portrait) | H |
| `witness` | B with `speaker`/`pose` (invalid) | **Dialogue** (`original_witness`, screened) | A conversation with the Original that the player requested; currently not importable | Author the pending prose as dialogue; the automatic recorder detection stays a scene effect; B/C unchanged. Never reveal the Original's nature | existing record (not-started), partition only | H |
| `grand` | B with `speaker: registrar` (invalid) | **Dialogue** (`registrar`) | The Registrar's hearing | Dialogue; three approaches unchanged | existing record (not-started) | H |
| `grand_0` exchange (`contest_inadmissible`, `end_admin`) | Approved four-line exchange lives in notes / ending text | Dialogue + **single beat** | "You: Then the record is wrong." is a natural player beat | Card `grand_0` (mixed: indicate the record + speak) → Registrar line → single spoken **"THEN THE RECORD IS WRONG."** → "Or your presence is." → the d6≥4 check on that card; odds, nonstacking bonus and destinations unchanged. Needs one new intermediate node | existing | H |
| `registry` | B; Registrar quoted; "You point out… You ask…" | Dialogue + single beat | Player speech narrated | Dialogue; one beat for "which kind am I supposed to be?" (wording needed); the two registry checks unchanged | existing | M |
| `original_refusal`, `original_refusal_denied`, `contest_inadmissible` | B transcripts | Dialogue | Registrar–Original exchange; "You insist…" duplicates the card | Dialogue with `{say, who: 'original_witness'}` runs; drop the narrated duplicate (prose change → Story Director) | existing | M |
| `disposition` | B; "You suggest… you ask…" | Dialogue, **still exactly two choices** | Player speech narrated | Possibly one beat before the two choices — **owner must confirm** it does not breach "exactly two choices" | existing | M |
| `reconcile`, `records` | B (prose pending) | Decide when prose arrives | Staffed counters; unknown speakers | Author as dialogue if a person is meaningfully engaged | possibly new | L |
| `c02_a` (Mrs. Pruitt) | B; one quoted line | B event + short dialogue | A named human witness whose testimony returns at the finale | Owner decision; her portrait is already noted as a future requirement | **new** (Pruitt portrait) | M |
| `end_admin`, `end_two`, `end_identity_review` | B with Registrar/Original lines | Keep B (aftermath) | Endings close in narration; converting would split ending nodes | None unless the owner wants the final exchange in dialogue | none | M |
| `b_*`, `c_*`, `b0*`, `c0*` results | B; machine voices ("VISITOR RECORDS:", "CONTROL ROOM:") | Keep B | Machines and signage, incidental | None (`c01_a/b` "You ask…" could become beats; low value) | none | L |
| Six `focus` refs on B nodes (`b_gate`, `c_workshop`, `c02_a`, `registry`, `a_fourth`, `end_model_citizen`) | Inert | Decide per node | Focus A is never shown | `b_gate` counter and `a_fourth` source photo suit Focus A excursions; `end_model_citizen` (an ending) should stay B | Focus art exists as briefs | M |

Routes, flags, inventory, d6 checks, nonstacking bonuses, endings and death behaviour are unchanged by every Chapter 3 proposal; the only structural addition is one intermediate node for the `grand_0` beat.

## 5. Before and after

**Chapter 1 `orientation_refusal` (Batch 1, implemented):**
- Before (B): *You insist on keeping your possessions. The speaker pauses. "Certainly. We would never put your things away without permission." A quiet motor starts somewhere behind the wall.* Card: `"ASK FOR THE BATHROOM AGAIN."` (quoted, though it is not a line).
- After (dialogue, House foyer view): direction *You insist on keeping your possessions. The speaker pauses.* · House: *Certainly. We would never put your things away without permission.* · direction *A quiet motor starts somewhere behind the wall.* Card in action ink: `ASK FOR THE BATHROOM AGAIN.`

**Chapter 3 `human` (proposed):**
- Before (B): *…You ask an attendant where the actual restroom is. Attendant: You're looking at it. You: Can I use it? Attendant: Certainly. You're using it right now.*
- After: B narrates the sign and plaque → dialogue, Attendant: *You're looking at it.* → **single card** `"CAN I USE IT?"` → Attendant: *Certainly. You're using it right now.* → B narrates the vibrating service pipe → the three approved choices.

**Chapter 3 `grand_0` (proposed):** card `CONTEST THE ORIGINAL'S EXCLUSIVE CERTIFICATION` (echo: *you indicate the certified departure record* + "According to this, I've already left. Yet here I am.") → Registrar: *Yes. Your departure was processed very efficiently.* → **single card** `"THEN THE RECORD IS WRONG."` → Registrar: *Or your presence is.* → optional photo/Pruitt callbacks → hidden d6≥4.

## 6. Proposed art calls (for later review; none generated or registered)

1. **Pavilion Attendant portrait**: transparent 564×278 foreground over the `pavilion/human_requirements` / `satisfaction_demo` portrait backgrounds (new backgrounds needed, or one shared). A tidy 1960s exhibit attendant, unflappable and courteous; the house style (no brass/steampunk, clean clusters); no protagonist.
2. **Mrs. Pruitt portrait** (only if approved): a real human employee, cardigan, ledger, badge INDEPENDENT CHOICE SUPERVISOR — CLASS II; over a Human Behavior Workshop portrait background.
3. **House of Tomorrow complete views** (only if Batch 3 is approved): `house_of_tomorrow/lounge` and `house_of_tomorrow/dining`, matching the integrated foyer and gallery views.
4. Registrar and Original Witness records already exist (`not-started`). The Original stays a screened partition only: nothing establishing what it is.

## 7. Implementation batches

| Batch | Scope | Needs | Status |
|---|---|---|---|
| **1** | Ch1 `orientation_refusal` → dialogue; 5 mis-typed cards → action | Nothing | **Done** on `agent/presentation-audit-ch01-20261117` (6dc6dee), not merged |
| **2** | Ch1 spoken wording for the 5 cards; beats at `drone_intercepts`, `portrait_before_album` | Story Director wording; no art | Proposed |
| **3** | Ch1 House dialogue: `foyer_attempt`, `dinner_redirect` (views exist); `comfort_offer`, `refused_both`, `refreshments`, `dinner_arrival` (need views) | Owner decision; 2 House views | Proposed |
| **4** | Ch3 dialogue conversion + 5 beats (`human`, `satisfy`, `grand_0`, `registry`, `disposition` if allowed) + remove invalid `speaker` fields + Focus A decisions | Story Director's pending prose; Attendant (and Pruitt) portrait | Plan only |
| — | Chapter 2 | — | No change |

**Game integration** (after the owner merges a batch to public main): `sync.js pull --rev <sha>` in the game, `import.js`, then QA. Batch 1 was proven in a throwaway game worktree at `a15b240`, comparing the public head `066ea36` with the branch commit `6dc6dee`. Both runs had identical results:

| Check | Base 066ea36 | Branch 6dc6dee |
|---|---|---|
| `import.js` (preview) | OK | OK |
| `validate_ch01_art` | 253/253 | 253/253 |
| `validate_story` | 178/178 | 178/178 |
| `validate_ch02_routes` | 157/157 | 157/157 |
| `validate_story_import` | 92/92 | 92/92 |
| `run_ch01_routes_qa` (Chromium + Firefox) | — | **154/154** |
| `validate_death_controls` | 44/45 | 44/45 |

The single `validate_death_controls` failure is its pinned content-hash check (`407d8ec78f1c`). It fails on any canon change, the base included, and needs a deliberate fixture update when the game next pulls.
