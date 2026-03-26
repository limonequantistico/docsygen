You are picking up the next task from the user's backlog.

**Custom instructions from user:** $ARGUMENTS

**Read:**
- `.docs/backlog.md` — take the first item from the top of the list
- `.docs/seed-document.md` — only if the task requires understanding the project's direction (e.g., building a new feature). Skip for small fixes or styling tasks. Keep in mind the seed may be outdated if `/sync` hasn't been run recently — when in doubt, trust the actual code over what the seed says.
- The relevant project files needed to complete the task — always check the actual codebase, not just the docs

**Your task:**

### 1. Confirm
Show the user the first item from the backlog and ask: "This is next on the list — should I go ahead? If you'd rather do a different one, let me know."

Do NOT start working until the user confirms.

### 2. Work
Complete the task. Follow all project rules from CLAUDE.md (use the tech stack, design system, centralized styles, etc.). If the task is vague, ask the user to clarify before guessing.

### 3. Verify
When done, show the user what was done and ask if they're satisfied. If yes, move the item from the backlog to `.docs/archive/archive.md` with today's date.

**RULES:**
- One item at a time. Never pick up multiple tasks.
- If the backlog is empty, tell the user and suggest `/resume` for a fresh assessment.
- If the task requires a specific docsygen command (e.g., it says "update design system"), suggest that command instead of doing it yourself.
- The user controls priority through the order of the list — always pick the first item unless they say otherwise.
