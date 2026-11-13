// node compare.js <chunkId> <answersFile>
// Prints every question where the blind solver and the answer key disagree, or something else looks off.
const fs = require('fs'), path = require('path');
const { localGrade } = require('./grader.js');
const [chunkId, ansFile] = process.argv.slice(2);
const Q = JSON.parse(fs.readFileSync(path.join(__dirname, 'data/questions.json'), 'utf8'));
const chunk = JSON.parse(fs.readFileSync(path.join(__dirname, 'data/chunks.json'), 'utf8')).find(c => c.id === chunkId);
if (!chunk) { console.error('unknown chunk ' + chunkId); process.exit(2); }
let raw = JSON.parse(fs.readFileSync(ansFile, 'utf8'));
const answers = Array.isArray(raw) ? raw : raw.answers;
const A = {}; for (const a of answers) A[String(a.id).trim()] = a;
const LET = 'ABCDEF';
const disputes = []; let agree = 0;
for (const id of chunk.qids) {
  const q = Q[id], a = A[id];
  const base = { id, card: q.sid, src: q.src, style: q.style || 'plain', kind: q.kind, stem: q.q };
  if (!a) { disputes.push({ ...base, reasons: ['solver gave no answer'] }); continue; }
  const reasons = []; const ans = String(a.answer ?? '').trim();
  let keyText, solverText = ans;
  if (q.kind === 'mc') {
    const m = ans.toUpperCase().match(/^[A-F]/); const idx = m ? LET.indexOf(m[0]) : -1;
    keyText = `${LET[q.answer]}) ${q.choices[q.answer]}`;
    solverText = idx >= 0 && idx < q.choices.length ? `${LET[idx]}) ${q.choices[idx]}` : ans + ' (not a valid letter)';
    if (idx !== q.answer) reasons.push('solver chose a different answer than the key');
    if (String(a.alsoCorrect || '').trim()) reasons.push('solver says other choices are also correct: ' + a.alsoCorrect);
    base.choices = q.choices.map((c, k) => `${LET[k]}) ${c}`);
  } else if (q.kind === 'tf') {
    keyText = q.answer ? 'True' : 'False';
    const t = /^t/i.test(ans) ? true : /^f/i.test(ans) ? false : null;
    if (t !== q.answer) reasons.push('solver chose a different answer than the key');
  } else {
    keyText = q.answer;
    base.accept = q.accept || []; base.keys = q.keys || [];
    if (!localGrade(q, ans)) reasons.push("the app's local grader REJECTED the solver's typed answer (decide: was the solver's answer actually right?)");
  }
  if (a.supported && a.supported !== 'yes') reasons.push(`solver says the card text supports the answer: "${a.supported}"`);
  if (String(a.note || '').trim()) reasons.push('solver note: ' + a.note);
  if (!reasons.length) { agree++; continue; }
  disputes.push({ ...base, key: keyText, solverAnswer: solverText, solverQuote: a.quote || '', why: q.why, ref: q.ref, reasons });
}
console.log(`CHUNK ${chunkId}: ${chunk.qids.length} questions, ${agree} clean agreements, ${disputes.length} to rule on.`);
console.log('Review-question keys (src=review) come from the manual\'s Appendix A and are final.');
for (const d of disputes) console.log('\n' + JSON.stringify(d, null, 1));
