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

for(const scene of new Set([chapter.scene,...Object.values(chapter.nodes).map(x=>x.scene).filter(Boolean)]))
  assert.ok(artwork.scenes[scene],'scene reference '+scene);
for(const n of Object.values(chapter.nodes)){
  if(n.speaker)assert.ok(artwork.portraits[n.speaker+':'+(n.pose||'default')],'portrait '+n.speaker);
  if(n.focus)assert.ok(artwork.focus[n.focus],'focus '+n.focus);
}
for(const id of Object.keys(items)){
  assert.ok(artwork.items[id]?.slot?.prompt,'slot prompt '+id);
  assert.ok(artwork.items[id]?.inspect?.prompt,'inspect prompt '+id);
}

class Element {
  constructor(tag='div',id=''){
    this.tagName=tag;this.id=id;this.children=[];this.style={};this.attributes={};
    this.listeners={};this.textContent='';this.value='';this.disabled=false;
    this.scrollLeft=0;this.scrollTop=0;this.clientWidth=1200;this.clientHeight=720;
  }
  append(...children){this.children.push(...children);}
  replaceChildren(...children){this.children=[...children];}
  addEventListener(name,fn){this.listeners[name]=fn;}
  setAttribute(name,value){this.attributes[name]=value;}
  closest(){return null;}
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
const errors=[];
const context={
  document,window:{addEventListener(){}},location:{href:'https://example.org/CYOA-storyboard/tools/storyboard/'},
  fetch:load,URL,Blob,JSON,Object,Math,Number,String,console,
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

document.getElementById('showItems').onclick();
assert.ok(button('APPLAUSE TIMING CLICKER'),'items still selectable');
button('APPLAUSE TIMING CLICKER').click();
assert.ok(button('APPLAUSE TIMING CLICKER — INVENTORY SLOT'),'item slot artwork link');
assert.ok(button('APPLAUSE TIMING CLICKER — INSPECTION ART'),'item inspection artwork link');

console.log(JSON.stringify({
 result:'PASS',nodes:Object.keys(chapter.nodes).length,
 artRecords:Object.keys(artwork.scenes).length+Object.keys(artwork.portraits).length+
  Object.values(artwork.items).reduce((n,v)=>n+Object.keys(v).length,0),
 checked:['manifest','all scene references','portrait references','all item artwork','startup','artwork library','edit prompt','export artwork','item links']
}));
