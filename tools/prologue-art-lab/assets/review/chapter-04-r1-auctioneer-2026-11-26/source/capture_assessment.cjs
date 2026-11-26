// Additional public visual captures; measurements live in the full browser report.
const fs=require('fs'),path=require('path');
const {chromium,firefox}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const [url,out]=process.argv.slice(2);fs.mkdirSync(out,{recursive:true});
(async()=>{
 for(const[name,engine]of Object.entries({chromium,firefox})){
  const browser=await engine.launch({headless:true});const page=await browser.newPage({viewport:{width:2460,height:1600},deviceScaleFactor:1});
  await page.goto(url,{waitUntil:'load',timeout:120000});await page.waitForSelector('article#benchmarks');
  await page.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(i=>i.decode())));
  await page.screenshot({path:path.join(out,name+'-entry-native.png')});
  for(const index of [9,12]){
   const figure=page.locator('section.figure').nth(index);await figure.locator('button[data-scale="4"]').click();
   await figure.locator('img').evaluate(i=>new Promise((resolve,reject)=>{
    const start=Date.now();function check(){if(i.complete&&i.naturalWidth===Number(i.dataset.w)*4)return i.decode().then(resolve,reject);if(Date.now()-start>90000)return reject(Error('4x raster incomplete'));setTimeout(check,40);}check();
   }));
   await figure.screenshot({path:path.join(out,name+'-background-'+index+'-4x.png')});
  }
  await browser.close();
 }
 console.log(JSON.stringify({publicScreenshots:6,browsers:2}));
})().catch(e=>{console.error(e);process.exit(1)});
