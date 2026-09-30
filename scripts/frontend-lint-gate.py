#!/usr/bin/env python3
"""frontend-lint-gate · forced-checklist items 5/6 machine subset (inline styles /
hardcoded colors / console / empty catch).

Item 5 (inline styles / hardcoded colors: zero tolerance for new code) and item 6
(dead binding: dead code / empty catch) as executable checks. Mode aligned with
registry-gate: **baseline exempts legacy, flags new violations only** — a
"correct but expensive" default kills adoption (same philosophy as §7 sizing).

Checks (component files, outside <style> blocks):
  R1 inline style: style=" / :style=" / style={{
  R2 hardcoded color: hex #fff… (3–8 digits) and rgb(/rgba( literals (css files
    and <style> blocks are legal, not scanned; content color values on <meta>
    lines are page metadata, exempt)
  R3 console.*: console.log/debug/info/warn/error (+table/trace/dir/count);
    delivery check: errors go into the log module — zero tolerance
  R4 empty catch: catch (…) { } with no statements (swallowed errors = the
    dead-binding family)
  R5 empty state (warning level, baseline not applied): the file has a v-for
    list but no v-else / v-if="!…length" / empty-state keyword branch — an empty
    dataset with no guidance

Baseline semantics: --write-baseline records every current violation as legacy
exempt; from then on new violations exit 1 and legacy is silent.
Honest boundary: regex-level detection — for "legitimate exemptions" of inline
styles (e.g. dynamic positioning), use the baseline or the ledger; no semantic
judgment is attempted here.

Usage:
  python frontend-lint-gate.py --path <component-dir> [--ext .vue,.tsx,.jsx] [--baseline f] [--write-baseline]
  python frontend-lint-gate.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Exclusions are path-segment anchored: a filename that merely contains an
# excluded word (TaskHistory.vue contains "story") must not exclude the whole
# file — History-style names are everywhere and the bare-substring form fails in
# the false-negative direction. test/spec/story/evidence/smoke must be complete
# directory segments; node_modules/dist/build etc. as directory segments; .d.ts
# as a suffix.
COMPONENT_EXCLUDE = re.compile(
    r"(^|[/\\])(test|tests|spec|specs|story|stories|evidence|smoke)([/\\])"
    r"|(^|[/\\])(node_modules|\.next|dist|build)([/\\])"
    r"|\.d\.ts$")
STYLE_BLOCK = re.compile(r"<style[\s>].*?</style>", re.S)
# Single-quoted style=' and uppercase RGB( are real bypass shapes (covered by re.I / both quote forms).
R1 = re.compile(r"style=[\"']|:style=[\"']|style=\{\{")
R2 = re.compile(r"#[0-9a-f]{3,8}\b|rgba?\(", re.IGNORECASE)
# console.table/trace/dir/count bypassed a log/error-only enumeration — the full set is checked.
R3 = re.compile(r"console\.(log|debug|info|warn|error|table|trace|dir|count)\b")
# Optional-binding catch {} (no parentheses) bypassed the parenthesized form.
R4 = re.compile(r"catch\s*(?:\([^)]*\))?\s*\{\s*\}")
RULES = {"R1": R1, "R2": R2, "R3": R3, "R4": R4}
# R2's second canvas exemption shape: 2D-context property assignment
# (strokeStyle/fillStyle are canvas-specific API names; the false-pass surface is
# ~0. Custom-function parameters like makeGlowSprite('#..') have un-mechanizable
# semantics — a human domain, still flagged).
CANVAS_ASSIGN = re.compile(r"\.(?:strokeStyle|fillStyle)\s*=")

# R5 empty-state heuristic (warning level): v-else is legal, v-else-if does not
# count as an empty branch; the v-if="!x.length" shape does.
V_FOR = re.compile(r"\bv-for\b")
EMPTY_BRANCH = re.compile(
    r"v-else(?!-if)|v-(?:if|show)=[\"']\s*!|no items|no data|no records|nothing yet|empty-state|EmptyState|no-data|NoData")

RULE_NAMES = {
    "R1": "inline style (checklist 5)",
    "R2": "hardcoded color (checklist 5 — colors belong to tokens/style blocks, not the component area)",
    "R3": "console debug leftover (delivery check)",
    "R4": "empty catch swallowing errors (checklist 6, dead-binding)",
}


def strip_style_blocks(text: str) -> str:
    return STYLE_BLOCK.sub("", text)


def scan_file(p: Path, rules: dict[str, re.Pattern]) -> list[str]:
    try:
        raw = p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    # R2's css exemption: color values belong to css files / <style> blocks —
    # when a .css file is passed explicitly via --ext, its colors must not be
    # reported as component-area hardcoded colors.
    active = {k: v for k, v in rules.items() if not (p.suffix == ".css" and k == "R2")}
    text = strip_style_blocks(raw)
    out: list[str] = []
    for i, line in enumerate(text.splitlines(), 1):
        for rid, rx in active.items():
            # R2's meta exemption: theme-color and friends on <meta> lines are page
            # metadata, not component styling.
            if rid == "R2" and line.lstrip().startswith("<meta"):
                continue
            # R2's canvas exemption: color values inside addColorStop( call lines
            # are drawing parameters of the canvas gradient API (particle/chart
            # animation), not styling-token escapes.
            if rid == "R2" and (".addColorStop(" in line or CANVAS_ASSIGN.search(line)):
                continue
            if rx.search(line):
                out.append(f"{p.as_posix()}:{i} [{rid}] {RULE_NAMES[rid]}: {line.strip()[:80]}")
    return out


def collect(path: Path, exts: list[str]) -> list[Path]:
    if path.is_file():
        return [path]
    return [p for p in sorted(path.rglob("*"))
            if p.is_file() and p.suffix in exts and not COMPONENT_EXCLUDE.search(str(p))]


def scan_warnings(p: Path) -> list[str]:
    """R5 empty state: a file-level heuristic; warnings never affect exit and
    never enter the baseline."""
    try:
        text = p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    if not V_FOR.search(text) or EMPTY_BRANCH.search(text):
        return []
    first = next((ln for ln in text.splitlines() if "v-for" in ln), "").strip()[:70]
    return [f"{p.as_posix()} [R5-W] v-for list without an empty-state branch (no guidance when the data is empty): {first}"]


def selftest() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        bad = t / "Bad.vue"
        bad.write_text(
            '<template><div style="color: #ff0000">x</div></template>\n'
            "<template><div style='color: blue'>y</div></template>\n"  # single-quote form
            "<script>console.table(t); try {} catch (e) {}</script>\n"  # console.table + parameterized empty catch
            "<script>try {} catch {}</script>\n"  # optional-binding empty catch
            "<script>el.style.background = 'RGB(255,0,0)';</script>\n",  # uppercase RGB
            encoding="utf-8")
        good = t / "Good.tsx"
        good.write_text('export const A = () => <div className="c">x</div>;\n', encoding="utf-8")
        styleblock = t / "S.vue"
        styleblock.write_text("<style>.a { color: #ff0000; }</style>", encoding="utf-8")
        v = scan_file(bad, RULES)
        ok1 = any("[R1]" in x for x in v) and any("[R2]" in x for x in v) and any("[R4]" in x for x in v)
        # Reverse mutations (#407 discipline): every bypass shape must be flagged
        ok6 = (sum(1 for x in v if "[R1]" in x) >= 2  # double- and single-quoted styles both flagged
               and sum(1 for x in v if "[R3]" in x) >= 1  # console.table
               and sum(1 for x in v if "[R4]" in x) >= 2  # parameterized + optional-binding catches
               and any("RGB" in x and "[R2]" in x for x in v))  # uppercase RGB(
        ok2 = scan_file(good, RULES) == []
        text_s = strip_style_blocks(styleblock.read_text(encoding="utf-8"))
        ok3 = "#ff0000" not in text_s and scan_file(styleblock, RULES) == []
        cssfile = t / "tokens.css"
        cssfile.write_text(":root { --accent: #4a7297; }", encoding="utf-8")
        ok4 = scan_file(cssfile, RULES) == []  # regression: css-file colors are R2-exempt
        metafile = t / "meta.html"
        metafile.write_text('<html lang="en">\n<head>\n<meta name="theme-color" content="#eef1f5">\n</head>\n</html>', encoding="utf-8")
        ok5 = scan_file(metafile, RULES) == []  # regression: meta-line content colors are metadata-exempt
        warn_no = t / "NoEmpty.vue"  # R5 reverse: v-for with no empty branch -> W
        warn_no.write_text('<template><div v-for="i in list" :key="i">{{ i }}</div></template>', encoding="utf-8")
        warn_else = t / "WithElse.vue"  # R5 forward: v-else branch present
        warn_else.write_text('<template><div v-for="i in list" :key="i">{{ i }}</div><div v-else>Nothing yet</div></template>', encoding="utf-8")
        warn_notlen = t / "WithNotLen.vue"  # R5 forward: the v-if="!list.length" empty-branch shape
        warn_notlen.write_text('<template><div v-for="i in list" :key="i">{{ i }}</div><div v-if="!list.length">Empty</div></template>', encoding="utf-8")
        warn_elseif = t / "OnlyElseIf.vue"  # R5 reverse: v-else-if alone is not an empty branch (bypass shape)
        warn_elseif.write_text('<template><div v-if="loading">…</div><div v-else-if="list.length"><div v-for="i in list" :key="i">{{ i }}</div></div></template>', encoding="utf-8")
        ok7w = len(scan_warnings(warn_no)) == 1 and scan_warnings(warn_else) == [] \
            and scan_warnings(warn_notlen) == [] and len(scan_warnings(warn_elseif)) == 1
        # canvas addColorStop drawing parameters pass; ordinary style colors still flagged (both directions)
        canvasfile = t / "canvas.js"
        canvasfile.write_text("grad.addColorStop(0, 'rgba(90,70,160,0.14)');\n"
                              "ctx.strokeStyle = '#cfe4ff';\n"
                              "ctx.fillStyle = 'rgba(0,0,0,0.5)';\n"
                              "el.style.background = 'rgba(0,0,0,0.5)';\n"
                              "s = makeGlowSprite('#dbeeff', 'rgba(1,2,3,0.9)');\n", encoding="utf-8")
        vc = scan_file(canvasfile, RULES)
        ok8c = ((not any("addColorStop" in x or "strokeStyle" in x or "fillStyle" in x for x in vc))
                and sum(1 for x in vc if "[R2]" in x) == 2)  # the ordinary style assignment + the custom-function call stay flagged
        # evidence/smoke directories are excluded whole-file (same semantics as test/spec)
        evdir = t / "evidence"
        evdir.mkdir()
        smokef = evdir / "smoke-core.js"
        smokef.write_text("console.log('SMOKE RESULT: ok');\n", encoding="utf-8")
        ok9e = collect(evdir, [".js"]) == []
        # reverse mutation: a filename containing the "story" substring (TaskHistory)
        # must not exclude the whole file; the story/ directory is still excluded
        compdir = t / "components"
        compdir.mkdir()
        hf = compdir / "TaskHistory.vue"
        hf.write_text("<script setup>\nconsole.log('x')\n</script>\n", encoding="utf-8")
        ok10h = (collect(compdir, ['.vue']) and
                 sum(1 for x in scan_file(hf, RULES) if '[R3]' in x) == 1)
        sdir = compdir / "story"
        sdir.mkdir()
        (sdir / "A.vue").write_text("console.log('y')\n", encoding="utf-8")
        kept = collect(compdir, ['.vue'])
        ok10s = len(kept) == 1 and kept[0].name == "TaskHistory.vue"
        print(f"selftest: violation triple (R1/R2/R4)={ok1} clean file passes={ok2} style-block colors legal={ok3} "
              f"css-file colors exempt={ok4} meta colors exempt={ok5} reverse FL1-4={ok6} "
              f"R5 empty-state W flag/pass={ok7w} canvas exempt={ok8c} evidence dir excluded={ok9e} "
              f"History name kept / story dir still excluded={ok10h and ok10s}")
        return 0 if ok1 and ok2 and ok3 and ok4 and ok5 and ok6 and ok7w and ok8c and ok9e and ok10h and ok10s else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", help="component directory or a single file")
    ap.add_argument("--ext", default=".vue,.tsx,.jsx")
    ap.add_argument("--baseline", help="baseline JSON (legacy exempt); defaults to <path>/.lint-baseline.json")
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
    warnings: list[str] = []
    for f in files:
        violations += scan_file(f, RULES)
        warnings += scan_warnings(f)
    if a.write_baseline:
        bl = path / ".lint-baseline.json" if path.is_dir() else path.parent / ".lint-baseline.json"
        bl.write_text(json.dumps({"violations": violations}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"baseline written to {bl} ({len(violations)} legacy violation(s) exempt)")
        return 0
    bl_path = Path(a.baseline) if a.baseline else (path / ".lint-baseline.json" if path.is_dir() else None)
    base_set = set()
    if bl_path and Path(bl_path).exists():
        base_set = set(json.loads(Path(bl_path).read_text(encoding="utf-8")).get("violations", []))
    fresh = [v for v in violations if v not in base_set]
    for w in warnings:
        print("W", w)
    if fresh:
        print(f"FAIL: {len(fresh)} new frontend-lint violation(s) (legacy {len(violations) - len(fresh)} exempt via baseline):")
        for x in fresh[:20]:
            print("  ✗", x)
        return 1
    print(f"OK: frontend lint passed ({len(files)} files scanned; {len(violations)} legacy exempt via baseline)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
