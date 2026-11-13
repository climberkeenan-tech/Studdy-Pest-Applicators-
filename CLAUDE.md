# Pest Applicator Study: session playbook

Live study page (artifact): https://claude.ai/artifact/1uWpmvZdD47qMje9MtvAE6
Republish to that URL every session. Never create a second artifact.

## Mission
The user is studying for a pesticide applicator license. Deadline: about **January 11, 2027**.
The license is required for a summer internship. Be blunt. If they fail, say so.

Manual: **Pennsylvania Pesticide Applicator Certification Core Manual**, Second Edition, 2014
(Penn State Extension, Pesticide Education Program). Exam: Core. 11 chapters, pp. 1–169; Appendix A from p. 171.

The user is in Pennsylvania and is studying for the **Core** exam only, for now.
Pennsylvania Core exam (per a search summary of the PA Dept. of Agriculture page, which this
session's network could not open directly): 50 multiple-choice questions, 35 correct (70%) to pass.

## Status: all 11 chapters are in
The manual has 11 chapters; Appendix A (the answer key) starts at p. 171. Everything is built:
220 cards, 1,197 questions (93 of them the manual's own review questions). `content/study.json` has
`"complete": true`, so the home page groups cards by chapter and shows a cards-per-day pace.
The default branch `claude/zen-feynman-sp8nec` holds everything. The older per-chapter session
branches (`claude/*`) are fully merged into it and can be ignored.

- **Source of truth: `content/chapters/chNN.json`. Edit the JSON directly.** The one-time generators that
  first typed Chapters 3, 4, 6, 8 and 10 are retired in `tools/retired/` (they exit at once; rerunning them
  would undo later fixes).
- **Appendix A answer key** is in `content/answer-key.json`. `tools/build.py` fails if any review question's
  answer disagrees with it. Review choices must stay in the manual's A, B, C order (index 0 = A). The question
  number comes from "Review question N" in the `ref`, or else from the id's `-rN` suffix. All 93 match.
  Never change a review question's key, stem, or choices.
- **Typed-answer grading tests:** `node tools/check_grader.js` runs `tools/grader_cases.json` (right answers
  that must pass, wrong answers that must fail) against the grader in `app/template.html`. Run it after
  changing any short-answer question or the grader. Add cases when adding short-answer questions.
- Uploaded page photos live only in the session that received them. Only Chapter 1's photos were
  available when the content audit ran, so only Chapter 1 has been re-checked against its photos.

| Ch | Title | Pages (review) | Cards | Notes |
|---|---|---|---|---|
| 1 | Pest Management | 1–15 (17–18) | 25 | Figures 1.1–1.4 redrawn; `tools/fig_1_4.py` |
| 2 | Federal Pesticide Laws and Regulations | 19–28 (29) | 15 | p. 28 holds only the last 5 lines of the summary |
| 3 | Pesticide Labeling | 31–45 (47) | 25 | Cards 18–21 type out Figure 3.1 (sample label, p. 42). p. 46 not sent (likely blank) |
| 4 | Pesticide Formulations | 49–66 (67) | 26 | p. 49 prints "an organic solvent of mineral clay" (typed as printed). p. 66 number inferred |
| 5 | Pesticide Hazards and First Aid | 69–85 (87–88) | 31 | Figure 5.1 as a bar chart, Table 5.1 as `tab-5-1.svg`. p. 86 not sent |
| 6 | Personal Protective Equipment | 89–102 (103) | 21 | Figure 6.1 bar heights read off the chart. "Rinse and slash used gloves" (p. 95) typed as printed. p. 102 number inferred |
| 7 | Pesticides in the Environment | 105–120 (121) | 23 | Table 7.1 prints "Extra Course"; the card says Extra Coarse and notes it. p. 120 number inferred |
| 8 | Transportation, Storage, and Security | 123–131 | 13 | The user called these pages "Chapter 7"; the photos say Chapter 8. p. 131 number inferred |
| 9 | Emergency or Incident Response | 135–140 (141) | 8 | `tools/fig_9_1.py`. NFPA diamond: the drawing says "reactivity", the box text says "instability" |
| 10 | Planning the Pesticide Application | 143–154 (155–156) | 17 | Diagrams `fig-10-jar.svg`, `fig-10-sump.svg` |
| 11 | Pesticide Application Procedures | 157–168 (169) | 16 | Figure 11.1 (nozzle patterns) is a photo crop with every label typed into `explain` |

Photo crops: `tools/crop_photos_chNN.py` (Chapters 7 to 11 are grayscale because those photos had a purple cast).

## Rules for every session (the user's own rules)
1. The user sends photos of manual pages. Work **only** from those pages.
   If a photo is blurry, cut off, or has glare, name the photo and ask for a retake.
   Never fill gaps from memory. If the pages do not say it, say so.
2. Break the pages into short sections: about 2 to 3 minutes of reading each
   (roughly 250 to 420 words, max 95 spoken lines).
3. Each section becomes a study card:
   - **Type the actual text in.** The user explicitly does not want "look at your photo" or screenshots
     of text. Short, plain sentences. Keep every fact, number, and term exactly as the manual has it.
   - Mark key terms with `**double asterisks**`. Avoid "e.g." and "vs." in sentences (they are read aloud);
     write "for example" and "versus".
   - Manual boxes (green boxes with lists) become `box` blocks. Numbered boxes use `ol`.
   - Diagrams: redraw as SVG with real text labels in `content/figures/`. Explain what each shows.
   - Photographs (insects, weeds, equipment): crop them from the user's photo into `content/images/`
     and use the manual's caption text as the title.
4. Quiz after each card, one question at a time:
   - First, the manual's own review questions that belong to this card (`"src": "review"`), in the manual's order.
   - Then 3 to 5 new test-style questions (`"src": "test"`), including at least one scenario question
     (`"style": "scenario"`) and one "which of these is NOT" question (`"style": "not"`) when the content allows.
5. Every question needs `ref`: where in the pages the answer is (page and heading).
6. Pass = 100%. Misses come back later in the session and next session until right twice in a row.
   The page enforces this. Do not change that logic without the user asking.
7. Keep written explanations (`why`) to one short sentence.

## Files
- `content/study.json`: manual metadata and the practice card.
- `content/answer-key.json`: Appendix A answers to the review questions, by chapter.
- `content/chapters/chNN.json`: `{"chapter", "pages", "sections": [...]}` for each chapter, merged in file-name order.
- `content/figures/*.svg`: diagrams. Referenced from a figure as `"svgFile": "fig-1-1.svg"`.
- `content/images/*.jpg`: photo crops. Referenced as `"imgFile": "p4-thistle.jpg"`.
- `app/template.html`: the app (reader, quiz engine, grader, progress). Content gets injected at `__CONTENT__`.
- `tools/build.py`: validates content, inlines figures and images, writes `dist/pest-study.html`. Fails on bad content.
- `tools/check_grader.js` + `tools/grader_cases.json`: regression test for typed-answer grading.
- `tools/crop_photos_chNN.py`, `tools/fig_1_4.py`, `tools/fig_9_1.py`: how the photo crops and two figures were made.
- `tools/retired/`: retired one-time chapter generators. Do not run.
- Uploaded photos arrive under `/root/.claude/uploads/<session>/`. Crop them WITHOUT applying EXIF rotation:
  the raw pixel orientation matches what is shown in the conversation. Do not commit the full photos.

## Adding a batch of pages
1. Read every photo. Report any retakes needed before writing cards. Zoom (crop + enlarge) on any small
   or angled text before trusting a number.
2. Write or extend `content/chapters/chNN.json` in manual order. Fill in `manual.totalPages` once known
   (the progress bar and daily pace depend on it).
3. `python3 tools/build.py`, then `node tools/check_grader.js`
4. Publish: Artifact tool, `file_path: dist/pest-study.html` (same path keeps the URL; from a new
   conversation pass `url: https://claude.ai/artifact/1uWpmvZdD47qMje9MtvAE6`).
   Omit `capabilities` and `icon` on redeploys (keeps tts, sample, db, user).
5. Commit and push to the working branch.

## Section schema
```json
{
  "id": "c01-s01",                       // stable forever; question stats are keyed on ids
  "chapter": "Chapter 1 · Pest Management",
  "title": "Short card title",
  "pages": [3, 4],                       // first and last manual page numbers
  "body": [
    {"h": "Heading"},
    {"p": ["Sentence one.", "Sentence two with a **key term**."]},
    {"list": ["Bullet one.", "Bullet two."]},
    {"ol": ["Step one.", "Step two."]},
    {"box": "Box title from the manual", "p": ["..."], "list": ["..."], "ol": ["..."]},
    {"fig": "fig-1-1"},
    {"gallery": ["p4-thistle", "p4-wasp"]}
  ],
  "figures": [
    {"id": "fig-1-1", "title": "Figure 1.1: Biomagnification in the food chain", "page": "p. 3",
     "svgFile": "fig-1-1.svg", "explain": ["What it shows, in one or two sentences."]},
    {"id": "p4-thistle", "title": "Weed pest: Canada thistle flowers.", "page": "p. 4", "imgFile": "p4-thistle.jpg"}
  ],
  "questions": [
    {"id": "c01-s01-r1", "src": "review", "kind": "mc", "q": "...", "choices": ["...", "..."], "answer": 0,
     "ref": "p. 16, Review question 1", "why": "..."},
    {"id": "c01-s01-t1", "src": "test", "kind": "mc", "style": "not", "q": "Which of these is NOT ...?",
     "choices": ["...", "...", "...", "..."], "answer": 2, "ref": "p. 3, 'Heading'", "why": "..."},
    {"id": "c01-s01-t2", "src": "test", "kind": "tf", "q": "...", "answer": false, "ref": "...", "why": "..."},
    {"id": "c01-s01-t3", "src": "test", "kind": "short", "q": "...", "answer": "canonical answer",
     "accept": ["other correct wordings"], "keys": [["required point", "or synonym"], ["second required point"]],
     "ref": "...", "why": "..."}
  ]
}
```
- `kind`: `mc` (answer = choice index), `tf` (answer = true/false), `short` (typed, graded by meaning,
  spelling ignored). Short answers: the page first checks locally (with `keys`, every key group must
  appear; typos allowed, but "vertebrates" never matches "invertebrates"), and asks Claude when the
  local check fails. Test new short questions with realistic right and wrong answers.
- Choices that mention other choices ("All of the above", "Both A and B") need `"fixed": true`.
- Every spoken sentence is a line for the voice; figure titles and `explain` lines are read too.
- SVG figures: use theme classes so they work in light and dark mode:
  `f-ink f-muted f-card f-field f-hi f-line f-ok f-bad f-on` (fills) and `s-ink s-field s-muted f-arrow` (strokes).
  Use `font-family="var(--f-display)"` or `var(--f-body)` for labels. Give `<marker>` ids a unique suffix.

## How the page works (for reference)
- Claude voice through the artifact `tts` capability: Chrome or Edge on a computer, or the Claude desktop app.
  Not available in Safari, Firefox, or the Claude phone apps; there it falls back to the device voice.
- Yellow highlight: the current sentence is shaded, the current word is solid yellow.
  Sentence timing is exact; word position inside a sentence is estimated from speech time.
- Progress is saved per user in the artifact database (`data/users/<id>/profile`), mirrored in localStorage.
- Session: 5-question rapid round from studied cards (open misses first), next card, quiz, summary.
