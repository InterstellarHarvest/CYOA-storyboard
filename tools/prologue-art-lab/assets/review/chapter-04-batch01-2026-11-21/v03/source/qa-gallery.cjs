const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert/strict');
const {chromium,firefox}=require('playwright');
const root=path.resolve(__dirname,'..'),siteRoot=path.dirname(root),remote=process.env.REVIEW_URL;
const out=remote?'/private/tmp/ch4-v03-live-browser':path.join(root,'evidence/browser');fs.mkdirSync(out,{recursive:true});
const prefix='/CYOA-storyboard/tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21/';
const server=http.createServer((req,res)=>{
 const u=new URL(req.url,'http://localhost');if(u.pathname==='/favicon.ico'){res.writeHead(204).end();return}
 if(!u.pathname.startsWith(prefix)){res.writeHead(404).end();return}
 let file=path.resolve(siteRoot,decodeURIComponent(u.pathname.slice(prefix.length))||'v03/index.html');
 if(!file.startsWith(siteRoot+path.sep)){res.writeHead(403).end();return}
 if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
 if(!fs.existsSync(file)){res.writeHead(404).end();return}
 const type={'.html':'text/html','.json':'application/json','.png':'image/png','.txt':'text/plain','.py':'text/plain','.cjs':'text/plain'}[path.extname(file)]||'application/octet-stream';
 res.writeHead(200,{'content-type':type});fs.createReadStream(file).pipe(res);
});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const url=remote||'http://127.0.0.1:'+server.address().port+prefix+'v03/',checks=[];
 for(const [name,driver]of [['chromium',chromium],['firefox',firefox]]){
  const executablePath=process.env['PLAYWRIGHT_'+name.toUpperCase()+'_EXECUTABLE'];
  const browser=await driver.launch({headless:true,...(executablePath?{executablePath}:{})});
  try{
   const p=await browser.newPage({viewport:{width:1440,height:1050},deviceScaleFactor:1});
   const errors=[];p.on('pageerror',e=>errors.push(String(e)));p.on('response',r=>{if(r.status()>=400&&!r.url().endsWith('/favicon.ico'))errors.push(r.status()+' '+r.url())});
   await p.goto(url,{waitUntil:'domcontentloaded',timeout:60000});await p.locator('.scale[data-target="CH4-01"]').first().waitFor({timeout:30000});
   assert.equal(await p.locator('article').count(),3);
   await p.evaluate(()=>document.querySelectorAll('details').forEach(d=>d.open=true));
   await p.locator('img').evaluateAll(async imgs=>{await Promise.all(imgs.map(async i=>{i.loading='eager';await i.decode();if(!i.naturalWidth)throw Error('Image decode '+i.src)}))});
   assert.deepEqual(errors,[]);checks.push({browser:name,check:'all candidate/history/canonical/concept images decode',imageCount:await p.locator('img').count(),passed:true});
   await p.evaluate(()=>document.querySelectorAll('details').forEach(d=>d.open=false));
   for(const id of ['CH4-01','CH4-02','CH4-03']){
    const w=id==='CH4-01'?314:564,h=id==='CH4-01'?206:278;
    const a=p.locator('.candidate[data-target="'+id+'"]'),old=p.locator('.previous[data-target="'+id+'"]');
    assert.deepEqual(await a.evaluate(i=>[i.width,i.height,i.naturalWidth,i.naturalHeight]),[w,h,w,h]);
    await p.locator('.scale[data-target="'+id+'"][data-scale="4"]').click();
    for(const i of [a,old]){await i.evaluate(i=>i.decode());assert.deepEqual(await i.evaluate(i=>[i.width,i.height,i.naturalWidth,i.naturalHeight]),[w*4,h*4,w*4,h*4])}
    if(id==='CH4-01'){
     await p.locator('#benchmark').selectOption({label:'Control Tower'});
     const ref=p.locator('.benchmark[data-target="CH4-01"]');await ref.evaluate(i=>i.decode());assert.match(await ref.getAttribute('src'),/control-tower-4x\.png$/);
     await a.screenshot({path:path.join(out,name+'-lobby-4x.png')});
    }
    await p.locator('.scale[data-target="'+id+'"][data-scale="1"]').click();await a.evaluate(i=>i.decode());
    assert.deepEqual(await a.evaluate(i=>[i.getBoundingClientRect().width,i.getBoundingClientRect().height]),[w,h]);
    checks.push({browser:name,check:id+' native and exact 4x v02/v03 comparisons',passed:true});
   }
   await p.locator('#CH4-01').screenshot({path:path.join(out,name+'-lobby-native-card.png')});
   await p.locator('#composite').screenshot({path:path.join(out,name+'-portrait-comparisons.png')});
   await p.setViewportSize({width:390,height:844});
   assert.deepEqual(await p.locator('.candidate[data-target="CH4-01"]').evaluate(i=>[i.getBoundingClientRect().width,i.getBoundingClientRect().height]),[314,206]);
   assert.deepEqual(await p.locator('.candidate[data-target="CH4-03"]').evaluate(i=>[i.getBoundingClientRect().width,i.getBoundingClientRect().height]),[564,278]);
   await p.locator('#CH4-01').scrollIntoViewIfNeeded();await p.screenshot({path:path.join(out,name+'-mobile.png')});
   assert.deepEqual(errors,[]);checks.push({browser:name,check:'mobile retains native pixels with scrollable comparisons; no runtime/load errors',passed:true});
  }finally{await browser.close()}
 }
 const report={passed:true,url,checks};fs.writeFileSync(remote?path.join(out,'remote-browser-qa.json'):path.join(root,'evidence/browser-qa.json'),JSON.stringify(report,null,2)+'\n');console.log(checks.length+' v03 browser checks passed in Chromium and Firefox.');
})().catch(e=>{console.error(e);process.exitCode=1}).finally(()=>server.close());
