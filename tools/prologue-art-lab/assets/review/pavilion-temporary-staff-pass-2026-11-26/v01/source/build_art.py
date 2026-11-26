"""Independent native-grid credential pair. Never reads generated raster pixels."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,zipfile,io,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
P={
'ink':'#303f3c','deep':'#263632','edge':'#45534a','green':'#667768','greenLight':'#859180','greenPale':'#a4ad97',
'cream':'#e4d5ab','creamLight':'#f2e6c5','creamShade':'#c7b78f','paperWarm':'#decca1','paperPale':'#eaddb7','paperEdge':'#b09e79','paperDark':'#8f8268',
'wine':'#754448','wineLight':'#986361','wineDark':'#55393e',
'metalDark':'#4a5350','metal':'#7b8580','metalMid':'#9da49a','metalLight':'#c3c8b8','metalBright':'#e3e4ce',
'back':'#7c877c','backLight':'#899184','backDark':'#717d72','shadow':'#59665b','contact':'#435348'}
G={
'A':['01110','11011','11011','11111','11011','11011','11011'],
'B':['11110','11011','11011','11110','11011','11011','11110'],
'C':['01111','11000','11000','11000','11000','11000','01111'],
'D':['11110','11011','11011','11011','11011','11011','11110'],
'E':['11111','11000','11000','11110','11000','11000','11111'],
'F':['11111','11000','11000','11110','11000','11000','11000'],
'G':['01111','11000','11000','11011','11011','11011','01111'],
'H':['11011','11011','11011','11111','11011','11011','11011'],
'I':['11111','00100','00100','00100','00100','00100','11111'],
'J':['00111','00011','00011','00011','11011','11011','01110'],
'K':['11011','11011','11110','11100','11110','11011','11011'],
'L':['11000','11000','11000','11000','11000','11000','11111'],
'M':['10001','11011','11111','10101','10001','10001','10001'],
'N':['11001','11001','11101','11111','11011','11011','11011'],
'O':['01110','11011','11011','11011','11011','11011','01110'],
'P':['11110','11011','11011','11110','11000','11000','11000'],
'Q':['01110','11011','11011','11011','11111','01110','00011'],
'R':['11110','11011','11011','11110','11100','11010','11011'],
'S':['01111','11000','11000','01110','00011','00011','11110'],
'T':['11111','00100','00100','00100','00100','00100','00100'],
'U':['11011','11011','11011','11011','11011','11011','01110'],
'V':['11011','11011','11011','11011','11011','01110','00100'],
'W':['10001','10001','10001','10101','11111','11011','10001'],
'X':['11011','11011','01110','00100','01110','11011','11011'],
'Y':['11011','11011','11011','01110','00100','00100','00100'],
'Z':['11111','00011','00110','00100','01100','11000','11111'],
'0':['01110','11011','11011','11011','11011','11011','01110'],
'1':['00100','01100','00100','00100','00100','00100','01110'],
'2':['01110','11011','00011','00110','01100','11000','11111'],
'3':['11110','00011','00011','01110','00011','00011','11110'],
'4':['11011','11011','11011','11111','00011','00011','00011'],
'5':['11111','11000','11000','11110','00011','00011','11110'],
'6':['01111','11000','11000','11110','11011','11011','01110'],
'7':['11111','00011','00110','00100','01100','01100','01100'],
'8':['01110','11011','11011','01110','11011','11011','01110'],
'9':['01110','11011','11011','01111','00011','00011','11110'],
':':['00000','00100','00100','00000','00100','00100','00000'],
"'":['00110','00110','00100','00000','00000','00000','00000'],
'-':['00000','00000','00000','11111','00000','00000','00000'],
'/':['00001','00011','00110','00100','01100','11000','10000'],
' ':['00000']*7}

class Art:
 def __init__(self,size):self.size=size;self.layers=[];self.commands=[];self.texts=[]
 def layer(self,name):
  self.im=Image.new('RGBA',self.size);self.d=ImageDraw.Draw(self.im);self.layers.append((name,self.im));self.name=name
 def mark(self,kind,coords,c,width=1):
  self.commands.append({'layer':self.name,'kind':kind,'coordinates':coords,'colour':c,'width':width})
  if kind=='polygon':self.d.polygon(coords,fill=P[c])
  elif kind=='line':self.d.line(coords,fill=P[c],width=width)
  elif kind=='ellipse':self.d.ellipse(coords,fill=P[c])
  else:self.d.rectangle(coords,fill=P[c])
 def rect(self,xy,c):self.mark('rectangle',xy,c)
 def poly(self,xy,c):self.mark('polygon',xy,c)
 def line(self,xy,c,width=1):self.mark('line',xy,c,width)
 def ellipse(self,xy,c):self.mark('ellipse',xy,c)
 def text(self,s,x,y,k,c,zone=None):
  width=(len(s)*6-1)*k
  box=[x,y,x+width,y+7*k]
  if zone:assert zone[0]<=x and zone[1]<=y and box[2]<=zone[2] and box[3]<=zone[3],(s,box,zone)
  self.texts.append({'text':s,'box':box,'scale':k,'safeZone':zone,'layer':self.name})
  for n,ch in enumerate(s):
   for row,bits in enumerate(G[ch]):
    for col,v in enumerate(bits):
     if v=='1':self.rect([x+(n*6+col)*k,y+row*k,x+(n*6+col+1)*k-1,y+(row+1)*k-1],c)
 def center(self,s,y,k,c,zone):self.text(s,(self.size[0]-(len(s)*6-1)*k)//2,y,k,c,zone)
 def save(self,name,rgb):
  final=Image.new('RGBA',self.size)
  for _,im in self.layers:final=Image.alpha_composite(final,im)
  if rgb:final=final.convert('RGB')
  final.save(ROOT/'native'/f'{name}.png')
  for ln,im in self.layers:im.save(ROOT/'layers'/f'{name}-{ln}.png')
  xml=ET.Element('image',w=str(self.size[0]),h=str(self.size[1]),name=name,version='0.0.3');stack=ET.SubElement(xml,'stack')
  with zipfile.ZipFile(ROOT/'source'/f'{name}.ora','w') as z:
   z.writestr('mimetype','image/openraster')
   for n,(ln,im) in reversed(list(enumerate(self.layers))):
    file=f'data/layer{n}.png';buf=io.BytesIO();im.save(buf,format='PNG');z.writestr(file,buf.getvalue());ET.SubElement(stack,'layer',name=ln,src=file,x='0',y='0',opacity='1.0',visibility='visible',**{'composite-op':'svg:src-over'})
   z.writestr('stack.xml',ET.tostring(xml));buf=io.BytesIO();final.save(buf,format='PNG');z.writestr('mergedimage.png',buf.getvalue())
  (ROOT/'source'/f'{name}-marks.json').write_text(json.dumps({'canvas':self.size,'palette':P,'glyphs':G,'marks':self.commands,'textLayout':self.texts,'generatedPixelsUsed':False,'method':'Independent native marks; no resizing/sampling/quantization of source reference'},indent=2)+'\n')
  return final

def inspection():
 a=Art((565,451));a.layer('backing-and-shadow');a.rect([0,0,564,450],'back')
 # Broad quiet backing planes, not noise or a mathematical gradient.
 a.poly([(0,0),(564,0),(564,67),(0,191)],'backLight');a.poly([(0,373),(564,275),(564,450),(0,450)],'backDark')
 a.poly([(63,107),(512,94),(527,107),(530,415),(515,429),(71,429),(60,415)],'shadow')
 a.poly([(58,101),(510,92),(521,104),(521,413),(510,420),(62,420),(54,411)],'contact')
 a.layer('cardstock-and-laminate')
 a.poly([(61,78),(504,78),(515,89),(515,401),(503,414),(60,414),(49,403),(49,90)],'edge')
 a.poly([(62,80),(502,80),(511,90),(511,398),(501,408),(62,408),(54,400),(54,92)],'greenLight')
 a.poly([(64,84),(499,84),(507,92),(507,397),(499,404),(64,404),(58,397),(58,94)],'green')
 a.line([(60,97),(60,93),(66,86),(498,86),(504,92)],'greenPale',2)
 a.line([(507,105),(507,396),(499,405),(75,405)],'deep',2)
 a.poly([(77,119),(487,119),(493,126),(493,383),(486,393),(78,393),(70,385),(70,128)],'wineDark')
 a.poly([(79,120),(485,120),(490,127),(490,381),(484,389),(80,389),(74,382),(74,129)],'wine')
 a.poly([(84,126),(481,126),(485,131),(485,378),(480,383),(84,383),(80,378),(80,132)],'cream')
 a.poly([(84,126),(481,126),(485,131),(485,139),(87,139),(80,145),(80,132)],'creamLight')
 a.poly([(80,367),(85,374),(478,374),(485,367),(485,378),(480,383),(84,383),(80,378)],'creamShade')
 a.line([(84,126),(481,126),(485,131)],'creamShade')
 # Connected paper shade clusters follow the bowed sleeve and curled insert.
 # Print stays above these subtle regions; no random speckle or gradients.
 a.poly([(82,142),(103,139),(119,142),(166,142),(176,145),(359,145),(370,148),(441,148),(450,151),(480,151),(480,170),(450,168),(441,165),(371,165),(360,162),(174,162),(163,159),(117,159),(104,156),(82,158)],'paperPale')
 a.poly([(81,171),(86,174),(86,351),(92,361),(124,366),(161,366),(174,370),(461,370),(480,362),(483,352),(483,375),(475,380),(88,380),(82,375)],'paperWarm')
 a.poly([(450,376),(461,371),(468,364),(476,361),(484,351),(484,374),(477,381),(450,381)],'creamShade')
 a.poly([(467,379),(474,370),(482,365),(480,375),(475,380)],'creamLight')
 a.line([(473,380),(480,375),(483,366)],'paperEdge')
 a.line([(85,181),(85,198)],'creamLight');a.line([(482,215),(482,248)],'paperWarm')
 # Grouped abrasion follows exposed corners and sleeve edges, not printed regions.
 for xy,c in [([59,95,62,108],'creamShade'),([65,88,78,89],'creamLight'),([82,87,97,87],'greenPale'),([55,379,57,395],'metalMid'),([61,400,74,402],'paperEdge'),([484,403,495,404],'creamShade'),([504,369,506,386],'greenPale'),([504,96,506,111],'metalMid'),([117,81,151,82],'greenPale'),([391,408,421,409],'greenLight')]:a.rect(xy,c)
 a.line([(62,117),(89,88),(100,88),(62,130)],'metalMid',2)
 a.line([(476,402),(501,378)],'greenPale',2)
 a.layer('punch-and-clip')
 a.rect([247,92,317,110],'creamShade');a.rect([249,94,315,108],'deep');a.rect([252,97,312,107],'contact')
 a.poly([(268,26),(296,26),(301,31),(301,99),(297,107),(268,107),(263,101),(263,32)],'metalDark')
 a.rect([266,30,297,98],'metal');a.rect([267,31,295,91],'metalMid');a.rect([268,32,270,89],'metalLight');a.line([(271,29),(293,29),(297,33)],'metalBright',2)
 a.rect([270,91,297,100],'metalDark');a.rect([270,92,295,94],'metalLight');a.line([(267,101),(296,101)],'metalMid',2)
 a.rect([259,68,263,79],'metalDark');a.rect([260,69,262,76],'metalLight');a.rect([301,68,305,80],'metalDark');a.rect([302,69,304,75],'metal')
 a.ellipse([273,39,291,57],'metalDark');a.ellipse([275,40,289,54],'metalLight');a.ellipse([276,42,288,54],'metal');a.line([(278,52),(286,44)],'metalDark',2);a.line([(280,52),(288,44)],'metalBright')
 for xy in [[279,66,290,66],[273,81,282,81],[289,73,294,73]]:a.rect(xy,'metalLight')
 a.layer('institutional-printing')
 # Decorative printed features occupy their own top register and bottom margin.
 a.rect([94,144,220,169],'wine');a.rect([96,146,218,167],'cream');a.text('HP-03 / 0417',100,151,1,'ink',[98,148,218,167])
 # Small Pavilion building pictogram, not a new organizational logo/entitlement.
 a.line([(251,177),(354,177)],'wine',2);a.rect([267,160,338,175],'wine');a.poly([(263,159),(303,150),(343,159)],'wine');a.rect([301,140,303,152],'wine');a.ellipse([300,137,304,141],'wine')
 for x in [274,285,296,307,318,329]:a.rect([x,163,x+2,174],'cream')
 a.ellipse([426,140,468,182],'wine');a.ellipse([429,143,465,179],'cream');a.ellipse([433,147,461,175],'wineLight');a.ellipse([435,149,459,173],'cream');a.text('P',440,154,2,'wine',[437,151,459,172])
 a.rect([91,194,473,234],'ink');a.center('TEMPORARY STAFF',200,4,'creamLight',[98,198,467,230])
 a.center("PEOPLE'S PAVILION",250,3,'ink',[95,247,470,274])
 a.line([(96,282),(468,282)],'wine',2)
 a.center('DEPARTMENT: HUMAN PRESENTATION',295,2,'ink',[94,291,471,313])
 a.line([(96,320),(468,320)],'wine',2)
 a.center('VALID UNTIL CORRECTED',336,2,'wineDark',[103,333,462,353])
 for x in [96,108,120,132]:
  a.rect([x,363,x+8,370],'wineLight');a.rect([x+1,364,x+7,369],'cream')
 for x in [424,436,448,460]:
  a.rect([x,363,x+8,370],'wineLight');a.rect([x+1,364,x+7,369],'cream')
 return a.save('pavilion_temporary_staff_pass_inspect',True)

def slot():
 a=Art((96,96));a.layer('cardstock-and-laminate')
 a.poly([(15,25),(79,25),(86,31),(86,82),(80,89),(15,89),(9,83),(9,32)],'deep')
 a.poly([(15,26),(78,26),(84,32),(84,81),(78,87),(16,87),(11,82),(11,33)],'greenLight')
 a.poly([(16,29),(77,29),(81,33),(81,80),(77,84),(17,84),(14,80),(14,34)],'green')
 a.rect([17,36,78,79],'wineDark');a.rect([18,37,77,78],'wine');a.rect([20,39,75,76],'cream');a.rect([21,39,74,40],'creamLight');a.rect([20,74,75,76],'creamShade')
 a.line([(12,40),(25,27),(28,27),(12,44)],'metalLight');a.line([(73,85),(82,76)],'greenPale');a.rect([15,84,21,85],'creamShade')
 a.layer('punch-and-clip');a.rect([37,29,59,33],'deep')
 a.poly([(44,6),(52,6),(55,9),(55,29),(52,34),(43,34),(41,31),(41,10)],'metalDark');a.rect([43,8,52,28],'metalMid');a.rect([44,8,45,26],'metalLight');a.rect([44,29,53,31],'metal');a.line([(44,7),(51,7)],'metalBright')
 a.ellipse([45,11,51,17],'metalDark');a.ellipse([46,12,50,16],'metal');a.line([(46,16),(50,12)],'metalBright')
 a.layer('institutional-printing');a.line([(35,46),(60,46)],'wine');a.poly([(37,43),(48,40),(58,43)],'wine');a.rect([40,43,56,45],'wine');a.rect([47,39,48,42],'wine')
 a.rect([23,50,72,61],'ink');a.text('STAFF',33,52,1,'creamLight',[25,51,71,60])
 a.rect([24,65,57,66],'wine');a.rect([24,69,48,70],'ink');a.rect([24,72,39,72],'green')
 a.ellipse([62,66,70,74],'wine');a.ellipse([64,68,68,72],'cream')
 return a.save('pavilion_temporary_staff_pass_slot',False)

if __name__=='__main__':
 for d in ['native','layers','source']:(ROOT/d).mkdir(exist_ok=True)
 inspection();slot();print('Constructed two independent native images; zero generated pixels read.')
