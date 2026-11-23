# Out of Order — Permanent Pixel-Art Production Standard

We need to correct and standardize the artwork-generation pipeline for all remaining chapters.

**The primary visual benchmark is approved Chapter 2 artwork.** Its best scenes achieve impressive environmental detail, lighting, depth and material definition using very small native resolutions and restrained color palettes.

We want that level of craftsmanship consistently throughout the game.

## 1. The detailed image is a reference, not the final asset

You may—and should—generate a large, richly detailed illustration first.

Use that illustration to establish:

- Composition, perspective and architecture.
- Object placement and recognizable story details.
- Materials, lighting, shadows and reflections.
- The overall mood and environmental storytelling.
- Character positions and silhouettes.

This high-resolution illustration is a **production reference**.

**Do not simply shrink it to 314×206, enlarge the result 4×, and declare it finished.**

That process preserves photographic texture and tiny color variations that become visual noise.

## 2. Create a separate low-resolution interpretation

The next stage should follow the principle demonstrated by the recent 64-tone NPC portrait revisions.

Reinterpret the detailed reference using:

- A deliberately constrained, cohesive palette.
- Broad, readable color regions.
- Intentional pixel clusters.
- Clearly defined edges and silhouettes.
- Material-specific shading ramps.
- Carefully placed highlights and shadows.
- Selective details that remain recognizable at native resolution.

You may generate an additional simplified, pixel-friendly source illustration to support this process.

Construct and refine the final native-resolution image as its own artwork. Use separate structural layers or masks where useful, so individual areas can be corrected without damaging the whole composition.

A direct resize may be used as a diagnostic or starting reference, but **it is not sufficient as the final production method**.

Palette reduction alone is also insufficient. The shapes, edges, shading and detail distribution must be reconstructed intelligently.

Do not claim independent native-grid authorship if the actual method remains source-derived. Preserve accurate provenance.

## 3. Main-scene artwork — 314×206

Main scenes must prioritize:

1. Strong architectural perspective.
2. Readable objects and environmental storytelling.
3. Clear, simplified NPC silhouettes.
4. Convincing lighting expressed through deliberate shading.
5. Detail density comparable to approved Chapter 2 environments.

Use approved Chapter 2 scenes—especially the Public Conveniences Bureau, Environmental Control Tower and other detailed environments—as primary benchmarks.

Their restrained palettes are examples of what is possible, not arbitrary mathematical limits that every image must match.

**Avoid:**

- Photographic grain.
- Thousands of barely distinguishable intermediate shades.
- Blurred or softened pixel boundaries.
- Excessively detailed miniature faces and hands.
- Random single-pixel texture attempting to preserve every feature of the large reference.
- Smooth gradients where stepped shading would better match the game's style.

NPCs in main scenes should be recognizable through clothing, posture, color and silhouette. Detailed facial anatomy belongs in their portraits.

## 4. Portraits and portrait backgrounds — 564×278

Portrait artwork may retain substantially more detail than main-scene NPCs.

Facial expressions, hands, hair, tailoring and anatomy should remain expressive and carefully rendered.

However, portraits also need palette discipline.

Use the recent 64-tone plumber alternatives and the approved Chapter 2/3 NPC portraits as references for:

- Cleaner shading transitions.
- Reduced grain.
- Defined facial and hand detail.
- Deliberate material-specific highlights.
- Consistent line and edge quality.

**Do not indiscriminately flatten portraits to the same detail level as 314×206 scenes.**

Portrait backgrounds can likewise remain richly detailed, but should use controlled palettes and deliberate lighting rather than unrestricted photographic texture. Their palette requirements need not be identical to character foregrounds.

## 5. Mandatory visual quality gate

Every new image must be compared against approved canonical artwork from earlier chapters.

Check **both native resolution and exact 4× nearest-neighbor display**.

At 4×, inspect whether:

- Pixels form intentional clusters.
- Edges appear clean and stable.
- Lighting consists of readable shade transitions.
- Materials remain distinguishable.
- NPCs remain recognizable without excessive detail.
- The image genuinely resembles the established game's pixel art.

Technical validation—correct dimensions, hashes, transparency and exact 4× scaling—is necessary but does not establish artistic quality.

Measure palette size and examine excessive color variation as diagnostic evidence. Do not treat a palette count alone as proof of success.

Include direct comparisons with approved Chapter 2 references in every review gallery.

An image that looks attractive as a reduced digital painting but fails this comparison is **not selection-ready**.

## 6. Immediate work: Chapter 4 B2-02

The four main scenes need a new pixel-art treatment:

- CH4-B2-06 — Loading Lane
- CH4-B2-07 — Service Alley
- CH4-B2-08 — Loading Dock
- CH4-B2-09 — Service Stairs

Their current compositions and detailed source illustrations are valuable. Preserve them as references.

B2-08 and B2-09 have the strongest starting compositions. Use them to establish the corrected treatment, then apply that standard to all four.

Preserve the humor, object placement, perspective and environmental details. Do not sacrifice the richness of the scenes merely to achieve a lower palette count.

The new foreman portrait and portrait background can remain at their current level of detail, subject to the portrait palette requirements above.

Do not modify already approved artwork. The B2-01 v01 selections remain registered; the two v02 palette alternatives remain separate until explicitly approved.

## 7. Production and review

1. Record these standards in the repository's existing artwork-production guidance.
2. Rework the four B2-02 main scenes.
3. Perform internal comparisons against approved Chapter 2 and Chapter 4 art.
4. Correct deficiencies before publishing.
5. Publish one consolidated review package, with native and exact 4× comparisons, to the existing public art review branch.
6. Preserve original references, processing records and provenance.
7. Keep all revised candidates **UNSELECTED** until Nate approves.

Avoid unnecessary intermediate approval requests. Complete the four-scene quality pass before requesting owner review.

**The objective is not to make the artwork less detailed. It is to express that detail through better, more deliberate pixel art.**


## Owner's final artwork hierarchy

| Artwork type | Detail expectation | Primary reference |
|---|---|---|
| Main scenes,314×206 | High environmental detail through restrained palettes and deliberate pixel clusters | Approved Chapter2 |
| Small NPCs inside scenes | Simplified, recognizable silhouettes | Chapter2 and approved Chapter4 |
| Portrait characters,564×278 | Rich faces, hands and clothing; controlled palette | Approved Pavilion portraits and64-tone studies |
| Portrait backgrounds,564×278 | Richer materials and lighting; still palette-controlled | Approved reception and Chapter4 backgrounds |
| Focus close-ups,564×278 | Maximum useful object detail and readable lettering | Approved Focus artwork |

Chapter2 establishes pixel-art craftsmanship; the detailed reference establishes artistic ambition. Both are required. The64-tone examples calibrate the treatment; they are not a blanket numerical limit on every asset class. Approval, native-authorship provenance and engine integration remain separate.
