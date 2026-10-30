import puppeteer from 'puppeteer';
const htmlPath = 'file://' + process.cwd() + '/work/scene_withjs.html';
(async () => {
  const b = await puppeteer.launch({args: ['--no-sandbox','--disable-setuid-sandbox']});
  const p = await b.newPage();
  await p.setViewport({width:1920,height:1080});
  await p.goto(htmlPath, {waitUntil:'networkidle0'});
  await new Promise(r => setTimeout(r, 5000));
  const f = await p.screenshot({path: 'work/dompnp.png'});
  await b.close();
  console.log('screenshot done', f.length);
})().catch(e => { console.error(e.message); process.exit(1); });
