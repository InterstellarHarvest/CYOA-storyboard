"""Add an explicit continuity correction without rewriting frozen v01 artifacts."""
from pathlib import Path
import argparse
B=Path(__file__).resolve().parents[2]
REPO=next(p for p in B.parents if(p/'story/artwork.draft.json').exists())
def main():
 p=argparse.ArgumentParser();p.add_argument('--addendum-commit',required=True);a=p.parse_args()
 raw='https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/'+a.addendum_commit+'/'+B.relative_to(REPO).as_posix()+'/'
 blob='https://github.com/InterstellarHarvest/CYOA-storyboard/blob/'+a.addendum_commit+'/'+B.relative_to(REPO).as_posix()+'/'
 text=(B/'v01/online.html').read_text()
 text=text.replace('Six UNSELECTED candidates.','Six UNSELECTED candidates; post-lift closer reference HELD.')
 text=text.replace('Nearest lifting bay is outside this closer view. No redundant stall-removal dialogue background is needed.','The approved image includes an open-stall edge at far right. It remains valid before the lift; post-lift reuse is NOT verified. See the current continuity addendum.')
 text=text.replace('Approved closer background — reused before burst and for porter','Approved closer background — pre-lift reuse only; post-lift view held')
 text=text.replace('hotel_stall_lot_claimed, hotel_stall_crane_success, hotel_stall_porter_protest','hotel_stall_lot_claimed, hotel_stall_crane_success')
 text=text.replace('Full story/state reconciliation','Initial reconciliation (see current addendum)')
 text=text.replace('Manifest and node mappings','Frozen image manifest (current mapping addendum governs)')
 marker='<table>'
 notice='<p class="concern"><b>Current continuity correction:</b> the far-right open-stall edge is visible in CH4-B2-03. The initial v01 reuse assumption is withdrawn. A post-lift closer reference is HELD after its local tile reconstruction failed the quality gate. The six candidate PNGs are unchanged. <a href="'+blob+'CONTINUITY-ADDENDUM.md">Authoritative review mapping and held-state explanation</a> · <a href="'+blob+'CURRENT-REVIEW.json">Current status</a>.</p>'
 text=text.replace(marker,notice+marker)
 section='<article id="continuity"><h2>Approved camera edge — why post-lift reuse is held</h2><section class="figure"><h3>Unchanged approved open-stall edge</h3><p>Exact native crop x=[520,564), y=[65,278). The hinges, door leaf and foot are visible. This is approved-source evidence, not a new candidate.</p><p><button data-scale="1">Native 1×</button> <button data-scale="4">Exact 4×</button> <a href="'+raw+'continuity-addendum/evidence/approved-nearest-stall-edge.png">PNG</a></p><div class="viewport"><img src="'+raw+'continuity-addendum/evidence/approved-nearest-stall-edge.png" data-one="'+raw+'continuity-addendum/evidence/approved-nearest-stall-edge.png" data-four="'+raw+'continuity-addendum/evidence/approved-nearest-stall-edge-4x.png" data-w="44" data-h="213" width="44" height="213" alt="Approved nearest-stall edge"></div></section></article>'
 text=text.replace('<article id="benchmarks">',section+'<article id="benchmarks">')
 (B/'review.html').write_text(text)
if __name__=='__main__':main()
