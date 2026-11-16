# Chapter 3 — The People's Pavilion: route, ending and failure audit

**Status:** STORY STRUCTURE AUDIT — PROPOSED FIXES, NOT PLAYABLE OR OWNER-APPROVED STORY CANON.
**Date:** 2026-11-16.
**Owner-locked:** Original Witness may escape independently, may return in a later chapter, and is not the protagonist's companion.
**Source:** conversation-authored Chapter 3 storyboard through CH3-010C2; Route B/C structural outlines and Grand Reconciliation design; Chapter 2 playable source at e98602f7992908a750672006f556b8efc15d686f. No Chapter 3 JSON presently exists.
**Scope:** planning only. This is not authorization to code, merge, promote art or deploy.

## Executive verdict

Architecture is viable but NOT reachability-complete. Route A has many fully drafted early scenes and dangling subroutes; Routes B and C have three-incident outlines only. The four successful finale concepts are distinct; failure transitions and a no-item guaranteed survivable exit remain undefined in earlier drafts.

Locked invariants:
1. Chapter 2 entry groups are exactly public_concourse, service_infrastructure, underground_transit. All three reach CH3-002.
2. CH3-002 chooses route A Human Requirements, B Visitor Records or C Exhibit Operations once. Forward-only transitions; no repeated choice banks or backtracking.
3. Every surviving route has an accessible, nonfatal exit without inherited items or favorable random rolls. Lack of family photograph never blocks chapter completion.
4. Four planned nonfatal exits: PERSONALLY RELEASED, NO PERSON PRESENT, TWO PERSONS DEPART, UNAPPROVED BROADCAST. Two proposed fatal endings: SUCCESSFULLY RECONCILED and PERMANENTLY ARCHIVED.
5. Only TWO PERSONS DEPART sets Original Witness status to escaped_independently; other outcomes retained or unknown. Original chooses to depart and travels by a different exit. No face reveal or confirmed technical nature.
6. The House portrait has three wholly empty chairs and one partially cropped occupied chair showing the protagonist's shoes, legs, shirt and lap, never face. Its inventory image is unchanged, never automatically confiscated.
7. No dice roll for simply arguing, reading or inspecting. Checks appear on physically uncertain or contested outcomes; risk-marked action when fatal failure possible.
8. Seven inventory slots are VISIBLE, with arrow navigation; do not invent a seven-item carry cap.

## Route graph

Chapter 2 3 entry groups -> CH3-001 variants -> CH3-002 (Attendance)
- A: CH3-003 (Human Requirements) -> CH3-004A/B/C -> existing deep investigations or one-way transfer
- B: RB01 Completed Visit -> RB02 Anticipated Conduct -> RB03 Predicted Departure
- C: RC01 Control Room -> RC02 Representation Workshop -> RC03 Presentation Feed
All flow forward into one of ADMIN / RECORDS / TECHNICAL finale-staging variants.
All finale-staging variants -> Grand Reconciliation.
First finale menu uses three cards:
A CONTEST IDENTITY -> PERSONALLY RELEASED or denial with one-way fallback
B MANIPULATE REGISTRY -> one further committed choice of QUIET UNREGISTRATION or CONTRADICTORY BROADCAST (no revisiting menu)
C ADDRESS ORIGINAL -> TWO PERSONS DEPART or denial with one-way fallback
FATAL outcomes require separate, explicitly high-risk physical decisions.

## Route A existing leaves: unclosed forward links

All identifiers below refer to conversational story drafts, not existing JSON nodes.

| Leaf / drafted path | Required forward link |
|---|---|
| CH3-003 B -> CH3-004B plumbing | Link to RC01/RC02 with technical staging; no bathroom success |
| CH3-003 C -> CH3-004C volunteer | Link to staff/administrative staging, with provisional-human classification |
| CH3-004A A -> CH3-005A | Existing 005A choices |
| CH3-004A B -> CH3-005B script refusal | Witness Standards or one-way RB02 transfer |
| CH3-004A C -> CH3-005C success | One-way maintenance access to RC01 |
| CH3-004A C -> CH3-005D failure | Shared Behavioral Correction bridge, nonfatal |
| CH3-005A A -> CH3-006A | Reconciliation branches |
| CH3-005A B -> CH3-006B future record | One-way RB02 / records staging |
| CH3-005A C -> CH3-006C staff | One-way RC01 / technical staging |
| CH3-006A A -> CH3-007A | Original Witness |
| CH3-006A B -> CH3-007B life | Human Verification -> admin staging; infection variant |
| CH3-006A C -> CH3-007C surplus | Surplus Processing -> technical staging, dangerous but avoidable |
| CH3-007A A -> CH3-008A testimony | Witness Standards -> admin/witness staging |
| CH3-007A B check success -> CH3-008B1 | Technical Adjustments -> technical staging |
| CH3-007A B check failure -> CH3-008B2 | Behavioral Correction bridge |
| CH3-007A C -> CH3-008C | Image Standards choices |
| CH3-008C A -> CH3-009A negatives | Source Registration -> records staging |
| CH3-008C B, photo held -> CH3-009B Fourth Chair | Four CH3-010 destinations |
| CH3-008C B, no photo -> CH3-009C | Photographic Correction -> staging; independent alternative proof |
| CH3-008C C check success -> CH3-009D | Image Production -> technical staging |
| CH3-008C C check failure -> CH3-009E | Behavioral Correction bridge |
| CH3-009B A -> CH3-010A Custody | admin staging, source-conflict hold |
| CH3-009B B -> CH3-010B Household Routing | records/witness staging, routing strip |
| CH3-009B C pass -> CH3-010C1 | Representation Repair -> witness/technical staging |
| CH3-009B C fail -> CH3-010C2 | Live Source Calibration: one safe withdrawal and one marked physical-risk choice |

This table is an INVENTORY of missing closure, not an invitation to add new office chains. Author only enough transitional incidents to link each leaf to finale staging; keep the deep photo route optional. A short Route A must reach finale without visiting every drafted department.

## Route B authoring contract

RB01 Completed Visit: one of (certified discrepancy, questionable departure permit, source provenance). Choice advances, no compulsory roll.
RB02 Office of Anticipated Conduct: prove forecasts are work orders used to make approved outcomes happen. Choose preserve evidence, exploit staff instructions or introduce a controlled contradiction. At most one major route reward.
RB03 Predicted Departure: a departed official identity and present claimant coexist. Choose administrative proof, registry bypass or separate-identity evidence. All lead to finale staging, without compulsory check success.
The story should NOT confirm supernatural literal future sight. Office actively engineers events.

## Route C authoring contract

RC01 Control Room: choose staff authorization, unexplained error or follow the cables. Applause clicker offers optional bonus when a real check exists.
RC02 Representation Workshop: unauthorized movement outside approved sequence; acquire diagnostic evidence or access. Do NOT conclusively classify Original as robot, clone or human.
RC03 Central Presentation Feed: access, diagnostic proof, broadcast preparation. One major technical reward, not three.
All forward. Technical tools useful but no inherited item is required to enter finale.

## Finale resolution and proposed safe fallback

A Administrative exception: challenge documentary claim. A failed roll means denial then one-way disposition choice, not death, reroll or return to menu.
B Quiet unregister: technical action to erase Pavilion claimant registration while physically leaving via an outward, unregistered-material service transfer. An unauthorized attempt has a check; failure advances.
C Original departure: original actively declares an independent desire and may refuse player's name. Registrar certification requires check; failed certification retains Original, while claimant can escape by another method. Previously encountered vs first-seen Original needs distinct short prose.
D Broadcast: signal contradictory records Pavilion-wide; failed operation triggers a nonfatal correction/retention alarm with a later escape decision, not automatic death.

**Recommended essential safety closure:** if all other procedures fail or player elects it immediately, permit a deterministic voluntary surrender of identity claims. Registrar removes claimant's recognized status and routes their **physical body safely out** through outbound unregistered transfer. Ending NO PERSON PRESENT, severe Exposition-wide identity loss; technical unregister yields the same named ending while preserving other identity records. This is a new proposed rule, NOT an owner-locked one. It keeps the game survivable for all no-item/no-luck states. Without this or an equivalent deterministic exit the graph is not safe-complete.

The previous NO PERSON PRESENT tally was semantically inconsistent with an Original still certified; distinguish REGISTERED CLAIMANTS: 0 from RECOGNIZED ORIGINALS: 1. The player remains physically present until exit, despite loss of registration.

## Proposed check table

| Attempt | Base need on d6 | Modifiers | Failure |
|---|---|---|---|
| Administrative exception, absent conclusive approval | 4 | +1 valid documentary evidence, nonstacking | Denial -> one-time disposition |
| Technical unregister with wider identity intact | 4 | +1 tech evidence/tool, nonstacking | Controlled-transfer fallback |
| Independent Original recognition | 5 | +1 observed independent response; +1 proof of separate source; maximum +2 | Original retained, claimant can choose another exit |
| Pavilion broadcast override | 4 | +1 presentation access/tool, nonstacking | Correction alarm -> one-time recovery |
| Deliberate hazardous physical fitting/retention intervention | 4 provisional | +1 explicit suitable tool | Only such warned actions may reach fatal endings |

Need 4 on d6 = 50%; +1 = 66.7%. Need 5 = 33.3%; +1 = 50%; +2 = 66.7%. Dice are behind scenes; check marker remains even if an allowed modifier later makes success certain. No repeat rerolls, no automatic success for one legacy item.

## Ending contract

| Exit | ch3_exit_route | ch3_original_status | Other persistent values |
|---|---|---|---|
| PERSONALLY RELEASED | administrative_exception | retained | claimant legally separate |
| NO PERSON PRESENT, technical | unregistered | retained | ch3_identity_unregistered true; scope pavilion_only |
| NO PERSON PRESENT, voluntary erasure | unregistered | retained | ch3_identity_unregistered true; scope exposition_wide |
| TWO PERSONS DEPART | two_persons_depart | escaped_independently | ch3_original_independent_identity true |
| UNAPPROVED BROADCAST | broadcast_disruption | unknown | ch3_pavilion_disrupted true |
| SUCCESSFULLY RECONCILED (fatal) | none | author explicitly | claimant physically used as fitting material; player face unseen |
| PERMANENTLY ARCHIVED (fatal) | none | author explicitly | claimant physically retained as source material; player face unseen |

The fatal titles and outcomes are proposals, not approved modal/button text. Do not accidentally present them as already generated art.

**Original state continuity:** if fitting previously suspended or interrupted, move its sealed mobile witness apparatus to the hearing or present an approved remote presence, but do not silently declare fitting complete. The Original's independence must remain a real choice. Outside TWO PERSONS DEPART it may stay in Pavilion or remain unknown depending on ending.

## Canonical state and items

Chapter 2 hands off exactly chapter3_entry_group values public_concourse, service_infrastructure, underground_transit (five living endings). Do not confuse with ch2_exit_route. Flags tram_satisfaction_certified, equipment_registered, spore_infected, thorn_infected and held items remain persistent.

At CH3-002 set ch3_primary_route = A/B/C once. Crossing into another route's set does not overwrite it.

Use CH3 finale evidence flags exactly:
- ch3_original_independent_response_seen
- ch3_separate_identity_evidence

Earlier narrative-specific pavilion_original_unscripted_answer, pavilion_house_photo_matched, pavilion_source_negatives_examined, pavilion_source_conflict_hold and related flags are upstream authored events; at the actual evidence-awarding node explicitly set one canonical finale flag or use an audited derived predicate. Never silently assume previous flags imply it.

The one-off Chapter 3 proposed documents include certificate_fulfilled_requirements, pavilion_discrepancy_receipt, pavilion_temporary_staff_pass, pavilion_original_appearance_order, pavilion_disputed_testimony_notice, pavilion_proof_of_life, pavilion_duplicate_routing_tag, pavilion_source_contribution_receipt, pavilion_household_routing_strip, pavilion_empty_claimant_photo, pavilion_unapproved_exposure, pavilion_mandatory_adjustment_summons. Do not give every item on one path. Prefer a give/take document exchange or persistent NOTES evidence for superseded paperwork.

House photo remains held after Pavilion scans, with evidence benefits but no hard gate. Item bonuses from stapler, rubber band ball and clicker must check actual inventory: these may have been consumed or seized earlier. Botanical infections alter verification text/risks but cannot force automatic fatality. The seed canister may matter as optional biological evidence but must not be automatically released.

## Audit blockers and closures

BLOCKER: 25+ Route A leaf/variant destinations lack authoring closure. Make every one reach admin/records/technical staging or an explicit warned fatal.
BLOCKER: Route B/C have no complete authored nodes/choice outcome contracts. Write their full choice graphs.
BLOCKER: no guaranteed safe no-item/no-luck disposition is approved. Obtain owner ruling on costly identity relinquishment or an alternative.
BLOCKER: finale failures lack defined no-reroll transitions; implement one-way recovery.
HIGH: Original staging needs consistent earlier-suspension/first-encounter handling.
HIGH: evidence flags and item names need one canonical schema.
HIGH: Route A too long if every scene made mandatory; deep witness/photo path should be optional.
HIGH: House photo and carryover items must not be missing-item hard gates.
MED: finale base list has four conceptual endings while UI baseline fits three 2-line choices; use the nested B/D registry decision.
MED: ending title NO PERSON PRESENT vs still-certified Original needs accurate tally wording.
MED: bathroom objective must be visible in the finale and denied for route-specific identity reasons without undoing chapter survival.

## Required test matrix (PLANNED; NOT EXECUTED)

1. Three Chapter 2 success entry groups by three CH3-002 primary routes = nine baseline no-inherited-item starts; each reaches at least one safe ending without guaranteed favorable rolls.
2. Every Route A leaf in closure table passes scripted forward-only route reachability, including failure variants.
3. Route B/C each have at least three meaningful decisions with item/flag delta and at least one route to distinct finale leverage.
4. All four nonfatal endings reachable from a justified choice path; no single inherited item compulsory.
5. Family photo present/absent in Image Standards; both have independent evidence route; original photo never auto-lost.
6. Check at roll 1 and 6 with/without modifiers; bonuses nonstacking except independent evidence max +2; marker retained.
7. Failed admin, quiet unregister, Original independence, broadcast all lead to safe disposition or later separately opted-in risk; no repeated rolls.
8. Original first seen in finale / met previously / fitting suspended / fitting interrupted; escaped_independently only on successful two-person outcome.
9. House ownership, badges, infected/cured, tram certificate, seed canister carried/surrendered/destroyed, and no carried items.
10. Save/restore at Chapter 2 to 3 transition, route joins, finale, and separate chapter endings; global NOTES persist.
11. Audit second-person present-tense voice, 314x206 scene identity, portrait crop rules, user face never rendered.
12. Only after written Chapter 3 JSON exists may content validator, story graph coverage and browser QA be reported. NONE have been run for Chapter 3 now.

## Owner decisions pending

1. Approve or revise guaranteed voluntary identity surrender as no-item safe exit.
2. Approve three finale opening options with registry bifurcating into B/D rather than four initial cards.
3. Agree deep Route A witness/photo investigation is optional and shorter routes to finale remain available.
4. Approve the two fatal concepts and their explicit warned risk mechanisms before final death prose/art.
5. Then author missing bridges and B/C dialogue, run route audit again, write playable Chapter 3 JSON, and hand implementation through ChatGPT Gameplay PMO to local Claude.

**No production, story JSON, engine, art, merge, deployment or Gameplay PMO authorization is granted by this document.**
