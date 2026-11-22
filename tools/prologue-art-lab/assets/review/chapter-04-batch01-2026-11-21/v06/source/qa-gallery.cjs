const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert/strict');
const {chromium,firefox}=require('playwright');
const root=path.resolve(__dirname,'..'),siteRoot=path.dirname(root),remote=process.env.REVIEW_URL;
const out=remote?'/private/tmp/ch4-v06-live-browser':path.join(root,'evidence/browser');fs.mkdirSync(out,{recursive:true});
const prefix='/CYOA-storyboard/tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21/';
const server=http.createServer((req,res)=>{
 const u=new URL(req.url,'http://localhost');if(u.pathname==='/favicon.ico'){res.writeHead(204).end();return}
 if(!u.pathname.startsWith(prefix)){res.writeHead(404).end();return}
 let file=path.resolve(siteRoot,decodeURIComponent(u.pathname.slice(prefix.length))||'v06/index.html');
 if(!file.startsWith(siteRoot+path.sep)){res.writeHead(403).end();return}
 if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
 if(!fs.existsSync(file)){res.writeHead(404).end();return}
 const type={'.html':'text/html','.json':'application/json','.png':'image/png','.txt':'text/plain','.md':'text/plain','.py':'text/plain','.cjs':'text/plain'}[path.extname(file)]||'application/octet-stream';
 res.writeHead(200,{'content-type':type});fs.createReadStream(file).pipe(res);
});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const url=remote||'http://127.0.0.1:'+server.address().port+prefix+'v06/',checks=[];
 for(const [name,driver]of [['chromium',chromium],['firefox',firefox]]){
  const executablePath=process.env['PLAYWRIGHT_'+name.toUpperCase()+'_EXECUTABLE'];const browser=await driver.launch({headless:true,...(executablePath?{executablePath}:{})});
  try{
   const p=await browser.newPage({viewport:{width:1920,height:1080},deviceScaleFactor:1}),errors=[];
   p.on('pageerror',e=>errors.push(String(e)));p.on('response',r=>{if(r.status()>=400&&!r.url().endsWith('/favicon.ico'))errors.push(r.status()+' '+r.url())});
   await p.goto(url,{waitUntil:'domcontentloaded',timeout:60000});await p.locator('#CH4-03').waitFor({timeout:30000});
   assert.equal(await p.locator('article').count(),3);
   await p.evaluate(()=>document.querySelectorAll('details').forEach(d=>d.open=true));
   await p.locator('img').evaluateAll(async imgs=>{await Promise.all(imgs.map(async i=>{i.loading='eager';await i.decode();if(!i.naturalWidth)throw Error('Image decode '+i.src)}))});
   await p.evaluate(()=>document.querySelectorAll('details').forEach(d=>d.open=false));
   assert.match(await p.locator('.intro').textContent(),/source-derived NPCs/);assert.match(await p.locator('header').textContent(),/UNSELECTED/);
   checks.push({browser:name,check:'All candidate/history/approved/original/composite images decode; methods and unselected status explicit',passed:true});
   for(const id of ['CH4-03','CH4-04','CH4-05']){
    const w=id==='CH4-03'?564:314,h=id==='CH4-03'?278:206;
    const a=p.locator('.candidate[data-target="'+id+'"]');assert.deepEqual(await a.evaluate(i=>[i.width,i.height,i.naturalWidth,i.naturalHeight]),[w,h,w,h]);
    await p.locator('.scale[data-target="'+id+'"][data-scale="4"]').click();
    for(const role of ['candidate','previous','benchmark']){
     await p.waitForFunction(({selector,w,h})=>{const i=document.querySelector(selector);return i.complete&&i.currentSrc===i.src&&i.naturalWidth===w&&i.naturalHeight===h},{selector:'.'+role+'[data-target="'+id+'"]',w:w*4,h:h*4},{timeout:60000});
    }
    const select=p.locator('.benchmark-select[data-target="'+id+'"]');
    await select.selectOption({label:id==='CH4-03'?'Pavilion presenter':id==='CH4-04'?'Control Tower':'Bureau'});
    await p.waitForFunction(({id,w,h})=>{const i=document.querySelector('.benchmark[data-target="'+id+'"]');return i.complete&&i.currentSrc===i.src&&i.naturalWidth===w&&i.naturalHeight===h},{id,w:w*4,h:h*4},{timeout:60000});
    await a.screenshot({path:path.join(out,name+'-'+id+'-4x.png')});
    await p.locator('.scale[data-target="'+id+'"][data-scale="1"]').click();
    await p.waitForFunction(({id,w,h})=>{const i=document.querySelector('.candidate[data-target="'+id+'"]');return i.complete&&i.currentSrc===i.src&&i.naturalWidth===w&&i.naturalHeight===h},{id,w,h});
    assert.deepEqual(await a.evaluate(i=>[i.getBoundingClientRect().width,i.getBoundingClientRect().height]),[w,h]);
    checks.push({browser:name,check:id+' native/exact4x images, previous comparison and alternate approved benchmark work',passed:true});
   }
   await p.locator('#CH4-03').screenshot({path:path.join(out,name+'-portrait-native-comparison.png')});
   await p.locator('#CH4-04').screenshot({path:path.join(out,name+'-restroom-native-comparison.png')});
   await p.locator('#CH4-05').screenshot({path:path.join(out,name+'-ballroom-native-comparison.png')});
   await p.locator('#composite').screenshot({path:path.join(out,name+'-frozen-background-composite.png')});
   await p.setViewportSize({width:390,height:844});
   for(const id of ['CH4-03','CH4-04','CH4-05'])assert.equal(await p.locator('.candidate[data-target="'+id+'"]').evaluate(i=>i.getBoundingClientRect().width),id==='CH4-03'?564:314);
   assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
   await p.locator('#CH4-04').scrollIntoViewIfNeeded();await p.screenshot({path:path.join(out,name+'-mobile.png')});
   assert.deepEqual(errors,[]);checks.push({browser:name,check:'Mobile retains native pixels inside scrollable viewports; no page overflow or runtime/load errors',passed:true});
  }finally{await browser.close()}
 }
 const report={passed:true,url,checks};fs.writeFileSync(remote?path.join(out,'remote-browser-qa.json'):path.join(root,'evidence/browser-qa.json'),JSON.stringify(report,null,2)+'\n');console.log(checks.length+' v06 browser checks passed in Chromium and Firefox.');
})().catch(e=>{console.error(e);process.exitCode=1}).finally(()=>server.close());
