# Temporary Staff Pass — v01 owner review

**Two new candidates. Both UNSELECTED.**

Item identity: `pavilion_temporary_staff_pass`.
Canonical base: `89cf0adf09dfadba27bb82f87201160f68818b46`.

| Candidate | Contract | Purpose |
| --- | --- | --- |
| `native/pavilion_temporary_staff_pass_slot.png` | 96×96 RGBA, binary transparency | Inventory silhouette: cheap clip, green-grey sleeve, cream card, STAFF bar and burgundy seal |
| `native/pavilion_temporary_staff_pass_inspect.png` | 565×451 opaque RGB | Independently drawn close view with the four exact owner-specified lines |

The inspection reads:

```text
TEMPORARY STAFF
PEOPLE'S PAVILION
DEPARTMENT: HUMAN PRESENTATION
VALID UNTIL CORRECTED
```

The serial `HP-03 / 0417`, registration boxes and Pavilion building pictogram are
decorative printing, not narrative facts or gameplay entitlements. No face/photo,
barcode, additional access promises, inventory frame or extra objects are added.
The slot uses only readable STAFF lettering; it does not cram the inspection text
into its smaller canvas. Text is frontal and aligned with the paper edges.

## Construction and provenance

Built-in imagegen supplied only `originals/credential-design-reference.png`, using
the exact prompt in `prompts/reference.txt` and the two identified approved Chapter
2 inspection references. Original file hash, dimensions and generation path are in
`evidence/generation-receipt.json`.

`source/build_art.py` separately paints the actual 96×96 and 565×451 canvases.
It reads no reference raster: no sampling, tracing pixel colours, downsampling,
sharpening, quantization, image-to-palette conversion or alpha correction is used.
The two canvases share a semantic design and deliberately chosen material ramps;
their geometry and print layouts are separately authored. Chunky lettering uses a
custom explicit 5×7 bitmap alphabet, placed at integer coordinates without font
antialiasing. The largest heading has 4× glyph cells authored directly on the
inspection canvas. This is typography construction, not enlargement of the slot.

Broad connected paper shades follow the bowed sleeve and curling corner. Wear is
grouped on exposed edges. Metal has distinct edge highlights, a screw slot and a
spring jaw. The sleeve is faded green-grey; cream paper and burgundy machine print
retain clear separation. No random noise, photographic grain or smooth gradients.
The current slot has 16 RGBA values including transparency; inspection has 25 RGB
colours. These counts document the result, not an imposed quality threshold.

Editable sources: `source/*.ora`, `source/*-marks.json`, `layers/*.png` and the
explicit Python construction. ORA files contain the named layers and merged image.
Layer recomposition is verified against the exported native PNG bytes after decoding.

Reproduce from any working directory with Python 3 and Pillow:

```sh
python3 source/build_art.py
python3 source/build_review.py
```

`source/build_review.py` verifies pinned canonical inputs, native contracts, safe
text zones, layer composition and every 4× pixel block. `index.html` uses the exact
native/4× exports with integer presentation. A pinned public `online.html` is added
after the native artwork commit; browser/public-byte receipts are outside v01.

## Visual comparison

Compare actual canonical Chapter 2 examiner, acting-director and bathroom-pass art,
plus the approved Chapter 4 dispute-ticket inspection. All reference PNGs are
preserved byte-for-byte, with immutable commit/path/hash records. The pair matches
the established credential silhouette, muted cream/green materials and crisp
machine lettering. Its matte paper carries deliberately quieter shading than the
more reflective Chapter 2 examiner laminate. Inspect both native and exact 4×;
technical success does not establish Nate's artistic approval.

## Coordination with Claude's grant work

This isolated branch owns only this new review package. The owner has now approved
the item's grant at the Chapter 3 temporary-presenter appointment and its carryover
to existing Chapter 4 maintenance routes. Claude owns the grant work separately.
No files in Claude's worktree are shared, edited or overwritten here.

At this pinned base, the legacy art prompts remain archived and the item still has
null art paths. Those historical records are not revived or edited. The owner's
current artwork instruction supplies this new scope. The appointment beat is in
`story/chapters/chapter-03.reboot-candidate.json`, node `unauthorized_presenter`;
the Chapter 4 existing SHOW choices use `pavilion_temporary_staff_pass` at
`hotel_collection_stairs` and `hotel_boiler_pressure_intro`.

Handoff to Claude: retain the exact item key. Do not bind these review paths or
mark artwork approved automatically. The serial and seal confer no new rules.
After Nate selects the PNG hashes, use the normal separate registration and
integration workflow; this artwork task implements neither grant nor bindings.
No conversation with Claude is claimed by this document.

Main, narrative, engine, registry, existing approvals and all earlier art remain
unchanged. Stop at Nate's review gate.
