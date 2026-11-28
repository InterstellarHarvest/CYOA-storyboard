# Chapter 5 — property delivery and forward continuation / review 53

## Owner approval

Nate’s next “ok” approves review 52’s map-to-lake and map-to-property-station arrivals, corrected lake geography, reuse of the established two lake choices, and optional ticket redemption or onward bypass. Earlier Chapter 5 material remains preserved.

The delivery mechanisms and probabilities below were already approved in review 44. Exact prose, collection-card wording and the short onward transition below are proposed for review. This is not a claim that the full Chapter 5 JSON or the earlier upstream graph is complete.

## Committing the claim — common lead-in

You feed the claim ticket into the slot.

The machine draws it in.

A distant clunk travels along the overhead pipe.

Something comes towards you at considerable speed.

The receiving chamber gives a heavy bang.

PROPERTY RETURN: COMPLETE.

The delivery hatch opens.

One hidden d6 for the complete deposited parcel: raw 3–6 intact; raw 1–2 damaged. Redemption requires a real matching unredeemed ticket and stored-property record, consumes that ticket on commitment, and stores the result. No per-item roll, extra cosmetic gameplay roll, claim repetition or reroll on re-opening the delivered parcel.

## Intact — raw 3–6

Your deposited belongings sit inside a broad carrier capsule.

Each returned article still bears its numbered intake tag.

You check the contents carefully.

Everything you actually left with them is here.

Terminal: PLEASE CONFIRM THAT YOUR PROPERTY HAS BEEN RETURNED.

Player: IT HAS.

Terminal: CONFIRMATION RETURNED.

Single collection action: COLLECT YOUR RETURNED BELONGINGS.

Grant only the actual deposited subset once, then continue forward. For property_record=stored_all, the subset is timing_clicker, desk_plant, red_stapler and rubber_band_ball. For stored_three, exclude the specific retained_item recorded at intake. Prevent duplicate grants; do not restore a retained object that was used, lost, traded, adopted or destroyed later. Do not award unrelated correspondence, badges, keys, capsule, packaging or another effects box. Six visible slots are not an item limit.

## Damaged — raw 1–2

Bent metal, cracked plastic and fragments of things you cannot identify fill the capsule.

A numbered intake tag lies on top.

It is the best-preserved part.

Player: THESE WERE MY THINGS.

Terminal: YOUR PROPERTY HAS BEEN RETURNED.

The machine waits for you to collect it.

Single collection action: TAKE THE PILE OF BROKEN BITS.

Award exactly one item: broken_property_bits / PILE OF BROKEN BITS. Suggested inspection copy, pending review: “A HANDFUL OF BENT METAL, CRACKED PLASTIC AND UNRECOGNISABLE FRAGMENTS. NOTHING IS IN WORKING ORDER.”

No deposited article is returned in working form on this outcome. Existing held belongings remain intact. No hidden key, functioning salvage, repairable stapler, recovered plant, seed reward or rubber-band-ball centre is revealed. Junk has no mandatory future-use obligation. The parcel result is resolved, not a fatal ending, injury, cure or chance to request a second shipment.

## Shared onward transition — also used when skipping collection

You leave the awning.

The broad pipe turns back towards the Exposition buildings. The footpath continues between the security exhibits.

You follow the path.

Join review 51’s later_park_arrival once: footpath towards the drinking fountain/fence, open lawn towards refreshments/foam, or maintenance verge towards the depot. Keep the later section’s optional paths, inventory, claim result and all earlier states. Redemption, taking broken bits, and walking past the station do not end Chapter 5 or imply that the player has left the Exposition.

If redemption has already been resolved, do not replay the intake/delivery/collection sequence. Skipping makes no mutation to the ticket or deposited-property state. A stored on-screen image of a destroyed ticket is not a physical replacement. Donation, nothing-declared, unopened discarded box and other ineligible cases keep the onward path without fabricated property grants.

## Assembly note

At implementation, separate committed/resolved parcel state from any pending collection action, so a saved result cannot reroll and a collected reward cannot be awarded twice. Use the existing schema’s one-shot/effect conventions. Do not introduce a new carrying-capacity rule, pickup timer, extra chance roll or external obligation to make the parcel work.

Next outstanding connective work: distinct arrivals from the far gate and land-side collection bay into this same station/forward junction, preserving whether the lake, robot and other incidents were actually visited. No backtracking through a completed incident.
