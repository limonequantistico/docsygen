Show the user the docsygen workflow. Don't execute any command, just print this guide clearly:

## Docsygen Workflow

Changelog entries (command runs, completed tasks, releases) live in `.docs/changelog.md` and follow **`.docs/changelog-spec.md`**.

### Phase 1 — Think

Define what you're building and challenge it before investing time.

1. Write raw notes in `.docs/idea.md`
2. `/seed` — Generate structured seed document from your idea
3. `/seed-update` — Integrate new notes into existing seed
4. `/seed-review` — Stress-test assumptions, find blind spots

### Phase 2 — Shape

Design the experience and define the tools. Prototype comes before stack because what you see in wireframes may influence tech choices.

5. `/prototype` — Generate a prompt for external design tools (Stitch, Figma AI, V0, etc.); save wireframes under `.docs/assets/imgs/prototypes/` when ready
6. `/stack` — Define the tech stack (informed by prototype)
7. `/design` — Create the design system (visual tokens and decisions)

### Phase 3 — Build

Start coding. Use your own templates when you have them, or scaffold from scratch.

8. `/scaffold` — Validate existing project structure or create one from scratch
9. `/setup` — Wire design tokens into the codebase and build base components
10. `/new` — Ad-hoc feature or fix with full project context (use when not pulling from the backlog)
11. `/next` — Pick up and execute the first item from `.docs/backlog.md`
12. `/resume` — Fresh situational assessment: where you are, what's next, what's off
13. `/test` — Testing strategy, critical-path coverage, flakiness guardrails
14. `/review` — Read-only review of uncommitted changes before commit
15. `/commit` — Generate a copyable commit message for the latest changes

### Phase 4 — Maintain & harden

Keep docs honest, dependencies current, and quality visible.

16. `/tidy` — Clean up the backlog, move completed items to the changelog
17. `/sync` — Reconcile docs with reality (seed, stack, design, components)
18. `/deps` — Bump dependencies to latest stable versions; align `tech-stack.md`
19. `/env` — Environment variables, secrets hygiene, production config checklist
20. `/performance` — Performance and observability (logging, metrics, bottlenecks)
21. `/a11y` — WCAG-focused accessibility pass on the current UI
22. `/ux-review` — Broader UI/UX quality check (hierarchy, flow, consistency)
23. `/clean` — Audit modularity, structure, and separation of concerns; refactor on approval
24. `/version` — Cut a new app version: reviews changes, writes to `versions.json`
25. `/onboard` — Refresh README / onboarding so another dev can run and contribute

---

**Tips:**

- Dump ideas and tasks in `.docs/backlog.md` anytime. Pin it in the IDE. Use `/next` to work through them in order, `/tidy` to archive done items to the changelog, `/version` when cutting a release.
- Reusable UI can be built via `/new` (or `/next` if the backlog says so); there is no separate `/component` command.
- For small updates to the design system or tech stack, you can ask the agent directly. Use `/sync` after bigger changes to catch drift.
- Run `/review` before commits; use `/test`, `/env`, `/performance`, or `/a11y` when those dimensions matter.

Ask the user which step they'd like to start with.
