# Out of Order — current Chapter 3 approval and Claude registration handoff

**2026-11-20: creative approval is complete.** Nate selected seven exact v04 environments, explicitly superseding A04/A05, and retained three exact v02 foregrounds. This ten-record handoff supersedes the old docs/116 eight-entry execution batch and resolves the subsequent visual-review holds. Preserve those earlier documents and decisions as history. No second visual approval is required.

- Environments: `InterstellarHarvest/CYOA-storyboard@7bf1f426f3a1d5dba14e7a1bd56ece86a4d23bdb`, branch `art/ch3-pavilion-batch03-20261119`, `v04-perspective-corrections/candidates/`.
- Foregrounds: original `5e0449b3da84764176f9744f5624a88868f5fdcb`, same branch, `v02-localized-corrections/candidates/`. Retain their full original provenance as well as their bytes.
- Both are under `tools/prologue-art-lab/assets/review/chapter-03-batch03-2026-11-19/`.

[Current owner manifest and verbatim authorization](119_OUT_OF_ORDER_CH3_CURRENT_SELECTED_ARTWORK_20261120.json) · [Ten-entry batch](119_OUT_OF_ORDER_CH3_CURRENT_APPROVAL_REGISTRATION_BATCH_20261120.json) · [Verification evidence](119_OUT_OF_ORDER_CH3_CURRENT_SELECTION_VALIDATION_20261120.json).

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

## Superseded A04/A05 approval history

Nate explicitly selected v04 continuity replacements for the same two registry keys. The older images remain historically approved with their earlier provenance; they are superseded as current selections. Exact copies of the previous canonical selected previews are archived before any future replacement:

| Superseded record | Original SHA-256 | Preserved file |
|---|---|---|
| `scenes:pavilion_reboot/human_verification_stage` | `9207bfdc140dd115783adba2f042ce756d51a288c053a3113f9a46f479e6e3c5` | [CH3-A04-verification-selected-before-v04.png](artwork-history/chapter-03/pre-v04-2026-11-20/CH3-A04-verification-selected-before-v04.png) |
| `scenes:pavilion_reboot/human_verification_stage#portraitBackground` | `beb64cc6e9c3c0dc48f6dbe341e98762556b8e9ef4261fe132c8093c5e63b382` | [CH3-A05-verification-selected-before-v04.png](artwork-history/chapter-03/pre-v04-2026-11-20/CH3-A05-verification-selected-before-v04.png) |

The current owner manifest retains each old canonical commit/path/Git blob, original source repository/ref/commit/path, old hash, preserved attachment and new replacement hash/source. Original source files also remain in pinned Batch A and historical Batch C references. The attachments are documentation evidence, not gameplay paths or additional active preview records. Claude may replace only these two active curated preview files through the established tool, after verifying their preserved copies.

The five older v02 environment approvals are also preserved in docs/116 and the ledger, superseded by v04. The three foreground selections stay v02. The original docs/116 decision JSON and batch remain byte-identical; the current manifest binds the old decision by SHA-256. Historical generated/unselected labels inside all four galleries remain unchanged and are superseded by this later owner decision outside those snapshots.

## Accepted unresolved limitation

Complete original native-grid authorship remains unresolved / unproven. Original generators returned oversized rasters. Derived target-grid realizations and precisely documented native-pixel finishing do not prove original full-scene or full-character native-grid authorship. Residual source-derived RGB softness remains. Nate accepts the exact selected bytes with this limitation; no regeneration, filtering, sharpening, resizing, alpha reprocessing or further polish is requested.

## Claude task — administrative registration only

1. Fetch latest canonical `main` and the artwork branch. Create an isolated registration branch from current `main`. Bring over docs/119, the two `docs/artwork-history/chapter-03/pre-v04-2026-11-20/` attachments, the verifier below and the append-only ledger/current-status additions. Preserve any newer canonical entries. Do not merge/cherry-pick the generation branch wholesale.
2. Independently verify and stage only the exact ten native inputs. The dependency-free verifier checks pinned Git blobs and SHA-256s, owner mapping, record contracts, binary foreground alpha, retained v02 provenance, old approval JSON and preserved prior A04/A05 sources. It refuses the obsolete eight-entry batch or a wrong expected hash before staging. Supply an empty temporary directory outside the checkout:

   ```sh
   node tools/sync/verify-ch3-current-selection.mjs --stage <empty-temporary-directory>
   node tools/sync/register-art.mjs --batch <empty-temporary-directory>/batch.json --dry-run
   node tools/sync/register-art.mjs --batch <empty-temporary-directory>/batch.json
   ```

3. Keep batch keys, approved statuses, expected hashes and full source objects unchanged; only local staged `file` paths differ. `register-art.mjs` does not enforce `expectedSha256` itself, which is why independent verification is mandatory. **Do not pass `--integration`.** Keep every production `assetPath` null and status approved, never integrated. Register backgrounds separately and native transparent foregrounds, not composites. Let the established tool derive curated storyboard-only preview destinations.
4. At verified main `d4bae261c93c0b7cd8617aaf0a1e054526df0c0d`, expect eight new previews and exactly two authorized A04/A05 replacements: 128 preview records become 136. On newer main, reconcile these same ten keys without changing unrelated previews/records. Verify all ten curated hashes/source objects and both history attachments. Preserve every other selected asset, historical package, narrative and integration report. Reconcile stale generation/provenance annotations only on selected records if needed, without changing briefs or narrative.
5. Run `node tools/sync/check-canon.mjs`, `node tools/storyboard/qa-smoke.mjs`, `node tools/sync/qa-sync.mjs` and relevant Chapter 3 QA. Preserve narrative blob `857ffdf1bc9432cf4bbbfd7819f5f430a06d9036`, all routes, choices, checks, items, endings and game integration evidence. Update administrative completion notes to actual state; retain prior approval history and the accepted limitation.
6. Return a separate registration branch/commit/PR, the ten exact hashes and QA evidence. PR #13 is updated to the complete immutable v04 gallery, retaining all older versions and the selected v02 foregrounds. It remains draft/unmerged. **Do not merge or deploy in this handoff**, even after verification. No direct generation-branch deployment or environment-policy exception.

Stop after administrative registration. No changes to `InterstellarHarvest/out-of-order`, gameplay paths, menu imports, engine integration or Chapter 3 Batch D.

## Verification before handoff

All ten pinned inputs and both archived prior sources pass independent verification. A ten-entry dry run passes. Full registration is rehearsed only in a disposable detached checkout of verified main: eight additions, two replacements, exact curated bytes/provenance, unchanged unrelated selected files and null production paths. Canonical, smoke, sync and Chapter 3 QA pass against that rehearsal. Negative probes reject a tampered hash and the obsolete batch. This rehearsal is not live canonical registration: current branches retain their original registries. See the linked validation report for exact evidence.
