#!/usr/bin/env node
// Art publishing + integration verification for the canonical storyboard (docs/105).
//
// Registers selected artwork: copies the exact selected PNG into the curated public preview package
// (assets/selected/), records its provenance and hash in story/artwork-preview.json, and raises the
// record's status in story/artwork.draft.json. Status is never lowered.
//
//   One image (Art Director / owner selection = approval):
//     node tools/sync/register-art.mjs --key scenes:biology_park/formal_entrance --file <png> \
//       --source-repo InterstellarHarvest/CYOA --source-ref <branch> --source-commit <sha> --source-path <path> [--status approved]
//   A batch (Gameplay PMO, from the game's `tools/story-sync/sync.js publish`):
//     node tools/sync/register-art.mjs --batch <batch.json> [--integration <game-integration.json>]
//   Options: --dry-run reports without writing.
//
// batch.json: { "entries": [ { key, file, status, source: { repo, ref, commit, path } } ] }
// --integration copies a game integration report to story/game-integration.json (verified by
// tools/sync/check-canon.mjs: every `integrated` record must appear in it, and vice versa).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { artRecords, checkContract, sha256, readJson, writeJson } from './lib.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const ART = path.join(ROOT, 'story/artwork.draft.json');
const PREVIEW = path.join(ROOT, 'story/artwork-preview.json');
const PACKAGE = 'assets/selected';
const RANK = { 'not-started': 0, prompted: 1, generated: 2, approved: 3, integrated: 4, reused: 4 };

// Where the preview copy lives: the production path when the record has one, otherwise a
// pending-integration path derived from the key (never written back as an assetPath).
export function previewPath(entry) {
  if (entry.path) return PACKAGE + '/' + entry.path;
  const slug = entry.key.replace(/^([a-zA-Z]+):/, '$1/').replace(/[#:]/g, '/').replace(/[^a-zA-Z0-9_./-]/g, '_');
  return PACKAGE + '/pending-integration/' + slug + '.png';
}

export function emptyPreview() {
  return { schema: 'cyoa-storyboard-artwork-preview-v1',
    about: 'Storyboard-only. Curated public copies of SELECTED artwork (approved, integrated or reused), with exact source provenance. Written by tools/sync/register-art.mjs; checked by tools/sync/check-canon.mjs. The game importer never reads this file.',
    images: {} };
}

export function register(entries, opts = {}) {
  const art = readJson(ART);
  const preview = fs.existsSync(PREVIEW) ? readJson(PREVIEW) : emptyPreview();
  const byKey = new Map(artRecords(art).map((e) => [e.key, e]));
  const log = [], errors = [];
  for (const req of entries) {
    const e = byKey.get(req.key);
    if (!e) { errors.push(req.key + ': no such artwork record'); continue; }
    if (e.record.views || e.record.pages || e.record.layers) { errors.push(req.key + ': is a container; register its views/pages/layers'); continue; }
    const status = req.status || 'approved';
    if (!['approved', 'integrated', 'reused'].includes(status)) { errors.push(req.key + ': status must be approved, integrated or reused'); continue; }
    const src = req.source || {};
    for (const k of ['repo', 'commit', 'path']) if (!src[k]) errors.push(req.key + ': source.' + k + ' is required (provenance)');
    if (src.commit && !/^[0-9a-f]{40}$/.test(src.commit)) errors.push(req.key + ': source.commit must be a full 40-hex SHA');
    if (src.path && /(^|\/)(originals|source)\//.test(src.path)) errors.push(req.key + ': originals/ and source/ masters are never published');
    let buf;
    try { buf = fs.readFileSync(req.file); } catch (err) { errors.push(req.key + ': cannot read ' + req.file); continue; }
    const c = checkContract(e, buf);
    if (c.problems.length) { errors.push(req.key + ': ' + c.problems.join('; ')); continue; }
    if (errors.some((m) => m.startsWith(req.key + ':'))) continue;
    const hash = sha256(buf), rel = previewPath(e);
    const clash = Object.entries(preview.images).find(([k, v]) => k !== req.key && v.file === rel && v.sha256 !== hash);
    if (clash) { errors.push(req.key + ': ' + rel + ' already holds different pixels for ' + clash[0]); continue; }
    const before = preview.images[req.key];
    preview.images[req.key] = { file: rel, sha256: hash, size: [c.png.width, c.png.height], alpha: c.contract.alpha || (c.png.transparent ? 'transparent' : 'opaque'),
      source: { repo: src.repo, ...(src.ref ? { ref: src.ref } : {}), commit: src.commit, path: src.path } };
    // Status: raise only. A layer inherits its portrait's status, so it is not written.
    const target = e.layer ? null : e.record;
    const was = target ? target.status || 'not-started' : null;
    if (target && RANK[status] > (RANK[was] ?? 0)) target.status = status;
    // A container (complete views / pages) is as advanced as its least advanced selected child.
    if (e.parent && !e.layer && (e.parent.views || e.parent.pages)) {
      const kids = e.parent.views ? Object.values(e.parent.views) : e.parent.pages;
      const lo = kids.reduce((m, k) => Math.min(m, RANK[k.status] ?? 0), 9);
      const name = Object.keys(RANK).find((s) => RANK[s] === lo && s !== 'reused');
      if (lo >= RANK.approved && RANK[name] > (RANK[e.parent.status] ?? 0)) e.parent.status = name;
    }
    log.push((before && before.sha256 === hash ? '= ' : before ? '~ ' : '+ ') + req.key + ' -> ' + rel + (target && target.status !== was ? ' (status ' + was + ' -> ' + target.status + ')' : ''));
    if (!opts.dryRun) { fs.mkdirSync(path.dirname(path.join(ROOT, rel)), { recursive: true }); fs.writeFileSync(path.join(ROOT, rel), buf); }
  }
  if (errors.length) return { ok: false, errors, log };
  preview.images = Object.fromEntries(Object.keys(preview.images).sort().map((k) => [k, preview.images[k]]));
  if (!opts.dryRun) { writeJson(ART, art); writeJson(PREVIEW, preview); }
  return { ok: true, errors, log };
}

function main(argv) {
  const args = argv.slice(2), val = (f) => { const i = args.indexOf(f); return i === -1 ? undefined : args[i + 1]; };
  const dryRun = args.includes('--dry-run');
  let entries;
  if (val('--batch')) entries = readJson(val('--batch')).entries;
  else if (val('--key')) entries = [{ key: val('--key'), file: val('--file'), status: val('--status'),
    source: { repo: val('--source-repo'), ref: val('--source-ref'), commit: val('--source-commit'), path: val('--source-path') } }];
  else { console.log(fs.readFileSync(fileURLToPath(import.meta.url), 'utf8').split('\n').slice(1, 18).map((l) => l.replace(/^\/\/ ?/, '')).join('\n')); return 2; }
  const r = register(entries, { dryRun });
  r.log.forEach((l) => console.log('  ' + l));
  if (!r.ok) { r.errors.forEach((m) => console.log('  x ' + m)); console.log('RESULT: REFUSED - nothing was written.'); return 1; }
  const integ = val('--integration');
  if (integ && !dryRun) { const rep = readJson(integ); if (rep.schema !== 'cyoa-game-integration-v1') { console.log('x integration report schema'); return 1; } writeJson(path.join(ROOT, 'story/game-integration.json'), rep); console.log('  wrote story/game-integration.json (game ' + rep.game.commit.slice(0, 12) + ')'); }
  console.log('RESULT: ' + (dryRun ? 'DRY RUN, ' : '') + entries.length + ' image(s) registered. Next: node tools/sync/check-canon.mjs');
  return 0;
}

if (process.argv[1] && fs.realpathSync(path.resolve(process.argv[1])) === fs.realpathSync(fileURLToPath(import.meta.url))) process.exitCode = main(process.argv);
