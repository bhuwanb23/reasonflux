import puppeteer from 'puppeteer';
import fs from 'fs';
const htmlPath = 'file://' + process.cwd() + '/work/scene_withjs.html';
const outDir = 'work/renderframe';
fs.rmSync(outDir, {recursive:true, force:true});
fs.mkdirSync(outDir, {recursive:true});
const FPS = 30, TOTAL = 60*FPS;
(async () => {
  const b = await puppeteer.launch({args: ['--no-sandbox','--disable-setuid-sandbox']});
  const p = await b.newPage();
  await p.setViewport({width:1920,height:1080});
  await p.goto(htmlPath, {waitUntil:'networkidle0'});
  await new Promise(r => setTimeout(r, 1500));
  for (let t=0; t<TOTAL; t++) {
    await p.evaluate((sec) => {
      document.querySelectorAll('[id^=s]').forEach(el => el.classList.add('hidden'));
      const scenes = [['s0',0,3],['s1',3,10],['s2',10,14],['s3',14,24],['s4',24,36],['s5',36,48],['s6',48,60]];
      for (const [id,start,end] of scenes) {
        if (sec >= start && sec < end) {
          const el = document.getElementById(id);
          if (el) {
            el.classList.remove('hidden');
            if (id === 's1' || id === 's6') el.style.transform = 'scale(1)';
            if (id === 's6') el.style.opacity = '1';
            document.getElementById('cross').classList.remove('on');
          }
        }
      }
      const cv = document.getElementById('curve');
      if (cv) {
        const ctx = cv.getContext('2d');
        const w = cv.width, h = cv.height;
        ctx.clearRect(0,0,w,h);
        ctx.fillStyle = '#4fe0c8';
        ctx.fillRect(10,10,40,40);
      }
    }, t/FPS);
    await new Promise(r => setTimeout(r, 16));
    await p.screenshot({path: outDir + '/frame_' + String(t).padStart(4,'0') + '.png'});
    if (t % 180 === 0) console.log('rendered', t);
  }
  await b.close();
  console.log('done rendered', TOTAL, 'frames');
})().catch(e => { console.error(e.message); process.exit(1); });
