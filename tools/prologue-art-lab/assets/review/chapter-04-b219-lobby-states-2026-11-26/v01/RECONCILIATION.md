# B2-19 — minimum-state reconciliation before production

Source: canonical main `3785e87506c4218a360cf7a309b2fbe690cc4546`, docs/129,
docs/137–138 and authored Chapter 4 nodes. R1 remains suspended. All new B2-19
images are UNSELECTED conditional references, not new scene keys or bindings.

| Necessary image | Authored beat and coverage | Reuse / narration |
| --- | --- | --- |
| Lobby, both restroom door leaves removed | Persistent result of `hotel_auctioneer_arrival`; removal continues as the player enters `hotel_restroom_entry`; later lobby visits retain the open entrances | The first door being carried away is a transient narrated beat. No arbitrary left-first/right-first variation, new workmen or removal machinery. Keep both existing stone-framed openings and central pier. |
| Lot 61 pod, open | `hotel_lot61_pod_auction`, after the booth is wheeled out and its entrance opens; also `hotel_lot61_pod_declined` while departure begins | One open view covers slightly-open/revealed/open-for-demonstration beats. Porters' motion and the warning wording remain narrated. No closed/occupied/folding-animation images. |
| Lot 61 compact case, empty after escape | `hotel_lot61_pod_escaped`, **after** the metallic folding finishes | `ch4_pod_survived_packing=true` is set on node entry before the folding text; do not use that flag alone to reveal the packed image prematurely. The case is ordinary briefcase size. No loose shoe or occupant bulge on the successful escape path. |

All Lot 61 frames retain the already-removed doors. The compact case occupies the
pod's former floor area. The same doorless lobby can be reused when the declined
pod has departed; no duplicate departure/empty-lobby PNG is needed.

The failed packing outcome already has the approved FOLDED FOR CONVENIENCE death
illustration. Preserve it unchanged, including its fatal-specific shoe and slight
bulge. It supplies the steel case design benchmark, not pixels to resize into the
new wide-room state. Do not copy the fatal shoe into the successful escape frame.

The auctioneer's approved closer background shows his wall/podium context rather
than the restroom-door pair or floor presentation area. No extra closer-camera
variant is added to the docs/137 main-scene families. All runtime timing remains
for a later authorized integration; no new flags, Focus IDs, modes or bindings.

## PMO resolution of B2-18 hold

The current owner instruction authorizes reuse of approved CH4-B2-03 for
`hotel_stall_porter_protest`. Native/4× assessment with the approved businesslike
porter confirms the edge remains visible but peripheral; it is not occluded.
The PMO accepts it at native size. No post-lift closer reconstruction is required.
The unchanged source PNG remains authoritative. This supersedes the earlier
review hold and docs/150's historical pending-camera note without editing them.

Canonical main already includes PR #42's upper-salvage wording correction. The
earlier toilet-location conflict is resolved; do not report it as a new blocker.
