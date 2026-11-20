const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=__dirname,url='http://127.0.0.1:8780/tools/prologue-art-lab/assets/review/chapter-03-batch03-2026-11-19/v02-localized-corrections/';
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 try{
  fs.mkdirSync(path.join(root,'screenshots'),{recursive:true});
  const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});
  const errors=[],failed=[],checks=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('requestfailed',r=>failed.push(r.url()));
  await page.goto(url,{waitUntil:'networkidle'});
  await page.locator('img').evaluateAll(xs=>Promise.all(xs.map(i=>i.decode())));
  assert.equal(await page.locator('.candidate').count(),8);
  async function verify(s){
   const images=await page.locator('img.scaled').evaluateAll(xs=>xs.map(i=>({w:i.width,h:i.height,nw:i.naturalWidth,nh:i.naturalHeight,bw:+i.dataset.w,bh:+i.dataset.h,rendering:getComputedStyle(i).imageRendering})));
   assert.ok(images.length>=20);
   assert.ok(images.every(i=>i.nw===i.bw&&i.nh===i.bh&&i.w===i.bw*s&&i.h===i.bh*s&&['pixelated','crisp-edges'].includes(i.rendering)));
   assert.ok(await page.locator('img.fixed-proof').evaluateAll(xs=>xs.every(i=>i.width===i.naturalWidth&&i.height===i.naturalHeight)));
  }
  await verify(1);checks.push('Eight candidates and native comparisons decode at exact intrinsic dimensions');
  await page.screenshot({path:path.join(root,'screenshots/gallery-native.png')});
  await page.locator('[data-scale="4"]').click();await verify(4);
  checks.push('All scalable views use exact integer 4x; fixed close-ups retain exact 8x');
  for(const id of ['CH3-C01-urgency','CH3-C03-locomotion']){
   await page.locator('#'+id+' .viewport').first().scrollIntoViewIfNeeded();
   await page.screenshot({path:path.join(root,'screenshots/'+id+'-4x.png')});
  }
  await page.locator('[data-scale="1"]').click();await verify(1);
  await page.locator('#continuity').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(root,'screenshots/stage-continuity-native.png')});
  const m=await(await page.request.get(new URL('manifest.json',url).href)).json();
  assert.equal(m.currentCandidateCount,8);assert.equal(m.pagesDeployed,false);assert.equal(m.generationCallsThisPass,0);
  assert.ok(m.candidates.every(c=>c.status==='generated'&&!c.selected&&!c.approved&&c.assetPath===null));
  const q=await(await page.request.get(new URL('qa.json',url).href)).json();
  assert.equal(q.result,'PASS');assert.equal(q.changedPixelsTotal,239);assert.equal(q.editedCandidateCount,2);
  assert.equal(q.candidates.filter(c=>c.byteIdenticalToV01).length,6);
  assert.ok(q.candidates.every(c=>c.unexpectedChangesOutsideAllowedMask===0));
  assert.equal(q.composites.length,6);assert.ok(q.composites.every(c=>c.byteIdenticalToV01&&c.allForegroundPixelsExact));
  assert.ok(q.fixedRightWallChecks.every(c=>c.differences===0));assert.ok(q.consoleContinuity.every(c=>c.differencesFromV01===0));
  checks.push('239 localized changes; six candidates and six composites byte-identical; wall/console continuity and unselected metadata verified');
  for(const href of await page.locator('a[href]').evaluateAll(xs=>xs.map(x=>x.getAttribute('href')).filter(h=>!h.startsWith('#')&&!h.startsWith('http'))))
   assert.ok((await page.request.get(new URL(href,url).href)).ok(),href);
  checks.push('Every linked local provenance file, mask, coordinate list, historical image and comparison resolves');
  await page.setViewportSize({width:390,height:844});await page.goto(url,{waitUntil:'networkidle'});
  await page.locator('img').evaluateAll(xs=>Promise.all(xs.map(i=>i.decode())));await verify(1);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await page.screenshot({path:path.join(root,'screenshots/gallery-mobile.png')});
  checks.push('390px mobile page has contained proof scrolling and no document overflow');
  assert.equal(errors.length,0);assert.equal(failed.length,0);checks.push('No browser errors or failed requests');
  const result={result:'PASS',url,browser:await browser.version(),checks,errors,failed,
   publication:'Local browser verification only. No Pages deployment or PR #13 update/merge.',
   limitation:'Original native-grid authorship remains unresolved; selection is pending Nate.'};
  fs.writeFileSync(path.join(root,'browser-qa.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
