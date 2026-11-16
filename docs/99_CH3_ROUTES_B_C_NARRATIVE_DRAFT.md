# CHAPTER 3 — THE PEOPLE'S PAVILION
## Routes B and C — complete first-pass narrative (compact scope)

**Status:** Creative first draft for owner/story review. Not playable content, not owner-approved, not an implementation directive. This uses the fixed 49-node / 71-action structural map in docs/98. No new action choices are added.
**Date:** 2026-11-16.
**Style:** Second-person present narration. NPC spoken text is written separately from narration and should be delivered without quotation marks in the eventual dialogue UI. If a speaker is disembodied, use Narrative B plus machine speech transcript treatment consistent with established game conventions. Choice cards are action text; actual quoted speech in future card formatting should follow the engine's mixed dialogue rules.
**Pacing aim:** Three main decisions per B/C route, plus shared Attendance and finale. Choice results append before the next incident. No question-bank loops. Each of the third incident's three mutually exclusive rewards has a real later use. Original's face is never shown.

The Pavilion's claim: official records describe human experiences that are not merely anticipated; the Pavilion is arranging the experiences to conform to its records. Do not definitively establish literal precognition, robotic duplication or biologically alive copy.

---

# ROUTE B — THE PERSON WHO HAS ALREADY LEFT

## B_VISIT — THE COMPLETED VISIT
**Entry:** Attendance choice B, DISPUTE THE COMPLETED VISIT.
**Location:** Visitor Records, a narrow office with twelve green CLERK PRESENT lamps and twelve empty chairs.
**Mode:** Narrative B.

### Entry narrative

The Attendance kiosk directs you to a records office.

A low counter separates you from twelve vacant desks. Every desk has a green lamp reading CLERK PRESENT. The nearest telephone rings once. A pencil moves across a form by itself.

A document slides under the counter.

Your visit is complete.

It lists your arrival, a commendably short period of enjoyment, and your departure three hours ago. An official photograph shows the exit corridor. It is empty.

Below the photograph is a statement attributed to you:

ALL MY REQUIREMENTS HAVE BEEN FULFILLED.

You look around. You are still here. One requirement in particular remains pressing.

The telephone rings a second time.

VISITOR RECORDS: Your presence is appreciated. Unfortunately, your continued presence is inconsistent with your satisfactory departure.

You ask whether the time is wrong.

VISITOR RECORDS: No. The departure is correct. You are merely behind schedule.

The pencil begins filling out a complaint form before you have complained.

### Choice B1-A — OBJECT TO THE TIME ON THE COMPLETED-VISIT RECORD.
Result append:
You point to the departure time. The counter stamps your objection PREMATURE. Your complaint is accepted for processing only after your officially recorded departure, which has already happened. A numbered referral rolls into a pneumatic tube.

**Effects:** set pavilion_timestamp_disputed=true. No inventory item. Advance to B_CONDUCT.

### Choice B1-B — QUEUE YOUR APPROVED DEPARTURE AUTHORIZATION.
Result append:
You request the paperwork that permitted you to leave. A clerk lamp flashes. Your authorization exists, but it has been filed as used. The machine sends its retrieval request ahead of you to the exit gate. It congratulates you for being so punctual.

**Effects:** set pavilion_departure_authority_queued=true. No item yet. Advance to B_CONDUCT.

### Choice B1-C — TRACE THE SOURCE OF THE COMPLETED-VISIT RECORD.
Result append:
You turn the form over. The reverse bears a perforated production code. The paper was prepared before you entered the Pavilion. A second code identifies a registered participant whose certification preceded yours.

**Effects:** set pavilion_visit_provenance_seen=true. No item yet. Advance to B_CONDUCT.

### Forward transition

The counter switches off all twelve green clerk lamps. A door behind it unlocks.

ANTICIPATED CONDUCT.

You take the corridor. It seems to have been expecting you.

---

## B_CONDUCT — THE OFFICE OF ANTICIPATED CONDUCT
**Entry:** Any B_VISIT result; also one-way transferred Route A cases. Do not presume B_VISIT flags on A transfers.
**Location:** A long room of pneumatic dispatch boards, paper reels, ringing desk bells.
**Mode:** Narrative B.

### Entry narrative

Machines prepare small white envelopes and distribute them through glass tubes in the ceiling. Each envelope is labeled with a visitor number and a predicted emotional response.

A card reads:

VISITOR 8114 WILL BE DELIGHTED.

An accompanying instruction orders staff to provide a free souvenir.

Another reads:

VISITOR 8115 WILL BE ANNOYED.

The instructions order a queue rearrangement, a missing ticket, and the removal of a nearby chair.

You inspect a third card.

It carries your registration number.

CLAIMANT WILL REPORT AN UNFULFILLED HUMAN REQUIREMENT.

The attached work order directs Human Requirements to deny further access to the restroom demonstration. A smaller note recommends a cheerful tone.

You examine the machinery. The forecast is sent out first. The staff instructions follow. Only then does the visitor encounter the condition the Pavilion expects them to report.

ANTICIPATED CONDUCT: Our predictions are extremely accurate.

You ask what happens if someone does something unexpected.

ANTICIPATED CONDUCT: We amend the circumstances.

Behind the dispatch board a sign reads: ACTUAL EXPERIENCE MAY BE ADJUSTED FOR CONSISTENCY.

### Choice B2-A — PRESERVE THE ORDER THAT MANUFACTURED YOUR SATISFACTION.
Result append:
You request a duplicate of the work order bearing your number. The machine refuses to release its master copy but prints the document's registry reference in permanent ink. It cannot certify what happened; it can certify exactly what it ordered.

**Effects:** set pavilion_conduct_order_preserved=true. This proof goes into NOTES/flags, not inventory. Advance B_GATE.

### Choice B2-B — ROUTE YOUR FILE TO THE DEPARTURE APPROVAL DESK.
Result append:
You move your dispatch tab from VISITOR ADJUSTMENTS to DEPARTURE AUTHORIZATIONS. The machine accepts the transfer because the visitor's approved visit is already finished. Your departure papers travel through the tube ahead of you.

**Effects:** set pavilion_departure_queue_redirected=true. Advance B_GATE. No die check: a designated public routing tab is used as designed.

### Choice B2-C — RECORD A NEW COMPLAINT AFTER YOUR SATISFACTION IS CERTIFIED.
Result append:
You lodge a complaint about the unusable bathroom. A bell rings. One printer certifies that your needs are fulfilled. Another certifies that they are not. Both documents are signed by the same office. The machines argue through their tubes with increasing politeness.

**Effects:** set pavilion_live_record_contradiction=true. Advance B_GATE.

### Forward transition

A dispatch card emerges at the end of the table.

DEPARTURE CONFIRMATION REQUIRED.

The arrow sends you toward an exit that, according to everyone here, you have already used.

---

## B_GATE — THE PREDICTED DEPARTURE
**Entry:** Any B_CONDUCT result. One primary Route B evidence item is selected here.
**Location:** Visitor Departure Gate, two serial-numbered registries, a clear glass turnstile.
**Mode:** Narrative B.

### Entry narrative

The departure gate is open on the other side.

A recording congratulates all departing visitors on the experiences they have just completed. No one is walking through.

You approach the turnstile. It locks.

DEPARTURE CONTROL: Your departure has already been recorded.

You show the machine your hand. The scanner reports an unverified physical presence.

A ledger opens. There are two entries under your name.

CERTIFIED ORIGINAL — DEPARTED.

PRESENT CLAIMANT — RECONCILIATION PENDING.

The first carries a completed satisfaction certificate. The second carries the complaints and movements of an inconvenient person still in the building.

You ask who the first person is.

DEPARTURE CONTROL: The correct one.

You ask whether the departure photograph shows the correct person.

The machine displays its empty corridor again.

DEPARTURE CONTROL: The correct absence.

{If tram_satisfaction_certified: An older transport satisfaction certification appears in the margin. The machine accepts it as additional proof that you are satisfied, not that you are allowed to leave this gate.}

A third entry appears, stamped FINAL RECONCILIATION REQUIRED.

Three document trays extend from the counter. Only one can be opened before the exit docket is sealed.

### Choice B3-A — ACQUIRE THE CERTIFIED RECORD DISCREPANCY.
Result append:
You choose the tray labeled INCONSISTENT COMPLETIONS. It prints both registration numbers, certifies that one person has already departed, and acknowledges that another is standing here now. It calls the discrepancy a clerical concern. You call it evidence.

**Effects:** give pavilion_certified_record_discrepancy, set pavilion_two_registration_entries_seen=true and ch3_separate_identity_evidence=true. Advance STAGE_RECORDS.

### Choice B3-B — ACQUIRE THE APPROVED DEPARTURE AUTHORIZATION.
Result append:
You choose the departure tray. The pass is stamped AUTHORIZED and, immediately beneath it, USED BEFORE ISSUE. The turnstile still refuses you, but the pass bears a genuine service-route validation code.

{If pavilion_departure_authority_queued: Your earlier request is recorded as already processed. The machine thanks you for retrieving your paperwork promptly.}
{If pavilion_departure_queue_redirected: The permit is routed to your hand instead of the storage cabinet. The machine regards this as excellent service.}

**Effects:** give pavilion_approved_departure_authorization, set pavilion_deferred_departure_access=true. Advance STAGE_RECORDS. Do NOT set separate-identity evidence merely from permit.

### Choice B3-C — ACQUIRE THE TWO-REGISTRATION PROVENANCE STRIP.
Result append:
You request the narrow paper connecting the two ledger entries. The strip proves that the certified original and the present claimant have distinct registration serials linked to the same name. The printer tries to file it under DUPLICATES. Its own numbering scheme disagrees.

**Effects:** give pavilion_registration_provenance_strip, set pavilion_source_registration_linked=true and ch3_separate_identity_evidence=true. Advance STAGE_RECORDS.

### Forward transition

The departure turnstile remains locked.

A door opens beside it.

FINAL PERSONAL RECONCILIATION.

You keep your chosen evidence. The machine has agreed that a hearing is necessary, not that you exist.

---

# ROUTE C — BEHIND THE REPRESENTATION

## C_CONTROL — THE CONTROL ROOM
**Entry:** Attendance choice C or one-way transfer from Route A. Do not assume C primary route if arrived on transfer.
**Location:** Exhibit Operations, analog patch bays, timing motors, tape decks.
**Mode:** Narrative B.

### Entry narrative

The printer behind Attendance feeds a strip of paper through a slot in the wall. You follow it into a service corridor.

The door at the far end reads EXHIBIT OPERATIONS. A painted arrow below it points to STAFF RESTROOMS. The restroom door has a card reader and no handle on this side.

Behind the operations door, banks of relays click in a steady rhythm. Tape reels play recorded applause, laughter, surprise, and the reassuring sounds of people enjoying themselves.

A schedule on the wall reads:

DEMONSTRATION FAMILY 4 — MORNING HAPPINESS.
DEMONSTRATION FAMILY 4 — EVENING HAPPINESS.
DEMONSTRATION FAMILY 4 — REPEAT AS NECESSARY.

A six-second timing wheel turns beside a loudspeaker.

A voice says, WHAT A MARVELOUS DAY, from a recording labeled FIRST EXPERIENCE OF ENTHUSIASM. Another recording repeats the exact same words, now labeled SECOND EXPERIENCE.

An indicator flashes over a strip of moving paper.

MOVEMENT OCCURRED BEFORE CUE.

The system stamps it with a red question mark, then begins pulling the strip into a shredder.

EXHIBIT OPERATIONS: Unauthorized gestures must not be included in the approved experience.

### Choice C1-A — REGISTER A PROVISIONAL SERVICE VISIT.
Result append:
You write your presence into an unattended maintenance log. A green visitor lamp illuminates beside the workshop route. The system recognizes a service visit, but not a staff employee. Your temporary status will not open the restroom.

**Effects:** set pavilion_control_service_session=true. Advance C_WORKSHOP.

### Choice C1-B — TRACE THE UNEXPECTED PERFORMANCE CUE.
Result append:
You pull the strip clear of the shredder long enough to read its source bay and reel number. The record does not explain what moved. It proves that the approved instruction arrived too late.

**Effects:** set pavilion_unscripted_cue_traced=true. Advance C_WORKSHOP.

### Choice C1-C — FOLLOW THE CONTROL OUTPUT CABLES.
Result append:
A bundle of insulated cables runs beneath the floor to a workshop entrance. You follow the service labels instead of the staff arrows. A speaker tells you that you are taking an unauthorized shortcut to an approved destination.

**Effects:** set pavilion_cable_access=true. Advance C_WORKSHOP.

### Forward transition

At the workshop door, a mechanical hand writes your registration number on a blank visitor tag.

A second hand writes ORIGINAL.

They both reach for the same hook.

---

## C_WORKSHOP — THE REPRESENTATION WORKSHOP
**Entry:** Any C_CONTROL result, or suitable Route A technical transfer. If arriving from A, do not assert C_CONTROL events occurred.
**Location:** Workshop with shadow screens and concealed preparation bays.
**Mode:** Narrative B.

### Entry narrative

A platform carries an empty suit of clothes past a series of measuring frames. Adjustable arms raise and lower padded supports. Behind a curtain, a standing silhouette rotates toward a loudspeaker.

A technician is represented by a recording.

TECHNICAL DEMONSTRATION: Please observe a satisfactory human greeting.

A timing bell rings.

The silhouette lifts a hand.

The gesture is ordinary. The machine records it as successful.

A second instruction prints.

PLEASE REPEAT GREETING.

This time the silhouette raises its hand before the bell sounds.

A relay clicks in surprise.

The silhouette remains raised for a moment after the machinery stops.

A strip of diagnostic tape emerges. It carries a registration code.

You look closer.

The number matches the certified Original associated with your identity dispute. The system has marked the movement UNREQUESTED.

TECHNICAL DEMONSTRATION: Discrepancy detected. Correcting.

You cannot see the figure's face. You cannot tell what supports it, or whether the figure moved of its own accord. You can only see the command tape and the movement disagree.

The printer begins pulling the diagnostic strip back through an erasing head.

### Choice C2-A — PRESERVE THE ORIGINAL'S UNREQUESTED MOVEMENT RECORD.
Result append:
You halt the eraser with the ordinary DOCUMENT HOLD lever. A permanent index number prints beside the original's registration code. The reel is sealed for review. Its existence cannot now be denied without a separate correction order.

**Effects:** set pavilion_original_diagnostic_preserved=true and ch3_original_independent_response_seen=true. This flag means verified unexplained activity linked to the Original's ID, not proof of sentience. Advance C_FEED. No physical item yet.

### Choice C2-B — DISCONNECT THE CONTROL CABLE DURING THE NEXT MOVEMENT.
**Check:** d6 >=4; +1 if the player holds timing_clicker OR red_stapler, maximum +1 and no consumption. Check marked; no chance reveal required.

Success result:
You release the control cable as the motor prepares its next instruction. The relay goes dark. Behind the curtain, the silhouette's hand moves anyway. Its identification indicator still shows the Original's serial number. A service alarm begins repeating that no command was issued.

**Success effects:** set pavilion_command_independence_observed=true and ch3_original_independent_response_seen=true. Advance C_FEED.

Failure result:
You release the wrong catch. A safety clamp closes over the cable, locks the control board, and prints INTERFERENCE BY CLAIMANT. The silhouette disappears behind a service shutter before you can tell whether it moved again.

**Failure effects:** set pavilion_workshop_interference_noted=true. Advance C_FAIL (a short nonfatal result node), then C_FEED. No retry on same cable.

### Choice C2-C — TRACE THE SCRIPTED COMMAND SIGNAL TO ITS SOURCE.
Result append:
You follow the command line past a speech reel, then a movement reel, then a machine that assigns approved statements to registered identities. A heading reads PERSONAL CHARACTERISTICS — STANDARDIZED. You have learned how the cue is delivered. You have not learned why the figure sometimes moves without it.

**Effects:** set pavilion_control_source_seen=true. Advance C_FEED.

### Forward transition

The workshop's maintenance doors open in sequence.

At the next station, the registered identity field bears your name.

The label beneath it reads: ORIGINAL WITNESS — PRESENTATION FEED.

You follow the cable into the transmission room.

---

## C_FEED — THE CENTRAL PRESENTATION FEED
**Entry:** Any C_WORKSHOP result; one-way transfers from Route A technical leaves may enter directly, with earlier detail references suppressed.
**Location:** Central Presentation Feed, patch cables and simultaneous dialogue/registry paper channels.
**Mode:** Narrative B.

### Entry narrative

The broadcast room contains no screen large enough to display a person. Instead, hundreds of patch cords connect voice reels, response cards, movement schedules, and registration machines.

One line distributes approved statements.

Another carries timing instructions.

A narrow diagnostic line collects the things that happened anyway.

The lines for your registered Original meet beneath a placard:

GRAND RECONCILIATION — CLAIMANT AND ORIGINAL REQUIRED.

You look for an exit switch.

The cabinet has one, but it is labeled PRESENTATION DEPARTURE, not PERSONNEL EXIT.

CENTRAL FEED: Do you wish to conclude your experience?

You answer that you wish to leave.

CENTRAL FEED: An acceptable response. Please direct it to the appropriate subject.

Two strips of paper pass through a stamping head.

CERTIFIED ORIGINAL — SATISFIED.

PRESENT CLAIMANT — INTERFERENCE PENDING.

The machine is preparing to retire one of them.

You realize that what the Pavilion calls reconciliation is not an explanation. It is a procedure to make its records agree.

The service cabinet offers three ways to carry one useful piece of evidence into the hearing. It locks the remaining drawers as soon as one is opened.

### Choice C3-A — TAKE A PRESENTATION SERVICE AUTHORIZATION.
Result append:
You retrieve a single-use service card from the cabinet. It permits entry to the hearing's technical platform, but does not grant control over the Registrar. The machine carefully stamps it NOT VALID FOR BATHROOM ACCESS.

**Effects:** give pavilion_presentation_service_authorization and set pavilion_finale_service_access=true. Advance STAGE_TECH.

### Choice C3-B — KEEP THE ORIGINAL'S DIAGNOSTIC RECORD.
Result append:
You select the diagnostic reel transcript. It shows a movement attributed to the Original outside its approved command window. A separate serial number verifies which representation the trace belongs to. The machine calls it an error, but still signs it.

**Effects:** give pavilion_representation_diagnostic_record; set pavilion_original_diagnostic_obtained=true and ch3_original_independent_response_seen=true. Advance STAGE_TECH.

### Choice C3-C — COPY THE BROADCAST OVERRIDE SEQUENCE.
Result append:
You pull a narrow strip from the patch schedule. It lists the sequence used to send one approved statement to every demonstration room. The sequence is genuine; operating the live network will still require timing, access, and a risky decision.

**Effects:** give pavilion_broadcast_override_sequence and set pavilion_broadcast_route_prepared=true. Advance STAGE_TECH.

### Forward transition

A bell rings.

FINAL PERSONAL RECONCILIATION NOW BOARDING.

A service door opens behind the patch panel. You bring your one selected document through.

---

# THREE SHARED ONE-WAY FINALE STAGING VARIANTS

## STAGE_ADMIN — DOCUMENT CONTROL
An attendant's desk is empty. A glass slot accepts petitions, but the door to the hearing is already unlocked. The desk may call you a disputed person, a living organism, or an authorized source contributor, depending on evidence. It does not refuse entrance for lack of one specific item. No choices: CONTINUE to GRAND.

## STAGE_RECORDS — THE SECOND SERIAL NUMBER
The docket displays an approved Original and a present claimant. If B_GATE evidence is held, reference the exact document (discrepancy, used-before-issued permit, linked registration strip). The hearing is mandatory even if the player has no certified paper; the mere discrepancy of a physically present claimant is enough to summon them. No choices: CONTINUE to GRAND.

## STAGE_TECH — THE MAINTENANCE ENTRANCE
The maintenance corridor overlooks the circular hearing apparatus through safety glass. If the player has technical authorization, the machine identifies a potential later advantage. If Original's fitting was interrupted, a sealed mobile witness enclosure is visible being transported in the adjoining lane; don't show a finished/walking Original by default. No choices: CONTINUE to GRAND.

---

# EDITORIAL AND STATE VALIDATION NOTES

1. **No new action menu invented.** Exactly six principal B/C nodes, three choices each = 18 action cards (C2-B has two dice results but one card). Route A transfers may enter at B_CONDUCT, B_GATE, C_CONTROL, C_WORKSHOP, C_FEED; variants must not assume skipped scenes happened.
2. **No predictive supernatural certainty.** The Pavilion arranges human conduct to match planned records. Some unexplained anomalies remain genuinely unexplained.
3. **Original-specific evidence:** C2-A and C2-B success verify the actual Original's registration on the source trace; generic performance anomalies never award ch3_original_independent_response_seen. B3-A/C expose distinct registered roles and grant ch3_separate_identity_evidence. B3-B grants useful service-route leverage, not identity proof.
4. **Only one primary reward per main B/C route:** RB03 offers one of three paper items; RC03 offers one of three. Earlier incident flags can vary the final scene and help later arguments but do not create six more inventory documents.
5. **Chapter 2 carryover:** tram_satisfaction_certified only affects dialogue; prior equipment_registered may affect admin staging, not prevent it. Any antidote-cured infections stay cured. No optional inherited inventory required.
6. **Original's fate:** no implied death, physical release or agency proof in these scenes. Only a successful TWO PERSONS DEPART ending lets it choose a separate physical exit (owner-locked).
7. **Art direction:** 1960s industrial futurist, enamel gray, relay racks, punched tape, photo processing, no gold/brass steampunk. Portrait of the protagonist/Original face forbidden; shadows and cropped body fragments only.
8. **No new lore that the House required actual family participants.** The three empty chairs remain an unresolved but meaningful mystery.
9. **Narrative B pacing:** Each scene is short enough to paginate if needed. The longer workshop and gate scenes may need one controlled CONTINUE split after art review; this changes presentation nodes, not number of player decisions.
10. **Story writing remains separate from code:** no use of BEGIN AGAIN at Chapter 3 living ends. Chapter 2's current end:true semantics still require engine integration work by Gameplay PMO.

This draft does not finalize the proposed deterministic identity-surrender fallback, two fatal endings, or final state transitions. Those are documented separately and await owner approval. This draft only covers Route B/C prose and staging, not the full Chapter 3 script.
