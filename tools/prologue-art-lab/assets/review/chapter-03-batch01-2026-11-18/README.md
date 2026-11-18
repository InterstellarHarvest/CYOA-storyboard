# Chapter 3 Batch A — generated / unselected

Open index.html for exactly six current candidates, 1× and 4× nearest-neighbor views, literal foreground/background composites, white/dark alpha proofs, approved references, exact prompts and source provenance. Candidate IDs are CH3-A01-restroom through CH3-A06-presenter-idle. CANDIDATE_HASHES.md identifies the six exact review PNGs.

Branch: `art/ch3-pavilion-batch01-20261118`, based on preparation commit `2a1022ba7d96f9cf887402fc59c8266f81be577c`. Approved narrative blob: `857ffdf1bc9432cf4bbbfd7819f5f430a06d9036`. The narrative, dialogue, branching, checks, endings, canonical catalogue and approved prior artwork are unchanged.

## Actual output and limitations

The built-in image_gen tool returned larger RGB/RGBA rasters despite exact native-dimension prompts. All nine untouched tool originals are retained under generation-source/ with their original filenames. Six dimension-correct review exports are under candidates/: 314×206 for main scenes and 564×278 for conversation layers. They use full-frame NEAREST sampling, with original generated foreground alpha preserved. Their 4× previews are exact integer expansions.

These exports **do not meet the requirement that the original artwork be authored directly at native resolution**. Both foregrounds also contain partial alpha and therefore **do not meet strict 0/255 pixel-sharp alpha**. These are recorded as unmet requirements, not silently passed or remedied through undisclosed palette/alpha conversion. The review package is valid; artistic/production compliance is incomplete. No original native-resolution PNGs were returned by the tool.

No palette cap was invented. Actual visible RGB counts and dominant colors are in palette.json. No palette quantization, dithering, sharpening, crop or painted pixels are introduced by packaging. The close backgrounds were generated independently, not derived from resized main scenes.

## Owner steering and revisions

The initial restroom repeated the receptionist appearance and literal reception architecture. Nate rejected that repetition and requested modest chapter-level palette/architecture variation. Those two initial sources are superseded. The final set uses a new middle-aged male attendant, a separate auburn-haired female presenter, and cream/coral/slate-blue Pavilion architecture. Exact owner messages and the applied interpretation are in sources/owner-steering.json. Original registered prompts remain byte-exact; the owner direction is appended to relevant submissions.

A third superseded source is a counter-height study caught during composite QA. Nine tool calls therefore produce six current review candidates plus three unselectable studies. generation-records.json preserves each call's prompt, reference order, original path/hash and role. No Batch B candidate exists.

## Rebuild and verification

Use Python 3 and Pillow: `python3 build_review.py`, then `python3 verify_review.py`. The latter checks exact dimensions, 4× pixels, composites, alpha preservation, source hashes, prompt inclusion, reference provenance, narrative lock and protected-source scope. Its successful exit means packaging integrity, not artistic approval; qa.json separately reports failed artwork requirements. Browser evidence is in browser-qa.json.

The isolated branch variant of the existing `.github/workflows/pages.yml` builds the latest public `main`, then overlays only this review directory from the generation commit. It preserves public story/catalogue/viewer/selected-art content from `main`. It does not publish the preparation branch's story files. deployment-provenance.json is written by the workflow and records both source commits. No branch merge or gameplay integration is performed.

Public review URL: https://interstellarharvest.github.io/CYOA-storyboard/tools/prologue-art-lab/assets/review/chapter-03-batch01-2026-11-18/

Stop at Nate's visual selection gate. All six remain generated/unselected with no production assetPath. Selection is not inferred from generation, QA, committing or publication. Native-grid and alpha remediation remain outstanding production requirements.
