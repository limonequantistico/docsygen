---
name: help
description: Show the docsygen workflow guide — the full command reference and recommended order. Use only when the user explicitly asks for help or runs /help.
---

Show the user the docsygen workflow. Don't execute any command, just print this guide clearly:

## Docsygen Workflow

Steps 0-8 are the spine: roughly the order a project goes through once. Everything after them has no fixed place — reach for it when the work calls for it.

### Phase 0 — Set up

| Step | Command | What it does |
| ---- | ------- | ------------ |
| 0 | `/init` | Scaffolds `.docs/` plus a root `CLAUDE.md`. Idempotent — **re-run it after updating docsygen**. |

### Phase 1 — Think

| Step | Command | What it does |
| ---- | ------- | ------------ |
| 1 | — *(manual)* | Dump raw notes into `.docs/idea.md` — or run `/grill-with-docs` and let the interview find the idea. |
| 2 | `/seed` | Turns your notes into a structured seed document. Run it again later to integrate new notes. |
| 3 | `/seed-review` | Stress-tests the seed (scope, riskiest assumption, gaps) with a Proceed/Revise/Rethink verdict. |
| 4 | `/stack` | Defines the tech stack. Gates `/scaffold`, `/setup`, and `/design-system` — settle it first. |

### Phase 2 — Shape

| Step | Command | What it does |
| ---- | ------- | ------------ |
| — *(manual)* | — | Drop screenshots of interfaces you like into `.docs/assets/imgs/references/`. |
| 5 | `/design-system` | Settles aesthetic direction and visual tokens through a guided interview. Curates a reference shortlist if you have none. |
| — | `/prototype` | Generates a paste-ready prompt **per screen** for external design tools, carrying the design system with it. |
| — | `/asset` | Makes an image, icon, illustration, marketing frame, or store screenshot — or just its prompt. |

### Phase 3 — Build

No command writes the code itself — describe the work, or paste a backlog item, and `CLAUDE.md` carries the context.

| Step | Command | What it does |
| ---- | ------- | ------------ |
| 6 | `/scaffold` | Validates existing project structure, or creates one from scratch. |
| 7 | `/setup` | Wires design tokens into the codebase and builds base components, always on role tokens so a later mode is cheap. |
| — | `/theming` | Adds or repairs color modes: dark, high contrast, brand themes. Offered by `/setup`. |
| — | `/showcase` | One dev-only page rendering every token and base component with its variants and states. Offered by `/setup`. |
| — | `/tweaks` | Dev-only panel to tune color, fonts, type scale, and shape live in the running app. Offered by `/setup`. |
| 8 | `/test` | Testing strategy, critical-path coverage, flakiness guardrails. |

### Anytime — Sharpen and capture

Interrogate what you're holding in your head — a plan, a design, a bug you can't explain — then write down what survives.

| Command | What it does |
| ------- | ------------ |
| `/grill-me` | Interview that walks the decision tree one question at a time, resolving every open decision before you build. |
| `/grill-with-docs` | A `/grill-me` interview that captures glossary terms and ADRs as it goes. **The one to start a project or feature with.** |
| `/domain-modeling` | Maintains the ubiquitous language in `CONTEXT.md` and records decisions as ADRs in `.docs/adr/`. |
| `/to-prd` | Synthesizes the conversation and its decisions into a PRD under `.docs/prds/`. |
| `/to-issues` | Slices a plan or PRD into vertical slices → `.docs/backlog.md` or GitHub Issues (it asks). |
| `/resume` | Fresh situational assessment after time away: where you are, what's next, what's off. |
| `/debug` | Diagnoses one bug you can point at — competing hypotheses, instrumentation, a reproduction, a root-cause fix, then cleanup. |

### Ship

Pick the level of commitment — these are alternatives, not a sequence.

| Command | What it does |
| ------- | ------------ |
| `/review` | Read-only review of uncommitted changes — or triage of another agent's review of your work. |
| `/herdr-review` | Automated second opinion inside [herdr](https://herdr.dev): spawns a reviewer agent, triages its findings, applies the ones that hold up. |
| `/commit` | Writes a copyable commit message. Runs nothing. |
| `/push` | Commits and pushes the current branch. No PR, no merge. |
| `/merge` | Ships it, branch-aware: PR against `main` + auto-merge on a feature branch, straight push when already on `main`. |
| `/version` | Cuts a new app version: reviews changes, writes to `versions.json`. |

### Quality passes

Focused reviews of what's already built. Run one when that dimension matters — not on a schedule.

| Command | What it does |
| ------- | ------------ |
| `/deep-audit` | Whole-codebase sweep for latent bugs, security holes, broken failure paths, architectural risk. Stamped report to `.docs/audits/`. |
| `/ux-review` | UI/UX quality check: hierarchy, flow, consistency, cognitive load. **Sets up the agent's eyes** → `.docs/preview.md`. |
| `/a11y` | WCAG-focused accessibility pass on the current UI, reusing the same access path. |
| `/logs` | Establishes or audits application logging — what, at what level, with what context → `.docs/logging.md`. |
| `/performance` | Performance and observability: bottlenecks, baselines, metrics, tracing. |

### Maintain & harden

| Command | What it does |
| ------- | ------------ |
| `/drift` | Finds where docs and code have diverged and fixes each in the right direction. |
| `/tidy` | Archives completed backlog items to the changelog; proposes burying items untouched 60+ days in `.docs/graveyard.md`. |
| `/deps` | Bumps dependencies to latest stable; aligns `tech-stack.md`. |
| `/env` | Environment variables, secrets hygiene, production config checklist. |
| `/clean` | Audits modularity, structure, and separation of concerns; refactors on approval. |
| `/onboard` | Refreshes README and onboarding so another dev can run and contribute. |

Work is logged to `.docs/changelog.md`, following `.docs/changelog-spec.md`. Full reference and conventions: the [README](https://github.com/limonequantistico/docsygen).

---

**Version check.** After printing the guide, check whether the user is on the latest docsygen. Both agents cache plugins by version and third-party marketplaces don't auto-update by default, so an out-of-date install is the normal state, not the exception:

```bash
INSTALLED="$(cat "${CLAUDE_PLUGIN_ROOT:-.}/.claude-plugin/plugin.json" 2>/dev/null | grep -o '"version"[^,]*' | head -1 | cut -d'"' -f4)"
LATEST="$(curl -fsSL --max-time 5 https://raw.githubusercontent.com/limonequantistico/docsygen/main/.claude-plugin/plugin.json 2>/dev/null | grep -o '"version"[^,]*' | head -1 | cut -d'"' -f4)"
echo "installed=${INSTALLED:-unknown} latest=${LATEST:-unknown}"
```

- **Same version, or either value is unknown** — say nothing. A failed network call is not worth a line of output.
- **Installed is behind** — add one line at the bottom with the version numbers and the right command for the agent in use, plus a reminder to run `/init` afterwards to bring this project's conventions up to date:
  - Claude Code: `claude plugin update docsygen@docsygen`
  - Codex: `codex plugin marketplace upgrade docsygen && codex plugin add docsygen@docsygen`

Don't run the update — just show the command. Don't offer to check again.

---

Ask the user which step they'd like to start with.
