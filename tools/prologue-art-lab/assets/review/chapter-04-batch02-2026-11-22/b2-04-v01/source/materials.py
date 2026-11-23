"""Material ramps/classifier reused unchanged from approved B2-02 v02 production; ramps are not universal palette limits."""
RAMP={
 'ink':['#202c2d','#303b38','#424b43'],
 'plaster':['#625e50','#81765e','#a19477','#bbae8c','#cec29e','#e0d4b0'],
 'floor':['#4b5150','#626662','#777b72','#909184','#a7a38f','#bcb59e','#d4c9a9'],
 'green':['#263c37','#3c5146','#4d6252','#677761','#88927a','#acb198'],
 'steel':['#344b4a','#526965','#718681','#92a29a','#b4bfb1','#d6dbca'],
 'gold':['#5c4230','#886035','#ad7d3a','#d5a345','#eed17a','#f6e6aa'],
 'copper':['#4c3a2b','#79513a','#a46b43','#c78953','#e3b778'],
 'wood':['#473a2d','#69503a','#8c6946','#ac8758','#c5a574','#dfc493'],
 'red':['#3e3035','#65383e','#894a4f','#a86362','#c18777','#dfb095'],
 'brick':['#64493c','#855c46','#a77758','#c29870','#dbc098'],
 'piano':['#20282b','#303538','#45484b','#626367','#92928a'],
 'skin':['#634936','#9a6747','#c28d5c','#e4b67f','#f0cf9e'],
 'cream':['#756b52','#a39472','#c5b994','#dfd6b5','#f3e9c8'],
 'navy':['#303f4b','#465766','#637382','#8b9799'],
 'foliage':['#25443b','#4a6848','#6f8c4d','#96aa5e','#c1c88b'],
 'sky':['#6c9ec4','#8fc0db','#b8d9df','#e0e8d4']}
def rgb(h):return tuple(bytes.fromhex(h[1:]))
RAMP={k:[rgb(c)for c in v]for k,v in RAMP.items()}
def nearest(p,colors):return min(colors,key=lambda c:(p[0]-c[0])**2+(p[1]-c[1])**2+(p[2]-c[2])**2)
def classify(p):
 r,g,b=p
 if max(p)<67:return'ink'
 if min(p)>210:return'cream'
 if b>r*1.13 and b>g*1.04:return'sky'if max(p)>170 and min(p)>110 else'navy'
 if g>r*1.12 and g>b*1.1:return'foliage'
 if g>r*1.025 and b>r*.88:return'steel'
 if g>r*1.015 and g>b*1.1:return'green'
 if r>g*1.25 and r>b*1.3:
  return'red'if b>g*.72 else'gold'if g>100 else'wood'
 if r>g*1.1 and g>b*1.18:return'cream'
 return'floor'
