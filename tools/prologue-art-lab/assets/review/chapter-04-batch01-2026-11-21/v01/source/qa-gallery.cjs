const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert/strict');
const {chromium,firefox}=require('playwright');
const root=path.resolve(__dirname,'..'),out=path.join(root,'evidence/browser');
fs.mkdirSync(out,{recursive:true});
const prefix='/CYOA-storyboard/tools/prologue-art-lab/assets/review/chapter-04-batch01-2026-11-21/v01/';
const server=http.createServer((req,res)=>{
 const url=new URL(req.url,'http://localhost');
 if(url.pathname==='/favicon.ico'){res.writeHead(204).end();return;}
 if(!url.pathname.startsWith(prefix)){res.writeHead(404).end();return;}
 let file=path.resolve(root,decodeURIComponent(url.pathname.slice(prefix.length))||'index.html');
 if(!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}
 if(!fs.existsSync(file)){res.writeHead(404).end();return;}
 const type={'.html':'text/html','.json':'application/json','.png':'image/png','.txt':'text/plain','.py':'text/plain','.cjs':'text/plain'}[path.extname(file)]||'application/octet-stream';
 res.writeHead(200,{'content-type':type});fs.createReadStream(file).pipe(res);
});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const url='http://127.0.0.1:'+server.address().port+prefix,results=[];
 for(const [name,driver] of [['chromium',chromium],['firefox',firefox]]){
  const executablePath=process.env['PLAYWRIGHT_'+name.toUpperCase()+'_EXECUTABLE'];
  const browser=await driver.launch({headless:true,...(executablePath?{executablePath}:{})});
  try{
   const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});
   const errors=[];page.on('pageerror',e=>errors.push(String(e)));page.on('response',r=>{if(r.status()>=400)errors.push(r.status()+' '+r.url())});
   await page.goto(url);await page.locator('h1').waitFor();
   assert.equal(await page.locator('article').count(),5);
   await page.evaluate(()=>document.querySelectorAll('details').forEach(d=>d.open=true));
   await page.locator('img').evaluateAll(async imgs=>{for(const i of imgs){i.loading='eager';if(!i.complete)await new Promise((ok,no)=>{i.onload=ok;i.onerror=no});if(!i.naturalWidth)throw Error('Image did not decode: '+i.src)}});
   assert.deepEqual(errors,[]);results.push({browser:name,check:'all five cards and every reference/image decode at Pages-style prefix',passed:true});
   await page.evaluate(()=>document.querySelectorAll('details').forEach(d=>d.open=false));
   for(const id of ['CH4-01','CH4-04','CH4-05']){
    const a=page.locator('.candidate[data-id="'+id+'"]');
    assert.deepEqual(await a.evaluate(i=>[i.width,i.height,i.naturalWidth,i.naturalHeight]),[314,206,314,206]);
    await page.locator('.scale[data-target="'+id+'"][data-scale="4"]').click();
    await a.evaluate(i=>i.decode());
    assert.deepEqual(await a.evaluate(i=>[i.width,i.height,i.naturalWidth,i.naturalHeight]),[1256,824,1256,824]);
    const ref=page.locator('.comparison[data-id="'+id+'"]');
    await page.locator('.benchmark[data-target="'+id+'"]').selectOption({label:'spore garden'});await ref.evaluate(i=>i.decode());
    assert.match(await ref.getAttribute('src'),/spore_garden-4x\.png$/);
    assert.deepEqual(await ref.evaluate(i=>[i.width,i.height,i.naturalWidth,i.naturalHeight]),[1256,824,1256,824]);
    if(id==='CH4-01')await a.screenshot({path:path.join(out,name+'-lobby-4x.png')});
    await page.locator('.scale[data-target="'+id+'"][data-scale="1"]').click();
    await a.evaluate(i=>i.decode());
    assert.deepEqual(await a.evaluate(i=>[i.getBoundingClientRect().width,i.getBoundingClientRect().height]),[314,206]);
    results.push({browser:name,check:id+' native/4x switch, benchmark selector and exact rendered dimensions',passed:true});
   }
   await page.locator('#CH4-03').screenshot({path:path.join(out,name+'-portrait-card.png')});
   await page.setViewportSize({width:390,height:844});
   assert.deepEqual(await page.locator('.candidate[data-id="CH4-01"]').evaluate(i=>[i.getBoundingClientRect().width,i.getBoundingClientRect().height]),[314,206]);
   await page.locator('#CH4-01').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,name+'-mobile.png')});
   assert.deepEqual(errors,[]);results.push({browser:name,check:'mobile preserves native pixels and no load/runtime errors',passed:true});
  }finally{await browser.close()}
 }
 fs.writeFileSync(path.join(root,'evidence/browser-qa.json'),JSON.stringify({passed:true,checks:results},null,2)+'\n');
 console.log(results.length+' gallery browser checks passed in Chromium and Firefox.');
})().catch(e=>{console.error(e);process.exitCode=1}).finally(()=>server.close());
