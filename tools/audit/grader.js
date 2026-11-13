// Loads the page's own typed-answer grader straight from app/template.html.
const fs = require('fs');
const src = fs.readFileSync(require('path').join(__dirname, 'template.snapshot.html'), 'utf8');
const i = src.indexOf('const NEG ='), j = src.indexOf('let samplerOff', i);
if (i < 0 || j < 0) throw new Error('grader not found in template');
const code = "const plain = s => String(s ?? '').replace(/\\*\\*/g, '');\n" + src.slice(i, j) + '\nreturn localGrade;';
module.exports = { localGrade: new Function(code)() };
