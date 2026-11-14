// A stalled or dead connection must not leave the reader silent with no message.
// usage: node cold.js <site dir>      (the dir holds pest-study.html and audio/)
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const SITE = fs.realpathSync(path.resolve(process.argv[2]));
const results = [];
const check = (name, ok, detail) => { results.push(ok); console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail !== undefined ? '  ' + JSON.stringify(detail) : '')); };

// element requests carry a Range header; the page's own fetch does not
function serve(rule) {
  const st = { hits: [] };
  const srv = http.createServer((req, rsp) => {
    let f = path.join(SITE, decodeURIComponent(req.url.split('?')[0]));
    try { f = fs.realpathSync(f); } catch (e) { rsp.writeHead(404); return rsp.end('no'); }
    if (!f.startsWith(SITE) || fs.statSync(f).isDirectory()) { rsp.writeHead(404); return rsp.end('no'); }
    const mp3 = f.endsWith('.mp3'), size = fs.statSync(f).size, type = mp3 ? 'audio/mpeg' : 'text/html; charset=utf-8';
    const go = () => {
      if (rsp.destroyed) return;
      const m = /bytes=(\d+)-(\d*)/.exec(req.headers.range || '');
      if (m) { const a = +m[1], b = m[2] ? +m[2] : size - 1; rsp.writeHead(206, { 'Content-Type': type, 'Content-Range': `bytes ${a}-${b}/${size}`, 'Content-Length': b - a + 1, 'Accept-Ranges': 'bytes', 'Cache-Control': 'no-store' }); fs.createReadStream(f, { start: a, end: b }).pipe(rsp); }
      else { rsp.writeHead(200, { 'Content-Type': type, 'Content-Length': size, 'Accept-Ranges': 'bytes', 'Cache-Control': 'no-store' }); fs.createReadStream(f).pipe(rsp); }
    };
    if (!mp3) return go();
    const kind = req.headers.range ? 'element' : 'fetch';
    st.hits.push(kind);
    const wait = rule(kind, st);
    if (wait === 0) return go();
    if (wait > 0) return setTimeout(go, wait);
    if (wait === -2) {          // sends the headers and the first bytes, then goes quiet for good
      rsp.writeHead(200, { 'Content-Type': type, 'Content-Length': size, 'Cache-Control': 'no-store' });
      rsp.write(fs.readFileSync(f).subarray(0, 20000));
      return;
    }
    // wait === -1: never answered
  });
  return new Promise(r => srv.listen(0, '127.0.0.1', () => r({ srv, st, url: `http://127.0.0.1:${srv.address().port}/pest-study.html` })));
}
const probe = () => {
  const a = (window.__audios || [])[0];
  return { t: a ? +a.currentTime.toFixed(2) : null, paused: a ? a.paused : null,
    src: a ? (a.currentSrc ? (a.currentSrc.startsWith('blob:') ? 'blob' : 'file') : '(none)') : null, rs: a ? a.readyState : null,
    btn: ((document.querySelector('#dock [data-act="play"]') || {}).textContent || '').trim(),
    note: ((document.querySelector('#voicenote') || {}).textContent || '').slice(0, 140), speaks: window.__speaks || 0 };
};
async function open(browser, url) {
  const ctx = await browser.newContext({ viewport: { width: 420, height: 900 } });
  const page = await ctx.newPage();
  const errs = []; page.on('pageerror', e => errs.push(e.message));
  await page.addInitScript(() => {
    const A = window.Audio; window.__audios = [];
    window.Audio = function () { const el = new A(); window.__audios.push(el); return el; };
    // a device voice that counts what it is asked to say and speaks nothing
    window.__speaks = 0;
    const fake = { speak: u => { window.__speaks++; setTimeout(() => { if (u.onstart) u.onstart({}); }, 30); }, cancel() {}, pause() {}, resume() {}, getVoices: () => [], speaking: false, pending: false, paused: false, onvoiceschanged: null };
    try { Object.defineProperty(window, 'speechSynthesis', { value: fake, configurable: true }); } catch (e) {}
  });
  await page.goto(url); await page.waitForTimeout(400);
  return { ctx, page, errs };
}
const openCard = async (page, sid) => {
  await page.evaluate(s => { const r = document.querySelector('.secrow[data-sid="' + s + '"]'); const d = r.closest('details'); if (d && !d.open) d.open = true; }, sid);
  await page.waitForTimeout(60); await page.click('.secrow[data-sid="' + sid + '"]');
};
const playing = x => x.btn === 'Pause' && x.t > 0.2 && x.paused === false;

async function pauseResume(browser) {
  // the element's request never answers; the fetched copy takes 1 s
  const { srv, st, url } = await serve(kind => kind === 'element' ? -1 : 1000);
  const { ctx, page, errs } = await open(browser, url);
  await openCard(page, 'c01-s01');
  await page.waitForTimeout(3000);
  await page.click('#dock [data-act="play"]'); await page.waitForTimeout(300);            // Pause, nothing has arrived
  const paused = await page.evaluate(probe);
  await page.waitForTimeout(1700);
  await page.click('#dock [data-act="play"]'); await page.waitForTimeout(500);            // Resume
  const resumed = await page.evaluate(probe);
  await page.waitForTimeout(18500);                                                       // 15 s limit + 1 s copy + margin
  const later = await page.evaluate(probe);
  check('Pause then Resume while nothing has arrived: the dock shows Resume, then Pause', paused.btn === 'Resume' && resumed.btn === 'Pause', { paused: paused.btn, resumed: resumed.btn });
  check('... and the reader does not wait on the dead request: the fetched copy plays within 20 s of Resume', playing(later) && later.src === 'blob', later);
  check('... no page errors', errs.length === 0, errs);
  await ctx.close(); srv.close();
}
async function stopPlay(browser) {
  const { srv, st, url } = await serve(kind => kind === 'element' ? -1 : 1000);
  const { ctx, page, errs } = await open(browser, url);
  await openCard(page, 'c01-s01');
  await page.waitForTimeout(3000);
  await page.click('#dock [data-act="play"]'); await page.waitForTimeout(400);            // Pause
  await page.click('#dock [data-act="stop"]'); await page.waitForTimeout(400);            // Stop
  await page.click('#dock [data-act="play"]');                                            // Play
  await page.waitForTimeout(19000);
  const later = await page.evaluate(probe);
  check('Pause, Stop, Play while nothing has arrived: the fetched copy plays within 20 s', playing(later) && later.src === 'blob', later);
  check('... no page errors', errs.length === 0, errs);
  await ctx.close(); srv.close();
}
async function dead(browser, label, fetchRule) {
  // neither the element's request nor the fetched copy completes
  const { srv, st, url } = await serve(kind => kind === 'element' ? -1 : fetchRule);
  const { ctx, page, errs } = await open(browser, url);
  await openCard(page, 'c01-s01');
  await page.waitForTimeout(14000);
  const early = await page.evaluate(probe);
  const notes = [];
  for (let k = 0; k < 12; k++) { await page.waitForTimeout(2000); const x = await page.evaluate(probe); notes.push(x.note); if (/could not load/.test(x.note)) break; }
  const end = await page.evaluate(probe);
  check(label + ': still waiting quietly at 14 s (inside the limit)', early.btn === 'Pause' && !/could not load/.test(early.note), { btn: early.btn, note: early.note });
  check(label + ': within 40 s the page says why and moves to another voice', /could not load \(the connection is too slow\)/.test(end.note) && end.speaks > 0, { note: end.note, speaks: end.speaks, fetches: st.hits.filter(h => h === 'fetch').length });
  check(label + ': no page errors', errs.length === 0, errs);
  await ctx.close(); srv.close();
}
async function slowButAlive(browser) {
  // the element's request never answers; the copy trickles in: 40 KB every 2 s (about 35 s for the file), never 15 s quiet
  const st = { hits: [] };
  const srv = http.createServer((req, rsp) => {
    let f = path.join(SITE, decodeURIComponent(req.url.split('?')[0]));
    try { f = fs.realpathSync(f); } catch (e) { rsp.writeHead(404); return rsp.end('no'); }
    const mp3 = f.endsWith('.mp3');
    if (!mp3) { rsp.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' }); return fs.createReadStream(f).pipe(rsp); }
    if (req.headers.range) return;                       // the element: never answered
    const data = fs.readFileSync(f); let at = 0;
    rsp.writeHead(200, { 'Content-Type': 'audio/mpeg', 'Content-Length': data.length, 'Cache-Control': 'no-store' });
    const tick = () => { if (rsp.destroyed) return; rsp.write(data.subarray(at, at + 40000)); at += 40000; if (at >= data.length) rsp.end(); else setTimeout(tick, 2000); };
    tick();
  });
  const url = await new Promise(r => srv.listen(0, '127.0.0.1', () => r(`http://127.0.0.1:${srv.address().port}/pest-study.html`)));
  const { ctx, page, errs } = await open(browser, url);
  await openCard(page, 'c01-s01');
  await page.waitForTimeout(15000 + 38000 + 3000);
  const later = await page.evaluate(probe);
  check('a slow copy that keeps arriving is left to finish (about 36 s), then plays', playing(later) && later.src === 'blob', later);
  await ctx.close(); srv.close();
}
(async () => {
  const browser = await chromium.launch();
  await Promise.all([pauseResume(browser), stopPlay(browser), dead(browser, 'copy never answered', -1), dead(browser, 'copy goes quiet after the first bytes', -2), slowButAlive(browser)]);
  await browser.close();
  console.log(`\n${results.filter(Boolean).length} of ${results.length} checks passed`);
  process.exit(results.every(Boolean) ? 0 : 1);
})();
