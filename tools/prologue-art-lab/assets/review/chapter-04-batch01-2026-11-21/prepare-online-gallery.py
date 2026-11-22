"""Create an additive HTML preview entry using immutable direct GitHub images."""
from pathlib import Path
from urllib.parse import urlparse
import re

ROOT=Path(__file__).resolve().parent
REPO=next(p for p in ROOT.parents if (p/'story/artwork.draft.json').exists())
ASSET_COMMIT='ab654f24666d1c87a5c3f1096ccf46c61f5cd67c'
RAW='https://raw.githubusercontent.com/InterstellarHarvest/CYOA-storyboard/'+ASSET_COMMIT+'/'
BLOB='https://github.com/InterstellarHarvest/CYOA-storyboard/blob/'+ASSET_COMMIT+'/'

def rewrite(m):
 attr,value=m.group(1),m.group(2)
 if not value or value.startswith('#') or urlparse(value).scheme:return m.group(0)
 target=(ROOT/'v02'/value).resolve()
 assert target.is_relative_to(ROOT) and target.is_file(),value
 relative=target.relative_to(REPO).as_posix()
 url=(RAW if target.suffix=='.png' else BLOB)+relative
 return attr+'="'+url+'"'

text=(ROOT/'v02/index.html').read_text()
text=re.sub(r'\b(src|href|data-native|data-large|value)="([^"\n]*)"',rewrite,text)
(ROOT/'v02/online.html').write_text(text)
