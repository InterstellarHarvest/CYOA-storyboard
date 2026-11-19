# Out of Order — Public Storyboard

This is the **public, JSON-backed Storyboard + Artwork Production viewer** for Out of Order. The site displays authored scenes, branching choices, inventory items, shared art prompts, asset references and production statuses. You can edit prompts and export updated JSON locally, but the live site never commits changes to GitHub.

**Repository identity:** The public GitHub repository and Pages slug intentionally remain `CYOA-storyboard`; that is a URL, not the game title. The game itself is **Out of Order** at [InterstellarHarvest/out-of-order](https://github.com/InterstellarHarvest/out-of-order). Historical approved art prompts and `cyoa-*` schemas stay unchanged for provenance and compatibility.

- **[Open the storyboard](https://interstellarharvest.github.io/CYOA-storyboard/)**
- **[Open the Prologue Artwork Lab](https://interstellarharvest.github.io/CYOA-storyboard/tools/prologue-art-lab/)** — public-safe visual review with approved M2 shell assets and 28 draft PNGs; no private game engine
- [Viewer](tools/storyboard/index.html) · [Chapter manifest](story/storyboard-manifest.json) · [Prologue draft](story/chapters/prologue-00.draft.json) · [Item records](story/items.draft.json) · [Shared art prompts](story/artwork.draft.json)

> **Chapter 3 creative reboot (2026-11-18):** The old People's Pavilion graph is **archived, not active story canon**. The viewer retains it for historical inspection and labels it `archived`. Its old nodes, choices, endings, and Chapter 3-only artwork briefs must not be imported into the game or commissioned as new art. Read the [Chapter 3 reboot brief](docs/109_CH3_REBOOT_ONE_EXPERIENCE_PER_PERSON_20261118.md) and the [immutable legacy archive](story/archives/chapter-03-pre-reboot-20261118.json) before any new Chapter 3 work. Prologue, Chapter 1 and Chapter 2 remain unaffected.

## Canon and the production pipeline

**This repository is the canonical creative source** for Out of Order. Read [docs/105](docs/105_CANONICAL_SYNC_PIPELINE.md) first; the owner rulings are in [docs/102](docs/102_ARTWORK_APPROVAL_AND_STORYBOARD_SYNC_POLICY.md) and [docs/103](docs/103_RETROACTIVE_ARTWORK_APPROVAL_LEDGER.md).

- **Narrative, items, checks and art briefs** are edited here. Publish them after `node tools/sync/check-canon.mjs` passes. You do not need to wait for game integration.
- **Art selection is approval.** Register the selected PNG with `node tools/sync/register-art.mjs`: it records the exact bytes, hash and source, sets `approved`, and makes the image visible on the site. **Never regenerate or re-approve selected art** unless the owner asks for a revision.
- **The private game** (`InterstellarHarvest/out-of-order`) consumes a *pinned revision* of this repository as a generated, read-only projection (`tools/story-sync/sync.js` there). It publishes back only `story/game-integration.json`, the images a real build uses, which marks them `integrated`.
- **Drift is a CI failure.** Pages deploys only when `check-canon` passes. It fails on missing chapters, broken routes, undeclared fields, missing or altered selected-art previews, a selected image falling back to `generated` / `not-started`, and `integrated` claims a game build does not back.

Everything here is **public**. The private engine, review worktrees and generation masters are never published. Only the curated `assets/selected/` package of selected images is, with provenance.

## Viewing selected artwork

Open **Artwork** and choose **Selected**. Each record shows:

- **Actual pixels** at native resolution; click to zoom 1–4×.
- **Scene states** drawn over (overlay) or instead of (replace) their scene.
- **Portraits:** NPC foregrounds composited on their portrait background; the House intercom's complete opaque views.
- **Album:** the Focus A pages.
- **Items:** inventory slot beside the inspection art.
- **Death screens.**
- **Provenance:** the source commit and path, and the game build that uses the image.

## Arrange your own timeline

Drag a story-node box to move it while its connections follow. Click without dragging to inspect. Positions auto-save in your browser per chapter. Use **Export Layout** to download shareable `storyboard-layout.json`, **Import Layout** to restore it, or **Reset Layout** to return the selected chapter to the automatic arrangement. Layout data is separate from all story and artwork definitions. Changes are not automatically committed to GitHub.

### Timeline view (Prologue, Chapter 1, Chapter 2)

The Prologue, Chapter 1 (House of Tomorrow) and Chapter 2 (Biology Park) open as a left-to-right **timeline** at reading zoom, at the start of the chapter. Switching chapters in the dropdown and back returns each chapter to the zoom and scroll you left it at. Scroll or drag sideways to follow the story; **Jump to incident…** moves to a named incident, **Start** returns to the beginning, and **Fit** shows the whole chapter as an overview.

- Cards are grouped by authored incident (tinted panels with a title above the first card of each incident). The grouping is viewer-only metadata in `story/storyboard-layout.json`; the game never reads it.
- Connector labels sit next to the decision they leave. **PASS** / **FAIL** badges mark check outcomes; dotted lines are item SHOW/USE routes. Hover a label for the full choice text, or click it to open the destination.
- The few genuine loops (Chapter 1's dinner/foyer/Martin and housekeeping cycles; Chapter 2's three antidote-kit inspections) are drawn as dashed **↩ return** connectors running under the cards, instead of sending the loop to a far column.
- Pills at the edges show routes between chapters: Chapter 1's five surviving exits → Chapter 2, Chapter 2's five incoming Chapter 1 routes (all arriving at the single `bureau_arrival`), and Chapter 2's five **preview-only** handoffs to Chapter 3 (storyboard links, not gameplay transitions); the Prologue shows its hand-off to Chapter 1. Pills behave like cards: click one to see the route in the right-hand panel, drag it to move it (saved with the chapter's layout). The panel's **Open …** button switches to the other chapter.

Chapter 3 keeps its original arrangement.

**Saved arrangements from before the timeline.** Positions this browser saved for the Prologue, Chapter 1 or Chapter 2 before the timeline existed were offsets for the old automatic layout. They are moved aside (never deleted) so the new timeline shows by default. **Restore previous arrangement** brings them back. Older exported layout files still import.

### Storyboard QA

```
node tools/storyboard/qa-smoke.mjs                                   # dependency-free logic + layout checks
NODE_PATH="$(npm root -g)" node tools/storyboard/qa-browser.js       # chapter navigation, Chromium + Firefox
NODE_PATH="$(npm root -g)" node tools/storyboard/qa-timeline.js      # timeline geometry + screenshots, Chromium + Firefox
```

## Paired scene art for Codex

Codex reads requirements from `story/artwork.draft.json`; records whose status is `approved`, `integrated` or `reused` are finished — do not regenerate them.


`story/artwork.draft.json` is the authority. The `scenes` records contain main 314×206 images; a scene may also contain a nested `portraitBackground` for a distinct opaque 564×278 closer environment view. NPC foreground portraits live separately in `portraits` as transparent 564×278 PNGs. Both scene records and portrait-background records are browsable/editable from the public storyboard. Reception scene/background are reused approved art and must not be regenerated.
