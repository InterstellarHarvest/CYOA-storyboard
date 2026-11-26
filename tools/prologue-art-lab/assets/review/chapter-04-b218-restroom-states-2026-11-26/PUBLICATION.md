# Chapter 4 — restroom state-family publication

2026-11-26. Branch: `art/ch4-b218-restroom-states-review-20261126`.
Current gallery payload: `c6a9dc80b67f20d031ed0d28bbd7f14b1646f4dc`.
The final receipt commit is reported separately to Nate.

**Six candidates are UNSELECTED. A post-lift closer reference is HELD.**
No approved master is replaced or registered. R1 remains suspended, and both
failed R1 reviews remain untouched as unselected historical evidence.

## Public review

- [Current browser gallery](https://htmlpreview.github.io/?https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/c6a9dc80b67f20d031ed0d28bbd7f14b1646f4dc/tools/prologue-art-lab/assets/review/chapter-04-b218-restroom-states-2026-11-26/review.html).
- [Current mapping and held-state addendum](https://github.com/InterstellarHarvest/CYOA-storyboard/blob/c6a9dc80b67f20d031ed0d28bbd7f14b1646f4dc/tools/prologue-art-lab/assets/review/chapter-04-b218-restroom-states-2026-11-26/CONTINUITY-ADDENDUM.md).
- [Native main-state progression PNG](https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/c6a9dc80b67f20d031ed0d28bbd7f14b1646f4dc/tools/prologue-art-lab/assets/review/chapter-04-b218-restroom-states-2026-11-26/v01/comparisons/main-state-progression.png).
- [Exact 4x progression PNG](https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/c6a9dc80b67f20d031ed0d28bbd7f14b1646f4dc/tools/prologue-art-lab/assets/review/chapter-04-b218-restroom-states-2026-11-26/v01/previews/main-state-progression-4x.png).
- [Native files, masks, editable layers and prompts](https://github.com/InterstellarHarvest/CYOA-storyboard/blob/c6a9dc80b67f20d031ed0d28bbd7f14b1646f4dc/tools/prologue-art-lab/assets/review/chapter-04-b218-restroom-states-2026-11-26/v01/README.md).

## Six viable images — exact hashes, no registration

| Candidate | Changed pixels against approved source | SHA-256 | Canonical story coverage |
| --- | ---: | --- | --- |
| restroom-active-leak-main | 2974 | `9a6243310bb7af1958854110af742c603275b2ebf9c889050c6c065737e57279` | `hotel_restroom_plumber` |
| restroom-active-leak-close | 1294 | `35a8f8297da89038a0a7b30596363bfa6ad86e3edc6b02bf0efb360a4dc3a46a` | `hotel_restroom_plumber`, `hotel_wheel_buyer_lead` |
| restroom-braced-main | 2796 | `dcbe6ebf8319e3fe0dabe9c30637494e51342303be9923aba29ccd71acca7fcd` | `hotel_valve_braced` |
| restroom-contained-main | 2766 | `674cb60c905347e99c95b99ec87dfacc218cf15483abe89bc4e092d40b43ed1a` | `hotel_wheel_return`, `hotel_key_master_cabinet` |
| restroom-flood-onset-main | 15942 | `432ce64f5e7e0420f678774ec8cf2edb02ce745ff532d83b3e1723af9d90fb46` | `hotel_valve_flood` |
| restroom-stall-lifting-main | 7998 | `84976c116d9fc87b6ce8f4cf5d7f316d7185fa308f889df6d1c76eafe6bc525e` | `hotel_stall_lot_claimed`, `hotel_stall_crane_success` |

Main scenes retain 314x206 opaque RGB; the closer background retains 564x278
opaque RGB. Each has an exact changed-pixel mask, independent allowed region,
editable native layers and an OpenRaster project. Existing source material
rendering, figure scale/identity and floor perspective are retained.

Approved CH4-04 SHA-256:
`83cf1f0df4d130f24c53c931cae83fd92abef8fdc7e8f80359c5657ce051ce06`.

Approved CH4-B2-03 SHA-256:
`77325aca0d3c61d5b6d1980232fb11fa55156454a26659c6887c4d726a82c377`.

## Reconciliation and quality gate

The braced state retains a dribble; contained stops flow while leaving wetness.
The flood image captures onset before Eddie floats past. Later basket/gesture
motion stays in narration. Existing approved master-isolator Focus art is reused;
no additional lever close-up or fully empty-bay state is invented.

Final continuity QA corrected the initial v01 assumption about the closer camera:
a nearest-stall leaf is visible at the far right. Unchanged CH4-B2-03 is **not
verified for post-lift porter dialogue**. The narrow exposed-wall proof degraded
tile spacing, so that closer state stopped at its quality gate. The diagnostic
is explicitly not a seventh candidate. The current addendum supersedes the
initial reuse statements without rewriting the frozen v01 review or its hashes.

A separate existing canon conflict remains: the restroom and fatal nodes leave
the toilet grounded, while the later mezzanine node says it is inside the lifted
stall. Current art follows the explicit restroom moment. No text or invented
offscreen transport event resolves the contradiction here.

## Verification and provenance

- All six native contracts, exact RGB-difference masks and zero-outside-region
  checks passed. Protected source figure areas and the grounded lift-state toilet
  remain exact. Every OpenRaster merged image and native layer composite matches
  its flattened PNG.
- Actual approved Chapter 2 Bureau and Control Tower references appear at native
  and exact nearest-neighbour 4x, alongside approved-source/state comparisons.
- The corrected public gallery passed 27 figures in Chromium and Firefox:
  54 figure checks and 108 scale checks. Public screenshots were inspected.
- At the current gallery commit, all 191 public review/source objects matched
  hashes, 145 PNGs decoded, and all 13 immutable source/control files matched.
- The frozen v01 directory is unchanged since
  `760bdacb40181e907cb45813ad9a1b0e4d889d4e`; all six candidate PNGs are unchanged.
- Built-in imagegen supplied one staging reference only. Its exact prompt,
  original PNG and receipt are preserved. No generated reference pixels were
  resized or pasted into a state. State sources use approved native masters,
  native water/hatch marks and integer source-pixel relocation for the enclosure.
- Final receipt-commit bytes are independently checked after the last push.

Only this new review-package folder differs from canonical base
`2af6606c25ce252752c65aa5c68c87ff84f804ae`. Main was observed at that same SHA;
PR #32 remains `f320e63934c13e27fd13b9482d0cfba58911362d`; the failed R1 portrait
branch remains `6e59549e2ccf4b60e77ba7783987fd26637fcbbe` and material-pilot branch
remains `e06c93fa0618054a2c4e2b630f6544709db410bd`.

No canonical selection, registry, narrative, gameplay, engine or deployment file
changed. No merge or deployment occurred. Lobby-door and Lot 61 production have
not started. Stop at this first-family review gate.
