#!/usr/bin/env python3
"""statechart-gate · state + transition structure check (the strict statement of "every
state has a way out").

Checks the translated-table source statechart JSON:
  C1 initial exists   C2 no dead ends (every non-final state has out-edges)
  C3 fully reachable (BFS from initial)
  C4 every error state has a recovery transition (an out-edge to a non-error state)
  C5 a guarded transition must carry a guardDesc explanation
  C6 reference integrity: every transition target must exist in states (the old BFS used
     to skip dangling targets silently)
  C7 recovery two-way reconciliation (needs --contract):
     forward = every contract recovery row (state, action, target) must hit the matching
     transition in the statechart (a missing edge = a promise with nowhere to land)
     reverse = error-state out-edges ⊆ recovery rows ∪ the non_error_failures whitelist
     (an extra edge = an unregistered invention)
     Both directions exit 1.

Error-state recognition (three sources, backward compatible):
  declared ("type": "error" in the state body) ∪ the name heuristic (error/fail in the
  state name) ∪ states mentioned in contract recovery rows.
  The name heuristic misses names like permission_denied — when accurate recognition is
  needed, declare "type": "error" explicitly, or register that state's exit in the
  contract recovery rows.

Contract JSON shape (--contract; field names follow references/contract-schema.md):
  {"recovery": [{"state": "export_failed", "action": "RETRY_EXPORT", "target": "exporting", "note": "..."}],
   "non_error_failures": [{"state": "loading", "action": "LOAD_FAIL", "target": "empty"}]}

Honest capability boundary: the schema = flat states (no nesting / parallel regions).
"Granularity semantics" such as file-level or batch-level can only be expressed as a
self-loop + a guardDesc textual convention; the gate cannot check whether granularity is
correct — structural checks (graph properties) and domain-semantic review (granularity,
propagation) are both required. Nested states wait until a real project hurts.
A dict transition without a "target" key = an internal transition (legal, no out-edge
semantics); this gate does not flag it.

Usage: python statechart-gate.py --file sc.json [--contract contract.json]
       python statechart-gate.py --probe-recovery <dir>   # probe markdown with suspected recovery semantics (remind, never fail)
       python statechart-gate.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import deque
from pathlib import Path


def targets(tr) -> list[str]:
    if isinstance(tr, str):
        return [tr]
    if isinstance(tr, dict):
        return [tr["target"]] if "target" in tr else []
    return []


def norm_transitions(on) -> list[tuple[str, dict]]:
    """Normalize the on-table → [(event, transition dict)]; a str is lifted to
    {"target": s}; a dict passes through as-is (it may have no target)."""
    out: list[tuple[str, dict]] = []
    for event, tr in (on or {}).items():
        items = tr if isinstance(tr, list) else [tr]
        for x in items:
            if isinstance(x, str):
                out.append((event, {"target": x}))
            elif isinstance(x, dict):
                out.append((event, dict(x)))
    return out


def error_states(states: dict, contract: dict | None = None) -> set[str]:
    declared = {n for n, b in states.items()
                if isinstance(b, dict) and str((b or {}).get("type", "")).lower() == "error"}
    heuristic = {n for n in states if "error" in n.lower() or "fail" in n.lower()}
    from_contract = {r.get("state") for r in (contract or {}).get("recovery", []) if r.get("state")}
    return declared | heuristic | from_contract


def check(sc: dict, contract: dict | None = None) -> list[str]:
    fails: list[str] = []
    states: dict = sc.get("states", {})
    initial = sc.get("initial")
    if initial not in states:
        return [f"C1 initial '{initial}' is not in states"]
    edges: dict[str, list[str]] = {}
    for name, body in states.items():
        on = (body or {}).get("on", {}) or {}
        out: list[str] = []
        for event, tr in norm_transitions(on):
            tgt = tr.get("target")
            if tgt is None:
                if isinstance(tr, dict) and "target" not in tr:
                    if "guard" in tr and not tr.get("guardDesc"):
                        fails.append(f"C5 guard '{tr['guard']}' on the '{name}' transition has no guardDesc")
                    continue
                tgt = ""  # "target": null — an explicit empty target, treated as dangling
            out.append(tgt)
            if tgt not in states:
                fails.append(f"C6 reference integrity: '{name}' event {event} targets nonexistent state '{tgt}'")
            if isinstance(tr, dict) and "guard" in tr and not tr.get("guardDesc"):
                fails.append(f"C5 guard '{tr['guard']}' on the '{name}' transition has no guardDesc")
        edges[name] = out
        if name not in ("final",) and not (body or {}).get("type") == "final" and not out:
            fails.append(f"C2 dead end: state '{name}' has no outgoing edges")
    seen, q = {initial}, deque([initial])
    while q:
        for t in edges.get(q.popleft(), []):
            if t in states and t not in seen:
                seen.add(t)
                q.append(t)
    for name in states:
        if name not in seen:
            fails.append(f"C3 unreachable: state '{name}' cannot be reached from initial")
    est = error_states(states, contract)
    for name in sorted(est):
        if name not in states:
            continue
        recover = [t for t in edges.get(name, []) if t not in est]
        if not recover:
            fails.append(f"C4 error state '{name}' has no recovery transition (no way out)")
    if contract is not None:
        fails += reconcile(states, contract)
    return fails


def contract_c7_hint(contract: dict) -> str | None:
    """A reminder for --contract present with no recovery rows (passing the statechart
    itself as the contract is legal JSON with rows = ∅ → C7 reverse reports every
    error-state out-edge as "unregistered", which looks like a project defect but is a
    run mistake; or recovery still lives in a markdown human contract — brownfield
    projects should faithfully transcribe contract.json first, then run C7).
    Never a FAIL: a contract with no error-exit promises is a legal shape; intent is not
    machine-checkable."""
    if contract.get("recovery"):
        return None
    return ("Reminder: --contract is present but has no recovery rows — C7 reverse reconciliation "
            "will report every error-state out-edge as unregistered. Confirm this is not the wrong file "
            "(e.g. the statechart itself passed as the contract), and that recovery is not still living in a "
            "markdown human contract (brownfield: faithfully transcribe contract.json first, then run C7).")


# markdown recovery probe: error-state semantics often live in a markdown human contract —
# the exceptions-and-recovery section of a design doc — a natural blind window for C7.
# Hit criteria (either): a heading line with semantic-word × state-domain-word co-occurrence
# (a single-word criterion measured high false positives — ops "backup recovery", monitoring
# "exception detection", debugging headings — hence the tightening) | a table header row
# containing a recovery column (separator-line lookahead prevents data-row false hits).
RECOVERY_TITLE = re.compile(
    r"^#{1,6}\s(?=.*\b(?:recovery|recover\w*|error\w*|fail\w*|exception\w*|retry\w*|fallback\w*)\b)"
    r"(?=.*\b(?:states?|statechart|transition\w*|matrix|tables?)\b)", re.IGNORECASE)
RECOVERY_COL = re.compile(r"recover(?:y|ies)?\b", re.IGNORECASE)
TABLE_SEP = re.compile(r"^\s*\|[\s:|-]+\|\s*$")
PROBE_SKIP = re.compile(r"(node_modules|\.git[\\/]|dist|build|\.next)")
PROBE_MD_LIMIT, PROBE_HEAD_LIMIT = 200, 65536


def probe_recovery_md(root: str | Path) -> list[tuple[str, str]]:
    """Scan a directory for markdown docs with suspected recovery semantics; return
    (path, hit evidence). Remind only, never fail: a markdown contract present is a legal,
    common brownfield shape — the value is steering a faithful transcription into
    contract.json."""
    hits: list[tuple[str, str]] = []
    p = Path(root)
    if not p.is_dir():
        return hits
    md_files = [f for f in p.rglob("*.md") if not PROBE_SKIP.search(str(f))]
    for f in md_files[:PROBE_MD_LIMIT]:
        try:
            head = f.read_text(encoding="utf-8", errors="replace")[:PROBE_HEAD_LIMIT]
        except OSError:
            continue
        lines = head.splitlines()
        for i, line in enumerate(lines):
            if RECOVERY_TITLE.match(line):
                hits.append((str(f), f"title: {line.strip()[:48]}"))
                break
            if line.lstrip().startswith("|") and RECOVERY_COL.search(line) \
                    and i + 1 < len(lines) and TABLE_SEP.match(lines[i + 1]):
                hits.append((str(f), f"recovery column header: {line.strip()[:48]}"))
                break
    return hits


def reconcile(states: dict, contract: dict) -> list[str]:
    """C7: contract recovery rows ↔ statechart transitions, two-way reconciliation
    (a missing edge = a promise with nowhere to land / an extra edge = an unregistered
    invention)."""
    fails: list[str] = []
    rows = contract.get("recovery", []) or []
    registered = {(r.get("state"), r.get("action"), r.get("target")) for r in rows}
    for r in rows:
        st, act, tgt = r.get("state"), r.get("action"), r.get("target")
        if st not in states:
            fails.append(f"C7 forward: recovery row state '{st}' is not in the statechart (a promise with nowhere to land)")
            continue
        cand = [t for ev, td in norm_transitions((states[st] or {}).get("on", {}))
                if ev == act for t in [td.get("target")] if t is not None]
        if tgt not in cand:
            got = "/".join(cand) if cand else "no such event"
            fails.append(f"C7 forward: contract promise {st} --{act}--> {tgt} does not exist in the statechart (actual: {got})")
    allow = registered | {(r.get("state"), r.get("action"), r.get("target"))
                          for r in (contract.get("non_error_failures", []) or [])}
    for name in sorted(error_states(states, contract)):
        if name not in states:
            continue
        for ev, td in norm_transitions((states[name] or {}).get("on", {})):
            tgt = td.get("target")
            if tgt is not None and (name, ev, tgt) not in allow:
                fails.append(f"C7 reverse: error state '{name}' out-edge {ev}->{tgt} is unregistered "
                             "(an extra edge = an unregistered invention, or a missing recovery row)")
    return fails


def selftest() -> int:
    good = {"initial": "idle", "states": {
        "idle": {"on": {"GO": "parsing"}}, "parsing": {"on": {"DONE": "done", "FAIL": "error"}},
        "error": {"on": {"RETRY": "parsing"}}, "done": {"type": "final"}}}
    bad = {"initial": "idle", "states": {
        "idle": {"on": {"GO": "parsing"}}, "parsing": {"on": {"DONE": "done", "FAIL": "error"}},
        "error": {"on": {}}, "ghost": {"on": {"X": "idle"}}, "done": {"type": "final"}}}
    ok1 = check(good) == []
    f = check(bad)
    ok2 = any("C4" in x for x in f) and any("C3" in x for x in f)

    # C6 reference integrity: a dangling target must be flagged
    dangling = {"initial": "idle", "states": {
        "idle": {"on": {"GO": "nowhere"}}, "done": {"type": "final"}}}
    f6 = check(dangling)
    ok6 = any("C6" in x for x in f6) and any("nowhere" in x for x in f6)

    # declared error state: recognizable even when the name has no error/fail ("type": "error")
    c4_decl = {"initial": "idle", "states": {
        "idle": {"on": {"GO": "denied"}}, "denied": {"type": "error", "on": {}}}}
    ok_c4 = any("C4" in x and "denied" in x for x in check(c4_decl))

    # C7 forward: a contract row missing from the graph → flagged
    contract = {"recovery": [{"state": "error", "action": "RETRY", "target": "parsing"}],
                "non_error_failures": [{"state": "parsing", "action": "FAIL", "target": "error"}]}
    ok7f = check(good, contract) == []
    broken = {"initial": "idle", "states": {
        "idle": {"on": {"GO": "parsing"}}, "parsing": {"on": {"DONE": "done", "FAIL": "error"}},
        "error": {"on": {"ABORT": "idle"}}, "done": {"type": "final"}}}
    f7a = check(broken, contract)
    ok7a = any("C7 forward" in x and "RETRY" in x for x in f7a)

    # C7 reverse: an extra unregistered error-state out-edge → flagged
    extra = {"initial": "idle", "states": {
        "idle": {"on": {"GO": "parsing"}}, "parsing": {"on": {"DONE": "done", "FAIL": "error"}},
        "error": {"on": {"RETRY": "parsing", "SECRET": "idle"}}, "done": {"type": "final"}}}
    f7b = check(extra, contract)
    ok7b = any("C7 reverse" in x and "SECRET" in x for x in f7b)

    ok = all([ok1, ok2, ok6, ok_c4, ok7f, ok7a, ok7b])

    # run hint: --contract without recovery rows → hint present; a normal contract → no hint
    hint_bad = contract_c7_hint({"contract_version": "0.2.6", "states": {}})
    hint_good = contract_c7_hint({"recovery": [{"state": "error", "action": "RETRY", "target": "parsing"}]})
    ok_hint = hint_bad is not None and "recovery" in hint_bad and hint_good is None
    ok = ok and ok_hint

    # markdown probe: title hit + node_modules excluded + ordinary README zero hits + bare header hit
    import tempfile
    ok_p1 = ok_p2 = ok_p3 = False
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        (tdp / "node_modules").mkdir()
        (tdp / "node_modules" / "x.md").write_text("## Error states and recovery transitions\n", encoding="utf-8")
        (tdp / "interaction-design.md").write_text(
            "# Interaction design\n\n## 4 States and exceptions master table\n\n"
            "| Scenario | Display | Recovery |\n|---|---|---|\n| empty warehouse | guide card | guide |\n",
            encoding="utf-8")
        hits = probe_recovery_md(td)
        ok_p1 = len(hits) == 1 and "interaction-design" in hits[0][0] and "title" in hits[0][1]
        with tempfile.TemporaryDirectory() as td2:
            (Path(td2) / "README.md").write_text("# Project\n\nInstall and usage guide. Great performance.\n", encoding="utf-8")
            ok_p2 = probe_recovery_md(td2) == []
        with tempfile.TemporaryDirectory() as td3:
            (Path(td3) / "bare-table.md").write_text(
                "# Module\n\n| State | Action | Recovery target |\n|---|---|---|\n| offline | RECONNECT | online |\n",
                encoding="utf-8")
            h3 = probe_recovery_md(td3)
            ok_p3 = len(h3) == 1 and "header" in h3[0][1]
    ok = ok and ok_p1 and ok_p2 and ok_p3
    print(f"selftest: valid chart pass={ok1} C2/C3/C4 blocked={ok2} C6 dangling target blocked={ok6} "
          f"declared error state C4 blocked={ok_c4} C7 forward missing edge blocked={ok7a} "
          f"C7 reverse extra edge blocked={ok7b} contract-consistent pass={ok7f} no-recovery hint={ok_hint} "
          f"probe title hit+exclusion={ok_p1} ordinary doc zero hits={ok_p2} bare recovery header hit={ok_p3} "
          f"→ {'PASS' if ok else 'FAIL'}")
    if not ok:
        print("  detail:", {"basic_bad": f, "c6": f6, "c7_forward": f7a, "c7_reverse": f7b,
                            "probe": {"p1": ok_p1, "p2": ok_p2, "p3": ok_p3}})
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("statechart", nargs="?", help="statechart JSON (positional, for bare-path invocation)")
    ap.add_argument("--file", dest="file_opt")
    ap.add_argument("--contract", help="contract JSON (recovery / non_error_failures); enables C7 two-way reconciliation")
    ap.add_argument("--probe-recovery", dest="probe_recovery",
                    help="probe the directory for markdown with suspected recovery semantics (remind, never fail; "
                         "steers a faithful transcription into contract.json)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.probe_recovery:
        root = Path(a.probe_recovery)
        if not root.is_dir():
            print(f"FAIL: --probe-recovery directory does not exist: {a.probe_recovery}")
            return 1
        hits = probe_recovery_md(root)
        if not hits:
            print("PROBE: no markdown with suspected recovery semantics found "
                  "(scan = recursive *.md, excluding node_modules/.git/dist/build, cap 200 files).")
            return 0
        print(f"PROBE: {len(hits)} markdown file(s) with suspected recovery semantics "
              "(error-state semantics living in a human contract = C7 reconciliation input missing):")
        for pth, why in hits:
            print(f"  ✗ {pth}")
            print(f"      ←{why}")
        print("Reminder: a markdown contract is not a machine-readable C7 input — faithfully transcribe the "
              "recovery key into contract.json ((state, action, target) rows) and rerun C7; this probe only "
              "reminds, never fails; transcription intent needs human review.")
        return 0
    # the positional path form is accepted for invocation compatibility
    a.file = a.file_opt or a.statechart
    if not a.file:
        print("FAIL: a statechart path (positional or --file) or --selftest is required")
        return 1
    sc = json.loads(Path(a.file).read_text(encoding="utf-8"))
    contract = json.loads(Path(a.contract).read_text(encoding="utf-8")) if a.contract else None
    hint = contract_c7_hint(contract) if contract is not None else None
    fails = check(sc, contract)
    if fails:
        if hint:
            print(hint)
        print(f"FAIL: {len(fails)} structural defects:")
        for x in fails:
            print("  ✗", x)
        return 1
    scope = "with C7 contract reconciliation" if contract else "no contract (C7 disabled)"
    print(f"OK: statechart structure check passed (no dead ends / fully reachable / error states have exits / "
          f"references intact; {scope})")
    if hint:
        print(hint)
    return 0


if __name__ == "__main__":
    sys.exit(main())
