const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert/strict');
const {chromium,firefox}=require('playwright');
const root=path.resolve(__dirname,'..'),siteRoot=path.dirname(root),remote=process.env.REVIEW_URL;
const out=remote?'/private/tmp/ch4-v08-live-browser':path.join(root,'evidence/browser');fs.mkdirSync(out,{recursive:true});
const prefix='/CYOA-storyboard/tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21/';
const server=http.createServer((req,res)=>{
 const u=new URL(req.url,'http://localhost');if(u.pathname==='/favicon.ico'){res.writeHead(204).end();return}
 if(!u.pathname.startsWith(prefix)){res.writeHead(404).end();return}
 let file=path.resolve(siteRoot,decodeURIComponent(u.pathname.slice(prefix.length))||'v08/index.html');
 if(!file.startsWith(siteRoot+path.sep)){res.writeHead(403).end();return}
 if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
 if(!fs.existsSync(file)){res.writeHead(404).end();return}
 const type={'.html':'text/html','.png':'image/png','.json':'application/json','.md':'text/plain','.tsv':'text/tab-separated-values','.txt':'text/plain','.py':'text/plain','.cjs':'text/plain'}[path.extname(file)]||'application/octet-stream';res.writeHead(200,{'content-type':type});fs.createReadStream(file).pipe(res);
});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const url=remote||'http://127.0.0.1:'+server.address().port+prefix+'v08/',checks=[];
 for(const [name,driver]of [['chromium',chromium],['firefox',firefox]]){
  const executablePath=process.env['PLAYWRIGHT_'+name.toUpperCase()+'_EXECUTABLE'];const browser=await driver.launch({headless:true,...(executablePath?{executablePath}:{})});
  try{
   const p=await browser.newPage({viewport:{width:1920,height:1080},deviceScaleFactor:1}),errors=[];
   p.on('pageerror',e=>errors.push(String(e)));p.on('response',r=>{if(r.status()>=400&&!r.url().endsWith('/favicon.ico'))errors.push(r.status()+' '+r.url())});
   await p.goto(url,{waitUntil:'domcontentloaded',timeout:60000});await p.locator('#portrait').waitFor({timeout:30000});
   await p.locator('img').evaluateAll(async imgs=>{await Promise.all(imgs.map(i=>i.decode()))});
   assert.equal(await p.locator('img.portrait').count(),3);assert.equal(await p.locator('img.frozen').count(),4);assert.match(await p.locator('header').textContent(),/UNSELECTED/);assert.match(await p.locator('.intro').textContent(),/source-derived/);
   assert.match(await p.locator('#batch2').textContent(),/120 canonical nodes/);assert.match(await p.locator('#batch2').textContent(),/five production units/);
   checks.push({browser:name,check:'Final/approved/composite/four frozen PNGs decode; unselected/source-derived status and Batch2 scope explicit',passed:true});
   for(const scale of [4,1]){
    await p.locator('.portrait-scale[data-scale="'+scale+'"]').click();
    await p.waitForFunction(scale=>[...document.querySelectorAll('img.portrait')].every(i=>i.complete&&i.currentSrc===i.src&&i.naturalWidth===564*scale&&i.naturalHeight===278*scale),scale,{timeout:60000});
    assert.deepEqual(await p.locator('img.portrait').first().evaluate(i=>[i.width,i.height]),[564*scale,278*scale]);
   }
   checks.push({browser:name,check:'Portrait and two approved benchmarks use actual native and exact4x rasters',passed:true});
   for(const scale of [4,1]){
    await p.locator('.composite-scale[data-scale="'+scale+'"]').click();await p.waitForFunction(scale=>{const i=document.querySelector('img.composite');return i.complete&&i.currentSrc===i.src&&i.naturalWidth===564*scale&&i.naturalHeight===278*scale},scale,{timeout:60000});
   }
   checks.push({browser:name,check:'Frozen-background composite native/exact4x controls',passed:true});
   for(const id of ['CH4-01','CH4-02','CH4-04','CH4-05']){
    const w=id==='CH4-02'?564:314,h=id==='CH4-02'?278:206;
    for(const scale of [4,1]){
     await p.locator('.frozen-scale[data-target="'+id+'"][data-scale="'+scale+'"]').click();
     await p.waitForFunction(({id,w,h})=>{const i=document.querySelector('img.frozen[data-target="'+id+'"]');return i.complete&&i.currentSrc===i.src&&i.naturalWidth===w&&i.naturalHeight===h},{id,w:w*scale,h:h*scale},{timeout:60000});
    }
    checks.push({browser:name,check:id+' exact preserved candidate and original4x preview render',passed:true});
   }
   await p.locator('#portrait').screenshot({path:path.join(out,name+'-portrait-approved-native.png')});
   await p.locator('#composite').screenshot({path:path.join(out,name+'-frozen-background-composite.png')});
   await p.locator('#batch2').screenshot({path:path.join(out,name+'-batch2-recommendation.png')});
   await p.setViewportSize({width:390,height:844});assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);assert.deepEqual(await p.locator('img.portrait').first().evaluate(i=>[i.getBoundingClientRect().width,i.getBoundingClientRect().height]),[564,278]);
   await p.locator('#portrait').scrollIntoViewIfNeeded();await p.screenshot({path:path.join(out,name+'-mobile.png')});assert.deepEqual(errors,[]);checks.push({browser:name,check:'Mobile preserves native pixels inside scrollable views; no load/runtime errors',passed:true});
  }finally{await browser.close()}
 }
 const report={passed:true,url,checks};fs.writeFileSync(remote?path.join(out,'remote-browser-qa.json'):path.join(root,'evidence/browser-qa.json'),JSON.stringify(report,null,2)+'\n');console.log(checks.length+' v08 browser checks passed in Chromium and Firefox.');
})().catch(e=>{console.error(e);process.exitCode=1}).finally(()=>server.close());
