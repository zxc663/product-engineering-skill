# contract schema (Interaction / Gate / Evidence)

> Purpose: pin the scattered artifacts (six questions / statechart / spec-trace / gates / evidence / ledger) into **contracts an agent can consume, execute, verify, and inherit** — with a schema it is a specification layer; without one it is just methodology.
> **Hard/soft boundary (the core constraint of this file)**: hard layer = machine-decidable fields (states / transitions / permissions / recovery / gate inputs-outputs / evidence existence) — these can exit 1. Soft layer = reasons and trade-offs (intent / rejected candidates / rulings) — only traceability is required, and it lives in `decision-ledger.md`. **Do not JSON-ify the whole chain**: filling tables for their own sake is a token explosion and kills adoption.

## 1. Interaction Contract (hard layer)

Location: `docs/contracts/<feature>.json` (the statechart is the source; this contract references it; tables/matrices are rendered views).

| Field | Type | Meaning | Check |
|---|---|---|---|
| feature | string | The feature sentence (who / which scenario / accomplishes what) | non-empty |
| scope | tier 0–3 | §7 tier (per judgement-table §Risk tiers) | enum |
| promise | string[] | Promise list (one "what happens on click" per interactive element) | non-empty |
| six_questions | object | ①input ②timing ③success ④failure{prevent,recover,exit} ⑤undo{window,cost} ⑥persistence | **no blanks** (a missing item = interaction debt) |
| states / transitions / initial | — | Same as the statechart (≥3 states; single-state pieces exempt) | statechart-gate |
| permissions | string[] | Who may trigger each transition (mandatory where permission semantics exist) | mandatory at tier 3 |
| recovery | object[] | One exit row per error state; fields = `{state, action, target, note?}` (the spelling is the contract; gates read it as such) | mandatory at tier 3; **C7 forward reconciliation**: every row must hit the corresponding statechart transition (missing edge = promised but nonexistent, exit 1) |
| non_error_failures | object[] | Whitelist of failure exits named on non-error states (same fields; e.g. `loading --LOAD_FAIL--> empty`) | optional; **C7 reverse** exemption registry — registered explicitly, never silently waived |
| soft_ref | path | Points to the soft layer (intent / trade-offs / rulings → decision-ledger entries) | existence |

## 2. Gate Contract (hard layer)

Location: every `scripts/*-gate.py` self-describes via `--help` and `--selftest` output.

| Field | Meaning |
|---|---|
| gate_id | Gate name (registry / statechart / spec-trace / inline-style / dead-binding / a11y / …) |
| scope | Triggering tiers (tier 0–3, see judgement-table §Risk tiers) |
| check | One machine-decidable sentence of what is judged |
| input | Input shape (path / file / JSON) |
| output | pass/block + exit code (0/1) — **a criterion open to negotiation is not a gate** |
| evidence_required | Whether evidence existence is required (evidence-type gates) |
| selftest | `--selftest` both states (intercepting state + passing state) |

## 3. Evidence Contract (hard layer)

Location: the evidence column of the connected-rows list in design docs / delivery reports + the GATE `cmd/exit/files` triple attachment.

| Field | Meaning |
|---|---|
| feature / claim | The promise entry being verified (an Interaction Contract row) |
| evidence_type | render (screenshot) / dom (DOM dump) / command (rerunnable command + exit code) / log |
| artifact | Evidence path (inside the repo) or the verbatim command |
| produced_by / verified_at | Producer (session / gate) and timestamp |
| validity | Invalidation condition — **any change to that surface invalidates it**; old evidence never covers new changes |
| verdict | pass / fail / unverified (unverified must be explicit; defaulting to pass is forbidden) |

## 4. Mother architecture (unimplemented — do not impersonate)

The full Product Contracts chain = **Intent → Scope → Structure → Interaction → Runtime → Implementation → Verification**. This skill implements **Interaction only** (Gate/Evidence are its support pieces); every other domain is unimplemented and must be declared as such — methodology must not impersonate a schema. Roadmap: Intent/Structure next, Runtime after; Verification grows with the evidence system. This file describes only the three landed contracts; unimplemented domains get no fields (no table-filling for its own sake).

## 5. When to use

- **Any tier**: pass the level gate first (`references/layer-stack.md`): locate the layer → check upstream → pass / backfill.
- **Contracts with recovery rows**: run `statechart-gate.py --file <sc.json> --contract <contract.json>` to enable C7 bidirectional reconciliation (missing edge = promised but nonexistent; extra edge = invented but unregistered; both exit 1).
- **Tier 1**: answer orally; no files.
- **Tier 2**: Interaction Contract as JSON (statechart source) + Gate/Evidence flows exercised.
- **Tier 3**: all three contracts + recovery rows + runtime evidence + regression.
- Contract–implementation drift = a defect (written but not followed, or followed but not written, are both **fake connectivity**) — intercepted by the spec-trace bidirectional gate.
