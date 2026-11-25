# Gameplay PMO / Claude — separate informational INSPECT handoff

Artwork task only. **No engine feature, runtime binding, narrative edit, merge or deployment is implemented here.** New widescreen candidates are UNSELECTED. Existing v01 dressing room and two detailed panels are owner-approved unchanged; historical review labels remain historical. Resolve selection and registration separately.

## Presentation contract

- Existing node: `hotel_bridal_door_focus`; existing Focus identifier: `grand_bellevue/bridal_privacy_panel`.
- Default presentation:564×278 opaque RGB widescreen Focus, with ordinary story choices visible and available under their existing conditions. New locked/provisional frames share identical architecture/hardware.
- Contextual **INSPECT** opens the corresponding approved565×451 detailed image with additional descriptive information. These are object-inspection images under the owner's finalized two-view decision; they do not redefine the Focus canvas.
- INSPECT is an informational view action, **not a story choice**. Do not add a story node, flag, inventory item or gameplay mode to represent opening it.
- X or Escape closes inspection and restores the exact previous Focus presentation, original choices, dialogue position and keyboard focus. Restore focus to the invoking INSPECT control. Normal story text/choice progress must not restart.
- Open/close must not call `Rules.step`, replay node-entry effects, set/clear flags, consume a choice, mutate inventory or restart dialogue. In particular, opening inspection must not rerun `hotel_bridal_door_focus.effects.set.ch4_bridal_door_inspected`.
- Verify any proposed reuse of inventory inspection or scene-pickup behavior first. Their look does not establish safe semantics. No such reuse or implementation is authorized in this artwork change.

## Preserve all five canonical choices

| Focus choice ID | Existing condition / destination |
| --- | --- |
| `door_ask_bridal_criteria` | `notFlag: ch4_bridal_identification_explained` → `hotel_bridal_criteria` |
| `door_request_override` | `notFlag: ch4_bridal_emergency_override_denied` → `hotel_bridal_emergency_override` |
| `door_show_ring` | `has: wedding_ring_lot31` → `hotel_bridal_ring_argument` |
| `door_inspect_gown` | Existing gown inspection action → `hotel_bridal_gown_focus` |
| `door_leave` | Existing leave action → `hotel_bridal_corridor_exit` |

Do not replace, absorb or consume any of these with INSPECT. The return hub `hotel_bridal_door_options` is narrative mode and has the parallel `door_return_*` IDs; closing inspection must not silently navigate to that hub or turn it into a new Focus node. Its existing destinations/conditions remain unchanged.

Preserve canonical missing-ring/exhausted-choice notes: future disabled/missing-item presentation must not be invented or changed by this art task. `hotel_bridal_ring_argument` keeps the indicator red, does not consume the ring and does not open the door. Its staff-lavatory/park returns must remain intact.

Provisional imagery is a conditional production reference for the existing `hotel_bridal_autofit_survived` outcome / existing `ch4_provisional_bride_registered` flag. The node's current CONTINUE destination is `hotel_seashell_room`. Do not invent a second expression, extra Focus key, new state flag or new dispatch binding. The shared close-view door geometry stays closed; this artwork does not implement the narrative door-opening transition or the later lavatory scene.

## Engineering acceptance evidence required before activation

1. Snapshot node, relevant flags, inventory, dialogue cursor, available choice IDs/order and focused control before INSPECT; verify exact equality after open/close, including repeated open/close. Spy on `Rules.step` and node-entry effects: zero calls caused by inspection.
2. Exercise all five existing choices after closing; each still executes its original destination/condition once. Check criteria/override both before and after exhaustion, and ring present/absent. Do not convert ring rejection into access or consumption.
3. Verify return-hub behavior and both ring-argument exits without replaying dialogue. Closing inspection returns to the originating presentation, not a newly entered node.
4. Verify mouse/X, keyboard activation, Tab/Shift-Tab, Escape, focus restoration and prevention of accidental activation of hidden underlying choices. Inspection must not strand keyboard focus or consume a choice key.
5. Save/resume in locked and provisional situations, with/without ring and exhausted conditions. Inspection is transient view state; saving or resuming must not create story-state changes, repeat effects or lose original choices. Document the chosen overlay restoration policy separately.
6. Test the corresponding approved detailed image in each state at565×451 and default Focus at564×278. No stretching/cropping approved PNGs; preserve the exact registered hashes.

**If the feature cannot preserve the existing choices and state, do not activate it.** Implementation, regression tests, selection/registration and deployment require the separate engineering workflow. This handoff defines intended behavior, not proof that the current engine supports it.
