const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=process.env.QA_OUTPUT_DIR||__dirname;
const url=process.env.GALLERY_URL||'http://127.0.0.1:8780/tools/prologue-art-lab/assets/review/chapter-03-batch03-2026-11-19/v01/';
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 try{
  fs.mkdirSync(path.join(root,'screenshots'),{recursive:true});
  const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});const errors=[],failed=[],checks=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('requestfailed',r=>failed.push(r.url()));
  await page.goto(url,{waitUntil:'networkidle'});await page.locator('img').evaluateAll(xs=>Promise.all(xs.map(i=>i.decode())));
  assert.equal(await page.locator('.candidate').count(),8);checks.push('Exactly eight current candidates: seven Batch C plus explicit B07 carry-forward');
  async function verify(scale){
   const mains=await page.locator('img.scene-art').evaluateAll(xs=>xs.map(i=>({w:i.width,h:i.height,nw:i.naturalWidth,nh:i.naturalHeight,bw:+i.dataset.w,bh:+i.dataset.h,rendering:getComputedStyle(i).imageRendering})));
   assert.ok(mains.every(i=>i.nw===i.bw&&i.nh===i.bh&&i.w===i.bw*scale&&i.h===i.bh*scale&&['pixelated','crisp-edges'].includes(i.rendering)));
   assert.ok(await page.locator('img.portrait-art').evaluateAll(xs=>xs.every(i=>i.width===i.naturalWidth&&i.height===i.naturalHeight)));
  }
  await verify(1);checks.push('Native views decode at exact intrinsic dimensions; portraits/composites remain native');
  await page.screenshot({path:path.join(root,'screenshots/gallery-native.png')});
  await page.locator('[data-scale="4"]').click();await verify(4);checks.push('Main scene and continuity/style comparisons use exact integer 4x with pixelated rendering');
  for(const id of ['CH3-C01-urgency','CH3-C03-locomotion','CH3-C04-surprise']){
   await page.locator('#'+id+' .viewport').first().scrollIntoViewIfNeeded();await page.screenshot({path:path.join(root,'screenshots/'+id+'-4x.png')});
  }
  await page.locator('[data-scale="1"]').click();await verify(1);
  await page.locator('#layout .viewport').nth(1).scrollIntoViewIfNeeded();await page.screenshot({path:path.join(root,'screenshots/main-close-layout.png')});
  await page.locator('#composites').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(root,'screenshots/composites-native.png')});
  const manifest=await(await page.request.get(new URL('manifest.json',url).href)).json();assert.equal(manifest.currentCandidateCount,8);
  assert.ok(manifest.candidates.every(c=>c.status==='generated'&&c.selected===false&&c.approved===false&&c.assetPath===null));
  assert.equal(manifest.candidates.filter(c=>c.carryForward).length,1);assert.equal(manifest.pagesDeployed,false);
  const qa=await(await page.request.get(new URL('qa.json',url).href)).json();assert.equal(qa.candidates.length,8);assert.equal(qa.composites.length,6);
  assert.ok(qa.fixedRightWallChecks.every(c=>c.rightWallPixelDifferences===0));assert.ok(qa.consoleCorrespondence.every(c=>c.unexpectedConsolePixels===0));
  for(const c of qa.composites){assert.deepEqual(c.anchor,[0,0]);assert.equal(c.scale,1);assert.equal(c.allForegroundPixelsExact,true);}
  checks.push('Unselected metadata, six fixed-anchor composites, identical right-wall pixels and paired console checks verified');
  for(const name of ['CANDIDATE_HASHES.md','sources/generation-records.json','sources/shared-stage-layout.json'])assert.ok((await page.request.get(new URL(name,url).href)).ok());
  await page.setViewportSize({width:390,height:844});await page.goto(url,{waitUntil:'networkidle'});await page.locator('img').evaluateAll(xs=>Promise.all(xs.map(i=>i.decode())));await verify(1);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await page.screenshot({path:path.join(root,'screenshots/gallery-mobile.png')});
  checks.push('390px mobile layout has bounded horizontal proof scrolling, no document overflow or fractional artwork scaling');
  assert.equal(errors.length,0);assert.equal(failed.length,0);checks.push('No browser errors or failed requests');
  const report={result:'PASS',url,browser:await browser.version(),checks,errors,failed,publication:'Local gallery only. No generation-branch deployment; main-only publication proposal stays separate.',scope:'Display/export and metadata checks only; original native-grid authorship remains unproven and creative selection is pending Nate.'};
  fs.writeFileSync(path.join(root,'browser-qa.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
