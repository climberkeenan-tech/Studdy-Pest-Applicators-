#!/usr/bin/env node
// Regression test for the page's typed-answer grading (short-answer questions).
// Usage: node tools/check_grader.js
// Runs the grader exactly as it is written in app/template.html against tools/grader_cases.json:
// every "right" answer must be accepted and every "wrong" answer must be rejected.
// A wrong answer that passes is the serious failure: the local check has no second opinion when it says "correct".
const fs = require('fs'), path = require('path');
const root = path.join(__dirname, '..');
const src = fs.readFileSync(path.join(root, 'app/template.html'), 'utf8');
const i = src.indexOf('const NEG ='), j = src.indexOf('let samplerOff', i);
if (i < 0 || j < 0) { console.error('grader not found in app/template.html'); process.exit(2); }
const localGrade = new Function("const plain = s => String(s ?? '').replace(/\\*\\*/g, '');\n" + src.slice(i, j) + '\nreturn localGrade;')();

const Q = {};
const dir = path.join(root, 'content/chapters');
for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.json')))
  for (const s of JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')).sections)
    for (const q of s.questions) Q[q.id] = q;
for (const s of JSON.parse(fs.readFileSync(path.join(root, 'content/study.json'), 'utf8')).sections)
  for (const q of s.questions) Q[q.id] = q;

const cases = JSON.parse(fs.readFileSync(path.join(__dirname, 'grader_cases.json'), 'utf8'));
let falseAccept = 0, falseReject = 0, total = 0, missing = 0;
const covered = new Set();
for (const c of cases) {
  const q = Q[c.id];
  if (!q || q.kind !== 'short') { console.log(`MISSING: ${c.id} is not a short-answer question any more (remove or rename its cases)`); missing++; continue; }
  covered.add(c.id);
  for (const a of c.right || []) { total++; if (!localGrade(q, a)) { falseReject++; console.log(`FALSE REJECT ${c.id}: ${JSON.stringify(a)}`); } }
  for (const a of c.wrong || []) { total++; if (localGrade(q, a)) { falseAccept++; console.log(`FALSE ACCEPT ${c.id}: ${JSON.stringify(a)}`); } }
}
const uncovered = Object.values(Q).filter(q => q.kind === 'short' && !covered.has(q.id)).map(q => q.id);
if (uncovered.length) console.log(`note: ${uncovered.length} short-answer questions have no cases: ${uncovered.join(', ')}`);
console.log(`${total - falseAccept - falseReject}/${total} grader cases pass (${falseAccept} false accepts, ${falseReject} false rejects, ${missing} missing questions).`);
process.exit(falseAccept || falseReject || missing ? 1 : 0);
