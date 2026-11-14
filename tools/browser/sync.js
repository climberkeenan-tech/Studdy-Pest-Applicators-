// Saved progress must survive taps made before it has loaded. usage: node sync.js <built page>
const { chromium } = require('playwright');
const page_ = process.argv[2];
const results = [];
const check = (name, ok, detail) => { results.push(ok); console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail !== undefined ? '  ' + JSON.stringify(detail) : '')); };

const fake = opts => {
  // the account already holds real progress; this device's copy is empty (or older)
  window.__remote = { v: 1, updatedAt: opts.remoteStamp, xp: 4321, bestCombo: 9, days: {}, passed: { 'c01-s01': { at: 5, score: 100 } }, attempts: {}, q: {}, sessions: [], settings: { voice: 'buttery', rate: 1, sound: true } };
  window.__sets = [];
  if (opts.local) localStorage.setItem('pas-profile-v1', JSON.stringify(opts.local));
  const doc = { get: () => new Promise(r => setTimeout(() => r({ exists: true, data: () => window.__remote }), opts.delay)), set: v => { window.__sets.push(JSON.parse(JSON.stringify(v))); window.__remote = v; return Promise.resolve(); } };
  window.claude = { use: name => Promise.resolve(name === 'db' ? { doc: () => doc } : name === 'user' ? { id: () => Promise.resolve('u1') } : null) };
};
const state = () => ({ sets: window.__sets.map(s => ({ xp: s.xp, passed: Object.keys(s.passed || {}).length, chain: s.settings && s.settings.chain })), remoteXp: window.__remote.xp,
  chip: (document.querySelector('#chip-xp') || {}).textContent, local: JSON.parse(localStorage.getItem('pas-profile-v1') || '{}').xp });

(async () => {
  const browser = await chromium.launch();
  const run = async (name, opts, act) => {
    const ctx = await browser.newContext({ viewport: { width: 420, height: 900 } });
    const page = await ctx.newPage();
    await page.addInitScript(fake, opts);
    await page.goto('file://' + page_);
    await page.waitForTimeout(250);
    await act(page);                      // taps made while the saved copy is still loading
    await page.waitForTimeout(opts.delay + 1800);
    const s = await page.evaluate(state);
    await ctx.close();
    return s;
  };
  const tapEarly = async page => {
    await page.evaluate(() => { const r = document.querySelector('.secrow[data-sid="c01-s02"]'); r.closest('details').open = true; });
    await page.click('.secrow[data-sid="c01-s02"]');
    await page.waitForTimeout(150);
    await page.check('#chk-chain');       // a new place that saves
    await page.selectOption('#sel-rate', '1.15');
  };

  let s = await run('empty device', { remoteStamp: 1700000000000, delay: 1500 }, tapEarly);
  check('an empty device does not overwrite saved progress when the student taps before it loads', s.remoteXp === 4321 && s.sets.every(x => x.xp === 4321 && x.passed === 1), s);
  check('the saved progress is what the page then shows and keeps on this device', /4,321/.test(s.chip || '') && s.local === 4321, { chip: s.chip, local: s.local });

  s = await run('older device copy', { remoteStamp: 1700000000000, delay: 1500, local: { v: 1, updatedAt: 1600000000000, xp: 10, passed: {}, q: {}, days: {}, attempts: {}, sessions: [], settings: {} } }, tapEarly);
  check('an older copy on the device does not overwrite newer saved progress', s.remoteXp === 4321 && s.sets.every(x => x.xp === 4321), s);

  s = await run('newer device copy', { remoteStamp: 1600000000000, delay: 800, local: { v: 1, updatedAt: 1700000000000, xp: 9999, passed: { a: 1, b: 2 }, q: {}, days: {}, attempts: {}, sessions: [], settings: {} } }, async () => {});
  check('a device copy that really is newer is still saved to the account', s.remoteXp === 9999 && s.sets.length >= 1 && s.sets[0].xp === 9999, s);

  s = await run('newer device copy plus early taps', { remoteStamp: 1600000000000, delay: 1200, local: { v: 1, updatedAt: 1700000000000, xp: 9999, passed: { a: 1 }, q: {}, days: {}, attempts: {}, sessions: [], settings: {} } }, tapEarly);
  check('early taps on a newer device copy are kept and saved', s.remoteXp === 9999 && s.sets.length >= 1 && s.sets[s.sets.length - 1].chain === true, s);

  s = await run('loaded, then a change', { remoteStamp: 1700000000000, delay: 300 }, async page => { await page.waitForTimeout(900); await tapEarly(page); });
  check('after loading, a change is saved on top of the saved progress', s.sets.length >= 1 && s.sets[s.sets.length - 1].xp === 4321 && s.sets[s.sets.length - 1].chain === true, s);

  await browser.close();
  console.log(`\n${results.filter(Boolean).length} of ${results.length} checks passed`);
  process.exit(results.every(Boolean) ? 0 : 1);
})();
