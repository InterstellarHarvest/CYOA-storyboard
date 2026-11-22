const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert/strict');
const {chromium,firefox}=require('playwright');
const root=path.resolve(__dirname,'..'),siteRoot=path.dirname(root),remote=process.env.REVIEW_URL;
const out=remote?'/private/tmp/ch4-v07-live-browser':path.join(root,'evidence/browser');fs.mkdirSync(out,{recursive:true});
const prefix='/CYOA-storyboard/tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21/';
const server=http.createServer((req,res)=>{
 const u=new URL(req.url,'http://localhost');if(u.pathname==='/favicon.ico'){res.writeHead(204).end();return}
 if(!u.pathname.startsWith(prefix)){res.writeHead(404).end();return}
 let file=path.resolve(siteRoot,decodeURIComponent(u.pathname.slice(prefix.length))||'v07/index.html');
 if(!file.startsWith(siteRoot+path.sep)){res.writeHead(403).end();return}
 if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
 if(!fs.existsSync(file)){res.writeHead(404).end();return}
 const type={'.html':'text/html','.png':'image/png','.json':'application/json','.md':'text/plain','.txt':'text/plain','.py':'text/plain','.cjs':'text/plain'}[path.extname(file)]||'application/octet-stream';res.writeHead(200,{'content-type':type});fs.createReadStream(file).pipe(res);
});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const url=remote||'http://127.0.0.1:'+server.address().port+prefix+'v07/',checks=[];
 for(const [name,driver]of [['chromium',chromium],['firefox',firefox]]){
  const executablePath=process.env['PLAYWRIGHT_'+name.toUpperCase()+'_EXECUTABLE'];const browser=await driver.launch({headless:true,...(executablePath?{executablePath}:{})});
  try{
   const p=await browser.newPage({viewport:{width:1440,height:1050},deviceScaleFactor:1}),errors=[];
   p.on('pageerror',e=>errors.push(String(e)));p.on('response',r=>{if(r.status()>=400&&!r.url().endsWith('/favicon.ico'))errors.push(r.status()+' '+r.url())});
   await p.goto(url,{waitUntil:'domcontentloaded',timeout:60000});await p.locator('#CH4-04').waitFor({timeout:30000});assert.equal(await p.locator('article').count(),2);
   await p.locator('img').evaluateAll(async imgs=>{await Promise.all(imgs.map(i=>i.decode()))});assert.match(await p.locator('header').textContent(),/UNSELECTED/);assert.match(await p.locator('.intro').textContent(),/scene NPC pixels only/);
   checks.push({browser:name,check:'All candidate/history/approved/detail images decode; NPC-only scope explicit',passed:true});
   await p.locator('#npc-native').click();await p.waitForFunction(()=>{const i=document.querySelector('.npc-sheet');return i.complete&&i.currentSrc===i.src&&i.naturalWidth===456});
   assert.deepEqual(await p.locator('.npc-sheet').evaluate(i=>[i.width,i.height]),[456,372]);
   await p.locator('#npc-four').click();await p.waitForFunction(()=>{const i=document.querySelector('.npc-sheet');return i.complete&&i.currentSrc===i.src&&i.naturalWidth===1824});
   assert.deepEqual(await p.locator('.npc-sheet').evaluate(i=>[i.width,i.height,i.naturalWidth,i.naturalHeight]),[1824,1488,1824,1488]);
   checks.push({browser:name,check:'NPC before/after sheet uses exact original and4x raster pixels',passed:true});
   for(const id of ['CH4-04','CH4-05']){
    const a=p.locator('.candidate[data-target="'+id+'"]');assert.deepEqual(await a.evaluate(i=>[i.width,i.height,i.naturalWidth,i.naturalHeight]),[314,206,314,206]);
    await p.locator('.scale[data-target="'+id+'"][data-scale="4"]').click();
    for(const role of ['candidate','previous','benchmark'])await p.waitForFunction(({role,id})=>{const i=document.querySelector('.'+role+'[data-target="'+id+'"]');return i.complete&&i.currentSrc===i.src&&i.naturalWidth===1256&&i.naturalHeight===824},{role,id},{timeout:60000});
    await a.screenshot({path:path.join(out,name+'-'+id+'-4x.png')});
    await p.locator('.scale[data-target="'+id+'"][data-scale="1"]').click();await p.waitForFunction(id=>{const i=document.querySelector('.candidate[data-target="'+id+'"]');return i.complete&&i.currentSrc===i.src&&i.naturalWidth===314},id);
    assert.deepEqual(await a.evaluate(i=>[i.getBoundingClientRect().width,i.getBoundingClientRect().height]),[314,206]);checks.push({browser:name,check:id+' v06/v07/approved panels render native and exact4x',passed:true});
   }
   await p.locator('#CH4-04').screenshot({path:path.join(out,name+'-native-room-comparison.png')});
   await p.setViewportSize({width:390,height:844});assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);assert.equal(await p.locator('.candidate[data-target="CH4-04"]').evaluate(i=>i.getBoundingClientRect().width),314);
   await p.locator('#CH4-04').scrollIntoViewIfNeeded();await p.screenshot({path:path.join(out,name+'-mobile.png')});assert.deepEqual(errors,[]);checks.push({browser:name,check:'Mobile preserves native pixels with internal scrolling; no runtime/load errors',passed:true});
  }finally{await browser.close()}
 }
 const report={passed:true,url,checks};fs.writeFileSync(remote?path.join(out,'remote-browser-qa.json'):path.join(root,'evidence/browser-qa.json'),JSON.stringify(report,null,2)+'\n');console.log(checks.length+' v07 browser checks passed in Chromium and Firefox.');
})().catch(e=>{console.error(e);process.exitCode=1}).finally(()=>server.close());
