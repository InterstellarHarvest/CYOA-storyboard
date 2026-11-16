# CH3 — Route A Closure and Grand Reconciliation Failure Rules

**Status:** story-design specification, pending owner approval. No playable JSON or game integration.
**Date:** 2026-11-16. Companion documents: 94 route/ending audit and 95 Routes B/C structural authoring.
**Owner-locked:** Original Witness may escape independently and may return later; never mandatory companion; no protagonist face reveal. CYOA advances, no backtracking or repeated question banks.
**Unapproved proposal:** guaranteed voluntary identity surrender as a survivable fallback, detailed at end. This is not canon until approved.

## Core graph

Entry groups public_concourse, service_infrastructure, underground_transit -> CH3-001A/B/C -> CH3-002 Attendance -> A Human Requirements (CH3-003), B Visitor Records (RB01), or C Exhibit Operations (RC01).

Route A is a *family of paths*, not a compulsory twenty-room chain. Players can take a **short path** via plumbing or demonstrator registration to finale staging, or a **deep path** through certificate, Original, photographic archives and the Fourth Chair. Preserve ch3_primary_route=A when entering an RB/RC scene by one-way transfer.

Every authored Route A leaf below must reach:
- ch3_finale_admin_staging, ch3_finale_records_staging or ch3_finale_technical_staging;
- one of the established RB02/RB03/RC01/RC02/RC03 scenes (forward-only); or
- a clearly marked, explicitly voluntary high-risk fatal branch.

Staging scenes converge on ch3_grand_reconciliation and never reset inventory, chapter flags or NOTES. A previous failed dice check cannot be tried again simply by changing rooms.

## A0: CH3-003 Human Requirements

A lift barrier -> CH3-004A (existing Satisfaction Demonstration).
B follow utility pipe -> CH3-004B (new Plumbing).
C register as human demonstrator -> CH3-004C (new Demonstrator Registration).

### CH3-004B Plumbing

Narrative B: real water supply reaches a working display fixture, but a secured backflow valve separates it from visitor use. Inspection plate: HUMAN REQUIREMENTS — ALREADY SATISFIED. A staff washroom is glimpsed but not accessible. Three one-time choices:
- FOLLOW THE WATER SUPPLY TO ITS MAINTENANCE MANIFOLD: set pavilion_restroom_service_line_seen; go RC01.
- REQUEST AN ACTUAL FLOW-METER READING: meter prints OPERATING / CONSUMPTION NOT REQUIRED; set pavilion_usage_vs_record_discrepancy; go records staging. This is not by itself legal identity proof.
- FILE AN EMERGENCY PLUMBING INSPECTION: set pavilion_public_maintenance_claim; go technical staging. If expo_examiner_badge or acting_director_badge is held, variant official phrasing, never required.

No dice. These are deterministic observations, not risky mechanical interference. No bathroom use.

### CH3-004C Demonstrator Registration

Real-live-participant booth offers a family comfort demonstration; "REAL HUMAN PARTICIPATION OPTIONAL". Working toilet is secured behind demonstration glass, and preissued completion record awaits.
- REGISTER AS LIVE EXAMPLE, RESERVING YOUR NAME: set pavilion_claimant_live_status_asserted, pavilion_live_demo_reservation; go admin staging. Explicitly NOT accepting a replacement.
- REQUEST DEMONSTRATOR SERVICE EXIT: set pavilion_demonstrator_exit_referral; go RC01. Backstage, not bathroom.
- REFUSE DEMONSTRATION AND REQUEST ATTENDANCE REVIEW: set pavilion_participation_refused; go RB02.
No check, no automatic proof or cure.

## A1: CH3-004A Satisfaction Demonstration (existing)

A press button -> CH3-005A; give certificate_fulfilled_requirements.
B refuse scripted reply -> CH3-005B (new Records Review).
C force curtain release with hidden d6 >=4, rubber_band_ball +1; success CH3-005C (new Backstage Facility); failure CH3-005D, shared correction. Both outcomes survive.

### CH3-005B Records Review

The refusal is partly anticipated; an unapproved silence appears on a reel, but this is *the player's* behavior, NOT proof the Original has independent agency.
- PRESERVE THE AUDIO/TEXT MISMATCH: set pavilion_unscripted_testimony_preserved; go CH3-008A (witness standards accepts an initial archived complaint).
- TRACE WHO ISSUED THE APPROVED SCRIPT: set pavilion_script_workorder_found; go RB02.
- REQUEST FORMAL TRANSCRIPT REVIEW: set pavilion_disputed_transcript_accepted; go records staging.
Never set ch3_original_independent_response_seen merely because player refused a script.

### CH3-005C Backstage Facility

After curtain release, toilet fixture physically rolls away on display platform, revealing a service walkway. Existing pavilion_facility_breach remains true.
- FOLLOW THE ROLLING FIXTURE'S SERVICE RAIL: set pavilion_prop_transport_seen; go RC01.
- FILE THE FUNCTIONING-BUT-UNAVAILABLE FACILITY AS EVIDENCE: set pavilion_facility_real_but_unavailable; go admin staging.
- TAKE EXPOSED MAINTENANCE ACCESS: set pavilion_service_exit_found; go technical staging.
No second dice check for access that was already opened.

### Shared ch3_shared_correction

Used by CH3-005D (frustration), CH3-008B2 (witness partition failure), CH3-009E (image process failure). Entry-cause-specific narration; earlier flags and any official summons persist. Machine insists that player behavior or images require adjustment.
- ACCEPT A SUPERVISED CORRECTION REPORT: set pavilion_corrective_observation_requested; go admin staging.
- FOLLOW CORRECTION CONTROL CABLES: set pavilion_correction_controls_traced; go RC02.
- CHALLENGE THE CORRECTION OFFICE'S JURISDICTION: set pavilion_correction_jurisdiction_challenged; go records staging.
No reroll of failed earlier checks and no automatic physical alteration. A distinct source choice can still have future consequences.

## A2: CH3-005A Satisfaction Records (existing)

A submit certificate for correction -> CH3-006A Reconciliation; TAKE certificate_fulfilled_requirements, GIVE pavilion_discrepancy_receipt.
B inspect preprinted original -> CH3-006B.
C temporary staff route -> CH3-006C with pavilion_temporary_staff_pass.

### CH3-006B Original Records

File shows previous morning, fabricated or planned future and REPLACEMENT PARTICIPANT READY. If House photo held, HOUSEHOLD H-04 cross-reference appears; no forced surrender.
- PROVE A FORECAST WAS A WORK ORDER: set pavilion_forecast_is_workorder_evidence; go RB02.
- KEEP REPLACEMENT PREPARATION AS OFFICIAL EVIDENCE: set pavilion_replacement_preparation_documented and ch3_separate_identity_evidence (the file displays certified Original registration plus distinct claimant); go records staging. Evidence resides in NOTES/flags, not another ticket.
- FOLLOW THE ORIGINAL REGISTRATION NUMBER: set pavilion_original_registry_number_seen; go CH3-007A Witness. Guard uses file provenance for access; do NOT invent a pre-owned Appearance Order.

### CH3-006C Staff Services

Staff-only washroom remains locked because outstanding personal needs are reclassified as job duties; no successful bathroom use.
- USE TEMPORARY PASS FOR TECHNICAL SERVICE INSPECTION: set pavilion_staff_service_used; go RC01.
- FILE CONFLICT BETWEEN EXISTING EMPLOYMENT AND PAVILION CLAIM: set pavilion_employment_status_disputed; if equipment_registered also pavilion_employment_disputed; go admin staging.
- FOLLOW STAFF ATTENDANCE LOGS: set pavilion_staff_attendance_access; go RB02.
No dice. Temporary pass is held if originally gained, not cloned.

## A3: CH3-006A Reconciliation Office (existing)

A demand Original -> CH3-007A. TAKE pavilion_discrepancy_receipt, GIVE pavilion_original_appearance_order.
B demand physical life test -> CH3-007B. TAKE receipt, GIVE pavilion_proof_of_life.
C accept duplicate -> CH3-007C. TAKE receipt, GIVE pavilion_duplicate_routing_tag.

### CH3-007B Evidence of Life

Pulse and body heat verified; identity is not. If spore_infected or thorn_infected, a MULTIPLE ORGANISM STATUS warning is conditional *infection evidence*, not an automatic second sentient claimant or death.
- SUBMIT PROOF WITH DISTINCT ORIGINAL REGISTRATION: set pavilion_life_evidence_filed and ch3_separate_identity_evidence after both numbers explicitly compared; go admin staging.
- COMPARE LIFE TEST TO ORIGINAL'S RECORD: set pavilion_life_registry_comparison and ch3_separate_identity_evidence; go records staging.
- DECLINE ANY FURTHER BIOLOGICAL SAMPLE: set pavilion_biological_sample_refused; go admin staging.
Keep Proof of Life item. No check for receiving an already administered result.

### CH3-007C Surplus Department

Warehouse of labeled belongings, staged voices, discarded official persons. Duplicate tag held. House equipment ownership dispute shown if relevant.
- FOLLOW SURPLUS PROPERTY TRANSFER: set pavilion_surplus_property_route_seen; go technical staging.
- REQUEST REVIEW OF DUPLICATE TAG: set pavilion_surplus_duplicate_challenged; go admin staging.
- INSPECT RETENTION ENTRY WITHOUT ENTERING IT: set pavilion_retention_architecture_seen; go RC02. This safe inspection must not secretly lead to a fatal chute.
No compulsory death for duplicate status.

## A4: CH3-007A Original Witness (existing)

A test unscripted bathroom knowledge -> CH3-008A.
B release partition, d6 >=4 (+1 timing_clicker), pass CH3-008B1, fail CH3-008B2 -> shared correction.
C demand official photograph -> CH3-008C Image Standards.

### CH3-008A Witness Standards

Witness said "Because you have not found one" outside approved script; official incident report confirms Original uttered it. Set ch3_original_independent_response_seen=true, not a claim of biological identity.
- SUBMIT THE ORIGINAL'S UNSCRIPTED ANSWER: set pavilion_original_testimony_preserved; go admin staging.
- TRACE ITS SPEECH FEED: set pavilion_original_speech_trace_requested; go RC02.
- REQUEST THE ORIGINAL AT A FORMAL IDENTITY HEARING: set pavilion_witness_hearing_requested; go records staging.
If accessed from CH3-005B without prior witness encounter, play introductory comparison that obtains and verifies Original-specific recorded anomaly; never assume player knows Original.

### CH3-008B1 Technical Adjustments

Partition success exposed positioning machinery, fleeting non-face arm, CLAIMANT FINAL FITTING notice; exact physical nature unresolved.
- PRESERVE CLAIMANT FITTING ORDER NUMBER: set pavilion_claimant_fitting_number_seen; go records staging.
- FOLLOW MOVING REPRESENTATION PLATFORM: set pavilion_platform_transfer_seen; go RC02.
- REQUEST LOCAL SERVICE RAIL SHUTDOWN: set pavilion_local_prep_shutdown_requested; go technical staging. Does not falsely suspend Original's separate fitting unit.
CH3-008B2 is a shared correction entry (previous failed check), not a second new office chain.

## A5: CH3-008C Image Standards (existing)

A examine negatives -> CH3-009A.
B with family_portrait_photo -> CH3-009B (The Fourth Chair).
B without photo -> CH3-009C (Photographic Correction).
C interrupt photo registration, d6 >=4 (+1 appropriate nonstacking tool); success CH3-009D, fail CH3-009E -> shared correction.

### CH3-009A Source Registration

Original raw negatives show genuinely empty chairs. Visitor names assigned after exposure; if family photo held, optional linked House archive index appears.
- TRACE WHO CERTIFIED THE SUBJECT: set pavilion_source_assignment_trace and ch3_separate_identity_evidence after displaying distinct Original/claimant registration numbers; go records staging.
- CONTRAST RAW NEGATIVE WITH PHYSICAL OCCUPANCY: set pavilion_raw_image_not_presence; go admin staging.
- FOLLOW IMAGE REGISTRATION TRANSMISSION: set pavilion_image_registration_route_seen; go RC03.
No need to have the House photo.

### CH3-009C Photographic Correction (no House photo)

Actual claimant sat for a photo; approved image shows empty stool with appearance-order number. pavilion_empty_claimant_photo was awarded in CH3-008C B-no-photo and is retained.
- PRESERVE THE EMPTY PHOTO AS EVIDENCE: set pavilion_empty_photo_preserved and ch3_separate_identity_evidence after crosschecking distinct certified Original; go admin staging.
- TRACE THE PROCESSOR REMOVING CLAIMANT IMAGE: set pavilion_claimant_image_exclusion_traced; go RC03.
- ASK FOR CONTRADICTORY RECORD RULING: set pavilion_absence_dispute_filed; go records staging.
No missing-photo hard gate or check.

### CH3-009D Image Production (process interruption success)

Unapproved photograph depicts parts of two figures but no face and proves no specific biological/robotic nature. pavilion_unapproved_exposure held.
- AUTHENTICATE EXPOSURE SOURCE NUMBER: set pavilion_unapproved_exposure_authenticated; go records staging.
- TRACE SERVICE PATCH CABLES: set pavilion_exposure_service_cable_seen; go RC03.
- REPORT SAFETY EXCEPTION: set pavilion_unsafe_source_production_reported; go admin staging.
CH3-009E uses shared correction with image-interference variant, no forced confiscation.

## A6: CH3-009B The Fourth Chair (already full draft)

A source conflict hold -> CH3-010A.
B household routing strip -> CH3-010B.
C jam live fitting d6 >=4 (+1 one suitable tool), success CH3-010C1, failure CH3-010C2. This initial failure does NOT kill player.

### CH3-010A Custody of Originals

Previous source hold remains active; pavilion_original_fitting_suspended must persist and finale cannot pretend fitting is complete.
- CLAIM SEPARATE LEGAL STATUS OF SOURCE AND REPRESENTATION: set pavilion_source_identity_separation_claim and ch3_separate_identity_evidence; go admin staging.
- DEMAND ORIGINAL'S TESTIMONY ABOUT SOURCE HOLD: set pavilion_original_custody_hearing_requested; go records staging. Original still decides its own request at finale.
- INSPECT SOURCE OWNERSHIP CONTRACT: set pavilion_source_contract_seen; go RB03 if transfer is narratively motivated, otherwise records staging. No earlier RB01/02 flags fabricated.

### CH3-010B Household Routing

Three registered empty-seat positions: Domestic Demonstrations, Participant Preparation, P.R. Retention. No assertion that a real family is alive/trapped based on routing alone. Original fitting continues.
- PRESERVE HOUSEHOLD ROUTING STRIP: set pavilion_household_records_preserved; go records staging. Keep strip.
- FOLLOW RETENTION ROUTE FROM OUTSIDE SEALED CHUTE: set pavilion_household_retention_routed; go technical staging.
- REQUEST FAMILY-PARTICIPATION AUDIT: set pavilion_household_attendance_disputed; go admin staging.
Keep original family photo and source receipt.

### CH3-010C1 Representation Repair

Successful earlier fitting interruption leaves Original unfinished with certification blocked. A sealed movable witness enclosure and voice feed can still reach the finale; don't silently restore complete fitting.
- PRESERVE TRACE OF ORIGINAL MOVEMENT WITHOUT CUE: set pavilion_original_repair_diagnostic_preserved and ch3_original_independent_response_seen if diagnosis conclusively tags Original's ID; go technical staging.
- DEMAND A WITNESS HEARING BEFORE REPAIR: set pavilion_original_repair_hearing_requested; go admin staging.
- FOLLOW SEALED TRANSFER SERVICE ROUTE: set pavilion_original_repair_route_seen; go RC03, without exposing Original's face.

### CH3-010C2 Live Source Calibration

The earlier fitting check failed; player identified as live reference material, **not** automatically restrained, transformed or killed. Present safe alternatives.
- REFUSE CALIBRATION, REQUEST SAFETY TRANSFER: set pavilion_calibration_refused and pavilion_calibration_deferred; go admin staging.
- FOLLOW CONTROL CABLING WHILE STAYING OFF PLATFORM: set pavilion_calibration_controls_seen; go technical staging.
- PULL OCCUPIED FITTING FRAME EMERGENCY RELEASE: explicitly **high-risk marked** check d6>=4 (+1 one suitable stapler/clicker); on success set pavilion_live_fitting_release_success and pavilion_original_fitting_interrupted then technical staging; on failure proposed fatal SUCCESSFULLY RECONCILED, when machine physically absorbs claimant as reference material. This fatal mechanism is *provisional pending owner confirmation*. Do not hide risk behind innocuous card text.

## Grand Reconciliation — precise proposed forward rules

All three finale staging nodes -> ch3_grand_reconciliation. Existing introductory scene has one certified Original, one physically present claimant. Conditional prose for Original previously met, first met, fitting suspended, fitting interrupted. A sealed mobile enclosure is used if fitting previously interrupted; no player face. Registered count: ORIGINALS=1, CLAIMANTS=1, not contradictory "1 person present" when two bodies are implied.

The first screen fits THREE choice cards; a fourth ending is reached by a committed subchoice:
1. **CONTEST CERTIFICATION OF THE ORIGINAL** -> admin exception check d6>=4, +1 valid documentary evidence (nonstacking). Success PERSONALLY RELEASED. Failure ch3_final_disposition, no retry.
2. **INTERFERE WITH THE PERSON REGISTRY** -> ch3_registry_commit, choose one:
  - REMOVE ONLY PAVILION CLAIMANT RECORD: d6>=4, +1 tech access/tool (nonstacking). Success NO PERSON PRESENT with identity_scope=pavilion_only; failure ch3_final_disposition.
  - BROADCAST THE TWO INCOMPATIBLE CERTIFICATIONS: d6>=4, +1 network access/sequence (nonstacking). Success UNAPPROVED BROADCAST, Original status unknown; failure ch3_final_disposition.
3. **ASK THE ORIGINAL TO DECLARE AN INDEPENDENT IDENTITY** -> Original must voluntarily assert preference (not controlled like a tool); Registrar check d6>=5, +1 Original verified unscripted response, +1 independent source proof (max +2). Success TWO PERSONS DEPART with Original exiting separately, may return later; failure original retained, claimant enters ch3_final_disposition, no reroll.

Only independent evidence of the ORIGINAL (not generic demonstration, not player refusal) earns ch3_original_independent_response_seen. Separate legal source evidence earns ch3_separate_identity_evidence. The two flags do not prove biological humanity.

### ch3_final_disposition — after any unsuccessful method

Different decision from earlier failed check, not a retry bank:
- **SURRENDER ALL EXPOSITION IDENTITY CLAIMS TO ACCEPT SAFE UNREGISTERED TRANSFER:** PROPOSED guaranteed no-roll survival (identity_scope=exposition_wide). Output NO PERSON PRESENT. An outbound material/service corridor safely transfers the living protagonist, not an incinerator/archival machine. Severe long-term identity consequences in Chapter 4. **NOT OWNER-LOCKED.**
- **FORCE AN EMERGENCY OPENING IN THE RETENTION TRANSFER ASSEMBLY:** explicitly hazard-marked d6>=4, +1 one suitable physical tool (nonstacking). Success breaks local registry hold and exits as NO PERSON PRESENT with scope pavilion_only; failure PROPOSED fatal PERMANENTLY ARCHIVED, physically trapped as source material. **NOT OWNER-LOCKED.**
The player is never required to pick the dangerous action if deterministic identity surrender is approved. Failed paperwork never directly kills.

### Ending persistence

PERSONALLY RELEASED: ch3_exit_route=administrative_exception, ch3_original_status=retained.
NO PERSON PRESENT, limited quiet technical removal: ch3_exit_route=unregistered, ch3_identity_unregistered=true, ch3_identity_scope=pavilion_only, Original retained.
NO PERSON PRESENT, voluntary full surrender: same route/unregistered, scope=exposition_wide, Original retained.
TWO PERSONS DEPART: ch3_exit_route=two_persons_depart, ch3_original_status=escaped_independently, ch3_original_independent_identity=true; Original and protagonist separate exits, no companion.
UNAPPROVED BROADCAST: ch3_exit_route=broadcast_disruption, ch3_original_status=unknown, ch3_pavilion_disrupted=true.
FATAL SUCCESSFULLY RECONCILED and PERMANENTLY ARCHIVED: explicit end nodes, no Chapter 4 transfer, no protagonist face.

Original stage flags like pavilion_original_fitting_suspended or pavilion_original_certification_blocked are NOT overridden by finale staging. A special ch3_original_condition may be derived as standard / suspended / interrupted / in_progress to select an appropriate presentation; independent from terminal ch3_original_status.

## Item and action consistency

Earlier CH3-005A A replaces Satisfaction Certificate with Discrepancy Receipt. CH3-006A A/B/C consumes that receipt, awards *one* of Appearance Order, Proof of Life or Duplicate Tag. CH3-009B retains family_portrait_photo after scanning and adds Source Contribution Receipt only on chosen path; Household Routing Strip acquired on chosen followup. Other route-specific papers can be recorded as persistent FLAGS/NOTES rather than filling inventory. Seven is *visible* slots with scroll arrows, not a universal carry cap.

Tool bonuses: curtain in CH3-004A rubber_band_ball +1; witness partition in CH3-007A timing_clicker +1; image processor in CH3-008C one relevant tool +1; fitting in CH3-009B one tool +1; high-risk physical transfer one tool +1. Nonstacking unless separately authored. Tool availability determined by actual retained inventory. No forced item sacrifice.

spore_infected/thorn_infected only affect Verification text and possible identity ambiguity, never instant death. equipment_registered may trigger prior House ownership claim but is not automatic transfer of the claimant. tram_satisfaction_certified can add recognized-satisfaction dialogue without pre-clearing all Chapter 3 claims.

Every nonfatal ending leaves bathroom need unresolved. A route-specific exit gag can be brief and bureaucratically relevant; avoid replaying an identical blocked-toilet exchange four times.

## Design QA requirements and honest limits

Proposed missing Route A bridge nodes closed here: CH3-004B/C, 005B/C/D, 006B/C, 007B/C, 008A/B1/B2, 009A/C/D/E, 010A/B/C1/C2. These should be mapped as executable nodes/conditional outcomes only after owner confirms fatal and safe fallback rules. Some shared correction incidents can be consolidated to avoid scene/art bloat. Route A deep investigation optional; two short routes reach staging without Original/photo.

This document is an **authored structural specification, not tested Chapter 3 playable content**. No Chapter 3 story JSON, route validator results, browser QA, new art approval, or transition engine implementation is implied.

### Decisions not yet locked

1. Whether to adopt deterministic identity surrender (full Exposition identity loss) as safe fallback; or replace with another guarantee.
2. Whether to use three initial finale options, registry choice nested to keep UI geometry.
3. Whether to approve two high-risk fatal concepts as specified, or choose less punitive outcomes.
4. If accepted, write full Route A concise bridges / full Route B-C narrative, complete end scenes, then story JSON and artwork registry. Gameplay PMO remains owner of coordinating Claude implementation, not this creative document.
