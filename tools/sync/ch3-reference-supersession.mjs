// Batch D historical approved-source references vs the canonical registry (used by stage-ch3-batch04-review.mjs).
//
// The pinned Batch D v01 review gallery (e65f42c, immutable) records the 23 approved selections it was reviewed
// against (references/approved-sources.json). Every one must still be the canonical selected preview, byte for
// byte, with exactly ONE recorded exception: Nate's later approved replacement of Paper Emergency v03 by v04
// (2026-11-22, docs/103 Paper Emergency v04 addendum). That reference passes only when ALL of these hold:
//   - the reference is the original v03 (ac0f7c44...) and the canonical preview is exactly v04 (93a48082...),
//     in the registry and in the preview file's bytes;
//   - the preserved v03 history copy still has its original hash;
//   - the record is still `approved` with no production assetPath, and its notes name both hashes.
// Any other difference, for this key or any other, fails. The gallery itself is never modified.
export const PAPER_EMERGENCY_V04 = Object.freeze({
  key: 'scenes:pavilion_reboot/paper_emergency',
  record: 'pavilion_reboot/paper_emergency',
  historicalSha256: 'ac0f7c44d267dd54897507ae3b8b02959a5b76f4fcd9d0418b77b8fdb777ba7e',
  currentSha256: '93a48082124600b1afeb45e5ea54856bf253e858e55111295e9d9c26919bc978',
  historyFile: 'docs/artwork-history/chapter-03/pre-v04-paper-emergency-2026-11-22/CH3-B06-paper-emergency-approved-v03.png',
  approved: '2026-11-22 (Nate, Paper Emergency v04 selection; docs/103 addendum)'
});
export const SUPERSESSIONS = Object.freeze([PAPER_EMERGENCY_V04]);
export const REFERENCE_COUNT = 23;

// refs: approved-sources.json; previews: artwork-preview.json images; art: artwork.draft.json;
// readRepo(rel) -> Buffer (canonical repository file); reviewDigest(reviewFile) -> sha256 of the pinned gallery file.
export function checkApprovedReferences({ refs, previews, art, readRepo, reviewDigest, digest }) {
  const fail = (msg) => { const e = new Error(msg); e.code = 'ERR_REFERENCE'; throw e; };
  const keys = Object.keys(refs);
  if (keys.length !== REFERENCE_COUNT) fail('expected ' + REFERENCE_COUNT + ' approved-source references, found ' + keys.length);
  const strict = [], superseded = [];
  for (const key of keys) {
    const r = refs[key];
    if (reviewDigest(r.reviewFile) !== r.sha256) fail(key + ': pinned review file ' + r.reviewFile + ' does not match its recorded sha256');
    const p = previews[key];
    if (!p) fail(key + ': no canonical selected preview');
    if (p.sha256 === r.sha256) {
      if (digest(readRepo(p.file)) !== r.sha256) fail(key + ': canonical preview bytes differ from ' + r.sha256);
      strict.push(key);
      continue;
    }
    const s = SUPERSESSIONS.find((x) => x.key === key);
    if (!s) fail(key + ': canonical preview ' + p.sha256 + ' differs from the approved reference ' + r.sha256 + ' (no recorded supersession)');
    if (r.sha256 !== s.historicalSha256) fail(key + ': reference ' + r.sha256 + ' is not the recorded historical selection ' + s.historicalSha256);
    if (p.sha256 !== s.currentSha256) fail(key + ': canonical preview ' + p.sha256 + ' is not the recorded approved replacement ' + s.currentSha256);
    if (digest(readRepo(p.file)) !== s.currentSha256) fail(key + ': canonical preview bytes are not the approved replacement ' + s.currentSha256);
    let history;
    try { history = readRepo(s.historyFile); } catch (e) { fail(key + ': preserved historical copy ' + s.historyFile + ' is missing'); }
    if (digest(history) !== s.historicalSha256) fail(key + ': preserved historical copy ' + s.historyFile + ' no longer has its original sha256 ' + s.historicalSha256);
    const rec = art.scenes[s.record];
    if (!rec || rec.status !== 'approved' || rec.assetPath !== null) fail(key + ': record must stay approved with no production assetPath');
    if (!String(rec.notes).includes(s.currentSha256) || !String(rec.notes).includes(s.historicalSha256)) fail(key + ': record notes must name the replacement and the historical selection');
    superseded.push({ key, historicalSha256: s.historicalSha256, currentSha256: s.currentSha256, historyFile: s.historyFile, approved: s.approved });
  }
  if (strict.length + superseded.length !== REFERENCE_COUNT || superseded.length > SUPERSESSIONS.length) fail('reference accounting');
  return { strict, superseded };
}
