const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert/strict');
const {chromium,firefox}=require('playwright');
const root=path.resolve(__dirname,'..'),siteRoot=path.dirname(root),remote=process.env.REVIEW_URL;
const out=remote?'/private/tmp/ch4-portrait-study-01-live-browser':path.join(root,'evidence/browser');fs.mkdirSync(out,{recursive:true});
const prefix='/CYOA-storyboard/tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21/';
const server=http.createServer((req,res)=>{
 const u=new URL(req.url,'http://localhost');if(u.pathname==='/favicon.ico'){res.writeHead(204).end();return}
 if(!u.pathname.startsWith(prefix)){res.writeHead(404).end();return}
 let file=path.resolve(siteRoot,decodeURIComponent(u.pathname.slice(prefix.length))||'portrait-study-01/index.html');
 if(!file.startsWith(siteRoot+path.sep)){res.writeHead(403).end();return}
 if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
 if(!fs.existsSync(file)){res.writeHead(404).end();return}
 const type={'.html':'text/html','.json':'application/json','.png':'image/png','.txt':'text/plain','.md':'text/plain','.py':'text/plain','.cjs':'text/plain'}[path.extname(file)]||'application/octet-stream';
 res.writeHead(200,{'content-type':type});fs.createReadStream(file).pipe(res);
});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const url=remote||'http://127.0.0.1:'+server.address().port+prefix+'portrait-study-01/',checks=[];
 for(const [name,driver]of [['chromium',chromium],['firefox',firefox]]){
  const executablePath=process.env['PLAYWRIGHT_'+name.toUpperCase()+'_EXECUTABLE'];
  const browser=await driver.launch({headless:true,...(executablePath?{executablePath}:{})});
  try{
   const p=await browser.newPage({viewport:{width:1440,height:1050},deviceScaleFactor:1});
   const errors=[];p.on('pageerror',e=>errors.push(String(e)));p.on('response',r=>{if(r.status()>=400&&!r.url().endsWith('/favicon.ico'))errors.push(r.status()+' '+r.url())});
   await p.goto(url,{waitUntil:'domcontentloaded',timeout:60000});await p.locator('#raster-test').waitFor({timeout:30000});
   assert.equal(await p.locator('article').count(),6);
   await p.locator('img').evaluateAll(async imgs=>{await Promise.all(imgs.map(async i=>{await i.decode();if(!i.naturalWidth)throw Error('Image decode '+i.src)}))});
   assert.match(await p.locator('#decision').textContent(),/No new native portrait candidate is claimed/);
   assert.match(await p.locator('#frozen').textContent(),/UNSELECTED/);
   assert.deepEqual(errors,[]);checks.push({browser:name,check:'All six actual-art/reference PNGs decode; failed native gate and environment freeze explicit',passed:true});
   for(const id of ['raster-test','frontal-reference','v05-auctioneer','receptionist','pavilion-attendant','pavilion-presenter']){
    const sourceSized=['raster-test','frontal-reference'].includes(id),w=sourceSized?1785:564,h=sourceSized?881:278;
    const img=p.locator('.artwork[data-target="'+id+'"]');
    assert.deepEqual(await img.evaluate(i=>[i.width,i.height,i.naturalWidth,i.naturalHeight]),[w,h,w,h]);
    await p.locator('.scale[data-target="'+id+'"][data-scale="4"]').click();
    await p.waitForFunction(({id,w,h})=>{const i=document.querySelector('.artwork[data-target="'+id+'"]');return i.complete&&i.currentSrc===i.src&&i.naturalWidth===w&&i.naturalHeight===h},{id,w:w*4,h:h*4},{timeout:60000});
    assert.deepEqual(await img.evaluate(i=>[i.width,i.height,i.naturalWidth,i.naturalHeight]),[w*4,h*4,w*4,h*4]);
    await p.locator('.scale[data-target="'+id+'"][data-scale="1"]').click();
    await p.waitForFunction(({id,w,h})=>{const i=document.querySelector('.artwork[data-target="'+id+'"]');return i.complete&&i.currentSrc===i.src&&i.naturalWidth===w&&i.naturalHeight===h},{id,w,h});
    assert.deepEqual(await img.evaluate(i=>[i.getBoundingClientRect().width,i.getBoundingClientRect().height]),[w,h]);
    checks.push({browser:name,check:id+' uses actual original pixels and exact4x; no CSS fit/downsample',passed:true});
   }
   await p.locator('#decision').screenshot({path:path.join(out,name+'-method-decision.png')});
   await p.locator('#raster-test').screenshot({path:path.join(out,name+'-source-test-card.png')});
   await p.locator('#v05-auctioneer').screenshot({path:path.join(out,name+'-v05-card.png')});
   await p.locator('#receptionist').screenshot({path:path.join(out,name+'-receptionist-card.png')});
   await p.setViewportSize({width:390,height:844});
   for(const id of ['raster-test','v05-auctioneer']){
    assert.deepEqual(await p.locator('.artwork[data-target="'+id+'"]').evaluate(i=>[i.getBoundingClientRect().width,i.getBoundingClientRect().height]),id==='raster-test'?[1785,881]:[564,278]);
   }
   assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
   await p.locator('#decision').scrollIntoViewIfNeeded();await p.screenshot({path:path.join(out,name+'-mobile.png')});
   assert.deepEqual(errors,[]);checks.push({browser:name,check:'Mobile scrolls inside art viewport without shrinking art or page overflow; no load/runtime errors',passed:true});
  }finally{await browser.close()}
 }
 const report={passed:true,url,newNativeCandidateExists:false,checks};fs.writeFileSync(remote?path.join(out,'remote-browser-qa.json'):path.join(root,'evidence/browser-qa.json'),JSON.stringify(report,null,2)+'\n');console.log(checks.length+' study gallery browser checks passed in Chromium and Firefox.');
})().catch(e=>{console.error(e);process.exitCode=1}).finally(()=>server.close());
