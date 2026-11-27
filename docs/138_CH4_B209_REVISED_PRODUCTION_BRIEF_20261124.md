# Chapter 4 B2-09 (revised) — production brief and revised Chapter 4 queue

**Authority:** Nate approved the docs/137 consolidation on 2026-11-24 (PR #31). This brief replaces the original four-asset B2-09. That plan is in docs/136 "Automatic next group", now marked SUPERSEDED.

**Do not produce:**
- a refreshment-table scene or closer background;
- a second Bixby expression ("commanding");
- any image for the text-led or voice-only keys (docs/137 C1/C2).

All new images are published **UNSELECTED** on the review branch `art/ch4-batch01-review-20261121`. Registration happens only after Nate selects them (docs/105 `register-art.mjs`).

## 1. Assets (3 primary units)

| Unit | Canonical key at registration | Contract | Nodes |
|---|---|---|---|
| **CH4-NEW-05** Commodore Bixby | `portraits:hotel_commodore_bixby:delighted` | 564×278 transparent RGBA foreground | `hotel_commodore_bixby`, `hotel_bixby_emergency` (pose remapped from commanding), `hotel_bixby_trade` |
| **CH4-NEW-06** Wedding organizer | `portraits:hotel_wedding_organizer:urgent` | 564×278 transparent RGBA foreground | `hotel_wedding_arrival`, `hotel_bridal_organizer` |
| **CH4-NEW-18** Ballroom / reception closer background | `scenes:grand_bellevue/ballroom#portraitBackground` | 564×278 opaque RGB | the five nodes above. `refreshment_table` reuses it at integration (docs/137 C3). |

### CH4-NEW-05 — Commodore Bixby (one reusable expression)

Canon facts:
- a gentleman wedding guest in a **miniature naval cap** (it "nearly falls off" when he straightens);
- a **green auction paddle** sticking out of his coat pocket;
- polished shoes;
- a small whistle.

Expression: delighted, enthusiastic and nautical. It must also carry "An emergency at sea! Why didn't you say so?" without a second portrait.

**Hands are empty.** The brass valve wheel and the silver ice bucket are environment props: he pulls the wheel free and *presses it into your hands* (`hotel_bixby_emergency`), or *hands you the brass wheel* (`hotel_bixby_trade`). The portrait must never show the wheel permanently. No protagonist, and no protagonist's hands, in frame.

### CH4-NEW-06 — Wedding organizer

Match the organizer already drawn in approved CH4-05:
- curled auburn-brown hair worn up;
- charcoal-slate skirt suit with a white collar;
- dark heels;
- a **stack of clipboards** (canon: "consulting three clipboards").

Expression: urgent and over-committed, briskly kind ("Excellent. We've already lost two."). One portrait only.

### CH4-NEW-18 — Ballroom / reception closer background (shared)

It must be physically true for every node that uses it:
- "the lavishly decorated reception hall" (arrival);
- "outside the ballroom… a florist explains a missing centerpiece" (organizer);
- "at the edge of the reception… water creeps out from beneath the ballroom door" (Bixby).

**Compose it at the ballroom's threshold:**
- an ornate **ballroom door** in view, with a visible floor gap at its base;
- the edge of the reception: a white-clothed **refreshment table** with an ice bucket position, white flowers, drapes and swags matching CH4-05;
- the same architecture as CH4-05 and CH4-01: green-gray paneling, sconces, ducting.

Leave clear foreground space for a 564×278 portrait. There is no Lot 31 chair, no auction podium and no piano lot; those belong to the lobby (CH4-02).

### Localized prop treatment: conditional references, not primary images

Following the B2-07/B2-08 pattern, provide UNSELECTED supplemental reference frames of NEW-18 with exact localized changes and no new keys:
1. **wheel boat**: the brass valve wheel mounted on the silver ice bucket on the table (`hotel_commodore_bixby`);
2. **wheel gone**: the bucket without the wheel (`hotel_bixby_emergency`; wheel handed over);
3. **fender**: the bucket with the rubber-band ball tied on with a napkin (`hotel_bixby_trade`; it stays with him);
4. **water**: a thin sheet of water spreading from under the ballroom door (combinable with 1–3).

Timing is decided by a later authorized integration task. No flags, nodes or bindings are prescribed.

## 2. Standard (docs/129, mandatory)

- A detailed reference first, then a **separate native-resolution interpretation**, never a downscale or palette reduction.
- Portraits keep expressive faces and hands with palette discipline. Backgrounds stay rich but deliberately lit, with controlled palettes. For scale: the other approved Chapter 4 closer backgrounds measure 123–172 colours; CH4-02 measures 689, and CH4-B2-03 and B2-11 are flagged.
- The gallery compares against approved Chapter 2 references and CH4-05 / CH4-B2-23 at **native and exact 4× nearest-neighbour**.
- Record honest provenance (source-derived vs native-authored), SHA-256 values, prompts and masks.

## 3. Revised Chapter 4 production queue (after B2-09)

| Group | Units | Notes |
|---|---|---|
| B2-10 | NEW-03 upper salvage mezzanine | Must show the freight-lift doors and W.C. panel (freight_lift reuses it), the hatch and the service stairs. No clerk portrait (voice-only). |
| B2-11 | NEW-04 public corridor (dry base) | Plus `public_corridor_flood` state references. No guest or attendant portraits (voice-only). |
| B2-12 | NEW-01 bridal dressing room, NEW-07 privacy panel (Focus A) | Plus `bridal_privacy_status` states. The door AI is voice-only. |
| B2-13 | NEW-08 AutoFit gown (Focus A) | Plus `gown_motor_manual_slack` states. |
| B2-14 | NEW-02 bridal lavatory, NEW-09 three seashells (Focus A) | No toilet or concealed fixture. The bathroom AI is voice-only. |
| B2-16 | NEW-14–17 four fatal aftermaths | Popups unchanged; never the protagonist's face. |
| B2-17 | NEW-10–13 dispute ticket and ring, slot + inspection | The ring brief is corrected in the registry to **AS IS, WHERE IS.** |
| R1 | Refinement redraws of CH4-01, CH4-04, CH4-05, CH4-B2-03, CH4-B2-11 and **CH4-03** (added 2026-11-24, docs/141) | UNSELECTED; the approved PNGs stay selected until Nate picks replacements. Keep composition, layout, materials, objects and humor. CH4-03 must also match the approved auctioneer identity in CH4-B2-31/35 and use binary alpha. Not started: no redraws until Nate says so. |
| B2-18 / B2-19 | Restroom, lobby and Lot 61 state families | Derive from the R1-refined masters once selected. |

Old B2-15 (approaches and exits) needs no production: it is resolved by text-led presentation and reuse (docs/137).

## 4. Reconciliation with the existing B2-09 v01/v02 package (docs/139 §3)

An UNSELECTED B2-09 package made under the old brief already exists on the review branch (`b896f50`). **Do not regenerate what it already covers.** Candidates go to Nate for selection, unchanged:
- **NEW-05 Bixby:** CH4-B2-49 v01.
- **NEW-18 base:** CH4-B2-51-emergency v02 (the no-wheel plate).
- **Localized states:** CH4-B2-51 v01 (wheel boat) and CH4-B2-51-trade v02 (fender).

**Still to produce, after Nate approves:**
1. the wedding organizer portrait (NEW-06);
2. one water-under-the-ballroom-door state derived from the NEW-18 base.

**Redundant, preserved, never selected:** CH4-B2-50, CH4-B2-48 and its two states (B2-48 also has a red-rectangle artifact).
