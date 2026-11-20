// Public-safe visual review only. This does NOT import the private gameplay engine.
// All visible M2 chrome and art is copied byte-identically; the scene, portrait,
// inventory and inspector positions follow the approved M2 art geometry.
(() => {
  "use strict";

  const $ = id => document.getElementById(id);
  const stage = $("stage");
  const viewport = $("previewViewport");
  const wrap = $("previewWrap");
  const SPARE_SLOTS = 3; // Game and M1 lab expose adjacent items during the slide.
  let inventoryFrame = null;
  const data = { catalog: null, index: null, controls: null, layout: null, fonts: null, exposition: null, scenes: [], items: [], urls: new Map() };
  const state = {
    scene: "workplace/applause_station",
    sceneVersion: "current",
    portrait: "auto",
    visibleBackground: true,
    visibleForeground: true,
    poseX: 0,
    poseY: 0,
    slots: 6,
    buttonMode: "label",
    buttonSkin: "up",
    pressedUtility: null,
    inventoryStart: 0,
    inventorySlide: null,
    selectedItem: "termination_notice",
    inspection: null,
    fit: true
  };

  // Explicit, stable scope of this historical Prologue / early Exposition study. The shared
  // story/artwork.draft.json catalogue grows with every chapter; the lab displays ONLY these
  // original records, in this order, and never enumerates the whole catalogue. Keep this list
  // JSON-literal: tools/prologue-art-lab/qa/qa-static.mjs parses it and checks it against its audit.
  const LAB_SCOPE = Object.freeze(/* LAB_SCOPE_BEGIN */{
    "scenes": [
      "workplace/applause_station", "workplace/corridor", "workplace/exit", "street/outside_workplace",
      "exposition/entrance", "exposition/property_intake", "exposition/reception", "exposition/facilities_corridor"
    ],
    "items": [
      "termination_notice", "timing_clicker", "desk_plant", "effects_box_full", "effects_box_empty",
      "red_stapler", "rubber_band_ball", "property_claim_ticket", "expo_examiner_badge", "wc_key"
    ],
    "portraits": ["termination_drone:slot_closed", "termination_drone:paper_extended", "receptionist:default"]
  }/* LAB_SCOPE_END */);
  const SELECTED_STATUSES = ["approved", "integrated", "reused"];

  const PAIRINGS = [
    {id:"auto",title:"Automatic — matched to scene"},
    {id:"none",title:"No portrait"},
    {id:"drone-closed",title:"Termination drone — closed slot"},
    {id:"drone-paper",title:"Termination drone — paper extended"},
    {id:"receptionist",title:"Approved receptionist"}
  ];

  function safe(id) {
    const name = String(id);
    if (!/^art\/[a-zA-Z0-9._/-]+$/.test(name) || name.includes("..")) throw new Error("Unsafe art asset path");
    return name;
  }
  function asset(record, fallback) {
    if (fallback) return "assets/approved/" + safe(fallback);
    if (!record || !record.assetPath) return null;
    // Asset storage stays SHA-pinned to its original draft/approved review directory.
    // The new integrated/approved statuses describe selection, NOT directory location.
    const filename=safe(record.assetPath);
    const candidates=["assets/draft/"+filename,"assets/approved/"+filename];
    const rows=(data.index?.files||[]).filter(row=>candidates.includes(row.path));
    if(rows.length!==1)throw new Error("Pinned Prologue source is missing or ambiguous: "+filename);
    return rows[0].path;
  }
  function setImg(el, url, visible = true) {
    const show = !!url && visible;
    el.hidden = !show;
    if (show && el.getAttribute("src") !== url) el.src = url;
  }
  function option(select, value, title) {
    const node = document.createElement("option");
    node.value = value;
    node.textContent = title;
    select.appendChild(node);
  }
  function itemTitle(id) {
    const row = data.catalog.items[id];
    return row && row.slot && row.slot.title
      ? row.slot.title.split(" — ")[0]
      : id.replaceAll("_", " ").toUpperCase();
  }
  function sceneTitle(id) {
    const entry = data.catalog.scenes[id];
    return (entry && entry.title) || id.replaceAll("/", " / ").toUpperCase();
  }
  function matchedPose() {
    if (state.portrait !== "auto") return state.portrait;
    if (state.scene === "workplace/corridor") return "drone-closed";
    if (state.scene === "exposition/reception") return "receptionist";
    return "none";
  }
  function portraitSpec(id) {
    if (id === "none") return null;
    if (id === "drone-closed" || id === "drone-paper") {
      return {
        scene: "workplace/corridor",
        background: asset(data.catalog.scenes["workplace/corridor"].portraitBackground),
        foreground: asset(data.catalog.portraits[id === "drone-closed"
          ? "termination_drone:slot_closed" : "termination_drone:paper_extended"])
      };
    }
    if (id === "receptionist") {
      const src = data.catalog.portraits["receptionist:default"];
      const bg = src.layers.find(l => l.role === "background");
      const fg = src.layers.find(l => l.role === "foreground");
      return {
        scene: "exposition/reception",
        background: asset(null, bg.path),
        foreground: asset(null, fg.path)
      };
    }
    throw new Error("Unknown portrait: " + id);
  }
  function previousSceneRecord(id) {
    const row = data.exposition && data.exposition.scenes.find(s => s.id === id);
    if (!row || !row.comparisonInPublicLab) return null;
    return { status: "generated", assetPath: row.retainedPreviousAssetPath };
  }
  function currentSceneRecord() {
    return state.sceneVersion === "previous" && previousSceneRecord(state.scene)
      ? previousSceneRecord(state.scene)
      : data.catalog.scenes[state.scene];
  }
  function setSceneVersion(version) {
    if (version !== "current" && version !== "previous") throw new Error("Unsupported scene artwork version");
    if (version === "previous" && !previousSceneRecord(state.scene)) throw new Error("Archived version not safe for preview");
    state.sceneVersion = version;
    renderScene();
    renderControls();
  }
  function setScene(id) {
    if (!data.scenes.includes(id)) throw new Error("Unknown scene " + id);
    state.scene = id;
    state.sceneVersion = "current";
    state.inspection = null;
    render();
  }
  function changeScene(step) {
    const at = data.scenes.indexOf(state.scene);
    setScene(data.scenes[(at + step + data.scenes.length) % data.scenes.length]);
  }
  function setPortrait(id) {
    if (!PAIRINGS.some(p => p.id === id)) throw new Error("Unknown portrait " + id);
    state.portrait = id;
    renderPortrait();
    renderControls();
  }
  function setSlots(n) {
    if (n !== data.layout.inventory.slotCount) throw new Error("The owner baseline is six slots; comparison with seven is retired");
    state.slots = n;
    state.inventoryStart = Math.min(state.inventoryStart, Math.max(0, data.items.length - n));
    renderInventory();
    renderControls();
  }
  // Preserve the original M1/game easing, overshoot, recoil and per-slot lag.
  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }
  function slideCurve(elapsed, from, motion) {
    const u = elapsed / Math.max(1, motion.durationMs);
    if (u <= 0) return from;
    if (u >= 1) return 0;
    const sign = from < 0 ? -1 : 1;
    const past = -sign * motion.overshoot;
    const back = sign * motion.settle;
    if (u < 0.6) {
      const q = 1 - u / 0.6;
      return past + (from - past) * q * q * q;
    }
    if (u < 0.85) return past + ((back - past) * (u - 0.6)) / 0.25;
    return (back * (1 - u)) / 0.15;
  }
  function slideShift(now) {
    const slide = state.inventorySlide;
    return slide ? Math.round(slideCurve(now - slide.start, slide.from, data.layout.inventory.motion)) : 0;
  }
  function slotShift(now, row, last) {
    const slide = state.inventorySlide;
    const motion = data.layout.inventory.motion;
    const order = slide.from > 0 ? row : last - row;
    return Math.round(slideCurve(
      now - slide.start - clamp(order, 0, last) * motion.lagMs, slide.from, motion
    ));
  }
  function inventoryWindow(inventory, at) {
    const pad = inventory.motion.overshoot + inventory.motion.settle;
    const width = (state.slots - 1) * inventory.pitch + inventory.slotSize[0];
    const left = Math.max(pad, at.x - (inventory.leftArrow.x + inventory.leftArrow.displayWidth));
    const right = Math.max(pad, inventory.rightArrow.x - (at.x + width));
    return {x: at.x - left, left, width: left + width + right};
  }
  function inventoryTick(now) {
    inventoryFrame = null;
    const slide = state.inventorySlide;
    if (!slide) return;
    const motion = data.layout.inventory.motion;
    if (now - slide.start >= motion.durationMs + motion.lagMs * (state.slots - 1)) {
      state.inventorySlide = null;
    }
    renderInventory(now);
    if (state.inventorySlide) inventoryFrame = requestAnimationFrame(inventoryTick);
  }
  function wakeInventory() {
    if (inventoryFrame === null) inventoryFrame = requestAnimationFrame(inventoryTick);
  }
  function setInventoryStart(n) {
    const next = clamp(Math.round(Number(n) || 0), 0, Math.max(0, data.items.length - state.slots));
    const moved = next - state.inventoryStart;
    if (!moved) return;
    const now = performance.now();
    const inv = data.layout.inventory;
    const prefersReducedMotion = window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (inv.motion.slide && !prefersReducedMotion) {
      // Rebase the running slide before starting another: rapid reverse clicks
      // retain momentum rather than snapping the items to new slots.
      const from = clamp(slideShift(now) + moved * inv.pitch, -2 * inv.pitch, 2 * inv.pitch);
      state.inventorySlide = {from, start: now};
    } else {
      state.inventorySlide = null;
      if (inventoryFrame !== null) cancelAnimationFrame(inventoryFrame);
      inventoryFrame = null;
    }
    state.inventoryStart = next;
    renderInventory(now);
    renderControls();
    if (state.inventorySlide) wakeInventory();
  }
  function openItem(id) {
    if (!data.items.includes(id)) throw new Error("Unknown item " + id);
    state.selectedItem = id;
    state.inspection = id;
    renderInspector();
    renderControls();
  }
  function closeInspector() {
    state.inspection = null;
    renderInspector();
    renderControls();
  }
  function setLayers(spec) {
    if (Object.hasOwn(spec, "background")) state.visibleBackground = !!spec.background;
    if (Object.hasOwn(spec, "foreground")) state.visibleForeground = !!spec.foreground;
    if (Object.hasOwn(spec, "x")) state.poseX = Math.max(-40, Math.min(40, Math.round(Number(spec.x) || 0)));
    if (Object.hasOwn(spec, "y")) state.poseY = Math.max(-40, Math.min(40, Math.round(Number(spec.y) || 0)));
    renderPortrait();
    renderControls();
  }

  function renderScene() {
    const scene = data.catalog.scenes[state.scene];
    setImg($("sceneImage"), asset(currentSceneRecord()));
    $("sceneAperture").setAttribute("aria-label", scene.title + " — 314 by 206 scene at 4 times native scale");
    $("sceneLabel").textContent = scene.title;
    $("sourceLabel").textContent = scene.status === "reused"
      ? "Approved M2 reception comparison · original art"
      : state.sceneVersion === "previous"
        ? "Archived earlier candidate · comparison only"
        : data.exposition.scenes.some(r => r.id === state.scene)
          ? "Current Exposition V03 study · generated · owner approval pending"
          : "Generated prologue art · awaiting owner approval";
    renderText();
  }
  function renderPortrait() {
    const id = matchedPose();
    const spec = portraitSpec(id);
    setImg($("portraitBackground"), spec && spec.background, state.visibleBackground);
    setImg($("portraitForeground"), spec && spec.foreground, state.visibleForeground);
    $("portraitForeground").style.left = state.poseX + "px";
    $("portraitForeground").style.top = state.poseY + "px";
    $("portraitAperture").setAttribute("aria-label", id === "none" ? "No character portrait in this scene" :
      (id === "receptionist" ? "Approved receptionist" : id === "drone-closed" ?
        "Drone with closed paper slot" : "Drone with paper extended") + " with separate portrait background");
    const pairing = $("portraitPairing");
    if (!spec) {
      pairing.textContent = "No NPC portrait is authored for this scene.";
      pairing.classList.remove("mismatch");
    } else {
      const match = spec.scene === state.scene;
      pairing.textContent = match
        ? "Correct scene pairing: independent, 564 × 278 background and foreground layers."
        : "Composition comparison only: this portrait does not belong to the selected scene.";
      pairing.classList.toggle("mismatch", !match);
    }
  }

  // The 2026-11-13 six-slot placement is data, not another hand-tuned CSS preset.
  function locate(element, x,y,w,h) {
    const el = typeof element === "string" ? $(element) : element;
    Object.assign(el.style,{left:x+"px",top:y+"px",width:w+"px",height:h+"px"});
  }
  function applyLayout() {
    const L=data.layout, inv=L.inventory;
    for (const [id,spec] of [["stagePrev",inv.leftArrow],["stageNext",inv.rightArrow]]) {
      locate(id,spec.x,spec.y,spec.displayWidth,spec.displayHeight);
      locate($(id).querySelector("img"),0,0,spec.displayWidth,spec.displayHeight);
    }
    const c=L.choices, height=c.cardHeights["2"];
    for (const [i,id] of ["cardPrev","cardNext","cardInspect"].entries()) {
      const card=$(id);
      locate(card,c.viewport.x,c.viewport.y+i*(height+c.gap),c.cardWidth,height);
      const label=card.querySelector("canvas");
      locate(label,c.text.offsetX,Math.floor((height-2*c.text.lineHeight)/2)+c.text.offsetY,c.text.maxWidth,2*c.text.lineHeight);
    }
    const t=L.speech.text;
    locate("speechExample",t.x,t.y,t.width,t.height);
    locate("speechCanvas",0,0,t.width,t.height);
    const o=L.objective;
    locate("objectiveLabel",o.title.plaque.x,o.title.y,o.title.plaque.width,30);
    locate("objectiveText",o.body.x,o.body.y,o.body.width,75);
    const track=L.scrollbar.track;
    locate("choiceThumb",track.x,track.y+Math.floor((track.height-40)/2),track.width,40);
    const thumb=$("choiceThumb");
    thumb.querySelector(".thumb-top").src="assets/approved/art/ui/sprites/controls/choice_scroll_thumb_top.png";
    thumb.querySelector(".thumb-bottom").src="assets/approved/art/ui/sprites/controls/choice_scroll_thumb_bottom.png";
    thumb.querySelector(".thumb-middle").style.backgroundImage='url("assets/approved/art/ui/sprites/controls/choice_scroll_thumb_middle.png")';
  }
  function setButtonMode(mode) {
    if (mode!=="label" && mode!=="glyph") throw new Error("Unknown button artwork mode");
    state.buttonMode=mode;renderButtons();renderControls();
  }
  function setButtonSkin(skin) {
    if (skin!=="up" && skin!=="down") throw new Error("Unknown button state");
    state.buttonSkin=skin;renderButtons();renderControls();
  }
  function renderButtons() {
    if (!data.layout) return;
    const labels=["utilPrev","utilInspect","utilNext"];
    data.layout.utility.buttons.forEach((spec,i)=>{
      const el=$(labels[i]),img=el.querySelector(".utility-skin"),canvas=el.querySelector(".utility-label"),glyph=el.querySelector(".utility-glyph");
      locate(el,spec.x,spec.y,spec.displayWidth,spec.displayHeight);
      const down=state.buttonSkin==="down" || state.pressedUtility===labels[i];
      img.src="assets/approved/art/ui/sprites/controls/"+spec.spriteFamily+"_"+(down?"down":"up")+".png";
      locate(img,0,0,spec.displayWidth,spec.displayHeight);
      canvas.hidden=state.buttonMode!=="label";
      glyph.hidden=state.buttonMode!=="glyph";
      const off=down?data.layout.utility.pressedLabelOffset:{dx:0,dy:0};
      locate(canvas,off.dx+spec.labelOffset.dx,off.dy+spec.labelOffset.dy,spec.displayWidth,spec.displayHeight);
      locate(glyph,Math.floor((spec.displayWidth-96)/2)+off.dx+spec.labelOffset.dx,Math.floor((spec.displayHeight-96)/2)+off.dy+spec.labelOffset.dy,96,96);
      glyph.src="assets/approved/art/actions/"+spec.glyph+".png";
    });
    renderButtonLabels();
  }
  function renderButtonLabels() {
    if (!data.layout) return;
    const T=window.PUBLIC_PIXEL_TEXT,L=data.layout;
    L.utility.buttons.forEach((spec,i)=>{
      T.draw($("utilityLabel"+i),spec.label,L.typeface.labels,"light",
        {width:spec.displayWidth,height:spec.displayHeight,align:"center",valign:"center",lineHeight:24});
    });
  }
  function renderText() {
    if (!data.layout) return;
    const L=data.layout,T=window.PUBLIC_PIXEL_TEXT;
    const sceneName=sceneTitle(state.scene).replace(/[^A-Za-z0-9 \/-]/g," ");
    T.draw($("speechCanvas"),"ARTWORK REVIEW\nART: "+sceneName,L.typeface.dialogue,"dark",
      {width:L.speech.text.width,height:L.speech.text.height,lineHeight:L.speech.text.lineHeight,maxWidth:L.speech.text.width});
    ["VIEW PREVIOUS SCENE","VIEW NEXT SCENE","INSPECT SELECTED ITEM"].forEach((value,i)=>{
      T.draw($("choiceLabel"+i),value,L.typeface.choices,"dark",
        {width:L.choices.text.maxWidth,height:2*L.choices.text.lineHeight,lineHeight:L.choices.text.lineHeight});
    });
    T.draw($("objectiveLabel"),L.objective.title.text,L.typeface.objective,"light",
      {width:L.objective.title.plaque.width,height:30,align:"center"});
    T.draw($("objectiveText"),L.objective.body.text,L.typeface.objective,"light",
      {width:L.objective.body.width,height:75,lineHeight:L.objective.body.lineHeight,maxWidth:L.objective.body.width,align:"center"});
  }

  function buildInventory() {
    const strip = $("inventoryStrip");
    if (strip.children.length) return;
    const inv = data.layout.inventory;
    const slotArt = "assets/approved/art/ui/sprites/inventory/inventory_slot.png";
    // Persistent nodes: no image reloading or focus loss on every animation frame.
    // Keep document order equal to the original item order for keyboard navigation.
    for (let index = 0; index < data.items.length; ++index) {
      const itemId = data.items[index];
      const button = document.createElement("button");
      button.type = "button";
      button.className = "inventory-slot";
      button.dataset.item = itemId;
      button.dataset.index = String(index);
      button.setAttribute("aria-label", "Inspect " + itemTitle(itemId));
      button.style.width = inv.slotSize[0] + "px";
      button.style.height = inv.slotSize[1] + "px";
      button.hidden = true;
      const background = document.createElement("img");
      background.src = slotArt;
      background.alt = "";
      button.appendChild(background);
      const image = document.createElement("img");
      image.className = "item-image";
      image.src = asset(data.catalog.items[itemId].slot);
      image.alt = "";
      button.appendChild(image);
      button.addEventListener("click", () => openItem(itemId));
      strip.appendChild(button);
    }
  }
  function renderInventory(now = performance.now()) {
    const strip = $("inventoryStrip");
    const inv = data.layout.inventory;
    const at = inv.slotLayouts[String(inv.slotCount)];
    const box = inventoryWindow(inv, at);
    const sliding = !!state.inventorySlide && inv.motion.slide;
    buildInventory();
    Object.assign(strip.style, {
      left: box.x + "px",
      top: at.y + "px",
      width: box.width + "px",
      height: inv.slotSize[1] + "px"
    });
    const visible = new Set();
    const first = sliding ? -SPARE_SLOTS : 0;
    const last = sliding ? state.slots + SPARE_SLOTS - 1 : state.slots - 1;
    for (let row = first; row <= last; ++row) {
      const index = state.inventoryStart + row;
      if (index < 0 || index >= data.items.length) continue;
      const x = box.left + row * inv.pitch + (sliding ? slotShift(now, row, state.slots - 1) : 0);
      if (x + inv.slotSize[0] <= 0 || x >= box.width) continue;
      const button = strip.children[index];
      button.style.left = x + "px";
      button.style.top = "0px";
      button.dataset.row = String(row);
      visible.add(button);
    }
    for (const button of strip.children) button.hidden = !visible.has(button);
    strip.dataset.moving = sliding ? "true" : "false";
    strip.setAttribute("aria-label", state.slots + "-slot owner inventory with spring-slide art");
    $("inventoryStatus").textContent = "Showing items " + (state.inventoryStart + 1) + "–" +
      Math.min(data.items.length, state.inventoryStart + state.slots) +
      " of " + data.items.length + ". Use arrows to move one item at a time.";
  }
  function renderInspector() {
    const container = $("inspectionLayer");
    container.hidden = !state.inspection;
    if (!state.inspection) return;
    const row = data.catalog.items[state.inspection];
    setImg($("inspectionImage"), asset(row.inspect));
    $("inspectionName").textContent = itemTitle(state.inspection);
    $("inspectionLayer").setAttribute("aria-label", "Inspect " + itemTitle(state.inspection));
  }
  function renderControls() {
    $("sceneSelect").value = state.scene;
    $("sceneVersion").value = state.sceneVersion;
    $("sceneVersion").disabled = !previousSceneRecord(state.scene);
    $("sceneVersionInfo").textContent = previousSceneRecord(state.scene)
      ? "Previous unoccupied artwork available for comparison."
      : data.exposition.scenes.some(r => r.id === state.scene)
        ? "Earlier entrance/intake art contains staff and stays archived, not displayed."
        : "Only current art is displayed for this scene.";
    $("portraitSelect").value = state.portrait;
    $("showBackground").checked = state.visibleBackground;
    $("showForeground").checked = state.visibleForeground;
    $("poseX").value = String(state.poseX);
    $("poseY").value = String(state.poseY);
    $("slotStatus").textContent = state.slots + " slots · " + data.layout.inventory.gap + " px spacing · current baseline";
    $("buttonMode").value = state.buttonMode;
    $("buttonSkin").value = state.buttonSkin;
    $("inventoryPosition").max = String(Math.max(0, data.items.length - state.slots));
    $("inventoryPosition").value = String(state.inventoryStart);
    $("itemSelect").value = state.selectedItem;
  }
  function render() {
    renderScene();
    renderPortrait();
    renderInventory();
    renderInspector();
    renderControls();
    renderButtons();
    renderText();
  }
  function fitStage() {
    const scale = state.fit
      ? Math.max(.1, Math.min((viewport.clientWidth - 26) / 1920, (viewport.clientHeight - 26) / 1080, 1))
      : 1;
    stage.style.transform = "scale(" + scale + ")";
    wrap.style.width = (1920 * scale) + "px";
    wrap.style.height = (1080 * scale) + "px";
    $("fitPreview").setAttribute("aria-pressed", state.fit ? "true" : "false");
    $("actualPreview").setAttribute("aria-pressed", state.fit ? "false" : "true");
  }

  function bindCard(id, fn) {
    const element = $(id);
    element.addEventListener("click", fn);
    element.addEventListener("keydown", e => {
      if (e.key !== "Enter" && e.key !== " ") return;
      e.preventDefault();
      fn();
    });
  }
  function bind() {
    $("sceneSelect").addEventListener("change", e => setScene(e.target.value));
    $("sceneVersion").addEventListener("change", e => setSceneVersion(e.target.value));
    $("prevScene").addEventListener("click", () => changeScene(-1));
    $("nextScene").addEventListener("click", () => changeScene(1));
    $("compareReception").addEventListener("click", () => {
      state.portrait = "auto";
      setScene("exposition/reception");
    });
    $("portraitSelect").addEventListener("change", e => setPortrait(e.target.value));
    function layers() {
      setLayers({
        background: $("showBackground").checked,
        foreground: $("showForeground").checked,
        x: Number($("poseX").value),
        y: Number($("poseY").value)
      });
    }
    ["showBackground", "showForeground", "poseX", "poseY"].forEach(id =>
      $(id).addEventListener("change", layers));
    $("resetOffsets").addEventListener("click", () => setLayers({x:0,y:0}));
    $("buttonMode").addEventListener("change", e => setButtonMode(e.target.value));
    $("buttonSkin").addEventListener("change", e => setButtonSkin(e.target.value));
    $("inventoryPosition").addEventListener("input", e => setInventoryStart(Number(e.target.value)));
    $("inventoryPrev").addEventListener("click", () => setInventoryStart(state.inventoryStart - 1));
    $("inventoryNext").addEventListener("click", () => setInventoryStart(state.inventoryStart + 1));
    $("stagePrev").addEventListener("click", () => setInventoryStart(state.inventoryStart - 1));
    $("stageNext").addEventListener("click", () => setInventoryStart(state.inventoryStart + 1));
    for (const [button,base] of [["stagePrev","inv_left"],["stageNext","inv_right"]]) {
      const img = $(button + "Img");
      const loc = "assets/approved/art/ui/sprites/controls/" + base;
      $(button).addEventListener("pointerdown", () => {img.src = loc + "_down.png";});
      ["pointerup", "pointerleave", "pointercancel", "blur"].forEach(event =>
        $(button).addEventListener(event, () => {img.src = loc + "_up.png";}));
    }
    $("itemSelect").addEventListener("change", e => {
      state.selectedItem = e.target.value;
      openItem(state.selectedItem);
    });
    $("openInspector").addEventListener("click", () => openItem(state.selectedItem));
    $("closeInspector").addEventListener("click", closeInspector);
    $("inspectionCloseX").addEventListener("click", closeInspector);
    $("fitPreview").addEventListener("click", () => {state.fit=true;fitStage();});
    $("actualPreview").addEventListener("click", () => {state.fit=false;fitStage();});
    bindCard("cardPrev", () => changeScene(-1));
    bindCard("cardNext", () => changeScene(1));
    bindCard("cardInspect", () => openItem(state.selectedItem));
    $("utilPrev").addEventListener("click", () => openItem(state.selectedItem));
    $("utilInspect").addEventListener("click", () => { $("loadStatus").textContent = "NOTES button artwork · visual study only"; });
    $("utilNext").addEventListener("click", () => { $("loadStatus").textContent = "FILES button artwork · visual study only"; });
    for (const id of ["utilPrev", "utilInspect", "utilNext"]) {
      const button=$(id);
      button.addEventListener("pointerdown", () => {state.pressedUtility=id;renderButtons();});
      for (const evt of ["pointerup","pointercancel","pointerleave","blur"]) button.addEventListener(evt,()=>{state.pressedUtility=null;renderButtons();});
    }
    document.querySelectorAll("[data-inspect]").forEach(button =>
      button.addEventListener("click", () => openItem(button.dataset.inspect)));
    document.querySelectorAll("[data-scene]").forEach(button =>
      button.addEventListener("click", () => {state.portrait="auto";setScene(button.dataset.scene);}));
    window.addEventListener("resize", fitStage);
    if (window.ResizeObserver) new ResizeObserver(fitStage).observe(viewport);
    document.addEventListener("keydown", e => {
      if (e.key === "Escape" && state.inspection) closeInspector();
    });
  }
  function publicState() {
    return {
      ready: true,
      scene: state.scene,
      sceneVersion: state.sceneVersion,
      activeSceneAssetPath: currentSceneRecord().assetPath,
      currentCatalogAssetPath: data.catalog.scenes[state.scene].assetPath,
      sceneStatus: currentSceneRecord().status,
      sceneTitle: sceneTitle(state.scene),
      portrait: state.portrait,
      activePortrait: matchedPose(),
      slots: state.slots,
      slotPitch: data.layout.inventory.pitch,
      slotGap: data.layout.inventory.gap,
      buttonMode: state.buttonMode,
      buttonSkin: state.buttonSkin,
      buttonLabels: data.layout.utility.buttons.map(b=>b.label),
      inventoryStart: state.inventoryStart,
      inventoryMoving: !!state.inventorySlide,
      inventoryShift: slideShift(performance.now()),
      inventoryMotion: data.layout.inventory.motion,
      items: data.items.slice(state.inventoryStart,state.inventoryStart+state.slots),
      inspection: state.inspection,
      sceneSize: [314,206],
      sceneScale: 4,
      portraitSize: [564,278],
      iconSize: [96,96],
      inspectSize: [565,451],
      paired: !portraitSpec(matchedPose()) || portraitSpec(matchedPose()).scene === state.scene
    };
  }

  // Every scoped record must exist, be active (not archived), be selected art, and resolve to
  // exactly one SHA-pinned public source file. Unrelated catalogue records are never read.
  function scopeRecords() {
    const problems = [];
    const usable = (label, record) => {
      if (!record) { problems.push("missing " + label); return; }
      if (/^ARCHIVED \/ RETIRED \/ UNUSED\b/.test(record.notes || "")) problems.push(label + " is archived");
      if (!SELECTED_STATUSES.includes(record.status)) problems.push(label + " is not selected artwork (status " + (record.status || "not-started") + ")");
      try { if (!asset(record)) problems.push(label + " has no artwork"); }
      catch (error) { problems.push(label + ": " + error.message); }
    };
    const pinned = (label, file) => {
      try { if (!(data.index.files || []).some(row => row.path === asset(null, file))) problems.push(label + ": pinned source missing " + file); }
      catch (error) { problems.push(label + ": " + error.message); }
    };
    for (const id of LAB_SCOPE.scenes) usable("scene " + id, data.catalog.scenes?.[id]);
    usable("portrait background workplace/corridor", data.catalog.scenes?.["workplace/corridor"]?.portraitBackground);
    for (const id of LAB_SCOPE.items) {
      const row = data.catalog.items?.[id];
      if (!row) { problems.push("missing item " + id); continue; }
      usable("item " + id + " slot", row.slot);
      usable("item " + id + " inspector", row.inspect);
    }
    for (const id of LAB_SCOPE.portraits) {
      const record = data.catalog.portraits?.[id];
      if (record && record.layers) {
        for (const role of ["background", "foreground"]) {
          const layer = record.layers.find(l => l.role === role);
          if (!layer) problems.push("portrait " + id + " has no " + role + " layer");
          else pinned("portrait " + id + " " + role, layer.path);
        }
        if (!SELECTED_STATUSES.includes(record.status)) problems.push("portrait " + id + " is not selected artwork (status " + (record.status || "not-started") + ")");
      } else usable("portrait " + id, record);
    }
    if (problems.length) throw new Error("Prologue lab scope invalid: " + problems.slice(0, 6).join("; "));
    data.scenes = LAB_SCOPE.scenes.slice();
    data.items = LAB_SCOPE.items.slice();
  }

  async function preload(index,controls) {
    const errors = [];
    const batch = [...index.files,...controls.files].map(entry => new Promise(done => {
      const img = new Image();
      img.onload = () => done();
      img.onerror = () => {errors.push(entry.path);done();};
      img.src = "./" + entry.path;
    }));
    await Promise.all(batch);
    if (errors.length) throw new Error("Missing public artwork files: " + errors.slice(0,8).join(", "));
  }

  window.PROLOGUE_LAB = {
    ready: () => !!data.catalog,
    scope: LAB_SCOPE,
    getState: publicState,
    setScene,
    setSceneVersion,
    setPortrait,
    setSlots,
    setButtonMode,
    setButtonSkin,
    setInventoryStart,
    openItem,
    closeInspector,
    setLayers,
    nextScene: () => changeScene(1),
    previousScene: () => changeScene(-1)
  };

  (async function boot() {
    try {
      const responses = await Promise.all([
        "../../story/artwork.draft.json","./asset-index.json","./control-asset-manifest.json",
        "./layout-reference.json","./bitmap-fonts.json","./exposition-v03.json"
      ].map(url=>fetch(url,{cache:"no-cache"})));
      if (responses.some(r=>!r.ok)) throw new Error("Cannot read public artwork, layout or font metadata");
      [data.catalog,data.index,data.controls,data.layout,data.fonts,data.exposition] = await Promise.all(responses.map(r=>r.json()));
      if (data.exposition.schema !== "cyoa-exposition-v03-public-review-v1" ||
          data.exposition.scenes.length !== 4 ||
          data.exposition.ownerVisualApproval !== "approved" ||
          data.exposition.narrativePatchApplied !== false) throw new Error("Invalid Exposition V03 public-only manifest");
      for (const row of data.exposition.scenes) {
        const current = data.catalog.scenes[row.id];
        if (!current || current.status !== "integrated" || current.assetPath !== row.assetPath ||
            row.status !== "integrated" || row.humanFigureInCurrentArtwork !== false)
          throw new Error("Exposition artwork catalog mismatch: " + row.id);
      }
      if (data.layout.schema !== "cyoa-public-artwork-lab-layout-v1" || data.layout.inventory.slotCount!==6 || data.layout.inventory.pitch!==116 || data.layout.inventory.gap!==20) throw new Error("Incorrect six-slot layout baseline");
      if (data.controls.schema !== "cyoa-public-control-art-v1") throw new Error("Unknown approved control-art manifest");
      state.slots=data.layout.inventory.slotCount;
      state.buttonMode=data.layout.utility.show;
      await window.PUBLIC_PIXEL_TEXT.configure(data.fonts);
      applyLayout();
      if (data.index.schema !== "cyoa-public-prologue-review-assets-v1") throw new Error("Unrecognized public asset index");
      scopeRecords();
      if (data.scenes.length !== 8 || data.items.length !== 10) throw new Error("Expected eight scene entries and ten inventory items");
      for (const scene of data.scenes) {
        const item = data.catalog.scenes[scene];
        option($("sceneSelect"), scene, item.title + (item.status==="integrated" ? " [INTEGRATED]" : item.status==="reused" ? " [REUSED]" : " [REVIEW]"));
      }
      for (const p of PAIRINGS) option($("portraitSelect"),p.id,p.title);
      for (const item of data.items) {
        const rec = data.catalog.items[item];
        option($("itemSelect"),item,itemTitle(item)+(rec.slot.status==="integrated"?" [INTEGRATED]":rec.slot.status==="reused"?" [REUSED]":" [REVIEW]"));
      }
      bind();
      render();
      fitStage();
      $("loadStatus").textContent = "Loading " + (data.index.files.length + data.controls.files.length) + " visual assets…";
      await preload(data.index,data.controls);
      document.body.dataset.ready = "true";
      $("loadStatus").textContent = "Ready · Exposition V03 candidates + M2 reception · " + (data.index.files.length + data.controls.files.length) + " verified-source images · six-slot layout";
    } catch (error) {
      document.body.dataset.ready = "error";
      $("loadStatus").textContent = String(error.message || error);
      console.error(error);
    }
  })();
})();