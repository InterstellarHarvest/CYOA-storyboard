# Chapter 5 — preserved narrative and later-section assembly / review 51

## Owner placement decision

Nate explicitly selected **Preserve earlier material; add this section later** when asked whether the recent short draft should replace the earlier Chapter 5.

The earlier opening, security representative, keeper, mechanical dog, Public Protector, lake, boathouse, bin/gate, document handling, pneumatic property return, and existing inventory consequences remain in force. This work does not replace those scenes with the recent short opening or declare the recent five-outcome summary to be the full chapter.

## Source preservation

- Assembly base: storyboard main `428a3d63412f470bbd9bbb5c0f772c511661ba32`.
- Earlier Chapter 5 source: `story/ch5-concept-review-20261125` at `2f0f3e124ce7054ab8ce6720848043109f67605e`.
- All earlier `docs/chapter-05/` records from that source are preserved byte-for-byte. New files are additive.
- The earlier branch's old copies of Chapters 1–4, art registries and integration records are not copied over main.
- Later owner-approved prose in this conversation controls the fence/foam expansion where it differs from review 50's earlier proposed mechanisms or odds.

## Files

- [Structured later section](../../story/review/chapter-05-later-park/later-park.section.json): 36 nodes, 48 choices, three hidden d6 checks, two shared later-section fatal presentations, and two park exits.
- [Readable full later-section prose](LATER_PARK_NARRATIVE_REVIEW_51.md).
- [Additive item definition](../../story/review/chapter-05-later-park/items.additions.json): one-charge foam-release cartridge.
- [Unselected artwork requirements](../../story/review/chapter-05-later-park/artwork.additions.json): placeholder scene references, cartridge slot/inspection, later deaths, plus the earlier electric-shrub death's approved concept direction. This sidecar is not a final art-count commitment.
- [Electric-shrub Codex artwork addendum](CH5_ELECTRIC_SHRUB_ARTWORK_ADDENDUM.md): links the exact approved image; 314×206 native, exact 4× review; no external holding arms; protagonist face concealed inside the printed cover scene.
- [Section state/route audit](../../tools/storyboard/qa-ch5-later-section.py).

## Placement and terminology

This section begins **beyond the earlier property-return/land-side collection area**. Property redemption is optional; damaged, intact, already consumed, retained and absent belongings must remain correct. The section offers paths to the fence, directly to the foam lawn, or to the depot, so experiencing every incident is not required.

`depot_early` means reaching the depot before the **new foam incident**, not at the original chapter opening. The new supply-cable shortcut is staged after property return; it is not wired over the earlier opening's representative route. Likewise, `first_restroom` labels in this section mean the fence-side building, not the earlier sensor/cleaning restroom in reviews 09–12 and 47–48.

Older map/far-gate/after-return paths exist as approved narrative records and frontiers, not as completed structured chapter nodes. Their exact upstream edges remain to be assembled with the earlier chapter body. Do not fabricate existing node IDs or claim this patch completes those links.

## Continuity reconciliation

- Keep the earlier no-cooperative-shutdown ruling on its original representative scenes. The newly approved demonstrator reacts to the current foam damage and operates his local fence/foam exhibit. These new local outcomes do not rewrite earlier refusals or switch off the entire park/Expo.
- The first service-room switch is **PERIMETER MOTOR — RUN / STOP**, affecting that fence only. A separate handwheel retracts its panels.
- The current scene's shutdown cannot make previously paused or retracted panels rise again. Text uses the actual incoming fence and nozzle states. Effects occur on the forward transition after observation.
- Existing foam keeps expanding after discharge stops. Its entry through a path drain is narrated before the rear-restroom intrusion.
- The early depot arrival has the mechanic alone and no cleanup emergency. The later arrival includes the demonstrator and blocked-restroom cleanup.
- The new demonstrator, mechanic and trapped clock worker are the specific actors approved in this conversation; no additional staff, entertainment, balloon or truck incident is commissioned here. The wider sparse-cast guidance remains applicable during full-chapter reconciliation.
- The delivery truck, loading favour and truck ending are cut completely. A hand trolley in dispatch remains a prop, not a vehicle route.
- Original items are retained. The rubber-band solution uses one outer band, preserving the ball and its unknown centre. Staff and vegetation credentials persist. The brass gate key is used locally and returned.
- The cartridge pickup is optional before either exit, once only, with no six-item capacity limit. Its future-use payoff is still an open carry-forward obligation; no use is invented solely to spend it.
- The earlier electric-shrub deterministic fatality retains its exact WHIZ title. Its subsequently approved board-game-box concept belongs in the later production prompt, not in the production registry as a finished pixel asset.

## Review and verification boundary

Run:

```sh
python3 tools/storyboard/qa-ch5-later-section.py --write
node tools/sync/check-canon.mjs
node tools/storyboard/export-death-presentations.mjs --check
node tools/storyboard/qa-smoke.mjs
```

The section audit checks declared fields, destinations, state-reachability, all raw d6 outcomes, optional-item/read-mark configurations, original inventory and state preservation, alternate arrivals, shared fatal metadata, and preservation of every earlier Chapter 5 record. It is not a private-game runtime test or a whole-chapter route audit.

This patch does not register a full Chapter 5 in the public manifest. Earlier scene assembly and its frontiers remain necessary before that can be represented accurately. `notForGameplay` stays true. The existing game-ready death export must remain unchanged.

Next: assemble the preserved earlier body and its unresolved map/property-return connections, join this section forward once, then run whole-chapter route/state/layout checks and prepare the full artwork handoff. No earlier completed incident should be replayed to recover an item or reach this section.
