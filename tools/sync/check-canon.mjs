#!/usr/bin/env node
// Canonical storyboard drift check (docs/105). Dependency-free; runs in CI before every Pages deploy.
//
//   node tools/sync/check-canon.mjs            full check, exit 1 on any error
//   node tools/sync/check-canon.mjs --json     machine-readable result
//
// It proves, from the committed files alone:
//   chapters   every required chapter is in the manifest; every chapter file parses; start nodes and
//              every choice / SHOW / USE destination resolve (cross-chapter hand-offs included)
//   fields     every node / choice field is a runtime field or a declared storyboard-only field
//              (story/sync-contract.json), so a new annotation can never silently break the game import
//   statuses   every artwork status is a known value
//   selected   every selected record (approved / integrated / reused) that holds an image has a public
//              preview whose bytes match its recorded SHA-256, native size and transparency contract
//   regression no previewed (selected) record has fallen back to generated / not-started / prompted
//   integrated every `integrated` record is in story/game-integration.json with the same SHA-256, and
//              every image the game reports is `integrated` or `reused` here
//   package    nothing in assets/selected/ is unregistered
//   no-image   'text-led' / 'voice-only' records (docs/137) are approved and carry no path, preview or nested art
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { artRecords, statusOf, checkContract, sha256, readJson, SELECTED, STATUS_VALUES, FORMATS, NO_IMAGE_FORMATS } from './lib.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const S = (p) => path.join(ROOT, 'story', p);

export function checkCanon() {
  const errors = [], notes = [];
  const err = (m) => errors.push(m);
  const contract = readJson(S('sync-contract.json'));
  const manifest = readJson(S('storyboard-manifest.json'));
  const rf = contract.runtimeFields, so = contract.storyboardOnlyFields;
  const allowed = (level) => new Set([...(rf[level] || []), ...(so[level] || [])]);

  // Chapters -------------------------------------------------------------------------------------
  const ids = (manifest.chapters || []).map((c) => c.id);
  contract.requiredChapters.forEach((id) => { if (!ids.includes(id)) err('manifest: required chapter ' + id + ' is missing'); });
  Object.keys(manifest).forEach((k) => { if (!rf.manifest.includes(k)) err('manifest: field "' + k + '" would be rejected by the game importer'); });
  const chapters = {};
  for (const entry of manifest.chapters || []) {
    Object.keys(entry).forEach((k) => { if (!rf.manifestChapter.includes(k)) err('manifest chapter ' + entry.id + ': field "' + k + '" would be rejected by the game importer'); });
    try { chapters[entry.id] = readJson(S(entry.file)); } catch (e) { err('chapter ' + entry.id + ': cannot read ' + entry.file + ' (' + e.message + ')'); }
  }
  const nodeOk = new Set(), choiceOk = allowed('choice'), entryOk = allowed('entry'), nodeAllowed = allowed('node');
  let nodes = 0, routes = 0;
  for (const [cid, ch] of Object.entries(chapters)) {
    Object.keys(ch).forEach((k) => { if (!allowed('chapter').has(k)) err(cid + ': chapter field "' + k + '" is neither runtime nor storyboard-only'); });
    // notForGameplay is true until artwork and engine integration are complete; the Gameplay PMO sets it
    // false explicitly when a game integration consumes the chapter (docs/152 section 7B.6). Never absent.
    if (ch.development && typeof ch.development.notForGameplay !== 'boolean')
      err(cid + ': development metadata requires notForGameplay=true until artwork and engine integration are complete (false only once a game integration consumes it)');
    if (!ch.nodes || !ch.nodes[ch.start]) err(cid + ': start node ' + ch.start + ' does not exist');
    const target = (where, t) => {
      if (t.chapter) { if (!chapters[t.chapter] && !ids.includes(t.chapter)) err(where + ': hand-off to unknown chapter ' + t.chapter); routes++; return; }
      if (t.to && !ch.nodes[t.to]) err(where + ': destination ' + t.to + ' does not exist');
      for (const side of ['pass', 'fail']) if (t[side] && typeof t[side] === 'string' && !ch.nodes[t[side]]) err(where + ': ' + side + ' destination ' + t[side] + ' does not exist');
      for (const side of ['pass', 'fail']) if (t[side] && typeof t[side] === 'object' && t[side].to && !ch.nodes[t[side].to]) err(where + ': ' + side + ' destination ' + t[side].to + ' does not exist');
      routes++;
    };
    for (const [nid, n] of Object.entries(ch.nodes || {})) {
      nodes++; nodeOk.add(cid + ':' + nid);
      Object.keys(n).forEach((k) => { if (!nodeAllowed.has(k)) err(cid + ':' + nid + ': field "' + k + '" is neither runtime nor declared storyboard-only (story/sync-contract.json)'); });
      (n.choices || []).forEach((c, i) => {
        const w = cid + ':' + nid + ' choice ' + (c.id || '#' + i);
        Object.keys(c).forEach((k) => { if (!choiceOk.has(k)) err(w + ': field "' + k + '" is neither runtime nor declared storyboard-only'); });
        target(w, c);
      });
      for (const verb of ['show', 'use']) for (const [item, e] of Object.entries(n[verb] || {})) {
        if (!e || typeof e !== 'object') continue;
        Object.keys(e).forEach((k) => { if (!entryOk.has(k)) err(cid + ':' + nid + ' ' + verb + ' ' + item + ': field "' + k + '" is neither runtime nor storyboard-only'); });
        target(cid + ':' + nid + ' ' + verb + ' ' + item, e);
      }
      if (n.storyboardNextChapter && !ids.includes(n.storyboardNextChapter)) err(cid + ':' + nid + ': storyboardNextChapter ' + n.storyboardNextChapter + ' is not a manifest chapter');
    }
  }
  const items = readJson(S(manifest.items));
  Object.entries(items).forEach(([id, it]) => Object.keys(it).forEach((k) => { if (!rf.item.includes(k)) err('item ' + id + ': field "' + k + '" would be rejected by the game importer'); }));

  // Artwork --------------------------------------------------------------------------------------
  const art = readJson(S(manifest.artwork));
  const preview = fs.existsSync(S('artwork-preview.json')) ? readJson(S('artwork-preview.json')) : { images: {} };
  const integration = fs.existsSync(S('game-integration.json')) ? readJson(S('game-integration.json')) : null;
  const records = artRecords(art);
  const byKey = new Map(records.map((e) => [e.key, e]));
  const counts = {};
  let previewed = 0;
  for (const e of records) {
    const st = statusOf(e);
    if (!e.layer) counts[st] = (counts[st] || 0) + 1;
    if (!STATUS_VALUES.includes(st)) err(e.key + ': unknown status ' + st);
    const container = !!(e.record.views || e.record.pages || e.record.layers);
    const p = preview.images[e.key];
    const fmt = e.layer ? undefined : e.record.format;
    if (fmt !== undefined && (FORMATS[fmt] !== e.group || e.variant)) err(e.key + ': format "' + fmt + '" is not valid here (known: ' + Object.entries(FORMATS).map(([f, g]) => f + ' on ' + g).join(', ') + ')');
    if (NO_IMAGE_FORMATS.includes(fmt)) {
      // An owner-approved presentation decision with no image (docs/137): never an art slot.
      if (st !== 'approved') err(e.key + ': a ' + fmt + ' record is an approved no-image decision; status must be approved, not ' + st);
      if (e.record.assetPath != null || e.record.suggestedFilename != null) err(e.key + ': a ' + fmt + ' record must not name an assetPath or suggestedFilename');
      if (p) err(e.key + ': a ' + fmt + ' record must not have a public preview');
      if (e.record.portraitBackground || e.record.states || e.record.views || e.record.pages || e.record.layers) err(e.key + ': a ' + fmt + ' record must not nest art');
      continue;
    }
    if (container) {
      const kids = records.filter((k) => k.key.startsWith(e.key + '#'));
      if (SELECTED.includes(st) && !kids.some((k) => SELECTED.includes(statusOf(k)))) err(e.key + ': selected container without any selected view/page/layer');
      continue;
    }
    if (SELECTED.includes(st) && !p) err(e.key + ': ' + st + ' but has no public preview (register it with tools/sync/register-art.mjs)');
    if (p && !SELECTED.includes(st)) err(e.key + ': REGRESSION - a selected image is previewed, but the record now says ' + st);
    if (p) {
      previewed++;
      let buf = null;
      try { buf = fs.readFileSync(path.join(ROOT, p.file)); } catch (x) { err(e.key + ': preview file ' + p.file + ' is missing'); }
      if (buf) {
        if (sha256(buf) !== p.sha256) err(e.key + ': ' + p.file + ' bytes do not match the recorded SHA-256');
        const c = checkContract(e, buf);
        c.problems.forEach((m) => err(e.key + ': ' + m));
      }
      if (e.path && p.file !== 'assets/selected/' + e.path) err(e.key + ': preview ' + p.file + ' does not mirror assetPath ' + e.path);
    }
  }
  Object.keys(preview.images).forEach((k) => { if (!byKey.has(k)) err('artwork-preview: ' + k + ' names no artwork record'); });
  // Every file in the package is registered.
  const files = new Set(Object.values(preview.images).map((p) => p.file));
  const walk = (dir) => (fs.existsSync(dir) ? fs.readdirSync(dir, { withFileTypes: true }).flatMap((d) => (d.isDirectory() ? walk(path.join(dir, d.name)) : [path.join(dir, d.name)])) : []);
  walk(path.join(ROOT, 'assets/selected')).map((f) => path.relative(ROOT, f).split(path.sep).join('/')).filter((f) => !/\.DS_Store$/.test(f))
    .forEach((f) => { if (!files.has(f)) err('assets/selected: ' + f + ' is not registered in story/artwork-preview.json'); });

  // Integration ----------------------------------------------------------------------------------
  if (integration) {
    const reported = new Map(integration.images.map((i) => [i.key, i]));
    for (const i of integration.images) {
      const e = byKey.get(i.key);
      if (!e) { err('game-integration: ' + i.key + ' names no artwork record'); continue; }
      const st = statusOf(e);
      if (st !== 'integrated' && st !== 'reused') err(i.key + ': the game build uses it, but its status is ' + st + ' (should be integrated)');
      const p = preview.images[i.key];
      if (p && p.sha256 !== i.sha256) err(i.key + ': the game uses different pixels (' + i.sha256.slice(0, 12) + ') than the public preview (' + p.sha256.slice(0, 12) + ')');
    }
    for (const e of records) {
      if (e.layer || e.record.views || e.record.pages || e.record.layers) continue;
      if (statusOf(e) === 'integrated' && !reported.has(e.key)) err(e.key + ': marked integrated, but game build ' + integration.game.commit.slice(0, 12) + ' does not report it');
    }
    notes.push('game build ' + integration.game.commit.slice(0, 12) + ' consumed storyboard ' + integration.storyboard.revision.slice(0, 12) + ' (' + integration.images.length + ' images)');
  } else if (records.some((e) => statusOf(e) === 'integrated')) err('story/game-integration.json is missing, so no `integrated` status can be verified');

  return { ok: !errors.length, errors, notes, stats: { chapters: Object.keys(chapters).length, nodes, routes, artRecords: records.filter((e) => !e.layer).length, statuses: counts, previewed } };
}

if (process.argv[1] && fs.realpathSync(path.resolve(process.argv[1])) === fs.realpathSync(fileURLToPath(import.meta.url))) {
  const r = checkCanon();
  if (process.argv.includes('--json')) console.log(JSON.stringify(r, null, 2));
  else {
    console.log('Canonical storyboard check');
    console.log('  ' + r.stats.chapters + ' chapters, ' + r.stats.nodes + ' nodes, ' + r.stats.routes + ' routes; ' + r.stats.artRecords + ' art records ('
      + Object.entries(r.stats.statuses).sort().map(([k, v]) => v + ' ' + k).join(', ') + '); ' + r.stats.previewed + ' previewed');
    r.notes.forEach((n) => console.log('  - ' + n));
    r.errors.forEach((m) => console.log('  x ' + m));
    console.log(r.ok ? 'RESULT: OK' : 'RESULT: ' + r.errors.length + ' ERROR(S)');
  }
  process.exitCode = r.ok ? 0 : 1;
}
