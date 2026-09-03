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

**Scan the file list before staging.** This skill stages everything, so glance at what "everything" is. Speed is the point — say nothing and keep going unless something genuinely doesn't belong:

- **OS / editor junk** — `.DS_Store`, `Thumbs.db`, `.idea/`, `*.swp`. Don't commit these. Add them to `.gitignore` instead, mention it in one line, and continue.
- **Possible secrets** — `.env`, `.env.local`, `*.pem`, `*.key`, `credentials*`, `*.p12`. **Stop and ask.** Never commit one on your own initiative — and here it would land in `main`.
- **Clearly unrelated work** — untracked scratch files, or edits in a part of the repo the current work never touched. Name them in one line and ask whether to include them, since the commit message and PR won't describe them.

Anything else, just stage it. Don't narrate a clean file list, and don't turn this into an approval step — `/merge` is meant to be one shot.

### 2. Generate the commit message

Read `skills/commit/SKILL.md` and follow its steps 1–3 — figuring out what changed, checking `.docs/commit-convention.md` (detecting or asking and persisting it if missing), and writing the message — exactly as `/commit` would. Stop before its step 4 (`Output`): that step is `/commit`-specific ("print it, don't touch git") and doesn't apply here. Keep the message you produced; use it for staging and committing below.

The convention check is the one narrow exception to "ship without asking" in this skill — same category as the secrets check in Step 1. It only asks the user directly when `.docs/commit-convention.md` doesn't exist yet and recent history is genuinely ambiguous; once answered it's persisted to that file and never asks again.

### 3. Ship without asking

This skill is a one-shot ship: running it **is** the confirmation. Do not ask the user to confirm — invoking `/merge` already means "commit and get this into `main`". If the user only wanted the message, they would have run `/commit`. Proceed straight to the remaining steps with the generated message. (You may briefly state the message, the base branch, and which flow you're taking as you go, but do not pause for approval.)

The only reasons to stop before shipping are hard blockers, not confirmation: nothing to commit, detached HEAD, or an explicit override in the invocation that you must honor.

### 4. Obey the project's own pre-ship rules

If `CLAUDE.md` (or equivalent workspace rules) defines steps that must happen before shipping — a validation script, a version bump, a changelog entry — do them now, before anything is committed. If one fails, stop and report; don't ship a knowingly broken commit. If the project defines no such steps, skip straight to the next section.

### 5. Run the flow

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

### 6. Report

Tell the user the outcome in one or two lines:

- Case A: the commit title, the PR URL, and that it was merged.
- Case B: the commit title and that it was pushed straight to `main` (no PR).

Or exactly where it stopped and why.
