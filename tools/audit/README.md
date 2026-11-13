# Content audit kit (as run on 2026-11-13)

A record of how the full content audit was run, kept so it can be repeated after new content is added.
These files are copied as they ran. They contain absolute paths from that session (the scratchpad
folder and the workflow transcript folder), so adjust the paths at the top of each file before reuse.

What the audit does:
1. `prep.py` renders every card into plain-text files, in chunks of up to 9 cards: a quiz copy without
   answer keys (`solve/`), an audit copy with keys (`audit/`), and the whole chapter text (`ctx/`).
2. `audit-study-content.workflow.js` is the Workflow script. Per chunk it runs:
   - a blind solver that answers every question from the card text alone, then an adjudicator that runs
     `compare.js` (solver answers against the key, typed answers through the page's own grader) and rules
     on each disagreement;
   - an auditor that checks key, single answer, answerability, explanation, reference and wording, then
     a verifier that re-judges every finding;
   - a skeptic that tries to refute every content-changing fix.
   Per chapter it also probes the typed-answer grader with right and wrong answers (`probe.js`),
   reviews screenshots of every figure (`shots.js` makes them), and, where the page photos are in the
   session, checks the card text against the photos.
3. `collect.py` rebuilds the merged findings from the workflow journals. `grader_fixes.py`,
   `select_fixes.py` and `evalshort.js` pick the fixes and test every proposed typed-answer grading
   against all probes. `apply.py` applies fixes with safety checks (never touches a review question's
   key, stem or choices). `handfix.py` holds hand-written rewrites.

Rules the reviewers worked under: read-only; the card text is the ground truth (never corrected from
outside knowledge); every finding needs an exact quote; review-question keys come from Appendix A and
are final.
