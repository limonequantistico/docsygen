You are helping the user resume work on this project. Generate a fresh situational assessment — not a static checklist.

**Custom instructions from user:** $ARGUMENTS

**Read the current state:**
- Recent git history — ask the user how many commits to check before reading (e.g., "How many recent commits should I look at? A handful or more?")
- `.docs/seed-document.md` for project direction
- Scan the project files to understand current structure and what's actually built
- Check for TODO/FIXME/HACK comments in the codebase
- `.docs/tech-stack.md` and `.docs/design-system.md` if they exist
- `.docs/idea.md` — check if there are unprocessed notes or ideas the user jotted down
- `.docs/backlog.md` — check pending items (if it exists)

**Output:**

1. **Where you are** — Brief summary of current project state based on what actually exists (not what was planned). What's built, what's half-done, what hasn't been touched.

2. **What seems next** — Based on the project's direction and current state, suggest 1-3 concrete next steps. Be specific ("implement the login screen using the auth flow from the seed doc") not vague ("continue working on features"). If the project is in the documentation phase, suggest the next docsygen command to run.

3. **Unprocessed ideas** — If `.docs/idea.md` has content, mention that there are unprocessed ideas and suggest running `/tidy`. If `.docs/backlog.md` has pending items, list them briefly so the user can see what's on the table.

4. **Watch out** — Flag anything that looks off: docs that contradict the code, half-finished work that should be completed or reverted, scope creep signals. If things look significantly drifted, suggest running `/sync`.

**RULES:**
- Base everything on what you actually see, not assumptions
- Keep it short — the user wants to start working, not read a report
- This assessment is always generated fresh from the current state. No static task files.
- If the project is brand new and there's nothing to resume, say so and point to `/help`
