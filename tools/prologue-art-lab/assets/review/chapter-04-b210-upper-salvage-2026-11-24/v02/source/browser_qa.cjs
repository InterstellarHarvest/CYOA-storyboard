const fs=require('fs'),path=require('path');
const {chromium,firefox}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const args=process.argv.slice(2),arg=n=>args.includes(n)?args[args.indexOf(n)+1]:undefined;
const root=path.resolve(__dirname,'..'),url=arg('--url')||'file://'+root+'/index.html',out=path.resolve(arg('--out'));
fs.mkdirSync(out,{recursive:true});
async function ready(img,scale){
 await img.evaluate((i,s)=>new Promise((resolve,reject)=>{
  const deadline=Date.now()+90000;
  function poll(){
   if(i.complete&&i.currentSrc===i.src&&i.naturalWidth===Number(i.dataset.w)*s)return i.decode().then(resolve,reject);
   if(Date.now()>deadline)return reject(Error('Raster did not complete: '+i.src));
   setTimeout(poll,40);
  }poll();
 }),scale);
}
(async()=>{
 const results=[];
 for(const [name,engine]of Object.entries({chromium,firefox})){
  const browser=await engine.launch({headless:true});const page=await browser.newPage({viewport:{width:2460,height:1600},deviceScaleFactor:1});const errors=[];
  page.on('pageerror',e=>errors.push(String(e)));await page.goto(url,{waitUntil:'load',timeout:120000});await page.waitForSelector('article#benchmarks');
  await page.locator('img').evaluateAll(async imgs=>Promise.all(imgs.map(i=>i.decode())));
  const figures=await page.locator('section.figure').all();if(figures.length<11)throw Error('Missing comparisons/composites');
  let index=0;
  for(const figure of figures){
   const img=figure.locator('img'),label=await figure.locator('h3').innerText();
   const article=await figure.evaluate(e=>e.closest('article')?.id||'combinations');
   const capture=(label==='v02 candidate'||label==='Nested sinks: before / after'||label==='Rack: before / after');
   const scales=[];
   for(const scale of [1,4]){
    await figure.locator('button[data-scale="'+scale+'"]').click();await ready(img,scale);
    const v=await img.evaluate(i=>({natural:[i.naturalWidth,i.naturalHeight],display:[i.width,i.height],rendered:[i.getBoundingClientRect().width,i.getBoundingClientRect().height],rendering:getComputedStyle(i).imageRendering,src:i.src}));
    if(v.natural.join()!=v.display.join()||v.natural.join()!=v.rendered.join()||!['pixelated','crisp-edges'].includes(v.rendering))throw Error('Fractional/scaled/blurred raster '+label+JSON.stringify(v));
    scales.push({scale,...v});
    if(capture)await figure.screenshot({path:path.join(out,name+'-'+article+'-'+scale+'x.png')});
   }
   if(scales[1].natural[0]!==scales[0].natural[0]*4||scales[1].natural[1]!==scales[0].natural[1]*4)throw Error('Not exact4x '+label);
   results.push({browser:name,article,label,index:index++,native:scales[0],exact4x:scales[1],passed:true});
   await figure.locator('button[data-scale="1"]').click();await ready(img,1);
  }
  if(errors.length)throw Error(errors.join('\n'));await browser.close();
 }
 const report={passed:true,url,browsers:['chromium','firefox'],allCandidateComparisonAndCompositeRastersDecoded:true,allIntegerNativeAnd4xControlsPassed:true,figureChecks:results.length,results};
 fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({passed:true,browsers:2,figureChecks:results.length,url}));
})().catch(e=>{console.error(e);process.exit(1)});
