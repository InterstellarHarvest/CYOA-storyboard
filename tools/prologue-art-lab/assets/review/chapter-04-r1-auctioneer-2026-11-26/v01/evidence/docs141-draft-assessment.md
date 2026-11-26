# CH4-03 refinement assessment and the B2-09 review sheet

**Status:** review record only, on a draft PR; not merged. Nate's decisions, 2026-11-24:
- CH4-03 joins the Chapter 4 refinement-review queue as its **sixth** candidate;
- its approval, selected file, hash and history stay intact, and it is not replaced automatically;
- B2-09 selection waits for Nate's visual review;
- no organizer portrait, water variant or refinement redraw is generated;
- the B2-09 STOP notice stays active.

## 1. B2-09 review sheet

[B2-09_proposed_selections_comparison.png](141_evidence/B2-09_proposed_selections_comparison.png), at exact 2× nearest-neighbour, labelled NOTHING SELECTED:
- CH4-B2-49 over CH4-B2-51 (`hotel_commodore_bixby`), over CH4-B2-51-emergency (`hotel_bixby_emergency`) and over CH4-B2-51-trade (`hotel_bixby_trade`);
- CH4-B2-51-emergency alone, as the shared ballroom background;
- approved references CH4-03/CH4-02 and CH4-B2-43/CH4-B2-47, the CH4-05 ballroom, and CH4-02 (lobby-only);
- a 4× face-detail strip.

The sources are the unselected review package at `b896f50` and the selected files on main. All four proposed assets stay **UNSELECTED** and unregistered.

## 2. CH4-03 (auctioneer, showman): added to the refinement queue

| | |
|---|---|
| Record | `portraits:hotel_auctioneer:showman`, approved 2026-11-22 (docs/127); 6 story nodes |
| Selected file | `assets/selected/pending-integration/portraits/hotel_auctioneer/showman.png`, SHA-256 `231baf25ffd00511144693927354e73f42cae4f052964a9db0a99323689a0d78`. **Unchanged**: byte-identical to the approved v08 source at `3463e20` |
| How it was made (pinned derivation evidence) | The 1788×880 generated original `6727d162…` (hash verified) → premultiplied-alpha **Lanczos** reduction to 564×278 → cutout cleanup → **UnsharpMask** (radius 0.55, 85%) on interior features. `paletteReduction: false` |

**Evidence:** [CH4-03_refinement_assessment.png](141_evidence/CH4-03_refinement_assessment.png) shows native 2× composites, 4× face and gavel-hand crops beside the original, CH4-B2-31 and the Chapter 2 style, and an alpha map.

| Measure | CH4-03 | CH4-B2-31 (same auctioneer, B2-06) | CH4-B2-35 | CH4-B2-43 | Chapter 2 conductor | Chapter 2 groundskeeper |
|---|---:|---:|---:|---:|---:|---:|
| Colours (RGBA) | **12,198** | 61 | 60 | 62 | 50 | 61 |
| RGB colours in the figure interior | **10,508** | 61 | 60 | 62 | 50 | 61 |
| Colours used by a single pixel | **82%** | 0% | 0% | 0% | 8% | 5% |
| Alpha levels | **205** | 2 | 2 | 2 | 2 | 2 |
| Partly transparent pixels | **30,597** | 0 | 0 | 0 | 0 | 0 |

**Findings:**
1. **Continuous-tone colour, not pixel clusters.** Lanczos resampling plus sharpening makes almost every pixel its own colour (10,508 RGB). At 4× the face, hair and hands read as a reduced digital painting: soft blended shading and smeared edges. The approved Chapter 2 and later Chapter 4 portraits are built from about 60 deliberate stepped clusters. The original itself is a 39,300-colour painting; the reduction preserved that character instead of reinterpreting it at the native grid (docs/129 §1–2).
2. **The interior is not opaque.** **95.5%** of the figure has alpha 250–254 (mostly 253). Every other approved portrait uses binary alpha. Composited over its lobby background, 22,969 pixels differ from an opaque version: about 1% background bleed throughout and up to 90 levels at the soft edges. The colour of the figure therefore shifts slightly with whatever is behind it.
3. **Identity drift against the same character.** Next to CH4-B2-31 / B2-35 (the same auctioneer, approved later with palette discipline), CH4-03 has cooler skin, a duller jacket and finer, softer modelling. The two would visibly alternate within one auction conversation (`hotel_auctioneer_arrival` uses CH4-03; `hotel_auction_testimonial` uses CH4-B2-31).
4. **Contracts still pass.** Size 564×278 RGBA; check-canon only requires that some pixels are transparent. The art is attractive and the composition is good. This is a style and pipeline mismatch, not a content error.

**Refinement requirement, queued (R1, docs/138). Not started:**
- Redraw natively at 564×278 from the approved composition: pose, gavel grip, bow tie, pocket square, expression and tailoring.
- Use a disciplined palette (about 60–70 colours, like CH4-B2-31 / B2-35) and **binary alpha**.
- Match the approved auctioneer identity of CH4-B2-31 / B2-35 / B2-36.
- Publish it UNSELECTED for Nate's comparison. CH4-03 stays selected until he chooses.

**Option for Nate only, not applied:** a purely mechanical alpha correction (interior alpha 250–254 → 255) would remove the bleed without touching any colour. It is still a change to approved bytes, so it needs his explicit approval and a new approval record. It would not fix finding 1.

## 3. Queue after this decision

**R1 refinement candidates (6):** CH4-01, CH4-04, CH4-05, CH4-B2-03, CH4-B2-11, **CH4-03**.

Observation only, not queued: CH4-02 (lobby background, Batch 1) has 689 colours against 123–172 for the other approved closer backgrounds (docs/137 §2).

docs/138 remains the controlling production brief. docs/140 remains the deferred integration package.
