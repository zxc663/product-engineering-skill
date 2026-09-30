English | [中文](README.zh.md)

# product-engineering

A skill that turns "build me a X page / tool / app" into **decidable contracts** — a layer gate, six product questions, a statechart, and machine-checkable acceptance gates — so the difference between a demo and a product is verified, not assumed.

It ships as a [skill](SKILL.md) (the runway an agent follows) plus nine self-testing gate scripts (the machine-checkable slice).

## What it checks

| Script | One-line role |
|---|---|
| `statechart-gate` | Every state has a way out: no dead ends, fully reachable, error states have recovery transitions, contract reconciliation both ways (C1–C7) |
| `spec-trace-gate` | Three-way binding traceability page ↔ component ↔ backend ↔ evidence: orphans, dead logic, ghost endpoints (T1–T6) |
| `product-object-gate` | The product object exists: exactly one primary function, layer declarations with upstream references, operability answered (P1–P4) |
| `l0-l5-gate` | Goal quality + IA floor: a measurable north star, time-bound key results, the navigation trio, no dead-end pages (L0/L5) |
| `registry-gate` | Every new component carries an attribution mark (`registry: … source=…` or a self-built reason); baseline mode exempts legacy |
| `frontend-lint-gate` | No inline styles / hardcoded colors / `console.*` / empty catch in components; list views get an empty-state branch (R1–R5) |
| `a11y-gate` | Static accessibility floor: `img` alt, accessible names on form controls and icon buttons, `html` lang (A1–A4) |
| `spec-trace-extract` | Extracts component/endpoint lists from code to feed `spec-trace-gate` |
| `usage-probe` | Counts skill mentions in agent logs — a decay monitor |

## Install

```bash
npx skills add zxc663/product-engineering-skill
```

## Run

Each gate is standalone and self-testing:

```bash
python scripts/statechart-gate.py --file sc.json --contract contract.json
python scripts/frontend-lint-gate.py --path src/components --write-baseline   # baseline exempts legacy, blocks new
python scripts/l0-l5-gate.py --goal goal.json --ia ia.json
```

All nine: `python scripts/<gate>.py --selftest`

## How it works

- [SKILL.md](SKILL.md) — the eight-step runway: layer gate → six questions → statechart → risk tiering → implement → acceptance.
- [references/](references/) — the detail layer: judgement table, layer stack, product object, interaction bridge, contract schema, and more. Loaded on demand.
- `scripts/` — the machine gates above. Detection is regex-level by design: low false positives, baseline adoption for brownfield repos.

## Honest limits

- The gates check **form, not semantics**: a passing statechart is not a correct statechart. Structural checks and domain review are both required.
- `a11y-gate` / `frontend-lint-gate` are low-false-positive static subsets — not axe-core, not a full lint setup.
- Baseline mode (`--write-baseline`) makes adoption into existing repos cheap (legacy exempt, new code blocked) — rebuild the baseline after refactors.
- A skill shapes agent behavior **probabilistically**; it is a guardrail, not a guarantee.
- This repo checks **English artifacts** (the judgement word lists are English). For Chinese-language projects, use the Chinese source package [`shisan-xinuo-product`](https://github.com/zxc663/shisan-xinuo-workflow) (same mechanisms, Chinese word lists).

## Contributing

Rules state the rule itself plus at most one sentence of why. Every script change must come with `--selftest` coverage including reverse samples (each bypass shape needs a test that would have caught it).

## License

[MIT](LICENSE)
