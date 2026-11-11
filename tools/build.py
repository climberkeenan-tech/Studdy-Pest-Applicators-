#!/usr/bin/env python3
"""Validate content/study.json and build dist/pest-study.html.

Usage: python3 tools/build.py
Fails loudly on any content error so a broken card never ships.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "study.json"
TEMPLATE = ROOT / "app" / "template.html"
OUT = ROOT / "dist" / "pest-study.html"

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


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
        figs = {f.get("id"): f for f in s.get("figures", [])}
        lines = 0
        for b in s.get("body", []):
            kinds = [k for k in ("h", "p", "list", "fig") if k in b]
            if len(kinds) != 1:
                err(f"{where}: each body block needs exactly one of h/p/list/fig, got {list(b)}")
                continue
            k = kinds[0]
            if k == "h":
                lines += 1
                texts = [b["h"]]
            elif k in ("p", "list"):
                texts = b[k]
                lines += len(texts)
            else:
                f = figs.get(b["fig"])
                if not f:
                    err(f"{where}: figure {b['fig']!r} not defined")
                    continue
                if not (f.get("svg") or f.get("img") or f.get("photo")):
                    err(f"{where}: figure {b['fig']!r} needs svg, img, or a photo reference")
                texts = [f.get("title", "")] + f.get("explain", [])
                lines += len(texts)
            for t in texts:
                if not isinstance(t, str) or not t.strip():
                    err(f"{where}: empty sentence")
                elif len(t) > 1500:
                    err(f"{where}: sentence over 1500 chars")
                elif t.count("**") % 2:
                    err(f"{where}: unbalanced ** in {t[:60]!r}")
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
                    refers = any(w in c.lower() for c in ch for w in ("all of the above", "none of the above", "both a", "a and b", "a and c", "b and c"))
                    if refers and not q.get("fixed"):
                        err(f"{qw}: choices refer to other choices; set \"fixed\": true")
            elif kind == "tf":
                if not isinstance(q.get("answer"), bool):
                    err(f"{qw}: tf answer must be true/false")
            elif kind == "short":
                if not isinstance(q.get("answer"), str) or not q["answer"].strip():
                    err(f"{qw}: short answer must be a string")
                keys = q.get("keys")
                if keys is not None and not (isinstance(keys, list) and all(isinstance(g, (str, list)) for g in keys)):
                    err(f"{qw}: keys must be a list of strings or lists of alternatives")
            else:
                err(f"{qw}: kind must be mc, tf, or short")
            if q.get("style") not in (None, "recall", "scenario", "not"):
                err(f"{qw}: style must be recall, scenario, or not")


def main():
    data = json.loads(CONTENT.read_text(encoding="utf-8"))
    check(data)
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
    print(f"built {OUT.relative_to(ROOT)}: {len(real)} cards, {nq} questions, {OUT.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
