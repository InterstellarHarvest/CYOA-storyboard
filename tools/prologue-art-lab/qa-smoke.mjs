// Public-safe artwork lab smoke QA: no private game JS is exported.
// Run: node tools/prologue-art-lab/qa-smoke.mjs
import fs from 'node:fs';
import path from 'node:path';

const lab = 'tools/prologue-art-lab';
const cat = JSON.parse(fs.readFileSync('story/artwork.draft.json', 'utf8'));
const records = [];
const expected = {
  scene:[314,206,2], background:[564,278,2], pose:[564,278,6],
  slot:[96,96,6], inspect:[565,451,2]
};
for (const [id, s] of Object.entries(cat.scenes)) {
  if (s.status === 'generated') records.push([id,s.assetPath,'scene']);
  if (s.portraitBackground?.status === 'generated') records.push([id+' background',s.portraitBackground.assetPath,'background']);
}
for (const [id, p] of Object.entries(cat.portraits)) {
  if (p.status === 'generated') records.push([id,p.assetPath,'pose']);
}
for (const [id, p] of Object.entries(cat.items)) {
  if (p.slot?.status === 'generated') records.push([id+' icon',p.slot.assetPath,'slot']);
  if (p.inspect?.status === 'generated') records.push([id+' inspect',p.inspect.assetPath,'inspect']);
}
if (records.length !== 28) throw Error('Expected 28 draft PNGs, got '+records.length);
let checked=0;
function check(rel, dimensions, purpose) {
  const file=path.join(lab,'assets',rel);
  if(!fs.existsSync(file))throw Error('Missing '+purpose+': '+file);
  const b=fs.readFileSync(file);
  if(b.length < 26 || b.subarray(0,8).toString('hex')!=='89504e470d0a1a0a')throw Error('Invalid PNG '+file);
  const x=[b.readUInt32BE(16),b.readUInt32BE(20),b[25]];
  if(dimensions && x.join(',')!==dimensions.join(','))throw Error('Wrong '+purpose+' dimensions/type '+file+': '+x);
  checked++;
}
for(const [id,rel,kind] of records)check(rel,expected[kind],id);
const approved=[
 ['art/scenes/conference_hall/reception/reception_scene.png',[314,206,2]],
 ['art/portraits/receptionist/reception_background.png',[564,278,2]],
 ['art/portraits/receptionist/receptionist_idle.png',[564,278,6]],
 ['art/items/bathroom_pass_slot.png',[96,96,6]],
 ['art/items/bathroom_pass_inspect.png',[565,451,2]],
 ['art/ui/shell/layout-final.png',[1920,1080,6]],
 ['art/ui/shell/item-overlay.png',[1920,1080,6]],
 ['art/ui/sprites/inventory/inventory_slot.png',null],
 ['art/ui/sprites/inspect_close.png',null],
 ['art/ui/sprites/choice_cards/choice_2line_a.png',null],
 ['art/ui/sprites/controls/inv_left_up.png',null],
 ['art/ui/sprites/controls/inv_right_up.png',null],
 ['art/ui/sprites/controls/utility_a_up.png',null],
 ['art/ui/sprites/controls/utility_b_up.png',null],
 ['art/ui/sprites/controls/utility_c_up.png',null]
];
for(const [rel,dim] of approved)check(rel,dim,'approved M2 image');
for(const file of ['index.html','lab.css','lab.js']){
 if(!fs.statSync(path.join(lab,file)).size)throw Error('Missing viewer '+file);
}
const source=fs.readFileSync(path.join(lab,'lab.js'),'utf8');
if(/\/game\/js\/|CYOA_RECEPTION|CYOA_RULES|internal rulings|\/review\//.test(source))throw Error('Private game source reference detected');
const root=fs.readdirSync('.', {withFileTypes:true}).map(x=>x.name);
if(root.includes('game'))throw Error('Private game directory exported into public site');
console.log('Public prologue lab QA passed: '+records.length+' draft images, '+approved.length+' approved images; '+checked+' PNG headers checked.');