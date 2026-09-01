```text
██████╗  ██████╗  ██████╗███████╗██╗   ██╗ ██████╗ ███████╗███╗   ██╗
██╔══██╗██╔═══██╗██╔════╝██╔════╝╚██╗ ██╔╝██╔════╝ ██╔════╝████╗  ██║
██║  ██║██║   ██║██║     ███████╗ ╚████╔╝ ██║  ███╗█████╗  ██╔██╗ ██║
██║  ██║██║   ██║██║     ╚════██║  ╚██╔╝  ██║   ██║██╔══╝  ██║╚██╗██║
██████╔╝╚██████╔╝╚██████╗███████║   ██║   ╚██████╔╝███████╗██║ ╚████║
╚═════╝  ╚═════╝  ╚═════╝╚══════╝   ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═══╝
 The Comprehensive Documentation Toolset

╔═══════════════════════╗  [INIT] Starting Docsygen CLI...
║ 31          Dev Tools ║  [INFO] Version 1.7.0 (Build 512)
║                       ║
║                       ║  [INFO] Element ID: [dOc]
║         d O c         ║  [INFO] Group: Dev Tools
║                       ║  [INFO] Registered to: DEVTOOLS GLOBAL
║                       ║
║       Docsygen        ║  [OK] Plugins: auto-gen, type-inference
║         1.7.0         ║  [OK] Config: /etc/docsygen/config.toml
╚═══════════════════════╝  [READY] System is operational.
 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒

Type '/help' to list available commands.
docsygen >
```

```text
╔════════════════════════════════════════════════════════════════╗
║  CLAUDE CODE — QUICK GUIDE  ·  install once per machine        ║
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
║  CODEX — QUICK GUIDE  ·  install once per machine              ║
╟────────────────────────────────────────────────────────────────╢
║  codex plugin marketplace add limonequantistico/docsygen       ║
║  codex plugin add docsygen@docsygen                            ║
║                                                                ║
║  per project   /init   (or ask: "initialize docsygen")         ║
║  update        codex plugin marketplace upgrade docsygen       ║
╚════════════════════════════════════════════════════════════════╝
```

# Docsygen

**Docsygen** is a **documentation-driven development workflow** that runs in both [Claude Code](https://claude.com/claude-code) and [Codex](https://developers.openai.com/codex). It's a set of **31 skills** (`SKILL.md` files) that guide a project from raw idea → shaped design → tracked work → shipped release, keeping docs honest along the way.

It's **language-agnostic** — the skills and docs work the same whether the project is Swift, Android, web, or anything else. Docsygen ships no application code; it's a toolkit of skills plus a `.docs/` convention.

Skills are a **cross-agent standard**: the same [`skills/`](skills/) directory is the single source of truth for both agents. The repo is its own marketplace on each — one plugin manifest per agent, both pointing at that one `skills/` folder. One repo, no forks.

## Where this comes from

Docsygen wasn't designed as a framework. It grew out of my own work across several projects: every skill here exists because the same steps kept getting done by hand, or the same quality check kept getting skipped whenever I was moving fast. The goal was never to add process — it was to hit a consistent standard for code and content without having to hold the whole checklist in my head.

That also means it's opinionated in ways that fit those projects and may not fit yours. **None of it is fixed.** Delete the skills you'd never run, rewrite the ones that are close but wrong, add your own. The `.docs/` convention and the `CLAUDE.md` rules are the parts I'd keep; the command list is a starting point, not a spec.

One thing I'd pass on from experience: resist accumulating. There's about to be a skill for everything, and installing all of them is tempting — but you only reach for a handful in any given project, and a skill you've forgotten you have is worse than one you never installed. A small set you actually remember beats a large set you don't.

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

The repo doubles as a Codex plugin marketplace. From a terminal:

```
codex plugin marketplace add limonequantistico/docsygen
codex plugin add docsygen@docsygen
```

Requires a Codex CLI with plugin support (`codex plugin --help` should list `add` / `marketplace`).

> Alternative — track `main` directly. If you'd rather follow the branch than pinned versions, clone once and symlink Codex's skills folder at it, so updates are a single `git pull`:
>
> ```
> git clone https://github.com/limonequantistico/docsygen ~/.docsygen
> ln -s ~/.docsygen/skills ~/.codex/skills/docsygen
> ```
>
> `~/.codex/skills/` is global (all projects). For a single project shared with a team, copy skills into the repo's `.codex/skills/` and commit them instead. Don't run both methods at once — you'd load every skill twice.

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
claude plugin update docsygen@docsygen        # Claude Code (or /plugin update … in a session)

codex plugin marketplace upgrade docsygen     # Codex — refresh the marketplace snapshot,
codex plugin add docsygen@docsygen            #         then reinstall at the new version
```

> On the symlink alternative, `git -C ~/.docsygen pull` is the whole update — the symlink picks up changes immediately.

Skills update in place — nothing is copied into your project, so they never go stale. Your project's own `.docs/` content is yours and is untouched by updates.

## The workflow

`/help` prints this. The numbered phases are a spine, not a rule — the un-numbered sections have no fixed place in the order.

> **How to invoke:** In Claude Code, type the skill as a slash command (`/seed`). In Codex, either ask for the task in plain language (*"create the seed"*) — skills load by description — or name the skill directly. The `/name` notation below is the canonical reference for both.

### Phase 0 — Set up

| Command | Purpose                                                          |
| ------- | ---------------------------------------------------------------- |
| `/init` | Scaffold the baseline `.docs/` structure — and re-run it after updating docsygen to bring an older project up to current conventions. |

### Anytime — Sharpen and capture

Not a phase. These interrogate whatever you're currently holding in your head — a plan, a design, a half-formed decision — then write down what survives. Useful at any point in any project.

| Command            | Purpose                                                                                   |
| ------------------ | ----------------------------------------------------------------------------------------- |
| `/grill-me`        | Interactive interview that resolves every open decision before you build. |
| `/grill-with-docs` | A `/grill-me` interview that also captures glossary terms and Architecture Decision Records (ADRs) as it goes. The one to start a project with. |
| `/domain-modeling` | Maintain the ubiquitous language (`CONTEXT.md`) and record architectural decisions (ADRs). |
| `/to-prd`          | Synthesize the conversation and its decisions into a PRD under `.docs/prds/`.             |
| `/to-issues`       | Slice a plan/PRD into vertical items — into `.docs/backlog.md` or GitHub Issues, your pick. |
| `/resume`          | Fresh situational assessment after time away: where you are, what's next.                |

### Phase 1 — Think

Define what you're building, challenge it, and decide what you're building it with. **There are two ways in**, and `/init` asks which you want: dump raw notes into `.docs/idea.md`, or run `/grill-with-docs` and let the interview find the idea while settling the vocabulary. The second is the better route when the idea is still fuzzy. Either way the notes land in `.docs/idea.md` and `/seed` takes it from there.

| Command        | Purpose                                                                   |
| -------------- | ------------------------------------------------------------------------- |
| `/seed`        | Turn raw notes in `.docs/idea.md` into a structured seed document — and integrate later notes into it. |
| `/seed-review` | Stress-test the seed (scope, riskiest assumption, gaps) with a verdict.   |
| `/stack`       | Define the tech stack → `.docs/tech-stack.md`. Gates `/scaffold`, `/setup`, and `/design-system`. |

### Phase 2 — Shape

| Command          | Purpose                                                              |
| ---------------- | -------------------------------------------------------------------- |
| `/design-system` | Guided interview that settles the aesthetic direction and visual tokens → `.docs/design-system.md`. |
| `/prototype`     | Generate a paste-ready prompt **per screen** for external design tools, carrying the design system with it. |

This phase has one deliberately manual step in the middle: **collect screenshots of interfaces you like into `.docs/assets/imgs/references/`**. Taste is yours, not the agent's — but you don't have to start from a blank search. If that folder is empty, `/design-system` curates a shortlist first: named products worth studying and why, the right gallery for this kind of product, and what to look for given your users. Then the interview begins, and every question after that is sharper for it.

### Phase 3 — Build

| Command     | Purpose                                                         |
| ----------- | --------------------------------------------------------------- |
| `/scaffold` | Validate or create the project structure.                       |
| `/setup`    | Wire design tokens into the codebase and build base components. |
| `/test`     | Testing strategy, critical-path coverage, flakiness guardrails. |

### Phase 4 — Ship

| Command    | Purpose                                                                                                |
| ---------- | ------------------------------------------------------------------------------------------------------ |
| `/review`  | Read-only review of uncommitted changes before commit — or triage another agent's review of your work. |
| `/commit`  | Generate a copyable commit message for the latest changes (message only, runs nothing).                |
| `/push`    | Commit and push the current branch. Stops there — no PR, no merge.                                     |
| `/merge`   | One-shot ship, branch-aware: commit, then open+merge a PR against `main` — or push straight to `main` when already on it. |
| `/version` | Cut a new app version; record it in `versions.json`.                                                   |

### Quality passes

Focused reviews of what's already built. Run one when that dimension matters, not on a schedule.

| Command        | Purpose                                                                     |
| -------------- | --------------------------------------------------------------------------- |
| `/ux-review`   | UI/UX quality check (hierarchy, flow, consistency, cognitive load) — and the agent's eyes setup. |
| `/a11y`        | WCAG-focused accessibility pass on the current UI.                          |
| `/logs`        | Establish or audit application logging → `.docs/logging.md`.                |
| `/performance` | Performance and observability (bottlenecks, baselines, metrics, tracing).   |

**`/ux-review` is where the agent gets its eyes.** Reviewing a UI by reading source is guessing, so the skill's first job is working out how to reach the *real running product*: it investigates what's possible for this project, proposes a ranked shortlist (browser tooling via the `chrome-devtools` MCP server, a simulator, a screenshot script, an existing e2e harness — or just screenshots you take yourself), and tells you what each one needs from you. **You decide what it's allowed to touch** — it proposes, it doesn't install. The working path is recorded in `.docs/preview.md`, so every later run, including `/a11y`, starts with sight instead of guesswork. Findings are labelled seen/measured or inferred, so a guess never reads like an observation. Screenshots a run captures are kept under `.docs/assets/imgs/screens/<date>/`, giving you a visual history and the agent a regression baseline — never a substitute for looking at the live app. All of it is optional; nothing breaks without it.

### Maintain & harden

| Command    | Purpose                                                            |
| ---------- | ------------------------------------------------------------------ |
| `/drift`   | Find where docs and code have diverged; fix each in the right direction. |
| `/tidy`    | Clean up the backlog; move completed items to the changelog.       |
| `/deps`    | Bump dependencies to latest stable; align `tech-stack.md`.         |
| `/env`     | Environment variables, secrets hygiene, production checklist.      |
| `/clean`   | Audit modularity and separation of concerns; refactor on approval. |
| `/onboard` | Refresh README / onboarding so another dev can run and contribute. |

**The planning pipeline:** `/grill-me` resolves open decisions → `/to-prd` documents them → `/to-issues` slices them into backlog items → you build each one. All four sit in **Anytime** because the loop starts whenever a decision gets murky, not at a fixed point in the project. The trigger for the last two is continuity: run `/to-prd` when the reasoning must outlive the session, `/to-issues` when the work spans more than one sitting. For a feature you'll finish this afternoon, both are overhead.

**Writing the code needs no command.** The `CLAUDE.md` that `/init` writes already tells the agent to load the stack, design system, and seed, read nearby code before writing new code, extend rather than duplicate, and skip the over-building — on every task, whether or not you typed a slash command. Describe the work, or paste a backlog item.

## Principles

The shape of this toolkit follows a few rules. They're worth knowing mostly because they explain what *isn't* here.

- **The cost of a skill isn't writing it — it's remembering it exists.** Every command added is one more to forget at the exact moment it would have helped. So new behaviour goes wherever it already fires — a project rule in `CLAUDE.md`, a step inside a skill you were going to run anyway — and only becomes its own command when it genuinely has to be invoked on purpose.
- **A command needs a trigger moment.** The ones that get used answer a question you actually ask out loud: *what changed while I was away?* → `/resume`. *Ship it* → `/merge`. A command whose trigger is "I'm about to write code" will never get typed, because that's the default state — which is exactly why writing code needs no command here.
- **Name it for what it does.** `/drift` finds drift. It used to be called `/sync`, which implied a direction it doesn't actually have.
- **Measured beats inferred, and the difference is stated.** A contrast ratio from a real audit and one guessed from a hex value are not the same claim. The quality passes label which one you got, so a hypothesis never reads like an observation.
- **Propose, don't install.** Anything that needs new access — a browser, a simulator, a dependency, a vendor — is offered with its trade-offs. You grant it.
- **Taste stays yours.** The agent curates options, measures what's measurable, and records what you decide. It doesn't pick the aesthetic, cut the version, or delete the plan.

## Project map

After `/init` (and as commands run), a project's docs live under `.docs/`:

| Location                  | Purpose                                                      | Created by |
| ------------------------- | ------------------------------------------------------------ | ---------- |
| `.docs/idea.md`           | Raw notes; input for `/seed`.                                | `/init`    |
| `.docs/backlog.md`        | Scratchpad task queue; pin it in your IDE.                   | `/init`    |
| `.docs/changelog.md`      | Dated log of work and command runs.                          | `/init`    |
| `.docs/changelog-spec.md` | Canonical changelog format (commands follow this).           | `/init`    |
| `.docs/assets/imgs/`      | Prototypes and references.                                   | `/init`    |
| `.docs/seed.md`           | Product/context seed.                                        | `/seed`    |
| `.docs/tech-stack.md`     | Tools and runtime versions.                                  | `/stack`   |
| `.docs/design-system.md`  | Visual tokens and UI rules.                                  | `/design-system` |
| `.docs/prds/`             | Product requirement docs.                                    | `/to-prd`  |
| `.docs/preview.md`        | How to run the app so the agent can see it.                  | `/ux-review` |
| `.docs/assets/imgs/screens/` | Dated screenshots of the running app; visual history and regression baseline. | `/ux-review` |
| `.docs/logging.md`        | The logging contract: fields, levels, what never gets logged. | `/logs`   |
| `.docs/adr/`              | Architecture Decision Records (numbered, append-only).       | `/domain-modeling` |
| `CONTEXT.md`              | Ubiquitous-language glossary (root, or per context).         | `/domain-modeling` |
| `CONTEXT-MAP.md`          | Map of bounded contexts (multi-context repos only).          | `/domain-modeling` |
| `CLAUDE.md`               | Project rules agents follow.                                 | `/init`    |

## Conventions

- **Changelog:** Every command logs to `.docs/changelog.md` in the format defined by `.docs/changelog-spec.md`. Timestamps (`HH:mm`) are never stripped.
- **Backlog vs. GitHub Issues — two stages, not two lists.** `.docs/backlog.md` is the scratchpad: pin it in your IDE and dump anything in one line. No network, no auth, no context switch, and the agent reads it for free on every task. GitHub Issues is for work that's *definitely happening* — assignable, discussable, linkable to a PR, visible to people who aren't you. An item graduates from one to the other and never lives in both, so there is nothing to keep in sync. `/to-issues` writes to whichever you pick, proposing GitHub when the repo has a remote, `gh` is authenticated, and issues already exist.
- **Backlog-driven:** hand an item to the agent when you're ready to build it, `/tidy` archives done backlog work to the changelog (closed issues are their own record), `/version` cuts releases.
- **Before committing:** Run `/review` for a read-only pass; reach for a quality pass (`/ux-review`, `/a11y`, `/performance`) or `/test` / `/env` when those dimensions matter. For a second opinion, have another agent run `/review`, then paste its findings back into `/review` on the original agent to triage and apply the ones that hold up.
- **Measured over inferred:** The UI quality passes open the real running app when they can reach it and label every finding accordingly. A finding read off the source is a hypothesis, and it says so.
- **Propose, don't install:** Skills that need new access — a browser, a simulator, a dependency — present the options and let you grant them. Nothing reaches for a new resource on its own.
- **Truth over docs:** If docs and code disagree about what *exists*, the code wins — run `/drift` to reconcile. What the docs say is *intended* is a different matter: `/drift` confirms before removing a plan the code hasn't caught up to yet.

## Developing Docsygen itself

This repository **is** the source of truth, the plugin, and the marketplace — for both agents at once:

- [`skills/`](skills/) — the 31 skills, one `SKILL.md` per directory. This is the single source both agents use, and this repo also dogfoods them directly. Claude Code auto-discovers it as the plugin's skills; Codex reads it via the `skills` path in its manifest.
- `.claude-plugin/plugin.json` — Claude Code plugin manifest (name, version). Components in `skills/` are auto-discovered, so there's no path to maintain.
- `.claude-plugin/marketplace.json` — makes the repo its own Claude Code marketplace.
- `.codex-plugin/plugin.json` — Codex plugin manifest. Mirrors the Claude one, plus an `interface` block (display name, category, sample prompts) and an explicit `"skills": "./skills/"`.
- `.agents/plugins/marketplace.json` — makes the repo its own Codex marketplace. The single plugin entry uses `"path": "."`, so the repo root *is* the plugin root.

To work on it:

- **Add a skill — but first check it needs to be one.** If the behaviour could live as a rule in the `CLAUDE.md` that `/init` writes, or as a step inside a skill that already runs at the right moment, put it there instead: it then costs nobody any recall. Reserve a new command for things that genuinely have to be invoked deliberately. To add one: create `skills/<name>/SKILL.md` with YAML frontmatter (`name` + `description`). The description controls when the agent reaches for it — gate deliberate steps to explicit invocation (*"Use only when the user explicitly asks … or runs /name"*) so they don't auto-fire. Add it to the `/help` skill so it's documented.
- **Validate:** run `python3 scripts/validate.py` — it checks every `SKILL.md` has frontmatter with a `name` matching its directory and a `description`, that all four manifests parse, that the two `plugin.json` versions and the README banner agree, and that `/help` lists every skill. The same script runs in CI on every push and PR ([`.github/workflows/validate.yml`](.github/workflows/validate.yml)). Additionally: `claude plugin validate .` for Claude Code, and for Codex `codex plugin marketplace add .` from a clone, then `codex plugin add docsygen@docsygen` — it fails loudly on a malformed manifest.
- **Ship an update:** bump `version` in **both** `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` (keep them equal), update the two version spots in the README banner, then push. `scripts/validate.py` fails if you miss one of the four. ⚠️ Both agents cache by version — pushing commits alone does nothing. Users then run `/plugin update docsygen@docsygen` (Claude Code) or `codex plugin marketplace upgrade docsygen && codex plugin add docsygen@docsygen` (Codex).

Repo: [github.com/limonequantistico/docsygen](https://github.com/limonequantistico/docsygen)

## License

[MIT](LICENSE) — use it, fork it, adapt it to your own workflow.
