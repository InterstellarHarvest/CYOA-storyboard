"""Read-only canonical Chapter 4 artwork demand and production-group inventory.

Explicit scene/speaker-pose/focus/item/death keys are extracted, not invented.
Narrative-derived variants and reuse/voice questions are labelled separately.
This writes review planning files only; it never edits canonical registries.
"""
from pathlib import Path
from collections import defaultdict
import json,re,hashlib

ROOT=Path(__file__).resolve().parent.parent
CANON=ROOT/'evidence/canonical'
MAIN='622ad879dfe187ff2683ae7072515ed740522243'
GROUPS={
 'B2-01':('Public restroom dialogue and controls','Recommended first group: one close background, two character foregrounds and two existing Focus A demands; five production units.'),
 'B2-02':('Loading dock and service arrivals','Dock/lane/alley/stairs continuity, foreman and dock conversation view.'),
 'B2-03':('Maintenance access and water isolation','Pipe walkway, boiler access, groom identity/poses and the two-lever Focus A.'),
 'B2-04':('Lot 31 and Collection Stairs','Service passage, porter core poses and both authored chair-armrest Focus A views/conditional states.'),
 'B2-05':('Bride and auction clerk','Four exact bride poses and the precise clerk; reuse frozen lobby portrait background where appropriate.'),
 'B2-06':('Auctioneer and porter expression extensions','Three remaining auctioneer poses and three porter poses; retain established identities.'),
 'B2-07':('Staff lavatory used as storage','The boxed-in actual toilet, closer background and three wedding-assistant poses.'),
 'B2-08':('Boiler pressure-test room','Boiler setting/background and four engineer poses; keep fatal hanger artwork separate.'),
 'B2-09':('Commodore Bixby and the wheel','Refreshment-table setting/background and two exact Bixby poses. Wheel is a temporary story prop, not new inventory.'),
 'B2-10':('Upper salvage and freight lift','Mezzanine, freight-lift context, clerk and voice cue. Reuse salvage continuity; W.C. means Warehouse Collection.'),
 'B2-11':('Public corridor, dry and flooded','Shared corridor, closer background, guest/attendant and the explicit flood difference.'),
 'B2-12':('Organizer and bridal privacy access','Ballroom dialogue background/organizer, dressing-room setting/background, camera panel Focus A and neutral door voice context.'),
 'B2-13':('AutoFit gown inspection','Gown Focus A, manual-slack detail and authored fitting/access states; no new inventory gown or invented player portrait.'),
 'B2-14':('Three-seashell lavatory','Lavatory setting/background, shells Focus A and bathroom-voice context. No concealed fixture or usable toilet.'),
 'B2-15':('Hotel approaches and park-bound exits','Remaining arrival/forecourt/wedding-entry/bridal-corridor/courtyard keys. Reuse views where canonical continuity allows; no Chapter 5 hazards.'),
 'B2-16':('Four fatal aftermaths','Four exact artRef briefs, with strict incident-specific exclusions; no generation in this planning handoff.'),
 'B2-17':('Ticket and ring inventory/inspection','Four existing registry records. Visual briefs remain draft/review-only; record the stale inscription note, not an invented requirement.'),
 'B2-18':('Public restroom event-state derivatives','Leak/braced/flood/stall-lift families, based on frozen v07. New state files only; never overwrite the frozen entry PNG.'),
 'B2-19':('Lot 61 pod event states','Open booth, packing sequence and escaped compact case, derived from narrative; no new invented Focus A key.'),
}
SCENE_GROUP={
 'arrival':'B2-15','loading_lane':'B2-02','service_alley':'B2-02','forecourt':'B2-15','wedding_entry':'B2-15','lobby':'BATCH1','loading_dock':'B2-02','ballroom':'BATCH1','restroom':'BATCH1','maintenance':'B2-03','service_stairs':'B2-02','refreshment_table':'B2-09','service_passage':'B2-04','boiler_access':'B2-03','staff_lavatory':'B2-07','boiler_room':'B2-08','bridal_dressing_room':'B2-12','bridal_corridor':'B2-15','courtyard':'B2-15','bridal_lavatory':'B2-14','upper_salvage':'B2-10','public_corridor':'B2-11','freight_lift':'B2-10',
}
SPEAKER_GROUP={'hotel_auctioneer':'B2-06','hotel_salvage_foreman':'B2-02','hotel_wedding_organizer':'B2-12','hotel_plumber':'B2-01','hotel_plumber_assistant':'B2-01','hotel_commodore_bixby':'B2-09','hotel_bride':'B2-05','hotel_auction_clerk':'B2-05','hotel_wedding_assistant':'B2-07','hotel_boiler_engineer':'B2-08','hotel_groom':'B2-03','bridal_door_ai':'B2-12','bathroom_ai':'B2-14','hotel_salvage_clerk':'B2-10','hotel_wedding_guest':'B2-11','hotel_attendant':'B2-11','hotel_lift_voice':'B2-10'}
FOCUS_GROUP={'grand_bellevue/maintenance/water_isolator':'B2-03','grand_bellevue/restroom/lot_14_receipt':'B2-01','grand_bellevue/restroom/master_isolator':'B2-01','grand_bellevue/auction_floor/chair_armrest':'B2-04','grand_bellevue/collection_stairs/chair_armrest':'B2-04','grand_bellevue/bridal_privacy_panel':'B2-12','grand_bellevue/autofit_gown':'B2-13','grand_bellevue/three_seashells':'B2-14'}
VOICES={'bridal_door_ai','bathroom_ai','hotel_lift_voice'}

def load(name):return json.loads((CANON/name.replace('/','__')).read_text())
def flat(v):
 if isinstance(v,str):return [v]
 if isinstance(v,list):return sum((flat(x) for x in v),[])
 if isinstance(v,dict):return sum((flat(x) for k,x in v.items() if k in ['text','desc','say']),[])
 return []
def walk(v):
 if isinstance(v,dict):
  yield v
  for x in v.values():yield from walk(x)
 elif isinstance(v,list):
  for x in v:yield from walk(x)
def strings(v):
 if isinstance(v,str):yield v
 elif isinstance(v,dict):
  for k,x in v.items():yield k;yield from strings(x)
 elif isinstance(v,list):
  for x in v:yield from strings(x)

def main():
 chapter=load('story/chapters/chapter-04.wip.json');nodes=chapter['nodes'];registry=load('story/artwork.draft.json');items=load('story/items.draft.json')
 assets=[];coverage={id_:[] for id_ in nodes}
 def add(category,key,nodeids,group,**extra):
  entry={'inventoryId':category+':'+key,'category':category,'logicalKey':key,'nodeIds':list(dict.fromkeys(nodeids)),'group':group,'artworkStatus':'UNSELECTED','registeredAssetPath':None,**extra};assets.append(entry)
  for id_ in entry['nodeIds']:coverage[id_].append(entry['inventoryId'])
  return entry
 scenes=defaultdict(list);poses=defaultdict(list);bgs=defaultdict(list);focus=defaultdict(list);inline=defaultdict(list)
 for id_,n in nodes.items():
  scenes[n['scene']].append(id_)
  if n.get('speaker'):poses[(n['speaker'],n.get('pose'))].append(id_);bgs[n['scene']].append(id_)
  if n.get('focus'):focus[n['focus']].append(id_)
  for part in walk(n.get('text')):
   if part.get('who'):inline[part['who']].append(id_)
 frozen={'grand_bellevue/lobby':'CH4-01','grand_bellevue/restroom':'CH4-04','grand_bellevue/ballroom':'CH4-05'}
 for scene,ids in scenes.items():
  add('main_scene',scene,ids,SCENE_GROUP[scene.split('/')[-1]],canonicalEvidenceFields=['scene'],dimensions=[314,206],coverageState='FROZEN_PREFERRED_UNSELECTED' if scene in frozen else 'UNPRODUCED_LOGICAL_DEMAND',preferredBatch1Asset=frozen.get(scene),sourceExcerpt=flat(nodes[ids[0]].get('text'))[:2],planningNote='Router/arrival context; a separate bitmap is not automatically required. Reuse may resolve this scene key.' if scene.endswith('/arrival') else 'Scene key is canonical; required visual content comes from its nodes, not a newly invented asset brief.')
 for (speaker,pose),ids in poses.items():
  group=SPEAKER_GROUP.get(speaker)
  if speaker=='hotel_porter':group='B2-04' if pose in ['businesslike','practical','uncertain'] else 'B2-06'
  covered=speaker=='hotel_auctioneer' and pose=='showman'
  if covered:group='BATCH1'
  add('portrait',speaker+':'+pose,ids,group,canonicalEvidenceFields=['speaker','pose'],speaker=speaker,pose=pose,dimensions=[564,278],alpha='transparent foreground where a visible character/device foreground is used',coverageState='V08_REVIEW_CANDIDATE_UNSELECTED' if covered else 'UNPRODUCED_EXPLICIT_POSE_KEY',preferredBatch1Asset='CH4-03' if covered else None,visualRealization='Voice/device context only is authored; do not invent a human face or a device design. May reuse the matching panel/focus/frame instead of a new foreground PNG.' if speaker in VOICES else 'Human NPC portrait; retain identity across the exact authored poses.',sceneKeys=sorted({nodes[i]['scene'] for i in ids}))
 for scene,ids in bgs.items():
  group='B2-01' if scene.endswith('/restroom') else 'B2-12' if scene.endswith('/ballroom') else SCENE_GROUP[scene.split('/')[-1]]
  add('portrait_background',scene,ids,group,canonicalEvidenceFields=['scene','speaker'],dimensions=[564,278],alpha='opaque architectural background',coverageState='FROZEN_PREFERRED_UNSELECTED' if scene.endswith('/lobby') else 'PLANNED_DIALOGUE_CONTEXT',preferredBatch1Asset='CH4-02' if scene.endswith('/lobby') else None,canonicalKeyNote='Derived dialogue-location demand under the established layered portrait contract, not an already registered new canonical background ID.',planningNote='One location can share a consistent closer camera among speakers. Voice-only panels may reuse a context view; do not automatically count every key as a distinct PNG.')
 for key,ids in focus.items():
  add('focus_a',key,ids,FOCUS_GROUP[key],canonicalEvidenceFields=['mode','focus','text'],dimensions=[564,278],dimensionsBasis='Established Focus A convention; no CH4 registry record yet',coverageState='UNPRODUCED_EXPLICIT_FOCUS_KEY',sourceTexts={i:nodes[i]['text'] for i in ids},sourceNotes={i:nodes[i].get('notes') for i in ids})
 # Inventory demands are taken from actual existing registry records, not
 # inferred from every prop mentioned in dialogue.
 for item in ['lot_53_dispute_ticket','wedding_ring_lot31']:
  ids=[id_ for id_,n in nodes.items() if item in set(strings(n))]
  if item=='wedding_ring_lot31':ids+=['hotel_ring_inspect_inscription']
  for kind,record in registry['items'][item].items():
   add('inventory_'+kind,item,ids,'B2-17',canonicalEvidenceFields=['items.draft entry','artwork.draft items/'+item+'/'+kind],dimensions=[int(v) for v in record['dimensions'].split('x')],registryStatus=record['status'],suggestedFilename=record.get('suggestedFilename'),registeredAssetPath=record.get('assetPath'),registryPromptVerbatim=record['prompt'],registryNotesVerbatim=record.get('notes'),itemDescriptionVerbatim=items[item]['description'],coverageState='EXISTING_DRAFT_ART_RECORD_UNPRODUCED',briefGate='Planning only: canonical registry labels these visual briefs review-only/not yet approved. No item artwork is generated here.')
 for id_,n in nodes.items():
  if not n.get('endingArt'):continue
  add('fatal_aftermath',n['endingArt'],[id_],'B2-16',canonicalEvidenceFields=['endingArt','deathPopup.artRef','notes'],dimensions=[314,206],dimensionsBasis='Existing project death-screen logical-grid standard; integration/runtime presentation remains a later check',title=n['deathPopup']['title'],sourcePopupVerbatim=n['deathPopup'],sourceBriefVerbatim=n['notes'],coverageState='NARRATIVE_BRIEF_AUTHORED_ART_UNPRODUCED',artworkApprovalInheritedFromNarrative=False)
 # Supported visual-state families, labelled as narrative-derived planning.
 # These are NOT new canonical art keys or automatic full-scene bitmap mandates.
 states=[
  ('lobby_door_removal',['hotel_auctioneer_arrival','hotel_restroom_entry'],'B2-18','Removal in progress / doorless entrance. Separate state layer/file over the frozen lobby, not a cosmetic rewrite.'),
  ('restroom_active_leak',['hotel_restroom_plumber'],'B2-18','Burst copper pipe, spray and airborne towels during the authored dialogue sequence; timing/state-layer representation is a production proposal.'),
  ('restroom_braced_or_contained',['hotel_valve_braced','hotel_wheel_return','hotel_key_master_cabinet'],'B2-18','Braced/dripping or contained water states. Reuse compatible frames when no visible distinction is necessary.'),
  ('restroom_flood',['hotel_valve_flood'],'B2-18','Flooded room, floating towel basket/Eddie and open service escape. Preserve entry-state geometry.'),
  ('stall_lifting_and_removed',['hotel_stall_lot_claimed','hotel_stall_crane_success','hotel_stall_public_corridor_walk'],'B2-18','Closed stall lifts through the ceiling; a later missing-enclosure view. No invented protagonist face or nudity.'),
  ('chair_and_ring_states',['hotel_chair_stapler_stealth','hotel_chair_ring_focus','hotel_ring_slips','hotel_collection_ring_focus','hotel_collection_ring_porter_recovery','hotel_collection_ring_stapler_recovery'],'B2-04','Focus/prop variants for loosened seam, caught ring, deeper slipped ring and recovered ring. Use the exact conditional flag text; do not mandate whole-room repaints.'),
  ('staff_boxes_attempt',['hotel_staff_lavatory_storage','hotel_staff_lavatory_move_boxes'],'B2-07','Boxes and storage obstruction are authored. If a single base carries both pages, no extra bitmap is required.'),
  ('boiler_pressure_state',['hotel_boiler_pressure_intro','hotel_boiler_pressure_relieved'],'B2-08','Authored pressure test/relief can use gauge/steam overlays or reuse. No invented explosion state or global power failure.'),
  ('lot61_open_and_packed',['hotel_lot61_pod_auction','hotel_lot61_pod_escaped','hotel_lot61_pod_declined'],'B2-19','Open booth with actual toilet/warning; packing phase; escaped compact case. Fatal case/shoe artwork is a separate exact aftermath brief.'),
  ('bridal_privacy_status',['hotel_bridal_door_focus','hotel_bridal_autofit_survived'],'B2-12','Locked bride-only panel versus green/provisional authorization and opened door. Prefer a state layer; ring never opens this door.'),
  ('gown_motor_manual_slack',['hotel_bridal_gown_focus','hotel_bridal_gown_motor','hotel_bridal_autofit_survived'],'B2-13','Lining/motor/cables/manual-slack detail, safety clue and authorized fitting result. The motor inspection is narrative, not an invented ninth Focus A key; no new gown inventory item or player portrait is implied.'),
  ('public_corridor_flood',['hotel_stall_public_corridor_walk','hotel_flooded_public_corridor'],'B2-11','Dry corridor versus flooded carpet/WET FLOOR sign. The authored scene key is shared.'),
 ]
 for key,ids,group,description in states:
  add('state_family',key,ids,group,canonicalEvidenceFields=['text','effects/flags where present'],canonicalKey=None,coverageState='NARRATIVE_DERIVED_VARIANT_PLAN',representation='Layer/focus-state/full-frame choice remains production planning; one family can have multiple images or reuse.',description=description,evidence={i:{'scene':nodes[i]['scene'],'text':nodes[i]['text'],'effects':nodes[i].get('effects')} for i in ids})
 known=set(items);used=defaultdict(list)
 for id_,n in nodes.items():
  for key in sorted(set(strings(n))&known):used[key].append(id_)
 reuses=[{'item':k,'nodeIds':v,'artworkRecords':registry['items'].get(k),'action':'Reuse existing prior-chapter slot/inspection assets; no new CH4 item identity.'} for k,v in sorted(used.items()) if k not in ['lot_53_dispute_ticket','wedding_ring_lot31']]
 primary={s for s,p in poses}
 unresolved=[]
 for who,ids in inline.items():
  if who=='visitor' or who in primary:continue
  unresolved.append({'speakerTag':who,'nodeIds':list(dict.fromkeys(ids)),'pose':None,'issue':'Inline-only tag, no authored foreground pose. Do not invent a mandatory new portrait PNG.','reuseProposal':{'hotel_second_porter':'Second existing porter identity can supply inline dialogue if a visible portrait is needed; pose remains unspecified.','hotel_service_foreman':'Likely alias of primary hotel_salvage_foreman; record the canonical tag mismatch rather than creating a second foreman.','autofit_system':'Machine voice can reuse gown/mechanism context; no invented human.'}.get(who)})
 bygroup=[]
 for key,(title,note) in GROUPS.items():
  members=[a for a in assets if a['group']==key];bygroup.append({'id':key,'title':title,'note':note,'inventoryIds':[a['inventoryId'] for a in members],'primaryUnits':sum(a['category']!='state_family' for a in members),'stateFamilies':sum(a['category']=='state_family' for a in members),'nodeIds':sorted({i for a in members for i in a['nodeIds']}),'generationStarted':False})
 for g in bygroup:
  if g['id']=='B2-04':
   g['reviewSlices']=[{'slice':'A','scope':'Service passage, closer background and three core porter poses','primaryUnits':5},{'slice':'B','scope':'Two authored chair-armrest Focus A views plus supported ring-position states','primaryUnits':2,'stateFamilies':1}]
  elif g['id']=='B2-18':
   g['reviewSlices']=[{'slice':'A','scope':'Leak, braced/contained and flood states','stateFamilies':3},{'slice':'B','scope':'Door removal and stall lifting/removed states','stateFamilies':2}]
 first=next(g for g in bygroup if g['id']=='B2-01')
 totals={category:sum(a['category']==category for a in assets) for category in sorted({a['category'] for a in assets})}
 inventory={'title':'Chapter 4 Batch 2 onward — canonical artwork inventory','canonicalMain':MAIN,'canonicalSources':'evidence/canonical-sources.json','chapterNodeCount':len(nodes),'nodeCoverageCount':len([v for v in coverage.values() if v]),'scope':'Inventory/planning only. No Batch2 artwork generated; all unselected review assets remain separate from formal approval/production registration.','explicitReferenceCounts':{'sceneKeys':len(scenes),'speakerPoseKeys':len(poses),'primarySpeakers':len(primary),'dialogueLocations':len(bgs),'focusKeys':len(focus),'newItemArtRecords':4,'fatalAftermathKeys':4},'remainingAfterBatch1':{'sceneKeysWithoutPreferredBase':len(scenes)-3,'portraitPoseKeysBeyondShowman':len(poses)-1,'dialogueLocationsBeyondFrozenLobby':len(bgs)-1,'focusKeys':len(focus),'newItemArtRecords':4,'fatalAftermathKeys':4},'counts':totals,'assetCountsAreLogicalDemandsNotFinalUniquePNGCounts':True,'assets':assets,'groups':bygroup,'recommendedFirstGroup':first,'priorItemReuses':reuses,'inlineSpeakerQuestions':unresolved,'nonInventoryProps':['recalled shutoff wheel','three seashells on the counter','temporary worn AutoFit gown'],'canonicalRegistryGaps':['No Chapter4 scene/portrait/focus/death registry records yet. Logical references and source node coverage are inventoried without writing registry entries.','Existing ring inspection art notes say inscription not authored, but approved chapter node hotel_ring_inspect_inscription and items.draft already specify AS IS, WHERE IS. Treat the older art note as stale; decide presentation/reveal before producing inspection art. No extra image variant is automatically mandated.','AI/voice primary speaker-pose keys are authored; visible human/device foreground designs are not. Reuse hardware/focus/context when appropriate.','Inline hotel_service_foreman differs from primary hotel_salvage_foreman. Preserve the mismatch for mapping review; do not change story tags in this artwork branch.'],'restrictions':['No wedding-management errands or new story nodes.','No Chapter5 fried-animal/security-plant imagery on Chapter4 exits.','Three seashells remain on a bare counter; no toilet, button, hose or hidden fixture.','Ring never unlocks bride-only door.','Keep fatal images to their exact incident-specific briefs.','Use approved Chapter2 environmental rendering and Pavilion/human NPC portrait finish; small scene NPCs remain simpler but recognizable.'],'nodeCoverage':coverage}
 (ROOT/'BATCH2-INVENTORY.json').write_text(json.dumps(inventory,indent=2)+'\n')
 lines=['# Chapter 4 Batch 2 artwork inventory','',f'Canonical main: `{MAIN}`. All **120/120 nodes** are covered by source references. This is planning, not art approval, registry insertion or new production work.','',f'Explicit demands: **{len(scenes)} scene keys, {len(poses)} speaker/pose keys across {len(primary)} primary speakers, {len(bgs)} dialogue locations, {len(focus)} Focus A keys, 4 new inventory-art records and 4 fatal aftermaths**. Three base scenes, the lobby portrait background and auctioneer showman have Batch 1 review candidates. Logical keys do not imply one new bitmap each: reuse and state layers may resolve several demands.','', '## Recommended first production group','',f'**{first["id"]} — {first["title"]}**: five units, all from explicit existing demands:','']
 for a in assets:
  if a['group']=='B2-01':lines.append(f'- `{a["category"]}` — `{a["logicalKey"]}`. Nodes: '+', '.join('`'+i+'`' for i in a['nodeIds'])+'.')
 lines+=['','Use frozen v07 restroom geometry, the high-resolution plumber/assistant masters for character continuity, approved Pavilion portraits as the finish benchmark, and a separately authored closer 564×278 background. Do not enlarge tiny scene sprites into portraits. Lot14 receipt text and the red cabinet lever come directly from their Focus A nodes. This group establishes the next dialogue pair and actionable clues without changing any frozen environment. No Batch2 generation has started.','', '## Manageable follow-on groups','', '| Group | Scope | Primary units / state families |','|---|---|---|']
 for g in bygroup:lines.append(f'| {g["id"]} | {g["title"]} | {g["primaryUnits"]} / {g["stateFamilies"]} |')
 lines += ['', 'Larger families have explicit review slices rather than an oversized image dump: B2-04A is the five-unit passage/porter kit; B2-04B is the two Focus A views with ring-state variants. B2-18A covers leak/braced/flood; B2-18B covers door removal and stall lift/removal. Reuse/overlays may reduce PNG counts without dropping authored visual differences.']
 for cat,title in [('main_scene','Main scene keys'),('portrait','Exact portrait speaker/pose keys'),('portrait_background','Portrait-background contexts'),('focus_a','Explicit Focus A close-ups'),('inventory_slot','New inventory slot art'),('inventory_inspect','New inspection art'),('fatal_aftermath','Fatal aftermath illustrations'),('state_family','Narrative-derived scene/focus state families')]:
  lines+=['','## '+title,'','| Logical key | Group | Source nodes / status |','|---|---|---|']
  for a in assets:
   if a['category']!=cat:continue
   nodes_text=', '.join('`'+i+'`' for i in a['nodeIds'])
   if cat=='main_scene':nodes_text=str(len(a['nodeIds']))+' nodes; '+a['coverageState']+'; see JSON for every node ID'
   if cat=='portrait_background':nodes_text=str(len(a['nodeIds']))+' dialogue nodes; '+a['coverageState']
   if cat=='state_family':nodes_text=a['description']+' Sources: '+nodes_text
   lines.append(f'| `{a["logicalKey"]}` | {a["group"]} | {nodes_text} |')
 lines+=['','## Evidence, reuse and unresolved mappings','','- Every inventory row has exact node IDs and canonical evidence fields; state families additionally preserve the relevant narrative text. [Machine-readable inventory](BATCH2-INVENTORY.json), [120-node coverage table](BATCH2-NODE-COVERAGE.tsv), [canonical snapshots](evidence/canonical-sources.json).','- Portraits: 564×278 transparent foreground plus opaque location context; Focus A: established 564×278 convention. Inventory: existing registry explicitly specifies 96×96 slot and 565×451 inspection. Fatal aftermaths: existing project 314×206 standard; runtime/approval integration remains separate.','- AI/voice entries are not instructions to invent human bodies or unapproved hardware. Inline-only tags do not create new pose requirements.','- Existing ticket/ring art briefs are labelled draft/review-only in the registry. They are inventoried, not generated or silently approved. The ring engraving is already authored in the current narrative/item text; the older art note is stale.','- Do not make inventory art for the temporary wheel, seashells or gown. Reuse existing prior-chapter carried-item art where referenced.','']
 for q in unresolved:lines.append('- `'+q['speakerTag']+'`: '+q['reuseProposal'])
 lines+=['','## Exact fatal art constraints','']
 for a in assets:
  if a['category']=='fatal_aftermath':lines+=['### '+a['title'],'',a['sourceBriefVerbatim'],'']
 lines+=['## Guardrails','']+['- '+v for v in inventory['restrictions']]
 (ROOT/'BATCH2-INVENTORY.md').write_text('\n'.join(lines)+'\n')
 table=['node_id\tmode\tscene\tspeaker_pose\tinventory_references']
 for id_,n in nodes.items():table.append('\t'.join([id_,n['mode'],n['scene'],(n.get('speaker','')+(':'+n['pose'] if n.get('pose') else '')),';'.join(coverage[id_])]))
 (ROOT/'BATCH2-NODE-COVERAGE.tsv').write_text('\n'.join(table)+'\n')
 print(json.dumps({'nodes':len(nodes),'coverage':inventory['nodeCoverageCount'],'explicit':inventory['explicitReferenceCounts'],'recommendedFirstGroup':first['id'],'firstGroupUnits':first['primaryUnits']},indent=2))

if __name__=='__main__':main()
