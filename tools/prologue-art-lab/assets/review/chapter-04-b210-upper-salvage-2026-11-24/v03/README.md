# B2-10 v03 — fuller rack, original stairs

**UNSELECTED.** One 314×206 opaque scene and its exact nearest-neighbor 1256×824 export. This combines the v02 foreground sinks with the fuller v01 rack arrangement, rendered using the same localized porcelain treatment as v02.

The owner rejected the attempted stair reconstructions and explicitly accepted falling back to the original layout. **The original v01/v02 stairwell and guardrail PNG layers are restored byte-for-byte.** Their remaining perspective ambiguity is documented; this version does not claim a perspective correction. Rejected stair studies are excluded from the review candidate.

Only the rack layer differs from v02. All nine other layers, including the improved foreground, stairs, rails, lift/W.C., hatch, architecture and floor, retain their exact bytes. The rack restores multiple salvage pieces, loose fittings, leaning partitions and mirrors. Native masks, restrained porcelain ramps, sockets, rims and contact shadows connect these pieces to the v02 treatment. No whole-scene shading or palette pass was applied.

## Sources and provenance

SOURCE-DERIVED, not wholly independently authored. The original detailed reference and its generation prompt remain unchanged in `../v01/originals/` and the v01 source records. Local fixture underpainting uses that source; deliberate native masks, material clusters and contact/fitting repairs shape the final rack. The approved Chapter 4 native bowl fragment is inherited from v02. The original source-defined contours remain part of the work. No new image generation was used for v03.

`source/refine_existing.py` imports the preserved v02 material helper without executing its builder. `source/package_review.py` makes the comparisons and gallery. `evidence/repair.json`, `manifest.json` and `SHA256SUMS` record the derivation and hashes. The ten editable RGBA layers use binary alpha.

## Review

- Native and exact4× v01/v02/v03 scene and rack comparisons.
- Actual approved Chapter 2 Control Tower, Maintenance Exit and Damaged Walkway.
- Actual approved Chapter 4 Service Stairs, Loading Dock and restroom porcelain reference.
- Explicit before/after crops showing unchanged v02 foreground and original stairwell.
- Hash, preservation, exact4×, replay and browser-display checks. These do not constitute owner visual approval.

Run `python3 source/refine_existing.py`, then `python3 source/package_review.py`, then `python3 source/validate.py` from any directory. The scripts resolve repository-relative sources.

No production selections, approved PNGs, story, gameplay, runtime bindings, `main` or PR #32 are modified. Both published earlier review versions remain intact.
