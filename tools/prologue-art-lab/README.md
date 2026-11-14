# The Acceptable Error — Public Prologue Artwork Lab

Live address (after acceptance and Pages deployment):
https://interstellarharvest.github.io/CYOA-storyboard/tools/prologue-art-lab/

This is a public-safe, non-playable visual review tool. It displays the exact approved M2 shell, inventory, arrow, choice-card, utility-button and inspector images at the approved whole-pixel stage coordinates. It does not publish or execute the private CYOA gameplay engine, story scripts, save files, test fixtures, review notes or internal rulings.

## Exposition V02 refresh — 2026-11-14

Current Exposition artwork is pinned to private `InterstellarHarvest/CYOA` commit
`48eac78b07746e185cac6726220cd0b023ce6dab`, whose selected visual
candidates were reviewed under `review/exposition-automation-revision-2026-11-14/`.
Exactly four new native 314×206 candidate PNGs were published:

- Street approach — `continuity-v01/street-approach.png` (unoccupied)
- Entrance — `continuity-v02/entrance.png` (enclosed three-door facade and unattended intercom)
- Property intake — `continuity-v02/property-intake.png` (automated custody device, no attendant)
- Facilities corridor — `continuity-v01/facilities-corridor.png` (unoccupied)

Both V01 scene candidates were deliberately retained, not replaced with a newer
image: the source private catalog explicitly points to them. The approved M2
reception art and separate portrait layers remain byte-identical and are the
only scene with a person. Human-shaped *pictograms* are signage, not scene
characters.

The four prior public scene images remain in the package. Only the earlier
unoccupied street and facilities images can be displayed in the public comparison
selector. Older entrance/property candidates involving staff remain archived but
are not selectable as scene backgrounds.

`exposition-v02.json` contains only selected public-safe IDs, paths, native
dimensions, hashes, status, archive references and provenance. Every replacement
is `generated` with owner visual approval pending; no narrative patches, private
prose, game logic, production assets or source transport rasters are imported.
The current six-slot inventory, spring-slide physics, UI geometry, action buttons
and bitmap text are unchanged.

## Public contents

- Seven draft prologue main scenes (314 by 206 at 4× nearest), including four current Exposition references, plus the approved M2 reception scene.
- Two transparent termination drone poses on their separate 564 by 278 corridor background, plus approved receptionist layers.
- Nine draft 96 by 96 inventory icons and nine separate 565 by 451 item inspection illustrations, plus the approved Facilities Key pair.
- Seventeen original M2 images plus fourteen additional byte-exact approved control/font images (pressed utility sprites, action glyphs, scrollbar thumb and bitmap font atlases).
- Metadata from the same public artwork catalogue used by the storyboard.

The November 13 artwork-quality audit from <code>CYOA/docs/story-gameplay-study-v01</code> contributes 16 corrected source PNGs (5 scenes and 11 item images); the remaining 12 generated PNGs are unchanged. All 28 pass the source audit's technical checks, but visual owner approval is pending. The audit records and original-versus-final SHA-256 values are retained in <code>artwork-audit.json</code>. Nothing is merged into the private game or promoted to approved production artwork. The 4× evidence sheets and static shell composites are not runtime assets.

All 49 primary images retain SHA-256 and dimension verification. The fourteen added approved images are pinned against their original Git blob hashes. No draft artwork is marked approved by publication.

## Visual review controls

The sidebar changes scenes, safely archived street/corridor image comparisons, portrait pair/pose/offset, foreground and background visibility, one-at-a-time inventory scrolling, and the item inspector. The inventory uses the current six-slot, 96×96, 20px-gap, 116px-pitch baseline from the owner's November 13 layout export. The original bitmap face atlases are used for dialogue/choice labels, objective, and action-button labels. The three approved action buttons can be reviewed with labels or INSPECT / NOTES / FILES glyphs, each with the actual UP and DOWN artwork. The navigation and speech text are neutral review-only copy; no private story scripts or gameplay engine are published.

The obsolete seven-slot comparison is removed. The current six-slot row ends before the right arrow. Inventory navigation now ports the original M1/game motion curve: 275 ms slide with 5 px overshoot, 1 px settle, and 2 ms stagger per slot. The six-slot window clips incoming/outgoing items behind the arrow bays; one item advances per arrow click and rapid reverse clicks preserve residual movement. Reduced-motion preference disables the animation. The sidebar previous/next buttons and position slider use the same motion; selecting a new scene does not reset the inventory. The approved action-button artwork is now separately reviewable in this lab, without changing live game UI assets or mechanics.

Still pending owner approval: termination notice signature and review markings, ticket reading FOUR in a possible three-item outcome, the effects box's H. Carter name, drone alignment, inspector object backgrounds/placement, and workplace-to-Exposition-to-reception continuity.

## Testing

Run the public storyboard smoke test and byte-level artwork verifier:

    node tools/storyboard/qa-smoke.mjs
    node tools/prologue-art-lab/qa/qa-static.mjs

For full browser screenshots, install Playwright and browsers, then run:

    node tools/prologue-art-lab/qa/qa-browser.mjs

The branch-scoped GitHub Actions workflow does both and uploads screenshots as a run artifact. The main Pages workflow copies only the public UI files and images into the deployed site.

## Provenance and boundary

- Approved M2 visual baseline: 312928afbac4aace37c6602e9033574f90849d2b
- Draft art source: story/artwork.draft.json, already mirrored on the public storyboard.
- Public image hashes: asset-index.json and control-asset-manifest.json.
- Public-safe geometry snapshot: layout-reference.json (no private game data).
- Original font glyph mappings and approved atlas references: bitmap-fonts.json, rendered by pixel-type.js.
- No private rules engine, no unpublished narrative content beyond the public draft catalogue, and no automatic promotion of draft artwork.
