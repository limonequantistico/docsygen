You are picking up the next task from the user's backlog.

**Custom instructions from user:** $ARGUMENTS

**Read:**

- `.docs/seed.md` — project context before you implement (vision, scope, non-goals)
- `.docs/backlog.md` — take the first item from the top of the list
- The relevant project files needed to complete the task — always check the actual codebase, not just the docs

**Your task:**

### 1. Confirm

If the top backlog item is clear enough to implement safely, start working. If anything is ambiguous (scope, behavior, acceptance criteria), ask the user **once** with a focused batch of questions — do not guess.

### 2. Work

Complete the task. Follow all project rules from CLAUDE.md (use the tech stack, design system, centralized styles, etc.). If the task is vague, clarify before guessing.

### 3. Verify

When done, show the user what was done and ask if they're satisfied. If yes, move the item from the backlog to `.docs/changelog.md` per `.docs/changelog-spec.md` as `- YYYY-MM-DD HH:mm [x] item description`.

**RULES:**

- One item at a time. Never pick up multiple tasks.
- If the backlog is empty, tell the user and suggest `/resume` for a fresh assessment.
- If the task requires a specific docsygen command (e.g., it says "update design system"), suggest that command instead of doing it yourself.
- The user controls priority through the order of the list — always pick the first item unless they say otherwise.
