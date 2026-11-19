# Chapter 3 v06 — two fresh 314×206 main scenes

Built-in imagegen was used for two initial attempts and one targeted density regeneration per scene (four calls total). See `sources/generation-records.json` and `sources/initial-attempts/generation-records.json` for exact prompts, references, actual source sizes and hashes. The two current candidates remain generated/unselected. Native-grid limitations are explicit in `qa.json` and the gallery.

The original 314×206 contract is retained. The 628 study remains archived, unchanged, unselected and excluded from the new generation inputs. A02/A03/A05/A06 remain unchanged at 564×278. No narrative, gameplay, selected artwork or production registry edits; no approval or next batch.

`python3 build_review.py` exports dimensionally correct working images and exact 4× previews, side-by-side previous/new comparisons, and same-scale comparisons with approved earlier chapters. It never sharpens, quantizes or adds outlines. If a returned source is oversized, its reduction is explicitly identified as a derived export, not native-grid authorship.

Run `qa-browser.cjs`, then rebuild to include its report and screenshots in checksum lists.
