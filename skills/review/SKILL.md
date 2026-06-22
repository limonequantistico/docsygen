---
name: review
description: Read-only review of uncommitted changes for bugs before commit. Use only when the user explicitly asks to review changes or runs /review.
---

You are reviewing the user's recent work for problems before it gets committed or shipped.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

---

## Step 1 — Identify what changed

Run `git diff` and `git diff --cached` to see all uncommitted changes (staged and unstaged). Also check `git status` for new untracked files and read those too.

These are the files you're reviewing. Read each one in full — don't rely only on the diff, because bugs often come from how the change interacts with surrounding code.

---

## Step 2 — Review

Go through each changed file and look for:

- **Bugs** — logic errors, off-by-one, wrong variable, missing early returns, broken control flow, race conditions
- **Runtime failures** — uncaught exceptions, null/undefined access, missing imports, wrong types, broken references to renamed things
- **Regressions** — does this change break something that was working? Check callers, imports, and dependents of anything that was modified or renamed
- **Security issues** — injection, exposed secrets, missing auth checks, unsafe input handling
- **State & data problems** — stale state, missing cleanup, wrong data flow, inconsistent updates
- **Copy-paste mistakes** — duplicated code that wasn't updated, leftover debug code, TODO comments that should have been resolved

Don't nitpick style, formatting, naming, or missing comments. Focus only on things that would cause real problems.

---

## Step 3 — Report

If you find issues, present them as a clear list:

- **File** → what's wrong → why it matters → suggested fix

Group by severity: breaking issues first, then potential bugs, then minor concerns.

If everything looks clean, say so briefly — don't invent problems.

---

## Rules

- Don't modify any files. This is a read-only review.
- If there are no uncommitted changes, tell the user and stop.
- Be direct. If something is fine, don't pad the review with praise.
- Use Context7's MCP to make sure the code is well written and follows official documentation's standards.
