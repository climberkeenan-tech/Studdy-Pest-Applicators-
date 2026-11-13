// node probe.js <probesFile>
// probesFile: JSON array of { id, right: [answers that must be accepted], wrong: [answers that must be rejected],
//   answer?, accept?, keys? }  -- answer/accept/keys, when present, are PROPOSED replacements tested instead of the current ones.
const fs = require('fs'), path = require('path');
const { localGrade } = require('./grader.js');
const Q = JSON.parse(fs.readFileSync(path.join(__dirname, 'data/questions.json'), 'utf8'));
const probes = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
let bad = 0, total = 0;
for (const p of probes) {
  const base = Q[p.id]; if (!base) { console.log('UNKNOWN QUESTION ' + p.id); bad++; continue; }
  if (base.kind !== 'short') { console.log('NOT A SHORT QUESTION ' + p.id); continue; }
  const q = { ...base };
  const over = ['answer', 'accept', 'keys'].filter(k => p[k] !== undefined);
  for (const k of over) q[k] = p[k];
  if (over.includes('keys') && Array.isArray(p.keys) && p.keys.length === 0) delete q.keys;
  const lines = [];
  for (const r of p.right || []) { total++; if (!localGrade(q, r)) { bad++; lines.push(`  FALSE REJECT (right answer refused): ${JSON.stringify(r)}`); } }
  for (const w of p.wrong || []) { total++; if (localGrade(q, w)) { bad++; lines.push(`  FALSE ACCEPT (wrong answer passed): ${JSON.stringify(w)}`); } }
  console.log(`${p.id} ${over.length ? '[testing proposed ' + over.join('+') + ']' : '[current grading]'}: ${lines.length ? 'PROBLEMS' : 'ok'}  (canonical: ${JSON.stringify(q.answer)}; accept: ${JSON.stringify(q.accept || [])}; keys: ${JSON.stringify(q.keys || [])})`);
  for (const l of lines) console.log(l);
}
console.log(`\n${total - bad}/${total} probes behaved as expected.`);
