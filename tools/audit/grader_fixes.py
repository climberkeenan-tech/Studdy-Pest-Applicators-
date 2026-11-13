#!/usr/bin/env python3
"""Turn the grader agents' results into (1) findings for apply.py and (2) the raw probe list.

Usage: python3 grader_fixes.py   -> writes results/grader-findings.json and results/probes-all.json
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
res = json.load(open(HERE / 'results' / 'grader.json'))
Q = json.load(open(HERE / 'data' / 'questions.json'))
findings, probes, notes = [], [], []
for ch, r in sorted(res.items()):
    for q in r.get('questions', []):
        qid = q['id']
        if qid not in Q or Q[qid]['kind'] != 'short':
            notes.append(f'{qid}: not a short question, ignored')
            continue
        probes.append({'id': qid, 'right': q.get('rightProbes', []), 'wrong': q.get('wrongProbes', [])})
        if not q.get('changed'):
            continue
        obj = {}
        try:
            if q.get('acceptJson', '').strip():
                obj['accept'] = json.loads(q['acceptJson'])
            if q.get('keysJson', '').strip():
                obj['keys'] = json.loads(q['keysJson'])
        except Exception as e:
            notes.append(f'{qid}: could not parse proposed grading ({e})')
            continue
        if q.get('answer', '').strip():
            obj['answer'] = q['answer'].strip()
        if not obj:
            notes.append(f'{qid}: marked changed but no fields given')
            continue
        findings.append({'chunk': ch, 'sec': Q[qid]['sid'], 'q': qid, 'cat': 'short_grading', 'sev': 'medium',
                         'problem': (q.get('note') or 'grader probes') + (' | still failing: ' + q['remainingProblems'] if q.get('remainingProblems') else ''),
                         'evidence': '', 'action': 'set_short_grading', 'old': '', 'new': json.dumps(obj, ensure_ascii=False),
                         'origin': 'grader', 'verify': 'confirmed', 'skeptic': 'not_needed'})
json.dump(findings, open(HERE / 'results' / 'grader-findings.json', 'w'), ensure_ascii=False, indent=1)
json.dump(probes, open(HERE / 'results' / 'probes-all.json', 'w'), ensure_ascii=False, indent=1)
covered = {p['id'] for p in probes}
shorts = [k for k, v in Q.items() if v['kind'] == 'short']
print(f'{len(probes)} questions with probes ({sum(len(p["right"]) + len(p["wrong"]) for p in probes)} probes); {len(findings)} proposed grading changes')
print('short questions without probes:', [k for k in shorts if k not in covered])
for n in notes:
    print('note:', n)
