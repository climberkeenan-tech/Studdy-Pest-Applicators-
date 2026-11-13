#!/usr/bin/env python3
"""Build the final list of fixes to apply from the merged findings.

Usage: python3 select_fixes.py   -> writes results/apply-list.json and results/short-candidates.json
Policy decisions made by hand after reading the findings are encoded here.
"""
import collections
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
F = json.load(open(HERE / 'results' / 'findings.json'))
G = json.load(open(HERE / 'results' / 'grader-findings.json'))
P = {p['id']: p for p in json.load(open(HERE / 'results' / 'probes-all.json'))}
Q = json.load(open(HERE / 'data' / 'questions.json'))

# 1. explanations: skip pure "two sentences" style nits (two short sentences are fine by the user's rule)
nit = lambda f: (f['action'] == 'replace_why' and f['sev'] == 'low' and re.search(r'sentence', f['problem'], re.I)
                 and not re.search(r'letter|shuffl|contradict|not in the (card|text)|never|wrong|incorrect|position', f['problem'], re.I))
# 2. explanations I rewrite myself in handfix.py (letter/position references)
MINE = {'c01-s08-r1', 'c01-s11-r1', 'c01-s23-r1', 'c02-s02-r1', 'c02-s04-r1', 'c02-s07-r1', 'c08-s08-r4',
        'c10-s03-t1', 'c10-s09-t4', 'c11-s05-r1', 'c11-s08-r1', 'c11-s09-r1'}
# 3. where two reviewers proposed different wording for the same thing, keep this one
PREFER_NEW = {
    ('c03-s10-t3', 'replace_stem'): 'Which of these is NOT correct about the Spanish words that appear with signal words on a label?',
    ('c05-s06-t4', 'replace_choice'): 'Dermal and eye',
    ('c08-s04-t5', 'replace_stem'): 'Who does the manual say will give you any required placards?',
    ('c08-s09-t3', 'replace_stem'): 'Which of these is NOT something the manual says about a buildup of unwanted pesticides?',
    ('c08-s06-t3', 'replace_why'): 'The manual calls for cement or other impervious flooring and nonabsorbent shelving such as plastic or metal.',
    ('c03-s18-t1', 'replace_ref'): "Figure 3.1, sample pesticide label, p. 42, ingredient statement; p. 36, 'Ingredient Statement'",
    ('c10-s04-t1', 'replace_choice'): 'One-tenth full',
}
# 4. my own edit of a proposed text
EDIT_NEW = {
    ('c09-s04-r3', 'replace_why'): 'Installing a fire-detection system is in the list of precautions to reduce fire hazards. The sign appears only as a photo caption, and combustible pesticides are stored away from heat.',
}
# 5. not applied: the manual prints this wording (see CLAUDE.md, Chapter 4 notes); handled with a note in handfix.py
SKIP = {('c04-s01', 'replace_sentence')}

out, dropped = [], collections.Counter()
for f in F:
    k = (f['q'] or f['sec'], f['action'])
    if f['action'] in ('none', 'needs_photo_check'):
        continue
    if f['action'] == 'set_short_grading':
        continue                      # handled below with probes
    if nit(f):
        dropped['why sentence-count nit'] += 1; continue
    if f['action'] == 'replace_why' and f['q'] in MINE:
        dropped['why rewritten by hand'] += 1; continue
    if k in SKIP:
        dropped['kept as printed'] += 1; continue
    if k in PREFER_NEW and f['new'].strip() != PREFER_NEW[k]:
        dropped['other wording preferred'] += 1; continue
    if k in EDIT_NEW:
        f = dict(f, new=EDIT_NEW[k])
    out.append(f)

# short-answer grading: gather every proposal per question and let the probes decide
cands = collections.defaultdict(list)
for f in F:
    if f['action'] == 'set_short_grading':
        try:
            obj = json.loads(f['new'])
        except Exception:
            continue
        cands[f['q']].append(dict(obj, name=f['origin']))
for f in G:
    cands[f['q']].append(dict(json.loads(f['new']), name='grader'))
items = []
for qid, q in Q.items():
    if q['kind'] != 'short':
        continue
    pr = P.get(qid, {'right': [], 'wrong': []})
    items.append({'id': qid, 'right': pr['right'], 'wrong': pr['wrong'], 'candidates': [{'name': 'current'}] + cands.get(qid, [])})
json.dump(items, open(HERE / 'results' / 'short-candidates.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open(HERE / 'results' / 'apply-list.json', 'w'), ensure_ascii=False, indent=1)
print(len(out), 'non-grading fixes selected:', dict(collections.Counter(f['action'] for f in out)))
print('dropped:', dict(dropped))
print(len(items), 'short questions;', sum(1 for i in items if len(i['candidates']) > 1), 'with at least one proposed grading change')
