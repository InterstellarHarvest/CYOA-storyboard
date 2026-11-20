// Trusted main-only Pages helper: verify immutable v01/v02 history plus the localized v03 correction as data.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {decodePng} from './lib.mjs';
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
 assert.equal(record.status,'generated');assert.equal(record.assetPath,null);assert.ok(record.notes.includes(changed?prior.sha256:c.sha256));assert.ok(record.notes.includes(changed?prior.candidateSourceCommit:c.candidateSourceCommit));if(changed)assert.ok(!record.notes.includes(c.sha256),'D05 correction stays review-only; no canonical registration');assert.equal(previews[c.record],undefined,'unselected candidate has no selected preview');
}
assert.equal(expected.size,0);assert.equal(manifest.candidates.filter(c=>c.retainedFromPreviousReview).length,8);
const refs=JSON.parse(fs.readFileSync(path.join(historical,'references/approved-sources.json'),'utf8'));
for(const [key,r] of Object.entries(refs)){
 assert.equal(r.sha256,previews[key].sha256);assert.equal(digest(fs.readFileSync(safe(historical,r.reviewFile))),r.sha256);assert.equal(digest(fs.readFileSync(previews[key].file)),r.sha256);
}
const audit=JSON.parse(fs.readFileSync(path.join(historical,'inventory.json'),'utf8'));assert.equal(audit.nodeCoverage.length,34);assert.deepEqual(audit.missingRegisteredRequirements,[]);
const changeProof=JSON.parse(fs.readFileSync(path.join(current,'pixel-change-verification.json'),'utf8'));
assert.equal(changeProof.changedPixels,1287);assert.equal(changeProof.outsideAllowedMaskChanged,0);assert.equal(changeProof.outsideEffectiveMaskChanged,0);assert.equal(changeProof.cabinetBaseAndCasterRows122Through205Unchanged,true);assert.equal(changeProof.correctedSha256,'aa90896023a59454887e9b3bd5b1745cb8b95a5d9737829119abddd9176f4889');
const contract=JSON.parse(fs.readFileSync(path.join(current,'mask-contract.json'),'utf8'));assert.equal(contract.declaredBeforeGeneration,true);assert.equal(contract.allowedPixels,2132);assert.equal(contract.maskSha256,'09ea806000ae75f58eb0935ad932a471247d231759e0b61dd17c4a4fcbbf0ece');assert.equal(digest(fs.readFileSync(path.join(current,contract.allowedMask))),contract.maskSha256);
for(const root of [historical,previousRoot,current])for(const report of ['qa/results.json','qa/browser-results.json','qa/canonical-results.json'])assert.equal(JSON.parse(fs.readFileSync(path.join(root,report),'utf8')).result,'PASS');
assert.ok(!fs.existsSync(dest),'refuse to overwrite existing review directory');fs.mkdirSync(path.dirname(dest),{recursive:true});fs.cpSync(gallery,dest,{recursive:true});
for(const [name,pkg] of [['v01',history],['v02-close-camera-corrections',previous],[version,latest]])for(const [file,hash] of pkg.sums)assert.equal(digest(fs.readFileSync(path.join(dest,name,file))),hash,'staged '+file);
fs.writeFileSync(path.join(dest,'deployment-provenance.json'),JSON.stringify({publicSiteSource:process.env.GITHUB_SHA||'local-validation',gallerySource:process.env.CH3_BATCH_D_REVIEW_COMMIT,reviewVersion:version,retainedUnchanged:8,revised:1,status:'generated / unselected',approved:false,gameplayIntegrated:false,nativeGridAuthorship:'unproven; documented derived exports',historicalV01AndV02Preserved:true,canonicalRegistrationChanged:false},null,2)+'\n');
fs.writeFileSync(path.join(dest,'index.html'),'<!doctype html><html lang="en"><meta charset="utf-8"><title>Chapter 3 Batch D review</title><meta http-equiv="refresh" content="0;url='+version+'/"><a href="'+version+'/">Open Batch D v03 — generated / unselected</a> · <a href="v01/">Historical v01</a> · <a href="v02-close-camera-corrections/">Historical v02</a></html>');
console.log('PASS: staged immutable v01/v02 and current v03; one masked correction, eight retained candidates, all checksums/contracts verified; no gallery code executed.');
