# B2-12 v03 — INSPECT alternatives with a dedicated lock row

**Both new565×451 square INSPECT images are UNSELECTED.** The approved v01 square images, approved dressing room and newly approved v02 widescreen images remain unchanged. No canonical registration, narrative/gameplay/runtime change, main merge, PR#32 change or deployment is included.

The only visual edit is inside the CRT's existing content area. The centered two-line text moves up11 native pixels, with a4-pixel line gap. A separate shared icon zone beneath the text contains the larger closed/open lock. Both states use the same text box, horizontal center and lock-body position. Clear space between text and icon is9 rows for locked and8 for provisional. No extra divider, border, status light or decorative treatment was added.

CRT glass accents, bezel, brass frame, camera, policy badges, button, wall, lighting and every surrounding pixel are exact. Each image retains the exact source29-colour palette, with no new colours, dithering or antialiasing. Actual change masks verify zero changed pixels outside the authorized CRT-content rectangle. Native full images remain565×451 opaque RGB; exact nearest-neighbor4× exports are2260×1804.

## Method and provenance

This is a small edit of existing editable native raster artwork; no image generation or new large reference is needed. `source/build.py` reuses the approved v01 bitmap glyph shapes stored in `source/bitmap-glyphs.json`, paints a localized native RGBA content patch and composites it over an exact approved source copy. The image's original SOURCE-DERIVED illustration provenance is retained; no wholly independent native authorship claim is made. Original illustration sources/prompts/layers remain immutable in v01 at source commit `ce8cc78f7683c99d96399091ab92cc3ac52e4f05`; approved square source is `1261658ed882bff7340405e91f5d44f4e5404012`. The full preservation baseline is `a944f9aeff110ddc66301840c2d415f1ba9bc357`.

`layers/` preserves editable content patches and standalone icons; `masks/` preserves authorized and actual changes. `evidence/layout.json` records native text/icon boxes and clear spacing. `manifest.json` records exact source/final/patch hashes. `evidence/reference-provenance.json` pins all approved v01/v02 reference copies. Current owner approval of the widescreen images is recorded as reference provenance without rewriting their historical review manifests or canonical selection records.

## Review and checks

Open `index.html` locally or the published immutable `online.html`. The gallery leads with close-up before/after comparisons for both states and provides complete v03 images, exact approved v01 sources, approved v02 widescreen references and an approved Chapter2 Focus benchmark. Close-ups use the same176×99 CRT crop, without scaling; separate4× versions are exact nearest-neighbor. Comparison captions sit outside artwork. All native/4× gallery images display at full integer dimensions with horizontal scrolling when needed.

Replay with Python3 + Pillow: `python3 source/build.py`, `python3 source/gallery.py`, `python3 source/validate.py`. The validator checks local edits, exact source palette, native/layer/crop/preview identity, shared layout, alpha, hashes and preservation of every pre-existing tracked blob. Browser checks verify real decoded images and full-size native/4× controls in Chromium and Firefox. Public byte receipts are stored outside the frozen v03 package.

Visual review: at native size the text and icon are now distinct groups. At4× the padlock shackle/body are coherent solid pixel shapes, with one open end in the provisional icon. The CRT's physical styling and all material/lighting detail remain identical to approved v01. Technical checks and this internal assessment do not establish Nate's approval. v01 remains the approved version unless Nate selects an alternative through the separate workflow.
