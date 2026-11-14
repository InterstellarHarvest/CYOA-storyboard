# The Acceptable Error — Public Prologue Artwork Lab

Live address (after acceptance and Pages deployment):
https://interstellarharvest.github.io/CYOA-storyboard/tools/prologue-art-lab/

This is a public-safe, non-playable visual review tool. It displays the exact approved M2 shell, inventory, arrow, choice-card, utility-button and inspector images at the approved whole-pixel stage coordinates. It does not publish or execute the private CYOA gameplay engine, story scripts, save files, test fixtures, review notes or internal rulings.

## Public contents

- Seven draft prologue main scenes (314 by 206 at 4x nearest), plus the approved M2 reception scene.
- Two transparent termination drone poses on their separate 564 by 278 corridor background, plus approved receptionist layers.
- Nine draft 96 by 96 inventory icons and nine separate 565 by 451 item inspection illustrations, plus the approved Facilities Key pair.
- Seventeen approved M2 visual files required to show the original shell, inspector, cards and controls.
- Metadata from the same public artwork catalogue used by the storyboard.

All 45 images were copied byte-for-byte from the accepted source and are verified by SHA-256 and PNG dimensions. No draft artwork is marked approved by publication.

## Visual review controls

The sidebar changes scenes, portrait pair/pose/offset, foreground and background visibility, 6-vs-7 inventory slots, one-item-at-a-time scrolling and the item inspector. The stage's neutral lab actions also switch scenes and show an item. Navigation text is only a review UI; the original game's dialogue, mechanics and exact bitmap-font rendering are not part of this public export.

The seven-slot owner-target layout overlaps the M2 baseline right inventory arrow. The current M2 checked-in layout defaults to six slots; both are shown for comparison without altering the original game.

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
- Public exported image hashes and byte counts: asset-index.json.
- No private rules engine, no unpublished narrative content beyond the public draft catalogue, and no automatic promotion of draft artwork.
