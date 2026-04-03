You are helping the user resume work on this project after a few days away.

**Custom instructions from user:** $ARGUMENTS

**Read (silently, no questions asked):**

- Last ~5 git commits
- `.docs/backlog.md`
- Git status for uncommitted work

**Output:**

1. **Last time** — What happened recently: what changed, what direction things were moving in. Enough to jog the user's memory, not a changelog.

2. **Next up** — 1-2 concrete next steps based on the backlog or the natural continuation of recent work. Be specific enough to be actionable ("review the full command flow end-to-end for gaps" not "continue working"). If a step maps to a docsygen command, mention it.

3. **Heads up** — Only if something needs attention: something that looks off or not updated. Skip this section entirely if everything looks clean.

**RULES:**

- The user knows their own project. Don't explain what the project is.
- Don't ask questions before scanning — just read and report.
- Aim for a quick but useful read — not a wall of text, not a telegram either.
- If the project is brand new and there's nothing to resume, just say so and point to `/help`.
