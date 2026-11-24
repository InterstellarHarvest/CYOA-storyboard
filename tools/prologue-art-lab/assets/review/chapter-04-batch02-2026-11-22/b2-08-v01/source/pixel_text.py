"""Integer bitmap lettering from the project's approved Tiny5 atlas."""
from PIL import Image,ImageDraw
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
FACE=json.loads((ROOT/'fonts/tiny5-approved-mapping.json').read_text())
ATLAS=Image.open(ROOT/'fonts/tiny5-approved-atlas.png').convert('RGBA')
def glyph(ch,face='tiny'):
 if face=='pressstart':
  f=json.loads((ROOT/'fonts/pressstart-approved-mapping.json').read_text());g=f['mapping'][ch]
  if not g['w']:return Image.new('L',(8,8)),8
  atlas=Image.open(ROOT/'fonts/pressstart-approved-atlas.png').convert('RGBA')
  mask=atlas.crop((g['x'],g['y'],g['x']+g['w'],g['y']+g['h'])).getchannel('A').resize((8,8),Image.Resampling.NEAREST)
  return mask.point(lambda p:255 if p>=128 else 0),8
 if ch=='—':
  im=Image.new('L',(5,5));ImageDraw.Draw(im).line((0,2,4,2),fill=255);return im,6
 g=FACE['mapping'][ch]
 if not g['w']:return Image.new('L',(1,5)),2
 im=ATLAS.crop((g['x'],g['y'],g['x']+g['w'],g['y']+g['h'])).getchannel('A')
 # Source atlas consists of exact 3x bitmap clusters. No smooth resampling.
 im=im.resize((g['w']//3,g['h']//3),Image.Resampling.NEAREST)
 im=im.point(lambda p:255 if p>=128 else 0)
 # Bearings place punctuation at the baseline instead of the cap top.
 cell=Image.new('L',(im.width,6));cell.paste(im,(0,max(0,(g.get('bearingY',3)-3)//3)))
 return cell,max(2,g['advance']//3)+1
def measure(text,scale=2,face='tiny'):return sum(glyph(c,face)[1]*scale for c in text)
def draw(im,text,xy,scale=2,color='#353b32',face='tiny'):
 x,y=xy;start=x
 for ch in text:
  mask,advance=glyph(ch,face);mask=mask.resize((mask.width*scale,mask.height*scale),Image.Resampling.NEAREST)
  im.paste(color,(x,y,x+mask.width,y+mask.height),mask);x+=advance*scale
 return (start,y,x,y+(8 if face=='pressstart' else 5)*scale)

def project(layer,quad,size=(564,278)):
 """Map rectangular lettering to its physical plane using nearest pixels."""
 src=[(0,0),(layer.width,0),(layer.width,layer.height),(0,layer.height)]
 matrix=[]
 for (x,y),(u,v) in zip(quad,src):
  matrix.extend([[x,y,1,0,0,0,-u*x,-u*y,u],[0,0,0,x,y,1,-v*x,-v*y,v]])
 for col in range(8):
  pivot=max(range(col,8),key=lambda i:abs(matrix[i][col]));matrix[col],matrix[pivot]=matrix[pivot],matrix[col]
  val=matrix[col][col];matrix[col]=[v/val for v in matrix[col]]
  for row in range(8):
   if row==col:continue
   val=matrix[row][col];matrix[row]=[a-val*b for a,b in zip(matrix[row],matrix[col])]
 coefficients=tuple(row[8] for row in matrix)
 return layer.transform(size,Image.Transform.PERSPECTIVE,coefficients,Image.Resampling.NEAREST)
