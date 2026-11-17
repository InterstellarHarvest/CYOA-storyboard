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
