# Storyboard Timeline Layout — Chapter 1 and Chapter 2

**Status:** REVIEW BRANCH ONLY (`agent/storyboard-timeline-ch01-ch02`, from `main` 0ebcf48). 2026-11-16. Not merged and not deployed. The public site stays unchanged until the owner approves.

> **Update (owner follow-up, same day):** PR #2 was merged. The Prologue now also uses the timeline, chapter pills select/inspect/drag instead of switching chapters, and the view is remembered per chapter. See the addendum at the end; statements below that the Prologue is unchanged are superseded. Chapter 3 is still unchanged.

## What changed

Chapter 1 (36 nodes) and Chapter 2 (99 nodes) are now drawn as a left-to-right timeline.
- They open at 100% zoom at the start of the chapter.
- Authored incidents stay together.
- Labelled connectors sit beside the decision they leave.
- Pills mark the routes between chapters.

The Prologue and Chapter 3 still use the original `layout()` and `redrawEdges()` code without any change. The QA proves they render identically (see the end of this document).

No story, item, artwork or manifest file was changed. Only these files changed:
- `tools/storyboard/index.html`
- `story/storyboard-layout.json`: viewer-only metadata for Chapters 1 and 2.
- The storyboard QA scripts.
- README.
- A PR-only review workflow.

## Why the old layout failed

- **Kahn layering.** `layout()` layered the graph with Kahn's algorithm. Every node left on a cycle got the same "tail" depth. So the dinner/foyer/Martin group (6 nodes) and the housekeeping group (3 nodes) in Chapter 1, and all three antidote-kit loops in Chapter 2, were pushed into one far-right column. There they sat beside unrelated nodes.
- **Fit.** The default Fit then shrank a 99-node chapter to around 25%, where the text cannot be read.
- **Labels.** Edge labels were cut at 23 characters and centred on the curve, so labels on parallel connectors overlapped.

## Layout algorithm (deterministic)

1. **Connectors.** There is one connector per source→destination pair. Each authored route keeps its own label line:
   - **Choice** lines are plain.
   - **PASS** / **FAIL** lines have a badge.
   - **SHOW** / **USE** item routes are dotted.
   - When the same check passes and fails into the same destination, it gets one explicit `PASS|FAIL` line. It is never a generic "2 routes" line.
2. **Cycle groups.** Tarjan finds the strongly connected components. Inside each group, the order is chosen by brute force (the groups have at most 7 nodes; larger ones fall back to breadth-first order). The rules, in priority order:
   - The group starts at an entry node: one reached from outside the group, or the chapter start.
   - It has as few backwards connectors as possible.
   - It stays close to breadth-first reading order.
   - Ties go to authored order.

   The few backwards connectors left over become explicit **return** connectors.
   - Chapter 1: `storage_reclaimed → comfort_offer` and `dinner_redirect → dinner_arrival`.
   - Chapter 2: the six kit→exit returns (the PASS|FAIL "use the antidote" routes of each kit and read-label view).
3. **Columns.** Longest path over the condensed acyclic graph, with each return reversed as a constraint, so every forward connector moves right.
   - Surviving chapter exits are aligned in the last column, so the five House exits and the five Biology Park living endings form a recognisable right edge.
   - Fatal endings stay in the column just after the choice that causes them.
4. **Waypoints.** A connector that spans more than one column gets a reserved 14px slot in every column it crosses. Lines run straight through their own slots and only curve in the gaps between columns, so they never cross a card.
5. **Order within each column.**
   - 24 barycentre sweeps run downward and upward, and the order with the fewest crossings is kept.
   - Incidents from `storyboard-layout.json` stay contiguous in every column.
   - Waypoint slots sit between incident stacks, not inside them.
6. **Rows.** Each column is solved by weighted isotonic regression (pool-adjacent-violators) toward the average height of its neighbours. Each item's spacing allows for:
   - the card itself, 30px apart, or 14px around waypoint slots;
   - the height of its label stack;
   - the lanes under a card used by return connectors;
   - the incident title above the first card of an incident.

   As a result, cards and labels cannot overlap.
7. **Gaps.** The gap after each column is wide enough for the widest label stack leaving it, plus room for a curve. Labels use a monospace font, so widths are computed the same way in every browser and in the Node smoke test. Labels are up to 30 characters; return labels fit under the card. The full text is in the hover tooltip and in the inspector.

Return connectors leave from under the source card and carry a `↩` label there. They run left in their own lane in each gap and arrive under the destination with an upward arrow. They are dashed violet.

When a node is selected, its connectors are drawn thicker.

## Incidents (viewer-only metadata)

`story/storyboard-layout.json` → `chapters.chapter-01` / `chapter-02` now carry `layoutRevision: 2` and a `timeline.incidents` list.

| Chapter | Incidents |
|---|---|
| Chapter 1 | Arrival · badge · House introduction; Housekeeping & storage; Comfort, refreshments & dinner; Martin & the wardrobe passage; Family photographs & album; Rest Assured chair & service escape; Surviving House exits → Chapter 2 |
| Chapter 2 | Conveniences Bureau & groundskeeper; Sorting & hopper outcomes; Environmental Control Tower; Spore Garden & damaged walkway; Moving Forest; Tour tram & reserve tram; Central flower, appeals & planting; Translator sabotage & late tower; Courier route & customs exit; Public exit & antidote kit; Irrigation & maintenance exit; Living endings → Chapter 3 (preview) |

The private importer never reads this file: `convert.js` names it as not read, and `validate_story_import` checks that it is never read. The manifest is untouched, because the importer rejects unknown manifest keys.

## Routes between chapters

These pills are diagram markers only. They are not `.node` cards and add no story nodes.

- **Chapter 1 → Chapter 2.** Each of `exit_named_plant`, `exit_martin`, `exit_service_clean`, `exit_service_registered` and `exit_showroom_reset` has a solid teal pill: "TO CHAPTER 2 · GAMEPLAY → Bureau Arrival". Each comes from its authored `chapter:"chapter-02"` choice. Clicking a pill opens Chapter 2 at `bureau_arrival`. `exit_chair_fatal` has none: it is terminal.
- **Into Chapter 2.** Five "FROM CHAPTER 1 EXIT" pills, one per surviving House exit, all feed the single canonical `bureau_arrival`. Its narration varies by route. The `bureau_arrival` inspector lists the five routes. Clicking a pill opens Chapter 1 with that exit selected.
- **Chapter 2 → Chapter 3.** `end_concourse_robot`, `end_underground_station`, `end_public`, `end_maintenance` and `end_customs` each have a dashed amber pill: "PREVIEW HANDOFF · NOT GAMEPLAY", from `storyboardNextChapter`. Their tooltip says the game ending is unchanged. The five fatal Chapter 2 endings have no pill.
- **Chapter 1** also shows its one real incoming route, the Prologue `reception_hallway` CONTINUE.

Chapter 3 is still drawn with the original code and shows no pills.

## Saved positions in the browser

- Cache entries for a chapter with `layoutRevision` > 1 are written as `{positions, layoutRevision}`.
- On load, a cached Chapter 1 or 2 entry from an older revision is handled like this:
  - If it is not empty, it is copied to `cyoa-storyboard-layout-v1:<chapter>@archive-r1`. An existing archive is never overwritten.
  - The stale entry is removed, so the timeline is the default.
  - **Restore previous arrangement** applies the archive.
- The Prologue and Chapter 3 have no revision. Their cache entries are never read differently, rewritten, archived or removed.
- **Reset Layout** resets only the chapter you are viewing.
- **Export Layout** keeps schema `cyoa-storyboard-layout-v1` and adds `layoutRevision` and `timeline` for Chapters 1 and 2. The Prologue and Chapter 3 entries keep the exact `{positions}` shape.
- An import is a deliberate choice, so its positions always apply, including older v1 files without metadata. A file without `timeline` keeps the current incident metadata.

## QA

| Suite | Before (main 0ebcf48) | Now |
|---|---|---|
| `qa-smoke.mjs` (Node, dependency-free) | PASS (29 checked areas, 412 assertions executed) | PASS (51 checked areas, 24,620 assertions executed) |
| `qa-browser.js` (Chromium + Firefox) | 22/24: the stale "exactly three chapters" check failed in both browsers | 24/24 (that check now expects the four manifest chapters) |
| `qa-timeline.js` (new, Chromium + Firefox) | — | 88/88 |

### New checks

- **Rendering.** All 36 and 99 nodes are rendered. No card, port or label overlaps, measured from real bounding boxes. Every connector is sampled every 5px (about 30,000 points) and never passes through an unrelated card or port.
- **Left to right.** Forward connectors run left to right. Return connectors appear only on real cycles.
- **Routes preserved.** Every authored route is drawn exactly once and none are invented. Every choice text is in a hover tooltip. Labels are at least 10px at the default zoom.
- **Chapter ports.** Chapter 1's five exits are in the right column with gameplay ports. The fatal chair is terminal. Chapter 2 shows five incoming routes into `bureau_arrival` and five preview-only handoffs. Fatal endings never connect onward.
- **Antidote loops.** Each loop sits within three columns of its exit and on the same level.
- **Stability.** The output is identical after a reload and in a second fresh viewer.
- **Interactions.** Drag, pan, wheel zoom, Fit (whole-chapter overview), Start, Reset, Export and Import all work. Port clicks navigate correctly in both directions.
- **Saved layouts.** Old Chapter 1 cache is archived, not applied, and can be restored. Old Prologue and Chapter 3 caches are untouched. Reset affects one chapter only.
- **Unchanged chapters.** The Prologue and Chapter 3 render identically to the published viewer: every card's position, class and text, and every SVG connector, arrow and label. The comparison runs against `tools/storyboard/qa-fixtures/legacy-render-snapshot.json`, generated from main 0ebcf48 with `qa-legacy-render.mjs`, in Node and in both browsers.

### Pixel comparison

Default Prologue and Chapter 3 screenshots, branch against main:
- Firefox: byte-identical.
- Chromium: the board is pixel-identical. Only a few header-text pixels differ, by at most 2 levels, and Chromium varies the same way between two runs of unchanged main.

## Addendum: owner follow-up (branch `agent/storyboard-ports-prologue-view`)

Three owner requests after PR #2 was merged:

1. **Chapter pills behave like cards.**
   - Clicking any pill (incoming, outgoing or preview) no longer switches chapters. It selects the pill and shows the route in the right-hand panel: the route, the authored choice or `storyboardNextChapter`, and what happens in the game.
   - Pills can be dragged. Their position is saved with the chapter's layout under the port id, and Reset Layout puts them back.
   - Moving to the other chapter is an explicit **Open …** button in the panel. The start node's "Arrives from other chapters" list now selects the matching pill instead of leaving the chapter.
2. **The Prologue uses the timeline.**
   - `prologue-00` gets `layoutRevision: 2` and five incidents: Work complete & the drone's notice; Leaving work; Exposition property intake; Reception & the examiner badge; Directions, key & hallway → Chapter 1.
   - It has no cycles. `reception_hallway` sits in the right-hand column with its Chapter 1 gameplay pill.
   - Prologue positions saved before this change are archived like Chapters 1 and 2 (Restore previous arrangement).
   - SHOW/USE item routes are now labelled with their authored action text, e.g. "SHOW · HOLD OUT THE TERMINATION NOTICE.", instead of repeating the verb.
3. **View memory.** Leaving a chapter records its zoom and scroll. Returning to it through the dropdown, or the inspector's chapter buttons, restores that view. A chapter not yet visited in the session opens at its default view. A jump to a specific node (Open … from a pill) still centres on that node.

Chapter 3 is unchanged. Its snapshot fixture was regenerated from main 0ebcf48 and now covers Chapter 3 only. It matches byte for byte in Node, and every card and connector matches in both browsers.

QA on this branch:
- `qa-smoke.mjs` PASS.
- `qa-browser.js` 24/24.
- `qa-timeline.js` 110/110 in Chromium and Firefox. It now also covers the Prologue timeline, pill select/inspect/drag with no navigation, the explicit Open buttons, view memory across dropdown switches, and Prologue cache archiving.
