# Out of Order — Chapter 5 continuity and concept review
Date: 2026-11-25. Status: continuity findings; three UNAPPROVED creative proposals awaiting Nate's selection.
Source: storyboard main 5a4290d672e1904b4b5ad361562f05168c328a50; game main c7a2d3dc7e19b8d574deedec0e5b4b7098daa9a1.
This planning branch does not alter Chapter 4, the public selector, art records, or playable content.

## Authority and verified continuity
Read actual story/chapters/chapter-04.wip.json, active Prologue–Chapter 3 source, story/items.draft.json, manifest, docs/123–126, and game docs/104.
Chapter 4's canonical title is Something Old, Something Sold. The current JSON and final closeout supersede the older working narrative's wedding-search and groom-escort branches.
Independent structural scan: 120 nodes, 120 graph-reachable when counting conditional edges, zero missing targets, eight authored checks, four fatal and three nonfatal ends. This is graph verification, not exhaustive state/runtime validation.

| Ending node | ch4_exit_route | Physical handoff |
| --- | --- | --- |
| hotel_service_park_exit | service_loading_dock | Service passage, loading dock, pedestrian side gate; across courtyard toward public park |
| hotel_bridal_corridor_park_exit | bridal_corridor_departure | Bridal corridor, hotel lobby, outside across courtyard toward public park |
| hotel_bridal_lavatory_park_exit | bridal_lavatory_departure | Leaves seashell room, removes gown in dressing room, exits hotel toward public park |

All three set ch4_exit_park_approached=true. All preserve surviving inventory and flags, including any pending bridal fee. No route arrives wearing the gown. They do not establish separate park entrances. Opening should recognize the exit route briefly and then converge without erasing state.

Four fatal nodes are terminal: fatal_stall_final_occupancy, fatal_boiler_pressed_and_steamed, fatal_lot61_folded, fatal_bridal_made_to_measure. No Chapter 5 continuation from those states.

## Inventory and relationships
Chapter 4 awards only lot_53_dispute_ticket and wedding_ring_lot31. Ticket persists; showing it does not consume it. Ring is acquired at the chair or collection, and explicitly handing it to the bride removes it. Current groom SHOW retains it; older groom handover/escort documentation is superseded.
Rubber-band ball is consumed if traded to Bixby (ch4_bixby_fender_trade). The recovered plumbing wheel, blue delivery ledger, Lot 14 receipt, seashells, gown, and organizer's access key are not newly awarded inventory. wc_key is the earlier Facilities Key and is not consumed at the hotel.
Potential earlier carried items must be gated by actual possession: notice, claim ticket, timing clicker, desk plant, stapler, rubber-band ball, examiner badge, Facilities Key, family photograph, vegetation credential, seed canister, unused route-specific antidote.
Prologue intake may store/donate belongings or permit only a selected one; House storage may not be recovered; plant residency consumes the plant. Chapter 2 may consume stapler, clicker, ball, seed canister or antidote; Chapter 3's printer sabotage consumes the stapler. Never restore them.
The active Chapter 3 reboot awards no new carried item. Temporary Staff Pass and many retired identity documents remain catalog entries without acquisition in the active story. Do not design an ordinary Chapter 5 route around obtaining these; Chapter 4's staff-pass cards are a pre-existing integration issue.
Relationships: preserve ch4_bride_ally, ch4_bride_service_permission, ch4_knows_blue_delivery_ledger, ch4_groom_located, ch4_groom_saw_ring, ch4_groom_left_behind, ch4_plumber_helped and Bixby's expectations when set. None creates an obligation to reunite the wedding party.
Preserve ch4_bridal_registration_fee_pending and provisional bride state; ring ownership/inscription; witnessed recovery and upholstery damage; NOT INCLUDED tag; flood/water shutdown; crane/pod/AutoFit survival. Preserve earlier spore_infected/thorn_infected, consumed treatment, House equipment/residency, prior exit flags and any tram liability. Hotel water shutoff does not establish park water shutoff.
The historical note mentions ch4_exit_frustrated; the current three terminal nodes do not write it. Dispatch by the actual ch4_exit_route values.
Chapter 3→4 wiring remains deferred in game docs/104; do not repair it as Chapter 5 story work.

## Prior park seed and scope
docs/124 fixes the Chapter 4 destination as a nearby public park. It parks an UNAPPROVED Chapter 5 idea: singed small wildlife near concealed security shrubs, a dubious company sponsoring a real restroom, possible fatal misuse of a shrub. It approves no Chapter 5 scenes, odds, sponsor, or gameplay.
Nate's new Chapter 5 mandate authorizes concept development now and supersedes that note's old instruction to finish Chapter 4 first.
All proposals below preserve the park arrival. A develops the parked seed. B and C are alternatives for Nate's ruling, not silent replacement canon.

## A — A Little Privacy (recommended)
Location: real municipal park with a newly sponsored security installation.
Arrival: all three hotel departures reach the park; conditional first line preserves experience.
Bathroom problem: an existing restroom has been fenced into the sponsor's demonstration; the guard has lost the remote that switches the perimeter off.
Characters: pleasant security representative proud of low crime; practical park keeper who knows the dangerous shrubs by their serial numbers.
Central incident: concealed devices mistake ordinary park life for incursions, funneling visitors toward the only safe location, the restroom, while excluding the protagonist outside the perimeter.
Existing items: surviving desk plant can test plant recognition; rubber-band ball can divert motion tracking; timing clicker can aid timing a sweep. Credential can obtain a supervised demonstration without magically granting control.
New item candidate: removable maintenance bypass plug with possible later electrical use; consequences of removal must matter.
Checks: crossing a scanner sweep, recovering remote from a mechanical grounds vehicle; no probabilities selected.
Death candidates: urinating on an electrified false shrub after discoverable singed-wildlife clues; lethal pruning of an intruder. No authored deaths or art prompts yet.
Exit candidates: park keeper's culvert; outbound service vehicle; being expelled through a perimeter gate after disabling the demonstration.
Identity: outdoor stealth, improvisation and escalating physical danger. Short, self-contained; no investigation into corporate conspiracy.

## B — In the Event of an Emergency
Location: park lake and bandstand hosting a civic disaster rehearsal.
Arrival: player crosses the park seeking the ordinary lakeside restroom.
Bathroom problem: restroom stands inside a staged flood zone. A rescuer insists on evacuation before the player can enter.
Characters: exhausted rescue captain; performer employed as the official drowning man, who objects to anyone else taking his place.
Central incident: the scheduled mock flood arrives as real water. Personnel keep following the rehearsal while the player is assigned increasingly unsuitable rescue roles.
Items: rubber band may repair an inflatable; stapler can fasten a flotation strap at risk; timing clicker helps cross a timed sluice. Seeds are not assumed to grow instantly.
New item candidate: rescue throw-line, useful for reaching a boat or later chapters; sacrificing it must be explicit.
Checks: reaching a drifting pontoon or boarding a boat; failed nonfatal outcomes can strand player with the drowning performer.
Death candidates: powerful evacuation suction; trusting a display-only flotation device with a readable warning.
Exits: rescue launch to a canal district; storm drain onto a towpath; evacuation bus beyond the Expo.
Identity: wet physical farce, cooperation and rescue logistics, rather than another biological park or access-verification process.
This replaces the parked security-shrub concept only if Nate selects it.

## C — Request Stop
Location: park-edge transport stop and a municipal vehicle travelling beyond the Expo.
Arrival: player walks through the same park and notices a lavatory sign on a waiting coach.
Bathroom problem: door closes and the coach departs before the player reaches its onboard toilet; the vehicle couples into a longer convoy, leaving the toilet in another section.
Characters: unflappable driver; refreshments attendant running a lavish service for one passenger; a commuter who recognizes every landmark but cannot remember getting off.
Central incident: reaching the toilet means moving between vehicle sections as the convoy divides for different destinations. Player can cooperate with staff, attempt a crossing, or force an unscheduled stop.
Items: timing clicker helps time a crossing; stapler can secure a loose bell wire; Facilities Key can be tried on a service cupboard with a locally authored result, not universal access.
New item candidate: detachable conductor's bell handle, with practical signal/mechanical uses later; taking it alters the ability to request a stop.
Checks: crossing the coupling or retrieving something through a roof hatch. No odds selected.
Death candidates: standing in the automatic decoupling vestibule; exiting through a road-level baggage hatch at speed, with fair warning.
Exits: unscheduled roadside stop; freight depot after wrong-section detachment; river terminal after driver assistance.
Identity: confined ensemble comedy and movement through the wider world, with permanently changing locations.
This replaces the parked security-shrub concept only if Nate selects it.

## Recommendation and next step
Recommend A: strongest existing continuity, outdoor physical play, earlier-item opportunities, and a readily understandable hazard. Keep restroom access short; do not create another permit ladder. Avoid repeating Biology Park: shrubs are disguised hardware, real park is ordinary, and no planting/reclassification arc is needed.
A/B/C here are editorial concept selections, not player choice cards. Await Nate's ruling before authoring the opening. Keep all three in design history; selection does not delete alternatives.
Narrative, artwork, production assets, and engine integration remain unapproved/unstarted for Chapter 5.
