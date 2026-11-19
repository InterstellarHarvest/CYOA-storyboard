const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=process.env.QA_OUTPUT_DIR||__dirname;
const url=process.env.GALLERY_URL||'http://127.0.0.1:8775/v06-314-regeneration-2026-11-19/';
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 try{
  fs.mkdirSync(path.join(root,'screenshots'),{recursive:true});
  const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});
  const errors=[],failedRequests=[],checks=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('requestfailed',r=>failedRequests.push(r.url()));
  await page.goto(url,{waitUntil:'networkidle'});
  await page.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(i=>i.decode())));
  assert.equal(await page.locator('.candidate').count(),2);checks.push('Exactly two new main-scene candidate cards');
  async function metrics(scale){
   const data=await page.locator('img.art').evaluateAll(imgs=>imgs.map(i=>({w:i.width,h:i.height,nw:i.naturalWidth,nh:i.naturalHeight,baseW:Number(i.dataset.w),baseH:Number(i.dataset.h),rendering:getComputedStyle(i).imageRendering})));
   assert.ok(data.every(i=>i.nw===i.baseW&&i.nh===i.baseH&&i.w===i.baseW*scale&&i.h===i.baseH*scale));
   assert.ok(data.every(i=>['pixelated','crisp-edges'].includes(i.rendering)));
  }
  await metrics(1);checks.push('Candidates, side-by-side proofs, density comparisons and unchanged identity references load at exact 1x dimensions');
  await page.screenshot({path:path.join(root,'screenshots/gallery-desktop-1x.png')});
  await page.locator('[data-scale="4"]').click();await metrics(4);
  checks.push('4x control applies exact integer scale to every displayed image');
  for(const id of ['CH3-A01-restroom-v06','CH3-A04-verification-v06']){
   await page.locator('#'+id+' .viewport').first().scrollIntoViewIfNeeded();
   await page.screenshot({path:path.join(root,'screenshots/'+id+'-desktop-4x.png')});
   const sides=page.locator('#'+id+' .viewport').nth(1);
   assert.ok(await sides.evaluate(n=>n.scrollWidth>n.clientWidth));
  }
  checks.push('Large comparison rows scroll inside bounded containers without fit-to-width scaling');
  await page.locator('[data-scale="1"]').click();await metrics(1);
  await page.locator('#CH3-A04-verification-v06 .viewport').nth(2).scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(root,'screenshots/approved-density-comparison-1x.png')});
  await page.setViewportSize({width:390,height:844});await page.goto(url,{waitUntil:'networkidle'});
  await page.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(i=>i.decode())));await metrics(1);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await page.screenshot({path:path.join(root,'screenshots/gallery-mobile-1x.png')});
  checks.push('390px mobile layout has no horizontal document overflow; artwork remains integer scaled');
  for(const name of ['manifest.json','qa.json','sources/generation-records.json','sources/reference-manifest.json']){
   const response=await page.request.get(new URL(name,url).href);assert.ok(response.ok());
  }
  assert.equal(errors.length,0);assert.equal(failedRequests.length,0);
  checks.push('Records load and browser has no page exceptions or failed requests');
  const report={result:'PASS',url,browser:await browser.version(),checks,errors,failedRequests,scope:'Gallery behavior only. Does not certify native-grid authorship or select/approve artwork.'};
  fs.writeFileSync(path.join(root,'browser-qa.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
