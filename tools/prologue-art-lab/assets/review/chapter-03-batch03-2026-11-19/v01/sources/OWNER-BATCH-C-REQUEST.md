# Out of Order — Chapter 3 Artwork Batch C

You are Codex, responsible for generating the next Chapter 3 artwork candidates for **Out of Order**.

Repository: `InterstellarHarvest/CYOA-storyboard`

The separate game repository is `InterstellarHarvest/out-of-order`. Do not modify it.

## 1. Preflight

Fetch the latest storyboard `main`.

The last verified commit is `d4bae261`; recheck before starting.

Read the canonical Chapter 3 artwork briefs and narrative lock, particularly:

- `story/artwork.draft.json`
- `docs/111_CH3_ARTWORK_PMO_HANDOFF_AND_NARRATIVE_LOCK_20261118.md`
- `docs/112_CH3_ARTWORK_AUDIT_AND_GENERATION_HANDOFF_20261118.md`

Verify the approved Chapter 3 narrative blob remains `857ffdf1bc9432cf4bbbfd7819f5f430a06d9036`.

Use **Out of Order** as the game title. Older title references inside existing image prompts are historical wording, not a direction to revert branding.

## 2. Generate Batch C

Generate these seven candidates from their exact canonical artwork briefs:

| ID | Registry record |
|---|---|
| CH3-C01-urgency | `scenes:pavilion_reboot/urgency_stage` |
| CH3-C02-urgency-bg | `scenes:pavilion_reboot/urgency_stage#portraitBackground` |
| CH3-C03-locomotion | `scenes:pavilion_reboot/locomotion_stage` |
| CH3-C04-surprise | `scenes:pavilion_reboot/surprise_stage` |
| CH3-C05-surprise-bg | `scenes:pavilion_reboot/surprise_stage#portraitBackground` |
| CH3-C06-presenter-excited | `portraits:pavilion_presenter:excited` |
| CH3-C07-presenter-alarmed | `portraits:pavilion_presenter:alarmed` |

Also generate one explicitly labeled carry-forward candidate:

**CH3-B07-attendant-alarmed**

Registry record: `portraits:pavilion_attendant:alarmed`

This pose was assigned to Batch B but remains `not-started`. It is not part of the six already approved Batch B selections.

Total: **eight new candidates**.

## 3. Visual continuity

Use the approved artwork from Batches A and B as authoritative references.

Especially important:

- All three stage environments must share the established People's Pavilion architecture and equipment.
- Do not invent a different auditorium for urgency, locomotion or surprise.
- Preserve the existing camera, presentation platform, curtains and structural landmarks wherever applicable.
- The urgency scene must show the genuine restroom beyond the curtains without implying the protagonist enters.
- The locomotion scene must clearly distinguish moving floor, safe landing area and padded pit.
- The surprise scene must communicate premature confetti and the interrupted presentation.
- Both new presenter poses must preserve the exact identity, costume, scale and bottom anchoring of approved A06.
- The attendant's alarmed pose must preserve the approved A03 identity and anchoring.

Review the new presenter foregrounds composited over their intended backgrounds, including applicable approved Batch A backgrounds.

Review the attendant foreground over the approved record-scanner portrait background.

No rectangular masking artifacts, halos, floating characters or accidental occlusion of important equipment.

## 4. Pixel density — important

Maintain our established cross-chapter visual standard:

**Main scenes: 314×206 logical pixels, displayed at exactly 4× nearest-neighbor.**

Do not switch to double-density scene artwork.

Favor deliberate, larger pixel clusters and simplified architectural detail consistent with Chapters 1 and 2.

Avoid:

- Excessively fine lines
- Faux-pixelated high-resolution illustrations
- Soft antialiased outlines
- Global sharpening
- Resizing an existing scene as a substitute for fresh artwork
- Inconsistent pixel density within the same scene

Portrait backgrounds and character foregrounds remain 564×278.

Portrait foregrounds must have clean binary alpha and no baked-in scenery.

Attempt genuine native-grid authorship. If the generator produces oversized images, preserve the original sources, document all derivations and explicitly report that native-grid authorship remains unproven. Do not claim the limitation has been solved.

## 5. Continuity review

Build comparison sheets showing:

1. Approved A04 verification stage versus all three new stage scenes.
2. Approved A06 presenter versus both new expressions.
3. Approved A03 attendant versus the alarmed expression.
4. New scenes alongside approved Chapter 1 and Chapter 2 main scenes.

Check the images at native 1× and exact 4×.

Pay particular attention to pixel density, line weight, softness, architecture, colors and character consistency.

## 6. Review package

Work on an isolated artwork-generation branch.

Preserve every approved image and historical review package unchanged.

Produce:

- Eight labeled candidate PNGs
- Native and exact 4× previews
- Foreground/background composites
- Side-by-side continuity comparisons
- Exact generation prompts
- Source and derivative files
- SHA-256 hashes
- Dimension and alpha checks
- Documented visual defects
- A Pages-compatible review gallery

Do not deploy directly from the generation branch. Preserve the established `main`-only Pages deployment restriction. If public gallery publication requires a workflow change, prepare a separately reviewable proposal without merging it.

## 7. Boundaries

All eight new candidates remain **generated/unselected** until Nate reviews them.

Do not:

- Modify approved Batch A/B artwork.
- Change narrative, dialogue or gameplay.
- Register candidates as approved.
- Set production asset paths.
- Integrate artwork into the game.
- Begin Batch D.
- Regenerate unrelated assets.

Run the relevant canonical, Chapter 3 and technical artwork QA.

Return the candidate gallery or review location, branch, commit, eight hashes, QA results and outstanding visual concerns.

**Stop for Nate's Art Director review.**