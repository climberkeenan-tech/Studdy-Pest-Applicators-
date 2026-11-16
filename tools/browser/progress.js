// Does progress really save, and does the day streak really work? Real Chromium, several "devices"
// (browser contexts) that share one stand-in account, and a calendar the test can move.
// usage: node progress.js <site dir> [scenario]      (the dir holds pest-study.html and audio/)
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const SITE = fs.realpathSync(path.resolve(process.argv[2]));
const ONLY = process.argv[3] || '';
const results = [];
const check = (name, ok, detail) => { results.push(ok); console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail !== undefined ? '  ' + JSON.stringify(detail).slice(0, 420) : '')); };
const LS = 'pas-profile-v1';

function serve() {
  const srv = http.createServer((req, rsp) => {
    let f = path.join(SITE, decodeURIComponent(req.url.split('?')[0]));
    try { f = fs.realpathSync(f); } catch (e) { rsp.writeHead(404); return rsp.end('no'); }
    if (!f.startsWith(SITE) || fs.statSync(f).isDirectory()) { rsp.writeHead(404); return rsp.end('no'); }
    const size = fs.statSync(f).size, type = f.endsWith('.mp3') ? 'audio/mpeg' : 'text/html; charset=utf-8';
    const m = /bytes=(\d+)-(\d*)/.exec(req.headers.range || '');
    if (m) { const a = +m[1], b = m[2] ? +m[2] : size - 1; rsp.writeHead(206, { 'Content-Type': type, 'Content-Range': `bytes ${a}-${b}/${size}`, 'Content-Length': b - a + 1, 'Accept-Ranges': 'bytes' }); fs.createReadStream(f, { start: a, end: b }).pipe(rsp); }
    else { rsp.writeHead(200, { 'Content-Type': type, 'Content-Length': size, 'Accept-Ranges': 'bytes' }); fs.createReadStream(f).pipe(rsp); }
  });
  return new Promise(r => srv.listen(0, '127.0.0.1', () => r({ srv, url: `http://127.0.0.1:${srv.address().port}/pest-study.html` })));
}

// What runs in the page before its own script: a calendar the test can move, and the account stand-in.
const inPage = () => {
  const R = Date;
  window.__off = +(localStorage.getItem('__test_off') || 0);
  function D(...a) { if (!new.target) return new R(R.now() + window.__off).toString(); return a.length ? new R(...a) : new R(R.now() + window.__off); }
  D.now = () => R.now() + window.__off; D.parse = R.parse; D.UTC = R.UTC; D.prototype = R.prototype;
  window.Date = D;
  const A = window.Audio; window.__audios = [];
  window.Audio = function () { const el = new A(); window.__audios.push(el); return el; };
  const down = () => ({ code: 'unavailable', message: 'the account cannot be reached' });
  const doc = {
    get: async () => { let d; try { d = await window.__acctGet(); } catch (e) { throw down(); } return { id: 'profile', exists: d !== null && d !== undefined, data: () => d, metadata: { fromCache: false, hasPendingWrites: false } }; },
    set: async v => { try { await window.__acctSet(JSON.parse(JSON.stringify(v))); } catch (e) { throw down(); } },
  };
  window.claude = { use: name => Promise.resolve(name === 'db' ? { doc: () => doc } : name === 'user' ? { id: () => Promise.resolve('u_test') } : null) };
};

// One account, any number of devices. A device is a browser context with its own storage and its own connection.
async function world(browser, url) {
  const acct = { doc: null, gets: 0, sets: 0 };
  const devices = [];
  async function device(opts) {
    const dev = { down: false, hang: false, lateNext: 0, slowGetNext: 0, flying: 0, overlap: 0 };      // slowGetNext: the next read answers after that many ms, with what the account held when it was asked      // down: calls fail at once. hang: calls never answer. lateNext: the next write lands after that many ms.
    dev.ctx = await browser.newContext({ viewport: { width: 420, height: 900 }, timezoneId: (opts && opts.timezoneId) || 'America/New_York', locale: 'en-US' });
    await dev.ctx.exposeFunction('__acctGet', () => {
      if (dev.hang) return new Promise(() => {});
      if (dev.down) throw new Error('down');
      acct.gets++;
      if (dev.slowGetNext) { const ms = dev.slowGetNext, then = acct.doc; dev.slowGetNext = 0; return new Promise(r => setTimeout(() => r(then), ms)); }
      return acct.doc;
    });
    await dev.ctx.exposeFunction('__acctSet', v => {
      if (dev.hang) return new Promise(() => {});
      if (dev.down) throw new Error('down');
      if (dev.flying) dev.overlap++;                    // a write sent while an earlier one from this device had not settled
      if (dev.lateNext) { const ms = dev.lateNext; dev.lateNext = 0; dev.flying++; return new Promise(r => setTimeout(() => { acct.sets++; acct.doc = v; dev.flying--; r(); }, ms)); }
      acct.sets++; acct.doc = v;
    });
    await dev.ctx.addInitScript(inPage);
    if (opts && opts.noFrames) await dev.ctx.addInitScript(() => { window.requestAnimationFrame = () => 0; window.cancelAnimationFrame = () => {}; });      // a page that is not on screen gets no animation frames
    if (opts && opts.noAccount) await dev.ctx.addInitScript(() => { window.claude = { use: () => Promise.resolve(null) }; });
    if (opts && opts.noStorage) await dev.ctx.addInitScript(() => { const real = Storage.prototype.setItem; Storage.prototype.setItem = function (k, v) { if (String(k).startsWith('pas-profile-v1')) throw new DOMException('refused', 'QuotaExceededError'); return real.call(this, k, v); }; });
    dev.errs = [];
    dev.tab = async () => { const page = await dev.ctx.newPage(); page.on('pageerror', e => dev.errs.push(e.message)); await page.goto(url); await page.waitForSelector('.mission'); await page.waitForTimeout(500); return page; };
    devices.push(dev);
    return dev;
  }
  return { acct, device, close: async () => { for (const d of devices) await d.ctx.close(); }, errs: () => devices.flatMap(d => d.errs) };
}
// Move the device's calendar to a local date and time ("2026-11-16T15:00:00"). The clock keeps running from there.
const setNow = (page, iso) => page.evaluate(t => { const off = new Date(t).getTime() - (Date.now() - window.__off); window.__off = off; localStorage.setItem('__test_off', String(off)); }, iso);
const prof = page => page.evaluate(k => JSON.parse(localStorage.getItem(k) || 'null'), LS);
const home = async page => { if (await page.evaluate(() => document.body.dataset.view) !== 'home') { await page.click('header .brand'); await page.waitForSelector('.mission'); } };
const stats = page => page.evaluate(() => {
  const tile = name => { const s = [...document.querySelectorAll('.stat')].find(x => (x.querySelector('.lbl') || {}).textContent === name); return s ? (s.querySelector('b') || {}).textContent.replace(/\s+/g, ' ').trim() : null; };
  return { streak: tile('Day streak'), today: tile('Today'), hint: (document.querySelector('#streak-hint') || {}).textContent || null,
    dots: document.querySelectorAll('.dots i.on').length, xp: (document.querySelector('#chip-xp') || {}).textContent,
    saved: (document.querySelector('#sync-text') || document.querySelector('#foot span') || {}).textContent || '', progress: (document.querySelector('.panel .mono') || {}).textContent };
});
const rowPills = (page, sid) => page.evaluate(s => [...document.querySelectorAll('.secrow[data-sid="' + s + '"] .pill')].map(x => x.textContent.trim()), sid);
async function openCard(page, sid) {
  await home(page);
  await page.evaluate(s => { const r = document.querySelector('.secrow[data-sid="' + s + '"]'); const d = r.closest('details'); if (d && !d.open) d.open = true; }, sid);
  await page.click('.secrow[data-sid="' + sid + '"]');
  await page.waitForSelector('#reading');
}
async function startQuiz(page, sid) { await openCard(page, sid); await page.click('.view > button[data-act="quiz"]'); await page.waitForSelector('.qcard'); }
// Answer the question on screen, right or wrong. Leaves the feedback showing.
async function answer(page, right) {
  // the page keeps its state to itself, so the question on screen is looked up in the page's content by its text
  const q = await page.evaluate(() => {
    if (!window.__Q) { window.__Q = {}; for (const s of JSON.parse(document.getElementById('content').textContent).sections) for (const x of s.questions || []) window.__Q[String(x.q).replace(/\*\*/g, '')] = x; }
    const x = window.__Q[document.querySelector('.qtext').textContent];
    return x ? { id: x.id, kind: x.kind, answer: x.answer, n: (x.choices || []).length } : null;
  });
  if (!q) throw new Error('the question on screen was not found in the content');
  if (q.kind === 'mc') await page.click(`.choice[data-k="${right ? q.answer : (q.answer + 1) % q.n}"]`);
  else if (q.kind === 'tf') await page.click(`.choice[data-v="${right ? q.answer : !q.answer}"]`);
  else { await page.fill('#short-in', right ? String(q.answer) : 'zebra crossing'); await page.click('form.short button[type="submit"]'); }
  await page.waitForSelector('#btn-next', { timeout: 20000 });
  return q.id;
}
const next = async page => { await page.click('#btn-next'); await page.waitForTimeout(40); };
// Answer everything right until the result shows.
async function passQuiz(page) { let n = 0; while (await page.evaluate(() => document.body.dataset.view) === 'quiz') { await answer(page, true); await next(page); if (++n > 60) throw new Error('quiz does not end'); } return n; }
const wait = (page, ms) => page.waitForTimeout(ms);
const run = async (name, fn) => { if (ONLY && ONLY !== name) return; try { await fn(); } catch (e) { check(name + ': the scenario ran', false, String(e && e.stack || e).slice(0, 600)); } };

(async () => {
  const { srv, url } = await serve();
  const browser = await chromium.launch();

  await run('save', async () => {
    const w = await world(browser, url); const A = await w.device(); let a = await A.tab();
    await setNow(a, '2026-11-16T15:00:00'); await a.reload(); await a.waitForSelector('.mission'); await wait(a, 600);
    const first = (await stats(a)).saved;
    check('a first visit does not claim anything was saved', /Nothing to save yet/.test(first), first);
    await startQuiz(a, 'c01-s01');
    const qid = await answer(a, true);
    let p = await prof(a);
    check('an answer is saved on the device at once', !!(p.q[qid] && p.q[qid].seen === 1 && p.days['2026-11-16'] && p.days['2026-11-16'].a === 1 && p.xp > 0), { q: p.q[qid], day: p.days['2026-11-16'] });
    await wait(a, 2000);
    check('... and in the account within 2 seconds', !!(w.acct.doc && w.acct.doc.q[qid] && w.acct.doc.days['2026-11-16'].a === 1), { sets: w.acct.sets, q: w.acct.doc && w.acct.doc.q[qid] });
    await next(a);
    const qid2 = await answer(a, true);
    await a.reload();                                             // closed within a blink of answering: the save to the account never ran
    await a.waitForSelector('.mission'); await wait(a, 2500);
    check('an answer given just before the page was closed reaches the account at the next visit', !!(w.acct.doc && w.acct.doc.q[qid2] && w.acct.doc.days['2026-11-16'].a === 2), { q: w.acct.doc && w.acct.doc.q[qid2], day: w.acct.doc && w.acct.doc.days['2026-11-16'] });
    const s = await stats(a);
    check('the home page shows it: answered today, streak 1, saved to the account with a time', /^2 \/ 25/.test(s.today || '') && s.streak === '1' && /saved to your account/.test(s.saved) && /last saved \d+:\d\d [AP]M/.test(s.saved), s);
    check('no page errors (save)', w.errs().length === 0, w.errs());
    await w.close();
  });

  await run('two-devices', async () => {
    const w = await world(browser, url); const A = await w.device(), B = await w.device();
    const a = await A.tab();
    await startQuiz(a, 'c01-s01'); const n = await passQuiz(a);
    await a.waitForSelector('.stamp'); await wait(a, 2200);
    const res = await a.evaluate(() => ({ stamp: document.querySelector('.stamp').textContent, saved: (document.querySelector('#saved-line') || {}).textContent || '' }));
    check('passing a card says Passed and that it was saved', res.stamp === 'Passed' && /saved to your account/.test(res.saved), Object.assign({ questions: n }, res));
    const b = await B.tab(); await wait(b, 800);
    const s = await stats(b), pills = await rowPills(b, 'c01-s01');
    check('a second device shows the same progress: the card Passed, the XP, the streak', pills.includes('Passed') && s.streak === '1' && s.xp !== '0' && s.xp === (await stats(await (async () => { await home(a); return a; })())).xp, { pills, s });
    check('no page errors (two devices)', w.errs().length === 0, w.errs());
    await w.close();
  });

  await run('stale-tab', async () => {
    const w = await world(browser, url); const A = await w.device(), B = await w.device();
    const a = await A.tab();                                      // device A: the page is open and stays open
    const b = await B.tab();
    await startQuiz(b, 'c01-s01'); await passQuiz(b); await wait(b, 2200);      // device B: a card passed, saved
    const afterB = JSON.parse(JSON.stringify(w.acct.doc));
    await startQuiz(a, 'c01-s02'); const qid = await answer(a, true); await wait(a, 2500);      // back on A, never reloaded
    const d = w.acct.doc;
    check('a page left open on one device does not wipe what another device saved', !!(d.passed['c01-s01'] && Object.keys(afterB.q).every(k => d.q[k] && d.q[k].seen >= afterB.q[k].seen) && d.xp >= afterB.xp), { passed: Object.keys(d.passed), xp: d.xp, xpAfterB: afterB.xp });
    check('... and its own new answer is saved too', !!(d.q[qid] && d.q[qid].seen === 1), d.q[qid]);
    await home(a);
    check('... and it now shows the other device\'s passed card without a reload', (await rowPills(a, 'c01-s01')).includes('Passed'), await rowPills(a, 'c01-s01'));
    // a third device opens, hidden for a while, comes back: it catches up without a tap
    const C = await w.device(); const c = await C.tab();
    await startQuiz(b, 'c01-s02'); await passQuiz(b); await wait(b, 2200);
    await c.evaluate(() => { window.__off += 60000; document.dispatchEvent(new Event('visibilitychange')); });
    await wait(c, 1200);
    check('a page that comes back into view catches up by itself', (await rowPills(c, 'c01-s02')).includes('Passed'), await rowPills(c, 'c01-s02'));
    check('no page errors (stale tab)', w.errs().length === 0, w.errs());
    await w.close();
  });

  await run('two-tabs', async () => {
    const w = await world(browser, url); const A = await w.device();
    const t1 = await A.tab(), t2 = await A.tab();                 // same device, two tabs
    await startQuiz(t2, 'c01-s01'); await passQuiz(t2); await wait(t2, 2200);
    await startQuiz(t1, 'c01-s02'); const qid = await answer(t1, true); await wait(t1, 2500);
    const d = w.acct.doc, local = await prof(t1);
    check('two tabs on one device: neither wipes the other in the account', !!(d.passed['c01-s01'] && d.q[qid]), { passed: Object.keys(d.passed), q: d.q[qid] });
    check('... or on the device', !!(local.passed['c01-s01'] && local.q[qid]), { passed: Object.keys(local.passed) });
    await w.close();
  });

  await run('offline', async () => {
    const w = await world(browser, url); const A = await w.device(), B = await w.device();
    const a = await A.tab();
    A.down = true;                                                // device A loses its connection after loading
    await startQuiz(a, 'c01-s02'); const q1 = await answer(a, true); await next(a); const q2 = await answer(a, false); await wait(a, 2500);
    const mid = await a.evaluate(() => ({ view: document.body.dataset.view }));
    const b = await B.tab(); await startQuiz(b, 'c01-s01'); await passQuiz(b); await wait(b, 2200);      // meanwhile device B passes a card
    await home(a); const sOff = await stats(a);
    check('with no connection the page says so and keeps the answers on the device', /Could not reach your account/.test(sOff.saved) && !!(await prof(a)).q[q1], { saved: sOff.saved, mid });
    A.down = false;
    await a.reload(); await a.waitForSelector('.mission'); await wait(a, 2500);
    const d = w.acct.doc;
    check('back online: the account holds both devices\' work', !!(d.passed['c01-s01'] && d.q[q1] && d.q[q1].right === 1 && d.q[q2] && d.q[q2].wrong === 1 && d.q[q2].open === true), { passed: Object.keys(d.passed), q1: d.q[q1], q2: d.q[q2] });
    check('... and so does the device that was offline', (await rowPills(a, 'c01-s01')).includes('Passed'), await rowPills(a, 'c01-s01'));
    // the connection drops and comes back without a reload: the page retries by itself
    A.down = true;
    await startQuiz(a, 'c01-s03'); const q3 = await answer(a, true); await wait(a, 1500);
    A.down = false;
    await a.evaluate(() => window.dispatchEvent(new Event('online')));
    await wait(a, 1500);
    check('the connection comes back while the page is open: saved without a reload', !!(w.acct.doc.q[q3]), w.acct.doc.q[q3]);
    check('no page errors (offline)', w.errs().length === 0, w.errs());
    await w.close();
  });

  await run('no-answer', async () => {
    const w = await world(browser, url); const A = await w.device(); const a = await A.tab();
    A.hang = true;                                                // the account stops answering: no error, just silence
    await startQuiz(a, 'c01-s01'); const q1 = await answer(a, true);
    await home(a); await wait(a, 3000);
    const early = await stats(a);
    await wait(a, 14000);
    const late = await stats(a);
    check('an account that never answers: the page waits 15 seconds, then says it could not reach it', /Saving to your account/.test(early.saved) && /Could not reach your account/.test(late.saved), { early: early.saved, late: late.saved });
    A.hang = false;
    await startQuiz(a, 'c01-s01'); const q2 = await answer(a, true); await wait(a, 2500);      // the next answer finds the account answering again
    check('... and it is not stuck: once the account answers, everything is saved', !!(w.acct.doc && w.acct.doc.q[q1] && w.acct.doc.q[q2]), { q1: w.acct.doc && w.acct.doc.q[q1], q2: w.acct.doc && w.acct.doc.q[q2] });
    await home(a);
    check('... and the page says so', /saved to your account/.test((await stats(a)).saved), (await stats(a)).saved);
    check('no page errors (no answer)', w.errs().length === 0, w.errs());
    await w.close();
  });

  await run('two-tabs-offline', async () => {
    const w = await world(browser, url); const A = await w.device();
    const t1 = await A.tab(), t2 = await A.tab();                 // same device, two tabs, then the account cannot be reached
    A.down = true;
    await startQuiz(t1, 'c01-s01'); await passQuiz(t1); await wait(t1, 1200);
    await home(t2); await t2.click('#foot [data-act="sound"]'); await wait(t2, 600);      // one tap that saves, in the other tab
    const local = await prof(t2);
    check('two tabs with no connection: a tap in one tab does not wipe the card passed in the other from the device', !!(local.passed && local.passed['c01-s01']), { passed: Object.keys(local.passed || {}) });
    await t1.close();
    A.down = false;
    await t2.reload(); await t2.waitForSelector('.mission'); await wait(t2, 2500);
    check('... and it reaches the account when the connection is back', !!(w.acct.doc && w.acct.doc.passed['c01-s01']), w.acct.doc && Object.keys(w.acct.doc.passed));
    check('no page errors (two tabs offline)', w.errs().length === 0, w.errs());
    await w.close();
  });

  await run('late-write', async () => {
    const w = await world(browser, url); const A = await w.device(); const a = await A.tab();
    A.lateNext = 26000;                                           // the next write gets no answer for 26 s, and then it lands
    await startQuiz(a, 'c01-s01'); const q1 = await answer(a, true);
    await wait(a, 17500);                                         // the page gave up on it after 15 s
    await next(a); const q2 = await answer(a, true);              // the student goes on
    await wait(a, 3000);
    check('a write that is still on its way is not overtaken by the next one', A.overlap === 0, { overlap: A.overlap, sets: w.acct.sets });
    await wait(a, 9000);                                          // the late write has landed; the page saves what came after it
    const d = w.acct.doc;
    check('... and once it lands, the account ends up with everything', !!(d && d.q[q1] && d.q[q2]) && A.overlap === 0, { q1: !!(d && d.q[q1]), q2: !!(d && d.q[q2]), overlap: A.overlap });
    await home(a);
    check('... and only then does the page say saved', /saved to your account/.test((await stats(a)).saved), (await stats(a)).saved);
    check('no page errors (late write)', w.errs().length === 0, w.errs());
    await w.close();
  });

  await run('wake-offline', async () => {
    const w = await world(browser, url); const A = await w.device(), B = await w.device();
    const a = await A.tab();
    const b = await B.tab(); await startQuiz(b, 'c01-s01'); await passQuiz(b); await wait(b, 2200);
    A.down = true;                                                // the page comes back into view while its connection is still down
    await a.evaluate(() => { window.__off += 60000; document.dispatchEvent(new Event('visibilitychange')); });
    await wait(a, 1500);
    A.down = false;                                               // the connection returns; nothing tells the page
    await a.waitForFunction(() => [...document.querySelectorAll('.secrow[data-sid="c01-s01"] .pill')].some(x => x.textContent.trim() === 'Passed'), null, { timeout: 35000 }).catch(() => {});
    check('a page that came back into view with no connection looks again by itself and catches up', (await rowPills(a, 'c01-s01')).includes('Passed'), await rowPills(a, 'c01-s01'));
    await w.close();
  });

  await run('overtaken', async () => {
    const w = await world(browser, url); const A = await w.device(), B = await w.device();
    const a = await A.tab(), b = await B.tab();
    A.slowGetNext = 13000;                                        // the laptop's next read of the account takes 13 s to come back
    await startQuiz(a, 'c01-s02'); const qa = await answer(a, true);            // its save starts: the read is sent, the reply is on its way
    await wait(a, 1200);
    await startQuiz(b, 'c01-s01'); await passQuiz(b); await wait(b, 2500);      // meanwhile the phone passes a card and saves it
    const mid = !!(w.acct.doc && w.acct.doc.passed && w.acct.doc.passed['c01-s01']);
    // the laptop's reply arrives and it writes what it joined: an account without the phone's card
    for (let k = 0; k < 40 && !(w.acct.doc && w.acct.doc.q && w.acct.doc.q[qa]); k++) await wait(a, 500);
    const after = !!(w.acct.doc.passed && w.acct.doc.passed['c01-s01']);
    check('(setup) the phone saved its card while the laptop\'s save was under way, and the laptop\'s write then landed on top of it', mid && !after, { mid, after });
    for (let k = 0; k < 90 && !(w.acct.doc.passed && w.acct.doc.passed['c01-s01']); k++) await wait(b, 500);      // the phone looks at the account again by itself
    const d = w.acct.doc;
    check('a save from another device landing on top does not cost the passed card: the phone puts it back by itself, with nobody touching it', !!(d.passed && d.passed['c01-s01'] && d.q[qa]), { passed: Object.keys(d.passed || {}), laptopAnswer: !!d.q[qa] });
    await home(a);
    await a.evaluate(() => { window.__off += 61000; });
    await a.waitForFunction(() => [...document.querySelectorAll('.secrow[data-sid="c01-s01"] .pill')].some(x => x.textContent.trim() === 'Passed'), null, { timeout: 40000 }).catch(() => {});
    check('... and the laptop shows the phone\'s card too', (await rowPills(a, 'c01-s01')).includes('Passed'), await rowPills(a, 'c01-s01'));
    check('no page errors (overtaken)', w.errs().length === 0, w.errs());
    await w.close();
  });

  await run('in-view', async () => {
    const w = await world(browser, url); const A = await w.device(), B = await w.device();
    const a = await A.tab();                                      // stays open and in view the whole time: no reload, no event
    const b = await B.tab(); await startQuiz(b, 'c01-s01'); await passQuiz(b); await wait(b, 2500);
    const reads = w.acct.gets;
    await a.evaluate(() => { window.__off += 61000; });           // a minute passes on that page's clock
    await a.waitForFunction(() => [...document.querySelectorAll('.secrow[data-sid="c01-s01"] .pill')].some(x => x.textContent.trim() === 'Passed'), null, { timeout: 40000 }).catch(() => {});
    check('a page that simply stays in view shows what another device saved within about a minute', (await rowPills(a, 'c01-s01')).includes('Passed') && w.acct.sets > 0, { pills: await rowPills(a, 'c01-s01'), readsByThatPage: w.acct.gets - reads });
    const sets = w.acct.sets;
    await a.evaluate(() => { window.__off += 61000; }); await wait(a, 32000);
    check('... and looking again with nothing new writes nothing', w.acct.sets === sets, { sets, now: w.acct.sets });
    await w.close();
  });

  await run('streak', async () => {
    const w = await world(browser, url); const A = await w.device(); const a = await A.tab();
    const day = async (iso) => { await setNow(a, iso); await a.reload(); await a.waitForSelector('.mission'); await wait(a, 600); return stats(a); };
    const one = async () => { await startQuiz(a, 'c01-s01'); await answer(a, true); await home(a); return stats(a); };
    let s = await day('2026-11-16T15:00:00');
    check('day 1 before any answer: streak 0, and the page says what starts it', s.streak === '0' && /Answer 1 question today to start it/.test(s.hint || ''), s);
    s = await one();
    check('day 1 after one answer: streak 1, today counted', s.streak === '1' && /Today is counted/.test(s.hint || '') && s.dots === 1, s);
    s = await day('2026-11-17T09:00:00');
    check('day 2 before any answer: the streak still shows 1 and asks for an answer to keep it', s.streak === '1' && /to keep it/.test(s.hint || ''), s);
    s = await one();
    check('day 2 after one answer: streak 2', s.streak === '2' && s.dots === 2, s);
    s = await day('2026-11-19T09:00:00');                         // the 18th was missed
    check('a missed day: the streak is back to 0', s.streak === '0' && /to start it/.test(s.hint || ''), s);
    s = await one();
    check('... and one answer starts a new streak at 1', s.streak === '1' && s.dots === 3, s);
    // late at night: an answer before midnight and one after, with no reload in between
    await setNow(a, '2026-11-19T23:59:40'); await startQuiz(a, 'c01-s01'); await answer(a, true); await next(a);
    await setNow(a, '2026-11-20T00:00:20'); await answer(a, true);
    const p = await prof(a); await home(a); s = await stats(a);
    check('an answer after midnight counts for the new day', !!(p.days['2026-11-19'] && p.days['2026-11-19'].a === 2 && p.days['2026-11-20'] && p.days['2026-11-20'].a === 1) && s.streak === '2', { d19: p.days['2026-11-19'], d20: p.days['2026-11-20'], streak: s.streak });
    // the streak travels: a second device sees it
    await wait(a, 1500);
    const B = await w.device(); const b = await B.tab(); await setNow(b, '2026-11-20T08:00:00'); await b.reload(); await b.waitForSelector('.mission'); await wait(b, 800);
    check('the streak is the same on a second device', (await stats(b)).streak === '2', await stats(b));
    check('no page errors (streak)', w.errs().length === 0, w.errs());
    await w.close();
  });

  await run('overnight', async () => {
    const w = await world(browser, url); const A = await w.device(); const a = await A.tab();
    await setNow(a, '2026-11-16T21:30:00'); await a.reload(); await a.waitForSelector('.mission');
    await startQuiz(a, 'c01-s01'); await answer(a, true); await next(a); await answer(a, true); await home(a); await wait(a, 1500);
    let s = await stats(a);
    check('evening: two answers, streak 1, today counted', s.streak === '1' && /Today is counted/.test(s.hint || '') && /^2 \/ 25/.test(s.today || ''), s);
    await setNow(a, '2026-11-17T08:00:00');                       // the page stayed open; next morning the student looks at it again
    await a.evaluate(() => { document.dispatchEvent(new Event('visibilitychange')); window.dispatchEvent(new Event('focus')); });
    await wait(a, 900); s = await stats(a);
    check('the same page the next morning no longer says today is counted', s.streak === '1' && /to keep it/.test(s.hint || '') && /^0 \/ 25/.test(s.today || ''), s);
    await setNow(a, '2026-11-18T08:00:00');                       // nobody touches it: the page notices the date by itself
    await wait(a, 32000); s = await stats(a);
    check('a day later, untouched, the streak has dropped to 0 by itself', s.streak === '0' && /to start it/.test(s.hint || ''), s);
    check('no page errors (overnight)', w.errs().length === 0, w.errs());
    await w.close();
  });

  await run('first-read-fails', async () => {
    const w = await world(browser, url); const A = await w.device(), B = await w.device();
    const b = await B.tab(); await startQuiz(b, 'c01-s01'); await passQuiz(b); await wait(b, 2200);      // the account holds a passed card
    A.down = true;
    const a = await A.tab();                                      // this device cannot read the account when the page opens
    await a.waitForFunction(() => /Could not reach your account/.test((document.querySelector('#sync-text') || {}).textContent || ''), null, { timeout: 30000 });
    const gets = w.acct.gets;
    check('the account cannot be read at the start: the page says so, and shows only this device', /Trying again/.test((await stats(a)).saved) && !(await rowPills(a, 'c01-s01')).includes('Passed'), (await stats(a)).saved);
    A.down = false;                                               // the outage ends. The student does nothing.
    await a.waitForFunction(() => /saved to your account/.test((document.querySelector('#sync-text') || {}).textContent || ''), null, { timeout: 40000 }).catch(() => {});
    const s = await stats(a);
    check('... and it does try again by itself: the saved progress appears without a tap', /saved to your account/.test(s.saved) && (await rowPills(a, 'c01-s01')).includes('Passed') && w.acct.gets > gets, { saved: s.saved, pills: await rowPills(a, 'c01-s01') });
    check('no page errors (first read fails)', w.errs().length === 0, w.errs());
    await w.close();
  });

  await run('storage-refused', async () => {
    const w = await world(browser, url); const A = await w.device({ noAccount: true, noStorage: true }); const a = await A.tab();
    await startQuiz(a, 'c01-s01'); await answer(a, true); await home(a);
    const s = await stats(a);
    check('a browser that refuses to store anything, and no account: the page does not say "saved on this device"', /not storing your progress/.test(s.saved) && !/saved on this device/i.test(s.saved), s.saved);
    const B = await w.device({ noAccount: true }); const b = await B.tab();
    await startQuiz(b, 'c01-s01'); await answer(b, true); await home(b);
    check('... and with storage working it says saved on this device', /Progress saved on this device/.test((await stats(b)).saved), (await stats(b)).saved);
    await w.close();
  });

  await run('summary', async () => {
    const w = await world(browser, url); const A = await w.device(); const a = await A.tab();
    await a.click('[data-act="start-session"]'); await a.waitForSelector('#reading');
    await a.click('.view > button[data-act="quiz"]'); await a.waitForSelector('.qcard');
    await answer(a, false);                                       // one miss, then the quiz is left before its end
    await a.click('[data-act="quit-quiz"]'); await a.waitForSelector('.mission');
    await a.click('[data-act="end-session"]'); await a.waitForSelector('.sumgrid');
    const txt = await a.evaluate(() => document.querySelector('.result').textContent);
    check('the session summary does not promise a rapid round the next session cannot give', !/rapid round/.test(txt) && /Weak on/.test(txt), txt.slice(-260));
    await w.close();
  });

  await run('listening', async () => {
    const w = await world(browser, url); const A = await w.device(); const a = await A.tab();
    await setNow(a, '2026-11-16T15:00:00'); await a.reload(); await a.waitForSelector('.mission');
    // tapping the last sentence and hearing only that is not "listened"
    await openCard(a, 'c01-s01'); await wait(a, 600);
    await a.evaluate(() => { const all = document.querySelectorAll('#reading .sent'); const el = all[all.length - 1]; el.scrollIntoView({ block: 'center' }); el.click(); });
    await a.waitForSelector('#dock-quiz.hi', { timeout: 30000 });      // the reading ran to its end
    let p = (await prof(a)) || {};                                     // nothing may have been saved yet
    check('hearing only the last sentence does not mark the card as listened', !(p.read && p.read['c01-s01']), p.read);
    // the whole card, played fast
    await a.click('#dock [data-act="play"]'); await wait(a, 700);
    await a.evaluate(() => { const el = window.__audios[0]; el.playbackRate = 12; });
    await a.waitForSelector('#dock-quiz.hi', { timeout: 60000 });
    const toast = await a.evaluate(() => document.querySelector('#toast').textContent);
    p = await prof(a);
    check('a card listened to the end is remembered', !!(p.read && p.read['c01-s01'] && p.read['c01-s01'].n === 1), p.read);
    check('... the page then points to the quiz', /Take the quiz/.test(toast), toast);
    check('... it is not a study day and earns nothing: no answers, no XP', !!(p.days['2026-11-16'] && p.days['2026-11-16'].a === 0 && p.days['2026-11-16'].r === 1 && p.xp === 0), { day: p.days['2026-11-16'], xp: p.xp });
    await home(a); const s = await stats(a), pills = await rowPills(a, 'c01-s01');
    check('the home page shows it: Listened, quiz next, streak 0, and says listening does not count', pills.includes('Listened') && pills.includes('Quiz next') && s.streak === '0' && /Listening does not count/.test(s.hint || ''), { pills, s });
    await wait(a, 1500);
    check('... and it is saved to the account', !!(w.acct.doc && w.acct.doc.read && w.acct.doc.read['c01-s01']), w.acct.doc && w.acct.doc.read);
    check('no page errors (listening)', w.errs().length === 0, w.errs());
    await w.close();
  });

  await run('listening-off-screen', async () => {
    // a locked phone or a tab in the background: the sound plays, but the browser runs no animation frames
    const w = await world(browser, url); const A = await w.device({ noFrames: true }); const a = await A.tab();
    await openCard(a, 'c01-s05'); await wait(a, 700);
    await a.evaluate(() => { window.__audios[0].playbackRate = 12; });
    await a.waitForSelector('#dock-quiz.hi', { timeout: 60000 });
    let p = (await prof(a)) || {};
    check('a card heard to the end while the page is not on screen is still marked as listened', !!(p.read && p.read['c01-s05']), p.read);
    await openCard(a, 'c01-s06'); await wait(a, 700);
    await a.evaluate(() => { const all = document.querySelectorAll('#reading .sent'); all[all.length - 1].click(); });
    await a.waitForSelector('#dock-quiz.hi', { timeout: 30000 });
    p = (await prof(a)) || {};
    check('... and hearing only the last sentence that way still does not mark a card', !(p.read && p.read['c01-s06']), p.read);
    check('no page errors (listening off screen)', w.errs().length === 0, w.errs());
    await w.close();
  });

  await run('clock-back', async () => {
    const w = await world(browser, url); const A = await w.device(); const a = await A.tab();
    await setNow(a, '2026-11-18T10:00:00'); await a.reload(); await a.waitForSelector('.mission');      // the device clock is two days ahead
    await startQuiz(a, 'c01-s01'); const qid = await answer(a, false); await home(a); await wait(a, 1500);
    await setNow(a, '2026-11-16T10:00:00'); await a.reload(); await a.waitForSelector('.mission'); await wait(a, 800);      // the clock is corrected
    for (let round = 0; round < 2; round++) {                     // the missed question, drilled right twice
      await home(a); await a.click('[data-act="drill"]'); await a.waitForSelector('.qcard');
      await answer(a, true); await next(a); await wait(a, 1800);
    }
    const p = await prof(a); await home(a); const s = await stats(a);
    check('after the device clock was moved back, a miss answered right twice still leaves the weak list', !!(p.q[qid] && p.q[qid].open === false && p.q[qid].run >= 2) && w.acct.doc.q[qid].open === false, { device: p.q[qid], account: w.acct.doc.q[qid] });
    check('... and the page shows no save time from the future', !/Nov 18/.test(s.saved) && /saved to your account/.test(s.saved), s.saved);
    await w.close();
  });

  await run('practice', async () => {
    const w = await world(browser, url); const A = await w.device(); const a = await A.tab();
    await startQuiz(a, 'practice'); await answer(a, true);
    const band = await a.evaluate(() => document.querySelector('.band').textContent);
    check('the practice card does not promise XP', /not counted/i.test(band) && !/\+\d+ XP/.test(band), band);
    await next(a); await passQuiz(a); await a.waitForSelector('.result');
    const note = await a.evaluate(() => (document.querySelector('#practice-note') || {}).textContent || '');
    const p = await prof(a);
    check('... its result says nothing on it counts', /Nothing on it counts/.test(note), note);
    check('... and nothing was recorded for it', (!p || (p.xp === 0 && Object.keys(p.days).length === 0 && Object.keys(p.q).length === 0)) && w.acct.sets === 0, { xp: p && p.xp, sets: w.acct.sets });
    await startQuiz(a, 'c01-s01'); await answer(a, true);
    const band2 = await a.evaluate(() => document.querySelector('.band').textContent), p2 = await prof(a);
    check('... and its right answers do not raise the pay or the best streak of the first real answer', /\+10 XP/.test(band2) && p2.xp === 10 && p2.bestCombo === 1, { band: band2, xp: p2.xp, bestCombo: p2.bestCombo });
    check('no page errors (practice)', w.errs().length === 0, w.errs());
    await w.close();
  });

  await browser.close(); srv.close();
  console.log(`\n${results.filter(Boolean).length} of ${results.length} checks passed`);
  process.exit(results.every(Boolean) ? 0 : 1);
})();
