// Public-safe visual review only. This does NOT import the private gameplay engine.
// All visible M2 chrome and art is copied byte-identically; the scene, portrait,
// inventory and inspector positions follow the approved M2 art geometry.
(() => {
  "use strict";

  const $ = id => document.getElementById(id);
  const stage = $("stage");
  const viewport = $("previewViewport");
  const wrap = $("previewWrap");
  const data = { catalog: null, index: null, controls: null, layout: null, fonts: null, scenes: [], items: [], urls: new Map() };
  const state = {
    scene: "workplace/applause_station",
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
    selectedItem: "termination_notice",
    inspection: null,
    fit: true
  };

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
    if (fallback) return "assets/approved/" + fallback;
    if (!record || !record.assetPath) return null;
    return "assets/" + (record.status === "generated" ? "draft/" : "approved/") + safe(record.assetPath);
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
  function setScene(id) {
    if (!data.catalog.scenes[id]) throw new Error("Unknown scene " + id);
    state.scene = id;
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
  function setInventoryStart(n) {
    state.inventoryStart = Math.min(Math.max(0, Math.round(n)), Math.max(0, data.items.length - state.slots));
    renderInventory();
    renderControls();
  }
  function openItem(id) {
    if (!data.catalog.items[id]) throw new Error("Unknown item " + id);
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
    setImg($("sceneImage"), asset(scene));
    $("sceneAperture").setAttribute("aria-label", scene.title + " — 314 by 206 scene at 4 times native scale");
    $("sceneLabel").textContent = scene.title;
    $("sourceLabel").textContent = scene.status === "reused"
      ? "Approved M2 reception comparison · original art"
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

  function renderInventory() {
    const strip = $("inventoryStrip");
    strip.replaceChildren();
    const config = data.layout.inventory;
    const at = config.slotLayouts[String(config.slotCount)];
    const baseX = at.x;
    const slotArt = "assets/approved/art/ui/sprites/inventory/inventory_slot.png";
    for (let i = 0; i < state.slots; ++i) {
      const itemId = data.items[state.inventoryStart + i];
      const button = document.createElement("button");
      button.type = "button";
      button.className = "inventory-slot";
      button.style.left = (baseX + config.pitch * i) + "px";
      button.style.top = at.y + "px";
      button.style.width = config.slotSize[0] + "px";
      button.style.height = config.slotSize[1] + "px";
      button.dataset.item = itemId || "";
      button.setAttribute("aria-label", itemId ? "Inspect " + itemTitle(itemId) : "Empty inventory slot");
      if (!itemId) button.disabled = true;
      const background = document.createElement("img");
      background.src = slotArt;
      background.alt = "";
      button.appendChild(background);
      if (itemId) {
        const image = document.createElement("img");
        image.className = "item-image";
        image.src = asset(data.catalog.items[itemId].slot);
        image.alt = "";
        button.appendChild(image);
        button.addEventListener("click", () => openItem(itemId));
      }
      strip.appendChild(button);
    }
    strip.setAttribute("aria-label", state.slots + "-slot owner layout displaying art for " + state.slots + " items");
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
    getState: publicState,
    setScene,
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
        "./layout-reference.json","./bitmap-fonts.json"
      ].map(url=>fetch(url,{cache:"no-cache"})));
      if (responses.some(r=>!r.ok)) throw new Error("Cannot read public artwork, layout or font metadata");
      [data.catalog,data.index,data.controls,data.layout,data.fonts] = await Promise.all(responses.map(r=>r.json()));
      if (data.layout.schema !== "cyoa-public-artwork-lab-layout-v1" || data.layout.inventory.slotCount!==6 || data.layout.inventory.pitch!==116 || data.layout.inventory.gap!==20) throw new Error("Incorrect six-slot layout baseline");
      if (data.controls.schema !== "cyoa-public-control-art-v1") throw new Error("Unknown approved control-art manifest");
      state.slots=data.layout.inventory.slotCount;
      state.buttonMode=data.layout.utility.show;
      await window.PUBLIC_PIXEL_TEXT.configure(data.fonts);
      applyLayout();
      if (data.index.schema !== "cyoa-public-prologue-review-assets-v1") throw new Error("Unrecognized public asset index");
      data.scenes = Object.keys(data.catalog.scenes);
      data.items = Object.keys(data.catalog.items);
      if (data.scenes.length !== 8 || data.items.length !== 10) throw new Error("Expected eight scene entries and ten inventory items");
      for (const scene of data.scenes) {
        const item = data.catalog.scenes[scene];
        option($("sceneSelect"), scene, item.title + (item.status==="generated" ? " [DRAFT]" : " [M2]"));
      }
      for (const p of PAIRINGS) option($("portraitSelect"),p.id,p.title);
      for (const item of data.items) {
        const rec = data.catalog.items[item];
        option($("itemSelect"),item,itemTitle(item)+(rec.slot.status==="generated"?" [DRAFT]":" [M2]"));
      }
      bind();
      render();
      fitStage();
      $("loadStatus").textContent = "Loading " + (data.index.files.length + data.controls.files.length) + " visual assets…";
      await preload(data.index,data.controls);
      document.body.dataset.ready = "true";
      $("loadStatus").textContent = "Ready · " + (data.index.files.length + data.controls.files.length) + " verified-source images loaded · six-slot layout";
    } catch (error) {
      document.body.dataset.ready = "error";
      $("loadStatus").textContent = String(error.message || error);
      console.error(error);
    }
  })();
})();