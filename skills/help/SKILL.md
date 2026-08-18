---
name: help
description: Show the docsygen workflow guide — the full command reference and recommended order. Use only when the user explicitly asks for help or runs /help.
---

Show the user the docsygen workflow. Don't execute any command, just print this guide clearly:

## Docsygen Workflow

Changelog entries (command runs, completed tasks, releases) live in `.docs/changelog.md` and follow **`.docs/changelog-spec.md`**.

### Phase 0 — Set up

In a brand-new project, run this once to create the baseline docs structure the other commands rely on.

0. `/init` — Scaffold the `.docs/` skeleton (`idea.md`, `backlog.md`, `changelog.md`, `changelog-spec.md`, asset folders). Idempotent — safe to re-run; never overwrites existing work.

### Phase 1 — Think

Define what you're building and challenge it before investing time.

1. Write raw notes in `.docs/idea.md`
2. `/seed` — Generate structured seed document from your idea
3. `/seed-update` — Integrate new notes into existing seed
4. `/seed-review` — Quick structured stress-test of the seed (scope, riskiest assumption, gaps) with a Proceed/Revise/Rethink verdict
5. `/grill-me` — Interactive interview that walks the decision tree one question at a time, resolving every open decision in a plan or design before you invest in building
6. `/grill-with-docs` — A `/grill-me` interview that also captures the domain model as it goes (glossary terms and ADRs via `/domain-modeling`)
7. `/domain-modeling` — Actively build and sharpen the domain model: maintain the ubiquitous language in `CONTEXT.md` and record architectural decisions as ADRs in `.docs/adr/`

### Phase 2 — Shape

Design the experience and define the tools. Prototype comes before stack because what you see in wireframes may influence tech choices.

8. `/prototype` — Generate a prompt for external design tools (Stitch, Figma AI, V0, etc.); save wireframes under `.docs/assets/imgs/prototypes/` when ready
9. `/stack` — Define the tech stack (informed by prototype)
10. `/design` — Create the design system (visual tokens and decisions)

### Phase 3 — Build

Turn a shaped idea into tracked work, then start coding. Use your own templates when you have them, or scaffold from scratch.

11. `/to-prd` — Synthesize the current conversation and decisions into a PRD saved under `.docs/prds/` (no interview — run `/grill-me` first if decisions are still open)
12. `/to-issues` — Break a plan or PRD into independently-grabbable, vertically-sliced backlog items in `.docs/backlog.md`
13. `/scaffold` — Validate existing project structure or create one from scratch
14. `/setup` — Wire design tokens into the codebase and build base components
15. `/new` — Ad-hoc feature or fix with full project context (also how you pull a backlog item into action — pass it as context)
16. `/resume` — Fresh situational assessment: where you are, what's next, what's off
17. `/test` — Testing strategy, critical-path coverage, flakiness guardrails
18. `/review` — Read-only review of uncommitted changes before commit, or triage another agent's review of your work
19. `/commit` — Generate a copyable commit message for the latest changes (message only, runs nothing)
20. `/push` — Commit and push the current branch (*does* run git). Stops at the push: no branch, no PR, no merge
21. `/merge` — One-shot ship (*does* run git and `gh`): generate a message, then commit and — on a feature branch — push, open a PR against `main`, and auto-merge it; or, if you're already on `main`, push straight to it with no branch and no PR

### Phase 4 — Maintain & harden

Keep docs honest, dependencies current, and quality visible.

22. `/tidy` — Clean up the backlog, move completed items to the changelog
23. `/sync` — Reconcile docs with reality (seed, stack, design, components)
24. `/deps` — Bump dependencies to latest stable versions; align `tech-stack.md`
25. `/env` — Environment variables, secrets hygiene, production config checklist
26. `/performance` — Performance and observability (logging, metrics, bottlenecks)
27. `/a11y` — WCAG-focused accessibility pass on the current UI
28. `/ux-review` — Broader UI/UX quality check (hierarchy, flow, consistency)
29. `/clean` — Audit modularity, structure, and separation of concerns; refactor on approval
30. `/version` — Cut a new app version: reviews changes, writes to `versions.json`
31. `/onboard` — Refresh README / onboarding so another dev can run and contribute

---

**Tips:**

- The planning pipeline: `/grill-me` resolves open decisions → `/to-prd` documents them → `/to-issues` slices them into backlog items → `/new` builds each one.
- Dump ideas and tasks in `.docs/backlog.md` anytime. Pin it in the IDE. Use `/to-issues` to break a plan into items, `/new` to work through them, `/tidy` to archive done items to the changelog, `/version` when cutting a release.
- Reusable UI can be built via `/new`; there is no separate `/component` command.
- For small updates to the design system or tech stack, you can ask the agent directly. Use `/sync` after bigger changes to catch drift.
- Three levels of commitment: `/commit` writes the message and stops, `/push` commits and pushes the branch you're on, `/merge` gets the work into `main`. `/merge` is branch-aware — on a feature branch it ships via PR, on `main` it just commits and pushes — so you don't need to check which branch you're on first.
- Run `/review` before commits; use `/test`, `/env`, `/performance`, or `/a11y` when those dimensions matter. For a second opinion, have another agent run `/review` and paste its findings back into `/review` on the original agent to triage them.
- To pin down the domain language while you think, run `/grill-with-docs` instead of `/grill-me` — it captures glossary terms (`CONTEXT.md`) and architectural decisions (ADRs in `.docs/adr/`) as the interview surfaces them. Use `/domain-modeling` on its own to sharpen the glossary or record an ADR outside an interview.

---

**Version check.** After printing the guide, check whether the user is on the latest docsygen. Both agents cache plugins by version and third-party marketplaces don't auto-update by default, so an out-of-date install is the normal state, not the exception:

```bash
INSTALLED="$(cat "${CLAUDE_PLUGIN_ROOT:-.}/.claude-plugin/plugin.json" 2>/dev/null | grep -o '"version"[^,]*' | head -1 | cut -d'"' -f4)"
LATEST="$(curl -fsSL --max-time 5 https://raw.githubusercontent.com/limonequantistico/docsygen/main/.claude-plugin/plugin.json 2>/dev/null | grep -o '"version"[^,]*' | head -1 | cut -d'"' -f4)"
echo "installed=${INSTALLED:-unknown} latest=${LATEST:-unknown}"
```

- **Same version, or either value is unknown** — say nothing. A failed network call is not worth a line of output.
- **Installed is behind** — add one line at the bottom with the version numbers and the right command for the agent in use:
  - Claude Code: `claude plugin update docsygen@docsygen`
  - Codex: `codex plugin marketplace upgrade docsygen && codex plugin add docsygen@docsygen`

Don't run the update — just show the command. Don't offer to check again.

---

Ask the user which step they'd like to start with.
