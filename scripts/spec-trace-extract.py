#!/usr/bin/env python3
"""spec-trace-extract · binding-list helper extractor.

Purpose: spec-trace-gate's --components/--backends list files are unsustainable
to maintain by hand on real repositories. This tool extracts both lists from the
codebase:
  --components <- scan the component directories (.vue/.tsx/.jsx, excluding
                  tests / stories / declaration files / build output)
  --backends   <- recognize three shapes of backend endpoint declarations:
                  1) FastAPI/Flask decorators: @router.get("/x") / @app.post("/y")
                  2) Next.js App Router API: src/app/**/route.ts paths -> /api/… endpoints
                  3) generic inline literals: `GET /path` (common in service layers)
Output: two one-entry-per-line list files, fed straight into spec-trace-gate
(whole-string comparison semantics).
Boundary: it only extracts "what exists" — it never produces bindings (the
feature↔component mapping is a runway product, a human/session judgment).

Usage:
  python spec-trace-extract.py --src <component-dir> --api <backend-dir-or-file>… \
      --out-components comps.txt --out-backends backs.txt [--ext .vue,.tsx] [--selftest]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

COMPONENT_EXTS = [".vue", ".tsx", ".jsx"]

# Exclusions are anchored, never bare substrings: a filename that merely contains
# an excluded word (TaskHistory.vue contains "story") must not exclude the file.
SEGMENT_EXCLUDE = re.compile(
    r"(^|/)(test|tests|spec|specs|story|stories|evidence|smoke|storybook|node_modules|\.next|dist|build)(/)")
FILE_MARK_EXCLUDE = re.compile(r"\.(test|spec|stories|story)\.[^.]+$", re.I)
DECL_SUFFIX_EXCLUDE = re.compile(r"\.d\.tsx?$", re.I)


def _excluded(p: Path) -> bool:
    seg = str(p).replace("\\", "/")
    return bool(SEGMENT_EXCLUDE.search(seg) or FILE_MARK_EXCLUDE.search(p.name)
                or DECL_SUFFIX_EXCLUDE.search(p.name))


def extract_components(src: Path, exts: list[str]) -> list[str]:
    out: list[str] = []
    if not src.exists():
        return out
    for p in sorted(src.rglob("*")):
        if not p.is_file() or p.suffix not in exts:
            continue
        if _excluded(p):
            continue
        out.append(p.stem)
    return sorted(set(out))


DECORATOR = re.compile(r"@(?:router|app|api|blueprint|bp)\.(get|post|put|delete|patch)\(\s*[\"']([^\"']+)[\"']", re.I)
INLINE_ENDPOINT = re.compile(r"[\"']((?:GET|POST|PUT|DELETE|PATCH)\s+/[^\"']+)[\"']", re.I)
PY_FILE = re.compile(r"\.(py)$")
API_ROUTE_FILE = re.compile(r"route\.(ts|js)$")


def _extract_decorators(text: str) -> list[str]:
    return [f"{m.group(1).upper()} {m.group(2)}" for m in DECORATOR.finditer(text)]


def _extract_inline(text: str) -> list[str]:
    return [m.group(1).upper().replace("  ", " ") for m in INLINE_ENDPOINT.finditer(text)]


def _extract_next_routes(root: Path) -> list[str]:
    out: list[str] = []
    for p in sorted(root.rglob("*")):
        if p.is_file() and API_ROUTE_FILE.search(p.name) and not _excluded(p):
            rel = p.parent.relative_to(root)
            parts = [seg for seg in rel.parts if seg != "api"]
            dyn = re.sub(r"\[([^\]]+)\]", r"{\1}", "/".join(parts))
            out.append(f"/api/{dyn}" if parts else "/api")
    return out


def extract_backends(roots: list[Path]) -> list[str]:
    out: list[str] = []
    for root in roots:
        if not root.exists():
            continue
        if root.is_dir():
            out += _extract_next_routes(root)  # Next.js App Router route.ts -> /api/* endpoints
        files = [root] if root.is_file() else sorted(root.rglob("*"))
        for p in files:
            if not p.is_file():
                continue
            if API_ROUTE_FILE.search(p.name):
                continue  # handled by path via _extract_next_routes
            if _excluded(p):
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if PY_FILE.search(p.name):
                out += _extract_decorators(text)
            out += _extract_inline(text)
    return sorted(set(out))


def selftest() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        (t / "src").mkdir()
        (t / "src" / "Alpha.vue").write_text("<template/>", encoding="utf-8")
        (t / "src" / "beta.tsx").write_text("export default ()=><div/>", encoding="utf-8")
        (t / "src" / "Alpha.test.tsx").write_text("test", encoding="utf-8")  # excluded: filename mark
        (t / "src" / "TaskHistory.vue").write_text("history", encoding="utf-8")  # kept: contains "story" only as substring
        comps = extract_components(t / "src", COMPONENT_EXTS)
        ok1 = comps == ["Alpha", "TaskHistory", "beta"]
        api = t / "api"
        api.mkdir()
        (api / "users.py").write_text(
            '@router.get("/users")\n@router.post("/users")\n', encoding="utf-8")
        (api / "svc.py").write_text('r = client.fetch("GET /stats/mini")\n', encoding="utf-8")
        (api / "users" / "route.ts").parent.mkdir(parents=True, exist_ok=True)
        (api / "users" / "route.ts").write_text("export const GET = handlers.GET\n", encoding="utf-8")
        backs = extract_backends([api])
        ok2 = "GET /users" in backs and "POST /users" in backs and "GET /STATS/MINI" in backs and "/api/users" in backs
        print(f"selftest: component extraction (tests excluded, TaskHistory kept)={ok1} "
              f"endpoint extraction (decorators+inline)={ok2} comps={comps} backs={backs}")
        return 0 if ok1 and ok2 else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", help="component root directory")
    ap.add_argument("--api", nargs="*", help="backend root dirs / files (several allowed: Python decorators + inline, Next route.ts paths)")
    ap.add_argument("--ext", default=",".join(COMPONENT_EXTS), help="component extensions (comma-separated)")
    ap.add_argument("--out-components", default="comps.txt")
    ap.add_argument("--out-backends", default="backs.txt")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.src:
        print("FAIL: --src is required (or use --selftest)")
        return 1
    comps = extract_components(Path(a.src), [e.strip() for e in a.ext.split(",")])
    backs = extract_backends([Path(p) for p in (a.api or [])])
    Path(a.out_components).write_text("\n".join(comps) + ("\n" if comps else ""), encoding="utf-8")
    Path(a.out_backends).write_text("\n".join(backs) + ("\n" if backs else ""), encoding="utf-8")
    print(f"OK: {len(comps)} components -> {a.out_components}; {len(backs)} endpoints -> {a.out_backends}")
    print("Reminder: bindings.json (feature↔component bindings) is a runway product; this tool never produces it — write the bindings before feeding the gate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
