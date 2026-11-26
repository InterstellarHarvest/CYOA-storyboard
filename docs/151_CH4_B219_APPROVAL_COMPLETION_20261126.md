# Chapter 4 B2-19 — lobby and Lot 61 conditional state references v01

**Owner approval:** On 2026-11-26, Nate approved **all three B2-19 v01 images**.
- They are **APPROVED / PRESERVED** conditional-production references derived from the selected CH4-01 lobby master. They are not new primary scenes or selections.
- This registration follows the B2-18 precedent (docs/150).
- No pixels were generated, modified, downscaled, re-encoded or regenerated.

**Approved review source:**
- Branch `art/ch4-b219-lobby-states-review-20261126`, review head [`7c85a4150655d1988866dafd7278d2a4a0aba0f3`](https://github.com/InterstellarHarvest/CYOA-storyboard/commit/7c85a4150655d1988866dafd7278d2a4a0aba0f3).
- All three natives were introduced in `801dbd9` at `tools/prologue-art-lab/assets/review/chapter-04-b219-lobby-states-2026-11-26/v01/native/`. They are byte-identical at the pinned gallery commit `6305bd7` and at `7c85a41`.
- They match the v01 manifest, the hashes published in `PUBLICATION.md`, the review's public byte receipt, and the public raw files at both commits.
- `v01/RECONCILIATION.md` is the authoritative state mapping.

## Approved / preserved references

All three are 314×206 opaque RGB, stored in `tools/prologue-art-lab/assets/approved/conditional-production-references/chapter-04/b2-19/`.

| Reference | Shows | When it applies | SHA-256 |
|---|---|---|---|
| `lobby-doors-removed.png` | the lobby with both restroom door leaves removed; stone-framed openings and central pier kept | **Doors remain absent after the sale:** once the workmen in `hotel_auctioneer_arrival` have removed them, and on every later lobby visit. The removal itself (the first door carried away, continuing as you enter `hotel_restroom_entry`) is narrated, not pictured. | `e2aa3835dca0edf1e76b93df2a3cf628db8dc5ff8f56c1f5df8e6188ea7d218e` |
| `lot61-open.png` | doors absent; the Lot 61 convenience pod open, with its toilet visible | **The pod appears during the demonstration:** `hotel_lot61_pod_auction`, after it is wheeled out and its door opens. It also covers `hotel_lot61_pod_declined` while the pod departs, after which the doorless lobby returns. | `3913c8ad89c0245c31827f1933926ff0d1a00ec9da71f34dfa9818ff222c42b5` |
| `lot61-packed.png` | doors absent; an ordinary briefcase-size empty aluminium case where the pod stood. No shoe, no bulge | **Only on the successful escape route** (`hotel_lot61_pod_escaped`), and **only after the authored folding finishes.** The node sets `ch4_pod_survived_packing` on entry, before the folding text, so that flag alone must not reveal the case. | `f3c27be75a18007850f8eb9bff7ae71f031063aa44735f9bfbd24bf5d876b558` |

**Unsuccessful folding:**
- `fatal_lot61_folded` keeps the approved `deathScreens:grand_bellevue/folded_for_convenience` illustration (`30490a4259b363879dc126e273dcc07bb979d96ad4f6534dd75cb7e3901ddc07`), unchanged, including its fatal-only shoe and slight bulge.
- The successful-escape case never borrows them.

**What these references do not create:**
- No artwork key, Focus ID, flag, mode or runtime binding.
- No `artwork-preview.json` entry; canonical selections stay at 214.

**Masters preserved:**
- The selected CH4-01 lobby master (`scenes:grand_bellevue/lobby`, `582bcd51de937e5fe124160a8beb74b4ee469f52eeb6d9d0d38b918cfb0d6be0`) stays selected and remains the default.
- Its record gains only an appended, dated note with the three references, hashes and the timing above. The earlier note text is kept verbatim; status, prompt and paths are untouched.

## B2-18 post-lift background decision

The B2-18 review (docs/150) had held a post-lift closer background for `hotel_stall_porter_protest`.

**Decision (Nate / PMO, 2026-11-26):** reuse the approved CH4-B2-03 restroom conversation background **unchanged** for that node.
- Key `scenes:grand_bellevue/restroom#portraitBackground`, SHA-256 `77325aca0d3c61d5b6d1980232fb11fa55156454a26659c6887c4d726a82c377`.
- The B2-19 porter assessment found the far-right stall edge visible but peripheral, and it does not occlude the porter.
- No replacement background is produced or needed.

**Where it is recorded:**
- An appended, dated note on that record.
- This document, which supersedes the "held" status in docs/150. docs/150 itself is unchanged as the historical record.

## Gameplay handoff (not performed here)

When Gameplay PMO integrates Chapter 4 lobby states:
- Show the doorless lobby after the sale and on every later lobby visit.
- Show the open pod during the demonstration and the decline departure.
- Show the empty case only after the folding finishes on the escape route.
- Keep FOLDED FOR CONVENIENCE for the fatal outcome.
- Use CH4-B2-03 for the porter protest.
- Use authored text beats for timing; never use node-entry flags alone.
- The auctioneer's approved closer background needs no state variant.

No conditional dispatch is introduced here. The engine items in docs/140 remain open. No narrative, gameplay, engine behavior, game integration, deployment, approved artwork or draft PR #32 is changed.

## Workflow and verification

1. Confirmed that no other agent was performing this registration. The Codex review producer finished at 14:38, and no B2-19 registration branch or PR existed. Worked in a new dedicated worktree, `_worktrees/CYOA-ch4-b219-registration-20261126`.
2. Read the three PNGs from the review head and verified them against the manifest, `PUBLICATION.md`, the public receipt, the public raw bytes and the review history. Copied them byte-for-byte.
3. Appended the dated notes to the lobby record and the restroom conversation-background record.
4. `node tools/sync/check-canon.mjs` reports OK: 293 art records (79 approved, 140 integrated, 69 not-started, 5 reused) and 214 previewed, all unchanged.
5. Every CI step passes locally:
   - `qa-sync`, both Chapter 3 suites, `qa-smoke`, the death-export check and `qa-static`;
   - storyboard `qa-browser` 26/26, `qa-timeline` 136/136 and `qa-artwork-preview` 64/64;
   - art-lab `qa-pages-site` 70/70 and `qa-browser` 106/106.
6. `python3 tools/sync/verify-ch4-b219-approval.py` passes against canonical base `3785e87506c4218a360cf7a309b2fbe690cc4546`, which includes B2-18. Report: `docs/151_CH4_B219_VERIFICATION_20261126.json`. The checks cover:
   - exact bytes and formats;
   - manifest, publication and public-receipt agreement, and identity at all three review commits;
   - no bindings;
   - the approved tree gains exactly three files, with every earlier reference unchanged, including B2-18;
   - the review package kept on its branch;
   - no new selection, with all 214 selected images unchanged in bytes, including the lobby master, CH4-B2-03 and FOLDED FOR CONVENIENCE;
   - registry changes limited to the two appended notes;
   - the canonical timing facts (the flag set on entry, the fatal art reference, the porter scene);
   - every story file, the QA tools and docs/150 unchanged;
   - only approval files changed;
   - an unchanged PR #32 head.
