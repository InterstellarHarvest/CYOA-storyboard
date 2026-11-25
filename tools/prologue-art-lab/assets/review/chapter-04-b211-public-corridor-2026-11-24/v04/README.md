# B2-11 v04 — adult doorway scale and cleaner character rendering

**UNSELECTED.** One revised flooded reference; the dry master and the rest of the room remain unchanged. All previous review versions, source studies, prompts and hashes are preserved.

The previous94-pixel attendant was too short beside the doorway and her shade texture obscured useful detail. v04 rebuilds the same gray-haired hotel attendant from a dedicated clean-cluster source at132 native pixels tall. Her feet stay at the same193-pixel floor boundary. The near edge of the existing STAFF door leaf is174 pixels tall;132/174 is about76%, a useful image-scale check rather than a claim about an exact physical measurement.

The source preserves her navy work jacket/trousers, pale blouse, silver bob, composed professional expression and leftward pointing gesture toward the staff passage. It uses broad connected hair, face and fabric shade shapes rather than many tiny marks. Approved Pavilion scene NPC rendering informs the clean treatment; that scene's person is not copied as an identity. The staff-lavatory figure remains a detail benchmark, not this character.

The new source is processed directly at132 pixels, not enlarged from a previous94-pixel candidate. Object-only nearest-neighbor interpretation, coherent material ramps, binary alpha and removal of tiny interior cloth islands preserve useful face/hand/costume construction without blur, stochastic dithering or whole-scene processing. Source-defined shapes remain: provenance is **SOURCE-DERIVED**, not wholly independent native authorship.

Only `state-attendant.png` is newly authored. Fifteen other scene/state layers are reused unchanged from v03/v02, including the separated sign, room, hatch, doors, outside view and water. The unchanged floating sign stays17 pixels horizontally clear of the new character bounding box. Changed composited pixels are restricted to the union of old/new character silhouettes.

Built-in `image_gen` produced `originals/attendant-clean-cluster-source.png`. Its exact prompt is `source/attendant-clean-cluster-prompt.txt`; hashes and input roles are in `evidence/generation-provenance.json`. `source/refine.py` reproduces the native figure and scene assembly. `source/package_review.py` builds the native/exact4× gallery; `source/validate.py` checks dimensions, alpha, scale, clearance, source hashes, exact assembly, replay and preservation.

The gallery compares v03/v04 at native and exact4× with actual approved Staff Lavatory, Chapter2 and Pavilion scenes. Checks do not constitute Nate's visual approval. No narrative/gameplay, selection, approved artwork, canonical main, runtime binding or PR32 changes are made.
