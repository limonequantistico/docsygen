# New work

You are starting **new work** in this project. Your job is to understand the request, gather enough context, and implement it **correctly the first time** — not to rush into code and patch mistakes after.

**What the user wants:** $ARGUMENTS

---

## Principles

- **Context before code.** Never start implementing until you understand the project's patterns, constraints, and the user's intent. Wrong assumptions are more expensive than a few questions.
- **Match the shape of the work.** If the user asks for a **UI component**, build it like one — structure, tokens, variants, and a showcase if the project does that. If the work is **reusable**, design for reuse — clean API, correct placement, tests if the project tests similar things. If it is a **standalone feature** (API route, job, migration, config), implement it the idiomatic way for _this_ codebase — not a generic tutorial.
- **Extend before you duplicate.** Before building from scratch, search for similar patterns, components, or utilities already in the repo. If something close exists, **propose** extending or adapting it. Only create parallel implementations when there is a clear reason — and say what that reason is.

---

## Step 1 — Load context (silently)

Before doing anything, read what this project treats as canonical. Do not narrate this step — just absorb it.

1. **Project orientation** — `.docs/seed.md` or README / product docs.
2. **Tech stack** — `.docs/tech-stack.md` — stay within listed technologies unless the user explicitly approves an exception.
3. **Design system** — `.docs/design-system.md` — for any UI work, align with documented patterns and tokens.
4. **Centralized visual source of truth** — globals / theme / Tailwind config (or equivalent). **No hardcoded** colors, spacing, typography, radii, or shadows when tokens exist.
5. **Nearby code** — read a few files of the same kind (components, routes, hooks, handlers) to absorb naming, folder layout, import style, and error handling patterns.

If any of these are missing or outdated, trust the code over stale docs.

---

## Step 2 — Ask or build

After loading context, decide:

- **If the request is clear enough to implement safely** — go straight to building. No questions, no proposal, no waiting.
- **If anything is genuinely unclear** — ask a single batch of focused questions before starting. Cover everything you need in one round — do not drip-feed questions across multiple turns. Things that might be unclear:
  - User-facing behavior, edge cases, or what is out of scope
  - Data sources, auth, permissions
  - For components: expected variants, sizes, states
  - For features: main flows and boundaries
  - Whether this is backward-compatible or a breaking change

Use judgment. If you can make a reasonable default choice, make it and mention it — don't ask about every detail.

---

## Step 3 — Implement

- Follow **existing patterns** in this repository. New code should look like it was written by the same team.
- For **components**: pull all styling from centralized tokens. If the component library (shadcn, MUI, etc.) ships a base version, extend it rather than reinventing.
- **Do not over-build** — only the variants, options, and surfaces the user actually needs.
- **Do not** make unrelated refactors or edit files you were not asked to touch without checking first.
- **Showcase**: if the project has a storybook, showcase, or demo page, add the new piece there. If none exists, mention it — don't create one without asking.
- Add or update tests, types, and docs **as you go** — if that is how this repo works.

> **See also** (separate passes, not part of `/new`): `/test` testing strategy · `/env` secrets hygiene · `/deps` dependency bumps · `/performance` observability · `/a11y` accessibility · `/onboard` onboarding docs.

---

## Rules

- Obey **CLAUDE.md** and workspace rules.
- If the user added extra instructions after the command name, those **override or extend** this prompt.
