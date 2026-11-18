# Fatal-node contract — death popup data belongs to the storyboard

Owner rulings, 2026-11-16: the storyboard is the canonical source from which Gameplay PMO imports scene and ending data. Every fatality box must supply **all three** death-popup essentials: **illustration/artwork ID**, **popup title**, and **popup narrative beat**. The inspector must show these in a dedicated **Death popup · engine handoff** section, **not** under "Choices & destinations." The graph node itself displays the title, short beat and art ID. Original narrative and mechanics remain intact.

## Single-source representation

Each fatal node in `story/chapters/*.draft.json` has exactly one `deathPopup` object, for example:

```json
{
  "end": true,
  "endingArt": "house_of_tomorrow/rest_assured",
  "deathPopup": {
    "id": "rest_assured",
    "title": "PERMANENTLY SATISFIED.",
    "subtitle": "REST ASSURED — TREATMENT COMPLETE",
    "description": "You have achieved permanent relaxation. The House is delighted to report that its newest customer has stopped complaining.",
    "artRef": "house_of_tomorrow/rest_assured",
    "status": "approved-art-copy-draft"
  }
}
```

The art key resolves into `story/artwork.draft.json/deathScreens`, with `status`, `dimensions`, `prompt`, selected file provenance, etc.

The retained `BEGIN AGAIN` system choice in older story data is legacy gameplay compatibility, **not a choice to list within a fatality box**. Popup controls are governed by Gameplay PMO's separate, more recent Retry / Checkpoint / Exit contract. Existing death scenes and game rules are not rewritten by this metadata.

## Owner-specific Rest Assured rule

Chapter 1's `exit_chair_fatal` has three inbound causes: voluntary Rest Assured, failed stapler escape, failed bare-handed escape. They all end with the same permanently restraining chair and death, and **share exactly one fatal node, one popup, and one already approved illustration**. The owner's latest ruling overrides an older recommendation to draw different images per cause. Never regenerate the approved image.

Exact approved native PNG: `InterstellarHarvest/CYOA@agent/rest-assured-death-visual-proof:art/deaths/rest_assured_voluntary.png`; SHA-256 `7f469efa40548568af5dfe3c11602b9c6293282d9574caa5f36fc37113e72d9c`. Image content and design are frozen; any remaining popup text is a draft pending copy review.

## Coverage

Nine fatal endings = nine popup data records and nine unique `deathScreens` art records:
- Chapter 1: `exit_chair_fatal` — **PERMANENTLY SATISFIED.** — approved art.
- Chapter 2: `fatal_sorter` (**CLASSIFIED AS COMPOST.**), `fatal_hopper` (**NEW ARRIVAL.**), `fatal_transformation` (**PERSONAL GROWTH.**), `fatal_planting` (**RECLASSIFIED.**), `fatal_roots` (**SITE IMPROVEMENT.**) — new artwork briefs, popup wording drafts.
- Chapter 3: `end_model_citizen` (**A MODEL CITIZEN**) — approved fatal mechanism, ungenerated art; `end_reconciled` and `end_archived` — deliberately provisional concept and copy.

Every death vignette is native **314×206**, displayed at **2×** inside the previously selected A1 modal. The older 565×451 on unproduced Chapter 3 death prompts was wrong (item-inspection art size) and is corrected.

## ENGINE EXPORT — mandatory for Gameplay PMO

The normal game story importer (`InterstellarHarvest/CYOA/tools/story-import/convert.js` on the earlier story branch) **currently removes** `deathPopup` and `endingArt` as authoring-only metadata. Therefore, fatal story JSON alone does **not** guarantee a functioning engine popup.

The canonical public repo now generates an explicit engine handoff:

```sh
node tools/storyboard/export-death-presentations.mjs
node tools/storyboard/export-death-presentations.mjs --check
```

Committed output: **`story/death-presentations.export.json`**, published next to the chapter source files.

Each entry has stable `id`, `when.end`, `title`, `subtitle`, `body`, `narrativeBeat`, `artwork.id`, `artwork.status`, selected/proposed asset path, provenance/hash, and `readyForGameplay` flag. This file is derived deterministically from the fatal node `deathPopup` and the shared artwork catalog, not independently authored. The Pages workflow and storyboard review CI reject out-of-date exports. The header offers an **Export death popups** download link.

**Gameplay PMO must consume `story/death-presentations.export.json` when integrating death popups**, or explicitly update its importer to carry identical fields without duplication. Do not silently drop popup metadata or create parallel manually maintained text/art entries in the game. The export is a data contract; it does not by itself activate any player-facing death modal. Before runtime enablement, honor pending art, finalized copy, save/checkpoint controls, and engine QA.

## Status semantics

An already-approved image remains approved despite no public preview image bytes being mirrored. `not-started` art needs production; `proposed` ending narrative needs owner story approval. A popup text draft is not a finished owner-approved joke. New images follow normal Codex → ChatGPT review → approval → Gameplay PMO integration flow.

The storyboard's death-popup inspector must clearly expose the title, narrative beat, and artwork record even when the approved illustration is not yet publicly previewable; it must never confuse a missing public thumbnail with a requirement to regenerate already-approved art.

## Death-popup copy approval — 2026-11-18

The Story Director approved the exact current title, subtitle and body text of the six death popups the game uses (PMO ruling, final PR #2 corrections):

| Node | Title |
|---|---|
| `chapter-01:exit_chair_fatal` | PERMANENTLY SATISFIED. |
| `chapter-02:fatal_sorter` | CLASSIFIED AS COMPOST. |
| `chapter-02:fatal_hopper` | NEW ARRIVAL. |
| `chapter-02:fatal_transformation` | PERSONAL GROWTH. |
| `chapter-02:fatal_planting` | RECLASSIFIED. |
| `chapter-02:fatal_roots` | SITE IMPROVEMENT. |

**What changed:**
- `deathPopup.status` moved to `owner-approved`. Each node's notes record the approval.
- The derived export carries `popupStatus: owner-approved` and, since their art is integrated, `readyForGameplay: true`.

**Not changed:**
- No wording.
- Artwork approval and integration status, which stay in the artwork catalog, separately.
- Chapter 3 entries.
