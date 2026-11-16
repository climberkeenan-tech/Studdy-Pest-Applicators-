#!/usr/bin/env node
// Tests for joinProfiles() in app/template.html: the rule that keeps two copies of the saved progress
// (two devices, a tab left open, a device that was offline) from wiping each other out.
// Usage: node tools/check_join.js [seed]
// It runs the function exactly as it is written in the page against random study histories on several
// devices, and checks the promises the page makes:
//   - joining loses nothing (passed cards, answers, study days, XP, listened cards, sessions)
//   - a copy joined with an older version of itself comes back unchanged
//   - the order of joining does not matter, and devices that keep syncing end up identical
//   - a miss is never forgiven by a join
const fs = require('fs'), path = require('path');
const ROOT = process.env.JOIN_ROOT || path.join(__dirname, '..');      // JOIN_SRC: another copy of the page to test (a patched trial)
const src = fs.readFileSync(process.env.JOIN_SRC || path.join(ROOT, 'app/template.html'), 'utf8');
const i = src.indexOf('function blank()'), j = src.indexOf('let P = normalize(lsGet(LS_KEY));', i);
if (i < 0 || j < 0) { console.error('joinProfiles not found in app/template.html'); process.exit(2); }
const { blank, normalize, joinProfiles, sig, sigP } = new Function(src.slice(i, j) + '\nreturn { blank, normalize, joinProfiles, sig, sigP };')();
const clone = x => JSON.parse(JSON.stringify(x));

let seed = +(process.argv[2] || 20261116);
const rnd = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };
const pick = a => a[Math.floor(rnd() * a.length)];
let failures = 0, checks = 0;
const ok = (cond, name, detail) => { checks++; if (!cond) { failures++; if (failures <= 25) console.log('FAIL ' + name + (detail ? '\n     ' + JSON.stringify(detail).slice(0, 700) : '')); } };

// ---- a small model of how the page changes the profile (record(), finishQuiz(), sessions, markRead(), settings)
const CARDS = Array.from({ length: 12 }, (_, k) => 'c01-s' + String(k + 1).padStart(2, '0'));
const ALLQ = CARDS.flatMap(c => [1, 2, 3, 4].map(n => c + '-t' + n));
let QIDS = ALLQ;                                            // some runs use only a few questions, so two devices answer the same ones
const dayOf = t => 'd' + Math.floor(t / 1000);              // 1000 ticks to a "day"
function device(p) { return { P: normalize(clone(p)), combo: 0, sess: null, log: [] }; }
function touch(d, t) { d.P.updatedAt = Math.max(d.P.updatedAt || 0, t); }
function today(d, t) { return d.P.days[dayOf(t)] || (d.P.days[dayOf(t)] = { a: 0, c: 0, xp: 0 }); }
function sessOf(d) { return d.sess && d.P.sessions.find(x => x.id === d.sess && !x.end); }
function answer(d, qid, right, t) {
  const st = d.P.q[qid] || (d.P.q[qid] = { seen: 0, right: 0, wrong: 0, run: 0, open: false, last: 0 });
  let gain = 0;
  if (right) { d.combo++; gain = 10 + Math.min(d.combo - 1, 5) * 2; } else d.combo = 0;
  st.seen++; st.last = t;
  d.log.push([t, qid, right]);
  const s = sessOf(d);
  if (right) { st.right++; st.run++; if (st.open && st.run >= 2) { st.open = false; gain += 25; if (s && !s.cleared.includes(qid)) s.cleared.push(qid); } }
  else { st.wrong++; st.run = 0; st.open = true; st.miss = t; if (s && !s.missed.includes(qid)) s.missed.push(qid); }
  const day = today(d, t); day.a++; if (right) day.c++; day.xp += gain;
  d.P.xp += gain; d.P.bestCombo = Math.max(d.P.bestCombo, d.combo);
  if (s) { s.a++; if (right) s.c++; s.xp += gain; s.best = Math.max(s.best, d.combo); s.touch = t; }
  touch(d, t);
}
function finish(d, sid, score, t) {
  const at = d.P.attempts[sid] || (d.P.attempts[sid] = { n: 0, best: 0, last: 0 });
  at.n++; at.best = Math.max(at.best, score); at.last = score;
  const s = sessOf(d);
  if (score === 100) {
    if (!d.P.passed[sid]) { d.P.passed[sid] = { at: t, tries: at.n }; d.P.xp += 50; today(d, t).xp += 50; if (s) s.xp += 50; }
    if (s && !s.passed.includes(sid)) s.passed.push(sid);
  } else if (s && !s.failed.includes(sid)) s.failed.push(sid);
  touch(d, t);
}
function startSession(d, t) {
  const s = { id: 's' + t + '-' + Math.floor(rnd() * 1e6), start: t, touch: t, end: null, a: 0, c: 0, xp: 0, best: 0, passed: [], cleared: [], failed: [], missed: [], studied: [], rapid: null };
  d.P.sessions.unshift(s); d.P.sessions = d.P.sessions.slice(0, 30); d.sess = s.id; touch(d, t);
}
function endSession(d, t) { const s = sessOf(d); if (s) { s.end = t; touch(d, t); } d.sess = null; }
function listen(d, sid, t) {
  const r = d.P.read[sid] || (d.P.read[sid] = { n: 0, at: 0 }); r.n++; r.at = t;
  const day = today(d, t); day.r = (day.r || 0) + 1;
  const s = sessOf(d); if (s && !s.studied.includes(sid)) { s.studied.push(sid); s.touch = t; }
  touch(d, t);
}
// a reload: the page closes a session this copy last saw in use more than 3 "hours" ago (resumeSession)
function reload(d, t) { for (const x of d.P.sessions) if (!x.end && t - (x.touch || x.start) > 125) x.end = x.touch || x.start; d.sess = (d.P.sessions.find(x => !x.end) || {}).id || null; }
// the weak list as it truly is: every answer of every device, in the order given, by the page's own rule
function truth(logs) {
  const st = {};
  for (const [t, qid, right] of logs.flat().sort((a, b) => a[0] - b[0])) {
    const r = st[qid] || (st[qid] = { run: 0, open: false, n: 0 });
    r.n++;
    if (right) { r.run++; if (r.open && r.run >= 2) r.open = false; } else { r.run = 0; r.open = true; }
  }
  return st;
}
function setting(d, t) { d.P.settings.rate = pick([0.8, 1, 1.15, 1.3]); d.P.settings.chain = rnd() < 0.5; d.P.settingsAt = t; touch(d, t); }
function step(d, t) {
  const r = rnd();
  if (r < 0.62) answer(d, pick(QIDS), rnd() < 0.7, t);
  else if (r < 0.74) finish(d, pick(CARDS), rnd() < 0.5 ? 100 : pick([40, 60, 80]), t);
  else if (r < 0.80) { if (sessOf(d)) endSession(d, t); else startSession(d, t); }
  else if (r < 0.88) listen(d, pick(CARDS), t);
  else if (r < 0.93) reload(d, t);
  else setting(d, t);
}
function streak(P, t) {
  let n = 0, k = Math.floor(t / 1000);
  if (!(P.days['d' + k] && P.days['d' + k].a)) k--;
  while (P.days['d' + k] && P.days['d' + k].a) { n++; k--; }
  return n;
}
const same = (x, y) => sig(normalize(clone(x))) === sig(normalize(clone(y)));
// where two values first differ, for a failure message
function firstDiff(x, y, at = '') {
  if (sig(x) === sig(y)) return null;
  if (x && y && typeof x === 'object' && typeof y === 'object' && Array.isArray(x) === Array.isArray(y)) {
    for (const k of new Set([...Object.keys(x), ...Object.keys(y)])) { const d = firstDiff(x[k], y[k], at + '/' + k); if (d) return d; }
  }
  return { at, first: x, second: y };
}

// ---- what "nothing is lost" means
function holdsAll(m, x, name) {
  for (const k of Object.keys(x.passed)) ok(!!m.passed[k], name + ': a passed card is kept', k);
  for (const k of Object.keys(x.q)) {
    const a = x.q[k], b = m.q[k] || {};
    ok(b.seen >= a.seen && b.right >= a.right && b.wrong >= a.wrong, name + ': answer counts never shrink', { k, a, b });
    ok(b.seen >= b.right + b.wrong, name + ': seen covers right + wrong', { k, b });
  }
  for (const k of Object.keys(x.days)) { const a = x.days[k], b = m.days[k] || {}; ok(b.a >= a.a && b.c >= a.c && b.xp >= a.xp && (b.r || 0) >= (a.r || 0), name + ': a study day is kept', { k, a, b }); }
  for (const k of Object.keys(x.read)) ok(m.read[k] && m.read[k].n >= x.read[k].n && m.read[k].at >= x.read[k].at, name + ': a listened card is kept', k);
  for (const k of Object.keys(x.attempts)) ok(m.attempts[k] && m.attempts[k].n >= x.attempts[k].n && m.attempts[k].best >= x.attempts[k].best, name + ': quiz attempts are kept', k);
  ok(m.xp >= x.xp && m.bestCombo >= x.bestCombo && m.updatedAt >= x.updatedAt, name + ': XP, best streak and the time stamp never shrink');
}

// ================= 1. fixed cases
{
  const q = (o) => Object.assign({ seen: 0, right: 0, wrong: 0, run: 0, open: false, last: 0 }, o);
  const P = (o) => normalize(Object.assign(blank(), o));
  // a miss on one copy, a clearing answer on the other, in either time order: still on the weak list
  const base = { seen: 3, right: 1, wrong: 2, run: 1, open: true, last: 100 };
  const cleared = q({ seen: 4, right: 2, wrong: 2, run: 2, open: false, last: 210 });
  const missed = q({ seen: 4, right: 1, wrong: 3, run: 0, open: true, last: 205 });
  let m = joinProfiles(P({ q: { x: cleared }, updatedAt: 210 }), P({ q: { x: missed }, updatedAt: 205 })).q.x;
  ok(m.open === true && m.run <= 1 && m.seen >= 4 && m.wrong === 3 && m.right === 2, 'a miss on the other copy is not forgiven (cleared later)', m);
  const missedLater = q({ seen: 4, right: 1, wrong: 3, run: 0, open: true, last: 300 });
  m = joinProfiles(P({ q: { x: cleared }, updatedAt: 210 }), P({ q: { x: missedLater }, updatedAt: 300 })).q.x;
  ok(m.open === true && m.run === 0, 'a miss on the other copy is not forgiven (missed later)', m);
  // the review's first case: both devices miss it while one cannot save. Monday phone: wrong, right, right (cleared).
  // Tuesday laptop: wrong. Wednesday phone: right once. Only one right answer came after the last miss.
  const phone = q({ seen: 4, right: 3, wrong: 1, run: 3, open: false, last: 300, miss: 100 });
  const laptop = q({ seen: 1, right: 0, wrong: 1, run: 0, open: true, last: 200, miss: 200 });
  for (const [a, b] of [[phone, laptop], [laptop, phone]]) {
    m = joinProfiles(P({ q: { x: a }, updatedAt: a.last }), P({ q: { x: b }, updatedAt: b.last })).q.x;
    ok(m.open === true && m.run <= 1 && m.miss === 200, 'a miss made while a device could not save is not forgiven by the other device\'s later right answer', m);
  }
  // the review's second case: cleared on the phone; a laptop page left open still lists it and answers right once
  const cleared2 = q({ seen: 3, right: 2, wrong: 1, run: 2, open: false, last: 210, miss: 100 });
  const stale = q({ seen: 2, right: 1, wrong: 1, run: 1, open: true, last: 300, miss: 100 });
  for (const [a, b] of [[cleared2, stale], [stale, cleared2]]) {
    m = joinProfiles(P({ q: { x: a }, updatedAt: a.last }), P({ q: { x: b }, updatedAt: b.last })).q.x;
    ok(m.open === false && m.run >= 2, 'a question cleared after the newest miss stays cleared when a page left open answers it again', m);
  }
  // lists that hold the same items in another order, or one of them twice: both orders of joining agree
  {
    const sA = { id: 's5', start: 10, touch: 20, end: null, a: 2, c: 1, xp: 20, best: 1, passed: [], cleared: ['q1'], failed: [], missed: ['q1', 'q2'], studied: [], rapid: null };
    const sB = Object.assign(clone(sA), { cleared: ['q1', 'q1'], missed: ['q2', 'q1'] });
    const ab = joinProfiles(P({ sessions: [sA], updatedAt: 20 }), P({ sessions: [sB], updatedAt: 20 })), ba = joinProfiles(P({ sessions: [sB], updatedAt: 20 }), P({ sessions: [sA], updatedAt: 20 }));
    ok(sig(ab) === sig(ba), 'session lists with the same items in another order join to one result', [ab.sessions[0].cleared, ba.sessions[0].cleared, ab.sessions[0].missed, ba.sessions[0].missed]);
  }
  // a session closed by a stale page's 3-hour rule (end = its old touch) stays open if another copy used it later
  {
    const live = { id: 's6', start: 10, touch: 900, end: null, a: 7, c: 5, xp: 70, best: 3, passed: [], cleared: [], failed: [], missed: [], studied: [], rapid: null };
    const closedByStalePage = Object.assign(clone(live), { touch: 300, end: 300, a: 3, c: 2, xp: 30 });
    m = joinProfiles(P({ sessions: [live], updatedAt: 900 }), P({ sessions: [closedByStalePage], updatedAt: 950 })).sessions[0];
    ok(m.end === null && m.a === 7 && m.touch === 900, 'a session a stale page closed is still open when another copy used it after that', m);
    const reallyEnded = Object.assign(clone(live), { end: 905 });
    m = joinProfiles(P({ sessions: [live], updatedAt: 900 }), P({ sessions: [reallyEnded], updatedAt: 905 })).sessions[0];
    ok(m.end === 905, 'a session the student ended stays ended', m);
  }
  // an older version of the same record does not un-clear a question
  m = joinProfiles(P({ q: { x: q(base) }, updatedAt: 100 }), P({ q: { x: cleared }, updatedAt: 210 })).q.x;
  ok(m.open === false && m.run === 2 && m.seen === 4, 'an older copy does not put a cleared question back', m);
  // passed anywhere stays passed, and the first pass stands
  m = joinProfiles(P({ passed: { a: { at: 500, tries: 3 } }, updatedAt: 500 }), P({ passed: { a: { at: 300, tries: 1 }, b: { at: 310, tries: 2 } }, updatedAt: 310 }));
  ok(m.passed.a.at === 300 && m.passed.a.tries === 1 && m.passed.b.at === 310, 'the first pass of a card stands, and both copies\' passes are kept', m.passed);
  // an empty device never wipes the account, whatever its time stamp
  const full = P({ xp: 4000, passed: { a: { at: 1, tries: 1 } }, days: { d1: { a: 30, c: 25, xp: 4000 } }, q: { x: cleared }, updatedAt: 1000 });
  m = joinProfiles(P({ updatedAt: 999999 }), full);
  ok(m.xp === 4000 && m.passed.a && m.days.d1.a === 30 && m.q.x.seen === 4, 'an empty copy with a newer time stamp wipes nothing', { xp: m.xp });
  // settings follow the copy whose settings were changed last, not the copy that was saved last
  m = joinProfiles(P({ settings: { rate: 1.3 }, settingsAt: 50, updatedAt: 60 }), P({ settings: { rate: 0.8 }, settingsAt: 40, updatedAt: 900 }));
  ok(m.settings.rate === 1.3 && m.settingsAt === 50, 'settings come from the copy that changed them last', m.settings);
  // settings saved before settingsAt existed: what somebody chose beats a fresh device's untouched defaults, in either order
  {
    const chosen = P({ settings: { autoplay: false, sound: false }, updatedAt: 700 }), fresh = P({ updatedAt: 900 });
    const one = joinProfiles(chosen, fresh), two = joinProfiles(fresh, chosen);
    ok(one.settings.autoplay === false && one.settings.sound === false && sig(one) === sig(two), 'settings chosen before this change are not replaced by a fresh device\'s defaults', [one.settings, two.settings]);
  }
  // sessions: ended on either copy is ended, lists are joined, the newest 30 are kept
  const s1 = { id: 's1', start: 10, touch: 20, end: null, a: 2, c: 1, xp: 20, best: 1, passed: [], cleared: [], failed: [], missed: ['q1'], studied: ['a'], rapid: null };
  const s2 = Object.assign(clone(s1), { touch: 30, end: 40, a: 3, c: 2, xp: 32, missed: ['q1', 'q2'], studied: ['a', 'b'] });
  m = joinProfiles(P({ sessions: [s1], updatedAt: 20 }), P({ sessions: [s2], updatedAt: 40 })).sessions[0];
  ok(m.end === 40 && m.a === 3 && m.missed.length === 2 && m.studied.join() === 'a,b', 'a session ended on one copy is ended, and its lists are joined', m);
  const many = Array.from({ length: 45 }, (_, k) => Object.assign(clone(s1), { id: 's' + (100 + k), start: 100 + k, touch: 100 + k }));
  m = joinProfiles(P({ sessions: many.slice(0, 30).reverse(), updatedAt: 1 }), P({ sessions: many.slice(15).reverse(), updatedAt: 2 }));
  ok(m.sessions.length === 30 && m.sessions[0].id === 's144' && m.sessions[29].id === 's115', 'the 30 newest sessions are kept, newest first', m.sessions.map(x => x.id).slice(0, 3));
  // something a later version of the page adds is carried, not dropped
  m = joinProfiles(P({ updatedAt: 5, future: { a: 1 } }), P({ updatedAt: 9 }));
  ok(m.future && m.future.a === 1, 'a field this version does not know is carried along', m.future);
  // rubbish in, no crash
  for (const bad of [null, undefined, 7, 'x', [], { q: 'no', days: [], sessions: {}, passed: null, settings: 3 }, { sessions: [null, 3, { id: 's9', start: 1 }] }]) {
    let threw = false; try { joinProfiles(bad, full); joinProfiles(full, bad); joinProfiles(bad, bad); } catch (e) { threw = String(e); }
    ok(!threw, 'a damaged copy does not stop the join', { bad, threw });
    ok(joinProfiles(bad, full).xp === 4000, 'a damaged copy does not wipe a good one', bad);
  }
  // a copy from before this change (with the old "base" mark) joins cleanly and loses the mark
  m = joinProfiles(Object.assign(clone(full), { base: 123 }), P({ updatedAt: 5 }));
  ok(m.base === undefined && m.xp === 4000, 'the old "base" mark is dropped');
  // the profile as it is saved for the student today
  const real = { attempts: {}, bestCombo: 0, days: {}, passed: {}, q: {}, sessions: [{ a: 0, best: 0, c: 0, cleared: [], end: null, failed: [], id: 's1794853431150', missed: [], passed: [], rapid: null, start: 1794853431150, studied: ['c01-s01'], touch: 1794853431150, xp: 0 }, { a: 0, best: 0, c: 0, cleared: [], end: 1794677649338, failed: [], id: 's1794677649338', missed: [], passed: [], rapid: null, start: 1794677649338, studied: ['c01-s01'], touch: 1794677649338, xp: 0 }], settings: { autoplay: true, chain: false, engine: 'auto', rate: 1, sound: true, voice: 'buttery' }, updatedAt: 1794853536153, v: 1, xp: 0 };
  ok(sigP(joinProfiles(real, real)) === sigP(normalize(clone(real))), 'a copy saved by the page before this change joins with itself unchanged');
  ok(sigP(joinProfiles(blank(), real)) === sigP(normalize(clone(real))) && sigP(joinProfiles(real, blank())) === sigP(normalize(clone(real))), '... and with an empty device');
}

// ================= 2. random histories
const RUNS = 1500;
let forgiven = 0, strict = 0, compared = 0;
for (let run = 0; run < RUNS; run++) {
  QIDS = run % 3 === 0 ? ALLQ : ALLQ.slice(0, run % 3 === 1 ? 5 : 12);
  let t = 1000 + Math.floor(rnd() * 3000);
  const start = device(blank());
  for (let k = Math.floor(rnd() * 25); k > 0; k--) step(start, t += 1 + Math.floor(rnd() * 400));
  const base = clone(start.P);

  // (a) one device going on from the base: joining its old and new copies gives the new one back
  const one = device(base); one.sess = (base.sessions.find(x => !x.end) || {}).id || null;
  for (let k = 1 + Math.floor(rnd() * 20); k > 0; k--) step(one, t += 1 + Math.floor(rnd() * 400));
  ok(same(joinProfiles(base, one.P), one.P) && same(joinProfiles(one.P, base), one.P), 'joined with an older copy of itself, a copy comes back unchanged', { run });
  ok(same(joinProfiles(one.P, one.P), one.P), 'joined with itself, a copy comes back unchanged', { run });

  // (b) two devices going on from the base at the same time
  const A = device(base), B = device(base);
  A.sess = B.sess = (base.sessions.find(x => !x.end) || {}).id || null;
  let ta = t + (t % 2), tb = t + (t % 2) + 1;               // A answers on even ticks, B on odd ones: the order of all answers is known
  for (let k = Math.floor(rnd() * 18); k > 0; k--) step(A, ta += 2 * (1 + Math.floor(rnd() * 250)));
  for (let k = Math.floor(rnd() * 18); k > 0; k--) step(B, tb += 2 * (1 + Math.floor(rnd() * 250)));
  const ab = joinProfiles(A.P, B.P), ba = joinProfiles(B.P, A.P);
  ok(sig(ab) === sig(ba), 'the order of joining does not matter', { run });
  const again = [joinProfiles(ab, A.P), joinProfiles(ab, B.P), joinProfiles(B.P, ab)].find(x => sig(x) !== sig(ab));
  ok(!again, 'joining again with either copy changes nothing', again && { run, where: firstDiff(ab, again) });
  holdsAll(ab, A.P, 'two devices'); holdsAll(ab, B.P, 'two devices');
  const now = Math.max(ta, tb);
  ok(streak(ab, now) >= Math.max(streak(A.P, now), streak(B.P, now)), 'the day streak never gets shorter by joining', { run, joined: streak(ab, now), a: streak(A.P, now), b: streak(B.P, now) });
  for (const k of Object.keys(ab.q)) {
    const x = A.P.q[k], y = B.P.q[k], m = ab.q[k];
    if (x && y && x.open && y.open) ok(m.open, 'a question on both weak lists stays on the weak list', k);
    if (m.open === false) ok((x && !x.open) || (y && !y.open), 'a question leaves the weak list only if some copy cleared it', k);
  }
  // against the truth: every answer of both devices in the order given
  const real = truth([start.log, A.log, B.log]);
  for (const k of Object.keys(real)) {
    compared++;
    if (real[k].open && !(ab.q[k] && ab.q[k].open)) { forgiven++; ok(false, 'a question that is truly on the weak list is on it after the join (no miss is forgiven)', { run, k, real: real[k], a: A.P.q[k], b: B.P.q[k], joined: ab.q[k] }); }
    if (!real[k].open && ab.q[k] && ab.q[k].open) strict++;      // kept on the list although truly cleared: the safe side, counted below
  }
  for (const id of [...A.P.sessions, ...B.P.sessions].map(x => x.id)) {
    const all = [...new Map([...A.P.sessions, ...B.P.sessions].map(x => [x.id, x])).values()].sort((p, q) => q.start - p.start).slice(0, 30).map(x => x.id);
    if (all.includes(id)) ok(ab.sessions.some(x => x.id === id), 'a recent session is kept', id);
  }

  // (c) three devices and an account: every sync is read, join, write. After two rounds everyone agrees.
  if (run % 3 === 0) {
    const devs = [device(base), device(base), device(base)];
    const tt = [t, t, t];
    let account = clone(base);
    const syncDev = d => { d.P = joinProfiles(d.P, account); account = clone(d.P); };
    for (let k = 0; k < 40; k++) {
      const n = Math.floor(rnd() * 3);
      if (rnd() < 0.3) syncDev(devs[n]); else step(devs[n], tt[n] += 1 + Math.floor(rnd() * 500));
    }
    const before = devs.map(d => clone(d.P));
    for (let round = 0; round < 2; round++) for (const d of devs) syncDev(d);
    ok(devs.every(d => sigP(d.P) === sigP(account)), 'after two rounds of syncing, every device and the account hold the same progress', { run });
    before.forEach((p, n) => holdsAll(account, p, 'three devices, device ' + n));
    // the same devices synced in the opposite order end at the same progress (settings and time stamp aside)
    const devs2 = before.map(p => device(p)); let account2 = clone(base);
    const sync2 = d => { d.P = joinProfiles(d.P, account2); account2 = clone(d.P); };
    for (let round = 0; round < 2; round++) for (const d of devs2.slice().reverse()) sync2(d);
    // whatever the order of syncing, the same progress comes out: passed cards, days, counts, and the weak list
    const core = p => sig({ passed: Object.keys(p.passed).sort(), days: p.days, read: p.read, xp: p.xp, attempts: Object.fromEntries(Object.entries(p.attempts).map(([k, v]) => [k, [v.n, v.best]])),
      q: Object.fromEntries(Object.entries(p.q).map(([k, v]) => [k, [v.seen, v.right, v.wrong, v.open]])) });
    ok(core(account) === core(account2), 'three devices synced in the opposite order end at the same progress and the same weak list', { run, where: firstDiff(JSON.parse(core(account)), JSON.parse(core(account2))) });
  }
}

// ================= 3. what the page itself relies on
{
  // xp equals the sum of the days' xp in every state the model can reach, so a join can rebuild it
  const d = device(blank()); let t = 5000;
  for (let k = 0; k < 400; k++) step(d, t += 1 + Math.floor(rnd() * 300));
  const sum = Object.values(d.P.days).reduce((s, x) => s + x.xp, 0);
  ok(sum === d.P.xp, 'XP is the sum of the days\' XP', { sum, xp: d.P.xp });
  // size: the profile at full use of the real manual (every question answered many times, every card passed and
  // listened to, four months of study days, 30 long sessions) must fit the store's 256 KiB limit.
  // The page trims old sessions once the text passes 200,000 characters and never below 3 sessions.
  const dir = path.join(ROOT, 'content/chapters');
  const cards = fs.readdirSync(dir).filter(f => f.endsWith('.json')).flatMap(f => JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')).sections);
  const big = blank(); let tt = 1;
  for (const c of cards) {
    big.passed[c.id] = { at: 1794853536153, tries: 3 }; big.attempts[c.id] = { n: 12, best: 100, last: 100 }; big.read[c.id] = { n: 9, at: 1794853536153 };
    for (const q of c.questions) big.q[q.id] = { seen: 14, right: 11, wrong: 3, run: 2, open: false, last: 1794853536153 + (tt++) };
  }
  for (let k = 0; k < 120; k++) big.days['2026-' + String(11 + Math.floor(k / 30)).padStart(2, '0') + '-' + String(1 + k % 30).padStart(2, '0')] = { a: 180, c: 150, xp: 2600, r: 12 };
  const ids = Object.keys(big.q), cids = Object.keys(big.passed);
  const noSessions = JSON.stringify(big).length;
  for (let k = 0; k < 30; k++) big.sessions.push({ id: 's' + (1794853431150 + k), start: 1794853431150 + k, touch: 1794853431150 + k, end: 1794853431150 + k, a: 200, c: 170, xp: 3000, best: 31, passed: cids.slice(0, 25), cleared: ids.slice(0, 60), failed: cids.slice(25, 35), missed: ids.slice(60, 140), studied: cids.slice(0, 30), rapid: { right: 5, total: 5 } });
  let body = JSON.stringify(big); const full = body.length;
  while (body.length > 200000 && big.sessions.length > 3) { big.sessions.pop(); body = JSON.stringify(big); }
  ok(cards.length >= 220 && ids.length >= 1197, 'the size test uses the real manual', { cards: cards.length, questions: ids.length });
  ok(noSessions < 170000, 'everything but the sessions fits with room to spare', { noSessions });
  ok(body.length <= 200000, 'the profile at full use is written under 200,000 characters (the store allows 262,144)', { full, written: body.length, sessionsKept: big.sessions.length });
  console.log('size at full use: ' + noSessions + ' characters without sessions, ' + full + ' with 30 long sessions, ' + body.length + ' written with ' + big.sessions.length + ' sessions kept (the store allows 262,144)');
}

console.log(`weak list against the true order of answers: ${compared} questions compared, ${forgiven} misses forgiven (must be 0), ${strict} kept on the list although truly cleared (the safe side: one more right answer clears them).`);
console.log(`${checks - failures}/${checks} join checks pass (${RUNS} random histories, seed ${process.argv[2] || 20261116}).`);
process.exit(failures ? 1 : 0);
