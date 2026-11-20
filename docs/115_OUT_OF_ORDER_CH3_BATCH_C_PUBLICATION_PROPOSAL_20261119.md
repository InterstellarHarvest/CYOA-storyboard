# Out of Order — Chapter 3 Batch C review publication proposal

This unmerged proposal would publish the isolated eight-candidate gallery through the canonical `main` Pages workflow. It does not publish from an artwork branch, change the environment deployment allowlist, or import artwork into the canonical registry or game.

- Immutable gallery source: `53358b9df78f72e815cd69ee4128b1c86c08818d`.
- Source branch: `art/ch3-pavilion-batch03-20261119`.
- Review directory: `tools/prologue-art-lab/assets/review/chapter-03-batch03-2026-11-19/`.
- Current local browser review: http://127.0.0.1:8780/tools/prologue-art-lab/assets/review/chapter-03-batch03-2026-11-19/v01/.
- Proposed public URL after a separate merge and successful main deployment: https://interstellarharvest.github.io/CYOA-storyboard/tools/prologue-art-lab/assets/review/chapter-03-batch03-2026-11-19/v01/.

The workflow sparse-checks out only the pinned review directory, checks all supplied PNG/source checksum manifests and the eight candidate hashes, validates generated/unselected metadata, and stages the package byte-for-byte at build time. It does not execute package scripts. It refuses to overwrite an existing site directory. Deployment provenance is written outside the immutable `v01` package. Existing Batch A/B pins and staging remain unchanged. A job guard explicitly restricts deployment to `refs/heads/main`, including manual dispatch.

All eight candidates remain generated/unselected: C01–C07 plus the B07 attendant carry-forward. Asset paths remain null. Original native-grid authorship remains unproven: oversized generation sources, derivative exports, local masks and provenance are retained. Local browser inspection and export QA passed; Nate's visual selection is outstanding.

The owner selected the red-curtain reveal geometry and the portrait's three-button wall panel as the new layout authority. New stage variants share the doorway, two-person restroom sign, three-button panel and separate narrative loudspeaker grille. Front-console placement and active green-button identity correspond between main and close views. Approved earlier artwork, historical packages, narrative, gameplay and the separate `InterstellarHarvest/out-of-order` repository remain unchanged.

Validation before opening the draft: workflow YAML parsed; Batch C validation/staging run locally against the pinned commit; staged gallery byte-compared with source; selected-art canonical drift and storyboard smoke QA passed. No workflow dispatch, merge or deployment was performed.
