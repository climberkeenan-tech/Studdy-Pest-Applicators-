"""Render audit inputs from the repo content. Read-only on the repo."""
import json, glob, re, os, math, html, pathlib
REPO = pathlib.Path('/home/user/Studdy-Pest-Applicators-')
OUT = pathlib.Path(os.environ.get('AUDIT_OUT') or pathlib.Path(__file__).resolve().parent)
OUT.mkdir(exist_ok=True)
ONLY = set(json.load(open(os.environ['AUDIT_ONLY']))) if os.environ.get('AUDIT_ONLY') else None
PREFIX = os.environ.get('AUDIT_PREFIX', '')
LET = 'ABCDEF'
for d in ('solve', 'audit', 'ctx', 'data', 'out', 'probes'):
    (OUT / d).mkdir(exist_ok=True)

def svg_texts(name):
    p = REPO / 'content' / 'figures' / name
    if not p.exists(): return []
    s = p.read_text(encoding='utf-8')
    out = []
    for m in re.findall(r'<text[^>]*>(.*?)</text>', s, flags=re.S):
        t = html.unescape(re.sub(r'<[^>]+>', ' ', m)); t = re.sub(r'\s+', ' ', t).strip()
        if t: out.append(t)
    return out

def render_card(sec, bold):
    T = (lambda s: s) if bold else (lambda s: s.replace('**', ''))
    figs = {f['id']: f for f in sec.get('figures', [])}
    L = []
    def fig(fid):
        f = figs[fid]; svg = f.get('svgFile')
        L.append(f"[{'DIAGRAM' if svg else 'PHOTO'} {fid}] {T(f['title'])}")
        if svg:
            tx = svg_texts(svg)
            if tx: L.append('   (labels drawn inside the diagram: ' + ' | '.join(tx) + ')')
        for e in f.get('explain', []): L.append('   ' + T(e))
    for b in sec['body']:
        if 'box' in b:
            L.append(f"[BOX: {T(b['box'])}]")
            if 'p' in b: L.append('   ' + ' '.join(T(x) for x in b['p']))
            for x in b.get('list', []): L.append('   - ' + T(x))
            for i, x in enumerate(b.get('ol', []), 1): L.append(f'   {i}. ' + T(x))
            L.append('[END BOX]')
        elif 'h' in b: L.append('## ' + T(b['h']))
        elif 'p' in b: L.append(' '.join(T(x) for x in b['p']))
        elif 'list' in b: L.extend('- ' + T(x) for x in b['list'])
        elif 'ol' in b: L.extend(f'{i}. ' + T(x) for i, x in enumerate(b['ol'], 1))
        elif 'fig' in b: fig(b['fig'])
        elif 'gallery' in b:
            for fid in b['gallery']: fig(fid)
    return L

def pages(sec):
    p = sec.get('pages') or []
    return '' if not p else (f'p. {p[0]}' if p[0] == p[-1] else f'pp. {p[0]}-{p[-1]}')

def render_q(q, keys):
    T = lambda s: str(s).replace('**', '') if not keys else str(s)
    kind = {'mc': 'multiple choice', 'tf': 'true/false', 'short': 'short answer (student types a few words)'}[q['kind']]
    L = [f"--- Q {q['id']} [{kind}]" + (f" src={q['src']} style={q.get('style') or 'plain'}" + (' fixed-order' if q.get('fixed') else '') if keys else '')]
    L.append(T(q['q']))
    if q['kind'] == 'mc':
        for i, c in enumerate(q['choices']): L.append(f'   {LET[i]}) {T(c)}')
    if keys:
        if q['kind'] == 'mc': L.append(f"   KEY: {LET[q['answer']]}")
        elif q['kind'] == 'tf': L.append(f"   KEY: {'True' if q['answer'] else 'False'}")
        else:
            L.append(f"   KEY (canonical answer): {q['answer']}")
            L.append(f"   ACCEPT (other exact wordings): {json.dumps(q.get('accept', []), ensure_ascii=False)}")
            L.append(f"   KEYS (required points; each inner list = alternatives): {json.dumps(q.get('keys', []), ensure_ascii=False)}")
        L.append(f"   WHY: {q.get('why', '')}")
        L.append(f"   REF: {q.get('ref', '')}")
    return L

chunks, allq, chapters = [], {}, []
for f in sorted(glob.glob(str(REPO / 'content/chapters/ch*.json'))):
    ch = os.path.basename(f)[:-5]
    d = json.load(open(f, encoding='utf-8'))
    secs = d['sections']; chapters.append(ch)
    ctx = [f"CHAPTER TEXT: {secs[0]['chapter']} (all cards, no questions)", '']
    for s in secs:
        ctx.append(f"=== CARD {s['id']}: {s['title']} ({pages(s)}) ==="); ctx.extend(render_card(s, True)); ctx.append('')
        for q in s['questions']: allq[q['id']] = dict(q, sid=s['id'], chapter=ch, cardTitle=s['title'], cardPages=pages(s))
    (OUT / 'ctx' / f'{ch}.txt').write_text('\n'.join(ctx), encoding='utf-8')
    if ONLY is not None:
        secs = [s for s in secs if s['id'] in ONLY]
        if not secs: continue
    k = math.ceil(len(secs) / 9); base, extra = divmod(len(secs), k); i = 0
    for j in range(k):
        n = base + (1 if j < extra else 0); part = secs[i:i + n]; i += n
        cid = f'{PREFIX}{ch}-{j + 1}'
        for keys in (False, True):
            L = [f"{'AUDIT COPY (with answer keys)' if keys else 'QUIZ COPY (no answer keys)'}: {part[0]['chapter']}, cards {part[0]['id']} to {part[-1]['id']}", '']
            for s in part:
                L.append(f"=================== CARD {s['id']}: {s['title']} ({pages(s)}) ===================")
                L.append('CARD TEXT:'); L.extend(render_card(s, keys)); L.append('')
                L.append(f"QUESTIONS FOR CARD {s['id']}:")
                for q in s['questions']: L.extend(render_q(q, keys)); L.append('')
            (OUT / ('audit' if keys else 'solve') / f'{cid}.txt').write_text('\n'.join(L), encoding='utf-8')
        qids = [q['id'] for s in part for q in s['questions']]
        chunks.append({'id': cid, 'chapter': ch, 'cards': len(part), 'first': part[0]['id'], 'last': part[-1]['id'], 'questions': len(qids), 'short': sum(1 for q in qids if allq[q]['kind'] == 'short'), 'qids': qids})
json.dump(allq, open(OUT / 'data' / 'questions.json', 'w'), ensure_ascii=False)
json.dump(chunks, open(OUT / 'data' / 'chunks.json', 'w'), ensure_ascii=False)
print(len(chunks), 'chunks;', len(allq), 'questions')
for c in chunks: print(c['id'], c['cards'], 'cards', c['questions'], 'q', c['short'], 'short', os.path.getsize(OUT / 'audit' / (c['id'] + '.txt')) // 1024, 'KB')
print({ch: os.path.getsize(OUT / 'ctx' / (ch + '.txt')) // 1024 for ch in chapters}, 'ctx KB')
print('short per chapter', {ch: sum(1 for q in allq.values() if q['chapter'] == ch and q['kind'] == 'short') for ch in chapters})
