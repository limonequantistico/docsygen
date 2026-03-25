You are helping the user resume work on this project. Generate a fresh situational assessment — not a static checklist.

**Read the current state:**
- Check recent git history (`git log --oneline -20`) to see what's been done
- Read `.docs/seed-document.md` for project direction
- Scan the project files to understand current structure
- Check for any TODO/FIXME/HACK comments in the codebase
- Read `.docs/tech-stack.md` and `.docs/design-system.md` if they exist

**Output:**

1. **Where you are** — Brief summary of current project state based on what actually exists (not what was planned). What's built, what's half-done, what hasn't been touched.

2. **What seems next** — Based on the project's direction and current state, suggest 1-3 concrete next steps. Be specific ("implement the login screen using the auth flow from the seed doc") not vague ("continue working on features").

3. **Watch out** — Flag anything that looks off: docs that contradict the code, dependencies that might cause issues, scope creep signals, half-finished work that should be completed or reverted.

**RULES:**
- Base everything on what you actually see, not assumptions
- Keep it short — the user wants to start working, not read a report
- Don't reference any tasks.md or similar file — this assessment is always generated fresh
- If the project is brand new and there's nothing to resume, say so and point to `/guide`
