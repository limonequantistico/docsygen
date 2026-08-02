---
name: push
description: Commit and push the current branch in one shot — generates the commit message, then stages, commits, and pushes. Never opens a PR and never merges (use /merge for that). Use only when the user explicitly asks to commit and push, or runs /push.
---

You are committing and pushing the current work in one shot: generate a commit message (the same way `/commit` does), then **actually run** stage → commit → push. Unlike `/commit`, this skill *does* execute git.

**This skill stops at the push.** Whatever branch you're on, it stays that branch — no new branch, no PR, no merge. If the user wants the work landed in `main`, that's `/merge`.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below (e.g. a message they dictate, or a specific remote).

### 1. Check you can ship

```bash
git status --porcelain
BRANCH="$(git branch --show-current)"
echo "current=$BRANCH"
```

- If `git status --porcelain` is empty, stop and tell the user — don't create an empty commit.
- If `BRANCH` is empty you're in detached HEAD. Stop and report; don't guess a branch.

### 2. Generate the commit message

Produce the message exactly as the `/commit` skill would:

- Rely first on the **conversation history** — if the changes were made earlier in this chat, you already know what and why.
- Otherwise inspect the working tree: `git status`, `git diff`, `git diff --staged`.
- Consult `.docs/backlog.md` if it clarifies intent.

Format — a `<type>: ...` title line, a blank line, then concrete bullets:

​```
<type>: changed this, added that, removed this

- specific bullet about one change
- specific bullet about another change
​```

Pick the `<type>` (`feat`, `fix`, `docs`, `refactor`, `chore`, `style`, `test`) that matches the dominant change. No footers, Co-Authored-By lines, emoji, or marketing language.

### 3. Push without asking

Running this skill **is** the confirmation. Do not ask the user to approve the message — invoking `/push` already means "commit this and push it". If they only wanted the message, they would have run `/commit`. Proceed straight to step 4. (You may state the message as you go, but don't pause for approval.)

### 4. Run it

Write the full message to a temp file so multi-line bodies survive shelling out:

```bash
MSG_FILE="$(mktemp)"
cat > "$MSG_FILE" <<'EOF'
<the generated commit message goes here>
EOF

git add -A && \
git commit -F "$MSG_FILE" && \
git push -u origin HEAD && \
rm -f "$MSG_FILE"
```

Notes:
- If the push is rejected as non-fast-forward (the remote moved), run `git pull --rebase` once and push again. If the rebase hits conflicts, stop and report them — don't resolve them silently and never force-push.
- If the push is rejected because the branch is protected, stop and tell the user the branch requires a PR, so `/merge` from a feature branch is the way in. Don't create a branch behind their back.
- If any other step fails, stop and report the exact error. Don't retry blindly.

### 5. Report

One or two lines: the commit title and the branch it was pushed to. Say plainly that no PR was opened — if they want it merged into `main`, `/merge` is next. Or report exactly where it stopped and why.
