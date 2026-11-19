// Targeted, lossless v03 native edits. No generation, scaling or filtering.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
const {PNG}=createRequire(import.meta.url)(process.env.PNG_CODEC||'pngjs');
const R=path.dirname(fileURLToPath(import.meta.url)),V2=path.join(R,'../v02');
const parent=JSON.parse(fs.readFileSync(path.join(V2,'manifest.json')));
const anchors=JSON.parse(fs.readFileSync(path.join(V2,'sources/silhouettes.json')));
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const read=p=>PNG.sync.read(fs.readFileSync(p));
const write=(p,im)=>fs.writeFileSync(p,PNG.sync.write(im));
function inside(x,y,ps){let hit=false;for(let i=0,j=ps.length-1;i<ps.length;j=i++){const [a,b]=ps[i],[c,d]=ps[j];if((b>y)!==(d>y)&&x<(c-a)*(y-b)/(d-b)+a)hit=!hit;}return hit;}
const offsets={attendant:[44,0],presenter:[-44,29]};
// Device and its base/shadow, excluding the plant pot at x>=487. Wall seam
// at x~451 is restored from clean wall pixels in the same source columns.
const removalPolygon=[[404,227],[470,227],[474,231],[485,258],[485,275],[479,275],[479,272],[406,272],[394,263],[394,252],[400,231]];
const records=[];const anchorReport={};
for(const c of parent.candidates){
 const source=path.join(V2,c.candidate),dest='candidates/'+c.id+'-v03.png',target=path.join(R,dest),src=read(source),w=src.width,h=src.height;
 let out,operation='byte-identical carry-forward',modified=false,changed=0,clippedVisiblePixels=0,preservedVisiblePixels=0,changedOutsideScope=0,box=[w,h,-1,-1];
 if(c.character){
  const [dx,dy]=offsets[c.character];out=new PNG({width:w,height:h});operation='lossless integer foreground translation';modified=true;
  for(let y=0;y<h;y++)for(let x=0;x<w;x++){
   const s=(y*w+x)*4,xx=x+dx,yy=y+dy;
   if(xx>=0&&xx<w&&yy>=0&&yy<h){src.data.copy(out.data,(yy*w+xx)*4,s,s+4);if(src.data[s+3])preservedVisiblePixels++;}
   else if(src.data[s+3])clippedVisiblePixels++;
  }
  const a=anchors[c.character];anchorReport[c.character]={sourceForeground:c.candidate,translationFromV02:[dx,dy],cumulativeSourceOffset:[a.offset[0]+dx,a.offset[1]+dy],eyeAnchorBefore:a.eyeAnchor,eyeAnchorAfter:[a.eyeAnchor[0]+dx,a.eyeAnchor[1]+dy],handAnchorBefore:a.handAnchor,handAnchorAfter:[a.handAnchor[0]+dx,a.handAnchor[1]+dy],scale:1,rotation:0,clippedVisiblePixels,preservedVisiblePixels};
 }else if(c.id==='CH3-A02-restroom-bg'){
  out=read(source);operation='localized native device removal using adjacent original wall/desk pixels';modified=true;
  for(let y=227;y<275;y++)for(let x=394;x<485;x++)if(inside(x+.5,y+.5,removalPolygon)){
   // No synthesized colors. Above the desktop, use a clean 5-row strip in
   // the same wall columns; below it, copy the adjacent clean desktop rows.
   const sx=y<=260?x:390+(x-394)%4,sy=y<=260?220+(y-227)%5:y;
   src.data.copy(out.data,(y*w+x)*4,(sy*w+sx)*4,(sy*w+sx)*4+4);
  }
 }else{
  fs.copyFileSync(source,target);out=read(target);
 }
 if(modified)write(target,out);
 const alphas=new Set();let visible=0;
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){
  const p=(y*w+x)*4;alphas.add(out.data[p+3]);if(out.data[p+3]){visible++;box=[Math.min(box[0],x),Math.min(box[1],y),Math.max(box[2],x+1),Math.max(box[3],y+1)];}
  if(!out.data.subarray(p,p+4).equals(src.data.subarray(p,p+4))){changed++;if(c.id==='CH3-A02-restroom-bg'&&!inside(x+.5,y+.5,removalPolygon))changedOutsideScope++;}
 }
 records.push({id:c.id,version:'v03',source:'../v02/'+c.candidate,sourceSha256:hash(source),candidate:dest,sha256:hash(target),dimensions:[w,h],status:'generated',selected:false,assetPath:null,character:c.character,modified,operation,translation:c.character?offsets[c.character]:[0,0],scale:1,rotation:0,changedPixels:changed,changedOutsideApprovedScope:changedOutsideScope,allowedRegion:c.id==='CH3-A02-restroom-bg'?removalPolygon:null,spriteBounds:c.character?box:null,headroom:c.character?box[1]:null,bottomClearance:c.character?h-box[3]:null,visiblePixels:visible,clippedVisiblePixels,preservedVisiblePixels,alphaValues:[...alphas].sort((a,b)=>a-b),originalNativeAuthorship:'UNPROVEN — inherited from derived v02; this pass does not repair original-native authorship.'});
}
const save=(p,v)=>fs.writeFileSync(path.join(R,p),JSON.stringify(v,null,2)+'\n');
save('edit-report.json',{sourcePin:'32273a2839e3a941530a153b69fb9a508e92f57b',deviceRemoval:{allowedPolygon:removalPolygon,wallDonor:'same x; y=220+((targetY-227)%5), for y<=260',deskDonor:'x=390+((targetX-394)%4), same y, for y>=261',gateHardwareRetained:true,plantRetained:true},candidates:records});
save('sources/pose-anchors.json',anchorReport);
console.log(JSON.stringify(records.map(c=>({id:c.id,modified:c.modified,translation:c.translation,changedPixels:c.changedPixels,bounds:c.spriteBounds,clipped:c.clippedVisiblePixels})),null,2));
