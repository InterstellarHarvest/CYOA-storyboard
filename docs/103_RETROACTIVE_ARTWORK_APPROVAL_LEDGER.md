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

**Registration status — 2026-11-19 (Claude, administrative registration completed):** the six approvals above are registered in the canonical registry on branch `art/ch3-batch-b-approval-registration-20261119`, created from canonical `main` 3ac5422. The six selected blobs were extracted only from `7337e5e550e64a64357666a0fab6f118500913cd` and independently checked against `expectedSha256`, their git blob IDs, their dimensions and opacity (8-bit RGB, no `tRNS`) before registration. `tools/sync/register-art.mjs --batch` ran a dry run first, targeting exactly these six records, and then the real registration, without `--integration`. In the staged batch only the local `file` fields changed; `key`, `status` and the full `source` objects are as recorded in docs/113.

| ID | Record | Status | Production `assetPath` | Public selected preview (byte-identical to the pinned source) |
|---|---|---|---|---|
| B01 | `scenes:pavilion_reboot/arrival` | approved | null | `assets/selected/pending-integration/scenes/pavilion_reboot/arrival.png` |
| B02 | `scenes:pavilion_reboot/record_printer` | approved | null | `assets/selected/pending-integration/scenes/pavilion_reboot/record_printer.png` |
| B03 | `scenes:pavilion_reboot/record_printer#portraitBackground` | approved | null | `assets/selected/pending-integration/scenes/pavilion_reboot/record_printer/portraitBackground.png` |
| B04 | `scenes:pavilion_reboot/record_scanner` | approved | null | `assets/selected/pending-integration/scenes/pavilion_reboot/record_scanner.png` |
| B05 | `scenes:pavilion_reboot/record_scanner#portraitBackground` | approved | null | `assets/selected/pending-integration/scenes/pavilion_reboot/record_scanner/portraitBackground.png` |
| B06 | `scenes:pavilion_reboot/paper_emergency` | approved | null | `assets/selected/pending-integration/scenes/pavilion_reboot/paper_emergency.png` |

B03 and B05 are registered as their own `#portraitBackground` records: independent background plates, not foreground composites. The already approved A03 attendant foreground is reused unchanged and was not re-registered. In each record's `notes`, only the stale "NO IMAGE GENERATED OR APPROVED" clause was replaced with the approval and provenance line, as for Batch A. No other artwork record, selected preview, historical review package, narrative, item, route, ending or gameplay field changed.

**The native-grid authorship limitation stated above still stands, unresolved.** Registration does not certify original native-grid authorship. Gameplay integration has not begun, and Chapter 3 Batch C has not begun. The approvals are live on the public storyboard only once this branch merges into `main` and its Pages deployment is verified.

## Chapter 3 Batch C v02 final Art Director approval — 2026-11-19

Nate explicitly selected and approved all eight Chapter 3 Batch C review candidates exactly as mapped in v02 at `InterstellarHarvest/CYOA-storyboard@5e0449b3da84764176f9744f5624a88868f5fdcb` on `art/ch3-pavilion-batch03-20261119`: C01–C07 plus the explicit B07 attendant-alarmed carry-forward. Creative approval is complete. **Canonical administrative registration is pending the separate Claude handoff; gameplay integration and Batch D are not authorized.**

| Candidate | Registry key | Selected native PNG | SHA-256 |
|---|---|---|---|
| CH3-C01-urgency | `scenes:pavilion_reboot/urgency_stage` | `CH3-C01-urgency-v02.png` | `81fb5242df1e7cfec26c58bf6ecd4863e2a3089ea7b9b38b5038c99cc1492898` |
| CH3-C02-urgency-bg | `scenes:pavilion_reboot/urgency_stage#portraitBackground` | `CH3-C02-urgency-bg-v02.png` | `de0a1cf44962ee81294926279d9121260814d7bec4ee89db975669e5a471e319` |
| CH3-C03-locomotion | `scenes:pavilion_reboot/locomotion_stage` | `CH3-C03-locomotion-v02.png` | `1a6927cc2688be5c046efe581ca2ce6a3b2c180237c138cb1e586dc7030a10e6` |
| CH3-C04-surprise | `scenes:pavilion_reboot/surprise_stage` | `CH3-C04-surprise-v02.png` | `da1387f2af4e3331e2cf2311a98052afdecdd0fe041746f30f786452d68f0f45` |
| CH3-C05-surprise-bg | `scenes:pavilion_reboot/surprise_stage#portraitBackground` | `CH3-C05-surprise-bg-v02.png` | `90370ad584d1f7ed72f5738f9380f25d03748f16e9486be9ee4c69930a480770` |
| CH3-C06-presenter-excited | `portraits:pavilion_presenter:excited` | `CH3-C06-presenter-excited-v02.png` | `d5aafddc9792a9e294b5f8793cef4d3c629354911a732a64a4976e1ed9acdd95` |
| CH3-C07-presenter-alarmed | `portraits:pavilion_presenter:alarmed` | `CH3-C07-presenter-alarmed-v02.png` | `4bc10c1b0ceb997d0ae51831f4368a60d35b74a59f8c1e24f1772553d638b887` |
| CH3-B07-attendant-alarmed | `portraits:pavilion_attendant:alarmed` | `CH3-B07-attendant-alarmed-v02.png` | `51c2556b865ede1a997977c66e4f79cc1c0b271334a35aba36ef73555d40a43f` |

The selected native paths and exact provenance are recorded in [docs/116](116_OUT_OF_ORDER_CH3_BATCH_C_APPROVAL_REGISTRATION_HANDOFF_20261119.md), with the machine-readable owner decision and ready eight-record batch. The six unchanged candidates retain their v01 bytes, but are explicitly selected from the v02 paths. Historical gallery labels remain as immutable provenance and are superseded by this owner decision.

**Accepted unresolved limitation:** Complete original native-grid authorship remains unresolved / unproven. Original generators returned oversized rasters. Derived target-grid realizations and precisely documented native-pixel finishing do not prove original full-scene or full-character native-grid authorship. Residual source-derived RGB softness remains. Nate accepts the exact selected bytes with this limitation; no regeneration, filtering, sharpening, resizing, alpha reprocessing or further polish is requested.

The artwork generator independently verified all eight source-commit blobs, hashes, dimensions and alpha, then performed only a successful eight-entry registration dry-run. No real registration, selected-art modification or production path assignment occurred. All production `assetPath` values remain null. Draft PR #13 is updated separately to stage the selected v02 gallery through the protected main-only Pages workflow; no merge or deployment is performed as part of this handoff.

## Chapter 3 later continuity correction review — 2026-11-19

After the v02 selection, Nate requested a further localized v03 environment pass and chose raised control pedestals matching main/portrait cameras. The original v02 approval and hashes above remain preserved. Seven environment revisions, including separate A04/A05 continuity options, are unselected; the three unchanged selected pose foregrounds retain their approval. See [docs/117](117_OUT_OF_ORDER_CH3_V03_CONTINUITY_REVIEW_20261119.md). Defer pending registration and publication until the replacement versions are selected; never mix unselected v03 images into the v02 batch. No approved image bytes, registry, narrative, game integration or Batch D changes.

### Further correction clarification — 2026-11-20

Nate requested v04 wall-plane corrections, clearer pedestal controls and placement of the main presenter to the left/firing side of the cannon. See [docs/118](118_OUT_OF_ORDER_CH3_V04_PERSPECTIVE_REVIEW_20261120.md). This remains an unselected replacement review; prior v02 approval and exact historical bytes are preserved, and the unchanged selected pose foregrounds retain their approval. Pending registration/publication remains deferred; no gameplay integration or Batch D.

## Chapter 3 current v04 environments and retained v02 foregrounds — 2026-11-20

Nate approved the seven exact v04 environments at `7bf1f426f3a1d5dba14e7a1bd56ece86a4d23bdb` and retained the three exact v02 foregrounds at `5e0449b3da84764176f9744f5624a88868f5fdcb`. **A04/A05 v04 explicitly supersede the prior approved versions as current selections. Creative approval is complete.** Earlier approvals, files, hashes and provenance remain in history. This resolves the previous visual-review hold; docs/119 is the current ten-record execution authority. Canonical registration remains the separate Claude administrative step.

| Candidate | Version | Registry key | SHA-256 |
|---|---|---|---|
| CH3-C01-urgency | v04 | `scenes:pavilion_reboot/urgency_stage` | `368134fe2363134d3b63e7a7eae3a7b71b393a9d59484c4b3c456296239a7d2c` |
| CH3-C02-urgency-bg | v04 | `scenes:pavilion_reboot/urgency_stage#portraitBackground` | `7d89b7d7c2ee22e6b324076ce988b3e5520e84be5b4068e79fe8d759ab529714` |
| CH3-C03-locomotion | v04 | `scenes:pavilion_reboot/locomotion_stage` | `be99d790754951bcbcd1c26b94a94ff4e84280f5385735951b0f024b322e13c5` |
| CH3-C04-surprise | v04 | `scenes:pavilion_reboot/surprise_stage` | `8a85f438b734930985140851d38d2d691c8326e71d1aae7891e37b453a03412d` |
| CH3-C05-surprise-bg | v04 | `scenes:pavilion_reboot/surprise_stage#portraitBackground` | `90f29651222b62bca461c0c33f09092290b374fd0cf10094c40267202515e255` |
| CH3-A04-verification-continuity | v04 | `scenes:pavilion_reboot/human_verification_stage` | `8df7e5dd2fffb17449fd43f4d9e7df167d75347efc53b0bde1771fd6d8d001ca` |
| CH3-A05-verification-bg-continuity | v04 | `scenes:pavilion_reboot/human_verification_stage#portraitBackground` | `d09e2a7cf13c6382cd8d726a8852f32cfe359651f4c6c9538f4f7825d41844ef` |
| CH3-C06-presenter-excited | v02 | `portraits:pavilion_presenter:excited` | `d5aafddc9792a9e294b5f8793cef4d3c629354911a732a64a4976e1ed9acdd95` |
| CH3-C07-presenter-alarmed | v02 | `portraits:pavilion_presenter:alarmed` | `4bc10c1b0ceb997d0ae51831f4368a60d35b74a59f8c1e24f1772553d638b887` |
| CH3-B07-attendant-alarmed | v02 | `portraits:pavilion_attendant:alarmed` | `51c2556b865ede1a997977c66e4f79cc1c0b271334a35aba36ef73555d40a43f` |

| Superseded record | Original SHA-256 | Preserved file |
|---|---|---|
| `scenes:pavilion_reboot/human_verification_stage` | `9207bfdc140dd115783adba2f042ce756d51a288c053a3113f9a46f479e6e3c5` | [CH3-A04-verification-selected-before-v04.png](artwork-history/chapter-03/pre-v04-2026-11-20/CH3-A04-verification-selected-before-v04.png) |
| `scenes:pavilion_reboot/human_verification_stage#portraitBackground` | `beb64cc6e9c3c0dc48f6dbe341e98762556b8e9ef4261fe132c8093c5e63b382` | [CH3-A05-verification-selected-before-v04.png](artwork-history/chapter-03/pre-v04-2026-11-20/CH3-A05-verification-selected-before-v04.png) |

The older A04/A05 canonical preview bytes are preserved as documentation attachments with their full canonical and original source provenance. The five earlier v02 environment approvals remain historical, superseded by v04; three foreground selections retain v02 bytes and provenance. Original docs/116 JSON/batch, all earlier ledger content and every review package remain unchanged.

**Accepted unresolved limitation:** Complete original native-grid authorship remains unresolved / unproven. Original generators returned oversized rasters. Derived target-grid realizations and precisely documented native-pixel finishing do not prove original full-scene or full-character native-grid authorship. Residual source-derived RGB softness remains. Nate accepts the exact selected bytes with this limitation; no regeneration, filtering, sharpening, resizing, alpha reprocessing or further polish is requested.

[Current manifest, verification evidence and Claude handoff](119_OUT_OF_ORDER_CH3_CURRENT_APPROVAL_REGISTRATION_HANDOFF_20261120.md). PR #13 is updated to the selected v04 package and mixed-version ten-image authority. No merge/deployment is performed, even after verification. No production paths, gameplay integration or Batch D.

**Registration status — 2026-11-20 (Claude, administrative registration completed):** the ten current selections above are registered in the canonical registry on branch `art/ch3-current-approval-registration-20261120`, created from canonical `main` `d4bae261c93c0b7cd8617aaf0a1e054526df0c0d`. The seven v04 blobs were extracted only from `7bf1f426f3a1d5dba14e7a1bd56ece86a4d23bdb` and the three retained v02 blobs only from `5e0449b3da84764176f9744f5624a88868f5fdcb`. Before registration, each was independently checked against `expectedSha256`, its Git blob ID, its dimensions and its alpha contract: environments are 8-bit RGB with no `tRNS`; foregrounds are 8-bit RGBA with binary 0/255 alpha. `tools/sync/verify-ch3-current-selection.mjs --stage` passed and staged the ten bytes outside the checkout. `tools/sync/register-art.mjs --batch` ran a dry run first, then the real registration, without `--integration`. In the staged batch only the local `file` fields changed; `key`, `status`, `expectedSha256` and the full `source` objects are as recorded in docs/119. The obsolete docs/116 eight-entry batch was not executed; the verifier refuses it.

| ID | Version | Record | Status | Production `assetPath` | Public selected preview (byte-identical to the pinned source) | Change |
|---|---|---|---|---|---|---|
| C01 | v04 | `scenes:pavilion_reboot/urgency_stage` | approved | null | `assets/selected/pending-integration/scenes/pavilion_reboot/urgency_stage.png` | new |
| C02 | v04 | `scenes:pavilion_reboot/urgency_stage#portraitBackground` | approved | null | `assets/selected/pending-integration/scenes/pavilion_reboot/urgency_stage/portraitBackground.png` | new |
| C03 | v04 | `scenes:pavilion_reboot/locomotion_stage` | approved | null | `assets/selected/pending-integration/scenes/pavilion_reboot/locomotion_stage.png` | new |
| C04 | v04 | `scenes:pavilion_reboot/surprise_stage` | approved | null | `assets/selected/pending-integration/scenes/pavilion_reboot/surprise_stage.png` | new |
| C05 | v04 | `scenes:pavilion_reboot/surprise_stage#portraitBackground` | approved | null | `assets/selected/pending-integration/scenes/pavilion_reboot/surprise_stage/portraitBackground.png` | new |
| A04 | v04 | `scenes:pavilion_reboot/human_verification_stage` | approved | null | `assets/selected/pending-integration/scenes/pavilion_reboot/human_verification_stage.png` | authorized replacement |
| A05 | v04 | `scenes:pavilion_reboot/human_verification_stage#portraitBackground` | approved | null | `assets/selected/pending-integration/scenes/pavilion_reboot/human_verification_stage/portraitBackground.png` | authorized replacement |
| C06 | v02 | `portraits:pavilion_presenter:excited` | approved | null | `assets/selected/pending-integration/portraits/pavilion_presenter/excited.png` | new |
| C07 | v02 | `portraits:pavilion_presenter:alarmed` | approved | null | `assets/selected/pending-integration/portraits/pavilion_presenter/alarmed.png` | new |
| B07 | v02 | `portraits:pavilion_attendant:alarmed` | approved | null | `assets/selected/pending-integration/portraits/pavilion_attendant/alarmed.png` | new |

**A04/A05 replacement protection.** Before the two curated previews were overwritten, each was confirmed to hold its documented prior bytes:
- `9207bfdc…e3c5` (Git blob `8cca133e`).
- `beb64cc6…b382` (Git blob `27a928e2`).

Each was also confirmed byte-identical to three copies:
- Its preserved attachment under `docs/artwork-history/chapter-03/pre-v04-2026-11-20/`.
- Its original Batch A source at `a87155bfadad42e0deae3bee2e749963d1459a4b`.
- The v04 gallery's historical reference.

The registry keeps one active record per key; no duplicates were created. The superseded approval text, hash and provenance are retained in each record's `notes` as history, together with the preserved-file path. The Batch A ledger section above is unchanged. No other approved preview was overwritten: the dry run reported eight additions, two replacements and no path clash.

Counts on this branch:
- Preview entries: 128 → 136.
- Statuses: approved 13 → 21, not-started 86 → 78; integrated 111 and reused 5 unchanged.

In each newly approved record's `notes`, only the stale "NO IMAGE GENERATED OR APPROVED" clause was replaced, with the approval, provenance and limitation line. For A04/A05, a current-approval clause was placed before the retained prior-approval text. No narrative, brief, route, choice, check, item, ending, game-integration report or other selected artwork changed. Locked narrative blob `857ffdf1bc9432cf4bbbfd7819f5f430a06d9036` is unchanged.

**The accepted native-grid authorship limitation still stands, unresolved.** Original full-scene and full-character native-grid authorship remains unproven, and source-derived RGB softness remains. Registration acknowledges Nate's approval of the exact bytes; it does not certify native-grid authorship.

Further state:
- Gameplay integration has not begun.
- Main-menu assets are not imported.
- Chapter 3 Batch D has not begun.
- The approvals are live on the public storyboard only after this branch merges into `main` and its Pages deployment is verified. Draft PR #13 (gallery publication proposal) remains separate and unmerged.


## 2026-11-20 — Chapter 3 Batch D owner selection

Nate explicitly approved and selected all nine Batch D artworks exactly as mapped in the v03 manifest at `e65f42c19e54f566819289d2b133be246ede13f5`. **Creative approval is complete.** D01/D04/D06/D07/D08 retain v01, D02/D03/D09 retain v02, and D05 is v03. No further visual approval is required for these exact bytes.

| Candidate | Selected version | Registry key | SHA-256 |
|---|---|---|---|
| CH3-D01-service-exit | v01 | `scenes:pavilion_reboot/service_exit` | `4a736b2d7b5fd7dea50fe9d93fe36e7465674ce0b8e38e7f2d6517fca73df392` |
| CH3-D02-service-exit-bg | v02 | `scenes:pavilion_reboot/service_exit#portraitBackground` | `241bfb8e817cf7c42508c218c188a1ac2706bad2e5f577484ce10a359b9a88e9` |
| CH3-D03-attendant-quiet | v02 | `portraits:pavilion_attendant:quiet` | `7f00208a3a96628f18fd23f079913dcb706e0e220db081d4cb438107f15bdf90` |
| CH3-D04-presenter-relieved | v01 | `portraits:pavilion_presenter:relieved` | `29a349c7bcdfe32d2885709dc91977beb7e3869d2461913cfd89afdacebbda9b` |
| CH3-D05-backstage | v03 | `scenes:pavilion_reboot/backstage` | `aa90896023a59454887e9b3bd5b1745cb8b95a5d9737829119abddd9176f4889` |
| CH3-D06-exterior-exit | v01 | `scenes:pavilion_reboot/exterior_exit` | `76b3232f685fd392f981f0c846382e3ddccd61ed94d44e09ea1bc5cf032c3e8a` |
| CH3-D07-exit-vestibule | v01 | `scenes:pavilion_reboot/exit_vestibule` | `cc2d2ce27e1e2cbf609fcae2210d3c46c57b749e8850be2219ad6de7f7f807c8` |
| CH3-D08-courtesy-stage | v01 | `scenes:pavilion_reboot/courtesy_stage` | `0b413a7b9a669365f114fda8765a242fc3ce00fc9c1ea3bd535c7a2b3d1cdb98` |
| CH3-D09-courtesy-stage-bg | v02 | `scenes:pavilion_reboot/courtesy_stage#portraitBackground` | `b0786ebd4147c6b0e6441838c725751a794db04fa9bcce4341aa1a3a7f1e7623` |

**Accepted limitation:** Nate accepts the documented unresolved/unproven original native-grid authorship limitation and residual source-derived softness. This approval acknowledges exact selected bytes; it does not establish original native-grid authorship or request regeneration, resizing, sharpening, filtering, alpha changes or additional polish.

[Owner selection and verbatim instruction](122_OUT_OF_ORDER_CH3_BATCH_D_SELECTED_ARTWORK_20261120.json) · [Prepared nine-entry Claude batch](122_OUT_OF_ORDER_CH3_BATCH_D_APPROVAL_REGISTRATION_BATCH_20261120.json) · [Verified Claude handoff](122_OUT_OF_ORDER_CH3_BATCH_D_APPROVAL_REGISTRATION_HANDOFF_20261120.md) · [Verification report](122_OUT_OF_ORDER_CH3_BATCH_D_SELECTION_VALIDATION_20261120.json). All nine native files, SHA-256s, Git blobs and dimensions/alpha contracts are verified against the immutable source commit.

**Canonical registration has not been performed.** Per Nate’s explicit instruction, this is a verified approval handoff only: `story/artwork.draft.json`, `story/artwork-preview.json`, curated selected assets and production paths remain unchanged. Any generated/not-started catalogue statuses are an administrative registration backlog, not a pending creative decision. The immutable v01/v02/v03 galleries retain their historical generated/unselected labels; this later owner selection supersedes them without rewriting any historical package. All earlier ledger text and approvals remain intact.

PR #16 remains draft/unmerged at head `0805f4dd6f4c5d6554ef854be1e569e98eee0ee7`, pinned to the same v03 source. CI run `44825495367` completed successfully. CI success does not authorize publication; separate publication authorization is still required. Claude must reconcile the proposal’s pre-registration catalogue/staging assumptions after any future administrative registration and rerun CI before separately authorized publication.

No merge, deployment, gameplay integration, game-repository modification or new art batch is authorized or performed. Stop after the verified handoff.
