---
name: merge
description: One-shot ship, branch-aware — generate a commit message, then commit and either open+merge a PR against main (on a feature branch) or push straight to main (when already on main). Use only when the user explicitly asks to ship/merge the current work or runs /merge.
---

You are shipping the current work in one shot: generate a commit message (the same way `/commit` does), then **actually run** the flow using that message. Unlike `/commit`, this skill *does* execute git and `gh`.

The flow branches on where you are:

- **On a feature branch** (anything other than the base branch): stage → commit → push → open a PR against the base → auto-merge it.
- **Already on the base branch** (`main`): stage → commit → push directly. **Never create a branch, never open a PR.**

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below (e.g. a different base branch, or a message they dictate).

### 1. Work out where you are

Run these first — the answer decides which flow you take:

```bash
git status --porcelain
BASE="$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@')"
BASE="${BASE:-main}"
BRANCH="$(git branch --show-current)"
echo "base=$BASE current=$BRANCH"
```

- If `git status --porcelain` is empty, stop and tell the user — don't create an empty commit or PR.
- If `BRANCH` is empty you're in detached HEAD. Stop and report; don't guess a branch.
- If the user named a base branch in the invocation, that wins over the detected `BASE`.
- If the detected base looks wrong for the repo (e.g. the repo actually uses `master`), trust the git output over the default.

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

### 3. Ship without asking

This skill is a one-shot ship: running it **is** the confirmation. Do not ask the user to confirm — invoking `/merge` already means "commit and get this into `main`". If the user only wanted the message, they would have run `/commit`. Proceed straight to step 4 with the generated message. (You may briefly state the message, the base branch, and which flow you're taking as you go, but do not pause for approval.)

The only reasons to stop before shipping are hard blockers, not confirmation: nothing to commit, detached HEAD, or an explicit override in the invocation that you must honor.

### 4. Run the flow

Write the full message to a temp file so multi-line bodies survive shelling out. `TITLE` is the first line; the whole message is the PR body and commit message:

```bash
MSG_FILE="$(mktemp)"
cat > "$MSG_FILE" <<'EOF'
<the generated commit message goes here>
EOF

TITLE="$(head -n 1 "$MSG_FILE")"
```

**Case A — on a feature branch (`BRANCH` != `BASE`):**

```bash
git add -A && \
git commit -F "$MSG_FILE" && \
git push -u origin HEAD && \
PR_URL=$(gh pr create --base "$BASE" --head "$BRANCH" --title "$TITLE" --body-file "$MSG_FILE") && \
gh pr merge "$PR_URL" --merge && \
rm -f "$MSG_FILE"
```

**Case B — already on the base branch (`BRANCH` == `BASE`):**

No branch, no PR — commit and push straight up:

```bash
git add -A && \
git commit -F "$MSG_FILE" && \
git push origin HEAD && \
rm -f "$MSG_FILE"
```

Notes:
- In Case B, if the push is rejected as non-fast-forward (the remote moved), run `git pull --rebase` once and push again. If the rebase hits conflicts, stop and report them — don't resolve them silently and never force-push.
- In Case B, if the push is rejected because the branch is protected, stop and tell the user: `main` requires a PR here, so they should ship from a feature branch instead. Don't invent one behind their back.
- In Case A, if a PR already exists for the branch, `gh pr create` will fail — fall back to pushing and running `gh pr merge "$BRANCH" --merge` on the existing PR.
- If any other step fails (merge blocked by checks or reviews, etc.), stop and report the exact error. Don't retry blindly or force anything.

### 5. Report

Tell the user the outcome in one or two lines:

- Case A: the commit title, the PR URL, and that it was merged.
- Case B: the commit title and that it was pushed straight to `main` (no PR).

Or exactly where it stopped and why.
