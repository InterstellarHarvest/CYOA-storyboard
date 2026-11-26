# B2-19 publication and PMO handoff

Status: **UNSELECTED — owner visual review required**. No selection or integration.

Review branch: `art/ch4-b219-lobby-states-review-20261126`.
Canonical source: `3785e87506c4218a360cf7a309b2fbe690cc4546`.
Native artwork payload: `801dbd91c89742b9272d451188297ddac9b0b9f3`.
Pinned gallery publication: `6305bd70c566e7dd254b40d9cce17d6c02f356c0`.

[Browser gallery](https://htmlpreview.github.io/?https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/6305bd70c566e7dd254b40d9cce17d6c02f356c0/tools/prologue-art-lab/assets/review/chapter-04-b219-lobby-states-2026-11-26/v01/online.html)

| Native image | SHA-256 | Coverage |
| --- | --- | --- |
| `v01/native/lobby-doors-removed.png` | `e2aa3835dca0edf1e76b93df2a3cf628db8dc5ff8f56c1f5df8e6188ea7d218e` | Persistent doorless lobby; removal motion narrated |
| `v01/native/lot61-open.png` | `3913c8ad89c0245c31827f1933926ff0d1a00ec9da71f34dfa9818ff222c42b5` | Pod introduced/open for demonstration; decline departure narrated |
| `v01/native/lot61-packed.png` | `f3c27be75a18007850f8eb9bff7ae71f031063aa44735f9bfbd24bf5d876b558` | Only after successful escape and completed folding |

All three are opaque RGB 314×206. Exact nearest-neighbour exports are 1256×824.
Masks contain respectively 2585, 7502 and 3287 changed pixels versus the master;
zero changed pixels lie outside the allowed local regions. Protected figures and
furniture have zero changes. OpenRaster merged images and layer recompositions
match the native candidates exactly. The immutable approved lobby source retains
SHA-256 `582bcd51de937e5fe124160a8beb74b4ee469f52eeb6d9d0d38b918cfb0d6be0`.

Chromium and Firefox decoded all 19 gallery figures at native and 4× (38 figure
checks, 76 scale checks). Raster dimensions, displayed dimensions and rendered
dimensions match exactly; no fractional CSS scaling. Public screenshots include
the progression and porter assessment. See `public-browser/report.json` and
`PUBLIC-BYTE-VERIFICATION.json` for the published verification evidence.

## Integration handoff, not implementation

Use the three-image minimum in `v01/RECONCILIATION.md`. Both pod states retain the
already-removed doors. Do not reveal the packed case merely because the survival
flag is set at node entry: wait until the authored folding finishes. The compact
case has no loose shoe or occupied bulge on the successful escape path. Keep the
existing approved FOLDED FOR CONVENIENCE illustration for the fatal outcome.

PMO resolves the B2-18 closer-camera hold by reusing approved CH4-B2-03 unchanged
for `hotel_stall_porter_protest`. The assessment confirms a peripheral visible
edge, not porter occlusion. No selectable replacement background is produced.

The native layers preserve the master room. New native metalwork is independently
painted; the toilet is a disclosed exact 1:1 approved native cutout. Built-in
imagegen produced a reference only; its original, prompt and receipt are retained
under `v01/originals`, `v01/prompts` and `v01/evidence`. No generated reference
pixels were shrunk, recoloured or substituted into the final scenes.

No unresolved canonical continuity blocker was found. Scene-state timing is
documented for a later authorized integration. Nate's artistic approval is still
required. R1 remains suspended. All existing approvals and historical packages
are untouched; no main, PR #32, registrations, story, gameplay, engine or deployment
changes are included.
