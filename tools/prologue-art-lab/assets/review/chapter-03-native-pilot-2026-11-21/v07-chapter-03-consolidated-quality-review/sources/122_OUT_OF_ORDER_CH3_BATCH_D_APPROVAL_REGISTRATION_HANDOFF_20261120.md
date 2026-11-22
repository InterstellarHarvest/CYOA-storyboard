# Out of Order — Chapter 3 Batch D approval and Claude registration handoff

**Nate’s creative approval is complete, 2026-11-20.** All nine selections below are approved for their exact bytes in the v03 mapping at `e65f42c19e54f566819289d2b133be246ede13f5`. The accepted original native-grid authorship limitation remains unresolved/unproven. No further visual selection or polish is required.

**Codex has not performed canonical registration.** This package records the owner decision, independently verifies exact native sources and prepares a future nine-entry Claude batch. The canonical registries, selected assets, production paths, gameplay repository and immutable historical galleries remain unchanged.

[Owner decision and verbatim instruction](122_OUT_OF_ORDER_CH3_BATCH_D_SELECTED_ARTWORK_20261120.json) · [Prepared batch](122_OUT_OF_ORDER_CH3_BATCH_D_APPROVAL_REGISTRATION_BATCH_20261120.json) · [Verification results](122_OUT_OF_ORDER_CH3_BATCH_D_SELECTION_VALIDATION_20261120.json) · [PR #16 CI snapshot](122_OUT_OF_ORDER_CH3_BATCH_D_PUBLICATION_CI_SNAPSHOT_20261120.json).

## Exact approved sources

Repository: `InterstellarHarvest/CYOA-storyboard`. Review branch: `art/ch3-pavilion-batch04-20261120`. Every batch `source.commit` is the full immutable selection source `e65f42c19e54f566819289d2b133be246ede13f5`; this commit contains all nine native files, including retained v01/v02 bytes. Earlier authorship provenance remains in the untouched manifests and generation receipts.

Source manifest: `tools/prologue-art-lab/assets/review/chapter-03-batch04-2026-11-20/v03-clapper-correction/manifest.json`. SHA-256: `d7239e3dddc0cb8ff753e746a74f739e3774b38b5f57a03eadcd75e0ef45b77d`.

| Candidate | Selection | Registry key | Native contract | SHA-256 |
|---|---|---|---|---|
| CH3-D01-service-exit | v01 | `scenes:pavilion_reboot/service_exit` | 314×206 RGB | `4a736b2d7b5fd7dea50fe9d93fe36e7465674ce0b8e38e7f2d6517fca73df392` |
| CH3-D02-service-exit-bg | v02 | `scenes:pavilion_reboot/service_exit#portraitBackground` | 564×278 RGB | `241bfb8e817cf7c42508c218c188a1ac2706bad2e5f577484ce10a359b9a88e9` |
| CH3-D03-attendant-quiet | v02 | `portraits:pavilion_attendant:quiet` | 564×278 RGBA | `7f00208a3a96628f18fd23f079913dcb706e0e220db081d4cb438107f15bdf90` |
| CH3-D04-presenter-relieved | v01 | `portraits:pavilion_presenter:relieved` | 564×278 RGBA | `29a349c7bcdfe32d2885709dc91977beb7e3869d2461913cfd89afdacebbda9b` |
| CH3-D05-backstage | v03 | `scenes:pavilion_reboot/backstage` | 314×206 RGB | `aa90896023a59454887e9b3bd5b1745cb8b95a5d9737829119abddd9176f4889` |
| CH3-D06-exterior-exit | v01 | `scenes:pavilion_reboot/exterior_exit` | 314×206 RGB | `76b3232f685fd392f981f0c846382e3ddccd61ed94d44e09ea1bc5cf032c3e8a` |
| CH3-D07-exit-vestibule | v01 | `scenes:pavilion_reboot/exit_vestibule` | 314×206 RGB | `cc2d2ce27e1e2cbf609fcae2210d3c46c57b749e8850be2219ad6de7f7f807c8` |
| CH3-D08-courtesy-stage | v01 | `scenes:pavilion_reboot/courtesy_stage` | 314×206 RGB | `0b413a7b9a669365f114fda8765a242fc3ce00fc9c1ea3bd535c7a2b3d1cdb98` |
| CH3-D09-courtesy-stage-bg | v02 | `scenes:pavilion_reboot/courtesy_stage#portraitBackground` | 564×278 RGB | `b0786ebd4147c6b0e6441838c725751a794db04fa9bcce4341aa1a3a7f1e7623` |

Five main scenes are opaque 314×206; two portrait backgrounds are opaque 564×278; two foregrounds are transparent 564×278 RGBA with binary alpha. All nine are 8-bit PNGs with zero partial-alpha pixels. Only the native `candidates/*.png` files are registration inputs. Composites, previews, masks, clean plates, generator originals and rejected candidates are excluded.

## Approval and preservation

The new owner decision and ledger appendix supersede historical “generated/unselected” review labels without editing them. v01, v02 close-camera corrections and v03 clapper correction remain immutable, including all earlier candidates and discarded generator attempts. Their 189 files/checksum manifests are independently verified from the source commit and compared with any local copies. No selected art is regenerated or transformed.

At fetched canonical main `5134edb160afaa019e11f872a3b87d3b01b257b0`, all nine keys remain `not-started`, with null production paths and no selected previews; that is an administrative backlog, not incomplete creative approval. The artwork branch carries historical `generated` metadata. This handoff deliberately leaves both registries untouched under Nate’s instruction. On that verified main, future registration should add nine previews: **136 → 145**, with no existing selected-image replacement. If newer main differs, reconcile these same keys and stop on any unexpected conflicting selected hash.

The previous approval-ledger bytes are preserved exactly; only the Batch D owner-decision appendix is added. Chapters 1–3 approved assets, the locked Chapter 3 narrative blob `857ffdf1bc9432cf4bbbfd7819f5f430a06d9036`, all choices/checks/items/endings, and game integration evidence remain unchanged.

## Accepted limitation

Original full-scene/full-character native-grid authorship is unresolved/unproven. Larger generator originals, documented target-grid exports and local native-pixel mask corrections do not establish original native-grid authorship; residual source-derived softness remains. Nate explicitly accepts this for the selected bytes. Do not resize, sharpen, filter, reprocess alpha, regenerate or perform additional finishing on these inputs.

## Claude administrative registration task

The following is a prepared handoff for a separately initiated Claude registration step. **Do not execute registration during this Codex verification task.** The owner’s present instruction is to stop after this verified package; publication, merge, deployment and gameplay remain separate decisions.

1. Read docs/102, docs/103, docs/105 and docs/122. Fetch latest canonical main and the review branch. Create an isolated registration branch from current main; copy only the docs/122 owner records, this verifier and the append-only ledger addition, preserving any newer entries. Do not merge/cherry-pick the generation branch wholesale. Preserve the separately pinned source manifest and all historical packages.
2. Verify the exact selection and batch before any write. The dependency-free verifier reads pinned Git blobs, checks the fixed nine-version/registry-key/hash mapping, validates native PNG contracts, verifies all three review snapshots and confirms the prior ledger prefix. It never calls or imports the registration tool. Optional staging copies only nine exact native images plus a future batch to an empty temporary directory outside the checkout:

   ```sh
   node tools/sync/verify-ch3-batch-d-selection.mjs
   node tools/sync/verify-ch3-batch-d-selection.mjs --stage <empty-temporary-directory>
   ```

3. Only in that separate Claude task, use the staged batch with the existing registration tool, dry-run first and real registration only after verification:

   ```sh
   node tools/sync/register-art.mjs --batch <empty-temporary-directory>/batch.json --dry-run
   node tools/sync/register-art.mjs --batch <empty-temporary-directory>/batch.json
   ```

   `register-art.mjs` does **not** enforce `expectedSha256` itself; independent verifier success is mandatory. Keep all keys, approved statuses, expected hashes and full source objects unchanged. Only staged local `file` fields differ. Do not use `--integration`, invent gameplay paths, or register a composite/background master in place of a selected native image. Production `assetPath` values stay null; registered status is approved, never integrated.
4. Confirm exactly nine current selected previews with matching hashes and pinned source objects, no unrelated modifications and no altered approved image. Reconcile stale generated/not-started annotations only for these nine records; preserve their briefs, accepted limitation, earlier version history and all existing approvals. Run canonical, smoke, sync and relevant Chapter 3 checks, then return a separate registration branch/commit/PR and evidence. No merge, deployment, engine work, game-repository change or next batch.

## PR 16 remains draft and publication is separate

PR #16 is still draft/unmerged at head `0805f4dd6f4c5d6554ef854be1e569e98eee0ee7`, with the v03 gallery pin unchanged at `e65f42c19e54f566819289d2b133be246ede13f5`. Review workflow run [44825495367](https://github.com/InterstellarHarvest/CYOA-storyboard/actions/runs/44825495367) passed, including canonical, sync, timeline, selected-preview and built-site Prologue browser steps. **CI success does not authorize publication.** Keep the PR draft; no merge, workflow dispatch or deploy is performed by this handoff.

The proposal’s catalogue patch and trusted staging helper currently expect pre-registration generated records, including the old unregistered D05 hash. After future canonical registration, PR #16 must be reconciled/rebased against the registered state and its helper checks updated to the approved owner decision without rewriting immutable snapshots or lowering selected statuses. Historical gallery labels should be explained by a later selection receipt outside those snapshots. Rerun CI after that reconciliation. Do not merge the existing generated-status catalogue patch over approved registrations. These are future publication dependencies, not work performed or authorized now; separate publication authorization remains required.

## Verification evidence

The linked report records independent source/SHA-256/Git-blob/PNG checks, all 189 historical package files, exact staged inputs, negative rejection probes, append-only ledger preservation, unchanged canonical sources/assets/older approvals, and PR draft/CI evidence. Temporary staging is not registration. No registration dry-run, registration rehearsal, real registration, merge, deployment or gameplay integration is executed by Codex.

Stop after this verified handoff. All nine images are owner-approved; only administrative registration remains pending.
