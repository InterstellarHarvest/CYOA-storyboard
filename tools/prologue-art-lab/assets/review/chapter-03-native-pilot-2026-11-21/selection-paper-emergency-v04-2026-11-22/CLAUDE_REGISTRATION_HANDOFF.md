# Claude registration handoff for selected Paper Emergency v04

Nate has explicitly selected and approved the exact v04 localized repair. Creative approval is complete. This handoff prepares **one administrative registration**, on a separate registration branch from the latest canonical `main`. Codex has performed verification and dry runs only; the canonical preview and notes still describe v03.

## Exact selected input

- Repository: `InterstellarHarvest/CYOA-storyboard`
- Record: `scenes:pavilion_reboot/paper_emergency`
- Version: **v04 localized repair**
- Source branch: `art/ch3-native-pilot-20261121`
- Immutable source commit: `d1600a34a58497b4886518c6aa9feeaa205d8426`
- Source path: `tools/prologue-art-lab/assets/review/chapter-03-native-pilot-2026-11-21/v04-paper-emergency-localized-repair/candidate/CH3-B06-paper-emergency-local-v04.png`
- SHA-256: `93a48082124600b1afeb45e5ea54856bf253e858e55111295e9d9c26919bc978`
- Native contract: **314×206, 8-bit RGB, opaque**, zero transparent/partial-alpha pixels.
- Future catalogue status: **approved**, never integrated in this task. Keep production `assetPath` null.

[Immutable owner selection](selection-manifest.json) · [Verbatim decision excerpt](OWNER_SELECTION_VERBATIM.txt) · [One-record batch](registration-batch.json) · [Independent verifier](verify-selection.mjs) · [Standalone ledger addendum](APPROVAL_LEDGER_ADDENDUM.md)

## Preserve v03 and all history

The previous B06 v03 approval remains historically valid, superseded as the current creative selection by this v04. Its hash is `ac0f7c44d267dd54897507ae3b8b02959a5b76f4fcd9d0418b77b8fdb777ba7e`; the exact old canonical bytes and original source-commit bytes are retained here and match. Do not alter or delete the old source, earlier approvals, or any immutable v01–v04 review files.

Historical generated/unselected labels inside the v04 snapshot remain unchanged. This later owner decision supersedes them for the selected file. Original full-scene native-grid authorship remains unresolved/unproven; the accepted source-derived limitation must remain in the new record notes.

## Separate Claude execution

1. Fetch the latest canonical `main` and review branch. Create a new isolated registration branch from that latest `main`. Bring over this receipt, verifier and ledger addendum as needed; do not merge the artwork branch wholesale. Make the pinned source commit available locally without checking out or modifying it.
2. Check the target still has the expected v03 preview hash, approved status and null production path. If it is already v04, verify the exact completed registration and avoid a duplicate operation. If another hash/status/path appears, reconcile before writing; never overwrite an unexpected newer selection.
3. Independently verify and stage into an **empty temporary directory outside the checkout**. The verifier reads the pinned Git blob, validates exact source/key/hash and PNG contracts, checks the old source, and stages only the selected native PNG plus a one-record batch. It does not import or call registration.

   ```sh
   node <receipt-directory>/verify-selection.mjs --stage "$CH3_SELECTION_STAGE"
   node <receipt-directory>/verify-selection.mjs --batch "$CH3_SELECTION_STAGE/registration-batch.json"
   node tools/sync/register-art.mjs --batch "$CH3_SELECTION_STAGE/registration-batch.json" --dry-run
   ```

4. **Only in that separate Claude registration task**, after verification and dry run, apply the same one-record staged batch:

   ```sh
   node tools/sync/register-art.mjs --batch "$CH3_SELECTION_STAGE/registration-batch.json"
   ```

   Do not use `--integration`. Keep the staged entry’s key, approved status, expected hashes and full source object unchanged. Only its local `file` path differs. `register-art.mjs` does not enforce `expectedSha256` itself, so independent verification immediately before using the batch is mandatory.
5. Replace only the existing curated Paper Emergency preview bytes through the registration tool. Update **only this record’s notes**, using [future-record-notes.txt](future-record-notes.txt) as the prepared text while preserving any newer legitimate context. Retain the old approval/source in the historical receipt and notes. No brief, narrative, dimensions, item, route, flag, other scene, portrait, production path or integration report change is authorized.
6. Append the standalone ledger addendum to `docs/103_RETROACTIVE_ARTWORK_APPROVAL_LEDGER.md` at most once, preserving every prior byte and every other approval. Preserve the existing ledger if the same addendum is already present. Selection receipt/status is approved even while gameplay integration remains absent.
7. Verify exactly one preview record changes to the selected hash/source, the selected PNG is byte-identical, status is approved, production path remains null, other preview/image hashes remain unchanged, and story/game integration data is untouched. Run canonical, storyboard smoke, sync and relevant Chapter 3 checks; record actual results. Return a separate branch/commit and reviewable diff. **No main merge, Pages deployment or gameplay integration without separate authorization.**

## Codex validation scope

The root prepared batch and independently staged batch were exercised with `--dry-run` only. The native input, expected hashes, dimensions and opacity were independently verified. All preexisting repository files remain unchanged, including the canonical registries, current v03 preview, earlier ledger and other Chapter 3 approvals. No real registration or registration rehearsal occurred.

[Independent verification](qa/independent-verification.json) · [Direct batch dry run](qa/registration-dry-run.txt) · [Staged handoff validation](qa/staged-handoff-validation.json) · [Complete preservation checks](qa/preservation.json)
