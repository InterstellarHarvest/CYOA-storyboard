# Chapter 4 gameplay integration branch (game issue #27)

**Branch:** `integration/ch04-gameplay-20261126`, from `main` `7618d81` (the Temporary Staff Pass grant, PR #45). Draft only; do not merge until Nate approves the game review. Precedent: the Chapter 3 integration branch (PR #19). The game (`InterstellarHarvest/out-of-order`, branch `agent/ch04-gameplay-form27b6-integration`, game docs/107) pins this branch's head.

## Changes

- **Chapter 3 → 4 hand-off** (docs/126 §6.1, docs/152 addendum).
  - Each of the seven surviving endings' single BEGIN AGAIN card becomes `continue_to_chapter_04_<ending>`: kind continue, `effects.set.ch3_exit_route = <ending>`, `chapter: chapter-04`.
  - Text and node fields are unchanged.
  - Chapter 3 blob: `d0591d6` → `36a72dc`.
- **Chapter 4** (docs/152 §7):
  - `development.notForGameplay` false; manifest status `draft`;
  - the three park exits get the standard BEGIN AGAIN card until Chapter 5 exists;
  - `ch4_careful_ring_retrieval` `certain: true` (odds unchanged);
  - **Nate ruling 2026-11-26:** `hotel_seashell_first_attempt` gains `shell_first_leave` "PUT THE SEASHELLS DOWN AND LEAVE." → `hotel_bridal_lavatory_park_exit`. This fixes a reachable dead end the game's route validator found: room → complain → ask → second attempt → appeal → `appeal_other` → room → try.
- **Four docs/137 C3 reuse keys** registered `reused` through `register-art.mjs` (no new art; selections 216 → 220 preview copies):
  - `wedding_entry` and `refreshment_table` → CH4-05;
  - `bridal_corridor` → CH4-B2-19;
  - `freight_lift` → CH4-NEW-03.
- **Death export:**
  - `subtitle` is optional, because the four approved Chapter 4 popups have none. An absent subtitle is omitted; an empty one is refused.
  - Regenerated: the six earlier entries are byte-identical, and the four Chapter 4 entries are added (`readyForGameplay`, art pending game binding).
- **check-canon:** `notForGameplay` must be present and boolean.
- **QA:** pins for the intended changes in qa-smoke, qa-sync, qa-ch3-reboot-candidate, qa-browser and qa-timeline.

## Verification (local)

| Suite | Result |
|---|---|
| check-canon, qa-sync (23), qa-smoke, export --check, qa-static, qa-ch3-reboot-candidate, qa-ch3-integration-state, qa-ch3-reference-supersession | pass |
| qa-browser | 26/26 |
| qa-timeline | 136/136 |
| qa-artwork-preview | 64/64 |
| art-lab Pages site | 70/70 |
| art-lab browser | 106/106 |

`qa-ch3-artwork-briefs` fails on untouched `7618d81` too (pre-existing; not in CI).

## Not changed

Narration, choices other than those above, conditions, items, story ids, approved images, references, Chapter 5, PR #32.
