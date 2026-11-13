// Screenshot every figure of every card for visual review.
// Photos: 400px phone width. Diagrams: 800px (light and dark) plus 400px phone width.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const pagePath = process.argv[2] || '/home/user/Studdy-Pest-Applicators-/dist/pest-study.html';
const outDir = path.join(__dirname, 'figs');
(async () => {
  const b = await chromium.launch();
  const index = {};
  const errs = [];
  const modes = [
    { name: 'photo', w: 400, scheme: 'light', want: f => !f.svg },
    { name: 'light', w: 800, scheme: 'light', want: f => !!f.svg },
    { name: 'dark', w: 800, scheme: 'dark', want: f => !!f.svg },
    { name: 'phone', w: 400, scheme: 'light', want: f => !!f.svg },
  ];
  for (const m of modes) {
    const ctx = await b.newContext({ viewport: { width: m.w, height: 900 }, deviceScaleFactor: 1, colorScheme: m.scheme });
    const p = await ctx.newPage();
    p.on('pageerror', e => errs.push(m.name + ': ' + e.message));
    await p.goto('file://' + pagePath);
    await p.waitForTimeout(400);
    const secs = await p.evaluate(() => {
      const C = JSON.parse(document.getElementById('content').textContent);
      return C.sections.filter(s => !s.practice && (s.figures || []).length).map(s => {
        const order = [];
        const F = Object.fromEntries(s.figures.map(f => [f.id, f]));
        for (const blk of s.body) { if (blk.fig) order.push(blk.fig); if (blk.gallery) order.push(...blk.gallery); }
        return { id: s.id, title: s.title, figs: order.map(id => ({ id, svg: !!F[id].svg, title: F[id].title, page: F[id].page || '', explain: F[id].explain || [] })) };
      });
    });
    for (const s of secs) {
      if (!s.figs.some(m.want)) continue;
      await p.evaluate(sid => {
        const el = document.querySelector('.secrow[data-sid="' + sid + '"]');
        if (el) el.click();
      }, s.id);
      await p.waitForTimeout(150);
      const els = await p.$$('#reading figure.fig');
      if (els.length !== s.figs.length) errs.push(s.id + ': ' + els.length + ' figure elements vs ' + s.figs.length + ' expected');
      for (let k = 0; k < s.figs.length && k < els.length; k++) {
        const f = s.figs[k];
        if (!m.want(f)) continue;
        const ch = 'ch' + s.id.slice(1, 3);
        fs.mkdirSync(path.join(outDir, ch), { recursive: true });
        const file = path.join(outDir, ch, s.id + '__' + f.id + '__' + m.name + '.png');
        const target = f.svg ? await els[k].$('.fig-art') : els[k];
        await target.scrollIntoViewIfNeeded();
        await target.screenshot({ path: file });
        index[ch] = index[ch] || {};
        const key = s.id + '/' + f.id;
        index[ch][key] = index[ch][key] || { card: s.id, cardTitle: s.title, figId: f.id, type: f.svg ? 'diagram' : 'photo', title: f.title, page: f.page, explain: f.explain, files: {} };
        index[ch][key].files[m.name] = file;
      }
      await p.evaluate(() => { const h = document.querySelector('[data-act="home"]'); if (h) h.click(); });
      await p.waitForTimeout(60);
    }
    await ctx.close();
  }
  await b.close();
  const counts = {};
  for (const ch of Object.keys(index)) {
    fs.writeFileSync(path.join(outDir, ch, 'index.json'), JSON.stringify(Object.values(index[ch]), null, 1));
    counts[ch] = Object.keys(index[ch]).length;
  }
  console.log(JSON.stringify(counts));
  console.log('ERRORS:', errs.length ? errs.slice(0, 10).join(' | ') : 'none');
})();
