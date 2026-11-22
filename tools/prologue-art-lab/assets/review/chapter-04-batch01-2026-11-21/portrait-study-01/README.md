# CH4-03 portrait-specific reconstruction study 01

**UNSELECTED. Limitation study, not a completed v06 or a native game asset.** The fresh raster test is 1785×881 despite an explicit 564×278 request. It is preserved unchanged and has not been reduced into a candidate. See [method assessment and proposed native raster workflow](METHOD-DECISION.md), [the exact prompt](prompts/native-raster-reconstruction.txt), and [the measured receipt](evidence/generation-receipt.json).

[Open the review gallery](index.html). It includes the new source-sized raster test, unchanged primary frontal reference, v05 portrait and actual approved receptionist, Pavilion attendant and Pavilion presenter. Native references and v05 have actual 1× and exact 4× views. The new test is explicitly source-sized at 1× and exact 4×; it is never labelled native. Direct comparison PNGs preserve original pixels without scaling the studies down.

CH4-01 lobby and CH4-02 background are frozen at v05 as owner-review candidates. Their exact PNGs and hashes are recorded in [the freeze record](evidence/frozen-environments.json). No approval is registered. Every previous v01–v05 file remains unchanged.

Reproduce presentation exports and validate from this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/package_study.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

These scripts reproduce packaging from the preserved master, not the stochastic image-model generation. There is no native reconstruction script and no claim that the failed output gate passes. The next proposed production route is direct layered raster illustration on a blank 564×278 canvas with source/stage provenance, described in the method decision. Further portrait revisions have stopped at this decision point.

Publication remains on `art/ch4-batch01-review-20261121`. No production Pages workflow is changed. A read-only browser entry pins immutable GitHub image URLs; remote verification is recorded outside the package to avoid changing the commit being verified.
