---
name: product-engineering
description: "Pin \"build a X page/tool/app\" tasks into checkable contracts — on any new user-facing feature task, load this skill before writing code. Product engineering skill (bridging/structural layer): pins the path from feature requirement → interaction logic → implementation into decidable contracts — a level gate (locate which layer a question belongs to, then check upstream; implementation-layer completeness ≠ product-engineering completeness), the six birth questions of a feature, state+transition statecharts, double floors and double ceilings (usable / not-ugly / accessibility floors, more-usable / more-beautiful ceilings), spec-trace bidirectional traceability, decision-ledger write-back, a registry attribution gate, and the L0–L5 goal bar (all gates ship with --selftest). Boundary: product engineering ≠ product ideation — deciding what to create, market opportunity, and business models belong to the product-decision side; this skill governs \"given the decision, what the feature concretely should be\". Visual craft (how to make it look good) belongs to design skills. Use when: adding or modifying any user-visible feature surface (page / dialog / flow), however small; frontend or feature-design tasks; the user says \"hard to use / ugly / counterintuitive\", \"why does the interaction work this way\", \"fake feature / click does nothing / not wired up\", \"dumping raw JSON on the user\", \"reinventing wheels / ignoring existing components / building a duplicate page\", \"design and implementation diverge\", \"empty state with no guidance / error with no way out\", \"dense screen, broken hierarchy\", \"what should this page contain / which capability matters most / is the capability set complete / can ops manage it\", or when a feature is discussed at button/styling level before its behavior is defined (level misplacement); also for design reviews, interaction acceptance, and design walkthroughs. Not for: pure visual color tweaks, pure backend work, tasks with no user-facing surface, feature ideation / market opportunity / business-model work."
license: MIT
compatibility: "Any Agent-Skills-compatible CLI coding agent: Claude Code, Codex, Cursor, Windsurf, Trae, WorkBuddy, and similar"
metadata:
  version: 1.0.0
  tags: [product-engineering, interaction-design, statechart, quality-gates, spec-trace, design-contract]
  author: zxc663
  homepage: https://github.com/zxc663/product-engineering-skill
---

# Product Engineering · the bridging layer

> **Layer**: design skills own the craft layer (how it looks — style, components, motion). This skill owns the structural layer: how a decided feature comes to be — which states exist, how it flows between them, how transitions are perceived, and what happens when a flow dead-ends. It never defines themes or components; the registry only checks attribution, it does not define components.
> **Goal**: real-user journey completeness. Two products can ship the identical feature list and differ enormously in journey completeness; this skill turns that difference into a decidable, producible checklist.
> **Standalone**: installable on its own; every gate is a self-contained script under `scripts/` with a `--selftest` port.

## §1 When to use / when not to

**Use**: adding or modifying any user-visible surface (page / dialog / flow); reviews triggered by "hard to use / ugly / counterintuitive / why does it behave this way"; interaction design before a feature lands; connected acceptance before delivery.
**Not**: pure backend tasks (no user-visible surface); pure visual polish (no feature flow involved); tier-0 copy/style micro-changes (exemption gradient, see §7); **product ideation** (what to create, market opportunity, business model — the product-decision side; this skill governs "given the decision, what it concretely should be").

## §2 The line (runway — single entry)

Every user-visible feature goes through eight steps (0–7); each step has an exit artifact, and without the artifact you do not enter the next step. **The single entry is step 0's level gate**: locate which layer the question belongs to before answering any upstream definition.

0. **Level location + upstream gate (0a → 0b)**: **0a level gate** — ① declare "what problem is being solved now, and at which layer" (the L0–L10 layer stack, `references/layer-stack.md`, with a trigger interception table: discussing button placement = L8, creating a new component/API = L9, changing layout = L5, …). ② Walk **upward layer by layer** and check whether upstream is confirmed (L1–L4 mandatory: responsibility / capability / priority & completeness / operability & back office); if project artifacts already answer it, cite them and do not interrupt the user. ③ Unconfirmed → **stop and backfill; do not sink to a lower level past a hole**. Iron rule: implementation-layer completeness ≠ product-engineering completeness — a fully green downstream does not patch an upstream hole. **0b the product object's six questions** (backfill tool; **a missing answer blocks every later step**) — ① **Purpose** (what it solves / does not solve) ② **Responsibility sentence** ("X manages / operates …", not "displays X data") ③ **Capability list** ④ **Priority** (exactly one primary function + product-role tiers: core task / business operation / auxiliary / advanced / risky) ⑤ **Completeness** (page-level closure, eight groups) ⑥ **Operability** (who manages it / data source / permissions / review / fallback; no management path requires an explicit ruling "no back office this cycle + who curates content"). Details and both checklists = `references/product-object.md`. Boundary: L0 only checks that the object was stated — it does not produce one; product engineering ≠ product ideation.
1. **Feature-surface inventory + feature sentences**: enumerate **every surface the user will see** — primary function surfaces, navigation/entries, empty states, error pages, loading, help/about, boundary scenarios (mobile / weak network / dark mode), and the **management surface (fifth class: back office / ops side — who curates content and data, and where)**. When the task description is vague, derive from the user journey — never from "how many items the task mentioned". Then write one promise sentence per surface (who, in which scenario, accomplishes what). A missed surface invalidates every downstream step for it.
2. **Six-question translation table** (`references/interaction-bridge.md` §2): answer the six birth questions of every feature one by one — ① what goes in (execution gulf) ② when it happens / how long (feedback + Nielsen thresholds 0.1 / 1 / 10 s) ③ what success looks like and where it lands (evaluation gulf) ④ how failure is prevented → how recovery works once it slips through → the way out (prevention over recovery) ⑤ can it be undone, at what cost (user control) ⑥ will it still be recognized next time / in another environment (persistence / consistency / device / language / weak network). Any question without an answer = **interaction debt; stop and design the missing piece**; an answer the user has to guess = hostile design. The persuasion column adds a seventh: the emotional goal.
3. **Statechart** (`scripts/statechart-gate.py`, checks C1–C7): write states + transitions as machine-readable JSON (each state's `on` event table + `initial`) — **no dead ends** (every non-final state has an outgoing edge), **all reachable**, **every error state has a recovery transition** (error-state recognition: declared `"type":"error"` ∪ name contains error/fail ∪ the contract's recovery section mentions it), **reference integrity** (every transition target ∈ states), and **bidirectional reconciliation of the contract's recovery rows** (enable with `--contract <json>`: a missing edge = a promised recovery that does not exist; an extra edge = an invented one. Recovery needs a machine-readable carrier — a markdown contract is not valid C7 input; for legacy projects, faithfully transcribe recovery into `contract.json` first. When `--contract` is present but has no recovery rows, the gate prints a reminder; `--probe-recovery <dir>` scans legacy markdown for likely recovery semantics (title "semantic word × state word" co-occurrence | recovery-list headers) — advisory only, never FAIL). Tables and walkthrough paths are derived from the statechart. Scope: feature surfaces with ≥3 states or async flows; single-state pieces are exempt. Structural checks cannot see "missing abandon paths" (cancel/interrupt not modeled is structurally legal) — in-progress/holding states get the abandon-path three questions from `interaction-bridge.md` §4 as a semantic walkthrough.
4. **Promise list + six-state matrix**: one promise sentence per interactive element (what happens on click) + the six states per cell (loading / empty / error / edge / disabled / success) + every state-to-state arrow annotated with transition semantics / duration / interruptibility (change blindness: an unmarked abrupt change is a defect).
5. **Acceptance criteria first**: 3–5 verifiable acceptance criteria (Given/When/Then) before any implementation.
6. **Implementation**: the first action of building is consulting the table (registry / capability map); self-building requires an attribution. Component-driven design (picking the control before the interaction) is a veto-level anti-pattern.
7. **Acceptance triad**: ① spec-trace bidirectional traceability (forward: every feature row has an element fulfilling it; reverse: every on-screen element points back to a feature row) ② real evidence (no claimed interaction verification without a real render) ③ rulings written back to the `decision-ledger`. **Tier 3 adds a fourth**: regression — after changes, rerun existing features' gates + walkthrough checklist (golden sample); the criterion is the same rerunnable command exiting 0.

**Conflict order**: floor gates > process discipline > taste judgment; the user's brief verbatim always beats this skill; the same-layer conflict ruled twice gets promoted into the ledger.

## §3 Floors and ceilings

- **Usable (floor · law)**: all six questions answered + zero tolerance for anti-patterns (dead-end errors, clicks that do nothing, raw JSON dumps, infinite spinners).
- **Not ugly (floor · law)**: zero tolerance for the AI-slop list (`references/judgement-table.md`, ugly domain).
- **Accessible (floor · law)**: no WCAG POUR violations; the statically checkable subset (alt / labels / contrast / focus order / keyboard reachability).
- **More usable / more beautiful (ceiling · persuasion)**: progressive disclosure, frequency adaptation, humane automation; transition semantics, layered texture, craft — judgment table + critic push, never a gate.

## §4 Forced checklist (rule-level, exit 1)

Machine-decidable, intercepts at decision/delivery points, cost-tested — ten items:

1 Six questions, no blanks (machine subset: `product-object-gate.py` P1/P2 — responsibility sentence exists, exactly one primary function)｜2 Six-state matrix complete before build｜3 spec-trace bidirectional traceability (`spec-trace-gate.py` T1–T6)｜4 Registry attribution exists (`registry-gate.py`)｜5 Inline styles / hardcoded colors: zero tolerance for new code (`frontend-lint-gate.py` R1/R2)｜6 Dead binding logic — dead code / empty catch (`frontend-lint-gate.py` R3/R4)｜7 Evidence exists (no claiming verification without a real render)｜8 Ledger write-back exists｜9 Accessibility static floor (`a11y-gate.py` A1–A4+A3b machine subset — img alt / form-control accessible name / interactive-element accessible name (empty content **or bare symbols ▶/×**) / html lang / pseudo-buttons (click handler without role); legacy code under baseline exemption; a full axe-core audit stays a human domain)｜10 Statechart structural soundness (`statechart-gate.py` C1–C7 — no dead ends / all reachable / error-state recovery / reference integrity / contract recovery reconciliation; the product object is additionally checked by P3/P4: level declaration + upstream references exist, operability dimensions present).

**Exemption gradient**: exemptions are declared per §7 tier (tier-0 small changes exempt items 1–3 and 10; 5 and 9 still hold). An exemption must be declared in the GATE `exempt` field — skip + declare is legal, silent violation is not.

## §5 Anti-excuse table (twelve entries, full text `references/anti-excuses.md")

"Already implemented" does not count without a run｜"Didn't find it": zero results ≠ no result exists｜"There should be a library": dependencies are never assumed｜"The default is fine": an option left empty = no decision made｜"The animation is for beauty": the animation four-questions first｜"UX is probably fine": requires screenshot + DOM corroboration｜"Simple / obvious": danger words, self-check｜"Omitted for simplicity": prose longer than the code = smuggled complexity｜"Used in moderation": the model ignores moderation — every rule is binary.

## §6 Artifacts and gates

References:
- `references/interaction-bridge.md` — the three legitimate sources (user mental model > feature derivation > red lines; illegitimate sources: component inventory, model vibes, coolness) + six questions + translation-table schema + floors/ceilings.
- `references/judgement-table.md` — judgment table (every row carries a source + confidence level).
- `references/capability-map.md` — capability map (action point × symptom → capability → exit artifact).
- `references/decision-ledger.md` — decision ledger (records "why this was decided"; written back at close; harvested).
- `references/contract-schema.md` — contract schema (Interaction / Gate / Evidence; hard layer machine-verifiable, soft layer traceable).
- `references/layer-stack.md` — product layer stack L0–L10 + the three-stage level gate (locate → check upstream → pass / backfill) + trigger interception table (runway step 0a).
- `references/product-object.md` — product object (upstream six questions + page-level closure eight groups + operability checklist + priority role table; runway step 0b).
- `references/registry.md` — component registry (**pure checker**: verifies "was the table consulted, was attribution made"; defines nothing).
- `references/anti-excuses.md` — the twelve-entry anti-excuse table in full.

Gates (all with `--selftest`):
- `scripts/product-object-gate.py` — product object P1–P4 (+P4-W): definition existence / primary-function uniqueness / level declaration + upstream references / operability dimensions.
- `scripts/statechart-gate.py` — state machine structure C1–C7 + recovery bidirectional reconciliation + legacy markdown recovery probe.
- `scripts/spec-trace-extract.py` — binding-list extractor: generates the component/backend lists from source directories to feed spec-trace-gate (bindings themselves are a runway product, never auto-produced).
- `scripts/spec-trace-gate.py` — three-way binding traceability T1–T6 (placeholder rows / redundancy / UI orphans / dead logic / ghost endpoints — a URL-shaped backend absent from the real backend list is flagged; an empty list never swallows the check; path-parameter segments normalized to `{}` to prevent parameter-name double kills; rows missing due to T1 get a "chained" annotation so they are not confused with true orphans/dead logic).
- `scripts/registry-gate.py` — component attribution markers + baseline mode.
- `scripts/frontend-lint-gate.py` — checklist items 5/6 machine subset: inline styles / hardcoded colors / console / empty catch / empty-branch warning; baseline exempts legacy, new code only; canvas drawing parameters exempt (`addColorStop` call lines and `strokeStyle`/`fillStyle` assignment lines — custom-function parameter semantics are a human domain and still flagged); evidence/smoke directories are excluded whole-file, path-segment anchored (a filename merely containing an excluded word does not exclude the file).
- `scripts/a11y-gate.py` — checklist item 9 machine subset (A1 img without alt / A2 form control without accessible name / A3 interactive element without accessible name, incl. bare-symbol content / A4 html without lang / A3b pseudo-buttons); baseline exempts legacy.
- `scripts/l0-l5-gate.py` — L0 goal-statement bar + L5 information-architecture floor (single value / metric form / KR time window / navigation triad / front-door reachable / dead-end pages; an IA file present but unparseable = FAIL; unresolvable text references degrade to warnings; warnings cover the semantic-judgment checks incl. vanity metrics — cumulative counts of business volume are flagged, cumulative quality rates are not).
- `scripts/usage-probe.py` — usage monitor: counts skill mentions in the project log; zero hits = decay alarm.

## §7 Sizing (risk-adaptive tiers; named tier-N to avoid clashing with the L0–L10 layer stack)

**Judge risk first, then depth** (like a static analyzer: not everything on by default) — the tier matrix is in `references/judgement-table.md` §Risk tiers.

- **Tier 0 micro-change** (copy / pure style / spacing): **do not start §2**; exempt §2 steps 2–4 and checklist items 1–3, 10; items 5 and 9 still hold.
- **Tier 1 single piece** (one page / one dialog): **lightweight contract** — six questions answered orally + single-page matrix.
- **Tier 2 feature surface / flow** (≥3 states or multi-page; ordinary CRUD / forms / filters / pagination): six questions + spec-trace bidirectional + statechart-gate + walkthrough evidence.
- **Tier 3 high risk** (payment / deletion recovery / permissions / migration / collaboration / async / cross-device): all of tier 2 + **recovery rows** (every error state's way out, one per row, targets verified to exist) + **runtime evidence** (not just UI screenshots) + **regression** (golden sample).

When unsure, take the higher tier. The tier goes into the ledger — that is what stops "hide behind the small tier to skip steps".

## §8 Quick path + field rules

Level location (L0–L10) → upstream confirm → feature sentences → six questions → statechart → matrix → acceptance first → table-checked implementation → trace + evidence + write-back.

Intellectual sources: Norman's seven stages / Garrett's five planes / Nielsen's ten heuristics / WCAG POUR / ISO 9241-11 / Laws of UX. Every judgment-table row carries a source + confidence level and accepts spot checks.

**Field rules** (distilled from real sessions; stated as rules, confidence lives in the judgment table):
1. Input commit: `change` is blur semantics; every "input + primary action" entry must explicitly commit the current input (covers "filled it in and clicked without blurring").
2. Timing-coupled interactions: a trigger state and its dependent state (toast undo-button class) must be walked in one continuous pass; on timeout, check the app's timing semantics before judging a defect.
3. Persistence completeness: a persisted state-machine position must answer "after restore, what is the next step, and is it consistent without a refresh"; the same fact is never stored in two places.
4. Judgment-table granularity: independent degradation exits stay out of the main state machine (flattening them in = phantom coupling and combinatorial explosion); recovery may be empty but the absence must be declared; never fill tables for their own sake.
5. Reverse spec-trace: every on-screen element must point back to one feature behavior; "the wiring was probably done" is a fake-green variant.
6. Gate false positives: for a regex-level false positive, first fix the code or the naming; writing a baseline exemption = installing a mute button on the gate.
7. Acceptance entry mapping: every "how to use it" entry in the delivery note must map to one assertion; if it cannot map, add a test or mark it not verified.
8. Explicit interaction debt: deciding not to build a state also requires a ledger declaration; keep it strictly apart from silent omission.
9. Uncertain → ask before writing: judgment rows with insufficient evidence go to a pending-questions list; never invent them into the judgment table.
