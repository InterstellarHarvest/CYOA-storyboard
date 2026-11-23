# Chapter 4 B2-04 v01 approval completion and gameplay handoff

Nate approves/selects all seven B2-04 v01 primary assets unchanged, and approves/preserves the three supplemental conditional production reference states without runtime bindings.

Seven primary assets are **APPROVED / SELECTED**, with exact existing PNG bytes. Three supplemental states are **APPROVED / PRESERVED conditional production references**, separate from canonical selections. Nothing is integrated. Authoritative source: `3804fa2013aeb81e17236e4995e2ef1e9596d404`; base: `0e83a6ed4d781d484697d475c692a4e47b63123b`. Registration follows docs/105 and B2-03 docs/131.

## Primary selections

| Asset | Canonical key | SHA-256 |
|---|---|---|
| CH4-B2-19 — Service passage — Lot31 at collection | `scenes:grand_bellevue/service_passage` | `a5d416c47786a070c3a6acfdba91e2f7756cea4418f39425fea23511608220f9` |
| CH4-B2-20 — Porter — businesslike | `portraits:hotel_porter:businesslike` | `863bffb11ce70970dd8f18a2e6188e7835092c4c8218c6f0a74b487ad26e89eb` |
| CH4-B2-21 — Porter — uncertain | `portraits:hotel_porter:uncertain` | `25d6ac8823dff67881c076c2405e50c7229375ab98bb5e4324511b2f7033f77d` |
| CH4-B2-22 — Porter — practical | `portraits:hotel_porter:practical` | `646386199bfad2bd77e73bb3137dfac9c5b8effa85e324e906208ae48a62c11e` |
| CH4-B2-23 — Service-passage conversation background | `scenes:grand_bellevue/service_passage#portraitBackground` | `b3c41ce02b3812d7ee3829bdd39e556fc648f730094d781ce19680c2a6ce6721` |
| CH4-B2-24 — Auction armrest — ring caught | `focus:grand_bellevue/auction_floor/chair_armrest` | `facb4981ccef1f270f200346333ce108a9db7679fb383982d4704e8b65fa0fc7` |
| CH4-B2-25 — Collection armrest — ring caught | `focus:grand_bellevue/collection_stairs/chair_armrest` | `68bbf32b040a984201dfb0f5b83b1315cf391848848500b1e7ee97819a5f5645` |

### CH4-B2-19 — Service passage — Lot31 at collection

Selected PNG: [`assets/selected/pending-integration/scenes/grand_bellevue/service_passage.png`](../assets/selected/pending-integration/scenes/grand_bellevue/service_passage.png). Dimensions: 314×206 RGB.

Suggested engine destination, not bound: `art/scenes/grand_bellevue/service_passage.png`.

Canonical nodes: `hotel_chair_follow_collection`, `hotel_chair_staff_escort_loading`, `hotel_collection_stairs`, `hotel_collection_ring_focus`, `hotel_collection_ring_porter_recovery`, `hotel_collection_ring_stapler_recovery`, `hotel_collection_ring_in_pocket`, `hotel_collection_porters_groom_clue`, `hotel_collection_staff_pass`, `hotel_collection_staff_pass_first`, `hotel_collection_staff_pass_recognized`, `hotel_collection_staff_pass_authorized`, `hotel_bride_service_shortcut`, `hotel_wedding_service_shortcut`, `hotel_water_outage_confirmation`.

### CH4-B2-20 — Porter — businesslike

Selected PNG: [`assets/selected/pending-integration/portraits/hotel_porter/businesslike.png`](../assets/selected/pending-integration/portraits/hotel_porter/businesslike.png). Dimensions: 564×278 RGBA.

Suggested engine destination, not bound: `art/portraits/grand_bellevue/hotel_porter/businesslike.png`.

Canonical nodes: `hotel_stall_porter_protest`, `hotel_collection_ring_stapler_recovery`.

### CH4-B2-21 — Porter — uncertain

Selected PNG: [`assets/selected/pending-integration/portraits/hotel_porter/uncertain.png`](../assets/selected/pending-integration/portraits/hotel_porter/uncertain.png). Dimensions: 564×278 RGBA.

Suggested engine destination, not bound: `art/portraits/grand_bellevue/hotel_porter/uncertain.png`.

Canonical nodes: `hotel_chair_vegetation_inspection`, `hotel_collection_staff_pass_first`.

### CH4-B2-22 — Porter — practical

Selected PNG: [`assets/selected/pending-integration/portraits/hotel_porter/practical.png`](../assets/selected/pending-integration/portraits/hotel_porter/practical.png). Dimensions: 564×278 RGBA.

Suggested engine destination, not bound: `art/portraits/grand_bellevue/hotel_porter/practical.png`.

Canonical nodes: `hotel_chair_staff_escort`, `hotel_chair_staff_escort_loading`, `hotel_collection_ring_porter_recovery`, `hotel_collection_porters_groom_clue`, `hotel_collection_staff_pass_authorized`.

### CH4-B2-23 — Service-passage conversation background

Selected PNG: [`assets/selected/pending-integration/scenes/grand_bellevue/service_passage/portraitBackground.png`](../assets/selected/pending-integration/scenes/grand_bellevue/service_passage/portraitBackground.png). Dimensions: 564×278 RGB.

Suggested engine destination, not bound: `art/portraits/grand_bellevue/backgrounds/service_passage.png`.

Canonical nodes: `hotel_chair_staff_escort_loading`, `hotel_collection_ring_porter_recovery`, `hotel_collection_ring_stapler_recovery`, `hotel_collection_porters_groom_clue`, `hotel_collection_staff_pass`, `hotel_collection_staff_pass_first`, `hotel_collection_staff_pass_recognized`, `hotel_collection_staff_pass_authorized`, `hotel_water_outage_confirmation`.

### CH4-B2-24 — Auction armrest — ring caught

Selected PNG: [`assets/selected/pending-integration/focus/grand_bellevue/auction_floor/chair_armrest.png`](../assets/selected/pending-integration/focus/grand_bellevue/auction_floor/chair_armrest.png). Dimensions: 564×278 RGB.

Suggested engine destination, not bound: `art/focus/grand_bellevue/auction_floor/chair_armrest.png`.

Canonical nodes: `hotel_chair_ring_focus`.

### CH4-B2-25 — Collection armrest — ring caught

Selected PNG: [`assets/selected/pending-integration/focus/grand_bellevue/collection_stairs/chair_armrest.png`](../assets/selected/pending-integration/focus/grand_bellevue/collection_stairs/chair_armrest.png). Dimensions: 564×278 RGB.

Suggested engine destination, not bound: `art/focus/grand_bellevue/collection_stairs/chair_armrest.png`.

Canonical nodes: `hotel_collection_ring_focus`.

## Supplemental references — approved and preserved, not canonical Focus variants

### CH4-B2-24-open — Auction armrest — seam opened, ring still caught

Preserved PNG: [`tools/prologue-art-lab/assets/approved/conditional-production-references/chapter-04/b2-04/CH4-B2-24-open-v01.png`](../tools/prologue-art-lab/assets/approved/conditional-production-references/chapter-04/b2-04/CH4-B2-24-open-v01.png). SHA-256: `a90e705303261114f882f0f270c195716f1a6e6b7384f6792373bc650c9b204c`. Dimensions: 564×278 RGB.

Base context: `focus:grand_bellevue/auction_floor/chair_armrest`. Exact existing authored conditions and node evidence:

```json
{
  "id": "CH4-B2-24-open",
  "baseAssetId": "CH4-B2-24",
  "baseFocusKey": "grand_bellevue/auction_floor/chair_armrest",
  "canonicalKey": null,
  "title": "Auction armrest — seam opened, ring still caught",
  "authoredCondition": {
    "flag": "ch4_chair_seam_open"
  },
  "nodeIds": [
    "hotel_chair_stapler_stealth",
    "hotel_chair_ring_focus"
  ],
  "truth": "The seam is separated just enough; ring still caught by pale blue ribbon and not yet in inventory. No stapler remains in the image."
}
```

Conditional production reference only. No canonical Focus key, page, node, mode, runtime binding or assetPath is introduced. Integration must resolve existing authored conditions separately.

### CH4-B2-25-slipped — Collection armrest — slipped ring beneath wooden brace

Preserved PNG: [`tools/prologue-art-lab/assets/approved/conditional-production-references/chapter-04/b2-04/CH4-B2-25-slipped-v01.png`](../tools/prologue-art-lab/assets/approved/conditional-production-references/chapter-04/b2-04/CH4-B2-25-slipped-v01.png). SHA-256: `afc5ba21cf2b472a762538ee9bbeb8ae571f64e27815d36a3849fd9ba5dd6846`. Dimensions: 564×278 RGB.

Base context: `focus:grand_bellevue/collection_stairs/chair_armrest`. Exact existing authored conditions and node evidence:

```json
{
  "id": "CH4-B2-25-slipped",
  "baseAssetId": "CH4-B2-25",
  "baseFocusKey": "grand_bellevue/collection_stairs/chair_armrest",
  "canonicalKey": null,
  "title": "Collection armrest — slipped ring beneath wooden brace",
  "authoredCondition": {
    "flag": "ch4_ring_slipped_inside_chair"
  },
  "nodeIds": [
    "hotel_ring_slips",
    "hotel_collection_ring_focus"
  ],
  "truth": "Ring is detached from ribbon and visible deeper beneath the wooden brace only at the tilted collection camera; it remains unreachable by fingers."
}
```

Conditional production reference only. No canonical Focus key, page, node, mode, runtime binding or assetPath is introduced. Integration must resolve existing authored conditions separately.

### CH4-B2-25-recovered — Collection armrest — ring recovered, cavity empty

Preserved PNG: [`tools/prologue-art-lab/assets/approved/conditional-production-references/chapter-04/b2-04/CH4-B2-25-recovered-v01.png`](../tools/prologue-art-lab/assets/approved/conditional-production-references/chapter-04/b2-04/CH4-B2-25-recovered-v01.png). SHA-256: `6cd99a639036a2ae746d7e7bcaca30a4d3914ebb125a3a59fde62e3a37f7ade1`. Dimensions: 564×278 RGB.

Base context: `focus:grand_bellevue/collection_stairs/chair_armrest`. Exact existing authored conditions and node evidence:

```json
{
  "id": "CH4-B2-25-recovered",
  "baseAssetId": "CH4-B2-25",
  "baseFocusKey": "grand_bellevue/collection_stairs/chair_armrest",
  "canonicalKey": null,
  "title": "Collection armrest — ring recovered, cavity empty",
  "authoredInventoryEvidence": {
    "has": "wedding_ring_lot31"
  },
  "nodeIds": [
    "hotel_collection_ring_porter_recovery",
    "hotel_collection_ring_stapler_recovery"
  ],
  "truth": "After explicit recovery gives the ring, the cavity no longer contains it. Ribbon and existing loose upholstery remain; no new damage is invented.",
  "bindingNote": "Post-recovery object-state reference only. The authored recovery nodes are dialogue; this does not propose displaying Focus there or changing their mode."
}
```

Conditional production reference only. No canonical Focus key, page, node, mode, runtime binding or assetPath is introduced. Integration must resolve existing authored conditions separately.

## Provenance and verification

All ten files are byte-exact copies from the pinned review commit, checked independently against its manifest SHA-256, decoded dimensions/modes and exact nearest-neighbor 4× previews. All retain SOURCE-DERIVED provenance. Detailed references, generation receipts, prompts, editable native material/structural/object layers and masks remain in the immutable source package. Nothing was regenerated, resized, re-encoded or retouched during registration.

[Machine-readable approval](132_CH4_B204_APPROVAL_COMPLETION_20261123.json) records source commit, native/4× hashes, selected/preserved paths and canonical node associations. [Verifier](../tools/sync/verify-ch4-b204-selection.py) checks the seven canonical registrations and three preserved references, previous selected files/mappings, earlier approval records, unchanged narrative/gameplay/workflows and the absence of supplemental canonical IDs. [Verification results](132_CH4_B204_VERIFICATION_20261123.json). Local QA passed: 365 selection/preservation checks, canonical drift check, 23 sync regression checks, 10 Chapter 3 reference guards, storyboard smoke, fatal export, art-lab static QA and 60 selected-art browser checks in Chromium/Firefox. Public raw-file, deployed Pages and gallery verification follow publication; receipts are published separately on the art review branch.

## Gameplay handoff

Pin the canonical approval commit and verify all ten hashes before any later integration. Use native masters; previews are display-only. Composite the porter foregrounds over the service-passage background or their existing authored lobby/restroom contexts. Respect each exact speaker/pose and scene/node mapping.

Supplemental references are mutually exclusive object-state examples for existing authored flags/inventory. They are not sequential Focus pages. In particular, recovered is an empty-cavity production reference after explicit ring-granting recovery; its dialogue nodes remain dialogue. Do not install new Focus IDs, runtime bindings, narrative nodes, gameplay modes or automatic state dispatch through this approval. A later gameplay integration must implement and test existing conditions separately.

All previous approvals, including B2-03, and historical review versions stay exact. The two B2-01 plumber alternatives remain unselected. No narrative, routes, items, flags, choices, dice, game integration report, runtime assetPath or engine code is changed.

## Automatic continuation

Proceed with canonical inventory group B2-05 — Bride and auction clerk: bride determined/hopeful/grateful/helpful and precise auction clerk. Follow permanent docs/129: detailed references, separate native interpretation, controlled material ramps and purposeful clusters, approved Chapter 2 comparisons at native/exact 4×. Publish on the existing art review branch as UNSELECTED pending Nate.
