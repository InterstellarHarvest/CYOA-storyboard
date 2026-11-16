// Lightweight, dependency-free browser-logic smoke check for the storyboard.
// Exercises the real standalone HTML script with a minimal DOM in Node.js.
// This is NOT a substitute for screenshot/interaction QA in a browser.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const html=fs.readFileSync(path.join(root,'tools/storyboard/index.html'),'utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
assert.ok(script,'HTML contains the viewer script');
new vm.Script(script);

const manifest=JSON.parse(fs.readFileSync(path.join(root,'story/storyboard-manifest.json'),'utf8'));
const artwork=JSON.parse(fs.readFileSync(path.join(root,'story/artwork.draft.json'),'utf8'));
const chapter=JSON.parse(fs.readFileSync(path.join(root,'story',manifest.chapters[0].file),'utf8'));
const items=JSON.parse(fs.readFileSync(path.join(root,'story',manifest.items),'utf8'));
assert.equal(manifest.artwork,'artwork.draft.json');
assert.equal(artwork.scenes['workplace/corridor'].portraitBackground.dimensions,'564x278','corridor paired portrait background dimensions');
assert.equal(artwork.scenes['workplace/corridor'].portraitBackground.status,'generated','corridor paired portrait background generated');
assert.equal(artwork.scenes['exposition/reception'].portraitBackground.status,'reused','approved reception background reuse');
const productionRecords=[
  ...Object.values(artwork.scenes).flatMap(scene=>[scene,...(scene.portraitBackground?[scene.portraitBackground]:[])]),
  ...Object.values(artwork.portraits),
  ...Object.values(artwork.items).flatMap(variants=>Object.values(variants)),
  ...Object.values(artwork.focus||{}),
  ...Object.values(artwork.deathScreens||{})
];
assert.equal(productionRecords.length,165,'shared artwork includes Chapter 3 and death screens');
assert.equal(productionRecords.filter(r=>r.status==='generated').length,28,'published metadata matches private generated count');
assert.equal(productionRecords.filter(r=>r.status==='reused').length,5,'approved reused records unchanged');
assert.equal(productionRecords.filter(r=>r.status==='not-started').length,132,'67 additional prompt-only Chapter 3 art records');
assert.equal(artwork.scenes['biology_park/conveniences_bureau']?.status,'not-started','Chapter 2 Bureau scene is not-started');
assert.equal(artwork.scenes['biology_park/conveniences_bureau']?.assetPath,null,'Chapter 2 Bureau scene has no image yet');
assert.equal(artwork.scenes['house_of_tomorrow/arrival']?.status,'not-started','Chapter 1 arrival scene is not-started');
assert.equal(artwork.scenes['house_of_tomorrow/arrival']?.assetPath,null,'Chapter 1 arrival scene has no image yet');
for(const record of productionRecords){
  if(record.status==='generated')assert.ok(record.assetPath?.endsWith('.png'),'generated art has logical PNG path: '+record.title);
}
assert.ok(artwork.deathScreens['pavilion/a_model_citizen']?.prompt,'death screen art registered');
assert.equal(artwork.scenes['pavilion/human_behavior_workshop']?.assetPath,null,'workshop art pending');
// Public storyboard intentionally mirrors metadata, not private generated images.

for(const portrait of Object.values(artwork.portraits)){
  assert.equal(portrait.foregroundFormat,'transparent-rgba-png','all NPC foregrounds are transparent');
  assert.ok(artwork.scenes[portrait.portraitBackgroundScene]?.portraitBackground,"portrait scene background exists");
}
assert.equal(manifest.layout,'storyboard-layout.json');
const layoutSource=JSON.parse(fs.readFileSync(path.join(root,'story',manifest.layout),'utf8'));
assert.equal(layoutSource.schema,'cyoa-storyboard-layout-v1');

// The header lists exactly the manifest's chapters, in order; every chapter's art resolves through
// the ONE shared artwork catalog (no per-chapter art catalogs).
assert.deepEqual(manifest.chapters.map(c=>[c.id,c.title,c.status]),[
  ['prologue-00','Prologue — The Last Good Day','draft'],['chapter-01','Chapter 1 — House of Tomorrow','draft'],['chapter-02','Chapter 2 — Biology Park','draft'],['chapter-03',"Chapter 3 — The People's Pavilion",'draft']],'manifest chapters, order, titles, draft status');
const chapters=manifest.chapters.map(c=>JSON.parse(fs.readFileSync(path.join(root,'story',c.file),'utf8')));
for(const ch of chapters){
  for(const scene of new Set([ch.scene,...Object.values(ch.nodes).map(x=>x.scene).filter(Boolean)]))
    assert.ok(artwork.scenes[scene],'scene reference '+scene);
  for(const n of Object.values(ch.nodes)){
    if(n.speaker)assert.ok(artwork.portraits[n.speaker+':'+(n.pose||'default')],'portrait '+n.speaker);
    if(n.focus)assert.ok(artwork.focus[n.focus],'focus '+n.focus);
    if(n.endingArt)assert.ok(artwork.deathScreens[n.endingArt],'death screen '+n.endingArt);
  }
}
assert.deepEqual(Object.keys(layoutSource.chapters),['prologue-00','chapter-01','chapter-02','chapter-03'],'layout has four chapters');
assert.deepEqual(layoutSource.chapters['prologue-00'].positions,{},'prologue positions retained exactly (none committed)');
assert.equal(Object.keys(chapters[3].nodes).length,62,'Chapter 3 has 63 storyboard nodes');
assert.equal(chapters[3].nodes.end_model_citizen.deathPopup.title,'A MODEL CITIZEN','owner-approved fatal metadata');
assert.equal(chapters[3].nodes.b_gate.choices.find(c=>c.id==='ch3_b03_c').check.need,4,'departure counter check');
for(const id of ['end_concourse_robot','end_underground_station','end_public','end_maintenance','end_customs'])
  assert.equal(chapters[2].nodes[id].storyboardNextChapter,'chapter-03','Chapter 2 preview handoff '+id);
for(const id of Object.keys(items)){
  assert.ok(artwork.items[id]?.slot?.prompt,'slot prompt '+id);
  assert.ok(artwork.items[id]?.inspect?.prompt,'inspect prompt '+id);
}

class Element {
  constructor(tag='div',id=''){
    this.tagName=tag;this.id=id;this.children=[];this.style={};this.attributes={};
    this.listeners={};this.textContent='';this.value='';this.disabled=false;
    this.scrollLeft=0;this.scrollTop=0;this.clientWidth=1200;this.clientHeight=720;
    this.classList={add(){},remove(){}};this.captured=null;
  }
  append(...children){this.children.push(...children);}
  replaceChildren(...children){this.children=[...children];}
  addEventListener(name,fn){this.listeners[name]=fn;}
  setAttribute(name,value){this.attributes[name]=value;}
  closest(){return null;}
  getBoundingClientRect(){return {left:0,top:0,width:this.clientWidth,height:this.clientHeight};}
  setPointerCapture(id){this.captured=id;}
  hasPointerCapture(id){return this.captured===id;}
  releasePointerCapture(id){if(this.captured===id)this.captured=null;}
  remove(){}
  click(){this.onclick?.();this.listeners.click?.();}
}
const elements=new Map();
const document={
  getElementById(id){if(!elements.has(id))elements.set(id,new Element('div',id));return elements.get(id);},
  createElement(tag){return new Element(tag);},
  createElementNS(_ns,tag){return new Element(tag);},
  body:new Element('body')
};
const flatten=n=>[n,...(n.children||[]).flatMap(flatten)];
const pane=()=>document.getElementById('details');
const button=(text)=>flatten(pane()).find(x=>x.tagName==='button' && String(x.textContent).includes(text));
const load=async(url)=>{
  const pathname=new URL(String(url)).pathname;
  const rel=pathname.startsWith('/CYOA-storyboard/')?pathname.slice('/CYOA-storyboard/'.length):pathname.slice(1);
  const full=path.resolve(root,rel);
  assert.ok(full.startsWith(root+path.sep),'file stays under root '+rel);
  return {ok:true,json:async()=>JSON.parse(fs.readFileSync(full,'utf8'))};
};
const downloads=[];
class QAURL extends URL{static createObjectURL(blob){downloads.push(blob);return 'blob:qa/'+downloads.length;} static revokeObjectURL(){}}
const windowListeners={};
const storage=new Map();
const localStorage={getItem:key=>storage.has(key)?storage.get(key):null,setItem:(key,value)=>storage.set(key,value),removeItem:key=>storage.delete(key)};
const context={
  document,window:{addEventListener(name,fn){windowListeners[name]=fn;},localStorage},location:{href:'https://example.org/CYOA-storyboard/tools/storyboard/'},
  fetch:load,URL:QAURL,Blob,JSON,Object,Math,Number,String,console,
  setTimeout(fn){fn();return 0;},
};
vm.runInNewContext(script,context);
await new Promise(resolve=>setTimeout(resolve,20));
assert.match(document.getElementById('status').textContent,/Loaded \d+ nodes/);
assert.equal(document.getElementById('exportArtwork').disabled,false);
assert.ok(flatten(pane()).some(x=>String(x.textContent).includes('Artwork references')),
          'selected opening node includes linked scene art');

document.getElementById('showArtwork').onclick();
assert.ok(button('APPLAUSE TIMING STATION'),'artwork library lists scene prompts');
button('APPLAUSE TIMING STATION').click();
const textarea=flatten(pane()).find(x=>x.tagName==='textarea'&&String(x.value).includes('A modest, narrow corporate timing desk'));
assert.ok(textarea,'editable scene prompt text area');
textarea.value='QA EDITED PROMPT';
assert.ok(button('Apply artwork changes'),'edit action exists');
button('Apply artwork changes').click();
assert.ok(flatten(pane()).some(x=>String(x.textContent).includes('QA EDITED PROMPT')),
          'edit was applied and rendered in inspector');
assert.match(document.getElementById('status').textContent,/in memory/);
document.getElementById('exportArtwork').onclick();
// Scene and paired 564×278 background are distinct editable records.
document.getElementById('showArtwork').onclick();
assert.ok(button('EMPLOYEE CORRIDOR — DRONE PORTRAIT BACKGROUND'),'paired background is listed in the scene catalog');
button('EMPLOYEE CORRIDOR — DRONE PORTRAIT BACKGROUND').click();
assert.ok(button('Open main scene'),'paired background links to its 314×206 scene');
const pairedEdit=flatten(pane()).find(x=>x.tagName==='textarea'&&String(x.value).includes('SAME employee corridor'));
assert.ok(pairedEdit,'nested portrait background has editable text prompt');
pairedEdit.value='QA PAIRED BACKGROUND PROMPT';
button('Apply artwork changes').click();
assert.ok(flatten(pane()).some(x=>x.textContent==='QA PAIRED BACKGROUND PROMPT'),'nested prompt edit shown');
assert.ok(button('Open main scene'),'pair still navigable after edit');
button('Open main scene').click();
assert.ok(flatten(pane()).some(x=>String(x.textContent).includes('quiet fluorescent workplace corridor')),'main scene prompt preserved when editing paired background');
assert.ok(button('Open paired portrait background'),'main scene links back to detailed portrait background');

document.getElementById('showItems').onclick();
assert.ok(button('APPLAUSE TIMING CLICKER'),'items still selectable');
button('APPLAUSE TIMING CLICKER').click();
assert.ok(button('APPLAUSE TIMING CLICKER — INVENTORY SLOT'),'item slot artwork link');
assert.ok(button('APPLAUSE TIMING CLICKER — INSPECTION ART'),'item inspection artwork link');

// SHOW links are real story edges: the original layout wrongly left this node orphaned.
const graphNodes=document.getElementById('nodes').children;
const findNode=id=>document.getElementById('nodes').children.find(n=>n.children[0]?.textContent===id);
const receptionOpen=findNode('reception_opening');
const noticeReply=findNode('reception_notice_reply');
assert.ok(receptionOpen&&noticeReply,'reception and notice nodes on graph');
const openingX=parseFloat(receptionOpen.style.left);
const noticeX=parseFloat(noticeReply.style.left);
assert.equal(noticeX-openingX,340,'notice reply occupies next timeline column');
const noticeGap=Math.abs(parseFloat(receptionOpen.style.top)-parseFloat(noticeReply.style.top));
assert.ok(noticeGap<=520,'notice reply stays near its parent branch, vertical gap '+noticeGap);
const edgeLabels=flatten(document.getElementById('edges')).filter(x=>x.tagName==='text').map(x=>x.textContent);
assert.ok(edgeLabels.some(s=>String(s).includes('SHOW Termination Notice')),
          'item-triggered route drawn and labeled on graph');
receptionOpen.click();
assert.ok(button('SHOW Termination Notice'),'item-triggered branch visible in node inspector');
button('SHOW Termination Notice').click();
assert.ok(flatten(pane()).some(x=>x.textContent==='Reception Notice Reply'),
          'inspector item action navigates to corresponding node');

// Mouse wheel zoom preserves the graph coordinate under the pointer.
const viewport=document.getElementById('viewport'),stage=document.getElementById('stage');
viewport.scrollLeft=500;viewport.scrollTop=210;
const scale=()=>Number(stage.style.transform.replace("scale(","").replace(")",""));
const before=scale(),anchor={x:320,y:160};
const worldBefore={x:(viewport.scrollLeft+anchor.x)/before,y:(viewport.scrollTop+anchor.y)/before};
let prevented=false;
viewport.listeners.wheel({deltaY:-120,deltaMode:0,clientX:anchor.x,clientY:anchor.y,
 preventDefault(){prevented=true;}});
const after=scale();
assert.ok(prevented,'wheel event prevents default scrolling');
assert.ok(after>before,'wheel up zooms in');
assert.ok(Math.abs((viewport.scrollLeft+anchor.x)/after-worldBefore.x)<1e-7,'wheel cursor x remains anchored');
assert.ok(Math.abs((viewport.scrollTop+anchor.y)/after-worldBefore.y)<1e-7,'wheel cursor y remains anchored');
viewport.listeners.wheel({deltaY:120,deltaMode:0,clientX:anchor.x,clientY:anchor.y,preventDefault(){}});
assert.ok(Math.abs(scale()-before)<1e-10,'equal opposite wheel motion restores scale');

// Manual layout: drag one node, check connector redraw, persistence, reload, import, and reset.
const xFromNode=id=>parseFloat(findNode(id).style.left);
const yFromNode=id=>parseFloat(findNode(id).style.top);
const movedId='drone_intercepts',nodeToDrag=findNode(movedId);
assert.ok(nodeToDrag,'node available for drag');
const initialX=xFromNode(movedId),initialY=yFromNode(movedId);
const edgePathsBefore=document.getElementById('edges').children.filter(n=>n.tagName==='path').map(n=>n.attributes.d).join('|');
let stopped=false;
nodeToDrag.listeners.pointerdown({pointerId:22,button:0,clientX:200,clientY:150,stopPropagation(){stopped=true;}});
assert.ok(stopped,'drag does not start viewport panning');
const zoomBefore=scale(),dxPixels=100,dyPixels=40;
windowListeners.pointermove({pointerId:22,clientX:200+dxPixels,clientY:150+dyPixels,preventDefault(){}});
assert.ok(Math.abs(xFromNode(movedId)-(initialX+Math.round(dxPixels/zoomBefore)))<=1,'drag converts screen displacement by zoom');
assert.ok(Math.abs(yFromNode(movedId)-(initialY+Math.round(dyPixels/zoomBefore)))<=1,'drag moves node vertically');
const edgePathsAfter=document.getElementById('edges').children.filter(n=>n.tagName==='path').map(n=>n.attributes.d).join('|');
assert.notEqual(edgePathsAfter,edgePathsBefore,'connectors move with the dragged node');
windowListeners.pointerup({pointerId:22});
const storageKey='cyoa-storyboard-layout-v1:prologue-00';
assert.ok(storage.has(storageKey),'browser storage saved node layout');
assert.equal(JSON.parse(storage.get(storageKey)).positions[movedId].x,xFromNode(movedId),'saved coordinate matches node');
assert.equal(document.getElementById('exportLayout').disabled,false,'layout export available');

// Reloading the same chapter through the chapter selector restores the browser's saved layout.
document.getElementById('chapterSelect').listeners.change({target:{value:'0'}});
await new Promise(resolve=>setTimeout(resolve,20));
assert.equal(xFromNode(movedId),Math.round(initialX+dxPixels/zoomBefore),'manual position survives chapter reload');

// Importing a shared layout takes precedence over the prior browser coordinates.
const customX=initialX+260,customY=initialY+210;
const input=document.getElementById('fileLayout');
input.files=[{name:'custom-layout.json',text:async()=>JSON.stringify({schema:'cyoa-storyboard-layout-v1',chapters:{'prologue-00':{positions:{[movedId]:{x:customX,y:customY}}}}})}];
await input.onchange({target:input});
assert.equal(xFromNode(movedId),customX,'imported layout updates visible diagram');
assert.equal(yFromNode(movedId),customY,'imported layout Y position applied');
assert.equal(JSON.parse(storage.get(storageKey)).positions[movedId].x,customX,'imported layout is cached');

// Reset restores automatic layout and saves an empty override (even if a shared layout exists).
document.getElementById('resetLayout').onclick();
assert.equal(xFromNode(movedId),initialX,'reset returns node to calculated position');
assert.equal(yFromNode(movedId),initialY,'reset returns node to automatic Y');
assert.deepEqual(JSON.parse(storage.get(storageKey)).positions,{},'reset stored empty positions');
document.getElementById('exportLayout').onclick();

// ---- Chapters: header, independent graphs/inspectors, independent layouts and selections ----------
const select=document.getElementById('chapterSelect');
assert.deepEqual(select.children.map(o=>[o.value,o.textContent]),[['0','Prologue — The Last Good Day'],['1','Chapter 1 — House of Tomorrow'],['2','Chapter 2 — Biology Park'],['3',"Chapter 3 — The People's Pavilion"]],'header dropdown lists all four manifest chapters in order');
const switchTo=async index=>{select.listeners.change({target:{value:String(index)}});await new Promise(resolve=>setTimeout(resolve,20));};
const nodeIds=()=>document.getElementById('nodes').children.map(n=>n.children[0]?.textContent);
const dragNode=(id,dx,dy,pointerId)=>{
  const card=findNode(id);assert.ok(card,'node on graph '+id);
  card.listeners.pointerdown({pointerId,button:0,clientX:300,clientY:300,stopPropagation(){}});
  windowListeners.pointermove({pointerId,clientX:300+dx,clientY:300+dy,preventDefault(){}});
  windowListeners.pointerup({pointerId});
  return {x:xFromNode(id),y:yFromNode(id)};
};
// 1. Move two Prologue nodes and select one.
const proA=dragNode('drone_intercepts',140,90,31),proB=dragNode('reception_hallway',-120,60,32);
findNode('reception_hallway').click();
assert.ok(flatten(pane()).some(x=>x.textContent==='Reception Hallway'),'prologue hand-off node selected');
const handoffCard=flatten(pane()).find(x=>x.tagName==='button'&&String(x.textContent).startsWith('CONTINUE'));
assert.ok(handoffCard&&!handoffCard.disabled&&/Chapter 1 — House of Tomorrow \(chapter-01\)/.test(flatten(handoffCard).map(x=>x.textContent).join(' ')),'hand-off card names its Chapter 1 destination and is clickable');
assert.ok(String(findNode('reception_hallway').children[2].textContent).includes('→ chapter-01'),'diagram card shows the cross-chapter exit');
// 2. Switch to Chapter 1: its own graph, inspector, choices and art references.
await switchTo(1);
assert.equal(select.value,'1','selector shows Chapter 1');
assert.equal(nodeIds().length,36,'Chapter 1 graph shows all 36 authored nodes');
assert.match(document.getElementById('chapterTitle').textContent,/^Chapter 1 — House of Tomorrow · draft$/,'board heading names the chapter and its draft status');
assert.ok(flatten(pane()).some(x=>x.textContent==='House Arrival'),'Chapter 1 inspector opens on its authored start node');
assert.ok(flatten(pane()).some(x=>/HOUSE OF TOMORROW/.test(String(x.textContent))),'House arrival narration appears in the inspector');
const ch1Art=flatten(pane()).find(x=>x.tagName==='button'&&String(x.textContent).includes('HOUSE OF TOMORROW'));
assert.ok(ch1Art&&flatten(ch1Art).some(x=>/scenes\/house_of_tomorrow\/arrival · not-started/.test(String(x.textContent))),'House arrival art resolves through shared catalog as not-started');
assert.ok(!flatten(pane()).some(x=>/facilities_corridor/.test(String(x.textContent))),'Chapter 1 does not borrow the facilities corridor art');
assert.ok(flatten(pane()).some(x=>/PUSH OPEN THE DISPLAY ENTRANCE/.test(String(x.textContent))),'authored arrival choice appears in the Chapter 1 inspector');
// 3. Move the Chapter 1 node.
const ch1=dragNode('house_arrival',210,130,33);
assert.ok(storage.has('cyoa-storyboard-layout-v1:chapter-01'),'Chapter 1 positions cached under their own key');
assert.equal(JSON.parse(storage.get(storageKey)).positions.drone_intercepts.x,proA.x,'moving Chapter 1 left the Prologue cache alone');
// 4. Switch back: Prologue arrangement and selection survive.
await switchTo(0);
assert.equal(select.value,'0');
assert.ok(nodeIds().length===29&&nodeIds().includes('reception_hallway'),'Prologue graph restored');
assert.deepEqual({x:xFromNode('drone_intercepts'),y:yFromNode('drone_intercepts')},proA,'Prologue node A position survives a chapter switch');
assert.deepEqual({x:xFromNode('reception_hallway'),y:yFromNode('reception_hallway')},proB,'Prologue node B position survives a chapter switch');
assert.ok(flatten(pane()).some(x=>x.textContent==='Reception Hallway'),'Prologue selection restored after the round trip');
// The hand-off card opens Chapter 1 directly, with its layout intact.
flatten(pane()).find(x=>x.tagName==='button'&&String(x.textContent).startsWith('CONTINUE')).click();
await new Promise(resolve=>setTimeout(resolve,20));
assert.equal(select.value,'1','hand-off card opens Chapter 1 and the selector follows');
assert.deepEqual({x:xFromNode('house_arrival'),y:yFromNode('house_arrival')},ch1,'Chapter 1 position survives');
// Chapter 1 surviving exits name Chapter 2; the fatal chair ending does not.
for(const exitId of ['exit_named_plant','exit_martin','exit_service_clean','exit_service_registered','exit_showroom_reset'])
  assert.ok(String(findNode(exitId).children[2].textContent).includes('→ chapter-02'),'Chapter 1 exit '+exitId+' links to Chapter 2');
assert.ok(!String(findNode('exit_chair_fatal').children[2].textContent).includes('→ chapter-02'),'fatal chair ending does not link to Chapter 2');
findNode('exit_martin').click();
const ch2Card=flatten(pane()).find(x=>x.tagName==='button'&&/Chapter 2 — Biology Park \(chapter-02\)/.test(flatten(x).map(y=>y.textContent).join(' ')));
assert.ok(ch2Card&&!ch2Card.disabled,'Chapter 1 exit card names its Chapter 2 destination and is clickable');
ch2Card.click();
await new Promise(resolve=>setTimeout(resolve,20));
// 4b. Chapter 2: its own graph, inspector, choices, art references and layout cache.
assert.equal(select.value,'2','exit card opens Chapter 2 and the selector follows');
assert.equal(nodeIds().length,99,'Chapter 2 graph shows all 99 authored nodes');
assert.match(document.getElementById('chapterTitle').textContent,/^Chapter 2 — Biology Park · draft$/,'board heading names Chapter 2 and its draft status');
assert.ok(flatten(pane()).some(x=>x.textContent==='Bureau Arrival'),'Chapter 2 inspector opens on its authored start node');
assert.ok(flatten(pane()).some(x=>/scenes\/biology_park\/conveniences_bureau · not-started/.test(String(x.textContent))),'Bureau art resolves through the shared catalog as not-started');
findNode('public_kit_focus').click();
assert.ok(flatten(pane()).some(x=>/USE THE ANTIDOTE DIRECTLY FROM THE OPEN KIT/.test(String(x.textContent))),'Chapter 2 focus node choices appear in the inspector');
const ch2=dragNode('park_junction',170,-80,34);
findNode('end_public').click();
const ch3Link=flatten(pane()).find(x=>x.tagName==='button'&&String(x.textContent).includes('PREVIEW NEXT CHAPTER'));
assert.ok(ch3Link&&!ch3Link.disabled,'Chapter 2 ending provides Chapter 3 storyboard handoff');
ch3Link.click();
await new Promise(resolve=>setTimeout(resolve,20));
assert.equal(select.value,'3','chapter transition opens Chapter 3');
assert.equal(nodeIds().length,62,'Chapter 3 graph shows 62 nodes');
findNode('end_model_citizen').click();
assert.ok(flatten(pane()).some(x=>String(x.textContent).includes('ILLUSTRATION PENDING')),'fatal popup design preview');
assert.ok(flatten(pane()).some(x=>String(x.textContent).includes('A MODEL CITIZEN')),'fatal popup title');
await switchTo(2);
assert.ok(storage.has('cyoa-storyboard-layout-v1:chapter-02'),'Chapter 2 positions cached under their own key');
await switchTo(1);
assert.deepEqual({x:xFromNode('house_arrival'),y:yFromNode('house_arrival')},ch1,'Chapter 1 position survives a Chapter 2 visit');
await switchTo(2);
assert.deepEqual({x:xFromNode('park_junction'),y:yFromNode('park_junction')},ch2,'Chapter 2 position survives a round trip');
await switchTo(0);
// 5. Export, then import into a fresh browser (empty storage): both arrangements survive.
downloads.length=0;
document.getElementById('exportLayout').onclick();
assert.equal(downloads.length,1,'one layout file exported');
const exported=JSON.parse(await downloads[0].text());
assert.equal(exported.schema,'cyoa-storyboard-layout-v1','exported schema unchanged');
assert.deepEqual(Object.keys(exported.chapters).sort(),['chapter-01','chapter-02','chapter-03','prologue-00'],'export holds all four chapters');
assert.deepEqual(exported.chapters['chapter-02'].positions.park_junction,ch2,'export holds Chapter 2');
assert.deepEqual(exported.chapters['prologue-00'].positions.drone_intercepts,proA,'export holds Prologue A');
assert.deepEqual(exported.chapters['prologue-00'].positions.reception_hallway,proB,'export holds Prologue B');
assert.deepEqual(exported.chapters['chapter-01'].positions.house_arrival,ch1,'export holds Chapter 1');
// A second viewer instance: fresh DOM, empty browser storage, committed layout file.
async function freshViewer(seed={}){
  const els=new Map(),store=new Map(Object.entries(seed)),wl={};
  const doc={getElementById(id){if(!els.has(id))els.set(id,new Element('div',id));return els.get(id);},createElement(tag){return new Element(tag);},createElementNS(_ns,tag){return new Element(tag);},body:new Element('body')};
  const ls={getItem:k=>store.has(k)?store.get(k):null,setItem:(k,v)=>store.set(k,v),removeItem:k=>store.delete(k)};
  vm.runInNewContext(script,{document:doc,window:{addEventListener(n,f){wl[n]=f;},localStorage:ls},location:{href:'https://example.org/CYOA-storyboard/tools/storyboard/'},
    fetch:load,URL:QAURL,Blob,JSON,Object,Math,Number,String,console,setTimeout(fn){fn();return 0;}});
  await new Promise(resolve=>setTimeout(resolve,20));
  return {doc,store};
}
const v2=await freshViewer();
const pos2=id=>{const n=v2.doc.getElementById('nodes').children.find(c=>c.children[0]?.textContent===id);return n&&{x:parseFloat(n.style.left),y:parseFloat(n.style.top)};};
assert.notDeepEqual(pos2('drone_intercepts'),proA,'fresh browser starts from the committed (automatic) Prologue layout');
const in2=v2.doc.getElementById('fileLayout');
in2.files=[{name:'storyboard-layout.json',text:async()=>JSON.stringify(exported)}];
await in2.onchange({target:in2});
assert.deepEqual(pos2('drone_intercepts'),proA,'imported Prologue A applied');
assert.deepEqual(pos2('reception_hallway'),proB,'imported Prologue B applied');
assert.ok(v2.store.has('cyoa-storyboard-layout-v1:chapter-01'),'import cached the Chapter 1 layout too (not only the open chapter)');
v2.doc.getElementById('chapterSelect').listeners.change({target:{value:'1'}});
await new Promise(resolve=>setTimeout(resolve,20));
assert.deepEqual(pos2('house_arrival'),ch1,'imported Chapter 1 arrangement survives in the fresh browser');
assert.ok(v2.store.has('cyoa-storyboard-layout-v1:chapter-02'),'import cached the Chapter 2 layout too');
v2.doc.getElementById('chapterSelect').listeners.change({target:{value:'2'}});
await new Promise(resolve=>setTimeout(resolve,20));
assert.deepEqual(pos2('park_junction'),ch2,'imported Chapter 2 arrangement survives in the fresh browser');
v2.doc.getElementById('chapterSelect').listeners.change({target:{value:'1'}});
await new Promise(resolve=>setTimeout(resolve,20));
// An import naming only one chapter leaves the other chapter's arrangement alone.
in2.files=[{name:'only-prologue.json',text:async()=>JSON.stringify({schema:'cyoa-storyboard-layout-v1',chapters:{'prologue-00':{positions:{}}}})}];
await in2.onchange({target:in2});
assert.deepEqual(pos2('house_arrival'),ch1,'a Prologue-only import does not touch Chapter 1');
v2.doc.getElementById('exportLayout').onclick();
const exported2=JSON.parse(await downloads.at(-1).text());
assert.deepEqual(exported2.chapters['chapter-01'].positions.house_arrival,ch1,'Chapter 1 survives a partial import in the export');
assert.deepEqual(exported2.chapters['prologue-00'].positions,{},'Prologue import applied');
// A browser that saved Chapter 1 earlier still exports it even if only the Prologue is opened.
const v3=await freshViewer({'cyoa-storyboard-layout-v1:chapter-01':JSON.stringify({positions:{house_arrival:ch1}})});
assert.equal(v3.doc.getElementById('chapterSelect').value,'0','third viewer opened only the Prologue');
v3.doc.getElementById('exportLayout').onclick();
assert.deepEqual(JSON.parse(await downloads.at(-1).text()).chapters['chapter-01'].positions.house_arrival,ch1,'export includes this browser\'s saved Chapter 1 layout without opening Chapter 1');

console.log(JSON.stringify({
 result:'PASS',nodes:Object.keys(chapter.nodes).length,chapters:manifest.chapters.map(c=>c.id),
 artRecords:productionRecords.length,
 checked:['manifest','all scene references','portrait references','all item artwork','paired scene backgrounds','editable portrait background','startup','artwork library','edit prompt','export artwork','item links','SHOW branches','branch proximity','pointer-centered wheel zoom','node drag','live connectors','local saved layout','reload layout','import layout','reset layout','chapter header','per-chapter graph+inspector+art refs','cross-chapter hand-off link','independent positions+selection across switches','export all four chapters','Chapter 2 graph+inspector+art refs+layout','Chapter 1 exits link Chapter 2','import into fresh browser','partial import keeps other chapter']
}));
