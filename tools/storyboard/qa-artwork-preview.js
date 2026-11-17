#!/usr/bin/env node
// Real-browser check of the selected-artwork previews (docs/105), Chromium + Firefox, over HTTP from
// the repository root.
//   NODE_PATH="$(npm root -g)" node tools/storyboard/qa-artwork-preview.js [--out <dir>]
// Proves: every registered preview is served byte-exact (SHA-256 in the page) at its native size;
// scene states composite over / replace their scene; NPC foregrounds sit on their portrait
// backgrounds with identical boxes; the House shows complete opaque views; Focus A pages, item slot
// + inspect pairs, layered portraits and death screens render; node cards show their art; the zoom
// dialog draws integer scales; no selected record reads as unfinished. Writes nothing to story/.
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const http = require('http');
const ROOT = path.resolve(__dirname, '../..');
let playwright;
try { playwright = require('playwright'); } catch (e) { console.log('Playwright is not installed here: run with NODE_PATH="$(npm root -g)"'); process.exit(2); }
const outArg = process.argv.indexOf('--out');
const OUT = outArg !== -1 ? path.resolve(process.argv[outArg + 1]) : fs.mkdtempSync(path.join(os.tmpdir(), 'cyoa-artwork-preview-qa-'));
fs.mkdirSync(OUT, { recursive: true });
const PREVIEW = JSON.parse(fs.readFileSync(path.join(ROOT, 'story/artwork-preview.json'), 'utf8'));

const results = [];
function check(browser, name, ok, detail) {
  results.push({ browser, name, ok: !!ok });
  if (!ok) console.log('FAIL [' + browser + '] ' + name, detail === undefined ? '' : JSON.stringify(detail).slice(0, 500));
}
function serve() {
  const types = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png', '.css': 'text/css' };
  const server = http.createServer((req, res) => {
    const file = path.normalize(path.join(ROOT, decodeURIComponent(req.url.split('?')[0])));
    if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404).end(); return; }
    const body = fs.readFileSync(file);
    res.writeHead(200, { 'content-type': types[path.extname(file)] || 'application/octet-stream', 'content-length': body.length, 'cache-control': 'no-store' });
    res.end(body);
  });
  return new Promise((r) => server.listen(0, '127.0.0.1', () => r(server)));
}

async function run(name, base) {
  const b = name, browser = await playwright[name].launch();
  const page = await browser.newPage({ viewport: { width: 1500, height: 1000 } });
  const errors = [];
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', (e) => errors.push(String(e)));
  await page.goto(base + '/tools/storyboard/index.html');
  await page.waitForFunction(() => /^Loaded \d+ nodes/.test(document.getElementById('status').textContent));

  // 1. Every registered preview: served bytes = recorded SHA-256, decoded size = recorded native size.
  const served = await page.evaluate(async (images) => {
    const hex = (buf) => Array.from(new Uint8Array(buf)).map((x) => x.toString(16).padStart(2, '0')).join('');
    const out = [];
    for (const [key, p] of Object.entries(images)) {
      const url = new URL('../../' + p.file, location.href).href;
      const r = await fetch(url, { cache: 'no-store' });
      const sha = r.ok ? hex(await crypto.subtle.digest('SHA-256', await r.arrayBuffer())) : null;
      const size = await new Promise((res) => { const i = new Image(); i.onload = () => res([i.naturalWidth, i.naturalHeight]); i.onerror = () => res(null); i.src = url; });
      out.push({ key, ok: r.ok, shaOk: sha === p.sha256, sizeOk: !!size && size[0] === p.size[0] && size[1] === p.size[1] });
    }
    return out;
  }, PREVIEW.images);
  const bad = served.filter((s) => !s.ok || !s.shaOk || !s.sizeOk);
  check(b, 'all ' + served.length + ' previews served byte-exact at native size', served.length >= 8 && !bad.length, bad.slice(0, 5));

  const openList = async (filter) => {
    await page.click('#showArtwork');
    await page.click('#details .art-filter button:text-is("' + (filter || 'All') + '")');
  };
  const openArt = async (title, filter) => {
    await openList(filter);
    await page.locator('#details button.art-brief', { hasText: title }).first().click();
    await page.waitForFunction(() => Array.from(document.querySelectorAll('#details .px-stack img')).every((i) => i.complete));
  };
  const figures = () => page.evaluate(() => Array.from(document.querySelectorAll('#details .art-preview figure')).map((f) => {
    const box = f.querySelector('.px-stack'), r = box.getBoundingClientRect();
    return { caption: f.querySelector('figcaption').textContent, w: Math.round(r.width), h: Math.round(r.height),
      imgs: Array.from(box.querySelectorAll('img')).map((i) => { const q = i.getBoundingClientRect(); return { src: i.src.split('/assets/selected/')[1], nw: i.naturalWidth, nh: i.naturalHeight, x: Math.round(q.left), y: Math.round(q.top), w: Math.round(q.width), h: Math.round(q.height) }; }) };
  }));
  const sameBox = (imgs) => imgs.every((i) => i.x === imgs[0].x && i.y === imgs[0].y && i.w === imgs[0].w && i.h === imgs[0].h);

  // 2. Library overview + filters.
  await openList();
  const overview = await page.textContent('#details');
  const n = Number((overview.match(/(\d+) selected images viewable here/) || [])[1]);
  check(b, 'library reports the viewable selected images', n === served.length, overview.slice(0, 300));
  await openList('Selected');
  const selectedButtons = await page.$$eval('#details button.art-brief', (bs) => bs.map((x) => ({ thumb: !!x.querySelector('img.thumb'), t: x.textContent })));
  check(b, 'Selected filter: every selected record shows a thumbnail', selectedButtons.length > 0 && selectedButtons.every((x) => x.thumb), selectedButtons.filter((x) => !x.thumb).slice(0, 3));
  await openList('Not selected yet');
  const pending = await page.$$eval('#details button.art-brief', (bs) => bs.map((x) => x.textContent));
  check(b, 'Not-selected filter lists only unselected records', pending.length > 50 && pending.every((t) => !/· (approved|integrated|reused)$/.test(t)), pending.slice(0, 3));

  // 3. Main scene at native 1x (314 fits the pane).
  await openArt('HOUSE OF TOMORROW — ARRIVAL');
  let f = await figures();
  check(b, 'scene shown at native 314x206, 1 image', f.length === 1 && f[0].w === 314 && f[0].h === 206 && f[0].imgs[0].nw === 314, f);
  check(b, 'scene provenance names the source commit', /Selected source: InterstellarHarvest\/CYOA/.test(await page.textContent('#details .prov')));
  await page.screenshot({ path: path.join(OUT, b + '_1_scene.png') });

  // 4. Scene states: overlay over its base scene, replacement alone.
  await openArt('HOUSE OF TOMORROW — STORAGE');
  const stateButtons = await page.$$eval('#details .art-preview button.art-brief', (bs) => bs.map((x) => x.textContent));
  check(b, 'storage lists its 4 conditional states with conditions', stateButtons.length === 4 && stateButtons.every((t) => /overlay · integrated · shows when/.test(t)), stateButtons);
  await page.locator('#details .art-preview button.art-brief', { hasText: 'DESK PLANT IN DRAWER' }).click();
  await page.waitForFunction(() => Array.from(document.querySelectorAll('#details .px-stack img')).every((i) => i.complete));
  f = await figures();
  check(b, 'overlay drawn over its scene (base first, same box), then alone on a checkerboard',
    f.length === 2 && f[0].imgs.length === 2 && /storage\.png$/.test(f[0].imgs[0].src) && /stored_desk_plant/.test(f[0].imgs[1].src) && sameBox(f[0].imgs) && f[1].imgs.length === 1, f);
  await page.screenshot({ path: path.join(OUT, b + '_2_state_overlay.png') });
  await openArt('HOUSE OF TOMORROW — PORTRAIT GALLERY');
  await page.locator('#details .art-preview button.art-brief', { hasText: 'ALBUM TEMPORARILY REMOVED' }).click();
  f = await figures();
  check(b, 'replace state shown alone as a full scene', f.length === 1 && f[0].imgs.length === 1 && /album_removed/.test(f[0].imgs[0].src) && /Replacement/.test(f[0].caption), f);

  // 5. Layered NPC: background + transparent foreground, identical boxes, never a resized scene.
  await openArt('GROUNDSKEEPER MACHINE - IDLE');
  f = await figures();
  check(b, 'groundskeeper: portrait background + transparent foreground composite (564x278, same box)',
    f.length === 2 && f[0].imgs.length === 2 && /groundskeeper\/portraitBackground/.test(f[0].imgs[0].src) && f[0].imgs.every((i) => i.nw === 564 && i.nh === 278) && sameBox(f[0].imgs), f);
  await page.screenshot({ path: path.join(OUT, b + '_3_npc_composite.png') });
  await openArt('TERMINATION DRONE — CLOSED SLOT');
  f = await figures();
  check(b, 'drone foreground composited on the corridor portrait background', f[0] && f[0].imgs.length === 2 && /corridor_background/.test(f[0].imgs[0].src) && sameBox(f[0].imgs), f);
  await openArt('RECEPTIONIST — APPROVED M2 LAYERS');
  f = await figures();
  check(b, 'reused layered receptionist: composite + each layer', f.length === 3 && f[0].imgs.length === 2 && sameBox(f[0].imgs), f);

  // 6. Opaque-complete House views (no foreground layering).
  await openArt('HOUSE INTERCOM — COMPLETE OPAQUE CONVERSATION VIEWS');
  f = await figures();
  check(b, 'House: two complete opaque views, one image each', f.length === 2 && f.every((x) => x.imgs.length === 1 && x.imgs[0].nw === 564) && /opaque-complete/i.test(await page.textContent('#details')), f);

  // 7. Focus A pages.
  await openArt('FAMILY ALBUM — MULTIPAGE INSPECTION');
  f = await figures();
  check(b, 'album: three Focus A pages in order', f.length === 3 && f.every((x, i) => new RegExp('album_page_' + (i + 1)).test(x.imgs[0].src) && /^Page /.test(x.caption)), f);

  // 8. Death screen.
  await openArt('PERMANENTLY SATISFIED.', 'All');
  f = await figures();
  check(b, 'Rest Assured death vignette shown (314x206)', f.length === 1 && f[0].imgs[0].nw === 314 && /Shown when/.test(await page.textContent('#details')), f);

  // 9. Approved-only (not integrated) Chapter 2 art reads as selected, not unfinished.
  await openArt('FORMAL ENTRANCE', 'Approved');
  const ch2 = await page.textContent('#details');
  check(b, 'approved Biology Park art is visible and explicitly needs no regeneration', /Selected and approved/.test(ch2) && !/Not generated/.test(ch2) && (await figures()).length === 1, ch2.slice(0, 400));

  // 10. Items: slot (transparent, checkerboard) + inspect.
  await page.click('#showItems');
  await page.locator('#details button.item-button', { hasText: 'COMPLIMENTARY FAMILY PORTRAIT' }).click();
  await page.waitForFunction(() => Array.from(document.querySelectorAll('#details .item-art img')).every((i) => i.complete));
  const item = await page.$$eval('#details .item-art .px-stack', (xs) => xs.map((x) => ({ checker: x.classList.contains('checker'), w: Math.round(x.getBoundingClientRect().width), nw: x.querySelector('img').naturalWidth, nh: x.querySelector('img').naturalHeight })));
  check(b, 'item: 96x96 slot at 2x on a checkerboard beside the 565x451 inspect view', item.length === 2 && item[0].checker && item[0].w === 192 && item[0].nw === 96 && item[1].nw === 565 && item[1].nh === 451, item);
  await page.screenshot({ path: path.join(OUT, b + '_4_item.png') });

  // 11. Node inspector: art references carry thumbnails; conditional states appear on their node.
  await page.selectOption('#chapterSelect', '1');
  await page.waitForFunction(() => /^Loaded 36 nodes/.test(document.getElementById('status').textContent));
  await page.evaluate(() => { const n = Array.from(document.querySelectorAll('#nodes .node')).find((c) => c.firstChild.textContent === 'plant_adoption'); n.click(); });
  const refs = await page.$$eval('#details button.art-brief', (bs) => bs.map((x) => ({ t: x.textContent, thumb: !!x.querySelector('img.thumb') })));
  check(b, 'node plant_adoption shows its scene + STATE pedestal overlay with thumbnails', refs.some((r) => /^STATE · /.test(r.t) && r.thumb) && refs.some((r) => /HOUSE OF TOMORROW — FOYER/.test(r.t) && r.thumb), refs);
  await page.evaluate(() => { const n = Array.from(document.querySelectorAll('#nodes .node')).find((c) => c.firstChild.textContent === 'exit_chair_fatal'); n.click(); });
  const death = await page.$$eval('#details button.art-brief', (bs) => bs.map((x) => x.textContent));
  check(b, 'fatal chair ending links its approved death screen', death.some((t) => /PERMANENTLY SATISFIED/.test(t)), death);

  // 12. Zoom dialog: integer scales of native pixels.
  await openArt('HOUSE OF TOMORROW — ARRIVAL');
  await page.click('#details .px-stack');
  await page.click('#artZoom [data-scale="2"]');
  const z2 = await page.$eval('#zoomBody .px-stack', (x) => [Math.round(x.getBoundingClientRect().width), Math.round(x.getBoundingClientRect().height)]);
  await page.click('#artZoom [data-scale="4"]');
  const z4 = await page.$eval('#zoomBody .px-stack', (x) => Math.round(x.getBoundingClientRect().width));
  check(b, 'zoom draws 2x = 628x412 and 4x = 1256', z2[0] === 628 && z2[1] === 412 && z4 === 1256, { z2, z4 });
  await page.screenshot({ path: path.join(OUT, b + '_5_zoom.png') });
  await page.click('#zoomClose');
  check(b, 'zoom closes', !(await page.$eval('#artZoom', (d) => d.open)));

  // 13. The Prologue Artwork Lab is still published next to the viewer.
  const lab = await page.evaluate(async () => (await fetch(new URL('../prologue-art-lab/index.html', location.href))).status);
  check(b, 'Prologue Artwork Lab still served', lab === 200, lab);
  check(b, 'no console errors', !errors.length, errors);
  await browser.close();
}

(async () => {
  const server = await serve();
  const base = 'http://127.0.0.1:' + server.address().port;
  try { for (const name of ['chromium', 'firefox']) await run(name, base); } finally { server.close(); }
  const failed = results.filter((r) => !r.ok);
  fs.writeFileSync(path.join(OUT, 'results.json'), JSON.stringify({ passed: results.length - failed.length, total: results.length, results }, null, 1));
  console.log((failed.length ? 'FAIL ' : 'PASS ') + (results.length - failed.length) + '/' + results.length + ' (screenshots: ' + OUT + ')');
  process.exitCode = failed.length ? 1 : 0;
})();
