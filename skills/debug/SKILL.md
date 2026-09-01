---
name: debug
description: Diagnose a specific reported bug from runtime evidence rather than guesswork — competing hypotheses, instrumentation, a reproduction, a root-cause fix, then cleanup. Use only when the user explicitly asks to debug a broken behaviour, or runs /debug.
---

You are diagnosing **one specific broken behaviour** the user can point at — not sweeping for bugs, not reviewing a diff.

Debugging by reading code is guessing. The agent that reads a file, spots a plausible cause, edits it, and asks "is it fixed now?" is right often enough to feel productive and wrong often enough to burn an afternoon. What breaks that loop is **evidence**: hold more than one explanation at once, add instrumentation that tells them apart, get the bug reproduced, and let the runtime output pick the winner. A fix you can't trace to an observation is a guess wearing a confident voice.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

**Scope note — what belongs to other skills.** This skill owns a *known symptom you can point at*. It does **not** own:

- **Latent bugs found by sweeping the codebase** → `/deep-audit`
- **The uncommitted diff, reviewed before commit** → `/review`
- **The project's permanent logging contract** → `/logs`
- **Structure, modularity, duplication** → `/clean`
- **Missing test coverage** → `/test`

If you trip over something in one of those, name it in one line and point at the skill that owns it. Fixing the bug is the job; the tour of everything else wrong nearby is not.

---

## Step 0 — Pin the symptom

Three things are needed before investigating:

- **Reproduction** — the exact steps, input, or conditions that produce it
- **Expected** — what should happen
- **Actual** — what happens instead, verbatim where there's an error or stack trace

A fourth is worth having when it's cheap: **did it ever work?** If yes, `git log` and `git bisect` over the suspect path are usually faster than any amount of reading.

Take whatever the user's report already contains. Ask, in **one** `AskUserQuestion` batch, only for what is both missing *and* not discoverable by reading the repo — never ask for something you could find yourself. If the report already carries all three, ask nothing and start work.

---

## Step 1 — Trace the real path before hypothesizing

Follow the actual execution path from entry point to symptom. Read the code that runs, not the code that looks related.

- Where a `.codegraph/` directory exists, `codegraph explore "<symbol or question>"` is the right tool here — the dynamic-dispatch hops it follows are exactly where a grep-based trace loses the thread.
- Read `.docs/logging.md` if it exists, so anything you add in Step 3 matches the project's levels and format instead of inventing a second style.
- Where the bug depends on how a library actually behaves, check with Context7's MCP. A hypothesis built on a misremembered API wastes a whole instrument-and-reproduce round.

---

## Step 2 — Form competing hypotheses

**Do not edit product code in this step.** This is the gate that separates debugging from guessing.

State **at least two** candidate explanations, ideally three or four. Each one needs:

- A falsifiable claim — *"the session token is expired before the retry, so the second call 401s"*
- The observation that would **kill** it — what you'd have to see for it to be wrong

Then rank them by likelihood × cheapness to test, and say which one you're testing first.

If you can only produce one hypothesis, you haven't read enough yet — go back to Step 1. A single hypothesis is how a confident wrong fix gets made.

---

## Step 3 — Instrument to discriminate

Add logging that **tells the hypotheses apart**. Logging that narrates the happy path ("entering handler", "calling API") tells you nothing you didn't already know — each line you add should be one whose value distinguishes one explanation from another.

- Mark every added line with a fixed sentinel so cleanup is mechanical and provable — `DEBUG-<slug>` in a trailing comment, using one slug for the whole session.
- Match the project's existing logging style and levels.
- Log the values that decide it: the actual state, the actual input, the actual branch taken.
- Report exactly what you added and where, so the user can see the blast radius before running anything.

---

## Step 4 — Get the reproduction

Drive it yourself wherever you can — a failing test, a CLI invocation, a script, or the launch path recorded in `.docs/preview.md` if that file exists. Reaching the running app yourself is always better than asking.

Hand off to the user only when reproducing genuinely needs a human. When you do, say precisely:

- What to do, step by step
- What to bring back — the log lines, the console output, the screenshot

Then stop and wait. Don't fill the silence by editing code on spec.

---

## Step 5 — Read the evidence and name the root cause

Say which hypothesis the output **supports** and which ones it **killed**, citing the actual values you saw. Then state the root cause in one sentence.

If nothing survived, say so plainly and return to Step 2 carrying what you ruled out — the eliminated explanations are real progress and must not be re-tested.

**Hard cap:** after **three** full instrument → reproduce rounds without a root cause, stop. Report what has been eliminated and what you'd try next, and let the user decide whether to keep going. A fourth round on the same footing is the runaway loop `CLAUDE.md` warns about.

---

## Step 6 — Fix the cause, not the symptom

The smallest change that addresses the cause you just named. Follow the project's stack, design system, and nearby conventions — the fix should look like the same team wrote it.

If the only fix available is a workaround — the real cause sits in a dependency, or behind a change too large for this session — say so and label it a workaround. A suppressed symptom quietly recorded as a fix is worse than an open bug.

---

## Step 7 — Verify by reproducing again

Run the Step 0 reproduction one more time, with the fix in and the instrumentation still in place. The symptom must be gone, and the instrumentation should now show the corrected values.

Also exercise the immediate neighbours — the path either side of what you touched. Then say what you checked and what you didn't. A fix that was written but never run is "written, not run".

---

## Step 8 — Strip the instrumentation

Remove every line you added in Step 3, then **prove** none survived by grepping the sentinel across the repo and showing the empty result.

**Then re-check the stripped tree.** Removing instrumentation is itself an edit, and it breaks things on its own: an import added only for logging becomes an unused import the linter rejects, a value hoisted purely so it could be logged becomes an unused variable, a deleted line takes a needed side effect with it. Re-run what Step 7 ran — build, typecheck, or lint at minimum, and the Step 0 reproduction wherever you can drive it yourself — and say what you re-checked. The tree that ships is the one that has to be verified; until this passes, the last edit was written but never run.

Present the final diff. It should be small — the instrumentation is scaffolding, and only the fix ships.

If some of what you added genuinely earned a permanent place, propose it separately, as its own decision, and point at `/logs` for where that contract lives. Don't smuggle it through as part of the fix.

---

## Rules

- Obey **CLAUDE.md** and workspace rules.
- **This skill runs only when the user invokes it.** Never enter it off your own judgement, and never fold its steps into an ordinary bug fix to get the same effect without being asked.
- No product code is modified between Steps 0 and 3 except instrumentation.
- A root cause you can't state in one sentence isn't a root cause — it's a suspicion. Say which it is.
- A disproven hypothesis stays disproven. Never re-test one, including after a context reset.
- Label each claim **measured** (you saw it at runtime) or **inferred** (you read it in source). An inferred root cause is a hypothesis; don't dress it up as an observation.
- Never add a logging framework, test framework, or preview setup to make this work — that's `/logs`, `/test`, and `/ux-review`, and each needs approval first.
- Don't broaden into refactoring. The bug is the job.
- Leave no sentinel-marked line behind. Shipping debug output is a worse outcome than the bug.

**Logging:** On completion, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /debug — [symptom, root cause, fix]`. Record the root cause, not just that a bug was fixed — that sentence is the part worth having in six months.
