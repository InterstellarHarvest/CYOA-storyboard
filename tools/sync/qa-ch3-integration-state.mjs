#!/usr/bin/env node
// Regression checks for the Chapter 3 integration-state rule (tools/sync/ch3-integration-state.mjs), which the main-only
// Pages helpers stage-ch3-batch04-review.mjs and ch3-reference-supersession.mjs apply. Offline.
//   node tools/sync/qa-ch3-integration-state.mjs
//
// 1. Both legitimate states pass, built explicitly from real records whatever the repository holds now:
//    approved with no production path; integrated at exactly its suggestedFilename by a game build that used exactly
//    the approved bytes there, its preview citing that build.
// 2. Every other state is refused: wrong hashes, wrong paths, missing or foreign reports, status regressions, previews
//    that do not cite the build.
// 3. The repository as it is now: all 29 Chapter 3 selections are in ONE legitimate state, every preview holds the
//    approved bytes, and once integrated, one game build is cited and no pending-integration preview copy remains.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { ch3IntegrationState, CH3_GAME_REPO } from './ch3-integration-state.mjs';
import { artRecords } from './lib.mjs';
import { previewPath } from './register-art.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const R = (rel) => fs.readFileSync(path.join(ROOT, rel));
const digest = (b) => createHash('sha256').update(b).digest('hex');
const clone = (v) => JSON.parse(JSON.stringify(v));
const results = [];
const ok = (name) => results.push(name);
const art = JSON.parse(R('story/artwork.draft.json'));
const previews = JSON.parse(R('story/artwork-preview.json')).images;
const firstSha = (rec) => { const m = /SHA-256[^0-9a-f]{0,3}([0-9a-f]{64})/.exec(String(rec.notes || '')); return m && m[1]; };

// The 29 Chapter 3 selections: every record whose production file belongs to the Pavilion reboot.
const ch3 = artRecords(art).filter((e) => e.record && /^art\/(scenes|portraits)\/pavilion_reboot\//.test(e.record.suggestedFilename || ''));
assert.equal(ch3.length, 29, '29 Chapter 3 selections (14 scenes, 8 conversation backgrounds, 7 poses)');
ok('the registry holds exactly 29 Chapter 3 selections');

// 1-2. Explicit states on two real records: a Batch D conversation background and a pose.
const GAME = { repo: CH3_GAME_REPO, branch: 'agent/example', commit: 'c'.repeat(40) };
for (const key of ['scenes:pavilion_reboot/service_exit#portraitBackground', 'portraits:pavilion_attendant:quiet']) {
  const e = ch3.find((x) => x.key === key);
  assert.ok(e, key);
  const sha = firstSha(e.record), at = e.record.suggestedFilename, file = 'assets/selected/' + at;
  assert.match(sha || '', /^[0-9a-f]{64}$/, key + ' names its approved SHA-256 first');
  const rec = (status, assetPath, over = {}) => ({ ...clone(e.record), status, assetPath, ...over });
  const report = (images, game = GAME) => ({ schema: 'cyoa-game-integration-v1', game, images });
  const used = (s = sha, p = at, k = key) => [{ key: k, path: p, sha256: s, kind: 'x' }];
  const pv = (over = {}, src = {}) => ({ file, sha256: sha, source: { repo: GAME.repo, ref: GAME.branch, commit: GAME.commit, path: at, ...src }, ...over });
  const state = (o) => ch3IntegrationState({ key, sha256: sha, ...o });
  const refused = (name, o, re) => { assert.throws(() => state(o), (err) => err.code === 'ERR_CH3_STATE' && re.test(err.message), name); ok(key + ': ' + name); };

  assert.equal(state({ record: rec('approved', null), integration: null, preview: { file: previewPath({ key }), sha256: sha, source: { repo: 'InterstellarHarvest/CYOA-storyboard' } } }), 'approved');
  ok(key + ': approved with no production path passes (before integration)');
  assert.equal(state({ record: rec('integrated', at), integration: report(used()), preview: pv() }), 'integrated');
  ok(key + ': integrated at its suggestedFilename by a build that used exactly the approved bytes, preview citing it, passes');

  // Status regressions and premature paths.
  for (const s of ['generated', 'prompted', 'not-started', 'reused', undefined]) refused('status ' + s + ' is refused', { record: rec(s, null), integration: report(used()), preview: pv() }, /neither approved nor integrated/);
  refused('approved WITH a production path is refused', { record: rec('approved', at), integration: report(used()), preview: pv() }, /no production assetPath before gameplay integration/);
  // Wrong paths.
  refused('integrated with no production path is refused', { record: rec('integrated', null), integration: report(used()), preview: pv() }, /exactly its suggestedFilename/);
  const other = at.replace(/\.png$/, '_other.png');
  refused('integrated at a path other than its suggestedFilename is refused (even when the report agrees)', { record: rec('integrated', other), integration: report(used(sha, other)), preview: pv({ file: 'assets/selected/' + other }, { path: other }) }, /exactly its suggestedFilename/);
  refused('a report that used the image at another path is refused', { record: rec('integrated', at), integration: report(used(sha, other)), preview: pv() }, /did not use exactly/);
  // Missing or foreign reports.
  refused('integrated with no report is refused', { record: rec('integrated', at), integration: null, preview: pv() }, /without a game integration report/);
  refused('a report with another schema is refused', { record: rec('integrated', at), integration: { ...report(used()), schema: 'x' }, preview: pv() }, /without a game integration report/);
  refused('a report that does not list the record is refused', { record: rec('integrated', at), integration: report(used(sha, at, 'scenes:pavilion_reboot/arrival')), preview: pv() }, /did not use exactly/);
  refused('a report listing the record twice is refused', { record: rec('integrated', at), integration: report(used().concat(used())), preview: pv() }, /did not use exactly/);
  refused('a report from another repository (the old game name) is refused', { record: rec('integrated', at), integration: report(used(), { ...GAME, repo: 'InterstellarHarvest/CYOA' }), preview: pv({}, { repo: 'InterstellarHarvest/CYOA' }) }, /must name InterstellarHarvest\/out-of-order/);
  refused('a report without a full game commit is refused', { record: rec('integrated', at), integration: report(used(), { ...GAME, commit: 'abc1234' }), preview: pv({}, { commit: 'abc1234' }) }, /full game commit/);
  // Wrong hashes.
  const wrong = 'f'.repeat(64);
  refused('a build that used other bytes is refused', { record: rec('integrated', at), integration: report(used(wrong)), preview: pv() }, /did not use exactly/);
  refused('a preview registered with other bytes is refused (approved)', { record: rec('approved', null), integration: null, preview: pv({ sha256: wrong }) }, /is not the approved/);
  refused('a preview registered with other bytes is refused (integrated)', { record: rec('integrated', at), integration: report(used()), preview: pv({ sha256: wrong }) }, /is not the approved/);
  assert.throws(() => ch3IntegrationState({ key, record: rec('approved', null), sha256: null }), /no approved SHA-256/); ok(key + ': no approved SHA-256 is refused');
  // Previews that do not cite the build.
  refused('an integrated preview still at its pending-integration path is refused', { record: rec('integrated', at), integration: report(used()), preview: pv({ file: previewPath({ key }) }) }, /an integrated preview lives at/);
  refused('an integrated preview still citing the approved selection is refused', { record: rec('integrated', at), integration: report(used()), preview: pv({}, { repo: 'InterstellarHarvest/CYOA-storyboard', commit: 'e'.repeat(40) }) }, /an integrated preview lives at/);
  refused('an integrated preview citing another game build is refused', { record: rec('integrated', at), integration: report(used()), preview: pv({}, { commit: 'd'.repeat(40) }) }, /an integrated preview lives at/);
  assert.throws(() => ch3IntegrationState({ key, record: null, sha256: sha }), /no canonical record/); ok(key + ': a missing record is refused');
}

// 3. The repository now.
const gi = fs.existsSync(path.join(ROOT, 'story/game-integration.json')) ? JSON.parse(R('story/game-integration.json')) : null;
const states = new Map();
for (const e of ch3) {
  const sha = firstSha(e.record), pv = previews[e.key];
  assert.ok(pv, e.key + ' has a canonical preview');
  assert.equal(digest(R(pv.file)), sha, e.key + ': the preview file holds exactly the approved bytes its notes name first');
  const s = ch3IntegrationState({ key: e.key, record: e.record, sha256: sha, integration: gi, preview: pv });
  if (s === 'approved') assert.equal(pv.source.repo, 'InterstellarHarvest/CYOA-storyboard', e.key + ': an approved preview cites its approved selection');
  else assert.ok(!fs.existsSync(path.join(ROOT, previewPath({ key: e.key }))), e.key + ': no pending-integration preview copy remains once integrated');
  assert.ok(String(e.record.notes).includes('NOT proven'), e.key + ': the accepted native-grid authorship limitation stays recorded');
  states.set(s, (states.get(s) || 0) + 1);
}
assert.equal(states.size, 1, 'all 29 Chapter 3 selections share one state: ' + JSON.stringify([...states]));
const now = [...states.keys()][0];
if (now === 'integrated') assert.equal(new Set(ch3.map((e) => previews[e.key].source.commit)).size, 1, 'one game build integrated all 29');
ok('repository: all 29 Chapter 3 selections ' + now + ', every preview byte-exact to its approved SHA-256' + (now === 'integrated' ? ', one game build (' + gi.game.commit.slice(0, 12) + '), no pending-integration copy left' : ''));
console.log(JSON.stringify({ result: 'PASS', state: now, checks: results.length, results }, null, 1));
