#!/usr/bin/env python3
"""product-object-gate · product-object definition check (the first machine-checkable
slice of upstream layers L1-L4).

Checks the product-object definition JSON (schema = references/product-object.md):
  P1 definition existence: purpose/responsibility non-empty; the responsibility sentence
     must open with a managerial verb (display/show openers forbidden — judgement table
     Domain J); capabilities non-empty and every entry has name+role.
  P2 primary-function uniqueness: main_function must point at one of the capabilities,
     and exactly one capability has role = core-task — a count ≠ 1 means "everything is
     there, nothing matters"; exit 1.
  P3 layer declaration + upstream-reference existence: layers.active non-empty; each of
     L1-L4 must declare an upstream entry in one of three forms — file:<path> (the file
     must exist and be non-empty) | brief:<note> (user-given) | adjudicated:<ruling>
     (explicit ruling); missing entries or dangling file references are reported per
     layer, exit 1.
  P4 operability: the operability array is non-empty and every entry has item+answer —
     a front-stage capability must have a management answer or an explicit ruling
     (otherwise it is a fake capability).
  P4-W coverage dimensions (warning level): operability that answers only one management
     dimension (e.g. source) while who-manages/permissions/backup-restore/fallback go
     unanswered — answering six-questions item ⑥ once is not answering it.

Relation to the layer gate: this gate is the machine spot-check for "upstream confirmed";
it does not replace run-step 0a layer placement (placement itself is a human adjudication
domain — see references/layer-stack.md).

Usage: python product-object-gate.py --file object.json
       python product-object-gate.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROLES = ("core-task", "business-op", "auxiliary", "advanced", "risky")
# banned opening verbs tolerate leading whitespace / brackets / quotes
BANNED_VERB_RE = re.compile(r"^[\s(\[{\"']*(?:display|show|present)\w*", re.IGNORECASE)
UPSTREAM_LAYERS = ("L1", "L2", "L3", "L4")
# P4-W: operability content dimensions (warning level — P4 blocks absence, this blocks
# "answered one dimension, counts as answered")
OPER_DIM = re.compile(
    r"\b(?:source|ingestion|admin|backend|permissions?|access|backup|restore|fallback|delete|export)\b",
    re.IGNORECASE)


def _clean_str(v) -> str:
    """Only str counts; non-str values (numbers/bools/None) return "" and trip the
    missing-value checks instead of slipping through via str() coercion."""
    return v.strip() if isinstance(v, str) else ""


def check(obj: dict, base: Path) -> list[str]:
    fails: list[str] = []
    purpose = _clean_str(obj.get("purpose"))
    responsibility = _clean_str(obj.get("responsibility"))
    caps = obj.get("capabilities") or []

    # P1 definition existence
    if not purpose:
        fails.append("P1 purpose missing (why it exists = six questions ①; non-empty str)")
    if not responsibility:
        fails.append("P1 responsibility missing (the responsibility sentence = six questions ②; non-empty str)")
    elif BANNED_VERB_RE.match(responsibility):
        m = re.match(r"[\s(\[{\"']*([A-Za-z]+)", responsibility)
        word = m.group(1) if m else responsibility[:10]
        fails.append(f"P1 responsibility opens with a display verb ('{word}') — use a managerial verb "
                     "(X manages/operates Y); display/show/present forbidden (judgement table Domain J)")
    if not caps:
        fails.append("P1 capabilities missing or empty (the capability list = six questions ③)")
    else:
        for c in caps:
            if not isinstance(c, dict) or not _clean_str(c.get("name")) or not _clean_str(c.get("role")):
                fails.append(f"P1 capability entry missing name/role: {c}")
            elif _clean_str(c.get("role")) not in ROLES:
                fails.append(f"P1 capability role '{c.get('role')}' is not in the enum {ROLES}")

    # P2 primary-function uniqueness
    main_fn = _clean_str(obj.get("main_function"))
    core = [str(c.get("name", "")).strip() for c in caps
            if isinstance(c, dict) and str(c.get("role", "")).strip() == "core-task"]
    if caps:
        if len(core) != 1:
            fails.append(f"P2 capabilities with role=core-task: {len(core)} (must be exactly 1) — "
                         "no primary function = 'everything is there, nothing matters'")
        if not main_fn:
            fails.append("P2 main_function missing/empty (an empty value once skipped the uniqueness check)")
        else:
            if main_fn not in {str(c.get("name", "")).strip() for c in caps if isinstance(c, dict)}:
                fails.append(f"P2 main_function '{main_fn}' is not among capabilities")
            if core and main_fn != core[0]:
                fails.append(f"P2 main_function '{main_fn}' mismatches the core-task capability '{core[0]}'")

    # P3 layer declaration + upstream-reference existence
    layers = obj.get("layers") or {}
    if not _clean_str(layers.get("active")):
        fails.append("P3 layers.active missing (layer gate 0a: declare this task's active layer)")
    upstream = layers.get("upstream") or {}
    for layer in UPSTREAM_LAYERS:
        if layer not in upstream:
            fails.append(f"P3 upstream {layer} has no confirmed source declared (layer gate 0b: unconfirmed means do not sink)")
            continue
        val = str(upstream[layer]).strip()
        if val.startswith("file:"):
            ref = base / val[5:].strip()
            if not ref.is_file() or ref.stat().st_size == 0:
                fails.append(f"P3 upstream {layer} file reference {val[5:].strip()} does not exist or is empty "
                             "(dangling upstream reference)")
        elif val.startswith(("brief:", "adjudicated:")):
            if len(val) <= len("brief:"):
                fails.append(f"P3 upstream {layer} {val.split(':', 1)[0]} note is empty")
        else:
            fails.append(f"P3 upstream {layer} value must start with file:/brief:/adjudicated:; got: {val[:40]}")

    # P4 operability
    oper = obj.get("operability") or []
    if not oper:
        fails.append("P4 operability missing or empty (six questions ⑥: who manages it / source / permissions / "
                     "fallback — or an explicit ruling: 'no backend this cycle' + who owns content)")
    else:
        for o in oper:
            if not isinstance(o, dict) or not _clean_str(o.get("item")) or not _clean_str(o.get("answer")):
                fails.append(f"P4 operability entry missing item/answer: {o}")
    return fails


def check_warnings(obj: dict) -> list[str]:
    warns: list[str] = []
    oper = obj.get("operability") or []
    if oper:
        blob = " ".join(_clean_str(o.get("item")) + " " + _clean_str(o.get("answer"))
                        for o in oper if isinstance(o, dict))
        dims = len(set(OPER_DIM.findall(blob)))
        if dims < 2:
            warns.append(f"P4-W operability covers only {dims} management dimension(s) ({blob.strip()[:40]}...) — "
                         "answer at least two of: who manages / source / permissions / backup-restore / fallback, "
                         "or adjudicate explicitly ('no backend this cycle' + who owns content)")
    return warns


def selftest() -> int:
    base = Path(".")
    good = {
        "purpose": "let the user manage saved items in one place; does not solve collaborative editing",
        "responsibility": "manages and operates the saved-item list",
        "capabilities": [{"name": "browse list", "role": "core-task"}, {"name": "export", "role": "auxiliary"}],
        "main_function": "browse list",
        "layers": {"active": "L6/L7",
                   "upstream": {"L1": "brief: given in the user task brief", "L2": "brief: 8 capabilities listed",
                                "L3": "brief: primary function specified",
                                "L4": "adjudicated: no backend this cycle; content is user-created"}},
        "operability": [{"item": "data source", "answer": "user-created"},
                        {"item": "backend", "answer": "adjudicated: no backend this cycle"}],
    }
    ok1 = check(good, base) == []

    bad_p1 = dict(good, purpose="", responsibility="displays saved data", capabilities=[])
    f_p1 = check(bad_p1, base)
    ok_p1 = sum(1 for x in f_p1 if x.startswith("P1")) >= 3

    bad_p2 = dict(good, capabilities=[
        {"name": "browse list", "role": "core-task"}, {"name": "quick save", "role": "core-task"},
        {"name": "export", "role": "auxiliary"}])
    bad_p2b = dict(good, main_function="quick save")
    ok_p2 = any("exactly 1" in x for x in check(bad_p2, base)) and any("mismatch" in x for x in check(bad_p2b, base))

    bad_p3 = dict(good, layers={"active": "L6",
                                "upstream": {"L1": "brief:x", "L2": "file:docs/ghost.md",
                                             "L4": "adjudicated: no backend"}})
    f_p3 = check(bad_p3, base)
    ok_p3 = (sum(1 for x in f_p3 if "L3" in x) >= 1
             and sum(1 for x in f_p3 if "L2" in x and "does not exist" in x) >= 1)

    bad_p4 = dict(good, operability=[])
    ok_p4 = any(x.startswith("P4") for x in check(bad_p4, base))

    # reverse mutations (each is a shape that once slipped past)
    bad_po1 = dict(good, main_function="")  # empty main_function once skipped the uniqueness check
    ok_po1 = any("main_function missing" in x for x in check(bad_po1, base))
    bad_po2 = dict(good, responsibility="(displays dashboard data)")  # bracket-wrapped opener once bypassed startswith
    ok_po2 = any("display/show" in x for x in check(bad_po2, base))
    bad_po3 = dict(good, purpose=123, layers=dict(good["layers"], active=6))  # numeric types slipping through str()
    f_po3 = check(bad_po3, base)
    ok_po3 = sum(1 for x in f_po3 if x.startswith("P1 purpose")) >= 1 and any("layers.active" in x for x in f_po3)
    bad_po4 = dict(good, capabilities=[{"name": "browse list", "role": "core-task"},
                                       {"name": "export", "role": "manager"}])  # role enum as dead code
    ok_po4 = any("not in the enum" in x for x in check(bad_po4, base))

    # P4-W: single-dimension operability → W; two or more dimensions → silent
    thin = dict(good, operability=[{"item": "data source", "answer": "user manual entry"}])
    w_thin = check_warnings(thin)
    ok_pw1 = len(w_thin) == 1 and "1 management dimension" in w_thin[0]
    full = dict(good, operability=[{"item": "data source", "answer": "user manual entry"},
                                   {"item": "delete permission", "answer": "owner only, restorable from trash"}])
    ok_pw2 = check_warnings(full) == []

    ok = all([ok1, ok_p1, ok_p2, ok_p3, ok_p4, ok_po1, ok_po2, ok_po3, ok_po4, ok_pw1, ok_pw2])
    print(f"selftest: valid definition pass={ok1} P1 existence/responsibility blocked={ok_p1} "
          f"P2 uniqueness blocked={ok_p2} P3 layer+upstream blocked={ok_p3} P4 operability blocked={ok_p4} "
          f"reverse PO1={ok_po1} PO2={ok_po2} PO3={ok_po3} PO4={ok_po4} "
          f"P4-W single-dim W/two-dim silent={ok_pw1}/{ok_pw2} → {'PASS' if ok else 'FAIL'}")
    if not ok:
        print("  detail:", {"p1": f_p1, "p2": check(bad_p2, base), "p3": f_p3,
                            "po1": check(bad_po1, base), "po2": check(bad_po2, base),
                            "po3": f_po3, "po4": check(bad_po4, base),
                            "pw1": w_thin})
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", help="product-object definition JSON (schema = product-object.md)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.file:
        print("FAIL: --file or --selftest required")
        return 1
    p = Path(a.file)
    obj = json.loads(p.read_text(encoding="utf-8"))
    for w in check_warnings(obj):
        print("W", w)
    fails = check(obj, p.resolve().parent)
    if fails:
        print(f"FAIL: {len(fails)} product-object defects:")
        for x in fails:
            print("  ✗", x)
        return 1
    print("OK: product-object definition check passed (definition exists / primary function unique / "
          "layer declaration + upstream references on file / operability answered)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
