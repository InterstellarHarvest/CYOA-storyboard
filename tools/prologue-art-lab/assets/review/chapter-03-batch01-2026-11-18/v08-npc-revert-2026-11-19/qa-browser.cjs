const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=process.env.QA_OUTPUT_DIR||__dirname;
const url=process.env.GALLERY_URL||'http://127.0.0.1:8777/v08-npc-revert-2026-11-19/';
(async()=>{
const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
try{
fs.mkdirSync(path.join(root,'screenshots'),{recursive:true});
const p=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1}),errors=[],failed=[];
p.on('pageerror',e=>errors.push(String(e)));p.on('requestfailed',r=>failed.push(r.url()));
await p.goto(url,{waitUntil:'networkidle'});await p.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(i=>i.decode())));
async function check(scale){assert.ok(await p.locator('img.art').evaluateAll((imgs,s)=>imgs.every(i=>i.width===Number(i.dataset.w)*s&&i.height===Number(i.dataset.h)*s&&i.naturalWidth===Number(i.dataset.w)&&i.naturalHeight===Number(i.dataset.h)),scale));}
await check(1);await p.screenshot({path:path.join(root,'screenshots/native.png')});
await p.locator('[data-scale="4"]').click();await check(4);await p.locator('img.art').first().scrollIntoViewIfNeeded();await p.screenshot({path:path.join(root,'screenshots/restroom-4x.png')});
await p.setViewportSize({width:390,height:844});await p.goto(url,{waitUntil:'networkidle'});await p.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(i=>i.decode())));await check(1);assert.ok(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
assert.equal(errors.length,0);assert.equal(failed.length,0);
const report={result:'PASS',url,browser:await browser.version(),checks:['All scene, identity and microphone images load','Exact native and 4x scene dimensions','Mobile page has no document overflow','No page exceptions or failed requests'],errors,failed};fs.writeFileSync(path.join(root,'browser-qa.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
}finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
