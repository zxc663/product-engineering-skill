#!/usr/bin/env python3
"""l0-l5-gate · goal-quality line + information-architecture floor (the machine-checkable
subset of stack layers L0 and L5).

Checks statement/artifact shape only — it never produces goals or designs
(PE≠PI: shape compliance is machine-checkable; whether the content is right is a
product decision on the human side).

Input artifact schemas:
goal.json (goal artifact; missing = immediate fail, L0-C10)
{
  "north_star": "primary-result statement (exactly 1; a list must have length 1)",  // L0-C1/C11/C12
  "key_results": ["KR1", "KR2", ...],                                               // L0-C4 form / C5 time window / C6 count
  "jobs": ["verb + object + context qualifier", ...]                                // optional; L0-C7 shape check when present
}
ia.json (information-architecture doc, optional; L5 is checked only when provided)
{
  "organization": "topic|task|user|format|time (primary organization scheme)",      // L5-C1
  "global_nav": true, "local_nav": true, "local_nav_exempt": "reason",              // L5-C3 trio
  "location_indicator": true,                                                       // L5-C3 current location
  "routes": [{"path": "/x", "has_global_nav": true}],                               // L5-C5 front-door reachability
  "pages": [{"path": "/x", "exits": 2, "terminal": false}],                         // L5-C10 dead-end pages (isomorphic to L7 no-dead-end)
  "find_paths": ["browse", "search"],                                               // L5-C6 find-path variety
  "tree_tests": [{"task": "...", "correct_leaf": "...", "success_rate": 0.8, "directness": 0.6}]  // L5-C11
}

Checks (fail = exit 1; warning = a W-prefixed line, exit 0):
  L0-C10 goal artifact exists and parses (fail)
  L0-C1  primary-result statement exactly 1 (≥2 with no primary marked = fail; 0 = fail)
  L0-C12 primary metric has a measurement form (number/comparison wording; none = fail)
  L0-C5  every KR has a time window (date/quarter/relative-period form; missing = fail)
  L0-C4  KR binary-decidability pre-screen (number + comparison form; shape doubtful = warning, human review)
  L0-C6  KR count 3-5 (outside = warning; the whatmatters.com convention, deliberately not a fail)
  L0-C13 vanity-metric wording as the primary metric (warning + human adjudication; cumulative
         volume can be legitimate for infrastructure products)
  L0-C7  job-statement three-part shape pre-screen (<3 parts = warning)
  L5-C3  navigation trio (global / local / location indicator; missing without exemption = fail)
  L5-C5  front-door reachability (a route without global nav = orphan page = fail)
  L5-C10 dead-end page (exits=0 and not terminal = fail)
  L5-C6  find-path variety ≥2 (=1 = warning)
  L5-C1  organization scheme declared (missing = warning)
  L5-C11 tree-testing report existence + four elements (task/correct_leaf/success_rate/directness;
         missing = warning; no hard-coded industry thresholds — none are widely accepted; the
         project sets its own thresholds and records them)

Usage: python l0-l5-gate.py --goal goal.json [--ia ia.json]
       python l0-l5-gate.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TIME_WINDOW = re.compile(
    r"\d{4}-\d{2}|\d{4}-\d{2}-\d{2}|\bQ[1-4]\b|\bQ[1-4]\s*\d{4}"
    r"|\d+\s*(?:day|days|week|weeks|month|months|quarter|quarters|year|years)\b"
    r"|(?:by|before|within)\s+(?:the\s+)?end\s+of\s+(?:Q[1-4]|\d{4})"
    r"|\bby\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*[^)]*\d{4}"
    r"|\bwithin\s+\d+\s*(?:business\s+)?(?:day|week|month|quarter|year)s?\b", re.IGNORECASE)
METRIC_FORM = re.compile(
    r"\d|≥|≤|>|<|%|\b(?:improve|improvement|reduce|reduction|reach|increase|decrease|grow|growth"
    r"|achieve|maintain|ratio|rate|percent(?:age)?|count|per\s+(?:user|week|day|month))\b", re.IGNORECASE)
# C13: beyond the bare vanity-noun list, also catch the "cumulative/total + volume noun"
# combination; quality metrics such as "cumulative success rate" stay out of the list (legitimate)
VANITY = re.compile(
    r"\btotal\s+(?:registered\s+)?(?:users|downloads|page\s?views|visits|sign-?ups)\b"
    r"|\bcumulative\s+(?:registered\s+)?users\b"
    r"|\b(?:cumulative|total|aggregate)\s+\w{0,12}?\s*(?:count|executions?|completions?|processed"
    r"|clicks|views|visits|hours|time)\b", re.IGNORECASE)
JOB_FORM = re.compile(
    r"\b\w+\s+\w+\s+(?:while|during|when|whenever|for|without)\s+\w+", re.IGNORECASE)


def _as_bool(v) -> bool:
    """Only genuine boolean-true wordings count; the string "false"/"0"/"no" and any other
    non-boolean shape must not slip through on Python truthiness."""
    if isinstance(v, bool):
        return v
    return isinstance(v, str) and v.strip().lower() in ("true", "yes", "1")


def _as_int_or_none(v):
    """Non-numeric shapes parse as None → treated conservatively as 0 (a string "0"
    must not escape the dead-end comparison)."""
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v
    s = str(v).strip() if isinstance(v, str) else ""
    return int(s) if s.lstrip("-").isdigit() else None


def check_goal(goal: dict) -> tuple[list[str], list[str]]:
    fails: list[str] = []
    warns: list[str] = []
    ns = goal.get("north_star")
    if ns is None:
        # key absent ≠ legitimate — it used to fall through every check silently
        fails.append("L0-C1/C10 north_star missing (key absent) — the goal was never stated")
    elif isinstance(ns, list):
        if len(ns) == 0:
            fails.append("L0-C1/C10 north_star empty — the goal was never stated")
        elif len(ns) > 1:
            fails.append(f"L0-C1/C11 north_star has {len(ns)} entries with no primary marked (single-value rule)")
        else:
            ns = ns[0]
    if isinstance(ns, str):
        if not ns.strip():
            fails.append("L0-C1/C10 north_star empty")
        elif VANITY.search(ns):
            warns.append(f"L0-C13 primary metric looks like a vanity/cumulative metric ({ns}) — "
                         "warning: legitimate for infrastructure products; human adjudication required")
        elif not METRIC_FORM.search(ns):
            fails.append(f"L0-C12 primary metric has no measurement form ({ns}) — an unmeasurable goal cannot be judged")
    elif ns is not None:
        # reverse mutation: a numeric north_star once slipped past every string-typed check
        fails.append(f"L0-C1/C10 north_star has an invalid type ({type(ns).__name__}) — "
                     "must be a string or a single-element array")
    krs = goal.get("key_results") or []
    if krs:
        for i, kr in enumerate(krs, 1):
            if not TIME_WINDOW.search(str(kr)):
                fails.append(f"L0-C5 KR {i} has no time window ({kr}) — not time-bound")
            elif not METRIC_FORM.search(str(kr)):
                warns.append(f"L0-C4 KR {i} has no numeric/comparison form ({kr}) — "
                             "human review: is it binary-decidable?")
        if not (3 <= len(krs) <= 5):
            warns.append(f"L0-C6 KR count {len(krs)} outside the 3-5 convention "
                         "(warning: a deliberately minimal single-metric goal may be explicitly adjudicated)")
    jobs = goal.get("jobs") or []
    for j in jobs:
        if len(str(j).split()) < 2 and not JOB_FORM.search(str(j)):
            warns.append(f"L0-C7 job-statement shape questionable ({j}) — verb + object + context qualifier")
    return fails, warns


def check_ia(ia: dict) -> tuple[list[str], list[str]]:
    fails: list[str] = []
    warns: list[str] = []
    if not str(ia.get("organization", "")).strip():
        warns.append("L5-C1 organization scheme missing (primary classification dimension: topic/task/user/format/time)")
    g, l, li = ia.get("global_nav"), ia.get("local_nav"), ia.get("location_indicator")
    exempt = str(ia.get("local_nav_exempt", "")).strip()
    missing = [n for n, v in (("global nav", g), ("local nav", l), ("location indicator", li)) if not _as_bool(v)]
    if "local nav" in missing and exempt:
        missing.remove("local nav")
    if missing:
        fails.append(f"L5-C3 navigation trio incomplete: {', '.join(missing)} (no exemption on file)")
    routes = ia.get("routes") or []
    orphans = [r.get("path", "?") for r in routes if not _as_bool(r.get("has_global_nav"))]
    if orphans:
        fails.append(f"L5-C5 front-door reachability failed: orphan routes {orphans} "
                     "(≥half of visits never pass the home page; every route must reach a global nav)")
    pages = ia.get("pages") or []
    dead = [p.get("path", "?") for p in pages
            if (_as_int_or_none(p.get("exits")) or 0) == 0 and not _as_bool(p.get("terminal"))]
    if dead:
        fails.append(f"L5-C10 dead-end pages {dead} (isomorphic to L7 no-dead-end: zero exits and not terminal)")
    fp = ia.get("find_paths") or []
    if len(fp) == 1:
        warns.append("L5-C6 find-path variety is 1 (the multiple-classification principle suggests ≥2: browse + search/filter)")
    tt = ia.get("tree_tests") or []
    if isinstance(tt, str) and tt.strip():
        # a text reference counts as "a report exists" (no missing-report warning) but its
        # elements are not machine-checkable; iterating it character-by-character used to
        # crash the whole IA check inside the outer except
        warns.append("L5-C11 tree_tests is a text reference (elements not machine-checkable); "
                     "record it structurally (task/correct_leaf/success_rate/directness)")
    elif not tt:
        warns.append("L5-C11 no tree-testing report — test ≥3 key navigation tasks (artifact existence)")
    else:
        for t in tt:
            for k in ("task", "correct_leaf", "success_rate", "directness"):
                if k not in t:
                    warns.append(f"L5-C11 tree-testing report missing element {k} (task: {t.get('task', '?')})")
    return fails, warns


def selftest() -> int:
    goal_ok = {"north_star": "raise personal monthly savings rate to 20%+ (by 2026-12)",
               "key_results": ["savings rate from 8% to 20% (by 2026-12)",
                               "30-day bookkeeping retention ≥60% (Q4 2026)",
                               "weekly active usage ≥3 sessions/user (2026-12)"]}
    ia_ok = {"organization": "by topic", "global_nav": True, "local_nav": True,
             "location_indicator": True,
             "routes": [{"path": "/home", "has_global_nav": True},
                        {"path": "/archive", "has_global_nav": True}],
             "pages": [{"path": "/home", "exits": 3}, {"path": "/archive", "exits": 2}],
             "find_paths": ["browse", "search"],
             "tree_tests": [{"task": "find the 2025 article", "correct_leaf": "/archive/2025",
                             "success_rate": 0.85, "directness": 0.6}]}
    f1, w1 = check_goal(goal_ok)
    f2, w2 = check_ia(ia_ok)
    ok1 = f1 == [] and f2 == []
    g_bad = {"north_star": ["metric A", "metric B"], "key_results": ["improve experience"]}
    f3, _ = check_goal(g_bad)
    ok2 = any("L0-C1" in x for x in f3) and any("L0-C5" in x for x in f3)
    g_nokey = {"key_results": ok_goal_krs()}  # file present, north_star key absent → must fail
    f6, _ = check_goal(g_nokey)
    ok5 = any("L0-C1" in x and "missing" in x for x in f6)
    g_vanity = {"north_star": "total registered users exceed ten thousand", "key_results": ok_goal_krs()}
    f4, w4 = check_goal(g_vanity)
    ok3 = any("L0-C13" in x for x in w4) and not any("L0-C12" in x for x in f4)
    ia_bad = {"routes": [{"path": "/lost", "has_global_nav": False}],
              "pages": [{"path": "/trap", "exits": 0}]}
    f5, w5 = check_ia(ia_bad)
    ok4 = any("L5-C5" in x for x in f5) and any("L5-C10" in x for x in f5) and any("L5-C3" in x for x in f5)
    # reverse mutations (each is a shape that once slipped past)
    g_ll1 = {"north_star": 123, "key_results": ok_goal_krs()}  # numeric ns once fell through silently
    f_ll1, _ = check_goal(g_ll1)
    ok6 = any("invalid type" in x for x in f_ll1)
    ia_ll2 = {"organization": "by task", "global_nav": "false", "local_nav": True, "location_indicator": True,
              "routes": [{"path": "/x", "has_global_nav": "false"}],  # string "false" truthiness escape
              "pages": [{"path": "/y", "exits": "0"}]}  # string "0" escaping the dead-end comparison
    f_ll2, _ = check_ia(ia_ll2)
    ok7 = any("L5-C3" in x for x in f_ll2) and any("L5-C5" in x for x in f_ll2) and any("L5-C10" in x for x in f_ll2)
    # a tree_tests text reference must not crash the check; the other L5 checks must not be swallowed
    ia_ll4 = {"organization": "by task", "global_nav": True, "local_nav": True, "location_indicator": True,
              "routes": [{"path": "/a", "has_global_nav": False}],
              "pages": [{"path": "/a", "exits": 0}],
              "find_paths": ["browse", "search"],
              "tree_tests": "2026-09 navigation test, 3/3 tasks passed"}
    f_ll4, w_ll4 = check_ia(ia_ll4)
    ok8 = (any("L5-C5" in x for x in f_ll4) and any("L5-C10" in x for x in f_ll4)
           and any("L5-C11" in x and "text reference" in x for x in w_ll4))
    # C13 combination form: cumulative × volume noun hits; a quality metric ("cumulative success rate") passes
    g_van2 = {"north_star": "cumulative execution count over one hundred thousand", "key_results": ok_goal_krs()}
    _, w_v2 = check_goal(g_van2)
    g_van3 = {"north_star": "cumulative focus time over one thousand hours", "key_results": ok_goal_krs()}
    _, w_v3 = check_goal(g_van3)
    g_van_neg = {"north_star": "data backup cumulative success rate ≥99% (by 2026-12)", "key_results": ok_goal_krs()}
    f_vn, w_vn = check_goal(g_van_neg)
    ok9 = (any("L0-C13" in x for x in w_v2) and any("L0-C13" in x for x in w_v3)
           and not any("L0-C13" in x for x in w_vn) and not f_vn)
    print(f"selftest: valid goal+IA pass={ok1} multi-NS/no-time-window blocked={ok2} "
          f"vanity=warning-not-fail={ok3} orphan/dead-end/trio blocked={ok4} missing-key blocked={ok5} "
          f"reverse numeric-ns={ok6} string-false/zero={ok7} text-reference-no-crash={ok8} "
          f"C13-combo/quality-metric-pass={ok9} (warning baseline {len(w1)+len(w2)+len(w4)+len(w5)+len(w_ll4)})")
    return 0 if ok1 and ok2 and ok3 and ok4 and ok5 and ok6 and ok7 and ok8 and ok9 else 1


def ok_goal_krs() -> list[str]:
    return ["sign-up conversion ≥30% (by 2026-12)", "next-month retention ≥40% (Q4 2026)",
            "acquisition cost ≤$10 per user (by 2026-12)"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--goal", help="goal artifact JSON (schema in the file header)")
    ap.add_argument("--ia", help="information-architecture doc JSON (optional)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.goal:
        print("FAIL: --goal or --selftest required")
        return 1
    gp = Path(a.goal)
    if not gp.exists():
        print("FAIL: L0-C10 goal artifact does not exist — the goal was never stated "
              "(stop and backfill; do not ghostwrite: PE≠PI)")
        return 1
    try:
        goal = json.loads(gp.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"FAIL: L0-C10 goal artifact not parseable ({e})")
        return 1
    fails: list[str] = []
    warns: list[str] = []
    f, w = check_goal(goal if isinstance(goal, dict) else {})
    fails += f
    warns += w
    if a.ia:
        ip = Path(a.ia)
        if not ip.exists():
            print(f"W L5 artifact path does not exist: {a.ia} (treated as not provided)")
        else:
            try:
                ia = json.loads(ip.read_text(encoding="utf-8"))
                f2, w2 = check_ia(ia if isinstance(ia, dict) else {})
                fails += f2
                warns += w2
            except Exception as e:  # noqa: BLE001
                # a damaged IA doc must count as a defect (exit 1), not as "not provided" —
                # fail-open here silently skipped every L5 check
                fails.append(f"L5 IA doc is present but not parseable ({e}) — "
                             "a damaged artifact counts as a defect, not as not-provided")
    for x in warns:
        print("W", x)
    if fails:
        print(f"FAIL: {len(fails)} L0/L5 criteria defects:")
        for x in fails:
            print("  ✗", x)
        return 1
    print(f"OK: L0/L5 machine-checkable subset passed ({len(warns)} warnings above; semantic adjudication belongs to humans)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
