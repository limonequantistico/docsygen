---
name: help
description: Show the docsygen workflow guide — the full command reference and recommended order. Use only when the user explicitly asks for help or runs /help.
---

Show the user the docsygen workflow. Don't execute any command, just print this guide clearly:

## Docsygen Workflow

Changelog entries (command runs, completed tasks, releases) live in `.docs/changelog.md` and follow **`.docs/changelog-spec.md`**.

The numbered phases are a spine, not a rule. The un-numbered sections have **no fixed place in the order** — reach for them whenever the work calls for them.

### Phase 0 — Set up

In a brand-new project, run this once to create the baseline docs structure the other commands rely on.

0. `/init` — Scaffold the `.docs/` skeleton (`idea.md`, `backlog.md`, `changelog.md`, `changelog-spec.md`, asset folders) plus a root `CLAUDE.md`. Idempotent — safe to re-run; never overwrites existing work. **Re-run it after updating docsygen** to catch conventions that changed since this project was set up.

Optionally, on an existing codebase of any size: install [CodeGraph](https://github.com/colbymchenry/codegraph) (`npm install -g @colbymchenry/codegraph`) and run `codegraph init` once in the repo. Docsygen works without it — but where a `.codegraph/` directory exists, the agent navigates code by call graph instead of grep, and `/review` and `/clean` get real blast-radius numbers.

### Anytime — Sharpen and capture

These interrogate whatever you're currently holding in your head — a plan, a design, a half-formed decision — then write down what survives. Useful at any point in any project, before writing code or in the middle of it.

- `/grill-me` — Interactive interview that walks the decision tree one question at a time, resolving every open decision in a plan or design before you invest in building
- `/grill-with-docs` — A `/grill-me` interview that also captures the domain model as it goes (glossary terms and Architecture Decision Records via `/domain-modeling`). The one to reach for when **starting** a project or feature, while the vocabulary is still up for grabs
- `/domain-modeling` — Actively build and sharpen the domain model: maintain the ubiquitous language in `CONTEXT.md` and record decisions as ADRs in `.docs/adr/`
- `/to-prd` — Synthesize the current conversation and its decisions into a PRD saved under `.docs/prds/`. Reach for it when the *reasoning* needs to outlive the session
- `/to-issues` — Break a plan or PRD into independently-grabbable, vertical slices, written to `.docs/backlog.md` or GitHub Issues (it asks). Reach for it when the work spans more than one sitting
- `/resume` — Fresh situational assessment after time away: where you are, what's next, what's off

### Phase 1 — Think

Define what you're building, challenge it, and decide what you're building it with.

**Two ways in** — `/init` asks which you want, and you can switch at any point:

- **Write it down.** Dump raw notes into `.docs/idea.md` — bullet points, a voice transcription, anything. Best when you already roughly know what you want.
- **Talk it out.** Run `/grill-with-docs` and let the interview find the idea, settling the vocabulary as it goes. Best when it's still fuzzy — waiting until you can write a coherent brief is exactly the wrong order.

Both converge on `/seed`, which reads `.docs/idea.md` *or* works from an interview still in the conversation.

1. Start with notes in `.docs/idea.md`, or a `/grill-with-docs` session
2. `/seed` — Turn your notes into a structured seed document; run it again later to integrate new notes into the existing seed
3. `/seed-review` — Quick structured stress-test of the seed (scope, riskiest assumption, gaps) with a Proceed/Revise/Rethink verdict
4. `/stack` — Define the tech stack. It gates `/scaffold`, `/setup`, and `/design-system`, so settle it before shaping anything

### Phase 2 — Shape

Design the experience before building it. This phase has one manual step in the middle — collecting reference screens — because taste is yours, not the agent's.

5. **Collect inspiration** — drop screenshots of interfaces you like into `.docs/assets/imgs/references/`. `/design-system` will curate a shortlist of what to look at if the folder is empty, so you don't have to start from a blank search
6. `/design-system` — Settle the aesthetic direction and visual tokens through a guided interview: it proposes options, you choose, and nothing is written until you do
7. `/prototype` — Generate a **paste-ready prompt per screen** for external design tools (Claude Design, Stitch, Figma AI, V0), carrying the design system with it so the output is usable rather than something to look past; save the screens you like under `.docs/assets/imgs/prototypes/`

### Phase 3 — Build

Stand up the structure, then write the code. There's no command for writing the code itself — describe the work, or paste a backlog item, and the project rules in `CLAUDE.md` carry the context.

8. `/scaffold` — Validate existing project structure or create one from scratch
9. `/setup` — Wire design tokens into the codebase and build base components
10. `/test` — Testing strategy, critical-path coverage, flakiness guardrails

### Phase 4 — Ship

Get the work reviewed, committed, and out.

11. `/review` — Read-only review of uncommitted changes before commit, or triage another agent's review of your work
12. `/herdr-review` — Automated second opinion inside [herdr](https://herdr.dev): spawns a reviewer agent in a sibling pane, captures its review, triages the findings, and applies the ones that hold up — no copy-paste
13. `/commit` — Generate a copyable commit message for the latest changes (message only, runs nothing)
14. `/push` — Commit and push the current branch (*does* run git). Stops at the push: no branch, no PR, no merge
15. `/merge` — One-shot ship (*does* run git and `gh`): generate a message, then commit and — on a feature branch — push, open a PR against `main`, and auto-merge it; or, if you're already on `main`, push straight to it with no branch and no PR
16. `/version` — Cut a new app version: reviews changes, writes to `versions.json`

### Quality passes

Focused reviews of what's already built. Run one when that dimension matters — not on a schedule.

- `/deep-audit` — The broad one: a whole-codebase sweep for latent bugs, security holes, broken failure paths, and architectural risk. No time limit, but every finding must survive a verification pass, so a clean codebase reports clean. Writes a stamped report to `.docs/audits/`, fixes only what you approve
- `/ux-review` — UI/UX quality check (hierarchy, flow, consistency, cognitive load). **Sets up the agent's eyes**: proposes ways to reach the real running app, and records the working one in `.docs/preview.md`
- `/a11y` — WCAG-focused accessibility pass on the current UI, reusing the same access path
- `/logs` — Establish or audit application logging: what gets recorded, at what level, with what context — shaped to the project's architecture, contract written to `.docs/logging.md`
- `/performance` — Performance and observability (bottlenecks, baselines, metrics, tracing)

### Maintain & harden

Keep docs honest, dependencies current, and the structure from rotting.

- `/drift` — Find where docs and code have diverged (seed, stack, design, components) and fix each in the right direction
- `/tidy` — Clean up the backlog, move completed items to the changelog
- `/deps` — Bump dependencies to latest stable versions; align `tech-stack.md`
- `/env` — Environment variables, secrets hygiene, production config checklist
- `/clean` — Audit modularity, structure, and separation of concerns; refactor on approval
- `/onboard` — Refresh README / onboarding so another dev can run and contribute

---

**Tips:**

- The planning pipeline: `/grill-me` resolves open decisions → `/to-prd` documents them → `/to-issues` slices them into backlog items → you build each one. All four live in **Anytime** because the loop starts whenever a decision gets murky, not at a fixed point in the project.
- Not sure whether you need `/to-prd` and `/to-issues`? The trigger is continuity, not size. If the reasoning would be lost when the session resets, run `/to-prd`. If the work spans more than one sitting, run `/to-issues`. For a feature you'll finish this afternoon, both are overhead — you are the continuity.
- **Backlog vs. GitHub Issues — two stages, not two lists.** `.docs/backlog.md` is the scratchpad: pin it in your IDE and dump anything, any time, in one line. No network, no auth, no context switch, and the agent reads it for free on every task. GitHub Issues is for work that's *definitely happening* — assignable, discussable, linkable to a PR, visible to someone who isn't you. An item graduates from one to the other; it never lives in both, so there's nothing to keep in sync.
- `/to-issues` writes to whichever you pick — it proposes GitHub when the repo has a remote, `gh` is authenticated, and issues already exist, and the backlog otherwise. Then hand one item to the agent when you're ready to build it, `/tidy` to archive done backlog items to the changelog (closed issues are their own record), `/version` when cutting a release.
- Building features and components needs no command — the `CLAUDE.md` that `/init` writes already tells the agent to load the stack, design system, and seed, match nearby code, and extend before duplicating.
- Running `/seed` again is how you update it — the first run creates `.docs/seed.md`, later runs integrate new notes into it, flagging conflicts and pivots instead of silently overwriting.
- Don't try to remember `/drift` — the project rules tell the agent to flag a doc that contradicts the code and offer it. Reach for it yourself after a long stretch of building, before handing the project to someone else, or after a pivot.
- If a command here feels like one you'd never remember to type, that's a bug in the command, not in you. The cost of a skill isn't writing it — it's remembering it exists, so anything that can live as a project rule or a step inside another skill does.
- Three levels of commitment: `/commit` writes the message and stops, `/push` commits and pushes the branch you're on, `/merge` gets the work into `main`. `/merge` is branch-aware — on a feature branch it ships via PR, on `main` it just commits and pushes — so you don't need to check which branch you're on first.
- Run `/review` before commits. For a second opinion inside herdr, `/herdr-review` automates the whole loop — it spawns a reviewer agent, triages its findings, and applies the ones that hold up, including one round of pushback on what it rejected. Outside herdr, do it by hand: have another agent run `/review` and paste its findings back into `/review` on the original agent.
- **Three review scopes, not three depths.** `/review` looks at the uncommitted diff, `/clean` at structure across the codebase, `/deep-audit` at correctness and safety across the codebase. `/deep-audit` isn't `/clean` turned up — it's the dimension `/clean` deliberately doesn't cover, and it hands structure back to `/clean` when it trips over it.
- Every `/deep-audit` report is stamped with the model, its reasoning effort, and the commit it ran against. Re-running it after a stronger model ships — or the same model at a higher effort — gives you two files you can diff by eye. That's the cheapest way to find out whether the new model actually sees more.
- Quality passes report whether each finding was **measured** against the running app or **inferred** from code. Inferred findings are weaker — worth checking before you act on them.
- Give `/ux-review` a way to actually see the product and it stops guessing. It proposes options (`agent-browser`, the `chrome-devtools` MCP server, a simulator, a screenshot script, or just your own screenshots), you decide what it's allowed to touch, and the working path lands in `.docs/preview.md` for every run after that. Screenshots it captures are kept in `.docs/assets/imgs/screens/<date>/` as a visual history and a regression baseline.

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
