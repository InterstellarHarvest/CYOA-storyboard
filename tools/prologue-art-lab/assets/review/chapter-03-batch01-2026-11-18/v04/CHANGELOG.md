# v04 targeted corrections — generated / unselected

Source: `0df9994a1162528cc0de33add680a7d43717b4fa`. No image-generation calls.

A06: additional integer translation (-28,0) relative to v03. Total displacement from v02 is (-72,+29). Eye anchor (220,113) → (192,113); open-hand anchor (343,174) → (315,174). Bounds (139,74)–(367,278) → (111,74)–(339,278). The existing bottom-edge alignment is unchanged; every visible source pixel is retained at scale 1, with no clipping or color modification. The complete conservative microphone mask is now covered. Both countdown digits remain unobscured. The camera remains recognizable with a limited right-edge overlap; the overlap is explicitly measured in qa.json.

A01: 934 native pixels changed. Exactly 138 remove the contactless desktop device/base inside polygon `(237,134), (246,134), (249,137), (251,140), (251,143), (232,143), (232,138), (234,136)`. Existing desk/background/seat RGB pixels reconstruct the exposed area. The separate restroom access/gate hardware is untouched.

The other 796 changes are hand-authored one-pixel dark-contour repairs: 200 seated-attendant pixels (hair, spectacle rims/bridge, cheek/jaw edge, shoulders/sleeves, vest edges and clasped-hand contour) and 596 architectural pixels (restroom inner lintel/jambs, side-exit frame, counter lower edge). Exact paths and ink colors are in sources/outline-strokes.json. Every actual changed pixel has its original and final RGBA values and reason in sources/a01-pixel-ledger.json. No pixels outside the removal polygon or these paths changed.

A02, A03, A04 and A05 are byte-identical v03 carry-forwards. All v01/v02/v03 history stays untouched. No global quantization, blur, sharpening, dithering, resampling or generative reinterpretation.
