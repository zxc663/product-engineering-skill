# interaction-bridge · bridging-layer details (three legitimate sources / six questions / translation table / floors and ceilings)

## 1. Three legitimate sources (where interaction logic comes from; conflict order: red lines > user mental model > feature derivation)

1. **User mental model (strongest source)**: industry conventions + the project's existing rulings. A convention is interaction logic pre-installed in the user's head; using it costs zero learning. The classic hostility mechanism is forcing the user to learn a new interaction for your implementation.
2. **Feature-semantics derivation**: interaction logic is not invented — it is the repayment of a debt the feature itself owes (the six questions).
3. **Red-line constraints**: way out / six states / promises / accessibility may not be violated.

**Illegitimate sources**: the component inventory (component-driven design — picking the control before the interaction — is a veto), model vibes, "looks cool".

## 1.5 Feature-surface inventory (runway step 1, expanded)

> Upstream: ① the **level gate first** (`references/layer-stack.md`, runway step 0a) — this file is an L6/L7 tool; L1–L4 must be confirmed before work starts (unconfirmed = level misplacement; stop and backfill). ② Before this inventory, pass the **product object's six questions** (`references/product-object.md`, runway step 0b) — **object-level definition precedes feature-level interaction**; with an incomplete capability list the inventory will necessarily miss surfaces.

Enumerate **every surface the user will see**, missing none of the five classes:
- **Primary function surfaces**: every function in the task description (one surface per independent component / tool / flow) — each atomic requirement in the brief enters the inventory table one by one and is reconciled against `capabilities[].name` (content-level traceability is a human walkthrough domain; a machine checker would be an NLP-matching false-positive machine — a missed row means both the implementation and the capability list are missing it, silently);
- **Auxiliary surfaces**: navigation / entries / home organization, help and explanation, about / version;
- **Boundary surfaces**: empty state (first open), error pages / error branches, loading and timeout, disabled / no-permission;
- **Environment surfaces**: mobile / narrow windows, weak network, dark mode, internationalization;
- **Management surface (fifth class)**: the content / data / state this feature depends on — who manages it and where: back-office configuration, review, enable/disable, ordering, defaults, fallback, audit. With no management path, an explicit ruling is required: "no back office this cycle + who curates the content" (see product-object.md §3).

A vague task description ≠ fewer surfaces — derive from the user journey (open → use → hit an error → come back), never from "how many things the task mentioned". A surface missed by the inventory loses its six questions and six states entirely.

## 2. The six birth questions of a feature (an engineering compression of Norman's seven stages and the two gulfs)

> Layer = L6 (interaction); upstream = L1–L4 (responsibility / capability / priority & completeness / operability) — **the six questions presuppose the feature itself is correctly decided**; if the premise fails, backfill first (layer-stack §2).

| # | Question | Where the answer lands | Disciplinary source | Confidence |
|---|---|---|---|---|
| ① | What goes in | Selectors / forms / drag-drop / import — affordances and signifiers | Norman, gulf of execution | source read |
| ② | When does it happen / how long | Progress / skeleton / optimistic update; **0.1 s instant / 1 s flow ceiling (beyond it, progress required) / 10 s attention ceiling (beyond it, cancelable)** | Nielsen response-time thresholds | reliably reported |
| ③ | What does success look like, where does it land | Success state + landing (which page it returns to / what gets highlighted) | Norman, gulf of evaluation | source read |
| ④ | How is failure prevented → how is it recovered once it slips through → the way out | Error prevention (constraints / validation timing) > recovery (retry / backfill) > way out (point to the action) | Nielsen #5 > #9 | reliably reported |
| ⑤ | Can it be undone, at what cost | Undo window / confirmation dialog / idempotence; destructive = confirm + undo safety window (~5 s) | Nielsen #3 | mixed |
| ⑥ | Will it still be recognized next time / in another environment | Persistence / consistency / concurrency / deep links / devices / language / weak network | Conceptual-model consistency | source read |

Persuasion column, the seventh: **emotional goal** (what the user should feel at this step — reassurance / control / delight — the journey-map emotion lane).

### Translation-table schema (source = statechart JSON/TS; tables are only views)
```json
{
  "id": "import-wizard",
  "initial": "idle",
  "states": {
    "idle":    {"on": {"SELECT_FILE": "parsing"}},
    "parsing": {"on": {"DONE": "review", "FAIL": "error"}},
    "review":  {"on": {"COMMIT": "done", "CANCEL": "idle"}},
    "error":   {"on": {"RETRY": "parsing", "ABORT": "idle"}}
  }
}
```
Gates: no dead ends (every non-final state has an outgoing edge) / all reachable / every error state has a recovery transition — `scripts/statechart-gate.py`.

## 3. Floors and ceilings, plus the fourth floor

Usable (all six questions answered + zero tolerance for anti-patterns) | not ugly (zero tolerance for the AI-slop list) | **accessible (WCAG POUR: perceivable / operable / understandable / robust; the axe static subset)** | more usable (progressive disclosure / frequency adaptation, rooted in cognitive load + Hick) | more beautiful (transition semantics / layered texture, Norman's behavioral and reflective levels).

## 4. Connected rows (the acceptance unit)

One row = feature semantics → interaction answers (six questions) → on-screen element → evidence (screenshot / DOM / statechart path). Delivery reports list connected rows so the user can accept row by row.

**Abandon-path three questions** (the semantic review checklist for in-progress / holding states): for every in-progress or holding state (dragging, uploading/exporting, a dialog holding sensitive information), walk: ① **can it be abandoned** — is the ESC / click-outside / close / CANCEL exit modeled in the state machine (success-only exits = the abandon path is missing); ② **where it falls back** — which state it returns to, never leaking an intermediate state (e.g. UI residue from a drag that never dropped); ③ **the consequence of abandoning** — irreversible discards warn first (e.g. a secret shown once: closing it means it is gone forever). This is where six-question ② "beyond the ceiling, cancelable" and ⑤ "can it be undone" get honored inside the statechart walkthrough; the structural gates (no dead ends / all reachable) cannot see a missing abandon path — it is a mandatory semantic-review item.
