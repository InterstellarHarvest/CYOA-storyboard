# Chapter 3 — Temporary Staff Pass grant (owner-approved addition)

**Owner approval (Nate, 2026-11-26):** grant the existing item `pavilion_temporary_staff_pass` during the People's Pavilion temporary-presenter appointment. This resolves docs/152 §8 D-1 with option (a).

**Status: APPROVED AND REGISTERED (storyboard PR #45).**
- **Approved by Nate on 2026-11-26** (recorded in the PR #45 comments):
  - the grant;
  - the printer run, exactly as written;
  - the item description, exactly as written;
  - both v01 item images, unchanged.
- **Registered:** both images, as approved selections (§4).
- **Game integration** is separate: game issue #27 (§6).

## 1. The change

**Authoritative source:**
- `story/chapters/chapter-03.reboot-candidate.json`, the file the manifest activates and the game consumes (game `story/canon.lock.json` lists `chapter-03` from it).
- The obsolete pre-reboot `chapter-03.draft.json` and `story/archives/chapter-03-pre-reboot-20261118.json` are untouched. Their byte locks still pass.

**Node `unauthorized_presenter`** (dialogue, presenter, `alarmed`):
- **Grant on arrival:** `"effects": {"give": ["pavilion_temporary_staff_pass"]}`.
  - The engine applies an arrival `give` with the node, so the pass is held before either card can be chosen.
  - It is the only `effects` in the reboot chapter.
- **Text:** the final run is split exactly after the announcement, and one run is inserted there:

| # | Run |
|---|---|
| 1–4 | unchanged |
| 5 | A second microphone drops before you. TEMPORARY PRESENTER APPOINTED. *(first half of the original run 5)* |
| **6** | **An administrative printer rattles and ejects a card: TEMPORARY STAFF. PEOPLE'S PAVILION. DEPARTMENT: HUMAN PRESENTATION. VALID UNTIL CORRECTED. You pocket it. Apparently, you have been hired again.** |
| 7 | A green BEGIN DEMONSTRATION button lights up beside a covered emergency release. *(second half of the original run 5)* |

**Unchanged:** both choices, `start_presenter_demonstration` → `genuine_surprise` and `free_real_presenter` → `presenter_help_end`. So are every other node, choice, check, flag and ending in Chapter 3, and all of Chapter 4, including both SHOW TEMPORARY STAFF PASS cards and the five downstream nodes. No authored rule takes the pass, so it stays in inventory.

## 2. Item record (`story/items.draft.json`)

**Kept:**
- the existing id;
- the name TEMPORARY STAFF PASS;
- `slotArt`/`inspectArt` `null`, until integration sets them through the registry;
- the READ mark.

No duplicate item is created.

**Description — approved by Nate exactly as written (2026-11-26).** The pre-reboot text "Provisional status authorizing one service inspection." contradicted the printed card and Chapter 4's two uses. It now uses only the approved card wording:

> A PRINTED CARD FROM THE PEOPLE'S PAVILION: TEMPORARY STAFF. DEPARTMENT: HUMAN PRESENTATION. VALID UNTIL CORRECTED.

## 3. Art records restored (`story/artwork.draft.json`)

`items.pavilion_temporary_staff_pass.slot` and `.inspect` were marked ARCHIVED / RETIRED pre-reboot prompts. They are now **active briefs, status `not-started`**:
- the same 96×96 transparent / 565×451 opaque contract;
- the same suggested paths (`art/items/pavilion/pavilion_temporary_staff_pass_{slot,inspect}.png`);
- prompts rewritten for the approved card. The inspect view carries exactly TEMPORARY STAFF / PEOPLE'S PAVILION / DEPARTMENT: HUMAN PRESENTATION / VALID UNTIL CORRECTED, with no name, photo, serial, date, signature or seal. The slot shows the same card with no legible text.
- The archived note follows the new note verbatim, as history.

No other record changes.

## 4. Artwork: approved and registered

Two images are an explicitly approved cross-chapter addition, outside the Chapter 4 set of 63. Both are **APPROVED / SELECTED, v01, unchanged**.

**Source:**
- branch `art/pavilion-temporary-staff-pass-review-20261126`;
- introduced in `a6a6bdb`, and byte-identical at the approved review head `ae35351`;
- path `tools/prologue-art-lab/assets/review/pavilion-temporary-staff-pass-2026-11-26/v01/native/`.

| Key | Selected PNG | Format | SHA-256 |
|---|---|---|---|
| `items:pavilion_temporary_staff_pass#slot` | `assets/selected/pending-integration/items/pavilion_temporary_staff_pass/slot.png` | 96×96 RGBA, binary alpha | `662ecb2c15b0b70afd5e6a14a73dadab6090fc2f4c75a389f9f5a96ba06b59b5` |
| `items:pavilion_temporary_staff_pass#inspect` | `assets/selected/pending-integration/items/pavilion_temporary_staff_pass/inspect.png` | 565×451 RGB | `527e17af4a27971d2d729441f8a74d097c5442df93f0161dc841d81ee1788e41` |

**How they were registered:**
- `register-art.mjs` (dry run, then real) copied the exact bytes, wrote the provenance to `story/artwork-preview.json` and raised both existing records from `not-started` to `approved`.
- Each record's notes now begin with the owner approval, the source commit, the review head and the SHA-256. The importer reads that SHA-256 as the approved selection. The restored brief and the archived pre-reboot note follow verbatim.
- `assetPath` stays `null` until the game integration.
- The review package stays on its branch.
- **Selections: 214 → 216.** `check-canon` reports 293 records (81 approved, 140 integrated, 67 not-started, 5 reused) and 216 previewed.

## 5. Route tests

### Storyboard: `tools/sync/verify-ch3-staff-pass-grant.py` (PASS, 41 checks)

**Scope and preservation:**
- the registration adds exactly the two PNGs; all 214 earlier preview entries and bytes are unchanged, and no reference file changed;
- only the files listed in §7 differ from `89cf0ad`;
- the split run rejoins to the original byte for byte;
- the other 33 Chapter 3 nodes, Chapter 2, Chapter 4, the manifest, layout, sync contract, death export and all images are unchanged.

**Grant scope:** the pass is given only at `chapter-03:unauthorized_presenter` and taken nowhere.

**State-tracking search** (flags, items, both outcomes of every check), from all 5 Chapter 2 hand-offs, with both an empty inventory and every earlier item:
- **All 7 Chapter 3 endings:** the pass is held **if and only if** the route went through the appointment.
  - `presenter_help_end` always holds it.
  - `backstage_exit` holds it only via the demonstration.
  - The other five endings never do.
- **Into Chapter 4** with `ch3_exit_route` set to the ending:
  - From both `presenter_help_end` and `backstage_exit`, holding the pass makes all five gated nodes reachable through the unchanged SHOW cards: `hotel_collection_staff_pass`, `_first`, `_recognized` and `_authorized`, plus `hotel_boiler_staff_access`.
  - Without the pass, they stay unreachable from every ending.

### Game engine (game `main` `c7a2d3d`, local and read-only, nothing pushed)

`sync.js pull --from-git` of the review commit, then `import.js`, then the 32 seeded routes of `game/qa/ch03_routes.js`, played by the real engine:

| | Control: storyboard `main` `89cf0ad` | With the grant |
|---|---|---|
| Projection | accepted | accepted. `effects` is a runtime field, and the item now enters the game's `items.draft.json`. |
| Routes gaining the pass | 0 of 32 | **exactly 4 of 32**: `presenter_begin` → `backstage_exit`, `presenter_release` → `presenter_help_end`, and their key variants. Endings unchanged; nothing else differs. |
| Import | production profile, 3 allowed warnings | **fixture profile (DEV PLACEHOLDERS)**, from the 2 missing item images |

**Game content QA** (15 CI content steps). Game `main` itself passes all 15.

| Suite | Control (re-pin to `89cf0ad`) | Grant (re-pin to `ffc5f2e`) | Reason |
|---|---|---|---|
| `qa-sync.js` | **fails** | fails | **Pre-existing, unrelated to the grant.** Its Chapter 4 fixture check assumes the four Chapter 4 death-screen records don't exist; B2-16 (docs/148) registered them. Any re-pin past B2-16 must update it. |
| `validate_story_import.js` | 107/107 | 106/107 | the no-missing-art gate: the 2 item images |
| `validate_ch03.js` | 453/453 | 445/453 | 8 expected pins: narrative blob `857ffdf`; production profile (item art); "no new item exists"; "no legacy Chapter 3 item" (the id predates the reboot); "nothing gained" on exactly the 4 appointment routes |
| `validate_death_controls.js` | 45/45 | 44/45 | pinned content hash `8045c71dcbf1` (now `9304cce5d4e9`) |
| other 11 | pass | pass | — |

Every grant-only failure is either the missing item art or a pin that this approved change is meant to move. Section 6 lists the updates.

**Chapter 4 cannot be played in the engine yet** (WP-1–3, and the exit hand-off in the docs/152 addendum). Chapter 4 reachability is therefore proved at the storyboard level above.

## 6. Proposed coordinated integration

The game pins a storyboard SHA (`story/canon.lock.json`, docs/97), so storyboard `main` can move without changing the game. The order avoids any placeholder build:

1. ~~Nate reviews this branch~~ — **done**: the narration and the description are approved.
2. ~~Artwork~~ — **done**: v01 was approved unchanged.
3. ~~Storyboard~~ — **done**: both images are registered on this branch, and PR #45 merges the grant and its approved art as one `main` revision.
4. **Game (Gameplay PMO, isolated branch; tracked in game issue #27; not merged or deployed without Nate's separate approval):**
   1. copy the two approved PNGs to their suggested paths, bound through `runtime-settings.pendingArtBindings` (docs/104 §3);
   2. `sync.js pull --rev <that main SHA>`;
   3. `import.js` — it must stay on the **production profile**;
   4. update the game QA pins:
      - `validate_ch03.js`: the narrative blob `857ffdf` → `d0591d6`; "no `pavilion_*` item" and "no legacy Chapter 3 item" → exactly this item, with bound art; "nothing gained" → the four appointment routes gain exactly this pass;
      - `validate_death_controls.js`: the content hash;
      - `qa-sync.js`: the Chapter 4 death-art fixture premise, which is needed for any re-pin;
   5. run the full content and browser QA, merge, then `sync.js publish` so the records become `integrated`.
5. **Chapter 4** stays `notForGameplay`. Its routes become playable only with the Chapter 4 integration in docs/152, including the `ch3_exit_route` hand-off.

## 7. Files changed (storyboard)

| File | Change |
|---|---|
| `story/chapters/chapter-03.reboot-candidate.json` | the node edit in §1 (text edit, formatting preserved) |
| `story/items.draft.json` | the description in §2 |
| `story/artwork.draft.json` | the two restored briefs in §3, then approved with approval notes (§4) |
| `story/artwork-preview.json`, `assets/selected/pending-integration/items/pavilion_temporary_staff_pass/{slot,inspect}.png` | the two registered selections (§4) |
| `tools/storyboard/qa-smoke.mjs`, `tools/storyboard/qa-ch3-reboot-candidate.mjs` | the Chapter 3 narrative lock moves from `857ffdf` to `d0591d6`; the "no effects" invariant allows exactly this grant |
| `tools/sync/verify-ch3-staff-pass-grant.py`, `docs/153_*` | this record and its verifier |
| `docs/152_…HANDOFF…md` | dated addendum: D-1 decided, plus the omitted Chapter 3 → 4 exit hand-off |

**Storyboard QA:** `check-canon`, `qa-smoke`, `qa-sync`, both Chapter 3 suites, `qa-ch3-reboot-candidate`, the death export check and `qa-static` all pass. Browser QA: `qa-browser` 26/26, `qa-timeline` 136/136, `qa-artwork-preview` 64/64, art-lab `qa-pages-site` 70/70 and `qa-browser` 106/106.

**Not touched:** earlier approved PNGs, selections and references, Chapter 4, the game repository, deployment and draft PR #32.
