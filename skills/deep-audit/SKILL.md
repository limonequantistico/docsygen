---
name: deep-audit
description: Deep whole-codebase audit for latent bugs, security holes, broken failure paths, and architectural risk — report first, fix only on approval. Use only when the user explicitly asks for a deep audit of the codebase, or runs /deep-audit.
---

You are auditing the **whole codebase** — not a diff — for **correctness and safety**: latent bugs, security holes, broken failure paths, and architectural risk that has already spread.

This is the deep pass. There is no time limit and no page limit on how carefully you read. What is bounded is the *shape* of the work, not its depth: you sweep a fixed set of areas in a fixed order, visit each once, and every finding must survive a verification pass before it reaches the user.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

**Scope note — what belongs to other skills.** This audit owns latent bugs, security, error handling, concurrency, data integrity, and architectural risk. It does **not** re-audit:

- **Structure, modularity, separation of concerns, duplication** → `/clean`
- **Secrets, env vars, production config** → `/env`
- **Bottlenecks, baselines, tracing** → `/performance`
- **Test coverage and strategy** → `/test`
- **Docs that no longer match the code** → `/drift`
- **A specific bug the user can already point at and reproduce** → `/debug`

If you trip over something in one of those, name it in one line and point at the skill that owns it. Don't design the fix here — that's how a deep audit turns into an everything audit nobody reads.

---

## Step 0 — Calibrate (one batch, skippable)

Ask up to four questions with `AskUserQuestion`, and only where the answer would actually change the sweep. Say up front that skipping is fine — you'll audit the whole repo on sensible defaults.

Worth asking:

- **Blast radius** — what does a bug here cost? A hobby project, real users' data, or money and safety? This sets the severity bar for everything that follows.
- **Known-shaky areas** — is there code the user already doesn't trust, or that was written in a hurry?
- **Exclusions** — is anything knowingly unfinished, vendored, generated, or scheduled for deletion? Auditing a half-built feature produces noise, not findings.
- **How it's exercised today** — real traffic, a handful of manual runs, or never actually run? Code that has never executed hides a different class of bug than code that has run for a year.

One batch. Don't drip-feed questions across turns, and don't ask anything you can answer by reading the repo.

---

## Step 1 — Load context (silently)

Read the project's canonical sources before judging anything. Do not narrate this step.

1. `.docs/seed.md` — what this product is and what must not break
2. `.docs/tech-stack.md` — the stack, so findings are idiomatic rather than generic
3. `CONTEXT.md` and `.docs/adr/` — the domain vocabulary and the decisions already made deliberately
4. `.docs/audits/` — earlier reports, if any. Findings already accepted, rejected, or deferred should not come back as if new
5. Enough code to know the project's conventions before calling anything wrong

If a doc conflicts with the code, **trust the code** — and note the contradiction in one line, pointing at `/drift`.

A choice recorded in an ADR is a decision, not a defect. You may still flag it if it has since caused a real bug, but say that it was deliberate.

---

## Step 2 — Map the territory

Do not start reading line by line. Build the map first, so the sweep in Step 3 follows the real shape of the system instead of the directory listing:

- **Entry points** — routes, handlers, CLI commands, event and queue consumers, scheduled jobs, UI actions that mutate something
- **Trust boundaries** — where unvalidated input crosses into trusted code: network, user input, files, third-party responses, IPC
- **Persistence** — schemas, migrations, writes, transactions, anything holding invariants
- **Outbound calls** — external APIs, and what happens when each one is slow, wrong, or down
- **Concurrency** — async work, background jobs, shared mutable state, caches
- **Auth** — where identity is established, and every path that assumes it already was

**If the repo has a `.codegraph/` directory**, build this map with `codegraph explore` rather than grep — it returns the symbols' source plus the call paths between them, including dynamic-dispatch hops grep can't follow, which is exactly what a trust-boundary map needs. Use `codegraph impact <symbol>` before claiming a change is contained. Skip this entirely if there is no index.

State the scope you settled on in one line before sweeping, so the user can stop you if you aimed at the wrong thing.

---

## Step 3 — Sweep

Work through these areas **in this order, each exactly once.** Depth within an area is unbounded — go as deep as the code warrants. But when an area is done, it is done: no revisiting, no re-reading a file you've already worked through. That fixed shape is what keeps an unbounded audit terminating.

1. **Entry points and input handling** — unvalidated input, injection (SQL, command, template, path traversal), deserialization of untrusted data, missing bounds and type checks, mass assignment
2. **Data flow and state** — values that can be null/undefined at a point that assumes otherwise, stale or duplicated state, updates that can interleave wrongly, cache invalidation that never happens
3. **Trust boundaries and authorization** — endpoints missing an authz check, checks that verify authentication but not ownership, IDs trusted straight from the client, privilege that leaks across a boundary
4. **Error and failure paths** — swallowed exceptions, `catch` blocks that log and continue into a broken state, partial writes with no rollback, retries without idempotency, timeouts that don't exist
5. **Concurrency and lifecycle** — races, missing locks, work started and never awaited, listeners and subscriptions never torn down, ordering assumed but not enforced
6. **Resource handling** — unbounded growth, connections and handles never released, unpaginated queries over data that grows, work proportional to something the user controls
7. **Architectural risk** — the findings that aren't a single line: a boundary the code keeps violating, an invariant that's wrong and has spread to a dozen call sites, two subsystems that disagree about who owns a piece of data

Explicitly **not** in scope: style, formatting, naming, comment density, or preference. If it can't produce a wrong outcome, it isn't a finding here.

---

## Step 4 — Verify (do not skip this)

You now have a list of candidates. Most reports are ruined at exactly this point, by shipping suspicion as if it were evidence.

Go back to the code behind **every** candidate and re-read it. Keep the finding only if you can state a **concrete failure scenario**: specific inputs or specific state, leading to a specific wrong outcome — a crash, wrong data, a leak, an unauthorized action.

- If you can't produce that scenario, **drop it.** Don't list it as "possible", don't hedge it into the report, don't demote it to MINOR. Dropping it silently is the correct outcome.
- If a guard elsewhere already prevents it, drop it. Check before assuming there isn't one.
- If it's deliberate — an ADR, a comment explaining the trade-off, an obvious constraint — drop it or say plainly that it was a choice.

Tag what survives:

- **CONFIRMED** — you traced the path end to end in the code
- **PLAUSIBLE** — the defect is real but depends on a path you couldn't fully verify (dynamic dispatch, external behavior, config you can't see). Say what you couldn't check

**Finding nothing is a real and expected outcome.** A clean sweep reported as clean is worth more than six invented findings, and on a well-maintained codebase it's the likely result. Never pad a report to look thorough.

---

## Step 5 — Report

Two readers, two versions.

### The scan version — in the conversation

Counts, a one-sentence health verdict, one bullet per finding, one-line bottom line:

```md
**Deep audit** — N findings (X confirmed, Y plausible) across <scope>.

Overall: <one-sentence health verdict>.

- **[1] CRITICAL** · CONFIRMED · `path/File.ext:120` — one-line gist
- **[2] MODERATE** · PLAUSIBLE · `path/Other.ext:44` — one-line gist

**Bottom line:** what must be fixed vs. what can wait. Full report: `.docs/audits/<file>`.
```

### The full report — written to a file

Write it to `.docs/audits/YYYY-MM-DD-<model>-<effort>.md` (create `.docs/audits/` if it doesn't exist). Start with a **run header**, which is what makes two audits comparable later:

```md
# Deep audit — YYYY-MM-DD

- **Model:** <model name and version>
- **Effort:** <reasoning/thinking effort level for this run>
- **Commit:** <git rev-parse --short HEAD>
- **Scope:** <what was swept, and what was excluded and why>
- **Calibration:** <the Step 0 answers, or "defaults — not asked">
```

**Read the model and effort out of the environment — don't ask first.** Both agents expose them:

- **Claude Code** — `CLAUDE_EFFORT` in the environment; `effortLevel` and `model` in `~/.claude/settings.json`. `AI_AGENT` carries the agent and its version.
- **Codex** — `model` and `model_reasoning_effort` in `~/.codex/config.toml`.

Ask the user only when none of those resolve. Never guess it and never leave it blank: a report that doesn't say how hard the model was thinking can't be compared against another one.

Then the findings, ordered by severity — `CRITICAL` (data loss, security, corruption), `MAJOR` (wrong behavior on a real path), `MINOR` (a genuine defect on an unlikely path):

```md
## [1] CRITICAL · CONFIRMED · path/to/File.ext:120

**What:** what's wrong
**Why:** what it costs when it happens
**Failure scenario:** these inputs / this state → this wrong outcome
**Fix:** the concrete change
```

Close with a **Bottom line** section, and a **Not audited** section naming what you deliberately left to `/clean`, `/env`, `/performance`, `/test`, or `/drift`.

**If nothing survived Step 4:** say so in the conversation in one sentence, and still write the file — header, an empty findings section, and the scope you covered. That empty report is the baseline every later run is measured against, so it's the most valuable one to have on disk.

---

## Step 6 — Fix (on approval only)

Present the report, then **ask which findings to fix** — all, some, or none. Never start fixing before the user answers; "none" is a legitimate answer to a good audit.

For approved items:

- One at a time, smallest change that closes the finding. No opportunistic refactoring alongside it — that's `/clean`.
- Follow the project's stack, design system, and nearby conventions. The fix should look like the same team wrote it.
- **Verify each fix.** Build, typecheck, or lint; run the tests that cover the area if there are any; exercise the path if you can. Then say what you checked and what you didn't — a fix that was written but never run is "written, not run".
- Record the outcome against each finding in the report file: **fixed** (and how), **skipped** (and why), or **no change needed**.

If a fix on a critical path has no test covering it, say so once and offer `/test`. Don't write the test unprompted.

---

## Step 7 — Route what's left

For findings not fixed in this session, offer **once** to slice them into work with `/to-issues` — `.docs/backlog.md` or GitHub Issues, whichever the user picks. Offer it; don't run it unprompted, and don't repeat the offer.

---

## Rules

- Obey **CLAUDE.md** and workspace rules.
- Steps 0–5 are **read-only**. Nothing is modified before the user approves findings in Step 6.
- A finding without a concrete failure scenario is not a finding. Drop it.
- Don't recommend new libraries or tools to fix findings; flag once if something would genuinely help, then move on.
- Don't re-raise findings a previous report in `.docs/audits/` already recorded as rejected, unless the code has changed since.
- Use Context7's MCP where a finding depends on how a library actually behaves — an audit built on a misremembered API produces false positives.
- If the sweep is ballooning far past what the codebase's size warrants, stop and check in rather than continuing. Deep is the point; runaway is not.

**Logging:** On completion, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /deep-audit — [scope swept, findings, what was fixed]`.
