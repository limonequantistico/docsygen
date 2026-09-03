# Changelog

## 2026-09-01

### 23:52

  - ran `/deep-audit` — audited `scripts/validate.py`; 2 findings, both fixed and regression-tested
  - added `/deep-audit` skill — whole-codebase sweep for latent bugs, security, failure paths, and architectural risk; report-first, fix on approval
  - fixed `check_skill_count()` crashing on a malformed Codex manifest instead of printing the collected errors
  - fixed the README banner check validating only the indent, letting a misaligned box pass green
  - bumped docsygen to 1.10.0

## 2026-09-02

### 00:32

  - added `/debug` skill — evidence-driven diagnosis of one reported bug: competing hypotheses, instrumentation to tell them apart, a reproduction, a root-cause fix, then the instrumentation stripped back out
  - shaped `/debug` as a runtime-evidence loop rather than the ticket-style interview the backlog proposed — the interview mostly collects what the agent can find by reading the repo; only repro, expected, and actual can't be, so intake is a gate, not a session. Cursor's Debug Mode confirmed the shape
  - kept `/debug` user-invoked only: the agent debugs from evidence on every bug via a new `CLAUDE.md` rule, and points at the skill once, after a second failed fix attempt on the same symptom
  - added a debugging rule to the `/init` `CLAUDE.md` template and the repo's own `CLAUDE.md` — the always-on half, since most bugs are never escalated to a command
  - wired scope boundaries: `/review` and `/deep-audit` hand a reproducible symptom to `/debug`
  - bumped docsygen to 1.11.0

## 2026-09-03

### 16:06

  - added convention detection to `/commit`, `/merge`, and `/push` — they now read `.docs/commit-convention.md` if it exists, otherwise sample recent git history for a dominant existing style, default to Conventional Commits when history is too thin, or ask once (and persist the answer) when it's genuinely mixed
  - fixed `/merge` and `/push` carrying a drifted, abbreviated copy of `/commit`'s message-format guidance (missing `perf`/`build`/`ci` types and breaking-change guidance)
  - had `/merge` and `/push` delegate to `/commit`'s steps 1–3 instead of duplicating them, cutting ~25 lines from each and removing the drift risk going forward
  - mentioned `.docs/commit-convention.md` in `/init`'s "newer artifacts" list — it's written lazily by `/commit`/`/merge`/`/push` on first use, same pattern as `.docs/preview.md`
  - bumped docsygen to 1.12.0
