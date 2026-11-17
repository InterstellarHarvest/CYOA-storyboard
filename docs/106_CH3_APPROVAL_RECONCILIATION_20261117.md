# CH3 — Approval reconciliation through 2026-11-17

**Status:** storyboard data synchronized to the owner-approved decisions supplied by the Gameplay PMO on 2026-11-17 (the "Synchronize Chapter 3 Before Auditing" addendum). The game does not consume Chapter 3 (`tools/story-sync/config.json` lists Prologue, Ch1, Ch2 only), so nothing here changes a game build.
**Base:** public `main` 7c7a50a. **Archive of everything removed:** [106_CH3_RETIRED_ROUTES_ARCHIVE_20261117.json](106_CH3_RETIRED_ROUTES_ARCHIVE_20261117.json) (full JSON of retired nodes and choices, plus every replaced field's old and new values).

Narrative approval and artwork status are separate. Nothing here generates, selects or re-approves art, and no approved/integrated art record was touched.

## Rules followed

- The supplied decisions are the authority. Docs 94–99 and 96 are pre-approval proposals; their extra flags, items and third options were **not** imported.
- Where only a decision (not exact prose) was supplied, the node's `text` is a short **decision summary** and its `notes` say `Exact scene prose PENDING EDITORIAL SYNCHRONIZATION`. Nothing is marked as approved prose that was not supplied as prose.
- Rejected options are removed from the active graph. Nodes left with no incoming route are retired. Both are preserved in the archive JSON and named in the parent node's notes as retired, never as active routes.
- No check odds, branch destinations, flags or item effects were changed except as listed below. Proposed tool bonuses that the owner has not approved are recorded as *not approved — do not wire*; none was ever wired.

## Reconciliation matrix

| Encounter (node) | Repository before | Approved state | Change made |
|---|---|---|---|
| Human Requirements (`human`) | Owner-approved, 3 routes | All three routes | None (already current) |
| Satisfaction Demonstration (`satisfy`) | Owner-approved A + C; B retired | A certificate (retained item); C curtain d6≥4, pass backstage, fail nonfatal correction; refusal not active | Notes: item now registered. Graph unchanged |
| `pavilion_satisfaction_certificate` item | Awarded by `satisfy_0` but **missing from items.draft.json** | Register; art pending | Added item record + 2 `not-started` art requirements (slot 96×96, inspect 565×451) |
| Satisfaction Records (`records`) | Unreviewed scaffold, 3 choices | A correction → Reconciliation; B preprinted future record → Tomorrow's Complaint → Anticipated Conduct; C provisional staff authorization → Presentation Control | Approved notes; B/C card wording aligned (*EXAMINE THE PREPRINTED FUTURE RECORD*, *OBTAIN PROVISIONAL STAFF AUTHORIZATION*); destinations unchanged |
| Reconciliation Office (`reconcile`) | Scaffold, 3 choices | A request Original; C duplicate-person classification → Surplus | **Retired** `reconcile_1` (living-body proof) and node `a_life`; C wording *ACCEPT DUPLICATE-PERSON CLASSIFICATION* |
| Original Witness (`witness`) | Scaffold, 3 choices; flag set only by a later player choice in `a_witstd` | Original speaks off-script; recorder logs it automatically; sets `ch3_original_independent_response_seen`; player has B (partition d6≥4) and C (photographic records) | **Scene-entry effect** sets the flag; **retired** `witness_0` + node `a_witstd`; C wording *DEMAND THE PHOTOGRAPHIC RECORDS*; Original's nature stays unstated |
| Technical Adjustments (`a_techadj`) | Scaffold, 2 choices | A fitting-order number → hearing records; B moving platform → Workshop | Approved notes only (already matched) |
| Image Standards Archive (`image`) | Scaffold, 4 cards (A + two B variants + C) | B challenge approved image with source evidence (photo held → Fourth Chair; not held → Empty Claimant Photograph); C processor d6≥4, pass Image Production, fail correction | **Retired** `image_0` + node `a_negative`; both B variants now read *CHALLENGE THE APPROVED IMAGE WITH SOURCE EVIDENCE.* (one logical card, `displayGroup` unchanged); fixed the B variants' wrong note ("if held: a_empty") |
| Empty Claimant Photograph (`a_empty`) | Scaffold, 2 choices | Only A: preserve photo, grant `pavilion_empty_claimant_photo`, admin route | **Retired** `a_empty_1`; existing entry effect (gives photo) kept |
| Image Production (`a_exposure`) | Scaffold, 2 choices | A authenticate → hearing records; B service cable → Presentation Feed; partial figure, no face | Approved notes only |
| Fourth Chair (`a_fourth`) | Scaffold, 3 choices | A source conflict + custody hold; C fitting machinery d6≥4 **with visible fatal warning before selection**, fail → Live Source Calibration; photo returned | **Retired** `a_fourth_1` + node `a_household`; C card now *INTERRUPT THE ORIGINAL FITTING MACHINERY — FATAL RISK.* (same suffix convention as `disposition_1`); photo still not consumed |
| Witness Custody (`a_custody`) | Scaffold, 2 choices | Both approved | Approved notes only |
| Live Source Calibration (`a_calibration`) | Scaffold: safe refusal + risky release | **Only B.** No safe refusal. Release d6≥4: pass technical passage; fail fatal | **Retired** `a_calibration_0`; card *ATTEMPT THE EMERGENCY RELEASE — FATAL RISK.*; check/destinations unchanged |
| SUCCESSFULLY RECONCILED (`end_reconciled`) | Popup `proposed`, placeholder subtitle/description | Title SUCCESSFULLY RECONCILED; subtitle NO FURTHER ADJUSTMENTS REQUIRED; description *For the first time, the official photograph and the person in it agree. Neither contains you.*; counterweight mechanism; no face/gore; art = approved brief only | Popup `owner-approved` with exact copy; scene `reconciliation_office` → `technical_services` (where calibration happens); death-screen brief rewritten to the approved mechanism, status stays `not-started`; death export regenerated |
| Surplus Department (`a_surplus`) | Scaffold, 2 choices | Both approved, no surprise death | Approved notes only |
| Working Water / Human Demonstrator / Tomorrow's Complaint / Provisional Employment (`a_plumb`, `a_demo`, `a_origrec`, `a_staff`) | Scaffold one-way transitions | Narrative B short transitions to Presentation Control / Anticipated Conduct / Anticipated Conduct / Presentation Control | Approved notes + decision-summary text; destinations unchanged; no effects added |
| Grand Reconciliation, registry, Original response, Final Disposition, all endings | Owner-approved | Same | **None** — verified matching (odds, nonstacking bonuses, item conditions, Original autonomy, two-choice disposition, PERMANENTLY ARCHIVED) |
| `attend` notes | "Route A and finale remain proposed" | — | Stale sentence superseded (kept quoted in the note) |

**Graph:** 66 → 62 nodes; 6 choices retired; no dangling or unreachable node. Bathroom still unresolved on every ending.

## Approvals that could not be faithfully recovered (owner input)

1. **Exact prose** for 16 nodes is not in the supplied decisions: `records`, `reconcile`, `witness`, `a_techadj`, `image`, `a_empty`, `a_exposure`, `a_fourth`, `a_custody`, `a_calibration`, `end_reconciled` (death narration; popup copy *is* exact), `a_surplus`, `a_plumb`, `a_demo`, `a_origrec`, `a_staff`. Each is marked pending.
2. **Provisional Employment item:** "staff authorization acquired" — should `a_staff` grant the registered (currently unused) `pavilion_temporary_staff_pass`? Not wired.
3. **Records A:** does submitting the satisfaction certificate for correction consume it? Not wired (it is retained everywhere).
4. **Fourth Chair receipt timing:** "awarded according to the approved encounter" — the receipt stays on the existing scene-entry effect. Confirm, or name the choice that awards it.
5. **Card wording** on changed cards is aligned to the approved descriptions but provisional.
6. **Unapproved bonus proposals** on `witness_1`, `image_2`, `a_fourth_2`, `a_calibration_1` are now explicitly *not approved*. The approved OR-type bonuses on `grand_0`, `grand_2`, `original_refusal_0`, `registry_*`, `disposition_1`, `ch3_b03_c` still need runtime wiring (no OR modifier in the engine yet).
7. **Not covered by the decisions, left as unreviewed scaffold:** `a_backstage`, `a_repair` (Fourth Chair C success), `correction`, the three hearing `stage_*` nodes.
8. **Art prompts drafted at sync, not owner-reviewed:** certificate slot/inspect; SUCCESSFULLY RECONCILED aftermath (from the approved brief).
9. **Registered Pavilion items no route awards** (all pre-existing, none caused by this sync): `pavilion_representation_diagnostic_record`, `pavilion_discrepancy_receipt`, `pavilion_temporary_staff_pass`, `pavilion_original_appearance_order`, `pavilion_proof_of_life`, `pavilion_duplicate_routing_tag`, `pavilion_unapproved_exposure`, `pavilion_household_routing_strip`, `pavilion_registration_provenance_strip`. Proof of Life and the Household Routing Strip belonged to now-retired ideas; candidates for retirement.

## Files

- `story/chapters/chapter-03.draft.json` — the reconciliation above.
- `story/items.draft.json` — `pavilion_satisfaction_certificate`.
- `story/artwork.draft.json` — certificate art requirements; SUCCESSFULLY RECONCILED brief.
- `story/death-presentations.export.json` — regenerated (`export-death-presentations.mjs`).
- `tools/storyboard/qa-fixtures/legacy-render-snapshot.json` — Chapter 3 snapshot regenerated for the intentional content change.
- `tools/storyboard/qa-smoke.mjs` — art-record count 169 → 171.
- `tools/storyboard/qa-browser.js` — items 32 → 33, records 169 → 171, not-started 110 → 83 (110 was already stale on 7c7a50a).
- This document and the archive JSON.

## Validation (local, before publication)

`check-canon` OK (226 nodes, 347 routes, 184 art records) · `qa-sync` pass · `qa-smoke` PASS · death export `--check` 9/9 · `qa-static` PASS · `qa-browser` 24/24 · `qa-timeline` 112/112 · `qa-artwork-preview` 48/48 (Chromium + Firefox).
