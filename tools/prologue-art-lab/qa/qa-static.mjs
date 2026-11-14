import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import {createHash} from "node:crypto";
import {fileURLToPath} from "node:url";
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"../../..");
const base=path.join(root,"tools/prologue-art-lab");
const idx=JSON.parse(fs.readFileSync(path.join(base,"asset-index.json"),"utf8"));
const controls=JSON.parse(fs.readFileSync(path.join(base,"control-asset-manifest.json"),"utf8"));
const layout=JSON.parse(fs.readFileSync(path.join(base,"layout-reference.json"),"utf8"));
const fonts=JSON.parse(fs.readFileSync(path.join(base,"bitmap-fonts.json"),"utf8"));
assert.equal(layout.schema,"cyoa-public-artwork-lab-layout-v1");
assert.equal(layout.inventory.slotCount,6);
assert.deepEqual(layout.inventory.slotSize,[96,96]);
assert.equal(layout.inventory.gap,20);
assert.equal(layout.inventory.pitch,116);
assert.deepEqual(layout.inventory.slotLayouts["6"],{x:92,y:935});
assert.deepEqual([layout.inventory.leftArrow.x,layout.inventory.rightArrow.x],[33,782]);
assert.ok(92+5*116+96<782,"six inventory slots do not overlap the right arrow");
assert.deepEqual(layout.utility.buttons.map(x=>x.label),["INSPECT","NOTES","FILES"]);
assert.deepEqual(layout.utility.buttons.map(x=>x.x),[1482,1619,1756]);
assert.equal(layout.choices.cardWidth,535);
assert.equal(layout.choices.viewport.y,527);
assert.equal(layout.speech.text.lineHeight,24);
assert.equal(layout.objective.body.lineHeight,25);
assert.equal(fonts.schema,"cyoa-public-artwork-lab-bitmap-fonts-v1");
assert.deepEqual(Object.keys(fonts.faces).sort(),["jersey15-1x","locked","pressstart2p-2x","tiny5-3x"].sort());
assert.equal(controls.schema,"cyoa-public-control-art-v1");
assert.equal(controls.files.length,14);
const iconFiles=new Set(["inspect.png","notes.png","files.png"]);
const controlPaths=new Set();
for(const row of controls.files){
  assert.ok(!controlPaths.has(row.path));controlPaths.add(row.path);
  assert.match(row.path,/^assets\/approved\/art\/[a-zA-Z0-9_./-]+\.png$/);
  const fp=path.resolve(base,row.path);
  assert.ok(fp.startsWith(base+path.sep)&&fs.existsSync(fp),"missing control artwork "+row.path);
  const bytes=fs.readFileSync(fp);
  assert.equal(bytes.length,row.size,"size of "+row.path);
  const gitHash=createHash("sha1").update("blob "+bytes.length+"\\0").update(bytes).digest("hex");
  assert.equal(gitHash,row.gitBlob,"source Git blob "+row.path);
  assert.equal(bytes.toString("hex",0,8),"89504e470d0a1a0a","PNG "+row.path);
  if(iconFiles.has(path.basename(row.path)))assert.deepEqual([bytes.readUInt32BE(16),bytes.readUInt32BE(20)],[96,96],"glyph size "+row.path);
}

const art=JSON.parse(fs.readFileSync(path.join(root,"story/artwork.draft.json"),"utf8"));
assert.equal(idx.schema,"cyoa-public-prologue-review-assets-v1");
assert.equal(idx.files.length,45);
assert.equal(Object.keys(art.scenes).length,8);
assert.equal(Object.keys(art.items).length,10);
assert.equal(Object.keys(art.portraits).length,3);
const expected=new Map();
function add(status,p,dims){assert.ok(p&&p.endsWith(".png"));expected.set("assets/"+(status==="generated"?"draft/":"approved/")+p,dims);}
for(const s of Object.values(art.scenes)){
  add(s.status,s.assetPath,[314,206]);
  if(s.portraitBackground)add(s.portraitBackground.status,s.portraitBackground.assetPath,[564,278]);
}
for(const p of Object.values(art.portraits)){
  if(p.status==="generated")add(p.status,p.assetPath,[564,278]);
  else for(const l of p.layers||[])add("reused",l.path,[564,278]);
}
for(const item of Object.values(art.items)){
  add(item.slot.status,item.slot.assetPath,[96,96]);
  add(item.inspect.status,item.inspect.assetPath,[565,451]);
}
assert.equal(expected.size,33);
let count=0,bytes=0;const seen=new Set();
const png=Buffer.from("89504e470d0a1a0a","hex");
for(const row of idx.files){
  assert.ok(!seen.has(row.path));seen.add(row.path);
  assert.match(row.path,/^assets\/(draft|approved)\/art\/[a-zA-Z0-9_./-]+\.png$/);
  assert.ok(!row.path.includes(".."));
  const fp=path.resolve(base,row.path);
  assert.ok(fp.startsWith(base+path.sep) && fs.existsSync(fp),"missing "+row.path);
  const b=fs.readFileSync(fp);
  assert.ok(b.subarray(0,8).equals(png),"invalid PNG "+row.path);
  assert.equal(b.length,row.bytes,"bytes "+row.path);
  assert.equal(createHash("sha256").update(b).digest("hex"),row.sha256,"SHA-256 "+row.path);
  const dims=[b.readUInt32BE(16),b.readUInt32BE(20)];
  if(expected.has(row.path))assert.deepEqual(dims,expected.get(row.path),"dims "+row.path);
  if(/\/art\/ui\/shell\/(layout-final|item-overlay)\.png$/.test(row.path))assert.deepEqual(dims,[1920,1080]);
  bytes+=b.length;count++;
}
for(const name of expected.keys())assert.ok(seen.has(name),"catalog asset not exported "+name);
assert.equal(idx.files.filter(x=>x.path.startsWith("assets/draft/")).length,28);
assert.equal(idx.files.filter(x=>x.path.startsWith("assets/approved/")).length,17);
const html=fs.readFileSync(path.join(base,"index.html"),"utf8");
const app=fs.readFileSync(path.join(base,"app.js"),"utf8");
const pages=fs.readFileSync(path.join(root,".github/workflows/pages.yml"),"utf8");
const board=fs.readFileSync(path.join(root,"tools/storyboard/index.html"),"utf8");
assert.ok(html.includes("approvedShell")&&html.includes("inspectionLayer"));
assert.ok(app.includes("asset-index.json")&&app.includes("../../story/artwork.draft.json"));
assert.ok(app.includes("layout-reference.json")&&app.includes("bitmap-fonts.json")&&app.includes("control-asset-manifest.json"));
assert.ok(!app.includes("slots: 7") && !html.includes("owner target"));
assert.ok(html.includes('id="buttonMode"')&&html.includes('id="buttonSkin"'));
assert.ok(html.includes('id="slotStatus"')&&html.includes('id="utilityLabel2"'));
assert.ok(fs.existsSync(path.join(base,"pixel-type.js")));
assert.ok(board.includes("../prologue-art-lab/"));
assert.ok(pages.includes("cp -a tools/prologue-art-lab/assets/."));
assert.ok(pages.includes("tools/prologue-art-lab/layout-reference.json")&&pages.includes("tools/prologue-art-lab/pixel-type.js"));
assert.ok(!fs.existsSync(path.join(root,"game")));
console.log("PASS public review package: "+count+" SHA-256 pinned images plus "+controls.files.length+" Git-blob-pinned approved control/font images; six-slot geometry, button labels and font assets verified.");
