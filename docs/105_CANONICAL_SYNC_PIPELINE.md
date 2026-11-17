# 105 — Canonical storyboard pipeline: how to publish, select, integrate and verify

**Status: in force from 2026-11-16.** This implements the production workflow and the artwork ruling in docs/102 and docs/103. Read this first in any new ChatGPT, Codex or Claude session.

## The one rule

**This repository is canon.** Narrative, choices, endings, items, conditions, dice checks, artwork briefs, artwork selections and approval states are edited here and nowhere else.

The game (`InterstellarHarvest/CYOA`, private) consumes a **pinned revision** of this repository. Its `story/` folder is a generated, read-only projection. Nothing in the game writes story data back here. The game publishes only one thing here: *evidence of what a real build uses*.

## Files

| File | Who writes it | Does the game read it? | What it is |
|---|---|---|---|
| `story/storyboard-manifest.json`, `story/chapters/*.json`, `story/items.draft.json` | Story Director + owner | **yes** (runtime fields only) | canonical narrative |
| `story/artwork.draft.json` | Story Director (briefs), Art Director / owner (selections), PMO (integrated) | **yes** (paths + status) | artwork requirements and status |
| `story/storyboard-layout.json` | anyone (viewer layout) | copied, never read | card positions |
| `story/sync-contract.json` | PMO, when a field is added | used by the projection | runtime fields vs storyboard-only fields |
| `story/artwork-preview.json` + `assets/selected/**` | `tools/sync/register-art.mjs` | no | curated public copies of **selected** art, with provenance |
| `story/game-integration.json` | the game's `sync.js publish` | no | the exact images one game build uses |

### Storyboard-only fields

`notes`, `storyboardNextChapter`, `deathPopup`, `endingArt`, `displayGroup`, `missingReason`, and the others listed in `story/sync-contract.json`. The game projection strips them.

A field that is in neither list fails `check-canon` here, and fails the game pull. **Add a new annotation to `storyboardOnlyFields` in the same commit that introduces it.**

## Statuses

| Status | Meaning | Who sets it |
|---|---|---|
| `not-started` | no selected image | — |
| `generated` | candidates exist; none selected | Codex (optional) |
| `approved` | **selected for use = creative approval complete** | `register-art.mjs` on the owner / Art Director's selection |
| `integrated` | approved **and** used by a working game build | the game's `sync.js publish` |
| `reused` | approved art reused in another context | catalog |

Rules:

- A status is never lowered by the tools.
- `check-canon` fails if any previewed (selected) record regresses to `generated`, `not-started` or `prompted`.
- `check-canon` fails if a record says `integrated` but the latest game report does not use it.
- **Never regenerate or re-approve selected art** unless the owner explicitly asks for a revision.

## Operations

### 1. Creative publishing (Story Director)

1. Edit `story/**`. The viewer's Export buttons produce the JSON.
2. Run `node tools/sync/check-canon.mjs`. It checks:
   - all required chapters are present;
   - every route resolves;
   - every field is declared;
   - statuses are valid.
3. Commit to `main`. Pages deploys only if `check-canon` and the smoke QA pass.

You do not need to wait for game integration.

### 2. Art publishing (Art Director / owner selection, any session)

```
node tools/sync/register-art.mjs --key scenes:biology_park/formal_entrance --file <selected.png> \
  --source-repo InterstellarHarvest/CYOA --source-ref <branch> --source-commit <40-hex> --source-path <path> --status approved
node tools/sync/check-canon.mjs
```

The tool:

- verifies the native size and transparency contract;
- copies the exact bytes to `assets/selected/…`;
- records the SHA-256 and provenance;
- raises the status to `approved`.

It never invents a production `assetPath`; Gameplay PMO assigns that at integration.

It refuses:

- wrong sizes (for example, a scene registered as a portrait);
- short SHAs;
- `source/` and `originals/` masters;
- container records.

Commit the result. **The selection is visible on the public storyboard as soon as Pages deploys.**

Record keys:

| Key | Record |
|---|---|
| `scenes:<id>` | a scene |
| `scenes:<id>#portraitBackground` | a scene's portrait background |
| `scenes:<id>#states:<state>` | a conditional scene state |
| `portraits:<id>` | a portrait |
| `portraits:<id>#views:<scene>` | one complete view of an opaque-complete portrait |
| `portraits:<id>#layers:<role>` | one layer of a layered portrait |
| `items:<id>#slot`, `items:<id>#inspect` | inventory slot and inspection art |
| `focus:<id>` | a Focus A close-up |
| `focus:<id>#pages:<n>` | one page of a paged Focus A close-up |
| `deathScreens:<id>` | a death screen |

### 3. Game integration (Gameplay PMO, in the game repository)

```
node tools/story-sync/sync.js status                    # what changed here since the game's pin
node tools/story-sync/sync.js pull --rev <40-hex>       # pin + project (refuses hand-edited story/)
node tools/story-import/import.js                       # preview build
<QA suites>                                             # docs/97 in the game repository
```

To integrate approved art:

1. Copy the selected PNG byte-exact to a production `art/` path in the game.
2. Set that `assetPath` here (the public catalog) in a normal commit.
3. Pull the new revision.

### 4. Integration verification (Gameplay PMO)

```
node tools/story-sync/sync.js publish --storyboard <this repository's worktree>   # from the committed, pushed game build
node tools/sync/check-canon.mjs                                                  # here
git commit + push; confirm the Pages run succeeds
```

`story/game-integration.json` records:

- the game repository, branch and commit;
- the storyboard revision it consumed;
- the build content hash;
- every image it uses, with its SHA-256.

### 5. Drift detection

- **Here:** `check-canon` runs in `pages.yml` before every deploy and in `storyboard-review.yml` on PRs. `qa-sync.mjs` proves that each kind of drift is caught.
- **In the game:** CI runs `sync.js verify`, which catches hand edits and stray canon, and `verify --online`, which re-projects the pin from this repository. It also runs `sync.js status` (informational: new nodes, changed checks, items, art statuses, unconsumed chapters).

## Viewing selected art

Open **Artwork** in the storyboard. The **Selected** filter shows every approved, integrated or reused image.

Each record shows the actual pixels at native resolution (integer zoom; click to zoom 1–4×):

- **Scenes:** each conditional state is drawn over its scene (overlay) or instead of it (replace).
- **Layered portraits:** the NPC foreground is composited on its portrait background (same box), and also shown alone on a checkerboard.
- **The House intercom:** its complete opaque views.
- **Focus A:** pages in order.
- **Items:** the inventory slot beside its inspection view.
- **Death screens.**

Each image shows its SHA-256, its source commit and path, and the game build that uses it. Node inspector cards show thumbnails, including the scene states selected at that node.

## Current state (2026-11-16)

- **Chapters:**
  - Prologue: 29 nodes.
  - Chapter 1: 36 nodes.
  - Chapter 2: 99 nodes.
  - Chapter 3: 62 nodes, draft. Not consumed by the game.
- **Game:** `InterstellarHarvest/CYOA` draft PR #14 (`agent/canonical-storyboard-sync-20261116`) consumes storyboard `d95c01e`. See `story/game-integration.json` for the exact build commit and 63 image records.
- **Integrated (verified by the game report):**
  - Prologue: 28.
  - Chapter 1: 28.
  - The shared Rest Assured death screen `deathScreens:house_of_tomorrow/rest_assured`, in the review-gated `?deathproof` presentation.
  - Plus 5 `reused` M2 images.
- **Approved, awaiting integration:**
  - 7 Biology Park Batch 1 images (signage-polish-v02 for the Bureau, the formal entrance and Jungle Junction).
  - The deliberately unbound chair state.
- **Not started:** every other Chapter 2 and Chapter 3 brief, including the eight unproduced death screens (docs/104).


## Owner/Story Director dimension resolution — 2026-11-17

For Chapter2 Batch7 and the current engine contract:Focus A is opaque564x278 at1x;inventory slots are transparent96x96;item inspection artwork is opaque565x451. Preserve the three existing botanical-treatment Focus records at564x278.

The future565x451 Scene Pickup presentation is a separate contract,not a redefinition of current Focus A. Do not stretch or crop564x278 artwork to fill that future inspector. Any future565x451 composition must be independently authored for that presentation. No runtime behavior or dimension migration is authorized by this art-production decision.

Verified integration evidence:game commit20b52601c5733a633a385bbb1c60995174e530cc declares `ART_CLASS.focus` size564x278,scale1 in game/js/stage.js;the importer enforces the same size. Report a contradictory current runtime before producing affected Focus art;continue unaffected item variants.
