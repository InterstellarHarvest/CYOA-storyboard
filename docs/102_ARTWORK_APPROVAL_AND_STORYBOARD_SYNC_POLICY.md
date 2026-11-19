# Artwork approval and storyboard synchronization policy

**Owner ruling — 2026-11-16.** Applies retroactively to Out of Order's Prologue and Chapters 1–2, and prospectively to Chapter 3 and later work.

## Source of truth and production flow

The public `InterstellarHarvest/CYOA-storyboard` repository is the canonical creative authoring and review source.

1. Story Director and owner approve narration, choices, flag/item consequences, and art briefs. Commit and publish the narrative and artwork requirements to `CYOA-storyboard/main` after approval.
2. Codex generates artwork from the current storyboard requirements; candidates may be revised in isolated branches.
3. ChatGPT Art Director and owner select the artwork to use. **Selection and actual use are approval evidence, even if nobody updated the JSON status at the time.** Branch location is irrelevant.
4. Gameplay PMO consumes a pinned revision of canonical storyboard story and art data, integrates the selected assets, runs validation, records build provenance, and reconciles public storyboard metadata as an integral part of its work.
5. Public Pages deployment must complete successfully. The storyboard must show what is written, what art was selected, and what is in the game.

## Retroactive approval rule

**Any artwork that was generated, selected for use, and actually used in the project is deemed owner-approved.** The missing approval-state entry in the storyboard is an administrative omission, not evidence of a pending creative decision. This rule holds whether the selected artwork is recorded in `main`, a review branch, a draft PR, or another development branch.

For previously authored or integrated work, Gameplay PMO must audit selected files/references and update the public art registry:

- `not-started`: no selected generated candidate.
- `generated`: a candidate exists, but it has not been selected/used.
- `approved`: selected for use, including a documented accepted candidate whose game integration has not yet occurred.
- `integrated`: the selected, therefore approved artwork is actually referenced by a working game build. This supersedes `approved` as the current status; no duplicate approval gate is needed.
- `reused`: a previously approved image legitimately reused for another scene/pose.

**Never classify a selected or actively used image as awaiting approval solely because its prior art registry field says `generated` or `not-started`.** Conversely, mere file existence or inclusion in a candidate gallery does not establish selection/use.

Preserve hashes, filenames, exact source paths, image dimensions, state variants and review provenance where available. When two candidate variants exist, determine the actually selected file before recording status; do not choose a replacement based on recency.

## What to reconcile now

- Audit all selected/used Prologue and Chapter 1 assets; Chapter 1 integrated PR #10 artwork should be marked `integrated` if verified as game referenced, even though PR is still draft.
- Inspect all existing Chapter 2 game worktrees, commits, review records, and locally selected art. Selected/accepted work should become `approved` or `integrated` as appropriate. Do not require another artistic sign-off for a file that was already selected/used.
- Make source image previews available on the public storyboard without uploading unrelated working material.
- Do not override verified Chapter 1 story corrections, Chapter 2 routes, or newer Chapter 3 co-written story decisions.
- Preserve all 67 pending Chapter 3 art prompts as `not-started` until a candidate is generated and selected.
- Add a sync/QA guard so future integration cannot silently leave the public artwork catalog behind.

## Separation of responsibilities

- ChatGPT Story Director: works with owner on narrative, publishes approved story and art requirements to public storyboard.
- Codex: produces technical artwork candidates based on storyboard files, does not approve its own unselected alternatives.
- ChatGPT Art Director and owner: review new artwork and select the final candidate.
- Claude Gameplay PMO: uses canonical story exports and selected art, implements gameplay, confirms QA, and ensures public metadata matches actual selection/integration.

**Do not require another approval ceremony for already-used legacy artwork.** This ruling supersedes older notes suggesting owner visual approval is still pending for such selected and used files. It does not authorize unselected variants or new story content.
