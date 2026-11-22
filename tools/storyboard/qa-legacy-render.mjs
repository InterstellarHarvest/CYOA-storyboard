// Serialises how the storyboard draws the chapter that must NOT change (the preserved legacy Chapter 3; the Prologue moved
// to the timeline view on owner request, 2026-11-16):
// every card's position and text, every SVG connector and label, the stage size and default zoom.
// The smoke test compares the current viewer against qa-fixtures/legacy-render-snapshot.json, which
// was produced from the published viewer before the timeline rework (main 0ebcf48):
//   git show 0ebcf48:tools/storyboard/index.html > /tmp/base.html
//   node tools/storyboard/qa-legacy-render.mjs /tmp/base.html > tools/storyboard/qa-fixtures/legacy-render-snapshot.json
// Dependency-free: the viewer script runs in node:vm with a minimal DOM, exactly like qa-smoke.mjs.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';

export const LEGACY_CHAPTERS=['chapter-03'];
// The preserved pre-reboot Chapter 3 (byte-identical to story/archives/chapter-03-pre-reboot-20261118.json).
export const LEGACY_FILE='chapters/chapter-03.draft.json';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');

class Element{
  constructor(tag='div',id=''){this.tagName=tag;this.id=id;this.children=[];this.style={};this.attributes={};this.listeners={};this.textContent='';this.value='';this.disabled=false;this.hidden=false;
    this.scrollLeft=0;this.scrollTop=0;this.clientWidth=1200;this.clientHeight=720;this.classList={add(){},remove(){}};}
  append(...c){this.children.push(...c);} replaceChildren(...c){this.children=[...c];} addEventListener(n,f){this.listeners[n]=f;}
  setAttribute(n,v){this.attributes[n]=v;} closest(){return null;} getBoundingClientRect(){return {left:0,top:0,width:this.clientWidth,height:this.clientHeight};}
  setPointerCapture(){} hasPointerCapture(){return false;} releasePointerCapture(){} remove(){} click(){this.onclick?.();this.listeners.click?.();}
}
const flat=n=>[n,...(n.children||[]).flatMap(flat)];

export async function renderLegacy(htmlPath,{storage=new Map()}={}){
  const html=fs.readFileSync(htmlPath,'utf8');
  const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
  const els=new Map();
  const doc={getElementById(id){if(!els.has(id))els.set(id,new Element('div',id));return els.get(id);},createElement:t=>new Element(t),createElementNS:(_n,t)=>new Element(t),body:new Element('body')};
  // Since the Chapter 3 gameplay integration the manifest's chapter-03 is the approved reboot (a timeline
  // chapter). The preserved legacy graph keeps its published geometry check: this harness alone swaps it
  // back in memory (legacy file, archived status, no timeline layout), exactly as the viewer saw it
  // before the activation. The committed manifest and layout are never touched.
  const legacySwap={'story/storyboard-manifest.json':m=>{const e=m.chapters.find(c=>c.id==='chapter-03');e.file=LEGACY_FILE;e.status='archived';return m;},
    'story/storyboard-layout.json':l=>{l.chapters['chapter-03']={positions:{}};return l;}};
  const load=async url=>{const p=new URL(String(url)).pathname;const rel=p.startsWith('/CYOA-storyboard/')?p.slice('/CYOA-storyboard/'.length):p.slice(1);
    return {ok:true,json:async()=>{const v=JSON.parse(fs.readFileSync(path.resolve(root,rel),'utf8'));return legacySwap[rel]?legacySwap[rel](v):v;}};};
  const ls={getItem:k=>storage.has(k)?storage.get(k):null,setItem:(k,v)=>storage.set(k,v),removeItem:k=>storage.delete(k)};
  vm.runInNewContext(script,{document:doc,window:{addEventListener(){},localStorage:ls},location:{href:'https://example.org/CYOA-storyboard/tools/storyboard/'},
    fetch:load,URL,Blob,JSON,Object,Math,Number,String,console,setTimeout(fn){fn();return 0;}});
  const settle=()=>new Promise(r=>setTimeout(r,30));
  await settle();
  const manifest=JSON.parse(fs.readFileSync(path.join(root,'story/storyboard-manifest.json'),'utf8'));
  const out={};
  for(const id of LEGACY_CHAPTERS){
    const index=manifest.chapters.findIndex(c=>c.id===id);
    doc.getElementById('chapterSelect').listeners.change({target:{value:String(index)}});
    await settle();
    const cards=doc.getElementById('nodes').children.map(c=>({id:c.children[0].textContent,className:c.className,left:c.style.left,top:c.style.top,
      text:c.children.map(x=>x.textContent),title:c.title}));
    const svg=doc.getElementById('edges');
    const shapes=svg.children.map(n=>({tag:n.tagName,attributes:n.attributes,text:n.textContent||undefined}));
    const stage=doc.getElementById('stage');
    out[id]={cards,shapes,svg:svg.attributes,stage:{width:stage.style.width,height:stage.style.height,transform:stage.style.transform},
      ports:els.has('ports')?flat(doc.getElementById('ports')).length-1:0};
  }
  return out;
}

if(process.argv[1]&&fileURLToPath(import.meta.url)===path.resolve(process.argv[1])){
  const target=process.argv[2]||path.join(root,'tools/storyboard/index.html');
  console.log(JSON.stringify(await renderLegacy(target)));
}
