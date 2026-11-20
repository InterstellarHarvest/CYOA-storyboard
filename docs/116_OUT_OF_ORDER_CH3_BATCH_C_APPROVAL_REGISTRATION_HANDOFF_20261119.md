# Out of Order — Chapter 3 Batch C approval and Claude registration handoff

**Nate selected and approved all eight v02 candidates on 2026-11-19. Creative approval is complete.** Canonical registry administration is the separate Claude task below; no second visual approval is required.

Immutable source: `InterstellarHarvest/CYOA-storyboard`, branch `art/ch3-pavilion-batch03-20261119`, commit **`5e0449b3da84764176f9744f5624a88868f5fdcb`**.

All selected paths are under `tools/prologue-art-lab/assets/review/chapter-03-batch03-2026-11-19/v02-localized-corrections/candidates/`. Select native candidate PNGs only, never a raw source, donor, preview, composite, mask or comparison. The six unchanged candidates retain their v01 bytes, but their selected provenance is the explicit v02 path at this full commit.

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

Machine-readable authority and contracts: [selected artwork](116_OUT_OF_ORDER_CH3_BATCH_C_SELECTED_ARTWORK_20261119.json). Exact registration input: [eight-entry batch](116_OUT_OF_ORDER_CH3_BATCH_C_APPROVAL_REGISTRATION_BATCH_20261119.json). B07 is the explicit Batch B carry-forward; it is outside Batch B's already approved B01–B06 and is approved by this eight-image decision.

## Owner authorization

> I approve and select all eight Chapter 3 Batch C review candidates exactly as mapped in the v02 package at commit `5e0449b3da84764176f9744f5624a88868f5fdcb`.
>
> Selections:
>
> - C01 urgency — v02
> - C02 urgency background — v02
> - C03 locomotion — v02
> - C04 surprise — v02
> - C05 surprise background — v02
> - C06 presenter excited — v02
> - C07 presenter alarmed — v02
> - B07 attendant alarmed — v02
>
> The six unchanged candidates retain their v01 bytes.
>
> I accept the documented unresolved native-grid authorship limitation.
>
> Proceed with the Claude approval-registration handoff. Update draft PR #13 to publish the correct v02 gallery through the protected `main` Pages workflow.
>
> Preserve historical packages and previously approved artwork. Do not integrate anything into gameplay or begin Chapter 3 Batch D.

This owner decision supersedes generated/unselected labels in the historical galleries. Preserve those snapshots verbatim. The images are approved; only registry administration remains pending.

## Accepted technical limitation

Complete original native-grid authorship remains unresolved / unproven. Original generators returned oversized rasters. Derived target-grid realizations and precisely documented native-pixel finishing do not prove original full-scene or full-character native-grid authorship. Residual source-derived RGB softness remains. Nate accepts the exact selected bytes with this limitation; no regeneration, filtering, sharpening, resizing, alpha reprocessing or further polish is requested.

## Claude task — approval registration only

1. Read docs/102, docs/103, docs/105 and this handoff. Fetch current canonical storyboard `main` and the generation branch. Create an isolated registration branch from current `main`. Bring over these three docs/116 files and append the Batch C owner-decision ledger section if not already present; preserve any newer canonical entries.
2. Extract exactly the eight selected PNG blobs from `5e0449b3da84764176f9744f5624a88868f5fdcb` into temporary staging. Independently verify `expectedSha256`, Git blob identity, dimensions, PNG mode and alpha. `register-art.mjs` computes hashes but **does not enforce `expectedSha256`**. In a staged batch, change only local `file` fields. Preserve each `key`, `status: approved` and complete original `source` object, including the v02 source path.
3. Dry-run the eight-entry batch and inspect that precisely these eight records are targeted; then perform administrative registration:

   ```sh
   node tools/sync/register-art.mjs --batch <staged-batch.json> --dry-run
   node tools/sync/register-art.mjs --batch <staged-batch.json>
   ```

   **Do not pass `--integration`.** Leave every production `assetPath` null. Status is `approved`, never `integrated`. C02/C05 are separate `#portraitBackground` records; C06/C07/B07 are transparent pose foregrounds, not composites. Let the established tool derive storyboard-only selected preview destinations.
4. Verify exactly eight new preview records with the selected SHA-256s and complete provenance. Preserve all prior preview entries and selected bytes, especially Batch A and Batch B. Preserve both historical Batch C packages byte-for-byte. Update administrative registration notes to actual completion without removing the accepted native-grid limitation.
5. Run `node tools/sync/check-canon.mjs`, `node tools/storyboard/qa-smoke.mjs`, `node tools/sync/qa-sync.mjs`, and relevant Chapter 3 QA. Preserve narrative blob `857ffdf1bc9432cf4bbbfd7819f5f430a06d9036`, all routes/checks/items/endings and the game integration report.
6. Commit the isolated registration changes and return its branch, commit/PR, eight hashes and QA evidence. Coordinate with draft PR #13, which stages the selected v02 gallery through protected `main` only. No direct artwork-branch deployment or environment allowlist exception. Publication does not constitute gameplay integration.

Do not merge/cherry-pick the artwork-generation branch wholesale into `main`. Extract only the selected blobs and approval documentation. The separately reviewed Pages proposal remains in PR #13. Do not import gallery scripts, donor images, alternative versions or proof composites as selected artwork.

**Stop after approval registration.** Do not modify `InterstellarHarvest/out-of-order`, assign gameplay paths, change game build/integration reports, integrate menu art or begin Chapter 3 Batch D.

## Handoff validation

- All eight native candidate files independently verified against selected-commit Git blobs, exact SHA-256s, dimensions, RGB/RGBA modes and alpha. Three main scenes are 314×206; two backgrounds and three transparent foregrounds are 564×278. Foreground alpha is exactly 0/255.
- Six unchanged selected candidates independently byte-compared with v01. All selected provenance remains v02.
- Eight-entry registration dry-run passed. **No real registration was performed by the artwork generator.** Canonical registry and selected preview files remain unchanged.
- Original v02 technical/browser/canonical QA and all pixel masks remain at the selected commit. No PNG or historical review file was changed by this handoff.
- PR #13 pins the exact selected source commit and preserves both v01/v02, with owner approval metadata outside both historical versions. It remains draft/unmerged; no deployment was run.

## Later owner correction request — registration execution deferred

Nate subsequently requested the v03 continuity corrections documented in [docs/117](117_OUT_OF_ORDER_CH3_V03_CONTINUITY_REVIEW_20261119.md). Preserve the v02 approval record above and its exact selected bytes. Defer pending Batch C registration/publication until the replacement review is resolved; do not substitute unselected v03 images into the approved v02 batch. The unchanged selected foreground poses retain their approval. No gameplay integration or Batch D.
