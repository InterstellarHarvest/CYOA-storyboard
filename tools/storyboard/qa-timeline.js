#!/usr/bin/env node
// Real-browser QA of the Prologue / Chapter 1 / Chapter 2 timeline layout (Chromium + Firefox), served over HTTP
// from the repository root. Measures the rendered DOM, not the layout code's own numbers.
//   NODE_PATH="$(npm root -g)" node tools/storyboard/qa-timeline.js [--out <dir>]
// Checks: card/port/label overlaps from real bounding boxes; every connector sampled along its path
// never runs through a card it does not belong to; reading zoom and label size; ports; Fit/Start;
// wheel zoom; pan; drag; Reset; Export/Import; old-cache migration; reload stability; port
// navigation; chapter pills select, inspect and drag; per-chapter view memory; the approved Chapter 3
// reboot timeline and its five incoming Chapter 2 routes; the preserved legacy Chapter 3 (swapped in
// for this check only, in its own browser context) with cards and connectors identical to the published viewer.
// Screenshots (beginning, middle, end, overview of both chapters) go to --out or the OS temp folder.
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const http = require('http');
const ROOT = path.resolve(__dirname, '../..');
let playwright;
try { playwright = require('playwright'); } catch (e) { console.log('Playwright is not installed here: run with NODE_PATH="$(npm root -g)"'); process.exit(2); }
const outArg = process.argv.indexOf('--out');
const OUT = outArg > 0 ? path.resolve(process.argv[outArg + 1]) : fs.mkdtempSync(path.join(os.tmpdir(), 'cyoa-storyboard-timeline-'));
fs.mkdirSync(OUT, { recursive: true });
const LEGACY = JSON.parse(fs.readFileSync(path.join(__dirname, 'qa-fixtures/legacy-render-snapshot.json'), 'utf8'));

const results = [];
function check(browser, name, ok, detail) {
  results.push({ browser, name, ok: !!ok });
  if (!ok) console.log('FAIL [' + browser + '] ' + name, detail === undefined ? '' : JSON.stringify(detail).slice(0, 600));
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

// Runs in the page: geometry of everything on the stage, in stage pixels (independent of zoom).
function measure() {
  const stage = document.getElementById('stage');
  const scale = Number((stage.style.transform.match(/scale\(([\d.]+)\)/) || [0, 1])[1]);
  const s = stage.getBoundingClientRect();
  const rect = (el) => { const r = el.getBoundingClientRect(); return { x: (r.left - s.left) / scale, y: (r.top - s.top) / scale, w: r.width / scale, h: r.height / scale }; };
  const cards = Array.from(document.querySelectorAll('#nodes .node')).map((c) => ({ id: c.firstChild.textContent, ...rect(c), cls: c.className }));
  const ports = Array.from(document.querySelectorAll('#ports .port')).map((p) => ({ id: p.dataset.port, ...rect(p), dir: p.dataset.dir, mode: p.dataset.mode, chapter: p.dataset.chapter, source: p.dataset.source || null, text: p.innerText }));
  const labels = Array.from(document.querySelectorAll('#edges g.tl-label')).map((g) => ({ from: g.dataset.from, to: g.dataset.to, ...rect(g.querySelector('rect.plate')),
    font: Math.min(...Array.from(g.querySelectorAll('text')).map((t) => parseFloat(getComputedStyle(t).fontSize) || parseFloat(t.getAttribute('font-size')))) }));
  const edges = Array.from(document.querySelectorAll('#edges g.tl-edge')).map((g) => {
    const p = g.querySelector('path.tl-line'), len = p.getTotalLength(), pts = [];
    for (let d = 0; d <= len; d += 5) { const q = p.getPointAtLength(d); pts.push([q.x, q.y]); }
    return { from: g.dataset.from, to: g.dataset.to, route: g.dataset.route, pts };
  });
  return { scale, cards, ports, labels, edges, width: stage.offsetWidth, height: stage.offsetHeight };
}
const overlap = (a, b, pad) => a.x < b.x + b.w + pad && b.x < a.x + a.w + pad && a.y < b.y + b.h + pad && b.y < a.y + a.h + pad;

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
  const choose = async (page, index, n) => { await page.selectOption('#chapterSelect', String(index)); await ready(page, n); await page.waitForTimeout(150); };
  const cardPos = (page, id) => page.evaluate((x) => { const n = Array.from(document.querySelectorAll('#nodes .node')).find((c) => c.firstChild.textContent === x); return n && { x: parseFloat(n.style.left), y: parseFloat(n.style.top) }; }, id);
  const shot = async (page, file) => page.screenshot({ path: path.join(OUT, name + '_' + file + '.png') });

  // ---- The preserved legacy Chapter 3 renders exactly as the published viewer did -------------
  // Since the gameplay integration the manifest's chapter-03 is the approved reboot. This context alone
  // serves the manifest and layout as they were before the activation (legacy file, archived status,
  // no Chapter 3 timeline); the committed files are untouched.
  const legacyCtx = await browser.newContext({ viewport: { width: 1500, height: 950 } });
  const readStory = (f) => JSON.parse(fs.readFileSync(path.join(ROOT, 'story', f), 'utf8'));
  await legacyCtx.route('**/story/storyboard-manifest.json', (route) => { const m = readStory('storyboard-manifest.json'); const e = m.chapters.find((c) => c.id === 'chapter-03'); e.file = 'chapters/chapter-03.draft.json'; e.status = 'archived'; route.fulfill({ contentType: 'application/json', body: JSON.stringify(m) }); });
  await legacyCtx.route('**/story/storyboard-layout.json', (route) => { const l = readStory('storyboard-layout.json'); l.chapters['chapter-03'] = { positions: {} }; route.fulfill({ contentType: 'application/json', body: JSON.stringify(l) }); });
  const legacyPage = await legacyCtx.newPage();
  watch(legacyPage);
  await legacyPage.goto(url);
  await ready(legacyPage, 29);
  for (const [index, key, count] of [[3, 'chapter-03', 62]]) {
    const page = legacyPage;
    await choose(page, index, count);
    const now = await page.evaluate(() => ({
      cards: Array.from(document.querySelectorAll('#nodes .node')).map((c) => ({ id: c.firstChild.textContent, className: c.className, left: c.style.left, top: c.style.top, text: Array.from(c.children).map((x) => x.textContent) })),
      shapes: Array.from(document.getElementById('edges').children).map((n) => ({ tag: n.tagName, d: n.getAttribute('d'), x: n.getAttribute('x'), y: n.getAttribute('y'), stroke: n.getAttribute('stroke'), dash: n.getAttribute('stroke-dasharray'), text: n.tagName === 'text' ? n.textContent : null })),
      ports: document.querySelectorAll('#ports .port').length, timelineClass: document.getElementById('app').classList.contains('timeline-on'),
      legend: getComputedStyle(document.getElementById('tlLegend')).display, jump: getComputedStyle(document.getElementById('tlJump')).display,
    }));
    const base = LEGACY[key];
    const baseCards = base.cards.map((c) => ({ id: c.id, className: c.className, left: c.left, top: c.top, text: c.text }));
    const baseShapes = base.shapes.map((n) => ({ tag: n.tag, d: n.attributes.d || null, x: n.attributes.x === undefined ? null : String(n.attributes.x), y: n.attributes.y === undefined ? null : String(n.attributes.y), stroke: n.attributes.stroke || null, dash: n.attributes['stroke-dasharray'] || null, text: n.tag === 'text' ? n.text : null }));
    // docs/104 (4b2b1bb) intentionally changed what the fatal Chapter 3 cards display (death title,
    // narrative beat, art ID, fatal colours), mirroring qa-smoke's 4b876c0: those cards keep their exact
    // position; every other card stays fully identical.
    const FATAL = new Set(['end_model_citizen', 'end_reconciled', 'end_archived']);
    const norm = (cards) => cards.map((c) => (FATAL.has(c.id) ? { id: c.id, className: 'node', left: c.left, top: c.top, text: ['FATAL POPUP CONTENT'] } : c));
    check(b, key + ': every card identical to the published viewer (position, class, text; fatal cards: position)', JSON.stringify(norm(now.cards)) === JSON.stringify(norm(baseCards)), norm(now.cards).find((c, i) => JSON.stringify(c) !== JSON.stringify(norm(baseCards)[i])));
    if (key === 'chapter-03') check(b, 'chapter-03: fatal cards show their death-popup title and art ID', now.cards.filter((c) => FATAL.has(c.id)).every((c) => /death-node/.test(c.className) && c.text.some((t) => /^ART: /.test(t))));
    check(b, key + ': every connector, arrow and label identical to the published viewer', JSON.stringify(now.shapes) === JSON.stringify(baseShapes), now.shapes.find((c, i) => JSON.stringify(c) !== JSON.stringify(baseShapes[i])));
    check(b, key + ': no timeline chrome, ports or legend', !now.ports && !now.timelineClass && now.legend === 'none' && now.jump === 'none', now);
    await shot(page, key + '_legacy_default');
  }
  await legacyCtx.close();

  const ctx = await browser.newContext({ viewport: { width: 1500, height: 950 }, acceptDownloads: true });
  const page = await ctx.newPage();
  watch(page);
  await page.goto(url);
  await ready(page, 29);

  // ---- Prologue, Chapter 1, Chapter 2 and Chapter 3 timelines --------------------------------------
  const geometry = {};
  const startOf = { 'prologue-00': 'work_complete', 'chapter-01': 'house_arrival', 'chapter-02': 'bureau_arrival', 'chapter-03': 'pavilion_arrival' };
  for (const [index, key, count] of [[0, 'prologue-00', 29], [1, 'chapter-01', 36], [2, 'chapter-02', 99], [3, 'chapter-03', 34]]) {
    await choose(page, index, count);
    await page.click('#tlStart');
    const view = await page.evaluate((start) => {
      const v = document.getElementById('viewport').getBoundingClientRect();
      const c = Array.from(document.querySelectorAll('#nodes .node')).find((n) => n.firstChild.textContent === start).getBoundingClientRect();
      return { inside: c.left >= v.left && c.right <= v.right && c.top >= v.top && c.bottom <= v.bottom, transform: document.getElementById('stage').style.transform, vh: v.height };
    }, startOf[key]);
    check(b, key + ': opens at 100% with the start node fully in view', view.transform === 'scale(1)' && view.inside, view);
    await shot(page, key + '_1_beginning');
    const g = await page.evaluate(measure);
    geometry[key] = g;
    check(b, key + ': all ' + count + ' nodes rendered', g.cards.length === count, g.cards.length);
    const boxes = [...g.cards, ...g.ports];
    const cardHits = [];
    for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) if (overlap(boxes[i], boxes[j], 4)) cardHits.push([boxes[i].id, boxes[j].id]);
    check(b, key + ': no overlapping cards or ports (real bounding boxes, 4px clearance)', !cardHits.length, cardHits.slice(0, 5));
    const labelHits = [];
    for (let i = 0; i < g.labels.length; i++) {
      for (let j = i + 1; j < g.labels.length; j++) if (overlap(g.labels[i], g.labels[j], 0)) labelHits.push([g.labels[i].from + '>' + g.labels[i].to, g.labels[j].from + '>' + g.labels[j].to]);
      for (const box of boxes) if (overlap(g.labels[i], box, 0)) labelHits.push([g.labels[i].from + '>' + g.labels[i].to, box.id]);
    }
    check(b, key + ': ' + g.labels.length + ' connector labels never collide with each other, cards or ports', !labelHits.length, labelHits.slice(0, 5));
    check(b, key + ': label text is at least 10px at the default zoom', g.labels.every((l) => l.font * g.scale >= 10), g.labels.map((l) => l.font).slice(0, 3));
    // Lines never travel through a card or port they do not belong to (sampled every 5px).
    const through = [];
    for (const e of g.edges) {
      for (const box of boxes) {
        if (box.id === e.from || box.id === e.to) continue;
        const inner = { x: box.x + 3, y: box.y + 3, w: box.w - 6, h: box.h - 6 };
        const hit = e.pts.find(([x, y]) => x > inner.x && x < inner.x + inner.w && y > inner.y && y < inner.y + inner.h);
        if (hit) { through.push(e.from + '>' + e.to + ' through ' + box.id + ' at ' + hit.map(Math.round)); break; }
      }
    }
    check(b, key + ': no connector passes through an unrelated card or port (' + g.edges.length + ' connectors sampled)', !through.length, through.slice(0, 5));
    // Left to right: forward connectors end to the right of where they start.
    const at = Object.fromEntries(g.cards.map((c) => [c.id, c]));
    const backwards = g.edges.filter((e) => e.route === 'forward' && !(at[e.to].x > at[e.from].x)).map((e) => e.from + '>' + e.to);
    check(b, key + ': every forward connector runs left to right', !backwards.length, backwards);
    // Middle and end of the timeline at reading zoom.
    for (const [file, fraction] of [['2_middle', 0.5], ['3_end', 1]]) {
      await page.evaluate((f) => {
        const v = document.getElementById('viewport');
        v.scrollLeft = (v.scrollWidth - v.clientWidth) * f;
        const cx = (v.scrollLeft + v.clientWidth / 2), cards = Array.from(document.querySelectorAll('#nodes .node')).map((n) => ({ x: parseFloat(n.style.left) + 110, y: parseFloat(n.style.top) + 50 }));
        const near = cards.filter((c) => Math.abs(c.x - cx) < v.clientWidth / 2).sort((a, c) => a.y - c.y);
        const mid = near.length ? (near[0].y + near[near.length - 1].y) / 2 : v.scrollHeight / 2;
        v.scrollTop = Math.max(0, mid - v.clientHeight / 2);
      }, fraction);
      await page.waitForTimeout(80);
      await shot(page, key + '_' + file);
    }
    await page.click('#fit');
    const fitted = await page.evaluate(() => { const v = document.getElementById('viewport'); return { sw: v.scrollWidth, cw: v.clientWidth, sh: v.scrollHeight, ch: v.clientHeight, t: document.getElementById('stage').style.transform }; });
    check(b, key + ': Fit shows the whole timeline as an overview', fitted.sw <= fitted.cw + 1 && fitted.sh <= fitted.ch + 1, fitted);
    await shot(page, key + '_4_fit_overview');
    await page.click('#tlStart');
    check(b, key + ': Start returns to 100% reading zoom', await page.evaluate(() => document.getElementById('stage').style.transform) === 'scale(1)');
  }
  // Chapter-specific port checks on real DOM.
  const c1 = geometry['chapter-01'], c2 = geometry['chapter-02'];
  const c1max = Math.max(...c1.cards.map((c) => c.x));
  const exits = ['exit_named_plant', 'exit_martin', 'exit_service_clean', 'exit_service_registered', 'exit_showroom_reset'];
  check(b, 'Chapter 1: five surviving exits in the right-hand column, each with a gameplay port to Chapter 2', exits.every((id) => c1.cards.find((c) => c.id === id).x === c1max)
    && c1.ports.filter((p) => p.dir === 'out').length === 5 && c1.ports.filter((p) => p.dir === 'out').every((p) => p.mode === 'gameplay' && p.chapter === 'chapter-02' && /Bureau Arrival/.test(p.text)));
  check(b, 'Chapter 1: fatal chair has no route or port out', !c1.edges.some((e) => e.from === 'exit_chair_fatal') && !c1.ports.some((p) => /exit_chair_fatal/.test(p.id)));
  check(b, 'Chapter 2: five incoming Chapter 1 routes into bureau_arrival', c2.ports.filter((p) => p.dir === 'in').map((p) => p.source).sort().join() === [...exits].sort().join()
    && c2.edges.filter((e) => e.route === 'port' && /^in:/.test(e.from)).every((e) => e.to === 'bureau_arrival'));
  const livingEnds = ['end_concourse_robot', 'end_underground_station', 'end_public', 'end_maintenance', 'end_customs'];
  check(b, 'Chapter 2: five gameplay transitions to Chapter 3 from the living endings, none from a fatal ending, no preview handoff', c2.ports.filter((p) => p.dir === 'out').map((p) => p.id).sort().join() === livingEnds.map((id) => 'out:' + id + '>chapter-03').sort().join()
    && c2.ports.filter((p) => p.dir === 'out').every((p) => p.mode === 'gameplay' && p.chapter === 'chapter-03' && /TO CHAPTER 3 · GAMEPLAY/.test(p.text) && /Pavilion Arrival/.test(p.text)) && !c2.ports.some((p) => p.mode === 'preview'));
  const c3 = geometry['chapter-03'];
  const ch3Exits = ['locomotion_fail', 'presenter_help_end', 'paper_problem_end', 'attendant_honest_end', 'door_dash_fail', 'door_reverse_end', 'backstage_exit'];
  check(b, 'Chapter 3: five incoming Chapter 2 routes into pavilion_arrival and seven outgoing Chapter 4 routes, one per surviving ending (game issue #27)', c3.ports.filter((p) => p.dir === 'in').map((p) => p.source).sort().join() === [...livingEnds].sort().join()
    && c3.ports.filter((p) => p.dir === 'in').every((p) => p.chapter === 'chapter-02' && p.mode === 'gameplay')
    && c3.ports.filter((p) => p.dir === 'out').map((p) => p.id).sort().join() === ch3Exits.map((id) => 'out:' + id + '>chapter-04').sort().join()
    && c3.ports.filter((p) => p.dir === 'out').every((p) => p.chapter === 'chapter-04' && p.mode === 'gameplay')
    && c3.edges.filter((e) => e.route === 'port' && /^in:/.test(e.from)).length === 5 && c3.edges.filter((e) => e.route === 'port' && /^in:/.test(e.from)).every((e) => e.to === 'pavilion_arrival'));
  const ch3Ends = ['locomotion_fail', 'presenter_help_end', 'paper_problem_end', 'attendant_honest_end', 'door_dash_fail', 'door_reverse_end', 'backstage_exit'];
  check(b, 'Chapter 3: its seven endings are drawn as surviving endings, never fatal', ch3Ends.every((id) => { const c = c3.cards.find((x) => x.id === id); return c && !/\bfatal\b|death-node/.test(c.cls); }));

  const c0 = geometry['prologue-00'];
  check(b, 'Prologue: timeline with its Chapter 1 hand-off pill on the right', c0.cards.find((c) => c.id === 'reception_hallway').x === Math.max(...c0.cards.map((c) => c.x))
    && c0.ports.length === 1 && c0.ports[0].dir === 'out' && c0.ports[0].chapter === 'chapter-01' && c0.ports[0].mode === 'gameplay');

  // ---- Chapter pills behave like cards ----------------------------------------------------------
  await choose(page, 2, 99);
  await page.click('#tlStart');
  await page.click('#ports .port[data-source="exit_martin"]');
  await page.waitForTimeout(100);
  check(b, 'clicking an incoming pill stays in Chapter 2 and inspects it', await page.inputValue('#chapterSelect') === '2'
    && await page.evaluate(() => document.querySelector('#details h2').textContent) === 'From Chapter 1 — House of Tomorrow — Exit Martin'
    && await page.evaluate(() => document.querySelector('#ports .port[data-source="exit_martin"]').classList.contains('selected')));
  const pillBefore = await page.evaluate(() => { const p = document.querySelector('#ports .port[data-source="exit_martin"]'); return { x: parseFloat(p.style.left), y: parseFloat(p.style.top) }; });
  const pillBox = await page.locator('#ports .port[data-source="exit_martin"]').boundingBox();
  await page.mouse.move(pillBox.x + 60, pillBox.y + 29); await page.mouse.down();
  await page.mouse.move(pillBox.x + 80, pillBox.y - 20, { steps: 5 }); await page.mouse.move(pillBox.x + 100, pillBox.y - 70, { steps: 5 }); await page.mouse.up();
  await page.waitForTimeout(100);
  const pillAfter = await page.evaluate(() => { const p = document.querySelector('#ports .port[data-source="exit_martin"]'); return { x: parseFloat(p.style.left), y: parseFloat(p.style.top) }; });
  const pillSaved = await page.evaluate(() => JSON.parse(localStorage.getItem('cyoa-storyboard-layout-v1:chapter-02')).positions['in:chapter-01>exit_martin']);
  check(b, 'a pill can be dragged like a card, is saved with the chapter, and dropping it does not navigate', pillAfter.x === pillBefore.x + 40 && pillAfter.y === pillBefore.y - 99
    && JSON.stringify(pillSaved) === JSON.stringify(pillAfter) && await page.inputValue('#chapterSelect') === '2', [pillBefore, pillAfter, pillSaved]);
  await page.click('#resetLayout');
  await page.click('#ports .port[data-port="out:end_customs>chapter-03"]');
  const ch3PillText = await page.evaluate(() => document.getElementById('details').innerText);
  check(b, 'clicking a Chapter 3 transition pill inspects it as gameplay and stays in Chapter 2', await page.inputValue('#chapterSelect') === '2'
    && !/storyboard preview only, not gameplay/.test(ch3PillText) && /Open Chapter 3 — The People's Pavilion at Pavilion Arrival/.test(ch3PillText), ch3PillText.slice(0, 300));

  // ---- Per-chapter view memory -------------------------------------------------------------------
  await choose(page, 1, 36);
  await page.evaluate(() => { const v = document.getElementById('viewport'); v.scrollLeft = 2100; v.scrollTop = 120; });
  await page.click('#zoomOut');
  const ch1View = await page.evaluate(() => ({ t: document.getElementById('stage').style.transform, l: document.getElementById('viewport').scrollLeft, top: document.getElementById('viewport').scrollTop }));
  await choose(page, 2, 99);
  await page.evaluate(() => { document.getElementById('viewport').scrollLeft = 5000; });
  const ch2View = await page.evaluate(() => ({ t: document.getElementById('stage').style.transform, l: document.getElementById('viewport').scrollLeft, top: document.getElementById('viewport').scrollTop }));
  await choose(page, 1, 36);
  const ch1Back = await page.evaluate(() => ({ t: document.getElementById('stage').style.transform, l: document.getElementById('viewport').scrollLeft, top: document.getElementById('viewport').scrollTop }));
  await choose(page, 2, 99);
  const ch2Back = await page.evaluate(() => ({ t: document.getElementById('stage').style.transform, l: document.getElementById('viewport').scrollLeft, top: document.getElementById('viewport').scrollTop }));
  check(b, 'switching chapters in the dropdown returns each chapter to its last zoom and scroll', JSON.stringify(ch1Back) === JSON.stringify(ch1View) && JSON.stringify(ch2Back) === JSON.stringify(ch2View), [ch1View, ch1Back, ch2View, ch2Back]);
  await shot(page, 'chapter-02_5_returned_view');

  // ---- Interactions on Chapter 1 ---------------------------------------------------------------
  await choose(page, 1, 36);
  const start = await page.evaluate(() => document.getElementById('stage').style.transform);
  const vbox = await page.locator('#viewport').boundingBox();
  await page.mouse.move(vbox.x + vbox.width / 2, vbox.y + 40);
  await page.mouse.wheel(0, -240);
  await page.waitForTimeout(100);
  check(b, 'wheel zoom still works on the timeline', await page.evaluate(() => document.getElementById('stage').style.transform) !== start);
  await page.click('#tlStart');
  const empty = await page.evaluate(() => { const v = document.getElementById('viewport').getBoundingClientRect(); for (let y = v.top + 20; y < v.bottom - 20; y += 30) for (let x = v.left + 300; x < v.right - 40; x += 40) { const el = document.elementFromPoint(x, y); if (el && (el.id === 'viewport' || el.id === 'space' || el.id === 'stage' || el.id === 'edges' || el.id === 'nodes' || el.id === 'ports')) return { x, y }; } return null; });
  const scrollBefore = await page.evaluate(() => document.getElementById('viewport').scrollLeft);
  await page.mouse.move(empty.x, empty.y); await page.mouse.down(); await page.mouse.move(empty.x - 260, empty.y, { steps: 6 }); await page.mouse.up();
  check(b, 'dragging empty space pans along the timeline', await page.evaluate(() => document.getElementById('viewport').scrollLeft) > scrollBefore + 200);
  await page.click('#tlStart');
  const defaultPos = await cardPos(page, 'welcome_home');
  const pathBefore = await page.evaluate(() => Array.from(document.querySelectorAll('#edges g.tl-edge[data-to="welcome_home"] path.tl-line')).map((p) => p.getAttribute('d')).join('|'));
  const card = await page.evaluate(() => { const n = Array.from(document.querySelectorAll('#nodes .node')).find((c) => c.firstChild.textContent === 'welcome_home'); n.scrollIntoView({ block: 'center', inline: 'center' }); const r = n.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; });
  await page.mouse.move(card.x, card.y); await page.mouse.down(); await page.mouse.move(card.x + 40, card.y + 60, { steps: 5 }); await page.mouse.move(card.x + 80, card.y + 120, { steps: 5 }); await page.mouse.up();
  const dragged = await cardPos(page, 'welcome_home');
  const saved = await page.evaluate(() => JSON.parse(localStorage.getItem('cyoa-storyboard-layout-v1:chapter-01')));
  check(b, 'dragging a timeline card moves it and saves it under Chapter 1 with the current layout revision', dragged.x === defaultPos.x + 80 && dragged.y === defaultPos.y + 120 && saved.layoutRevision === 2 && saved.positions.welcome_home.x === dragged.x, [defaultPos, dragged, saved]);
  check(b, 'connectors follow the dragged card', await page.evaluate(() => Array.from(document.querySelectorAll('#edges g.tl-edge[data-to="welcome_home"] path.tl-line')).map((p) => p.getAttribute('d')).join('|')) !== pathBefore);
  await page.click('#nodes .node >> text=exit_martin');
  check(b, 'clicking a card still opens it in the inspector', await page.evaluate(() => document.querySelector('#details h2').textContent) === 'Exit Martin');
  const [download] = await Promise.all([page.waitForEvent('download'), page.click('#exportLayout')]);
  const file = path.join(OUT, name + '_exported-layout.json');
  await download.saveAs(file);
  const exported = JSON.parse(fs.readFileSync(file, 'utf8'));
  check(b, 'Export Layout keeps schema v1 with every chapter\'s revision and incident metadata (Chapter 3: the reboot timeline, revision 3)', exported.schema === 'cyoa-storyboard-layout-v1' && exported.chapters['chapter-01'].layoutRevision === 2
    && exported.chapters['chapter-01'].positions.welcome_home.x === dragged.x && exported.chapters['chapter-02'].timeline.incidents.length >= 10 && exported.chapters['prologue-00'].layoutRevision === 2
    && exported.chapters['chapter-03'].layoutRevision === 3 && exported.chapters['chapter-03'].timeline.incidents.flatMap((i) => i.nodes).length === 34);
  await page.click('#resetLayout');
  check(b, 'Reset Layout returns Chapter 1 to the timeline default', JSON.stringify(await cardPos(page, 'welcome_home')) === JSON.stringify(defaultPos));
  await page.setInputFiles('#fileLayout', file);
  await page.waitForFunction(() => /Imported layout is active/.test(document.getElementById('status').textContent));
  check(b, 'Import Layout restores the exported Chapter 1 arrangement', JSON.stringify(await cardPos(page, 'welcome_home')) === JSON.stringify(dragged));
  await page.click('#resetLayout');
  // Navigation between chapters is an explicit inspector button on a selected pill.
  await choose(page, 2, 99);
  await page.click('#ports .port[data-source="exit_showroom_reset"]');
  await page.click('#details button.choice >> text=Open Exit Showroom Reset in Chapter 1');
  await ready(page, 36);
  check(b, 'an incoming pill\'s inspector button opens the matching Chapter 1 exit', await page.inputValue('#chapterSelect') === '1' && await page.evaluate(() => document.querySelector('#details h2').textContent) === 'Exit Showroom Reset');
  await page.click('#ports .port[data-port="out:exit_named_plant>chapter-02"]');
  await page.click('#details button.choice >> text=Open Chapter 2 — Biology Park at Bureau Arrival');
  await ready(page, 99);
  check(b, 'a Chapter 1 exit pill\'s inspector button opens Chapter 2 at bureau_arrival', await page.evaluate(() => document.querySelector('#details h2').textContent) === 'Bureau Arrival');
  await page.click('#ports .port[data-port="out:end_customs>chapter-03"]');
  await page.click("#details button.choice >> text=Open Chapter 3 — The People's Pavilion at Pavilion Arrival");
  await ready(page, 34);
  check(b, 'a Chapter 2 ending pill\'s inspector button opens Chapter 3 at pavilion_arrival with its five incoming and seven outgoing (Chapter 4) pills', await page.inputValue('#chapterSelect') === '3'
    && await page.evaluate(() => document.querySelector('#details h2').textContent) === 'Pavilion Arrival' && await page.evaluate(() => document.querySelectorAll('#ports .port').length) === 12);
  await ctx.close();

  // ---- Old cached layouts never hide the new default; reload stability -------------------------
  const ctx2 = await browser.newContext({ viewport: { width: 1500, height: 950 } });
  await ctx2.addInitScript(() => {
    if (sessionStorage.getItem('seeded')) return; sessionStorage.setItem('seeded', '1');
    localStorage.setItem('cyoa-storyboard-layout-v1:chapter-01', JSON.stringify({ positions: { house_arrival: { x: 3000, y: 900 } } }));
    localStorage.setItem('cyoa-storyboard-layout-v1:prologue-00', JSON.stringify({ positions: { drone_intercepts: { x: 777, y: 333 } } }));
    localStorage.setItem('cyoa-storyboard-layout-v1:chapter-03', JSON.stringify({ positions: { pavilion_arrival: { x: 555, y: 444 } } }));
  });
  const p2 = await ctx2.newPage();
  watch(p2);
  await p2.goto(url);
  await ready(p2, 29);
  const proDefault = c0.cards.find((c) => c.id === 'drone_intercepts');
  check(b, 'an old cached Prologue layout is archived and the Prologue timeline shows', JSON.stringify(await cardPos(p2, 'drone_intercepts')) === JSON.stringify({ x: Math.round(proDefault.x), y: Math.round(proDefault.y) })
    && await p2.evaluate(() => JSON.parse(localStorage.getItem('cyoa-storyboard-layout-v1:prologue-00@archive-r1')).positions.drone_intercepts.x) === 777);
  await choose(p2, 1, 36);
  const migrated = await p2.evaluate(() => ({ archive: JSON.parse(localStorage.getItem('cyoa-storyboard-layout-v1:chapter-01@archive-r1') || 'null'), restore: !document.getElementById('restoreLayout').hidden && getComputedStyle(document.getElementById('restoreLayout')).display !== 'none' }));
  check(b, 'an old cached Chapter 1 layout is archived, not applied, and Restore is offered', JSON.stringify(await cardPos(p2, 'house_arrival')) === JSON.stringify(c1.cards.find((c) => c.id === 'house_arrival') && { x: Math.round(c1.cards.find((c) => c.id === 'house_arrival').x), y: Math.round(c1.cards.find((c) => c.id === 'house_arrival').y) })
    && migrated.archive && migrated.archive.positions.house_arrival.x === 3000 && migrated.restore, migrated);
  const first = await p2.evaluate(() => Array.from(document.querySelectorAll('#nodes .node')).map((c) => c.firstChild.textContent + '@' + c.style.left + ',' + c.style.top).join(';') + '#' + Array.from(document.querySelectorAll('#edges path.tl-line')).map((p) => p.getAttribute('d')).join(';'));
  await p2.reload();
  await ready(p2, 29);
  await choose(p2, 1, 36);
  const second = await p2.evaluate(() => Array.from(document.querySelectorAll('#nodes .node')).map((c) => c.firstChild.textContent + '@' + c.style.left + ',' + c.style.top).join(';') + '#' + Array.from(document.querySelectorAll('#edges path.tl-line')).map((p) => p.getAttribute('d')).join(';'));
  check(b, 'Chapter 1 timeline identical across a reload', first === second);
  await p2.click('#restoreLayout');
  check(b, 'Restore previous arrangement brings the archived position back', JSON.stringify(await cardPos(p2, 'house_arrival')) === JSON.stringify({ x: 3000, y: 900 }));
  await choose(p2, 3, 34);
  const c3Start = c3.cards.find((c) => c.id === 'pavilion_arrival');
  check(b, 'an old cached legacy Chapter 3 layout is archived, not applied, and the reboot timeline shows', JSON.stringify(await cardPos(p2, 'pavilion_arrival')) === JSON.stringify({ x: Math.round(c3Start.x), y: Math.round(c3Start.y) })
    && await p2.evaluate(() => JSON.parse(localStorage.getItem('cyoa-storyboard-layout-v1:chapter-03@archive-r1') || 'null')?.positions?.pavilion_arrival?.x) === 555);
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
  fs.writeFileSync(path.join(OUT, 'qa-timeline-results.json'), JSON.stringify(results, null, 2));
  console.log('storyboard timeline QA ' + passed + '/' + results.length + (passed === results.length ? ' passed' : ' FAILED') + ' (screenshots: ' + OUT + ')');
  process.exitCode = passed === results.length ? 0 : 1;
})().catch((e) => { console.error(e); process.exitCode = 1; });
