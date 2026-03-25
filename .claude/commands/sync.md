You are auditing the project's documentation against the actual state of the codebase. The goal is to catch doc drift — places where docs and reality have diverged.

**Read:**
- `.docs/seed-document.md` — the project's stated direction
- `.docs/tech-stack.md` — the declared tech choices (if exists)
- `.docs/design-system.md` — the declared design tokens and patterns (if exists)
- Recent git history (`git log --oneline -30`) — what's actually been happening
- Scan the actual codebase structure and key files

**Compare and report:**

1. **Direction drift** — Does the code still match what the seed document describes? Are there features built that aren't in the seed? Are seed features abandoned without updating the doc?

2. **Stack drift** — Are there dependencies or tools in the code that aren't in the tech stack doc? Has anything been replaced or added without updating the doc?

3. **Design drift** — Are design tokens actually used? Are there hardcoded values that should use the design system? Are there components that ignore the declared patterns?

4. **Undocumented changes** — Significant code changes in recent commits that aren't reflected in any doc.

**Output:**
- List each drift item with: what the doc says vs. what the code does
- For each item, propose the specific doc update needed (not code changes — the code is the source of truth)
- Ask the user which updates to apply

**RULES:**
- The code is always right. Docs adapt to code, not the other way around.
- Only flag meaningful drift, not nitpicks
- If everything is in sync, say so and move on — don't invent problems
- Don't touch the code. Only propose doc updates.
