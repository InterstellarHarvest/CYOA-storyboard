#!/usr/bin/env node
// Read-only approval/source verification, with optional exact-byte TEMPORARY staging.
// Never registers artwork or assigns gameplay paths. See docs/119, 2026-11-20.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { readJson, sha256, artRecords, checkContract } from './lib.mjs';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const args=process.argv.slice(2),value=(flag,fallback)=>args.includes(flag)?args[args.indexOf(flag)+1]:fallback;
const DECISION='docs/119_OUT_OF_ORDER_CH3_CURRENT_SELECTED_ARTWORK_20261120.json';
const BATCH='docs/119_OUT_OF_ORDER_CH3_CURRENT_APPROVAL_REGISTRATION_BATCH_20261120.json';
const V04='7bf1f426f3a1d5dba14e7a1bd56ece86a4d23bdb',V02='5e0449b3da84764176f9744f5624a88868f5fdcb';
const GALLERY='tools/prologue-art-lab/assets/review/chapter-03-batch03-2026-11-19/';
const expected={
 'CH3-C01-urgency':'scenes:pavilion_reboot/urgency_stage',
 'CH3-C02-urgency-bg':'scenes:pavilion_reboot/urgency_stage#portraitBackground',
 'CH3-C03-locomotion':'scenes:pavilion_reboot/locomotion_stage',
 'CH3-C04-surprise':'scenes:pavilion_reboot/surprise_stage',
 'CH3-C05-surprise-bg':'scenes:pavilion_reboot/surprise_stage#portraitBackground',
 'CH3-A04-verification-continuity':'scenes:pavilion_reboot/human_verification_stage',
 'CH3-A05-verification-bg-continuity':'scenes:pavilion_reboot/human_verification_stage#portraitBackground',
 'CH3-C06-presenter-excited':'portraits:pavilion_presenter:excited',
 'CH3-C07-presenter-alarmed':'portraits:pavilion_presenter:alarmed',
 'CH3-B07-attendant-alarmed':'portraits:pavilion_attendant:alarmed',
};
const gitBlob=(commit,file)=>execFileSync('git',['show',`${commit}:${file}`],{cwd:ROOT,maxBuffer:16*1024*1024});
const blobId=buf=>crypto.createHash('sha1').update(Buffer.from(`blob ${buf.length}\0`)).update(buf).digest('hex');

function main(){
 const decision=readJson(path.resolve(ROOT,value('--decision',DECISION)));
 const batch=readJson(path.resolve(ROOT,value('--batch',BATCH)));
 assert.equal(decision.status,'approved');assert.equal(decision.selected,true);assert.equal(decision.approved,true);
 assert.equal(decision.gameplayIntegrationAuthorized,false);assert.equal(decision.beginBatchDAuthorized,false);
 assert.equal(decision.gallerySourceCommit,V04);assert.equal(decision.retainedForegroundSourceCommit,V02);
 assert.equal(decision.candidates.length,10);assert.equal(batch.entries.length,10);
 const candidates=new Map(decision.candidates.map(c=>[c.candidateId,c]));assert.equal(candidates.size,10);
 assert.deepEqual([...candidates.keys()].sort(),Object.keys(expected).sort());
 const entries=new Map(batch.entries.map(e=>[e.key,e]));assert.equal(entries.size,10);
 const catalog=new Map(artRecords(readJson(path.join(ROOT,'story/artwork.draft.json'))).map(e=>[e.key,e]));
 const history=decision.historicalOwnerDecision;const historyBytes=fs.readFileSync(path.join(ROOT,history.file));
 assert.equal(sha256(historyBytes),history.sha256);assert.deepEqual(historyBytes,gitBlob(history.sourceCommit,history.file));
 const oldById=new Map(JSON.parse(historyBytes).candidates.map(c=>[c.candidateId,c]));
 const inputs=[];const verified=[];
 for(const [id,c] of candidates){
  const retained=id.startsWith('CH3-C06-')||id.startsWith('CH3-C07-')||id.startsWith('CH3-B07-');
  const version=retained?'v02':'v04',folder=retained?'v02-localized-corrections':'v04-perspective-corrections';
  assert.equal(c.key,expected[id]);assert.equal(c.selectedVersion,version);assert.equal(c.retainedUnchanged,retained);
  assert.equal(c.status,'approved');assert.equal(c.selected,true);assert.equal(c.approved,true);assert.equal(c.assetPath,null);
  assert.equal(c.file,`${GALLERY}${folder}/candidates/${id}-${version}.png`);
  assert.equal(c.source.repo,'InterstellarHarvest/CYOA-storyboard');assert.equal(c.source.ref,'art/ch3-pavilion-batch03-20261119');
  assert.equal(c.source.commit,retained?V02:V04);assert.equal(c.source.path,c.file);
  const entry=entries.get(c.key);assert.ok(entry);assert.equal(entry.file,c.file);assert.equal(entry.status,'approved');
  assert.deepEqual(entry.source,c.source);assert.equal(entry.expectedSha256,c.sha256);
  const bytes=gitBlob(c.source.commit,c.file);assert.equal(sha256(bytes),c.sha256,`${id}: immutable source SHA-256`);
  assert.equal(blobId(bytes),c.gitBlob,`${id}: immutable Git blob`);
  if(fs.existsSync(path.join(ROOT,c.file)))assert.deepEqual(fs.readFileSync(path.join(ROOT,c.file)),bytes);
  const checked=checkContract(catalog.get(c.key),bytes);assert.deepEqual(checked.problems,[],c.key);
  assert.ok(checked.png.decoded);assert.equal(checked.png.depth,8);assert.equal(checked.png.partial,0);
  assert.deepEqual([checked.png.width,checked.png.height],c.dimensions);
  assert.equal(checked.png.colorType,retained?6:2);assert.ok(retained?checked.png.transparent>0:checked.png.transparent===0);
  assert.equal(catalog.get(c.key).path,null);
  if(retained){
   const old=oldById.get(id);assert.equal(c.sha256,old.sha256);assert.equal(c.file,old.file);assert.deepEqual(c.source,old.source);
   assert.deepEqual(gitBlob(V04,c.file),bytes); // identical retained file in the newer full gallery
  }
  inputs.push({entry,bytes,id});verified.push({candidateId:id,key:c.key,version,sha256:c.sha256,gitBlob:c.gitBlob,size:c.dimensions,partialAlpha:0,source:c.source});
 }
 assert.equal(decision.supersededCanonicalSelections.length,2);
 for(const old of decision.supersededCanonicalSelections){
  const bytes=fs.readFileSync(path.join(ROOT,old.preservedFile));assert.equal(sha256(bytes),old.sha256);
  assert.deepEqual(bytes,gitBlob(old.priorCanonicalCommit,old.priorSelectedPreview.file));
  const source=old.priorSelectedPreview.source;assert.deepEqual(bytes,gitBlob(source.commit,source.path));
  assert.equal(blobId(bytes),old.priorPreviewGitBlob);
  assert.deepEqual(bytes,gitBlob(V04,GALLERY+old.galleryHistoricalReference));
  const replacement=decision.candidates.find(c=>c.key===old.key);assert.equal(replacement.sha256,old.replacedBySha256);
  assert.deepEqual(replacement.source,old.replacedBySource);assert.equal(replacement.replacesCanonicalSelection,true);
 }
 const previews=readJson(path.join(ROOT,'story/artwork-preview.json')).images;
 const report={result:'PASS',scope:'Immutable approval inputs only; no canonical registration or gameplay integration.',
  selections:verified,counts:{total:10,v04Environments:7,retainedV02Foregrounds:3,archivedPriorSelections:2,
  expectedNewPreviewsOnThisCheckout:verified.filter(c=>!previews[c.key]).length,
  expectedChangedPreviewsOnThisCheckout:verified.filter(c=>previews[c.key]&&previews[c.key].sha256!==c.sha256).length},
  historicalOwnerDecisionUnchanged:true,oldApprovedFilesAndProvenancePreserved:true,nativeGridAuthorship:'UNRESOLVED / UNPROVEN; accepted by Nate.'};
 if(args.includes('--stage')){
  const directory=path.resolve(value('--stage'));
  const relative=path.relative(ROOT,directory);
  assert.ok(relative.startsWith('..'+path.sep)||path.isAbsolute(relative),'Use temporary staging outside the checkout.');
  fs.mkdirSync(directory,{recursive:true});assert.equal(fs.readdirSync(directory).length,0,'Use an empty staging directory.');
  const staged=inputs.map(({entry,bytes,id},i)=>{const file=path.join(directory,`${String(i+1).padStart(2,'0')}-${path.basename(entry.file)}`);fs.writeFileSync(file,bytes);return {...entry,file};});
  const file=path.join(directory,'batch.json');fs.writeFileSync(file,JSON.stringify({...batch,entries:staged},null,2)+'\n');
  report.staging={directory,batch:file};
 }
 if(args.includes('--output'))fs.writeFileSync(path.resolve(value('--output')),JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify(report,null,2));
}
try{main();}catch(e){console.error('REFUSED: '+e.message);process.exitCode=1;}
