(async function () {
'use strict';
const $=id=>document.getElementById(id);
const root='assets/';
const art=path=>root+path;
const state={scene:'workplace/applause_station',portrait:'auto',slotCount:7,start:0,inspected:null,poseX:0,poseY:0,showBackground:true,showPose:true,fit:true};
const candidates=['termination_notice','timing_clicker','desk_plant','effects_box_full','effects_box_empty','red_stapler','rubber_band_ball','property_claim_ticket','expo_examiner_badge'];
const expected={scene:[314,206],portrait:[564,278],slot:[96,96],inspect:[565,451]};
const json=await fetch('../../story/artwork.draft.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error('Cannot load artwork catalog');return r.json()});
const scenes=Object.entries(json.scenes).map(([id,v])=>({id,title:v.title,status:v.status,path:v.assetPath}));
const items=[...candidates.map(id=>({id,name:json.items[id].slot.title.split(' — ')[0],slot:json.items[id].slot.assetPath,inspect:json.items[id].inspect.assetPath,status:'generated'})),{id:'wc_key',name:'Facilities Key (approved M2)',slot:'art/items/bathroom_pass_slot.png',inspect:'art/items/bathroom_pass_inspect.png',status:'reused'}];
const portraitTypes=[{id:'auto',title:'Auto — paired to scene'},{id:'none',title:'No portrait'},{id:'drone-closed',title:'Termination drone — slot closed'},{id:'drone-paper',title:'Termination drone — paper extended'},{id:'receptionist',title:'Receptionist — approved M2'}];
const portraits={
 'drone-closed':{scene:'workplace/corridor',background:json.scenes['workplace/corridor'].portraitBackground.assetPath,foreground:json.portraits['termination_drone:slot_closed'].assetPath},
 'drone-paper':{scene:'workplace/corridor',background:json.scenes['workplace/corridor'].portraitBackground.assetPath,foreground:json.portraits['termination_drone:paper_extended'].assetPath},
 'receptionist':{scene:'exposition/reception',background:json.scenes['exposition/reception'].portraitBackground.assetPath,foreground:json.portraits['receptionist:default'].layers[1].path}
};
const asOption=(select,obj)=>{const x=document.createElement('option');x.value=obj.id;x.textContent=obj.title+(obj.status==='generated'?' [DRAFT]':obj.status==='reused'?' [M2]':'');select.append(x)};
scenes.forEach(x=>asOption($('scene'),x));portraitTypes.forEach(x=>asOption($('portrait'),x));items.forEach(x=>asOption($('item'),{id:x.id,title:x.name,status:x.status}));
function activePortrait(){if(state.portrait!=='auto')return state.portrait;if(state.scene==='workplace/corridor')return 'drone-closed';if(state.scene==='exposition/reception')return 'receptionist';return 'none'}
function renderScene(){const scene=scenes.find(x=>x.id===state.scene);$('scene-image').src=art(scene.path);$('scene-image').alt=scene.title;$('current-scene').textContent=scene.title;$('scene').value=state.scene}
function renderPortrait(){const id=activePortrait(),p=portraits[id];
 $('portrait').value=state.portrait;
 $('portrait-bg').style.display=p&&state.showBackground?'':'none';
 $('portrait-pose').style.display=p&&state.showPose?'':'none';
 if(p){$('portrait-bg').src=art(p.background);$('portrait-pose').src=art(p.foreground)}
 $('portrait-pose').style.left=state.poseX+'px';$('portrait-pose').style.top=state.poseY+'px';
 $('pairing').textContent=!p?'No portrait paired with this scene.':p.scene===state.scene?'Correct paired environment and foreground.':'Comparison only: this portrait belongs to '+p.scene+'.';
}
function decorate(){
 const layer=$('choice-decor');layer.replaceChildren();
 for(let i=0;i<3;i++){const img=new Image();img.src=art('art/ui/sprites/choice_cards/choice_2line_a.png');img.alt='';img.style.cssText='left:1324px;top:'+(529+i*111)+'px;width:548px;height:108px';layer.append(img)}
 const utilities=$('utility-decor');utilities.replaceChildren();
 ['utility_a_up','utility_b_up','utility_c_up'].forEach((name,i)=>{const im=new Image();im.src=art('art/ui/sprites/controls/'+name+'.png');im.alt='';im.style.cssText='left:'+(1482+137*i)+'px;top:930px;width:135px;height:114px';utilities.append(im)});
}
function inventory(){
 const root=$('inventory-strip');root.replaceChildren();
 const n=state.slotCount,x0=n===7?76:92,pitch=116;
 state.start=Math.max(0,Math.min(state.start,items.length-n));
 for(let i=0;i<n;i++){
   const item=items[i+state.start],button=document.createElement('button');button.type='button';button.style.left=x0+i*pitch+'px';button.style.top='935px';
   button.setAttribute('aria-label','Inspect '+item.name);button.title=item.name;
   const bg=new Image();bg.src=art('art/ui/sprites/inventory/inventory_slot.png');bg.style.cssText='left:0;top:0;width:96px;height:96px';
   const icon=new Image();icon.src=art(item.slot);icon.style.cssText='left:0;top:0;width:96px;height:96px';
   button.append(bg,icon);button.onclick=()=>inspect(item.id);root.append(button);
 }
 $('inventory-status').textContent='Visible '+(state.start+1)+'–'+(state.start+n)+' of '+items.length+' · '+n+' slots; M2 checked-in default is 6.';
 $('slot-count').value=n;
}
function inspect(id){state.inspected=id;const item=items.find(x=>x.id===id);$('item').value=id;$('inspector-overlay').hidden=false;$('inspector-image').src=art(item.inspect);$('inspector-image').alt=item.name+' inspection artwork';$('inspector-label').textContent=item.name.toUpperCase()+' · ART REVIEW';$('status').textContent='Inspecting '+item.name+' — draft state not implied'}
function closeInspect(){state.inspected=null;$('inspector-overlay').hidden=true;$('status').textContent='Review only — source art unchanged'}
function resize(){const viewport=$('viewport');const scale=state.fit?Math.max(.1,Math.min((viewport.clientWidth-20)/1920,(viewport.clientHeight-20)/1080,1)):1;
 $('stage-holder').style.width=1920*scale+'px';$('stage-holder').style.height=1080*scale+'px';
 $('stage').style.transform='scale('+scale+')';
 $('fit').setAttribute('aria-pressed',String(state.fit));$('native').setAttribute('aria-pressed',String(!state.fit));$('view-mode').textContent=state.fit?'Fit preview':'1:1 native stage'}
function setScene(id){state.scene=id;renderScene();renderPortrait();closeInspect()}
function setPortrait(id){state.portrait=id;renderPortrait()}
$('scene').onchange=e=>setScene(e.target.value);
$('reception').onclick=()=>{setScene('exposition/reception');setPortrait('auto')};
$('portrait').onchange=e=>setPortrait(e.target.value);
$('show-bg').onchange=e=>{state.showBackground=e.target.checked;renderPortrait()};
$('show-pose').onchange=e=>{state.showPose=e.target.checked;renderPortrait()};
function offset(){state.poseX=Math.max(-40,Math.min(40,Number($('dx').value)||0));state.poseY=Math.max(-40,Math.min(40,Number($('dy').value)||0));renderPortrait()}
$('dx').onchange=offset;$('dy').onchange=offset;$('reset-offset').onclick=()=>{$('dx').value=0;$('dy').value=0;offset()};
$('slot-count').onchange=e=>{state.slotCount=Number(e.target.value);state.start=0;inventory()};
function shift(by){state.start=Math.max(0,Math.min(items.length-state.slotCount,state.start+by));inventory()}
$('inventory-prev').onclick=()=>shift(-1);$('inventory-next').onclick=()=>shift(1);$('stage-prev').onclick=()=>shift(-1);$('stage-next').onclick=()=>shift(1);
$('item').onchange=e=>inspect(e.target.value);$('inspect').onclick=()=>inspect($('item').value);$('close-inspector').onclick=closeInspect;$('stage-close').onclick=closeInspect;
function cycle(d){const ix=items.findIndex(x=>x.id===(state.inspected||$('item').value));inspect(items[(ix+d+items.length)%items.length].id)}
$('item-prev').onclick=()=>cycle(-1);$('item-next').onclick=()=>cycle(1);
$('fit').onclick=()=>{state.fit=true;resize()};$('native').onclick=()=>{state.fit=false;resize()};
window.addEventListener('resize',resize);document.addEventListener('keydown',e=>{if(e.key==='Escape')closeInspect()});
decorate();renderScene();renderPortrait();inventory();resize();
$('status').textContent='Ready · 28 draft images · approved M2 visual assets';
window.PROLOGUE_PUBLIC_LAB={state,scenes,items,portraits,setScene,setPortrait,inspect,closeInspect,shift};
})().catch(error=>{document.getElementById('status').textContent='Load error: '+error.message;console.error(error)});
