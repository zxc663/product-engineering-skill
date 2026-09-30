#!/usr/bin/env python3
"""usage-probe · usage monitor v0 (the decay-chain countermeasure: installed but never
triggered = installed for nothing, and nobody would know).

Scans the given agent-log file(s) or directories and counts traces of the
product-engineering skill being mentioned / referenced, plus the most recent hit time.
Honest boundary v0: this counts text mentions, not platform-level real triggers — real
trigger monitoring v1 needs a platform hooks channel.
Usage: python usage-probe.py --logs <log file or dir> [--days 7]
       python usage-probe.py --selftest
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

HINTS = ["product-engineering", "product-engineering-skill", "product skill",
         "six questions", "statechart-gate", "registry-gate", "spec-trace"]
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def scan(paths: list[Path], days: int) -> dict:
    cutoff = datetime.now() - timedelta(days=days)
    hits: list[datetime] = []
    per_file: dict[str, int] = {}
    for f in paths:
        if f.is_dir():
            paths.extend(sorted(f.rglob("*.md")))
            continue
        if not f.is_file():
            continue
        n = 0
        for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
            if any(h in line for h in HINTS):
                n += 1
                m = DATE_RE.search(line)
                if m:
                    try:
                        d = datetime.strptime(m.group(1), "%Y-%m-%d")
                        if d >= cutoff:
                            hits.append(d)
                    except ValueError:
                        pass
        if n:
            per_file[str(f)] = n
    return {"total_mentions": sum(per_file.values()), "recent_hits": len(hits),
            "files": per_file, "last_hit": max(hits).strftime("%Y-%m-%d") if hits else "—"}


def selftest() -> int:
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        log = Path(d) / "agent-log.md"
        log.write_text("### 2026-09-21 | some round: six questions used\n"
                       "plain line\n"
                       "### 2026-09-10 | statechart-gate ran\n", encoding="utf-8")
        r = scan([log], days=30)
        ok = r["total_mentions"] == 2 and r["recent_hits"] >= 1 and r["last_hit"] == "2026-09-21"
        print(f"selftest: mention count + in-window hits + last hit={ok} ({r})")
        return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--logs", nargs="*")
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.logs:
        print("FAIL: --logs or --selftest required")
        return 1
    paths: list[Path] = [Path(p) for p in a.logs]
    r = scan(paths, a.days)
    print(f"usage report (last {a.days} days): {r['total_mentions']} mention(s) / "
          f"{r['recent_hits']} in-window hit(s) / last {r['last_hit']}")
    for k, v in sorted(r["files"].items(), key=lambda x: -x[1])[:8]:
        print(f"  {v:4d}  {k}")
    if r["recent_hits"] == 0:
        print("⚠ zero in-window hits — the skill is decaying (decay chain level 1); check hooks/deployment")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
