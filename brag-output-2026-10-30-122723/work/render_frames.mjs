import puppeteer from 'puppeteer';
import fs from 'fs';

const htmlPath = 'file://' + process.cwd() + '/work/scene_withjs.html?static';
const outDir = 'work/renderframe';
const FPS = 30;
const TOTAL = 60 * FPS;

fs.rmSync(outDir, { recursive: true, force: true });
fs.mkdirSync(outDir, { recursive: true });

const browser = await puppeteer.launch({
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--force-device-scale-factor=1', '--hide-scrollbars'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });
page.on('pageerror', (e) => { console.error('PAGE ERROR:', e.message); process.exitCode = 1; });
page.on('console', (m) => { if (m.type() === 'error') console.error('CONSOLE:', m.text()); });

await page.goto(htmlPath, { waitUntil: 'networkidle0' });
await page.evaluate(() => (document.fonts ? document.fonts.ready : Promise.resolve()));

const hasSeek = await page.evaluate(() => typeof window.__seek === 'function');
if (!hasSeek) { console.error('window.__seek missing — aborting'); process.exit(1); }

const t0 = Date.now();
for (let t = 0; t < TOTAL; t++) {
  const sec = t / FPS;
  await page.evaluate((s) => window.__seek(s), sec);
  await page.screenshot({
    path: `${outDir}/frame_${String(t).padStart(4, '0')}.png`,
    optimizeForSpeed: true,
  });
  if (t % 150 === 0) {
    const rate = t > 0 ? Math.round(t / ((Date.now() - t0) / 1000)) : 0;
    console.log(`rendered ${t}/${TOTAL} (${rate} fps)`);
  }
}
await browser.close();
console.log(`done: ${TOTAL} frames in ${Math.round((Date.now() - t0) / 1000)}s`);
