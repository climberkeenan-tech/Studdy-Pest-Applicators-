# Pest Applicator Study: session playbook

Live study page (artifact): https://claude.ai/artifact/1uWpmvZdD47qMje9MtvAE6
Republish to that URL every session. Never create a second artifact.

## Mission
The user is studying for a pesticide applicator license. Deadline: about **January 11, 2027**.
The license is required for a summer internship. Be blunt. If they fail, say so.

## Rules for every session (the user's own rules)
1. The user sends photos of manual pages. Work **only** from those pages.
   If a photo is blurry, cut off, or has glare, name the photo and ask for a retake.
   Never fill gaps from memory. If the pages do not say it, say so.
2. Break the pages into short sections: about 2 to 3 minutes of reading each
   (roughly 300 to 450 words, max 95 spoken lines).
3. Each section becomes a study card:
   - Text in short, plain sentences. Keep every fact, number, and term exactly as the manual has it.
   - Mark key terms with `**double asterisks**`.
   - Every picture or diagram: redraw it simply as SVG, or crop it from the photo if the photo file is on disk,
     or at minimum name the photo to look at. Always explain what it shows.
4. Quiz after each card, one question at a time:
   - First, the manual's own review questions that belong to this card (`"src": "review"`), in the manual's order.
   - Then 3 to 5 new test-style questions (`"src": "test"`), including at least one scenario question
     (`"style": "scenario"`) and one "which of these is NOT" question (`"style": "not"`) when the content allows.
5. Every question needs `ref`: where in the pages the answer is (page, heading, photo).
6. Pass = 100%. Misses come back later in the session and next session until right twice in a row.
   The page enforces this. Do not change that logic without the user asking.
7. Keep written explanations (`why`) to one short sentence.

## Files
- `content/study.json`: all manual content. The only file to edit when adding pages.
- `app/template.html`: the app (reader, quiz engine, progress). Content gets injected at `__CONTENT__`.
- `tools/build.py`: validates content and writes `dist/pest-study.html`. Fails on bad content.
- `photos/`: put the user's page photos here when they arrive as files, named `photo-01.jpg` and so on.

## Adding a batch of pages
1. Read every photo. Report any retakes needed before writing cards.
2. Append sections to `content/study.json` in manual order. Fill in `manual.title`, `state`, `category`,
   `totalPages` once the user says them (progress bar and daily pace depend on `totalPages`).
3. `python3 tools/build.py`
4. Publish: Artifact tool, `file_path: dist/pest-study.html`, `url: https://claude.ai/artifact/1uWpmvZdD47qMje9MtvAE6`.
   Omit `capabilities` and `icon` on redeploys (keeps tts, sample, db, user).
5. Commit and push to the working branch.

## Section schema
```json
{
  "id": "c01-s01",                       // stable forever; question stats are keyed on ids
  "chapter": "Chapter 1 · Pest Management",
  "title": "Short card title",
  "pages": [3, 4],                       // first and last manual page numbers
  "photos": ["Photo 1", "Photo 2"],
  "body": [
    {"h": "Heading from the manual"},
    {"p": ["Sentence one.", "Sentence two with a **key term**."]},
    {"list": ["Bullet one.", "Bullet two."]},
    {"fig": "fig-id"}
  ],
  "figures": [
    {"id": "fig-id", "title": "What the figure is", "photo": "Photo 2, bottom",
     "svg": "<svg viewBox=...>...</svg>",            // or "img": "data:image/jpeg;base64,..."
     "explain": ["What it shows, in one or two sentences."]}
  ],
  "terms": [{"term": "Term", "def": "Definition from the manual."}],
  "questions": [
    {"id": "c01-s01-r1", "src": "review", "kind": "mc", "q": "...", "choices": ["...", "..."], "answer": 0,
     "ref": "p. 4, Review question 1", "why": "..."},
    {"id": "c01-s01-t1", "src": "test", "kind": "mc", "style": "not", "q": "Which of these is NOT ...?",
     "choices": ["...", "...", "...", "..."], "answer": 2, "ref": "p. 3, 'Heading'", "why": "..."},
    {"id": "c01-s01-t2", "src": "test", "kind": "tf", "q": "...", "answer": false, "ref": "...", "why": "..."},
    {"id": "c01-s01-t3", "src": "test", "kind": "short", "q": "...", "answer": "canonical answer",
     "accept": ["other correct wordings"], "keys": [["required point", "or synonym"], ["second required point"]],
     "ref": "...", "why": "..."}
  ]
}
```
- `kind`: `mc` (answer = choice index), `tf` (answer = true/false), `short` (typed; graded by meaning,
  spelling ignored; Claude grades in the page when available, keyword match otherwise).
- Choices that mention other choices ("All of the above", "Both A and B") need `"fixed": true`
  so they are not shuffled. The build enforces this.
- SVG figures: use theme classes so they work in light and dark mode:
  `f-ink f-muted f-card f-field f-hi f-line f-ok f-bad f-on` (fills) and `s-ink s-field s-muted f-arrow` (strokes).
  Use `font-family="var(--f-display)"` for labels.

## How the page works (for reference)
- Claude voice through the artifact `tts` capability: Chrome or Edge on a computer, or the Claude desktop app.
  Not available in Safari, Firefox, or the Claude phone apps; there it falls back to the device voice.
- Yellow highlight: the current sentence is shaded, the current word is solid yellow.
  Sentence timing is exact; word position inside a sentence is estimated from speech time.
- Progress is saved per user in the artifact database (`data/users/<id>/profile`), mirrored in localStorage.
- Session: 5-question rapid round from studied cards (open misses first), next card, quiz, summary.
