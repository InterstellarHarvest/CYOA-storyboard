const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=__dirname,url='http://127.0.0.1:8780/tools/prologue-art-lab/assets/review/chapter-03-batch03-2026-11-19/v04-perspective-corrections/';
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 try{
  fs.mkdirSync(path.join(root,'screenshots'),{recursive:true});
  const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});
  const errors=[],failed=[],checks=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('requestfailed',r=>failed.push(r.url()));
  await page.goto(url,{waitUntil:'networkidle'});
  await page.locator('img').evaluateAll(xs=>Promise.all(xs.map(i=>i.decode())));
  assert.equal(await page.locator('.candidate').count(),7);
  async function verify(s){
   const images=await page.locator('img.scaled').evaluateAll(xs=>xs.map(i=>({w:i.width,h:i.height,nw:i.naturalWidth,nh:i.naturalHeight,bw:+i.dataset.w,bh:+i.dataset.h,rendering:getComputedStyle(i).imageRendering})));
   assert.ok(images.length>=20);
   assert.ok(images.every(i=>i.nw===i.bw&&i.nh===i.bh&&i.w===i.bw*s&&i.h===i.bh*s&&['pixelated','crisp-edges'].includes(i.rendering)));
   assert.ok(await page.locator('img.fixed').evaluateAll(xs=>xs.every(i=>i.width===i.naturalWidth&&i.height===i.naturalHeight)));
  }
  await verify(1);checks.push('Seven environment revisions and native comparisons decode at exact intrinsic dimensions');
  await page.screenshot({path:path.join(root,'screenshots/gallery-native.png')});
  await page.locator('[data-scale="4"]').click();await verify(4);
  checks.push('All scalable views use exact integer 4x; fixed close-ups retain exact 8x');
  for(const id of ['CH3-C04-surprise','CH3-A05-verification-bg-continuity']){
   await page.locator('#'+id+' .viewport').first().scrollIntoViewIfNeeded();
   await page.screenshot({path:path.join(root,'screenshots/'+id+'-4x.png')});
  }
  await page.locator('[data-scale="1"]').click();await verify(1);
  await page.locator('#continuity').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(root,'screenshots/stage-continuity-native.png')});
  const m=await(await page.request.get(new URL('manifest.json',url).href)).json();
  assert.equal(m.candidates.length,7);assert.equal(m.approvedPoseReferences.length,3);assert.equal(m.pagesDeployed,false);
  assert.ok(m.candidates.every(c=>c.status==='generated'&&!c.selected&&!c.approved&&c.assetPath===null));
  const q=await(await page.request.get(new URL('qa.json',url).href)).json();
  assert.equal(q.result,'PASS');assert.equal(q.candidateCount,7);assert.equal(q.additionalA04A05Options,2);
  assert.ok(q.candidates.every(c=>c.unexpectedChangesOutsidePredeclaredMasks===0));
  assert.equal(q.composites.length,4);assert.ok(q.composites.every(c=>c.exactForegroundPixels&&c.pedestalOverlap===0));
  assert.ok(q.wallContinuity.every(c=>c.pixelDifferences===0));
  assert.ok(q.presenterOcclusion.every(c=>c.pixelMismatches===0));
  assert.equal(q.cannonFiringSide.allPresenterPixelsLeftOfCannon,true);assert.equal(q.cannonFiringSide.horizontalMove,-73);assert.ok(q.pedestalClarity.every(c=>c.sameHeadGeometry));
  checks.push('Seven unselected revisions; four main/three portrait wall matches; exact sprite identity on firing side; clear pedestal state mapping; four fixed-anchor composites verified');
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
   publication:'Local browser verification only. No Pages deployment or merge; PR #13 remains draft and v02-pinned.',
   limitation:'Original native-grid authorship remains unresolved; selection is pending Nate.'};
  fs.writeFileSync(path.join(root,'browser-qa.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
