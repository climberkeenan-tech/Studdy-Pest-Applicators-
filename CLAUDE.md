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

## Content audit (2026-11-13) and what is still open
A full audit ran over all 11 chapters (kit and method: `tools/audit/README.md`): every question was
re-answered without the key, wording and explanations were reviewed, the typed-answer grader was probed,
every figure was looked at, and Chapter 1 was compared with its page photos.
- **No wrong answer key was found** in 1,197 questions. Chapter 1 matches its photos (no wrong fact).
- Fixed: 16 questions reworded or given a new wrong choice, 24 explanations, 13 references, a few card
  sentences, 7 diagrams, and the typed-answer rules of 47 questions. A second pass over the 38 changed
  cards found no new answer problems.
- `tools/build.py` now fails if an explanation names a choice by letter or position ("so C is wrong",
  "that last one"): choices are shuffled on screen. Restate the fact instead.
- Short questions that ask for an order use `"ordered": true` (key groups must appear in order).
- Explanations may be two short sentences. Do not merge them into one long sentence.

**Open checks. These need the manual pages, which only the user has. Ask for these photos, then settle each:**
1. **Appendix A (p. 171 and the page after it).** Re-read every answer letter against
   `content/answer-key.json`. Chapter 8 question 4 matters most: the key is C ("Store metal pesticide
   containers on the higher shelves to prevent rusting"), but the card text supports choice A better.
   Also needs the Chapter 8 review page and pp. 126–128 (any sentence about metal containers, shelves, rust).
2. **Chapter 10, pp. 148–149**, "Cleaning and Disposing of Pesticide Containers": any sentence about
   puncturing rinsed containers, or disposing of containers under current regulations (`c10-s08-r1`
   cannot rule out choice A from the card text).
3. **Chapter 9, pp. 135–137 and p. 140**: a sentence about a detailed report of what took place before,
   during, and after the incident (`c09-s06-r1` is only loosely supported).
4. **Chapter 8, p. 124**, "Transport Vehicle": a sentence about enclosed or lockable cargo boxes giving
   the greatest protection (`c08-s02-r1`).
5. Chapter 6, p. 93: apron coverage, body text ("middle of the chest to the knees") against the photo
   caption ("from your neck to at least your knees").
6. Chapter 6, p. 100: does "PAPRs do not need a fit test" carry a qualifier such as "loose-fitting"?
7. Chapter 4, p. 49: "an organic solvent of mineral clay" or "or mineral clay" (the card keeps "of" and notes it).
8. Chapter 4, p. 54, "Liquid Baits": "Most liquid insecticides" or "Most liquid insecticide baits".
9. Chapter 3, p. 33: "and a number of required applications" or "and number of required applications".
10. Chapter 3, p. 42 (Figure 3.1): the Spanish sentence ("para que se la explique"?) and the product
    names "VIP No Pest Gel", "VIP Pest-No", "VIP No Pest".
11. Chapter 2, p. 23: "Cosmetic" or "Cosmetics" in the act's name, and the FQPA sentence.
12. Chapter 8, pp. 130–131: which page holds the box "Steps to Prevent Security Problems"
    (`c08-s12-t1` says p. 131, `c08-s12-t4` says p. 130).
13. Chapter 2, p. 20 (restricted-use label photo): the sentence "For retail sale and use only by certified
    applicators or persons under the direct supervision of and only for those uses..." reads as if words
    were dropped. Retype it word for word.
14. Chapter 4, p. 64, "Types of Adjuvants": "Spreader" or "Spreaders", "allow" or "allows".
Photo crops that would be better re-cropped from fresh photos (all minor): `p22-24c-label`, `p20-epa-seal`,
`p57-dust`, `p98-halfface`, `p100-sealcheck`, `p100-wash`, `p125-spillkit`, `p126-shed`, `p124-passenger`,
`p148-triplerinse`.

## Recorded narration (the natural voice)
The user heard a robotic voice and had to tap to start each sentence: the Claude voice (`tts`) is not offered
in Safari, Firefox, the Claude phone apps, desktop pop-out windows or the Code tab's artifact pane, so the page
fell back to the device voice. Since 2026-11-14 every card has narration recorded ahead of time, and the page
plays that everywhere. A card starts reading when it opens. Do not remove this.

- **Voices in the page** (`app/template.html`, the "reader" block): `rec` (the recording), `claude` (live `tts`),
  `device` (speechSynthesis). "Best available" uses the Claude voice where it is offered, else the recording,
  else the device voice. With "Keep going to the next card" on, it prefers the recording (no hourly limit,
  keeps playing with the screen off). The recording plays from one shared audio element; if that fails it
  tries a fetched copy, then Web Audio, then the next voice, and says why in the voice note.
  If the viewer turned reading aloud off (`not_granted`), nothing speaks unless they pick the recording themselves.
- **Recording** (`tools/narrate.py`): Kokoro TTS, voice `af_heart`, on the CPU. All 221 cards are 8.2 hours
  of audio and 148 MB; about 90 minutes on 4 cores.
  - Once per container: `python3 tools/narrate.py --setup` (Python 3.12 venv, model and word lists, about 700 MB;
    needs `ffmpeg`). It prints the venv's python. `$NARRATE_HOME` moves the cache (default `~/.cache/pest-study-tts`).
  - `<venv python> tools/narrate.py` records every card that is missing or whose text or pronunciation changed.
    `--list` shows what is out of date. `--cards c01-s03 --force` records chosen cards again.
  - Output: `dist/audio/<card>.mp3` (not in git) and `content/narration.json` (in git). Per card: `h` hash of the
    card's sentences, `r` hash of what was asked of the voice (text after the pronunciation rules, voice,
    settings: a change means record again), `p` names the published file (it also covers the timings that came
    out, so a card recorded again gets a new name), `d` length in ms, `t` start and end of each sentence,
    `w` start of each word in each sentence. One recording run at a time (it takes a lock).
  - Pronunciation: `say()`, `PHONEMES` (acronyms), `TERMS` (words the engine gets wrong), `CONTEXT` (a word with
    two pronunciations, fixed for one sentence), `SPANISH`. `--say "text"` shows how a sentence will be read.
    `--words` lists every word the engine had to guess. Check both after adding cards with new terms.
    `python3 tools/narrate.py --check` runs `tools/say_cases.json` (sentences and how the rules must respell
    them; needs no model). Run it after touching the rules, and add a case for each new rule.
- **Build**: `tools/build.py` puts the timing of every recording that still matches its card into the page
  (`C.narration`) and warns about cards with no current recording. Those cards still work: the page reads them
  with a live voice until they are recorded.
- **Publishing audio**: the MP3s are supporting files of the artifact, named `audio/<card>.<p>.mp3`.
  `<venv python> tools/narrate.py --files 55` prints the Artifact `files` maps in batches under 55 MB (a publish
  takes at most 64 MB and 255 files). Publish the page once per batch with that map as `files`. Files already
  published stay. A card recorded again gets a new name: remove the old one with `"audio/<old name>": null`
  (Artifact `action: "list"`, `scope: "files"` shows what is published).
- **After changing a card's text**: build, record, build again, `node tools/check_narration.js`, publish the page
  with the new audio file, remove the old file.
- **Listening check** (`tools/listen.py`): nobody can proof-listen 8 hours of audio, and Claude cannot hear at
  all. A speech recogniser hears every recorded sentence and the result is compared with the card by sound.
  `<venv python> tools/listen.py --setup` once (about 700 MB), then `<venv python> tools/listen.py`
  (`--cards c08-s04` for a few cards; for everything, four `--shard K/4 --threads 1` runs side by side take
  about 25 minutes, then `--report`). Run it after recording new cards. The report has three parts:
  - Sentences that differ from the card. A sentence that differs is heard a second time on a wider cut first,
    because the recogniser now and then drops a word that is in the audio (an acronym in brackets, the first or
    last word, once a whole sentence).
  - Near matches where a whole word was not heard, or a word was heard that the card does not have.
  - Numbers: the digits heard against the digits on the card ("fifteen" for "fifty" is one sound, so the first
    part would miss it).
  A flag is a lead, not proof: the recogniser mishears rare words (ovicides, galactothion) and writes numbers
  its own way ("Class I", "Chapter X").
  **Result on 2026-11-14, all 221 recordings, 4,718 sentences:** 0.18% of sounds differ. 6 sentences flagged
  (phone and registration numbers, the sample label's chemical name), 16 near matches (a bracketed acronym or
  the first or last word), no extra words, 5 of 584 numbered sentences with different digits (all the
  recogniser's spelling). Every one of these was then checked word by word (loudness and length of the word in
  the audio, narrow cuts around it, and a second recogniser, Whisper small): each word is there. No dropped,
  garbled, repeated or wrong word was found. What this cannot judge is how natural the voice sounds.
- **The recordings exist only on the artifact** (and in this container until it is reclaimed). If they are lost,
  `narrate.py` makes them again from the content.

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
7. Keep written explanations (`why`) short: one or two short sentences. Never name a choice by its letter.

## Files
- `content/study.json`: manual metadata and the practice card.
- `content/answer-key.json`: Appendix A answers to the review questions, by chapter.
- `content/chapters/chNN.json`: `{"chapter", "pages", "sections": [...]}` for each chapter, merged in file-name order.
- `content/figures/*.svg`: diagrams. Referenced from a figure as `"svgFile": "fig-1-1.svg"`.
- `content/images/*.jpg`: photo crops. Referenced as `"imgFile": "p4-thistle.jpg"`.
- `app/template.html`: the app (reader, quiz engine, grader, progress). Content gets injected at `__CONTENT__`.
- `tools/build.py`: validates content, inlines figures and images, writes `dist/pest-study.html`. Fails on bad content.
- `tools/check_grader.js` + `tools/grader_cases.json`: regression test for typed-answer grading.
- `content/narration.json`: timing of the recorded narration (written by `tools/narrate.py`, read by the build).
- `tools/narrate.py`: records the narration and holds the pronunciation rules. `dist/audio/*.mp3` is its output (not in git).
- `tools/check_narration.js`: the page and `narrate.py` must split every card into the same sentences and words.
- `tools/say_cases.json`: regression cases for the pronunciation rules (`python3 tools/narrate.py --check`).
- `tools/listen.py`: listening check for the recordings (speech recogniser; optional, large download).
- `tools/crop_photos_chNN.py`, `tools/fig_1_4.py`, `tools/fig_9_1.py`: how the photo crops and two figures were made.
- `tools/retired/`: retired one-time chapter generators. Do not run.
- `tools/audit/`: the content audit kit as it ran (see its README).
- Uploaded photos arrive under `/root/.claude/uploads/<session>/`. Crop them WITHOUT applying EXIF rotation:
  the raw pixel orientation matches what is shown in the conversation. Do not commit the full photos.

## Adding a batch of pages
1. Read every photo. Report any retakes needed before writing cards. Zoom (crop + enlarge) on any small
   or angled text before trusting a number.
2. Write or extend `content/chapters/chNN.json` in manual order. Fill in `manual.totalPages` once known
   (the progress bar and daily pace depend on it).
3. `python3 tools/build.py`, then `node tools/check_grader.js`
4. Record the new cards (see "Recorded narration"), build again, then `node tools/check_narration.js`.
5. Publish: Artifact tool, `file_path: dist/pest-study.html` (same path keeps the URL; from a new
   conversation pass `url: https://claude.ai/artifact/1uWpmvZdD47qMje9MtvAE6`), with the new audio as `files`.
   Omit `capabilities` and `icon` on redeploys (keeps tts, sample, db, user).
6. Commit and push to the working branch.

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
- Voices: see "Recorded narration". The Claude voice (`tts`) works in Chrome or Edge on a computer and in the
  Claude desktop app's main window. Everywhere else the page plays the recording.
- Yellow highlight: the current sentence is shaded, the current word is solid yellow. With the recording both
  are exact (the model reports when each sound is spoken). With the live voices the word is estimated.
- A card starts reading when it is opened ("Read to me when a card opens"). "Keep going to the next card" opens
  the next card and reads it when one ends. Both are settings in the voice bar, saved with the profile.
- Progress is saved per user in the artifact database (`data/users/<id>/profile`), mirrored in localStorage.
  The page never writes to the account before it has read it (`loaded`, `P.base` in `app/template.html`).
  Keep that guard: without it a visit that could not read the saved copy overwrote it with an empty one.
- Session: 5-question rapid round from studied cards (open misses first), next card, quiz, summary.
