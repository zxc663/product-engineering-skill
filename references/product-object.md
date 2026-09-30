# product object · definition (upstream six questions + two checklists)

> **Position**: runway step 0, before the feature-surface inventory (step 1) and the six birth questions (step 2). **Object-level questions are answered first; feature-level interaction comes after** — this is the seam between product engineering and interaction engineering. Four distinctions it enforces: what the product is ≠ how the feature is implemented | page responsibility ≠ page interaction | feature priority ≠ feature completeness | the product loop ≠ the front-end loop.
> **Boundary**: **product engineering ≠ product innovation**. Innovation (what to create / market opportunity / business model / growth) belongs to the product-decision side and is not this skill's job; this skill governs "given the decision, what it concretely should be" — the core enemy is "the product was decided, and the AI built it crooked".

## 1. The product object's six questions (a missing answer = stop; step 1 may not start)

| # | Question | Answer shape | Check |
|---|---|---|---|
| ① | **Purpose — why it exists** | What it solves, what it does not (one sentence) | non-empty; not a duplicate of the responsibility sentence |
| ② | **Responsibility sentence** | "X manages / operates …" — **not** "displays X data" | display verbs (display / show / present) forbidden |
| ③ | **Capability list** | What this page can do (row by row, verb-first) | non-empty; aligned with the step-1 surface inventory |
| ④ | **Priority** | **Exactly one primary function** + each capability carries a product role (§4) | primary function unique; roles from the enum |
| ⑤ | **Completeness** | Walk the page-level closure checklist (§2) row by row | a missing item = incomplete capability: build it, or explicitly rule it out (into the ledger) |
| ⑥ | **Operability** | Walk the operability checklist (§3) row by row | no management path requires an explicit ruling "no back office this cycle + who curates the content" |

## 2. The page-level closure checklist (question ⑤)

A page, as **a product capability**, must answer at least eight groups of questions; every missing item gets "build it" or "explicitly ruled out":

1. **Source**: where does the data / content come from (user-created / imported / system-generated / third-party)?
2. **Lifecycle**: create / edit / delete (soft vs hard) / disable (and what happens after disabling) — who may do each?
3. **Self-service vs management**: what can users change themselves, what can administrators change (two separate lists)?
4. **Search & bulk**: search / filter / pagination / sort / bulk operations (if present, where is the entry; if absent, rule it out)?
5. **Boundaries & capacity**: empty state (first open) / large data / overlong text / concurrent edits / insufficient permission — what does each look like?
6. **Definition & ownership**: where are states and enums defined (single source), which object do they belong to, who owns them?
7. **System support**: does the API support it, does the database support it, how is failure recovered (on inconsistency, who wins)?
8. **Audit & exit**: operation audit, export, recovery (trash / undo)?

## 3. The operability checklist (question ⑥)

For every front-end capability, ask "who manages it", and answer each item or rule explicitly:
back-office config entry | data source | ordering rules | enable/disable mechanism | permissions | review | defaults | fallback (what shows when content is missing) | data structure (where stored, where the schema lives).

**Fake-capability criterion**: visible in the front end, manageable by no one in the product system = **merely drawn in the UI**, not a product capability — record it as a defect; "drawn" never counts as "done".

## 4. Priority tiers (question ⑥'s product role table — question ④'s enum)

| Product role | Example | Consequences |
|---|---|---|
| core-task | view / search / filter orders | Owns the primary visual area, shown by default |
| business-op | change a status | First-level entry or inline action |
| auxiliary | export | Folded / toolbar |
| advanced | bulk processing | Second-level action + conditional appearance |
| risky | delete / cancel | Confirm + permission + hard to reach by accident (never visible in the blast zone by default) |

Unclear priority = every function treated as equal = "everything is there, nothing matters".

## 5. Joins to the downstream

- **Step 1** (feature-surface inventory): the capability list → surface-by-surface inventory (including the fifth class, the management surface).
- **Step 2** (the six birth questions): answer the interaction loop **per capability** — the object six questions govern "what should exist", the feature six questions govern "how this one is complete".
- **Step 6** (implementation): the **isolated-capability check** (judgement-table row 2) — when a page needs X, check the product state model / components / back-office capabilities first; reuse first, extend if necessary and write back to product knowledge; building an isolated capability for one local page is the highest-weight debt.
- **Judgement table**: the J-domain rows (responsibility sentence / primary-function uniqueness / page-level closure / fake capability) are its ruling-grade form.

## 6. Machine-checkable form (product-object-gate.py)

The runway step 0b answers land as JSON (`docs/contracts/<page>.object.json`); the gate judges item by item:

| Field | Meaning | Check |
|---|---|---|
| purpose / responsibility | six questions ①② | non-empty; the responsibility sentence must not start with a display verb (display / show / present) |
| capabilities[] | six questions ③: `{name, role}`, role ∈ the five-role enum (§4) | non-empty; both keys on every row |
| main_function | six questions ④ | **exactly one capability with role = core-task, and it must equal main_function** (count ≠ 1 → exit 1) |
| layers | step 0a: `{active, upstream{L1..L4}}` | each of L1–L4 must be `file:<path>` / `brief:` / `adjudicated:`; a dangling file reference exits 1 per layer |
| operability[] | six questions ⑥: `{item, answer}` | non-empty; no-management-path requires the explicit ruling on record (fake-capability criterion) |

Usage: `python product-object-gate.py --file docs/contracts/<page>.object.json` (reported as P1–P4). These are the first machine criteria for upstream L1–L4 — "primary-function count ≠ 1", "dangling upstream reference", "misplaced responsibility sentence" can all exit 1 from now on.
