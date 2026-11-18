# Visual comparison and limitations

Both v02 candidates remain unselected pending Art Director review. These are technical production candidates, not approval decisions.

## Shared House design

The approved foyer and gallery PNGs were used directly as image-generation references. Both candidates retain a tall ivory rounded housing, brown woven grille, tiny upper-right black camera dot, lower-left green circular lamp, and lower-right ribbed thumbwheel. They mount directly against a peach wall with a shallow shadow. There are no posts, people, hands, separate sprites, captions or interface elements. The v02 housings are approximately 168x216 logical pixels, close to the approved gallery's approximately 170x218 housing; the approved foyer's housing is slightly taller, approximately 170x236. These bounds are visual estimates, not segmentation measurements.

## Lounge versus approved lounge scene

The new close view retains the garden daylight at left, peach wall/coral trim, warm cabinet and a cropped empty mint recliner at the lower right. The intercom occupies the center at conversational scale. The original main scene remains wider and shows the full recliner and room. Only a sliver of coral appears at the lower-left corner; its separation from the nearby trim/rug is visually ambiguous at this crop.

## Dining versus approved dining scene

The close view retains the garden-window edge, warm serving cabinets and coral pot, an empty white plate and cup at the lower table rim, and two visibly empty mint chair backs. The full main scene establishes four settings; this intentionally tight portrait shows only the near setting and two cropped chair backs. The complete four-place table and all four chairs are outside this framing. No food is visible. Room perspective is reinterpreted for the closer intercom view; furniture locations are consistent cues, not a pixel registration of the main scene.

## Pixel fidelity and generation limits

All four tool-returned originals are preserved byte-exact. The tool returned 1784x882, 1786x881, 1788x880 and 1785x881 RGB renders rather than the requested 2256x1112 integer-grid output. Native candidates use full-frame NEAREST sampling to exactly 564x278. This introduces a small aspect-ratio adjustment (current v02 candidates under 0.15% in magnitude; archived lounge v01 approximately 0.302%; see generation records) and cannot prove that the original was authored on a strict logical pixel grid. No blur or interpolation filter was applied. Four-times PNGs are verified pixel-for-pixel expansions of each native export; the gallery also uses integer CSS dimensions and pixelated image rendering.

The generated grille weave, housing bevels, wall shading and edge highlights are newly rendered rather than byte-identical reproductions of approved pixels. Grille texture is denser and less regular than the source in places, and the wall retains gentle tonal shading. Hard stepped contours remain visible at native resolution and 4x, but microtexture consistency requires Art Director review. No palette reduction or smoothing was applied to disguise these differences. v01 files are archived scale studies, not additional selected options.

## Scope

Only this review directory is added relative to branch base 1ce7e79, preserving the concurrently published final Chapter 2 Batch 8 approvals. Generation source b3e374b remains pinned in sources/; all Chapter 1 target briefs and approved references are unchanged between those revisions. No canonical registry, selected artwork, gameplay, dialogue conversion, choices, flags, inventory, routes, workflows, Chapter 3 files or existing approved PNGs are changed. Batch B branch 004758e is not merged, copied or edited. Production paths remain empty. No review approval is inferred from generating, committing or publishing these files.
