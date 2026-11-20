# Chapter 3 Batch D — audit and review

Audited latest fetched main `5134edb160afaa019e11f872a3b87d3b01b257b0` on 2026-11-20. Narrative blob `857ffdf1bc9432cf4bbbfd7819f5f430a06d9036` is unchanged. **Nine remaining active records: five main scenes, two portrait backgrounds, two foregrounds.** Twenty approved Chapter 3 records are reused; all 65 pre-reboot historical calls are excluded. All 34 review nodes map to registered scenes, poses and close backgrounds; no missing static artwork requirement is established.

| Order | Artwork ID | Registry key | Type / dimensions | Review nodes | Approved dependencies | New generation? | Continuity constraints |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | CH3-D01-service-exit | `scenes:pavilion_reboot/service_exit` | scene 314×206 | presenter_help_end, attendant_honest_end | `scenes:pavilion_reboot/restroom_entrance` | Yes: distinct scene/state/pose | One threshold shared by presenter_help_end and attendant_honest_end; door right, cabinet/pipes left; no restroom access. |
| 2 | CH3-D02-service-exit-bg | `scenes:pavilion_reboot/service_exit#portraitBackground` | portrait-background 564×278 | presenter_help_end, attendant_honest_end | `scenes:pavilion_reboot/restroom_entrance#portraitBackground` | Yes: distinct scene/state/pose | Independent close camera sharing D01 right-side door, left cabinet, stripe, daylight; either approved human anchor. |
| 3 | CH3-D03-attendant-quiet | `portraits:pavilion_attendant:quiet` | portrait 564×278 | attendant_honest, attendant_honest_end | `portraits:pavilion_attendant:idle`, `scenes:pavilion_reboot/record_printer#portraitBackground` | Yes: distinct scene/state/pose | Approved attendant identity, glasses, tie, vest and badge; same seated waist baseline as idle; used with printer AND service background. |
| 4 | CH3-D04-presenter-relieved | `portraits:pavilion_presenter:relieved` | portrait 564×278 | presenter_help_end | `portraits:pavilion_presenter:idle` | Yes: distinct scene/state/pose | Approved presenter identity, coral blouse, slate jacket, auburn bob; bottom-anchored waist and rightward open hand. |
| 5 | CH3-D05-backstage | `scenes:pavilion_reboot/backstage` | scene 314×206 | locomotion_pass, backstage_exit | `scenes:pavilion_reboot/restroom_entrance`, `scenes:pavilion_reboot/locomotion_stage` | Yes: distinct scene/state/pose | Behind existing exhibit, concrete/teal structure; cables, half sandwich, carton, podium, certificates and clapper machine clear of walkway. |
| 6 | CH3-D06-exterior-exit | `scenes:pavilion_reboot/exterior_exit` | scene 314×206 | locomotion_fail, door_dash_fail, door_reverse_end | `scenes:pavilion_reboot/arrival` | Yes: distinct scene/state/pose | Same Pavilion exterior materials; empty padded cart, cushions, loading door, concourse/bench; three safe endings, no permanent ribbon. |
| 7 | CH3-D07-exit-vestibule | `scenes:pavilion_reboot/exit_vestibule` | scene 314×206 | door_dash_pass | `scenes:pavilion_reboot/restroom_entrance`, `scenes:pavilion_reboot/record_scanner` | Yes: distinct scene/state/pose | Same sinks, teal stall, reader and one-way gate; glass blocks access; descending exit assistance to maintenance. |
| 8 | CH3-D08-courtesy-stage | `scenes:pavilion_reboot/courtesy_stage` | scene 314×206 | door_courtesy | `scenes:pavilion_reboot/restroom_entrance`, `portraits:pavilion_attendant:alarmed` | Yes: distinct scene/state/pose | Changed real restroom state, frame moves left BEHIND foreground bench; original opening shuttered; right desk and all fixtures pixel-locked. |
| 9 | CH3-D09-courtesy-stage-bg | `scenes:pavilion_reboot/courtesy_stage#portraitBackground` | portrait-background 564×278 | door_courtesy | `scenes:pavilion_reboot/restroom_entrance#portraitBackground`, `portraits:pavilion_attendant:alarmed` | Yes: distinct scene/state/pose | Same close camera and counter; shutter/track at left, relocated frame partly outside crop; intercom/mic/plant and right wall pixel-locked. |

Full node coverage, exact prompts, source originals, derivations and hashes: [inventory.json](../tools/prologue-art-lab/assets/review/chapter-03-batch04-2026-11-20/v01/inventory.json), [manifest.json](../tools/prologue-art-lab/assets/review/chapter-03-batch04-2026-11-20/v01/manifest.json), [generation receipts](../tools/prologue-art-lab/assets/review/chapter-03-batch04-2026-11-20/v01/generation-receipts-final.json).

No new item, visitor portrait, death or Focus A images. Existing key/photo/stapler/clicker art is reused. Service exit, backstage and exterior each support multiple nodes without redundant generation.

`stapler_printer_snarl` has a narrated printer loop and opening maintenance shutter, but no separate state brief. Reuse the approved printer master; Nate should decide whether a separately scoped masked overlay would improve it. `record_scanner_result` likewise narrates its door transition using the approved master. Neither finding authorizes redrawing approved art.

All candidates remain **generated / unselected**. Generator originals are larger rasters; original native-grid authorship is **unproven**. The logical images are nearest-neighbor source-derived exports, and 4× previews are exact nearest-neighbor enlargements of those exports. Approved images are never represented as freshly generated higher-resolution art. The two courtesy variants retain exact approved pixels outside explicit state masks.

The original seated attendant cut floated at the service door. A generated lower-torso correction extends it to the canvas edge, preserving the upper portrait pixels; both corrected service and printer composites are shown for review.

Visual review questions and known limitations are shown per candidate in the gallery; technical passing does not constitute creative approval.

## Review location and source

Generation branch: `art/ch3-pavilion-batch04-20261120`. Exact native candidates and generator originals first committed at `4fc277651c7d05163817d9ab99d0fc3fcf522d47`; later package-completion commits preserve those candidate bytes. The canonical nine generated records cite that immutable source commit. Approved preview registry and selected artwork are unchanged.

[Open local/repository gallery](../tools/prologue-art-lab/assets/review/chapter-03-batch04-2026-11-20/v01/index.html). Proposed public gallery after a separately reviewed main-only publication: `https://interstellarharvest.github.io/CYOA-storyboard/tools/prologue-art-lab/assets/review/chapter-03-batch04-2026-11-20/v01/`. This URL is not live from the generation branch. A separate draft publication PR pins the completed review package; no direct deployment, merge or workflow dispatch is performed.

## Native candidate SHA-256

| Candidate | SHA-256 |
| --- | --- |
| CH3-D01-service-exit | `4a736b2d7b5fd7dea50fe9d93fe36e7465674ce0b8e38e7f2d6517fca73df392` |
| CH3-D02-service-exit-bg | `49e008b1ee37a01d49dc8e2c43ecc93b3b7c1914a23a4e80ce7c5a80d1818dee` |
| CH3-D03-attendant-quiet | `dda560880cecd42fa843fe35b66cb7d2d9222d8301a68934e594f0552d24a5db` |
| CH3-D04-presenter-relieved | `29a349c7bcdfe32d2885709dc91977beb7e3869d2461913cfd89afdacebbda9b` |
| CH3-D05-backstage | `ea18247e0564c459c5573a10e2bf8d7dee9e713c8f27d3e6b095eb5df857d11f` |
| CH3-D06-exterior-exit | `76b3232f685fd392f981f0c846382e3ddccd61ed94d44e09ea1bc5cf032c3e8a` |
| CH3-D07-exit-vestibule | `cc2d2ce27e1e2cbf609fcae2210d3c46c57b749e8850be2219ad6de7f7f807c8` |
| CH3-D08-courtesy-stage | `0b413a7b9a669365f114fda8765a242fc3ce00fc9c1ea3bd535c7a2b3d1cdb98` |
| CH3-D09-courtesy-stage-bg | `9664be30b82cfb963cf9f6f2bf24b659fe0e0136701fea6f57e7035922b9ffba` |

## Validation

- All nine PNGs pass dimensions, opacity/binary-alpha and exact 4× nearest-neighbor validation. Seven RGB opaque images; two RGBA transparent foregrounds; zero partial-alpha pixels.
- Every selected-art file, all preview registry bytes, the narrative blob and historical archive remain unchanged. Courtesy state masks preserve exact approved pixels outside the mask; all changed coordinates and state-only RGBA layers are included.
- All 34 nodes map to registered artwork; 20 approved active Chapter 3 records reused, 65 historical calls excluded. No missing static requirement established. Narrated printer jam/shutter state is flagged for Nate without expanding scope.
- Chapter 3 brief preparation/audit and reboot narrative QA pass; storyboard smoke and canonical drift pass; sync QA passes 22/22; death export and Prologue static QA pass.
- Gallery browser QA passes in Chromium and Firefox on the built Pages site at the project path prefix, including all image/link loads, native/4× dimensions and mobile native-size preservation.
- Storyboard browser regression: 24/24. Selected-artwork browser regression: 60/60. Repaired Prologue Lab built-site regression: 70/70.
- Smoke provenance validation was extended narrowly to recognize Batch D’s pinned commit, PNG path and SHA-256; its prior Chapter 2-only assumption rejected valid new generated candidates. Existing selection/integration assertions remain unchanged.

## Nate’s Art Director questions

1. Does the service main/close pair feel like the same humble, narrow passage? The close camera is still somewhat panoramic.
2. Do the quiet attendant and relieved presenter preserve the approved faces, costumes and proportions? Is the attendant’s corrected lower waist natural at the service doorway and behind the existing printer counter?
3. Does the backstage ordinary door and courtyard align with the final exit beat? Is the sparse mechanical clapper readable without looking like a character?
4. Does the vestibule clearly show a blocked real restroom and a descending smooth exit ramp? Confirm the inferred camera/topology against the approved entrance/scanner views.
5. Is the courtesy door/frame visibly displaced on a plausible rail behind the bench? Are spotlight, shutter, retained desk equipment and close cropped jamb sufficient to show the same event?
6. Is source-derived pixel softness acceptable beside Chapters 1–3, or should specific candidates get another finishing pass? Native-grid authorship remains unproven, with no claim of true native authorship.
7. Should the narrated stapler/printer loop and maintenance shutter receive a separately scoped masked state overlay later, or does the approved printer master plus narration suffice?

## Current review update — v02 close cameras and attendant proportions

Nate found the attendant vertically compressed and the portrait backgrounds too wide. Three unselected candidates are revised: D02 service background, D03 quiet attendant, D09 courtesy background. Six other candidates and the entire v01 package remain byte-identical. The two service composites share one background.

[Open v02 gallery](../tools/prologue-art-lab/assets/review/chapter-03-batch04-2026-11-20/v02-close-camera-corrections/index.html). Both backgrounds are independently re-authored close views with large cropped fixtures and no ceiling or interior floor. The attendant is newly drawn with a naturally taller neck/torso, exported with uniform nearest-neighbor scale and transparent padding; no forced silhouette bounding-box fit is applied. Existing presenter and alarmed attendant foregrounds are unchanged.

Exact revised image/original source: `15f17fd3b3ebd348160c61ff3573e8fa8825ee21`. The v01 source commits above remain historical. All candidates remain generated/unselected. Native-grid authorship is still unproven.

| Revised candidate | SHA-256 |
| --- | --- |
| CH3-D02-service-exit-bg | `241bfb8e817cf7c42508c218c188a1ac2706bad2e5f577484ce10a359b9a88e9` |
| CH3-D03-attendant-quiet | `7f00208a3a96628f18fd23f079913dcb706e0e220db081d4cb438107f15bdf90` |
| CH3-D09-courtesy-stage-bg | `b0786ebd4147c6b0e6441838c725751a794db04fa9bcce4341aa1a3a7f1e7623` |

Image dimensions, alpha, exact 4×, uniform scaling, six retained images and all v01/approved/narrative preservation checks pass. Revised gallery Chromium and Firefox checks pass at the built Pages prefix, with native/mobile dimensions and all links verified. Chapter 3 briefs, narrative, smoke, canonical and sync checks pass. Review the new service composites, tighter courtesy shot and the attendant’s natural proportions; no further visual approval is implied.
