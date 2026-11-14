// Public-safe artwork metadata only. No private story graph or production gameplay code.
window.PUBLIC_PROLOGUE_ART = {
  "schema": "public-prologue-art-review-v1",
  "source": "Approved M2 Round 2 visuals and 28 candidate artwork PNGs",
  "scenes": [
    {
      "id": "workplace/applause_station",
      "title": "APPLAUSE TIMING STATION",
      "path": "art/scenes/workplace/applause_station.png",
      "status": "generated",
      "background": null
    },
    {
      "id": "workplace/corridor",
      "title": "EMPLOYEE CORRIDOR",
      "path": "art/scenes/workplace/corridor.png",
      "status": "generated",
      "background": "art/portraits/termination_drone/corridor_background.png"
    },
    {
      "id": "workplace/exit",
      "title": "PERSONAL EFFECTS EXIT",
      "path": "art/scenes/workplace/personal_effects_exit.png",
      "status": "generated",
      "background": null
    },
    {
      "id": "street/outside_workplace",
      "title": "STREET / EXPOSITION APPROACH",
      "path": "art/scenes/exposition/street_approach.png",
      "status": "generated",
      "background": null
    },
    {
      "id": "exposition/entrance",
      "title": "EXPOSITION TURNSTILE / CONTAINER CHUTE",
      "path": "art/scenes/exposition/entrance_turnstile.png",
      "status": "generated",
      "background": null
    },
    {
      "id": "exposition/property_intake",
      "title": "PROPERTY FOR YOUR CONVENIENCE",
      "path": "art/scenes/exposition/property_counter.png",
      "status": "generated",
      "background": null
    },
    {
      "id": "exposition/reception",
      "title": "RECEPTION HALL — APPROVED M2 ART",
      "path": "art/scenes/conference_hall/reception/reception_scene.png",
      "status": "reused",
      "background": "art/portraits/receptionist/reception_background.png"
    },
    {
      "id": "exposition/facilities_corridor",
      "title": "AMBIGUOUS FACILITIES HALL",
      "path": "art/scenes/exposition/facilities_corridor.png",
      "status": "generated",
      "background": null
    }
  ],
  "portraits": [
    {
      "id": "none",
      "title": "No portrait",
      "type": "none"
    },
    {
      "id": "drone-closed",
      "title": "Drone — closed slot",
      "type": "drone",
      "background": "art/portraits/termination_drone/corridor_background.png",
      "foreground": "art/portraits/termination_drone/drone_slot_closed.png",
      "scene": "workplace/corridor"
    },
    {
      "id": "drone-paper",
      "title": "Drone — paper extended",
      "type": "drone",
      "background": "art/portraits/termination_drone/corridor_background.png",
      "foreground": "art/portraits/termination_drone/drone_paper_extended.png",
      "scene": "workplace/corridor"
    },
    {
      "id": "receptionist",
      "title": "Approved receptionist",
      "type": "reception",
      "background": "art/portraits/receptionist/reception_background.png",
      "foreground": "art/portraits/receptionist/receptionist_idle.png",
      "scene": "exposition/reception"
    }
  ],
  "items": [
    {
      "id": "termination_notice",
      "title": "TERMINATION NOTICE",
      "slot": "art/items/termination_notice_slot.png",
      "inspect": "art/items/termination_notice_inspect.png",
      "status": "generated"
    },
    {
      "id": "timing_clicker",
      "title": "APPLAUSE TIMING CLICKER",
      "slot": "art/items/applause_timing_clicker_slot.png",
      "inspect": "art/items/applause_timing_clicker_inspect.png",
      "status": "generated"
    },
    {
      "id": "desk_plant",
      "title": "SMALL DESK PLANT",
      "slot": "art/items/small_desk_plant_slot.png",
      "inspect": "art/items/small_desk_plant_inspect.png",
      "status": "generated"
    },
    {
      "id": "effects_box_full",
      "title": "SEALED PERSONAL EFFECTS BOX",
      "slot": "art/items/effects_box_full_slot.png",
      "inspect": "art/items/effects_box_full_inspect.png",
      "status": "generated"
    },
    {
      "id": "effects_box_empty",
      "title": "OPENED / EMPTY EFFECTS BOX",
      "slot": "art/items/effects_box_empty_slot.png",
      "inspect": "art/items/effects_box_empty_inspect.png",
      "status": "generated"
    },
    {
      "id": "red_stapler",
      "title": "RED SWANGLINE STAPLER",
      "slot": "art/items/red_swangline_stapler_slot.png",
      "inspect": "art/items/red_swangline_stapler_inspect.png",
      "status": "generated"
    },
    {
      "id": "rubber_band_ball",
      "title": "RUBBER-BAND BALL",
      "slot": "art/items/rubber_band_ball_slot.png",
      "inspect": "art/items/rubber_band_ball_inspect.png",
      "status": "generated"
    },
    {
      "id": "property_claim_ticket",
      "title": "PROPERTY CLAIM TICKET",
      "slot": "art/items/property_claim_ticket_slot.png",
      "inspect": "art/items/property_claim_ticket_inspect.png",
      "status": "generated"
    },
    {
      "id": "expo_examiner_badge",
      "title": "TEMPORARY EXAMINER BADGE",
      "slot": "art/items/expo_examiner_badge_slot.png",
      "inspect": "art/items/expo_examiner_badge_inspect.png",
      "status": "generated"
    },
    {
      "id": "wc_key",
      "title": "FACILITIES KEY",
      "slot": "art/items/bathroom_pass_slot.png",
      "inspect": "art/items/bathroom_pass_inspect.png",
      "status": "reused"
    }
  ]
};
