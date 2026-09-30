# decision ledger (records "why this was decided", for the next session to reuse directly)

> Division of labor with debt lists: debt = debt semantics (records "why it was not written", for harvesting); this ledger = **ruling semantics** (records "why it was decided this way", effective immediately). Sources: spec-trace evidence, walkthrough conclusions, user verbal rulings.

## Row schema
`date | ruling subject | ruling content (one sentence) | basis (user verbatim / disciplinary source / measured evidence) | rejected candidates | impact surface | confidence level`

## Admission five questions (anti-bloat)
① What real conflict or symptom does it resolve? ② At which action will the next session use it? ③ Does it conflict with an existing entry (if so, write the relation: reuse / complement / overturn)? ④ Can it fit in one line? ⑤ Does it have a source or evidence?
Default ≤3 entries per close, hard cap 5; if genuinely nothing new, write "none this session".

## Write-back timing
Fixed close action: walkthrough/evidence conclusions, user rulings, style choices (the separated 【style】 items) → append to this ledger (append-only, never compressed; monthly harvest dedupes).

## Relation to the registry
Registry component rows reference ledger entries (a component's "why it is built this way" lives in the ledger); the ledger never copies registry content.

## Example entries (illustrative format only)
- 2026-09-30 | Destructive-action confirmation copy | Name the object and the consequence ("Delete 3 drafts? This cannot be undone"), never a generic "Are you sure?" | Basis: user ruling | Rejected: generic confirm dialogs | Impact: every destructive flow | Confidence: illustrative
- 2026-09-30 | Toast duration | Notifications auto-dismiss after 4s; error toasts persist until dismissed | Basis: checklist cost discipline | Rejected: one duration for all severities | Impact: every feedback surface | Confidence: illustrative
