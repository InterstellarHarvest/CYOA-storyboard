// Idempotent mechanical registration of the owner-approved Chapter 3 art briefs.
// This script never generates images, assigns production asset paths, or changes
// the locked narrative. Run on an isolated artwork branch only.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const artPath=path.join(root,'story/artwork.draft.json');
const sourcePath=path.join(root,'story/chapters/chapter-03.reboot-candidate.json');
const art=JSON.parse(fs.readFileSync(artPath,'utf8'));
const chapter3Exception='CHAPTER 3 REBOOT — OWNER-APPROVED HUMAN STAGING EXCEPTION (2026-11-18): The earlier no-people-in-scene-backgrounds rule governed prior unpopulated Exposition/House batches. The People\'s Pavilion explicitly has live human attendants, presenters, and one-use visitors; its main scenes may depict small figures where needed to tell the locked incident truthfully. Native 564×278 conversation BACKGROUNDS remain without the NPC, because the separately authored transparent human foreground is composited over them. Never show the protagonist\'s face or an embodied Original.';
if(!art.direction.includes(chapter3Exception))art.direction+='\n\n'+chapter3Exception;
const source=fs.readFileSync(sourcePath);
const sourceBlob='blob '+source.length+'\0';
const hash=createHash('sha1').update(sourceBlob).update(source).digest('hex');
assert.equal(hash,'857ffdf1bc9432cf4bbbfd7819f5f430a06d9036','Locked CH3 narrative blob changed: re-audit before updating art.');
const chapter=JSON.parse(source);
const check=process.argv.includes('--check');
const retiredPrefix='ARCHIVED / RETIRED / UNUSED — PRE-REBOOT CHAPTER 3. Historical prompt ONLY; do not generate, select, import or treat as production backlog. The 2026-11-18 approved story uses pavilion_reboot/* instead. See docs/112_CH3_ARTWORK_AUDIT_AND_GENERATION_HANDOFF_20261118.md.\n';
let retiredCount=0;
function retire(r){
  assert.equal(r.status,'not-started','Legacy art unexpectedly has selected or generated status; investigate before retiring.');
  if(!r.notes?.startsWith(retiredPrefix))r.notes=retiredPrefix+(r.notes||'');
  retiredCount++;
}
for(const [id,r] of Object.entries(art.scenes))if(id.startsWith('pavilion/'))retire(r);
for(const [id,r] of Object.entries(art.focus))if(id.startsWith('pavilion/'))retire(r);
for(const [id,r] of Object.entries(art.deathScreens))if(id.startsWith('pavilion/'))retire(r);
for(const id of ['registrar:idle','original_witness:screened'])retire(art.portraits[id]);
for(const [id,variants] of Object.entries(art.items))if(id.startsWith('pavilion_')){
  for(const r of Object.values(variants))retire(r);
}
assert.equal(retiredCount,65,'Expected all 65 archived legacy image calls (21+7+3+2+32).');

const sceneBase='Native logical-grid 314×206 OPAQUE pixel-art background for The Acceptable Error, not rescaled from larger source. Stylistic continuity with the approved Exposition reception: teal structural beams, squared gray panels, cream service counters, steel fittings, fluorescent light and crisp intentional pixel clusters; lively original 1960s civic futurism, enamel/plastic/chrome/paper, no steampunk, gold, brass, grimy dystopian fog, blur, antialiasing, generic spaceship aesthetic or UI frame. Readable signage limited to one or two important short words, actual source-size legibility; all smaller documents and announcements use non-letter marks. Never depict the protagonist or an Original/duplicate. ';
const bgBase='Exactly 564×278 newly authored OPAQUE pixel-art conversation background, independently composed at native resolution. It is a tighter, closer POV into the companion 314×206 scene, matching its architecture, palette, lights, furniture and action geography without reusing, enlarging, blurring or panning a crop. No NPCs, no portraits, no protagonist, no UI frame; reserve clean center space for a separately composited full-size transparent human foreground. ';
const fgBase='Exactly 564×278 TRANSPARENT RGBA native pixel-art NPC foreground for separate compositing over the selected matching opaque portrait background. No scenery, no shadow painted on an opaque backdrop, no UI, no protagonist; transparent outside the sprite with pixel-sharp alpha. Match the approved reception portrait density, crisp intentional shading and approachable expressive human anatomy, not a cartoon, photograph or upscale of a scene figure. ';

const sceneData=[
  ['arrival','PEOPLE\'S PAVILION — APPROACH','The Pavilion entrance seen from the Exposition concourse: cheerful rectangular civic marquee, front-facing sign PEOPLE\'S PAVILION if fully legible or simply PAVILION, a prominent restroom pictogram plus directional arrow, three subtly distinct access paths (public concourse, service stairs, tiled underground approach) joining at one public entry. Functional, inviting, bustling-by-design rather than a faceless empty claims office; no invented additional obligatory stop.','B'],
  ['restroom_entrance','THE REAL RESTROOM','A public restroom hallway with a genuinely functional door and visible short tiled sightline to sinks, gleaming pipes, paper towel bin and small stall area beyond, separated by a believable inner one-way gate and a public exit vestibule. A reassuring compact attendant desk is right beside the entrance, a human attendant seated there as a small scene figure, a bench opposite, ordinary visitor movement possible. Give the RESTROOM sign or pictogram visual prominence. A green/red one-use entry reader, industrial floor tiles and sincere civic hospitality; this is a REAL restroom, not a model or fake. No view into an occupied stall and no protagonist face.','A'],
  ['human_verification_stage','LIVE HUMAN VERIFICATION STAGE','A small cheerful live-show auditorium off the main restroom hall. One large inspection camera, microphone position, a modest marked circular moving platform, curtain track, an oversized stage countdown (graphic or large digits), one lonely spectator chair and a visible back curtain exit. A real human presenter is present as a tiny scene figure, not a synthetic host; the funny spectacle should read before any signs. Make this one coherent stage architecture to reuse across urgency, locomotion and surprise states.','A'],
  ['urgency_stage','AUTHENTIC URGENCY DEMONSTRATION','Same recognizable human-verification stage, now with the red curtains dropped around a slowly rotating platform, a bell, one spectator in a lone chair, and the genuine public restroom visible tantalizingly through a curtain gap. Comic theatrical spotlight, clear revolving-floor geometry and route backstage; do not imply the protagonist accessed the restroom. Use the same stage equipment silhouettes as human_verification_stage, not an unrelated theater.','C'],
  ['locomotion_stage','HUMAN LOCOMOTION DEMONSTRATION','The same live-stage footprint, transformed into a short mechanized moving walkway aimed toward an unmistakably soft padded pit. Safety net unfolding overhead, a reachable but tricky stationary floor behind a curtain, and a maintenance door past folding chairs. Clearly distinguish moving platform, pit and safe escape surface: the d6 jump has fair spatial stakes; no spikes or lethal cues. Camera positioned to show the imminent absurd athletic challenge.','C'],
  ['backstage','BACKSTAGE — AN ORDINARY EXIT','A disarmingly plain gray concrete service corridor behind painted exhibition flats, hanging electrical cables, discarded podium and certificates, half-eaten sandwich resting on an equipment crate, one machine seemingly applauding itself and an unopened refill carton. A simple metal EXIT door at far end, and a small daylight courtyard glimpse with a distant restroom pictogram from another building. Comically threadbare behind the optimism, one honest ordinary door. No definite Chapter 4 location.','D'],
  ['exterior_exit','PAVILION EXTERIOR — SURVIVING EXITS','Exterior service/loading margin of the same Pavilion, a large mundane loading door, foam cushions and a padded wheeled safety cart nearby, with public concourse and bench edge suggested. This one truthful master can support safe-fall and public escort terminal text; the zero-second ribbon is an event prop handled in narration, NOT a permanent inventory object. Clear daylight, nonfatal tone, no bodily harm or face of protagonist.','D'],
  ['surprise_stage','GENUINE SURPRISE — TOO EARLY','Recognizably the SAME live human-verification stage and green BEGIN DEMONSTRATION control, now raised presentation platform, early-firing confetti cannon, confetti falling at the wrong moment, the presenter caught by surprise as a small scene figure, with backstage access unlatched. The count uses a big TWO or two clear lamps if lettering is too small; absurdity visible even without text. Not a new auditorium or secret tribunal.','C'],
  ['service_exit','A HUMAN KINDNESS — SERVICE DOOR','A narrow utilitarian Pavilion service threshold, low plain maintenance door opening to daylight, understated blue-gray pipes and control cabinet. The quiet alternate departure for either the honest attendant or the relieved presenter; a single architectural setting that plausibly serves both. Warm strip of sunlight stands in deliberate contrast to the machinery. No access back to restroom and no new destination promised.','D'],
  ['record_printer','THE ENDLESS ACCURATE RECORD','Compact adjunct counter near the same genuine restroom, mechanically simple long-roll receipt printer actively streaming white paper in ridiculous coils onto gray floor tiles; a portion of the ribbon could visibly say ORIGINAL if letters are truly legible. Include attendant position, small ceremonial plant, adjacent passage and enough open floor for paper to entangle visitors. The literal official paper trail is the visual joke, not a vast registry or faceless archive office.','B'],
  ['record_scanner','AUTHORIZED PAPER — RESTROOM READER','Tight main-scene view of the same restroom door and one-way reader as restroom_entrance, with a motorized document roller at the jamb swallowing a long record slip. Door opens only a narrow slit and reveals a real tiled interior; a green indicator demonstrates that PAPER is authorized, not its human carrier. A small side counter connects believably to record_printer; no living Original person.','B'],
  ['paper_emergency','PAPER EMERGENCY — SAFETY BRUSHES','The record_printer counter in full mechanical chaos: impossible loops of white receipts entangle desk legs and a decorative plant while oversized soft motorized safety brushes sweep paper toward big exterior emergency doors. Bright absurd harmless cleanup machinery, not a shredder or violent industrial death. A few tiny bystander figures may convey physical comedy, but no protagonist face.','B'],
  ['exit_vestibule','RESTROOM EXIT VESTIBULE — ALMOST','A narrow real tiled exit vestibule inside the restroom threshold. Through a convincing transparent divider and one-way entry gate, a sink and tantalizing closed stall are plainly visible but unreachable; a polished descending EXIT ASSISTANCE ramp leads away to maintenance. Close enough to smell soap, never close enough to use a toilet. Spatially consistent with restroom_entrance and record_scanner.','D'],
  ['courtesy_stage','UNSCHEDULED COURTESY DEMONSTRATION','The actual restroom exit door AND ITS ENTIRE FRAME have slid SIDEWAYS on a concealed floor/ceiling rail into a ridiculous spotlight alcove; the real restroom remains sealed behind an inner shutter. Show travel tracks, door frame, modest spotlight and one lonely audience area. A tiny attendant and courteous visitor may remain alongside moving door; no duplicate person or manufactured Original. Canned applause starts before the spotlight, as a visual hint of the protagonist\'s old timing job.','D']
];
const bgData={
  restroom_entrance:'Attendant-facing conversational view from the doorway: attendant desk edge with enamel card reader, brushed-steel rail, real restroom threshold and small portion of tiled entrance at a side. Warm institutional practical lighting. Align desk eye-level with the seated attendant foreground; no person baked in.',
  human_verification_stage:'Presenter camera looking inward from the platform toward the performer: same big verification camera, curtain line, microphone mount and a few recognizable stage controls in closer detail. Practical theatrical lights. Leave visual breathing room for presenter silhouette; stage remains public and cheerful.',
  urgency_stage:'Close POV of rotating-platform edge, red descending curtain and distant sliver of real restroom corridor; a single lonely spectator chair at a side. Keep the original stage rail and lighting landmarks. Room for the presenter gesturing toward the visitor.',
  surprise_stage:'Close POV of the raised platform and confetti cannon housing, light-count indicator and the same green demo console as human_verification_stage, with confetti in the environment. Do not paint the startled presenter into the background.',
  record_printer:'Across the same counter, detailed endless receipt roll spilling under the attendant desk, one readable oversized ORIGINAL on slip if feasible, modest ornamental plant and glimpsed door route. A distinct camera placement from the main scene, but clearly the same actual printer.',
  record_scanner:'Tighter close POV from beside the actual restroom jamb, mechanical paper roller, green authorization indicator, narrow open-door crack and tilework; recognizable reader design from restroom_entrance. Attendant foreground faces this reader in alarm.',
  service_exit:'At the humble service door, a blue-gray wall cabinet and simple opened door revealing daylight. Neutral enough to plausibly hold the SAME close camera framing with either the relieved presenter or the honest attendant, at separate moments. No person baked in.',
  courtesy_stage:'Close POV onto the relocated restroom door frame on its overhead rail, sealed former doorway and spotlight at a side. Same restroom entrance tile, reader and door hardware as restroom_entrance; visibly dislocated rather than a magical replacement.'
};
const portraitData=[
  ['pavilion_attendant','idle','PAVILION ATTENDANT — REASSURING','A human male attendant in his late forties or fifties, neatly side-parted dark hair with a trace of gray, tidy small spectacles, modest cream shirt and slate-teal vest with plain enamel name tab. Seated-to-waist conversation framing, welcoming slightly overeager smile, hands politely together; sincere belief in rules without menace. Consistent model for all attendant poses.','restroom_entrance','A'],
  ['pavilion_attendant','alarmed','PAVILION ATTENDANT — ALARMED','SAME attendant, exact face/hair/clothes and canvas anchor as idle. Expression strained, brows raised, mouth opened mid-protest, one palm raised in a gentle stop gesture. Not a shouting villain; a courteous man briefly losing control of a ridiculous situation.','record_scanner','B'],
  ['pavilion_attendant','quiet','PAVILION ATTENDANT — HONEST QUIET','SAME attendant, exact face/hair/clothes and anchor as idle. Shoulders soften, small resigned half-smile, direct compassionate eye contact, hands lowered. Sincere human sympathy without a grand dramatic revelation.','record_printer','B'],
  ['pavilion_presenter','idle','HUMAN PRESENTER — SHOWTIME','A human female presenter in her late thirties or forties, distinctive neat short auburn bob, spirited eyebrows, tailored muted-coral blouse with slate-blue presentation jacket and simple clipped microphone. Waist-up, optimistic stage poise, one open inviting hand. Brisk animated personality but genuine humanity; distinct from receptionist and attendant. Consistent model for all presenter poses.','human_verification_stage','A'],
  ['pavilion_presenter','excited','HUMAN PRESENTER — THRILLED','SAME presenter exact face, auburn bob, muted-coral blouse and slate-blue jacket, same anchor. Eyes alight, broad delighted show-business smile, hand presenting the absurd authenticity event as a triumph. Keep her human and recognizably the same woman.','urgency_stage','C'],
  ['pavilion_presenter','alarmed','HUMAN PRESENTER — UNEXPECTED SUBJECT','SAME presenter and anchor. Alarmed eyes, mouth slightly open, microphone hand interrupted, other hand reaching to halt the demonstration; a competent employee suddenly subjected to her own machine. Expressive and sympathetic, no horror effect.','surprise_stage','C'],
  ['pavilion_presenter','relieved','HUMAN PRESENTER — HUMAN KINDNESS','SAME presenter and anchor, expression genuinely relieved, warm unguarded thankful smile, one hand gesturing toward the humble service door. A rare quiet human connection, not a new glamorous costume or authority figure.','service_exit','C']
];

const uses=new Map();
for(const [id,node] of Object.entries(chapter.nodes)){
  if(!uses.has(node.scene))uses.set(node.scene,[]);
  uses.get(node.scene).push(id);
}
assert.deepEqual([...uses.keys()].sort(),sceneData.map(row=>'pavilion_reboot/'+row[0]).sort(),'New scene list must match locked JSON exactly.');
function addRecord(group,id,record){
  if(art[group][id]){
    assert.equal(art[group][id].kind,record.kind,'Record kind must not drift: '+group+':'+id);
    assert.equal(art[group][id].dimensions,record.dimensions,'Native size must not drift: '+group+':'+id);
    // Do not overwrite later candidate revisions, source pins, owner selections,
    // status promotions or confirmed Gameplay PMO asset paths.
  }else{
    assert.ok(!check,'Missing registered art record: '+group+':'+id);
    art[group][id]=record;
  }
}
for(const [slug,title,description,batch] of sceneData){
  const id='pavilion_reboot/'+slug;
  const rec={title,kind:'scene',status:'not-started',dimensions:'314x206',assetPath:null,
    suggestedFilename:'art/scenes/pavilion_reboot/'+slug+'.png',
    prompt:sceneBase+'SCENE: '+description,
    notes:'CH3 REBOOT APPROVED SCRIPT / ART BRIEF READY; NO IMAGE GENERATED OR APPROVED. Batch '+batch+'. Source nodes: '+uses.get(id).join(', ')+'. Locked narrative blob 857ffdf1bc9432cf4bbbfd7819f5f430a06d9036. Do not assign an actual assetPath before gameplay integration.'};
  if(bgData[slug]){
    rec.portraitBackground={title:title+' — CLOSE CONVERSATION BACKGROUND',
      kind:'portrait-background',status:'not-started',dimensions:'564x278',assetPath:null,
      suggestedFilename:'art/portraits/pavilion_reboot/backgrounds/'+slug+'.png',
      prompt:bgBase+bgData[slug],
      notes:'CH3 REBOOT: paired with pavilion_reboot/'+slug+'; shared by every attendee/presenter pose used at this scene. Batch '+batch+'. NO IMAGE GENERATED OR APPROVED.'};
  }
  addRecord('scenes',id,rec);
}
for(const [speaker,pose,title,description,scene,batch] of portraitData){
  const id=speaker+':'+pose;
  addRecord('portraits',id,{title,kind:'portrait',status:'not-started',dimensions:'564x278',
    assetPath:null,suggestedFilename:'art/portraits/pavilion_reboot/'+speaker+'/'+pose+'.png',
    foregroundFormat:'transparent-rgba-png',portraitBackgroundScene:'pavilion_reboot/'+scene,
    prompt:fgBase+description,
    notes:'CH3 REBOOT: model sheet and canvas anchor must match every pose of '+speaker+'. Source instances: '+Object.entries(chapter.nodes).filter(([,n])=>n.speaker===speaker&&n.pose===pose).map(([id])=>id).join(', ')+'. Suggested default background pavilion_reboot/'+scene+'; other scene-appropriate backgrounds are catalogued on their scene records. Batch '+batch+'. NO IMAGE GENERATED OR APPROVED.'});
}
assert.equal(sceneData.length,14);
assert.equal(Object.keys(bgData).length,8);
assert.equal(portraitData.length,7);
if(!check)fs.writeFileSync(artPath,JSON.stringify(art,null,2)+'\n');
console.log((check?'CHECKED':'REGISTERED')+': 14 scenes, 8 close conversation backgrounds, 7 human pose foregrounds; 65 legacy records conspicuously archived; no image status or asset path advanced.');
