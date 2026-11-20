// Regression QA for the public Prologue Artwork Lab as DEPLOYED: it builds the standalone site
// with the exact "Build standalone public site" step of .github/workflows/pages.yml, serves it
// under the Pages path prefix, and drives the lab in Chromium and Firefox. Catalogue fixtures
// (unrelated growth, missing/invalid scoped records) are injected over the network only; no
// repository file is modified.
//
//   node tools/prologue-art-lab/qa/qa-pages-site.mjs [--site <built _site>] [--out <screenshot dir>]
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import http from "node:http";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { chromium, firefox } from "playwright";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../..");
const arg = (flag) => (process.argv.includes(flag) ? process.argv[process.argv.indexOf(flag) + 1] : null);
const out = path.resolve(arg("--out") || fs.mkdtempSync(path.join(os.tmpdir(), "prologue-lab-pages-qa-")));
fs.mkdirSync(out, { recursive: true });

// 1. The site under test is the Pages artifact, built by pages.yml's own step (not a copy of it).
function buildSite() {
  const workflow = fs.readFileSync(path.join(root, ".github/workflows/pages.yml"), "utf8").split("\n");
  const at = workflow.findIndex((l) => /^\s*- name: Build standalone public site\s*$/.test(l));
  assert.ok(at >= 0, "pages.yml has a 'Build standalone public site' step");
  const runAt = at + 1;
  assert.match(workflow[runAt], /^\s*run: \|\s*$/, "that step is a literal run block");
  const indent = workflow[runAt + 1].match(/^\s*/)[0].length;
  const body = [];
  for (let i = runAt + 1; i < workflow.length; i++) {
    const line = workflow[i];
    if (line.trim() && line.match(/^\s*/)[0].length < indent) break;
    body.push(line.slice(indent));
  }
  const target = path.join(root, "_site");
  assert.ok(!fs.existsSync(target), "refusing to overwrite an existing _site; remove it or pass --site");
  execFileSync("bash", ["-e", "-c", body.join("\n")], { cwd: root, stdio: ["ignore", "inherit", "inherit"] });
  const site = fs.mkdtempSync(path.join(os.tmpdir(), "prologue-lab-site-"));
  fs.cpSync(target, site, { recursive: true });
  fs.rmSync(target, { recursive: true, force: true });
  return site;
}
const site = arg("--site") ? path.resolve(arg("--site")) : buildSite();
assert.ok(fs.existsSync(path.join(site, "tools/prologue-art-lab/index.html")), "built site contains the lab");
const catalog = JSON.parse(fs.readFileSync(path.join(site, "story/artwork.draft.json"), "utf8"));

// Serve exactly like GitHub Pages: project prefix, directory index, 404 otherwise.
const prefix = "/CYOA-storyboard/";
const types = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".json": "application/json", ".png": "image/png" };
const server = http.createServer((req, res) => {
  const url = new URL(req.url, "http://localhost");
  let name = decodeURIComponent(url.pathname);
  if (!name.startsWith(prefix)) { res.writeHead(404).end(); return; }
  let file = path.resolve(site, name.slice(prefix.length));
  if (file !== site && !file.startsWith(site + path.sep)) { res.writeHead(404).end(); return; }
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, "index.html");
  if (!fs.existsSync(file) || !fs.statSync(file).isFile()) { res.writeHead(404).end(); return; }
  res.writeHead(200, { "content-type": types[path.extname(file)] || "application/octet-stream", "cache-control": "no-store" });
  fs.createReadStream(file).pipe(res);
});
await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
const lab = "http://127.0.0.1:" + server.address().port + prefix + "tools/prologue-art-lab/";

const SCENES = ["workplace/applause_station", "workplace/corridor", "workplace/exit", "street/outside_workplace",
  "exposition/entrance", "exposition/property_intake", "exposition/reception", "exposition/facilities_corridor"];
const ITEMS = ["termination_notice", "timing_clicker", "desk_plant", "effects_box_full", "effects_box_empty",
  "red_stapler", "rubber_band_ball", "property_claim_ticket", "expo_examiner_badge", "wc_key"];
const clone = (x) => JSON.parse(JSON.stringify(x));

// Fixture 8: heavy unrelated growth, inserted BEFORE the scoped records so catalogue order cannot leak in.
function grownCatalog() {
  const c = clone(catalog);
  const scenes = {}, items = {};
  for (let i = 0; i < 40; i++) scenes["fixture_chapter/scene_" + i] = { title: "FIXTURE " + i, kind: "scene", status: ["not-started", "approved", "integrated"][i % 3], dimensions: "314x206", assetPath: null, notes: i % 4 ? "fixture" : "ARCHIVED / RETIRED / UNUSED fixture" };
  for (let i = 0; i < 25; i++) items["fixture_item_" + i] = { slot: { status: "not-started", assetPath: null, title: "FIXTURE ITEM " + i }, inspect: { status: "not-started", assetPath: null } };
  c.scenes = { ...scenes, ...c.scenes };
  c.items = { ...items, ...c.items };
  return c;
}
// Fixture 9: each must stop startup with a specific scope error.
const broken = [
  ["required scene removed", (c) => { delete c.scenes["workplace/exit"]; }, /scope invalid: .*missing scene workplace\/exit/],
  ["required item removed", (c) => { delete c.items.red_stapler; }, /scope invalid: .*missing item red_stapler/],
  ["inspector art points at an unpinned file", (c) => { c.items.wc_key.inspect.assetPath = "art/items/not_pinned.png"; }, /scope invalid: .*item wc_key inspector: Pinned Prologue source is missing/],
  ["scene artwork removed", (c) => { c.scenes["workplace/applause_station"].assetPath = null; }, /scope invalid: .*scene workplace\/applause_station has no artwork/],
  ["scene no longer selected", (c) => { c.scenes["workplace/corridor"].status = "not-started"; }, /scope invalid: .*scene workplace\/corridor is not selected artwork/],
  ["scene archived", (c) => { c.scenes["exposition/reception"].notes = "ARCHIVED / RETIRED / UNUSED fixture"; }, /scope invalid: .*scene exposition\/reception is archived/],
  ["portrait layer removed", (c) => { c.portraits["receptionist:default"].layers = c.portraits["receptionist:default"].layers.filter((l) => l.role !== "foreground"); }, /scope invalid: .*portrait receptionist:default has no foreground layer/],
];

const results = [];
async function suite(name, driver) {
  const browser = await driver.launch();
  let passed = 0;
  const check = (ok, label, detail) => {
    if (!ok) throw new Error(label + (detail === undefined ? "" : " " + JSON.stringify(detail).slice(0, 400)));
    passed++; console.log("pass [" + name + "] " + label);
  };
  async function open(fixture) {
    const page = await browser.newPage({ viewport: { width: 2640, height: 1500 }, deviceScaleFactor: 1 });
    const errors = [];
    page.on("pageerror", (e) => errors.push(String(e)));
    page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
    page.on("response", (r) => { if (r.status() >= 400) errors.push(r.status() + " " + r.url()); });
    if (fixture) await page.route("**/story/artwork.draft.json*", (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(fixture) }));
    await page.goto(lab, { waitUntil: "domcontentloaded", timeout: 45000 });
    await page.waitForFunction(() => document.body.dataset.ready === "true" || document.body.dataset.ready === "error", null, { timeout: 60000 });
    return { page, errors };
  }
  const state = (page) => page.evaluate(() => window.PROLOGUE_LAB.getState());
  const options = (page, id) => page.$$eval("#" + id + " option", (os) => os.map((o) => o.value));
  const settle = (page) => page.waitForFunction(() => !window.PROLOGUE_LAB.getState().inventoryMoving, null, { timeout: 3000 });
  try {
    // --- Real catalogue, built site ---
    const { page, errors } = await open(null);
    const status = await page.locator("#loadStatus").textContent();
    check(await page.evaluate(() => document.body.dataset.ready) === "true", "1 lab starts from the built Pages site: " + status);
    check(JSON.stringify(await page.evaluate(() => window.PROLOGUE_LAB.scope)) === JSON.stringify({ scenes: SCENES, items: ITEMS, portraits: ["termination_drone:slot_closed", "termination_drone:paper_extended", "receptionist:default"] }), "explicit lab scope exposed");
    check(JSON.stringify(await options(page, "sceneSelect")) === JSON.stringify(SCENES), "2 exactly the eight scoped scenes, in original order", await options(page, "sceneSelect"));
    check(JSON.stringify(await options(page, "itemSelect")) === JSON.stringify(ITEMS), "3 exactly the ten scoped items, in original order", await options(page, "itemSelect"));
    const strip = await page.$$eval(".inventory-slot", (bs) => bs.map((b) => b.dataset.item));
    check(JSON.stringify(strip) === JSON.stringify(ITEMS), "3 inventory strip holds exactly the ten scoped items", strip);
    check(Object.keys(catalog.scenes).length > 8 && Object.keys(catalog.items).length > 10, "real catalogue is larger than the scope (" + Object.keys(catalog.scenes).length + " scenes, " + Object.keys(catalog.items).length + " items)");

    // 4. Required images: every rendered src decodes; every scoped scene, slot and inspector at native size.
    const undecoded = await page.evaluate(() => Array.from(document.images).filter((i) => i.getAttribute("src") && (!i.complete || !i.naturalWidth)).map((i) => i.getAttribute("src")));
    check(undecoded.length === 0, "4 every rendered image decodes", undecoded);
    const slotSizes = await page.$$eval(".inventory-slot .item-image", async (is) => Promise.all(is.map(async (i) => { await i.decode(); return [i.naturalWidth, i.naturalHeight]; })));
    check(slotSizes.length === 10 && slotSizes.every((s) => s[0] === 96 && s[1] === 96), "4 ten 96x96 inventory icons", slotSizes);

    // 5. Scene navigation through the real controls, both directions and wrap-around.
    await page.locator("#actualPreview").click();
    const seen = [(await state(page)).scene];
    for (let i = 0; i < SCENES.length; i++) {
      await page.locator("#nextScene").click();
      await page.waitForFunction(() => { const i = document.querySelector("#sceneImage"); return i.complete && i.naturalWidth === 314 && i.naturalHeight === 206; });
      seen.push((await state(page)).scene);
    }
    check(JSON.stringify(seen) === JSON.stringify([...SCENES, SCENES[0]]), "5 Next visits all eight 314x206 scenes in order and wraps", seen);
    await page.locator("#prevScene").click();
    check((await state(page)).scene === SCENES[7], "5 Previous wraps to the last scoped scene");
    await page.locator("#cardNext").click();
    check((await state(page)).scene === SCENES[0], "5 in-frame NEXT choice card navigates");
    await page.selectOption("#sceneSelect", "exposition/property_intake");
    check((await state(page)).scene === "exposition/property_intake", "5 scene picker navigates");
    const outOfScope = await page.evaluate(() => { try { window.PROLOGUE_LAB.setScene("pavilion_reboot/urgency_stage"); return false; } catch (e) { return /Unknown scene/.test(String(e)); } });
    check(outOfScope, "5 unrelated catalogue scenes cannot be displayed");

    // 6. Inventory: six-slot window, spring scrolling by the stage arrows, inspection of every item.
    check((await state(page)).slots === 6 && await page.locator(".inventory-slot:visible").count() === 6, "6 historical six-slot window preserved");
    await page.locator("#stageNext").click(); await settle(page);
    check((await state(page)).inventoryStart === 1, "6 right stage arrow scrolls one item");
    for (let i = 0; i < 5; i++) { await page.locator("#stageNext").click(); await settle(page); }
    const end = await state(page);
    check(end.inventoryStart === 4 && end.items[5] === "wc_key", "6 scrolling stops at the last scoped item", end.items);
    await page.locator('.inventory-slot[data-item="wc_key"]').click();
    await page.waitForFunction(() => { const i = document.querySelector("#inspectionImage"); return i.complete && i.naturalWidth === 565 && i.naturalHeight === 451; });
    check((await state(page)).inspection === "wc_key" && await page.locator("#inspectionLayer").isVisible(), "6 clicking a slot opens its 565x451 inspector");
    await page.keyboard.press("Escape");
    check((await state(page)).inspection === null, "6 Escape closes the inspector");
    await page.locator("#stagePrev").click(); await settle(page);
    check((await state(page)).inventoryStart === 3, "6 left stage arrow scrolls back");
    const inspected = [];
    for (const id of ITEMS) {
      await page.selectOption("#itemSelect", id);
      await page.waitForFunction(() => { const i = document.querySelector("#inspectionImage"); return i.complete && i.naturalWidth === 565; });
      inspected.push((await state(page)).inspection);
    }
    check(JSON.stringify(inspected) === JSON.stringify(ITEMS), "6 all ten scoped items inspect");
    await page.locator("#closeInspector").click();
    await page.evaluate(() => window.PROLOGUE_LAB.setInventoryStart(0)); await settle(page);
    await page.locator("#stage").screenshot({ path: path.join(out, name + "_inventory_and_scene.png") });

    // 7. Portrait layers: separate 564x278 background + transparent foreground in one box, foreground on top.
    async function layers() {
      return page.evaluate(async () => {
        const bg = document.querySelector("#portraitBackground"), fg = document.querySelector("#portraitForeground");
        await Promise.all([bg.decode(), fg.decode()]);
        const box = (e) => { const r = e.getBoundingClientRect(); return [r.left, r.top, r.width, r.height].map(Math.round); };
        const c = document.createElement("canvas"); c.width = fg.naturalWidth; c.height = fg.naturalHeight;
        const g = c.getContext("2d"); g.drawImage(fg, 0, 0); const a = g.getImageData(0, 0, c.width, c.height).data;
        let clear = 0, solid = 0; for (let i = 3; i < a.length; i += 4) a[i] === 0 ? clear++ : a[i] === 255 && solid++;
        const r = fg.getBoundingClientRect(), top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
        return { bg: [bg.naturalWidth, bg.naturalHeight, bg.hidden], fg: [fg.naturalWidth, fg.naturalHeight, fg.hidden], same: JSON.stringify(box(bg)) === JSON.stringify(box(fg)), clear, solid,
          fgAbove: !!(bg.compareDocumentPosition(fg) & Node.DOCUMENT_POSITION_FOLLOWING), topIsLayer: top === fg || top === bg || fg.parentElement.contains(top) };
      });
    }
    for (const [scene, pose] of [["workplace/corridor", "drone-closed"], ["exposition/reception", "receptionist"]]) {
      await page.selectOption("#sceneSelect", scene);
      const s = await state(page), L = await layers();
      check(s.activePortrait === pose && s.paired && L.bg[0] === 564 && L.bg[1] === 278 && L.fg[0] === 564 && L.fg[1] === 278 && !L.bg[2] && !L.fg[2] && L.same && L.fgAbove && L.clear > 0 && L.solid > 0,
        "7 " + scene + ": " + pose + " foreground composited over its own background (same 564x278 box, transparent surround)", L);
      await page.locator("#stage").screenshot({ path: path.join(out, name + "_portrait_" + pose + ".png") });
    }
    await page.selectOption("#sceneSelect", "workplace/corridor");
    await page.selectOption("#portraitSelect", "drone-paper");
    const paper = await page.locator("#portraitForeground").getAttribute("src");
    check(/drone_paper_extended\.png$/.test(paper) && (await state(page)).activePortrait === "drone-paper", "7 alternate drone pose swaps only the foreground");
    await page.locator("#showBackground").uncheck();
    check(await page.locator("#portraitBackground").evaluate((e) => e.hidden) && !(await page.locator("#portraitForeground").evaluate((e) => e.hidden)), "7 background layer toggles independently");
    await page.locator("#showBackground").check();
    check(errors.length === 0, "1 no console, page or HTTP errors", errors);
    await page.close();

    // 8. Unrelated catalogue growth cannot stop startup or leak into the lab.
    const grown = await open(grownCatalog());
    check(await grown.page.evaluate(() => document.body.dataset.ready) === "true", "8 starts with 40 extra scenes (incl. archived/pending) and 25 extra items prepended");
    check(JSON.stringify(await options(grown.page, "sceneSelect")) === JSON.stringify(SCENES) && JSON.stringify(await options(grown.page, "itemSelect")) === JSON.stringify(ITEMS), "8 still exactly the scoped scenes and items, original order");
    check(grown.errors.length === 0, "8 no errors with the grown catalogue", grown.errors);
    await grown.page.close();

    // 9. Missing or invalid scoped records fail loudly with the specific record named.
    for (const [label, mutate, expected] of broken) {
      const fixture = clone(catalog); mutate(fixture);
      const b = await open(fixture);
      const st = await b.page.evaluate(() => ({ ready: document.body.dataset.ready, status: document.getElementById("loadStatus").textContent, scenes: document.querySelectorAll("#sceneSelect option").length }));
      check(st.ready === "error" && expected.test(st.status) && st.scenes === 0, "9 " + label + " -> startup refused: " + st.status, st);
      await b.page.close();
    }
    results.push({ name, passed, failed: 0 });
  } catch (e) {
    console.error("FAIL [" + name + "] " + (e.stack || e));
    results.push({ name, passed, failed: 1, error: String(e.message || e) });
  } finally { await browser.close(); }
}

try { await suite("chromium", chromium); await suite("firefox", firefox); }
finally {
  await new Promise((resolve) => server.close(resolve));
  const total = results.reduce((n, x) => n + x.passed, 0), failed = results.reduce((n, x) => n + x.failed, 0);
  fs.writeFileSync(path.join(out, "qa-pages-site-results.json"), JSON.stringify({ schema: "cyoa-public-prologue-pages-site-qa-v1", passed: total, failed, results }, null, 2) + "\n");
  console.log("Prologue Artwork Lab (built Pages site) QA: " + total + " passed; " + failed + " failures; screenshots + results in " + out);
  if (failed || results.length !== 2) process.exitCode = 1;
}
