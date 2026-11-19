# Batch A v03 — exact correction scope

All files remain generated/unselected. Source: `32273a2839e3a941530a153b69fb9a508e92f57b`. No image generation, scaling, filtering, quantization, dithering or new interpretation.

| Candidate | Operation | Changed native pixels |
|---|---|---:|
| A01 | Byte-identical v02 carry-forward | 0 |
| A02 | Local device/base/shadow removal | 3,761 |
| A03 | Integer translation (+44, 0) | 35,382 canvas positions; internal RGBA pixels unchanged |
| A04 | Byte-identical v02 carry-forward | 0 |
| A05 | Byte-identical v02 carry-forward | 0 |
| A06 | Integer translation (-44, +29) | 31,553 canvas positions; internal RGBA pixels unchanged |

A02 allowed native polygon (pixel centers): `(404,227), (470,227), (474,231), (485,258), (485,275), (479,275), (479,272), (406,272), (394,263), (394,252), (400,231)`. It covers the device and its shadow, including the small trailing base mark at x479–484/y272–274. No changed pixel lies outside this polygon. The plant starts beyond it and is untouched.

Wall restoration: copy existing wall pixels in the same x columns from rows `220 + ((targetY - 227) % 5)` through target row 260. This continues the original vertical wall joint. Desktop restoration: for rows 261–274, copy original clean adjacent desktop pixels from x `390 + ((targetX - 394) % 4)` at the same y. No new RGB colors are synthesized, and the gate/access-control hardware is not removed.

A03 anchors: eye (270,86) → (314,86); hands (276,254) → (320,254). Bounds (179,43)–(368,263) → (223,43)–(412,263). Headroom stays 43 px, bottom clearance 15 px. No visible pixel clipped.

A06 anchors: eye (264,84) → (220,113); open-hand anchor (387,145) → (343,174). Bounds (183,45)–(411,249) → (139,74)–(367,278). Headroom 74 px, bottom clearance 0 px. The lowest occupied source row lands exactly at y277; no visible source pixel is clipped. Costume, fingers, hair and expression are preserved.

A01 exception/concern: the miniature desktop device remains in the main scene. A01 is explicitly protected; it is carried forward byte-identically. Any narrowly scoped removal there needs Nate's separate continuity approval. No such exception was applied in v03.
