# Consolidated Chapter 4 B2-09 v01

Three primary review units, all **UNSELECTED**: CH4-NEW-05 Bixby (exact existing PNG), CH4-NEW-06 wedding organizer, CH4-NEW-18 shared ballroom threshold. Four supplemental reference frames: wheel mounted, wheel removed, rubber-band fender, water emerging. The neutral background and removed-wheel reference intentionally have identical PNG bytes.

[Browser gallery](index.html) · [manifest / exact hashes](manifest.json) · [before/after](comparisons/before-after-native.png) · [four states](comparisons/four-states-native.png) · [threshold detail](comparisons/threshold-detail-4x.png) · [speaker composites](comparisons/speaker-composites-native.png) · [QA](evidence/validation.json).

## Authority and scope

Canonical main is pinned at `d82ae25bd39855412797bb2632dc61b1001b940a`: consolidation applied, active primary target63. Read docs129,137,138,139 and draft PR32's docs141 at `f320e63934c13e27fd13b9482d0cfba58911362d`. Read-only copies are in `evidence/briefs/`. Nate's current production instruction authorizes this isolated consolidated review and supersedes the earlier generation pause for this work only. [Scope/authority record](evidence/authority-and-scope.json).

The historical branch `art/ch4-batch01-review-20261121` remains at `1459c4ed2f4288a41805365d1085e8fd3cdb76ae`; its old B2-09 packages and STOP notice are preserved. This package does not resume the old four-asset scope. No commanding portrait, redundant refreshment main scene or its old states is produced or selected. The new branch is `art/ch4-b209-consolidated-review-20261124`.

No canonical production selection, narrative, gameplay, runtime binding, flag, Focus ID, engine code or deployment is changed. PR32 remains a draft and is not merged. Supplemental labels are review labels only. Timing/conditional dispatch belongs to later authorized integration. Organizer composites over non-neutral states are fit diagnostics, not a requirement to show those props during her nodes.

## Native background reconstruction

Starting pixels: exact `CH4-B2-51-emergency-v02.png`, retained as `references/before-wheel-removed.png`. The old table/chair concealed lower door construction. A separately preserved imagegen clean-room underdrawing supplies the missing material/form information. Its native transfer is retained as a **diagnostic**, then interpreted only within old-occluder masks using the existing room palette, protected original room pixels, target-grid cluster/contour work and explicit door seam, threshold, floor joints and gap construction.

The refreshment table is recomposed to the right of the door gap. Native table/linen, glasses and napkins are editable layers. The original silver bucket and rich flower/vase clusters move exactly42 native pixels without scaling. Unobscured original linen clusters are reused without scaling. The room's upper doors, swags, duct, lamps, green-gray wall and right-hand window/cabinet stay exact outside the recorded correction. Both lower door edges, stone threshold and dark gap are visible; no table prop or foreground silhouette intersects the gap mask.

The brass four-spoke plumbing wheel is a transparent native layer with real open holes; no brass semantic mask is applied to exposed plaster. The fender is a separate spherical tan/slate/rust bundle of unequal overlapping rubber bands, without a hub, metallic rim or radial spokes. A folded ivory napkin strip and knot connect it to the bucket. Its design/colors are studied from the preserved exact approved `rubber_band_ball` inspection artwork; that image is not resized and pasted into the scene. Water begins directly at the gap, uses discrete wet-floor ramps retaining the underlying floor divisions, has sparse reflection edges, and is excluded from cloth/props. Water+wheel and water+fender previews demonstrate composability without assigning runtime conditions.

All these are **SOURCE-DERIVED** images with explicit native structural/material/prop construction, not a claim of independently authored whole-frame native artwork. A source resize or palette fit alone is not offered as completion. [Background derivation](evidence/background-derivation.json), editable `layers/`, [exact layer assembly recipe](evidence/layer-assembly.json), localized `masks/`, [original prompts/receipts](evidence/generation-receipts.json). An internally rejected plain geometry study is preserved under `evidence/internal-study/` and is not a proposed candidate.

## Organizer and preserved Bixby

Organizer identity comes from the exact approved CH4-05 crop `(195,74,231,155)` and full ballroom; approved Pavilion humans and Chapter4 engineer guide portrait finish. The single source has auburn-brown curled hair up, white collar, charcoal-slate suit, natural hands holding three distinct clipboards and an urgent, kindly expression. This waist-up crop excludes heels. No invented readable clipboard copy, key or extra character prop is added. A source-added blank nameplate is removed with native tailoring planes.

Detailed imagegen source → native composition diagnostic → opaque-only coherent palette interpretation → material-specific cluster construction preserving face/hair/hands/clips → native tailoring and binary silhouette cleanup → editable semantic layers. The local64-tone fit is calibrated to approved portraits, not a universal palette rule or an approval test. [Organizer derivation](evidence/organizer-derivation.json).

Bixby is **not regenerated or cleaned up**: `CH4-B2-49-v01.png` remains byte-for-byte under the new review filename. SHA-256 `44f81292dc520eeabc6864c21449fb033db4891702c6102634b126b344ee05b8`. His original illustration, prompt and pinned derivation are preserved. One delighted portrait covers all three consolidated Bixby nodes. Hands remain empty and no wheel/bucket/ball is added to the foreground.

## Visual gate, QA and reproduction

Actual native and exact nearest-neighbor4× artwork is compared with approved Chapter2 Bureau/Tower, Chapter2 portrait cluster/material examples, Pavilion human portraits, Chapter4 engineer/auctioneer, CH4-05 and CH4-B2-23. The Chapter2 conductor and groundskeeper are robots: they benchmark clusters/materials, not human anatomy. Human identity/anatomy comparisons use Pavilion and Chapter4 humans. [Visual assessment](evidence/visual-review.md). Dimensions, palette counts and hashes are technical evidence, not Nate's approval.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/build_background.py
PYTHONDONTWRITEBYTECODE=1 python3 source/build_organizer.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package_review.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

Gallery controls display actual native/exact4× PNGs at integer dimensions; oversized comparisons scroll rather than shrink. The verifier checks masks, layers, original hashes, binary alpha, exact composites, untouched canonical files and deterministic replay. Public verification and real Chromium/Firefox decoding are recorded after publication. All earlier approvals and unselected plumber alternatives remain exact.

B2-09 is now presented at its owner-review gate. After its review, the next revised queue item is B2-10 / NEW-03 upper salvage mezzanine in docs138. CH4-03 replacement remains deferred to R1 and is not started here.
