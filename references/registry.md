# registry · the component registry (pure checker: defines no components; only checks "was the table consulted, was attribution made")

> Themes and components are never defined here — component content belongs entirely to upstream libraries (shadcn / Radix / the project's own inventory). This file does two things: ① **register** the project's settled components and their usage points (the map); ② be consumed by `registry-gate.py` for **attribution checks** (self-built requires an attribution; the check verifies the table was consulted).

## Row schema
`component | responsibility (one sentence) | source (upstream library + version / self-built + attribution link) | typical usage points | status (in use / retired → replacement + reason)`

## Two views
- **Capability index** (read at design time): category level — which capabilities the project has, which it lacks (guards against phantom ideas and forced fits).
- **Component card** (read at build time): API level — concrete usage / props / source attribution.

## Registration flow
When a new component lands: one registry row (name / responsibility / source / usage points) + an attribution comment in the code (`<!-- registry: <name> self-built-attribution=<why the upstream cannot solve this> -->` or `registry: <name> source=<upstream-lib@version>`) — registry-gate checks via this marker.

## Retirement discipline
A retired component's row is never deleted: set status to "retired → replacement=<new component> + reason" — the provenance chain survives (references in old code stay traceable).

## Adopting in a legacy project (baseline mode)
First adoption on an existing codebase: `python registry-gate.py --path <component-dir> --write-baseline` — the inventory at that moment becomes the baseline (legacy exempt, not retroactive); from then on only "new components outside the baseline without attribution" are flagged. The baseline file `.registry-baseline.json` goes into git with the project (the team shares one exemption surface).
