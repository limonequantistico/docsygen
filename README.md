```text
██████╗  ██████╗  ██████╗███████╗██╗   ██╗ ██████╗ ███████╗███╗   ██╗
██╔══██╗██╔═══██╗██╔════╝██╔════╝╚██╗ ██╔╝██╔════╝ ██╔════╝████╗  ██║
██║  ██║██║   ██║██║     ███████╗ ╚████╔╝ ██║  ███╗█████╗  ██╔██╗ ██║
██║  ██║██║   ██║██║     ╚════██║  ╚██╔╝  ██║   ██║██╔══╝  ██║╚██╗██║
██████╔╝╚██████╔╝╚██████╗███████║   ██║   ╚██████╔╝███████╗██║ ╚████║
╚═════╝  ╚═════╝  ╚═════╝╚══════╝   ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═══╝
 The Comprehensive Documentation Toolset

╔═══════════════════════╗  [INIT] Starting Docsygen CLI...
║ 28          Dev Tools ║  [INFO] Version 1.0.0 (Build 492)
║                       ║
║                       ║  [INFO] Element ID: [dOc]
║         d O c         ║  [INFO] Group: Dev Tools
║                       ║  [INFO] Registered to: DEVTOOLS GLOBAL
║                       ║
║       Docsygen        ║  [OK] Plugins: auto-gen, type-inference
║         1.0.0         ║  [OK] Config: /etc/docsygen/config.toml
╚═══════════════════════╝  [READY] System is operational.
 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

Type '/help' to list available commands.
docsygen >
```

# Docsygen

**Docsygen** is a **documentation-driven development workflow** for [Claude Code](https://claude.com/claude-code), packaged as a **Claude Code plugin**. It adds ~28 slash commands that guide a project from raw idea → shaped design → tracked work → shipped release, keeping docs honest along the way.

It's **language-agnostic** — the commands and docs work the same whether the project is Swift, Android, web, or anything else. Docsygen ships no application code; it's a toolkit of commands plus a `.docs/` convention.

## Install

Add the marketplace and install the plugin **once per machine** — it installs at user scope, so the commands then work in **every project** you open with Claude Code on that machine. There are two equivalent ways to run these — pick whichever fits where you are:

**From a terminal** (`claude` CLI — works in every environment):

```
claude plugin marketplace add limonequantistico/docsygen
claude plugin install docsygen@docsygen
```

**From inside a Claude Code session** (slash commands — needs an interactive session; not available in some surfaces like the IDE panel):

```
/plugin marketplace add limonequantistico/docsygen
/plugin install docsygen@docsygen
```

> User scope is per machine, not per GitHub account — on another computer, run these once there too. To scope the install to a single project instead (e.g. to share it with a team via committed settings), add `--scope project` to the install command.

Once installed, the commands are available everywhere. The only **per-project** step is scaffolding the docs structure — run this in Claude Code inside each project where you want the workflow:

```
/init
```

`/init` creates the baseline `.docs/` skeleton the other commands rely on (`idea.md`, `backlog.md`, `changelog.md`, `changelog-spec.md`, asset folders). It's idempotent — safe to re-run, never overwrites existing work.

> New here? Run `/help` for the full guided workflow, then start by dropping notes in `.docs/idea.md`.

## Update

When a new version of Docsygen is published, pull it the same two ways:

```
claude plugin update docsygen@docsygen   # from a terminal
```

```
/plugin update docsygen@docsygen          # inside a Claude Code session
```

Commands update in place — nothing is copied into your project, so they never go stale. Your project's own `.docs/` content is yours and is untouched by updates.

## The workflow

`/help` prints this inside Claude Code. Phases are a guide, not a rule — jump to whatever fits.

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
| `CLAUDE.md`               | Project rules agents follow (recommended; not auto-created). | you        |

## Conventions

- **Changelog:** Every command logs to `.docs/changelog.md` in the format defined by `.docs/changelog-spec.md`. Timestamps (`HH:mm`) are never stripped.
- **Backlog-driven:** Dump tasks in `.docs/backlog.md` anytime. `/to-issues` slices plans into items, `/new` works through them, `/tidy` archives done work, `/version` cuts releases.
- **Before committing:** Run `/review` for a read-only pass; reach for `/test`, `/env`, `/performance`, or `/a11y` when those dimensions matter.
- **Truth over docs:** If docs and code disagree, the code wins — run `/sync` to reconcile.

## Developing Docsygen itself

This repository **is** the plugin and its marketplace:

- `.claude-plugin/plugin.json` — manifest. Its `commands` field points at `./.claude/commands/`, so command files live there and this repo dogfoods them as project commands.
- `.claude-plugin/marketplace.json` — makes the repo its own marketplace.

To work on it:

- **Add a command:** drop a markdown file in `.claude/commands/`. No manifest change needed — commands are auto-discovered. Add it to `/help` so it's documented.
- **Validate:** `claude plugin validate .`
- **Ship an update:** bump `version` in `plugin.json`, then push. ⚠️ Updates only reach installed projects when the version changes — pushing commits alone does nothing, because Claude Code caches by version. Users then run `/plugin update docsygen@docsygen`.

Repo: [github.com/limonequantistico/docsygen](https://github.com/limonequantistico/docsygen)
