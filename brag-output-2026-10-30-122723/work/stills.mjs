import puppeteer from 'puppeteer';
import fs from 'fs';

const htmlPath = 'file://' + process.cwd() + '/work/scene_withjs.html?static';
const outDir = 'work/stills';
fs.mkdirSync(outDir, { recursive: true });

// one settled moment per scene (mid-scene, after entrance motion)
const marks = [
  ['s0_hook', 1.5], ['s1_thesis', 7], ['s2_pipeline', 13],
  ['s3_contribs', 22], ['s4_isnt', 34], ['s5_metrics', 46], ['s6_outro', 58],
];

const browser = await puppeteer.launch({
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--force-device-scale-factor=1', '--hide-scrollbars'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });
page.on('pageerror', (e) => console.error('PAGE ERROR:', e.message));
await page.goto(htmlPath, { waitUntil: 'networkidle0' });
await page.evaluate(() => (document.fonts ? document.fonts.ready : Promise.resolve()));

for (const [name, sec] of marks) {
  await page.evaluate((s) => window.__seek(s), sec);
  await page.screenshot({ path: `${outDir}/${name}.png` });
  console.log('still', name, 'at', sec + 's');
}
await browser.close();
console.log('stills done');
