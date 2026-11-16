// End-to-end test of the recorded voice in a real browser, served over HTTP the way the artifact serves it.
// usage: node rec.js <site dir> [scenario]
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const SITE = process.argv[2];
const ONLY = process.argv[3] || '';

function serve() {
  return new Promise(res => {
    const srv = http.createServer((req, rsp) => {
      const f = path.join(SITE, decodeURIComponent(req.url.split('?')[0]));
      if (!f.startsWith(SITE) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { rsp.writeHead(404); return rsp.end('not found'); }
      const size = fs.statSync(f).size, type = f.endsWith('.mp3') ? 'audio/mpeg' : 'text/html; charset=utf-8';
      const m = /bytes=(\d+)-(\d*)/.exec(req.headers.range || '');
      if (m) {
        const a = +m[1], b = m[2] ? +m[2] : size - 1;
        rsp.writeHead(206, { 'Content-Type': type, 'Content-Range': `bytes ${a}-${b}/${size}`, 'Content-Length': b - a + 1, 'Accept-Ranges': 'bytes' });
        fs.createReadStream(f, { start: a, end: b }).pipe(rsp);
      } else { rsp.writeHead(200, { 'Content-Type': type, 'Content-Length': size, 'Accept-Ranges': 'bytes' }); fs.createReadStream(f).pipe(rsp); }
    });
    srv.listen(0, '127.0.0.1', () => res(srv));
  });
}

const results = [];
const check = (name, ok, detail) => { results.push({ name, ok: !!ok, detail }); console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail !== undefined ? '  ' + JSON.stringify(detail) : '')); };

// What the page shows and what the audio is doing, read from outside the page's own code.
const probe = () => {
  const C = window.__C || (window.__C = JSON.parse(document.getElementById('content').textContent));
  const a = (window.__audios || [])[0];
  const on = document.querySelector('#reading .sent.on'), w = document.querySelector('#reading .w.on');
  const sid = (document.querySelector('#dock-quiz') || {}).dataset ? document.querySelector('#dock-quiz').dataset.sid : null;
  const out = { view: document.body.dataset.view, sid, line: on ? +on.dataset.i : -1, word: -1, wordText: w ? w.textContent : null,
    t: a ? a.currentTime : null, paused: a ? a.paused : null, rate: a ? a.playbackRate : null, src: a ? a.currentSrc.replace(/^.*\//, '').slice(0, 40) : null,
    ended: a ? a.ended : null, btn: (document.querySelector('#dock [data-act="play"]') || {}).textContent, clock: (document.querySelector('#dock-time') || {}).textContent,
    note: (document.querySelector('#voicenote') || {}).textContent, quizHi: !!document.querySelector('#dock-quiz.hi'), title: (document.querySelector('.label-head h1') || {}).textContent,
    ac: window.__ac ? { state: window.__ac.state, t: window.__ac.currentTime, started: window.__acStarted || 0 } : null };
  if (on && w) out.word = [...on.querySelectorAll('.w')].indexOf(w);
  const n = sid && C.narration && C.narration.cards[sid];
  if (n && out.t !== null) {      // where the highlight should be for this audio time
    const ms = out.t * 1000, T = n.t; let i = 0; while (i < T.length / 2 - 1 && T[2 * i + 2] <= ms) i++;
    const W = n.w[i]; let k = 0; while (k + 1 < W.length && W[k + 1] <= ms - T[2 * i]) k++;
    out.want = { line: i, word: ms > T[2 * i + 1] + 140 ? -1 : k };
  }
  return out;
};

async function open(browser, opts = {}) {
  const ctx = await browser.newContext({ viewport: { width: 420, height: 900 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  const errs = [];
  page.on('pageerror', e => errs.push('pageerror ' + e.message));
  page.on('console', m => { if (m.type() === 'error' && !/Failed to load resource|net::ERR/.test(m.text())) errs.push('console ' + m.text()); });
  await page.addInitScript(mode => {
    const A = window.Audio;
    window.__audios = [];
    if (mode === 'no-element') {     // an audio element that can never play, so only Web Audio is left
      window.Audio = function () { const el = new A(); el.play = () => { setTimeout(() => el.dispatchEvent(new Event('error')), 0); return Promise.reject(new DOMException('no', 'NotSupportedError')); }; window.__audios.push(el); return el; };
    } else window.Audio = function () { const el = new A(); window.__audios.push(el); return el; };
    if (mode === 'needs-tap') {      // sound is refused until the page has really been tapped
      const real = HTMLMediaElement.prototype.play; let ok = false;
      window.addEventListener('pointerdown', () => { ok = true; }, true);
      HTMLMediaElement.prototype.play = function () { return ok ? real.call(this) : Promise.reject(new DOMException('blocked', 'NotAllowedError')); };
    }
    const AC = window.AudioContext;
    window.AudioContext = function () { const ac = new AC(); window.__ac = ac; const cbs = ac.createBufferSource.bind(ac); ac.createBufferSource = () => { const s = cbs(); const st = s.start.bind(s); s.start = (...x) => { window.__acStarted = (window.__acStarted || 0) + 1; window.__acOff = x[1]; return st(...x); }; return s; }; return ac; };
  }, opts.mode || '');
  if (opts.route) await opts.route(page);
  await page.goto(opts.url);
  await page.waitForTimeout(400);
  return { ctx, page, errs };
}
async function openCard(page, sid) {
  const ch = await page.evaluate(s => { const r = document.querySelector('.secrow[data-sid="' + s + '"]'); const d = r && r.closest('details'); if (d && !d.open) { d.querySelector('summary').scrollIntoView(); return true; } return false; }, sid);
  if (ch) await page.evaluate(s => document.querySelector('.secrow[data-sid="' + s + '"]').closest('details').querySelector('summary').click(), sid);
  await page.waitForTimeout(100);
  await page.click('.secrow[data-sid="' + sid + '"]');       // a real tap: this is what allows sound
}
const settle = (page, ms) => page.waitForTimeout(ms);

(async () => {
  const srv = await serve();
  const url = `http://127.0.0.1:${srv.address().port}/pest-study.html`;
  const browser = await chromium.launch();
  const run = async (name, fn) => { if (ONLY && ONLY !== name) return; console.log('\n== ' + name); try { await fn(); } catch (e) { check(name + ' ran', false, String(e).slice(0, 300)); } };

  await run('play', async () => {
    const { ctx, page, errs } = await open(browser, { url });
    await openCard(page, 'c01-s01');
    await settle(page, 1800);
    let p = await page.evaluate(probe);
    check('opening a card starts the recording with no extra tap', p.view === 'study' && p.paused === false && p.t > 0.8, { t: p.t, src: p.src, btn: (p.btn || '').trim() });
    check('the dock shows Pause and a clock', /Pause/.test(p.btn) && /^\d:\d\d \/ \d:\d\d$/.test(p.clock || ''), p.clock);
    check('the voice note names the recorded voice', /Recorded voice/.test(p.note || ''), p.note);
    // the highlight follows the audio: sample it many times
    let same = 0, n = 0, moved = new Set(), bad = [];
    for (let i = 0; i < 40; i++) {
      await settle(page, 220);
      p = await page.evaluate(probe);
      if (!p.want) continue;
      n++; moved.add(p.line + ':' + p.word);
      if (p.line === p.want.line && (p.word === p.want.word || Math.abs(p.word - p.want.word) <= 1)) same++; else bad.push([p.t.toFixed(2), p.line, p.word, p.want.line, p.want.word]);
    }
    check('line and word highlight match the recording at ' + n + ' sample points', n >= 30 && same >= n - 1, { same, n, bad: bad.slice(0, 4) });
    check('the highlight moved through many words', moved.size >= 15, moved.size);
    // tap a later sentence
    await page.click('#reading .sent[data-i="6"]');
    await settle(page, 700);
    p = await page.evaluate(probe);
    const want6 = await page.evaluate(() => window.__C.narration.cards['c01-s01'].t[12] / 1000);
    check('tapping a sentence jumps the recording there', p.line === 6 && p.paused === false && p.t >= want6 - 0.1 && p.t < want6 + 1.5, { t: p.t, want6, line: p.line });
    // pause, resume
    await page.click('#dock [data-act="play"]');
    await settle(page, 300);
    const a = await page.evaluate(probe); await settle(page, 500); const b = await page.evaluate(probe);
    check('Pause holds the voice and keeps the highlight', a.paused === true && Math.abs(a.t - b.t) < 0.01 && /Resume/.test(a.btn) && b.line === 6, { t1: a.t, t2: b.t, btn: (a.btn || '').trim() });
    await page.click('#dock [data-act="play"]');
    await settle(page, 600);
    p = await page.evaluate(probe);
    check('Resume carries on from the same place', p.paused === false && p.t > b.t + 0.3 && p.t < b.t + 1.5, { t: p.t });
    // speed
    await page.selectOption('#sel-rate', '1.3');
    await settle(page, 300);
    p = await page.evaluate(probe);
    check('Speed changes the playback rate without restarting', Math.abs(p.rate - 1.3) < 0.001 && p.paused === false && p.t > b.t, p.rate);
    // stop
    await page.click('#dock [data-act="stop"]');
    await settle(page, 300);
    p = await page.evaluate(probe);
    check('Stop silences it and clears the highlight', p.paused === true && p.line === -1 && /Play/.test(p.btn), { line: p.line });
    // read to the end
    await page.click('#dock [data-act="play"]');
    await settle(page, 500);
    await page.evaluate(() => { const a = window.__audios[0]; a.currentTime = a.duration - 1.2; });
    await settle(page, 2600);
    p = await page.evaluate(probe);
    check('at the end the reader goes idle and the Quiz button lights up', p.quizHi && /Play/.test(p.btn) && p.view === 'study' && p.sid === 'c01-s01', { quizHi: p.quizHi, btn: (p.btn || '').trim() });
    check('no page errors', errs.length === 0, errs.slice(0, 3));
    await page.screenshot({ path: path.join(SITE, 'rec-idle.png') });      // kept with the staged site, not in the repo
    await ctx.close();
  });

  await run('chain', async () => {
    const { ctx, page, errs } = await open(browser, { url });
    await openCard(page, 'c01-s01');
    await settle(page, 800);
    await page.check('#chk-chain');
    await page.evaluate(() => { const a = window.__audios[0]; a.currentTime = a.duration - 1.0; });
    await settle(page, 3500);
    const p = await page.evaluate(probe);
    check('with "keep going" on, the next card opens and reads itself', p.sid === 'c01-s02' && p.paused === false && p.t > 0.3 && /c01-s02/.test(p.src), { sid: p.sid, t: p.t, src: p.src, title: p.title });
    await page.screenshot({ path: path.join(SITE, 'rec-playing.png') });      // kept with the staged site, not in the repo
    // leaving the card stops the voice
    await page.click('[data-act="home"]');
    await settle(page, 300);
    const q = await page.evaluate(probe);
    check('going Home stops the voice', q.view === 'home' && q.paused === true, { view: q.view, paused: q.paused });
    check('no page errors', errs.length === 0, errs.slice(0, 3));
    await ctx.close();
  });

  await run('autoplay-off', async () => {
    const { ctx, page } = await open(browser, { url });
    await openCard(page, 'c01-s01');
    await settle(page, 500);
    await page.uncheck('#chk-auto');
    await page.click('[data-act="home"]');
    await settle(page, 200);
    await openCard(page, 'c01-s02');
    await settle(page, 1200);
    let p = await page.evaluate(probe);
    check('with "read to me" off, a card opens silent', p.view === 'study' && p.sid === 'c01-s02' && (p.paused === true || p.t === 0) && /Play/.test(p.btn), { paused: p.paused, t: p.t });
    await page.click('#dock [data-act="play"]');
    await settle(page, 1200);
    p = await page.evaluate(probe);
    check('Play then starts it', p.paused === false && p.t > 0.4 && /c01-s02/.test(p.src), { t: p.t });
    await ctx.close();
  });

  await run('fetch-fallback', async () => {
    // the audio element's own request fails; the script's fetch works: the page should play from memory
    const { ctx, page, errs } = await open(browser, { url, route: page => page.route('**/audio/*.mp3', r => r.request().resourceType() === 'media' ? r.abort() : r.continue()) });
    await openCard(page, 'c01-s01');
    await settle(page, 3000);
    const p = await page.evaluate(probe);
    check('if the direct file fails, the fetched copy plays (blob)', p.paused === false && p.t > 0.5 && /^[0-9a-f-]{36}$/.test(p.src || '') && p.line >= 0, { t: p.t, src: p.src, note: p.note });
    check('no page errors', errs.length === 0, errs.slice(0, 3));
    await ctx.close();
  });

  await run('webaudio-fallback', async () => {
    const { ctx, page, errs } = await open(browser, { url, mode: 'no-element' });
    await openCard(page, 'c01-s01');
    await settle(page, 3500);
    let p = await page.evaluate(probe);
    check('if the audio element cannot play at all, Web Audio plays the recording', p.ac && p.ac.state === 'running' && p.ac.started >= 1 && p.line >= 0 && /Pause/.test(p.btn), { ac: p.ac, line: p.line, btn: (p.btn || '').trim(), note: p.note });
    const l1 = p.line, w1 = p.word;
    await settle(page, 2500);
    p = await page.evaluate(probe);
    check('and the highlight still moves', p.line > l1 || p.word !== w1, { from: [l1, w1], to: [p.line, p.word], clock: p.clock });
    await page.click('#reading .sent[data-i="8"]');
    await settle(page, 600);
    p = await page.evaluate(probe);
    check('tapping a sentence seeks in Web Audio too', p.line === 8, { line: p.line, clock: p.clock });
    await page.click('#dock [data-act="play"]'); await settle(page, 300);
    const c1 = (await page.evaluate(probe)).clock; await settle(page, 600); const c2 = (await page.evaluate(probe)).clock;
    check('Pause holds it', c1 === c2 && /\d/.test(c1 || ''), { c1, c2 });
    check('no page errors', errs.length === 0, errs.slice(0, 3));
    await ctx.close();
  });

  await run('missing-file', async () => {
    // the audio is not published at all: the page must say so and use another voice, not hang
    const { ctx, page, errs } = await open(browser, { url, route: page => page.route('**/audio/*.mp3', r => r.fulfill({ status: 404, body: 'no' })) });
    await openCard(page, 'c01-s01');
    await settle(page, 2500);
    const p = await page.evaluate(probe);
    check('a missing recording is reported and another voice is used', /could not load/.test(p.note || '') && /sound file is missing/.test(p.note || ''), { note: p.note, btn: (p.btn || '').trim() });
    check('no page errors', errs.length === 0, errs.slice(0, 3));
    await ctx.close();
  });

  await run('no-recording', async () => {
    // a card that has no recording yet keeps working with the device voice
    const sid = await (async () => { const { ctx, page } = await open(browser, { url }); const s = await page.evaluate(() => { const C = JSON.parse(document.getElementById('content').textContent); const x = C.sections.find(s => !s.practice && !(C.narration.cards[s.id])); return x ? x.id : null; }); await ctx.close(); return s; })();
    if (!sid) { console.log('every card has a recording: skipped'); return; }
    const { ctx, page, errs } = await open(browser, { url });
    await openCard(page, sid);
    await settle(page, 1200);
    const p = await page.evaluate(probe);
    check('a card without a recording opens and offers Play (' + sid + ')', p.view === 'study' && /no recording yet|device/.test(p.note || ''), { note: p.note, btn: (p.btn || '').trim() });
    check('no page errors', errs.length === 0, errs.slice(0, 3));
    await ctx.close();
  });

  await run('needs-tap', async () => {
    // a browser that refuses sound until the page has been tapped: the card must say so, and one tap on Play must work
    const strict = browser;
    const { ctx, page, errs } = await open(strict, { url, mode: 'needs-tap' });
    await page.evaluate(() => { const r = document.querySelector('.secrow[data-sid="c01-s01"]'); r.closest('details').open = true; r.click(); });   // a click made by script: no permission to play
    await settle(page, 1500);
    let p = await page.evaluate(probe);
    check('when the browser wants a tap first, the card says so and waits', p.view === 'study' && /Tap Play/.test(p.note || '') && /Play/.test(p.btn) && (p.paused === true || p.paused === null), { note: p.note, btn: (p.btn || '').trim(), paused: p.paused });
    await page.click('#dock [data-act="play"]');
    await settle(page, 1500);
    p = await page.evaluate(probe);
    check('one tap on Play then starts the recording', p.paused === false && p.t > 0.5 && p.line >= 0 && /Recorded voice/.test(p.note || ''), { t: p.t, line: p.line, note: p.note });
    check('no page errors', errs.length === 0, errs.slice(0, 3));
    await ctx.close();
  });

  await browser.close();
  srv.close();
  const failed = results.filter(r => !r.ok);
  console.log(`\n${results.length - failed.length} of ${results.length} checks passed`);
  process.exit(failed.length ? 1 : 0);
})();
