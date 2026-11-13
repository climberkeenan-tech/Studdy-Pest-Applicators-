#!/usr/bin/env python3
"""Rebuild the merged audit results from the workflow journals (same merge rules as the workflow script).

Usage: python3 collect.py            -> writes results/*.json and prints a summary
"""
import collections
import glob
import json
import os
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
WF = pathlib.Path('/root/.claude/projects/-home-user-Studdy-Pest-Applicators-/60eedd49-8ed0-5a31-9e3d-e8100822f80a/subagents/workflows')
OUT = HERE / 'results'
OUT.mkdir(exist_ok=True)
CONTENT_ACTIONS = {'set_answer', 'replace_choice', 'replace_stem', 'delete_question', 'replace_sentence'}
chunks = json.load(open(HERE / 'data' / 'chunks.json'))


def needs_skeptic(f):
    return f['fixAction'] in CONTENT_ACTIONS or (f['severity'] == 'high' and f['fixAction'] not in ('needs_photo_check', 'none'))


def first_prompt(run, aid):
    p = WF / run / f'agent-{aid}.jsonl'
    if not p.exists():
        return ''
    out = []
    with open(p, encoding='utf-8') as fh:
        for i, line in enumerate(fh):
            if i > 6:
                break
            try:
                row = json.loads(line)
            except Exception:
                continue
            m = row.get('message') or {}
            if m.get('role') != 'user':
                continue
            c = m.get('content')
            if isinstance(c, str):
                out.append(c)
            elif isinstance(c, list):
                out.extend(x.get('text', '') for x in c if isinstance(x, dict) and x.get('type') == 'text')
    return '\n'.join(out)


agents = {}          # label -> list of results (latest last)
skeptics = {}        # (sec, q, action, old, new) -> verdict
pending = collections.Counter()
for run in sorted(os.listdir(WF)):
    jp = WF / run / 'journal.jsonl'
    if not jp.exists():
        continue
    rows = [json.loads(l) for l in open(jp, encoding='utf-8') if l.strip()]
    started = {r['agentId']: r for r in rows if r['type'] == 'started'}
    done = {r['agentId']: r for r in rows if r['type'] == 'result'}
    for aid, s in started.items():
        if aid not in done:
            pending[s['phase']] += 1
            continue
        res = done[aid].get('result')
        label = s['label']
        if label.startswith('skeptic:'):
            txt = first_prompt(run, aid)
            m = re.search(r'Proposed fix: action=(\w+)\s*\n\s*old: (.*)\n\s*new: (.*)', txt)
            c = re.search(r'The change concerns (?:question (\S+)|the card text) in card (\S+?)\.\s', txt)
            if not m or not c or not res:
                continue
            try:
                old, new = json.loads(m.group(2).strip()), json.loads(m.group(3).strip())
            except Exception:
                continue
            skeptics[(c.group(2), c.group(1) or '', m.group(1), old, new)] = res
        elif res is not None:
            agents.setdefault(label, []).append(res)


def last(label):
    v = agents.get(label)
    return v[-1] if v else None


def with_skeptic(f, origin):
    f = dict(f, origin=origin)
    if not needs_skeptic(f):
        f['skeptic'] = 'not_needed'
        return f
    v = skeptics.get((f['sectionId'], f['questionId'] or '', f['fixAction'], f['fixOld'], f['fixNew']))
    if not v:
        f['skeptic'] = 'unavailable'
        return f
    if v.get('refuted'):
        f.update(skeptic='refuted', skepticReason=v.get('reason', ''))
        return f
    f.update(skeptic='upheld', skepticReason=v.get('reason', ''))
    if v.get('betterAction'):
        f.update(fixAction=v['betterAction'], fixOld=v.get('betterOld', ''), fixNew=v.get('betterNew', ''), adjustedBySkeptic=True)
    return f


all_findings, dropped, status = [], [], []
solver_stats = collections.Counter()
for c in chunks:
    cid = c['id']
    row = {'chunk': cid}
    solve = last('solve:' + cid)
    if solve:
        row['answers'] = len(solve.get('answers', []))
        for a in solve.get('answers', []):
            solver_stats[a.get('supported')] += 1
        json.dump(solve, open(HERE / 'out' / f'solve-{cid}.collected.json', 'w'), ensure_ascii=False)
    adj = last('adjudicate:' + cid)
    if adj:
        row['disputes'] = adj.get('disputes')
        fs = [with_skeptic(f, 'solver') for f in adj.get('findings', [])]
        row['solverFindings'] = len(fs)
        all_findings += [dict(f, chunk=cid) for f in fs]
    aud = last('audit:' + cid)
    if aud:
        row['checked'] = aud.get('checked')
        fs = aud.get('findings', [])
        row['auditRaw'] = len(fs)
        if fs:
            ver = last('verify:' + cid)
            if ver is None:
                row['verify'] = 'pending'
                kept = [dict(f, verify='unverified') for f in fs]
            else:
                by_n = {v['n']: v for v in ver.get('verdicts', [])}
                kept = []
                for n, f in enumerate(fs):
                    v = by_n.get(n)
                    if not v:
                        kept.append(dict(f, verify='unverified'))
                        continue
                    if v['verdict'] == 'refuted':
                        dropped.append(dict(f, chunk=cid, verifyReason=v.get('reason', '')))
                        continue
                    g = dict(f, verify=v['verdict'], verifyReason=v.get('reason', ''))
                    for k in ('fixAction', 'fixOld', 'fixNew'):
                        if v.get(k):
                            g[k] = v[k]
                    kept.append(g)
            row['auditKept'] = len(kept)
            all_findings += [dict(with_skeptic(f, 'auditor'), chunk=cid) for f in kept]
    status.append(row)

slim = [{'chunk': f['chunk'], 'sec': f['sectionId'], 'q': f['questionId'], 'cat': f['category'], 'sev': f['severity'], 'problem': f['problem'],
         'evidence': f['evidence'], 'action': f['fixAction'], 'old': f['fixOld'], 'new': f['fixNew'], 'origin': f['origin'],
         'verify': f.get('verify', ''), 'verifyReason': f.get('verifyReason', ''), 'skeptic': f['skeptic'], 'skepticReason': f.get('skepticReason', '')} for f in all_findings]
json.dump(slim, open(OUT / 'findings.json', 'w'), ensure_ascii=False, indent=1)
json.dump(dropped, open(OUT / 'dropped-by-verifier.json', 'w'), ensure_ascii=False, indent=1)
for kind in ('grader', 'figures', 'photos'):
    res = {lab.split(':', 1)[1]: v[-1] for lab, v in agents.items() if lab.startswith(kind + ':')}
    json.dump(res, open(OUT / f'{kind}.json', 'w'), ensure_ascii=False, indent=1)

print('pending agents by phase:', dict(pending))
done_chunks = sum(1 for r in status if 'disputes' in r and 'checked' in r and r.get('verify') != 'pending')
print(f'chunks with both pipelines reported: {done_chunks}/{len(chunks)}')
print('solver answers by support:', dict(solver_stats), '| disputes total:', sum(r.get('disputes') or 0 for r in status))
print('findings:', len(slim), '| by skeptic:', dict(collections.Counter(f['skeptic'] for f in slim)), '| dropped by verifier:', len(dropped))
print('by category:', dict(collections.Counter(f['cat'] for f in slim if f['skeptic'] != 'refuted')))
print('by action:', dict(collections.Counter(f['action'] for f in slim if f['skeptic'] != 'refuted')))
print('by severity:', dict(collections.Counter(f['sev'] for f in slim if f['skeptic'] != 'refuted')))
for kind in ('grader', 'figures', 'photos'):
    print(kind, 'reports:', sorted(json.load(open(OUT / f'{kind}.json')).keys()))
missing = [r['chunk'] for r in status if not ('disputes' in r and 'checked' in r)]
if missing:
    print('chunks still missing a pipeline:', missing)
