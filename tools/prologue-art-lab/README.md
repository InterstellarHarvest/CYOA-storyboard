# The Acceptable Error — Public Prologue Artwork Lab

Live address (after acceptance and Pages deployment):
https://interstellarharvest.github.io/CYOA-storyboard/tools/prologue-art-lab/

This is a public-safe, non-playable visual review tool. It displays the exact approved M2 shell, inventory, arrow, choice-card, utility-button and inspector images at the approved whole-pixel stage coordinates. It does not publish or execute the private CYOA gameplay engine, story scripts, save files, test fixtures, review notes or internal rulings.

## Public contents

- Seven draft prologue main scenes (314 by 206 at 4x nearest), plus the approved M2 reception scene.
- Two transparent termination drone poses on their separate 564 by 278 corridor background, plus approved receptionist layers.
- Nine draft 96 by 96 inventory icons and nine separate 565 by 451 item inspection illustrations, plus the approved Facilities Key pair.
- Seventeen original M2 images plus fourteen additional byte-exact approved control/font images (pressed utility sprites, action glyphs, scrollbar thumb and bitmap font atlases).
- Metadata from the same public artwork catalogue used by the storyboard.

All 45 original images retain SHA-256 and dimension verification. The fourteen added approved images are pinned against their original Git blob hashes. No draft artwork is marked approved by publication.

## Visual review controls

The sidebar changes scenes, portrait pair/pose/offset, foreground and background visibility, one-at-a-time inventory scrolling, and the item inspector. The inventory uses the current six-slot, 96×96, 20px-gap, 116px-pitch baseline from the owner's November 13 layout export. The original bitmap face atlases are used for dialogue/choice labels, objective, and action-button labels. The three approved action buttons can be reviewed with labels or INSPECT / NOTES / FILES glyphs, each with the actual UP and DOWN artwork. The navigation and speech text are neutral review-only copy; no private story scripts or gameplay engine are published.

The obsolete seven-slot comparison is removed. The current six-slot row ends before the right arrow. The approved action-button artwork is now separately reviewable in this lab, without changing live game UI assets or mechanics.

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
