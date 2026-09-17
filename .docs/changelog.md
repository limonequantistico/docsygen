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

## 2026-09-16

### 15:48

  - added Pinterest to `/design-system` Step 0's gallery list, for loose moodboarding that the curated galleries miss
  - had `/design-system` Step 0 suggest 5-8 project-specific search keywords, matched to how each gallery searches (Mobbin by screen and flow, Dribbble and Pinterest by style)

### 17:17

  - added a craft-floor check to `/setup` Phase 2 — states, real content, contrast, focus, undrawn browser surfaces, and action-naming copy, verified on the rendered result in one bounded round per batch
  - had `/design-system` push back on default-by-accident recommendations, open its summary with a one-line design read, and record what the direction deliberately isn't
  - added a "templated look" dimension to `/ux-review`, checked against the design system's stated anti-directions and ranked below usability issues
  - added a UI-completeness rule to the `/init` CLAUDE.md template (states, long or missing content, contrast, default look)

### 17:30

  - tightened the new craft floor after a second-opinion review — `/setup` builds the showcase with the first batch and renders through it, falls back to a labelled "written, not run" check instead of setting up a preview unasked, and routes any new tint or surface color through the styles-file tokens
  - made the `/init` template UI rule conditional ("where they apply", "if design-system.md exists") and the `/design-system` design read's "avoids" clause optional
  - replaced the generic Pinterest example searches in `/design-system` Step 0, which contradicted the project-specific keyword guidance

### 17:41

  - added `/showcase` — creates or updates one dev-only page or screen rendering the design tokens and base components (variants, applicable states, one awkward-content case each); updates an existing showcase rather than duplicating it, and records its location in `.docs/preview.md` on approval
  - made the showcase optional in `/setup`: Phase 1 now offers it once alongside the styles-file check, Phase 2 adds batches to it only if one exists, and the closing check no longer assumes one
  - pointed the `/init` template rule (and this repo's `CLAUDE.md`) at `/showcase` when a project has no showcase, and had `/ux-review` use a recorded showcase as a component-level view
  - listed `/showcase` in `/help` and the README, and updated the skill count to 35

## 2026-09-17

### 01:27

  - added `/theming` — adds or repairs color modes (dark, high contrast, brand themes) on new or existing projects: assesses the token layer and hardcoded colors, settles each mode's values with contrast checks and writes them back to `design-system.md` on approval, wires the modes per the stack (checking current syntax against docs), migrates components to role tokens in approved batches, and verifies every mode rendered
  - made `/setup` Phase 1 always build role tokens on top of the palette, even for light-only projects, and offer `/theming` (when more than one mode is recorded or requested) alongside `/showcase`
  - fixed `/setup`'s Tailwind instruction, which still pointed at `tailwind.config` — v4 defines theme tokens in CSS with `@theme`
  - had `/design-system` design each mode's values up front when more than one is chosen, record a color-roles table with a column per mode, and check contrast in every mode
  - had `/showcase` render every color mode and `/setup`'s craft floor check contrast in each
  - listed `/theming` in `/help` and the README, and updated the skill count to 36

### 01:35

  - tightened the design-phase handoffs after a second-opinion review — `/setup` takes role tokens from `design-system.md` (proposing and writing them back when an older doc has none), wires only the primary mode and says visibly when recorded modes are left for `/theming`, and absorbs `/theming`'s verification into the showcase when it runs both
  - moved `/theming` and `/showcase` in `/help` from Quality passes to Phase 3 under `/setup`, matching the README

### 01:55

  - structured `/showcase` like a Figma design-system file — an index, foundations from primitive to composite (palette → role tokens, type, spacing/radii/elevation), components grouped by purpose (or by the project's own folder groups) with the same variant-grid, states-row, and awkward-case frame for each, flagging variants that won't form clean axes; updates slot new components into their group and offer to reorganize a flat showcase rather than doing it unasked
  - bumped docsygen to 1.13.0
