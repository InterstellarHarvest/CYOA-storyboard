# B2-13 — authored conditions and artwork handoff

**UNSELECTED artwork only.** Intended future primary key: `focus:grand_bellevue/autofit_gown`. This registry entry does not exist at canonical baseline `436e83f43c01b0a64620056d44aabf14c61fb444`; no entry, asset path or runtime binding is added here.

## Two-image scope

1. **CH4-NEW-08 primary,564×278 RGB:** whole empty gown on its rolling stand. Outer lace exposes a compact motor, geared drum and routed bodice/neck cables. Inner lining still conceals the manual release and its warning. The physically small maker plate and safety pictogram are subordinate to fabric/machinery; full wording belongs to the canonical inspection text.
2. **One supplemental motor-discovery reference,564×278 RGB:** closer camera on the same garment/stand. Inner lining is lifted, revealing the brass MANUAL SLACK tab and NOT AN EMERGENCY STOP warning. Cable routes show slight slack after the authored press. Both are re-rasterized from shared native geometry, with no crop/enlargement of a completed image.

The closer camera follows Nate's clarification that text need not be readable in the wider scene; the closer dress/mechanism view carries detailed lettering. It does not add a square inspection, portrait foreground, extra Focus identifier or third production state.

## Why one supplemental reference is sufficient

`hotel_bridal_gown_focus` is the existing Focus node. Its `gown_examine_motor` choice is available under `notFlag: ch4_autofit_release_located` and leads to `hotel_bridal_gown_motor`. The primary text already pulls aside outer lace, reveals the AutoFit motor and warns to disconnect it before garment removal/adjustment. It must not reveal the separate manual-slack solution.

`hotel_bridal_gown_motor` is currently **narrative mode**. Within one authored sequence the player lifts inner lining, follows cables, discovers the brass tab, presses it, sees the neckline loosen, releases it with cables remaining slack, and later replaces the lining. There is no separate pre-press/post-press choice or dispatch. Therefore one reference depicts a useful moment after the press and before lining replacement; separate found/pressed/returned frames are redundant for this review.

The existing node sets `ch4_autofit_release_located`. That flag provides one nonstacking+1 modifier to the later risky gown-fitting roll; discovering the tab does not guarantee survival or switch the motor off. The authored warning explicitly says it is not an emergency stop, and the system remains ready for fitting. Do not infer a new power-off state from the slack cables or safety pictogram.

## Integration boundaries

- Supplemental identifier `CH4-NEW-08-manual-slack` is a review-package label only, not a canonical Focus key. Logical family `gown_motor_manual_slack` comes from docs/138; no new flags, modes or conditions are authored.
- Do not convert the motor node to Focus mode or automatically bind this closeup. Separate approved engineering integration must choose safe informational presentation under existing authored progression.
- Do not persist an exposed-lining pose after the text replaces the lining. The supplemental is a moment/reference, not a new permanent open-cover flag. The registered room/gown remain on the same stand.
- Preserve all existing primary choices: examine motor, try gown, hold to camera, leave it alone. Preserve all motor-node choices and their destinations. No choice text, eligibility, inventory, rule or roll changes are authorized.
- `hotel_bridal_gown_camera` returns the gown to its stand. `hotel_bridal_gown_try` and `hotel_bridal_autofit_survived` concern a wearer and are not illustrated by these empty-garment images. No protagonist, worn gown or fatal aftermath is supplied.
- `fatal_bridal_made_to_measure` belongs to B2-16. B2-14 lavatory/shell artwork is also outside this package. Continue the queue only after owner review.

The world-coordinate diagnostic in `diagnostics/` demonstrates that only lining/cables change before the closer camera is applied. It is explicitly NOT an extra candidate or runtime asset. All production candidates remain UNSELECTED; registration and gameplay presentation require separate approval.
