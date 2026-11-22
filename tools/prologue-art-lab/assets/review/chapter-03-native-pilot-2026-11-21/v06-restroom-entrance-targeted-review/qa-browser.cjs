const fs = require('fs'), path = require('path'), http = require('http'), assert = require('assert');
const { chromium, firefox } = require('playwright');
const B = __dirname, R = path.resolve(B, '../../../../../..');
const manifest = JSON.parse(fs.readFileSync(path.join(B, 'manifest.json')));
const report = { scope: 'Restroom Entrance A01 KEEP assessment', browsers: [] };
fs.writeFileSync(path.join(B, 'qa/browser.json'), JSON.stringify({ status: 'running' }));
const server = http.createServer((req, res) => {
  const request = decodeURIComponent(req.url.split('?')[0]).replace(/^\/CYOA-storyboard\//, '');
  let file = path.resolve(R, request);
  if (!file.startsWith(R + path.sep)) return res.writeHead(403).end();
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
  if (!fs.existsSync(file)) return res.writeHead(404).end();
  const types = { '.png': 'image/png', '.html': 'text/html', '.json': 'application/json', '.md': 'text/markdown', '.txt': 'text/plain' };
  res.writeHead(200, { 'content-type': types[path.extname(file)] || 'application/octet-stream', 'cache-control': 'no-store' });
  res.end(fs.readFileSync(file));
});

(async () => {
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const relative = path.relative(R, B).split(path.sep).join('/');
  const url = `http://127.0.0.1:${server.address().port}/CYOA-storyboard/${relative}/index.html`;
  for (const [name, engine] of [['chromium', chromium], ['firefox', firefox]]) {
    const row = { browser: name, checks: [], status: 'not-run' };
    report.browsers.push(row);
    let browser;
    const check = (name, pass) => { row.checks.push({ name, pass: !!pass }); assert(pass, name); };
    try {
      browser = await engine.launch();
      const page = await browser.newPage({ viewport: { width: 1440, height: 1100 }, deviceScaleFactor: 1 });
      const errors = [];
      page.on('pageerror', e => errors.push(String(e)));
      await page.goto(url, { waitUntil: 'load' });
      await page.locator('img').evaluateAll(images => Promise.all(images.map(i => i.decode())));
      const text = await page.locator('body').innerText();
      check('KEEP and zero artwork edits clearly displayed', text.includes('Recommendation: KEEP') && text.includes('Zero artwork pixels changed'));
      check('Paper v04 selection and pending registration distinguished', text.includes('registration pending') && text.includes('still canonical until Claude registration'));
      check('Native comparison is two 314x206 images', await page.locator('.pair').first().locator('img').evaluateAll(a => a.length === 2 && a.every(i => i.getBoundingClientRect().width === 314 && i.getBoundingClientRect().height === 206)));
      await page.screenshot({ path: path.join(B, 'qa', name + '-overview.png') });
      const assets = [[manifest.approvedOriginal, manifest.approvedSource.sha256], ...manifest.references.map(r => [r.reviewFile, r.sha256])];
      check('Browser independently fetches exact original and reference hashes', await page.evaluate(async assets => (await Promise.all(assets.map(async ([p, h]) => {
        const r = await fetch(p), digest = await crypto.subtle.digest('SHA-256', await r.arrayBuffer());
        return r.ok && [...new Uint8Array(digest)].map(x => x.toString(16).padStart(2, '0')).join('') === h;
      }))).every(Boolean), assets));
      check('Canonical A01 hash and Paper v03 remain unchanged', await page.evaluate(async () => {
        const p = (await (await fetch('/CYOA-storyboard/story/artwork-preview.json')).json()).images;
        return p['scenes:pavilion_reboot/restroom_entrance'].sha256 === '117dd9d00b6c9d32b4b153f71aaf51c2546ade70b803d45a748728f8d1a1f8b4' && p['scenes:pavilion_reboot/paper_emergency'].sha256 === 'ac0f7c44d267dd54897507ae3b8b02959a5b76f4fcd9d0418b77b8fdb777ba7e';
      }));
      check('Browser decodes closed zero-pixel repair mask', await page.evaluate(async () => {
        const image = await createImageBitmap(await (await fetch('masks/proposed-repair-mask.png')).blob());
        const c = document.createElement('canvas'); c.width = 314; c.height = 206;
        const x = c.getContext('2d'); x.drawImage(image, 0, 0);
        const d = x.getImageData(0, 0, 314, 206).data;
        for (let i = 0; i < d.length; i += 4) if (d[i] || d[i + 1] || d[i + 2]) return false;
        return image.width === 314 && image.height === 206;
      }));
      await page.locator('#expand').click();
      check('Expand opens every exact 4x panel', await page.locator('details.four:not([open])').count() === 0);
      check('Full 4x comparison remains 1256x824 per image', await page.locator('details.four').first().locator('.pair img').evaluateAll(a => a.length === 2 && a.every(i => i.getBoundingClientRect().width === 1256 && i.getBoundingClientRect().height === 824)));
      check('4x panels scroll instead of shrinking', await page.locator('details.four').first().locator('.scroll').evaluate(d => d.scrollWidth > d.clientWidth));
      check('Every image decodes at declared dimensions', await page.locator('img').evaluateAll(a => a.every(i => i.complete && i.naturalWidth === Number(i.getAttribute('width')) && i.naturalHeight === Number(i.getAttribute('height')))));
      const links = await page.locator('a[href]').evaluateAll(a => a.map(i => i.getAttribute('href')).filter(h => !h.startsWith('#') && !h.startsWith('http')));
      row.links = await page.evaluate(async a => Promise.all(a.map(async h => ({ href: h, status: (await fetch(h)).status }))), links);
      check('Every local source evidence and QA link resolves', row.links.every(r => r.status === 200));
      await page.locator('#collapse').click();
      check('Collapse closes all enlarged views', await page.locator('details[open]').count() === 0);
      await page.setViewportSize({ width: 390, height: 844 });
      check('Mobile retains native 314x206 display', await page.locator('.pair').first().locator('img').evaluateAll(a => a.every(i => i.getBoundingClientRect().width === 314 && i.getBoundingClientRect().height === 206)));
      await page.screenshot({ path: path.join(B, 'qa', name + '-mobile.png') });
      await page.goto(url.replace('index.html', 'standalone-gallery.html'), { waitUntil: 'load' });
      await page.locator('img').evaluateAll(a => Promise.all(a.map(i => i.decode())));
      check('Portable HTML embeds and decodes all images', await page.locator('img').evaluateAll(a => a.length > 0 && a.every(i => i.src.startsWith('data:image/png;base64,') && i.complete && i.naturalWidth > 0)));
      check('No JavaScript exceptions', errors.length === 0);
      row.errors = errors;
      row.status = 'PASS';
    } catch (e) {
      row.status = 'FAIL'; row.error = String(e); process.exitCode = 1;
    } finally {
      if (browser) await browser.close();
    }
  }
  fs.writeFileSync(path.join(B, 'qa/browser.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify({ scope: report.scope, browsers: report.browsers.map(r => ({ browser: r.browser, status: r.status, checks: r.checks.length, error: r.error })) }, null, 2));
  server.close();
})().catch(e => { console.error(e); server.close(); process.exit(1); });
