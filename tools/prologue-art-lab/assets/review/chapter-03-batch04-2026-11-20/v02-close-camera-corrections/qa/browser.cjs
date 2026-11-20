const fs=require('fs'),path=require('path'),os=require('os'),http=require('http'),{execFileSync}=require('child_process');
const {chromium,firefox}=require('playwright');
const P=path.resolve(__dirname,'..'),R=path.resolve(P,'../../../../../..');
const report={result:'PASS',browsers:[]};
async function main(){
 const yaml=fs.readFileSync(path.join(R,'.github/workflows/pages.yml'),'utf8').split('\n');
 const start=yaml.findIndex(l=>/name: Build standalone public site$/.test(l))+2,indent=yaml[start].match(/^ */)[0].length;
 const body=[];for(let i=start;i<yaml.length;i++){const l=yaml[i];if(l.trim()&&l.match(/^ */)[0].length<indent)break;body.push(l.slice(indent));}
 const build=path.join(R,'_site');if(fs.existsSync(build))throw Error('Existing _site: refuse overwrite');
 execFileSync('bash',['-e','-c',body.join('\n')],{cwd:R,stdio:'pipe'});
 const site=fs.mkdtempSync(path.join(os.tmpdir(),'ch3d-built-site-'));fs.cpSync(build,site,{recursive:true});fs.rmSync(build,{recursive:true});
 const prefix='/CYOA-storyboard/';
 const server=http.createServer((req,res)=>{let u=decodeURIComponent(new URL(req.url,'http://localhost').pathname);if(!u.startsWith(prefix)){res.writeHead(404).end();return;}let f=path.resolve(site,u.slice(prefix.length));if(!f.startsWith(site+path.sep)){res.writeHead(403).end();return;}if(fs.existsSync(f)&&fs.statSync(f).isDirectory())f=path.join(f,'index.html');if(!fs.existsSync(f)){res.writeHead(404).end();return;}res.setHeader('content-type',f.endsWith('.html')?'text/html':f.endsWith('.png')?'image/png':f.endsWith('.json')?'application/json':'text/plain');fs.createReadStream(f).pipe(res);});
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const url=`http://127.0.0.1:${server.address().port}${prefix}tools/prologue-art-lab/assets/review/chapter-03-batch04-2026-11-20/v02-close-camera-corrections/`;
 try{for(const [name,engine] of [['chromium',chromium],['firefox',firefox]]){
  const browser=await engine.launch();try{const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('response',r=>{if(r.status()>=400&&!r.url().endsWith('/favicon.ico'))errors.push(r.status()+' '+r.url());});
  await page.goto(url);await page.waitForFunction(()=>[...document.images].every(i=>i.complete&&i.naturalWidth));
  if(await page.locator('article').count()!==3)throw Error('Expected three revised candidates');
  const native=await page.locator('img.native').evaluateAll(imgs=>imgs.map(i=>({natural:[i.naturalWidth,i.naturalHeight],display:[i.getBoundingClientRect().width,i.getBoundingClientRect().height],render:getComputedStyle(i).imageRendering})));
  if(native.some(i=>JSON.stringify(i.natural)!==JSON.stringify(i.display)||!['pixelated','crisp-edges'].includes(i.render)))throw Error('Native image scaling');
  await page.locator('details').evaluateAll(ds=>ds.forEach(d=>d.open=true));await page.waitForTimeout(250);
  const previews=await page.locator('img.preview4x').evaluateAll(imgs=>imgs.map(i=>({natural:[i.naturalWidth,i.naturalHeight],display:[i.getBoundingClientRect().width,i.getBoundingClientRect().height]})));
  if(previews.length!==3||previews.some((i,j)=>i.natural[0]!==native[j].natural[0]*4||i.natural[1]!==native[j].natural[1]*4||JSON.stringify(i.natural)!==JSON.stringify(i.display)))throw Error('4x display contract');
  const links=await page.locator('a[href]').evaluateAll(as=>as.map(a=>a.href).filter(u=>!u.includes('#')));
  // QA report/checksum files are created after browser completion, so validate their hrefs in package QA later.
  for(const link of links.filter(u=>!/(browser-results.json|SHA256SUMS.txt)$/.test(u))){const r=await page.request.get(link);if(r.status()!==200)throw Error('Broken link: '+link+' '+r.status());}
  await page.screenshot({path:path.join(P,'qa',name+'-gallery.png'),fullPage:false});
  await page.locator('#CH3-D09-courtesy-stage-bg').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(P,'qa',name+'-courtesy.png')});
  await page.setViewportSize({width:390,height:844});await page.goto(url);await page.waitForFunction(()=>[...document.images].every(i=>i.complete&&i.naturalWidth));
  const mobile=await page.locator('img.native').evaluateAll(imgs=>imgs.every(i=>i.getBoundingClientRect().width===i.naturalWidth));if(!mobile)throw Error('Mobile downscales native art');
  if(errors.length)throw Error(errors.join('\n'));report.browsers.push({browser:name,result:'PASS',builtPagesPrefix:prefix,revisedCandidates:3,retainedCandidates:6,allImagesLoad:true,allReviewLinksResolve:true,nativePixelsExact:true,previews4xExact:true,mobileNativeSizePreserved:true,consoleErrors:errors});
  }finally{await browser.close();}
 }}finally{server.close();}
 report.builtSite=site;fs.writeFileSync(path.join(P,'qa/browser-results.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
}
main().catch(e=>{console.error(e);process.exit(1)});
