"""Reproducible derived exports. Generator originals are immutable; no native-grid claim.
Run from repo root. Only writes this review package and nine generated catalogue notes.
"""
from pathlib import Path
import json, hashlib, subprocess, html, shutil
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[6]
OUT = Path(__file__).resolve().parent
ART = ROOT/'story/artwork.draft.json'
a = json.loads(ART.read_text())
n = json.loads((ROOT/'story/chapters/chapter-03.reboot-candidate.json').read_text())
refs = json.loads((OUT/'references/approved-sources.json').read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
savejson = lambda p,d: p.write_text(json.dumps(d,indent=2)+'\n')
NEAR = Image.Resampling.NEAREST
specs = [
 ('CH3-D01-service-exit','scenes:pavilion_reboot/service_exit'),
 ('CH3-D02-service-exit-bg','scenes:pavilion_reboot/service_exit#portraitBackground'),
 ('CH3-D03-attendant-quiet','portraits:pavilion_attendant:quiet'),
 ('CH3-D04-presenter-relieved','portraits:pavilion_presenter:relieved'),
 ('CH3-D05-backstage','scenes:pavilion_reboot/backstage'),
 ('CH3-D06-exterior-exit','scenes:pavilion_reboot/exterior_exit'),
 ('CH3-D07-exit-vestibule','scenes:pavilion_reboot/exit_vestibule'),
 ('CH3-D08-courtesy-stage','scenes:pavilion_reboot/courtesy_stage'),
 ('CH3-D09-courtesy-stage-bg','scenes:pavilion_reboot/courtesy_stage#portraitBackground'),
]
def record(key):
 category,k = key.split(':',1)
 if k.endswith('#portraitBackground'):return a[category][k.split('#')[0]]['portraitBackground']
 return a[category][k]
def nodes(key):
 category,k = key.split(':',1)
 return [name for name,v in n['nodes'].items() if (v.get('scene') == k.split('#')[0] if category=='scenes' else v.get('speaker','')+':'+v.get('pose','')==k)]
deps = {
 'D01':['scenes:pavilion_reboot/restroom_entrance'],
 'D02':['scenes:pavilion_reboot/restroom_entrance#portraitBackground'],
 'D03':['portraits:pavilion_attendant:idle','scenes:pavilion_reboot/record_printer#portraitBackground'],
 'D04':['portraits:pavilion_presenter:idle'],
 'D05':['scenes:pavilion_reboot/restroom_entrance','scenes:pavilion_reboot/locomotion_stage'],
 'D06':['scenes:pavilion_reboot/arrival'],
 'D07':['scenes:pavilion_reboot/restroom_entrance','scenes:pavilion_reboot/record_scanner'],
 'D08':['scenes:pavilion_reboot/restroom_entrance','portraits:pavilion_attendant:alarmed'],
 'D09':['scenes:pavilion_reboot/restroom_entrance#portraitBackground','portraits:pavilion_attendant:alarmed'],
}
constraints = [
 'One threshold shared by presenter_help_end and attendant_honest_end; door right, cabinet/pipes left; no restroom access.',
 'Independent close camera sharing D01 right-side door, left cabinet, stripe, daylight; either approved human anchor.',
 'Approved attendant identity, glasses, tie, vest and badge; same seated waist baseline as idle; used with printer AND service background.',
 'Approved presenter identity, coral blouse, slate jacket, auburn bob; bottom-anchored waist and rightward open hand.',
 'Behind existing exhibit, concrete/teal structure; cables, half sandwich, carton, podium, certificates and clapper machine clear of walkway.',
 'Same Pavilion exterior materials; empty padded cart, cushions, loading door, concourse/bench; three safe endings, no permanent ribbon.',
 'Same sinks, teal stall, reader and one-way gate; glass blocks access; descending exit assistance to maintenance.',
 'Changed real restroom state, frame moves left BEHIND foreground bench; original opening shuttered; right desk and all fixtures pixel-locked.',
 'Same close camera and counter; shutter/track at left, relocated frame partly outside crop; intercom/mic/plant and right wall pixel-locked.',
]
limitations = [
 'New view is more front-facing and spacious than the brief’s narrow service threshold; confirm architectural fit.',
 'New close view retains objects but is somewhat panoramic rather than a distinctly tighter camera; confirm main/close correspondence.',
 'Source-derived face/hand proportions vary slightly from idle. Lower torso extended by generated correction to canvas edge for service anchoring; upper portrait pixels preserved. Confirm natural waist and hands in both contexts.',
 'Generator added a small lapel microphone absent from approved idle; removed from derived foreground using approved jacket pixels. Identity/expression need review.',
 'The first source had a separate daylight gap; a masked generated correction now places daylight through one ordinary open exit. Clapper machine is deliberately mechanical; confirm rear-wall perspective.',
 'One loading-margin master relies on terminal narration for the escorted and zero-second exits; no action figures or ribbon are baked in.',
 'Generated ramp correction removes stair-like treads; actual toilet is not visible below stall, although the sink and blocked stall are clear. Confirm descending slope and implied restroom topology.',
 'State layer changes left-wall area and gate details; inner doorway trim remains fixed while portable frame moves. Bench occludes frame base; confirm physical travel clearance.',
 'Moved frame mostly outside close crop; counter keeps original foreground equipment while state sits behind it. Confirm this framing sufficiently explains relocation.',
]
candidates=[]
for i,(ident,key) in enumerate(specs):
 r=record(key); dim=tuple(map(int,r['dimensions'].split('x')))
 source=OUT/'originals'/f'{ident}-generator.png'
 if i==7:source=OUT/'originals/CH3-D08-window-correction-generator.png'
 original=Image.open(source)
 im=original.resize(dim,NEAR)
 operations=[{'operation':'nearest-neighbor source-grid transfer','from':list(original.size),'to':list(dim),'nativeAuthorship':'unproven; this is a derived export, not fresh higher-resolution authorship'}]
 if i in (2,3):
  im=im.convert('RGBA'); alpha=im.getchannel('A').point(lambda x:255 if x>=128 else 0);im.putalpha(alpha)
  # Re-anchor the generated silhouette to the approved character’s alpha bounds.
  approved=Image.open(OUT/refs['portraits:pavilion_attendant:idle' if i==2 else 'portraits:pavilion_presenter:idle']['reviewFile']).convert('RGBA')
  source_bbox=im.getbbox();target_bbox=approved.getbbox()
  sprite=im.crop(source_bbox).resize((target_bbox[2]-target_bbox[0],target_bbox[3]-target_bbox[1]),NEAR)
  im=Image.new('RGBA',dim,(0,0,0,0));im.paste(sprite,target_bbox[:2])
  operations.append({'operation':'binary-alpha threshold 128 and nearest-neighbor alpha-bounds alignment','generatedBounds':source_bbox,'approvedBounds':target_bbox})
  # Retain exact approved torso pixels for presenter costume continuity, excluding head/raised arm.
  if i==3:
   # Remove invented dark lapel microphone at native coordinates using matching approved jacket region.
   # Mask is a small semantic jacket patch; never a rectangular background protection around a person.
   mask=Image.new('L',dim,0);ImageDraw.Draw(mask).polygon([(177,179),(190,179),(191,204),(176,204)],fill=255)
   for y in range(179,205):
    for x in range(176,192):
     if mask.getpixel((x,y)) and im.getpixel((x,y))[3] and approved.getpixel((x,y))[3]:im.putpixel((x,y),approved.getpixel((x,y)))
   mask.save(OUT/'proofs/D04-costume-repair-mask.png')
   operations.append({'operation':'approved jacket pixels inside lapel repair mask','mask':'proofs/D04-costume-repair-mask.png','approvedSource':'portraits:pavilion_presenter:idle'})
  if i==2:
   correction=Image.open(OUT/'originals/CH3-D03-anchoring-correction-generator.png').resize(dim,NEAR).convert('RGBA')
   correction.putalpha(correction.getchannel('A').point(lambda x:255 if x>=128 else 0))
   im.save(OUT/'proofs/D03-initial-seated-cut-before-correction.png')
   # Keep all upper portrait pixels; generated lower-torso correction supplies a natural canvas-edge anchor.
   im.paste(correction.crop((0,230,564,278)),(0,230))
   operations.append({'operation':'generated lower-torso correction, rows 230..277 only; upper pixels unchanged','source':'originals/CH3-D03-anchoring-correction-generator.png','prompt':'prompts/CH3-D03-anchoring-correction.txt','sha256':sha(OUT/'originals/CH3-D03-anchoring-correction-generator.png')})
  # Canonicalize hidden transparent RGB so no colored matte can survive exported alpha.
  pixels=[p if p[3] else (0,0,0,0) for p in im.getdata()];im.putdata(pixels)
 else:im=im.convert('RGB')
 if i in (4,6):
  correction=Image.open(OUT/f'originals/CH3-D{str(i+1).zfill(2)}-correction-generator.png').resize(dim,NEAR).convert('RGB')
  mask=Image.new('L',dim,0);d=ImageDraw.Draw(mask)
  if i==4:d.polygon([(142,55),(223,55),(223,128),(142,128)],fill=255)
  else:d.polygon([(191,185),(239,160),(263,160),(305,193)],fill=255)
  im=Image.composite(correction,im,mask)
  maskfile=f'proofs/{ident}-correction-mask.png';mask.save(OUT/maskfile)
  operations.append({'operation':'generated localized correction inside explicit mask; original source pixels retained elsewhere','mask':maskfile,'source':f'originals/CH3-D{str(i+1).zfill(2)}-correction-generator.png','prompt':f'prompts/CH3-D{str(i+1).zfill(2)}-correction.txt','sha256':sha(OUT/f'originals/CH3-D{str(i+1).zfill(2)}-correction-generator.png')})
 if i in (7,8):
  refkey='scenes:pavilion_reboot/restroom_entrance'+('#portraitBackground' if i==8 else '')
  approved=Image.open(OUT/refs[refkey]['reviewFile']).convert('RGB')
  mask=Image.new('L',dim,0);draw=ImageDraw.Draw(mask)
  if i==7:
   draw.polygon([(24,32),(72,32),(72,64),(177,64),(177,185),(67,185),(67,139),(24,139)],fill=255)
   # Preserve foreground bench pixels; the back-wall door travels behind it.
   draw.polygon([(24,139),(67,139),(67,185),(24,185)],fill=0)
  else:
   draw.polygon([(0,4),(110,4),(110,164),(88,164),(88,213),(0,213)],fill=255)
  im=Image.composite(im,approved,mask)
  maskfile=f'proofs/{ident}-state-mask.png';mask.save(OUT/maskfile)
  overlay=im.convert('RGBA');overlay.putalpha(mask);overlay.save(OUT/f'proofs/{ident}-state-layer.png')
  changed=[]
  for y in range(dim[1]):
   for x in range(dim[0]):
    if im.getpixel((x,y))!=approved.getpixel((x,y)):changed.append([x,y])
  savejson(OUT/f'proofs/{ident}-changed-coordinates.json',changed)
  operations.append({'operation':'opaque generated state inside explicit mask over exact approved base','base':refkey,'mask':maskfile,'changedCoordinates':f'proofs/{ident}-changed-coordinates.json','changedPixelCount':len(changed),'outsideMaskChanged':0})
 file=f'candidates/{ident}-v01.png';im.save(OUT/file)
 preview=f'proofs/{ident}-4x.png';im.resize((dim[0]*4,dim[1]*4),NEAR).save(OUT/preview)
 alpha=im.convert('RGBA').getchannel('A'); hist=alpha.histogram()
 c={'candidateId':ident,'record':key,'status':'generated','selected':False,'approved':False,'assetPath':None,'file':file,'preview4x':preview,'sha256':sha(OUT/file),'dimensions':dim,'mode':im.mode,'opacity':'binary alpha' if i in (2,3) else 'opaque','alphaValidation':{'transparent':hist[0],'opaque':hist[255],'partial':sum(hist[1:255])},'source':{'tool':'image_gen built-in','original':str(source.relative_to(OUT)),'sha256':sha(source),'dimensions':original.size,'mode':original.mode},'registeredPrompt':r['prompt'],'prompt':f'prompts/{ident}.txt','operations':operations,'sourceNodes':nodes(key),'approvedDependencies':deps[ident[4:7]],'constraints':constraints[i],'knownLimitations':[limitations[i],'Original native-grid authorship unproven; source softness and high color count remain.'],'generationOrder':i+1,'newGenerationNecessary':True}
 candidates.append(c)
 # Record generated state only. Preview registry and production paths remain unchanged.
 r['status']='generated'
 original_notes=r['notes'].split(' BATCH D CANDIDATE GENERATED ')[0]
 r['notes']=original_notes.replace('NO IMAGE GENERATED OR APPROVED','NO IMAGE APPROVED')+' BATCH D CANDIDATE GENERATED 2026-11-20; unselected, not approved. '+ident+' v01; SHA-256 '+c['sha256']+'; review '+str(OUT.relative_to(ROOT))+'/index.html. Native-grid authorship unproven; generator original and documented derived export preserved. No production assetPath or gameplay integration.'

# Node coverage is established from exact script references, not historical node names.
coverage=[]
for name,v in n['nodes'].items():
 keys=['scenes:'+v['scene']]
 if v.get('speaker') in ('pavilion_attendant','pavilion_presenter'):
  keys+=['scenes:'+v['scene']+'#portraitBackground','portraits:'+v['speaker']+':'+v.get('pose','idle')]
 coverage.append({'node':name,'requirements':keys,'missingRegistryRequirements':[k for k in keys if not record(k)]})
audit={'baseMain':'5134edb160afaa019e11f872a3b87d3b01b257b0','narrativeBlob':'857ffdf1bc9432cf4bbbfd7819f5f430a06d9036','reviewNodeCount':len(coverage),'activeChapter3Records':29,'alreadyApprovedRecordsReused':20,'remainingRecordsAtAudit':9,'excludedHistoricalRecords':65,'missingRegisteredRequirements':[],'reuseFindings':['20 approved active Chapter 3 images retain their exact bytes and preview entries.','service_exit serves two different humans at separate moments; one environment pair is sufficient.','backstage and exterior_exit are shared masters, not one image per ending.','Facilities Key, Family Photo, Red Swangline Stapler and Timing Clicker retain existing approved illustrations.','Visitor and machine voices require no new portrait IDs under docs/111.','Zero new Focus A, inventory or fatal ending art.'],'narrativeStateQuestions':[{'node':'stapler_printer_snarl','existingRecord':'scenes:pavilion_reboot/record_printer','finding':'Paper feeds back into printer and maintenance shutter opens; current approved master does not establish a visibly jammed state. Node permits narration-only event staging. No separate state brief is registered.','recommendation':'Reuse approved master for this batch; Nate to decide whether a separately scoped masked state overlay is needed. Do not regenerate approved printer.'},{'node':'record_scanner_result','existingRecord':'scenes:pavilion_reboot/record_scanner','finding':'Same scene spans door-open feeding and door-closed completion. Dialogue/narration conveys transition; no additional static art requirement.'}],'candidates':candidates,'nodeCoverage':coverage}
savejson(OUT/'inventory.json',audit)
manifest={'schema':'out-of-order-art-review-v1','title':'Chapter 3 Batch D — v01','baseMain':audit['baseMain'],'narrativeBlob':audit['narrativeBlob'],'status':'generated','selected':False,'approved':False,'assetPath':None,'nativeGridAuthorship':'UNPROVEN. Immutable generator originals are larger raster images. Logical exports are documented nearest-neighbor transfers; no approved low-resolution image is enlarged and represented as new authorship.','candidates':candidates}
savejson(OUT/'manifest.json',manifest)
ART.write_text(json.dumps(a,indent=2,ensure_ascii=False)+'\n')

# Composite proofs: common shared background and every newly introduced context/pose pairing.
def candidate(idx):return Image.open(OUT/candidates[idx]['file']).convert('RGBA')
def ref(key):return Image.open(OUT/refs[key]['reviewFile']).convert('RGBA')
def composite(name,bg,fg,support=False):
 canvas=bg.copy();canvas.alpha_composite(fg)
 if support:
  # Shared service setting has no desk: a separate context-only foreground ledge supports seated waist.
  # It never alters the reusable portrait/background candidate. Both variants are shown for review.
  ImageDraw.Draw(canvas).polygon([(0,259),(563,259),(563,277),(0,277)],fill=(218,205,178,255))
 canvas.convert('RGB').save(OUT/'proofs'/name)
composite('service-presenter.png',candidate(1),candidate(3))
composite('service-attendant.png',candidate(1),candidate(2))
printer_bg=ref('scenes:pavilion_reboot/record_printer#portraitBackground')
printer=printer_bg.copy();printer.alpha_composite(candidate(2))
# Existing counter is in front of the lower waist: use its exact pixels as a foreground occluder.
printer.paste(printer_bg.crop((0,263,564,278)),(0,263))
printer.convert('RGB').save(OUT/'proofs/printer-attendant-quiet.png')
composite('courtesy-attendant-alarmed.png',candidate(8),ref('portraits:pavilion_attendant:alarmed'))

# Keep background geometry intact; context ledge above is a proof option only, never hidden in a candidate.
for c in candidates:
 images=[(c['candidateId'],OUT/c['file'])]+[(k,OUT/refs[k]['reviewFile']) for k in c['approvedDependencies'] if k in refs]
 sheet=Image.new('RGB',(700,325*len(images)),(28,36,42));d=ImageDraw.Draw(sheet)
 for row,(label,path) in enumerate(images):
  im=Image.open(path).convert('RGBA');scale=min(2,660/im.width,285/im.height)
  im=im.resize((round(im.width*scale),round(im.height*scale)),NEAR)
  d.text((15,row*325+8),label,fill='white');sheet.paste(im,(15,row*325+30),im)
 dest='proofs/'+c['candidateId']+'-comparison.png';sheet.save(OUT/dest);c['comparison']=dest
savejson(OUT/'manifest.json',manifest)
savejson(OUT/'inventory.json',audit)

# Technical diagnostics are descriptive; palette counts do not establish native authorship.
diagnostics=[]
for label,p in [(c['candidateId'],OUT/c['file']) for c in candidates]+[(k,OUT/v['reviewFile']) for k,v in refs.items() if k.startswith('scenes:')]:
 im=Image.open(p).convert('RGB');pix=list(im.getdata());w,h=im.size
 same=sum(pix[y*w+x]==pix[y*w+x-1] for y in range(h) for x in range(1,w))
 diagnostics.append({'id':label,'dimensions':[w,h],'uniqueColors':len(set(pix)),'horizontalEqualNeighborFraction':round(same/(h*(w-1)),4)})
savejson(OUT/'qa/pixel-density.json',{'interpretation':'Compare native clusters visually. Color/neighbor diagnostics are not a pass/fail aesthetic test. New source-derived exports can be softer or more finely shaded than prior selected art.','images':diagnostics})

rows=[]
for c in candidates:
 rows.append('| '+str(c['generationOrder'])+' | '+c['candidateId']+' | `'+c['record']+'` | '+record(c['record'])['kind']+' '+str(c['dimensions'][0])+'×'+str(c['dimensions'][1])+' | '+', '.join(c['sourceNodes'])+' | '+', '.join('`'+k+'`' for k in c['approvedDependencies'])+' | Yes: distinct scene/state/pose | '+c['constraints']+' |')
md='# Chapter 3 Batch D — audit and review\n\nAudited latest fetched main `'+audit['baseMain']+'` on 2026-11-20. Narrative blob `'+audit['narrativeBlob']+'` is unchanged. **Nine remaining active records: five main scenes, two portrait backgrounds, two foregrounds.** Twenty approved Chapter 3 records are reused; all 65 pre-reboot historical calls are excluded. All 34 review nodes map to registered scenes, poses and close backgrounds; no missing static artwork requirement is established.\n\n| Order | Artwork ID | Registry key | Type / dimensions | Review nodes | Approved dependencies | New generation? | Continuity constraints |\n| --- | --- | --- | --- | --- | --- | --- | --- |\n'+'\n'.join(rows)+'\n\nFull node coverage, exact prompts, source originals, derivations and hashes: [inventory.json](inventory.json), [manifest.json](manifest.json), [generation receipts](generation-receipts-final.json).\n\nNo new item, visitor portrait, death or Focus A images. Existing key/photo/stapler/clicker art is reused. Service exit, backstage and exterior each support multiple nodes without redundant generation.\n\n`stapler_printer_snarl` has a narrated printer loop and opening maintenance shutter, but no separate state brief. Reuse the approved printer master; Nate should decide whether a separately scoped masked overlay would improve it. `record_scanner_result` likewise narrates its door transition using the approved master. Neither finding authorizes redrawing approved art.\n\nAll candidates remain **generated / unselected**. Generator originals are larger rasters; original native-grid authorship is **unproven**. The logical images are nearest-neighbor source-derived exports, and 4× previews are exact nearest-neighbor enlargements of those exports. Approved images are never represented as freshly generated higher-resolution art. The two courtesy variants retain exact approved pixels outside explicit state masks.\n\nThe original seated attendant cut floated at the service door. A generated lower-torso correction extends it to the canvas edge, preserving the upper portrait pixels; both corrected service and printer composites are shown for review.\n\nVisual review questions and known limitations are shown per candidate in the gallery; technical passing does not constitute creative approval.\n'
(OUT/'README.md').write_text(md)

esc=html.escape
cards=[]
composites={1:['service-presenter.png','service-attendant.png'],2:['printer-attendant-quiet.png','service-attendant.png'],3:['service-presenter.png'],8:['courtesy-attendant-alarmed.png']}
for i,c in enumerate(candidates):
 extra=''.join('<figure><img src="proofs/'+f+'" width="564" height="278"><figcaption>'+esc(f)+'</figcaption></figure>' for f in composites.get(i,[]))
 cards.append('<article id="'+c['candidateId']+'"><h2>'+esc(c['candidateId'])+'</h2><p><code>'+esc(c['record'])+'</code> · generated / unselected · '+str(c['dimensions'][0])+'×'+str(c['dimensions'][1])+'</p><p>'+esc(c['constraints'])+'</p><h3>Native size</h3><figure class="checker"><img class="native" src="'+c['file']+'" width="'+str(c['dimensions'][0])+'" height="'+str(c['dimensions'][1])+'"></figure><details><summary>Exact 4× nearest-neighbor preview</summary><div class="scroll"><img class="preview4x" src="'+c['preview4x']+'" width="'+str(c['dimensions'][0]*4)+'" height="'+str(c['dimensions'][1]*4)+'"></div></details>'+extra+'<details><summary>Approved continuity comparisons</summary><img class="comparison" src="'+c['comparison']+'"></details><details><summary>Prompt, original and derived export provenance</summary><p><a href="'+c['prompt']+'">Full generation prompt</a> · <a href="'+c['source']['original']+'">Immutable generator original</a></p><pre>'+esc(json.dumps(c['operations'],indent=2))+'</pre></details><p>SHA-256 <code>'+c['sha256']+'</code></p><p>'+esc(c['mode']+'; '+c['opacity'])+'; partial-alpha pixels: '+str(c['alphaValidation']['partial'])+'</p><p class="question">Review: '+esc(' '.join(c['knownLimitations']))+'</p></article>')
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Out of Order — Chapter 3 Batch D</title><style>body{background:#18242a;color:#eee6d6;font:16px/1.5 system-ui;margin:0 auto;max-width:1200px;padding:28px}a{color:#9de0d7}article{border-top:2px solid #587878;margin-top:32px;padding-top:20px}h1,h2,h3{line-height:1.2}code,pre{overflow-wrap:anywhere;white-space:pre-wrap}figure{margin:12px 0;width:fit-content;max-width:100%;overflow:auto}img{image-rendering:pixelated;vertical-align:top}.native,.preview4x{max-width:none}.comparison{max-width:100%;height:auto}.checker{background:repeating-conic-gradient(#536064 0 25%,#334249 0 50%) 50%/16px 16px}.scroll{max-width:100%;overflow:auto}summary{cursor:pointer;padding:12px;background:#26383f}details{margin:10px 0}.question{border-left:4px solid #dba46f;padding:12px;background:#2c3333}nav a{display:inline-block;margin:6px 12px 6px 0}</style></head><body><h1>Out of Order — Chapter 3 Batch D</h1><p><strong>v01 · generated / unselected · Nate’s Art Director review required</strong></p><p>9 candidates: 5 main scenes (314×206), 2 independent close backgrounds and 2 transparent poses (564×278). No approval, gameplay import, narrative change or deployment from this branch.</p><p>Generator originals are larger rasters. Original native-grid authorship is <strong>unproven</strong>; logical exports are documented source-derived nearest-neighbor transfers. Source softness remains. Native images below are displayed at exact pixel size; 4× views scroll without responsive downscaling.</p><p><a href="README.md">Batch inventory</a> · <a href="inventory.json">34-node audit</a> · <a href="manifest.json">Candidate manifest and hashes</a> · <a href="qa/pixel-density.json">Chapters 1–3 pixel diagnostics</a> · <a href="qa/results.json">Technical QA</a> · <a href="qa/browser-results.json">Browser QA</a> · <a href="SHA256SUMS.txt">All package hashes</a></p><p class="question">Review priorities: service-exit camera correspondence; attendant lower-torso anchoring in both contexts; exact character identities; backstage EXIT geometry; vestibule ramp versus steps; courtesy frame movement, track clearance, shutter and cropped close view. Printer jam state remains a separate scope question.</p><nav>'''+''.join('<a href="#'+c['candidateId']+'">'+c['candidateId']+'</a>' for c in candidates)+'</nav>'+''.join(cards)+'</body></html>'
stylekeys=['scenes:exposition/reception','scenes:house_of_tomorrow/foyer','scenes:biology_park/conveniences_bureau','scenes:pavilion_reboot/restroom_entrance','scenes:pavilion_reboot/human_verification_stage']
style='<h2>Approved style and pixel density — Chapters 1–3</h2>'+''.join('<figure><img src="'+refs[k]['reviewFile']+'" width="314" height="206"><figcaption>'+esc(k)+'</figcaption></figure>' for k in stylekeys)
page=page.replace('<nav>',style+'<nav>')
(OUT/'index.html').write_text(page)
print('Produced nine derived candidates, exact 4x previews, state masks, original references, composites and inventory.')
