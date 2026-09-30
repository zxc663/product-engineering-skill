#!/usr/bin/env python3
"""a11y-gate · forced-checklist item 9: the accessibility static floor (axe subset).

This gate is the low-false-positive four-check static subset; it does not replace
a full axe-core audit. Mode aligned with frontend-lint-gate: **baseline exempts
legacy, new violations only** — a "correct but expensive" default kills adoption.

Checks (.html/.vue/.tsx/.jsx):
  A1 img without alt: an <img> tag with no alt attribute (alt="" is legal for
     decorative images)
  A2 form control without accessible name: <input|select|textarea> with no
     aria-label/aria-labelledby, no label reference (for=/htmlFor= literal
     reconciliation), not wrapped in <label>, and not type hidden/submit/button/reset
  A3 interactive element without accessible name: <button> or <a href> whose
     content, after stripping child tags, is empty or bare symbols (▶/×/⋯ have
     glyphs but no words), with no aria-label/aria-labelledby/title (icon buttons
     without an accessible name are a high-frequency real defect)
  A4 html without lang: an <html> tag with no lang attribute (.html files only)

Honest boundary: regex-level detection — no contrast / focus order / keyboard
trap / ARIA semantics / tabindex checks. JSX expression children ({expr}) count
as possibly-has-content (conservative pass; false-positive resistance first,
same stance as frontend-lint-gate).

Usage:
  python a11y-gate.py --path <dir-or-file> [--ext .html,.vue,.tsx,.jsx] [--baseline f] [--write-baseline]
  python a11y-gate.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Exclusions are path-segment anchored: a filename merely containing an excluded
# word (TaskHistory.vue contains "story") must not exclude the whole file.
COMPONENT_EXCLUDE = re.compile(
    r"(^|[/\\])(test|tests|spec|specs|story|stories|evidence|smoke)([/\\])"
    r"|(^|[/\\])(node_modules|\.next|dist|build)([/\\])"
    r"|\.d\.ts$")
TAG_IMG = re.compile(r"<img\b[^>]*>")
TAG_FIELD = re.compile(r"<(input|select|textarea)\b[^>]*?>")
TAG_FLOW = re.compile(r"<(label|input|select|textarea)\b[^>]*?>|</label>")
TAG_CLICKABLE = re.compile(r"<(button|a)\b[^>]*?>(.*?)</\1>", re.S)
# A3b: pseudo-buttons — a click binding on a non-semantic element (modifiers like
# .self/.prevent included)
TAG_PSEUDO = re.compile(r"<([a-z][a-z0-9-]*)\b[^>]*?(?:@click(?:\.\w+)*|v-on:click(?:\.\w+)*|onClick|\(click\))=", re.I)
NON_INTERACTIVE = {"div", "span", "p", "li", "ul", "ol", "section", "img", "td", "tr", "table", "h1", "h2", "h3", "h4", "h5", "h6"}
TAG_HTML = re.compile(r"<html\b[^>]*>")
ATTR = re.compile(r"""([\w-]+)\s*=\s*["']([^"']*)["']""")

FREE_TYPES = {"hidden", "submit", "button", "reset"}
NAME_ATTRS = ("aria-label", "aria-labelledby")


def attrs_of(open_tag: str) -> dict[str, str]:
    return {m.group(1).lower(): m.group(2) for m in ATTR.finditer(open_tag)}


def has_any(attrs: dict[str, str], names: tuple[str, ...]) -> bool:
    # An accessible name must be non-empty: aria-label="" passes on key presence alone.
    return any(n in attrs and attrs[n].strip() for n in names)


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def scan_file(p: Path) -> list[str]:
    try:
        text = p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    out: list[str] = []
    rel = p.as_posix()

    for m in TAG_IMG.finditer(text):
        if "alt" not in attrs_of(m.group(0)):
            out.append((line_of(text, m.start()), "A1", "img without alt", m.group(0)[:60]))

    # A2: the label-for set + a label-flow scan (wrapping exemption)
    label_for = {a["for"] for a in map(attrs_of, re.findall(r"<label\b[^>]*>", text)) if a.get("for")}
    label_for |= {a["htmlfor"] for a in map(attrs_of, re.findall(r"<label\b[^>]*>", text)) if a.get("htmlfor")}
    depth = 0
    for m in TAG_FLOW.finditer(text):
        tag = m.group(0)
        if tag.startswith("</label"):
            depth = max(0, depth - 1)
            continue
        if tag.startswith("<label"):
            depth += 1
            continue
        attrs = attrs_of(tag)
        ok = (
            has_any(attrs, NAME_ATTRS)
            or attrs.get("type", "").lower() in FREE_TYPES
            or (attrs.get("id") in label_for if attrs.get("id") else False)
            or depth > 0
        )
        if not ok:
            out.append((line_of(text, m.start()), "A2",
                        f"{tag[1:tag.find(' ')] if ' ' in tag else tag[1:-1]} has no accessible name (no label/aria/wrapping)", tag[:60]))

    for m in TAG_CLICKABLE.finditer(text):
        open_tag, inner = m.group(0).split(">", 1)[0] + ">", m.group(2)
        attrs = attrs_of(open_tag)
        if open_tag.startswith("<a") and "href" not in attrs:
            continue
        if has_any(attrs, NAME_ATTRS) or "title" in attrs:
            continue
        visible = re.sub(r"<[^>]*>", "", inner).strip()
        if visible and re.search(r"\w", visible):
            continue
        if re.search(r"\{[^}]*\}", inner):  # JSX/template expression children: conservative pass
            continue
        name = open_tag[1:open_tag.find(" ")] if " " in open_tag else open_tag[1:-1]
        # Bare-symbol variant: ▶/⏸/× have glyphs but no words — a screen reader reads
        # the symbol name, not a meaning; the "content is not empty" shape once
        # slipped past the empty-content check.
        if visible:
            out.append((line_of(text, m.start()), "A3",
                        f"<{name}> content is a bare symbol (e.g. ▶/×/⋯) with no accessible name — icon buttons need aria-label", open_tag[:60]))
        else:
            out.append((line_of(text, m.start()), "A3", f"<{name}> content is empty with no accessible name", open_tag[:60]))

    # A3b: pseudo-buttons — click bound on a non-interactive element without a role
    # (the click target has no semantics: unreachable by keyboard and screen reader alike)
    for m in TAG_PSEUDO.finditer(text):
        open_tag = m.group(0)
        attrs = attrs_of(open_tag)
        tag = m.group(1).lower()
        if tag not in NON_INTERACTIVE:
            continue  # native interactive elements / custom components (capitalized): conservative pass
        if attrs.get("role", "").strip():
            continue  # role semantics already declared (role="button" etc.)
        out.append((line_of(text, m.start()), "A3b",
                    f"<{tag}> click without role (pseudo-button: add role=\"button\" + keyboard events, or use <button>)", open_tag[:60]))

    if p.suffix == ".html":
        for m in TAG_HTML.finditer(text):
            aa = attrs_of(m.group(0))
            # An empty lang is as good as a missing one — both pass on key presence alone.
            if "lang" not in aa:
                out.append((line_of(text, m.start()), "A4", "<html> has no lang attribute", m.group(0)[:60]))
            elif not aa["lang"].strip():
                out.append((line_of(text, m.start()), "A4", "<html> lang is empty", m.group(0)[:60]))

    # Baseline stability: fragment whitespace normalized (newline/indent insensitive);
    # line numbers drift with the source — rebuild the baseline on source changes
    # (a known trade-off, same as frontend-lint-gate).
    return [f"{rel}:{ln} [{rid}] {name}: {re.sub(r'\s+', ' ', frag).strip()[:80]}" for ln, rid, name, frag in out]


def collect(path: Path, exts: list[str]) -> list[Path]:
    if path.is_file():
        return [path]
    return [p for p in sorted(path.rglob("*"))
            if p.is_file() and p.suffix in exts and not COMPONENT_EXCLUDE.search(str(p))]


def selftest() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        bad = t / "Bad.vue"
        bad.write_text(
            "<template>\n"
            '  <img src="x.png">\n'
            '  <input type="text">\n'
            '  <input type="text" aria-label="">\n'  # empty aria-label is not an accessible name
            "  <button></button>\n"
            "</template>\n",
            encoding="utf-8")
        good = t / "Good.vue"
        good.write_text(
            "<template>\n"
            '  <img src="d.png" alt="">\n'
            '  <input type="text" aria-label="keyword">\n'
            "  <button>Search</button>\n"
            "</template>\n",
            encoding="utf-8")
        labelfor = t / "LabelFor.vue"
        labelfor.write_text(
            "<template>\n"
            '  <label for="q">Keyword</label>\n'
            '  <input type="text" id="q">\n'
            "</template>\n",
            encoding="utf-8")
        wrapped = t / "Wrapped.vue"
        wrapped.write_text(
            "<template>\n"
            "  <label>\n"
            '    <input type="text">\n'
            "  </label>\n"
            "</template>\n",
            encoding="utf-8")
        html_bad = t / "bad.html"
        html_bad.write_text("<html><body><p>x</p></body></html>", encoding="utf-8")
        html_emptylang = t / "emptylang.html"
        html_emptylang.write_text('<html lang=""><body><p>x</p></body></html>', encoding="utf-8")
        hidden_ok = t / "Hidden.vue"
        hidden_ok.write_text('<template><input type="hidden" name="csrf"></template>', encoding="utf-8")
        pseudobad = t / "PseudoBad.vue"  # A3b reverse: click-div without a role must be flagged
        pseudobad.write_text('<template><div class="row" @click="go()">{{ x }}</div></template>', encoding="utf-8")
        pseudook1 = t / "PseudoRole.vue"  # A3b forward: role declared -> pass
        pseudook1.write_text('<template><div role="button" @click="go()">x</div></template>', encoding="utf-8")
        pseudook2 = t / "PseudoNative.vue"  # A3b forward: native button -> pass
        pseudook2.write_text('<template><button @click="go()">x</button></template>', encoding="utf-8")
        pseudook3 = t / "PseudoComp.vue"  # A3b forward: custom component (capitalized) -> conservative pass
        pseudook3.write_text('<template><MyRow @click="go()" /></template>', encoding="utf-8")
        symbolbad = t / "SymbolBad.vue"  # A3 bare-symbol reverse: ▶ without aria-label must be flagged
        symbolbad.write_text('<template><button @click="play()">▶</button></template>', encoding="utf-8")
        symbolok1 = t / "SymbolLabel.vue"  # A3 forward: aria-label present -> pass
        symbolok1.write_text('<template><button aria-label="Play" @click="play()">▶</button></template>', encoding="utf-8")
        symbolok2 = t / "SymbolText.vue"  # A3 forward: real word content passes (CJK included — \w is unicode)
        symbolok2.write_text('<template><button @click="go()">开始</button></template>', encoding="utf-8")

        vb = scan_file(bad)
        ok1 = all(any(f"[{r}]" in x for x in vb) for r in ("A1", "A2", "A3"))
        ok2 = scan_file(good) == []
        ok3 = scan_file(labelfor) == []
        ok4 = scan_file(wrapped) == []
        ok5 = any("[A4]" in x for x in scan_file(html_bad))
        ok6 = scan_file(hidden_ok) == []
        ok7 = (sum(1 for x in vb if "[A2]" in x) >= 2  # nameless + empty aria-label both flagged
               and any("[A4]" in x for x in scan_file(html_emptylang)))  # empty lang flagged
        vb_p = scan_file(pseudobad)
        ok8 = any("[A3b]" in x for x in vb_p) and scan_file(pseudook1) == [] \
            and scan_file(pseudook2) == [] and scan_file(pseudook3) == []
        vb_s = scan_file(symbolbad)
        ok9 = any("[A3]" in x and "symbol" in x for x in vb_s) \
            and scan_file(symbolok1) == [] and scan_file(symbolok2) == []
        print(f"selftest: bad-file triple (A1/A2/A3)={ok1} clean file passes={ok2} label-for exempt={ok3} "
              f"wrapping exempt={ok4} html-lang hit={ok5} hidden exempt={ok6} reverse empty-aria/empty-lang={ok7} "
              f"A3b pseudo-button flag/pass={ok8} A3 bare-symbol flag/pass={ok9}")
        return 0 if all((ok1, ok2, ok3, ok4, ok5, ok6, ok7, ok8, ok9)) else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", help="directory or a single file")
    ap.add_argument("--ext", default=".html,.vue,.tsx,.jsx")
    ap.add_argument("--baseline", help="baseline JSON (legacy exempt); defaults to <path>/.a11y-baseline.json")
    ap.add_argument("--write-baseline", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.path:
        print("FAIL: --path is required (or use --selftest)")
        return 1
    path = Path(a.path)
    files = collect(path, [e.strip() for e in a.ext.split(",")])
    violations: list[str] = []
    for f in files:
        violations += scan_file(f)
    if a.write_baseline:
        bl = path / ".a11y-baseline.json" if path.is_dir() else path.parent / ".a11y-baseline.json"
        bl.write_text(json.dumps({"violations": violations}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"baseline written to {bl} ({len(violations)} legacy violation(s) exempt)")
        return 0
    bl_path = Path(a.baseline) if a.baseline else (path / ".a11y-baseline.json" if path.is_dir() else None)
    base_set = set()
    if bl_path and Path(bl_path).exists():
        base_set = set(json.loads(Path(bl_path).read_text(encoding="utf-8")).get("violations", []))
    fresh = [v for v in violations if v not in base_set]
    if fresh:
        print(f"FAIL: {len(fresh)} new a11y violation(s) (legacy {len(violations) - len(fresh)} exempt via baseline):")
        for x in fresh[:20]:
            print("  ✗", x)
        return 1
    print(f"OK: accessibility static floor passed ({len(files)} files scanned; {len(violations)} legacy exempt via baseline)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
