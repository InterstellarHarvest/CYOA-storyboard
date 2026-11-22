"""Build the one consolidated native/exact-4x review gallery."""
from pathlib import Path
from PIL import Image
from html import escape as E
import base64
import json
import re

B=Path(__file__).resolve().parent
M=json.loads((B/'manifest.json').read_text())
F=json.loads((B/'assessment/scene-findings.json').read_text())
matrix=json.loads((B/'chapter-03-completion-matrix.json').read_text())
portraits=json.loads((B/'assessment/portrait-composite-findings.json').read_text())
alternatives=json.loads((B/'assessment/unselected-alternatives.json').read_text())
refs=json.loads((B/'sources/cross-chapter-references.json').read_text())
order=M['newDetailedAssessments']+[s['key'].split('/')[-1]for s in matrix if s['key'].split('/')[-1]not in M['newDetailedAssessments']]
css='''*{box-sizing:border-box}body{margin:0;background:#f1eee6;color:#293d43;font:16px/1.6 system-ui,sans-serif}main{max-width:1440px;margin:auto;padding:30px}h1{font-size:36px;line-height:1.2}h2{line-height:1.3}p{max-width:1140px}a{color:#17616d}.notice{background:#e2ece3;padding:18px;border-left:5px solid #367c6c}.scroll{overflow:auto;padding-bottom:16px}.pair{display:flex;gap:22px;width:max-content}figure{margin:0;flex:none}figcaption{font-size:13px;padding:6px 0;max-width:650px}img{display:block;max-width:none;image-rendering:pixelated}summary{cursor:pointer;font-weight:650;padding:10px 0}code{font-size:12px;overflow-wrap:anywhere}.facts{background:#eef0e8;padding:14px;font-size:13px;overflow-wrap:anywhere}button{font:inherit;padding:6px 12px}section{background:#fffdf8;padding:22px;border:1px solid #c9d2ca;margin:24px 0;border-radius:6px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:10px}table{width:100%;min-width:850px;border-collapse:collapse}th,td{text-align:left;padding:10px 8px;border-bottom:1px solid #cad3cc;vertical-align:top;font-size:14px}nav{position:sticky;top:0;z-index:2;background:#f1eee6;padding:10px 0;border-bottom:1px solid #c9d2ca}section{scroll-margin-top:70px}.tag{font-size:12px;color:#37675d}li{margin-bottom:5px}@media(max-width:700px){main{padding:14px}h1{font-size:28px}section{padding:14px}}'''
def image(p,label):
    im=Image.open(B/p);w,h=im.size
    return f'<figure><figcaption>{E(label)} · {w}×{h}</figcaption><img src="{E(p)}" width="{w}" height="{h}" alt="{E(label)}" loading="eager"></figure>'
def single(p,label):return '<div class="scroll">'+image(p,label)+'</div>'
def pair(a,b,la,lb):return '<div class="scroll"><div class="pair">'+image(a,la)+image(b,lb)+'</div></div>'
def four(body,label='Exact nearest-neighbor 4× views'):
    return '<details class="four"><summary>'+E(label)+'</summary>'+body+'</details>'
def title(n):return n.replace('_',' ').title()
def paragraph(label,text):return '<p><strong>'+E(label)+':</strong> '+E(text)+'</p>'

h=[f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Out of Order · Chapter 3 consolidated artwork quality review</title><style>{css}</style><main>',
   '<p>OUT OF ORDER · CHAPTER 3 · CONSOLIDATED ART DIRECTOR REVIEW · NOVEMBER 22, 2026</p><h1>Chapter 3 artwork quality review</h1>',
   '<p><strong>The scene should look like good pixel art from a distance. The portrait should reward you for looking closer.</strong><br>Maximum useful detail, minimum unnecessary pixel noise.</p>',
   '<div class="notice"><strong>Six remaining scenes: KEEP.</strong> No new unambiguous defect warrants a repair candidate. <strong>Zero artwork or portrait pixels changed.</strong> All 14 scene records are covered; 15 approved portrait/background pairings cover all 20 dialogue nodes. Exit Vestibule’s earlier UNCERTAIN route reading is resolved to KEEP. No required manual touchup is demonstrated.<p><strong>Paper Emergency:</strong> Nate-selected v04 remains approved. Its registration is implemented on <a href="https://github.com/InterstellarHarvest/CYOA-storyboard/pull/18">draft PR #18</a>, open and unmerged. Canonical main still shows v03. This review performs no registration, merge or deployment.</p></div>',
   '<nav><a href="#matrix">14-scene matrix</a> · <a href="#six">Six new assessments</a> · <a href="#vestibule">Vestibule resolution</a> · <a href="#continuity">Continuity</a> · <a href="#portraits">Portraits</a> · <a href="#qa">Evidence / QA</a></nav>',
   '<p><button id="expand" type="button">Open exact 4× views</button> <button id="collapse" type="button">Close enlarged views</button></p>',
   '<section id="matrix"><h2>14-scene completion matrix</h2><p>These are review recommendations, not changes to catalogue approvals. Thirteen approved canonical masters are retained; Paper v03 is superseded creatively by the selected v04, awaiting the separate PR decision. Every scene has a closed zero-pixel repair mask. <a href="chapter-03-completion-matrix.json">Full JSON with exact source paths/hashes</a> · <a href="chapter-03-completion-matrix.csv">CSV</a> · <a href="chapter-03-completion-matrix.md">Readable complete matrix</a></p><div class="scroll"><table><thead><tr><th>Scene / baseline</th><th>Recommendation</th><th>Perspective / consistency</th><th>Alternatives / outstanding action</th></tr></thead><tbody>']
for row in matrix:
    n=row['key'].split('/')[-1]
    action='No required manual touchup.'
    if row['unselectedAlternatives']:action='Historical alternatives remain unselected; see below. No required touchup.'
    if n=='paper_emergency':action='Selected v04 published; registration implemented in draft PR #18, not merged. Canonical still v03.'
    h.append('<tr><td><a href="#scene-'+n+'">'+E(title(n))+'</a><br><span class="tag">'+E(row['scope'])+'</span><details><summary>Canonical source</summary><code>'+E(row['approvedVersion'])+'<br>'+row['canonicalSha256']+'<br>'+row['canonicalSource']['commit']+'</code></details></td><td><strong>'+E(row['recommendation'])+'</strong></td><td>Checked. '+E('Narrative route resolved.'if n=='exit_vestibule'else'Approved geometry and useful detail retained.')+'</td><td>'+E(action)+'</td></tr>')
h+=['</tbody></table></div><p>All existing statuses remain approved and production paths null. All '+str(M['priorTrackedFilesProtected'])+' prior tracked files remain unchanged. Original full-scene/native-grid authorship remains unresolved.</p></section>',
    '<section id="six"><h2>Six new assessments</h2><div class="grid">'+''.join('<a href="#scene-'+n+'">'+E(title(n))+' · KEEP</a>'for n in M['newDetailedAssessments'])+'</div><p>Each approved native source is shown before its diagnostic guide. Green outlines locate protected details; they are not rectangular character edits or paste masks. Cyan traces structure/depth; magenta marks support contacts. Guides are approximate visual traces, not recovered camera calibration. The original PNGs are byte-exact.</p></section>']
for n in order:
    f=F[n];row=next(r for r in matrix if r['key']==f['key']);source=next(s for s in M['sceneSources']if s['key']==f['key'])
    h+=['<section id="scene-'+n+'" class="scene" data-scene="'+n+'"><h2>'+E(title(n))+' · '+E(f['recommendation'])+'</h2><p class="tag">'+E(f['scope'])+' · original audit: '+E(f['initialRecommendation'])+'</p>',
        pair('approved/'+n+'.png','assessment/'+n+'-protected-native.png','Approved canonical native · unchanged','Protected-detail guide · diagnostic only'),
        four(pair('previews/'+n+'-4x.png','assessment/'+n+'-protected-4x.png','Approved canonical original · exact 4×','Protected guide · exact 4×')),
        '<p><a href="comparisons/'+n+'-approved-left-protected-right-native.png">Direct native comparison PNG</a> · <a href="comparisons/'+n+'-approved-left-protected-right-4x.png">Direct 4× comparison PNG</a> · <a href="masks/'+n+'-repair-mask.png">Closed 0-pixel repair mask</a></p>',
        paragraph('Useful detail / readability',f['detail']),paragraph('Mandatory perspective check',f['perspective']),paragraph('Narrative',f['narrative']),paragraph('Continuity',f['continuity']),
        '<p><strong>Protect:</strong> '+E('; '.join(f['protect']))+'.</p>',
        four(single('assessment/'+n+'-perspective-4x.png','Perspective and contact guide · exact 4×'),'Perspective construction guide at exact 4×')]
    if n in M['newDetailedAssessments']:
        h+=[single('assessment/'+n+'-focus-native.png','Unchanged approved focus crop · native'),four(single('assessment/'+n+'-focus-4x.png','Same focus crop · exact 4×'),'Focus detail at exact 4×')]
    if n=='paper_emergency':
        h+=[pair('approved/paper_emergency.png','references/paper-emergency-selected-v04.png','Canonical v03 · historical approval preserved','Nate-selected approved v04 · PR #18 unmerged'),four(single('previews/paper-emergency-selected-v04-4x.png','Nate-selected v04 · exact 4×'),'Selected v04 at exact 4×'),'<p>V04 changes 327 pixels in the prior localized repair package; this consolidated assessment changes none. Its earlier review labels remain immutable and are superseded by the later owner-selection receipt. No reapproval is requested.</p>']
    h+=['<details><summary>Exact baseline contract and source</summary><div class="facts"><strong>Key:</strong> <code>'+E(row['key'])+'</code><br><strong>Canonical SHA-256:</strong> <code>'+row['canonicalSha256']+'</code><br><strong>Source commit:</strong> <code>'+row['canonicalSource']['commit']+'</code><br><strong>Source path:</strong> <code>'+E(row['canonicalSource']['path'])+'</code><br><strong>Dimensions / opacity:</strong> 314×206 opaque RGB. 4×: 1256×824.<br><strong>Unique RGB:</strong> '+str(source['metrics']['uniqueRGB'])+'; descriptive only, no target.<br><strong>New repair:</strong> none. Artwork pixels changed: 0.</div></details></section>']

h+=['<section id="vestibule"><h2>Exit Vestibule: UNCERTAIN → KEEP</h2><p>The previous concern was whether the two-part image accidentally offers a second restroom entrance. The locked sequence resolves the intended reading: enter the exit vestibule, see fixtures through a blocking inner gate, then descend via automatic exit assistance. The visible EXIT arrow and lower ramp support that route. The maintenance worker appears at the later destination, not necessarily in this frame.</p>',
    single('assessment/exit-vestibule-route-interpretation.png','Semantic route interpretation · not a measured floor plan'),
    '<p><a href="assessment/exit-vestibule-resolution.json">Evidence and retained calibration limitation</a>. There is no recovered floor plan or compass orientation. That limitation does not demonstrate impossible topology or justify new geometry.</p></section>',
    '<section id="continuity"><h2>Stage, restroom and cross-chapter continuity</h2><p>Verification and Urgency were compared directly with the approved Surprise and Locomotion images above. Pavilion lettering is byte-identical in the tested shared sign crop; stage equipment and corrected wall planes remain consistent. Curtain state, platform height, microphone presence, bell, visitor and display changes are intentional narrative differences. No automatic sprite or equipment propagation.</p><p>Record Printer differs from A01 only in the bounded receipt region. Courtesy preserves every pixel at x≥180. This protects the desk layout, corrected microphone, attendant and right plant and prevents a newly introduced character-protection rectangle. Paper v04’s urgent gesture is a later state, not a template to copy into calm scenes.</p>',
    '<p>Reception sets the scene/portrait detail relationship. Chapter 2 permits rich foliage, reflections, equipment and material shading. Pavilion’s brighter theatrical coral/teal palette is coherent with those approved views. Its inherited softness remains visible; lower color counts are not a substitute for a demonstrated improvement.</p>']
for ref in refs:
    if ref['key']in ['scenes:exposition/reception#portraitBackground','portraits:receptionist:default#layers:foreground']:continue
    stem=Path(ref['reviewFile']).stem
    h+=[single(ref['reviewFile'],'Approved reference · '+ref['key']+' · native'),four(single('previews/'+stem+'-4x.png','Same approved reference · exact 4×'),'Reference at exact 4×')]
h+=[single('composites/reception-reference-native.png','Approved Reception portrait layers · diagnostic composite, unchanged'),four(single('composites/reception-reference-4x.png','Reception conversation pairing · exact 4×')),
    '<p><a href="assessment/cross-chapter-consistency.json">Full cross-chapter findings and limitations</a></p></section>',
    '<section id="portraits"><h2>All approved Chapter 3 conversation pairings</h2><p>15 unique combinations cover all 20 dialogue nodes. Each uses the exact approved 564×278 foreground/background canvases with no scaling, translation, portrait repaint or registration. Foreground occlusion is expected; bottom waist crops are not missing legs. The quiet attendant’s taller v02 proportions and close service/courtesy cameras were explicitly approved in Batch D and remain protected.</p>']
for p in portraits:
    h+=['<details class="portrait" data-pair="'+p['id']+'"><summary>'+E(p['scene']+' · '+p['portrait'])+'</summary><p>Nodes: '+E(', '.join(p['nodes']))+'. '+E(p['finding'])+'</p>',single(p['native'],'Diagnostic composite from unchanged approved layers · native'),four(single(p['fourX'],'Same approved-layer composite · exact 4×')),'<p><a href="'+p['backgroundFile']+'">Exact approved background</a> · <a href="'+p['foregroundFile']+'">Exact approved foreground</a></p></details>']
h+=['<p><a href="assessment/portrait-composite-findings.json">All layer hashes, alpha bounds, node coverage and findings</a></p></section>',
    '<section id="alternatives"><h2>Historical unselected alternatives remain unchanged</h2><p>The full-scene v01 reconstruction direction was withdrawn. The v02 six-pixel Locomotion presenter alternative remains unselected, with no approval implied by publication. Neither is a required next correction. Earlier snapshots and approvals are immutable.</p><ul>']
for a in alternatives:
    url='https://github.com/InterstellarHarvest/CYOA-storyboard/blob/'+M['startingReviewCommit']+'/'+a['file']
    h.append('<li><a href="'+url+'">'+E(a['key']+' · '+a['version'])+'</a> — '+E(a['status'])+'<br><code>'+a['sha256']+'</code></li>')
h+=['</ul><p><a href="assessment/unselected-alternatives.json">Exact alternative hashes and paths</a></p></section>',
    '<section id="qa"><h2>Preservation, provenance and actual QA</h2><p>'+E(M['nativeGridAuthorshipLimitation'])+'</p><div class="facts"><strong>Verified main:</strong> <code>'+M['verifiedMain']+'</code><br><strong>Starting review head:</strong> <code>'+M['startingReviewCommit']+'</code><br><strong>Existing files protected:</strong> '+str(M['priorTrackedFilesProtected'])+'<br><strong>New artwork candidates:</strong> 0<br><strong>New artwork/portrait pixel changes:</strong> 0<br><strong>Scene masks:</strong> 14 closed black masks, 0 repair pixels each.</div>',
    '<p><a href="manifest.json">Manifest and image metrics</a> · <a href="qa/preservation.json">Technical and byte-preservation proof</a> · <a href="qa/results.json">Checks run / not run</a> · <a href="qa/browser.json">Chromium/Firefox results</a> · <a href="assessment/scene-findings.json">Every scene finding</a> · <a href="assessment/guide-coordinates.json">Guide coordinates</a> · <a href="sources/scene-records.json">Exact prompts and narrative nodes</a> · <a href="sources/paper-pr18-snapshot.json">Read-only PR #18 snapshot</a> · <a href="sources/paper-v04-selection-receipt.json">Paper v04 owner-selection receipt</a></p>',
    '<p>Source artwork statuses, source bytes, production paths, narrative, gameplay, Chapter 4 and all earlier packages remain unchanged. No canonical registration, PR merge or Pages deployment occurred in this task.</p><p><strong>Stop for Nate’s consolidated Art Director review.</strong> The audit is complete as an assessment; these KEEP recommendations do not replace his visual review.</p></section></main><script>document.getElementById("expand").onclick=()=>document.querySelectorAll("details.four").forEach(d=>{d.open=true;let p=d.parentElement.closest("details");if(p)p.open=true});document.getElementById("collapse").onclick=()=>document.querySelectorAll("details").forEach(d=>d.open=false);</script></html>']
html='\n'.join(h);(B/'index.html').write_text(html)
(B/'standalone-gallery.html').write_text(re.sub(r'src="([^"]+)"',lambda v:'src="data:image/png;base64,'+base64.b64encode((B/v[1]).read_bytes()).decode()+'"',html))

md=['# Chapter 3 consolidated artwork quality review','',
    '**Six new assessments: KEEP all six. Zero artwork/portrait pixels changed; no new candidates.** Exit Vestibule’s route uncertainty resolves to KEEP. No genuinely necessary manual touchup is demonstrated. Stop for Nate’s consolidated Art Director review.','',
    '[Portable browser gallery](standalone-gallery.html) · [HTML gallery](index.html) · [14-scene matrix](chapter-03-completion-matrix.md) · [JSON](chapter-03-completion-matrix.json) · [CSV](chapter-03-completion-matrix.csv) · [Actual QA](qa/results.json)','',
    'Paper Emergency v04 remains Nate-selected/approved. Its exact registration is implemented on open, unmerged draft [PR #18](https://github.com/InterstellarHarvest/CYOA-storyboard/pull/18), head `3768b174e544600c3a88e3ae8b18c0fb35982ac4`. Canonical `main` still uses v03. Selected v04 bytes are already published on the review branch; no merge or public Pages publication is authorized.','',
    '## Six assessments and direct comparison PNGs','', '| Scene | Recommendation | Native comparison | Exact 4× comparison |','|---|---|---|---|']
for n in M['newDetailedAssessments']:
    md.append('| '+title(n)+' | KEEP | [PNG](comparisons/'+n+'-approved-left-protected-right-native.png) | [PNG](comparisons/'+n+'-approved-left-protected-right-4x.png) |')
md+=['','Each scene has an exact approved 314×206 original, 1256×824 nearest-neighbor preview, protected-detail and perspective/contact guides, narrative/continuity findings and a 0-pixel mask. All 14 masters are included for chapter-wide comparison. Guides are diagnostics, not altered artwork or edit regions.','',
     '## Key findings','',
     '- Preserve Pavilion signs/30, presenter identity, gestures, corrected right wall, green BEGIN and covered red release. Urgency’s red curtains/bell/visitor, Surprise’s two lamps/brighter green and Locomotion’s floor/net/microphone state remain distinct.',
     '- Preserve A01/B02 desk geometry, left cream feed unit, corrected microphone, attendant and right plant. Receipt direction is readable. Courtesy’s moved frame stays behind the bench; the desk half is pixel-identical to A01. No extra device or rectangular character patch is introduced.',
     '- Exit Vestibule shows denied fixtures left and automatic descending exit assistance right. The narrative and adjacent threshold views resolve the earlier route concern; no measured floor plan is claimed. [Route diagram](assessment/exit-vestibule-route-interpretation.png) · [Resolution evidence](assessment/exit-vestibule-resolution.json).',
     '- Reception and approved Chapter 2 references support useful environment detail and separate portrait detail. Inherited softness and larger palettes remain accepted limitations rather than automatic repaint instructions.',
     '- All 15 used portrait/background combinations (20 dialogue nodes) were checked. No obvious new alignment/silhouette/perspective defect. The quiet attendant’s taller v02 framing and close service/courtesy cameras remain protected. No portrait edits.','',
     '## History and limits','',
     'V01 Backstage/Locomotion reconstructions remain not selected; their direction is withdrawn. The six-pixel Locomotion v02 alternative remains generated/unselected. Paper v04 is selected, superseding historical v03 without erasing its earlier approval. [Alternative hashes](assessment/unselected-alternatives.json).','',
     M['nativeGridAuthorshipLimitation'],'',
     'All '+str(M['priorTrackedFilesProtected'])+' pre-existing tracked files remain unchanged. No canonical registration, gameplay/narrative/menu/Chapter 4 changes, merge or Pages deployment. [Preservation proof](qa/preservation.json) · [QA actually run/not run](qa/results.json).']
(B/'README.md').write_text('\n'.join(md)+'\n')

md=['# Chapter 3 complete scene-quality matrix','',
    'Canonical state checked against `main` `'+M['verifiedMain']+'`. All statuses stay approved; all production paths stay null. Review recommendations await Nate’s consolidated visual review. Source SHA-256 values are exact current canonical PNG hashes, not newly selected or modified bytes.','',
    '| Scene / current file | Canonical SHA-256 | Source commit | Review | Remaining action |', '|---|---|---|---|---|']
for r in matrix:
    n=r['key'].split('/')[-1];action='None demonstrated'
    if n=='paper_emergency':action='Use already-selected v04 only through separate PR #18 decision; main still v03'
    elif r['unselectedAlternatives']:action='Historical alternatives stay unselected; no required touchup'
    md.append('| '+title(n)+'<br>`'+r['approvedVersion']+'` | `'+r['canonicalSha256']+'` | `'+r['canonicalSource']['commit']+'` | '+r['recommendation']+' | '+action+' |')
md+=['','Every row: perspective checked; cross-chapter consistency checked; no demonstrated required manual touchup. Full source repository/ref/path, previous recommendation, new/prior review status, repair mask and alternatives are in [JSON](chapter-03-completion-matrix.json).','',
     'Paper v04 selected SHA-256: `93a48082124600b1afeb45e5ea54856bf253e858e55111295e9d9c26919bc978`. Published source `d1600a34a58497b4886518c6aa9feeaa205d8426`. Registration implemented on open unmerged draft PR #18 (`3768b174e544600c3a88e3ae8b18c0fb35982ac4`); canonical v03 SHA remains `ac0f7c44d267dd54897507ae3b8b02959a5b76f4fcd9d0418b77b8fdb777ba7e`. No merge or Pages deployment in this task.','',
     'Original full-scene/full-character native-grid authorship remains unresolved/unproven. No low-palette requirement or global filtering was applied.']
(B/'chapter-03-completion-matrix.md').write_text('\n'.join(md)+'\n')
print('Built consolidated gallery:',len(h),'sections/fragments;',len(portraits),'composites;',len(matrix),'matrix rows.')
