// Test of the live Claude voice path and its fallbacks, with a stand-in for the platform's tts capability.
// usage: node claude.js <site dir>
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const SITE = process.argv[2];

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
const check = (name, ok, detail) => { results.push({ name, ok: !!ok }); console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail !== undefined ? '  ' + JSON.stringify(detail) : '')); };

// A stand-in for claude.use('tts'): speaks each line for a short fixed time and follows the documented events.
const fakeClaude = () => {
  const A = window.Audio; window.__audios = [];
  window.Audio = function () { const el = new A(); window.__audios.push(el); return el; };
  let stateCbs = [], lineCbs = [], posCbs = [], cur = null, state = 'idle';
  window.__tts = { calls: 0, stops: 0, fail: null, lineMs: 400, log: [] };
  const set = (s, reason) => { state = s; window.__tts.log.push(s + (reason ? ':' + reason : '')); stateCbs.forEach(f => f({ state: s, reason })); };
  const end = (job, reason, err) => { clearInterval(job.timer); if (cur === job) cur = null; set('idle', reason); if (err) job.reject(err); else job.resolve({ playedMs: 1 }); };
  function speak(lines) {
    window.__tts.calls++;
    if (window.__tts.fail) { const code = window.__tts.fail; return new Promise((_, rej) => setTimeout(() => { set('idle', code); rej({ code, message: code }); }, 30)); }
    if (cur) end(cur, 'replaced', { code: 'stopped', reason: 'replaced' });
    return new Promise((resolve, reject) => {
      const job = { lines: typeof lines === 'string' ? [{ text: lines }] : lines, i: 0, ms: 0, paused: false, resolve, reject, timer: null };
      cur = job; set('starting');
      setTimeout(() => {
        if (cur !== job) return;
        set('speaking');
        lineCbs.forEach(f => f({ line: 0, id: job.lines[0].id })); posCbs.forEach(f => f({ ms: 0, line: 0, id: job.lines[0].id }));
        job.timer = setInterval(() => {
          if (job.paused || cur !== job) return;
          job.ms += 100;
          if (job.ms >= window.__tts.lineMs) {
            job.i++; job.ms = 0;
            if (job.i >= job.lines.length) return end(job, 'completed');
            lineCbs.forEach(f => f({ line: job.i, id: job.lines[job.i].id }));
          }
          posCbs.forEach(f => f({ ms: job.ms, line: job.i, id: job.lines[job.i].id }));
        }, 100);
      }, 40);
    });
  }
  const tts = {
    speak, add: speak,
    stop: () => { window.__tts.stops++; if (cur) { const j = cur; setTimeout(() => end(j, 'stopped', { code: 'stopped', reason: 'stopped' }), 60); } return Promise.resolve(); },   // the idle event arrives late, as it can on the real platform
    pause: () => { if (cur) { cur.paused = true; set('paused'); } return Promise.resolve(); },
    resume: () => { if (cur) { cur.paused = false; set('speaking'); } return Promise.resolve(); },
    setRate: () => Promise.resolve(), active: () => state !== 'idle', voices: () => Promise.resolve(['buttery', 'airy']), languages: () => Promise.resolve(['en']),
    onState: f => { stateCbs.push(f); return () => {}; }, onLine: f => { lineCbs.push(f); return () => {}; }, onPosition: f => { posCbs.push(f); return () => {}; },
  };
  window.claude = { use: name => Promise.resolve(name === 'tts' ? tts : null) };
};
const probe = () => {
  const a = (window.__audios || [])[0];
  const on = document.querySelector('#reading .sent.on'), w = document.querySelector('#reading .w.on');
  return { view: document.body.dataset.view, line: on ? +on.dataset.i : -1, word: w ? w.textContent : null,
    btn: ((document.querySelector('#dock [data-act="play"]') || {}).textContent || '').trim(), playDisabled: !!(document.querySelector('#dock [data-act="play"]') || {}).disabled,
    stop: !!document.querySelector('#dock [data-act="stop"]'), note: (document.querySelector('#voicenote') || {}).textContent,
    engines: [...document.querySelectorAll('#sel-engine option')].map(o => o.value), style: !!document.querySelector('#sel-voice'),
    quizHi: !!document.querySelector('#dock-quiz.hi'), sid: (document.querySelector('#dock-quiz') || { dataset: {} }).dataset.sid,
    audio: a ? { paused: a.paused, t: a.currentTime, src: a.currentSrc.replace(/^.*\//, '').slice(0, 30) } : null, tts: window.__tts };
};
async function openCard(page, sid) {
  await page.evaluate(s => { const r = document.querySelector('.secrow[data-sid="' + s + '"]'); const d = r && r.closest('details'); if (d && !d.open) d.querySelector('summary').click(); }, sid);
  await page.waitForTimeout(100);
  await page.click('.secrow[data-sid="' + sid + '"]');
}

(async () => {
  const srv = await serve();
  const url = `http://127.0.0.1:${srv.address().port}/pest-study.html`;
  const browser = await chromium.launch();
  const fresh = async () => {
    const ctx = await browser.newContext({ viewport: { width: 420, height: 900 } });
    const page = await ctx.newPage(); const errs = [];
    page.on('pageerror', e => errs.push(e.message));
    await page.addInitScript(fakeClaude);
    await page.goto(url); await page.waitForTimeout(400);
    return { ctx, page, errs };
  };
  const wait = (page, ms) => page.waitForTimeout(ms);

  console.log('\n== claude voice');
  {
    const { ctx, page, errs } = await fresh();
    await openCard(page, 'c01-s01');
    await wait(page, 700);
    let p = await page.evaluate(probe);
    check('where the Claude voice is offered, opening a card uses it', p.tts.calls === 1 && /Pause/.test(p.btn) && p.stop && p.line >= 0 && /Claude voice/.test(p.note || '') && (!p.audio || p.audio.paused), { calls: p.tts.calls, btn: p.btn, line: p.line, note: p.note });
    check('the Voice menu offers the Claude voice and its styles', p.engines.includes('claude') && p.engines.includes('rec') && p.style, p.engines);
    const l0 = p.line; await wait(page, 1300); p = await page.evaluate(probe);
    check('the highlight follows the Claude voice from sentence to sentence', p.line > l0 && p.word, { from: l0, to: p.line, word: p.word });
    await page.click('#reading .sent[data-i="9"]');
    await wait(page, 500); p = await page.evaluate(probe);
    check('tapping a sentence restarts the Claude voice there and it keeps going', p.line >= 9 && p.line <= 10 && /Pause/.test(p.btn) && p.tts.calls === 2, { line: p.line, btn: p.btn, log: p.tts.log.slice(-4) });
    await wait(page, 900); p = await page.evaluate(probe);
    check('the reading did not die after the restart', p.line >= 11 && /Pause/.test(p.btn), { line: p.line, btn: p.btn });
    await page.click('#dock [data-act="play"]'); await wait(page, 300); p = await page.evaluate(probe);
    const held = p.line; await wait(page, 700); let q = await page.evaluate(probe);
    check('Pause holds the Claude voice', /Resume/.test(p.btn) && q.line === held, { btn: p.btn, line: held });
    await page.click('#dock [data-act="play"]'); await wait(page, 900); q = await page.evaluate(probe);
    check('Resume continues', /Pause/.test(q.btn) && q.line > held, { line: q.line });
    await page.click('#dock [data-act="stop"]'); await wait(page, 30); p = await page.evaluate(probe);
    check('Stop goes idle at once and clears the highlight', /Play/.test(p.btn) && p.line === -1 && !p.stop, { btn: p.btn });
    // Play again right away, before the old reading's late idle event arrives
    await page.click('#dock [data-act="play"]'); await wait(page, 400); p = await page.evaluate(probe);
    check('Play straight after Stop starts a new reading that a late event cannot end', /Pause/.test(p.btn) && p.line >= 0, { btn: p.btn, line: p.line, log: p.tts.log.slice(-5) });
    await wait(page, 600); p = await page.evaluate(probe);
    check('and it is still reading', /Pause/.test(p.btn) && p.line >= 1, { line: p.line });
    await page.evaluate(() => { window.__tts.lineMs = 100; });
    await wait(page, 5200); p = await page.evaluate(probe);
    check('when the Claude voice finishes the card, the Quiz button lights up', /Play/.test(p.btn) && p.quizHi, { btn: p.btn, quizHi: p.quizHi });
    check('no page errors', errs.length === 0, errs.slice(0, 3));
    await ctx.close();
  }

  console.log('\n== claude voice hits its limit');
  {
    const { ctx, page, errs } = await fresh();
    await page.evaluate(() => { window.__tts.fail = 'rate_limited'; });
    await openCard(page, 'c01-s01');
    await wait(page, 1800);
    const p = await page.evaluate(probe);
    check('if the Claude voice is rate limited, the recording takes over by itself', p.audio && p.audio.paused === false && p.audio.t > 0.3 && /recorded voice took over/.test(p.note || '') && /Pause/.test(p.btn), { audio: p.audio, note: p.note });
    check('no page errors', errs.length === 0, errs.slice(0, 3));
    await ctx.close();
  }

  console.log('\n== reading aloud turned off by the viewer');
  {
    const { ctx, page, errs } = await fresh();
    await page.evaluate(() => { window.__tts.fail = 'not_granted'; });
    await openCard(page, 'c01-s01');
    await wait(page, 900);
    let p = await page.evaluate(probe);
    check('if the viewer turned reading aloud off, nothing speaks on its own', (!p.audio || p.audio.paused) && /turned off/.test(p.note || '') && /Play/.test(p.btn) && p.playDisabled, { audio: p.audio, note: p.note, disabled: p.playDisabled });
    check('the device voice is no longer offered, the recording still is', !p.engines.includes('device') && !p.engines.includes('claude') && p.engines.includes('rec'), p.engines);
    await page.selectOption('#sel-engine', 'rec'); await wait(page, 200);
    await page.click('#dock [data-act="play"]'); await wait(page, 1500);
    p = await page.evaluate(probe);
    check('picking the recorded voice by hand then plays it', p.audio && p.audio.paused === false && p.audio.t > 0.3, { audio: p.audio, note: p.note });
    check('no page errors', errs.length === 0, errs.slice(0, 3));
    await ctx.close();
  }

  console.log('\n== keep going prefers the recording');
  {
    const { ctx, page, errs } = await fresh();
    await openCard(page, 'c01-s01');
    await wait(page, 500);
    await page.check('#chk-chain'); await wait(page, 100);
    await page.click('#dock [data-act="stop"]'); await wait(page, 200);
    await page.click('#dock [data-act="play"]'); await wait(page, 1500);
    const p = await page.evaluate(probe);
    check('with "keep going" on, Best available uses the recording even where the Claude voice exists', p.audio && p.audio.paused === false && p.audio.t > 0.3 && /Recorded voice/.test(p.note || ''), { audio: p.audio, note: p.note, calls: p.tts.calls });
    check('no page errors', errs.length === 0, errs.slice(0, 3));
    await ctx.close();
  }

  await browser.close(); srv.close();
  const failed = results.filter(r => !r.ok);
  console.log(`\n${results.length - failed.length} of ${results.length} checks passed`);
  process.exit(failed.length ? 1 : 0);
})();
