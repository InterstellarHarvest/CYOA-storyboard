// Chapter 3 selected-art integration state (game docs/104 sections 8-9). Used by the main-only Pages helpers
// stage-ch3-batch04-review.mjs (Batch D, 9 records) and ch3-reference-supersession.mjs (Paper Emergency v03 -> v04),
// and checked for every Chapter 3 record by qa-ch3-integration-state.mjs.
//
// Exactly two states are legitimate for an approved Chapter 3 selection:
//   approved    status `approved` and no production assetPath (before gameplay integration). The caller checks
//               that the canonical preview still cites the approved selection.
//   integrated  status `integrated` at exactly its suggestedFilename, AND the published game build in
//               story/game-integration.json used exactly the approved SHA-256 at that path for this key (one entry),
//               AND the canonical preview holds those bytes at assets/selected/<assetPath> and cites that game build
//               at that path (written by register-art.mjs through the game's sync.js publish).
// Anything else fails: a status below approved (registered approval is never lowered), approved with a path, integrated
// without a report, by another repository or with other bytes, at another path, or with a preview that does not cite
// the build. The callers still compare the preview file's bytes; nothing here reads or changes an image.
export const CH3_GAME_REPO = 'InterstellarHarvest/out-of-order';

export function ch3IntegrationState({ key, record, sha256, integration, preview }) {
  const fail = (msg) => { const e = new Error(key + ': ' + msg); e.code = 'ERR_CH3_STATE'; throw e; };
  if (!record) fail('no canonical record');
  if (!/^[0-9a-f]{64}$/.test(sha256 || '')) fail('no approved SHA-256 to compare');
  if (preview && preview.sha256 !== sha256) fail('canonical preview ' + preview.sha256 + ' is not the approved ' + sha256);
  if (record.status === 'approved') {
    if (record.assetPath !== null) fail('an approved record has no production assetPath before gameplay integration (found ' + record.assetPath + ')');
    return 'approved';
  }
  if (record.status !== 'integrated') fail('status "' + record.status + '" is neither approved nor integrated (registered approval is never lowered)');
  const at = record.assetPath;
  if (typeof at !== 'string' || !record.suggestedFilename || at !== record.suggestedFilename) fail('integrated only at exactly its suggestedFilename ' + record.suggestedFilename + ' (found ' + at + ')');
  if (!integration || integration.schema !== 'cyoa-game-integration-v1' || !integration.game || !Array.isArray(integration.images)) fail('integrated without a game integration report (story/game-integration.json)');
  const game = integration.game;
  if (game.repo !== CH3_GAME_REPO || !/^[0-9a-f]{40}$/.test(game.commit || '')) fail('the integration report must name ' + CH3_GAME_REPO + ' and a full game commit (found ' + game.repo + ' ' + game.commit + ')');
  const used = integration.images.filter((i) => i.key === key);
  if (used.length !== 1 || used[0].path !== at || used[0].sha256 !== sha256) fail('game build ' + game.commit.slice(0, 12) + ' did not use exactly ' + sha256 + ' at ' + at + ' (report: ' + JSON.stringify(used.map((i) => [i.path, i.sha256])) + ')');
  if (preview) {
    const s = preview.source || {};
    if (preview.file !== 'assets/selected/' + at || s.repo !== game.repo || s.commit !== game.commit || s.path !== at) fail('an integrated preview lives at assets/selected/' + at + ' and cites game build ' + game.commit.slice(0, 12) + ' at that path (found ' + preview.file + ' citing ' + s.repo + ' ' + s.commit + ' ' + s.path + ')');
  }
  return 'integrated';
}
