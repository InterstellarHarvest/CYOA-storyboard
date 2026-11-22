# Preservation report

Starting review commit `9ba1028821ad83759d3c809ca74775758a4d6aef`; checked canonical main `d9b6b91604b72115c5402253f00924665e957727`. All 1137 pre-existing tracked files remain byte-identical. Only this new v07 review directory is added.

| Protected source | Before / after SHA-256 | Result |
|---|---|---|
| `story/artwork.draft.json` | `8a7b5d71b5a0c4c2535e07d07f6d3ca583d9133ec46302eedefd0fd917f90d32` | unchanged |
| `story/artwork-preview.json` | `f91e754b3dcbec30e129542ab59c1997abccabb24dc31defe55b6a312613e860` | unchanged |
| `story/chapters/chapter-03.reboot-candidate.json` | `36ae178d05a9db7dd318c441e4d8681eaa674c28ced81df97dcaba6c1c5c0253` | unchanged |
| `docs/103_RETROACTIVE_ARTWORK_APPROVAL_LEDGER.md` | `6a05a20845b2add950f7ce0f202ad92a9a5b98fb2048dba70d2e450ace79dac3` | unchanged |

All 14 canonical scene PNGs, eight background layers, seven foreground layers, statuses and production paths are preserved. Every exact native/4x copy and diagnostic composite is validated; no candidate or altered artwork is produced. All 14 repair masks are black (0 pixels), and changed-pixels.json is empty. No rectangular character patch, extra device or equipment overlap is introduced.

Historical v01/v02 alternatives remain unselected and untouched. The existing Paper v04 owner selection is retained; main is v03 and its separate registration is implemented on draft PR #18, not merged. This task performs no registration or PR action.

No narrative, gameplay, menu, workflow, Chapter 4 or prior review file changes. No main merge or Pages deployment. Original full-scene/full-character native-grid authorship remains unresolved/unproven.

[553 technical checks](qa/preservation.json) · [Browser and canonical checks / exclusions](qa/results.json) · [All prior path hashes](sources/preservation-baseline.json).
