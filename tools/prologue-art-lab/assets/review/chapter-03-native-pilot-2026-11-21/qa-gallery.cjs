const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert');
const {chromium,firefox}=require('playwright');
const B=__dirname,R=path.resolve(B,'../../../../..');
const prefix='/CYOA-storyboard/';const rel=path.relative(R,B).split(path.sep).join('/');
const manifest=JSON.parse(fs.readFileSync(path.join(B,'manifest.json'),'utf8'));
const report={scope:'Local review gallery only; no Pages publication or gameplay',browsers:[]};
const server=http.createServer((req,res)=>{
 let u=decodeURIComponent(req.url.split('?')[0]);if(u.startsWith(prefix))u=u.slice(prefix.length);else u=u.replace(/^\//,'');
 let file=path.resolve(R,u);if(!file.startsWith(R+path.sep)){res.writeHead(403).end();return;}
 if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
 if(!fs.existsSync(file)){res.writeHead(404).end();return;}const types={'.png':'image/png','.html':'text/html','.json':'application/json','.js':'text/javascript','.cjs':'text/javascript','.txt':'text/plain'};res.writeHead(200,{'content-type':types[path.extname(file)]||'application/octet-stream','cache-control':'no-store'});res.end(fs.readFileSync(file));
});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));let port=server.address().port;
 for(const [name,engine] of [['chromium',chromium],['firefox',firefox]]){
  const row={browser:name,checks:[],status:'not-run'};report.browsers.push(row);let browser;
  const check=(name,ok)=>{row.checks.push({name,pass:!!ok});assert(ok,name);};
  try{
   browser=await engine.launch({headless:true});const page=await browser.newPage({viewport:{width:1440,height:1100},deviceScaleFactor:1});const errors=[];page.on('pageerror',e=>errors.push(String(e)));
   let url=`http://127.0.0.1:${port}${prefix}${rel}/index.html`;await page.goto(url,{waitUntil:'load'});await page.locator('img').evaluateAll(a=>Promise.all(a.map(i=>i.decode())));
   check('Two generated/unselected candidate sections',await page.locator('section#backstage,section#locomotion').count()===2);
   check('Native previews display exactly 314x206 CSS pixels',await page.locator('img[width="314"]').evaluateAll(a=>a.filter(i=>i.checkVisibility()).every(i=>i.getBoundingClientRect().width===314&&i.getBoundingClientRect().height===206)));
   await page.screenshot({path:path.join(B,'qa',`${name}-overview.png`)});
   await page.locator('#backstage').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(B,'qa',`${name}-backstage-native.png`)});
   await page.locator('#locomotion').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(B,'qa',`${name}-locomotion-native.png`)});
   await page.locator('#expand').click();check('Expand control opens every exact 4x comparison',await page.locator('details.four:not([open])').count()===0);
   check('All expanded 4x images retain 1256x824 CSS pixels',await page.locator('details.four img').evaluateAll(a=>a.every(i=>i.getBoundingClientRect().width===1256&&i.getBoundingClientRect().height===824)));
   check('Exact 4x comparison scrolls without shrinking',await page.locator('#backstage details.four .scroll').first().evaluate(d=>d.scrollWidth>d.clientWidth));
   await page.evaluate(()=>document.querySelectorAll('details').forEach(d=>d.open=true));
   check('Every image decodes at its declared native/export dimensions',await page.locator('img').evaluateAll(a=>a.every(i=>i.complete&&i.naturalWidth===Number(i.getAttribute('width'))&&i.naturalHeight===Number(i.getAttribute('height')))));
   const assets=[...manifest.references,...manifest.candidates.flatMap(c=>[c,c.approved])].map(x=>({file:x.file,sha256:x.sha256}));
   const verified=await page.evaluate(async a=>Promise.all(a.map(async x=>{let r=await fetch(x.file),b=await r.arrayBuffer(),h=await crypto.subtle.digest('SHA-256',b);return r.ok&&[...new Uint8Array(h)].map(v=>v.toString(16).padStart(2,'0')).join('')===x.sha256})),assets);
   check('Browser fetches exact candidate/approved/reference PNG hashes',verified.every(Boolean));
   const links=await page.locator('a[href]').evaluateAll(a=>a.map(x=>x.getAttribute('href')).filter(h=>!h.startsWith('#')&&!h.startsWith('http')));
   const statuses=await page.evaluate(async a=>Promise.all(a.map(async h=>[h,(await fetch(h)).status])),links);row.linkResponses=statuses;check('All gallery artifact links resolve',statuses.every(x=>x[1]===200));
   await page.locator('#collapse').click();check('Collapse control closes every details element',await page.locator('details[open]').count()===0);
   await page.setViewportSize({width:390,height:844});await page.locator('#backstage').scrollIntoViewIfNeeded();check('Mobile native previews retain logical size',await page.locator('#backstage > .scroll img').evaluateAll(a=>a.every(i=>i.getBoundingClientRect().width===314&&i.getBoundingClientRect().height===206)));await page.screenshot({path:path.join(B,'qa',`${name}-mobile.png`)});
   check('No page JavaScript exceptions',errors.length===0);row.errors=errors;row.status='PASS';
  }catch(e){row.status='FAIL';row.error=String(e);process.exitCode=1;}finally{if(browser)await browser.close();}
 }
 fs.writeFileSync(path.join(B,'qa/gallery-browser.json'),JSON.stringify(report,null,2));server.close();console.log(JSON.stringify(report,null,2));
})().catch(e=>{console.error(e);server.close();process.exit(1)});
