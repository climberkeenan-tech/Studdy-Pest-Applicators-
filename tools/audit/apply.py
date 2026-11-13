#!/usr/bin/env python3
"""Apply verified audit findings to content/chapters/*.json.

Usage: python3 apply.py <findings.json> [--write]
findings.json: list of {sec, q, cat, sev, problem, evidence, action, old, new, origin, verify, skeptic}
Without --write it is a dry run. Every change is checked before it is applied; anything unsafe or
unclear is skipped and listed for manual handling. Writes applied.json (what changed) next to this file.
"""
import collections
import glob
import json
import os
import pathlib
import re
import sys

REPO = pathlib.Path('/home/user/Studdy-Pest-Applicators-')
HERE = pathlib.Path(__file__).resolve().parent
LET = 'ABCDEF'
CONTENT_ACTIONS = {'set_answer', 'replace_choice', 'replace_stem', 'delete_question', 'replace_sentence'}
ORDER = ['replace_sentence', 'replace_stem', 'replace_choice', 'set_answer', 'set_short_grading', 'replace_why', 'replace_ref', 'delete_question']


def nws(s):
    return re.sub(r'\s+', ' ', str(s)).strip()


def loose(s):
    return nws(str(s).replace('**', '')).lower().rstrip('.')


class Book:
    def __init__(self):
        self.files = {}
        self.sec = {}
        self.q = {}
        for path in sorted(glob.glob(str(REPO / 'content/chapters/ch*.json'))):
            raw = open(path, encoding='utf-8').read()
            data = json.loads(raw)
            style = None
            for indent in (1, 2):
                for nl in ('', '\n'):
                    if json.dumps(data, ensure_ascii=False, indent=indent) + nl == raw:
                        style = (indent, nl)
            if style is None:
                raise SystemExit(f'{path}: unknown JSON formatting; normalize it first')
            self.files[path] = {'data': data, 'style': style, 'dirty': False}
            for s in data['sections']:
                self.sec[s['id']] = (path, s)
                for q in s['questions']:
                    self.q[q['id']] = (path, s, q)

    def touch(self, path):
        self.files[path]['dirty'] = True

    def save(self):
        n = 0
        for path, f in self.files.items():
            if f['dirty']:
                indent, nl = f['style']
                open(path, 'w', encoding='utf-8').write(json.dumps(f['data'], ensure_ascii=False, indent=indent) + nl)
                n += 1
        return n


def strings_of_section(s):
    """Yield (container, key) for every spoken/visible string in a section."""
    for b in s.get('body', []):
        for k in ('h', 'box'):
            if isinstance(b.get(k), str):
                yield b, k
        for k in ('p', 'list', 'ol'):
            if isinstance(b.get(k), list):
                for i in range(len(b[k])):
                    yield b[k], i
    for f in s.get('figures', []):
        if isinstance(f.get('title'), str):
            yield f, 'title'
        for i in range(len(f.get('explain', []))):
            yield f['explain'], i
    for t in s.get('terms', []):
        for k in ('term', 'def'):
            if isinstance(t.get(k), str):
                yield t, k
    if isinstance(s.get('title'), str):
        yield s, 'title'


def apply_one(book, f):
    """Return (status, message, record). status: applied | noop | skip."""
    action, old, new = f['action'], f.get('old') or '', f.get('new') or ''
    qid, sid = f.get('q') or '', f.get('sec') or ''
    path = s = q = None
    if qid:
        if qid not in book.q:
            return 'skip', f'unknown question {qid}', None
        path, s, q = book.q[qid]
    elif sid in book.sec:
        path, s = book.sec[sid]
    else:
        return 'skip', f'unknown card {sid}', None
    review = bool(q and q.get('src') == 'review')
    rec = {'q': qid, 'sec': s['id'], 'action': action}

    if action == 'set_answer':
        if not q:
            return 'skip', 'set_answer without a question', None
        if review:
            return 'skip', 'refused: review key is final (Appendix A)', None
        if q['kind'] == 'mc':
            m = re.match(r'^\(?([A-Fa-f])\)?(?:[\s.):]|$)', new.strip())
            if not m:
                return 'skip', f'cannot read new mc letter from {new!r}', None
            idx = LET.index(m.group(1).upper())
            if idx >= len(q['choices']):
                return 'skip', f'letter {m.group(1)} out of range', None
            if idx == q['answer']:
                return 'noop', 'key already that letter', None
            rec.update(before=f"{LET[q['answer']]}) {q['choices'][q['answer']]}", after=f"{LET[idx]}) {q['choices'][idx]}")
            q['answer'] = idx
        elif q['kind'] == 'tf':
            t = new.strip().lower()
            if not t or t[0] not in 'tf':
                return 'skip', f'cannot read true/false from {new!r}', None
            val = t[0] == 't'
            if val == q['answer']:
                return 'noop', 'key already that value', None
            rec.update(before=str(q['answer']), after=str(val))
            q['answer'] = val
        else:
            if not new.strip():
                return 'skip', 'empty new short answer', None
            if nws(new) == nws(q['answer']):
                return 'noop', 'same canonical answer', None
            rec.update(before=q['answer'], after=nws(new))
            q['answer'] = nws(new)
    elif action == 'replace_choice':
        if not q or q['kind'] != 'mc':
            return 'skip', 'replace_choice needs an mc question', None
        if review:
            return 'skip', 'refused: review choices stay as in the manual', None
        hits = [i for i, c in enumerate(q['choices']) if c == old] or [i for i, c in enumerate(q['choices']) if loose(c) == loose(old)]
        if len(hits) != 1:
            return 'skip', f'old choice matched {len(hits)} choices: {old!r}', None
        if not new.strip() or any(loose(c) == loose(new) for c in q['choices']):
            return 'skip', 'new choice empty or duplicates another choice', None
        rec.update(before=q['choices'][hits[0]], after=nws(new), wasKey=hits[0] == q['answer'])
        q['choices'][hits[0]] = nws(new)
    elif action == 'replace_stem':
        if not q:
            return 'skip', 'replace_stem without a question', None
        if review:
            return 'skip', 'refused: review stems stay as in the manual', None
        if old and loose(old) != loose(q['q']):
            return 'skip', 'old stem does not match the current stem', None
        if not new.strip() or nws(new) == q['q']:
            return 'noop', 'stem unchanged', None
        rec.update(before=q['q'], after=nws(new))
        q['q'] = nws(new)
    elif action == 'replace_why':
        if not q or not new.strip():
            return 'skip', 'replace_why needs a question and text', None
        if nws(new) == q.get('why'):
            return 'noop', 'why unchanged', None
        rec.update(before=q.get('why', ''), after=nws(new))
        q['why'] = nws(new)
    elif action == 'replace_ref':
        if not q or not new.strip():
            return 'skip', 'replace_ref needs a question and text', None
        if review and 'review question' in q.get('ref', '').lower() and 'review question' not in new.lower():
            return 'skip', 'refused: review ref must keep its "Review question N"', None
        rec.update(before=q.get('ref', ''), after=nws(new))
        q['ref'] = nws(new)
    elif action == 'set_short_grading':
        if not q or q['kind'] != 'short':
            return 'skip', 'set_short_grading needs a short question', None
        try:
            obj = json.loads(new)
        except Exception as e:
            return 'skip', f'fixNew is not JSON: {e}', None
        if not isinstance(obj, dict) or not set(obj) <= {'answer', 'accept', 'keys'} or not obj:
            return 'skip', 'fixNew must be an object with answer/accept/keys', None
        before = {k: q.get(k) for k in ('answer', 'accept', 'keys')}
        if 'answer' in obj and isinstance(obj['answer'], str) and obj['answer'].strip():
            q['answer'] = nws(obj['answer'])
        if 'accept' in obj and isinstance(obj['accept'], list):
            q['accept'] = [nws(x) for x in obj['accept'] if str(x).strip()]
        if 'keys' in obj and isinstance(obj['keys'], list):
            keys = [[nws(a) for a in ([g] if isinstance(g, str) else g) if str(a).strip()] for g in obj['keys']]
            keys = [g for g in keys if g]
            if keys:
                q['keys'] = keys
            else:
                q.pop('keys', None)
        after = {k: q.get(k) for k in ('answer', 'accept', 'keys')}
        if before == after:
            return 'noop', 'grading unchanged', None
        rec.update(before=before, after=after)
    elif action == 'delete_question':
        if not q:
            return 'skip', 'delete_question without a question', None
        if review:
            return 'skip', 'refused: review questions are never deleted', None
        if len(s['questions']) <= 3:
            return 'skip', 'card would drop below 3 questions', None
        rec.update(before=q['q'], after='(deleted)')
        s['questions'].remove(q)
    elif action == 'replace_sentence':
        if not old.strip() or not new.strip():
            return 'skip', 'replace_sentence needs old and new text', None
        slots = list(strings_of_section(s))
        exact = [(c, k) for c, k in slots if c[k] == old]
        part = [(c, k) for c, k in slots if old in c[k]]
        if len(exact) == 1:
            c, k = exact[0]
            rec.update(before=c[k], after=new.strip())
            c[k] = new.strip()
        elif len(part) == 1 and sum(c[k].count(old) for c, k in part) == 1:
            c, k = part[0]
            rec.update(before=c[k], after=c[k].replace(old, new.strip()))
            c[k] = c[k].replace(old, new.strip())
        else:
            return 'skip', f'old text matched {len(exact)} whole strings / {len(part)} partial in card {s["id"]}', None
        if rec['after'].count('**') % 2:
            return 'skip', 'replacement leaves unbalanced ** (reverted)', None
    else:
        return 'skip', f'action {action} is not automatic', None
    book.touch(path)
    return 'applied', '', rec


def eligible(f):
    """Policy: which findings may be applied automatically."""
    a = f['action']
    if a in ('none', 'needs_photo_check'):
        return False, 'manual: ' + a
    if f.get('skeptic') == 'refuted':
        return False, 'refuted by skeptic'
    if a in CONTENT_ACTIONS and f.get('skeptic') != 'upheld':
        return False, f"content change without an upheld skeptic check (skeptic={f.get('skeptic')})"
    if f.get('origin') == 'auditor' and f.get('verify') not in ('confirmed', 'modified') and f.get('skeptic') != 'upheld':
        return False, f"auditor finding not verified (verify={f.get('verify')})"
    return True, ''


def main():
    findings = json.load(open(sys.argv[1], encoding='utf-8'))
    write = '--write' in sys.argv
    book = Book()
    # de-duplicate identical fixes reported by both pipelines
    seen, uniq = set(), []
    for f in findings:
        key = (f.get('q') or f.get('sec'), f['action'], loose(f.get('old') or ''), loose(f.get('new') or ''))
        if key in seen:
            continue
        seen.add(key)
        uniq.append(f)
    # conflicts: two different new keys for one question, or delete + repair
    byq = collections.defaultdict(list)
    for f in uniq:
        if f.get('q'):
            byq[f['q']].append(f)
    conflict = set()
    for qid, fs in byq.items():
        ok = [f for f in fs if eligible(f)[0]]
        answers = {loose(f['new'])[:1] if (qid in book.q and book.q[qid][2]['kind'] != 'short') else loose(f['new']) for f in ok if f['action'] == 'set_answer'}
        if len(answers) > 1:
            conflict.add(qid)
        if any(f['action'] == 'delete_question' for f in ok) and any(f['action'] in ('set_answer', 'replace_choice', 'replace_stem') for f in ok):
            conflict.add(qid)
        stems = {loose(f['new']) for f in ok if f['action'] == 'replace_stem'}
        if len(stems) > 1:
            conflict.add(qid)
    applied, skipped, manual = [], [], []
    for f in sorted(uniq, key=lambda f: (f.get('sec') or '', f.get('q') or '', ORDER.index(f['action']) if f['action'] in ORDER else 99)):
        ok, why = eligible(f)
        if f.get('q') in conflict and f['action'] in CONTENT_ACTIONS:
            skipped.append((f, 'conflicting fixes for this question: resolve by hand'))
            continue
        if not ok:
            (manual if why.startswith('manual') else skipped).append((f, why))
            continue
        status, msg, rec = apply_one(book, f)
        if status == 'applied':
            rec.update(cat=f.get('cat'), sev=f.get('sev'), origin=f.get('origin'), problem=f.get('problem'))
            applied.append(rec)
        elif status == 'skip':
            skipped.append((f, msg))
    print(f'{len(findings)} findings, {len(uniq)} unique; applied {len(applied)}, skipped {len(skipped)}, manual {len(manual)}; conflicts on {len(conflict)} questions')
    by = collections.Counter(r['action'] for r in applied)
    print('applied by action:', dict(by))
    json.dump(applied, open(HERE / 'applied.json', 'w'), ensure_ascii=False, indent=1)
    json.dump([dict(f, skipReason=w) for f, w in skipped], open(HERE / 'skipped.json', 'w'), ensure_ascii=False, indent=1)
    json.dump([f for f, _ in manual], open(HERE / 'manual.json', 'w'), ensure_ascii=False, indent=1)
    if write:
        print('files written:', book.save())
    else:
        print('dry run: nothing written')


if __name__ == '__main__':
    main()
