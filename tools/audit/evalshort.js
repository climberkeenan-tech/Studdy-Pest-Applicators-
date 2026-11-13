// node evalshort.js <candidates.json> <out.json>
// candidates.json: [{ id, right: [...], wrong: [...], candidates: [{ name, answer?, accept?, keys? }] }]
// For each candidate grading of each short question, run every probe through the page's own grader.
const fs = require('fs'), path = require('path');
const { localGrade } = require('./grader.js');
const Q = JSON.parse(fs.readFileSync(path.join(__dirname, 'data/questions.json'), 'utf8'));
const items = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const out = [];
for (const it of items) {
  const base = Q[it.id];
  const res = { id: it.id, q: base.q, results: [] };
  for (const c of it.candidates) {
    const q = { ...base };
    for (const k of ['answer', 'accept', 'keys', 'ordered']) if (c[k] !== undefined) q[k] = c[k];
    if (Array.isArray(q.keys) && q.keys.length === 0) delete q.keys;
    const falseReject = (it.right || []).filter(a => !localGrade(q, a));
    const falseAccept = (it.wrong || []).filter(a => localGrade(q, a));
    res.results.push({ name: c.name, falseAccept, falseReject, grading: { answer: q.answer, accept: q.accept || [], keys: q.keys || [], ordered: !!q.ordered } });
  }
  out.push(res);
}
fs.writeFileSync(process.argv[3], JSON.stringify(out, null, 1));
console.log('evaluated', out.length, 'questions');
