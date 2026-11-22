from pathlib import Path
from PIL import Image
import json,hashlib,subprocess
B=Path(__file__).resolve().parent;R=B.parents[5];BASE='d9b6b91604b72115c5402253f00924665e957727';SRC='d1600a34a58497b4886518c6aa9feeaa205d8426';KEY='scenes:pavilion_reboot/paper_emergency';NEW='93a48082124600b1afeb45e5ea54856bf253e858e55111295e9d9c26919bc978';OLD='ac0f7c44d267dd54897507ae3b8b02959a5b76f4fcd9d0418b77b8fdb777ba7e';SOURCE_PATH='tools/prologue-art-lab/assets/review/chapter-03-native-pilot-2026-11-21/v04-paper-emergency-localized-repair/candidate/CH3-B06-paper-emergency-local-v04.png'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();blob=lambda commit,path:subprocess.check_output(['git','-C',str(R),'rev-parse',commit+':'+path],text=True).strip()
preview=json.loads((R/'story/artwork-preview.json').read_text())['images'][KEY];catalog=json.loads((R/'story/artwork.draft.json').read_text())['scenes']['pavilion_reboot/paper_emergency'];assert preview['sha256']==OLD and catalog['status']=='approved' and catalog['assetPath']is None
quote="Nate has explicitly approved and selected **Paper Emergency v04**."
(B/'OWNER_SELECTION_VERBATIM.txt').write_text('''# Out of Order — Chapter 3 Artwork PMO Handoff

Nate has explicitly approved and selected **Paper Emergency v04**.

Proceed with the selection documentation and Claude registration handoff, then begin the Surprise Stage quality assessment.

Selected candidate:
- Record: `scenes:pavilion_reboot/paper_emergency`
- Version: v04 localized repair
- Source commit: `d1600a34a58497b4886518c6aa9feeaa205d8426`
- SHA-256: `93a48082124600b1afeb45e5ea54856bf253e858e55111295e9d9c26919bc978`

Previously approved B06 v03:
- SHA-256: `ac0f7c44d267dd54897507ae3b8b02959a5b76f4fcd9d0418b77b8fdb777ba7e`

The existing canonical registry must continue to reflect v03 until the separate Claude registration step replaces its preview bytes and updates the record notes.

Do not perform that registration yourself.
''')
source={'repo':'InterstellarHarvest/CYOA-storyboard','ref':'art/ch3-native-pilot-20261121','commit':SRC,'path':SOURCE_PATH}
batch={'about':'Exactly one Nate-selected, owner-approved Paper Emergency v04. Independently verify expectedSha256 and expectedPreviousSha256 before register-art.mjs. This batch does not authorize Codex to register or anyone to integrate/merge/deploy.','entries':[{'key':KEY,'file':SOURCE_PATH,'status':'approved','expectedSha256':NEW,'expectedPreviousSha256':OLD,'source':source}]};(B/'registration-batch.json').write_text(json.dumps(batch,indent=2))
notes='IMAGE OWNER-APPROVED 2026-11-22 (Nate, explicit Paper Emergency v04 selection): exact selected bytes InterstellarHarvest/CYOA-storyboard@art/ch3-native-pilot-20261121 '+SRC+', path '+SOURCE_PATH+'; SHA-256 '+NEW+'. This v04 localized repair supersedes current B06 v03 ('+OLD+'), whose original approval, exact bytes and provenance are retained in the selection manifest and preserved source. Original full-scene native-grid authorship remains unresolved/unproven and the accepted source-derived limitation is retained. Approved, not integrated; production assetPath remains null. Historical v04 gallery labels generated/unselected are preserved as time-of-review provenance and are superseded by this later owner selection.\n\nHISTORICAL V03 APPROVAL (superseded as current selection; record preserved): '+catalog['notes']
manifest={'schema':'out-of-order-paper-emergency-v04-owner-selection-v1','date':'2026-11-22','timezone':'America/New_York','owner':'Nate, Story and Creative Director / Art Director','ownerSelectionVerbatim':quote,'ownerSelectionExcerptFile':'OWNER_SELECTION_VERBATIM.txt','ownerSelectionExcerptSha256':sha(B/'OWNER_SELECTION_VERBATIM.txt'),'record':KEY,'selectedVersion':'v04 localized repair','status':'approved','selected':True,'approved':True,'creativeApprovalComplete':True,'canonicalRegistrationPerformed':False,'gameplayIntegrationAuthorized':False,'mergeAuthorized':False,'pagesDeploymentAuthorized':False,'productionAssetPath':None,'source':source,'selectedFile':{'file':'selected/CH3-B06-paper-emergency-local-v04.png','sha256':NEW,'gitBlobAtSourceCommit':blob(SRC,SOURCE_PATH),'dimensions':[314,206],'mode':'RGB','alpha':'opaque','bitDepth':8},'verifiedCanonicalMain':BASE,'currentCanonicalPreview':preview,'supersedes':{'version':'B06 v03','status':'historically approved; superseded as current creative selection by v04','sha256':OLD,'source':preview['source'],'preservedFile':'preserved/CH3-B06-paper-emergency-approved-v03.png','canonicalGitBlobAtVerifiedMain':blob(BASE,preview['file']),'approvalHistoryDocuments':['docs/113_CH3_BATCH_B_SELECTED_ARTWORK_20261119.json','docs/103_RETROACTIVE_ARTWORK_APPROVAL_LEDGER.md']},'supersessionRule':'v04 is the selected approved artwork for this record. The canonical registry/preview intentionally remain v03 until the separate Claude registration step. Never downgrade or relabel the old v03 approval as unapproved.','nativeGridAuthorship':'Original full-scene native-grid authorship remains unresolved/unproven. Native coordinate repairs do not prove inherited scene authorship. The accepted source-derived limitation is retained for the exact selected bytes.','historicalPackageRule':'Do not modify any v01–v04 review package or its generated/unselected labels. This later immutable owner-selection record supersedes those labels for the selected v04 file.','registrationBatch':'registration-batch.json','approvalLedgerAddendum':'APPROVAL_LEDGER_ADDENDUM.md','handoff':'CLAUDE_REGISTRATION_HANDOFF.md','notesUpdateForClaude':'future-record-notes.txt','existingLedgerSha256':sha(R/'docs/103_RETROACTIVE_ARTWORK_APPROVAL_LEDGER.md'),'existingCatalogSha256':sha(R/'story/artwork.draft.json'),'existingPreviewRegistrySha256':sha(R/'story/artwork-preview.json')};(B/'selection-manifest.json').write_text(json.dumps(manifest,indent=2));(B/'future-record-notes.txt').write_text(notes+'\n')
ledger='''# Paper Emergency v04 approval ledger addendum

Owner decision, November 22, 2026: **Nate has explicitly approved and selected Paper Emergency v04.** Selection is creative approval complete; no second visual approval is required for these exact bytes.

- Record: `'''+KEY+'''`
- Selected version: **v04 localized repair**
- Source repository and branch: `InterstellarHarvest/CYOA-storyboard`, `art/ch3-native-pilot-20261121`
- Immutable source commit: `'''+SRC+'''`
- Source path: `'''+SOURCE_PATH+'''`
- Selected SHA-256: `'''+NEW+'''`
- Native contract: **314×206 RGB, opaque, 8-bit**
- Status of exact selected artwork: **approved, not integrated**; production `assetPath` remains null.

## Superseded approval preserved

V04 supersedes the previously approved B06 v03 for the same record. V03 remains historically approved, with its unchanged original provenance at `7337e5e550e64a64357666a0fab6f118500913cd`, branch `art/ch3-pavilion-batch02-20261119`, source path `tools/prologue-art-lab/assets/review/chapter-03-batch02-2026-11-19/v03-localized-corrections/candidates/CH3-B06-paper-emergency-v03.png`.

Previous SHA-256: `'''+OLD+'''`. Its exact bytes are preserved at `preserved/CH3-B06-paper-emergency-approved-v03.png` and independently match the original source-commit download. Earlier approval records and every review snapshot stay immutable.

## Accepted limitation and administrative state

Original full-scene native-grid authorship remains unresolved/unproven. The source-derived softness limitation is retained and accepted for these exact selected bytes; the localized repairs do not establish inherited scene authorship.

The existing canonical registry and preview intentionally continue to identify v03 until Claude performs the separately authorized registration step. This is an administrative backlog, not pending creative approval of v04. Historical generated/unselected labels in the immutable v04 gallery are time-of-review provenance and are superseded by this later owner decision.

This is a standalone immutable ledger addendum. The existing `docs/103_RETROACTIVE_ARTWORK_APPROVAL_LEDGER.md` is unchanged in this Codex task. Claude may append this addendum once during the separate registration task, preserving every prior byte and all other approvals. Do not edit or relabel historical ledger entries.

No gameplay integration, production-path invention, other Chapter 3 approval change, main merge or public Pages deployment is authorized by this receipt.
''';(B/'APPROVAL_LEDGER_ADDENDUM.md').write_text(ledger)
# Native and exact 4x selection-history comparison, copied approved bytes only.
for name,file in [('previous-approved-v03','preserved/CH3-B06-paper-emergency-approved-v03.png'),('selected-approved-v04','selected/CH3-B06-paper-emergency-local-v04.png')]:Image.open(B/file).resize((1256,824),Image.Resampling.NEAREST).save(B/(name+'-4x.png'))
o=Image.open(B/'preserved/CH3-B06-paper-emergency-approved-v03.png');n=Image.open(B/'selected/CH3-B06-paper-emergency-local-v04.png');pair=Image.new('RGB',(628,206));pair.paste(o,(0,0));pair.paste(n,(314,0));pair.save(B/'previous-v03-left-selected-v04-right-native.png');pair.resize((2512,824),Image.Resampling.NEAREST).save(B/'previous-v03-left-selected-v04-right-4x.png')
print('Owner-approved selection receipt, standalone ledger addendum and exact one-record batch prepared. Registry remains v03.')
