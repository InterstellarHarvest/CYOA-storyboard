#!/usr/bin/env node
// Self-test for the canonical sync tools (docs/105). Dependency-free. Each case copies the real
// repository state into a scratch folder, breaks one thing, and proves the check or the
// registration tool refuses it. The real files are never touched.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const results = [];
function scratch() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'cyoa-sync-qa-'));
  for (const p of ['story', 'tools/sync', 'assets/selected']) fs.cpSync(path.join(ROOT, p), path.join(dir, p), { recursive: true });
  return dir;
}
const J = (dir, p) => JSON.parse(fs.readFileSync(path.join(dir, p), 'utf8'));
const W = (dir, p, v) => fs.writeFileSync(path.join(dir, p), JSON.stringify(v, null, 2) + '\n');
function check(dir) {
  try { return JSON.parse(execFileSync(process.execPath, [path.join(dir, 'tools/sync/check-canon.mjs'), '--json'], { encoding: 'utf8' })); }
  catch (e) { return JSON.parse(e.stdout); }
}
function register(dir, args) {
  try { return { code: 0, out: execFileSync(process.execPath, [path.join(dir, 'tools/sync/register-art.mjs'), ...args], { encoding: 'utf8' }) }; }
  catch (e) { return { code: e.status, out: String(e.stdout) }; }
}
function expectError(name, mutate, pattern) {
  const dir = scratch();
  mutate(dir);
  const r = check(dir);
  assert.equal(r.ok, false, name + ': the check must fail');
  assert.ok(r.errors.some((m) => pattern.test(m)), name + ': expected an error matching ' + pattern + ', got ' + JSON.stringify(r.errors.slice(0, 4)));
  results.push(name);
  fs.rmSync(dir, { recursive: true, force: true });
}

// 0. The committed state passes.
{
  const dir = scratch(), r = check(dir);
  assert.equal(r.ok, true, 'committed state passes: ' + JSON.stringify(r.errors.slice(0, 5)));
  assert.equal(r.stats.chapters, 5, 'five chapters including the published Chapter 4 narrative');
  results.push('baseline passes (' + r.stats.previewed + ' previews)');
  fs.rmSync(dir, { recursive: true, force: true });
}
const preview = J(ROOT, 'story/artwork-preview.json');
const integratedKey = 'scenes:house_of_tomorrow/arrival';
// A selected (approved, or since docs/108 integration, integrated) Biology Park record with a public preview.
const approvedKey = 'scenes:biology_park/formal_entrance';
assert.ok(preview.images[approvedKey], 'selected Biology Park entrance is previewed');

expectError('missing chapter', (d) => { const m = J(d, 'story/storyboard-manifest.json'); m.chapters = m.chapters.filter((c) => c.id !== 'chapter-03'); W(d, 'story/storyboard-manifest.json', m); }, /required chapter chapter-03 is missing/);
expectError('broken route', (d) => { const c = J(d, 'story/chapters/chapter-01.draft.json'); c.nodes.house_arrival.choices[0].to = 'nowhere'; W(d, 'story/chapters/chapter-01.draft.json', c); }, /destination nowhere does not exist/);
expectError('undeclared field', (d) => { const c = J(d, 'story/chapters/chapter-02.draft.json'); c.nodes[c.start].directorComment = 'x'; W(d, 'story/chapters/chapter-02.draft.json', c); }, /directorComment.*neither runtime nor declared storyboard-only/);
expectError('narrative-only chapter metadata cannot be marked gameplay ready', (d) => { const c = J(d, 'story/chapters/chapter-04.wip.json'); c.development.notForGameplay = false; W(d, 'story/chapters/chapter-04.wip.json', c); }, /development metadata requires notForGameplay=true/);
expectError('manifest key the importer rejects', (d) => { const m = J(d, 'story/storyboard-manifest.json'); m.preview = 'x'; W(d, 'story/storyboard-manifest.json', m); }, /field "preview" would be rejected/);
expectError('approved art regresses to generated', (d) => { const a = J(d, 'story/artwork.draft.json'); a.scenes['biology_park/formal_entrance'].status = 'generated'; W(d, 'story/artwork.draft.json', a); }, /REGRESSION.*generated/);
expectError('integrated art regresses to not-started', (d) => { const a = J(d, 'story/artwork.draft.json'); a.scenes['house_of_tomorrow/arrival'].status = 'not-started'; W(d, 'story/artwork.draft.json', a); }, /REGRESSION.*not-started/);
expectError('preview bytes tampered', (d) => { fs.appendFileSync(path.join(d, preview.images[approvedKey].file), Buffer.from([0])); }, /do not match the recorded SHA-256/);
expectError('preview file missing', (d) => { fs.rmSync(path.join(d, preview.images[approvedKey].file)); }, /is missing/);
expectError('stray unregistered package file', (d) => { fs.writeFileSync(path.join(d, 'assets/selected/stray.png'), 'x'); }, /stray\.png is not registered/);
expectError('selected record without preview', (d) => { const p = J(d, 'story/artwork-preview.json'); delete p.images[approvedKey]; W(d, 'story/artwork-preview.json', p); fs.rmSync(path.join(d, preview.images[approvedKey].file)); }, /(approved|integrated) but has no public preview/);
if (fs.existsSync(path.join(ROOT, 'story/game-integration.json'))) {
  expectError('integrated but not in the game report', (d) => { const g = J(d, 'story/game-integration.json'); g.images = g.images.filter((i) => i.key !== integratedKey); W(d, 'story/game-integration.json', g); }, /marked integrated, but game build .* does not report it/);
  // The record is approved-only in this copy (since docs/108 integration it is integrated in canon), and the game
  // build reports using it: the canon check must refuse a used image that is not marked integrated.
  expectError('game uses an approved-only image', (d) => { const a = J(d, 'story/artwork.draft.json'); a.scenes['biology_park/formal_entrance'].status = 'approved'; W(d, 'story/artwork.draft.json', a);
    const g = J(d, 'story/game-integration.json'); if (!g.images.some((i) => i.key === approvedKey)) g.images.push({ key: approvedKey, path: 'x.png', sha256: preview.images[approvedKey].sha256, kind: 'scene' }); W(d, 'story/game-integration.json', g); }, /the game build uses it, but its status is approved/);
  expectError('game pixels differ from preview', (d) => { const g = J(d, 'story/game-integration.json'); g.images.find((i) => i.key === integratedKey).sha256 = '0'.repeat(64); W(d, 'story/game-integration.json', g); }, /uses different pixels/);
}

// register-art refusals and the never-lower rule.
{
  const dir = scratch();
  const src = { repo: 'InterstellarHarvest/CYOA', commit: 'a'.repeat(40), path: 'art/x.png' };
  const png = path.join(dir, preview.images[approvedKey].file);
  const portrait = path.join(dir, preview.images['portraits:groundskeeper:idle'].file);
  const batch = (entries) => { const f = path.join(dir, 'batch.json'); fs.writeFileSync(f, JSON.stringify({ entries })); return ['--batch', f]; };
  let r = register(dir, batch([{ key: 'scenes:house_of_tomorrow/arrival', file: portrait, status: 'approved', source: src }]));
  assert.notEqual(r.code, 0); assert.match(r.out, /is 564x278, record says 314x206/); results.push('register refuses wrong native size');
  r = register(dir, batch([{ key: 'portraits:groundskeeper:idle', file: png, status: 'approved', source: src }]));
  assert.notEqual(r.code, 0); assert.match(r.out, /is 314x206, record says 564x278/); results.push('register refuses a scene as a portrait');
  r = register(dir, batch([{ key: approvedKey, file: png, status: 'approved', source: { ...src, commit: 'abc123' } }]));
  assert.notEqual(r.code, 0); assert.match(r.out, /full 40-hex SHA/); results.push('register requires a pinned full commit');
  r = register(dir, batch([{ key: approvedKey, file: png, status: 'approved', source: { ...src, path: 'review/x/source/a.png' } }]));
  assert.notEqual(r.code, 0); assert.match(r.out, /never published/); results.push('register refuses source/ masters');
  r = register(dir, batch([{ key: 'portraits:house:idle', file: png, status: 'approved', source: src }]));
  assert.notEqual(r.code, 0); assert.match(r.out, /is a container/); results.push('register refuses containers');
  r = register(dir, batch([{ key: 'scenes:nowhere/none', file: png, source: src }]));
  assert.notEqual(r.code, 0); assert.match(r.out, /no such artwork record/); results.push('register refuses unknown records');
  // An integrated record re-registered as approved stays integrated (status never lowered).
  const arrival = path.join(dir, preview.images[integratedKey] ? preview.images[integratedKey].file : png);
  if (preview.images[integratedKey]) {
    r = register(dir, batch([{ key: integratedKey, file: arrival, status: 'approved', source: src }]));
    assert.equal(r.code, 0, r.out);
    assert.equal(J(dir, 'story/artwork.draft.json').scenes['house_of_tomorrow/arrival'].status, 'integrated');
    results.push('register never lowers integrated -> approved');
  }
  // A not-started record becomes approved when its selection is registered.
  const a = J(dir, 'story/artwork.draft.json');
  a.scenes['biology_park/public_exit'].status = 'not-started';
  a.scenes['biology_park/public_exit'].assetPath = null; // a fresh selection: no production path assigned yet
  W(dir, 'story/artwork.draft.json', a);
  r = register(dir, batch([{ key: 'scenes:biology_park/public_exit', file: png, status: 'approved', source: src }]));
  assert.equal(r.code, 0, r.out);
  assert.equal(J(dir, 'story/artwork.draft.json').scenes['biology_park/public_exit'].status, 'approved');
  assert.equal(J(dir, 'story/artwork.draft.json').scenes['biology_park/public_exit'].assetPath, null, 'registration never invents a production path');
  results.push('register: selection = approval, no invented assetPath');
  fs.rmSync(dir, { recursive: true, force: true });
}

console.log(JSON.stringify({ result: 'PASS', checks: results.length, results }, null, 1));
