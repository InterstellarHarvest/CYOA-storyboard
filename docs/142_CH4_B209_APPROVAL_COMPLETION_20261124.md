# Chapter 4 B2-09 consolidated v01 — owner approval and gameplay handoff

Nate approved the consolidated B2-09 v01 package on **2026-11-24** after independent native-resolution visual review. This replaces the obsolete B2-09 four-asset plan; the Chapter 4 active primary target remains **63 images** (docs/137/138). Three primary PNGs are **APPROVED / SELECTED** and four conditional frames **APPROVED / PRESERVED AS REFERENCES ONLY**. No PNG is regenerated, resized, palette-reduced, re-encoded or replaced.

**Immutable source:** `InterstellarHarvest/CYOA-storyboard@c8873e773a9cd8bc00eee4c11886f0ab2228e01b`, branch `art/ch4-b209-consolidated-review-20261124`, `tools/prologue-art-lab/assets/review/chapter-04-b209-consolidated-2026-11-24/v01/native/`.

[Review gallery](https://htmlpreview.github.io/?https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/5dc616cdd866aad912e03c2f681e3acf5ba2299f/tools/prologue-art-lab/assets/review/chapter-04-b209-consolidated-2026-11-24/v01/online.html) · [exact hashes and machine-readable approval](142_CH4_B209_APPROVAL_COMPLETION_20261124.json) · [verification results](142_CH4_B209_VERIFICATION_20261124.json) · [independent verifier](../tools/sync/verify-ch4-b209-selection.py).

## Three approved selections

| Unit | Canonical key | Selected public PNG | SHA-256 |
|---|---|---|---|
| CH4-NEW-05 — Bixby, delighted | `portraits:hotel_commodore_bixby:delighted` | `assets/selected/pending-integration/portraits/hotel_commodore_bixby/delighted.png` | `44f81292dc520eeabc6864c21449fb033db4891702c6102634b126b344ee05b8` |
| CH4-NEW-06 — wedding organizer, urgent | `portraits:hotel_wedding_organizer:urgent` | `assets/selected/pending-integration/portraits/hotel_wedding_organizer/urgent.png` | `ffb2444306854dc07373de096ff27e3328b8fe88bd0fe7e2e727a4b6f4127f76` |
| CH4-NEW-18 — shared ballroom threshold | `scenes:grand_bellevue/ballroom#portraitBackground` | `assets/selected/pending-integration/scenes/grand_bellevue/ballroom/portraitBackground.png` | `cc9d19c2413df5b017b72592e3d5c676a84ad0ad91c354093a0a9e0199233e7d` |

The two portraits are **564×278 transparent RGBA with binary alpha**; the background is **564×278 opaque RGB**. CH4-NEW-05 is exactly the existing CH4-B2-49 v01 Bixby portrait, including his empty hands, cap and green paddle. CH4-NEW-06 matches the approved organizer in CH4-05: curled auburn hair, charcoal-slate tailoring, white collar and three clipboards. CH4-NEW-18 shows the reception edge and the fully exposed lower ballroom doors, with no refreshment-table blockage. All new artwork is explicitly **SOURCE-DERIVED**; editable layers, imagegen originals, prompts, materials and provenance remain in the immutable review package. This registration does not assert independent whole-frame native-grid authorship.

## Four approved supplemental frames

All four preserved native files live in `tools/prologue-art-lab/assets/approved/conditional-production-references/chapter-04/b2-09/`:

| Frame | Native PNG | SHA-256 | Conditional meaning |
|---|---|---|---|
| Wheel mounted | `CH4-NEW-18-wheel-mounted-v01.png` | `ba0e7961134a632a522331f57945dd7889f9ae158a27a67e1cadc16cbdf1afc9` | Brass valve wheel with bucket before handoff. |
| Wheel removed | `CH4-NEW-18-wheel-removed-v01.png` | `cc9d19c2413df5b017b72592e3d5c676a84ad0ad91c354093a0a9e0199233e7d` | Wheel handed over; bytes intentionally equal the neutral master. |
| Rubber-band fender | `CH4-NEW-18-rubber-band-fender-v01.png` | `7c4261a915e62c91f394942eac5fe7c0e6f5fc847fcc68b248494cf76c0c850b` | Rubber-band sphere and napkin on bucket, wheel gone. |
| Water emerging | `CH4-NEW-18-water-emerging-v01.png` | `b5b1b1d0cc775cc02cfb61447efe12950fe78ca3e6184602b07c42dac9cb6f65` | Thin water sheet from the visible ballroom door gap; combinable with other states. |

These are **reference-only**, not additional primary art selections or new scene/Focus keys. No flags, node IDs, runtime bindings or automatic dispatch are introduced. In particular, the base and wheel-removed state sharing bytes is intentional, not accidental duplication.

## Storyboard and gameplay handoff

- `hotel_wedding_arrival` and `hotel_bridal_organizer`: organizer **urgent** portrait over shared **ballroom** background. The main scene remains the separately selected CH4-05.
- `hotel_commodore_bixby`, `hotel_bixby_emergency` and `hotel_bixby_trade`: same **delighted** Bixby portrait, never a commanding redraw, over the shared ballroom/reception threshold. The refreshment-table main scene is CH4-05 reused per docs/137; no bespoke close scene.
- Wheel handoff, rubber-band substitution and under-door water appearance follow the authored narrative. **Gameplay PMO must determine the conditional dispatch and timing later** using the seven preserved native PNGs, without inventing Focus IDs or story flags in this artwork registration.
- Suggested engine paths are advisory in the JSON approval record. `assetPath` remains `null`, status `approved`, not `integrated`. The game repository, chapter story JSON, narrative, choices and game import contract are unchanged.

## Preservation and verification

Run `node tools/sync/check-canon.mjs` and `python3 tools/sync/verify-ch4-b209-selection.py` before release. The latter validates hashes, PNG dimensions and transparency, selection metadata, unchanged 196 prior selections, unchanged prior registry records and unchanged narrative/engine-facing files. Source package QA already passed 861 local checks and 174 published-file / 138 PNG public verifications, plus Chromium/Firefox review behavior.

Earlier approvals, all approved conditional references, historical packages, the old B2-09 STOP material and unselected plumber alternatives are preserved. Draft PR #32 remains a separate draft and **must not be merged** as part of this registration. No deploy and no CH4-03 portrait replacement occur.

**Next artwork group:** Revised **B2-10 / CH4-NEW-03 upper salvage mezzanine** in docs/138: depict freight-lift doors, W.C. panel, hatch and service stairs in one reusable scene; salvage clerk is voice-only. The CH4-03 native portrait refinement is separate R1 work, with its current selected portrait retained until a new owner approval.
