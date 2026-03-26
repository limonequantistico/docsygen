Show the user the docsygen workflow. Don't execute any command, just print this guide clearly:

## Docsygen Workflow

### Phase 1 — Think
Define what you're building and challenge it before investing time.

1. Write raw notes in `.docs/idea.md`
2. `/seed` — Generate structured seed document from your idea
3. `/seed-update` — Integrate new notes into existing seed
4. `/seed-review` — Stress-test assumptions, find blind spots

### Phase 2 — Shape
Design the experience and define the tools. Prototype comes before stack because what you see in wireframes may influence tech choices.

5. `/prototype` — Generate a prompt for external design tools (Stitch, Figma AI, V0 etc.)
6. `/prototype-verify` — Analyze the wireframes you created externally
7. `/stack` — Define the tech stack (informed by prototype)
8. `/design` — Create the design system (visual tokens and decisions)

### Phase 3 — Build
Start coding. Use your own templates when you have them, or scaffold from scratch.

9. `/scaffold` — Validate existing project structure or create one from scratch
10. `/setup` — Wire design tokens into the codebase and build base components
11. `/component` — Build a new reusable component following the project's patterns
12. `/next` — Pick up and execute the first item from the backlog
13. `/resume` — Fresh situational assessment: where you are, what's next, what's off

### Phase 4 — Maintain
Keep docs honest without tracking every small change.

14. `/tidy` — Clean up the backlog, archive completed items
15. `/sync` — Reconcile docs with reality on demand. Also handles updates to design system and tech stack docs.

---

**Tips:**
- Dump ideas and tasks in `.docs/backlog.md` anytime. Pin it in the IDE to keep it visible. Use `/next` to work through them in order, `/tidy` to clean up and archive.
- Before building something directly into a feature, consider if it should be a reusable component first (`/component`).
- For small updates to the design system or tech stack, just tell the agent directly — no command needed. Use `/sync` to catch drift after bigger changes.

Ask the user which step they'd like to start with.
