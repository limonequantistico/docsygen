---
name: clean
description: Audit the codebase for modularity, structure, and separation of concerns, then refactor on approval. Use only when the user explicitly asks to clean up structure or runs /clean.
---

You are auditing the codebase for **modularity, structure, and separation of concerns** — then refactoring what the user approves.

**Scope note:** correctness and safety — latent bugs, security holes, broken failure paths, races — belong to `/deep-audit`. Flag one in a line if you trip over it, then point at `/deep-audit` rather than chasing it here. This pass is structural.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

---

## Step 1 — Load context (silently)

Before analyzing anything, read the project's canonical sources. Do not narrate this step.

1. `.docs/seed.md` — project scope and domain
2. `.docs/tech-stack.md` — technologies in use (limit advice to this stack)
3. `.docs/design-system.md` — visual tokens and component patterns
4. Nearby code — read enough files to understand the project's existing conventions (folder layout, naming, import style, patterns)

If any doc is missing or conflicts with the code, trust the code.

---

## Step 2 — Determine scope

- If the user pointed to specific files or folders, audit only those.
- If no arguments were given, scan the **entire source directory**.

---

## Step 3 — Analyze

Go through each file in scope and evaluate:

- **Modularity** — Is each file/function/component doing one thing? Flag god files, oversized components, functions with too many responsibilities.
- **Separation of concerns** — Is business logic leaking into UI components? Is data-fetching mixed with rendering? Is styling tangled with logic? Are side effects scattered instead of centralized?
- **Structure** — Are files in the right directories given the project's conventions? Are there naming inconsistencies? Are index/barrel files used where the project uses them?
- **Reuse** — Is there duplicated logic that should be extracted into a shared utility or hook? Are existing utilities or helpers being ignored in favor of inline re-implementation?
- **Best practices** — Specific to this project's tech stack. Not generic advice — concrete issues in the actual code. Think: proper hook usage, correct data flow patterns, idiomatic API usage for the frameworks in play.

**If the repo has a `.codegraph/` directory**, lean on it here: `codegraph explore` to see how a suspect file is actually wired before calling it a god file, and `codegraph impact <symbol>` before proposing that anything shared be extracted, moved, or renamed. The cost of a refactor is its number of dependents, and that number should come from the graph rather than a guess. Skip this if there is no index.

Skip anything that is purely stylistic (formatting, naming preferences with no functional impact, missing comments). Focus on structural issues that affect maintainability, readability, or correctness.

---

## Step 4 — Report

Present findings as a prioritized list grouped by severity:

### Critical — breaks maintainability or correctness
### Moderate — hinders clarity or introduces unnecessary coupling
### Minor — small structural improvements

Each item:
- **File** → what's wrong → why it matters → suggested refactor

If the codebase is clean, say so briefly — don't invent problems.

---

## Step 5 — Refactor (on approval)

After presenting the report, **ask the user which items to fix** (all, some, or none).

For approved items:
- Apply refactors one at a time, keeping each change small and verifiable.
- Follow existing project patterns — the cleaned code should look like it belongs.
- Do not change behavior. These are structural refactors only.
- Do not touch files outside the approved scope without asking.

---

## Rules

- Obey **CLAUDE.md** and workspace rules.
- Do not recommend adding new libraries or tools unless the user asks — flag once if something would genuinely help, then move on.
- Do not refactor anything before the user approves the report.
- If the user added extra instructions after the command name, those **override or extend** this prompt.

**Logging:** On completion, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /clean — [brief summary of what was audited and refactored]`.
