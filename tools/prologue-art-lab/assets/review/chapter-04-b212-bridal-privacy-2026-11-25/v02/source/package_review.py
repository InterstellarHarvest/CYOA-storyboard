from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,html
ROOT=Path(__file__).resolve().parents[1]
BASE='1261658ed882bff7340405e91f5d44f4e5404012'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(f):
 im=Image.open(ROOT/f);return {'file':f,'sha256':sha(ROOT/f),'dimensions':list(im.size),'mode':im.mode}
def four(f):
 im=Image.open(ROOT/f);p='previews/'+Path(f).stem+'-4x.png';im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/p);return p
def main():
 locked='native/CH4-NEW-07-focus-locked-v02.png';provisional='native/CH4-NEW-07-focus-provisional-v02.png'
 references=['references/approved-inspect-locked.png','references/approved-inspect-provisional.png','references/approved-dressing-room.png','references/ch2-exposure-dispenser.png','references/ch2-aid-box.png','references/ch2-bureau.png']
 for f in references:four(f)
 font=ImageFont.load_default(size=13);layouts=[]
 def sheet(name,items):
  sizes=[Image.open(ROOT/f).size for label,f in items];ws=[max(w+20,int(font.getlength(label))+20)for(label,f),(w,h)in zip(items,sizes)]
  im=Image.new('RGB',(sum(ws)+8,max(h for w,h in sizes)+50),'#263a32');d=ImageDraw.Draw(im);x=8
  for(label,f),w in zip(items,ws):
   d.text((x+6,9),label,font=font,fill='#f0e2bd');im.paste(Image.open(ROOT/f).convert('RGB'),(x+6,40));layouts.append({'caption':label,'fits':font.getlength(label)<=w-12});x+=w
  p='comparisons/'+name+'-native.png';im.save(ROOT/p);four(p)
 sheet('focus-states',[('LOCKED Focus - UNSELECTED',locked),('PROVISIONAL Focus - UNSELECTED',provisional)])
 sheet('locked-focus-approved-inspect',[('564x278 new Focus - UNSELECTED',locked),('565x451 approved INSPECT - EXACT','references/approved-inspect-locked.png')])
 sheet('provisional-focus-approved-inspect',[('564x278 new Focus - UNSELECTED',provisional),('565x451 approved INSPECT - EXACT','references/approved-inspect-provisional.png')])
 sheet('chapter2-focus-benchmarks',[('New Focus - UNSELECTED',locked),('Approved Ch2 Exposure Dispenser','references/ch2-exposure-dispenser.png'),('Approved Ch2 Aid Box','references/ch2-aid-box.png')])
 sheet('wainscot-correction',[('Pre-correction diagnostic - NOT current','diagnostics/pre-wainscot-correction-locked-NOT-current.png'),('Rail BELOW panel and shadow',locked)])
 sheet('source-diagnostic-native',[('Source-derived diagnostic - NOT production','diagnostics/wide-source-derived-diagnostic-NOT-production.png'),('Native structural interpretation',locked)])
 (ROOT/'evidence/comparison-layout.json').write_text(json.dumps(layouts,indent=2)+'\n')
 owner=[]
 for src,copy,id,role in [('native/CH4-NEW-07-bridal-privacy-panel-v01.png',references[0],'CH4-NEW-07-inspect-locked','Approved detailed INSPECT'),('native/CH4-NEW-07-provisional-authorized-v01.png',references[1],'CH4-NEW-07-inspect-provisional','Approved detailed INSPECT'),('native/CH4-NEW-01-bridal-dressing-room-v01.png',references[2],'CH4-NEW-01','Approved dressing room')]:
  owner.append({'id':id,'status':'APPROVED','ownerApproved':True,'approvedUnchanged':True,'approvalAuthority':'OWNER-DIRECTION.md; Nate explicit approval','sourceCommit':BASE,'sourcePath':ROOT.parent.relative_to(next(p for p in ROOT.parents if(p/'story/artwork.draft.json').exists())).as_posix()+'/v01/'+src,'referenceCopy':rec(copy),'role':role,'canonicalRegistrationPerformed':False})
 (ROOT/'evidence/owner-approval-preservation.json').write_text(json.dumps({'note':'Records explicit approval here without rewriting historical review manifests or canonical registration. v01 remains exact. New widescreen candidates are unselected.','assets':owner},indent=2)+'\n')
 states=[]
 for name,f in [('locked',locked),('provisionally authorized',provisional)]:states.append({'state':name,'status':'UNSELECTED','ownerApproved':False,'selected':False,'native':rec(f),'exact4x':rec('previews/'+Path(f).stem+'-4x.png'),'runtimeBinding':None,'newFocusId':None,'newFlag':None})
 manifest={'title':'B2-12 v02 - widescreen Focus / approved INSPECT','branch':'art/ch4-b212-bridal-privacy-review-20261125','preservationBaseline':BASE,'newArtworkStatus':'UNSELECTED','ownerApproved':False,'logicalFocusAsset':'CH4-NEW-07','existingCanonicalFocusIdentifier':'grand_bellevue/bridal_privacy_panel','existingStoryNode':'hotel_bridal_door_focus','widescreenStates':states,'approvedPreservedReferences':owner,'sourceDerived':True,'whollyIndependentNativeAuthorship':False,'method':'Source-informed native material fields plus separately drawn final-grid door/jamb, plaster extension, wainscot, conduit, lamp, full brass plate, camera optics, policy badges, physical button and native bitmap lettering. No approved square image was resized/cropped/recolored into a new asset.','source':'originals/widescreen-detailed-reference.png','sourcePrompt':'source/widescreen-reference-prompt.txt','layers':'evidence/native-layer-recipes.json','gameplayHandoff':'ENGINEERING-HANDOFF.md','inspectionBehaviorImplemented':False,'storyChoicesModified':False,'canonicalMainModified':False,'productionSelectionsModified':False,'ownerCorrection':'Wainscot rail moved below the plate AND its cast shadow, identically in both states.'}
 (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 provenance={'tool':'Built-in image_gen.imagegen','generationDate':'2026-11-25','source':rec('originals/widescreen-detailed-reference.png'),'prompt':'source/widescreen-reference-prompt.txt','promptSha256':sha(ROOT/'source/widescreen-reference-prompt.txt'),'referenceInputs':[rec('references/approved-inspect-locked.png'),rec('references/approved-dressing-room.png'),rec('references/ch2-exposure-dispenser.png')],'referenceRoles':['Panel identity only; immutable approved PNG','Approved room architecture/material continuity; immutable PNG','Approved Chapter2 pixel-art material benchmark; immutable PNG'],'sourceDerived':True,'whollyIndependentNativeAuthorship':False,'noApprovedImageUsedAsResizedProductionLayer':True,'nativeRecipe':'source/build_native.py','reusedCodeOnly':'source/native_support.py extracted from frozen v01 source; no approved image processing or calls to its old artwork builders','scope':'One new composition / two localized states. No regeneration of approved artwork.'}
 (ROOT/'evidence/generation-provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
 def fig(title,f):
  im=Image.open(ROOT/f);p='previews/'+Path(f).stem+'-4x.png'
  return f'<section class="figure"><h3>{html.escape(title)}</h3><nav><button data-scale="1">Native 1×</button><button data-scale="4">Exact 4×</button><a href="{f}">Native PNG</a><a href="{p}">4× PNG</a></nav><div class="raster"><img src="{f}" data-one="{f}" data-four="{p}" data-w="{im.width}" data-h="{im.height}" width="{im.width}" height="{im.height}" alt="{html.escape(title)}"></div></section>'
 css='body{margin:0;background:#172a23;color:#efe5c8;font:16px/1.55 system-ui,sans-serif}main{padding:22px}header,article{padding:20px;border:1px solid #697c6d;margin-bottom:26px}h1,h2,h3{margin:0 0 12px}a{color:#c5dfca;margin-right:14px}nav{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0}button{padding:10px;background:#435e4d;border:1px solid #bacbaa;color:#fff0ca;cursor:pointer}.figure{padding:14px;margin:20px 0;background:#294136}.raster{overflow:auto;max-width:100%;background:#253b32}.raster img{display:block;max-width:none!important;image-rendering:pixelated}p{max-width:1100px}'
 head='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>B2-12 v02 · Focus and INSPECT</title><style>'+css+'</style><main><header><h1>B2-12 v02 · Widescreen Focus + approved INSPECT</h1><p><strong>New564×278 widescreen views: UNSELECTED.</strong> Existing565×451 INSPECT views and314×206 dressing room: APPROVED, exact unchanged bytes. Approval registration and engine integration are separate.</p><p>One native composition: closed handle-less door on the left, same brass camera/CRT privacy system, warm wall lamp and restrained associated service conduit on the right. Panel and its shadow are entirely above the wainscot rail. Locked/provisional states change only screen and LED pixels.</p><p>The large reference guided material and light; native forms, profiles, hardware and pixel lettering are separately constructed. Honest SOURCE-DERIVED provenance is preserved. 4× views are exact nearest-neighbor exports at full integer sizes; wide sheets scroll horizontally.</p><nav><a href="#focus-locked">Locked Focus</a><a href="#focus-provisional">Provisional Focus</a><a href="#inspect-locked">Approved INSPECT</a><a href="#comparisons">Comparisons</a><a href="#benchmarks">Chapter2</a><a href="manifest.json">Manifest / hashes</a><a href="ENGINEERING-HANDOFF.md">Engineering handoff</a><a href="evidence/validation.json">QA</a><a href="README.md">Method</a><a href="source/widescreen-reference-prompt.txt">Exact prompt</a><a href="originals/widescreen-detailed-reference.png">Detailed source</a></nav></header>'
 body=''
 for id,title,f in [('focus-locked','New LOCKED Focus · UNSELECTED',locked),('focus-provisional','New PROVISIONAL Focus · UNSELECTED',provisional),('inspect-locked','Approved LOCKED INSPECT · exact v01 PNG',references[0]),('inspect-provisional','Approved PROVISIONAL INSPECT · exact v01 PNG',references[1]),('approved-room','Approved dressing room · unchanged',references[2])]:body+='<article id="'+id+'"><h2>'+title+'</h2>'+fig(title,f)+'</article>'
 body+='<article id="comparisons"><h2>Native / exact4× comparisons</h2>'
 for name,title in [('focus-states','Matching wide Focus states'),('locked-focus-approved-inspect','Locked Focus / approved INSPECT'),('provisional-focus-approved-inspect','Provisional Focus / approved INSPECT'),('chapter2-focus-benchmarks','Same-class approved Chapter2 benchmarks'),('wainscot-correction','Targeted wainscot correction'),('source-diagnostic-native','Diagnostic source / native structural interpretation')]:body+=fig(title,'comparisons/'+name+'-native.png')
 body+='</article><article id="benchmarks"><h2>Approved Chapter2 artwork · original native sizes</h2>'
 for f in references[3:]:body+=fig(Path(f).stem,f)
 body+='</article>'
 script='<script>document.querySelectorAll("button[data-scale]").forEach(b=>b.onclick=()=>{const i=b.closest("section.figure").querySelector("img"),s=Number(b.dataset.scale);i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;});</script></main></html>'
 (ROOT/'index.html').write_text(head+body+script)
 print(json.dumps({'newFocusStates':2,'approvedImagesPreserved':3,'newCandidatesStatus':'UNSELECTED'}))
if __name__=='__main__':main()
