# CH3 Storyboard Integration / Art Production / Fatal Popup — Review Handoff

**Status:** PRIVATE DRAFT REVIEW ONLY. 2026-11-16. Chapter 3 is registered as the fourth chapter in the existing storyboard. No live deployment, art generation or owner signoff is implied.

## Actual source files

- `story/storyboard-manifest.json`: Chapter 3 added after Chapter 2, same shared catalog.
- `story/chapters/chapter-03.draft.json`: **62 connected storyboard nodes**, **71 logical action cards** (73 raw cards; two sets of mutually exclusive conditional variants each display as one choice), **28 branching decision locations**, **3 fatal terminals** (one approved, two provisional).
- `story/chapters/chapter-02.draft.json`: storyboard-only next-chapter markers on the five living endings. The existing runtime `end:true` and `BEGIN AGAIN` were **not changed**.
- `story/items.draft.json`: 16 new Pavilion document/object entries, all connected to a shared item-art registry. Existing inventory IDs for timing clicker, red stapler, rubber-band ball, two prior badges and family photograph remain unchanged.
- `story/artwork.draft.json`: 67 new Chapter 3 art records in the shared catalog: **21 scene backgrounds**, **2 564×278 paired portrait backgrounds**, **2 transparent portrait poses**, **7 Focus A close-ups**, **32 item illustrations** for 16 items, **3 death-screen illustrations**.
- `story/storyboard-layout.json`: Chapter 3 gets independent canvas positions; the other chapters' saved layouts are preserved.
- `tools/storyboard/index.html`: adds death-popup preview with art placeholder and editable source ref; check pass/fail links; Chapter 2 ending preview links; one logical badge card even where importer requires two conditional source variants; artwork editing includes deathScreens.
- `tools/story-import/convert.js`: explicitly distinguishes and strips new storyboard-only fields before game content output, preserving key order for existing runtime choices.
- `tools/storyboard/qa-smoke.mjs`, `qa-browser.js`: assertions updated for four chapters, 165 shared artwork metadata records, 132 with not-started status, Chapter 3 links, and death-screen requirements.

The storyboard's Chapter 3 prose uses short collaborative draft text where approved, and brief **clearly marked** structural placeholders where writing is awaiting owner involvement. Do not promote the structural placeholders as canon.

## Owner-ratified Chapter 3 incidents

**Route B — Visitor Records:** Completed Visit options A dispute the false departure, B request supposedly authorized exit, C investigate record source. At Anticipated Conduct, all three methods retained: A alter predicted assistance, B deliberately behave unpredictably, C trace the plan to its source. At Predicted Departure, all three retained: A insist the official permit be honored, B make gate account for two registrations, C manipulate the six-second departure counting wheel.

**Route B, choice C check:** hidden d6 need >=4; one point bonus from held timing_clicker **or** red_stapler **or** rubber_band_ball; nonstacking; no consumption on success or failure; failure is nonfatal. NOTE: the legacy JSON records base check and exact owner rule in choice notes. Runtime OR-bonus handling still needs Gameplay PMO to implement without stacking.

**Route C — Control Room:** A inspection authority is **mandatory-gated** by either held expo_examiner_badge or acting_director_badge. No badge -> the logical A option should be visible but disabled with reason; B preserve unscripted movement report, C follow cables, both unrestricted. The storyboard has two mutually exclusive source choices for A to express OR under the old condition schema and visually groups them into one; an actual disabled-card renderer must be approved/integrated by Gameplay PMO. No badge consumed.

**Route C — Human Behavior Workshop:** deliberately funny, brightly lit human demonstrations, not a solemn robotic laboratory: SPONTANEOUS LAUGHTER, GENUINE SURPRISE countdown, FREE WILL with I AGREE / I AGREE ENTHUSIASTICALLY. Owner kept all three choices: A participate in Free Will; B request Replacement Original; C sabotage the behaviors. **A and C outcomes are NOT approved yet**; draft placeholders keep graph connected. Owner explicitly approved **B as unavoidable death**: the user misunderstands the replacement request as receiving a model; Pavilion registers them as volunteering to become the replacement. They are sealed in an airtight exhibit coating, cannot breathe, **suffocate and die**, body remains on pedestal, no die or item escape. Must visibly warn about *permanent display* before committing; never show protagonist's face.

**Ending:** A MODEL CITIZEN. Popup preview currently has title, subtitle, fatal text and an illustrated-art placeholder. No final pixel art exists. Popup displays a storyboard-only, inert visual sample of BEGIN AGAIN; real restart remains the chapter's system choice and actual game UI remains untouched.

**Original Witness:** owner-approved possibility to escape independently via TWO PERSONS DEPART; not automatically companion. Its fundamental nature never established; head/face never shown.

## Unreviewed decisions

- Route A's many legacy administrative/photo branches were imported as **scaffolding** from the earlier compact graph, not jointly revised after the new process ruling. The Fourth Chair source image remains three empty chairs and a crop of player legs/shoes in the fourth.
- Route C Free Will and sabotage outcomes, and C03 Presentation Feed choices, require co-writing.
- Grand Reconciliation and voluntary identity-erasure safe fallback require specific owner rulings; no presumed consent.
- SUCCESSFULLY RECONCILED and PERMANENTLY ARCHIVED are older **provisional** fatal placeholders; A MODEL CITIZEN is the only newly owner-approved fatal.
- Artwork prompts are available for every scene and item; actual image generation, visual QA, owner approval, and integration have **not** occurred.

## Art production instructions (Codex or dedicated Art PMO)

Preserve previously approved M2 reception source, UI shell, Chapter 1 and Chapter 2 assets unchanged. Source of truth is the expanded shared `story/artwork.draft.json`; generate only Pavilion assets, in manageable owner-reviewed batches:

1. **Foundation:** Pavilion arrival, attendance, Human Requirements, Visitor Records, Anticipated Conduct and Departure Gate; scene target exactly 314×206.
2. **Chapter 3 collaborative focus:** Control Room, Human Behavior Workshop, replacement pedestal, Free Will controls, replacement request close-up, death vignette. Confirm humor, legibility and shared palette before other art.
3. **Later unapproved Route A and finale scenes:** image archive, Fourth Chair, Original Witness, Grand Reconciliation, surplus/technical rooms — wait for collaborative narrative decisions before committing production compositions.
4. **Items:** author exact 96×96 transparent RGBA icons and separate 565×451 inspection art from the same object design, for all 16 Pavilion items; don't scale one into the other.
5. **Portraits:** opaque 564×278 tighter location backgrounds and separate 564×278 transparent foregrounds for the screened Witness and machine Registrar; no protagonist or Original face.

**Death popup treatment:** Reuse established 16:9 interface shell aesthetic, no new arbitrary game frame. The death illustration is a separately authored 565×451 vignette within a review-only popup design; title, subtitle and BEGIN AGAIN remain live UI typography (do not bake into pixel art). The active fatal illustration is approved only in story mechanism, **not** in artistic rendering. Never depict a breathing or conscious body after death, and no face/gore. Compare new popup to existing UI before Game PMO integrates it.

**File status**: all 67 new art records have `status=not-started` and null `assetPath`. Prompts are ready for creative review; none is marked generated, approved or integrated. Proposed filenames are not actual generated files. Do not claim pictures are finished.

## Verification already performed

- Programmatic JS route walk on new Chapter 3: 62/62 nodes reachable, zero missing choice destinations, no cycles, all reference scene/focus/death art IDs resolve, all 16 new item IDs exist; 71 logical action choices and 28 branching decision points.
- All five nonfatal Chapter 2 terminal nodes have storyboard-only next-chapter pointers. Existing Chapter 1->2 navigation remains unchanged.
- Ran pure `tools/story-import/convert.js` preview conversion against the actual committed four chapter sources: **ok, 0 conversion errors** (unproduced art and draft statuses are expected warnings).
- Compared converter output of original Chapter 1 and Chapter 2 to their pre-Chapter-3 branch: their entire generated runtime chapter objects are **byte-for-byte JSON identical** after excluding source-only metadata.
- Storyboard JavaScript parsed successfully. Browser/Node smoke suite and GitHub Actions checks may still be pending; do not claim them green without their results.

## Next creative step

Return to workshop Choice A — Free Will demonstration; owner selects the precise absurd event and outcome before marking it approved. Then C sabotage, C03, Route A branches, and Grand Reconciliation. Keep actual route length comparable to Chapter 2 and preserve new decisions directly in the storyboard files as they are ratified.

No merge, production push, game deployment or art signoff from this documentation-only handoff.
