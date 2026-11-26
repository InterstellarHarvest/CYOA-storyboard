# Temporary Staff Pass v01 — public review handoff

**Exactly two artwork candidates. Both UNSELECTED.** Nate's visual approval is
pending. No item registration, grant logic or gameplay integration is included.

Branch: `art/pavilion-temporary-staff-pass-review-20261126`.
Canonical base: `89cf0adf09dfadba27bb82f87201160f68818b46`.
Native artwork commit: `a6a6bdbc1d619ea75a8fe7ebb056b379db02eb4f`.
Pinned gallery commit: `cc40a62530e48430ab69d9d3615cc91c5eb363a5`.

[Public browser gallery](https://htmlpreview.github.io/?https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/cc40a62530e48430ab69d9d3615cc91c5eb363a5/tools/prologue-art-lab/assets/review/pavilion-temporary-staff-pass-2026-11-26/v01/online.html)

| Candidate | Native contract | Native SHA-256 |
| --- | --- | --- |
| `v01/native/pavilion_temporary_staff_pass_slot.png` | 96×96 transparent RGBA; binary alpha; 16 values including transparency | `662ecb2c15b0b70afd5e6a14a73dadab6090fc2f4c75a389f9f5a96ba06b59b5` |
| `v01/native/pavilion_temporary_staff_pass_inspect.png` | 565×451 opaque RGB; 25 colours | `527e17af4a27971d2d729441f8a74d097c5442df93f0161dc841d81ee1788e41` |

Exact nearest-neighbour exports are 384×384 and 2260×1804. All four inspection
lines match the owner's wording, with separate text safe zones, correct alignment
and margins. The small slot uses the readable STAFF label only. No inventory frame
is baked into it. Slot and inspection use independently drawn native geometry.

## Verification and artistic assessment

- Public byte verification matched all 65 gallery-payload files and 13 pinned
  canonical inputs. `PUBLIC-BYTE-VERIFICATION.json` records the exact public paths,
  hashes and PNG decode results for the pinned publication commit.
- Chromium and Firefox passed all eight figures at both native and exact 4×:
  16 figure checks / 32 scale checks. Natural, displayed and rendered dimensions
  match; no fractional scaling. Evidence is in `public-browser/report.json`.
- Technical QA verifies native dimensions/modes, binary slot alpha, full exact4×
  pixel replication, required text safe zones, named layer recomposition and
  OpenRaster merged-image equality. Every canonical source is unchanged.
- Native and 4× views were inspected against the actual approved Chapter 2
  examiner, acting-director and bathroom-pass artwork and approved Chapter 4 paper
  lettering. The credential silhouette remains clear at inventory scale. Inspection
  text is legible and separate from the seal, registration and attachment. Matte
  paper is quieter than the reflective Chapter 2 examiner laminate; this is an
  intentional material distinction. No smooth gradients or photographic grain.
- Technical checks are not owner approval. Recommend reviewing this pair together
  because their shared object identity is the intended selection unit.

## Honest provenance

Built-in imagegen supplied a large design reference only. Its exact original,
prompt and receipt remain in `v01/originals`, `v01/prompts` and `v01/evidence`.
The final native script reads no source raster. No shrink/sharpen/quantize pipeline
or image colour sampling was used. Deliberate material ramps, explicit native
shapes and a custom bitmap alphabet construct the two canvases independently.
Editable named PNG layers, native mark JSON and OpenRaster files are preserved.

## Coordination and integration boundary

Claude owns the credential-grant/narrative work. This producer owns only this new
isolated artwork review folder. No shared files or worktree are written. The
handoff in `v01/README.md` identifies the existing key
`pavilion_temporary_staff_pass`, the temporary-presenter appointment beat, the
existing Chapter 4 SHOW-route consumers and the selection-before-binding boundary.
No contact/acknowledgment from Claude is claimed.

Legacy archived art records, canonical main, narrative, item records, engine,
existing approvals and historical images remain untouched. The decorative serial
does not create an access rule. Stop here for Nate's review; do not automatically
register, merge or deploy.
