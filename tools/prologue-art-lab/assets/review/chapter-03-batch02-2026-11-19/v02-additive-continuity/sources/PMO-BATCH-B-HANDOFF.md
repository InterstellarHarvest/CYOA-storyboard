# Chapter 3 Artwork PMO — Begin Batch B

You are the Chapter 3 Artwork Generator for *The Acceptable Error*.

Chapter 3's narrative and Storyboard are published. Batch A's six images are approved and registered.

Begin **Batch B artwork generation and visual review only**.

## 1. Source of truth

Repository: `InterstellarHarvest/CYOA-storyboard`

Canonical starting commit: `3ac5422`

Read these documents and the current artwork registry:

- `docs/111_CH3_ARTWORK_PMO_HANDOFF_AND_NARRATIVE_LOCK_20261118.md`
- `docs/112_CH3_ARTWORK_AUDIT_AND_GENERATION_HANDOFF_20261118.md`
- `story/artwork.draft.json`
- `story/chapters/chapter-03.reboot-candidate.json`

Use the exact approved narrative and the existing prompts. Do not rewrite them.

The historical statements in doc 112 that no Chapter 3 images have been approved are superseded by Batch A's November 19 approval ledger.

## 2. Generate six Batch B candidates

| ID | Registry record |
|---|---|
| CH3-B01-arrival | `scenes:pavilion_reboot/arrival` |
| CH3-B02-record-printer | `scenes:pavilion_reboot/record_printer` |
| CH3-B03-record-printer-bg | `scenes:pavilion_reboot/record_printer#portraitBackground` |
| CH3-B04-record-scanner | `scenes:pavilion_reboot/record_scanner` |
| CH3-B05-record-scanner-bg | `scenes:pavilion_reboot/record_scanner#portraitBackground` |
| CH3-B06-paper-emergency | `scenes:pavilion_reboot/paper_emergency` |

Generate exactly these six candidates.

Use each record's full prompt, canonical art direction, and scene-reuse requirements.

## 3. Mandatory visual continuity

Treat the approved Chapter 3 Batch A artwork as the primary visual reference.

Preserve:

- Institutional gray, slate, muted teal, cream and restrained accents.
- The restroom architecture and machinery established by A01.
- The believable Pavilion design language.
- The Pavilion Attendant's approved identity, costume and proportions.
- Coherent microphone, counter, printer and verification hardware where those elements recur.

The record printer and scanner must look like different areas or views of the same institution, not unrelated buildings.

The portrait backgrounds must be independently composed close views, not enlargements of their main scenes.

For compositing tests, reuse the approved A03 attendant foreground. Maintain its position, anchoring and scale. Do not regenerate or modify the attendant.

## 4. Pixel-density rule

**All main scenes remain 314×206 logical pixels, intended for exact 4× nearest-neighbor display.**

Use the broader clusters and simplified detail density of the approved Batch A artwork.

Do not switch Chapter 3 to 628×412 or establish a new 2× display convention.

Avoid:

- Excessively detailed outlines.
- Soft, blended edges.
- Fine RGB tonal noise.
- Artificial sharpening.
- Dense anti-aliased textures.
- Tiny unreadable lettering.
- Faux-pixel art that looks like a reduced painting.

Review each main scene both at native size and exact 4×.

Also compare its 4× presentation against approved Chapter 1 and Chapter 2 main scenes. Cross-chapter consistency is a release requirement.

Attempt genuine native-grid authorship. Record the generator's actual source dimensions.

If a generator produces a larger image requiring downsampling, disclose the derivation and preserve the source. Never falsely claim that original native-grid authorship has been proven.

## 5. Narrative accuracy

The arrival scene must connect visually to the approved Pavilion environment.

The record printer and scanner must support the story's bureaucratic absurdity.

The paper emergency is a harmless paper-handling incident, not a death scene.

Do not:

- Show the protagonist's face.
- Depict a physical duplicate or embodied Original.
- Invent additional story outcomes.
- Introduce new inventory items.
- Generate death-popup images.
- Reuse archived pre-reboot Chapter 3 concepts.

## 6. Review package

Work on a new isolated generation branch.

Create a versioned Batch B review package containing:

- Six native-resolution candidates.
- Exact 4× nearest-neighbor main-scene previews.
- Native portrait-background previews.
- Composites using the approved attendant foreground.
- Comparisons against Batch A and earlier approved chapters.
- Generation prompts and source provenance.
- Actual generator output dimensions.
- Candidate SHA-256 hashes.
- Dimensions, opacity and alpha QA results.
- A publicly accessible review gallery through the established Pages-compatible process.

Preserve all historical review files and previously approved artwork byte-for-byte.

Do not modify production asset paths.

## 7. Stop for Nate's review

All six Batch B outputs must remain:

**`generated / unselected`**

Do not register them as approved.

Do not merge them into the canonical artwork registry or playable game.

Do not begin Batch C or D.

Return the public gallery URL, branch, commit, six candidate hashes, technical limitations and any visual issues requiring Art Director attention.

Nate will review and select the artwork. Selection will constitute approval, followed by a separate Claude approval-registration handoff.