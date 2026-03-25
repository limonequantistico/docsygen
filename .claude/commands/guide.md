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

5. `/prototype` — Generate a prompt for external design tools (Stitch, Figma AI, etc.)
6. `/prototype-verify` — Analyze the wireframes you created externally
7. `/stack` — Define the tech stack (informed by prototype)
8. `/stack-update` — Update stack with new decisions
9. `/design` — Create the design system
10. `/design-update` — Update design system

### Phase 3 — Build
Start coding. Use your own templates when you have them, or scaffold from scratch.

11. `/scaffold` — *(optional)* Init project for unfamiliar stacks where you don't have a template
12. `/resume` — Fresh situational assessment: where you are, what's next, what's off

### Phase 4 — Maintain
Keep docs honest without tracking every small change.

13. `/sync` — Reconcile docs with reality on demand. Run it when things feel out of sync.

---

`-update` commands (`/seed-update`, `/stack-update`, `/design-update`) are available anytime for targeted edits.

Ask the user which step they'd like to start with.
