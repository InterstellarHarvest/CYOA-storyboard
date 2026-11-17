#!/usr/bin/env node
// Real-browser check of the storyboard's chapter navigation (Chromium + Firefox), over HTTP from
// the repository root, with real mouse drags and a real file download/upload.
//   NODE_PATH="$(npm root -g)" node tools/storyboard/qa-browser.js
// Sequence: move Prologue nodes -> switch to Chapter 1 -> move its node -> switch back -> Export
// Layout -> fresh browser profile -> Import Layout -> both arrangements survive. Writes nothing to
// story/; screenshots go to the OS temp folder.
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const http = require('http');
const ROOT = path.resolve(__dirname, '../..');
let playwright;
try { playwright = require('playwright'); } catch (e) { console.log('Playwright is not installed here: run with NODE_PATH="$(npm root -g)"'); process.exit(2); }
const OUT = fs.mkdtempSync(path.join(os.tmpdir(), 'cyoa-storyboard-qa-'));

const results = [];
function check(browser, name, ok, detail) {
  results.push({ browser, name, ok: !!ok });
  if (!ok) console.log('FAIL [' + browser + '] ' + name, detail === undefined ? '' : JSON.stringify(detail).slice(0, 400));
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
  const b = name;
  const browser = await playwright[name].launch();
  const url = base + '/tools/storyboard/index.html';
  const errors = [];
  const watch = (page) => {
    page.on('console', (m) => { if (m.type() === 'error' && !/prologue-art-lab/.test(m.text())) errors.push(m.text()); });
    page.on('pageerror', (e) => errors.push(String(e)));
  };
  const ready = (page, n) => page.waitForFunction((k) => /^Loaded \d+ nodes/.test(document.getElementById('status').textContent) && document.querySelectorAll('#nodes .node').length === k, n);
  const pos = (page, id) => page.evaluate((x) => {
    const n = Array.from(document.querySelectorAll('#nodes .node')).find((c) => c.firstChild.textContent === x);
    return n && { x: parseFloat(n.style.left), y: parseFloat(n.style.top) };
  }, id);
  const drag = async (page, id, dx, dy) => {
    const box = await page.evaluate((x) => {
      const n = Array.from(document.querySelectorAll('#nodes .node')).find((c) => c.firstChild.textContent === x);
      n.scrollIntoView({ block: 'center', inline: 'center' });
      const r = n.getBoundingClientRect();
      return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
    }, id);
    await page.mouse.move(box.x, box.y);
    await page.mouse.down();
    await page.mouse.move(box.x + dx / 2, box.y + dy / 2, { steps: 4 });
    await page.mouse.move(box.x + dx, box.y + dy, { steps: 4 });
    await page.mouse.up();
    return pos(page, id);
  };
  const choose = async (page, index, n) => { await page.selectOption('#chapterSelect', String(index)); await ready(page, n); };

  const ctx = await browser.newContext({ viewport: { width: 1500, height: 950 }, acceptDownloads: true });
  const page = await ctx.newPage();
  watch(page);
  await page.goto(url);
  await ready(page, 29);
  const options = await page.evaluate(() => Array.from(document.querySelectorAll('#chapterSelect option')).map((o) => [o.value, o.textContent]));
  check(b, 'header dropdown: exactly the four manifest chapters (Prologue, Chapter 1, Chapter 2, Chapter 3), in order', JSON.stringify(options) === JSON.stringify([['0', 'Prologue — The Last Good Day'], ['1', 'Chapter 1 — House of Tomorrow'], ['2', 'Chapter 2 — Biology Park'], ['3', "Chapter 3 — The People's Pavilion"]]), options);
  const a = await drag(page, 'drone_intercepts', 120, 70);
  const h = await drag(page, 'reception_hallway', -90, 80);
  await page.click('#nodes .node >> text=reception_hallway');
  await page.screenshot({ path: path.join(OUT, name + '_1_prologue.png') });
  await choose(page, 1, 36);
  const ch1Inspector = await page.evaluate(() => document.getElementById('details').innerText);
  check(b, 'Chapter 1: 36 authored nodes, arrival inspector, item choice, and independent unstarted scene reference',
    /HOUSE OF TOMORROW/.test(ch1Inspector)
    && /scenes\/house_of_tomorrow\/arrival · integrated/.test(ch1Inspector)
    && /TRY THE UNMARKED DOOR\./.test(ch1Inspector)
    && !/facilities_corridor/.test(ch1Inspector), ch1Inspector.slice(0, 500));
  const c = await drag(page, 'house_arrival', 160, 110);
  await page.screenshot({ path: path.join(OUT, name + '_2_chapter01.png') });
  // Chapter 2: its own 99-node graph, inspector, art references and positions.
  await choose(page, 2, 99);
  const ch2Inspector = await page.evaluate(() => document.getElementById('details').innerText);
  check(b, 'Chapter 2: 99 authored nodes, Bureau inspector, choice, and unstarted shared-catalog scene reference',
    /Bureau Arrival/.test(ch2Inspector) && /scenes\/biology_park\/conveniences_bureau · approved/.test(ch2Inspector) && /CONTINUE/.test(ch2Inspector), ch2Inspector.slice(0, 500));
  const d = await drag(page, 'park_junction', 140, -70);
  await page.screenshot({ path: path.join(OUT, name + '_2b_chapter02.png') });
  await choose(page, 1, 36);
  check(b, 'switching Chapter 2 -> Chapter 1 keeps the Chapter 1 position', JSON.stringify(await pos(page, 'house_arrival')) === JSON.stringify(c));
  await page.click('#nodes .node >> text=exit_service_clean');
  await page.click('#details button.choice >> text=CONTINUE');
  await ready(page, 99);
  check(b, 'a Chapter 1 exit card opens Chapter 2 with its moved node where it was left', JSON.stringify(await pos(page, 'park_junction')) === JSON.stringify(d)
    && await page.inputValue('#chapterSelect') === '2');
  await choose(page, 0, 29);
  const a2 = await pos(page, 'drone_intercepts');
  const h2 = await pos(page, 'reception_hallway');
  const sel = await page.evaluate(() => document.querySelector('#details h2').textContent);
  check(b, 'switching back keeps both Prologue positions and the Prologue selection', JSON.stringify([a2, h2]) === JSON.stringify([a, h]) && sel === 'Reception Hallway', [a, a2, h, h2, sel]);
  // The hand-off card in the inspector opens Chapter 1, with its moved node where it was left.
  await page.click('#details button.choice >> text=CONTINUE');
  await ready(page, 36);
  check(b, 'the hand-off card opens Chapter 1 and its layout is intact', JSON.stringify(await pos(page, 'house_arrival')) === JSON.stringify(c)
    && await page.inputValue('#chapterSelect') === '1');
  await choose(page, 0, 29);
  const [download] = await Promise.all([page.waitForEvent('download'), page.click('#exportLayout')]);
  const file = path.join(OUT, name + '_storyboard-layout.json');
  await download.saveAs(file);
  const exported = JSON.parse(fs.readFileSync(file, 'utf8'));
  check(b, 'Export Layout: one cyoa-storyboard-layout-v1 file with every opened chapter\'s arrangement', exported.schema === 'cyoa-storyboard-layout-v1'
    && JSON.stringify(exported.chapters['chapter-02'].positions.park_junction) === JSON.stringify(d)
    && JSON.stringify(exported.chapters['prologue-00'].positions.drone_intercepts) === JSON.stringify(a)
    && JSON.stringify(exported.chapters['prologue-00'].positions.reception_hallway) === JSON.stringify(h)
    && JSON.stringify(exported.chapters['chapter-01'].positions.house_arrival) === JSON.stringify(c), exported);
  await ctx.close();

  // A fresh profile (no saved positions) imports the file: both arrangements come back.
  const ctx2 = await browser.newContext({ viewport: { width: 1500, height: 950 } });
  const p2 = await ctx2.newPage();
  watch(p2);
  await p2.goto(url);
  await ready(p2, 29);
  const auto = await pos(p2, 'drone_intercepts');
  await p2.setInputFiles('#fileLayout', file);
  await p2.waitForFunction(() => /Imported layout is active/.test(document.getElementById('status').textContent));
  const a3 = await pos(p2, 'drone_intercepts');
  const h3 = await pos(p2, 'reception_hallway');
  await choose(p2, 1, 36);
  const c3 = await pos(p2, 'house_arrival');
  await choose(p2, 2, 99);
  const d3 = await pos(p2, 'park_junction');
  check(b, 'Import Layout in a fresh browser restores the Prologue, Chapter 1 and Chapter 2 arrangements', JSON.stringify(auto) !== JSON.stringify(a)
    && JSON.stringify([a3, h3, c3, d3]) === JSON.stringify([a, h, c, d]), [auto, a3, h3, c3, d3]);
  await choose(p2, 0, 29);
  check(b, 'after the import, switching chapters keeps the imported Prologue arrangement', JSON.stringify(await pos(p2, 'drone_intercepts')) === JSON.stringify(a));
  // Zoom, pan and the item/artwork panels still work.
  const before = await p2.evaluate(() => document.getElementById('stage').style.transform);
  await p2.click('#zoomIn');
  await p2.click('#showItems');
  const items = await p2.evaluate(() => document.querySelectorAll('#details .item-button').length);
  await p2.click('#showArtwork');
  const art = await p2.evaluate(() => document.getElementById('details').innerText);
  // 2026-11-17 (docs/106): +1 item (pavilion_satisfaction_certificate) and its 2 pending art records.
  // The not-started figure was already stale on main 7c7a50a (110 expected, 81 shown after the Ch2 batch approvals): now 81 + 2.
  check(b, 'zoom, Items and Artwork panels still work (171 shared art records incl. nine death screens, 83 not-started)', before !== await p2.evaluate(() => document.getElementById('stage').style.transform)
    && items === 33 && /171 shared art records/.test(art) && /83 not-started/.test(art), [items, art.slice(0, 400)]);
  await p2.screenshot({ path: path.join(OUT, name + '_3_imported.png') });
  await ctx2.close();
  check(b, 'no console or page errors', !errors.length, errors);
  await browser.close();
}

(async () => {
  const server = await serve();
  const base = 'http://127.0.0.1:' + server.address().port;
  try {
    for (const name of ['chromium', 'firefox']) await run(name, base);
  } finally { server.close(); }
  const passed = results.filter((r) => r.ok).length;
  console.log('storyboard browser QA ' + passed + '/' + results.length + (passed === results.length ? ' passed' : ' FAILED') + ' (screenshots: ' + OUT + ')');
  process.exitCode = passed === results.length ? 0 : 1;
})().catch((e) => { console.error(e); process.exitCode = 1; });
