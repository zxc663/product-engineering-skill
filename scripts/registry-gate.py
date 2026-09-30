#!/usr/bin/env python3
"""registry-gate · forced-checklist item 4: component attribution (checks "was the
table consulted, was attribution made"; defines no components).

Rule: component files under the component directories must carry a registry
attribution marker:
  `registry: <name> source=<upstream-lib@version>` or
  `registry: <name> self-built-attribution=<why the upstream cannot solve this>`
Missing -> list the files -> exit 1 (add the attribution and rerun).

Baseline mode (adopting a legacy codebase): the first run with `--write-baseline`
records the file inventory of that moment (legacy exempt). Every later run
compares against the baseline and only flags "new files outside the baseline
without a marker" — new components must be attributed; legacy is not retroactive.

Usage: python registry-gate.py --path <component-dir> [--scope components] [--write-baseline] [--baseline <file>]
       python registry-gate.py --selftest
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

MARK = "registry:"
DEFAULT_BASELINE = ".registry-baseline.json"

# Component-directory segments (scope=components recognition set; guards against
# naming escapes such as src/ui).
COMPONENT_DIRS = {"components", "component", "ui", "widgets"}
# Non-source segments excluded (aligned with the lint/a11y exclusion set; keeps
# third-party code out of the report).
COMPONENT_EXCLUDE = {"node_modules", "dist", "build", ".git", "vendor", "coverage",
                     "test", "tests", "__tests__", "__pycache__", ".next", ".nuxt"}


def component_files(path: Path, scope: str, exts: list[str]) -> list[Path]:
    exts = [e.lower() for e in exts]
    out: list[Path] = []
    for f in sorted(path.rglob("*")):
        if f.suffix.lower() not in exts or not f.is_file():
            continue
        parts = {p.lower() for p in f.relative_to(path).parts[:-1]}
        parts.add(path.name.lower())  # the scan root itself may be a component dir (e.g. .../components)
        if parts & COMPONENT_EXCLUDE:
            continue
        if scope == "components" and not (parts & COMPONENT_DIRS):
            continue
        out.append(f)
    return out


def scan(path: Path, scope: str, exts: list[str], baseline: Path | None, write_baseline: bool) -> tuple[list[str], str]:
    files = component_files(path, scope, exts)
    all_rel = [str(f.relative_to(path)) for f in files]
    if write_baseline:
        baseline.write_text(json.dumps({"files": all_rel}, ensure_ascii=False, indent=1), encoding="utf-8")
        return [], f"baseline written to {baseline} ({len(all_rel)} legacy file(s) exempt)"
    known: set[str] = set()
    if baseline and baseline.exists():
        known = set(json.loads(baseline.read_text(encoding="utf-8")).get("files", []))
    missing = [rel for rel, f in zip(all_rel, files) if rel not in known and MARK not in f.read_text(encoding="utf-8", errors="ignore")]
    return missing, f"checked {len(all_rel)} component files (baseline exempts {len(known)})"


def selftest() -> int:
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        comp = root / "src" / "components"
        comp.mkdir(parents=True)
        (comp / "Old.vue").write_text("<template/>", encoding="utf-8")
        bl = root / DEFAULT_BASELINE
        # 1) baseline write: legacy Old.vue is exempt
        missing, msg = scan(comp, "components", [".vue"], bl, write_baseline=True)
        ok1 = missing == [] and "1 legacy file(s) exempt" in msg
        # 2) new component without a marker -> flagged
        (comp / "New.vue").write_text("export default () => <div/>", encoding="utf-8")
        missing, _ = scan(comp, "components", [".vue"], bl, write_baseline=False)
        ok2 = missing == ["New.vue"]
        # 3) new component with a marker -> passes
        (comp / "New.vue").write_text("// registry: New self-built-attribution=no upstream equivalent\nexport default () => <div/>", encoding="utf-8")
        missing, _ = scan(comp, "components", [".vue"], bl, write_baseline=False)
        ok3 = missing == []
        # 4) reverse: src/ui dir (no "component" in the name) without a marker -> must be flagged
        ui = root / "src" / "ui"
        ui.mkdir(parents=True)
        (ui / "Button.vue").write_text("export default () => <button/>", encoding="utf-8")
        missing, _ = scan(root / "src", "components", [".vue"], bl, write_baseline=False)
        ok4 = any("Button.vue" in m for m in missing)
        # 5) reverse: uppercase extension .VUE without a marker -> must be flagged
        (comp / "Upper.VUE").write_text("export default () => <div/>", encoding="utf-8")
        missing, _ = scan(comp, "components", [".vue"], bl, write_baseline=False)
        ok5 = any("Upper.VUE" in m for m in missing)
        # 6) reverse: node_modules third-party files -> not reported even with scope=all
        nm = root / "node_modules" / "some-lib"
        nm.mkdir(parents=True)
        (nm / "lib.vue").write_text("<template/>", encoding="utf-8")
        missing, _ = scan(root, "all", [".vue"], bl, write_baseline=False)
        ok6 = not any("node_modules" in m for m in missing)
        print(f"selftest: baseline legacy exempt={ok1} new unmarked flagged={ok2} new marked passes={ok3} "
              f"ui-dir escape flagged={ok4} uppercase suffix flagged={ok5} third-party excluded={ok6}")
        return 0 if ok1 and ok2 and ok3 and ok4 and ok5 and ok6 else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default="src")
    ap.add_argument("--ext", default=",".join([".vue", ".tsx", ".jsx"]))
    ap.add_argument("--scope", choices=["components", "all"], default="components",
                    help="components=component directories only (default); all=every matching file")
    ap.add_argument("--baseline", default=None)
    ap.add_argument("--write-baseline", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    path = Path(a.path)
    if not path.exists():
        print(f"FAIL: path does not exist: {path}")
        return 1
    baseline = Path(a.baseline) if a.baseline else path / DEFAULT_BASELINE
    missing, msg = scan(path, a.scope, [e.strip() for e in a.ext.split(",")], baseline, a.write_baseline)
    print(msg)
    if missing:
        print(f"FAIL: {len(missing)} new component(s) missing the registry attribution marker ({MARK} source=… / self-built-attribution=…):")
        for m in missing:
            print("  ✗", m)
        return 1
    print("OK: attribution check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
