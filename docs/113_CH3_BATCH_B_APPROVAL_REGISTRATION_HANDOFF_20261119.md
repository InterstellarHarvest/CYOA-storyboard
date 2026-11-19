# Chapter 3 Batch B — Nate's approval and Claude registration handoff

**Owner decision: 2026-11-19. All six v03 artworks are selected and approved.** Creative approval is complete. The remaining work is administrative approval registration in the canonical storyboard, with no gameplay integration or Batch C work.

## Immutable selection

- Repository: `InterstellarHarvest/CYOA-storyboard`.
- Generation branch: `art/ch3-pavilion-batch02-20261119`.
- Selected source commit: **`7337e5e550e64a64357666a0fab6f118500913cd`**.
- [Selected v03 gallery](https://interstellarharvest.github.io/CYOA-storyboard/tools/prologue-art-lab/assets/review/chapter-03-batch02-2026-11-19/v03-localized-corrections/).
- Source path prefix: `tools/prologue-art-lab/assets/review/chapter-03-batch02-2026-11-19/v03-localized-corrections/candidates/`.

| ID | Registry key | Selected filename | SHA-256 | Dimensions / alpha |
|---|---|---|---|---|
| B01 | `scenes:pavilion_reboot/arrival` | `CH3-B01-arrival-v03.png` | `37d0b189fda18ad6659b0fae1f214145acd4ec67595c5e5a520917d6a7cbd478` | 314×206 opaque |
| B02 | `scenes:pavilion_reboot/record_printer` | `CH3-B02-record-printer-v03.png` | `1f80f8f17359c07fd24c74741be72bfa6ad941da67bb1622931e3b429bb0a722` | 314×206 opaque |
| B03 | `scenes:pavilion_reboot/record_printer#portraitBackground` | `CH3-B03-record-printer-bg-v03.png` | `46e79ce63fb0bda0af2695393a92c9c7ae064edddedbab0e0f4a5f6e9ad01473` | 564×278 opaque |
| B04 | `scenes:pavilion_reboot/record_scanner` | `CH3-B04-record-scanner-v03.png` | `4afe7d0b1898c1e29443d45aba20614b14951bbf91c40e9508a62dc607fcd1b3` | 314×206 opaque |
| B05 | `scenes:pavilion_reboot/record_scanner#portraitBackground` | `CH3-B05-record-scanner-bg-v03.png` | `9099383613c587c3e2e10bcc33d839f75d2aaf685f20de7e47acc21e04c877ea` | 564×278 opaque |
| B06 | `scenes:pavilion_reboot/paper_emergency` | `CH3-B06-paper-emergency-v03.png` | `ac0f7c44d267dd54897507ae3b8b02959a5b76f4fcd9d0418b77b8fdb777ba7e` | 314×206 opaque |

Every selected PNG was independently read from the git blob at the full source commit, hashed, dimension/opacity checked and compared byte-for-byte with the working copy. Select the native candidate PNGs above, never a preview, comparison, donor, composite or raw generation. B01's bytes are unchanged from v02; its selected provenance is nevertheless the explicit v03 file at this source commit.

The machine-readable owner decision, full source paths, SHA-256s, git blob IDs and contracts are in [113_CH3_BATCH_B_SELECTED_ARTWORK_20261119.json](113_CH3_BATCH_B_SELECTED_ARTWORK_20261119.json). The ready registration batch is [113_CH3_BATCH_B_APPROVAL_REGISTRATION_BATCH_20261119.json](113_CH3_BATCH_B_APPROVAL_REGISTRATION_BATCH_20261119.json).

## Owner authorization

> I approve and select all six Chapter 3 Batch B artworks exactly as presented in v03: B01, B02, B03, B04, B05 and B06.
>
> Source commit: `7337e5e550e64a64357666a0fab6f118500913cd`.
>
> Record the unresolved original native-grid authorship limitation, as with Batch A.
>
> Proceed with the separate Claude approval-registration handoff, preserving the exact selected bytes. Do not integrate into gameplay or begin Batch C.

This final selection supersedes the generation-time `generated/unselected` labels in the immutable historical review snapshots. Those snapshots stay unchanged as provenance; the owner decision is now **approved**, with canonical registry administration pending Claude. No second artistic approval is required.

## Accepted unresolved technical limitation

Complete original native-grid authorship remains **unproven / not passed**, as with Batch A. Original generations were returned above the logical dimensions and transferred into target grids; later localized native-pixel corrections and compositing do not establish original full-scene grid authorship. Residual source-derived RGB softness and tonal variation may remain. The additional v03 transparent donor was returned at **1548×1016**, retained unchanged with its source record.

Nate knowingly approves the exact selected bytes with this limitation documented. Creative approval does not certify original native-grid authorship. This is an accepted provenance limitation, not a request for regeneration, resampling, palette filtering, sharpening, retouching, new alpha processing or further polish. Carry it into the approval ledger and the final registration handoff.

## Claude task — approval registration only

You are Claude handling Chapter 3 Batch B's separate approval-registration step. Read docs/102, docs/103, docs/105 and this handoff. Record these six already approved selections using the established `tools/sync/register-art.mjs` pipeline. Gameplay integration and Batch C are out of scope.

1. Fetch the generation branch and verify that the pinned source commit exists. Create an isolated registration branch from current canonical `main`. Bring over this handoff, its selection/batch JSON and the new Batch B owner-decision ledger section. Preserve any newer canonical ledger entries.
2. Extract only the six selected PNG blobs from `7337e5e550e64a64357666a0fab6f118500913cd` into a temporary staging directory. Verify each against `expectedSha256` before registration. The registration tool computes hashes but does **not** enforce the extra `expectedSha256` field itself. In a staged copy of the batch JSON, change only each `file` field to the staged filename; keep `key`, `status: approved` and the complete original `source` object unchanged.
3. Run the six-entry batch with `--dry-run`, inspect that only the six listed records are targeted, then run the real batch. Do not pass `--integration`.

   ```sh
   node tools/sync/register-art.mjs --batch <staged-batch.json> --dry-run
   node tools/sync/register-art.mjs --batch <staged-batch.json>
   ```

4. Let the existing tool derive curated public preview destinations under `assets/selected/`. These are storyboard previews, not invented production paths. Keep all six production `assetPath` values **null**, with status **approved**, never `integrated`. Register B03/B05 as their own `#portraitBackground` records. Reuse the already approved A03 foreground unchanged; do not register a composite as a selected background.
5. Verify every curated selected copy has the exact expected SHA-256 and source provenance. Confirm all pre-existing selected images and preview entries are unchanged and the only new preview entries are these six. Update the ledger addendum's administrative status to the actual registered state, retaining the full accepted native-grid limitation.
6. Run canonical checks: `node tools/sync/check-canon.mjs`, `node tools/storyboard/qa-smoke.mjs`, and `node tools/sync/qa-sync.mjs`. Preserve the approved narrative blob `857ffdf1bc9432cf4bbbfd7819f5f430a06d9036`, dialogue, routes, checks, items, endings, and all earlier approved assets.
7. Commit the isolated registration changes and provide a registration PR/commit, six exact hashes, QA results and the distinction between registration and game integration. If canonical publication is performed under the PMO's existing authority, use canonical `main`'s Pages workflow and verify the public selected previews. Preserve the existing review galleries and their bytes.

**Do not merge or cherry-pick the generation branch wholesale into main.** Its `.github/workflows/pages.yml` is an intentionally review-only deployment variant and must not enter canonical main. Extract selected blobs and the approval handoff/ledger additions instead. Do not copy generator donors, proof composites or alternative versions as selected art.

**Stop after approval registration.** Do not touch the private gameplay repository, assign production paths, update integration reports, begin engine imports or start Batch C.

## Handoff validation already completed

- Exact immutable source bytes, dimensions and opacity verified for all six selected files.
- Registration tool dry-run succeeds for precisely six approved records; no real registration has been run by the artwork generator.
- v03 technical/public QA remains at the selected source commit: exact 4× main previews, binary foreground anchoring, zero unexpected changes outside localized masks, and 388 downloaded public file hashes verified.
- This handoff changes only approval documentation and ledger additions. All historical review files, selected candidate bytes, approved Batch A images and current production files remain unchanged.
