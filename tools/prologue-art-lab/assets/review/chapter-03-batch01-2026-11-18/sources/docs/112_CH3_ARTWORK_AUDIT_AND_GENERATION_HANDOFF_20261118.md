# Chapter 3 — Artwork Audit, Quarantine and Batch A Handoff

**PMO date:** 2026-11-18. **Status:** 29 complete artwork briefs registered; **no Chapter 3 images have been generated, selected or integrated.** The narrative is owner-approved and locked for art.

Source of truth: `story/chapters/chapter-03.reboot-candidate.json`, blob SHA `857ffdf1bc9432cf4bbbfd7819f5f430a06d9036`. Authority: `docs/111_CH3_ARTWORK_PMO_HANDOFF_AND_NARRATIVE_LOCK_20261118.md`, then docs/110 and docs/109. The pre-reboot `story/chapters/chapter-03.draft.json` and archived old art are historical only.

All work is on an isolated artwork branch. The public storyboard manifest still points to the archived old Chapter 3. No permission to activate it, edit the playable game or merge to public `main`.

## Production inventory and scene reuse

The shared `story/artwork.draft.json` now has **14 new native 314×206 scene briefs**, **eight independent opaque 564×278 closer portrait backgrounds**, and **seven transparent 564×278 human pose foregrounds**. Every new record is `not-started`, with a complete exact prompt, `assetPath: null`, source node references and a *suggested* filename. A suggested path is not an existing PNG.

| Scene suffix after `pavilion_reboot/` | Source nodes / scene-reuse judgment | Batch |
| --- | --- | --- |
| `arrival` | `pavilion_arrival`; the three Chapter 2 entry groups converge on one real Pavilion approach | B |
| `restroom_entrance` | `real_restroom`, `attendant_greeting`, `attendant_refusal`, `attendant_key_callback`, `door_wait`, `door_choices`; one genuine restroom hallway, consistent reader, bench and visible gate | **A** |
| `human_verification_stage` | `human_verification_arrival`, `presenter_verification`, `photo_verification`, `photo_verification_reply`, `unauthorized_presenter`; foundational stage and camera design | **A** |
| `urgency_stage` | `authentic_urgency`, `authentic_urgency_visitor`, `authentic_urgency_reply`; same stage with curtains, rotating floor and real restroom visible | C |
| `locomotion_stage` | `human_locomotion`; same show machinery, now moving floor, net and padded pit | C |
| `backstage` | `locomotion_pass`, `backstage_exit`; shared ordinary backstage corridor and exit | D |
| `exterior_exit` | `locomotion_fail`, `door_dash_fail`, `door_reverse_end`; daylight exterior can truthfully support three harmless exits | D |
| `surprise_stage` | `genuine_surprise`; original verification stage with early confetti and backstage door | C |
| `service_exit` | `presenter_help_end`, `attendant_honest_end`; same humble daylight passage for two different humans | D |
| `record_printer` | `record_print`, `record_challenge`, `record_choices`, `stapler_printer_snarl`, `attendant_honest`; one receipt printer/counter | B |
| `record_scanner` | `record_scanner`, `record_scanner_result`; distinct view of one-way reader and paper roller | B |
| `paper_emergency` | `paper_problem_end`; harmless cleanup brushes and paper snarl | B |
| `exit_vestibule` | `door_dash_pass`; real tiles, unreachable inner gate, automatic ramp | D |
| `courtesy_stage` | `door_courtesy`; actual door frame slides sideways on track, restroom remains shuttered | D |

The scene list expresses *14 scene requirements*, not a mandate to redraw identical architectural elements from scratch. Preserve physical continuity, but create a distinct source where a machine or camera angle actually changes. No Focus A, new inventory illustration or Chapter 3 death image is authorized. Existing Facilities Key, Family Photo, Red Swangline Stapler and Timing Clicker art remain exactly unchanged.

### Human conversation coverage

| NPC | Scene/portrait background contexts | Required foreground poses |
| --- | --- | --- |
| Pavilion Attendant | `restroom_entrance`, `record_printer`, `record_scanner`, `service_exit`, `courtesy_stage` | `idle`, `alarmed`, `quiet` |
| Pavilion Presenter | `human_verification_stage`, `urgency_stage`, `surprise_stage`, `service_exit` | `idle`, `excited`, `alarmed`, `relieved` |

This is **nine contexts and eight distinct opaque close backgrounds** because `service_exit` serves both people at different moments. Each transparent pose is a separate native-resolution human layer sharing facial identity, outfit, scale and canvas anchor with its character's other poses. Backgrounds are *independently authored tighter views* of the correct scene—not blurred crops, enlarged scenes, or unrelated panoramas.

**Proposed first design, pending Nate's visual selection:** a reassuring middle-aged male attendant, tidy small spectacles, cream shirt and muted-teal uniform vest; a lively female presenter with short auburn bob, muted coral blouse and slate-blue jacket. Their expressive, believable human faces should contrast with the absurdity of the machinery. They must look different from the locked receptionist art. These designs are briefs, **not owner-approved images**.

The approved Chapter 3 events explicitly involve visible human attendant, presenter and one-use visitors. When a scene needs a tiny staged human figure to be truthful, this specific chapter requirement takes precedence over the old general unpopulated-room direction. Conversation portrait **backgrounds themselves remain empty of the foreground NPC**, because the human is separately layered. Never reveal the protagonist's face or show a physical Original/duplicate. The real restroom must unmistakably work.

## Historic-art quarantine

All **65** old Chapter 3 image records are preserved with their prompts and old `not-started` status, but their `notes` now begin **ARCHIVED / RETIRED / UNUSED — PRE-REBOOT CHAPTER 3**. That covers 21 old `pavilion/*` scenes, seven Focus A records, three old death illustrations, two old portraits (Registrar **and** Original Witness), and 32 slot/inspect records for 16 obsolete `pavilion_*` items. The 16 old item definitions remain in the item registry for archived history, but no reboot node references them.

`archived` is **not** a valid artwork status enum: we deliberately used the existing `notes` field. The storyboard UI now shows **ARCHIVED · DO NOT GENERATE**, its **Active pending** filter excludes historical calls, and a separate **Archived** filter shows them for provenance. The older fatal-popup brief language remains historical only; **all seven new Chapter 3 endings are surviving**.

The old Chapter 3 JSON archive and all preexisting selected artwork bytes remain untouched. No old prompt is a source for new generation.

## Batch A — six foundation candidates

Generate the following in order, using the **exact full `prompt` field for each record** from `story/artwork.draft.json`. Combine it with the catalogue's shared `direction` and this handoff's specific Chapter 3 human staging clarification. Candidate IDs below must appear verbatim in the generation manifest and gallery.

| Candidate ID | Exact catalogue record | Native output |
| --- | --- | --- |
| **CH3-A01-restroom** | `scenes:pavilion_reboot/restroom_entrance` | Opaque 314×206 main scene |
| **CH3-A02-restroom-bg** | `scenes:pavilion_reboot/restroom_entrance#portraitBackground` | Opaque 564×278 closer background |
| **CH3-A03-attendant-idle** | `portraits:pavilion_attendant:idle` | Transparent RGBA 564×278 foreground |
| **CH3-A04-verification** | `scenes:pavilion_reboot/human_verification_stage` | Opaque 314×206 main scene |
| **CH3-A05-verification-bg** | `scenes:pavilion_reboot/human_verification_stage#portraitBackground` | Opaque 564×278 closer background |
| **CH3-A06-presenter-idle** | `portraits:pavilion_presenter:idle` | Transparent RGBA 564×278 foreground |

Candidate filenames: `CH3-A01-restroom-v01.png` through `CH3-A06-presenter-idle-v01.png`. Proposed *production* filenames are in the catalogue, but do **not** write to these production paths or set `assetPath` now. This batch establishes physical architecture and the character model sheets; later poses must use the selected models.

Approved visual references, **read-only**:

- `assets/selected/art/scenes/conference_hall/reception/reception_scene.png`
- `assets/selected/art/portraits/receptionist/reception_background.png`
- `assets/selected/art/portraits/receptionist/receptionist_idle.png`
- `assets/selected/art/scenes/house_of_tomorrow/foyer.png`
- Selected Chapter 2 images/gallery reference PNGs under `assets/selected/` and `tools/prologue-art-lab/assets/review/`

The restroom scene must include credible genuine sinks/stalls, an inner gate, a small seated attendant and believable visitor flow; this is **not** another House bathroom prop. The stage must be cheerfully optimistic, with a large camera, movable platform, countdown, presenter and a nearly empty audience. Match the real approved reception's art density and visual materials, not its literal room layout.

## Copy-ready Codex generation instruction

> You are Codex, the **Chapter 3 Artwork Generator** for *The Acceptable Error*. Work only on a separate generation branch of `InterstellarHarvest/CYOA-storyboard` based on the approved Chapter 3 artwork-brief branch. Read `docs/111_CH3_ARTWORK_PMO_HANDOFF_AND_NARRATIVE_LOCK_20261118.md` and `docs/112_CH3_ARTWORK_AUDIT_AND_GENERATION_HANDOFF_20261118.md` completely. Verify the candidate narrative blob is `857ffdf1bc9432cf4bbbfd7819f5f430a06d9036`. Generate **only Batch A's six images A01–A06**, taking the exact full prompts from their registered `story/artwork.draft.json` records and the global art direction (with doc 112's specific human-staging exception). Author true native pixel art at precisely 314×206 or 564×278 as specified, with independent opaque scene-specific portrait backgrounds and transparent, separately composited human foregrounds. Never create an embodied Original, show the protagonist's face, revive `pavilion/*` art, redraw approved prior chapters, invent a death image, item or Focus A, or edit narrative/gameplay.
>
> Place original immutable candidates in `tools/prologue-art-lab/assets/review/chapter-03-batch01-2026-11-18/`. Record candidate IDs, generation sources, exact prompts, native filenames and SHA-256 hashes; prove actual dimensions, alpha, transparent composition and legible native-scale signage. Create a public Pages-compatible review gallery with 1× native and 4× nearest-neighbor views, foreground/background composite proofs, approved references and QA results. Keep all candidates **generated/unselected**, without `approved`, `integrated` or invented production `assetPath`. Stop after the six images and return the gallery URL, isolated branch/commit, hashes and visible defects for Nate's creative selection. Do not merge anything or integrate game assets.

After Nate selects a candidate, **selection means approval**: record its exact identity, source path/hash and `approved` status, even if gameplay integration is still pending. Never leave selected imagery looking unfinished. Actual production paths belong to the later Claude Gameplay PMO integration confirmation.

## Verification gates

Run:

1. `node tools/storyboard/prepare-ch3-artwork-briefs.mjs --check`
2. `node tools/storyboard/qa-ch3-artwork-briefs.mjs`
3. `node tools/storyboard/qa-ch3-reboot-candidate.mjs`
4. `node tools/storyboard/qa-smoke.mjs`
5. `node tools/sync/check-canon.mjs`
6. `node tools/sync/qa-sync.mjs`

Image production requires additional pixel/dimension/alpha QA and owner creative review. **No gameplay integration or public-main merge is authorized by this plan.**
