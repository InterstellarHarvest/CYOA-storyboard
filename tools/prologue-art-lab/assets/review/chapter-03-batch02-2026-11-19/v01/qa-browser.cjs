const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=process.env.QA_OUTPUT_DIR||__dirname;
const url=process.env.GALLERY_URL||'http://127.0.0.1:8780/tools/prologue-art-lab/assets/review/chapter-03-batch02-2026-11-19/v01/';
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 try{
  fs.mkdirSync(path.join(root,'screenshots'),{recursive:true});
  const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});
  const errors=[],failed=[],checks=[];page.on('pageerror',e=>errors.push(String(e)));page.on('requestfailed',r=>failed.push(r.url()));
  await page.goto(url,{waitUntil:'networkidle'});await page.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(i=>i.decode())));
  assert.equal(await page.locator('.candidate').count(),6);checks.push('Exactly six current candidate cards; superseded attempt is provenance only');
  async function verify(scale){
   const mains=await page.locator('img.scene-art').evaluateAll(imgs=>imgs.map(i=>({w:i.width,h:i.height,nw:i.naturalWidth,nh:i.naturalHeight,bw:Number(i.dataset.w),bh:Number(i.dataset.h),rendering:getComputedStyle(i).imageRendering})));
   assert.ok(mains.every(i=>i.nw===i.bw&&i.nh===i.bh&&i.w===i.bw*scale&&i.h===i.bh*scale&&['pixelated','crisp-edges'].includes(i.rendering)));
   assert.ok(await page.locator('img.portrait-art').evaluateAll(imgs=>imgs.every(i=>i.width===i.naturalWidth&&i.height===i.naturalHeight)));
  }
  await verify(1);checks.push('Native main scenes and all portrait/composite/reference images decode at exact intrinsic dimensions');
  await page.screenshot({path:path.join(root,'screenshots/gallery-native.png')});
  await page.locator('[data-scale="4"]').click();await verify(4);checks.push('4x main-scene control applies exact integer scale; portraits and composites remain native size');
  for(const id of ['CH3-B01-arrival','CH3-B02-record-printer','CH3-B04-record-scanner','CH3-B06-paper-emergency']){
   await page.locator('#'+id+' .viewport').first().scrollIntoViewIfNeeded();await page.screenshot({path:path.join(root,'screenshots/'+id+'-4x.png')});
   const comparison=page.locator('#'+id+' .viewport').nth(1);assert.ok(await comparison.evaluate(n=>n.scrollWidth>n.clientWidth));
  }
  checks.push('Every main scene has a bounded, same-scale cross-chapter comparison at4x');
  await page.locator('[data-scale="1"]').click();await verify(1);
  for(const id of ['CH3-B03-record-printer-bg','CH3-B05-record-scanner-bg']){
   await page.locator('#'+id+' .viewport').nth(1).scrollIntoViewIfNeeded();await page.screenshot({path:path.join(root,'screenshots/'+id+'-composite-native.png')});
  }
  const manifest=await(await page.request.get(new URL('manifest.json',url).href)).json();assert.equal(manifest.currentCandidateCount,6);assert.ok(manifest.candidates.every(c=>c.status==='generated'&&c.selected===false&&c.approved===false&&c.assetPath===null));
  for(const c of manifest.composites){assert.deepEqual(c.anchor,[0,0]);assert.equal(c.scale,1);assert.equal(c.foregroundSha256,'28fdf5523454ea2ccdb397bd4d7006fc1fb8f04109046b7646361692422c3ef2');}
  checks.push('All current metadata remains generated/unselected with null production paths; composite anchors and approved foreground hash match');
  for(const f of ['qa.json','sources/generation-records.json','sources/reference-manifest.json','CANDIDATE_HASHES.md'])assert.ok((await page.request.get(new URL(f,url).href)).ok());
  await page.setViewportSize({width:390,height:844});await page.goto(url,{waitUntil:'networkidle'});await page.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(i=>i.decode())));await verify(1);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await page.screenshot({path:path.join(root,'screenshots/gallery-mobile.png')});
  checks.push('390px mobile layout has no horizontal document overflow and no fractional artwork scaling');assert.equal(errors.length,0);assert.equal(failed.length,0);checks.push('No browser exceptions or failed network requests');
  const report={result:'PASS',url,browser:await browser.version(),checks,errors,failed,scope:'Browser behavior and metadata only. Original native-grid authorship and creative/cross-chapter approval are not passed by this test.'};
  fs.writeFileSync(path.join(root,'browser-qa.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
