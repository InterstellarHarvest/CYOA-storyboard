// Isolated story QA for the owner-approved Chapter 3 reboot candidate.
// The candidate intentionally is NOT in the active storyboard manifest yet.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const read=(relative)=>JSON.parse(fs.readFileSync(path.join(root,relative),'utf8'));
const candidate=read('story/chapters/chapter-03.reboot-candidate.json');
const ch2=read('story/chapters/chapter-02.draft.json');
const manifest=read('story/storyboard-manifest.json');
const items=read('story/items.draft.json');
const nodes=candidate.nodes;

assert.equal(manifest.chapters.find(ch=>ch.id==='chapter-03').status,'archived');
assert.equal(manifest.chapters.find(ch=>ch.id==='chapter-03').file,'chapters/chapter-03.draft.json');
const archive=fs.readFileSync(path.join(root,'story/archives/chapter-03-pre-reboot-20261118.json'));
assert.equal(createHash('sha256').update(archive).digest('hex'),
  '02beb009b667f6930408850db91ca078262df6807ecc7236d044a3a4dc0dcbe1');

const inputGroups={
  end_concourse_robot:'public_concourse',
  end_underground_station:'underground_transit',
  end_public:'public_concourse',
  end_maintenance:'service_infrastructure',
  end_customs:'public_concourse'
};
for(const [id,group] of Object.entries(inputGroups)){
  const end=ch2.nodes[id];
  assert.equal(end.end,true,id);
  assert.equal(end.effects?.set?.chapter3_entry_group,group,id);
  assert.equal(end.storyboardNextChapter,'chapter-03',id);
}
assert.equal(Object.values(ch2.nodes).filter(n=>n.end&&n.deathPopup).length,5);

const seen=new Set(),ends=[],broken=[],cycles=[],checks=new Map(),itemActions=new Map();
const validKinds=new Set(['action','spoken','continue','system']);
function walk(id,stack=[]){
  const node=nodes[id];
  if(!node){broken.push(id);return;}
  if(stack.includes(id)){cycles.push([...stack,id]);return;}
  seen.add(id);
  assert.ok(['narrative','dialogue','focus'].includes(node.mode),id+' valid mode');
  assert.ok(node.scene?.startsWith('pavilion_reboot/'),id+' uses new, isolated scene refs');
  assert.equal(node.effects,undefined,id+' does not mutate inherited state');
  assert.equal(node.deathPopup,undefined,id+' has no unapproved fatal popup');
  assert.equal(node.endingArt,undefined,id+' has no unapproved death art');
  if(node.mode==='dialogue')assert.ok(node.speaker,id+' has a dialogue speaker');
  if(node.mode!=='dialogue')assert.equal(node.speaker,undefined,id+' has no inert speaker');
  if(node.end){
    ends.push(id);
    assert.equal(node.choices?.length,1,id+' has one provisional end-system button');
    assert.equal(node.choices[0].kind,'system',id+' end system');
    return;
  }
  assert.ok(node.choices?.length,id+' has a forward action');
  for(const choice of node.choices){
    assert.ok(validKinds.has(choice.kind),id+' valid choice kind');
    assert.equal(choice.effects,undefined,id+' does not mutate earlier chapter state');
    if(choice.kind==='spoken')assert.ok(!choice.text.includes('"'),
      id+' spoken cards must not store literal quote marks');
    if(choice.check){
      const before=checks.get(choice.check.id);
      if(before)assert.deepEqual(choice.check,before,id+' repeat check is identical');
      checks.set(choice.check.id,choice.check);
    }
    const next=[choice.to,choice.pass?.to,choice.fail?.to].filter(Boolean);
    assert.ok(next.length,id+' must route to a destination');
    for(const target of next)walk(target,[...stack,id]);
  }
  for(const verb of ['show','use']){
    for(const [itemId,action] of Object.entries(node[verb]||{})){
      assert.ok(items[itemId],id+' references existing '+itemId);
      assert.equal(action.kind,'action',id+' item action ink');
      assert.ok(action.say,id+' item action includes echo text');
      assert.ok(action.to,id+' item action has a real destination');
      assert.equal(action.if,undefined,id+' is gated by item being held, not an extra arbitrary flag');
      itemActions.set([id,verb,itemId].join(':'),{node:id,verb,itemId,action});
      if(verb==='use'){
        assert.equal(itemId,'red_stapler','only the approved stapler is used');
        assert.deepEqual(action.effects,{take:['red_stapler']},'stapler gets consumed');
      }else{
        assert.equal(action.effects,undefined,id+' SHOW does not consume the item');
      }
      walk(action.to,[...stack,id]);
    }
  }
}
walk(candidate.start);
assert.deepEqual(broken,[],'no dangling edges');
assert.deepEqual(cycles,[],'no unintended loops');
assert.equal(seen.size,Object.keys(nodes).length,'all draft nodes reachable');
assert.equal(ends.length,28,'twelve original routes plus optional held-item variants');
const counts=ends.reduce((acc,id)=>(acc[id]=(acc[id]||0)+1,acc),{});
assert.deepEqual({...counts},{
  backstage_exit:16,
  locomotion_fail:2,
  presenter_help_end:2,
  paper_problem_end:2,
  attendant_honest_end:2,
  door_dash_fail:2,
  door_reverse_end:2
},'six original backstage / six early routes, plus optional key/photo/stapler variants');
assert.equal(itemActions.size,3,'exactly three approved inherited-item interactions');
assert.deepEqual([...itemActions.values()].map(({node,verb,itemId})=>[node,verb,itemId]).sort(),[
  ['attendant_refusal','show','wc_key'],
  ['presenter_verification','show','family_portrait_photo'],
  ['record_choices','use','red_stapler']
].sort());
assert.deepEqual(nodes.attendant_key_callback.choices.map(c=>[c.kind,c.text,c.to]),
  nodes.attendant_refusal.choices.map(c=>[c.kind,c.text,c.to]),
  'key callback preserves the original three chapter-opening options');
assert.equal(nodes.photo_verification_reply.choices[0].to,'backstage_exit');
assert.equal(nodes.stapler_printer_snarl.choices[0].to,'backstage_exit');
assert.equal(checks.size,2,'exactly two approved check definitions');
const leap=checks.get('ch3_locomotion_leap'),dash=checks.get('ch3_restroom_dash');
assert.equal(leap.id,'ch3_locomotion_leap');
assert.equal(leap.sides,6);
assert.equal(leap.need,4);
assert.deepEqual(leap.mods,[{if:{has:'timing_clicker'},add:1}],
  'held timing clicker alone adds one');
assert.ok(items.timing_clicker,'the modifier refers to a real, inherited item');
assert.equal(dash.id,'ch3_restroom_dash');
assert.equal(dash.sides,6);
assert.equal(dash.need,4);
assert.equal(dash.mods,undefined,'door dash has no modifier');
assert.equal(nodes.backstage_exit.mode,'narrative');
assert.equal(nodes.backstage_exit.end,true);

console.log('CH3 REBOOT CANDIDATE QA: PASS — '+seen.size+
  ' reachable nodes, '+ends.length+' paths, '+Object.keys(counts).length+
  ' survivor terminals, '+checks.size+' approved checks, '+itemActions.size+
  ' conditional inherited-item actions; old chapter archive and public manifest untouched.');
