// A visit in which the saved copy never loads, then a normal visit: the account copy must survive.
// usage: node sync2.js <built page>
const { chromium } = require('playwright');
const page_ = process.argv[2];
const results = [];
const check = (name, ok, detail) => { results.push(ok); console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail !== undefined ? '  ' + JSON.stringify(detail) : '')); };

const fake = () => {
  // the "account" lives in sessionStorage so it survives the reload inside this test
  const read = () => JSON.parse(sessionStorage.getItem('__acct') || 'null');
  if (!read()) sessionStorage.setItem('__acct', JSON.stringify({ v: 1, updatedAt: 1700000000000, xp: 4321, bestCombo: 9, days: {}, passed: { 'c01-s01': { at: 5, score: 100 } }, attempts: {}, q: {}, sessions: [], settings: { voice: 'buttery', rate: 1, sound: true } }));
  window.__sets = 0;
  const doc = {
    get: () => sessionStorage.getItem('__online') ? Promise.resolve({ exists: true, data: read }) : new Promise((_, rej) => setTimeout(() => rej({ code: 'unavailable' }), 100)),
    set: v => { window.__sets++; sessionStorage.setItem('__acct', JSON.stringify(v)); return Promise.resolve(); },
  };
  window.claude = { use: name => Promise.resolve(name === 'db' ? { doc: () => doc } : name === 'user' ? { id: () => Promise.resolve('u1') } : null) };
};
const state = () => ({ acct: JSON.parse(sessionStorage.getItem('__acct')).xp, passed: Object.keys(JSON.parse(sessionStorage.getItem('__acct')).passed).length,
  chip: (document.querySelector('#chip-xp') || {}).textContent, local: JSON.parse(localStorage.getItem('pas-profile-v1') || '{}'), sets: window.__sets });

(async () => {
  const browser = await chromium.launch();
  for (const [name, local] of [['empty device', null], ['older device copy', { v: 1, updatedAt: 1600000000000, xp: 10, passed: {}, q: {}, days: {}, attempts: {}, sessions: [], settings: {} }]]) {
    const ctx = await browser.newContext({ viewport: { width: 420, height: 900 } });
    const page = await ctx.newPage();
    await page.addInitScript(fake);
    if (local) await page.addInitScript(l => { if (!localStorage.getItem('pas-profile-v1')) localStorage.setItem('pas-profile-v1', JSON.stringify(l)); }, local);
    await page.goto('file://' + page_);
    await page.waitForTimeout(300);
    // offline visit: open a card, change two settings (each one saves)
    await page.evaluate(() => { const r = document.querySelector('.secrow[data-sid="c01-s02"]'); r.closest('details').open = true; });
    await page.click('.secrow[data-sid="c01-s02"]');
    await page.waitForTimeout(150);
    await page.check('#chk-chain');
    await page.selectOption('#sel-rate', '1.15');
    await page.waitForTimeout(13000);                  // let the three retries run out
    let s = await page.evaluate(state);
    check(name + ': nothing was written to the account during the visit that could not read it', s.acct === 4321 && s.sets === 0, { acct: s.acct, sets: s.sets, base: s.local.base });
    // next visit: the account can be read again
    await page.evaluate(() => sessionStorage.setItem('__online', '1'));
    await page.reload();
    await page.waitForTimeout(2500);
    s = await page.evaluate(state);
    check(name + ': on the next visit the account copy is kept and shown', s.acct === 4321 && s.passed === 1 && /4,321/.test(s.chip || '') && s.local.base === undefined, { acct: s.acct, chip: s.chip, base: s.local.base });
    await ctx.close();
  }
  // a device that was in step with the account keeps what it did offline
  {
    const ctx = await browser.newContext({ viewport: { width: 420, height: 900 } });
    const page = await ctx.newPage();
    await page.addInitScript(fake);
    await page.addInitScript(() => { if (!localStorage.getItem('pas-profile-v1')) localStorage.setItem('pas-profile-v1', JSON.stringify({ v: 1, updatedAt: 1700000000000, xp: 4321, bestCombo: 9, days: {}, passed: { 'c01-s01': { at: 5, score: 100 } }, attempts: {}, q: {}, sessions: [], settings: { voice: 'buttery', rate: 1, sound: true } })); });
    await page.goto('file://' + page_);
    await page.waitForTimeout(300);
    await page.evaluate(() => { const r = document.querySelector('.secrow[data-sid="c01-s02"]'); r.closest('details').open = true; });
    await page.click('.secrow[data-sid="c01-s02"]');
    await page.waitForTimeout(150);
    await page.check('#chk-chain');
    await page.waitForTimeout(800);
    await page.evaluate(() => sessionStorage.setItem('__online', '1'));
    await page.reload();
    await page.waitForTimeout(2500);
    const s = await page.evaluate(() => ({ acct: JSON.parse(sessionStorage.getItem('__acct')), sets: window.__sets }));
    check('a device that was in step saves its offline changes on the next visit', s.acct.xp === 4321 && s.acct.settings.chain === true && s.sets >= 1, { chain: s.acct.settings.chain, sets: s.sets });
    await ctx.close();
  }
  await browser.close();
  console.log(`\n${results.filter(Boolean).length} of ${results.length} checks passed`);
  process.exit(results.every(Boolean) ? 0 : 1);
})();
