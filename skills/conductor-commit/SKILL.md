---
name: conductor-commit
description: One-shot ship for a Conductor workspace — generate a commit message, then stage, commit, push, open a PR against main, and auto-merge it. Use only when the user explicitly asks to ship/commit-and-merge a Conductor workspace or runs /conductor-commit.
---

You are shipping the current Conductor workspace in one shot: generate a commit message (the same way `/commit` does), then **actually run** the full stage → commit → push → PR → merge flow using that message. Unlike `/commit`, this skill *does* execute git and `gh`.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below (e.g. a different base branch, or a message they dictate).

### 1. Generate the commit message

Produce the message exactly as the `/commit` skill would:

- Rely first on the **conversation history** — if the changes were made earlier in this chat, you already know what and why.
- Otherwise inspect the working tree: `git status`, `git diff`, `git diff --staged`.
- Consult `.docs/backlog.md` if it clarifies intent.

Format — a `<type>: ...` title line, a blank line, then concrete bullets:

```
<type>: changed this, added that, removed this

- specific bullet about one change
- specific bullet about another change
```

Pick the `<type>` (`feat`, `fix`, `docs`, `refactor`, `chore`, `style`, `test`) that matches the dominant change. No footers, Co-Authored-By lines, emoji, or marketing language.

If there is nothing to commit (`git status --porcelain` is empty), stop and tell the user — don't create an empty commit or PR.

### 2. Confirm before shipping

This flow pushes and **auto-merges** into `main` — it's hard to reverse. Show the user the message and the base branch you'll target, and get a quick confirmation before running step 3, unless they already told you to proceed without asking (e.g. included "no confirm" or ran it with that intent).

### 3. Run the flow

Write the full message to a temp file so multi-line bodies survive shelling out, then run the flow. `TITLE` is the first line; the whole message is the PR body and commit message:

```bash
MSG_FILE="$(mktemp)"
cat > "$MSG_FILE" <<'EOF'
<the generated commit message goes here>
EOF

TITLE="$(head -n 1 "$MSG_FILE")"
BRANCH="$(git branch --show-current)"

git add -A && \
git commit -F "$MSG_FILE" && \
git push -u origin HEAD && \
PR_URL=$(gh pr create --base main --head "$BRANCH" --title "$TITLE" --body-file "$MSG_FILE") && \
gh pr merge "$PR_URL" --merge && \
rm -f "$MSG_FILE"
```

Notes:
- Default base branch is `main`; honor any override the user gave.
- If a PR already exists for the branch, `gh pr create` will fail — fall back to pushing and running `gh pr merge "$BRANCH" --merge` on the existing PR.
- If any step fails (push rejected, merge blocked by checks/reviews, etc.), stop and report the exact error. Don't retry blindly or force anything.

### 4. Report

Tell the user the outcome in one or two lines: the commit title, the PR URL, and that it was merged (or exactly where it stopped and why).
