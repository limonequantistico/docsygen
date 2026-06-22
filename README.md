```text
██████╗  ██████╗  ██████╗███████╗██╗   ██╗ ██████╗ ███████╗███╗   ██╗
██╔══██╗██╔═══██╗██╔════╝██╔════╝╚██╗ ██╔╝██╔════╝ ██╔════╝████╗  ██║
██║  ██║██║   ██║██║     ███████╗ ╚████╔╝ ██║  ███╗█████╗  ██╔██╗ ██║
██║  ██║██║   ██║██║     ╚════██║  ╚██╔╝  ██║   ██║██╔══╝  ██║╚██╗██║
██████╔╝╚██████╔╝╚██████╗███████║   ██║   ╚██████╔╝███████╗██║ ╚████║
╚═════╝  ╚═════╝  ╚═════╝╚══════╝   ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═══╝
 The Comprehensive Documentation Toolset

╔═══════════════════════╗  [INIT] Starting Docsygen CLI...
║ 28          Dev Tools ║  [INFO] Version 1.1.0 (Build 492)
║                       ║
║                       ║  [INFO] Element ID: [dOc]
║         d O c         ║  [INFO] Group: Dev Tools
║                       ║  [INFO] Registered to: DEVTOOLS GLOBAL
║                       ║
║       Docsygen        ║  [OK] Plugins: auto-gen, type-inference
║         1.1.0         ║  [OK] Config: /etc/docsygen/config.toml
╚═══════════════════════╝  [READY] System is operational.
 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

Type '/help' to list available commands.
docsygen >
```

```text
╔════════════════════════════════════════════════════════════════╗
║  CLAUDE CODE  ·  install once per machine                      ║
╟────────────────────────────────────────────────────────────────╢
║  claude plugin marketplace add limonequantistico/docsygen      ║
║  claude plugin install docsygen@docsygen                       ║
║                                                                ║
║  per project   /init                                           ║
║  update        claude plugin update docsygen@docsygen          ║
╚════════════════════════════════════════════════════════════════╝
```

```text
╔════════════════════════════════════════════════════════════════╗
║  CODEX  ·  install once per machine                            ║
╟────────────────────────────────────────────────────────────────╢
║  git clone https://github.com/limonequantistico/docsygen \     ║
║      ~/.docsygen                                               ║
║  ln -s ~/.docsygen/skills ~/.codex/skills/docsygen             ║
║                                                                ║
║  per project   /init   (or ask: "initialize docsygen")         ║
║  update        git -C ~/.docsygen pull                         ║
╚════════════════════════════════════════════════════════════════╝
```

# Docsygen

**Docsygen** is a **documentation-driven development workflow** that runs in both [Claude Code](https://claude.com/claude-code) and [Codex](https://developers.openai.com/codex). It's a set of **28 skills** (`SKILL.md` files) that guide a project from raw idea → shaped design → tracked work → shipped release, keeping docs honest along the way.

It's **language-agnostic** — the skills and docs work the same whether the project is Swift, Android, web, or anything else. Docsygen ships no application code; it's a toolkit of skills plus a `.docs/` convention.

Skills are a **cross-agent standard**: the same [`skills/`](skills/) directory is the single source of truth for both agents. On Claude Code it's distributed as a plugin; on Codex you point its skills folder at the same files. One repo, no forks.

## Install

Pick your agent. Both install **once per machine** (user scope), so the skills then work in **every project** you open on that machine.

### Claude Code

Distributed as a plugin via its own marketplace. From a terminal:

```
claude plugin marketplace add limonequantistico/docsygen
claude plugin install docsygen@docsygen
```

Or the equivalent slash commands inside an interactive session: `/plugin marketplace add limonequantistico/docsygen` then `/plugin install docsygen@docsygen`.

### Codex

Codex has no plugin marketplace — clone the repo once and symlink Codex's skills folder at it, so updates are a single `git pull`:

```
git clone https://github.com/limonequantistico/docsygen ~/.docsygen
ln -s ~/.docsygen/skills ~/.codex/skills/docsygen
```

> Tip: `~/.codex/skills/` is global (all projects). For a single project shared with a team, copy skills into the repo's `.codex/skills/` and commit them instead.

### Per project

Whichever agent you use, the only per-project step is scaffolding the docs structure. In Claude Code, run `/init`; in Codex, run `/init` or just ask it to *"initialize docsygen"*:

```
/init
```

`/init` creates the baseline `.docs/` skeleton the other skills rely on (`idea.md`, `backlog.md`, `changelog.md`, `changelog-spec.md`, asset folders) plus a root `CLAUDE.md` with the project rules. It's idempotent — safe to re-run, never overwrites existing work (an existing `CLAUDE.md` is left untouched).

> New here? Run `/help` for the full guided workflow, then start by dropping notes in `.docs/idea.md`.

## Update

When a new version of Docsygen is published:

```
claude plugin update docsygen@docsygen   # Claude Code (or /plugin update … in a session)
git -C ~/.docsygen pull                   # Codex (the symlink picks up changes automatically)
```

Skills update in place — nothing is copied into your project, so they never go stale. Your project's own `.docs/` content is yours and is untouched by updates.

## The workflow

`/help` prints this. Phases are a guide, not a rule — jump to whatever fits.

> **How to invoke:** In Claude Code, type the skill as a slash command (`/seed`). In Codex, either ask for the task in plain language (*"create the seed"*) — skills load by description — or name the skill directly. The `/name` notation below is the canonical reference for both.

### Phase 0 — Set up

| Command | Purpose                                                          |
| ------- | ---------------------------------------------------------------- |
| `/init` | Scaffold the baseline `.docs/` structure (run once per project). |

### Phase 1 — Think

| Command        | Purpose                                                                   |
| -------------- | ------------------------------------------------------------------------- |
| `/seed`        | Turn raw notes in `.docs/idea.md` into a structured seed document.        |
| `/seed-update` | Integrate new notes into the existing seed.                               |
| `/seed-review` | Stress-test the seed (scope, riskiest assumption, gaps) with a verdict.   |
| `/grill-me`    | Interactive interview that resolves every open decision before you build. |

### Phase 2 — Shape

| Command      | Purpose                                                              |
| ------------ | -------------------------------------------------------------------- |
| `/prototype` | Generate a prompt for external design tools (Stitch, Figma AI, V0).  |
| `/stack`     | Define the tech stack → `.docs/tech-stack.md`.                       |
| `/design`    | Create the design system (visual tokens) → `.docs/design-system.md`. |

### Phase 3 — Build

| Command      | Purpose                                                                                         |
| ------------ | ----------------------------------------------------------------------------------------------- |
| `/to-prd`    | Synthesize the conversation into a PRD under `.docs/prds/`.                                     |
| `/to-issues` | Slice a plan/PRD into vertical backlog items in `.docs/backlog.md`.                             |
| `/scaffold`  | Validate or create the project structure.                                                       |
| `/setup`     | Wire design tokens into the codebase and build base components.                                 |
| `/new`       | Ad-hoc feature or fix with full project context (also how you pull a backlog item into action). |
| `/resume`    | Fresh situational assessment: where you are, what's next.                                       |
| `/test`      | Testing strategy, critical-path coverage, flakiness guardrails.                                 |
| `/review`    | Read-only review of uncommitted changes before commit.                                          |
| `/commit`    | Generate a copyable commit message for the latest changes.                                      |

### Phase 4 — Maintain & harden

| Command        | Purpose                                                            |
| -------------- | ------------------------------------------------------------------ |
| `/tidy`        | Clean up the backlog; move completed items to the changelog.       |
| `/sync`        | Reconcile docs with reality (seed, stack, design, components).     |
| `/deps`        | Bump dependencies to latest stable; align `tech-stack.md`.         |
| `/env`         | Environment variables, secrets hygiene, production checklist.      |
| `/performance` | Performance and observability (logging, metrics, bottlenecks).     |
| `/a11y`        | WCAG-focused accessibility pass on the current UI.                 |
| `/ux-review`   | Broader UI/UX quality check (hierarchy, flow, consistency).        |
| `/clean`       | Audit modularity and separation of concerns; refactor on approval. |
| `/version`     | Cut a new app version; record it in `versions.json`.               |
| `/onboard`     | Refresh README / onboarding so another dev can run and contribute. |

**The planning pipeline:** `/grill-me` resolves open decisions → `/to-prd` documents them → `/to-issues` slices them into backlog items → `/new` builds each one.

## Project map

After `/init` (and as commands run), a project's docs live under `.docs/`:

| Location                  | Purpose                                                      | Created by |
| ------------------------- | ------------------------------------------------------------ | ---------- |
| `.docs/idea.md`           | Raw notes; input for `/seed`.                                | `/init`    |
| `.docs/backlog.md`        | Task queue; pin it in your IDE.                              | `/init`    |
| `.docs/changelog.md`      | Dated log of work and command runs.                          | `/init`    |
| `.docs/changelog-spec.md` | Canonical changelog format (commands follow this).           | `/init`    |
| `.docs/assets/imgs/`      | Prototypes and references.                                   | `/init`    |
| `.docs/seed.md`           | Product/context seed.                                        | `/seed`    |
| `.docs/tech-stack.md`     | Tools and runtime versions.                                  | `/stack`   |
| `.docs/design-system.md`  | Visual tokens and UI rules.                                  | `/design`  |
| `.docs/prds/`             | Product requirement docs.                                    | `/to-prd`  |
| `CLAUDE.md`               | Project rules agents follow.                                 | `/init`    |

## Conventions

- **Changelog:** Every command logs to `.docs/changelog.md` in the format defined by `.docs/changelog-spec.md`. Timestamps (`HH:mm`) are never stripped.
- **Backlog-driven:** Dump tasks in `.docs/backlog.md` anytime. `/to-issues` slices plans into items, `/new` works through them, `/tidy` archives done work, `/version` cuts releases.
- **Before committing:** Run `/review` for a read-only pass; reach for `/test`, `/env`, `/performance`, or `/a11y` when those dimensions matter.
- **Truth over docs:** If docs and code disagree, the code wins — run `/sync` to reconcile.

## Developing Docsygen itself

This repository **is** the source of truth, the Claude Code plugin, and its marketplace:

- [`skills/`](skills/) — the 28 skills, one `SKILL.md` per directory. This is the single source both agents use. Claude Code auto-discovers it as the plugin's skills; Codex reads it via the symlink from the install step. This repo also dogfoods them directly.
- `.claude-plugin/plugin.json` — plugin manifest (name, version). Components in `skills/` are auto-discovered, so there's no path to maintain.
- `.claude-plugin/marketplace.json` — makes the repo its own marketplace.

To work on it:

- **Add a skill:** create `skills/<name>/SKILL.md` with YAML frontmatter (`name` + `description`). The description controls when the agent reaches for it — gate deliberate steps to explicit invocation (*"Use only when the user explicitly asks … or runs /name"*) so they don't auto-fire. Add it to the `/help` skill so it's documented.
- **Validate:** `claude plugin validate .`
- **Ship an update:** bump `version` in `plugin.json`, then push. ⚠️ On Claude Code, updates only reach installed projects when the version changes — pushing commits alone does nothing, because Claude Code caches by version; users then run `/plugin update docsygen@docsygen`. On Codex, a `git pull` picks up changes immediately (no version bump required).

Repo: [github.com/limonequantistico/docsygen](https://github.com/limonequantistico/docsygen)
