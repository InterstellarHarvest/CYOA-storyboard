# Chapter 4 B2-12 — Codex artwork production brief

**Scope: two primary images** for *Out of Order*, Chapter 4, and only the minimum useful conditional references:

1. **CH4-NEW-01 — Grand Bellevue bridal dressing room**, main scene, **314×206 opaque RGB**.
2. **CH4-NEW-07 — BRIDAL PRIVACY SYSTEM** smart-door panel, **Focus A, 565×451** (follow the established focus art contract and correct opacity).
3. Only narratively meaningful `bridal_privacy_status` reference states (e.g. access denied / provisional authorization), with exact shared underlying panel geometry. Supplemental states do **not** get new Focus IDs or runtime bindings yet.

This is the revised B2-12 queue in `docs/138_CH4_B209_REVISED_PRODUCTION_BRIEF_20261124.md`. Do not regenerate B2-10/B2-11, repeat the completed consolidation, or pull in B2-13 AutoFit gown Focus, B2-14 bridal lavatory / three-seashell Focus, or unrelated death/item images.

## Narrative and visual canon

Read `docs/129_PERMANENT_PIXEL_ART_PRODUCTION_STANDARD_20261122.md`, docs/137–139 and current `story/chapters/chapter-04.wip.json`, especially nodes `hotel_bridal_room`, `hotel_bridal_door_knock`, `hotel_bridal_door_focus`, `hotel_bridal_criteria`, `hotel_bridal_emergency_override`, `hotel_bridal_autofit_survived` and later door return. Do not infer absent scenes or flags. No narrative, choice or inventory edits.

- The room contains a second, closed **bathroom door** with **no physical handle or keyhole**. A polished brass camera/screen panel announces BRIDAL PRIVACY SYSTEM; **only the bride is authorized**. The smart-door AI is **voice-only**, not a person or portrait.
- A conspicuous white wedding gown hangs on a **wheeled dressing stand**, its very narrow waist a darkly comic warning. Keep the overall dressing room believable as the same pseudo-luxurious, technologically absurd Grand Bellevue as the approved lobby/ballroom: burgundy, faded cream, green/teal, upholstered furnishings and polished surfaces concealing old pipework, overbearing bureaucracy and slight decay.
- The Focus A panel reveals the camera, authorization screen and iconography for **visual identification**, **bride-only access** and **pre-wedding groom exclusion**. Design at 565×451 for readable pixel lettering where essential; the story/dialogue carries long wording, so do **not** cram entire paragraph text into tiny raster lettering.
- Conditional panel states should convey denied/locked status versus provisional bridal authorization with a green light/lock click. If one base plus one clearly distinct status overlay suffices, use that; no per-line images for every exchange. Keep the door closed in the dressing-room base; the later lavatory scene is a different production group.
- Character art: no organizer in the room (she has left), no invented attendants, bride or player face. Do not give the door AI a human portrait. The wedding gown is an object, not a dressed character.

## Owner's first-pass quality rule

Nate prefers coherent, detailed **first-pass** scenes, not v01–v09 cosmetic patch cycles. Use approved Chapter 2 high-detail low-palette main scenes and approved Chapter 4 lobby, ballroom, staff lavatory, and B2-11 public corridor as benchmark **at the native grid and exact 4×**, choosing references of the same asset class (main scene vs Focus). Read the approved B2-10 stop rule at `tools/prologue-art-lab/assets/review/chapter-04-b210-upper-salvage-2026-11-24/PMO-V03-APPROVAL-AND-STOP-RULE.md` on its review branch if not yet on main. It supersedes the impulse to micro-polish a scene that already reads well.

Create/select a strong detailed large concept image if useful, but it remains **reference only**; independently construct the production art at native size with crisp, intentional clusters and restrained palette. No simple downscale, posterized transfer or over-schematized programming rectangles passed off as finished work. Preserve honest `SOURCE-DERIVED` provenance and editable native masks/layers; use consistent lighting, depth and material-specific texture. **Do not make the clean hotel lavish or sterile**—the veneer and exposed stupid technology are the joke.

Self-critique one complete first pass against approved artwork. Revise only for a real issue: unreadable bathroom door/panel/gown, broken action geography, materially inconsistent lighting, wrong story object, or illegible Focus indicators. Favor one coherent correction rather than endless small pixel adjustments. Stop at good, publish UNSELECTED for Nate's review; do not self-approve.

## Publication and restrictions

Use branch `art/ch4-b212-bridal-privacy-review-20261125`. Package under `tools/prologue-art-lab/assets/review/chapter-04-b212-bridal-privacy-2026-11-25/v01/`, with source concept original/prompt, native layered recipes, final PNGs, exact4× previews, hashes, labeled comparison sheets (approved Ch2/Ch4 main and Focus references), browser gallery `online.html`, replay/quality checks and transparent provenance. Publish UNSELECTED on review branch. If image-generation tools are unavailable, report the blocker; do not replace concept art with inferior code-drawn placeholders.

Do **not** alter canonical main, `assets/selected`, previously approved images, any narrative/gameplay file, runtime paths, or draft PR #32. Registration follows **Nate's explicit approval only**, through separate engineering validation.
