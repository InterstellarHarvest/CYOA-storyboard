# Chapter 4 B2-18 — restroom conditional state references v01 and upper-salvage continuity fix

**Owner approval:** On 2026-11-26, Nate approved the B2-18 Artwork PMO recommendations.
- **Five v01 restroom state references are APPROVED / PRESERVED.** They are conditional references derived from the approved restroom masters, not new primary scenes.
- **`restroom-braced-main` stays an UNSELECTED alternative.** The contained wet-floor image serves both the braced and the contained outcomes. The narration in `hotel_valve_braced` already explains the temporary seal and dribble.
- **One authorized narrative correction** to `hotel_upper_salvage_arrival`.
- No pixels were modified, downscaled, re-encoded or regenerated.

**Approved review source:**
- Branch `art/ch4-b218-restroom-states-review-20261126`, review head [`109e201bdd99418aae66a73efa29acfafee8be94`](https://github.com/InterstellarHarvest/CYOA-storyboard/commit/109e201bdd99418aae66a73efa29acfafee8be94).
- All six candidates were introduced in `be883d9` at `tools/prologue-art-lab/assets/review/chapter-04-b218-restroom-states-2026-11-26/v01/native/`. They are byte-identical at `760bdac`, `74874c8`, `c6a9dc8` and `109e201`, and they match the v01 review manifest.
- The continuity addendum at the review head (`CONTINUITY-ADDENDUM.md`) is the authoritative node mapping.

## Approved / preserved references

All are opaque RGB and stored in `tools/prologue-art-lab/assets/approved/conditional-production-references/chapter-04/b2-18/`, following the B2-04, B2-07, B2-08, B2-09, B2-11, B2-12 and B2-13 precedent.

| Reference | Size | Derived from (unchanged master) | Nodes / condition | SHA-256 |
|---|---|---|---|---|
| `restroom-active-leak-main.png` | 314×206 | `scenes:grand_bellevue/restroom` (CH4-04 v07) | `hotel_restroom_plumber`, after the burst | `9a6243310bb7af1958854110af742c603275b2ebf9c889050c6c065737e57279` |
| `restroom-active-leak-close.png` | 564×278 | `scenes:grand_bellevue/restroom#portraitBackground` (CH4-B2-03) | the same burst at the closer camera; `hotel_wheel_buyer_lead` while the leak is uncontained | `35a8f8297da89038a0a7b30596363bfa6ad86e3edc6b02bf0efb360a4dc3a46a` |
| `restroom-contained-main.png` | 314×206 | `scenes:grand_bellevue/restroom` | contained: `hotel_wheel_return`, `hotel_key_master_cabinet`. **Also braced:** `hotel_valve_braced` | `674cb60c905347e99c95b99ec87dfacc218cf15483abe89bc4e092d40b43ed1a` |
| `restroom-flood-onset-main.png` | 314×206 | `scenes:grand_bellevue/restroom` | `hotel_valve_flood`, first surge only, before the narrated floating-basket beat | `432ce64f5e7e0420f678774ec8cf2edb02ce745ff532d83b3e1723af9d90fb46` |
| `restroom-stall-lifting-main.png` | 314×206 | `scenes:grand_bellevue/restroom` | `hotel_stall_lot_claimed`, `hotel_stall_crane_success`. The empty enclosure lifts through the hatch on four cables and the toilet stays on the floor | `84976c116d9fc87b6ce8f4cf5d7f316d7185fa308f889df6d1c76eafe6bc525e` |

**Unselected alternative:** `restroom-braced-main.png` (314×206 RGB, `dcbe6ebf8319e3fe0dabe9c30637494e51342303be9923aba29ccd71acca7fcd`). It is preserved unchanged on the review branch only. It is not copied into `main` and not selected.

**Held, not part of this approval:** the review found that a post-lift closer background for `hotel_stall_porter_protest` is needed. The unchanged CH4-B2-03 shows an open stall leaf at the far right, so it is not verified as correct after the lift. The local repair attempt failed its quality gate and was never a candidate. It remains open for a later Artwork PMO decision. Nothing here binds or replaces anything for that node.

**What these references do not create:**
- No artwork key, Focus ID, flag or runtime binding.
- No `artwork-preview.json` entry, so canonical selections stay at 214.
- The selected restroom master and conversation background are unchanged and remain the defaults.

**Registry notes:**
- The two restroom master records (`scenes:grand_bellevue/restroom` and its `portraitBackground`) each gain one appended, dated note line naming their approved references, hashes and the unselected alternative.
- Their earlier note text is kept verbatim. Status, prompt, paths and hashes are untouched.

## Narrative correction: `hotel_upper_salvage_arrival`

The restroom nodes, the FINAL OCCUPANCY fatal node and its approved art all leave the toilet on the restroom floor. The later mezzanine arrival said the toilet travelled inside the suspended stall. Nate authorized this correction:

| Run | Before | After |
|---|---|---|
| text[2] (description) | The toilet is still inside the stall. Its plumbing has been disconnected, and the whole arrangement hangs several feet above the floor. | The stall is only an empty enclosure now. It hangs from the crane cables in the mezzanine, several feet above the floor. The toilet stayed downstairs, still fixed to the restroom floor. |
| text[6] (you) | THE TOILET! | THE STALL! |

**Unchanged in this node:**
- the joke: CAN YOU PUT THAT BACK? / Which part? / … / Plumbing isn't included in the lot. / I JUST WANT TO USE IT! / Not while it's suspended. Insurance.;
- every other run and speaker;
- the three choice IDs, their text and targets;
- the effects (`ch4_upper_salvage_reached`, `ch4_stall_survived_crane`), the scene, speaker, pose and notes.

No other node, route, condition, flag or dice outcome changed anywhere. The approved B2-10 upper-salvage art shows no suspended stall or usable fixture, so the correction conflicts with no approved image.

## Gameplay handoff (not performed here)

**When Gameplay PMO integrates Chapter 4 restroom states:**
- Display these references only through authored conditions that already exist, such as `ch4_restroom_leak` values and `ch4_restroom_water_off`.
- Keep the selected masters as defaults.
- Use `restroom-contained-main` for both the braced and contained outcomes.
- Bring in the corrected arrival text with the next storyboard import.

**Still open:**
- No conditional scene-state dispatch is introduced here.
- The engine work items in docs/140 remain open.
- The held post-lift closer background remains open.

No gameplay, engine behavior, game integration, deployment, approved artwork or draft PR #32 is changed.

## Workflow and verification

1. Read the six candidates from the review head and confirmed them against the manifest and the whole review history.
2. Copied the five approved PNGs byte-for-byte into `b2-18/`. Braced was left on the review branch.
3. Appended the dated reference notes to the two restroom master records.
4. Applied the two-run narrative correction with an exact JSON round-trip; the file's formatting is unchanged.
5. `node tools/sync/check-canon.mjs` reports OK: 293 art records (79 approved, 140 integrated, 69 not-started, 5 reused) and 214 previewed, all unchanged.
6. Every CI step passes locally:
   - `qa-sync`, both Chapter 3 suites, `qa-smoke`, the death-export check and `qa-static`;
   - storyboard `qa-browser` 26/26, `qa-timeline` and `qa-artwork-preview`;
   - art-lab `qa-pages-site` and `qa-browser` 106/106.
7. `python3 tools/sync/verify-ch4-b218-approval.py` passes against canonical base `2af6606c25ce252752c65aa5c68c87ff84f804ae`. Report: `docs/150_CH4_B218_VERIFICATION_20261126.json`. The checks cover:
   - exact bytes, formats, manifest agreement and identity at all five review commits;
   - no binding, Focus ID or flag;
   - braced preserved, not copied and not selected;
   - the approved tree gains exactly five files;
   - no new selection, with all 214 selected images unchanged in bytes;
   - registry changes limited to the two appended notes;
   - exactly the two authorized narrative runs changed, with every other run, choice, effect, node and flag unchanged;
   - only approval files changed;
   - an unchanged PR #32 head.

**Next:** the held post-lift closer background for `hotel_stall_porter_protest`, which awaits an Artwork PMO decision. After that come the remaining B2-18/B2-19 lobby and Lot 61 state families. R1 production remains suspended.
