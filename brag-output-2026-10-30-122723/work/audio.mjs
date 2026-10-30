import { createWriteStream } from 'node:fs';
import { once } from 'node:events';

const SR = 48000;
const DUR = 60;
const N = SR * DUR;

const gain = new Float32Array(N);

const BPM = 92;
const BEAT = 60 / BPM;
const beat = (t) => t / BEAT;

function rand(a, b) { return a + Math.random() * (b - a); }
function smooth(t) { return t * t * (3 - 2 * t); }
function lerp(a, b, t) { return a + (b - a) * t; }

function bank(t, freq, amps) {
  let s = 0;
  for (let i = 0; i < amps.length; i++) {
    s += amps[i] * Math.sin(2 * Math.PI * freq * (i + 1) * t);
  }
  return s;
}

function kick(at, dur) {
  const start = Math.floor(at * SR);
  const n = Math.min(N, start + Math.floor(dur * SR));
  for (let i = start; i < n; i++) {
    const tt = (i - start) / SR;
    const env = Math.exp(-18 * tt);
    const f = 95 - 70 * smooth(i / n);
    gain[i] += env * Math.sin(2 * Math.PI * f * tt) * 0.9;
  }
}

function snap(at) {
  const start = Math.floor(at * SR);
  const n = Math.min(N, start + 600);
  for (let i = start; i < n; i++) {
    const tt = (i - start) / SR;
    const env = Math.exp(-32 * tt);
    gain[i] += (Math.random() * 2 - 1) * env * 0.18;
    gain[i] += Math.sin(2 * Math.PI * 2600 * tt) * env * 0.08;
  }
}

function padSwell(at, dur, freq, amps, scale) {
  const start = Math.floor(at * SR);
  const n = Math.min(N, start + Math.floor(dur * SR));
  for (let i = start; i < n; i++) {
    const tt = (i - start) / SR;
    const env = Math.exp(-2.2 * tt);
    gain[i] += env * bank(tt, freq, amps) * scale;
  }
}

function lowBed() {
  for (let i = 0; i < N; i++) {
    const t = i / SR;
    const side = 1 - 0.28 * Math.max(0, 1 - 24 * (t % BEAT) / BEAT);
    const seq = Math.sin(2 * Math.PI * 0.5 * t) * 0.18 +
                Math.sin(2 * Math.PI * 1.0 * t) * 0.12;
    gain[i] += seq * side * 0.5;
  }
}

function pulseStream() {
  for (let i = 0; i < N; i++) {
    const t = i / SR;
    const blip = Math.sin(2 * Math.PI * 118 * (t + 0.18 * Math.sin(2 * Math.PI * 0.6 * t))) *
                Math.max(0, Math.sin(Math.PI * ((t * 24) % 1)));
    gain[i] += blip * 0.10;
  }
}

function structureHits() {
  const on = [0, 3, 10, 14, 24, 36, 48];
  for (const s of on) {
    kick(s, 0.35);
    snap(s);
    padSwell(s, 1.2, s === 0 ? 55 : 73, [1, 0.6, 0.35, 0.2], 0.06);
  }
}

function endRise() {
  const t0 = 48;
  for (let i = 0; i < N; i++) {
    const t = i / SR;
    if (t < t0) continue;
    const u = smooth((t - t0) / 8);
    const seq = Math.sin(2 * Math.PI * 1.0 * t) * 0.10 +
                Math.sin(2 * Math.PI * 1.5 * t) * 0.07;
    gain[i] += seq * u * 0.6;
  }
  const start = Math.floor(58 * SR);
  const n = Math.min(N, start + Math.floor(1.6 * SR));
  for (let i = start; i < n; i++) {
    const tt = (i - start) / SR;
    const env = Math.exp(-2.0 * tt);
    gain[i] += env * Math.sin(2 * Math.PI * 68 * tt) * 0.14;
  }
}

function haze() {
  for (let i = 0; i < N; i++) {
    const t = i / SR;
    const nh = Math.random() * 2 - 1;
    gain[i] += nh * 0.006 * (0.5 + 0.5 * Math.sin(2 * Math.PI * 0.2 * t));
  }
}

lowBed();
pulseStream();
structureHits();
endRise();
haze();

let peak = 0;
for (let i = 0; i < N; i++) {
  if (Math.abs(gain[i]) > peak) peak = Math.abs(gain[i]);
}
const g = peak > 0 ? 0.92 / peak : 1;
for (let i = 0; i < N; i++) gain[i] *= g;

const file = createWriteStream('music.pcm');
const BUF = new Uint8Array(4 * SR);
let written = 0;
function nextChunk() {
  let pos = 0;
  let i = written;
  while (i < N && pos + 2 <= BUF.length) {
    const v = Math.max(-32768, Math.min(32767, Math.round(gain[i] * 32767)));
    BUF[pos++] = v & 0xff;
    BUF[pos++] = (v >> 8) & 0xff;
    i++;
  }
  written = i;
  return { buf: BUF.subarray(0, pos), done: i >= N };
}
async function run() {
  for (;;) {
    const { buf, done } = nextChunk();
    if (buf.length === 0 && done) break;
    await new Promise((resolve, reject) => {
      file.write(buf, (err) => { if (err) reject(err); else resolve(); });
    });
    if (done) break;
  }
  file.end();
  await once(file, 'finish');
  console.log('wrote music.pcm', N, 'samples');
}
run().catch((e) => { console.error(e); process.exit(1); });
