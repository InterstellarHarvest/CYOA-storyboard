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
assert.equal(artwork.scenes['workplace/corridor'].portraitBackground.status,'integrated','corridor paired portrait background integrated');
assert.equal(artwork.scenes['exposition/reception'].portraitBackground.status,'reused','approved reception background reuse');
const productionRecords=[
  ...Object.values(artwork.scenes).flatMap(scene=>[scene,...(scene.portraitBackground?[scene.portraitBackground]:[])]),
  ...Object.values(artwork.portraits),
  ...Object.values(artwork.items).flatMap(variants=>Object.values(variants)),
  ...Object.values(artwork.focus||{}),
  ...Object.values(artwork.deathScreens||{})
];
// 169 -> 171 (2026-11-17, docs/106): the owner-approved pavilion_satisfaction_certificate adds its pending slot + inspect requirements.
assert.equal(productionRecords.length,171,'shared art catalog includes death-popup illustrations for all fatal endpoints');
// docs/105 allows genuinely new, unselected candidates to be generated. Keep
// legacy selection/integration assertions below; never confuse new candidates
// with a regression of already selected artwork.
const batch2SelectedHashes={
 'control_tower':'fde023d3741641aa0f376ad1ac65508de3aeef84a05a8be0defecb3f4603daca',
 'spore_garden':'aded321d36cf2ea9c50d3d696230fe2a1606f181ff8fc0d1f2f7bffb92af4ed3',
 'tour_tram':'fd2b01dbff9db37a79b5a1519b0adc5be3ce8e60c425d7bfb039a5a2194f6d57',
 'damaged_walkway':'8ca919bedda4f414a7bfac7bfc1f0003f8531e7fcee36ce8f2873db0985af642',
 'moving_forest':'5a1f61ab9c8a1c7fac129683df09da9bae48a0f22adb9012d98183e0d10f5c81',
 'overgrown_tram':'d4c381642d2d54e6341fd82121ddcf5caef11029fa37c16d221edd5173d470c7',
 'sensor_gallery':'b2f23c8d015c1f45af200733ba28201627c6d10102dcd9e34b92230c32683a7c'
};
const selectedPreviews=JSON.parse(fs.readFileSync(path.join(root,'story/artwork-preview.json'),'utf8')).images;
for(const [name,hash] of Object.entries(batch2SelectedHashes)){
  const id='biology_park/'+name;
  const record=artwork.scenes[id];
  assert.ok(['approved','integrated'].includes(record.status),'owner-selected Batch2 image never returns to candidate status: '+id);
  const preview=selectedPreviews['scenes:'+id];
  assert.equal(preview.sha256,hash,'exact owner-selected Batch2 bytes: '+id);
  // Selected-only previews cite the owner approval commit; once a tested game build publishes the image as
  // integrated (docs/105 step 4) its preview cites that build at the production path, and the approval commit
  // stays recorded in the record's notes. The bytes (sha256 above) never change.
  if(record.status==='integrated'){assert.equal(preview.source.repo,'InterstellarHarvest/CYOA','integrated preview cites the game build: '+id);assert.equal(preview.source.path,record.assetPath,'integrated preview cites the production path: '+id);assert.ok(record.notes.includes('ed098eee6999b25d44a6b4db2ad7605e430d88c6'),'owner approval commit kept in notes: '+id);}
  else assert.equal(preview.source.commit,'ed098eee6999b25d44a6b4db2ad7605e430d88c6','exact owner approval commit: '+id);
  if(record.status==='approved'&&record.assetPath!==null)assert.equal(record.assetPath,'art/scenes/'+id+'.png','an approved record carries only the production path assigned at integration (docs/105): '+id);
  if(record.assetPath!==null)assert.equal(preview.file,'assets/selected/'+record.assetPath,'the preview mirrors the production path: '+id);
}
// New batches can be generated without changing a fixed count in this test.
// Previously selected images remain protected by the pinned checks and check-canon.
for(const record of productionRecords.filter(r=>r.status==='generated')){
  assert.equal(record.assetPath,null,'unselected candidate has no production path');
  assert.match(record.notes,/CANDIDATE GENERATED .*commit [0-9a-f]{40}; path review\/chapter-02-batch\d+-[^;]+; SHA-256 [0-9a-f]{64}\./,'generated candidate has full source provenance');
}
assert.equal(productionRecords.filter(r=>r.status==='reused').length,5,'approved reused records unchanged');
assert.equal(artwork.deathScreens['house_of_tomorrow/rest_assured_voluntary'],undefined,'one shared Rest Assured death record (owner ruling docs/104), no per-cause duplicate');
assert.ok(['approved','integrated'].includes(artwork.deathScreens['house_of_tomorrow/rest_assured']?.status),'owner-approved Rest Assured death screen is selected, never pending');
const restAssuredUsed=artwork.deathScreens['house_of_tomorrow/rest_assured']?.status==='integrated'?1:0;
assert.ok(productionRecords.filter(r=>r.status==='integrated').length>=46+restAssuredUsed,'previously used game artwork remains integrated');
assert.ok(productionRecords.filter(r=>['approved','integrated'].includes(r.status)).length>=54+Object.keys(batch2SelectedHashes).length,'legacy selections and seven Batch2 selections remain selected');
assert.ok(productionRecords.filter(r=>['not-started','generated'].includes(r.status)).every(r=>r.assetPath==null),'unfinished or unselected records never invent production paths');
assert.ok(['approved','integrated'].includes(artwork.scenes['biology_park/conveniences_bureau']?.status),'Chapter 2 Bureau artwork already selected');
assert.ok([null,'art/scenes/biology_park/conveniences_bureau.png'].includes(artwork.scenes['biology_park/conveniences_bureau']?.assetPath),'Chapter 2 Bureau has no production path, or exactly the one assigned at integration (docs/105)');
if(artwork.scenes['biology_park/conveniences_bureau']?.status==='integrated')assert.equal(artwork.scenes['biology_park/conveniences_bureau'].assetPath,'art/scenes/biology_park/conveniences_bureau.png','integrated Bureau art names its production path');
assert.equal(artwork.scenes['house_of_tomorrow/arrival']?.status,'integrated','Chapter 1 arrival artwork is already used in review game');
assert.equal(artwork.scenes['house_of_tomorrow/arrival']?.assetPath,'art/scenes/house_of_tomorrow/arrival.png','selected Chapter 1 arrival production path');
for(const record of productionRecords){
  if(record.status==='integrated')assert.ok(record.assetPath?.endsWith('.png')
      || Object.values(record.views||{}).some(v=>v.assetPath?.endsWith('.png'))
      || (record.pages||[]).some(v=>v.assetPath?.endsWith('.png')),'integrated artwork has selected PNG source: '+record.title);
}
assert.ok(artwork.deathScreens['pavilion/a_model_citizen']?.prompt,'death screen art registered');
assert.equal(Object.keys(artwork.deathScreens).length,9,'nine fatal terminals and nine death-art source records');
assert.ok(['approved','integrated'].includes(artwork.deathScreens['house_of_tomorrow/rest_assured'].status),'selected Rest Assured picture is already approved (integrated once the game reports it)');
assert.equal(artwork.deathScreens['house_of_tomorrow/rest_assured'].selectedSource.sha256,
  '7f469efa40548568af5dfe3c11602b9c6293282d9574caa5f36fc37113e72d9c','exact original owner-selected Rest Assured art SHA');
for(const rec of Object.values(artwork.deathScreens))assert.equal(rec.dimensions,'314x206','all death-popup artworks share the approved A1 illustration format');

assert.equal(artwork.portraits['house:idle'].status,'integrated','opaque House intercom views selected');
// docs/107 Batch B: lounge + dining views were BRIEFS (not-started, no image) until selected; owner-approved v02 selections 2026-11-18 (sha-pinned in artwork-preview.json).
const houseBriefViews=['house_of_tomorrow/lounge','house_of_tomorrow/dining'];
assert.ok(Object.entries(artwork.portraits['house:idle'].views).every(([k,v])=>houseBriefViews.includes(k)||(v.status==='integrated'&&v.assetPath)),'House conversation views selected');
for(const k of houseBriefViews){const v=artwork.portraits['house:idle'].views[k];assert.ok(v&&(v.status==='not-started'?v.assetPath===null:(['approved','integrated'].includes(v.status)&&v.assetPath==='art/portraits/house/'+k.split('/')[1]+'_conversation.png')),'House '+k+' view is a brief until selected, then carries its production path');}
assert.equal(artwork.focus['house_of_tomorrow/portrait_gallery/album'].status,'integrated','family album selected');
assert.ok(artwork.focus['house_of_tomorrow/portrait_gallery/album'].pages.every(p=>p.status==='integrated'&&p.assetPath),'three selected album pages');
assert.ok(artwork.scenes['house_of_tomorrow/storage'].states.every(v=>v.status==='integrated'&&v.assetPath),'all used House storage variants');
assert.equal(artwork.scenes['house_of_tomorrow/chair'].states.find(v=>v.id==='default_unrestrained').status,'approved','unbound selected alternative is approved, not falsely marked displayed');
assert.ok(['approved','integrated'].includes(artwork.scenes['biology_park/groundskeeper'].portraitBackground.status),'groundskeeper background selected');
assert.ok(['approved','integrated'].includes(artwork.portraits['groundskeeper:idle'].status),'groundskeeper foreground selected');
assert.ok(artwork.scenes['biology_park/conveniences_bureau'].notes.includes('SHA-256'),'chosen Biology Park candidate version pinned');
assert.equal(artwork.scenes['pavilion/human_behavior_workshop']?.assetPath,null,'workshop art pending');
// Public storyboard intentionally mirrors metadata, not private generated images.

for(const portrait of Object.values(artwork.portraits)){
  if(portrait.format==='opaque-complete'){
    assert.ok(Object.values(portrait.views||{}).length>=1,'House intercom uses complete scene-specific opaque views');
    assert.ok(Object.entries(portrait.views).every(([k,view])=>houseBriefViews.includes(k)||(view.status==='integrated'&&view.assetPath)),'all selected House portrait views integrated');
    continue;
  }
  assert.equal(portrait.foregroundFormat,'transparent-rgba-png','layered NPC foreground remains transparent');
  assert.ok(artwork.scenes[portrait.portraitBackgroundScene]?.portraitBackground,"layered NPC scene background exists");
}
assert.equal(manifest.layout,'storyboard-layout.json');
const layoutSource=JSON.parse(fs.readFileSync(path.join(root,'story',manifest.layout),'utf8'));
assert.equal(layoutSource.schema,'cyoa-storyboard-layout-v1');

// The header lists exactly the manifest's chapters, in order; every chapter's art resolves through
// the ONE shared artwork catalog (no per-chapter art catalogs).
assert.deepEqual(manifest.chapters.map(c=>[c.id,c.title,c.status]),[
  ['prologue-00','Prologue — The Last Good Day','draft'],['chapter-01','Chapter 1 — House of Tomorrow','draft'],['chapter-02','Chapter 2 — Biology Park','draft'],['chapter-03',"Chapter 3 — The People's Pavilion",'draft']],'manifest chapters, order, titles, draft status');
const chapters=manifest.chapters.map(c=>JSON.parse(fs.readFileSync(path.join(root,'story',c.file),'utf8')));
const fatalIds={
  'chapter-01':['exit_chair_fatal'],
  'chapter-02':['fatal_sorter','fatal_hopper','fatal_transformation','fatal_planting','fatal_roots'],
  'chapter-03':['end_model_citizen','end_reconciled','end_archived']
};
for(const [i,entry] of manifest.chapters.entries()){
  for(const id of fatalIds[entry.id]||[]){
    const n=chapters[i].nodes[id];
    assert.ok(n?.end,'fatal node is an ending: '+id);
    assert.ok(n.deathPopup?.title && n.deathPopup?.description,'fatal popup title and punchline exist: '+id);
    assert.ok(n.endingArt && n.endingArt===n.deathPopup.artRef,'single ending art and popup art refer to same record: '+id);
    assert.ok(artwork.deathScreens[n.endingArt],'death art brief registered: '+id);
  }
}
const chair=chapters[1].nodes;
assert.equal(chair.exit_chair_fatal.deathPopup.artRef,'house_of_tomorrow/rest_assured','all three Rest Assured deaths use one approved illustration');
assert.equal(Object.values(chair).flatMap(n=>(n.choices||[]).flatMap(c=>[c.to,c.pass?.to,c.fail?.to].filter(Boolean))).filter(to=>to==='exit_chair_fatal').length,3,'three Rest Assured arrival routes share one fatal node');

for(const ch of chapters){
  for(const scene of new Set([ch.scene,...Object.values(ch.nodes).map(x=>x.scene).filter(Boolean)]))
    assert.ok(artwork.scenes[scene],'scene reference '+scene);
  for(const n of Object.values(ch.nodes)){
    if(n.speaker)assert.ok(artwork.portraits[n.speaker+':'+(n.pose||'default')],'portrait '+n.speaker);
    if(n.focus)assert.ok(artwork.focus[n.focus],'focus '+n.focus);
    if(n.endingArt)assert.ok(artwork.deathScreens[n.endingArt],'death screen '+n.endingArt);
    if(n.deathPopup?.artRef)assert.ok(artwork.deathScreens[n.deathPopup.artRef],'fatal popup art '+n.deathPopup.artRef);
  }
}
assert.deepEqual(Object.keys(layoutSource.chapters),['prologue-00','chapter-01','chapter-02','chapter-03'],'layout has four chapters');
assert.deepEqual(layoutSource.chapters['prologue-00'].positions,{},'prologue positions retained exactly (none committed)');
const legacyFixture=JSON.parse(fs.readFileSync(path.join(root,'tools/storyboard/qa-fixtures/legacy-render-snapshot.json'),'utf8'));
assert.equal(Object.keys(chapters[3].nodes).length,legacyFixture['chapter-03'].cards.length,'Chapter 3 node count matches its committed renderer snapshot');
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
const columnXs=[...new Set(graphNodes.map(n=>parseFloat(n.style.left)))].sort((a,b)=>a-b);
assert.equal(columnXs.indexOf(noticeX)-columnXs.indexOf(openingX),1,'notice reply occupies next timeline column');
const noticeGap=Math.abs(parseFloat(receptionOpen.style.top)-parseFloat(noticeReply.style.top));
assert.ok(noticeGap<=520,'notice reply stays near its parent branch, vertical gap '+noticeGap);
const edgeLabels=flatten(document.getElementById('edges')).filter(x=>x.tagName==='title').map(x=>x.textContent);
assert.ok(edgeLabels.some(s=>/^SHOW: HOLD OUT THE TERMINATION NOTICE/m.test(String(s))),
          'item-triggered route drawn and labeled on graph (SHOW badge + authored action text)');
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
const edgePathsBefore=flatten(document.getElementById('edges')).filter(n=>n.tagName==='path').map(n=>n.attributes.d).join('|');
let stopped=false;
nodeToDrag.listeners.pointerdown({pointerId:22,button:0,clientX:200,clientY:150,stopPropagation(){stopped=true;}});
assert.ok(stopped,'drag does not start viewport panning');
const zoomBefore=scale(),dxPixels=100,dyPixels=40;
windowListeners.pointermove({pointerId:22,clientX:200+dxPixels,clientY:150+dyPixels,preventDefault(){}});
assert.ok(Math.abs(xFromNode(movedId)-(initialX+Math.round(dxPixels/zoomBefore)))<=1,'drag converts screen displacement by zoom');
assert.ok(Math.abs(yFromNode(movedId)-(initialY+Math.round(dyPixels/zoomBefore)))<=1,'drag moves node vertically');
const edgePathsAfter=flatten(document.getElementById('edges')).filter(n=>n.tagName==='path').map(n=>n.attributes.d).join('|');
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
assert.ok(flatten(pane()).some(x=>/plain ivory door with no nameplate/.test(String(x.textContent))),'House arrival narration (unmarked ivory door) appears in the inspector');
assert.ok(!flatten(pane()).some(x=>/complete sign reads HOUSE OF TOMORROW/.test(String(x.textContent))),'superseded HOUSE OF TOMORROW signage prose is gone');
const ch1Art=flatten(pane()).find(x=>x.tagName==='button'&&String(x.textContent).includes('HOUSE OF TOMORROW'));
assert.ok(ch1Art&&flatten(ch1Art).some(x=>/scenes\/house_of_tomorrow\/arrival · integrated/.test(String(x.textContent))),'House arrival art resolves as already integrated');
assert.ok(!flatten(pane()).some(x=>/facilities_corridor/.test(String(x.textContent))),'Chapter 1 does not borrow the facilities corridor art');
assert.ok(flatten(pane()).some(x=>/TRY THE UNMARKED DOOR\./.test(String(x.textContent))),'authored arrival choice appears in the Chapter 1 inspector');
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
findNode('exit_chair_fatal').click();
assert.ok(flatten(pane()).some(x=>String(x.textContent).includes('Death popup · engine handoff')),'fatal inspector displays engine-facing popup details');
assert.ok(flatten(pane()).some(x=>String(x.textContent).includes('PERMANENTLY SATISFIED.')),'fatal card supplies specific popup title');
assert.ok(flatten(pane()).some(x=>String(x.textContent).includes('house_of_tomorrow/rest_assured')),'fatal inspector supplies death artwork identifier');
assert.ok(flatten(pane()).some(x=>String(x.textContent).includes('You have achieved permanent relaxation.')),'fatal inspector supplies popup narrative beat');
assert.ok(!flatten(pane()).some(x=>x.textContent==='Choices & destinations'),'fatal inspector hides legacy restart choice section');
assert.ok(flatten(findNode('exit_chair_fatal')).some(x=>String(x.textContent).includes('ART: house_of_tomorrow/rest_assured')),'fatal graph box itself shows exact artwork ID');
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
assert.ok(flatten(pane()).some(x=>/scenes\/biology_park\/conveniences_bureau · (approved|integrated)/.test(String(x.textContent))),'Bureau artwork appears as selected (approved or integrated)');
findNode('public_kit_focus').click();
assert.ok(flatten(pane()).some(x=>/USE THE ANTIDOTE DIRECTLY FROM THE OPEN KIT/.test(String(x.textContent))),'Chapter 2 focus node choices appear in the inspector');
const ch2=dragNode('park_junction',170,-80,34);
findNode('end_public').click();
const ch3Link=flatten(pane()).find(x=>x.tagName==='button'&&String(x.textContent).includes('PREVIEW NEXT CHAPTER'));
assert.ok(ch3Link&&!ch3Link.disabled,'Chapter 2 ending provides Chapter 3 storyboard handoff');
ch3Link.click();
await new Promise(resolve=>setTimeout(resolve,20));
assert.equal(select.value,'3','chapter transition opens Chapter 3');
assert.equal(nodeIds().length,Object.keys(chapters[3].nodes).length,'Chapter 3 graph shows every authored node');
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
  return {doc,store,wl};
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
// (Saved against the current timeline revision; a save from before the timeline rework is archived
// instead — see the migration checks below.)
const v3=await freshViewer({'cyoa-storyboard-layout-v1:chapter-01':JSON.stringify({positions:{house_arrival:ch1},layoutRevision:2})});
assert.equal(v3.doc.getElementById('chapterSelect').value,'0','third viewer opened only the Prologue');
v3.doc.getElementById('exportLayout').onclick();
assert.deepEqual(JSON.parse(await downloads.at(-1).text()).chapters['chapter-01'].positions.house_arrival,ch1,'export includes this browser\'s saved Chapter 1 layout without opening Chapter 1');

// ==== Chapter 1 / Chapter 2 timeline layout =========================================================
const ch1Json=chapters[1],ch2Json=chapters[2],ch3Json=chapters[3];
const settle=()=>new Promise(resolve=>setTimeout(resolve,20));
const kids=(n,cls)=>flatten(n).filter(x=>String(x.attributes?.class||'').split(' ').includes(cls));
function authoredPairs(ch){
  const pairs=new Set();
  for(const [id,n] of Object.entries(ch.nodes)){
    for(const c of n.choices||[])for(const to of [c.to,c.pass?.to,c.fail?.to])if(to&&ch.nodes[to])pairs.add(id+'>'+to);
    for(const verb of ['show','use'])for(const e of Object.values(n[verb]||{}))if(e?.to&&ch.nodes[e.to])pairs.add(id+'>'+e.to);
  }
  return pairs;
}
function reaches(ch,from,to){
  const seen=new Set([from]),queue=[from];
  while(queue.length){const u=queue.shift();for(const p of authoredPairs(ch)){const [a,b]=p.split('>');if(a===u&&!seen.has(b)){if(b===to)return true;seen.add(b);queue.push(b);}}}
  return false;
}
function snapshot(v){
  const nodes=v.doc.getElementById('nodes').children.map(c=>({id:c.children[0].textContent,x:parseFloat(c.style.left),y:parseFloat(c.style.top),cls:c.className,tag:c.children[3]?.textContent}));
  const ports=v.doc.getElementById('ports').children.map(p=>({x:parseFloat(p.style.left),y:parseFloat(p.style.top),...Object.fromEntries(Object.entries(p.attributes).filter(([k])=>k.startsWith('data-'))),text:flatten(p).map(x=>x.textContent).join(' | '),title:p.title}));
  const svg=v.doc.getElementById('edges');
  const edges=kids(svg,'tl-edge').map(g=>({from:g.attributes['data-from'],to:g.attributes['data-to'],route:g.attributes['data-route'],d:g.children.find(x=>x.attributes.class==='tl-line').attributes.d,title:g.children.find(x=>x.tagName==='title').textContent}));
  const labels=kids(svg,'tl-label').map(g=>{const [x,y]=g.attributes.transform.match(/-?[\d.]+/g).map(Number);const r=g.children.find(c=>c.attributes.class==='plate');
    return {from:g.attributes['data-from'],to:g.attributes['data-to'],x,y,w:Number(r.attributes.width),h:Number(r.attributes.height),title:g.children.find(c=>c.tagName==='title').textContent};});
  return {nodes,ports,edges,labels,stage:v.doc.getElementById('stage').style.transform};
}
const overlaps=(a,b,pad=0)=>a.x<b.x+b.w+pad&&b.x<a.x+a.w+pad&&a.y<b.y+b.h+pad&&b.y<a.y+a.h+pad;
const cardBox=n=>({x:n.x,y:n.y,w:220,h:100,id:n.id});
const portBox=p=>({x:p.x,y:p.y,w:232,h:58,id:p['data-port']});
const tv=await freshViewer();
const tSwitch=async(v,i)=>{v.doc.getElementById('chapterSelect').listeners.change({target:{value:String(i)}});await settle();};
const shots={};
for(const [index,ch,count] of [[0,chapters[0],29],[1,ch1Json,36],[2,ch2Json,99]]){
  await tSwitch(tv,index);
  const s=snapshot(tv),key=manifest.chapters[index].id;shots[key]=s;
  assert.equal(s.nodes.length,count,key+': all '+count+' authored nodes rendered as cards');
  assert.equal(new Set(s.nodes.map(n=>n.id)).size,count,key+': each node rendered once');
  assert.ok(s.nodes.every(n=>/\bnode tl\b/.test(n.cls)),key+': timeline cards');
  assert.equal(s.stage,'scale(1)',key+': opens at reading zoom (100%), not shrunk to fit');
  // No overlapping cards, ports or labels (labels also never sit on a card or a port).
  const boxes=[...s.nodes.map(cardBox),...s.ports.map(portBox)];
  for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++)assert.ok(!overlaps(boxes[i],boxes[j],8),key+': '+boxes[i].id+' and '+boxes[j].id+' do not overlap');
  for(let i=0;i<s.labels.length;i++){
    for(let j=i+1;j<s.labels.length;j++)assert.ok(!overlaps(s.labels[i],s.labels[j],1),key+': labels '+s.labels[i].from+'>'+s.labels[i].to+' / '+s.labels[j].from+'>'+s.labels[j].to+' do not collide');
    for(const b of boxes)assert.ok(!overlaps(s.labels[i],b,2),key+': label '+s.labels[i].from+'>'+s.labels[i].to+' clear of '+b.id);
  }
  // Every authored destination is drawn, and nothing that is not authored.
  const drawn=new Set(s.edges.filter(e=>e.route!=='port').map(e=>e.from+'>'+e.to));
  assert.deepEqual([...drawn].sort(),[...authoredPairs(ch)].sort(),key+': every authored route drawn exactly once, none invented');
  // Full authored choice text stays available on hover (connector and label tooltips).
  const tips=s.edges.map(e=>e.title).join('\n');
  for(const [id,n] of Object.entries(ch.nodes))for(const c of n.choices||[])if(c.to||c.pass||c.fail)assert.ok(tips.includes(c.text||c.id),key+': hover text for '+id+' / '+c.id);
  // Left-to-right: every forward route moves right; only genuine cycles use explicit return connectors.
  const at=Object.fromEntries(s.nodes.map(n=>[n.id,n]));
  for(const e of s.edges.filter(e=>e.route!=='port')){
    if(e.route==='return'){assert.ok(at[e.to].x<at[e.from].x&&reaches(ch,e.to,e.from),key+': return '+e.from+'>'+e.to+' closes a real cycle');continue;}
    assert.equal(e.route,'forward');
    assert.ok(at[e.to].x>at[e.from].x,key+': forward route '+e.from+'>'+e.to+' runs left to right');
  }
  // Every connector is labelled except a lone CONTINUE (the only way on from a card).
  const labelled=new Set(s.labels.map(l=>l.from+'>'+l.to));
  for(const e of s.edges.filter(e=>e.route!=='port')){
    const n=ch.nodes[e.from],dests=new Set([...authoredPairs(ch)].filter(p=>p.startsWith(e.from+'>')));
    const lone=dests.size===1&&!(n.choices||[]).some(c=>c.chapter)&&!n.storyboardNextChapter&&!Object.keys(n.show||{}).length&&!Object.keys(n.use||{}).length&&(n.choices||[]).filter(c=>c.to===e.to).every(c=>/^CONTINUE\.?$/i.test(c.text||''))&&!(n.choices||[]).some(c=>c.pass||c.fail);
    assert.equal(labelled.has(e.from+'>'+e.to),!lone||e.route==='return',key+': '+e.from+'>'+e.to+(lone?' is a lone CONTINUE (no label)':' carries a label'));
  }
}
// Prologue: timeline view, its hand-off to Chapter 1 on the right, no loops.
const c0=shots['prologue-00'],c0at=Object.fromEntries(c0.nodes.map(n=>[n.id,n]));
assert.equal(c0.edges.filter(e=>e.route==='return').length,0,'Prologue: no cycles, so no return connectors');
assert.equal(c0at.reception_hallway.x,Math.max(...c0.nodes.map(n=>n.x)),'Prologue: the Chapter 1 hand-off sits in the right-hand column');
assert.deepEqual(c0.ports.map(p=>[p['data-port'],p['data-dir'],p['data-mode'],p['data-chapter']]),[['out:reception_hallway>chapter-01','out','gameplay','chapter-01']],'Prologue: one outgoing gameplay route, to Chapter 1');
assert.ok(c0at.work_complete.x===Math.min(...c0.nodes.map(n=>n.x))&&/start/.test(c0at.work_complete.cls),'Prologue: starts at work_complete on the left');
assert.ok(c0.labels.some(l=>/^SHOW: HOLD OUT THE TERMINATION NOTICE\.$/m.test(l.title))&&c0.labels.some(l=>/^SHOW: SHOW THE RECEPTIONIST THE KEY TAG\.$/m.test(l.title)),'Prologue: SHOW item routes carry a SHOW badge and the authored action text');
// Chapter 1: the cycle groups are drawn with return connectors, not pushed to a far column.
const c1=shots['chapter-01'],c1at=Object.fromEntries(c1.nodes.map(n=>[n.id,n]));
const c1returns=c1.edges.filter(e=>e.route==='return').map(e=>e.from+'>'+e.to).sort();
assert.deepEqual(c1returns,['dinner_redirect>dinner_arrival','storage_reclaimed>comfort_offer'],'Chapter 1: one return connector per cycle group');
const c1max=Math.max(...c1.nodes.map(n=>n.x));
const houseExits=['exit_named_plant','exit_martin','exit_service_clean','exit_service_registered','exit_showroom_reset'];
for(const id of houseExits)assert.equal(c1at[id].x,c1max,'Chapter 1: surviving exit '+id+' sits in the right-hand exit column');
assert.ok(c1.nodes.filter(n=>n.x===c1max).every(n=>houseExits.includes(n.id)),'Chapter 1: the exit column holds only the five surviving exits');
const c1out=c1.ports.filter(p=>p['data-dir']==='out');
assert.deepEqual(c1out.map(p=>p['data-port']).sort(),houseExits.map(id=>'out:'+id+'>chapter-02').sort(),'Chapter 1: five outgoing Chapter 2 transitions, one per surviving exit');
assert.ok(c1out.every(p=>p['data-mode']==='gameplay'&&p['data-chapter']==='chapter-02'&&/TO CHAPTER 2 · GAMEPLAY/.test(p.text)&&/Bureau Arrival/.test(p.text)),'Chapter 1: exits are labelled as gameplay transitions into Bureau Arrival');
assert.ok(c1.ports.filter(p=>p['data-dir']==='in').every(p=>p['data-chapter']==='prologue-00'&&p['data-source']==='reception_hallway'),'Chapter 1: its only incoming route is the Prologue hand-off');
assert.ok(/\bfatal\b/.test(c1at.exit_chair_fatal.cls)&&/death-node/.test(c1at.exit_chair_fatal.cls)&&/ART: house_of_tomorrow\/rest_assured/.test(c1at.exit_chair_fatal.tag),'Chapter 1: fatal chair displays its canonical death popup and image rather than legacy choice count');
assert.ok(!c1.edges.some(e=>e.from==='exit_chair_fatal')&&!c1.ports.some(p=>/exit_chair_fatal/.test(p['data-port'])),'Chapter 1: fatal chair is terminal (no route out, no chapter port)');
assert.ok(c1at.exit_chair_fatal.x===c1at.service_breach.x&&c1at.exit_chair_fatal.x>c1at.chair_locked.x&&c1at.exit_chair_fatal.x<c1max,'Chapter 1: fatal chair sits in the column right after the chair, not in the exit column');
// Chapter 2: incoming Chapter 1 routes, storyboard-only handoffs, antidote loops attached to their exits.
const c2=shots['chapter-02'],c2at=Object.fromEntries(c2.nodes.map(n=>[n.id,n]));
const c2in=c2.ports.filter(p=>p['data-dir']==='in');
assert.deepEqual(c2in.map(p=>p['data-source']).sort(),[...houseExits].sort(),'Chapter 2: five named incoming Chapter 1 routes');
assert.ok(c2in.every(p=>p['data-chapter']==='chapter-01'&&p['data-mode']==='gameplay'&&/FROM CHAPTER 1 EXIT/.test(p.text)),'Chapter 2: incoming ports name Chapter 1');
assert.ok(c2.edges.filter(e=>e.route==='port'&&e.from.startsWith('in:')).every(e=>e.to==='bureau_arrival')&&c2.edges.filter(e=>e.route==='port'&&e.from.startsWith('in:')).length===5,'Chapter 2: all five incoming routes feed the single canonical bureau_arrival');
assert.equal(c2.nodes.length,99,'Chapter 2: no runtime arrival nodes were invented for the incoming routes');
const livingEnds=['end_concourse_robot','end_underground_station','end_public','end_maintenance','end_customs'];
const c2out=c2.ports.filter(p=>p['data-dir']==='out');
assert.deepEqual(c2out.map(p=>p['data-port']).sort(),livingEnds.map(id=>'out:'+id+'>chapter-03:preview').sort(),'Chapter 2: five distinct outgoing Chapter 3 handoffs, one per living ending');
assert.ok(c2out.every(p=>p['data-mode']==='preview'&&/PREVIEW HANDOFF · NOT GAMEPLAY/.test(p.text)&&/not a gameplay transition|no gameplay transition/i.test(p.title)),'Chapter 2: handoffs are labelled storyboard previews, not gameplay transitions');
const fatal2=Object.entries(ch2Json.nodes).filter(([,n])=>n.end===true&&!n.storyboardNextChapter).map(([id])=>id);
assert.equal(fatal2.length,5,'Chapter 2: five fatal endings');
for(const id of fatal2){
  assert.ok(!c2.ports.some(p=>p['data-port'].includes(':'+id+'>')||p['data-port'].includes('out:'+id)),'Chapter 2: fatal '+id+' never connects to a later chapter');
  assert.ok(/fatal/.test(c2at[id].cls),'Chapter 2: '+id+' styled as fatal');
}
for(const id of livingEnds)assert.equal(c2at[id].x,Math.max(...c2.nodes.map(n=>n.x)),'Chapter 2: living ending '+id+' in the right-hand handoff column');
const columnStep=c2at.bureau_emergency.x-c2at.bureau_arrival.x;
for(const [staging,kit,read,end] of [['public_exit_staging','public_kit_focus','public_kit_read_focus','end_public'],['maintenance_exit_staging','maintenance_kit_focus','maintenance_kit_read_focus','end_maintenance'],['customs_exit','customs_kit_focus','customs_kit_read_focus','end_customs']]){
  assert.ok(c2at[kit].x>c2at[staging].x&&c2at[read].x>c2at[kit].x&&c2at[read].x-c2at[staging].x<=3*columnStep,'Chapter 2: '+kit+' loop sits immediately right of '+staging);
  assert.ok(Math.abs(c2at[kit].y-c2at[staging].y)<=320&&Math.abs(c2at[read].y-c2at[staging].y)<=320,'Chapter 2: '+kit+' loop stays level with its exit');
  const ret=c2.edges.filter(e=>e.route==='return').map(e=>e.from+'>'+e.to);
  assert.ok(ret.includes(kit+'>'+staging)&&ret.includes(read+'>'+staging),'Chapter 2: '+kit+' antidote returns drawn as return connectors to '+staging);
  assert.ok(c2.edges.some(e=>e.from===staging&&e.to===end&&e.route==='forward'),'Chapter 2: '+staging+' leads on to '+end);
}
assert.equal(c2.edges.filter(e=>e.route==='return').length,6,'Chapter 2: only the three antidote loops use return connectors');
// PASS and FAIL outcomes stay distinguishable on the diagram.
assert.ok(c2.labels.some(l=>/^PASS: /m.test(l.title))&&c2.labels.some(l=>/^FAIL: /m.test(l.title)),'Chapter 2: PASS and FAIL labels present');
const kitLabel=c2.labels.find(l=>l.from==='public_kit_focus'&&l.to==='public_exit_staging');
assert.ok(kitLabel&&/PASS\|FAIL: USE THE ANTIDOTE DIRECTLY/.test(kitLabel.title),'Chapter 2: a check whose PASS and FAIL share a destination says so explicitly');
// Stable across reloads: a second fresh viewer draws exactly the same timeline.
const tv2=await freshViewer();
for(const [index,key] of [[0,'prologue-00'],[1,'chapter-01'],[2,'chapter-02']]){await tSwitch(tv2,index);assert.deepEqual(snapshot(tv2),shots[key],key+': identical layout and connectors after a reload');}
// Clicking a chapter pill behaves like clicking a card: it is selected and inspected, the chapter does not change.
const pill=sel=>tv2.doc.getElementById('ports').children.find(sel);
const pane2=()=>flatten(tv2.doc.getElementById('details'));
pill(p=>p.attributes['data-source']==='exit_service_registered').listeners.click({});
await settle();
assert.equal(tv2.doc.getElementById('chapterSelect').value,'2','clicking an incoming pill stays in Chapter 2');
assert.ok(pane2().some(x=>x.textContent==='From Chapter 1 — House of Tomorrow — Exit Service Registered'),'incoming pill shows its details in the inspector');
assert.ok(pane2().some(x=>x.textContent==='exit_service_registered (Chapter 1 — House of Tomorrow) → bureau_arrival (Chapter 2 — Biology Park)'),'inspector names the route');
assert.match(pill(p=>p.attributes['data-source']==='exit_service_registered').className,/\bselected\b/,'the selected pill is highlighted');
// The pill is draggable like a card, and its position is saved with the chapter.
const pillPos=id=>{const p=pill(x=>x.attributes['data-port']===id);return {x:parseFloat(p.style.left),y:parseFloat(p.style.top)};};
const pillId='in:chapter-01>exit_service_registered',pill0=pillPos(pillId);
pill(x=>x.attributes['data-port']===pillId).listeners.pointerdown({pointerId:51,button:0,clientX:300,clientY:300,stopPropagation(){}});
tv2.wl.pointermove({pointerId:51,clientX:360,clientY:390,preventDefault(){}});tv2.wl.pointerup({pointerId:51});
assert.deepEqual(pillPos(pillId),{x:pill0.x+60,y:pill0.y+90},'a pill can be dragged');
assert.deepEqual(JSON.parse(tv2.store.get('cyoa-storyboard-layout-v1:chapter-02')).positions[pillId],{x:pill0.x+60,y:pill0.y+90},'the moved pill is saved with Chapter 2');
assert.ok(kids(tv2.doc.getElementById('edges'),'tl-edge').some(g=>g.attributes['data-from']===pillId),'the moved pill keeps its connector');
pill(x=>x.attributes['data-port']===pillId).listeners.click({});
assert.equal(tv2.doc.getElementById('chapterSelect').value,'2','releasing a dragged pill does not navigate');
// Navigation is an explicit inspector button.
pane2().find(x=>x.tagName==='button'&&/^Open Exit Service Registered in Chapter 1/.test(String(x.textContent))).click();
await settle();
assert.equal(tv2.doc.getElementById('chapterSelect').value,'1','the inspector button opens Chapter 1');
assert.ok(pane2().some(x=>x.textContent==='Exit Service Registered'),'and selects the matching Chapter 1 exit');
pill(p=>p.attributes['data-port']==='out:exit_martin>chapter-02').listeners.click({});
await settle();
assert.equal(tv2.doc.getElementById('chapterSelect').value,'1','clicking an outgoing pill stays in Chapter 1');
pane2().find(x=>x.tagName==='button'&&/^Open Chapter 2 — Biology Park at Bureau Arrival/.test(String(x.textContent))).click();
await settle();
assert.equal(tv2.doc.getElementById('chapterSelect').value,'2','Chapter 1 exit pill inspector opens Chapter 2');
assert.ok(pane2().some(x=>x.textContent==='Bureau Arrival'),'at bureau_arrival');
assert.ok(pane2().some(x=>/^FROM Chapter 1 — House of Tomorrow — Exit Martin$/.test(String(x.textContent))),'bureau_arrival inspector lists the incoming Chapter 1 routes');
pane2().find(x=>x.tagName==='button'&&/Exit Martin$/.test(String(x.textContent))).click();
assert.equal(tv2.doc.getElementById('chapterSelect').value,'2','an incoming route in the inspector selects its pill, staying in Chapter 2');
assert.ok(pane2().some(x=>x.textContent==='From Chapter 1 — House of Tomorrow — Exit Martin'),'the route\'s pill is now inspected');
pill(p=>p.attributes['data-port']==='out:end_public>chapter-03:preview').listeners.click({});
assert.ok(pane2().some(x=>/storyboard preview only, not gameplay/.test(String(x.textContent))),'a preview handoff is described as storyboard-only');
pane2().find(x=>x.tagName==='button'&&/^Open Chapter 3/.test(String(x.textContent))).click();
await settle();
assert.equal(tv2.doc.getElementById('chapterSelect').value,'3','preview handoff inspector opens Chapter 3');
assert.equal(tv2.doc.getElementById('ports').children.length,0,'Chapter 3 draws no ports');
// Switching chapters returns to the last view of each chapter (zoom and scroll).
const vp=tv2.doc.getElementById('viewport'),stg=tv2.doc.getElementById('stage');
await tSwitch(tv2,1);
vp.scrollLeft=1234;vp.scrollTop=56;tv2.doc.getElementById('zoomOut').onclick();
const ch1View={t:stg.style.transform,l:vp.scrollLeft,top:vp.scrollTop};
await tSwitch(tv2,3);
vp.scrollLeft=77;vp.scrollTop=88;
await tSwitch(tv2,1);
assert.deepEqual({t:stg.style.transform,l:vp.scrollLeft,top:vp.scrollTop},ch1View,'returning to Chapter 1 restores its zoom and scroll');
await tSwitch(tv2,3);
assert.deepEqual([vp.scrollLeft,vp.scrollTop],[77,88],'returning to Chapter 3 restores its scroll');
await tSwitch(tv2,0);
assert.equal(stg.style.transform,'scale(1)','a chapter not yet visited this session opens at its default view');
// Fit is a whole-graph overview for long timelines (below the old 25% floor); Start returns to reading zoom.
await tSwitch(tv2,2);
tv2.doc.getElementById('fit').onclick();
const fitScale=Number(tv2.doc.getElementById('stage').style.transform.match(/[\d.]+/)[0]);
assert.ok(fitScale<.25&&fitScale>0,'Chapter 2 Fit shows the whole timeline ('+fitScale+')');
tv2.doc.getElementById('tlStart').onclick();
assert.equal(tv2.doc.getElementById('stage').style.transform,'scale(1)','Start returns to reading zoom');

// ==== Layout revision migration: old cached Chapter 1/2 positions never hide the new default =======
const oldCh1={house_arrival:{x:900,y:900},comfort_offer:{x:40,y:40}},oldPro={drone_intercepts:{x:777,y:333}},oldCh3={pavilion_arrival:{x:555,y:444}};
const seed={'cyoa-storyboard-layout-v1:chapter-01':JSON.stringify({positions:oldCh1}),'cyoa-storyboard-layout-v1:chapter-02':JSON.stringify({positions:{}}),
  'cyoa-storyboard-layout-v1:prologue-00':JSON.stringify({positions:oldPro}),'cyoa-storyboard-layout-v1:chapter-03':JSON.stringify({positions:oldCh3})};
const mv=await freshViewer(seed);
assert.deepEqual(JSON.parse(mv.store.get('cyoa-storyboard-layout-v1:prologue-00@archive-r1')).positions,oldPro,'old Prologue arrangement archived for recovery (Prologue now uses the timeline)');
assert.ok(!mv.store.has('cyoa-storyboard-layout-v1:prologue-00'),'stale Prologue entry no longer overrides the timeline');
assert.equal(mv.store.get('cyoa-storyboard-layout-v1:chapter-03'),seed['cyoa-storyboard-layout-v1:chapter-03'],'Chapter 3 cache untouched by the migration');
assert.deepEqual(JSON.parse(mv.store.get('cyoa-storyboard-layout-v1:chapter-01@archive-r1')).positions,oldCh1,'old Chapter 1 arrangement archived for recovery');
assert.ok(!mv.store.has('cyoa-storyboard-layout-v1:chapter-01'),'stale Chapter 1 entry no longer overrides the default');
assert.ok(!mv.store.has('cyoa-storyboard-layout-v1:chapter-02@archive-r1'),'an empty old Chapter 2 entry needs no archive');
const mvPos=id=>{const n=mv.doc.getElementById('nodes').children.find(c=>c.children[0]?.textContent===id);return n&&{x:parseFloat(n.style.left),y:parseFloat(n.style.top)};};
assert.deepEqual(mvPos('drone_intercepts'),{x:c0at.drone_intercepts.x,y:c0at.drone_intercepts.y},'Prologue shows the timeline default despite the old cache');
assert.equal(mv.doc.getElementById('restoreLayout').hidden,false,'Restore previous arrangement offered for the Prologue');
await tSwitch(mv,1);
assert.deepEqual(snapshot(mv).nodes,shots['chapter-01'].nodes,'Chapter 1 shows the new timeline default despite the old cache');
assert.equal(mv.doc.getElementById('restoreLayout').hidden,false,'Restore previous arrangement offered');
assert.match(mv.doc.getElementById('status').textContent,/earlier arrangement was archived/,'status explains the archive');
mv.doc.getElementById('restoreLayout').onclick();
assert.deepEqual(mvPos('house_arrival'),oldCh1.house_arrival,'Restore brings the archived arrangement back');
assert.equal(JSON.parse(mv.store.get('cyoa-storyboard-layout-v1:chapter-01')).layoutRevision,2,'restored arrangement saved against the current revision');
// Reset Layout resets only the selected chapter.
const mvDrag=(id,dx,dy,pointerId)=>{const c=mv.doc.getElementById('nodes').children.find(n=>n.children[0]?.textContent===id);c.listeners.pointerdown({pointerId,button:0,clientX:300,clientY:300,stopPropagation(){}});mv.wl.pointermove({pointerId,clientX:300+dx,clientY:300+dy,preventDefault(){}});mv.wl.pointerup({pointerId});return mvPos(id);};
await tSwitch(mv,2);
const proSaved=mv.store.get('cyoa-storyboard-layout-v1:prologue-00');
const moved2=mvDrag('park_junction',90,60,41);
const ch2Saved=mv.store.get('cyoa-storyboard-layout-v1:chapter-02');
assert.equal(JSON.parse(ch2Saved).layoutRevision,2,'Chapter 2 drag saved with the current revision');
assert.ok(kids(mv.doc.getElementById('edges'),'tl-edge').some(g=>g.attributes['data-to']==='park_junction'),'connectors follow a dragged timeline card');
await tSwitch(mv,1);
mv.doc.getElementById('resetLayout').onclick();
assert.deepEqual(snapshot(mv).nodes,shots['chapter-01'].nodes,'Reset returns Chapter 1 to the timeline default');
assert.equal(mv.store.get('cyoa-storyboard-layout-v1:chapter-02'),ch2Saved,'Reset on Chapter 1 leaves Chapter 2 alone');
assert.equal(mv.store.get('cyoa-storyboard-layout-v1:prologue-00'),proSaved,'Reset on Chapter 1 leaves the Prologue alone');
assert.equal(mv.store.get('cyoa-storyboard-layout-v1:chapter-03'),seed['cyoa-storyboard-layout-v1:chapter-03'],'Reset on Chapter 1 leaves Chapter 3 alone');
assert.ok(mv.store.has('cyoa-storyboard-layout-v1:chapter-01@archive-r1'),'archive survives Reset');
await tSwitch(mv,2);
assert.deepEqual(mvPos('park_junction'),moved2,'Chapter 2 keeps its own arrangement');
// Export carries the revision and timeline metadata; an old v1 file (no revision, no timeline) still imports.
mv.doc.getElementById('exportLayout').onclick();
const ex=JSON.parse(await downloads.at(-1).text());
assert.equal(ex.schema,'cyoa-storyboard-layout-v1','export schema unchanged');
assert.equal(ex.chapters['chapter-01'].layoutRevision,2);assert.equal(ex.chapters['chapter-02'].layoutRevision,2);
assert.ok(ex.chapters['chapter-02'].timeline.incidents.length>=10,'export keeps the incident groups');
assert.equal(ex.chapters['prologue-00'].layoutRevision,2,'Prologue exports its timeline revision');
assert.deepEqual(Object.keys(ex.chapters['chapter-03']),['positions'],'Chapter 3 export entry shape unchanged');
const mvIn=mv.doc.getElementById('fileLayout');
mvIn.files=[{name:'old-v1.json',text:async()=>JSON.stringify({schema:'cyoa-storyboard-layout-v1',chapters:{'chapter-02':{positions:{park_junction:{x:4321,y:765}}}}})}];
await mvIn.onchange({target:mvIn});
assert.deepEqual(mvPos('park_junction'),{x:4321,y:765},'an old-format layout file still imports');
assert.equal(snapshot(mv).nodes[0].cls.includes('tl'),true,'the timeline (incident metadata) survives an import without metadata');
assert.equal(JSON.parse(mv.store.get('cyoa-storyboard-layout-v1:chapter-02')).layoutRevision,2,'imported positions are saved against the current revision');
// Committed layout file: the Chapter 3 entry is exactly as before; every node belongs to an incident.
assert.deepEqual(layoutSource.chapters['chapter-03'],{positions:{}},'committed Chapter 3 layout entry unchanged');
for(const [i,key] of [[0,'prologue-00'],[1,'chapter-01'],[2,'chapter-02']]){
  const listed=layoutSource.chapters[key].timeline.incidents.flatMap(inc=>inc.nodes);
  for(const id of listed)assert.ok(chapters[i].nodes[id],key+' incident names a real node '+id);
  if(key==='prologue-00')assert.deepEqual([...listed].sort(),Object.keys(chapters[i].nodes).sort(),'every Prologue node belongs to exactly one incident');
}

// ==== Chapter 3 keeps its published (pre-timeline) geometry; only its fatal-card contents changed ====
// (The Prologue moved to the timeline view on owner request, so it is checked by the timeline suite.)
const {renderLegacy}=await import('./qa-legacy-render.mjs');
const legacyNow=await renderLegacy(path.join(root,'tools/storyboard/index.html'));
const legacyBase=legacyFixture;
const fatalDetails=new Set(['end_model_citizen','end_reconciled','end_archived']);
function normalizeFatalPresentation(frame){
 const copy=JSON.parse(JSON.stringify(frame));
 copy.cards=copy.cards.map(card=>fatalDetails.has(card.id)
   ? {...card,className:'node',text:[card.id,'FATAL POPUP CONTENT','ART REFERENCE']} : card);
 return copy;
}
assert.deepEqual(normalizeFatalPresentation(legacyNow['chapter-03']),normalizeFatalPresentation(legacyBase['chapter-03']),
 'Chapter 3 geometry, edges, and all nonfatal card details remain identical; only fatal card contents and colors changed');
for(const card of legacyNow['chapter-03'].cards.filter(c=>fatalDetails.has(c.id))){
 const d=chapters[3].nodes[card.id].deathPopup;
 assert.match(card.className,/death-node/,'fatality box visually distinct: '+card.id);
 assert.equal(card.text[1],d.title,'fatality box displays actual engine popup title: '+card.id);
 assert.ok(card.text.some(t=>String(t).includes('ART: '+d.artRef)),'fatality box displays image reference: '+card.id);
 assert.ok(card.text.some(t=>String(t).includes(d.description)),'fatality box displays narrative beat: '+card.id);
}

console.log(JSON.stringify({
 result:'PASS',nodes:Object.keys(chapter.nodes).length,chapters:manifest.chapters.map(c=>c.id),
 artRecords:productionRecords.length,
 checked:['manifest','all scene references','portrait references','all item artwork','paired scene backgrounds','editable portrait background','startup','artwork library','edit prompt','export artwork','item links','SHOW branches','branch proximity','pointer-centered wheel zoom','node drag','live connectors','local saved layout','reload layout','import layout','reset layout','chapter header','per-chapter graph+inspector+art refs','cross-chapter hand-off link','independent positions+selection across switches','export all four chapters','Chapter 2 graph+inspector+art refs+layout','Chapter 1 exits link Chapter 2','import into fresh browser','partial import keeps other chapter',
   'timeline: 36+99 cards','no card/port/label overlap','all authored routes drawn, none invented','hover text','left-to-right forward routes','returns only on real cycles',
   'Ch1 five exits in right column + Ch2 ports','fatal chair terminal','Ch2 five incoming Ch1 routes','Ch2 five preview handoffs','fatal endings never cross chapters',
   'antidote loops attached','PASS/FAIL distinct','stable across reload','port navigation','Fit overview + Start','old cache archived not applied','restore archive',
   'reset one chapter only','export revision+timeline','old v1 import','Ch3 identical to published viewer','Prologue timeline + hand-off','pills select/inspect/drag, no auto-navigation','explicit inspector navigation','per-chapter view memory']
}));
