(()=>{
"use strict";
const M=window.PUBLIC_PROLOGUE_ART;
const $=id=>document.getElementById(id);
const draft=path=>'./assets/draft/'+path;
const approved=path=>'./assets/approved/'+path;
const locate=(path,status)=>status==='generated'?draft(path):approved(path);
const sceneMap=new Map(M.scenes.map(x=>[x.id,x])),poseMap=new Map(M.portraits.map(x=>[x.id,x])),itemMap=new Map(M.items.map(x=>[x.id,x]));
const state={scene:'workplace/applause_station',portrait:'auto',start:0,count:7,dx:0,dy:0,showBg:true,showFg:true,inspection:null,fit:true};
const allImages=[...M.scenes.map(x=>locate(x.path,x.status)),...M.portraits.flatMap(x=>x.type==='none'?[]:[locate(x.background,x.type==='drone'?'generated':'reused'),locate(x.foreground,x.type==='drone'?'generated':'reused')]),...M.items.flatMap(x=>[locate(x.slot,x.status),locate(x.inspect,x.status)]),'./assets/approved/art/ui/shell/layout-final.png','./assets/approved/art/ui/shell/item-overlay.png','./assets/approved/art/ui/sprites/inventory/inventory_slot.png'];
const setOptions=(select,items)=>{for(const item of items){const option=document.createElement('option');option.value=item.id;option.textContent=item.title+(item.status==='generated'?' [DRAFT]':item.status==='reused'?' [M2]':'');select.add(option)}};
setOptions($('scene'),M.scenes);
setOptions($('portrait'),[{id:'auto',title:'Auto-match location'},...M.portraits]);
setOptions($('item'),M.items);
function paired(){return state.scene==='workplace/corridor'?'drone-closed':state.scene==='exposition/reception'?'receptionist':'none'}
function activePose(){return state.portrait==='auto'?paired():state.portrait}
function renderScene(){
const s=sceneMap.get(state.scene);$('sceneImage').src=locate(s.path,s.status);$('sceneName').textContent=s.title;
$('sceneSpeech').textContent=s.title+'. THIS IS A VISUAL ART REVIEW, NOT PLAYABLE STORY CONTENT.';
$('sceneImage').alt='Artwork preview: '+s.title;
$('stage').setAttribute('aria-label','Art review: '+s.title);
}
function renderPose(){
const id=activePose(),p=poseMap.get(id),bg=$('portraitBg'),fg=$('portraitFg');
$('pair').textContent=id==='none'?'No NPC portrait for this scene.':(p.scene===state.scene?'This portrait matches the active scene.':'Cross-location comparison only: this portrait was not authored for the active scene.');
if(id==='none'){bg.hidden=true;fg.hidden=true;return}
const status=p.type==='drone'?'generated':'reused';bg.src=locate(p.background,status);fg.src=locate(p.foreground,status);
bg.hidden=!state.showBg;fg.hidden=!state.showFg;fg.style.left=state.dx+'px';fg.style.top=state.dy+'px';bg.alt='Separate portrait background';fg.alt=p.title;
}
const root='./assets/approved/art/ui/sprites/';
function renderInventory(){
const holder=$('inventory');holder.replaceChildren();const startX=state.count===7?76:92;
for(let i=0;i<state.count;i++){
  const item=M.items[state.start+i];
  const node=document.createElement('button');node.className='slot';node.type='button';node.style.left=(startX+i*116)+'px';node.style.top='935px';node.setAttribute('aria-label',item?'Inspect '+item.title:'Empty inventory slot');node.disabled=!item;
  const frame=document.createElement('img');frame.className='slotFrame';frame.src=root+'inventory/inventory_slot.png';frame.alt='';node.appendChild(frame);
  if(item){const picture=document.createElement('img');picture.className='slotArt';picture.src=locate(item.slot,item.status);picture.alt='';node.appendChild(picture);node.dataset.item=item.id;node.addEventListener('click',()=>openInspector(item.id))}
  holder.appendChild(node);
}
$('start').max=String(Math.max(0,M.items.length-state.count));$('start').value=String(state.start);
$('inventoryLabel').textContent='Slots '+(state.start+1)+'–'+Math.min(M.items.length,state.start+state.count)+' of '+M.items.length+' candidate/reused items. The seven-slot layout retains the known right-arrow overlap.';
}
function openInspector(id){
const item=itemMap.get(id);if(!item)return;state.inspection=id;$('item').value=id;
$('inspectionImage').src=locate(item.inspect,item.status);$('inspectionImage').alt='Detailed item illustration of '+item.title;$('inspectionCopy').textContent=item.title+' · '+(item.status==='generated'?'DRAFT ART — OWNER REVIEW REQUIRED':'APPROVED M2 ART');
$('inspector').hidden=false;$('visualState').textContent='Inspecting: '+item.title; }
function closeInspector(){state.inspection=null;$('inspector').hidden=true;$('visualState').textContent='Review-only art stage';}
function resize(){const vp=$('viewport');const s=state.fit?Math.min(1,(vp.clientWidth-20)/1920,(vp.clientHeight-20)/1080):1;const v=Math.max(.1,s);$('stage').style.transform='scale('+v+')';$('stageWrap').style.width=(1920*v)+'px';$('stageWrap').style.height=(1080*v)+'px';$('fit').setAttribute('aria-pressed',String(state.fit));$('pixel').setAttribute('aria-pressed',String(!state.fit));}
function update(){renderScene();renderPose();renderInventory();resize();}
const API=window.PROLOGUE_PUBLIC_LAB={
setScene(id){if(!sceneMap.has(id))throw Error('Unknown scene '+id);state.scene=id;$('scene').value=id;closeInspector();update();},
setPortrait(id){if(id!=='auto'&&!poseMap.has(id))throw Error('Unknown portrait '+id);state.portrait=id;$('portrait').value=id;renderPose();},
setInventoryStart(v){state.start=Math.max(0,Math.min(M.items.length-state.count,Math.round(v)));renderInventory();},
setCount(n){if(n!==6&&n!==7)throw Error('Six or seven slots only');state.count=n;state.start=Math.min(state.start,M.items.length-n);$('count').value=String(n);renderInventory();},
openInspector,closeInspector,
snapshot(){return {scene:state.scene,pose:activePose(),inventoryStart:state.start,slotCount:state.count,inspector:state.inspection,stageSize:[1920,1080],sceneSize:[314,206],portraitSize:[564,278],assets:M.items.length}}
};
$('scene').addEventListener('change',e=>API.setScene(e.target.value));$('portrait').addEventListener('change',e=>API.setPortrait(e.target.value));
$('reception').addEventListener('click',()=>{API.setScene('exposition/reception');API.setPortrait('auto')});
$('item').addEventListener('change',e=>openInspector(e.target.value));$('inspect').addEventListener('click',()=>openInspector($('item').value));
$('closeInspect').addEventListener('click',closeInspector);$('closeStageInspect').addEventListener('click',closeInspector);
$('count').addEventListener('change',e=>API.setCount(Number(e.target.value)));
$('start').addEventListener('input',e=>API.setInventoryStart(Number(e.target.value)));
$('prev').addEventListener('click',()=>API.setInventoryStart(state.start-1));$('next').addEventListener('click',()=>API.setInventoryStart(state.start+1));
$('leftArrow').addEventListener('click',()=>API.setInventoryStart(state.start-1));$('rightArrow').addEventListener('click',()=>API.setInventoryStart(state.start+1));
$('showBg').addEventListener('change',e=>{state.showBg=e.target.checked;renderPose()});$('showFg').addEventListener('change',e=>{state.showFg=e.target.checked;renderPose()});
const offsets=()=>{state.dx=Math.max(-40,Math.min(40,Number($('dx').value)||0));state.dy=Math.max(-40,Math.min(40,Number($('dy').value)||0));renderPose()};
$('dx').addEventListener('input',offsets);$('dy').addEventListener('input',offsets);
$('resetPose').addEventListener('click',()=>{$('dx').value=$('dy').value='0';offsets()});
$('fit').addEventListener('click',()=>{state.fit=true;resize()});$('pixel').addEventListener('click',()=>{state.fit=false;resize()});
window.addEventListener('resize',resize);
Promise.all([...new Set(allImages)].map(src=>new Promise((resolve,reject)=>{const img=new Image();img.onload=resolve;img.onerror=()=>reject(new Error('Missing image: '+src));img.src=src;})))
.then(()=>{$('status').textContent='READY · 8 scenes · 3 portrait poses · 10 items';document.body.dataset.labReady='true';update()})
.catch(err=>{$('status').textContent='LOAD ERROR: '+err.message;document.body.dataset.labReady='error';console.error(err)});
})();