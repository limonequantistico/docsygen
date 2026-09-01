# Changelog

## 2026-09-01

### 23:52

  - ran `/deep-audit` — audited `scripts/validate.py`; 2 findings, both fixed and regression-tested
  - added `/deep-audit` skill — whole-codebase sweep for latent bugs, security, failure paths, and architectural risk; report-first, fix on approval
  - fixed `check_skill_count()` crashing on a malformed Codex manifest instead of printing the collected errors
  - fixed the README banner check validating only the indent, letting a misaligned box pass green
  - bumped docsygen to 1.10.0
