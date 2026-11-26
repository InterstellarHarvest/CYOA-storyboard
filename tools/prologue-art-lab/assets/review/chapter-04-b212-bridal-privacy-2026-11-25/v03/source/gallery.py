from pathlib import Path
from PIL import Image
import html
ROOT=Path(__file__).resolve().parents[1]
def fig(title,f):
 im=Image.open(ROOT/f);four='previews/'+Path(f).stem+'-4x.png'
 return f'<section class="figure"><h3>{html.escape(title)}</h3><nav><button data-scale="1">Native 1×</button><button data-scale="4">Exact 4×</button><a href="{f}">Native PNG</a><a href="{four}">4× PNG</a></nav><div class="raster"><img src="{f}" data-one="{f}" data-four="{four}" data-w="{im.width}" data-h="{im.height}" width="{im.width}" height="{im.height}" alt="{html.escape(title)}"></div></section>'
def main():
 css='body{margin:0;background:#172a23;color:#efe5c8;font:16px/1.55 system-ui,sans-serif}main{padding:22px}header,article{padding:20px;border:1px solid #697c6d;margin-bottom:26px}h1,h2,h3{margin:0 0 12px}a{color:#c5dfca;margin-right:14px}nav{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0}button{padding:10px;background:#435e4d;border:1px solid #bacbaa;color:#fff0ca;cursor:pointer}.figure{padding:14px;margin:20px 0;background:#294136}.raster{overflow:auto;max-width:100%;background:#253b32}.raster img{display:block;max-width:none!important;image-rendering:pixelated}p{max-width:1100px}'
 head='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>B2-12 v03 · INSPECT lock row</title><style>'+css+'</style><main><header><h1>B2-12 v03 · Dedicated INSPECT lock row</h1><p><strong>Two new square INSPECT alternatives: UNSELECTED.</strong> Approved v01 originals and newly approved widescreen v02 artwork remain exact. Only CRT-content pixels change.</p><p>Same centered text block and icon row in both states. Text moves up11 native pixels; the lock icon has8–9 clear pixel rows below the text. Exact source palette, CRT styling, glass accents, brass, lighting and every surrounding pixel are preserved.</p><nav><a href="#closeups">Before / after close-ups</a><a href="#locked">New locked</a><a href="#provisional">New provisional</a><a href="#benchmarks">Approved sources</a><a href="#protected">Approved widescreen</a><a href="manifest.json">Manifest / hashes</a><a href="evidence/validation.json">QA / preservation</a><a href="evidence/layout.json">Exact layout</a><a href="README.md">Method / provenance</a><a href="source/OWNER-REQUEST.txt">Owner request</a><a href="source/build.py">Native edit recipe</a></nav></header>'
 body='<article id="closeups"><h2>Native / exact4× close-up comparisons</h2>'
 for title,name in [('Both states · approved v01 / unselected v03','both-states-crt-before-after'),('Locked close-up · before / after','locked-crt-before-after'),('Provisional close-up · before / after','provisional-crt-before-after')]:body+=fig(title,'comparisons/'+name+'-native.png')
 body+='</article>'
 for state in ['locked','provisional']:body+='<article id="'+state+'"><h2>v03 '+state+' INSPECT · 565×451 · UNSELECTED</h2>'+fig('New '+state+' INSPECT · UNSELECTED',f'native/CH4-NEW-07-inspect-{state}-v03.png')+'</article>'
 body+='<article id="benchmarks"><h2>Approved v01 sources and Chapter2 reference · unchanged bytes</h2>'
 for state in ['locked','provisional']:body+=fig('Approved v01 '+state+' INSPECT · unchanged',f'references/approved-inspect-{state}-v01.png')
 body+=fig('Approved Chapter2 Focus · unchanged','references/approved-ch2-focus.png')+'</article>'
 body+='<article id="protected"><h2>Newly approved widescreen v02 · unchanged bytes</h2>'
 for state in ['locked','provisional']:body+=fig('Approved v02 '+state+' Focus · protected',f'references/approved-focus-{state}-v02.png')
 body+='</article>'
 script='<script>document.querySelectorAll("button[data-scale]").forEach(b=>b.onclick=()=>{const i=b.closest("section.figure").querySelector("img"),s=Number(b.dataset.scale);i.src=s===4?i.dataset.four:i.dataset.one;i.width=Number(i.dataset.w)*s;i.height=Number(i.dataset.h)*s;});</script></main></html>'
 (ROOT/'index.html').write_text(head+body+script)
if __name__=='__main__':main()
