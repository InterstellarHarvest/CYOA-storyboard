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

Drag a story-node box to move it while its connections follow. Click without dragging to inspect. Positions auto-save in your browser per chapter. Use **Export Layout** to download shareable `storyboard-layout.json`, **Import Layout** to restore it, or **Reset Layout** to return to the automatic arrangement. Layout data is separate from all story and artwork definitions. Changes are not automatically committed to GitHub.

## Paired scene art for Codex

`story/artwork.draft.json` is the authority. The `scenes` records contain main 314×206 images; a scene may also contain a nested `portraitBackground` for a distinct opaque 564×278 closer environment view. NPC foreground portraits live separately in `portraits` as transparent 564×278 PNGs. Both scene records and portrait-background records are browsable/editable from the public storyboard. Reception scene/background are reused approved art and must not be regenerated.
