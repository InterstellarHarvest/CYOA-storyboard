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

// The artwork library's rows, derived from the committed catalogue with the viewer's own enumeration
// (tools/storyboard/index.html showArtwork: records, portrait backgrounds, scene states / views / pages,
// item variants; key = artKey) and its retirement rule (retiredArt) and filters.
const CATALOG = JSON.parse(fs.readFileSync(path.join(ROOT, 'story/artwork.draft.json'), 'utf8'));
const SELECTED = ['approved', 'integrated', 'reused'];
const isRetired = (r) => /^ARCHIVED \/ RETIRED \/ UNUSED\b/.test((r && r.notes) || '');
const CATALOG_REFS = [];
for (const group of ['scenes', 'portraits', 'focus', 'deathScreens']) {
  for (const [id, record] of Object.entries(CATALOG[group] || {})) {
    CATALOG_REFS.push({ key: group + '/' + id, record });
    if (group === 'scenes' && record.portraitBackground) CATALOG_REFS.push({ key: group + '/' + id + '/portraitBackground', record: record.portraitBackground });
    if (group === 'scenes') (record.states || []).forEach((s) => CATALOG_REFS.push({ key: group + '/' + id + '/states:' + s.id, record: s }));
    if (group === 'portraits') Object.entries(record.views || {}).forEach(([s, v]) => CATALOG_REFS.push({ key: group + '/' + id + '/views:' + s, record: v }));
    if (group === 'focus') (record.pages || []).forEach((p, i) => CATALOG_REFS.push({ key: group + '/' + id + '/pages:' + (i + 1), record: p }));
  }
}
for (const [id, variants] of Object.entries(CATALOG.items || {})) for (const [variant, record] of Object.entries(variants)) CATALOG_REFS.push({ key: 'items/' + id + '/' + variant, record });
const statusOf = (r) => r.status || 'not-started';
const FILTER_RULES = {
  Selected: (x) => !isRetired(x.record) && SELECTED.includes(statusOf(x.record)),
  Integrated: (x) => !isRetired(x.record) && ['integrated', 'reused'].includes(statusOf(x.record)),
  Approved: (x) => !isRetired(x.record) && statusOf(x.record) === 'approved',
  'Active pending': (x) => !isRetired(x.record) && !SELECTED.includes(statusOf(x.record)),
  Archived: (x) => isRetired(x.record),
};
// Preview keys (register format "scenes:id#portraitBackground") in the viewer's key format. A selected
// container (layered portrait, complete views, multipage Focus) is previewed through its children.
const PREVIEW_KEYS = Object.keys(PREVIEW.images).map((k) => k.replace(':', '/').replace('#', '/'));
// docs/137 C1/C2: approved no-image records show a NO IMAGE tag instead of a thumbnail and have no preview.
const NO_IMAGE_KEYS = new Set(CATALOG_REFS.filter((x) => ['text-led', 'voice-only'].includes(x.record && x.record.format)).map((x) => x.key));
const SELECTED_PREVIEWED = new Set(CATALOG_REFS.map((x) => x.key).filter((k) => PREVIEW_KEYS.includes(k) || PREVIEW_KEYS.some((p) => p.startsWith(k + '/'))));

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
  const selectedButtons = await page.$$eval('#details button.art-brief', (bs) => bs.map((x) => ({ thumb: !!x.querySelector('img.thumb'), noImage: !!x.querySelector('.no-image-tag'), key: (x.querySelector('.art-meta') || {}).textContent.split(' · ')[0], t: x.textContent })));
  check(b, 'Selected filter: every selected image record shows a thumbnail', selectedButtons.length > 0 && selectedButtons.every((x) => x.thumb || (x.noImage && NO_IMAGE_KEYS.has(x.key))), selectedButtons.filter((x) => !x.thumb && !x.noImage).slice(0, 3));
  check(b, 'Selected filter: the approved no-image records (docs/137) show a NO IMAGE tag and no thumbnail', selectedButtons.filter((x) => x.noImage).map((x) => x.key).sort().join() === [...NO_IMAGE_KEYS].sort().join() && selectedButtons.every((x) => !(x.noImage && x.thumb)), selectedButtons.filter((x) => x.noImage).map((x) => x.key));
  // Filter matrix. Since the Chapter 3 reboot (2a1022b) the library separates ACTIVE records from RETIRED
  // historical ones ("Archived"; the "Not selected yet" filter became "Active pending"). Every filter must list
  // exactly the records the committed catalogue predicts, and the five sets must partition consistently.
  const rows = async (filter) => { await openList(filter); return page.$$eval('#details button.art-brief .art-meta', (ms) => ms.map((m) => m.textContent)); };
  const keyOf = (meta) => meta.split(' · ')[0];
  const expected = {};
  for (const [filter, keep] of Object.entries(FILTER_RULES)) expected[filter] = CATALOG_REFS.filter(keep).map((r) => r.key).sort();
  const seen = {};
  for (const filter of Object.keys(FILTER_RULES)) {
    const metas = await rows(filter);
    seen[filter] = metas.map(keyOf).sort();
    const exact = JSON.stringify(seen[filter]) === JSON.stringify(expected[filter]);
    const statusOk = filter === 'Archived' ? metas.every((m) => /· ARCHIVED · DO NOT GENERATE$/.test(m))
      : filter === 'Active pending' ? metas.every((m) => !/· (approved|integrated|reused|ARCHIVED · DO NOT GENERATE)$/.test(m))
      : filter === 'Approved' ? metas.every((m) => /· approved$/.test(m))
      : filter === 'Integrated' ? metas.every((m) => /· (integrated|reused)$/.test(m))
      : metas.every((m) => /· (approved|integrated|reused)$/.test(m));
    check(b, filter + ' filter lists exactly the ' + expected[filter].length + ' catalogue records it should, with matching status labels', exact && statusOk && (filter !== 'Archived' || seen[filter].length > 0),
      { extra: seen[filter].filter((k) => !expected[filter].includes(k)).slice(0, 3), missing: expected[filter].filter((k) => !seen[filter].includes(k)).slice(0, 3), n: seen[filter].length });
  }
  const union = (...fs) => [...new Set(fs.flatMap((f) => seen[f]))].sort();
  const allKeys = (await rows('All')).map(keyOf).sort();
  check(b, 'Selected + Active pending + Archived partition All; Integrated + Approved = Selected',
    JSON.stringify(union('Selected', 'Active pending', 'Archived')) === JSON.stringify(allKeys) && seen.Selected.length + seen['Active pending'].length + seen.Archived.length === allKeys.length
    && JSON.stringify(union('Integrated', 'Approved')) === JSON.stringify(seen.Selected) && seen.Integrated.length + seen.Approved.length === seen.Selected.length,
    { all: allKeys.length, selected: seen.Selected.length, pending: seen['Active pending'].length, archived: seen.Archived.length });
  check(b, 'every Selected image record has a byte-checked preview', seen.Selected.every((k) => SELECTED_PREVIEWED.has(k) || NO_IMAGE_KEYS.has(k)), seen.Selected.filter((k) => !SELECTED_PREVIEWED.has(k) && !NO_IMAGE_KEYS.has(k)).slice(0, 3));

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
    f.length === 2 && f[0].imgs.length === 2 && /groundskeeper\/portraitBackground|portraits\/groundskeeper\/groundskeeper_background\.png/.test(f[0].imgs[0].src) && f[0].imgs.every((i) => i.nw === 564 && i.nh === 278) && sameBox(f[0].imgs), f);
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
  // Every SELECTED House view is shown (foyer + gallery, and since Batch B lounge + dining: public docs/107 section 9).
  const houseViews = Object.entries(JSON.parse(fs.readFileSync(path.join(ROOT, 'story/artwork.draft.json'), 'utf8')).portraits['house:idle'].views)
    .filter(([, v]) => ['approved', 'integrated', 'reused'].includes(v.status)).map(([k]) => k).sort();
  check(b, 'House: ' + houseViews.length + ' complete opaque views (' + houseViews.map((k) => k.split('/')[1]).join(', ') + '), one image each',
    houseViews.length === 4 && f.length === houseViews.length && houseViews.every((k) => f.some((x) => x.caption === 'Complete opaque view — ' + k))
    && f.every((x) => x.imgs.length === 1 && x.imgs[0].nw === 564) && /opaque-complete/i.test(await page.textContent('#details')), f.map((x) => x.caption));

  // 7. Focus A pages.
  await openArt('FAMILY ALBUM — MULTIPAGE INSPECTION');
  f = await figures();
  check(b, 'album: three Focus A pages in order', f.length === 3 && f.every((x, i) => new RegExp('album_page_' + (i + 1)).test(x.imgs[0].src) && /^Page /.test(x.caption)), f);

  // 8. Death screen.
  await openArt('PERMANENTLY SATISFIED.', 'All');
  f = await figures();
  check(b, 'Rest Assured death vignette shown (314x206), one shared record for all three causes', f.length === 1 && f[0].imgs[0].nw === 314 && /deathScreens\/house_of_tomorrow\/rest_assured /.test(await page.textContent('#details')), f);

  // 9. Selected Chapter 2 art reads as selected, never unfinished: before integration it says so explicitly, and once
  // Gameplay PMO assigns its production path (docs/105) the viewer names that path; integrated art stays under Selected.
  await openArt('FORMAL ENTRANCE', 'Selected');
  const ch2 = await page.textContent('#details');
  check(b, 'selected Biology Park art is visible and needs no regeneration (approved, or its production path)', /Selected and approved|art\/scenes\/biology_park\/formal_entrance\.png/.test(ch2) && !/Not generated/.test(ch2) && (await figures()).length === 1, ch2.slice(0, 400));

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
  await page.waitForFunction(() => Array.from(document.querySelectorAll('#details .death-preview img')).every((i) => i.complete));
  const popup = await page.$$eval('#details .death-preview img', (xs) => xs.map((i) => [i.naturalWidth, i.naturalHeight]));
  check(b, 'the fatal node\'s death-popup box shows the actual selected 314x206 art (not "preview pending")', popup.length === 1 && popup[0][0] === 314 && popup[0][1] === 206
    && !/PREVIEW PENDING/.test(await page.textContent('#details .death-preview')), popup);
  await page.screenshot({ path: path.join(OUT, b + '_6_death_popup.png') });

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
