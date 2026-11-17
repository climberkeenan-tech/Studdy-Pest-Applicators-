// Does the page really save when the store misbehaves, and how often does it ask?
// The storage block of app/template.html (from "profile + storage" to "derived stats") runs here unchanged, in
// node, against a clock the test moves and a stand-in store whose every call the test can make slow, silent,
// failing or cached. An hour of page time takes milliseconds, so the pauses between tries (20 s, 40 s ... 5 min),
// the hold after a write that got no answer and the looks of a page in view are checked to the second.
// The browser tests (tools/browser/progress.js) check the same code in a real page, in real time, for what fits
// into seconds.
// usage: node tools/check_sync.js [seed]        (SYNC_SRC=<file> tests another copy of the page)
const fs = require('fs'), path = require('path');
const FILE = process.env.SYNC_SRC || path.join(__dirname, '..', 'app', 'template.html');
const SRC = fs.readFileSync(FILE, 'utf8');
const cut = (from, to) => { const a = SRC.indexOf(from), b = SRC.indexOf(to, a + 1); if (a < 0 || b < 0) throw new Error('marker not found: ' + (a < 0 ? from : to)); return SRC.slice(a, b); };
const BLOCK = cut('/* ================= profile + storage ================= */', '/* ================= derived stats ================= */');
const SAYS = cut('/* When the account copy was last saved:', 'function renderFoot() {');
const SEED = +(process.argv[2] || 20261117);

let passed = 0, failed = 0;
const check = (name, ok, detail) => { if (ok) passed++; else failed++; if (!ok || process.env.VERBOSE) console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail !== undefined ? '  ' + JSON.stringify(detail).slice(0, 600) : '')); };
const rng = seed => { let s = seed >>> 0; return () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; };
const START = Date.UTC(2026, 10, 17, 15, 0, 0);

/* One account, any number of devices, one clock. Times are in seconds from the start. */
function world() {
  let now = 0, seq = 0;                                   // ms since START
  const timers = new Map();
  const add = (fn, ms, every) => { const id = ++seq; timers.set(id, { at: now + Math.max(0, ms || 0), fn, every: every ? ms : 0, n: seq }); return id; };
  const drain = async () => { for (let i = 0; i < 14; i++) await new Promise(r => setImmediate(r)); };
  async function run(untilSec) {
    const until = untilSec * 1000;
    for (;;) {
      await drain();
      let next = null;
      for (const [id, x] of timers) if (x.at <= until && (!next || x.at < next.x.at || (x.at === next.x.at && x.n < next.x.n))) next = { id, x };
      if (!next) break;
      now = Math.max(now, next.x.at);
      if (next.x.every) { next.x.at = now + next.x.every; next.x.n = ++seq; } else timers.delete(next.id);
      next.x.fn();
    }
    now = Math.max(now, until);
    await drain();
  }
  const acct = { doc: null, writes: [] };                 // writes: { t, by, keys } as they land
  const W = { acct, run, at: (sec, fn) => add(fn, sec * 1000 - now), sec: () => now / 1000, devices: [] };

  W.device = (name, opts) => {
    opts = opts || {};
    const dev = { name, off: 0, vis: 'visible', calls: [], flying: 0, overlaps: 0, renders: 0, chips: 0, foot: [], ls: opts.ls || {}, on: {}, cached: undefined,
      get: () => ({}), set: () => ({}) };                 // plans: get() -> { ms, fail, hang, cache, pending }   set() -> { land, answer, fail }   (ms; null = never)
    class FDate extends Date { constructor(...a) { if (a.length) super(...a); else super(START + now + dev.off); } static now() { return START + now + dev.off; } }
    const copy = x => (x === undefined || x === null ? x : JSON.parse(JSON.stringify(x)));
    const snap = (d, m) => ({ id: 'profile', exists: d !== null && d !== undefined, data: () => d, metadata: { fromCache: !!(m && m.cache), hasPendingWrites: !!(m && m.pending) } });
    const ref = {
      get() {
        const plan = dev.get() || {}, c = { t: now / 1000, k: 'get' }; dev.calls.push(c);
        return new Promise((ok, no) => {
          if (plan.hang) return;
          const ms = plan.ms === undefined ? 80 : plan.ms;
          let served;                                     // the store answers with what it held half way through the round trip
          add(() => { served = plan.cache ? copy(dev.cached === undefined ? null : dev.cached) : copy(acct.doc); }, plan.cache ? 0 : ms / 2);
          add(() => { if (plan.fail) return no({ code: plan.fail, message: 'stand-in' }); if (!plan.cache) dev.cached = copy(served); c.ok = true; ok(snap(served, plan)); }, ms);
        });
      },
      set(v) {
        const plan = dev.set() || {}, body = copy(v), c = { t: now / 1000, k: 'set' }; dev.calls.push(c);
        if (dev.flying) dev.overlaps++;
        dev.flying++;
        const land = plan.land === undefined ? 60 : plan.land, answer = plan.answer === undefined ? (land === null ? null : land + 40) : plan.answer;
        return new Promise((ok, no) => {
          if (plan.optimistic) dev.cached = copy(body);   // a client that shows its own write in later replies before the store has it
          if (plan.fail) { if (answer !== null) add(() => { dev.flying--; no({ code: plan.fail, message: 'stand-in' }); }, answer); return; }
          if (land !== null) add(() => { acct.doc = body; dev.cached = copy(body); acct.writes.push({ t: now / 1000, by: name, q: Object.keys(body.q || {}) }); }, land);
          if (answer !== null) add(() => { dev.flying--; c.ok = true; ok(); }, answer);
        });
      },
    };
    // any other document (the field log). opts.onePlace: a store that keeps one document whatever the path
    const other = { get: () => Promise.reject({ code: 'invalid_argument' }), set: v => { dev.logWrites = (dev.logWrites || 0) + 1; if (opts.onePlace) { acct.doc = copy(v); acct.writes.push({ t: now / 1000, by: name + ' (log)', q: [] }); } return Promise.resolve(); } };
    const claude = { use: n => Promise.resolve(n === 'db' ? { doc: p => (/\/profile$/.test(p) ? ref : other) } : n === 'user' ? { id: () => Promise.resolve('u_test') } : null) };
    const listen = (type, fn) => { (dev.on[type] = dev.on[type] || []).push(fn); };
    const document = { get visibilityState() { return dev.vis; }, addEventListener: listen, querySelector: () => null };
    const window = { claude, addEventListener: listen };
    const localStorage = { getItem: k => (k in dev.ls ? dev.ls[k] : null), setItem: (k, v) => { dev.ls[k] = String(v); }, removeItem: k => { delete dev.ls[k]; } };
    const S = { view: opts.view || 'home', sess: null };
    const body = `
      const $ = () => null;
      const dayKey = (d = new Date()) => d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
      function resumeSession() {}
      function render() { __dev.renders++; }
      function renderChips() { __dev.chips++; }
      function renderFoot() { const t = syncText(); if (t !== __dev.foot[__dev.foot.length - 1]) __dev.foot.push(t); }
      ${BLOCK}
      ${SAYS}
      return { initDb, save, flush, refresh, wake, syncText, P: () => P,
        st: () => ({ sync, dirty, saving, loaded, held: !!held, fails, pollWait }),
        answer: id => { const r = P.q[id] || (P.q[id] = { seen: 0, right: 0, wrong: 0, run: 0, open: false, last: 0 }); r.seen++; r.right++; r.run++; r.last = Math.max(Date.now(), r.last + 1);
          const d = P.days[dayKey()] || (P.days[dayKey()] = { a: 0, c: 0, xp: 0 }); d.a++; d.c++; d.xp += 10; P.xp += 10; save(); } };`;
    const api = new Function('window', 'document', 'localStorage', 'claude', 'setTimeout', 'clearTimeout', 'setInterval', 'Date', 'S', '__dev', body)(
      window, document, localStorage, claude, (f, ms) => add(f, ms), id => timers.delete(id), (f, ms) => add(f, ms, true), FDate, S, dev);
    Object.assign(dev, { api, S,
      fire: (type, ev) => { for (const f of dev.on[type] || []) f(ev || {}); },
      mouse: () => dev.fire('pointermove', { pointerType: 'mouse' }),
      hide: () => { dev.vis = 'hidden'; dev.fire('visibilitychange'); }, show: () => { dev.vis = 'visible'; dev.fire('visibilitychange'); },
      says: () => api.syncText(), has: id => !!api.P().q[id],
      times: (k, from, to) => dev.calls.filter(c => c.k === k && c.t >= (from || 0) && c.t < (to === undefined ? Infinity : to)).map(c => +c.t.toFixed(1)),
      lacks: () => Object.keys(api.P().q).filter(id => !(acct.doc && acct.doc.q && acct.doc.q[id])) });
    W.devices.push(dev);
    return dev;
  };
  return W;
}
const gaps = a => a.slice(1).map((x, i) => +(x - a[i]).toFixed(1));
const down = { fail: 'unavailable', ms: 30 };

(async () => {
  // ---- 1. A healthy store: one answer is one read and one write, then the page looks again 6 s and 35 s on
  {
    const w = world(), a = w.device('a');
    a.api.initDb(); await w.run(5);
    check('first visit, nothing to save: one read, no write', a.times('get').length === 1 && a.times('set').length === 0 && /Nothing to save yet/.test(a.says()), { calls: a.calls, says: a.says() });
    w.at(10, () => a.api.answer('q1')); await w.run(12);
    check('one answer: one more read, one write, "saved"', a.times('get', 10, 12).length === 1 && a.times('set').length === 1 && /saved to your account/.test(a.says()) && !a.lacks().length, { calls: a.calls, says: a.says() });
    await w.run(60);
    check('... and a look 6 s and 35 s after the write', JSON.stringify(a.times('get', 12, 60)) === JSON.stringify([16.8, 45.8]) || a.times('get', 12, 60).length === 2, a.times('get', 12, 60));
    await w.run(3660);
    const looks = a.times('get', 60, 3660);
    check('a page in view with nothing new looks less and less often, then every 2 minutes: about 30 reads an hour, no writes', looks.length >= 28 && looks.length <= 33 && a.times('set').length === 1 && Math.max(...gaps(looks)) <= 121, { n: looks.length, firstGaps: gaps(looks).slice(0, 5) });
    a.hide(); const n = a.times('get').length; await w.run(7300);
    check('a hidden page does not look at all', a.times('get').length === n, a.times('get').length - n);
  }

  // ---- 2. Two devices: news shows by itself, and brings the half-minute pace back
  {
    const w = world(), a = w.device('laptop'), b = w.device('phone');
    a.api.initDb(); b.api.initDb(); await w.run(600);                       // the laptop's pace is down to 2 minutes
    w.at(605, () => b.api.answer('p1')); await w.run(740);
    check('what the phone saved shows on a laptop that simply stays in view, within 2 minutes', a.has('p1'), { looks: a.times('get', 600, 740) });
    const t0 = a.times('get', 606, 740)[0];                // the look that brought the news
    await w.run(t0 + 215);
    check('... and the news brings the half-minute pace back (then 60 s, then 120 s)', JSON.stringify(gaps(a.times('get', t0 - 0.1, t0 + 215))) === JSON.stringify([30, 60, 120]), gaps(a.times('get', t0 - 0.1, t0 + 215)));
    check('... with no write by the laptop: it had nothing the account lacked', a.times('set').length === 0, a.times('set'));
  }

  // ---- 3. A short outage while the student answers: six failed saves are not a five-minute wait
  {
    const w = world(), a = w.device('a');
    a.api.initDb(); await w.run(60);
    let out = true; a.get = () => (out ? down : {});
    for (const t of [60, 68, 76, 84, 92, 100]) w.at(t, () => a.api.answer('q' + t));
    w.at(110, () => { out = false; });
    await w.run(109);
    check('six answers during an outage: the page says it could not reach the account, and the pause has not grown', /Could not reach your account/.test(a.says()) && a.api.st().fails === 1, { says: a.says(), st: a.api.st() });
    await w.run(135);
    check('... and all six are in the account within half a minute of the store coming back', !a.lacks().length && /saved to your account/.test(a.says()), { lacks: a.lacks(), gets: a.times('get', 100, 135), says: a.says() });
  }

  // ---- 4. A long outage: in view, one try a minute; hidden, the pause grows to 5 minutes
  {
    const w = world(), a = w.device('a');
    a.api.initDb(); await w.run(60);
    let out = true; a.get = () => (out ? down : {});
    w.at(60, () => a.api.answer('q1')); w.at(1260, () => { out = false; });
    await w.run(1259);
    const tries = a.times('get', 60.5, 1259);
    check('a page in view tries about once a minute while the account cannot be reached (20 minutes: 18 to 24 tries)', tries.length >= 18 && tries.length <= 24 && Math.max(...gaps(tries)) <= 61, { n: tries.length, gaps: gaps(tries).slice(0, 8) });
    await w.run(1325);
    check('... and saves within a minute of the store coming back, with no event to tell it', !a.lacks().length, { lacks: a.lacks(), gets: a.times('get', 1259, 1325) });

    const w2 = world(), h = w2.device('h');
    h.api.initDb(); await w2.run(60);
    let out2 = true; h.get = () => (out2 ? down : {});
    w2.at(60, () => h.api.answer('q1')); w2.at(62, () => h.hide()); await w2.run(3660);
    const ht = h.times('get', 63, 3660);
    check('a hidden page backs off: 20 s, 40 s, 80 s, 160 s, then every 5 minutes', JSON.stringify(gaps(h.times('get', 60.5, 3660)).slice(0, 6).map(Math.round)) === JSON.stringify([2, 20, 40, 80, 160, 300]) || (ht.length <= 16 && Math.max(...gaps(ht)) <= 301), { tries: ht.length, gaps: gaps(h.times('get', 60.5, 3660)).slice(0, 8) });
    out2 = false; w2.at(3700, () => h.show()); await w2.run(3705);
    check('... and saves at once when it comes back into view', !h.lacks().length, h.lacks());
  }

  // ---- 5. The account was never read (the first reads fail): in view, one try a minute, nothing written before a read
  {
    const w = world(), a = w.device('a');
    let out = true; a.get = () => (out ? down : {});
    w.acct.doc = { v: 1, updatedAt: START - 5000, xp: 50, q: { old: { seen: 1, right: 1, wrong: 0, run: 1, open: false, last: START - 5000 } }, passed: { c1: { at: START - 5000, tries: 1 } }, days: {}, attempts: {}, sessions: [] };
    a.api.initDb(); w.at(30, () => a.api.answer('q1')); w.at(600, () => { out = false; });
    await w.run(599);
    check('first read failing for 10 minutes: nothing is written, the page says so and keeps trying', a.times('set').length === 0 && /Could not reach your account/.test(a.says()) && a.times('get', 100, 599).length >= 7, { sets: a.times('set'), says: a.says(), tries: a.times('get').length });
    await w.run(665);
    check('... and within a minute of the store coming back the account copy is joined in and the answer saved on top of it', a.has('old') && !!(w.acct.doc.q.old && w.acct.doc.q.q1 && w.acct.doc.passed.c1), { has: a.has('old'), acct: Object.keys(w.acct.doc.q) });
  }

  // ---- 6. A write that never gets an answer: the hold, the growing pause, no pile of writes
  {
    const w = world(), a = w.device('a');
    a.api.initDb(); await w.run(5);
    a.set = () => ({ land: null, answer: null });
    w.at(10, () => a.api.answer('q1')); w.at(13, () => a.api.answer('q2')); w.at(28, () => a.api.answer('q3'));
    await w.run(20);
    check('3 s into a silent write the page is still "Saving"', /Saving to your account/.test(a.foot[a.foot.length - 1]) || /Saving/.test(a.says()), a.foot.slice(-2));
    await w.run(27);
    check('after 15 s it says it could not reach the account', /Could not reach your account/.test(a.says()), a.says());
    await w.run(44);
    check('an answer given during the hold does not send a second write on top of the first', a.times('set').length === 1, a.times('set'));
    await w.run(3610);
    const sets = a.times('set');
    check('the hold ends 20 s after the page gave up and the save asked for meanwhile goes out; from then on the pause grows: 35 s, 55 s, 95 s, 175 s, then 5 min 15 s', JSON.stringify(gaps(sets).slice(0, 7).map(Math.round)) === JSON.stringify([36, 35, 55, 95, 175, 315, 315]), gaps(sets).slice(0, 8));
    check('... 16 writes in an hour at most (it was 101), and the page never says saved', sets.length <= 16 && !a.foot.slice(2).some(t => /saved to your account/.test(t)), { sets: sets.length, foot: a.foot.slice(-3) });
    a.set = () => ({}); await w.run(3610 + 320);
    check('... and when the store answers writes again, everything is saved', !a.lacks().length && /saved to your account/.test(a.says()), { lacks: a.lacks(), says: a.says() });
  }

  // ---- 6b. A silent write, then reads fail too: the tries of a page in view come back
  {
    const w = world(), a = w.device('a');
    a.api.initDb(); await w.run(5);
    let out = false; a.set = () => (out || w.sec() < 20 ? { land: null, answer: null } : {}); a.get = () => (out ? down : {});
    w.at(10, () => a.api.answer('q1')); w.at(20, () => { out = true; }); w.at(640, () => { out = false; });
    await w.run(639);
    const tries = a.times('get', 60, 639).length;
    await w.run(705);
    check('a write without an answer, then an outage of ten minutes: the page in view goes back to one try a minute and saves within a minute of the end', tries >= 8 && !a.lacks().length, { triesDuringTheOutage: tries, lacks: a.lacks(), gets: a.times('get', 600, 705) });
  }

  // ---- 7. A write that is refused late, again and again: no storm
  {
    const w = world(), a = w.device('a');
    a.api.initDb(); await w.run(5);
    a.set = () => ({ fail: 'unavailable', answer: 16000 });
    w.at(10, () => a.api.answer('q1')); await w.run(3610);
    check('every write refused after 16 s: at most one try a minute (it was one every 17 s)', a.times('set').length <= 62 && Math.min(...gaps(a.times('set'))) >= 34, { sets: a.times('set').length, gaps: gaps(a.times('set')).slice(0, 6) });
  }

  // ---- 8. A late write that lands after its retry is put right, with or without an answer
  {
    const w = world(), a = w.device('a');
    a.api.initDb(); await w.run(5);
    let n = 0; a.set = () => (++n === 1 ? { land: 48000, answer: 48040 } : {});
    w.at(10, () => a.api.answer('q1')); w.at(28, () => a.api.answer('q2'));
    await w.run(50);
    check('an unanswered write: the retry goes out when the hold ends, about 36 s after the first', a.times('set').length === 2 && Math.round(a.times('set')[1] - a.times('set')[0]) === 36 && !a.lacks().length, { sets: a.times('set'), lacks: a.lacks() });
    await w.run(58.9);
    const mid = a.lacks();
    await w.run(62);
    check('... the old write then lands on top of it (the account goes back), is answered, and the page saves again at once', mid.length === 1 && !a.lacks().length && /saved to your account/.test(a.says()), { lackedMeanwhile: mid, lacksNow: a.lacks(), says: a.says() });

    const w2 = world(), b = w2.device('b');
    b.api.initDb(); await w2.run(5);
    let m = 0; b.set = () => (++m === 1 ? { land: 100000, answer: null } : {});
    w2.at(10, () => b.api.answer('q1')); w2.at(28, () => b.api.answer('q2')); w2.at(60, () => b.hide());
    await w2.run(112);
    const mid2 = b.lacks();
    await w2.run(260);
    check('the same without any answer, 100 s late, on a page that is hidden by then: the looks that follow an unanswered write put it right', mid2.length === 1 && !b.lacks().length, { lackedMeanwhile: mid2, lacksNow: b.lacks(), gets: b.times('get', 100, 260) });
  }

  // ---- 9. The answer to a stuck write arrives while the next save is reading
  {
    const w = world(), a = w.device('a');
    a.api.initDb(); await w.run(5);
    let n = 0;
    // write 1 (q1) lands at 71.5 s and is answered at 71.65 s; write 2 (q1, q2) lands 5 s after it is sent and is answered at 70.6 s
    a.set = () => { n++; const now = w.sec(); return n === 1 ? { land: (71.5 - now) * 1000, answer: (71.65 - now) * 1000 } : n === 2 ? { land: 5000, answer: (70.6 - now) * 1000 } : {}; };
    // the save that follows write 2's answer reads at 71.3 s: served at 71.49 s (before write 1 lands), back at 71.68 s (after write 1 was answered)
    a.get = () => (w.sec() > 71.2 && w.sec() < 71.4 ? { ms: 380 } : {});
    w.at(10, () => a.api.answer('q1')); w.at(27.9, () => a.api.answer('q2'));
    await w.run(71.6);
    const wentBack = a.lacks();
    await w.run(80);
    check('two writes unanswered at once, the older one lands and is answered while the next save is reading: the page saves again at once', wentBack.length === 1 && !a.lacks().length && /saved to your account/.test(a.says()), { accountWentBackTo: wentBack, lacksNow: a.lacks(), sets: a.times('set'), gets: a.times('get', 70, 80), says: a.says() });
  }

  // ---- 10. A reply that only repeats the page's own unanswered write proves nothing
  {
    const w = world(), a = w.device('a');
    a.api.initDb(); await w.run(5);
    a.set = () => ({ land: null, answer: null, optimistic: true });          // the write never reaches the store, but the client shows it in later replies
    a.get = () => ({ cache: true, pending: true, ms: 40 });
    w.at(10, () => a.api.answer('q1')); await w.run(700);
    check('the store holds nothing, the replies come from a cache that shows the write: the page never says saved', w.acct.doc === null && !a.foot.some(t => /saved to your account/.test(t)) && /Could not reach your account/.test(a.says()), { foot: a.foot.slice(-3), sets: a.times('set').length });
    a.set = () => ({}); a.get = () => ({}); await w.run(1100);
    check('... and it saves once the store really answers', !a.lacks().length && /saved to your account/.test(a.says()), { lacks: a.lacks(), says: a.says() });

    const w2 = world(), b = w2.device('b');
    b.api.initDb(); await w2.run(5);
    let k = 0; b.set = () => (++k === 1 ? { land: null, answer: null } : {});   // a plain store: the first write is lost, replies are honest
    w2.at(10, () => b.api.answer('q1')); await w2.run(60);
    check('a lost write on a plain store: the retry writes and the answer to it counts', !b.lacks().length && b.times('set').length === 2 && /saved to your account/.test(b.says()), { sets: b.times('set'), says: b.says() });
    const w4 = world(), d = w4.device('d');
    d.api.initDb(); await w4.run(5);
    let i = 0, cached = false;
    d.set = () => (++i === 1 ? { fail: 'unavailable', answer: 200, optimistic: true } : {});      // refused at once, but the client already shows it in its replies
    d.get = () => (cached ? { cache: true, pending: true, ms: 30 } : {});
    w4.at(10, () => d.api.answer('q1')); w4.at(11.5, () => { cached = true; }); w4.at(40, () => { cached = false; });
    await w4.run(39);
    check('a refused write that the client still shows in a reply it has not confirmed: the page writes again, it does not take that reply as proof', !d.lacks().length && d.times('set').length === 2 && /saved to your account/.test(d.says()), { lacks: d.lacks(), sets: d.times('set'), says: d.says() });

    const w3 = world(), c = w3.device('c');
    c.api.initDb(); await w3.run(5);
    let j = 0; c.set = () => (++j === 1 ? { land: 60, answer: null } : {});     // the first write landed, only its answer was lost
    w3.at(10, () => c.api.answer('q1')); await w3.run(60);
    check('a write that landed but whose answer was lost: one more write settles it (the reply alone is not taken as proof)', !c.lacks().length && c.times('set').length === 2 && /saved to your account/.test(c.says()), { sets: c.times('set'), says: c.says() });
  }

  // ---- 11. Looks that fail: no half-minute hammering, and a view that may not use the account stops asking
  {
    for (const [what, plan] of [['fail at once', down], ['never answer', { hang: true }], ['come from a cache', { cache: true, ms: 30 }], ['say slow down', { fail: 'resource_exhausted', ms: 30 }]]) {
      const w = world(), a = w.device('a');
      a.api.initDb(); await w.run(300);
      a.get = () => plan; await w.run(3900);
      const n = a.times('get', 300, 3900).length;
      check(`reads that ${what}, nothing to save: about 30 tries an hour, not 120`, n >= 20 && n <= 36 && /saved to your account|Nothing to save yet/.test(a.says()), { tries: n, gaps: gaps(a.times('get', 300, 3900)).slice(0, 6), says: a.says() });
      a.get = () => ({}); await w.run(4030);
      check(`... and the looks go on once reads work again (${what})`, a.times('get', 3900, 4030).filter((t, i, all) => a.calls.find(c => c.k === 'get' && +c.t.toFixed(1) === t && c.ok)).length >= 1, a.times('get', 3900, 4030));
    }
    const w = world(), a = w.device('a');
    a.api.initDb(); await w.run(300);
    a.get = () => ({ fail: 'revoked', ms: 30 }); await w.run(3900);
    check('a look refused for good (revoked): one try, then the page stops asking and says so', a.times('get', 300, 3900).length === 1 && /not available here/.test(a.says()), { tries: a.times('get', 300, 3900).length, says: a.says() });
  }

  // ---- 12. The device clock is set back three hours
  {
    const w = world(), a = w.device('laptop'), b = w.device('phone');
    a.off = 3 * 3600000; a.api.initDb(); b.api.initDb(); await w.run(300);
    w.at(300, () => { a.off = 0; }); w.at(360, () => b.api.answer('p1'));
    await w.run(520);
    check('a clock that jumps back does not stop the looks: the phone\'s answer shows within 2.5 minutes', a.has('p1'), a.times('get', 300, 520));
    w.at(530, () => a.api.answer('q1')); await w.run(540);
    check('... and the laptop still saves', !a.lacks().length && /saved to your account/.test(a.says()), { lacks: a.lacks(), says: a.says() });
  }

  // ---- 13. The mouse comes back
  {
    const w = world(), a = w.device('laptop'), b = w.device('phone');
    a.api.initDb(); b.api.initDb(); await w.run(600);
    w.at(605, () => b.api.answer('p1')); w.at(612, () => a.mouse());
    await w.run(613);
    check('a mouse that moves after a minute without one: the page looks at once', a.has('p1'), a.times('get', 600, 613));
    for (let t = 613; t < 730; t += 0.5) w.at(t, () => a.mouse());
    await w.run(730);
    check('... a mouse that keeps moving does not make it look again and again: two looks in the next two minutes, as without a mouse', a.times('get', 613, 730).length === 2, a.times('get', 613, 730));

    const w2 = world(), c = w2.device('laptop');
    c.api.initDb(); await w2.run(60);
    let out = true; c.get = () => (out ? down : {});
    w2.at(60, () => c.api.answer('q1')); w2.at(62, () => c.hide()); w2.at(400, () => { out = false; c.vis = 'visible'; });   // back in view without an event (the window never lost focus)
    w2.at(405, () => c.mouse());
    await w2.run(407);
    check('a returning mouse also sends what could not be saved', !c.lacks().length && /saved to your account/.test(c.says()), { lacks: c.lacks(), says: c.says() });
  }

  // ---- 14. News is taken in at once, but the home page is not redrawn under a hand that is about to click
  {
    const w = world(), a = w.device('laptop', { view: 'home' }), b = w.device('phone');
    a.api.initDb(); b.api.initDb(); await w.run(600);
    w.at(605, () => b.api.answer('p1'));
    for (let t = 612; t < 615; t += 0.1) w.at(t, () => a.mouse());              // the hand travels for 3 s
    await w.run(612.6);
    const r0 = a.renders;
    await w.run(614.9);
    check('news arrives while the mouse is moving: the numbers are in (a click acts on them), the home page is not redrawn yet', a.has('p1') && a.renders === r0, { has: a.has('p1'), redraws: a.renders - r0 });
    await w.run(616);
    check('... and it is redrawn half a second after the mouse has come to rest', a.renders === r0 + 1, a.renders - r0);
    w.at(700, () => b.api.answer('p2'));
    for (let t = 720; t < 740; t += 0.1) w.at(t, () => a.mouse());              // a mouse that never rests
    w.at(721, () => a.api.refresh());
    await w.run(721.5); const r1 = a.renders; await w.run(727.5);
    check('... at the latest after 5 seconds, however long the mouse goes on', a.has('p2') && a.renders === r1 + 1, { has: a.has('p2'), redraws: a.renders - r1 });
    w.at(800, () => { a.fire('pointerdown'); }); w.at(800.2, () => b.api.answer('p3')); w.at(803, () => a.api.refresh()); w.at(803.8, () => a.fire('pointerup'));
    await w.run(803.7); const r2 = a.renders; const got = a.has('p3');
    await w.run(805);
    check('a finger or button that is down: no redraw until it is up again', got && r2 === r1 + 1 && a.renders === r2 + 1, { got, before: r2 - r1 - 1, after: a.renders - r2 });
  }

  // ---- 15. The field log never goes into the progress document, and a store with one reference for everything gets none
  {
    const w = world(), a = w.device('a');
    a.api.initDb(); await w.run(5); w.at(10, () => a.api.answer('q1')); await w.run(200);
    check('the field log is written to its own document half a minute after the page opened, and the progress document holds no trace of it', a.logWrites === 1 && !('n' in w.acct.doc) && !('ua' in w.acct.doc), { logWrites: a.logWrites, keys: Object.keys(w.acct.doc) });
    await w.run(3800); a.hide(); await w.run(3810); a.show(); await w.run(3900);
    check('... an idle page that only looks at the account now and then does not write it again, in view or on leaving', a.logWrites === 1 && a.times('get', 200, 3800).length > 20, { logWrites: a.logWrites, looks: a.times('get', 200, 3800).length });
    w.at(3910, () => a.api.answer('q2')); await w.run(4300);
    const afterAnswer = a.logWrites;
    w.at(4310, () => a.api.answer('q3')); w.at(4320, () => a.hide()); await w.run(4330);
    check('... after an answer it is written again, once in five minutes at most while in view, and at once when the page is left', afterAnswer === 2 && a.logWrites === 3, { afterAnswer, onLeaving: a.logWrites });
    const log = JSON.parse(a.ls['pas-fieldlog-v1'] || '{}');
    check('... it counts calls and timings, and holds no answers', !!log.n && log.n.get >= 2 && log.n.set === 3 && log.n.set_ok === 3 && !/q1|q2|q3/.test(JSON.stringify(log)), log);
  }

  // ---- 15b. A store that keeps one document for every path: the log would land in the progress
  {
    const w = world(), a = w.device('a', { onePlace: true });
    a.api.initDb(); await w.run(5); w.at(10, () => a.api.answer('q1')); await w.run(29);
    const before = !!(w.acct.doc && w.acct.doc.q && w.acct.doc.q.q1);
    await w.run(31);
    const clobbered = !(w.acct.doc && w.acct.doc.q);            // the first log write has replaced the progress
    await w.run(400); a.hide(); await w.run(410); a.show(); w.at(420, () => a.api.answer('q2')); await w.run(800);
    const d = w.acct.doc || {};
    check('a store with one document for every path: the page sees its log in the progress document, puts the progress back and never logs again', before && clobbered && a.logWrites === 1 && !!(d.q && d.q.q1 && d.q.q2) && !('ua' in d) && !('n' in d) && !('dev' in d) && !('ua' in a.api.P()), { before, clobbered, logWrites: a.logWrites, keys: Object.keys(d) });
    const b = w.device('b', { onePlace: true, ls: a.ls });    // the same browser later: a new page load, with what the first one stored
    b.api.initDb(); await w.run(900); w.at(905, () => b.api.answer('q3')); await w.run(1300);
    check('... also not after the page is opened again on that device', (b.logWrites || 0) === 0 && !!(w.acct.doc.q && w.acct.doc.q.q3), { logWrites: b.logWrites || 0, keys: Object.keys(w.acct.doc) });
  }

  // ---- 15c. The log, too, waits for the first read of the account, and for a write that is on its way
  {
    const w = world(), a = w.device('a', { onePlace: true });
    w.acct.doc = { v: 1, updatedAt: START - 5000, xp: 50, q: { old: { seen: 1, right: 1, wrong: 0, run: 1, open: false, last: START - 5000 } }, passed: { c1: { at: START - 5000, tries: 1 } }, days: {}, attempts: {}, sessions: [] };
    let out = true; a.get = () => (out ? down : {});
    a.api.initDb(); w.at(200, () => { out = false; });
    await w.run(199);
    check('while the account has never been read, nothing at all is written, the log included', (a.logWrites || 0) === 0 && !!(w.acct.doc.passed && w.acct.doc.passed.c1), { logWrites: a.logWrites || 0, keys: Object.keys(w.acct.doc) });
    await w.run(900);
    check('... so even a store with one document for every path cannot lose what the account held: the page has it, and puts it back', a.has('old') && !!(w.acct.doc.q && w.acct.doc.q.old && w.acct.doc.passed && w.acct.doc.passed.c1) && a.logWrites === 1, { has: a.has('old'), logWrites: a.logWrites, keys: Object.keys(w.acct.doc) });

    const w2 = world(), b = w2.device('b');
    b.api.initDb(); await w2.run(5);
    let n = 0; b.set = () => (++n === 1 ? { land: 29000, answer: 29000 } : {});      // a write that takes 29 s
    w2.at(10, () => b.api.answer('q1')); await w2.run(38);
    check('no log is written while a write of the progress has not been answered', (b.logWrites || 0) === 0, { logWrites: b.logWrites || 0, sets: b.times('set') });
    await w2.run(75);
    check('... it follows once that write is settled', b.logWrites === 1 && !b.lacks().length, { logWrites: b.logWrites, lacks: b.lacks() });
  }

  // ---- 16. Random histories: whatever the store does for five minutes, the page settles once it is healthy
  {
    const N = +(process.env.HISTORIES || 300);
    let unsettled = 0, stuck = 0, worst = 0, worstSeed = 0, hiddenLack = 0, maxFly = 0;
    for (let i = 0; i < N; i++) {
      const r = rng(SEED + i * 7919), w = world(), a = w.device('a');
      a.api.initDb(); await w.run(1);
      let chaos = true;
      a.get = () => { if (!chaos) return {}; const x = r(); return x < 0.07 ? { hang: true } : x < 0.15 ? { fail: 'unavailable', ms: 20 + r() * 200 } : x < 0.2 ? { cache: true, ms: 30 } : { ms: 30 + (r() < 0.3 ? r() * 4000 : r() * 300) }; };
      a.set = () => { if (!chaos) return {}; const x = r(); if (x < 0.45) { const l = 30 + r() * 300; return { land: l, answer: l + 20 + r() * 200 }; } if (x < 0.55) return { land: null, answer: null }; if (x < 0.68) return { land: 50 + r() * 90000, answer: null };
        if (x < 0.9) { const l = 15000 + r() * 80000; return { land: l, answer: l + r() * 3000 }; } return { fail: 'unavailable', answer: 100 + r() * 40000 }; };
      let t = 1 + r() * 3, n = 0;
      while (t < 300) { const id = 'q' + (++n), at = t; w.at(at, () => a.api.answer(id)); t += r() < 0.5 ? 1 + r() * 6 : 5 + r() * 40; }
      for (let k = 0; k < 3; k++) { const s = 1 + r() * 299, d = 1 + r() * 30; w.at(s, () => a.hide()); w.at(s + d, () => a.show()); }
      const hiddenEnd = i % 3 === 0;                       // every third history ends with the page hidden for good
      w.at(301, () => { chaos = false; if (hiddenEnd) a.hide(); });
      let lied = 0, liedMax = 0;
      for (let s = 2; s <= 1000; s += 0.25) w.at(s, () => { const lie = /saved to your account/.test(a.says()) && a.lacks().length > 0; lied = lie ? lied + 0.25 : 0; liedMax = Math.max(liedMax, lied); });
      await w.run(1000);
      const st = a.api.st();
      if (a.lacks().length) { if (hiddenEnd) hiddenLack++; else unsettled++; }
      if (st.dirty && !hiddenEnd) stuck++;
      if (!hiddenEnd && liedMax > worst) { worst = liedMax; worstSeed = i; }
      maxFly = Math.max(maxFly, a.overlaps);
    }
    check(`${N} random histories (seed ${SEED}): 11 minutes after the store turned healthy, a page in view has everything in the account`, unsettled === 0 && stuck === 0, { unsettled, stuck });
    check('... and so has a page that was hidden when the store turned healthy', hiddenLack === 0, { hiddenLack });
    check('... the longest time a page in view said "saved" while the account lacked an answer stays under 2.5 minutes (an old write landing late, without a word)', worst <= 150, { worstSeconds: worst, history: worstSeed });
  }

  console.log(`${passed}/${passed + failed} sync checks pass (${path.relative(process.cwd(), FILE) || FILE}, seed ${SEED}).`);
  process.exit(failed ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
