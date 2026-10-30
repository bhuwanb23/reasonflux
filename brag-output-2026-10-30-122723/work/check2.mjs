import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--force-device-scale-factor=1', '--hide-scrollbars'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });
page.on('pageerror', (e) => console.error('PAGE ERROR:', e.message));
await page.goto('file://' + process.cwd() + '/work/scene_withjs.html?static', { waitUntil: 'networkidle0' });
await page.evaluate(() => (document.fonts ? document.fonts.ready : Promise.resolve()));

await page.evaluate(() => window.__seek(46)); await page.screenshot({ path: 'work/stills/s5_metrics_v2.png' });
await page.evaluate(() => window.__seek(10.12)); await page.screenshot({ path: 'work/stills/t_cut_dip.png' });
await page.evaluate(() => window.__seek(33)); await page.screenshot({ path: 'work/stills/s4_v2.png' });
await browser.close();
console.log('ok');
