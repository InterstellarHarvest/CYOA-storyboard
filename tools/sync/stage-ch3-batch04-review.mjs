// Trusted main-only Pages helper: verify immutable v01/v02 history plus the localized v03 correction as data,
// then verify Nate's nine approved Batch D selections (docs/122) against the canonical registry and publish a
// selection receipt OUTSIDE the immutable snapshots. Review-time generated/unselected labels stay untouched.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {decodePng} from './lib.mjs';
import {checkApprovedReferences} from './ch3-reference-supersession.mjs';
const [checkout,site]=process.argv.slice(2);
assert.ok(checkout&&site,'usage: node tools/sync/stage-ch3-batch04-review.mjs <pinned checkout> <site>');
const dir=process.env.CH3_BATCH_D_REVIEW_DIR,version=process.env.CH3_BATCH_D_REVIEW_VERSION;
assert.equal(dir,'tools/prologue-art-lab/assets/review/chapter-03-batch04-2026-11-20');
assert.equal(version,'v03-clapper-correction');
assert.match(process.env.CH3_BATCH_D_REVIEW_COMMIT||'',/^[0-9a-f]{40}$/);
const gallery=path.resolve(checkout,dir),current=path.join(gallery,version),historical=path.join(gallery,'v01'),previousRoot=path.join(gallery,'v02-close-camera-corrections'),dest=path.resolve(site,dir);
const digest=buf=>createHash('sha256').update(buf).digest('hex');
const walk=(root,rel='')=>fs.readdirSync(path.join(root,rel),{withFileTypes:true}).flatMap(e=>{
 assert.ok(!e.isSymbolicLink(),'no review symlinks');
 return e.isDirectory()?walk(root,path.join(rel,e.name)):[path.join(rel,e.name)];
});
assert.deepEqual(fs.readdirSync(gallery).sort(),['v01','v02-close-camera-corrections',version].sort(),'only the three immutable review snapshots');
const safe=(root,rel)=>{
 const f=path.resolve(root,rel);assert.ok(f.startsWith(gallery+path.sep),'review file confined to gallery');return f;
};
const verifyPackage=root=>{
 const sums=new Map(fs.readFileSync(path.join(root,'SHA256SUMS.txt'),'utf8').trim().split('\n').map(line=>{
  const m=line.match(/^([0-9a-f]{64})  (.+)$/);assert.ok(m,'valid checksum line');const file=path.resolve(root,m[2]);
  assert.ok(file.startsWith(root+path.sep),'checksum confined to snapshot');return [m[2],m[1]];
 }));
 const files=walk(root);assert.equal(files.length,sums.size+1,'all files checksummed except checksum manifest itself');
 for(const f of files)if(f!=='SHA256SUMS.txt')assert.equal(digest(fs.readFileSync(path.join(root,f))),sums.get(f),f);
 return {sums,files,manifest:JSON.parse(fs.readFileSync(path.join(root,'manifest.json'),'utf8'))};
};
const history=verifyPackage(historical),previous=verifyPackage(previousRoot),latest=verifyPackage(current);
const oldExpected=new Map(previous.manifest.candidates.map(c=>[c.candidateId,c]));
assert.equal(history.manifest.candidateSourceCommit,'4fc277651c7d05163817d9ab99d0fc3fcf522d47');
const manifest=latest.manifest;
for(const m of [history.manifest,previous.manifest,manifest]){
 assert.equal(m.narrativeBlob,'857ffdf1bc9432cf4bbbfd7819f5f430a06d9036');assert.equal(m.selected,false);assert.equal(m.approved,false);assert.equal(m.assetPath,null);assert.equal(m.candidates.length,9);
}
const expected=new Set(['CH3-D01-service-exit','CH3-D02-service-exit-bg','CH3-D03-attendant-quiet','CH3-D04-presenter-relieved','CH3-D05-backstage','CH3-D06-exterior-exit','CH3-D07-exit-vestibule','CH3-D08-courtesy-stage','CH3-D09-courtesy-stage-bg']);
const revised=new Set(['CH3-D05-backstage']);
const art=JSON.parse(fs.readFileSync('story/artwork.draft.json','utf8')),previews=JSON.parse(fs.readFileSync('story/artwork-preview.json','utf8')).images;
const decisionFile='docs/122_OUT_OF_ORDER_CH3_BATCH_D_SELECTED_ARTWORK_20261120.json',decisionBytes=fs.readFileSync(decisionFile),decision=JSON.parse(decisionBytes);
const batch=JSON.parse(fs.readFileSync('docs/122_OUT_OF_ORDER_CH3_BATCH_D_APPROVAL_REGISTRATION_BATCH_20261120.json','utf8'));
assert.equal(decision.status,'approved');assert.equal(decision.approved,true);assert.equal(decision.selected,true);
assert.equal(decision.sourceCommit,process.env.CH3_BATCH_D_REVIEW_COMMIT);assert.equal(decision.gallerySourceCommit,process.env.CH3_BATCH_D_REVIEW_COMMIT);assert.equal(decision.galleryVersion,version);
assert.equal(decision.sourceManifest.sha256,digest(fs.readFileSync(path.join(current,'manifest.json'))),'decision cites this exact v03 manifest');
const selections=new Map(decision.candidates.map(d=>[d.candidateId,d])),batchEntries=new Map(batch.entries.map(e=>[e.key,e]));
assert.equal(selections.size,9);assert.equal(decision.candidates.length,9);assert.equal(batchEntries.size,9);assert.equal(batch.entries.length,9);
for(const c of manifest.candidates){
 assert.ok(expected.delete(c.candidateId),'unique expected candidate');
 assert.equal(c.status,'generated');assert.equal(c.selected,false);assert.equal(c.approved,false);assert.equal(c.assetPath,null);
 const changed=revised.has(c.candidateId);assert.equal(c.retainedFromPreviousReview,!changed);
 const prior=oldExpected.get(c.candidateId);
 if(changed){assert.equal(c.file,'candidates/CH3-D05-backstage-v03.png');assert.equal(c.candidateSourceCommit,null);assert.equal(c.sourceCommitPinnedByGalleryWorkflow,true);assert.equal(c.sha256,'aa90896023a59454887e9b3bd5b1745cb8b95a5d9737829119abddd9176f4889');}
 else{assert.equal(safe(current,c.file),safe(previousRoot,prior.file));assert.equal(c.candidateSourceCommit,prior.candidateSourceCommit);}
 if(!changed)assert.equal(c.sha256,oldExpected.get(c.candidateId).sha256);
 else assert.equal(c.replacesUnselectedSha256,oldExpected.get(c.candidateId).sha256);
 const bytes=fs.readFileSync(safe(current,c.file));assert.equal(digest(bytes),c.sha256);
 const png=decodePng(bytes);assert.ok(png.decoded);assert.equal(png.depth,8);assert.equal(png.partial,0);assert.deepEqual([png.width,png.height],c.dimensions);
 const portrait=c.record.startsWith('portraits:');assert.equal(png.colorType,portrait?6:2);assert.ok(portrait?png.transparent>0:png.transparent===0);
 assert.deepEqual(c.dimensions,portrait||c.record.endsWith('#portraitBackground')?[564,278]:[314,206]);
 const zoom=decodePng(fs.readFileSync(safe(current,c.preview4x)));assert.deepEqual([zoom.width,zoom.height],c.dimensions.map(x=>x*4));
 assert.equal(digest(fs.readFileSync(safe(current,c.source.original))),c.source.sha256);
 const [group,key]=c.record.split(/:(.*)/s),record=key.endsWith('#portraitBackground')?art[group][key.split('#')[0]].portraitBackground:art[group][key];
 // Canonical registry (docs/122, PR #17): the v03 mapping is Nate's approved selection, registered byte-exact.
 const d=selections.get(c.candidateId);assert.ok(d,'approved selection for '+c.candidateId);assert.equal(d.key,c.record);assert.equal(d.sha256,c.sha256);assert.equal(path.resolve(checkout,d.file),safe(current,c.file),'selection is the exact v03-mapped file');
 assert.equal(d.selectedVersion,changed?'v03':path.basename(d.file,'.png').slice(-3));assert.deepEqual(d.source,{repo:'InterstellarHarvest/CYOA-storyboard',ref:'art/ch3-pavilion-batch04-20261120',commit:process.env.CH3_BATCH_D_REVIEW_COMMIT,path:d.file});
 assert.equal(d.status,'approved');assert.equal(d.approved,true);assert.equal(d.selected,true);assert.equal(d.assetPath,null);assert.equal(d.gitBlob,createHash('sha1').update('blob '+bytes.length+'\0').update(bytes).digest('hex'));
 const entry=batchEntries.get(c.record);assert.ok(entry);assert.equal(entry.status,'approved');assert.equal(entry.expectedSha256,c.sha256);assert.deepEqual(entry.source,d.source);
 assert.equal(record.status,'approved','registered approval is never lowered to generated');assert.equal(record.assetPath,null,'no production path before gameplay integration');
 assert.ok(record.notes.includes(c.sha256));assert.ok(record.notes.includes(process.env.CH3_BATCH_D_REVIEW_COMMIT));assert.ok(record.notes.includes('native-grid authorship NOT proven'),'accepted limitation recorded');
 if(changed)assert.ok(!record.notes.includes(prior.sha256),'superseded D05 v02 review bytes are not the registered selection');
 const pv=previews[c.record];assert.ok(pv,'approved selection has a canonical preview');assert.equal(pv.sha256,c.sha256);assert.deepEqual(pv.source,d.source);assert.deepEqual(fs.readFileSync(pv.file),bytes,'canonical preview byte-identical to the pinned gallery file');
}
assert.equal(expected.size,0);assert.equal(manifest.candidates.filter(c=>c.retainedFromPreviousReview).length,8);
const refs=JSON.parse(fs.readFileSync(path.join(historical,'references/approved-sources.json'),'utf8'));
// 23 references: strict byte equality, except the one recorded later approved replacement (Paper Emergency v03 -> v04).
const referenceCheck=checkApprovedReferences({refs,previews,art,digest,readRepo:rel=>fs.readFileSync(rel),reviewDigest:f=>digest(fs.readFileSync(safe(historical,f)))});
const audit=JSON.parse(fs.readFileSync(path.join(historical,'inventory.json'),'utf8'));assert.equal(audit.nodeCoverage.length,34);assert.deepEqual(audit.missingRegisteredRequirements,[]);
const changeProof=JSON.parse(fs.readFileSync(path.join(current,'pixel-change-verification.json'),'utf8'));
assert.equal(changeProof.changedPixels,1287);assert.equal(changeProof.outsideAllowedMaskChanged,0);assert.equal(changeProof.outsideEffectiveMaskChanged,0);assert.equal(changeProof.cabinetBaseAndCasterRows122Through205Unchanged,true);assert.equal(changeProof.correctedSha256,'aa90896023a59454887e9b3bd5b1745cb8b95a5d9737829119abddd9176f4889');
const contract=JSON.parse(fs.readFileSync(path.join(current,'mask-contract.json'),'utf8'));assert.equal(contract.declaredBeforeGeneration,true);assert.equal(contract.allowedPixels,2132);assert.equal(contract.maskSha256,'09ea806000ae75f58eb0935ad932a471247d231759e0b61dd17c4a4fcbbf0ece');assert.equal(digest(fs.readFileSync(path.join(current,contract.allowedMask))),contract.maskSha256);
for(const root of [historical,previousRoot,current])for(const report of ['qa/results.json','qa/browser-results.json','qa/canonical-results.json'])assert.equal(JSON.parse(fs.readFileSync(path.join(root,report),'utf8')).result,'PASS');
assert.ok(!fs.existsSync(dest),'refuse to overwrite existing review directory');fs.mkdirSync(path.dirname(dest),{recursive:true});fs.cpSync(gallery,dest,{recursive:true});
for(const [name,pkg] of [['v01',history],['v02-close-camera-corrections',previous],[version,latest]])for(const [file,hash] of pkg.sums)assert.equal(digest(fs.readFileSync(path.join(dest,name,file))),hash,'staged '+file);
// Deployment metadata and the owner-selection receipt live beside, never inside, the three immutable snapshots.
for(const f of ['deployment-provenance.json','owner-selection.json','selection.html','index.html'])assert.ok(!fs.existsSync(path.join(dest,f)),'refuse to overwrite '+f);
const registered=decision.candidates.filter(d=>previews[d.key]&&previews[d.key].sha256===d.sha256).length;assert.equal(registered,9);
fs.writeFileSync(path.join(dest,'deployment-provenance.json'),JSON.stringify({publicSiteSource:process.env.GITHUB_SHA||'local-validation',deployedBy:'canonical main Pages workflow (.github/workflows/pages.yml)',gallerySource:process.env.CH3_BATCH_D_REVIEW_COMMIT,galleryRef:'art/ch3-pavilion-batch04-20261120',selectedReviewVersion:version,creativeApproval:'Nate selected all nine Chapter 3 Batch D artworks on 2026-11-20 exactly as mapped in v03: D01/D04/D06/D07/D08 v01, D02/D03/D09 v02, D05 v03 (docs/122; docs/103 Chapter 3 Batch D section).',status:'approved',approved:true,canonicalExactSelectedPreviewCount:registered,gameplayIntegration:'Not authorized by this approval or publication; production assetPath null.',nativeGridAuthorship:'Unresolved/unproven; accepted by Nate for the exact selected bytes.',history:'v01, v02-close-camera-corrections and v03-clapper-correction remain byte-preserved. Their review-time generated/unselected labels are historical provenance, superseded by owner-selection.json.',approvedSourceReferences:{strict:referenceCheck.strict.length,laterApprovedReplacements:referenceCheck.superseded}},null,2)+'\n');
fs.writeFileSync(path.join(dest,'owner-selection.json'),decisionBytes);
const esc=t=>String(t).replace(/[&<>"]/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[ch]));
const rows=decision.candidates.map(d=>'<tr><td><a href="'+esc(d.file.slice(dir.length+1))+'">'+esc(d.candidateId)+'</a></td><td>'+d.selectedVersion+'</td><td><code>'+esc(d.key)+'</code></td><td><code>'+d.sha256+'</code></td></tr>').join('');
fs.writeFileSync(path.join(dest,'selection.html'),'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Out of Order — Chapter 3 Batch D selections</title><style>body{max-width:72rem;margin:2rem auto;padding:0 1rem;font:16px/1.6 system-ui}td,code,a{overflow-wrap:anywhere}td{padding:.5rem;vertical-align:top}table{table-layout:fixed;width:100%}</style><h1>Chapter 3 Batch D — Nate’s approved selections</h1><p>Owner-approved 2026-11-20: all nine Batch D artworks exactly as mapped in the v03 review. D01, D04, D06, D07 and D08 keep v01; D02, D03 and D09 keep v02; D05 is the v03 localized mechanical-clapper correction.</p><p><a href="'+version+'/">v03 gallery (current mapping)</a> · <a href="v02-close-camera-corrections/">Historical v02</a> · <a href="v01/">Historical v01</a> · <a href="owner-selection.json">Owner decision and provenance</a></p><p>Original native-grid authorship remains unresolved/unproven and is accepted by Nate for these exact bytes. Canonical previews matching these exact selections: '+registered+'/9. Approved, not integrated: no gameplay integration or production path is authorized.</p><table><tr><th>Selection</th><th>Version</th><th>Record</th><th>SHA-256</th></tr>'+rows+'</table><p>Historical generated/unselected labels inside the v01, v02 and v03 review snapshots remain unchanged as provenance; the later owner decision above supersedes them.</p></html>');
fs.writeFileSync(path.join(dest,'index.html'),'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 3 Batch D review</title><p><a href="selection.html">Batch D — Nate’s nine approved selections (receipt)</a></p><p><a href="'+version+'/">v03 gallery (approved mapping)</a> · <a href="v02-close-camera-corrections/">Historical v02</a> · <a href="v01/">Historical v01</a></p><p>Review galleries keep their original review-time labels.</p></html>');
console.log('PASS: staged immutable v01/v02/v03; nine approved selections registered byte-exact ('+registered+'/9); approved-source references '+referenceCheck.strict.length+' strict + '+referenceCheck.superseded.length+' recorded later replacement'+(referenceCheck.superseded.length?' ('+referenceCheck.superseded.map(x=>x.key).join(', ')+')':'')+'; receipt written outside the snapshots; no gallery code executed.');
