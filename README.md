```text
██████╗  ██████╗  ██████╗███████╗██╗   ██╗ ██████╗ ███████╗███╗   ██╗
██╔══██╗██╔═══██╗██╔════╝██╔════╝╚██╗ ██╔╝██╔════╝ ██╔════╝████╗  ██║
██║  ██║██║   ██║██║     ███████╗ ╚████╔╝ ██║  ███╗█████╗  ██╔██╗ ██║
██║  ██║██║   ██║██║     ╚════██║  ╚██╔╝  ██║   ██║██╔══╝  ██║╚██╗██║
██████╔╝╚██████╔╝╚██████╗███████║   ██║   ╚██████╔╝███████╗██║ ╚████║
╚═════╝  ╚═════╝  ╚═════╝╚══════╝   ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═══╝
 The Comprehensive Documentation Toolset

╔═══════════════════════╗  [INIT] Starting Docsygen CLI...
║ 15          Dev Tools ║  [INFO] Version 1.0.0 (Build 492)
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

**Docsygen** is a **documentation-and-build workflow** for [Claude Code](https://claude.com/claude-code): slash commands under `.claude/commands/` guide thinking, design, scaffolding, and maintenance. This repository is the **toolkit and docs**—there is **no separate application** to `npm install` or `docker compose` here unless you add one via `/scaffold`.

## Prerequisites

- **Git** — clone and branch as usual.
- **Claude Code** (or an environment that loads `.claude/commands/`) — slash commands are the primary interface.
- **Optional:** Markdown editor; pinned `.docs/backlog.md` is recommended.

Project-specific runtime versions and package managers appear in **`.docs/tech-stack.md`** after you run **`/stack`** (file may not exist until then).

## First run

1. **Clone** this repository.
2. Open the project in **Claude Code** (or your agent that reads `.claude/commands/`).
3. Run **`/help`** — lists the full workflow (think → shape → build → maintain).
4. **Optional orientation:** read **`CLAUDE.md`** (repo rules) and **`.docs/changelog-spec.md`** (how to log work).

## Project map

| Location                 | Purpose                                                                        |
| ------------------------ | ------------------------------------------------------------------------------ |
| `.claude/commands/`      | Slash command definitions (`/seed`, `/next`, `/onboard`, …).                   |
| `CLAUDE.md`              | Agent rules: tech stack doc, design system doc, changelog spec.                |
| `.docs/idea.md`          | Raw notes; input for **`/seed`**.                                              |
| `.docs/seed.md`          | Product/context seed (created or updated by **`/seed`** / **`/seed-update`**). |
| `.docs/tech-stack.md`    | Tools and commands (from **`/stack`**).                                        |
| `.docs/design-system.md` | Visual tokens and UI rules (from **`/design`**).                               |
| `.docs/backlog.md`       | Task queue; **`/next`** takes the top item.                                    |
| `.docs/changelog.md`     | Dated log per **`.docs/changelog-spec.md`**.                                   |
| `.docs/assets/imgs/`     | Prototypes and references (e.g. **`/prototype`**).                             |

## Conventions

- **Branches & commits:** Use your team’s Git conventions; this template does not enforce a branching model.
- **Before you commit:** Run **`/review`** on uncommitted changes when you want a read-only pass; use **`/test`**, **`/a11y`**, or **`/ux-review`** when those dimensions matter.
- **Changelog:** Append entries to **`.docs/changelog.md`** in the format defined in **`.docs/changelog-spec.md`**.
- **Design system:** **`CLAUDE.md`** asks agents to follow **`.docs/design-system.md`** and avoid hardcoded values. Create or update that file with **`/design`** / **`/setup`** so it stays aligned with code.
- **Truth:** If docs and code disagree, use **`/sync`** to reconcile.

## Common tasks

There are **no** npm/yarn/pnpm scripts in this template repo. Day-to-day work is driven by **slash commands**:

| Goal                              | Command                                                                                                                          |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| See the full workflow             | **`/help`**                                                                                                                      |
| Define or refresh product context | **`/seed`**, **`/seed-update`**, **`/seed-review`**                                                                              |
| Prototype / stack / design        | **`/prototype`**, **`/stack`**, **`/design`**                                                                                    |
| Implement or plan work            | **`/scaffold`**, **`/setup`**, **`/new`**, **`/next`**, **`/resume`**                                                            |
| Quality passes                    | **`/test`**, **`/review`**, **`/tidy`**, **`/sync`**, **`/deps`**, **`/env`**, **`/performance`**, **`/a11y`**, **`/ux-review`** |
| Release & onboarding              | **`/version`**, **`/onboard`**                                                                                                   |

## Where to ask

- **Tasks and priorities:** **`.docs/backlog.md`** (use **`/next`** to execute the top item; **`/tidy`** archives done work into the changelog).
- **Product intent:** **`.docs/seed.md`** (once **`/seed`** has run) and **`.docs/idea.md`** for raw input.
- **Upstream template:** [docsygen on GitHub](https://github.com/YOUR_USER/docsygen) — replace `YOUR_USER` when you fork or publish your own copy.

---

**Quick workflow (from `/help`):**

- **Think:** `.docs/idea.md` → `/seed`, `/seed-update`, `/seed-review`
- **Shape:** `/prototype` → `/stack` → `/design`
- **Build:** `/scaffold` → `/setup` → `/new` or `/next` (from `.docs/backlog.md`) → `/resume` → `/test` → `/review`
- **Maintain:** `/tidy` → `/sync` → `/deps` → `/env` → `/performance` → `/a11y` → `/ux-review` → `/version` → `/onboard`

**Tip:** Drop tasks in `.docs/backlog.md` anytime.
