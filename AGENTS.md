# product-engineering · repo rules

This repo ships one thing: the English edition of the product-engineering skill
(`SKILL.md` + `references/` + `scripts/`) plus its bilingual README. Nothing else belongs here.

- Development source (Chinese edition) lives in the mother repo
  `shisan-xinuo-workflow` at `skill/shisan-xinuo-product/`. Keep the two editions
  mechanism-equivalent; when a gate or rule changes, change both or note the divergence.
- Writing discipline: state the rule plus at most one sentence of why. No dates,
  decision logs, candidate/promotion narration, or local paths in any shipped file.
- Scripts are the product: every gate must keep `--selftest` green before commit.
  Never weaken an assertion or fixture to make a test pass.
- Gate keyword tables are English-domain by design; this edition checks artifacts
  written in English.
- No secrets in any file. `git push`, tags, and releases require owner approval.
