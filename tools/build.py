#!/usr/bin/env python3
"""Validate content and build dist/pest-study.html.

Content layout:
  content/study.json           manual metadata + the practice card
  content/chapters/chNN.json   {"sections": [...]} for each chapter, merged in file-name order
  content/figures/*.svg        diagrams, referenced from a figure as "svgFile": "fig-1-1.svg"
  content/images/*.jpg|png     photo crops, referenced as "imgFile": "p4-thistle.jpg"

Usage: python3 tools/build.py
Fails loudly on any content error so a broken card never ships.
"""
import base64
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
TEMPLATE = ROOT / "app" / "template.html"
OUT = ROOT / "dist" / "pest-study.html"

errors, warnings = [], []
BLOCK_KINDS = ("h", "box", "p", "list", "ol", "fig", "gallery")
# Multiple-choice answers are shuffled on screen, so an explanation must never point at a choice by its
# letter ("so C is wrong") or position ("that last one"). It would point at the wrong choice after a shuffle.
BY_LETTER = re.compile(
    r"(?:\b(?i:choices?|options?)\s+\(?[A-F]\)?(?![a-z])"
    r"|\b[A-F]\)?,?\s+(?:and|or)\s+\(?[A-F]\b(?![a-z'])"
    r"|(?:^|[.!?:]\s+)[A-F]\s+(?:is|are|was|has|describes?|says?)\b"
    r"|(?:\bso|\bbut|\band|\bonly|\bsays)\s+[A-F]\b(?![a-z'°])"
    r"|\b(?i:that|the) (?i:last|first|second|third|fourth) (?i:one|choice|option|answer|statement)\b)")
MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def load():
    data = json.loads((CONTENT / "study.json").read_text(encoding="utf-8"))
    chapters = sorted((CONTENT / "chapters").glob("*.json"))
    merged = []
    for path in chapters:
        try:
            ch = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            err(f"{path.name}: invalid JSON: {e}")
            continue
        merged.extend(ch.get("sections", []))
    practice = [s for s in data.get("sections", []) if s.get("practice")]
    other = [s for s in data.get("sections", []) if not s.get("practice")]
    data["sections"] = other + merged + practice
    return data


def resolve_figures(s, where):
    for f in s.get("figures", []):
        if "svgFile" in f:
            path = CONTENT / "figures" / f.pop("svgFile")
            if not path.exists():
                err(f"{where}: missing {path.relative_to(ROOT)}")
                continue
            svg = path.read_text(encoding="utf-8").strip()
            svg = re.sub(r"<\?xml[^>]*\?>", "", svg)
            svg = re.sub(r">\s+<", "><", svg)
            f["svg"] = svg
        if "imgFile" in f:
            path = CONTENT / "images" / f.pop("imgFile")
            mime = MIME.get(path.suffix.lower())
            if not path.exists() or not mime:
                err(f"{where}: missing or unsupported image {path.relative_to(ROOT)}")
                continue
            f["img"] = f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def check_text(where, t):
    if not isinstance(t, str) or not t.strip():
        err(f"{where}: empty sentence")
    elif len(t) > 1500:
        err(f"{where}: sentence over 1500 chars")
    elif t.count("**") % 2:
        err(f"{where}: unbalanced ** in {t[:60]!r}")


def check(data):
    sections = data.get("sections")
    if not isinstance(sections, list):
        err("sections must be a list")
        return
    sids, qids = set(), set()
    for s in sections:
        sid = s.get("id")
        where = f"section {sid!r}"
        if not sid or sid in sids:
            err(f"{where}: missing or duplicate id")
        sids.add(sid)
        for key in ("title", "chapter", "body", "questions"):
            if key not in s:
                err(f"{where}: missing {key}")
        pages = s.get("pages")
        if pages is not None and not (isinstance(pages, list) and 1 <= len(pages) <= 2 and all(isinstance(p, int) for p in pages)):
            err(f"{where}: pages must be null or [start, end] integers")
        if pages and len(pages) == 1:
            s["pages"] = [pages[0], pages[0]]
        resolve_figures(s, where)
        figs = {f.get("id"): f for f in s.get("figures", [])}
        used = set()
        lines = 0

        def fig_texts(fid):
            f = figs.get(fid)
            if not f:
                err(f"{where}: figure {fid!r} not defined")
                return []
            used.add(fid)
            if not (f.get("svg") or f.get("img") or f.get("photo")):
                err(f"{where}: figure {fid!r} needs svg, img, or a photo reference")
            return [f.get("title", "")] + f.get("explain", [])

        for b in s.get("body", []):
            kinds = [k for k in BLOCK_KINDS if k in b]
            texts = []
            if "box" in b:
                extra = [k for k in kinds if k not in ("box", "p", "list", "ol")]
                if extra or not any(k in b for k in ("p", "list", "ol")):
                    err(f"{where}: a box block takes a title plus p/list/ol, got {list(b)}")
                texts = [b["box"]] + b.get("p", []) + b.get("list", []) + b.get("ol", [])
            elif len(kinds) != 1:
                err(f"{where}: each body block needs exactly one of {BLOCK_KINDS}, got {list(b)}")
                continue
            elif kinds[0] == "h":
                texts = [b["h"]]
            elif kinds[0] in ("p", "list", "ol"):
                texts = b[kinds[0]]
            elif kinds[0] == "fig":
                texts = fig_texts(b["fig"])
            elif kinds[0] == "gallery":
                for fid in b["gallery"]:
                    texts += fig_texts(fid)
            lines += len(texts)
            for t in texts:
                check_text(where, t)
        for fid in figs:
            if fid not in used:
                warn(f"{where}: figure {fid!r} defined but not placed in body")
        if lines > 95:
            err(f"{where}: {lines} spoken lines; split the section (max 95)")
        qs = s.get("questions", [])
        if not s.get("practice") and len(qs) < 3:
            warn(f"{where}: only {len(qs)} questions")
        for q in qs:
            qid = q.get("id")
            qw = f"{where} question {qid!r}"
            if not qid or qid in qids:
                err(f"{qw}: missing or duplicate id")
            qids.add(qid)
            if q.get("src") not in ("review", "test"):
                err(f"{qw}: src must be 'review' or 'test'")
            if not q.get("q"):
                err(f"{qw}: missing q")
            if not q.get("ref"):
                err(f"{qw}: missing ref (where in the pages the answer is)")
            kind = q.get("kind")
            if kind == "mc":
                ch = q.get("choices")
                if not isinstance(ch, list) or not 2 <= len(ch) <= 6:
                    err(f"{qw}: mc needs 2-6 choices")
                elif not isinstance(q.get("answer"), int) or not 0 <= q["answer"] < len(ch):
                    err(f"{qw}: mc answer must be a valid choice index")
                else:
                    if len(set(c.strip().lower() for c in ch)) != len(ch):
                        err(f"{qw}: duplicate choices")
                    refers = any(w in c.lower() for c in ch for w in ("all of the above", "none of the above", "both a", "a and b", "a and c", "b and c"))
                    if refers and not q.get("fixed"):
                        err(f"{qw}: choices refer to other choices; set \"fixed\": true")
                    m = None if q.get("fixed") else BY_LETTER.search(q.get("why", ""))
                    if m:
                        err(f"{qw}: why names a choice by letter or position ({m.group(0).strip()!r}); choices are shuffled, so restate the fact instead")
            elif kind == "tf":
                if not isinstance(q.get("answer"), bool):
                    err(f"{qw}: tf answer must be true/false")
            elif kind == "short":
                if not isinstance(q.get("answer"), str) or not q["answer"].strip():
                    err(f"{qw}: short answer must be a string")
                keys = q.get("keys")
                if keys is not None and not (isinstance(keys, list) and all(isinstance(g, (str, list)) for g in keys)):
                    err(f"{qw}: keys must be a list of strings or lists of alternatives")
                if "ordered" in q and not (q["ordered"] is True and keys):
                    err(f"{qw}: ordered must be true and needs keys (the key groups are then required in order)")
            else:
                err(f"{qw}: kind must be mc, tf, or short")
            if q.get("style") not in (None, "recall", "scenario", "not"):
                err(f"{qw}: style must be recall, scenario, or not")


def check_answer_key(data):
    """Every review question must match Appendix A (content/answer-key.json)."""
    path = CONTENT / "answer-key.json"
    if not path.exists():
        return
    key = json.loads(path.read_text(encoding="utf-8"))["chapters"]
    for s in data["sections"]:
        for q in s.get("questions", []):
            if q.get("src") != "review":
                continue
            qw = f"review question {q.get('id')!r}"
            m = re.match(r"c(\d+)-", q.get("id", ""))
            n = re.search(r"Review question (\d+)", q.get("ref", "")) or re.search(r"-r(\d+)$", q.get("id", ""))
            if not m or not n:
                err(f"{qw}: cannot read chapter from id or 'Review question N' from ref")
                continue
            ch = key.get(str(int(m.group(1))))
            num = int(n.group(1))
            if not ch or num > len(ch["answers"]):
                warn(f"{qw}: no Appendix A answer for chapter {int(m.group(1))} question {num}")
                continue
            if q.get("kind") != "mc":
                err(f"{qw}: review questions must be mc to check against Appendix A")
                continue
            want = ord(ch["answers"][num - 1]) - ord("A")
            if q.get("answer") != want:
                got = chr(ord("A") + q["answer"]) if isinstance(q.get("answer"), int) else q.get("answer")
                err(f"{qw}: answer {got} disagrees with Appendix A ({ch['answers'][num - 1]})")


def main():
    data = load()
    check(data)
    check_answer_key(data)
    for w in warnings:
        print("warning:", w)
    if errors:
        for e in errors:
            print("ERROR:", e)
        sys.exit(1)
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = TEMPLATE.read_text(encoding="utf-8").replace("__CONTENT__", payload, 1)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    real = [s for s in data["sections"] if not s.get("practice")]
    nq = sum(len(s["questions"]) for s in real)
    nr = sum(1 for s in real for q in s["questions"] if q.get("src") == "review")
    print(f"built {OUT.relative_to(ROOT)}: {len(real)} cards, {nq} questions ({nr} review), {OUT.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
