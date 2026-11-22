#!/usr/bin/env node
// Regression checks for the Batch D approved-source reference guard (tools/sync/ch3-reference-supersession.mjs),
// which tools/sync/stage-ch3-batch04-review.mjs runs inside the Pages build. Offline; no gallery checkout needed:
// the 23 references are a byte-exact copy of the pinned gallery file (e65f42c, sha256 pinned below), and the
// gallery files' own hashes are verified end to end by the Pages staging step.
//   node tools/sync/qa-ch3-reference-supersession.mjs
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { checkApprovedReferences, PAPER_EMERGENCY_V04 as S } from './ch3-reference-supersession.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const digest = (b) => createHash('sha256').update(b).digest('hex');
const R = (rel) => fs.readFileSync(path.join(ROOT, rel));
const FIXTURE = 'tools/sync/qa-fixtures/ch3-batch04-v01-approved-sources.json';
const FIXTURE_SHA = 'd50d2948303be141cc4ede6bcaff0f6099d813e62f94e43ed3520063b209eb29'; // e65f42c:.../v01/references/approved-sources.json
const results = [];
const ok = (name) => results.push(name);

assert.equal(digest(R(FIXTURE)), FIXTURE_SHA, 'fixture is the byte-exact pinned Batch D reference file');
const refs = JSON.parse(R(FIXTURE));
const art = JSON.parse(R('story/artwork.draft.json'));
const previews = JSON.parse(R('story/artwork-preview.json')).images;
const clone = (v) => JSON.parse(JSON.stringify(v));
// One scenario: registry + files as given (overrides by path), gallery files as recorded.
function run({ p = previews, a = art, files = {}, missing = [] } = {}) {
  const readRepo = (rel) => { if (missing.includes(rel)) throw new Error('ENOENT ' + rel); return rel in files ? files[rel] : R(rel); };
  return checkApprovedReferences({ refs, previews: p, art: a, digest, readRepo, reviewDigest: (f) => Object.values(refs).find((r) => r.reviewFile === f).sha256 });
}
const refused = (scenario, re) => { assert.throws(() => run(scenario), (e) => e.code === 'ERR_REFERENCE' && re.test(e.message)); };
const v03 = R(S.historyFile), v04 = R(previews[S.key].file);
assert.equal(refs[S.key].sha256, S.historicalSha256, 'the pinned reference for Paper Emergency is v03');
assert.equal(digest(v03), S.historicalSha256); assert.equal(digest(v04), S.currentSha256);

// 1. The original v03 configuration (canonical main before the v04 registration) still passes: 23 strict.
{
  const p = clone(previews); p[S.key] = { ...p[S.key], sha256: S.historicalSha256 };
  const r = run({ p, files: { [p[S.key].file]: v03 } });
  assert.equal(r.strict.length, 23); assert.equal(r.superseded.length, 0); ok('original v03 configuration passes: 23 strict, no exception used');
}
// 2. The approved v04 replacement passes: 22 strict + the one recorded supersession.
{
  const r = run();
  assert.equal(r.strict.length, 22); assert.deepEqual(r.superseded.map((x) => x.key), [S.key]);
  assert.ok(!r.strict.includes(S.key)); ok('approved v04 replacement passes: 22 strict + 1 recorded later replacement (Paper Emergency)');
}
// 3. A modified v03 history file fails.
{
  const bad = Buffer.from(v03); bad[bad.length - 30] ^= 1;
  refused({ files: { [S.historyFile]: bad } }, /preserved historical copy .* no longer has its original sha256/); ok('a modified v03 history file fails');
  refused({ missing: [S.historyFile] }, /preserved historical copy .* is missing/); ok('a missing v03 history file fails');
}
// 4. An unexpected replacement hash fails (registry), and v04 registered over the wrong bytes fails (file).
{
  const p = clone(previews); p[S.key] = { ...p[S.key], sha256: 'f'.repeat(64) };
  refused({ p }, /is not the recorded approved replacement/); ok('an unexpected replacement hash fails');
  refused({ files: { [previews[S.key].file]: v03 } }, /canonical preview bytes are not the approved replacement/); ok('a v04 registry entry over non-v04 bytes fails');
}
// 5. Any other mismatched reference fails, including one that tries to reuse the exception.
{
  const others = Object.keys(refs).filter((k) => k !== S.key);
  assert.equal(others.length, 22);
  for (const k of others) {
    const p = clone(previews); p[k] = { ...p[k], sha256: S.currentSha256 };
    refused({ p }, new RegExp('^' + k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ': canonical preview .* \\(no recorded supersession\\)'));
  }
  ok('each of the other 22 references fails on any registry mismatch (no exception applies to them)');
  const k = 'scenes:pavilion_reboot/arrival', bad = Buffer.from(R(previews[k].file)); bad[bad.length - 30] ^= 1;
  refused({ files: { [previews[k].file]: bad } }, /canonical preview bytes differ/); ok('another reference with altered preview bytes fails');
  const r2 = clone(refs); r2[S.key] = { ...r2[S.key], sha256: 'e'.repeat(64) };
  assert.throws(() => checkApprovedReferences({ refs: r2, previews, art, digest, readRepo: R, reviewDigest: (f) => Object.values(r2).find((r) => r.reviewFile === f).sha256 }),
    /is not the recorded historical selection/); ok('a Paper Emergency reference other than v03 fails');
}
// The supersession also requires the record to stay approved, unintegrated and documented.
{
  const a = clone(art); a.scenes[S.record].assetPath = 'art/scenes/pavilion_reboot/paper_emergency.png';
  refused({ a }, /must stay approved with no production assetPath/);
  const b = clone(art); b.scenes[S.record].notes = b.scenes[S.record].notes.split(S.historicalSha256).join('');
  refused({ a: b }, /notes must name/); ok('the exception requires the record approved, no production path, notes naming both hashes');
}
console.log(JSON.stringify({ result: 'PASS', checks: results.length, results }, null, 1));
