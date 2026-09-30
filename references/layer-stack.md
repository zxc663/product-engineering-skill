# layer stack L0–L10 and the level gate (direction control)

> **Purpose**: not to tell the model the correct answer, but to **force the model to first confirm which layer's question it is answering** — an agent's native strength is rapidly generating complete answers inside a given frame; the real danger is whether the frame itself was correctly set.
> **Iron rule**: **implementation-layer completeness ≠ product-engineering completeness**. Feature / Interaction / State may be all green while Product Object / Capability / Priority / Completeness / Operability are undecided — in that state, product-engineering completeness may not be claimed.
> **Position**: runway step 0 (before the product object's six questions) — the level gate is the single entry action; every task / action / discussion passes it first.

## 1. The layer stack (the coordinate system for "which layer's question is this")

| Layer | Content | This skill's asset |
|---|---|---|
| **L0 product goal** | Why this product / module exists, what result it must achieve | **Checks the statement against the qualification bar only; never produces one** (PE ≠ PI) — l0-l5-gate L0 subset: single value / metric form / KR time window / artifact existence |
| **L1 product object / page responsibility** | Why this page / object exists, what it bears | Six questions ①② (`product-object.md`) |
| **L2 capabilities & features** | Which capabilities / features exist | Six questions ③ + the feature-surface inventory (step 1) |
| **L3 feature priority & completeness** | Which matters most, is the capability set complete | Six questions ④⑤ + the page-level closure eight groups |
| **L4 operations / back office / permissions / data** | Who manages it, data sources, back-office capability, permissions | Six questions ⑥ + the fifth-class management surface + the operability checklist |
| **L5 information architecture** | How information is organized, where features live, how users find them | **Structural floor, machine-checked** (l0-l5-gate L5 subset: navigation triad / front-door reachability / dead-end pages at FAIL level + organization declaration / path types / tree-testing reports at warning level; producing IA solutions stays with the mother architecture's Structure domain) |
| **L6 interaction** | How the user gets it done (input / timing / success / failure / undo / persistence) | `interaction-bridge.md` (steps 2 and 4) |
| **L7 state** | Which states exist, how it flows, what happens when it dead-ends | Statechart + the state/transition matrix (steps 3 and 4) |
| **L8 UI** | What it looks like (visuals / hierarchy / transitions / density) | Judgement table, ugly domain (craft belongs to design skills; this skill only holds the floor) |
| **L9 implementation** | How the code lands, where components / APIs / data come from | Registry / capability map (step 6) |
| **L10 verification** | How fulfillment is proven (evidence / traceability / regression) | Spec-trace / evidence / ledger write-back (steps 5 and 7) |

**Mapping to the mother architecture**: the stack is the vertical refinement of the Product Contracts seven domains — L0–L4 ↔ Intent / Scope / Runtime, L5 ↔ Structure, L6–L7 ↔ Interaction, L8–L9 ↔ Implementation, L10 ↔ Verification.

## 2. The level gate (three stages: locate → check upstream → pass / backfill)

1. **Locate**: settle "what problem are we actually solving now" → declare which layer it belongs to (write it out: "this is an L8 question").
2. **Check upstream**: from that layer **upward, layer by layer**, check for an **already-confirmed answer** — L1–L4 is the mandatory segment (Product Object / Capability / Priority / Completeness / Operability).
3. **Pass / backfill**: upstream sound → work at this layer is allowed; unconfirmed → **stop and backfill** (the backfill tool is the product object's six questions and its two checklists); **sinking past a hole is forbidden**.

**Self-answer first**: if the upstream answer already exists in project artifacts (product-object / contracts / ledger / design docs) → cite it and **do not interrupt the user**; only stop to ask a human when no answer exists (over-asking kills adoption).

**Four disciplines**:
- **No sinking past a hole**: while an upper layer is unconfirmed, lower-layer work does not start.
- **No same-layer blocking**: work within the same layer proceeds in parallel (prevents ritualized serial gating).
- **L0 checks, never produces**: the goal is given by the product-decision side; this skill only checks that it was stated (PE ≠ PI).
- **Reverse backfill**: a defect found downstream (L9/L10) whose root cause sits in a **skipped upstream layer** → backfill upstream; patching in place is forbidden (a missing answer is an unobservable deviation).

## 3. Trigger interception table (action / utterance → layer → upstream that must be answered → the follow-up question)

| Trigger signal | Layer | Upstream that must be confirmed | The follow-up question |
|---|---|---|---|
| "Left or right / what color / corner radius / font size" | L8 | L2 the feature is confirmed; L3 its priority role | "Hold on: is the function behind this button confirmed? What role does it play in the priority tiers?" |
| Writing empty / loading / error state components or copy (EmptyState.vue) | L7–L8 | L3 completeness (boundaries & capacity = the empty state's product semantics) | "Is this page's empty-state product semantics decided — should it tell the user to do something, or tell them something?" |
| Creating a component (*.vue / *.tsx / *.jsx) | L9 | L1 responsibility; L2 capability (does a same-responsibility component exist) → 0b | "Does the project already have a component with this responsibility?" — check the registry / component directory first |
| Creating an API / table / data model | L9 | L4 operations (who manages / data source / permissions / back-office capability) | "Who manages this data? Where does it come from? Is there back-office capability?" |
| "Add a toggle / should we do X" | L2–L3 | L1 the responsibility sentence (does X belong to this page); L2 the capability list | "Why does this capability belong to this page? What is the primary function?" |
| "Change the layout / how should the information sit / which column" | L5 | L2 / L3 (capabilities and priority) | "Which capabilities does the IA serve? Where does the primary function sit?" (self-answer first: run the l0-l5-gate L5 subset — navigation triad / front door / dead ends) |
| "Should we do X / why does this product exist" (the root question) | L0 | — (the goal is given by the product-decision side) | Check the goal statement bar (l0-l5-gate L0 subset: single primary result + measurable + KR with a time window); if unstated → stop and ask the decision side, **never ghost-write it** (PE ≠ PI); unattended with no one to ask → declare the assumption explicitly + into the ledger; silent sinking is forbidden |
| "How should the state flow / what if it dead-ends" | L7 | L6 six questions ④ (the way out) answered | Backfill six questions ④ → then the statechart |
| "Add an animation / transition" | L8 | L7 the change semantics | Pass the animation four questions first (frequency → purpose → easing → duration): what change should this transition make perceptible? |
| "Redo this page" (a downstream task thrown directly) | L6+ | Full scan L0–L4 | List everything unconfirmed layer by layer → backfill (six questions) before starting |
| A walkthrough / verification finds a defect | L10 | — (reverse backfill) | Is the root cause in a skipped upstream layer? → backfill upstream; patching in place is forbidden |

## 4. Interfaces and discipline

- **Runway mapping**: step 0a = this gate; step 1 = L2, 2 = L6, 3 = L7, 4 = L6/L7, 5 = L10, 6 = L9, 7 = L10.
- **Naming discipline** (three L-numbering schemes must not be confused): a bare "L+number" inside this skill = the **product layer** (this file); risk depth is written **tier 0–3** (`judgement-table.md` §Risk tiers); the host workflow's grading is written in full, e.g. "graded L2-F".
- **Machine-checkable**: `product-object-gate.py` P3 — the artifact's declared layer + the existence of L1–L4 upstream references (a missing layer or a dangling `file:` reference exits 1 per layer; schema = product-object.md §6). P2 (primary-function uniqueness) lands in the same gate.
- **Human-judgment domains**: the layer location itself (one sentence may span layers) and the sufficiency of "confirmed" upstream — require a human or a ledger entry.
