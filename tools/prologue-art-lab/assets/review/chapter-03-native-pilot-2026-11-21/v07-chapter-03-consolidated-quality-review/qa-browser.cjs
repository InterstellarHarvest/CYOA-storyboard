const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert');
const {chromium,firefox}=require('playwright');
const B=__dirname,R=path.resolve(B,'../../../../../..');
const m=JSON.parse(fs.readFileSync(path.join(B,'manifest.json'))),pairs=JSON.parse(fs.readFileSync(path.join(B,'assessment/portrait-composite-findings.json')));
const selected=process.argv.includes('--chromium-only')?'chromium':null;
const previous=selected&&fs.existsSync(path.join(B,'qa/browser.json'))?JSON.parse(fs.readFileSync(path.join(B,'qa/browser.json'))):null;
const report={scope:'Chapter 3 consolidated 14-scene quality review',browsers:previous?.browsers?.filter(r=>r.browser!==selected)||[]};
fs.writeFileSync(path.join(B,'qa/browser.json'),JSON.stringify({status:'running'}));
const server=http.createServer((req,res)=>{
 let request=decodeURIComponent(req.url.split('?')[0]).replace(/^\/CYOA-storyboard\//,'');
 let file=path.resolve(R,request);if(!file.startsWith(R+path.sep))return res.writeHead(403).end();
 if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
 if(!fs.existsSync(file))return res.writeHead(404).end();
 const types={'.png':'image/png','.html':'text/html','.json':'application/json','.md':'text/markdown','.txt':'text/plain','.csv':'text/csv'};
 res.writeHead(200,{'content-type':types[path.extname(file)]||'application/octet-stream','cache-control':'no-store'});res.end(fs.readFileSync(file));
});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const relative=path.relative(R,B).split(path.sep).join('/'),url=`http://127.0.0.1:${server.address().port}/CYOA-storyboard/${relative}/index.html`;
 for(const[name,engine]of[['chromium',chromium],['firefox',firefox]]){
  if(selected&&name!==selected)continue;
  const row={browser:name,checks:[],status:'not-run'};report.browsers.push(row);let browser;
  const check=(name,pass)=>{row.checks.push({name,pass:!!pass});assert(pass,name)};
  try{
   browser=await engine.launch();const page=await browser.newPage({viewport:{width:1440,height:1100},deviceScaleFactor:1}),errors=[];page.on('pageerror',e=>errors.push(String(e)));
   await page.goto(url,{waitUntil:'load'});row.initialDecodeFailures=await page.locator('img').evaluateAll(async a=>{const failures=[];for(const i of a){try{await i.decode()}catch(e){failures.push({src:i.getAttribute('src'),natural:[i.naturalWidth,i.naturalHeight],error:String(e)})}}return failures});assert(row.initialDecodeFailures.length===0,JSON.stringify(row.initialDecodeFailures));
   const text=await page.locator('body').innerText();
   check('Six KEEP, zero pixel changes and no merge clearly displayed',text.includes('Six remaining scenes: KEEP')&&text.includes('Zero artwork or portrait pixels changed')&&text.includes('open and unmerged')&&text.includes('Canonical main still shows v03'));
   check('Exactly 14 matrix rows and 14 scene sections',await page.locator('#matrix tbody tr').count()===14&&await page.locator('.scene[data-scene]').count()===14);
   check('Exactly 15 dialogue pairing sections',await page.locator('.portrait[data-pair]').count()===15);
   check('Every scene native pair remains two 314x206 images',await page.locator('.scene').evaluateAll(a=>a.every(s=>{const p=s.querySelector('.pair');return p&&p.querySelectorAll('img').length===2&&[...p.querySelectorAll('img')].every(i=>i.getBoundingClientRect().width===314&&i.getBoundingClientRect().height===206)})));
   await page.screenshot({path:path.join(B,'qa',name+'-overview.png')});await page.locator('#scene-human_verification_stage').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(B,'qa',name+'-scene-native.png')});
   const assets=[...m.sceneSources.map(s=>[s.reviewFile,s.sha256]),...m.crossChapterReferences.map(s=>[s.reviewFile,s.sha256]),...pairs.flatMap(p=>[[p.backgroundFile,p.background.sha256],[p.foregroundFile,p.foreground.sha256]]),['references/paper-emergency-selected-v04.png','93a48082124600b1afeb45e5ea54856bf253e858e55111295e9d9c26919bc978']];
   const unique=[...new Map(assets).entries()];row.sourceImagesVerified=unique.length;
   check('Browser hashes every scene/layer/reference/selected Paper input',await page.evaluate(async a=>(await Promise.all(a.map(async([p,h])=>{const r=await fetch(p),b=await crypto.subtle.digest('SHA-256',await r.arrayBuffer());return r.ok&&[...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('')===h}))).every(Boolean),unique));
   check('Browser confirms all 14 canonical hashes unchanged',await page.evaluate(async a=>{const p=(await(await fetch('/CYOA-storyboard/story/artwork-preview.json')).json()).images;return a.every(s=>p[s.key].sha256===s.sha256)},m.sceneSources));
   check('Browser independently decodes all 14 closed masks',await page.evaluate(async a=>(await Promise.all(a.map(async s=>{const n=s.key.split('/').pop(),im=await createImageBitmap(await(await fetch('masks/'+n+'-repair-mask.png')).blob()),c=document.createElement('canvas');c.width=314;c.height=206;const x=c.getContext('2d');x.drawImage(im,0,0);const d=x.getImageData(0,0,314,206).data;for(let i=0;i<d.length;i+=4)if(d[i]||d[i+1]||d[i+2])return false;return im.width===314&&im.height===206}))).every(Boolean),m.sceneSources));
   await page.locator('#expand').click();check('Expand opens every exact 4x panel and portrait parents',await page.locator('details.four:not([open])').count()===0&&await page.locator('.portrait:not([open])').count()===0);
   check('Every scene full 4x pair remains 1256x824 per image',await page.locator('.scene').evaluateAll(a=>a.every(s=>[...s.querySelector('details.four').querySelectorAll('.pair img')].every(i=>i.getBoundingClientRect().width===1256&&i.getBoundingClientRect().height===824))));
   check('4x pair scrolls instead of shrinking',await page.locator('.scene details.four').first().locator('.scroll').evaluate(d=>d.scrollWidth>d.clientWidth));
   check('All 15 native composite canvases retain 564x278',await page.locator('.portrait').evaluateAll(a=>a.every(p=>{const i=p.querySelector('img');return i.getBoundingClientRect().width===564&&i.getBoundingClientRect().height===278})));
   check('Every gallery image decodes at declared dimensions',await page.locator('img').evaluateAll(a=>a.every(i=>i.complete&&i.naturalWidth===Number(i.getAttribute('width'))&&i.naturalHeight===Number(i.getAttribute('height')))));
   const links=await page.locator('a[href]').evaluateAll(a=>a.map(i=>i.getAttribute('href')).filter(h=>!h.startsWith('#')&&!h.startsWith('http')));
   row.links=await page.evaluate(async a=>Promise.all([...new Set(a)].map(async h=>({href:h,status:(await fetch(h)).status}))),links);check('Every local matrix/evidence/layer/PNG/QA link resolves',row.links.every(r=>r.status===200));
   await page.locator('#collapse').click();check('Collapse closes enlarged and portrait panels',await page.locator('details[open]').count()===0);
   await page.setViewportSize({width:390,height:844});await page.locator('#scene-human_verification_stage').scrollIntoViewIfNeeded();check('Mobile retains native pixel scale',await page.locator('.scene').first().locator('.pair').first().locator('img').evaluateAll(a=>a.every(i=>i.getBoundingClientRect().width===314&&i.getBoundingClientRect().height===206)));await page.screenshot({path:path.join(B,'qa',name+'-mobile.png')});
   await page.goto(url.replace('index.html','standalone-gallery.html'),{waitUntil:'load'});await page.locator('img').evaluateAll(async a=>{for(const i of a)await i.decode()});row.embeddedImages=await page.locator('img').count();
   check('Portable gallery embeds and decodes every image',await page.locator('img').evaluateAll(a=>a.length>100&&a.every(i=>i.src.startsWith('data:image/png;base64,')&&i.complete&&i.naturalWidth>0)));
   check('No page JavaScript exceptions',errors.length===0);row.errors=errors;row.status='PASS';
  }catch(e){row.status='FAIL';row.error=String(e);process.exitCode=1}finally{if(browser)await browser.close()}
 }
 fs.writeFileSync(path.join(B,'qa/browser.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({scope:report.scope,browsers:report.browsers.map(r=>({browser:r.browser,status:r.status,checks:r.checks.length,sourceImagesVerified:r.sourceImagesVerified,embeddedImages:r.embeddedImages,error:r.error}))},null,2));server.close();
})().catch(e=>{console.error(e);server.close();process.exit(1)});
