# v03 material and light reconstruction

Scope: CH4-01 lobby, CH4-02 auctioneer close background, CH4-03 showman foreground. All remain UNSELECTED. The restroom and ballroom are unchanged. v01/v02 are preserved byte-for-byte.

Open `index.html` for native and exact 4× comparisons. Each asset shows v02 beside v03, its approved-art benchmark, preserved v01, and the original large concept. The common benchmark section includes the Bureau, Control Tower, approved reception scene/background/foreground. Direct comparison PNGs are under `previews/`.

The existing Stage A references are reused unchanged. There were no new image-generation calls in v03. Stage B starts on blank native canvases and uses integer-coordinate geometry, smooth contours evaluated into native coordinates, native geometric coverage masks and authored material/volume fields. Those fields paint the native pixels directly; there is no high-resolution image intermediary, source raster input, supersampling, filtering, downsampling or palette reduction. The Python sources are the editable native masters. Stage C reads finished native PNGs only for exact nearest-neighbor inspection exports and lossless layer composites. Supplemental portrait 4× views do not change the 564×278 portrait presentation contract.

The rendering pass changes broad light/material/form decisions rather than adding objects. Warm practical light, window fill, deeper recesses and contact shadows differentiate the lobby; heavy folds and rounded metal are reconstructed in the close background; broad anatomical volumes and hair locks replace the prior portrait's faceted fills and line-heavy rendering. Wool/velvet, satin and cotton use different light responses.

Known limits remain visible: the rendering is stylized and can look clean or sculpted compared with the approved receptionist; the material transitions are partly procedural; flowers and some room surfaces remain less rich than the concept reference and strongest Chapter 2 work. Likeness, apparent age, expression, hands, surface finish and darker-recess readability need Nate's decision. Technical passing is not a claim that the approved-art minimum has been achieved.

`manifest.json` records every image contract/hash, exact canonical source node IDs, sources, references and limitations. `comparison.json` records the eight comparison axes for each asset. The owner direction and immutable-history baseline are in `evidence/`.

Native reproduction, from this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/lobby.py
PYTHONDONTWRITEBYTECODE=1 python3 source/backdrop.py
PYTHONDONTWRITEBYTECODE=1 python3 source/auctioneer.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package_review.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

Native QA disables image reads and resampling, rejects non-native source canvas/mask sizes, and byte-reproduces all three PNGs. It also checks contracts, alpha, exact 4× exports, prior versions, canonical sources and gallery dependencies. `source/qa-gallery.cjs` tests Chromium/Firefox native/4× switches, canonical comparison selection, all image loads and mobile pixel preservation. Local QA results and screenshots are in `evidence/`. Remote checks write outside the package so they do not change the commit being verified.

Per Nate's standing publication instruction, completed reviews are committed/pushed to `art/ch4-batch01-review-20261121` without another publication request. `source/prepare_online.py --asset-commit SHA` adds a browser-preview entry using immutable direct GitHub image URLs; the final handoff supplies the exact published commit and verified browser/image links. No main, narrative, gameplay, approval registry or production Pages workflow changes are authorized here.

Published-art verification records are retained in `evidence/published-files-qa.json` (150 remote files / 100 PNGs, all byte-identical) and `evidence/published-browser-qa.json` (10 Chromium/Firefox checks). They pin the actual previously published gallery/art commit they tested. The final publication commit adds these records and the image-load wait correction without changing candidate or gallery pixels.
