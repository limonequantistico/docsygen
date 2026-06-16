Show the user the docsygen workflow. Don't execute any command, just print this guide clearly:

## Docsygen Workflow

Changelog entries (command runs, completed tasks, releases) live in `.docs/changelog.md` and follow **`.docs/changelog-spec.md`**.

### Phase 1 — Think

Define what you're building and challenge it before investing time.

1. Write raw notes in `.docs/idea.md`
2. `/seed` — Generate structured seed document from your idea
3. `/seed-update` — Integrate new notes into existing seed
4. `/seed-review` — Quick structured stress-test of the seed (scope, riskiest assumption, gaps) with a Proceed/Revise/Rethink verdict
5. `/grill-me` — Interactive interview that walks the decision tree one question at a time, resolving every open decision in a plan or design before you invest in building

### Phase 2 — Shape

Design the experience and define the tools. Prototype comes before stack because what you see in wireframes may influence tech choices.

6. `/prototype` — Generate a prompt for external design tools (Stitch, Figma AI, V0, etc.); save wireframes under `.docs/assets/imgs/prototypes/` when ready
7. `/stack` — Define the tech stack (informed by prototype)
8. `/design` — Create the design system (visual tokens and decisions)

### Phase 3 — Build

Turn a shaped idea into tracked work, then start coding. Use your own templates when you have them, or scaffold from scratch.

9. `/to-prd` — Synthesize the current conversation and decisions into a PRD saved under `.docs/prds/` (no interview — run `/grill-me` first if decisions are still open)
10. `/to-issues` — Break a plan or PRD into independently-grabbable, vertically-sliced backlog items in `.docs/backlog.md`
11. `/scaffold` — Validate existing project structure or create one from scratch
12. `/setup` — Wire design tokens into the codebase and build base components
13. `/new` — Ad-hoc feature or fix with full project context (also how you pull a backlog item into action — pass it as context)
14. `/resume` — Fresh situational assessment: where you are, what's next, what's off
15. `/test` — Testing strategy, critical-path coverage, flakiness guardrails
16. `/review` — Read-only review of uncommitted changes before commit
17. `/commit` — Generate a copyable commit message for the latest changes

### Phase 4 — Maintain & harden

Keep docs honest, dependencies current, and quality visible.

18. `/tidy` — Clean up the backlog, move completed items to the changelog
19. `/sync` — Reconcile docs with reality (seed, stack, design, components)
20. `/deps` — Bump dependencies to latest stable versions; align `tech-stack.md`
21. `/env` — Environment variables, secrets hygiene, production config checklist
22. `/performance` — Performance and observability (logging, metrics, bottlenecks)
23. `/a11y` — WCAG-focused accessibility pass on the current UI
24. `/ux-review` — Broader UI/UX quality check (hierarchy, flow, consistency)
25. `/clean` — Audit modularity, structure, and separation of concerns; refactor on approval
26. `/version` — Cut a new app version: reviews changes, writes to `versions.json`
27. `/onboard` — Refresh README / onboarding so another dev can run and contribute

---

**Tips:**

- The planning pipeline: `/grill-me` resolves open decisions → `/to-prd` documents them → `/to-issues` slices them into backlog items → `/new` builds each one.
- Dump ideas and tasks in `.docs/backlog.md` anytime. Pin it in the IDE. Use `/to-issues` to break a plan into items, `/new` to work through them, `/tidy` to archive done items to the changelog, `/version` when cutting a release.
- Reusable UI can be built via `/new`; there is no separate `/component` command.
- For small updates to the design system or tech stack, you can ask the agent directly. Use `/sync` after bigger changes to catch drift.
- Run `/review` before commits; use `/test`, `/env`, `/performance`, or `/a11y` when those dimensions matter.

Ask the user which step they'd like to start with.
