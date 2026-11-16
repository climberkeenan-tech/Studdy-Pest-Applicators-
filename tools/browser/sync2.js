// A visit in which the saved copy never loads, then a normal visit: the account copy must survive,
// and what the student did in the first visit must not be lost either.
// usage: node sync2.js <built page>
// The stand-in account lives in this script, not in the page: a browser may drop a page's own session
// storage on reload, and a test of saving must not depend on that.
const { chromium } = require('playwright');
const page_ = process.argv[2];
const results = [];
const check = (name, ok, detail) => { results.push(ok); console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail !== undefined ? '  ' + JSON.stringify(detail) : '')); };
const START = () => ({ v: 1, updatedAt: 1700000000000, xp: 4321, bestCombo: 9, days: {}, passed: { 'c01-s01': { at: 5, score: 100 } }, attempts: {}, q: {}, sessions: [], settings: { voice: 'buttery', rate: 1, sound: true } });

const inPage = () => {
  const down = () => ({ code: 'unavailable', message: 'the account cannot be reached' });
  const doc = {
    get: async () => { let d; try { d = await window.__acctGet(); } catch (e) { await new Promise(r => setTimeout(r, 100)); throw down(); } return { id: 'profile', exists: d !== null && d !== undefined, data: () => d, metadata: {} }; },
    set: async v => { try { await window.__acctSet(JSON.parse(JSON.stringify(v))); } catch (e) { throw down(); } },
  };
  window.claude = { use: name => Promise.resolve(name === 'db' ? { doc: () => doc } : name === 'user' ? { id: () => Promise.resolve('u1') } : null) };
};
async function visit(browser, local) {
  const w = { doc: START(), sets: 0, online: false };
  w.ctx = await browser.newContext({ viewport: { width: 420, height: 900 } });
  await w.ctx.exposeFunction('__acctGet', () => { if (!w.online) throw new Error('offline'); return w.doc; });
  await w.ctx.exposeFunction('__acctSet', v => { if (!w.online) throw new Error('offline'); w.sets++; w.doc = v; });
  await w.ctx.addInitScript(inPage);
  if (local) await w.ctx.addInitScript(l => { if (!localStorage.getItem('pas-profile-v1')) localStorage.setItem('pas-profile-v1', JSON.stringify(l)); }, local);
  w.page = await w.ctx.newPage();
  w.errs = []; w.page.on('pageerror', e => w.errs.push(e.message));
  await w.page.goto('file://' + page_);
  await w.page.waitForTimeout(300);
  return w;
}
const shown = page => page.evaluate(() => ({ chip: (document.querySelector('#chip-xp') || {}).textContent, local: JSON.parse(localStorage.getItem('pas-profile-v1') || '{}') }));
const tapOffline = async page => {      // open a card and change two settings: each one saves
  await page.evaluate(() => { const r = document.querySelector('.secrow[data-sid="c01-s02"]'); r.closest('details').open = true; });
  await page.click('.secrow[data-sid="c01-s02"]');
  await page.waitForTimeout(150);
  await page.check('#chk-chain');
  await page.selectOption('#sel-rate', '1.15');
};

(async () => {
  const browser = await chromium.launch();
  for (const [name, local] of [['empty device', null], ['older device copy', { v: 1, updatedAt: 1600000000000, xp: 10, passed: {}, q: {}, days: {}, attempts: {}, sessions: [], settings: {} }]]) {
    const w = await visit(browser, local);
    await tapOffline(w.page);
    await w.page.waitForTimeout(13000);                  // let the retries of the first read run out
    check(name + ': nothing was written to the account during the visit that could not read it', w.doc.xp === 4321 && w.sets === 0, { xp: w.doc.xp, sets: w.sets });
    w.online = true;                                     // next visit: the account can be read again
    await w.page.reload();
    await w.page.waitForTimeout(2500);
    const s = await shown(w.page);
    check(name + ': on the next visit the account copy is kept and shown', w.doc.xp === 4321 && Object.keys(w.doc.passed).length === 1 && /4,321/.test(s.chip || '') && s.local.xp === 4321 && s.local.base === undefined, { xp: w.doc.xp, chip: s.chip, localXp: s.local.xp });
    check(name + ': and the settings changed in the first visit are kept too', w.doc.settings.chain === true && w.doc.settings.rate === 1.15, w.doc.settings);
    check(name + ': no page errors', w.errs.length === 0, w.errs);
    await w.ctx.close();
  }
  // a device that was in step with the account keeps what it did offline
  {
    const w = await visit(browser, START());
    await tapOffline(w.page);
    await w.page.waitForTimeout(800);
    w.online = true;
    await w.page.reload();
    await w.page.waitForTimeout(2500);
    check('a device that was in step saves its offline changes on the next visit', w.doc.xp === 4321 && w.doc.settings.chain === true && w.sets >= 1, { chain: w.doc.settings.chain, sets: w.sets });
    await w.ctx.close();
  }
  await browser.close();
  console.log(`\n${results.filter(Boolean).length} of ${results.length} checks passed`);
  process.exit(results.every(Boolean) ? 0 : 1);
})();
