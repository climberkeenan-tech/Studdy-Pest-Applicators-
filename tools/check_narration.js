#!/usr/bin/env node
/* Checks that the page and tools/narrate.py agree about every card's spoken text.

   The page plays a card's recording only if its own hash of the card's sentences equals the hash that
   narrate.py stored, and it lights up words by number. So the two programs must split a card into the
   same sentences and the same words. This test runs the page's own functions (taken from the built page)
   over every card and compares them with narrate.py.

   usage: python3 tools/build.py && node tools/check_narration.js
*/
const fs = require('fs'), path = require('path'), vm = require('vm'), cp = require('child_process');
const ROOT = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'dist', 'pest-study.html'), 'utf8');
const C = JSON.parse(html.match(/<script id="content" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const js = html.slice(html.indexOf('<script>\n(() => {'));

// the page's own code, cut out by name
const grab = (start, end) => { const a = js.indexOf(start); const b = js.indexOf(end, a); if (a < 0 || b < 0) throw new Error('cannot find ' + start); return js.slice(a, b); };
const code = [
  grab('const esc = ', '\nconst md = '),
  grab('const plain = ', '\nconst dayKey'),
  grab('function fnv(str)', '\nconst hashMemo'),
  grab('function sentence(t, i) {', '\nfunction figureHtml'),
].join('\n');
const box = {};
vm.runInNewContext(code + '\nout.fnv = fnv; out.spokenLines = spokenLines; out.sentence = sentence;', { out: box });

const py = cp.execFileSync('python3', ['-c', `
import json, sys
sys.path.insert(0, ${JSON.stringify(path.join(ROOT, 'tools'))})
import narrate
out = {}
for s in narrate.load_sections():
    lines = narrate.spoken_lines(s)
    out[s['id']] = {'h': narrate.text_hash(lines), 'words': [len(narrate.display_words(t)) for _, t in lines]}
print(json.dumps(out))
`], { maxBuffer: 1 << 26 });
const want = JSON.parse(py);

let bad = 0, cards = 0, lines = 0, recorded = 0, wordLines = 0;
const fail = msg => { if (bad++ < 12) console.log('FAIL ' + msg); };
for (const s of C.sections) {
  cards++;
  const w = want[s.id];
  if (!w) { fail(s.id + ': narrate.py does not know this card'); continue; }
  const mine = box.spokenLines(s);
  const h = box.fnv(mine.join('\n'));
  if (h !== w.h) fail(`${s.id}: the page hashes its text to ${h}, narrate.py to ${w.h}`);
  if (mine.length !== w.words.length) { fail(`${s.id}: the page has ${mine.length} sentences, narrate.py ${w.words.length}`); continue; }
  // the words the page will wrap, sentence by sentence, from the same raw text the page renders
  const raw = [];
  const fig = id => { const f = (s.figures || []).find(f => f.id === id); raw.push(f.title + (/[.!?:]$/.test(f.title) ? '' : '.')); for (const e of f.explain || []) raw.push(e); };
  for (const b of s.body || []) {
    if (b.h) raw.push(b.h);
    else if (b.box !== undefined) { raw.push(b.box); for (const k of ['p', 'list', 'ol']) for (const t of b[k] || []) raw.push(t); }
    else if (b.p) raw.push(...b.p); else if (b.list) raw.push(...b.list); else if (b.ol) raw.push(...b.ol);
    else if (b.fig) fig(b.fig); else if (b.gallery) b.gallery.forEach(fig);
  }
  raw.forEach((t, i) => {
    lines++;
    const n = (box.sentence(t, i).match(/<span class="w/g) || []).length;
    if (n !== w.words[i]) fail(`${s.id} sentence ${i}: the page wraps ${n} words, narrate.py counts ${w.words[i]}`);
  });
  const rec = C.narration && C.narration.cards[s.id];
  if (rec) {
    recorded++;
    if (rec.t.length !== 2 * mine.length) fail(`${s.id}: recording has ${rec.t.length / 2} sentences, the card ${mine.length}`);
    rec.w.forEach((ws, i) => {
      wordLines++;
      if (ws.length !== w.words[i]) fail(`${s.id} sentence ${i}: recording has ${ws.length} word times, the card ${w.words[i]} words`);
      for (let k = 1; k < ws.length; k++) if (ws[k] < ws[k - 1]) { fail(`${s.id} sentence ${i}: word times go backwards`); break; }
      if (ws.length && ws[ws.length - 1] > rec.t[2 * i + 1] - rec.t[2 * i] + 1) fail(`${s.id} sentence ${i}: a word starts after its sentence ends`);
    });
    for (let i = 1; i < rec.t.length; i++) if (rec.t[i] < rec.t[i - 1]) { fail(`${s.id}: sentence times go backwards`); break; }
    if (rec.t[rec.t.length - 1] > rec.d) fail(`${s.id}: the last sentence ends after the audio does`);
  }
}
console.log(`${cards} cards, ${lines} sentences: page and narrate.py ${bad ? 'DISAGREE' : 'agree'}. ${recorded} recordings checked (${wordLines} sentences of word times).`);
process.exit(bad ? 1 : 0);
