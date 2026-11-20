# Out of Order — Chapter 3 Batch C selected v02 publication proposal

Nate selected and approved all eight v02 candidates on 2026-11-19 and accepted the documented unresolved native-grid authorship limitation. Creative approval is complete. The separate Claude registration handoff is [docs/116](116_OUT_OF_ORDER_CH3_BATCH_C_APPROVAL_REGISTRATION_HANDOFF_20261119.md); canonical registry administration remains pending. This publication proposal does not register or integrate artwork.

- Immutable selected/gallery source: `5e0449b3da84764176f9744f5624a88868f5fdcb`.
- Generation branch: `art/ch3-pavilion-batch03-20261119`.
- Review directory: `tools/prologue-art-lab/assets/review/chapter-03-batch03-2026-11-19/`.
- Selected version: `v02-localized-corrections/`, including six byte-identical v01 carry-forwards explicitly selected from their v02 paths.
- Proposed selected v02 gallery after a separate merge and successful main deployment: https://interstellarharvest.github.io/CYOA-storyboard/tools/prologue-art-lab/assets/review/chapter-03-batch03-2026-11-19/v02-localized-corrections/.
- Proposed owner-selection receipt: https://interstellarharvest.github.io/CYOA-storyboard/tools/prologue-art-lab/assets/review/chapter-03-batch03-2026-11-19/selection.html.

The workflow sparse-checks out only the complete pinned review directory, verifies both v01/v02 PNG and source checksum manifests, checks the exact eight native v02 hashes/paths against Nate's owner-decision manifest, and stages the gallery byte-for-byte at build time. It does not execute gallery code or overwrite existing site directories. Existing Batch A/B pins and staging remain unchanged. Deployment remains restricted to `refs/heads/main`, including manual dispatch; no environment-policy or allowlist change is proposed.

Historical generated/unselected labels inside v01/v02 remain unchanged. The later owner decision is published as `owner-selection.json` and a readable `selection.html` outside both immutable version directories. Deployment provenance also stays outside them and reports how many canonical previews currently match the exact selections. Copying the approval receipt does not administratively register artwork or modify source PNGs. Both historical version directories are byte-compared after staging and after adding the receipt.

All eight selections are approved: C01–C07 plus the explicit B07 attendant carry-forward. Production asset paths remain null. Original native-grid authorship remains unresolved/unproven and accepted by Nate; source-derived RGB softness may remain. No further polish, regeneration, filtering or alpha processing is requested.

Validation: eight selected-commit blobs independently hashed and size/mode/alpha checked; six unchanged candidates byte-compared with v01; precisely eight registration records passed dry-run without a real registration. Workflow YAML and the actual revised staging step are validated locally against the full selected commit, including both historical packages and selection metadata. Canonical drift, storyboard smoke and sync QA pass. The approval ledger preserves every prior byte and appends only the Batch C owner decision.

PR #13 remains draft/unmerged. No workflow dispatch, Pages deployment, direct generation-branch deployment, game repository change, gameplay integration or Chapter 3 Batch D is performed by this handoff.
