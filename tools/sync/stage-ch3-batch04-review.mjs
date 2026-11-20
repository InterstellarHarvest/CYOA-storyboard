// Trusted main-only Pages helper. Treat the pinned review package as data; never execute it.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {decodePng} from './lib.mjs';
const [checkout,site]=process.argv.slice(2);
assert.ok(checkout&&site,'usage: node tools/sync/stage-ch3-batch04-review.mjs <pinned checkout> <site>');
const dir=process.env.CH3_BATCH_D_REVIEW_DIR;
assert.equal(dir,'tools/prologue-art-lab/assets/review/chapter-03-batch04-2026-11-20/v01');
assert.match(process.env.CH3_BATCH_D_REVIEW_COMMIT||'',/^[0-9a-f]{40}$/);
const source=path.resolve(checkout,dir),dest=path.resolve(site,dir);
const digest=buf=>createHash('sha256').update(buf).digest('hex');
const walk=(root,rel='')=>fs.readdirSync(path.join(root,rel),{withFileTypes:true}).flatMap(e=>{
 assert.ok(!e.isSymbolicLink(),'no review symlinks');
 return e.isDirectory()?walk(root,path.join(rel,e.name)):[path.join(rel,e.name)];
});
const sums=new Map(fs.readFileSync(path.join(source,'SHA256SUMS.txt'),'utf8').trim().split('\n').map(line=>{
 const match=line.match(/^([0-9a-f]{64})  (.+)$/);assert.ok(match,'valid checksum line');
 const file=path.resolve(source,match[2]);assert.ok(file.startsWith(source+path.sep),'checksum confined to package');
 return [match[2],match[1]];
}));
const files=walk(source);assert.equal(files.length,sums.size+1,'every shipped file has a checksum except checksum manifest itself');
for(const f of files)if(f!=='SHA256SUMS.txt')assert.equal(digest(fs.readFileSync(path.join(source,f))),sums.get(f),f);
const manifest=JSON.parse(fs.readFileSync(path.join(source,'manifest.json'),'utf8'));
assert.equal(manifest.narrativeBlob,'857ffdf1bc9432cf4bbbfd7819f5f430a06d9036');
assert.equal(manifest.candidateSourceCommit,'4fc277651c7d05163817d9ab99d0fc3fcf522d47');
assert.equal(manifest.status,'generated');assert.equal(manifest.selected,false);assert.equal(manifest.approved,false);assert.equal(manifest.assetPath,null);
assert.equal(manifest.candidates.length,9);
const expected=new Set(['CH3-D01-service-exit','CH3-D02-service-exit-bg','CH3-D03-attendant-quiet','CH3-D04-presenter-relieved','CH3-D05-backstage','CH3-D06-exterior-exit','CH3-D07-exit-vestibule','CH3-D08-courtesy-stage','CH3-D09-courtesy-stage-bg']);
const art=JSON.parse(fs.readFileSync('story/artwork.draft.json','utf8'));
const previews=JSON.parse(fs.readFileSync('story/artwork-preview.json','utf8')).images;
for(const c of manifest.candidates){
 assert.ok(expected.delete(c.candidateId),'unique expected candidate');
 assert.match(c.file,/^candidates\/CH3-D\d{2}-[a-z-]+-v01\.png$/);
 assert.equal(c.status,'generated');assert.equal(c.selected,false);assert.equal(c.approved,false);assert.equal(c.assetPath,null);
 const bytes=fs.readFileSync(path.join(source,c.file));assert.equal(digest(bytes),c.sha256);
 const png=decodePng(bytes);assert.ok(png.decoded);assert.equal(png.depth,8);assert.equal(png.partial,0);assert.deepEqual([png.width,png.height],c.dimensions);
 const portrait=c.record.startsWith('portraits:');assert.equal(png.colorType,portrait?6:2);assert.ok(portrait?png.transparent>0:png.transparent===0);
 assert.deepEqual(c.dimensions,portrait||c.record.endsWith('#portraitBackground')?[564,278]:[314,206]);
 const zoom=decodePng(fs.readFileSync(path.join(source,c.preview4x)));assert.deepEqual([zoom.width,zoom.height],c.dimensions.map(x=>4*x));
 assert.equal(digest(fs.readFileSync(path.join(source,c.source.original))),c.source.sha256);
 const [group,key]=c.record.split(/:(.*)/s);const record=key.endsWith('#portraitBackground')?art[group][key.split('#')[0]].portraitBackground:art[group][key];
 assert.equal(record.status,'generated');assert.equal(record.assetPath,null);assert.ok(record.notes.includes(c.sha256));assert.ok(record.notes.includes(manifest.candidateSourceCommit));
 assert.equal(previews[c.record],undefined,'candidate never appears as selected artwork');
}
assert.equal(expected.size,0);
const refs=JSON.parse(fs.readFileSync(path.join(source,'references/approved-sources.json'),'utf8'));
for(const [key,r] of Object.entries(refs)){
 assert.equal(r.sha256,previews[key].sha256);assert.equal(digest(fs.readFileSync(path.join(source,r.reviewFile))),r.sha256);
 assert.equal(digest(fs.readFileSync(previews[key].file)),r.sha256);
}
const audit=JSON.parse(fs.readFileSync(path.join(source,'inventory.json'),'utf8'));
assert.equal(audit.nodeCoverage.length,34);assert.deepEqual(audit.missingRegisteredRequirements,[]);
for(const report of ['qa/results.json','qa/browser-results.json','qa/canonical-results.json'])assert.equal(JSON.parse(fs.readFileSync(path.join(source,report),'utf8')).result,'PASS');
assert.ok(!fs.existsSync(dest),'refuse overwrite of an existing review directory');
fs.mkdirSync(path.dirname(dest),{recursive:true});fs.cpSync(source,dest,{recursive:true});
for(const [file,hash] of sums)assert.equal(digest(fs.readFileSync(path.join(dest,file))),hash,'staged '+file);
// Provenance belongs outside the immutable v01 package; publication is not selection.
const parent=path.dirname(dest);
fs.writeFileSync(path.join(parent,'deployment-provenance.json'),JSON.stringify({publicSiteSource:process.env.GITHUB_SHA||'local-validation',gallerySource:process.env.CH3_BATCH_D_REVIEW_COMMIT,deployedBy:'canonical main-only Pages workflow',status:'generated / unselected',approved:false,gameplayIntegrated:false,nativeGridAuthorship:'unproven; documented derived logical exports'},null,2)+'\n');
fs.writeFileSync(path.join(parent,'index.html'),'<!doctype html><html lang="en"><meta charset="utf-8"><title>Chapter 3 Batch D review</title><meta http-equiv="refresh" content="0;url=v01/"><a href="v01/">Open Batch D v01 — generated / unselected</a></html>');
console.log(`PASS: staged nine unselected Batch D candidates and ${files.length} checksum-verified review files; approved art unchanged.`);
