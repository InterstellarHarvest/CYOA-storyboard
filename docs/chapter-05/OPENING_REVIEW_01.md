# Chapter 5 — opening review 01
Status: Nate-selected concept A as basis; owner-directed opening structure; exact prose and death title below are PROPOSED for review. Not a complete chapter, narrative lock, art authorization or gameplay import.
Supersedes the initial concept report only where directions below differ. Earlier proposals remain design history.

## Owner rulings
- All three nonfatal Chapter 4 exits converge on promising secluded trees/shrubs at the nearby public park. Keep ch4_exit_route and all inventory/state.
- No Expo signage, sponsor explanation or demonstration reveal before following the conspicuous wire.
- Approach reveals several apparently dead squirrels and the conspicuous wire running from the plants farther into the park.
- Exactly three initial player actions: follow wire; inspect squirrels to assess cause/apparent death (possible animatronic interpretation); urinate on shrub.
- Urination causes electrocution death, deterministic, no d6 or risk marker.
- Following wire leads deeper into park and reveals signage connecting park technology displays to Exposition of Everything.
- No keeper intercepts/warns player before this choice. No opening ceremony or trial scenario selected.
- Inventory has six visible slots with scrolling, no capacity limit. Opening consumes/awards no items.
- Chapter title A Little Privacy remains working, not final owner approval.

## Proposed narrative and cards

### ch5_park_edge — Narrative B
You cross the courtyard. Beyond the path, a cluster of trees and dense shrubs screens a quiet patch of grass.
No queue. No attendant. No one in sight.
For once, the obvious solution looks obvious.

Single action: APPROACH THE SECLUDED SHRUBS. -> ch5_shrub_discovery
Opening recognizes hotel exit via existing state when authored in schema; do not invent different park gates or reset fee/infection/ownership.

### ch5_shrub_discovery — Narrative B
You step off the path and move behind the shrubs.
Several squirrels lie beneath the branches. One rests on its back, paws curled. Another has its head tucked beneath its tail. The fur along its side is singed.
None of them moves.
Perhaps they're artificial. After everything you've seen today, even the squirrels might be entitled to a break.
A thick black wire emerges from the base of the shrub nearest you. It runs openly across the grass and disappears around a bend in the path.

A action: FOLLOW THE WIRE. -> ch5_wire_follow
B action: TAKE A CLOSER LOOK AT THE SQUIRRELS. -> ch5_squirrel_inspection
C action: URINATE ON THE SHRUB. -> fatal_ch5_well_grounded

### ch5_squirrel_inspection — proposed immediate result
You crouch without touching anything.
There is no visible breathing. No twitch of a nose. The singed fur looks unpleasantly convincing.
You look for a seam, a winding key, anything that would make this less troubling.
Nothing obvious presents itself.
Player speech: YOU'RE NOT REAL, ARE YOU?
The squirrels offer no clarification.

Sets proposed ch5_squirrels_inspected=true. Does not establish real versus animatronic as a locked fact; cause/conclusion can be refined with Nate. No award, consumption, roll or new hazard.
Follow with A FOLLOW THE WIRE and C URINATE ON THE SHRUB. Inspection card remains visible disabled ALREADY INSPECTED when supported; no repeatable inspection loop.

### ch5_wire_follow — proposed immediate result
You follow the wire around the bend.
The trees open onto a broad lawn. People sit on benches beneath bright exhibition banners. A small brick restroom stands beside a temporary display pavilion.
Above the pavilion, you recognize the emblem of the Exposition of Everything.
OUTDOOR TECHNOLOGY DEMONSTRATIONS.
Below it, a second banner reads:
FOR YOUR PROTECTION.
The wire continues toward the pavilion.

Editorial frontier: pause here to develop representative/system/next incident with Nate. This is not a chapter ending and not a playable unfinished node. No staff-pass assumption or previously suggested trial/ceremony automatically selected.

### fatal_ch5_well_grounded — proposed fatal text
You turn toward the shrub.
For one brief moment, it seems you might finally get some relief.
A sharp crack splits the air.
Every branch lights up.
You don't get another moment.

Title: DON'T WHIZZ ON THE ELECTRIC FENCE!
Popup body: The park's new security installation records one successfully neutralized intrusion. The landscaping remains undamaged.
Trigger: C from discovery or post-inspection; certain death, no d6, no risk marker.
Inventory: terminal state; no surviving transition, no special item rescue authored.
Aftermath art description for eventual handoff only: same shrub/wire and squirrel placement, a smoking abandoned shoe on grass; protagonist face/body/gore absent. Exact production prompt deferred until prose/visual requirements approved; no image generation.
Engine handoff later: RETRY last decision; CHECKPOINT chapter beginning; EXIT menu. No runtime changes here.

## Scope
No modifications to Chapter 4, public chapter manifest, current art records, game repository or other branches. Next owner review concerns this prose, squirrel-inspection result and remaining proposed prose, then the wire-follow arrival scene.

## Subsequent owner ruling — fatal title
Nate selected DON'T WHIZZ ON THE ELECTRIC FENCE! as the electrocution fatal-ending title, referencing Ren & Stimpy. This supersedes proposed WELL GROUNDED. Keep stable node ID fatal_ch5_well_grounded for now; the internal ID is not displayed. Exact remaining prose remains proposed; this title ruling alone does not approve the complete opening or authorize art generation.
