# Approved three kit-description corrections

Canonical authored file: story/chapters/chapter-02.draft.json, nodes public_kit_focus, maintenance_kit_focus, customs_kit_focus. Commit45b0488af8c0e4539105810b21d0651c1b7f49fa.

Exactly three instances of “a chunky medical injector secured beside a glass vial” become “a chunky medical injector with a glass vial secured inside its metal cage”. Reversing this phrase replacement reproduces the entire original file byte-for-byte. Openings, antidote identification, folded label, expiration years1977/1969/1981, choices, consequences and treatment mechanics are preserved. Concurrent Chapter3 unchanged.

At the last verified playable game commit20b52601c5733a633a385bbb1c60995174e530cc the separate copies still need PMO synchronization:

- story/chapters/chapter-02.draft.json:2216,2386,2556
- generated game/content/story.generated.js:5537,5707,5877

Gameplay PMO should pull the corrected canonical revision through story-sync and regenerate playable content. Do not hand-edit generated projections. No gameplay branch or engine file was changed.
