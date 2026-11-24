# Chapter 4 gameplay integration: deferred work package

**Owner decision (Nate, 2026-11-24): defer.** These gaps belong to the eventual Chapter 4 gameplay integration, not to the C1/C2 engine PR (game #25) or this consolidation (#31).
- Canonical content and conditions stay exactly as authored.
- Do **not** rename artwork identifiers or remove conditional logic to satisfy the current engine.
- Chapter 4 stays `notForGameplay` until this package is done and approved.

Found by importing real Chapter 4 read-only through the game's importer and validator (game branch `agent/ch4-presentation-capabilities-20261124`, storyboard PR #31).

## WP-1. Two-part Focus A identifiers (3)

The approved canon keys `grand_bellevue/bridal_privacy_panel`, `grand_bellevue/autofit_gown` and `grand_bellevue/three_seashells` have two segments. The engine validator requires `location/scene/target`.
- **Direction:** extend the engine (or the importer's key mapping) to accept or normalise these canon ids without renaming them in the storyboard.
- **Acceptance:** the importer, validator and Focus A presentation all work with the canon ids unchanged; NEW-07/08/09 register under the canon keys.

## WP-2. Per-run conditional text (17 runs)

17 text runs carry their own `if` (for example `hotel_boiler_staff_access` runs 1–2, `hotel_collection_ring_focus`, `hotel_groom_show_ring`, `hotel_chair_follow_collection`). The engine currently refuses an `if` on a run.
- **Direction:** a generic engine capability for conditional runs, evaluated against state at presentation time, deterministic in saves and replay, with conditions kept exactly as authored.
- **Acceptance:** all 17 runs import unchanged. Route tests show each variant on its real routes, and NOTES and replay keep the variant that was shown.

## WP-3. Fatal-ending popups and aftermath art (4)

`fatal_stall_final_occupancy`, `fatal_boiler_pressed_and_steamed`, `fatal_lot61_folded` and `fatal_bridal_made_to_measure` carry `deathPopup` / `endingArt`, which the importer rejects as node fields. Chapters 1–3 route these through `story/death-presentations.export.json` and the game's death-presentation content.
- **Direction:** route Chapter 4's four popups through the same export path, unchanged, with the aftermath art bound when NEW-14–17 are approved.
- **Acceptance:** `export-death-presentations --check` covers all four; the game shows each popup and its BEGIN AGAIN / RETRY / CHECKPOINT controls as in earlier chapters.

## Also seen (same integration task; content unchanged here)

- **Three park exits with no card** (`hotel_service_park_exit`, `hotel_bridal_corridor_park_exit`, `hotel_bridal_lavatory_park_exit`): they need the chapter hand-off to Chapter 5 or the agreed ending presentation.
- **Echo on a Focus node:** `hotel_collection_ring_focus` has a USE `red_stapler` `say` echo, which the engine allows only in dialogue nodes.
- **Unmarked 100% check:** one ring check (`hotel_chair_ring_focus` / `focus_free_ring_careful`) can reach 100% through mods without being marked `certain`.

## Already done (not part of this package)

- C1 text-led scenes and C2 voice-led dialogue: game PR #25.
- Player speaker correction: docs/139.
- Reuse scene keys still bind at integration through the existing `reused` status (docs/137 C3).
