You are auditing the project's documentation against the actual state of the codebase. The goal is to catch doc drift — places where docs and reality have diverged.

**Custom instructions from user:** $ARGUMENTS

**Read:**
- `.docs/seed-document.md` — the project's stated direction
- `.docs/tech-stack.md` — the declared tech choices (if exists)
- `.docs/design-system.md` — the declared design tokens (if exists)
- `.docs/archive/archive.md` — check the last entry date to understand how long it's been since the last sync or meaningful command run. Use this to calibrate how far back in git history to look: a few days means a handful of commits, a few weeks means a broader scan. If the archive is empty or missing, fall back to asking the user.
- Recent git history — use the time gap from the archive to decide how many commits to check. If the gap is unclear, ask the user (e.g., "How many recent commits should I look at to check for drift?").
- Scan the actual codebase structure, key files, and dependencies

**Compare and report:**

1. **Direction drift** — Does the code still match what the seed document describes? Features built that aren't in the seed? Seed features abandoned without updating the doc?

2. **Stack drift** — Dependencies or tools in the code that aren't in the tech stack doc? Anything replaced or added without updating the doc?

3. **Design drift** — Are design tokens from the design system actually used in the centralized styles file? Are there hardcoded values that should reference the centralized tokens instead?

4. **Component drift** — Duplicate components doing the same thing? One-off UI elements that should be centralized into reusable components? Base components not using the centralized styles?

5. **Undocumented changes** — Significant code changes in recent commits that aren't reflected in any doc.

6. **Archive update** — Check the commits reviewed against `.docs/archive/archive.md`. If there's meaningful work done (features built, bugs fixed, refactors) that isn't in the archive, propose adding it. This keeps a rough log of what was done even when the user didn't go through the backlog.

**Output:**
- List each drift item with: what the doc says vs. what the code does
- For each item, propose the specific update needed:
  - **Doc updates** when the code is right and the doc is outdated (most common)
  - **Code suggestions** only for style centralization issues (hardcoded values that should use tokens, duplicate components that should be consolidated)
- Ask the user which updates to apply

**RULES:**
- For direction, stack, and undocumented changes: the code is always right. Docs adapt to code.
- For design and component drift: suggest code fixes too, since scattered styles and duplicate components are bugs, not intentional divergence.
- Only flag meaningful drift, not nitpicks
- If everything is in sync, say so and move on — don't invent problems

**Logging:** When this command completes successfully, append a dated entry to `.docs/archive/archive.md`: `- YYYY-MM-DD ran /sync — [brief description of drift found or "all in sync"]`. Create the file if it doesn't exist.
