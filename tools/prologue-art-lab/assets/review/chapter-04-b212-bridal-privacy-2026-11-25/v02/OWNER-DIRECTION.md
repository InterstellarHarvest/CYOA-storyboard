
# Out of Order — Chapter 4 B2-12: Widescreen Privacy Panel and Square Inspection

You are continuing Chapter 4 artwork production for *Out of Order*.

Nate has approved the B2-12 v01 dressing room and both bridal privacy-panel images. He has now finalized how the privacy panel should be presented in-game.

**Do not restart B2-12, regenerate approved artwork, or modify gameplay code during this artwork task.**

## 1. Final approved design

The bridal privacy panel will have two views:

**A. Widescreen Focus — NEW artwork required**

- Native canvas: **564×278**.
- The bridal privacy panel occupies most of the image's height.
- Show substantial environmental context on both sides: the surrounding door, wall, brass fixtures and associated machinery.
- The panel should be recognizable as the same object depicted in the approved square artwork.
- Prioritize clear composition, convincing materials, coherent lighting and readable pixel clusters.
- Tiny lettering does not need to be fully legible here. The detailed inspection view handles that.
- Create both **LOCKED** and **PROVISIONALLY AUTHORIZED** variants with identical composition and background geometry.

This image appears while the player is interacting with the bridal privacy system. The ordinary story choices remain visible.

**B. Square INSPECT — Existing APPROVED artwork**

Reuse the exact approved **565×451** images:

- Locked privacy panel.
- Provisional authorization panel.

Do not modify, resize, crop, recolor or regenerate either image.

These will eventually appear when the player activates an **INSPECT** contextual action.

The square inspection provides a larger, more detailed view and additional descriptive information to help the player decide what to do.

Closing the inspection returns to the previous widescreen Focus scene and its original choices.

## 2. Canonical references

Repository:

https://github.com/InterstellarHarvest/CYOA-storyboard

Existing B2-12 review branch:

`art/ch4-b212-bridal-privacy-review-20261125`

Original review commit:

`1261658ed882bff7340405e91f5d44f4e5404012`

[Approved B2-12 v01 gallery](https://htmlpreview.github.io/?https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/22342ccca859cf450a1d7cef44c8e2b079182c24/tools/prologue-art-lab/assets/review/chapter-04-b212-bridal-privacy-2026-11-25/v01/online.html)

Source directory:

`tools/prologue-art-lab/assets/review/chapter-04-b212-bridal-privacy-2026-11-25/v01/`

Relevant standards:

- `docs/129` — permanent pixel-art production standard.
- `docs/138` — consolidated Chapter 4 artwork queue.
- `docs/105` — Focus A versus inventory inspection dimensions.

Use approved Chapter 2 artwork as the primary quality benchmark.

## 3. Artwork production method

Follow our established successful workflow:

1. Study the approved square panel and Chapter 2 artwork.
2. If useful, generate a large, detailed concept image for composition, lighting and materials.
3. Treat that large image **only as reference**.
4. Independently construct the actual artwork at **564×278 native resolution**.
5. Reinterpret and simplify detail using deliberate pixel clusters and a controlled palette.
6. Export exact nearest-neighbor 4× previews.

**Do not simply downscale the detailed image, sharpen it, reduce its palette and call it finished.**

The goal is Chapter 2's richness of detail within a low-resolution, low-palette image.

Avoid:

- Excessively intricate machinery that becomes visual noise.
- Thin, scattered pixels and grain.
- Flat, angular material rendering.
- Unnecessarily tiny lettering.
- Excessive colors.
- Artificially sharpening reduced paintings.
- Altering the approved square artwork.

The widescreen image should be attractive and immediately understandable at both native resolution and exact 4×.

Remember Nate's recent feedback: avoid unnecessary cycles of microscopic corrections. Build a strong composition from the beginning and compare it against Chapter 2 before publication.

## 4. Gameplay interaction requirements — engineering handoff only

The relevant story node is:

`hotel_bridal_door_focus`

Focus identifier:

`grand_bellevue/bridal_privacy_panel`

The intended interaction is:

1. The normal widescreen Focus scene appears with its existing story choices.
2. A contextual **INSPECT** action opens the approved 565×451 square image.
3. The player can examine the panel and read additional descriptive information.
4. X or Escape closes the inspection.
5. The player returns to the same widescreen scene with the same available choices.

**INSPECT is informational, not a story choice.**

Opening or closing it must not:

- Advance the story.
- Execute `Rules.step`.
- Set or clear flags.
- Consume a choice.
- Add or remove inventory items.
- Restart dialogue.
- Change which choices are available.

Do not repurpose inventory-item inspection or the existing scene-pickup mechanism without verifying their behavior.

Prepare a concise engineering handoff for Claude/the Gameplay PMO. Engineering must demonstrate that all five bridal-door choices, conditional ring interactions, return behavior, keyboard navigation and save/resume remain correct.

If the feature cannot preserve the story choices, it must not be activated.

**Do not implement, merge or deploy the engine change as part of this artwork task.**

## 5. Review deliverables

Produce:

- One 564×278 LOCKED widescreen candidate.
- One matching 564×278 PROVISIONALLY AUTHORIZED widescreen candidate.
- Native and exact 4× previews.
- Comparisons against the approved 565×451 designs.
- Comparisons against strong approved Chapter 2 artwork.
- Editable layers, source images, prompts and honest provenance records.
- A concise gameplay-engine handoff describing the separate INSPECT behavior.

Publish to the established artwork review branch in a new, versioned review directory.

The gallery must display:

- Widescreen gameplay compositions.
- Approved square inspection images.
- Native/4× comparisons.
- Chapter 2 quality benchmarks.

Run dimension, palette, nearest-neighbor scaling, preservation and published-file checks.

Verify that all previously approved PNG hashes remain unchanged.

## 6. Approval boundaries

- New widescreen images: **UNSELECTED until Nate reviews them**.
- Existing square panels: **APPROVED; preserve their exact bytes**.
- Existing dressing room: **APPROVED; do not modify**.
- Narrative and gameplay: unchanged.
- Canonical `main`: unchanged during this review.
- Draft PR #32: do not merge or change.
- No deployment.

Publish the completed review package and provide Nate with one browser gallery link and a concise recommendation.

**The goal is one strong, Chapter 2-quality widescreen composition paired with the square artwork Nate already approved—not another long revision cycle.**
