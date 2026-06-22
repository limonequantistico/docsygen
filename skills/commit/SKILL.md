---
name: commit
description: Produce a copyable commit message for the latest changes (does not run git commit). Use only when the user explicitly asks for a commit message or runs /commit.
---

You are producing a **copyable commit message** for the user's latest changes. Do not run `git commit` — just output the message in a single fenced code block so the user can copy it.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

### 1. Figure out what changed

- First, rely on the **conversation history**. If you (or the user) made the changes earlier in this chat, you already know what was done and why — use that as the primary source.
- If the chat history doesn't cover the changes, inspect the working tree to understand the latest uncommitted changes:
  - `git status` for the file list
  - `git diff` (and `git diff --staged`) for the actual edits
- Consult `.docs/backlog.md` if it helps explain the intent behind the changes (e.g. a backlog item that was just completed).
- If the scope is still unclear after all of the above, ask the user before writing the message.

### 2. Write the message

Format:

```
<type>: changed this, added that, edited this, removed this

- more specific bullet about one change
- more specific bullet about another change
- ...
```

- **Title line**: a `<type>: ...` summary (e.g. `feat`, `fix`, `docs`, `refactor`, `chore`, `style`, `test`), followed by a short comma-separated list of the main changes using plain verbs (`added`, `changed`, `removed`, `edited`, `fixed`). Keep it under ~100 characters when reasonable.
- **Body**: a blank line, then bullet points going a bit deeper — one bullet per meaningful change. Keep each bullet short and concrete. Don't pad with obvious filler.
- Pick the `<type>` that best matches the dominant change. If truly mixed, `chore` or `refactor` are fine.
- Describe the "what" plainly. Only include a "why" if it's non-obvious and useful.
- Do **not** add footers, Co-Authored-By lines, emoji, or marketing language.

### 3. Output

- Print the commit message inside a single fenced code block so it's easy to copy.
- Do not run `git commit`, do not stage files, do not modify the repo.
- After the code block, optionally add one short line if something is worth flagging (e.g. "there are also unstaged changes in X you may want to include").
