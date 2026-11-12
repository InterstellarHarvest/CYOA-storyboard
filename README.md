# The Acceptable Error — Public Storyboard

This is the **public, JSON-backed Storyboard + Artwork Production viewer** for The Acceptable Error. The site displays authored scenes, branching choices, inventory items, shared art prompts, asset references and production statuses. You can edit prompts and export updated JSON locally, but the live site never commits changes to GitHub.

- **[Open the storyboard](https://interstellarharvest.github.io/CYOA-storyboard/)** *(available once GitHub Pages is enabled and the deployment succeeds)*
- [Viewer](tools/storyboard/index.html) · [Chapter manifest](story/storyboard-manifest.json) · [Prologue draft](story/chapters/prologue-00.draft.json) · [Item records](story/items.draft.json) · [Shared art prompts](story/artwork.draft.json)

## Boundaries

The main game project **InterstellarHarvest/CYOA remains private**. The **only** content exported here is the standalone storyboard page and selected story/items/artwork JSON needed to display it. This public repository deliberately excludes game source, image assets, internal rulings/docs, and commit history from the private project.

Everything here is **public**. Do not commit secret data or unpublished private project material.

## Updating the viewer

The authoritative drafts are maintained on the private CYOA story branch. After review, copy **only approved-to-publish** `tools/storyboard/index.html` and `story/**` into this public mirror. The two repositories are **not automatically synchronized** (no cross-repository credentials or secret token setup).

On a change to these public files, GitHub Actions publishes the site with the [Pages workflow](.github/workflows/pages.yml). The viewer supports importing and exporting JSON locally, but edits made in your browser do not directly write back to either GitHub repository.
