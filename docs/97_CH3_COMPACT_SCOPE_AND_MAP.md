# Chapter 3 — COMPRESSED SCOPE / CANONICAL STORYBOARD DESIGN

**Status:** Owner-requested scope reduction, story planning only. No playable Chapter 3 JSON or game changes. The new documents supersede the EXCESS *menu count* in earlier docs 94–96; they preserve their story discoveries, item definitions, and exit outcome intent. Any previously discussed voluntary identity surrender and fatal-risk options remain **provisional**, awaiting explicit ruling.

**Reason:** Chapter 2 actual JSON on draft base has **99 nodes, 80 action choices, 27 multi-action branching nodes, 25 checks, 5 surviving and 5 fatal endings**. Its non-repeating surviving route samples involve **5–11 decision hubs**. Earlier Chapter 3 maximal-plan estimate was ~100 choices and ~34 hubs, with substantially wordier scenes. We have trimmed it rather than authoring all suggested three-choice departments.

## Current compact graph measurement

| Measure | Chapter 2 JSON | Chapter 3 compact structural graph |
|---|---:|---:|
| Nodes | 99 | 49 (event nodes may be expanded, not all playable) |
| Action choices | 80 | 71 |
| Multi-action decision hubs | 27 | 28 |
| Checks | 25 | 11 |
| Surviving named endings | 5 | 4 (5 terminal variants incl identity scope) |
| Fatal endings | 5 | 2 proposed |
| Longest graph decision path | 11 on Chapter 2 no-repeat analysis | 13 |

**Scope target:** keep Chapter 3 at approximately **65–85 meaningful action cards, 22–29 branching hubs, 80–100 story nodes at most if authored narration needs splits, and no route more than ~12 decision points, with only the deepest optional paths approaching that length.** This smaller-first graph includes 71 cards, 28 hubs, and is within the budget. Do not fill unused slots with arbitrary paperwork decisions. A shorter graph can contain more narration, so scene prose must be edited for pace against Chapter 2 as well.

## Measured playthrough pacing

The revised graph has **5–12 meaningful decision hubs per modeled route** (Chapter 2 non-repeating surviving routes: **5–11**). The shortest paths now require engagement with at least one substantive records or technical incident before the hearing. The longest paths are optional cross-route investigations and add at most one decision relative to Chapter 2's observed maximum. This counts structural decisions, not reading time; scene prose will be edited for equivalent pacing.

The **49 planning nodes are not directly comparable** to Chapter 2's 99 playable nodes: the draft often records outcomes as inline text plus effects, while Chapter 2 uses separate narration, choice and continue nodes. The relevant comparable metrics at this stage are 71 action cards versus 80, and 28 branching hubs versus 27. Do not pad the graph to force node parity.

## What stays

- One three-way Attendance choice, short/restroom paths, and deep optional Original/photo path.
- Satisfaction, Reconciliation, Original Witness, Image Standards and Fourth Chair all preserved as landmark scenes.
- Routes B/C each retain three substantive decisions. Their outcome lines append within existing scene, not expanded into three separate subrooms each.
- Original's independent departure remains its own choice; never companion, never player's face.
- Four distinct living ending concepts, two explicitly risky fatal concepts, and Chapter 2 carryover evidence remain.
- Optional House photograph gets a major Fourth Chair payoff; players without it gain an independent Empty Claimant Photograph route.

## What was CUT or collapsed

1. **Plumbing and demonstrator registration:** each becomes ONE narrated event with a CONTINUE to a substantive records or technical route, rather than new three-card question menus.
2. **Records Review, Backstage Facility, Original Records, Staff Services:** choice-specific result text and one-way continuation, NOT new three-card hubs.
3. **Shared correction:** one two-card decision node reused after several nonfatal failures, leading directly to finale staging, rather than three separate correction departments.
4. **Human Verification, Surplus, Witness Standards, Technical Adjustments, Source Registration, Empty Photo Correction, Unapproved Exposure:** only TWO meaningful actions each; remove the least distinctive third procedure.
5. **Custody of Originals and Household Routing:** two choices each; preserve photo story evidence without one extra bureaucratic investigation.
6. **Representation Repair:** result and CONTINUE to technical staging, no extra three-choice incident.
7. **Live Source Calibration:** two decisions, one safe administrative refusal and one explicitly marked physical danger. Do not force this risk on a check failure.
8. **Original's multi-office route:** optional. A player who never opens the photo file may still finish. Route B/C focus remains independent; no copycat bureaucracy chains.
9. **Grand Reconciliation:** three initial choices; the two registry methods appear only as a second committed menu. Failure disposition is one-way, not repeated rolls.

## Compact routing principles

- Every source node and conditional/roll outcome points forward to one of admin, records or technical finale staging; some go one-way through B/C, retaining primary route A.
- Family photo conditional occurs only in the Image Standards evidence action; no-photo players advance through Empty Claimant Photo evidence.
- Behind-the-scenes checks are counted as ONE player choice, with success/failure generated edges. No optional tool stacking unless specifically approved.
- Separate ending states for Pavilion-only unregistration and full Exposition-wide relinquishment are one named ending with different Chapter 4 costs.
- All endings remain provisional until fatal methods and identity relinquishment are explicitly approved; do not build JSON using those unapproved outcomes as locked rules.

## Abstract graph file and verification

Companion JSON: docs/98_CH3_COMPACT_ROUTE_GRAPH.json. This is **story planning data, not cyoa-story-v2**. It records every scene node, action card, item reward and check transition for this compact architecture. A local graph traversal has checked that all targets exist, no transition cycles exist, all endpoints are explicit, and all three entry variants can reach every named ending when ignoring optional inventory prerequisites and accounting for both roll outcomes. No actual Chapter 3 engine/story-schema validator or browser QA has run.

## Next actual writing work

Rewrite each retained scene to short playable prose, especially the very long Fourth Chair; don't simply squeeze long passages into one node. No excessive second-order three-choice menus. Once approved, author story/chapter-03.draft.json and the art manifest, then route/story/game QA through Gameplay PMO and Claude.

**Archived source docs, not production specifications:** docs/94_CHAPTER_03_ROUTE_AND_ENDING_AUDIT.md; docs/95_CHAPTER_03_ROUTES_B_C_STRUCTURAL_AUTHORING.md; docs/96_CHAPTER_03_ROUTE_A_CLOSURE_AND_FINALE_RULES.md.
