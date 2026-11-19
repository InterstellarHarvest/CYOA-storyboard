// DERIVED native realization: disclosed transfer plus native painting/manual
// silhouettes. No original-native claim, palette filter or alpha threshold.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
const {PNG}=createRequire(import.meta.url)(process.env.PNG_CODEC||'pngjs');
const R=path.dirname(fileURLToPath(import.meta.url));
const masks=JSON.parse(fs.readFileSync(path.join(R,'sources/silhouettes.json')));
const specs=JSON.parse(fs.readFileSync(path.join(R,'sources/edits.json')));
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(path.join(R,p))).digest('hex');
const write=(p,im)=>fs.writeFileSync(path.join(R,p),PNG.sync.write(im));
function inside(x,y,ps){let hit=false;for(let i=0,j=ps.length-1;i<ps.length;j=i++){const [a,b]=ps[i],[c,d]=ps[j];if((b>y)!==(d>y)&&x<(c-a)*(y-b)/(d-b)+a)hit=!hit;}return hit;}
const font={'3':['11110','00001','00001','01110','00001','00001','11110'],'0':['01110','10001','10001','10001','10001','10001','01110']};
const report=[];
for(const spec of specs){
 const src=PNG.sync.read(fs.readFileSync(path.join(R,'generation-source',spec.filename)));
 const [w,h]=spec.dimensions,im=new PNG({width:w,height:h}),guide=new PNG({width:w,height:h}),m=spec.character?masks[spec.character]:null;
 const edits=[];let nativePaintedPixels=0;
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){
  const xx=x-(m?.offset[0]||0),yy=y-(m?.offset[1]||0);
  const sx=Math.min(src.width-1,Math.max(0,Math.floor((xx+.5)*src.width/w))),sy=Math.min(src.height-1,Math.max(0,Math.floor((yy+.5)*src.height/h)));
  const s=(sy*src.width+sx)*4,p=(y*w+x)*4;
  for(let c=0;c<4;c++)guide.data[p+c]=src.data[s+c];
  const visible=!m||(inside(xx+.5,yy+.5,m.outline)&&!m.holes.some(ps=>inside(xx+.5,yy+.5,ps)));
  if(visible){for(let c=0;c<3;c++)im.data[p+c]=src.data[s+c];im.data[p+3]=255;}
 }
 const set=(x,y,color)=>{if(x<0||y<0||x>=w||y>=h)return;const p=(y*w+x)*4;for(let c=0;c<3;c++)im.data[p+c]=color[c];im.data[p+3]=255;nativePaintedPixels++;};
 const rect=(x,y,ww,hh,color)=>{for(let yy=y;yy<y+hh;yy++)for(let xx=x;xx<x+ww;xx++)set(xx,yy,color);};
 if(m){
  // Authored one-pixel contour inks replace contaminated edge colors along
  // the hand-traced mask. This uses no threshold of the generated alpha.
  for(let y=1;y<h-1;y++)for(let x=1;x<w-1;x++){
   const p=(y*w+x)*4;if(im.data[p+3]!==255)continue;
   if([p-4,p+4,p-w*4,p+w*4].every(q=>im.data[q+3]===255))continue;
   const yy=y-m.offset[1];let ink;
   if(spec.character==='attendant')ink=yy<80?[67,53,44]:yy<115?[126,84,57]:[108,103,86];
   else ink=yy<110?[112,57,34]:(x>365&&yy<155)?[156,99,63]:[52,65,74];
   set(x,y,ink);
  }
  edits.push({kind:'hand-traced binary silhouette with authored one-pixel contour inks',source:'sources/silhouettes.json'});
  for(const p of m.pixelTouchups||[])set(...p.at,p.rgb);
 }
 function plate(x,y,ww,hh){rect(x,y,ww,hh,[121,113,102]);rect(x+1,y+1,ww-2,hh-2,[238,222,193]);for(const dx of [2,ww-3])for(const dy of [2,hh-3])set(x+dx,y+dy,[91,91,84]);edits.push({kind:'clean cream repair plate with four fasteners',rect:[x,y,ww,hh]});}
 function countdown(cx,cy,radius,scale){
  const background=[57,79,89],ink=[249,226,188];
  for(let y=Math.floor(cy-radius);y<=cy+radius;y++)for(let x=Math.floor(cx-radius);x<=cx+radius;x++)if((x-cx)**2+(y-cy)**2<radius**2)set(x,y,background);
  const width=11*scale,start=Math.round(cx-width/2),top=Math.round(cy-7*scale/2);
  [...'30'].forEach((ch,k)=>font[ch].forEach((row,y)=>[...row].forEach((bit,x)=>{if(bit==='1')rect(start+(k*6+x)*scale,top+y*scale,scale,scale,ink);}))); 
  edits.push({kind:'native bitmap 30',center:[cx,cy],clearDiscRadius:radius,scale,glyphs:font});
 }
 if(spec.id==='CH3-A01-restroom'){
  plate(220,47,11,8);
 }
 if(spec.id==='CH3-A02-restroom-bg'){
  plate(175,51,18,11);
 }
 if(spec.id==='CH3-A04-verification')countdown(160,96,17,2);
 if(spec.id==='CH3-A05-verification-bg')countdown(292,113,33,5);
 const out='candidates/'+spec.id+'-v02.png';write(out,im);write('construction-guides/'+spec.id+'-transfer-only.png',guide);
 const palette=new Set(),alphas=new Set();let box=[w,h,-1,-1],visible=0,difference=0;
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){const p=(y*w+x)*4;alphas.add(im.data[p+3]);if(im.data[p+3]){visible++;palette.add(im.data.subarray(p,p+3).toString('hex'));box=[Math.min(box[0],x),Math.min(box[1],y),Math.max(box[2],x+1),Math.max(box[3],y+1)];}if(!im.data.subarray(p,p+4).equals(guide.data.subarray(p,p+4)))difference++;}
 report.push({...spec,candidate:out,sha256:hash(out),sourceSha256:hash('generation-source/'+spec.filename),sourceDimensions:[src.width,src.height],sourceAlphaValues:[...new Set(Array.from({length:src.width*src.height},(_,i)=>src.data[i*4+3]))].length,visibleColors:palette.size,alphaValues:[...alphas].sort((a,b)=>a-b),spriteBounds:m?box:null,headroom:m?box[1]:null,bottomClearance:m?h-box[3]:null,visiblePixels:visible,changesBeyondSourceTransfer:difference,nativePaintOperations:nativePaintedPixels,nativeEdits:edits,silhouette:m||null,method:'Explicit pixel-center transfer from targeted edit, then authored native pixel planes/repair plates/bitmap countdowns or manually traced silhouettes and integer anchor placement. No global palette filtering, dithering, smoothing or alpha threshold.',originalNativeAuthorship:'NOT DEMONSTRATED — derived from larger image_gen edits. Local native painting and manual masks do not establish original native authorship of the complete image.',status:'generated',selected:false,assetPath:null});
}
fs.writeFileSync(path.join(R,'realization-report.json'),JSON.stringify({sourcePin:'99b74b63a3407aafe7a468c2915291c997563700',candidates:report},null,2)+'\n');
console.log(JSON.stringify(report.map(r=>({id:r.id,colors:r.visibleColors,alpha:r.alphaValues,bounds:r.spriteBounds,changedBeyondTransfer:r.changesBeyondSourceTransfer})),null,2));
