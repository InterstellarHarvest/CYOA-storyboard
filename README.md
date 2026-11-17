# The Acceptable Error — Public Storyboard

This is the **public, JSON-backed Storyboard + Artwork Production viewer** for The Acceptable Error. The site displays authored scenes, branching choices, inventory items, shared art prompts, asset references and production statuses. You can edit prompts and export updated JSON locally, but the live site never commits changes to GitHub.

- **[Open the storyboard](https://interstellarharvest.github.io/CYOA-storyboard/)**
- **[Open the Prologue Artwork Lab](https://interstellarharvest.github.io/CYOA-storyboard/tools/prologue-art-lab/)** — public-safe visual review with approved M2 shell assets and 28 draft PNGs; no private game engine
- [Viewer](tools/storyboard/index.html) · [Chapter manifest](story/storyboard-manifest.json) · [Prologue draft](story/chapters/prologue-00.draft.json) · [Item records](story/items.draft.json) · [Shared art prompts](story/artwork.draft.json)

## Boundaries

The main game project **InterstellarHarvest/CYOA remains private**. The public export is limited to the standalone storyboard, its selected draft JSON, and the separately approved **Prologue Artwork Lab** package (28 draft PNGs plus 17 needed approved M2 visual PNGs and public-safe viewing code). The private gameplay engine, internal rulings, review notes, and private commit history are not published.

Everything here is **public**. Do not commit secret data or unpublished private project material.

## Updating the viewer

The authoritative drafts are maintained on the private CYOA story branch. After review, copy **only approved-to-publish** `tools/storyboard/index.html` and `story/**` into this public mirror. The two repositories are **not automatically synchronized** (no cross-repository credentials or secret token setup).

On a change to these public files, GitHub Actions publishes the site with the [Pages workflow](.github/workflows/pages.yml). The viewer supports importing and exporting JSON locally, but edits made in your browser do not directly write back to either GitHub repository.

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

`story/artwork.draft.json` is the authority. The `scenes` records contain main 314×206 images; a scene may also contain a nested `portraitBackground` for a distinct opaque 564×278 closer environment view. NPC foreground portraits live separately in `portraits` as transparent 564×278 PNGs. Both scene records and portrait-background records are browsable/editable from the public storyboard. Reception scene/background are reused approved art and must not be regenerated.
