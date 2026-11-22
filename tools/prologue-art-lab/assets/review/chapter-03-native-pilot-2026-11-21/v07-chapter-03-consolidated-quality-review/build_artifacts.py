"""Read-only artwork audit: build diagnostics, matrix and review evidence."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops, ImageFont
import csv
import hashlib
import json

B = Path(__file__).resolve().parent
R = B.parents[5]
records = json.loads((B/'sources/scene-records.json').read_text())
pairings = json.loads((B/'sources/portrait-pairings.json').read_text())
baseline = json.loads((B/'sources/preservation-baseline.json').read_text())
refs = json.loads((B/'sources/cross-chapter-references.json').read_text())
initial = json.loads((B/'sources/initial-findings.json').read_text())
new_scenes = ['human_verification_stage','urgency_stage','record_printer','courtesy_stage','arrival','exit_vestibule']
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, value):
    (B/p).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
def save(image, path):
    image.save(B/(path+'-native.png'))
    image.resize((image.width*4,image.height*4),Image.Resampling.NEAREST).save(B/(path+'-4x.png'))
def pair(left, right):
    result=Image.new('RGB',(left.width+right.width,max(left.height,right.height)),'#eee9dc')
    result.paste(left.convert('RGB'),(0,0));result.paste(right.convert('RGB'),(left.width,0))
    return result

# These findings supersede density-only prescriptions, not owner approvals.
findings = {
'human_verification_stage': {
 'detail':'The auburn/coral/slate presenter reads as an inviting human at scene scale. Her open palm, separate microphone, shoes and floor contact are clear. Preserve useful facial shading rather than flattening the figure into the withdrawn pilot style.',
 'perspective':'Camera cart wheels, microphone base, platform ellipse, curtain track, pedestal and floor joints occupy coherent planes. The corrected right-wall pictogram/buttons/grille remain on the approved wall interpretation. No collision or new geometric defect is demonstrated.',
 'narrative':'The camera, marked circle, thirty display and inviting gesture establish verification. Later identity messages and platform motion are successive dialogue events; the approved alarmed portrait handles the later emotional change.',
 'continuity':'Matches Urgency, Locomotion and Surprise in sign, architecture, large camera, curtain aperture and equipment family. Keep 30 here; Surprise intentionally changes its display to two lamps. Keep the already approved left green BEGIN and separate covered red release.',
 'protect':['PEOPLE’S PAVILION sign and 30','Presenter identity, palm and shoes','Camera/cart and microphone','Curtain folds, platform and corrected right wall','Pedestal BEGIN and covered red release'],
 'focus':[72,81,120,155], 'reference':'chapter2-control-tower'},
'urgency_stage': {
 'detail':'The bell hangs from the raised hand rather than floating; its earlier three-row placement correction remains. The small visitor is intentionally economical. Red folds frame the timer without hiding the presenter, hand or route.',
 'perspective':'The repeated platform, track, wall fixtures, microphone base, camera wheels and chair contacts remain coherent. The red curtain geometry shares the established opening. Soft rim shading does not establish a broken ellipse.',
 'narrative':'Bell, red curtains, lone visitor, restroom reveal and timer support authentic_urgency. Rotation and the visitor’s later departure cannot be fully expressed in this shared still; no new label or extra figure is justified.',
 'continuity':'Same room as Verification, Locomotion and Surprise. Red fabric, bell and occupied right chair are deliberate Urgency state differences. Preserve corrected pedestal controls and wall-plane fixtures; do not copy Locomotion’s microphone removal into this state.',
 'protect':['Pavilion sign and 30','Bell-to-fingers relationship','Presenter costume and economical visitor','Red curtain aperture and platform','Camera, microphone and corrected pedestal controls'],
 'focus':[72,81,120,155], 'reference':'chapter2-control-tower'},
'record_printer': {
 'detail':'The receipt starts at the existing left cream feed unit, descends over the desk edge, and curls onto the floor toward the left. The cream strip stays distinguishable from the coral counter and darker floor; its small fold/tangent does not demonstrate a disconnected branch. No printer/plant overlap or new character-protection rectangle is present.',
 'perspective':'The desk top/front, seated forearms, feed unit, plant pot, gate pedestal and bench contacts agree with Restroom Entrance. The hanging receipt changes plane at the counter and rests on the floor. No demonstrated perspective repair is needed.',
 'narrative':'The continuous long printout communicates official evidence without attempting the full record text in tiny pixels. Later stapler jam and quiet confession are shared-master compromises; the approved quiet portrait handles that dialogue.',
 'continuity':'A01 v09 and B02 differ only in the bounded receipt area; the attendant, microphone, right plant and signs are unchanged. Selected Paper v04 escalates the same source and paper direction, but its emergency face/gesture and crossing repair must not be copied automatically into this calm printing state.',
 'protect':['Left cream paper-feed unit and output','Continuous downward/left paper route','Attendant, microphone and desk contact','Right plant and clear equipment separation','Restroom signs, gate, bench and daylight'],
 'focus':[108,129,201,206], 'reference':'chapter2-conveniences-bureau'},
'courtesy_stage': {
 'detail':'Overhead track, hangers, displaced left frame, spotlight and shutter over the original opening make the mechanical change legible. The frame is deliberately behind the foreground bench. Every pixel at x≥180, including the desk, attendant, microphone and plant, matches A01 v09; no rectangular pasted character patch is introduced.',
 'perspective':'The track/hanger/frame relationship and floor rail establish sideways travel. Foreground bench occlusion is consistent depth ordering, not an accidental sliced frame. The sealed opening and gate retain the original front plane. No unambiguous small geometry correction is demonstrated.',
 'narrative':'door_courtesy describes several moving beats. This approved environmental still shows the relocated frame, shutter and spotlight; its seated calm attendant is an accepted static-master tradeoff, while the separately approved alarmed portrait carries the urgent conversation. Do not add the door-holding visitor or move the attendant speculatively.',
 'continuity':'Retains A01’s right desk, left feed unit, v09 microphone, far-right plant, sign and tiles. The independent approved close background crops the moved frame and shutter intentionally; it does not require a new main-scene device or an equipment overlap.',
 'protect':['Track, hangers and displaced frame behind bench','Shutter and inner gate at original opening','Spotlight and existing signs','Pixel-locked right desk and attendant','Feed unit, corrected microphone and right plant'],
 'focus':[20,30,178,187], 'reference':'chapter2-conveniences-bureau'},
'arrival': {
 'detail':'Pavilion title and central entry dominate; the restroom pictogram/right arrow, service stair and underground approach remain separate. Reflected interiors, foliage and rails carry useful depth at 4×. Their large palette alone is not a defect.',
 'perspective':'Front glazing/mullions, canopy underside, bench feet, planters, exterior steps and descending foreground well have readable plane and scale relationships. Rail posts meet their supports. No floating object or impossible shared junction warrants a correction.',
 'narrative':'The public concourse, maintenance ascent and tiled underground arrival converge at one Pavilion entry. The image does not need to depict all incoming characters or quote every banner phrase. The right arrow leads into the restroom route, not an exterior permission to use the fixtures.',
 'continuity':'Teal structure, coral stripe, cream enamel and daylight agree with the interior and exterior exits. Chapter 2’s Exposition Concourse supplies the public approach; Bureau, Control Tower and Spore Garden show that useful foliage/glazing detail is compatible with the approved style.',
 'protect':['Pavilion title and restroom directional sign','Central glazed entrance and canopy','Three distinct approach cues','Bench/planter scale and grounded rails','Useful foliage, reflections and daylight'],
 'focus':[162,76,314,206], 'reference':'chapter2-exposition-concourse'},
'exit_vestibule': {
 'detail':'Left sinks and teal stall are visible but blocked by the transparent divider and one-way gate. The right EXIT arrow points down/right to a lower, handrailed route with receding lamps and a closed destination door. The adjacent restroom pictogram identifies the denied area; it does not override EXIT.',
 'perspective':'The glass mullions and gate occupy the front boundary of the fixture zone. The right ramp lip meets the vestibule floor and its side rails and ceiling lights recede toward a lower landing. A slight authored stylization is not evidence of impossible topology. No perspective correction is warranted.',
 'narrative':'door_dash_pass explicitly enters the exit vestibule, blocks fixtures behind an inner gate, then opens a descending assistance ramp to a maintenance destination. The worker belongs to that later destination. This two-zone view can show the denied fixture zone and the automatic exit together without granting restroom access.',
 'continuity':'A01 establishes sinks left, teal stalls deeper/right and an inner gate. Record Scanner shows the threshold/reader from a tighter front camera. This interior camera is farther inside the exit lane; service_exit supplies the later way out. A semantic route diagram resolves the earlier UNCERTAIN classification to KEEP; it is not a surveyed floor plan.',
 'protect':['Transparent divider and visible denied fixtures','One-way gate and reader','EXIT arrow and right descending ramp','Rail attachments, lower landing and lamps','Tiles, teal/coral material continuity'],
 'focus':[184,87,310,206], 'reference':'chapter2-control-tower'},
'restroom_entrance': {'detail':'Earlier v06 KEEP reaffirmed: reassuring attendant, v09 microphone, left feed unit, right plant and doorway details remain readable.', 'perspective':'Desk, forearms, bench and gate contacts remain coherent; the seated lower body is intentionally occluded.', 'narrative':'Calm establishing/greeting state; the alarmed portrait serves door_choices.', 'continuity':'The source room anchors Record Printer, Courtesy and selected Paper v04.', 'protect':['Approved v09 microphone','Attendant and desk','Feed unit / plant separation','Signs, gate and bench'], 'focus':[177,94,274,190], 'reference':'chapter2-conveniences-bureau'},
'locomotion_stage': {'detail':'Approved original retained; the six-pixel v02 presenter test remains generated/unselected. Foreground chairs/camera and supported net remain useful detail.', 'perspective':'Moving floor, stationary landing, padded pit and bolted net supports read as distinct components; no further proven correction.', 'narrative':'Demonstration machinery and floor hazard remain clear without a visible protagonist.', 'continuity':'Same stage architecture, 30 and corrected wall/control system; microphone removal is specific to this state.', 'protect':['Detailed foreground camera/chairs','Pit, landing and supported net','30 and Pavilion title','Presenter and controls'], 'focus':[58,81,248,164], 'reference':'chapter2-control-tower'},
'backstage': {'detail':'Approved rich original retained; v01 full reconstruction is not selected and its direction was withdrawn. Cable/scenery/props remain useful storytelling.', 'perspective':'Wall/floor seams and shrinking overhead lights lead to ordinary daylight; crate and mechanical cart remain grounded.', 'narrative':'Sandwich, papers, scenery and attached clapper support an unglamorous backstage escape; no new character.', 'continuity':'Teal/coral props and normal daylight connect stage/backstage to the Pavilion exterior.', 'protect':['Attached mechanical clapper','Scenery, cables and storytelling props','Daylight exit','Crate, sandwich and podium'], 'focus':[233,81,298,177], 'reference':'chapter2-service-entry'},
'exterior_exit': {'detail':'Initial KEEP reaffirmed. Empty padded cart, cushions, loading shutter, bench and landscaping remain distinct.', 'perspective':'Cart wheels, cushion stack, bench feet and threshold meet the concourse floor; no demonstrated scale or geometry problem.', 'narrative':'Shared safe exterior ending, not restroom access; no extra permanent ribbon or body is needed.', 'continuity':'Facade, glazing, coral stripe and landscaping match Arrival’s Pavilion exterior.', 'protect':['Empty padded cart and cushions','Loading shutter/threshold','Facade, bench and planting'], 'focus':[57,110,300,174], 'reference':'chapter2-exposition-concourse'},
'surprise_stage': {'detail':'Earlier v05 KEEP reaffirmed. Presenter remains on cannon’s left/firing side with open mouth and raised hands.', 'perspective':'Connected cannon cradle/base, raised platform and corrected right-wall fixtures remain intact.', 'narrative':'Two lamps are the compact TWO cue; confetti and cannon support genuine_surprise.', 'continuity':'Same stage, camera and covered release; brighter green BEGIN is the approved Surprise state.', 'protect':['Left/firing-side presenter','Cannon mount and direction','Two lamps and confetti','Corrected wall and controls'], 'focus':[104,56,199,132], 'reference':'chapter2-control-tower'},
'service_exit': {'detail':'Initial KEEP reaffirmed. Daylight door, cabinet, pipes and control box remain readable.', 'perspective':'Door swing, threshold, cabinet legs and floor/light projection are coherent; close backgrounds intentionally use a nearer camera.', 'narrative':'Staff passage leads to ordinary outside space without granting restroom access. Either approved helping character can appear in dialogue.', 'continuity':'Shared doorway and fixtures support both quiet attendant and relieved presenter composites.', 'protect':['Daylight exit and swing','Cabinet, pipes and control box','Floor shadows and thresholds'], 'focus':[180,37,301,193], 'reference':'chapter2-service-entry'},
'record_scanner': {'detail':'Initial KEEP reaffirmed. Wall roller, narrow door gap, green reader and paper direction remain distinct.', 'perspective':'Door jamb, roller attachment, counter top and plant contact remain coherent in the tighter camera.', 'narrative':'Paper is authorized while its carrier remains denied; the narrow opening is intentional.', 'continuity':'Same restroom sign/reader/material family, with approved idle and alarmed attendant layers. No plant/roller overlap.', 'protect':['Door gap and roller attachment','Green/red reader','Counter and right plant','Receipt direction'], 'focus':[117,79,314,205], 'reference':'chapter2-conveniences-bureau'},
'paper_emergency': {'detail':'Owner-selected localized v04 is the creative final selection. Canonical v03 is retained here as the historical/current-main baseline only.', 'perspective':'The selected repair leaves architecture, desk, brushes, microphone and floor geometry unchanged; its tight attendant/paper masks preserve surrounding shapes.', 'narrative':'V04 clarifies the paper crossing and urgent attendant expression/gesture without a visible player or new event.', 'continuity':'Same left feed source, right plant and restroom architecture. Draft PR #18 implements registration but remains unmerged; main is still v03.', 'protect':['All environment and brush supports','Left feed unit and right plant','Selected v04 face/gesture/crossing repair'], 'focus':[170,88,272,160], 'reference':'chapter2-conveniences-bureau'}
}

stage = ['human_verification_stage','urgency_stage','locomotion_stage','surprise_stage']
restroom = ['restroom_entrance','record_printer','courtesy_stage','paper_emergency']
guides = {}
for record in records:
    name=record['key'].split('/')[-1];f=findings[name]
    im=Image.open(B/record['file']).convert('RGB')
    if name in stage:
        boxes=[[0,0,314,65],[0,103,64,194],[73,81,120,155],[128,51,191,126],[217,64,314,163],[251,157,308,201]]
        lines=[[(45,45),(45,162)],[(267,45),(267,162)],[(52,62),(264,62)],[(44,172),(265,172)],[(46,177),(27,192)],[(99,177),(92,192)],[(151,177),(151,192)],[(202,177),(211,192)]]
        contacts=[[(76,152),(98,152)],[(99,154),(110,154)],[(223,159),(246,159)]]
    elif name in restroom:
        boxes=[[63,34,179,185],[201,94,245,144],[190,119,208,146],[177,130,200,146],[241,108,271,146],[174,140,273,190],[0,136,69,206]]
        if name=='courtesy_stage':boxes.append([24,32,178,186])
        lines=[[(65,66),(65,185)],[(171,65),(171,185)],[(180,34),(180,139)],[(68,65),(169,65)],[(48,204),(78,174)],[(97,205),(105,177)],[(130,205),(130,179)],[(229,205),(204,186)]]
        contacts=[[(182,187),(265,187)],[(207,141),(238,141)],[(249,143),(261,143)]]
    elif name=='arrival':
        boxes=[[16,40,271,83],[85,80,197,150],[198,87,248,118],[163,127,314,206],[0,108,92,206]]
        lines=[[(87,0),(87,145)],[(265,0),(265,83)],[(88,84),(253,84)],[(89,146),(190,146)],[(68,205),(119,151)],[(139,205),(145,151)],[(175,158),(212,135)],[(212,135),(279,135)]]
        contacts=[[(42,151),(88,151)],[(274,194),(312,194)],[(252,134),(313,134)]]
    elif name=='exit_vestibule':
        boxes=[[28,5,192,183],[42,47,167,134],[80,114,169,181],[200,26,282,93],[188,98,309,195]]
        lines=[[(30,11),(30,179)],[(178,9),(178,179)],[(41,20),(172,20)],[(48,119),(170,119)],[(192,103),(243,135)],[(293,103),(263,135)],[(193,184),(243,164)],[(301,190),(263,164)]]
        contacts=[[(81,179),(169,179)],[(191,187),(301,191)]]
    elif name=='record_scanner':
        boxes=[[32,13,175,203],[152,81,236,156],[169,146,314,206],[258,105,314,160]]
        lines=[[(34,0),(34,199)],[(180,0),(180,198)],[(49,48),(147,48)],[(55,196),(142,200)],[(171,162),(314,162)]]
        contacts=[[(171,169),(311,169)],[(283,158),(302,158)]]
    elif name=='backstage':
        boxes=[[0,0,118,143],[0,131,145,206],[140,57,203,133],[234,82,294,177]]
        lines=[[(5,0),(105,29),(242,29),(310,0)],[(22,205),(120,129)],[(298,205),(218,129)],[(103,29),(103,129)],[(241,29),(241,129)]]
        contacts=[[(242,169),(285,169)],[(0,203),(64,203)]]
    elif name=='exterior_exit':
        boxes=[[47,0,314,83],[54,119,199,170],[200,64,302,168],[0,113,65,206]]
        lines=[[(60,69),(60,154)],[(204,69),(204,162)],[(295,69),(295,161)],[(53,78),(303,78)],[(28,204),(81,168)],[(153,205),(170,168)],[(300,205),(269,168)]]
        contacts=[[(124,164),(194,164)],[(62,163),(115,163)],[(207,167),(294,167)]]
    else:
        boxes=[[48,72,127,183],[130,94,174,183],[199,39,295,183],[20,33,156,76]]
        lines=[[(20,34),(20,178)],[(183,32),(183,178)],[(203,65),(203,178)],[(291,65),(291,178)],[(56,75),(127,75)],[(29,204),(57,183)],[(130,205),(130,183)],[(271,205),(244,183)]]
        contacts=[[(55,181),(121,181)],[(205,179),(285,179)]]
    overlay=Image.new('RGBA',im.size);d=ImageDraw.Draw(overlay)
    for box in boxes:d.rectangle([box[0],box[1],box[2]-1,box[3]-1],outline=(33,209,133,215))
    protected=Image.alpha_composite(im.convert('RGBA'),overlay).convert('RGB')
    save(protected,'assessment/'+name+'-protected')
    overlay=Image.new('RGBA',im.size);d=ImageDraw.Draw(overlay)
    for line in lines:d.line(line,fill=(60,207,237,225),width=1)
    for line in contacts:d.line(line,fill=(238,109,204,235),width=1)
    save(Image.alpha_composite(im.convert('RGBA'),overlay).convert('RGB'),'assessment/'+name+'-perspective')
    save(pair(im,protected),'comparisons/'+name+'-approved-left-protected-right')
    Image.new('L',(314,206),0).save(B/'masks'/(name+'-repair-mask.png'))
    save(im.crop(f['focus']),'assessment/'+name+'-focus')
    guides[name]={'protectedContextBoxes':boxes,'perspectiveTraces':lines,'contactTraces':contacts,'focusCrop':f['focus'],'guideOnly':True,'calibration':'Approximate visual construction traces; not recovered camera calibration. Green rectangles locate details, never paste or edit masks.'}

for record in records:
    name=record['key'].split('/')[-1];f=findings[name]
    f.update({'key':record['key'],'recommendation':'KEEP' if name!='paper_emergency' else 'KEEP SELECTED V04', 'scope':'new detailed assessment'if name in new_scenes else'prior decision rechecked', 'initialRecommendation':initial[name]['action'], 'demonstratedNewDefects':[], 'proposedRepairPixels':0, 'changedPixels':0,'candidateProduced':False})
write('assessment/scene-findings.json',findings)
write('assessment/guide-coordinates.json',guides)
write('sources/changed-pixels.json',[])

alternatives=[]
old=json.loads((B.parent/'manifest.json').read_text())
for candidate in old['candidates']:
    alternatives.append({'key':candidate['catalogueKey'],'version':'v01 full reconstruction','status':'not selected; full-scene reconstruction direction withdrawn','file':str((B.parent/candidate['file']).relative_to(R)),'sha256':candidate['sha256']})
old=json.loads((B.parent/'v02-localized-repair/manifest.json').read_text())['candidate']
alternatives.append({'key':old['key'],'version':'v02 six-pixel presenter repair','status':'generated/unselected; no selection inferred','file':str((B.parent/'v02-localized-repair'/old['file']).relative_to(R)),'sha256':old['candidateSha256'],'changedPixels':6})
write('assessment/unselected-alternatives.json',alternatives)

matrix=[]
for record in records:
    name=record['key'].split('/')[-1];f=findings[name]
    row={'key':record['key'],'approvedVersion':Path(record['canonical']['source']['path']).name,
         'canonicalFile':record['canonical']['file'],'canonicalSha256':record['canonical']['sha256'],
         'canonicalSource':record['canonical']['source'],'canonicalStatus':'approved','productionAssetPath':None,
         'reviewStatus':'assessment complete; consolidated recommendation awaiting Nate visual review',
         'recommendation':f['recommendation'],'scope':f['scope'],'initialRecommendation':f['initialRecommendation'],
         'unselectedAlternatives':[a for a in alternatives if a['key']==record['key']],
         'manualTouchupRecommendation':'None demonstrated','perspective':'CHECKED — '+f['perspective'],
         'continuity':'CHECKED — '+f['continuity'],
         'crossChapterConsistency':'CHECKED — comparable useful detail/materials; inherited softness retained, no palette target',
         'repairMask':'masks/'+name+'-repair-mask.png','changedArtworkPixels':0}
    if name=='paper_emergency':
        receipt=json.loads((B/'sources/paper-v04-selection-receipt.json').read_text())
        row['selectedSupersedingArtwork']={'version':'localized v04','sha256':receipt['selectedFile']['sha256'],'source':receipt['source'],'approval':'Nate explicitly selected/approved','publication':'Selected bytes published at d1600a34a58497b4886518c6aa9feeaa205d8426 on review branch','registration':'Implemented on open unmerged draft PR #18, head 3768b174e544600c3a88e3ae8b18c0fb35982ac4. Canonical main still v03; merge/public Pages not authorized.'}
    matrix.append(row)
write('chapter-03-completion-matrix.json',matrix)
with (B/'chapter-03-completion-matrix.csv').open('w',newline='')as stream:
    fields=['key','approvedVersion','canonicalSha256','canonicalSourceCommit','canonicalSourcePath','canonicalStatus','productionAssetPath','reviewStatus','recommendation','unselectedAlternatives','selectedSupersedingArtwork','manualTouchupRecommendation','perspective','continuity','crossChapterConsistency','changedArtworkPixels']
    writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
    for row in matrix:
        writer.writerow({**{k:row[k]for k in fields if k in row},'canonicalSourceCommit':row['canonicalSource']['commit'],'canonicalSourcePath':row['canonicalSource']['path'],'productionAssetPath':'null','unselectedAlternatives':json.dumps(row['unselectedAlternatives']),'selectedSupersedingArtwork':json.dumps(row.get('selectedSupersedingArtwork'))})

portrait_findings=[]
for p in pairings:
    note='No obvious alignment, clipping or perspective defect. Foreground intentionally occludes background; waist-edge crop is not a missing lower body.'
    if 'quiet'in p['portrait']:note+=' The taller quiet attendant and bottom waist are the approved v02 correction (doc 120); do not force the idle sprite’s bounds onto it.'
    if p['scene']=='service_exit':note+=' Approved close camera omits interior floor/ceiling and serves both helping characters; no visible feet or contact with distant fixtures is required.'
    if p['scene']=='courtesy_stage':note+=' Alarmed foreground conveys the conversation while close shutter/frame state remains visible; no rectangular protection patch is introduced.'
    portrait_findings.append({**p,'recommendation':'KEEP','finding':note,'pixelsChanged':0,'portraitModificationAuthorized':False})
write('assessment/portrait-composite-findings.json',portrait_findings)

bg=Image.open(B/'references/reception-background.png').convert('RGBA');fg=Image.open(B/'references/receptionist.png').convert('RGBA')
save(Image.alpha_composite(bg,fg),'composites/reception-reference')
# A clearly labeled semantic diagram, not an invented measured floor plan.
canvas=Image.new('RGB',(1050,480),'#f2eee4');d=ImageDraw.Draw(canvas)
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',19)
title=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',23)
d.text((24,18),'Exit Vestibule: route interpretation from the locked narrative',font=title,fill='#263e45')
for box,fill,text in [((30,88,370,213),'#d9e6dd','Denied fixtures\nSinks / teal stalls'),((30,292,370,409),'#e2e3df','Exit vestibule\nCamera / arriving player offscreen'),((590,292,1020,409),'#f3d8ae','Automatic descending ramp\nLater maintenance destination')]:
    d.rounded_rectangle(box,12,fill=fill,outline='#48727b',width=3);d.multiline_text((box[0]+20,box[1]+18),text,font=font,fill='#263e45',spacing=10)
d.line([(30,251),(370,251)],fill='#4d9da8',width=8);d.text((43,221),'Glass + one-way gate: BLOCKED',font=font,fill='#263e45')
d.line([(390,350),(565,350)],fill='#b7792b',width=7);d.polygon([(565,350),(544,337),(544,363)],fill='#b7792b');d.text((401,306),'EXIT ASSISTANCE',font=font,fill='#263e45')
d.text((30,437),'Semantic adjacency only. No scale, compass bearing, recovered camera or new architectural claim.',font=font,fill='#526970')
canvas.save(B/'assessment/exit-vestibule-route-interpretation.png')
write('assessment/exit-vestibule-resolution.json',{'previous':'UNCERTAIN','recommendation':'KEEP','resolved':'Route readability and narrative adjacency; not metric floor-plan calibration','evidence':['door_dash_pass: exit vestibule → denied inner gate → automatic descending assistance → maintenance worker later','A01: visible sinks, deeper/right teal stall and inner gate','Record Scanner: threshold and one-way reader from tighter front camera','Approved D07: glass/gate left, EXIT down/right, handrails and lower landing right','Service Exit: later ordinary way outside, not access to fixtures'],'remainingLimitation':'The narrative supplies no measured floor plan. An inferred but coherent camera arrangement is not a demonstrated artwork defect.','newGeometryProposed':False,'ownerDecisionNeededBeforeAnyFutureChange':True})

cross={'result':'KEEP existing detail hierarchy','references':[r['key']for r in refs],
       'reception':'Small scene receptionist communicates hair/costume/pose; the approved portrait adds face and expression. Pavilion scene figures remain readable by auburn/coral/slate or glasses/cream/teal identity without enlarging them or erasing useful shading.',
       'chapter2':'Bureau, Control Tower, Spore Garden, Service Entry and Concourse retain abundant foliage, equipment and architectural shading. Pavilion keeps a brighter coral/teal theatrical material family. Identical palette counts or equally sparse texture are not required.',
       'limits':'Pavilion inherits softer RGB transitions and finer tiny faces than Reception. This accepted source-derived difference remains visible; no new unambiguous readability defect warrants global filtering, palette reduction or reconstruction.',
       'manualTouchupsRequired':[],'newCandidates':0,'portraitEdits':0}
write('assessment/cross-chapter-consistency.json',cross)

def metrics(path):
    image=Image.open(B/path);alpha=image.convert('RGBA').getchannel('A');values=list(alpha.get_flattened_data())
    return {'dimensions':list(image.size),'mode':image.mode,'uniqueRGB':len(set(image.convert('RGB').get_flattened_data())),'alphaExtrema':list(alpha.getextrema()),'transparentPixels':values.count(0),'partialAlphaPixels':sum(0<a<255 for a in values)}
manifest={'schema':'chapter-03-consolidated-quality-review-v07','date':'2026-11-22','reviewBranch':'art/ch3-native-pilot-20261121',
          'startingReviewCommit':baseline['reviewCommit'],'verifiedMain':baseline['mainCommit'],
          'assessmentStatus':'generated/unselected review recommendations; existing artwork approvals unchanged',
          'newDetailedAssessments':new_scenes,'sceneCount':14,'newCandidates':0,'artworkPixelsChanged':0,'portraitPixelsChanged':0,
          'portraitPairingsChecked':len(pairings),'dialogueNodesCovered':sum(len(p['nodes'])for p in pairings),
          'recommendations':{'newSix':'KEEP all six','canonicalMasters':'KEEP 13; Paper canonical v03 superseded by Nate-selected v04','paperV04':'selected/approved; draft registration PR #18 open/unmerged'},
          'requiredManualTouchups':[],'exitVestibuleUncertainty':'Resolved to KEEP for route/narrative readability; no measured floor plan inferred',
          'nativeGridAuthorshipLimitation':'Original full-scene/full-character native-grid authorship remains unresolved/unproven. Prior localized coordinate-authored repairs do not establish inherited scene or portrait authorship. Source-derived softness remains; exact dimensions alone do not resolve provenance.',
          'noGenerationOrFiltering':True,'registrationPerformedByThisTask':False,'integrationPerformed':False,'mergePerformed':False,'pagesDeploymentPerformed':False,'chapter4Changes':False,
          'priorTrackedFilesProtected':len(baseline['files']),
          'sceneSources':[{'key':r['key'],'reviewFile':r['file'],**r['canonical'],'metrics':metrics(r['file'])}for r in records],
          'crossChapterReferences':refs,'paperSelectedV04':json.loads((B/'sources/paper-v04-selection-receipt.json').read_text())['selectedFile'],
          'promptRecord':'sources/review-direction.txt; no generation calls','guidePolicy':'Overlays and composites are diagnostics, not replacement art. All scene repair masks are black/zero; all original bytes are preserved.'}
write('manifest.json',manifest)
print('Built 14-scene matrix, 14 closed masks, 14 guide pairs, 15 portrait findings; six new KEEP; zero artwork edits.')
