#!/usr/bin/env node
// Deterministic engine handoff from the PUBLIC CANONICAL storyboard.
// The story-node deathPopup is the ONLY creative source for popup copy and art selection.
// Usage: node tools/storyboard/export-death-presentations.mjs [--check]
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const manifest=JSON.parse(fs.readFileSync(path.join(root,'story/storyboard-manifest.json'),'utf8'));
const art=JSON.parse(fs.readFileSync(path.join(root,'story',manifest.artwork),'utf8'));
const entries=[];
for(const chap of manifest.chapters){
 const source=JSON.parse(fs.readFileSync(path.join(root,'story',chap.file),'utf8'));
 for(const [nodeId,node] of Object.entries(source.nodes||{})){
  if(!node.deathPopup)continue;
  if(node.end!==true)throw Error('Death popup on nonterminal node '+chap.id+':'+nodeId);
  const p=node.deathPopup, artRef=p.artRef;
  const illustration=art.deathScreens?.[artRef];
  if(!artRef||!illustration)throw Error('Missing death-screen art catalog record '+chap.id+':'+nodeId);
  if(!p.title||!p.description||!p.subtitle)throw Error('Fatal popup needs title, subtitle, and narrative beat '+chap.id+':'+nodeId);
  if(illustration.dimensions!=='314x206')throw Error('Unexpected death-screen image size '+artRef);
  if(node.endingArt!==artRef)throw Error('End-node art ref diverges from popup '+chap.id+':'+nodeId);
  const selected=illustration.assetPath||illustration.selectedSource?.path||null;
  entries.push({
   id:chap.id+':'+nodeId,
   when:{end:chap.id+':'+nodeId},
   title:p.title,
   subtitle:p.subtitle,
   body:[p.description],
   narrativeBeat:p.description,
   artwork:{
    id:artRef,
    status:illustration.status,
    dimensions:[314,206],
    scale:2,
    selectedPath:selected,
    generatedPath:illustration.assetPath||null,
    proposedPath:illustration.suggestedFilename||null,
    selectedSource:illustration.selectedSource||null
   },
   popupStatus:p.status,
   // Never silently promote a proposed ending/copy or unproduced illustration to runtime-ready.
   readyForGameplay:(['approved','integrated','reused'].includes(illustration.status)&&p.status==='owner-approved')
  });
 }
}
const output={schema:'cyoa-death-presentations-export-v1',source:'InterstellarHarvest/CYOA-storyboard',authority:'story/chapters/*.draft.json nodes[].deathPopup + story/artwork.draft.json deathScreens',entries};
const rendered=JSON.stringify(output,null,2)+'\n';
const destination=path.join(root,'story/death-presentations.export.json');
if(process.argv.includes('--check')){
 const current=fs.existsSync(destination)?fs.readFileSync(destination,'utf8'):'';
 if(current!==rendered)throw Error('Death-presentations export drift: run node tools/storyboard/export-death-presentations.mjs and commit the result');
 console.log('OK: '+entries.length+' fatal popup records export exactly from canonical story nodes');
}else{
 fs.writeFileSync(destination,rendered);
 console.log('Wrote '+entries.length+' death presentations: '+destination);
}
