// Public-only bitmap lettering: reads published metadata and approved PNG atlases.
// This does not load the private game renderer or its narrative logic.
(() => {
  "use strict";
  let faces = {}, images = {};
  const inkColors = {dark:"#22363b",light:"#e4eadf"};
  function glyph(face, char) {
    return face.mapping[char] || face.mapping[char.toUpperCase()] || face.mapping[" "] || {advance:8,w:0,h:0};
  }
  function measure(text, face) {
    let width=0;
    for (const ch of text) width += glyph(face,ch).advance || 0;
    return width;
  }
  function wrap(text, face, width) {
    const result=[];
    for (const paragraph of String(text).split("\n")) {
      let line="";
      for (const word of paragraph.split(/\s+/)) {
        if (!word) continue;
        const candidate=line ? line+" "+word : word;
        if (line && measure(candidate,face)>width) {
          result.push(line);
          line=word;
        } else line=candidate;
      }
      result.push(line);
    }
    return result;
  }
  function image(url) {
    return new Promise((resolve,reject) => {
      const img=new Image();
      img.onload=()=>resolve(img);
      img.onerror=()=>reject(new Error("Missing bitmap atlas "+url));
      img.src=url;
    });
  }
  async function configure(data) {
    if (!data || data.schema!=="cyoa-public-artwork-lab-bitmap-fonts-v1") throw new Error("Unknown font metadata");
    faces=data.faces;
    const urls=new Set();
    for (const f of Object.values(faces)) for (const key of ["atlas","atlasDark","atlasLight"]) if(f[key])urls.add(f[key]);
    const loaded=await Promise.all([...urls].map(async url=>[url,await image(url)]));
    images=Object.fromEntries(loaded);
  }
  function draw(canvas,text,faceId,ink="dark",options={}) {
    const face=faces[faceId]||faces.locked;
    if (!face) return;
    const w=Math.max(1,options.width||canvas.width||100),h=Math.max(1,options.height||canvas.height||40);
    canvas.width=w;canvas.height=h;
    canvas.setAttribute("aria-label",String(text));
    const ctx=canvas.getContext("2d");
    if (!ctx) return;
    ctx.imageSmoothingEnabled=false;
    const url=faceId==="locked" ? (ink==="light"?face.atlasLight:face.atlasDark) : face.atlas;
    const atlas=images[url];
    if (!atlas) return;
    const lineHeight=options.lineHeight||face.lineHeight;
    const lines=wrap(text,face,options.maxWidth||w);
    let y=options.top||0;
    if(options.valign==="center") y=Math.max(0,Math.floor((h-lines.length*lineHeight)/2));
    for(const line of lines) {
      const lineWidth=measure(line,face);
      let x=options.align==="center" ? Math.floor((w-lineWidth)/2) : 0;
      for(const ch of line) {
        const g=glyph(face,ch);
        if(g.w && g.h) ctx.drawImage(atlas,g.x,g.y,g.w,g.h,Math.round(x+(g.bearingX||0)),Math.round(y+(g.bearingY||0)),g.w,g.h);
        x+=(g.advance||0);
      }
      y+=lineHeight;
      if(y>=h)break;
    }
    if(faceId!=="locked"){
      ctx.globalCompositeOperation="source-in";
      ctx.fillStyle=inkColors[ink]||ink;
      ctx.fillRect(0,0,w,h);
      ctx.globalCompositeOperation="source-over";
    }
  }
  window.PUBLIC_PIXEL_TEXT={configure,draw,measure:(s,id)=>faces[id]?measure(s,faces[id]):0};
})();
