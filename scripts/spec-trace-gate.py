#!/usr/bin/env python3
"""spec-trace-gate · three-way binding traceability (component granularity; the
machine-checkable slice of bidirectional tracing).

Binding-list JSON schema (each row = the binding of one component instance;
granularity = component, not feature):
{
  "bindings": [
    {"page": "ImportPage", "component": "ProgressConsole",
     "feature": "import-parse progress", "backend": "POST /imports/parse",
     "evidence": "shot-01.png"}
  ]
}
A pure-display component may declare backend explicitly as "NONE(<reason>)".

Checks:
  T1 every row has all five fields (page/component/feature/backend/evidence)
  T2 evidence forbids placeholder wording (none/not verified/TODO/...) — without real
     rendered proof, do not claim verified
  T3 a fully identical quadruple (page/component/feature/backend) repeated = redundant row
  T4 UI orphans: components present in --components <list> but unbound in the list =
     invented / forgotten to register
  T5 dead logic: a backend block present in --backends <list> but consumed by no component
  T6 ghost endpoints: a binding row whose backend looks like an HTTP endpoint (verb+path /
     URL) but is absent from the actual --backends list = referencing a backend that does
     not exist (client storage such as localStorage is not URL-shaped and is not flagged)
  T7 file-type evidence existence (dual-mode): if evidence looks like a file (common
     evidence extension or a path separator), it must really exist — relative paths resolve
     against the binding list's own directory; a directory path is rejected; textual
     external execution records (no path/extension shape) stay allowed — a claim of
     presence is not evidence of presence, file-type evidence must be touchable

Usage: python spec-trace-gate.py --file bindings.json [--components list.txt] [--backends list.txt]
       python spec-trace-gate.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BAD = re.compile(r"^\s*(none|not verified|unverified|todo|tbd|pending|placeholder|n/?a|-|—|–)$", re.IGNORECASE)
PURE_DISPLAY = re.compile(r"^NONE\(.+\)$")
# URL shape: an HTTP verb + path ("GET /x"), a scheme ("https://"), or a leading "/" —
# client storage such as localStorage / IndexedDB does not match
URLISH = re.compile(r"^(?:[A-Z]{3,8}\s+\S+|.+://|/)")
# file-type evidence shape: ends with a common evidence extension, or contains a path
# separator (conservative direction — when unsure, treat as file-type and check existence)
EVIDENCE_FILEISH = re.compile(r"\.(png|jpe?g|webp|gif|svg|bmp|pdf|md|txt|log|json|csv|html?|mp4|mov)$|[/\\]", re.I)


def is_file_evidence(ev: str) -> bool:
    return bool(EVIDENCE_FILEISH.search(ev or ""))


def _norm(s: str) -> str:
    """Normalize path-parameter segments: {anything} → {} — a hand-written {id} and a
    backend-declared {appt_id} are the same endpoint; strict string comparison would
    report one endpoint as both T5 dead logic and T6 ghost."""
    return re.sub(r"\{[^}/]*\}", "{}", s)


def check(bindings: list[dict], comp_list: set[str] | None, backend_list: set[str] | None,
          base_dir: Path | None = None) -> list[str]:
    fails: list[str] = []
    if not bindings:
        return ["T1 binding list is empty"]
    seen_quads: set[tuple] = set()
    used_components: set[str] = set()
    used_backends: set[str] = set()
    defect_rows: list[tuple[str, str]] = []  # T1-defective rows (component, backend) — not counted as consumers
    for i, b in enumerate(bindings, 1):
        page, comp = b.get("page", ""), b.get("component", "")
        feat, be, ev = b.get("feature", ""), b.get("backend", ""), b.get("evidence", "")
        if not (page and comp and feat and be and ev):
            fails.append(f"T1 row {i} missing one of the five fields: {page}/{comp}/{feat}/{be}/{ev or '(empty)'}")
            defect_rows.append((comp, be))
            continue
        if BAD.match(ev):
            fails.append(f"T2 row {i} evidence is placeholder text ({ev}) — without real rendered proof, do not claim verified")
        elif is_file_evidence(ev):  # T7 dual-mode: touch the file for file-type evidence; textual records pass
            p = Path(ev)
            target = p if p.is_absolute() else (base_dir / ev if base_dir else Path(ev))
            if target.is_dir():
                fails.append(f"T7 row {i} evidence is a directory, not a file: {ev} (base={base_dir or 'CWD'})")
            elif not target.exists():
                fails.append(f"T7 row {i} file-type evidence does not exist: {ev} (base={base_dir or 'CWD'})"
                             " — a claim of presence is not evidence of presence")
        if not PURE_DISPLAY.match(be) and BAD.match(be):
            fails.append(f"T1 row {i} backend empty and not declared pure-display: {comp}")
        quad = (page, comp, feat, be)
        if quad in seen_quads:
            fails.append(f"T3 duplicate binding row: {quad}")
        seen_quads.add(quad)
        used_components.add(comp)
        if not PURE_DISPLAY.match(be):
            used_backends.add(be)
    if comp_list:
        for ghost in sorted(comp_list - used_components):
            tag = next((f" (chained: T1-defective row '{c}' was not counted as a consumer; "
                        "this finding is exposed through that row)"
                        for c, _ in defect_rows if c == ghost), "")
            fails.append(f"T4 UI orphan: component '{ghost}' exists in code but is bound to no feature{tag}")
    # note the None/empty distinction: None = --backends not provided (check not applicable);
    # empty set = provided but zero backends — an empty list is exactly the classic
    # ghost-endpoint scenario (a pure-frontend fixture referencing an API that does not
    # exist); a falsy test must not swallow it
    if backend_list is not None:
        norm_list = {_norm(x) for x in backend_list}
        norm_used = {_norm(x) for x in used_backends}
        for dead in sorted(norm_list - norm_used):
            tag = next((f" (chained: T1-defective row backend '{_norm(b)}' was not counted as a consumer; "
                        "this finding is exposed through that row)"
                        for c, b in defect_rows if not PURE_DISPLAY.match(b) and _norm(b) == dead), "")
            fails.append(f"T5 dead logic: backend block '{dead}' has no component consumer{tag}")
        # the other half of the two-way reconciliation: T5 finds "a block nobody uses",
        # T6 finds "a row with no block"
        for b in bindings:
            be = b.get("backend", "")
            if PURE_DISPLAY.match(be) or not URLISH.match(be):
                continue
            if _norm(be) not in norm_list:
                fails.append(f"T6 ghost endpoint: '{b.get('component', '?')}' binds backend '{be}' which is absent "
                             "from the actual backend list (nonexistent endpoint / typo / unimplemented)")
    return fails


def selftest() -> int:
    # T7 onward the selftest needs real files (file-type evidence existence) — fixture
    # directory first; ok1/f3 and the T7 cases bind base_dir
    import tempfile
    td = tempfile.TemporaryDirectory()
    tdp = Path(td.name)
    (tdp / "s.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (tdp / "s2.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (tdp / "adir").mkdir()
    good = {"bindings": [
        {"page": "P", "component": "C1", "feature": "F1", "backend": "POST /a", "evidence": "s.png"},
        {"page": "P", "component": "C2", "feature": "F2", "backend": "NONE(pure display)", "evidence": "s2.png"}]}
    bad = {"bindings": [
        {"page": "P", "component": "C1", "feature": "F1", "backend": "POST /a", "evidence": "TODO"},
        {"page": "P", "component": "C1", "feature": "F1", "backend": "POST /a", "evidence": "TODO"}]}
    ok1 = check(good["bindings"], {"C1", "C2"}, {"POST /a"}, base_dir=tdp) == []
    f = check(bad["bindings"], {"C1", "C9"}, {"/a", "/dead"})
    ok2 = any("T2" in x for x in f) and any("T3" in x for x in f) and any("T4" in x for x in f) and any("T5" in x for x in f)
    # a multi-word backend id must traverse the whole file→list→compare path without
    # false positives or misses
    import os
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as tf:
        tf.write("POST /imports/parse\n\nGET /unused\n")
        tmp = tf.name
    try:
        loaded = _load_list(tmp)
    finally:
        os.unlink(tmp)
    ok3 = loaded == {"POST /imports/parse", "GET /unused"}
    f3 = check([{"page": "P", "component": "C1", "feature": "F1",
                 "backend": "POST /imports/parse", "evidence": "s.png"}], None, loaded, base_dir=tdp)
    ok4 = len(f3) == 1 and "T5" in f3[0] and "GET /unused" in f3[0]
    # T6 reverse: a ghost endpoint must be flagged; client storage (not URL-shaped) must not
    ghost = [{"page": "P", "component": "C1", "feature": "F1", "backend": "GET /api/stats", "evidence": "s.png"},
             {"page": "P", "component": "C2", "feature": "F2", "backend": "localStorage", "evidence": "s2.png"}]
    f5 = check(ghost, None, {"GET /real"})
    ok5 = any("T6" in x and "/api/stats" in x for x in f5) and not any("localStorage" in x and "T6" in x for x in f5)
    # empty-backend-list variant: --backends given but the file is empty (pure frontend) —
    # every URL-shaped binding is then a ghost; a falsy test must not swallow it
    f6 = check(ghost[:1], None, set())
    ok6 = any("T6" in x for x in f6)
    # parameter-segment normalization: {id} vs {appt_id} = same endpoint — neither T5 nor T6
    # may fire; a genuinely deleted endpoint still fires
    param = [{"page": "P", "component": "C1", "feature": "F1", "backend": "DELETE /appointments/{id}", "evidence": "s.png"}]
    f7 = check(param, None, {"DELETE /appointments/{appt_id}", "GET /x"})
    ok7 = not any(("T5" in x or "T6" in x) and "appointments" in x for x in f7)
    gone = check(param, None, {"GET /x"})
    ok8 = any(("T5" in x or "T6" in x) for x in gone)
    # T1 chained-annotation, all four faces: the component/backend of a T1-defective row
    # carries the "(chained: ...)" tag in T4/T5 messages; an orphan/dead entry with no
    # defective-row source (C9, GET /dead) must not be tagged
    linked = [{"page": "P", "component": "C1", "feature": "F1", "backend": "POST /a", "evidence": ""}]
    f9 = check(linked, {"C1", "C9"}, {"POST /a", "GET /dead"})
    t4_c1 = next((x for x in f9 if "T4" in x and "'C1'" in x), "")
    t4_c9 = next((x for x in f9 if "T4" in x and "'C9'" in x), "")
    t5_a = next((x for x in f9 if "T5" in x and "POST /a" in x), "")
    t5_dead = next((x for x in f9 if "T5" in x and "GET /dead" in x), "")
    ok9 = ("chained" in t4_c1 and t4_c9 and "chained" not in t4_c9
           and "chained" in t5_a and t5_dead and "chained" not in t5_dead)
    # T7 dual-mode + RT-04 fake-path rejection + RT-05 directory-path rejection: file-type
    # evidence must really exist (relative base = the binding list's own directory);
    # textual external execution records pass
    (tdp / "real-shot.png").write_bytes(b"\x89PNG\r\n")
    ok_file = check([{"page": "P", "component": "C1", "feature": "F1",
                      "backend": "POST /a", "evidence": "real-shot.png"}],
                    None, None, base_dir=tdp) == []
    ok_text = check([{"page": "P", "component": "C1", "feature": "F1",
                      "backend": "POST /a", "evidence": "external execution record: passed review and archived"}],
                    None, None, base_dir=tdp) == []
    rt04 = check([{"page": "P", "component": "C1", "feature": "F1",
                   "backend": "POST /a", "evidence": "missing-shot.png"}],
                 None, None, base_dir=tdp)
    ok_rt04 = len(rt04) == 1 and "T7" in rt04[0] and "does not exist" in rt04[0]
    rt05 = check([{"page": "P", "component": "C1", "feature": "F1",
                   "backend": "POST /a", "evidence": "./adir"}],
                 None, None, base_dir=tdp)
    ok_rt05 = len(rt05) == 1 and "T7" in rt05[0] and "directory" in rt05[0]
    ok_abs = check([{"page": "P", "component": "C1", "feature": "F1",
                     "backend": "POST /a", "evidence": str(tdp / "real-shot.png")}],
                   None, None, base_dir=Path("Z:/nonexistent-base")) == []
    td.cleanup()
    print(f"selftest: valid bindings pass={ok1} placeholder/dup/orphan/dead all blocked={ok2} ({len(f)} findings) "
          f"multi-word backend whole-string load={ok3} dead logic reports only real dead={ok4} "
          f"ghost blocked/client-storage exempt={ok5} empty list still blocks ghosts={ok6} "
          f"param-name normalization passes={ok7} genuinely-gone endpoint still blocked={ok8} "
          f"T1 chained tags four faces={ok9} ({len(f9)} findings) "
          f"T7 real file passes={ok_file} T7 textual record passes={ok_text} "
          f"RT-04 fake path blocked={ok_rt04} RT-05 directory path blocked={ok_rt05} "
          f"T7 absolute path direct={ok_abs}")
    return 0 if all([ok1, ok2, ok3, ok4, ok5, ok6, ok7, ok8, ok9,
                     ok_file, ok_text, ok_rt04, ok_rt05, ok_abs]) else 1


def _load_list(path: str) -> set[str]:
    # list-file semantics = one entry per line, loaded as whole strings — splitting the file
    # on whitespace would shred multi-word ids ("GET /favorites") and make every valid
    # list a false-positive T5
    return {ln.strip() for ln in Path(path).read_text(encoding="utf-8").splitlines() if ln.strip()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file")
    ap.add_argument("--components", help="component list file from code (one per line), for the T4 orphan check")
    ap.add_argument("--backends", help="backend block list file (one per line), for the T5 dead-logic check")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.file:
        print("FAIL: --file or --selftest required")
        return 1
    bindings = json.loads(Path(a.file).read_text(encoding="utf-8")).get("bindings", [])
    comp_list = _load_list(a.components) if a.components else None
    backend_list = _load_list(a.backends) if a.backends else None
    fails = check(bindings, comp_list, backend_list, base_dir=Path(a.file).resolve().parent)
    if fails:
        print(f"FAIL: {len(fails)} traceability defects:")
        for x in fails:
            print("  ✗", x)
        return 1
    print(f"OK: binding list passed ({len(bindings)} rows, component granularity, no orphans, no dead logic)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
