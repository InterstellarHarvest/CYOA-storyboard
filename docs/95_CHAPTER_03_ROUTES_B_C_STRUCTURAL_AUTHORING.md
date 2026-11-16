# Chapter 3 — Route B/C structural authoring and one-way convergence

**Status:** proposed story architecture; NOT owner-approved final narrative, no playable JSON, no implementation authorization.
**Prepared:** 2026-11-16. Builds on docs/94_CHAPTER_03_ROUTE_AND_ENDING_AUDIT.md and the prior storyboards.
**Owner-locked:** The Original Witness may choose to escape *independently*, never becomes a mandatory companion, may reappear later, and must never expose the protagonist's face.
**Scope of this document:** Concrete scene beats, choice labels, forward transitions, inventory/flag deltas, and catch-up at the Grand Reconciliation for Routes B and C. No artwork instructions beyond locations.

## High-level construction

Three Chapter 2 entry groups -> CH3-001 variant -> CH3-002 Attendance, with three choices:
- A FOLLOW HUMAN REQUIREMENTS -> CH3-003, previously drafted deep Route A; see docs/94 for unfinished leaves.
- B DISPUTE COMPLETED VISIT -> RB01 / ch3_completed_visit.
- C FOLLOW PRINTER INTO EXHIBIT OPERATIONS -> RC01 / ch3_control_room.

At CH3-002 set only once ch3_primary_route = A or B or C. Route transfers do not change it.

B has three shared incidents, each with three **forward-only** choices and one short unique result beat per choice. Route C does likewise. This is not a dialogue hub: on selecting one of the three, apply effects, append its result, then CONTINUE to next shared incident. Never reactivate or gray-out a spent bank. At each third incident the choice gives one exclusive principal reward, then moves to appropriate finale staging.

**All routes retain the urgency of finding a bathroom**, even in departments that deny the protagonist's presence.

## Route B — The Person Who Has Already Left

### RB01 — The Completed Visit
Node ID: ch3_completed_visit; scene: pavilion/visitor_records; mode Narrative B.
Entry: CH3-002 B, no prerequisite item.

Scene beats:
- The office clerk is a desk with green availability lamps and no occupant.
- It hands the protagonist a certified visit log: arrival, satisfaction, and departure were all completed three hours ago.
- A dated photographic proof of departure contains an empty exit corridor.
- A line describes the player's forthcoming objection in terms the player has not yet chosen. Do not assert supernatural literal precognition.
- The speaker claims the record is *ahead of schedule*, not inaccurate; it offers a correction process.

One-time choices:
1. **B1-A — "OBJECT TO THE TIME ON THE COMPLETED-VISIT RECORD."** Outcome rb01_timestamp_dispute: the machine stamps the complaint PREMATURE and submits an objection work order. Set pavilion_timestamp_disputed = true. No item yet. Continue RB02.
2. **B1-B — "ACCEPT THE APPROVED DEPARTURE AUTHORIZATION."** Outcome rb01_accept_departure: the desk places a numbered departure stub on its conveyor, insists the protagonist is already outside, and announces the stub is ready for retrieval at the exit checkpoint. Set pavilion_departure_authority_queued = true. Avoid awarding it immediately, keeping one principal B item for RB03. Continue RB02.
3. **B1-C — "TRACE THE SOURCE OF THE COMPLETED-VISIT RECORD."** Outcome rb01_trace_provenance: a perforated line identifies a control office and a prior registration that predates the visit. Set pavilion_visit_provenance_seen = true. Continue RB02.

No dice. The player is choosing which evidence to prioritize, not trying to win a contested mechanical maneuver.

### RB02 — The Office of Anticipated Conduct
Node ID: ch3_anticipated_conduct; scene: pavilion/anticipated_conduct; mode Narrative B.
All three RB01 outcomes lead here.

Scene beats:
- Work orders stream from record validation machines to the pavilion floor.
- Approved "happy visitor" records generate instructions to suppress complaints. Approved "angry visitor" records order staff to route visitors toward irritation.
- One order bears the claimant's number and tells Human Requirements to reject an already-fulfilled need. The prediction is a work order.
- Staff machines do not need to see a literal future; by controlling available choices they can make approved behavior likely or inevitable.
- A pneumatic tube begins delivering revised orders toward the final departure gate.

One-time choices:
1. **B2-A — "PRESERVE THE ORDER THAT MANUFACTURED YOUR SATISFACTION."** rb02_preserve_order: the desk prints a traceable reference number, leaving a flag rather than a loose extra inventory item. Set pavilion_conduct_order_preserved = true. Continue RB03.
2. **B2-B — "ROUTE YOUR FILE THROUGH THE DEPARTURE APPROVAL DESK."** rb02_redirect_order: alter the distribution address using the authorized visitor-change mechanism, not an unearned hacking power. The queue now sends the player's record to the gate ahead of its expected claimant. Set pavilion_departure_queue_redirected = true. Continue RB03.
3. **B2-C — "CAUSE A RECORDED COMPLAINT AFTER YOUR SATISFACTION IS ALREADY CERTIFIED."** rb02_force_conflict: log a fresh complaint while the satisfaction file remains closed; the system creates two conflicting statuses for one registration. Set pavilion_live_record_contradiction = true. Continue RB03.

No mandatory roll. Deliberate statements and use of visible desk controls reliably create the resulting documents; risk of manipulating the actual secure registry comes later.

### RB03 — The Predicted Departure
Node ID: ch3_predicted_departure; scene: pavilion/predicted_departure; mode Narrative B.
All RB02 outcomes lead here.

Scene beats:
- Real exit gate with green DEPARTED readout refuses to unlock for a physically present claimant, because the registered visitor has already left.
- A secondary ledger shows "certified departed original" and "unverified present claimant" under related but different serial entries.
- Player can go to registration hearing; the gate cannot simply be walked through. Corridor at end leads to the central chamber, not out of the chapter.
- Photograph on the gate shows the empty exit corridor with a neatly timed departure timestamp.
- If tram_satisfaction_certified, the system recognizes the old satisfaction certification but still distinguishes today's completed-visit record; do not collapse them.

**Mutually exclusive main B reward choices** (the B1/B2 flags modify dialogue/advantage but do not award additional principal B items):
1. **B3-A — "SECURE A CERTIFIED DISCREPANCY BETWEEN DEPARTURE AND PHYSICAL PRESENCE."** rb03_discrepancy: official machine produces discrepancy letter naming both certified departure and present claimant. Give pavilion_certified_record_discrepancy; set pavilion_two_registration_entries_seen = true and ch3_separate_identity_evidence = true. Continue ch3_finale_records_staging.
2. **B3-B — "CLAIM THE DEPARTURE AUTHORIZATION THE SYSTEM ALREADY ISSUED."** rb03_departure_auth: collect a permit stamped USED BEFORE ISSUE. Give pavilion_approved_departure_authorization; set pavilion_deferred_departure_access = true. Continue ch3_finale_records_staging. Without RB01-B it is still retrievable through the numbered registration at the gate, but RB01-B grants a useful earlier queue flag.
3. **B3-C — "COPY THE INTERNAL LINK BETWEEN THE DEPARTED ORIGINAL AND PRESENT CLAIMANT."** rb03_provenance_strip: pull a short linked-serial provenance strip from the inspection printer, no tampering. Give pavilion_registration_provenance_strip; set pavilion_source_registration_linked = true and ch3_separate_identity_evidence = true. Continue ch3_finale_records_staging.

This route reveals the existence of another certified holder of the player's identity, but does NOT show the Original Witness physically until the finale (unless the player came from a previously drafted Route A transfer).

### B item economy

No B1/B2 physical item required; RB03 gives exactly one of:
- pavilion_certified_record_discrepancy
- pavilion_approved_departure_authorization
- pavilion_registration_provenance_strip

They are not interchangeable in final consequences: discrepancy supports admin exception; departure permit supports a registration exit/controlled bypass; linked provenance supports separate-identity argument. Other evidence from Chapter 1/2 may coexist. No item is required for a safe chapter completion.

## Route C — Behind the Representation

### RC01 — The Control Room
Node ID: ch3_control_room; scene: pavilion/exhibit_control; mode Narrative B.
Entry: CH3-002 C or forward transfer from Route A service/technical leaves.

Scene beats:
- Reel-to-reel voice tracks, analog lamps, relay banks, timed laughter and applause; 1960s industrial, not digital touchscreen.
- Machines distribute approved dialogue to demonstrations. One console holds six-second cue cycles; optional applause timing clicker is recognizable but not consumed.
- A monitoring strip shows a representation occasionally moving out of sync with its printed cue. The identity field is partly obscured.
- A restroom arrow pointing toward STAFF REQUIREMENTS leads to a denied area; preserve the bathroom goal.

One-time choices:
1. **C1-A — "REGISTER A MAINTENANCE VISIT TO THE CONTROL ROOM."** rc01_staff_route: use an unattended maintenance signing spool to register a provisional access session. Set pavilion_control_service_session = true. Continue RC02. This is limited access, not a full staff credential.
2. **C1-B — "TRACE THE UNEXPECTED PERFORMANCE CUE."** rc01_unscripted_trace: identify the originating workshop bay and preserve its reel number. Set pavilion_unscripted_cue_traced = true. Continue RC02.
3. **C1-C — "FOLLOW THE PHYSICAL OUTPUT CABLES."** rc01_cable_route: enter a narrow shielded cable path and emerge at workshop service entrance. Set pavilion_cable_access = true. Continue RC02.

No dice yet. Each yields route knowledge/position but no principal physical reward.

### RC02 — The Representation Workshop
Node ID: ch3_representation_workshop; scene: pavilion/representation_workshop; mode Narrative B; optionally Focus A for actual console inspection only.
All RC01 results lead here.

Scene beats:
- Human-sized adjustable positioning frames, speaker modules, costumes, shadow screens, punched-tape schedules.
- One representative person performs a programmed motion; once, it moves *before* the timing cue.
- A registration card for the protagonist appears among preparation orders. The Original may be in an unseen adjacent bay; never expose a face, confirm no technology underlying the representation.
- System labels the unscheduled behavior "service irregularity", about to overwrite its diagnostic trace.

One-time choices:
1. **C2-A — "PRESERVE THE RAW DIAGNOSTIC OF THE UNCOMMANDED MOVEMENT."** rc02_preserve_diagnostic: capture trace reference on a diagnostic reel with the original's registration ID; no physical inventory item yet. Set pavilion_original_diagnostic_preserved = true and ch3_original_independent_response_seen = true **only if** the card and trace are explicitly verified to be the Original Witness rather than a generic representation. Continue RC03.
2. **C2-B — "DISCONNECT THE COMMAND CABLE DURING THE NEXT MOVEMENT."** rc02_disconnect is an authored **marked** check d6 >=4. +1 from timing_clicker OR red_stapler if held, nonstacking; no guaranteed success, no consumption. On pass: rc02_disconnect_pass, movement continues after unplugging the command cable, still not enough to prove mechanism/biology. Set pavilion_command_independence_observed = true and ch3_original_independent_response_seen = true if ID confirms it is the Original. Continue RC03. On fail: rc02_disconnect_fail, cable clamps shut and records unauthorized workshop interference; set pavilion_workshop_interference_noted = true, then continue RC03 via a different service route. No fatality.
3. **C2-C — "FOLLOW THE APPROVED CONTROL SIGNAL TO ITS SOURCE."** rc02_trace_control: show the scheduling reel and the distinct equipment that distributes certified dialogue. Set pavilion_control_source_seen = true. Continue RC03 without independent-response flag.

The C2 independent evidence is about behavior, not evidence of *separate legal identity*. The finale also needs documentary proof or an additional check for independent status.

### RC03 — Central Presentation Feed
Node ID: ch3_central_presentation_feed; scene: pavilion/presentation_feed; mode Narrative B.
All RC02 outcomes lead here.

Scene beats:
- A physical patch panel distributes registered visitor sounds, approved sentences, and certification status to exhibits.
- Two separately numbered feed strips carry the Original's approved speech and live discrepancies. The assembly uses the protagonist's identity number.
- System schedules GRAND RECONCILIATION: PRESENT CLAIMANT / CERTIFIED ORIGINAL, not a normal visitor exit.
- One feed will allow the Pavilion to reject the live claimant; the player can preserve evidence or prepare an escape.
- The final hearing chamber is accessible through one-way service door.

**Mutually exclusive main C reward choices**:
1. **C3-A — "TAKE THE AUTHORIZED PRESENTATION SERVICE ROUTE."** rc03_service_auth: secure a single-time technical service pass from the control desk. Give pavilion_presentation_service_authorization; set pavilion_finale_service_access = true. Continue ch3_finale_technical_staging.
2. **C3-B — "REMOVE THE DIAGNOSTIC STRIP BEFORE IT IS OVERWRITTEN."** rc03_diag_record: take printed diagnostic strip linked to Original's ID, distinct from approved speech reel. Give pavilion_representation_diagnostic_record; set pavilion_original_diagnostic_obtained = true and ch3_original_independent_response_seen = true (provided the text shows the authentic original-ID trace). Continue staging.
3. **C3-C — "COPY THE PRESENTATION OVERRIDE SEQUENCE."** rc03_override: collect physical patching instructions listing registered broadcast channels. Give pavilion_broadcast_override_sequence; set pavilion_broadcast_route_prepared = true. This is preparation, NOT execution of broadcast or guaranteed success. Continue staging.

No mandatory check to reach the finale from C.

### C item economy

RC01/RC02 award flags, RC03 gives exactly one of:
- pavilion_presentation_service_authorization
- pavilion_representation_diagnostic_record
- pavilion_broadcast_override_sequence

Never require any inherited tool to obtain an RC03 choice; using tools may improve the optional marked C2 disconnection and later finale attempts.

## Finale staging / first encounter normalization

Three forward staging nodes:
- ch3_finale_admin_staging
- ch3_finale_records_staging
- ch3_finale_technical_staging

All lead exactly once to ch3_grand_reconciliation, and none resets inventory/notes or changes ch3_primary_route.

- Admin: clerk demands proof of identity; claimant produces evidence or is labeled unverified. The door opens anyway as a mandatory hearing.
- Records: the two serial-number identities are entered into the hearing docket. If B3-B permit is held, the permit is marked already-used but **remains held**.
- Technical: protagonist observes presentation cabling or chamber equipment before being escorted to the claimant platform. If an independent diagnostic was preserved, record that it is properly indexed.

At finale:
- If Original Witness previously encountered in A, narrate recognition and variant based on fitting suspension/interruption. Do not silently "repair" or complete an interrupted Original; use a mobile sealed witness enclosure or a remote platform where needed.
- If Original never previously encountered (normal B/C), introduce it as a partly screened certified representation, with face always concealed.
- If Original already produced a verified unauthorized response, mention it; otherwise a short observed movement may supply a *new clue* but must not retroactively award earlier independent-evidence flag before the player decides its finale action.
- Original's decision to leave must be internally authored and consented, not simply an item-gated activation.

### Basic ending paths

Grand Reconciliation three displayed choices:
(1) contest identity -> personally released on success or one-time denial disposition;
(2) alter registration -> committed quiet unregister vs broadcast -> success or one-time alarm disposition;
(3) ask Original to claim separate identity -> two persons depart on successful recognition and its voluntary choice, else Original retained + one-time claimant disposition.

The universal non-item, no-luck identity-surrender fallback to NO PERSON PRESENT remains **provisional, not owner-locked**. Do not claim full mathematical survivability until a deterministic route is approved. It must not be an accidental suicide or physically dangerous "waste chute"; it is a secure outbound transfer with deep identity cost.

## Cross-route transitions and major route scope

Some Route A leaves transfer one-way to a technical or records scene, as inventoried in docs/94. Their primary-route flag remains A; they can earn B/C principal reward when crossing, but cannot return to the A choices.

A route that arrives at RC02 by transfer skips RC01 and its earlier flags. A route entering RB02 similarly skips RB01. All later nodes must be independently comprehensible.

Preexisting Chapter 2 flags: chapter3_entry_group (public_concourse, service_infrastructure, underground_transit), equipment_registered, tram_satisfaction_certified, spore_infected, thorn_infected and carried/cured items remain valid. A biological infection can affect identity-verification dialogue; it is NOT automatic extra-person identity status.

## Graph coverage and acceptance review

**Structural evidence here:** 6 shared incidents with 18 authored choice-result edges, plus one optional d6 split on RC02-B. All results lead to later incidents or finale staging. All three B3 and three C3 rewards are mutually exclusive within their direct branches. No branch loops, no backtracking. This is only a design graph, **not** a playwright JSON schema validator or a gameplay test.

**Remaining work:** Close Route A leaves (docs/94), author finale fallback and fatal choices, confirm owner rulings, write full narrative prose for B/C then all endings, audit item exchanges and state read conditions, generate Chapter 3 JSON and artwork registry, then route/game QA under ChatGPT Gameplay PMO and Claude.

**No code, merge, production art, or deployment is authorized by this document.**
