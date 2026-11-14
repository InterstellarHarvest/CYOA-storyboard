import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import http from "node:http";
import {fileURLToPath} from "node:url";
import {chromium,firefox} from "playwright";
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"../../..");
const shots=path.join(root,"tools/prologue-art-lab/qa/screenshots");
fs.mkdirSync(shots,{recursive:true});
const prefix="/CYOA-storyboard/";
const types={".html":"text/html",".css":"text/css",".js":"text/javascript",".json":"application/json",".png":"image/png"};
const server=http.createServer((req,res)=>{
  const url=new URL(req.url,"http://localhost");
  let filename=decodeURIComponent(url.pathname);
  if(!filename.startsWith(prefix)){res.writeHead(404).end();return;}
  filename=path.resolve(root,filename.slice(prefix.length));
  if(!filename.startsWith(root+path.sep)||!fs.existsSync(filename)||!fs.statSync(filename).isFile()){res.writeHead(404).end();return;}
  res.writeHead(200,{"content-type":types[path.extname(filename)]||"application/octet-stream","cache-control":"no-store"});
  fs.createReadStream(filename).pipe(res);
});
await new Promise(resolve=>server.listen(0,"127.0.0.1",resolve));
const base="http://127.0.0.1:"+server.address().port+prefix+"tools/prologue-art-lab/";
const results=[];
async function suite(name,driver){
  const browser=await driver.launch();
  const page=await browser.newPage({viewport:{width:2640,height:1500},deviceScaleFactor:1});
  const errors=[];let passed=0;
  page.on("pageerror",e=>errors.push(String(e)));
  page.on("console",m=>{if(m.type()==="error")errors.push(m.text());});
  page.on("response",r=>{if(r.status()>=400)errors.push(r.status()+" "+r.url());});
  const check=(ok,label)=>{assert.ok(ok,name+": "+label);passed++;console.log("pass ["+name+"] "+label);};
  const call=(fn,arg)=>page.evaluate(p=>window.PROLOGUE_LAB[p.fn](p.arg),{fn,arg});
  const state=()=>page.evaluate(()=>window.PROLOGUE_LAB.getState());
  const shot=key=>page.locator("#stage").screenshot({path:path.join(shots,name+"_"+key+".png"),animations:"disabled",timeout:30000});
  try{
    await page.goto(base+"index.html",{waitUntil:"domcontentloaded",timeout:45000});
    await page.waitForFunction(()=>document.body.dataset.ready==="true"||document.body.dataset.ready==="error",null,{timeout:45000});
    check((await page.locator("body").getAttribute("data-ready"))==="true",
      "45 images loaded: "+await page.locator("#loadStatus").textContent());
    await page.locator("#actualPreview").click();
    const initial=await state();
    check(initial.slots===6&&initial.slotPitch===116&&initial.slotGap===20&&initial.sceneScale===4&&initial.inspection===null,"six-slot owner preview, 116px pitch, 20px spacing, 4x native scene");
    check(JSON.stringify(initial.buttonLabels)===JSON.stringify(["INSPECT","NOTES","FILES"]),"original action labels restored");
    const positions=await page.locator(".inventory-slot:visible").evaluateAll(nodes=>nodes.map(n=>parseInt(n.style.left,10)+parseInt(n.parentElement.style.left,10)));
    check(JSON.stringify(positions)===JSON.stringify([92,208,324,440,556,672]),"inventory source positions 92px plus five 116px steps");
    check(await page.locator("#stageNext").evaluate(n=>parseInt(n.style.left,10))===782&&positions[5]+96<782,"right arrow clears the sixth slot");
    const windowBox=await page.locator("#inventoryStrip").evaluate(n=>({
      x:parseInt(n.style.left,10), width:parseInt(n.style.width,10),overflow:getComputedStyle(n).overflow
    }));
    check(windowBox.x===78&&windowBox.width===704&&windowBox.overflow==="hidden",
      "inventory window clips extra slots between arrow bays");
    check(JSON.stringify(initial.inventoryMotion)==='{"slide":true,"durationMs":275,"overshoot":5,"settle":1,"lagMs":2}',
      "original spring, recoil and 2ms per-slot lag values");

    // Click the actual artwork arrow, not just the programmatic setter.
    const forward=await page.evaluate(()=>{
      document.querySelector("#stageNext").click();
      const now=window.PROLOGUE_LAB.getState();
      const outgoing=document.querySelector('.inventory-slot[data-index="0"]');
      return {now,outgoingVisible:!outgoing.hidden,outgoingX:parseInt(outgoing.style.left,10)};
    });
    check(forward.now.inventoryStart===1&&forward.now.inventoryMoving&&
      forward.now.inventoryShift>0&&forward.now.inventoryShift<=116,
      "right arrow starts one-item spring slide, without swapping item art");
    check(forward.outgoingVisible&&forward.outgoingX>=0&&forward.outgoingX<60,
      "previous item stays visible briefly while sliding out");
    await page.waitForFunction(()=>!window.PROLOGUE_LAB.getState().inventoryMoving,null,{timeout:3000});
    check((await state()).inventoryShift===0&&
      await page.locator('.inventory-slot[data-index="0"]').isHidden()&&
      await page.locator(".inventory-slot:visible").count()===6,
      "slide settles with exactly six visible item slots");

    const backward=await page.evaluate(()=>{
      document.querySelector("#stagePrev").click();
      return window.PROLOGUE_LAB.getState();
    });
    check(backward.inventoryStart===0&&backward.inventoryMoving&&backward.inventoryShift<0,
      "left arrow starts reverse-direction spring slide");
    await page.waitForFunction(()=>!window.PROLOGUE_LAB.getState().inventoryMoving,null,{timeout:3000});
    const boundary=await page.evaluate(()=>{
      document.querySelector("#stagePrev").click();
      return window.PROLOGUE_LAB.getState();
    });
    check(boundary.inventoryStart===0&&!boundary.inventoryMoving,"boundary arrow does not start a phantom slide");

    await page.locator("#inventoryNext").click();
    await page.waitForTimeout(60);
    const reversed=await page.evaluate(()=>{
      document.querySelector("#inventoryPrev").click();
      return window.PROLOGUE_LAB.getState();
    });
    check(reversed.inventoryStart===0&&reversed.inventoryMoving&&reversed.inventoryShift<0,
      "rapid reversal carries the residual slide rather than snapping");
    await page.waitForFunction(()=>!window.PROLOGUE_LAB.getState().inventoryMoving,null,{timeout:3000});

    await page.emulateMedia({reducedMotion:"reduce"});
    const reduced=await page.evaluate(()=>{
      window.PROLOGUE_LAB.setInventoryStart(1);
      return window.PROLOGUE_LAB.getState();
    });
    check(reduced.inventoryStart===1&&!reduced.inventoryMoving&&reduced.inventoryShift===0,
      "reduced motion preference disables the slide");
    await page.emulateMedia({reducedMotion:"no-preference"});
    await call("setInventoryStart",0);
    await page.waitForFunction(()=>!window.PROLOGUE_LAB.getState().inventoryMoving,null,{timeout:3000});
    check(await page.locator("#objectiveLabel").evaluate(n=>n.width)===273,"objective typography follows owner's plaque width");
    check(await page.locator("#speechCanvas").evaluate(n=>n.width)===540,"dialogue uses the owner's font canvas geometry");
    check(JSON.stringify(initial.portraitSize)==="[564,278]"&&JSON.stringify(initial.inspectSize)==="[565,451]","approved portrait and inspector dimensions");
    for(const id of ["workplace/applause_station","workplace/corridor","workplace/exit",
      "street/outside_workplace","exposition/entrance","exposition/property_intake",
      "exposition/reception","exposition/facilities_corridor"]){
      await call("setScene",id);
      await page.waitForFunction(()=>{const i=document.querySelector("#sceneImage");return i.complete&&i.naturalWidth===314;});
      check((await state()).scene===id&&await page.locator("#sceneImage").evaluate(i=>i.naturalHeight)===206,
        "original 314x206 scene "+id);
      if(["workplace/applause_station","workplace/corridor","street/outside_workplace",
        "exposition/entrance","exposition/reception"].includes(id))await shot("scene_"+id.replaceAll("/","_"));
    }
    await call("setScene","workplace/corridor");
    check((await state()).activePortrait==="drone-closed","corridor auto-pairs drone");
    const bg=await page.locator("#portraitBackground").getAttribute("src");
    const fg=await page.locator("#portraitForeground").getAttribute("src");
    await shot("drone_closed");
    await call("setPortrait","drone-paper");
    const bg2=await page.locator("#portraitBackground").getAttribute("src");
    const fg2=await page.locator("#portraitForeground").getAttribute("src");
    check(bg===bg2&&fg!==fg2,"both drone poses share a separate corridor background");
    await shot("drone_paper_extended");
    await call("setLayers",{background:false,foreground:true,x:8,y:-4});
    check(await page.locator("#portraitBackground").evaluate(x=>x.hidden),"independent layer toggle");
    await call("setLayers",{background:true,foreground:true,x:0,y:0});
    await call("setSlots",6);await call("setInventoryStart",0);
    check((await state()).items.length===6&&await page.locator(".inventory-slot:visible").count()===6,"six native inventory slots");
    await shot("inventory_first_six");
    await call("setInventoryStart",4);
    await page.waitForFunction(()=>!window.PROLOGUE_LAB.getState().inventoryMoving,null,{timeout:3000});
    check((await state()).items[5]==="wc_key","one-at-a-time scroll reaches approved key with six slots");
    await shot("inventory_last_six");
    await call("setInventoryStart",0);
    await page.waitForFunction(()=>!window.PROLOGUE_LAB.getState().inventoryMoving,null,{timeout:3000});
    await call("setButtonMode","glyph");
    check((await state()).buttonMode==="glyph"&&await page.locator(".utility-glyph:visible").count()===3,"all three approved action glyphs visible");
    await shot("action_glyphs_up");
    await call("setButtonSkin","down");
    check((await state()).buttonSkin==="down"&&(await page.locator("#utilPrev .utility-skin").getAttribute("src")).includes("utility_a_down.png"),"approved physical DOWN sprite loaded");
    await shot("action_glyphs_down");
    await call("setButtonMode","label");await call("setButtonSkin","up");
    check(await page.locator(".utility-label:visible").count()===3,"original bitmap labels restored");
    await shot("action_labels_up");
    for(const id of ["termination_notice","property_claim_ticket","effects_box_full","rubber_band_ball","wc_key"]){
      await call("openItem",id);
      await page.waitForFunction(()=>{const i=document.querySelector("#inspectionImage");return i.complete&&i.naturalWidth===565;});
      check((await state()).inspection===id&&await page.locator("#inspectionImage").evaluate(i=>i.naturalHeight)===451,
        "original 565x451 inspector "+id);
      await shot("inspector_"+id);
    }
    await call("closeInspector");
    await call("setPortrait","auto");await call("setScene","exposition/reception");
    check((await state()).activePortrait==="receptionist"&&(await state()).paired,"approved reception scene and portrait match");
    await shot("approved_reception_continuity");
    check(errors.length===0,"no browser console or asset errors: "+errors.join(" | "));
    results.push({name,passed,failed:0});
  }catch(e){console.error("FAIL ["+name+"] "+e.stack);results.push({name,passed,failed:1,error:String(e.stack)});}
  finally{await browser.close();}
}
try{await suite("chromium",chromium);await suite("firefox",firefox);}
finally{
  await new Promise(resolve=>server.close(resolve));
  const total=results.reduce((n,x)=>n+x.passed,0),failed=results.reduce((n,x)=>n+x.failed,0);
  const report={schema:"cyoa-public-prologue-browser-qa-v1",passed:total,failed,
    screenshotCount:fs.readdirSync(shots).filter(f=>f.endsWith(".png")).length,results};
  fs.writeFileSync(path.join(root,"tools/prologue-art-lab/qa/qa-results.json"),JSON.stringify(report,null,2)+"\n");
  console.log("Public lab browser QA: "+total+" passed; "+failed+" failures; "+report.screenshotCount+" screenshots");
  if(failed)process.exitCode=1;
}
