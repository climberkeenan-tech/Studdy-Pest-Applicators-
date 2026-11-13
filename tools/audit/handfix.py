#!/usr/bin/env python3
"""Hand-written fixes that the audit pointed to but that need my own wording.
Run AFTER apply.py. Each fix checks the current text first, so nothing is overwritten blindly.
Usage: python3 handfix.py [--write]
"""
import glob
import json
import re
import sys

REPO = '/home/user/Studdy-Pest-Applicators-'
WRITE = '--write' in sys.argv
LETTER = re.compile(r"(?:\b(?i:choices?|options?)\s+\(?[A-F]\)?(?![a-z])|\b[A-F]\)?,?\s+(?:and|or)\s+\(?[A-F]\b(?![a-z'])|(?:^|[.!?:]\s+)[A-F]\s+(?:is|are|was|has|describes?|says?)\b|(?:\bso|\bbut|\band|\bonly|\bsays)\s+[A-F]\b(?![a-z'°])|\b(?i:that|the) (?i:last|first|second|third|fourth) (?i:one|choice|option|answer|statement)\b)")

# Explanations that named shuffled choices by letter or position. New text restates the fact instead.
WHY = {
    'c01-s08-r1': 'Keeping native natural enemies healthy, for example with pollen and nectar plants, is part of biological control.',
    'c01-s11-r1': 'Cultural controls reduce pest establishment, reproduction, dispersal, and survival. The other two statements describe chemical control and biological control.',
    'c01-s23-r1': 'Continual use of pesticides from the same chemical class increases the likelihood of resistance.',
    'c02-s02-r1': 'States, tribes, and territories may set rules more, but not less, restrictive than FIFRA.',
    'c02-s04-r1': 'Certified applicators may use or supervise the use of restricted-use pesticides.',
    'c02-s07-r1': 'Registration rests on data showing no unreasonable risks. Tolerances allow some residue, so zero residue is not the purpose.',
    'c08-s08-r4': "This is the manual's Appendix A answer: water makes metal containers rust, so store pesticides on raised pallets or shelves.",
    'c10-s03-t1': 'A chemical reaction that produces new substances is chemical incompatibility. Failing to stay uniformly mixed is physical incompatibility.',
    'c10-s09-t4': 'Filling one-quarter full, recapping, and shaking for 10 seconds is small-container triple rinsing.',
    'c11-s05-r1': 'Pads make cleanup easier and must be impermeable. They belong where large quantities of pesticides are handled or mixed.',
    'c11-s08-r1': 'Nozzles control the amount applied and the pattern. Large droplets cut drift and small droplets maximize coverage, so the other two statements are backwards.',
    'c11-s09-r1': 'The manual states the drop spreader sentence word for word, and it lists ground speed as affecting the application rate.',
}
# Scenario stems that named things "A" and "B", which collides with the shuffled choice letters on screen.
RENAME = {
    'c05-s12-t1': [('Pesticide A', 'Pesticide X'), ('Pesticide B', 'Pesticide Y')],
    'c07-s02-t2': [('Product A', 'Product X'), ('Product B', 'Product Y')],
    'c07-s03-t3': [('Site A', 'Site X'), ('Site B', 'Site Y')],
}
# Chapter 1 wording restored from the page photos (found by the photo check).
SENT = [
    ('c01-s18',
     ['To justify the cost of control, pest populations must be large enough to cause significant damage.',
      'The **economic threshold (ET)** is the pest population density, the number of pests per unit area, at which control measures are needed to prevent the pest from reaching the economic injury level.'],
     ['To justify the cost of control, pest populations must be large enough to cause significant damage.',
      'This is called the **economic threshold (ET)**.',
      'The economic threshold is the pest population density, the number of pests per unit area, at which control measures are needed to prevent the pest from reaching the economic injury level.']),
    ('c01-s22',
     ['Under some conditions, pesticides can change into a form that is ineffective, due to the age of the product or the pesticide storage conditions.'],
     ['Under some conditions, pesticides can change into a form that is ineffective.',
      'This might be due to the age of the product or the pesticide storage conditions.']),
]

log = []
for path in sorted(glob.glob(REPO + '/content/chapters/ch*.json')):
    raw = open(path, encoding='utf-8').read()
    data = json.loads(raw)
    style = next(((i, nl) for i in (1, 2) for nl in ('', '\n') if json.dumps(data, ensure_ascii=False, indent=i) + nl == raw), None)
    assert style, path
    dirty = False
    for s in data['sections']:
        for sid, old, new in SENT:
            if s['id'] != sid:
                continue
            done = False
            for b in s['body']:
                for k in ('p', 'list'):
                    arr = b.get(k)
                    if not isinstance(arr, list):
                        continue
                    for i in range(len(arr) - len(old) + 1):
                        if arr[i:i + len(old)] == old:
                            arr[i:i + len(old)] = new
                            done = dirty = True
                            log.append(f'{sid}: restored manual wording ({len(old)} -> {len(new)} sentences)')
                            break
            if not done:
                log.append(f'{sid}: SENTENCES NOT FOUND (already changed?)')
        for q in s['questions']:
            qid = q['id']
            if qid in WHY:
                if q['kind'] == 'mc' and not q.get('fixed') and LETTER.search(q.get('why', '')):
                    log.append(f'{qid}: why  «{q["why"]}»  ->  «{WHY[qid]}»')
                    q['why'] = WHY[qid]
                    dirty = True
                else:
                    log.append(f'{qid}: why already free of letter references, left as is: «{q.get("why", "")}»')
            if qid in RENAME:
                for a, b in RENAME[qid]:
                    for field in ('q', 'why'):
                        if a in q.get(field, ''):
                            q[field] = q[field].replace(a, b); dirty = True
                    q['choices'] = [c.replace(a, b) for c in q['choices']]
                log.append(f'{qid}: renamed to X/Y -> {q["q"]} | {q["choices"]}')
                dirty = True
    if dirty and WRITE:
        indent, nl = style
        open(path, 'w', encoding='utf-8').write(json.dumps(data, ensure_ascii=False, indent=indent) + nl)

print('\n'.join(log))
# anything left that still names choices by letter or position?
left = []
for path in sorted(glob.glob(REPO + '/content/chapters/ch*.json')):
    for s in json.load(open(path, encoding='utf-8'))['sections']:
        for q in s['questions']:
            if q['kind'] == 'mc' and not q.get('fixed') and LETTER.search(q.get('why', '')):
                left.append((q['id'], q['why']))
print('\nstill naming choices by letter/position' + (' (before writing)' if not WRITE else '') + ':', left or 'none')
print('written' if WRITE else 'dry run')
