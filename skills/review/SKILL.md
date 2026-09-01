---
name: review
description: Read-only review of uncommitted changes for bugs before commit, OR triage of another agent's review of your work. Use only when the user explicitly asks to review changes or runs /review.
---

You are vetting the user's recent work before it gets committed or shipped.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

---

## Step 0 — Pick the mode

Look at what the user passed in alongside the command:

- **No external review attached → First-pass review (Mode A).** You do the review yourself. Go to Mode A.
- **The user pasted in findings/a review from another agent → Triage mode (Mode B).** Another agent reviewed work that *you* (the main agent) produced. Your job is to judge those findings and act on the ones that hold up. Go to Mode B.

If you're unsure which mode applies (e.g. it's ambiguous whether the pasted text is a review or just context), ask the user before proceeding.

---

## Mode A — First-pass review (read-only)

### A1 — Identify what changed

Run `git diff` and `git diff --cached` to see all uncommitted changes (staged and unstaged). Also check `git status` for new untracked files and read those too.

These are the files you're reviewing. Read each one in full — don't rely only on the diff, because bugs often come from how the change interacts with surrounding code.

### A2 — Review

Go through each changed file and look for:

- **Bugs** — logic errors, off-by-one, wrong variable, missing early returns, broken control flow, race conditions
- **Runtime failures** — uncaught exceptions, null/undefined access, missing imports, wrong types, broken references to renamed things
- **Regressions** — does this change break something that was working? Check callers, imports, and dependents of anything that was modified or renamed
- **Security issues** — injection, exposed secrets, missing auth checks, unsafe input handling
- **State & data problems** — stale state, missing cleanup, wrong data flow, inconsistent updates
- **Copy-paste mistakes** — duplicated code that wasn't updated, leftover debug code, TODO comments that should have been resolved

**If the repo has a `.codegraph/` directory**, run `codegraph impact <symbol>` on every function, method, or type the diff modified or renamed before you judge regressions — it lists the real dependents and the call paths reaching them, including hops grep won't surface. Judging a changed symbol without knowing who calls it is how a "safe" rename ships broken. Skip this if there is no index.

Don't nitpick style, formatting, naming, or missing comments. Focus only on things that would cause real problems.

### A3 — Report

The report has **two readers with different needs**, so produce **two versions, in this order**:

1. **A short scan version for the user** — rendered markdown (real headers/bold), readable at a glance. Not copyable; it doesn't need to be.
2. **A thorough copyable version for the agent** — one fenced code block with full detail, ready to paste into the original agent for triage (Mode B).

Keep finding numbers and severity tags identical across both versions so they line up.

**Version 1 — Scan (for the user), as normal markdown:**

A header line with the counts, a one-sentence health check, then one bullet per finding (gist inline), then a one-line bottom line. No `What/Why/Fix` breakdown here; that's what Version 2 is for.

```md
**Review — Mode A** (read-only) — N findings, X blocking.

Overall: <one-sentence health check>.

- **[1] BREAKING** · `File.ext:line` — one-line gist of the problem
- **[2] MINOR** · `File.ext:line` — one-line gist

**Bottom line:** what must change vs. what's polish.
```

**Version 2 — Full (for the agent), inside one fenced code block:**

Put the **entire** detailed review inside a single block so it pastes as one unit — don't leave any of it outside; the triaging agent needs the summary and bottom line too. Keep it **minimal**: plain labels, no decorative rules or boxes (they're noise to an agent). Hard-wrap nothing artificially; let lines run.

```
REVIEW · Mode A (read-only first pass)

SUMMARY
2–4 sentences: what's solid (give due credit — it's context the
triaging agent needs), then how many issues you're flagging. Not a wall.

FINDINGS (N)

[1] BREAKING · path/to/File.ext:line
What: what's wrong
Why: why it matters / what it breaks
Fix: the suggested change

[2] MINOR · path/to/File.ext:line
What: ...
Why: ...
Fix: ...

BOTTOM LINE
Which findings actually matter vs. polish, plus any recommendation.
End by confirming the pass was read-only — nothing was modified.
```

Rules:

- **Number** the findings and **order by severity**: breaking first, then bugs, then minor. Tag each with `BREAKING`, `BUG`, or `MINOR`.
- In Version 2, keep `What / Why / Fix` on their own lines — don't collapse a finding onto one dense line, and don't pad it back out with separators or ASCII art.
- Keep the SUMMARY tight in both versions — a couple of sentences, not a paragraph-long wall.
- If everything looks clean, say so in Version 1 in a sentence and skip Version 2 entirely — no empty block, no invented problems.

**Mode A is read-only — don't modify any files.**

---

## Mode B — Triage another agent's review

The user has handed you a review that a *different* agent wrote about the changes you made. The point of this is to widen the net and catch mistakes a single agent would miss — so take it seriously. But the other agent reviewed in isolation: it didn't have your full context, the project's direction, or the reasoning behind your choices, so some of its findings could be wrong, out of scope, or false positives. Your job is to separate the signal from the noise and act on the signal.

### B1 — Ground yourself in the actual code

Don't evaluate the findings from memory. Re-establish the real state first:

- Run `git diff`, `git diff --cached`, and `git status`, and read the changed files (and relevant surrounding code) in full.
- Parse the external review into a discrete list of findings. Number them so you can refer back.

### B2 — Judge each finding on its merits

For **each** finding, verify it against the real code and decide:

- **Accept** — it's correct and worth fixing. The other agent caught something real.
- **Reject** — it's wrong, a false positive, based on a misreading, or already handled elsewhere. State the specific reason.
- **Defer** — it's a valid point but out of scope for this change, a larger refactor, or a judgment call that's the user's to make. Flag it; don't silently implement.

Be honest in both directions. Don't accept a finding just because another agent raised it (no deferring to authority), and don't reject findings defensively just because they critique your work. Verify, then decide.

If a finding is plausible but you genuinely can't tell whether it's right without a decision the user should make, surface it rather than guessing.

### B3 — Implement the accepted findings

Apply fixes for everything you accepted. Keep them tight and scoped to the finding — don't let triage turn into an unrelated refactor. Follow the project's tech stack and design system as usual.

### B4 — Report the verdict

Give the user a clear ledger:

- **Accepted & fixed** — finding → what you changed
- **Rejected** — finding → why it doesn't hold up
- **Deferred** — finding → why it's out of scope / needs your call

Be direct. The user wants to know what the second pass actually caught and what it got wrong, not a polite summary.

---

## Rules

- Mode A is strictly read-only. In Mode B you may modify files, but only to implement findings you've verified and accepted.
- If there are no uncommitted changes, tell the user and stop.
- Be direct. If something is fine, don't pad the review with praise.
- Use Context7's MCP to make sure the code is well written and follows official documentation's standards.
