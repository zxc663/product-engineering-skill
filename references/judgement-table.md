# judgement table

> Row schema: trigger scenario | judgment | action | source | confidence (source read / reliably reported — spot checks accepted; inflated labels downgrade the whole table).
> Sourcing: mature frameworks (the disciplinary baseline) + real-practice feedback. Two-column separation: 【consensus】 = industry-wide agreement; 【style】 = this skill's choice, explicitly not truth.
> Also hosts **§Risk tiers (the tier 0–3 routing matrix)** — judge risk first, then check depth.

## Domain 0 · meta-taste (highest weight)

1.【style】**Before producing anything (code / component / doc / artifact / convention), ask: who will maintain it, how often, and how many places one change touches** | The strict criterion for elegant laziness = **minimizing the future maintenance surface, not minimizing lines** (a 50-line abstract base class can owe more debt than three 10-line duplications — abstraction itself is debt). Every new "thing that must be remembered" (convention / config / special case / doc) is a debt; do not incur it if avoidable | ponytail ("the best code is the code not written"), Tufte data-ink ratio | source read
2.【style】**Building an isolated product capability for one local page** (new component / hard-coded enum / a state model of its own) → **highest-weight debt** | Check the product state model / components / back-office capabilities first → reuse → extend if necessary → write back to product knowledge. Elegant laziness re-understood: not writing less code, but not building isolated capabilities | product-object §5 | practice ruling

## Domain A · structure (statechart / flow)

3.【consensus】**Feature surface with ≥3 states or async flows → write the statechart before the component** | No state-machine definition = the structural layer is missing | Backfill the definition and run statechart-gate | Harel 1987 / XState | source read
4.【consensus】**List insert / delete / state flip without a marker → change blindness guarantees missed perception** | Flash highlight fading 1–2 s or a transition animation | Change-blindness research | reliably reported

## Domain B · usable floor (veto power)

5.【consensus】**An error message with no way out (reports the error, never points anywhere) → hostile** | Good: "Invalid API key — create a new one under Settings → Integrations". Bad: "Invalid key" | Vercel guidelines; Nielsen #9 | source read
6.【consensus】**A screen with no next step (dead end) → defect** | Empty states / terminal states must carry a jump or a recovery action | Vercel "no dead ends" | source read
7.【consensus】**A button that does nothing on click (inert interaction) → fake feature** | No claiming a connection without real-render evidence | anti-ui-slop | source read

## Domain C · not-ugly floor

8.【style→consensus】**The AI-slop trio (purple gradients / meaningless glow / corner-radius abuse) → zero tolerance** | Colors via theme tokens; decoration serves hierarchy | taste skill, binarized | reliably reported
9.【consensus】**Hierarchy built by ever-bigger font sizes → high-density meltdown** | Hierarchy = weight + gray steps + spacing (4/8 grid); font-size tiers ≤ 3 | Material type scale | reliably reported

## Domain D · timing discipline

10.【style】**Component-driven design (the control is chosen before the interaction) → veto** | Interaction promises come first; components are the fulfillment. "Right" beats "original" (reuse + extend) | Cooper, goal-directed design | source read

## Domain E · accessibility floor

11.【consensus】**State expressed by color alone → color blindness + change blindness, a double kill** | Redundant cues: color + icon / text / position | WCAG 1.4.1; Vercel | reliably reported
12.【consensus】**ARIA first, semantics later → treating symptoms** | Semantic HTML first (button / link / native input); ARIA only for what semantics cannot express | Vercel; WCAG POUR | reliably reported

## Admission and bloat control

New entries pass the five questions (see decision-ledger) + every row carries a source + confidence; the same conflict ruled twice gets promoted; cite row numbers, never copy bodies.

## Domain F · perception and transition

13.【consensus】**Async loading with a centered spinner + layout jump → a high-density disaster** | Skeleton screens lock the layout (CLS ≈ 0) | Vercel / Nielsen thresholds | reliably reported
14.【consensus】**Overlays rendered flat, no elevation semantics → distorted hierarchy** | Shadow / scrim / border per the elevation table | Material elevation | reliably reported
15.【consensus】**More than 4 font-size tiers on one screen → hierarchy meltdown** | Converge into a type scale of ≤ 3 tiers | Material type scale | reliably reported
16.【consensus】**Grouping with boxes inside boxes → a precursor to density meltdown** | Group by spacing first (Gestalt proximity) | Gestalt | source read
17.【consensus】**Density locked to one tier → scenario mismatch** | Offer compact / comfortable switching | Ant / Lightning density systems | reliably reported
18.【consensus】**Data silently refreshed in the background → the user misses it or is confused** | Optimistic update or an update marker + failure-rollback notice | optimistic-UI consensus | reliably reported
19.【consensus】**Press / toggle without a physical feedback curve → operations feel like clicking paper** | Press scale 0.96–0.98 + shadow / inset-shadow moving in lockstep, ≤ 260 ms, one-shot | motion craft (press-scale pattern) | practice-extracted
20.【style】**Gesture-driven widgets without velocity semantics → drawer/panel snap divorced from the flick** | Compute snap points from release velocity (damped spring); duration derived from physics, not fixed | HIG gestures | practice-extracted
21.【style】**List items entering in lockstep → machine feel (no life)** | Stagger 0.08–0.12 s + spring curve; full degradation under reduced-motion | Material motion | practice-extracted

## Domain G · structure, supplement

22.【style】**State flow with no statechart source on a ≥3-state surface → the contract is undecidable** | The statechart JSON is the source; tables are views | Harel 1987 / XState | source read
23.【consensus】**A non-final state with no outgoing edge → a dead end, the structural form of a missing way out** | Add recovery / escape transitions (statechart-gate C2 intercepts). Outgoing edges that only lead to success = a semantic dead end C2 cannot see — in-progress / holding states get the abandon-path three questions (interaction-bridge §4) | Nielsen #3 | source read
24.【consensus】**Parallel sub-states flat-enumerated → combinatorial explosion** | Model hierarchical states / parallel regions | Harel | reliably reported
25.【consensus】**Transitions without guard notes → races and double-fires unauditable** | Guard conditions go into the translation table (statechart-gate C5) | XState guards | reliably reported

## Domain H · performance and pacing

26.【consensus】**Async waits with no pacing → anxiety or missed changes** | 0.1 s instant / 1 s flow ceiling (beyond it, progress required) / 10 s attention ceiling (beyond it, cancelable) | Nielsen response-time thresholds; interaction-bridge six questions ② | reliably reported
27.【style】**Animations with no frequency audit → high-frequency operations dragged down by motion** | Pass the animation four questions first (frequency → purpose → easing → duration) | emil; anti-excuses #5 | reliably reported
28.【consensus】**Motion promises with no machine criterion → "we added the animation" is unverifiable** | A LIVE parameter panel (debug state) or getAnimations assertions in the walkthrough (persistent instances: capped per viewport, ≤ 2 whitelisted properties) | practice-extracted
29.【consensus】**Motion budget counted by keyframes → "same keyframes batch animation" endlessly multiplies instances around the quota** | Count by Animation instance (getAnimations, filtering infinite iterations); the criterion text pins vocabulary vs instances | practice-extracted

## Domain I · real-practice feedback

30.【consensus】**A loading state rendering misleading terminal copy** (e.g. "no providers available" while the service is merely starting) → loading / empty / error copy explicitly separated | six states + practice ×2 | reliably reported
31.【consensus】**Async completion faster than the poll interval → flush every consumer of the terminal state** (log / progress / status line from one source, preventing ghosts) | practice ×2 | reliably reported
32.【consensus】**Promise–capability break: zero tolerance — before copy claims "recoverable / exportable / undoable", grep the implementing code and its entry point** | anti-excuses #1 + practice | source read
33.【style】**Error copy reused across contexts without checking context semantics** (single-source message + per-context override mechanism) | practice ×2 | reliably reported
34.【consensus】**Same-page money symbols / counting calibers must have a single source** (badge vs in-page, KPI vs detail-table drift = a trust killer) | numeric red line + practice ×2 | source read

## Domain J · product object (upstream; details = references/product-object.md)

35.【style】**Page responsibility written as "display X data" → misplaced responsibility** (the page "manages / operates X") | The responsibility sentence = a managerial verb + its object; every button / feature answers "why does this capability belong to this page" | practice ruling
36.【consensus】**Primary function undeclared / multiple visual centers → no center of gravity; the AI treats all functions as equal** ("everything is there, nothing matters") | Exactly one primary function + the product-role tiers (core task / business operation / auxiliary / advanced / risky) — priority decides visual weight, default visibility, entry level, folding, confirmation, permissions, batching | practice ruling
37.【consensus】**Page capabilities limited to "list → view → edit" → product-level incompleteness** | Walk the page-level closure eight groups (product-object §2); missing items get built or explicitly ruled out (into the ledger) | practice ruling
38.【consensus】**Drawn in the front end but nobody can manage it → a fake capability** (drawn in the UI ≠ a product capability) | A management path exists (the management surface is in the inventory) or an explicit ruling "no back office this cycle + who curates the content" | practice ruling

## Domain K · level discipline (details = references/layer-stack.md)

39.【style】**Discussing concrete solutions at L6+ while upstream L1–L4 is unconfirmed → level misplacement: the "complete answer" answers the wrong question** (implementation-layer completeness ≠ product-engineering completeness) | Declare the level → confirm upward → stop and backfill if unconfirmed (the level gate) | layer-stack
40.【consensus】**All-green downstream treated as product-ready (L6–L10 all passing ≠ product-engineering complete) → completeness is layered: downstream never patches an upstream hole** | Completeness claims state which layers they cover; uncovered layers = explicitly unverified | practice ruling
41.【consensus】**Creating a component / API / table without checking "does the same responsibility already exist" (L9 skipping L1/L2) → isolated-capability debt** (row 2 sunk to the implementation layer) | Answer "does the project already have a component / capability with this responsibility" first | layer-stack interception table
42.【consensus】**Empty / error-state and button-placement semantics decided offhand by the implementer (L7–L8 skipping L3/L5) → states and layout lack product semantics; rework accumulates downstream** | Before writing states / layout, point back to the upstream answers (empty-state product semantics / priority roles) | layer-stack interception table

## Risk tiers (the tier 0–3 routing matrix)

Criterion (countable): **blast radius × reversibility of failure** — judge the tier first, then the check depth; **not everything on by default** (a "correct but expensive" default kills adoption).

| Tier | Trigger list (any hit enters the tier) | Check depth |
|---|---|---|
| **Tier 0** | Copy / pure style / spacing / color values; no state, no data, no permission semantics | §2 runway not started; forced-checklist items 5/9 still hold |
| **Tier 1** | Within a single page / dialog; no cross-page state; failure has no persistent consequence | Six questions answered orally + single-page matrix |
| **Tier 2** | ≥3 states or multi-page flow; ordinary CRUD / forms / filters / pagination | Six questions + spec-trace bidirectional + statechart-gate + walkthrough evidence |
| **Tier 3** | Payment / billing · deletion / wipe / restore · permissions / roles · migration / import-export · collaboration / concurrency · async / long tasks · cross-device or cross-session state | All of tier 2 + recovery rows (every exit verified against its target's existence) + runtime evidence + regression (golden sample) |

Scoping rules: the "≥3 states" count covers **interaction / async states** (statechart objects); pure display states (a highlight, a label swap) and in-place edits do not accumulate toward it. A capability **appended** to an existing surface is tiered by the **new capability's risk**, not the surface's existing tier.
The tier must be declared in the GATE (`v` / `exempt`) or the design doc; contested tiers take the higher one.
