
const { FinishedLaunch } = await import('chrome-launchpad');
const opts = JSON.parse(process.argv[1]);
const launch = await FinishedLaunch.launch({ args: ['--headless=new', '--disable-gpu', '--no-sandbox', '--disable-software-rasterizer'], handleSIGINT: false, handleSIGTERM: false, handleSIGHUP: false });
const p = launch.children[0]?.process; if (!p) { console.error('no browser'); process.exit(1); }
const timeout = 60000;
let page = await launch.newPage('file://' + opts.SCENE, { timeout });
await page.setViewport({ width: parseInt(opts.W), height: parseInt(opts.H), deviceScaleFactor: 1, isMobile: false, hasTouch: false });
await page.evaluate("()=>new Promise(r=>{document.fonts?.ready?r():document.fonts.addEventListener('ready',r)})", { timeout });
await page.waitForFunction('document.readyState==="complete"', { timeout });
const N = parseInt(opts.FPS) * parseInt(opts.DUR);
for (let i = 0; i < N; i++) {
  const t = (i / parseInt(opts.FPS)) * 1000;
  await page.evaluate((t) => { window.__seek = t; }, t, { timeout });
  await page.waitForFunction(() => {
    const el = document.querySelector('#stage');
    const s = new Map();
    el.querySelectorAll('.stagecard,.col,.tc li').forEach(n => { s.set(n, s.has(n) ? s.get(n) + 1 : 1); });
    const stable = s.size === 0 ? true : Array.from(s.values()).every(v => v === 1);
    return el.offsetHeight > 0 && stable;
  }, { timeout });
  const img = await page.evaluate(({ W, H }) => {
    const c = document.createElement('canvas'); c.width = W; c.height = H;
    c.getContext('2d').drawImage(document.querySelector('#stage'), 0, 0, W, H);
    return c.toDataURL('image/png');
  }, { W: parseInt(opts.W), H: parseInt(opts.H) }, { timeout });
  const raw = Buffer.from(img.split(',')[1], 'base64');
  await require('fs').promises.writeFile(opts.OUT + '/f' + String(i).padStart(4, '0') + '.png', raw, { mode: 0o644 });
}
await page.close();
await launch.kill();
console.log('frames', N);
