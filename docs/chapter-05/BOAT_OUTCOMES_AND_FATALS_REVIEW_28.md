# Chapter 5 — boat outcomes and fatal presentations review 28
## Owner approval
Nate's "ok" accepts review 27 as corrected: bird lands on bow once afloat, camera deploys and declares intruder, stubborn bird stays through decision; choice mechanics retained.
Steering d6 need 4: raw 4–6 survives/crosses, 1–3 fatal craft attack on own bow.
Cloth camera covering deterministic crossing if actually possessed, cloth recovered at dock.
Swim d6 need 5: raw 5–6 clears trailing net and crosses, 1–4 caught and drowned.
No wake-target mechanism, lakeside workers, supply boat or bridge. Long-way route separately diverges and abandons this lake objective.
Exact prose, death titles and aftermath concepts below remain proposed for owner review; no images generated.

## A steer success — proposed
You grip the wheel with both hands and force it towards the boathouse.
For a moment, it fights you.
Then the bow swings towards the far shore.
Boat: PLEASE DO NOT INTERFERE WITH INTERCEPTION.
The bird watches the approaching landing.
You bring the boat alongside, scramble ashore and run up the bank.
Without your hands on the wheel, the boat turns back towards open water.
Behind you, a sharp report echoes across the lake.
The bird flaps past and lands on the boathouse roof.
You reach the door on foot.
Proposed state ch5_lake_crossing=manual; ch5_boat_countermeasure_fired=true; no wetness set or cleared, no item loss. No extra shore blast roll. Mechanically crossing succeeded and gets player safely out of blast area before firing.

## A steer failure — proposed
The wheel jerks against your hands.
You pull harder.
It turns back.
Boat: INTRUDER REMAINS ABOARD.
A round metal charge rolls into the launching cradle.
The mechanism swivels towards the bow.
Towards the bird.
Towards the boat.
Player: DON'T—
The charge drops onto the foredeck.
The bird finally leaves.
You don't.

Proposed fatal node fatal_ch5_clear_the_deck; end:true; no outgoing chapter transition.
Proposed title CLEAR THE DECK.
Proposed popup: The intruder has been successfully repelled. The demonstration craft is no longer accepting passengers.
Trigger failed manual-steering roll raw1–3 only. No secondary escape window, item rescue or retry within same run. Earlier route state unchanged on terminal result.
Future aftermath concept: damaged small demonstration boat sitting low in lake, blasted foredeck, bird safely on distant landing/boathouse roof; no visible player face/body/gore. Reference actual boat/lake layout from future approved assets.
Future prompt draft: Match approved Chapter 5 security leisure boat and lake; aftermath of craft firing at its own foredeck, broken bow and low hull in water, distant intact timber boathouse with small unharmed bird, absurd security demonstration disaster, no people, face, gore, text or UI. Verify exact death-art dimensions at production handoff. No art generated.

## B cloth — proposed
You pull the yellow cloth over the camera.
Boat: INTRUDER—
The camera turns beneath the fabric.
Boat: VISUAL CONTACT LOST.
The wheel stops fighting you.
You steer towards the boathouse.
The bird stays exactly where it is.
At the landing, you step ashore and pull the cloth free.
Boat: INTRUDER DETECTED.
You leave it arguing with the bird and hurry up the bank.

Proposed state ch5_lake_crossing=cloth; cloth remains in inventory after explicitly recovered at dock; no duplicate or consumption. No roll. Item action only available on actual possession. Camera covered for trip; no permanent power cut or assertion learning resets. Target reacquisition happens after player safely ashore; no surprise extra roll. Can show boat turning away onto lake before later incident if needed for consistent spatial safety, don't add lethal loss to guaranteed result.

## C swim success — proposed
You jump clear of the stern.
The net brushes your shoe.
You kick free and swim.
Behind you, the boat announces that the perimeter is under control.
You don't look back.
By the time you reach the far bank, your arms ache and your clothes drag heavily through the water.
You haul yourself onto the landing below the boathouse.
The restroom sign hangs just above you.
Proposed state ch5_lake_crossing=swim; ch5_lake_drenched=true. Preserve prior pond wetness, item/marks, paper-hat state, botanical infections and consumed items. No antidote/cure, lost paper or further swimming roll.

## C swim failure — proposed
You hit the water.
For a moment, you are clear of the boat.
Then something tightens around your ankle.
You kick. The mesh closes around your other leg.
A motor starts above you.
The net draws taut and pulls beneath the hull.
You reach towards the bright patch of sky.
It grows smaller.
Boat: PERIMETER SECURED.

Proposed fatal node fatal_ch5_bycatch; end:true.
Proposed title BYCATCH.
Proposed popup: The swimmer-retention system has recovered one unauthorised occupant. Recovery does not include resuscitation.
Trigger failed swim raw1–4. No second struggle check or generic gear rescue. Stable separate fatal aftermath from boat blast; don't create versions per earlier wetness.
Future aftermath concept: security boat stern and partly submerged taut collection net, one shoe caught at mesh edge, quiet lake and boathouse beyond; player face/body absent, no gore.
Future prompt draft: Match approved Chapter 5 boat stern, partly submerged capture net taut below hull, single abandoned shoe caught on mesh edge, still municipal park lake and far-shore boathouse, understated absurd fatal aftermath, no face/body/gore/text/UI. Verify exact death-art dimensions later. No art generated.

## Convergence
All three surviving crossings reach boathouse opposite bank, with dry/wet and arrival-method differences preserved. None grants toilet use or ends Chapter 5. Exact boathouse scene next after owner review.
Long-way new incident remains independent and does not return here by default.
No artwork generation, gameplay engine, public manifest or Chapter 4 changes.
