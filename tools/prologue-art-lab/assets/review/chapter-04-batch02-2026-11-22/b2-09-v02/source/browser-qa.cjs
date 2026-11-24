// Decode actual gallery rasters and exercise native/exact4x controls in both engines.
const fs=require('fs'),path=require('path');
const {chromium,firefox}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const args=process.argv.slice(2),arg=n=>args.includes(n)?args[args.indexOf(n)+1]:undefined;
const root=path.resolve(__dirname,'..'),url=arg('--url')||'file://'+root+'/index.html',out=path.resolve(arg('--out')||path.join(root,'evidence/browser-local'));
fs.mkdirSync(out,{recursive:true});
async function ready(img,scale){
 // decode() can resolve the previously displayed raster just after a source
 // switch. Require the requested currentSrc and native size before decoding.
 await img.evaluate((i,s)=>new Promise((resolve,reject)=>{
  const deadline=Date.now()+60000;
  function poll(){
   if(i.complete&&i.currentSrc===i.src&&i.naturalWidth===Number(i.dataset.w)*s)return i.decode().then(resolve,reject);
   if(Date.now()>deadline)return reject(Error('Requested raster did not complete: '+i.src));
   setTimeout(poll,40);
  }poll();
 }),scale);
}
(async()=>{
 const results=[];
 for(const [name,engine]of Object.entries({chromium,firefox})){
  const browser=await engine.launch({headless:true});const page=await browser.newPage({viewport:{width:2400,height:1500},deviceScaleFactor:1});const errors=[];
  page.on('pageerror',e=>errors.push(String(e)));await page.goto(url,{waitUntil:'load',timeout:120000});
  await page.waitForSelector('article#CH4-B2-51-trade');
  await page.locator('img').evaluateAll(async imgs=>{await Promise.all(imgs.map(i=>i.decode()));});
  const native=await page.locator('article').count();if(native!==8)throw Error('Expected eight candidate frames, got '+native);
  for(const article of await page.locator('article').all()){
   const id=await article.getAttribute('id'),figure=article.locator('section.figure').first(),img=figure.locator('img');
   await figure.locator('button[data-scale="1"]').click();await ready(img,1);
   const one=await img.evaluate(i=>({natural:[i.naturalWidth,i.naturalHeight],display:[i.width,i.height],rendering:getComputedStyle(i).imageRendering,src:i.src}));
   if(one.natural.join()!=one.display.join()||!['pixelated','crisp-edges'].includes(one.rendering))throw Error('Bad native presentation '+id);
   await figure.screenshot({path:path.join(out,name+'-'+id+'-native.png')});
   await figure.locator('button[data-scale="4"]').click();await ready(img,4);
   const four=await img.evaluate(i=>({natural:[i.naturalWidth,i.naturalHeight],display:[i.width,i.height],src:i.src}));
   if(four.natural[0]!==one.natural[0]*4||four.natural[1]!==one.natural[1]*4||four.display.join()!=four.natural.join())throw Error('Bad 4x '+id+' '+JSON.stringify({one,four,buttons:await figure.locator('button').evaluateAll(bs=>bs.map(b=>b.outerHTML))}));
   await figure.screenshot({path:path.join(out,name+'-'+id+'-4x.png')});
   // The paired approved benchmark uses the same controls and fully decodes.
   const benchmark=article.locator('section.figure').nth(1);await benchmark.locator('button[data-scale="4"]').click();await ready(benchmark.locator('img'),4);
   await benchmark.locator('button[data-scale="1"]').click();await ready(benchmark.locator('img'),1);
   // Exercise every Chapter2/3 benchmark and approved-context composite too.
   for(const other of (await article.locator('section.figure').all()).slice(2))for(const scale of [4,1]){
    const raster=other.locator('img');await other.locator('button[data-scale="'+scale+'"]').click();await ready(raster,scale);
    const size=await raster.evaluate(i=>[i.naturalWidth,i.naturalHeight,i.width,i.height]);if(size[0]!==size[2]||size[1]!==size[3])throw Error('Noninteger reference/composite display '+id);
   }
   await figure.locator('button[data-scale="1"]').click();await ready(img,1);results.push({browser:name,id,native:one,exact4x:four,pairedBenchmarkDecoded:true,passed:true});
  }
  if(errors.length)throw Error(errors.join('\n'));await browser.close();
 }
 const report={passed:true,url,browsers:['chromium','firefox'],assetsPerBrowser:8,allRastersDecoded:true,allNativeAnd4xControlsPassed:true,results};
 fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({passed:true,url,browsers:2,candidateChecks:results.length}));
})().catch(e=>{console.error(e);process.exit(1)});
