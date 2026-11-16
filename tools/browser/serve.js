// A static file server for the browser tests. The page must be loaded over http, not from a file:// address:
// Chromium now and then hands a reloaded file:// page an empty localStorage, and a test of saving then fails
// at random (seen here in 13 of 30 runs under load, never over http).
// usage: const { srv, base } = await serve(dir);   page.goto(base + 'pest-study.html');   srv.close();
const http = require('http'), fs = require('fs'), path = require('path');
module.exports = function serve(dir) {
  const SITE = fs.realpathSync(path.resolve(dir));
  const srv = http.createServer((req, rsp) => {
    let f = path.join(SITE, decodeURIComponent(req.url.split('?')[0]));
    try { f = fs.realpathSync(f); } catch (e) { rsp.writeHead(404); return rsp.end('not found'); }
    if (!f.startsWith(SITE) || fs.statSync(f).isDirectory()) { rsp.writeHead(404); return rsp.end('not found'); }
    const size = fs.statSync(f).size, type = f.endsWith('.mp3') ? 'audio/mpeg' : f.endsWith('.html') ? 'text/html; charset=utf-8' : 'application/octet-stream';
    const m = /bytes=(\d+)-(\d*)/.exec(req.headers.range || '');
    if (m) { const a = +m[1], b = m[2] ? +m[2] : size - 1; rsp.writeHead(206, { 'Content-Type': type, 'Content-Range': `bytes ${a}-${b}/${size}`, 'Content-Length': b - a + 1, 'Accept-Ranges': 'bytes' }); fs.createReadStream(f, { start: a, end: b }).pipe(rsp); }
    else { rsp.writeHead(200, { 'Content-Type': type, 'Content-Length': size, 'Accept-Ranges': 'bytes' }); fs.createReadStream(f).pipe(rsp); }
  });
  return new Promise(r => srv.listen(0, '127.0.0.1', () => r({ srv, base: `http://127.0.0.1:${srv.address().port}/` })));
};
