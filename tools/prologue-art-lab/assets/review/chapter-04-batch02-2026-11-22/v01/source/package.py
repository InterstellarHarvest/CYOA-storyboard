from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,html
ROOT=Path(__file__).resolve().parents[1]
def main():
 m=json.loads((ROOT/'manifest.json').read_text());assets=m['assets']
 items=[('Worried plumber',assets[0]['native']['file']),('Pleased Eddie',assets[1]['native']['file']),('Plumber — shared background','previews/CH4-B2-01-composite.png'),('Eddie — shared background','previews/CH4-B2-02-composite.png'),('Lot 14 — native pixel lettering',assets[3]['native']['file']),('Master isolator — readable plaque',assets[4]['native']['file']),('Approved Pavilion attendant','references/approved-attendant.png'),('Approved Pavilion presenter','references/approved-presenter.png')]
 sheet=Image.new('RGB',(1164,1296),'#243932');d=ImageDraw.Draw(sheet)
 for i,(title,rel) in enumerate(items):
  x=(i%2)*582+9;y=(i//2)*324+9;d.text((x,y),title,font=ImageFont.load_default(size=15),fill='#f4e2c0');art=Image.open(ROOT/rel).convert('RGBA');back=Image.alpha_composite(Image.new('RGBA',art.size,'#43574d'),art);sheet.paste(back.convert('RGB'),(x,y+30))
 sheet.save(ROOT/'comparisons/B2-01-all-native.png');sheet.resize((4656,5184),Image.Resampling.NEAREST).save(ROOT/'comparisons/B2-01-all-4x.png')
 def card(title,one,four,note='',id_=''):
  im=Image.open(ROOT/one);w,h=im.size
  return f'<article id="{id_}"><h2>{html.escape(title)}</h2><p>{note}</p><div class="controls"><button data-scale="1">Native 1×</button><button data-scale="4">Exact 4×</button><a href="{one}">PNG</a> · <a href="{four}">4× PNG</a></div><div class="strip"><div class="checker"><img class="art" src="{one}" data-one="{one}" data-four="{four}" data-w="{w}" data-h="{h}" width="{w}" height="{h}" alt="{html.escape(title)}"></div></div></article>'
 cards=[]
 for a in assets:
  note=f"<strong>UNSELECTED</strong> · {a['kind']} · source-derived · <code>{a['key']}</code><br>Nodes: "+', '.join(a['nodeIds'])+f"<br>SHA-256: <code>{a['native']['sha256']}</code> · <a href=\"{a['original']['file']}\">Original</a> · <a href=\"{a['prompt']}\">Exact prompt</a>"
  cards.append(card(a['title'],a['native']['file'],a['preview4x']['file'],note,a['id']))
 for id_,title in [('CH4-B2-01','Plumber over shared restroom background'),('CH4-B2-02','Eddie over shared restroom background')]:cards.append(card(title,f'previews/{id_}-composite.png',f'previews/{id_}-composite-4x.png','Composite preview only; two separately exported layers.'))
 for name,title in [('approved-attendant','Approved Pavilion attendant'),('approved-presenter','Approved Pavilion presenter'),('approved-restroom','Approved Chapter 4 restroom — unchanged'),('approved-bureau','Approved Chapter 2 Bureau'),('approved-tower','Approved Chapter 2 Control Tower'),('approved-reception-background','Approved receptionist background')]:cards.append(card(title,f'references/{name}.png',f'previews/{name}-4x.png','Canonical benchmark; preserved reference copy, never a new candidate.'))
 head='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chapter 4 B2-01 — Restroom Dialogue and Controls</title><style>*{box-sizing:border-box}html{color-scheme:dark}body{margin:0;background:#182824;color:#eddfc5;font:16px/1.55 system-ui}main{max-width:1320px;margin:auto;padding:24px}a{color:#c0e3cd}h1{font-size:30px}h2{font-size:21px}article,section{border:1px solid #57695b;background:#22362f;padding:18px;margin:24px 0;min-width:0}.controls{display:flex;flex-wrap:wrap;gap:10px;align-items:center}button{font:inherit;padding:8px 14px;color:#f7ead5;background:#405b49;border:1px solid #90a38b;cursor:pointer}.strip{overflow:auto;max-width:100%;padding:10px;background:#11231d;margin-top:14px}.checker{width:max-content;background:repeating-conic-gradient(#42574d 0% 25%,#33483d 0% 50%) 0 0/16px 16px}img.art{display:block;max-width:none;image-rendering:pixelated;image-rendering:crisp-edges}code{font-size:12px;overflow-wrap:anywhere}nav{display:flex;flex-wrap:wrap;gap:18px}.status{color:#f1c98a}@media(max-width:600px){main{padding:10px}article,section{padding:10px}h1{font-size:24px}}</style><main><header><h1>Chapter 4 · B2-01 · Restroom Dialogue and Controls</h1><p class="status">Five new candidates — UNSELECTED, pending Nate’s review.</p><p>Detailed portraits, one shared background and two Focus A close-ups. All five are disclosed source-derived artwork at 564×278, with exact nearest-neighbor 4× files. Foregrounds are transparent; background and close-ups are opaque. Every image is shown at its actual raster size inside a scrollable view.</p></header><nav><a href="manifest.json">Manifest and exact hashes</a><a href="README.md">Production notes</a><a href="evidence/derivation.json">Derivation</a><a href="evidence/validation.json">QA</a><a href="evidence/generation-receipts.json">Generation provenance</a><a href="comparisons/B2-01-all-native.png">Direct comparison PNG</a><a href="comparisons/B2-01-all-4x.png">Exact 4× comparison PNG</a></nav><section><h2>Review points</h2><p>Compare the actual portraits with the approved Pavilion pair below: faces, natural hands, hair, fabric and detail retained through reduction. The worried plumber has empty hands after setting down his wrench; Eddie retains the receipt and pleased expression. Both use the approved scene identities, freshly posed for conversation.</p><p>Object lettering follows Nate’s direction: chunky approved bitmap fonts, correct receipt/plaque perspective and readable lot identification. The receipt’s full canonical copy stays inside an inset paper-plane margin. Eddie’s small held receipt shows LOT 14; the full copy is in Focus A. Main-scene markings are unchanged.</p><p>The closed background cabinet and the opened isolated-state close-up are different authored contexts. The Focus A cabinet has exactly one large red lever, pulled down; no invented controls, gauges, hands or puzzle clues.</p><p>Batch 1’s five artworks are now APPROVED and SELECTED unchanged. <a href="https://github.com/InterstellarHarvest/CYOA-storyboard/blob/ee5948f14144d2bd99b75432e8d58422e8958bf1/docs/127_CH4_BATCH1_APPROVAL_COMPLETION_20261122.md">Canonical approval, exact hashes and gameplay handoff</a>. These new five candidates remain UNSELECTED.</p></section>'''
 script='''<script>document.querySelectorAll('button[data-scale]').forEach(b=>b.addEventListener('click',()=>{const i=b.closest('article').querySelector('img.art'),s=Number(b.dataset.scale);i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;}));</script></main></html>'''
 (ROOT/'index.html').write_text(head+''.join(cards)+script)
 readme='''# Chapter 4 B2-01 — Restroom dialogue and controls v01

Five **UNSELECTED** review candidates, independently separate from the five approved Batch 1 selections. No engine integration or narrative changes. [Gallery](index.html), [manifest/exact hashes](manifest.json), [native comparison](comparisons/B2-01-all-native.png), [exact4× comparison](comparisons/B2-01-all-4x.png).

- CH4-B2-01: `hotel_plumber:worried`, transparent564×278.
- CH4-B2-02: `hotel_plumber_assistant:pleased`, transparent564×278.
- CH4-B2-03: shared `grand_bellevue/restroom` portrait background, opaque564×278.
- CH4-B2-04: `grand_bellevue/restroom/lot_14_receipt`, opaque564×278 Focus A.
- CH4-B2-05: `grand_bellevue/restroom/master_isolator`, opaque564×278 Focus A.

Built-in **image_gen.imagegen** produced the original illustrations from approved Pavilion portraits, approved Chapter4 architecture and approved Chapter2/reception environmental rendering references. [Originals](originals/), [exact prompts](prompts/), [tool receipts](evidence/generation-receipts.json), [input references/hashes](manifest.json). All final images are **SOURCE-DERIVED**, not independently authored at native resolution. Foregrounds use premultiplied-alpha Lanczos reduction, disconnected cutout/fringe cleanup and restrained near-opaque interior contrast retention, preserving anatomy. Room/Focus art uses controlled opaque reduction of newly composed close cameras, never an enlarged scene crop. No global palette cap. [Full derivation](evidence/derivation.json).

Nate’s final lettering direction is applied to portrait/inspection objects: approved Tiny5/Press Start bitmap atlases, binary glyph masks and nearest-pixel perspective mapping onto paper/plaque planes. The full receipt copy is canonical, including its wrapped exception; deliberate inset margins keep it clear of all four damaged edges. Eddie’s held receipt shows only readable LOT14, with full content in the close-up. Cabinet lettering is enlarged and perspective-aligned. The new background’s top plaque reads WATER; original main scenes and their markings are untouched.

Focus A is **564×278 opaque**, verified against canonical docs105, artwork helpers and a read-only inspection of actual game `ART_CLASS.focus` (recorded in evidence/dimension-contract.json). The565×451 item inspector is separate. Canonical nodes, the pinned v08 inventory and every unchanged approved reference are preserved. Both portraits are composed on the new shared background; light/dark transparency previews are retained.

Reproduce with the recorded Pillow version:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 source/prepare.py
PYTHONDONTWRITEBYTECODE=1 python3 source/package.py
PYTHONDONTWRITEBYTECODE=1 python3 source/validate.py
```

Native lettering is deterministic using bundled copies of already-approved project bitmap font atlases/mappings. No smooth system-font dependency in the artwork. Gallery labels use ordinary browser UI text. `source/qa-gallery.cjs` checks native/exact4× images and controls in Chromium/Firefox; `source/prepare_online.py` pins public gallery dependencies to an immutable artwork commit. No production Pages workflow change.

Batch1 approvals: canonical main `ee5948f14144d2bd99b75432e8d58422e8958bf1`, PR20. Runtime paths remain unbound until Gameplay PMO integration; all exact approved bytes are preserved. Full closeout: docs/127 in that commit. Historical review statuses remain unchanged; the later owner approval supersedes them.
'''
 (ROOT/'README.md').write_text(readme)
if __name__=='__main__':main()
