#!/usr/bin/env node
// Read-only selection/source verification. Optional staging writes exact native inputs to an EMPTY
// temporary directory outside the checkout. This script never imports or runs register-art.mjs.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {readJson,sha256,artRecords,checkContract} from './lib.mjs';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const PIN='e65f42c19e54f566819289d2b133be246ede13f5';
const GALLERY='tools/prologue-art-lab/assets/review/chapter-03-batch04-2026-11-20/';
const VERSION='v03-clapper-correction',MANIFEST=GALLERY+VERSION+'/manifest.json';
const MANIFEST_HASH='d7239e3dddc0cb8ff753e746a74f739e3774b38b5f57a03eadcd75e0ef45b77d';
const PREFIX='docs/122_OUT_OF_ORDER_CH3_BATCH_D_';
const EXPECTED=[
 ['CH3-D01-service-exit','scenes:pavilion_reboot/service_exit','v01','4a736b2d7b5fd7dea50fe9d93fe36e7465674ce0b8e38e7f2d6517fca73df392'],
 ['CH3-D02-service-exit-bg','scenes:pavilion_reboot/service_exit#portraitBackground','v02','241bfb8e817cf7c42508c218c188a1ac2706bad2e5f577484ce10a359b9a88e9'],
 ['CH3-D03-attendant-quiet','portraits:pavilion_attendant:quiet','v02','7f00208a3a96628f18fd23f079913dcb706e0e220db081d4cb438107f15bdf90'],
 ['CH3-D04-presenter-relieved','portraits:pavilion_presenter:relieved','v01','29a349c7bcdfe32d2885709dc91977beb7e3869d2461913cfd89afdacebbda9b'],
 ['CH3-D05-backstage','scenes:pavilion_reboot/backstage','v03','aa90896023a59454887e9b3bd5b1745cb8b95a5d9737829119abddd9176f4889'],
 ['CH3-D06-exterior-exit','scenes:pavilion_reboot/exterior_exit','v01','76b3232f685fd392f981f0c846382e3ddccd61ed94d44e09ea1bc5cf032c3e8a'],
 ['CH3-D07-exit-vestibule','scenes:pavilion_reboot/exit_vestibule','v01','cc2d2ce27e1e2cbf609fcae2210d3c46c57b749e8850be2219ad6de7f7f807c8'],
 ['CH3-D08-courtesy-stage','scenes:pavilion_reboot/courtesy_stage','v01','0b413a7b9a669365f114fda8765a242fc3ce00fc9c1ea3bd535c7a2b3d1cdb98'],
 ['CH3-D09-courtesy-stage-bg','scenes:pavilion_reboot/courtesy_stage#portraitBackground','v02','b0786ebd4147c6b0e6441838c725751a794db04fa9bcce4341aa1a3a7f1e7623'],
];
const args=process.argv.slice(2),allowed=new Set(['--decision','--batch','--stage','--output']);
for(let i=0;i<args.length;i+=2)assert.ok(allowed.has(args[i])&&args[i+1]&&!args[i+1].startsWith('--'),'Unsupported or missing argument');
const value=(flag,fallback)=>args.includes(flag)?args[args.indexOf(flag)+1]:fallback;
const blob=(commit,file)=>execFileSync('git',['show',commit+':'+file],{cwd:ROOT,maxBuffer:32*1024*1024});
const blobId=bytes=>crypto.createHash('sha1').update(Buffer.from('blob '+bytes.length+'\0')).update(bytes).digest('hex');
const resolveReview=rel=>{
 const file=path.posix.normalize(path.posix.join(GALLERY,VERSION,rel));
 assert.ok(file.startsWith(GALLERY),'review path stays in pinned gallery');return file;
};
function main(){
 const decision=readJson(path.resolve(ROOT,value('--decision',PREFIX+'SELECTED_ARTWORK_20261120.json')));
 const batch=readJson(path.resolve(ROOT,value('--batch',PREFIX+'APPROVAL_REGISTRATION_BATCH_20261120.json')));
 assert.equal(decision.sourceCommit,PIN);assert.equal(decision.gallerySourceCommit,PIN);assert.equal(decision.galleryVersion,VERSION);
 assert.equal(decision.status,'approved');assert.equal(decision.approved,true);assert.equal(decision.selected,true);
 for(const field of ['codexCanonicalRegistrationAuthorized','publicationAuthorized','mergeAuthorized','deploymentAuthorized','gameplayIntegrationAuthorized','nextArtBatchAuthorized'])assert.equal(decision[field],false);
 assert.equal(decision.candidates.length,9);assert.equal(batch.entries.length,9);
 const candidates=new Map(decision.candidates.map(c=>[c.candidateId,c])),entries=new Map(batch.entries.map(e=>[e.key,e]));
 assert.equal(candidates.size,9);assert.equal(entries.size,9);
 assert.deepEqual([...candidates.keys()].sort(),EXPECTED.map(x=>x[0]).sort());
 const manifestBytes=blob(PIN,MANIFEST);assert.equal(sha256(manifestBytes),MANIFEST_HASH);
 assert.equal(decision.sourceManifest.file,MANIFEST);assert.equal(decision.sourceManifest.sha256,MANIFEST_HASH);assert.equal(decision.sourceManifest.gitBlob,blobId(manifestBytes));
 const manifest=JSON.parse(manifestBytes);assert.equal(manifest.selected,false);assert.equal(manifest.approved,false);assert.equal(manifest.assetPath,null);
 const originalCandidates=new Map(manifest.candidates.map(c=>[c.candidateId,c]));assert.equal(originalCandidates.size,9);
 const catalog=new Map(artRecords(readJson(path.join(ROOT,'story/artwork.draft.json'))).map(e=>[e.key,e]));
 const previews=readJson(path.join(ROOT,'story/artwork-preview.json')).images;
 const verified=[],inputs=[];
 for(const [id,key,version,expectedHash] of EXPECTED){
  const c=candidates.get(id),original=originalCandidates.get(id);assert.ok(c&&original);
  const folder=version==='v01'?'v01':version==='v02'?'v02-close-camera-corrections':VERSION;
  const file=GALLERY+folder+'/candidates/'+id+'-'+version+'.png';
  assert.equal(c.key,key);assert.equal(c.selectedVersion,version);assert.equal(c.file,file);assert.equal(resolveReview(original.file),file);assert.equal(original.record,key);
  assert.equal(c.sha256,expectedHash);assert.equal(original.sha256,expectedHash);
  assert.equal(c.status,'approved');assert.equal(c.approved,true);assert.equal(c.selected,true);assert.equal(c.assetPath,null);assert.equal(c.replacesCanonicalSelection,false);
  assert.deepEqual(c.source,{repo:'InterstellarHarvest/CYOA-storyboard',ref:'art/ch3-pavilion-batch04-20261120',commit:PIN,path:file});
  const entry=entries.get(key);assert.ok(entry);assert.equal(entry.file,file);assert.equal(entry.status,'approved');assert.equal(entry.expectedSha256,expectedHash);assert.deepEqual(entry.source,c.source);
  const bytes=blob(PIN,file);assert.equal(sha256(bytes),expectedHash);assert.equal(blobId(bytes),c.gitBlob);
  if(fs.existsSync(path.join(ROOT,file)))assert.deepEqual(fs.readFileSync(path.join(ROOT,file)),bytes);
  const catalogEntry=catalog.get(key);assert.ok(catalogEntry);assert.equal(catalogEntry.path,null,'no production path assigned');
  const checked=checkContract(catalogEntry,bytes);assert.deepEqual(checked.problems,[]);assert.ok(checked.png.decoded);assert.equal(checked.png.depth,8);assert.equal(checked.png.partial,0);
  assert.deepEqual([checked.png.width,checked.png.height],c.dimensions);assert.deepEqual(c.dimensions,original.dimensions);
  const transparent=key.startsWith('portraits:');assert.equal(c.mode,transparent?'RGBA':'RGB');assert.equal(checked.png.colorType,transparent?6:2);assert.equal(c.alpha,transparent?'transparent':'opaque');
  assert.ok(transparent?checked.png.transparent>0:checked.png.transparent===0);
  if(previews[key])assert.equal(previews[key].sha256,expectedHash,'unexpected prior selection: stop before any replacement');
  verified.push({candidateId:id,key,version,file,sha256:expectedHash,gitBlob:c.gitBlob,dimensions:c.dimensions,mode:c.mode,alpha:c.alpha,partialAlpha:0,source:c.source});
  inputs.push({entry,bytes});
 }
 let packageFiles=0;
 for(const version of ['v01','v02-close-camera-corrections',VERSION]){
  const root=GALLERY+version+'/',sumBytes=blob(PIN,root+'SHA256SUMS.txt'),seen=new Set();
  for(const line of sumBytes.toString('utf8').trim().split('\n')){
   const match=line.match(/^([0-9a-f]{64})  (.+)$/);assert.ok(match);assert.ok(!seen.has(match[2]));seen.add(match[2]);
   const file=path.posix.normalize(root+match[2]);assert.ok(file.startsWith(root),'checksum path confined to snapshot');
   const bytes=blob(PIN,file);assert.equal(sha256(bytes),match[1]);
   if(fs.existsSync(path.join(ROOT,file)))assert.deepEqual(fs.readFileSync(path.join(ROOT,file)),bytes);
  }
  const tracked=execFileSync('git',['ls-tree','-r','--name-only',PIN,root],{cwd:ROOT,encoding:'utf8'}).trim().split('\n');
  assert.equal(tracked.length,seen.size+1,'every snapshot file checksummed except checksum manifest itself');packageFiles+=tracked.length;
 }
 assert.equal(packageFiles,189);
 const priorLedger=blob(PIN,'docs/103_RETROACTIVE_ARTWORK_APPROVAL_LEDGER.md'),ledger=fs.readFileSync(path.join(ROOT,'docs/103_RETROACTIVE_ARTWORK_APPROVAL_LEDGER.md'));
 assert.equal(sha256(priorLedger),decision.preservationBaseline.approvalLedgerSha256BeforeAppend);
 assert.deepEqual(ledger.subarray(0,priorLedger.length),priorLedger,'existing ledger is append-only');
 const appendix=ledger.subarray(priorLedger.length).toString('utf8');assert.ok(appendix.includes('Chapter 3 Batch D'));for(const c of verified)assert.ok(appendix.includes(c.sha256));
 const report={result:'PASS',scope:'Verified owner selections and future registration inputs only. No canonical registration, registration rehearsal, merge, deployment or gameplay integration.',sourceCommit:PIN,sourceManifestSha256:MANIFEST_HASH,selections:verified,counts:{selected:9,opaqueRGB:7,transparentRGBA:2,versions:{v01:5,v02:3,v03:1},historicalPackageFiles:189,newPreviewsOnThisCheckout:verified.filter(c=>!previews[c.key]).length,existingExactPreviewsOnThisCheckout:verified.filter(c=>!!previews[c.key]).length},acceptedNativeGridAuthorshipLimitation:true,historicalPackagesUnchanged:true,priorLedgerPrefixUnchanged:true,canonicalRegistrationPerformed:false};
 if(args.includes('--stage')){
  const directory=path.resolve(value('--stage'));assert.ok(directory!==ROOT&&!directory.startsWith(ROOT+path.sep),'temporary staging must be outside checkout');
  fs.mkdirSync(directory,{recursive:true});assert.equal(fs.readdirSync(directory).length,0,'staging directory must be empty');
  const staged=inputs.map(({entry,bytes},i)=>{const file=path.join(directory,String(i+1).padStart(2,'0')+'-'+path.basename(entry.file));fs.writeFileSync(file,bytes);return {...entry,file};});
  const batchFile=path.join(directory,'batch.json');fs.writeFileSync(batchFile,JSON.stringify({...batch,entries:staged},null,2)+'\n');report.temporaryStaging={directory,batch:batchFile};
 }
 if(args.includes('--output'))fs.writeFileSync(path.resolve(value('--output')),JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify(report,null,2));
}
try{main();}catch(error){console.error('REFUSED: '+error.message);process.exitCode=1;}
