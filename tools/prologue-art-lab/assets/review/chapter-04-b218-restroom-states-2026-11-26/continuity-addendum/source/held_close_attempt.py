"""Reproduce held diagnostic only; this is NOT a selectable production state."""
from pathlib import Path
from PIL import Image,ImageDraw
import argparse
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--sample-width',type=int,default=9);a=p.parse_args()
 im=Image.open(ROOT/'v01/references/approved-CH4-B2-03.png');out=im.copy();px=out.load()
 for y in range(91,255):
  for x in range(529,564):px[x,y]=im.getpixel((280+(x-529)%a.sample_width,105+(y-145)%27))
 out.paste(im.crop((529,91,564,255)),(529,-18));out.paste(im.crop((529,0,564,79)),(529,0))
 d=ImageDraw.Draw(out);d.polygon([(539,77),(563,74),(563,89),(529,94)],fill='#263f34');d.line([(539,77),(563,74)],fill='#b8b195');d.line([(529,94),(563,89)],fill='#768573',width=2);d.line([(540,80),(541,96)],fill='#c8cbbb');d.line([(558,78),(561,93)],fill='#c8cbbb');out.save(a.out)
if __name__=='__main__':main()
