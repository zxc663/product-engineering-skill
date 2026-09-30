# anti-excuses · the anti-excuse table (excuse → rebuttal pairs; danger words trigger a self-check)

| # | Excuse | Rebuttal | Upstream |
|---|---|---|---|
| 1 | "It's already implemented / wired up" | Without a real run (actual execution + host return) you may not claim it is connected | anti-ui-slop |
| 2 | "Couldn't find any information" | Zero results must not be treated as a result; declare the fallback | ui-ux-pro-max |
| 3 | "There should be a library / component for this" | Never assume the stack or a dependency exists — check package.json / the registry first | ui-ux-pro-max / taste |
| 4 | "The default is fine" | An option axis left empty = no decision was made; every default must state why | impeccable craft floor |
| 5 | "The animation is for beauty" | "For beauty" does not hold for high-frequency actions; pass the animation four questions first (frequency → purpose → easing → duration) | emil |
| 6 | "The UX is probably fine" | Judge by what the user actually sees at the interaction point; screenshot + DOM corroboration required | real-render walkthrough discipline |
| 7 | "This is simple / obvious / a tiny change" | A danger word appearing = self-check: a minimal change in the wrong place is not laziness, it is a second bug | shisan-xinuo / ponytail |
| 8 | "Omitted for simplicity" | Prose defending the simplification longer than the code = smuggled complexity; delete it | ponytail |
| 9 | (to skill authors) "Tell the model to use this sparingly" | Models ignore "used sparingly" — write every taste rule as a zero-tolerance binary rule | taste |
| 10 | "Write it first and see / the prototype becomes the feature" | Probes are legal but must declare a lifecycle: probe code is discarded by default and lessons go into the design doc; "let's see" is no excuse for skipping the six questions or the statechart | direction boundaries |
| 11 | "Lock the styles / interaction first, the features can come later" | Level misplacement: a "complete answer" at L8/L6 does not pay for answering the wrong question — backfill upstream (responsibility / capability / priority) first; sinking past a hole is forbidden | layer-stack interception table |
| 12 | "Verification failed, so the page is buggy" (or the reverse: "it's the test tool's fault") | An automated verification failure and a page defect are two different propositions — run an isolation experiment first (minimal repro / contrast path / dual-channel probe / event probe) and only then fix; attributing without isolation risks fixing the wrong side twice | isolation-experiment discipline |

**Trigger — danger words**: "obviously / just / there should be / probably fine / for beauty / in moderation / write it first" appears in dialogue or output → pause, check this table → reroute on a hit, continue otherwise.
**Trigger — level misplacement**: styling-detail words ("left or right / what color / corner radius / font size") or ground actions (new component / new API / new table) → pause, run the level gate (`layer-stack.md` §3: answer upstream before touching anything).
**Trigger — channel attribution** (#12): an automated verification failure or assertion miss → pause and run an isolation experiment (minimal repro + event probe + contrast path). Both "tool-channel defect" and "real page defect" are live possibilities — a channel defect being found does not exempt the page side, and vice versa.
**Usage**: every row is a zero-tolerance binary judgment; there is no "in moderation" (row 9 is aimed at this skill's own author too).
