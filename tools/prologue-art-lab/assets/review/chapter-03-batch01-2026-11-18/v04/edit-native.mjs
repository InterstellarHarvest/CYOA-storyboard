// Native targeted v04 correction; no generation or global processing.
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';
import {createRequire} from 'node:module';import {fileURLToPath} from 'node:url';
const {PNG}=createRequire(import.meta.url)(process.env.PNG_CODEC||'pngjs');
const R=path.dirname(fileURLToPath(import.meta.url)),V3=path.join(R,'../v03');
const parent=JSON.parse(fs.readFileSync(path.join(V3,'manifest.json')));
const strokes=JSON.parse(fs.readFileSync(path.join(R,'sources/outline-strokes.json'))).strokes;
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const read=p=>PNG.sync.read(fs.readFileSync(p));
const inside=(x,y,ps)=>{let hit=false;for(let i=0,j=ps.length-1;i<ps.length;j=i++){const [a,b]=ps[i],[c,d]=ps[j];if((b>y)!==(d>y)&&x<(c-a)*(y-b)/(d-b)+a)hit=!hit;}return hit;};
const polygon=[[237,134],[246,134],[249,137],[251,140],[251,143],[232,143],[232,138],[234,136]];
const records=[],pixelLedger=[];
for(const c of parent.candidates){
 const source=path.join(V3,c.candidate),src=read(source),out=new PNG({width:src.width,height:src.height});src.data.copy(out.data);
 const w=src.width,h=src.height,allowed=new Set(),reasons=new Map();let modified=false,op='byte-identical v03 carry-forward',translation=[0,0];
 const set=(x,y,rgb,reason)=>{const p=(y*w+x)*4;rgb.forEach((v,k)=>out.data[p+k]=v);out.data[p+3]=255;allowed.add(y*w+x);reasons.set(y*w+x,reason);};
 const line=(a,b,rgb,label)=>{let [x,y]=a;const [ex,ey]=b,dx=Math.abs(ex-x),sx=x<ex?1:-1,dy=-Math.abs(ey-y),sy=y<ey?1:-1;let er=dx+dy;for(;;){set(x,y,rgb,label);if(x===ex&&y===ey)break;const e=2*er;if(e>=dy){er+=dy;x+=sx;}if(e<=dx){er+=dx;y+=sy;}}};
 if(c.id==='CH3-A01-restroom'){
  modified=true;op='local desktop-device removal and authored one-pixel dark-contour reinforcement';
  for(let y=134;y<143;y++)for(let x=232;x<251;x++)if(inside(x+.5,y+.5,polygon)){
   let sx=228,sy=y;
   if(y<139){sx=249;sy=132;if(x>=239&&x<=245&&y<=136){sx=241;sy=131;}}
   else if(y===139){sx=264;sy=139;}
   const s=(sy*w+sx)*4;set(x,y,[...src.data.subarray(s,s+3)],'desktop device/base removal');
  }
  for(const s of strokes)for(let i=1;i<s.points.length;i++)line(s.points[i-1],s.points[i],s.rgb,s.label);
 }
 if(c.id==='CH3-A06-presenter-idle'){
  modified=true;op='lossless additional left translation';translation=[-28,0];out.data.fill(0);
  for(let y=0;y<h;y++)for(let x=28;x<w;x++)src.data.copy(out.data,(y*w+x-28)*4,(y*w+x)*4,(y*w+x)*4+4);
 }
 const dest='candidates/'+c.id+'-v04.png',target=path.join(R,dest);
 if(modified)fs.writeFileSync(target,PNG.sync.write(out));else fs.copyFileSync(source,target);
 let changed=0,unexpected=0,box=[w,h,-1,-1];const alphas=new Set();
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){const p=(y*w+x)*4;alphas.add(out.data[p+3]);if(out.data[p+3])box=[Math.min(box[0],x),Math.min(box[1],y),Math.max(box[2],x+1),Math.max(box[3],y+1)];
  if(!src.data.subarray(p,p+4).equals(out.data.subarray(p,p+4))){changed++;if(c.id==='CH3-A01-restroom'){if(!allowed.has(y*w+x))unexpected++;pixelLedger.push({x,y,before:[...src.data.subarray(p,p+4)],after:[...out.data.subarray(p,p+4)],reason:reasons.get(y*w+x)});}}
 }
 records.push({id:c.id,version:'v04',candidate:dest,sha256:hash(target),source:'../v03/'+c.candidate,sourceSha256:hash(source),modified,operation:op,translation,scale:1,rotation:0,dimensions:[w,h],character:c.character,changedPixels:changed,unexpectedChangedPixels:unexpected,spriteBounds:c.character?box:null,alphaValues:[...alphas].sort((a,b)=>a-b),status:'generated',selected:false,assetPath:null});
}
const save=(p,v)=>fs.writeFileSync(path.join(R,p),JSON.stringify(v,null,2)+'\n');
save('edit-report.json',{sourcePin:'0df9994a1162528cc0de33add680a7d43717b4fa',imageGenerationCalls:0,deviceRemovalPolygon:polygon,outlineStrokes:'sources/outline-strokes.json',candidates:records});
save('sources/a01-pixel-ledger.json',pixelLedger);
save('sources/pose-anchors.json',{attendant:{translationFromV03:[0,0],eyeAnchor:[314,86],handAnchor:[320,254]},presenter:{translationFromV03:[-28,0],translationFromV02:[-72,29],cumulativeSourceOffset:[-72,41],eyeAnchorBefore:[220,113],eyeAnchorAfter:[192,113],handAnchorBefore:[343,174],handAnchorAfter:[315,174],scale:1}});
console.log(JSON.stringify(records.map(c=>({id:c.id,modified:c.modified,changedPixels:c.changedPixels,bounds:c.spriteBounds})),null,2));
