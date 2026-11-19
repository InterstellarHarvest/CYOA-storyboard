# Retroactive Artwork Approval Ledger — 2026-11-16

**Owner ruling:** If an artwork image was generated, selected, and used in the project, it was approved. An old `generated` or `not-started` metadata entry is not evidence that the art must be redrawn or approved again. Approval is valid regardless of the Git branch on which the selected source resides.

## Applied catalog corrections

The shared `story/artwork.draft.json` file was updated directly. Current top-level artwork records (including standalone portrait backgrounds, but excluding nested image variants): **163 records**.

| State | Count | Meaning |
|---|---:|---|
| `integrated` | 46 | Previously selected art used in the Prologue or Chapter 1 gameplay review build. Already approved by owner ruling. |
| `reused` | 5 | Previously integrated and approved art reused from M2. |
| `approved` | 7 | Accepted Biology Park first-batch scene and portrait components, production game integration not yet confirmed. No re-generation or reapproval required. |
| `not-started` | 105 | Unselected/unproduced art requirements from Chapters 1–3, principally additional Biology Park and People's Pavilion work. |

**Nested production variants:** 12 additional integrated Chapter 1 view/page/scene-state records plus one *approved* but deliberately unbound chair image. The combined statuses represent the **29 selected Chapter 1 images** in private review PR #10.

**Prologue:** 28 historically labelled `generated` image records are now `integrated`, while the five M2 reusable records remain `reused`. This is owner retroactive approval, not an assertion that prior art processing produced different pixels. The Prologue art lab still reads exactly the original pinned review PNGs, independently of the new status. Its source audit and Exposition V03 review manifest now record the retroactive approval. Original asset-index hashes and original PNGs are untouched.

**Chapter 1:** 14 scene backgrounds, 8 conditional scene states, 2 complete opaque House conversation views, 3 album Focus A pages, and 2 family portrait item images — 29 total. Source: `InterstellarHarvest/CYOA` draft PR #10, head `83f6d051e036c54ccf05b602a4cbc3792e48bd07`. The final unrestrained chair variant is deliberately unbound in active gameplay; therefore its record is `approved`, not falsely labelled as displayed. The remaining 28 selected files are `integrated` in the review build. Metadata includes source provenance, exact chosen paths, and selection notes. The newer opaque House intercom design supersedes the old draft's unnecessary paired portrait backgrounds; the record count falls from 165 to 163 **without losing any selected image**.

**Chapter 2:** Seven accepted Batch 1 images are `approved`: Conveniences Bureau, Groundskeeper scene, formal entrance, service entrance, Jungle Junction, Groundskeeper portrait background and portrait foreground. The final selections for A/C/E are the signage-polish-v02 corrections; B/D/F/G are accepted earlier candidate pixels. The public catalog records each image's original source branch, exact review path and SHA-256. Their `assetPath` remains null because they were **not verified** at a production `art/` path, and the catalog must not invent such paths. Those images need no new art approval; Gameplay PMO should determine whether they are already integrated in a local worktree and promote status to `integrated` once confirmed.

**Chapter 3:** All unselected Pavilion artwork briefs remain `not-started`. `A MODEL CITIZEN` is narratively approved, not an approved art image.

## Workflow for every next asset

1. ChatGPT Story Director and owner approve story and record the brief in the public storyboard.
2. Codex generates candidates from this canonical catalog.
3. ChatGPT Art Director and owner select the asset. The selection itself approves it. Record exact selected path, version/hash and `approved` status on the public storyboard immediately.
4. Claude Gameplay PMO imports the pinned storyboard revision and selected artwork, validates runtime usage, and promotes only actually referenced/running images to `integrated`.
5. The public storyboard is published through a successful GitHub Pages deployment; QA fails when a known selected artwork record regresses to `not-started`.

**Important:** `approved` is a creative signoff; `integrated` is that signoff **plus verified gameplay use**. These are not competing states and do not require a second approval review. Unselected images and alternate candidates must not be auto-approved because a PNG exists in a branch. Do not force the older game repository's stale art catalog over this corrected public source.

The public storyboard records approval/status and selected provenance, but not all Chapter 1–2 image bytes have been mirrored to the public site for actual image preview. Adding approved preview packages and verifying all local Gameplay PMO worktrees is a separate technical integration task. Never confuse unavailable public preview pixels with missing/unfinished creative artwork.

## Addendum: Gameplay PMO verification, 2026-11-16 (docs/105)

- **Audit result.** The most advanced playable build is InterstellarHarvest/CYOA draft PR #13, `0f42e50`. It sits on PR #11, which sits on PR #10, which sits on PR #6. It references exactly **61** catalog images:
  - 28 Prologue images;
  - 28 Chapter 1 images;
  - 5 reused M2 images.
  - Every one matches this catalog's `integrated` / `reused` records.
- **The unbound chair state** stays `approved`.
- **The Rest Assured death vignette** (one shared record for all three causes per docs/104, `deathScreens["house_of_tomorrow/rest_assured"]`) is now `integrated` with its verified game path:
  - owner-approved at `000f096`;
  - byte-identical in the game's review-gated `?deathproof` presentation, sha256 `7f469efa…`;
  - the game's gated presentation still matches only the voluntary cause; widening it is a pending gameplay change.
- **Chapter 2:** no Biology Park image is integrated in any game branch, worktree or stash. The seven Batch 1 images stay `approved`, and their exact selected bytes are now previewable (SHA-256s verified against this ledger).
- **Verification is now mechanical.** `story/game-integration.json` (written by the game) lists each used image and its hash. `tools/sync/check-canon.mjs` fails the deploy in either case:
  - an `integrated` record is not in that report;
  - a selected record loses its preview, or regresses in status.

## Owner approval addendum — Chapter2 Batch2, 2026-11-17

All seven Batch2 images were visually reviewed and **approved without changes**. Registered with `tools/sync/register-art.mjs` from `InterstellarHarvest/CYOA@agent/ch02-art-batch02-biopark-routes`, approved commit `ed098eee6999b25d44a6b4db2ad7605e430d88c6`. Exact selected PNG bytes are public previews; production `assetPath` remains null. None is integrated. Earlier approvals, candidates and rejected studies remain preserved.

| Artwork key | Selected source path | SHA-256 |
|---|---|---|
| `scenes:biology_park/control_tower` | `review/chapter-02-batch02-2026-11-17/candidates/A-control-tower.png` | `fde023d3741641aa0f376ad1ac65508de3aeef84a05a8be0defecb3f4603daca` |
| `scenes:biology_park/spore_garden` | `review/chapter-02-batch02-2026-11-17/candidates/B-spore-garden.png` | `aded321d36cf2ea9c50d3d696230fe2a1606f181ff8fc0d1f2f7bffb92af4ed3` |
| `scenes:biology_park/tour_tram` | `review/chapter-02-batch02-2026-11-17/candidates/C-tour-tram.png` | `fd2b01dbff9db37a79b5a1519b0adc5be3ce8e60c425d7bfb039a5a2194f6d57` |
| `scenes:biology_park/damaged_walkway` | `review/chapter-02-batch02-2026-11-17/candidates/D-damaged-walkway.png` | `8ca919bedda4f414a7bfac7bfc1f0003f8531e7fcee36ce8f2873db0985af642` |
| `scenes:biology_park/moving_forest` | `review/chapter-02-batch02-2026-11-17/candidates/E-moving-forest.png` | `5a1f61ab9c8a1c7fac129683df09da9bae48a0f22adb9012d98183e0d10f5c81` |
| `scenes:biology_park/overgrown_tram` | `review/chapter-02-batch02-2026-11-17/candidates/F-overgrown-tram.png` | `d4c381642d2d54e6341fd82121ddcf5caef11029fa37c16d221edd5173d470c7` |
| `scenes:biology_park/sensor_gallery` | `review/chapter-02-batch02-2026-11-17/candidates/G-sensor-gallery.png` | `b2f23c8d015c1f45af200733ba28201627c6d10102dcd9e34b92230c32683a7c` |


## Addendum — Chapter 2 Batch 3 owner selections, 2026-11-17

Final owner approval without changes. Source `InterstellarHarvest/CYOA@009c5afea133f36a92f2af74887e00b351d9b914`, branch `agent/ch02-art-batch03-biopark-machinery`. Exact bytes registered using `tools/sync/register-art.mjs`; approved, never self-integrated. All game production paths remain null pending Gameplay PMO. Prior approved selections and original generations are preserved.

| Key | Source path | SHA-256 |
|---|---|---|
| `scenes:biology_park/authorization_archive` | `review/chapter-02-batch03-2026-11-17/candidates/A-authorization-archive.png` | `cf56a225b9341ac24c654562e002e4d45d5c56be36aa7f4d3f40f045bebc79ec` |
| `scenes:biology_park/central_flower` | `review/chapter-02-batch03-2026-11-17/candidates/B-central-flower.png` | `68698aea02b19bbc9fedca48b978be1c2329ca136c140084b2396dfafe4f8e58` |
| `scenes:biology_park/translator_machine` | `review/chapter-02-batch03-2026-11-17/candidates/C-translator-machine.png` | `ff5704d99d027ea8a86e78b228102826bcceec03b5ae1ba583200a99822e95a3` |
| `scenes:biology_park/planting_machine` | `review/chapter-02-batch03-2026-11-17/candidates/D-planting-machine.png` | `047282bbf1e5189645e5784d9b30278cb5b641a708eeed50f43945017d9b78da` |
| `scenes:biology_park/sorting_conveyor` | `review/chapter-02-batch03-2026-11-17/candidates/E-sorting-conveyor.png` | `fe26ce88586bc207a50c8a9ccc9bcb3ddf30dac1bfd1f9e2468abfdae0167e3b` |
| `scenes:biology_park/planting_hopper` | `review/chapter-02-batch03-2026-11-17/candidates/F-planting-hopper.png` | `5ab29aef160eb59a0d34465782d165c042b6ad8131ac04ad87215b03c33deb3b` |
| `scenes:biology_park/waste_chute` | `review/chapter-02-batch03-2026-11-17/candidates/G-waste-chute.png` | `fa2f9021a7c33f6ff188eff438ef4abec35d9ba0d1a77d805cd2ceb98bbaf498` |


## Addendum — Chapter 2 Batch 4 owner selections, 2026-11-17

Nate approved all six without changes; Art Director PASS A-F. Immutable source `InterstellarHarvest/CYOA@9b0d3a325c947e7c27e2b73b949c6ad70a8ee29a`; final review `ec54699bf15455e1003e8aa41cec008abac1983f`, branch `agent/ch02-art-batch04-reserve-transit`. Exact selected PNGs registered with `tools/sync/register-art.mjs --batch`. Approved, never self-integrated; production asset paths remain null pending Gameplay PMO. All85 previous selected images remain byte-exact. Original generations and processing history preserved.

| Record | Candidate source path | SHA-256 |
|---|---|---|
| `scenes:biology_park/reserve_siding` | `review/chapter-02-batch04-2026-11-17/candidates/A-reserve-siding.png` | `c54cc60a878faaf91edc7e642fb9c854a963bb455a86d6d724d6f2f483e7ae2e` |
| `scenes:biology_park/reserve_tram` | `review/chapter-02-batch04-2026-11-17/candidates/B-reserve-tram.png` | `e17c2d8fd7b569404248d86028b7a7ca4164a3856f36f261654bc941a13a7eaf` |
| `scenes:biology_park/concourse_crash` | `review/chapter-02-batch04-2026-11-17/candidates/C-concourse-crash.png` | `50552704840db6220eff3d588bb4a974d51edcd32a816717803f73b6d97d11f8` |
| `scenes:biology_park/concourse_crash#portraitBackground` | `review/chapter-02-batch04-2026-11-17/candidates/D-concourse-portrait-background.png` | `9f8f3d19d44a6433ef70391118a616d7dd6c8626f43eccda48d55af8fdd1cd80` |
| `portraits:courtesy_conductor:talking` | `review/chapter-02-batch04-2026-11-17/candidates/E-courtesy-conductor-talking.png` | `8c6601db91d262f5a6b362609b878589025cb924c15c0753df268d4f84592e4d` |
| `scenes:biology_park/abandoned_station` | `review/chapter-02-batch04-2026-11-17/candidates/F-abandoned-station.png` | `c9f78d96427d5fce0d1bde3651b90f09fd8d3380a65542378273c2fd1aa803f7` |


## Addendum — Chapter2 Batch5 owner selections,2026-11-17

Nate approved all five without changes;Art Director PASS A-E. Immutable source `InterstellarHarvest/CYOA@a9b3817d0c72d2ed5ba398f1f374b0c3b7befeaf`;final review `3112565df2fd6d2f2f7f72a1ae8d6d9998d14024`,branch `agent/ch02-art-batch05-irrigation-exits`. Registered exact bytes through docs/105 `register-art.mjs --batch`. Approved,not integrated;production paths stay null. All91 prior selected images and original review history preserved.

| Record | Source path | SHA-256 |
|---|---|---|
| `scenes:biology_park/lower_irrigation` | `review/chapter-02-batch05-2026-11-17/candidates/A-lower-irrigation.png` | `8f0df4ad7cbdd73182e5266bb253a8f415c2fbb4536fe908eff544b2902182a8` |
| `scenes:biology_park/public_exit` | `review/chapter-02-batch05-2026-11-17/candidates/B-public-exit.png` | `e47576d21610f3d5f2d85027192e37197cf317ffdabdbe72977bd971ec9a97aa` |
| `scenes:biology_park/maintenance_exit` | `review/chapter-02-batch05-2026-11-17/candidates/C-maintenance-exit.png` | `1417e2700c2d6bf29ef937dc4924e11cfcbdcee65f6daf1ef3710ddd2caed7c7` |
| `scenes:biology_park/agricultural_customs` | `review/chapter-02-batch05-2026-11-17/candidates/D-agricultural-customs.png` | `9bc80696f31efacdbba2babd95abfe460a9fb6158ad8b674299a91744403cdef` |
| `scenes:biology_park/exposition_concourse` | `review/chapter-02-batch05-2026-11-17/candidates/E-exposition-concourse.png` | `8d7f81908f9d65d2c24c042ea928b3a2d3f7497580b217e9fec673591ba575e3` |


## Addendum — Chapter2 Batch6 owner selections,2026-11-17

Nate approved all four without changes;Art Director PASS A-D. Immutable source `InterstellarHarvest/CYOA@db91a0a1e49d308292fa68348bf5d06ee7548417`;final review `4e1ab88a63cf830b829f88d51710eef25e729f95`,branch `agent/ch02-art-batch06-credentials-cargo`. Exact native PNGs registered through docs/105 `register-art.mjs --batch`. All96 prior selected images preserved. All four new production paths stay null;no self-integration. Source generations and processing history retained.

| Record | Source path | SHA-256 |
|---|---|---|
| `items:acting_director_badge#slot` | `review/chapter-02-batch06-2026-11-17/candidates/A-acting-director-badge-slot.png` | `a09dae0d8201b6062c51e4f5cc99c1e49b77240b400e7dbf5107bb805bf56c44` |
| `items:acting_director_badge#inspect` | `review/chapter-02-batch06-2026-11-17/candidates/B-acting-director-badge-inspect.png` | `a6a21d330139af8013d46f80dec7ad278d800d0b1b01c217fb0abd29d9544f3d` |
| `items:certified_seed_canister#slot` | `review/chapter-02-batch06-2026-11-17/candidates/C-certified-seed-canister-slot.png` | `0256464ebb925f1b34fef0a4bc6df7af262289ab9eaa57cea0a7520ffea17998` |
| `items:certified_seed_canister#inspect` | `review/chapter-02-batch06-2026-11-17/candidates/D-certified-seed-canister-inspect.png` | `958cdf2442ed5412efc14f8c9f9f65c90f64f702e3de452be80e3a8e172ed9f7` |


## Chapter2 Batch7 partial final owner approval — 2026-11-17

Nate finally approved A–H without changes. Source InterstellarHarvest/CYOA, branch agent/ch02-art-batch07-treatment-kits, immutable candidate7ea47f63b6bbf86ffa02dd5a3ee2cb5ad5d3065e, final review306aa694295829b6e0a13b25f78ed6b004826ffd. Exact native PNGs registered through docs/105. All100 earlier selected entries/PNGs preserved; total108. Production paths remain null. Asset I explicitly excluded: generated/unselected pending background-only polish and final review. No gameplay integration.

| ID | Record | SHA-256 |
|---|---|---|
| A | `focus:biology_park/public_exit/aid_box_open` | `706686f3d0186b0c5e71fad428bb99e8715ec5a6faa5b4af4e629cc1e067b229` |
| B | `items:botanical_antidote_public#slot` | `d9b51dc71af033bb01e24fc7fa27bea611144312c5ac10a594e532e10aac4961` |
| C | `items:botanical_antidote_public#inspect` | `4e9b94d727195d532f8dfaf2b85b07abc43c5170a11a34604317ce4453b4a0e9` |
| D | `focus:biology_park/maintenance_exit/decontamination_kit_open` | `d14ff669e3fb5f03e8c755a232a80f7064c6d7064a471255174b019a1ff42de8` |
| E | `items:botanical_antidote_maintenance#slot` | `ca1b9ea48ab96d0e2e98171d551a2af50ca95f345c4c9659a483783fb2e213b1` |
| F | `items:botanical_antidote_maintenance#inspect` | `f59a324d74a3a7bd772858a858f9bad95809fbdf83fa16f876563f1a20493c88` |
| G | `focus:biology_park/agricultural_customs/exposure_dispenser_open` | `c57ec1054693cd9e379a91d68cd315d3c0be05b3ab50d098a864dc957615ba4b` |
| H | `items:botanical_antidote_customs#slot` | `da857214a1bf850dbae043d32afa63db2423e57eafe3462186d0d685b9610e19` |


## Chapter2 Batch7 final Customs inspector approval — 2026-11-17

Nate approved the revised I without changes; Art Director PASS. Register items:botanical_antidote_customs#inspect from InterstellarHarvest/CYOA, branch agent/ch02-art-batch07-treatment-kits, final review2711cb1784aa368e790dcdf6992cd23f93eaf1d8, path review/chapter-02-batch07-polish-2026-11-17/candidates/I-customs-antidote-inspect-background-polish-v01.png, exact SHA-25635da940d24401a6964243179ec7c5d336ad3677fd31dce0ef368de63cecc42cc. Original pixel revision5174b3cc5414f18b3971af8bcbb9f7d499eaf90f. Previous108 selected entries/PNGs preserved; total109. A-H approval32971f8743851b1ed6997f629ad1c91076d9962c and narrative correction45b0488af8c0e4539105810b21d0651c1b7f49fa are already final and were not repeated. Batch7 complete; production paths remain null; no gameplay integration.


## Chapter2 Batch8 final Art Director approval — 2026-11-17

All five death-screen illustrations APPROVED UNCHANGED by Art Director/owner. Immutable candidate InterstellarHarvest/CYOA@29cf835db830b527021040b4960a64ab83e3699d, branch agent/ch02-art-batch08-death-aftermaths. Registered byte-exact via docs/105. Prior109 selected entries and image bytes preserved; selected total114. Chapter2 artwork generation and visual selection complete. No polish/regeneration, authored narrative or fatal-popup UI changes. Production paths remain null. Claude Gameplay PMO integration is separate.

| ID | Record | Exact selected SHA-256 |
|---|---|---|
| A | `deathScreens:biology_park/classified_as_compost` | `45ca9322666cd9fc4fc1238f7a3e771f96ea10d3ec49cc35a627090475647a86` |
| B | `deathScreens:biology_park/new_arrival` | `eeef7d902608343eb4b1c2136cc978d14b3dc27f2d924cc085e9e756900e26b5` |
| C | `deathScreens:biology_park/personal_growth` | `8952f6cdaaaf5c9f775516c16fb1d32d848a60b43a4ae25f104ba4075b3a7411` |
| D | `deathScreens:biology_park/reclassified` | `a4c635847abd0d4d11376fd3aa7574728c0dda67709cba7e11be6c1adb5c6ebc` |
| E | `deathScreens:biology_park/site_improvement` | `45212c1a10f88686354a0ae27817c81c6699cf65d3f242e2ef824de0ae7f28ff` |


## Chapter 3 Batch A final Art Director approval — 2026-11-19

Nate issued final Art Director approval of all six Chapter 3 Batch A artworks on 2026-11-19. The exact selected image bytes were registered as **`approved`** with `tools/sync/register-art.mjs --batch` (dry run first; the dry run and the real run touched only these six records). They are approved, **not** integrated. All six production `assetPath` values remain `null` until a separately authorized Gameplay PMO integration. No artwork was regenerated, retouched, upscaled or otherwise changed. Review packages v01–v09 are preserved unchanged. Chapter 3 Batch B has not begun.

Immutable source: `InterstellarHarvest/CYOA-storyboard`, branch `art/ch3-pavilion-batch01-20261118`, commit `a87155bfadad42e0deae3bee2e749963d1459a4b`. Source paths are relative to `tools/prologue-art-lab/assets/review/chapter-03-batch01-2026-11-18/`. Each SHA-256 was verified against the blob at that commit before registration. The A03 hash supersedes a mistyped hash in the first approval handoff; the file and selection (A03 v04) were never in question.

| ID | Selected version | Record | Source path | SHA-256 | Size / alpha |
|---|---|---|---|---|---|
| A01 | v09 | `scenes:pavilion_reboot/restroom_entrance` | `v09-microphone-final-2026-11-19/candidates/CH3-A01-restroom-v09.png` | `117dd9d00b6c9d32b4b153f71aaf51c2546ade70b803d45a748728f8d1a1f8b4` | 314×206 opaque |
| A02 | v04 | `scenes:pavilion_reboot/restroom_entrance#portraitBackground` | `v04/candidates/CH3-A02-restroom-bg-v04.png` | `e4967d1f0e4bc2497fb0ce6e59891d1a25a2e1854b8bf395515cd8d0cc4b5260` | 564×278 opaque |
| A03 | v04 | `portraits:pavilion_attendant:idle` | `v04/candidates/CH3-A03-attendant-idle-v04.png` | `28fdf5523454ea2ccdb397bd4d7006fc1fb8f04109046b7646361692422c3ef2` | 564×278 binary alpha |
| A04 | v07 | `scenes:pavilion_reboot/human_verification_stage` | `v07-native-finishing-2026-11-19/candidates/CH3-A04-verification-v07.png` | `9207bfdc140dd115783adba2f042ce756d51a288c053a3113f9a46f479e6e3c5` | 314×206 opaque |
| A05 | v04 | `scenes:pavilion_reboot/human_verification_stage#portraitBackground` | `v04/candidates/CH3-A05-verification-bg-v04.png` | `beb64cc6e9c3c0dc48f6dbe341e98762556b8e9ef4261fe132c8093c5e63b382` | 564×278 opaque |
| A06 | v04 | `portraits:pavilion_presenter:idle` | `v04/candidates/CH3-A06-presenter-idle-v04.png` | `da33e42a723c8f1a5fe82a2ecaa5cd1e22281caa3ee4abc26db8e81569cd6784` | 564×278 binary alpha |

Public preview copies (byte-identical) are under `assets/selected/pending-integration/`: `scenes/pavilion_reboot/restroom_entrance.png`, `scenes/pavilion_reboot/restroom_entrance/portraitBackground.png`, `portraits/pavilion_attendant/idle.png`, `scenes/pavilion_reboot/human_verification_stage.png`, `scenes/pavilion_reboot/human_verification_stage/portraitBackground.png`, `portraits/pavilion_presenter/idle.png`.

**Unresolved technical limitation (recorded at the Art Director's direction):**

> The six selected assets have passed the documented dimensions, opacity/binary-alpha, preview, composite, hash, and public-browser checks. However, complete original native-grid authorship remains unproven. The source generations were returned at higher resolutions and transferred into the target pixel grids, with some subsequent localized native-pixel corrections. Residual source-derived softness and fine RGB tonal variation may remain. Nate knowingly approves the exact selected image bytes with this limitation documented. Creative approval does not establish original native-grid authorship or waive the distinction between derived and genuinely native-authored artwork.

Native-grid authorship is **not** verified or passed by this registration. The limitation is not a request to regenerate anything.

**Publication status:** this approval is registered on branch `art/ch3-batch-a-approval-registration-20261119`, which is stacked on draft PR #6 (`art/ch3-pavilion-reboot-briefs-20261118`), which is itself stacked on draft PR #5 (`story/ch3-reboot-20261118`). The six records exist only in that reboot dependency chain. The approval is **not live on canonical `main` or on the public Pages site** until PR #5, PR #6 and this registration land on `main` and a Pages deployment is verified.

## Chapter 3 Batch B v03 final Art Director approval — 2026-11-19

Nate explicitly selected and approved **all six Batch B artworks B01–B06 exactly as presented in v03**, pinned to `InterstellarHarvest/CYOA-storyboard@7337e5e550e64a64357666a0fab6f118500913cd` on `art/ch3-pavilion-batch02-20261119`. Creative approval is complete. **Administrative registry registration is pending the separate Claude handoff; gameplay integration is not authorized.** The immutable historical generation galleries retain their original pre-selection labels as provenance, superseded by this owner decision.

| ID | Record | Selected native filename | SHA-256 | Size / alpha |
|---|---|---|---|---|
| B01 | `scenes:pavilion_reboot/arrival` | `CH3-B01-arrival-v03.png` | `37d0b189fda18ad6659b0fae1f214145acd4ec67595c5e5a520917d6a7cbd478` | 314×206 opaque |
| B02 | `scenes:pavilion_reboot/record_printer` | `CH3-B02-record-printer-v03.png` | `1f80f8f17359c07fd24c74741be72bfa6ad941da67bb1622931e3b429bb0a722` | 314×206 opaque |
| B03 | `scenes:pavilion_reboot/record_printer#portraitBackground` | `CH3-B03-record-printer-bg-v03.png` | `46e79ce63fb0bda0af2695393a92c9c7ae064edddedbab0e0f4a5f6e9ad01473` | 564×278 opaque |
| B04 | `scenes:pavilion_reboot/record_scanner` | `CH3-B04-record-scanner-v03.png` | `4afe7d0b1898c1e29443d45aba20614b14951bbf91c40e9508a62dc607fcd1b3` | 314×206 opaque |
| B05 | `scenes:pavilion_reboot/record_scanner#portraitBackground` | `CH3-B05-record-scanner-bg-v03.png` | `9099383613c587c3e2e10bcc33d839f75d2aaf685f20de7e47acc21e04c877ea` | 564×278 opaque |
| B06 | `scenes:pavilion_reboot/paper_emergency` | `CH3-B06-paper-emergency-v03.png` | `ac0f7c44d267dd54897507ae3b8b02959a5b76f4fcd9d0418b77b8fdb777ba7e` | 314×206 opaque |

All filenames above are relative to `tools/prologue-art-lab/assets/review/chapter-03-batch02-2026-11-19/v03-localized-corrections/candidates/`. Every file was verified directly against the git blob at the full selected commit and the published v03 manifest. The owner-decision manifest, exact registry batch and separate Claude instructions are in [docs/113](113_CH3_BATCH_B_APPROVAL_REGISTRATION_HANDOFF_20261119.md).

**Accepted unresolved technical limitation:** complete original native-grid authorship remains **unproven / not passed**, as with Batch A. Source generations were returned at larger dimensions and transferred into target grids, with later localized native-pixel work. Residual source-derived RGB softness and fine tonal variation may remain. Nate approves the exact selected bytes while retaining this limitation. Creative approval does not certify original native-grid authorship and does not request regeneration, retouching or further polish.

No artwork bytes, prior review packages, approved Batch A art, narrative or gameplay were changed by this approval record. The registry batch passed a six-record dry run only; the canonical registry and public selected-preview registration remain Claude's administrative step. Production `assetPath` values stay null. **Do not integrate into gameplay or begin Batch C.**
