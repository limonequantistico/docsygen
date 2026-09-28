---
name: version
description: Cut a new app version — summarize changes since last release and write to versions.json. Runs automatically from /merge, and from /push on the base branch; otherwise use only when the user explicitly asks to cut a version or runs /version.
---

You are cutting a new app version — reviewing what changed since the last release and producing a structured version record.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

**Two modes.** The steps are the same; only who signs off differs.

- **Manual** — the user ran `/version` or asked for a cut. Show the summary and the proposed number, and let them confirm or adjust before writing.
- **Automatic** — another skill (`/merge`, `/push` on the base branch) or the post-ship rule in `CLAUDE.md` runs this as part of shipping. **Nobody confirms.** Decide, write if the bar is met, and report in one line. The user has handed this over on purpose — don't turn it back into a question. Automatic mode runs under the extra limits in **Automatic guardrails** below; when a limit bites, skip or propose instead of writing.

**Read:**

- `.docs/versions.json` — previous versions (if exists)
- `.docs/changelog.md` — running log of completed work and command runs (format: `.docs/changelog-spec.md`)
- Recent git history — commits since the last version's date (or all commits if no versions exist yet)

**Your task:**

### 1. Gather changes

- Find the date of the last version in `.docs/versions.json`. If no versions exist, treat all changelog entries and recent commits as new.
- Collect everything that happened since that date:
  - Entries from `.docs/changelog.md`
  - Meaningful commits from git history (skip merge commits, typo fixes, and other noise)
- Deduplicate — if a changelog entry and a commit describe the same thing, keep one.

### 2. Summarize

- Group changes into a short list of human-readable bullet points (max ~8 items).
- Each item should be ≤15 words, written for an end user, not a developer. Think release notes, not commit messages.
- If there's nothing meaningful since the last version, tell the user and stop.

### 3. Decide whether to cut at all

**Most check-ins should not produce a version.** Version numbers are a communication device for whoever uses the software; inflating them destroys that signal, and an agent cutting a release per merge will burn through eighty versions in a week while the product stands still.

Apply this test first: **has anything changed that a user of this software would notice?** If not, say so and stop. The following are *not* versions on their own:

- Scaffolding, project setup, folder structure, config
- Documentation, README, comments, changelog tidying
- Refactors, renames, formatting, lint fixes
- CI, build tooling, test-only changes
- Dependency bumps with no visible effect
- Work in progress toward a feature that isn't usable yet

Also don't cut if the last version was minutes ago, or if the summary would amount to a single trivial line. Batch it — wait until there's a coherent set of changes worth announcing. When in doubt, don't cut; the next run will pick everything up.

### 4. Propose version

Follow **[Semantic Versioning](https://semver.org/)** (`MAJOR.MINOR.PATCH`) — the specification the rest of the ecosystem already assumes.

The rules below are a summary, not the authority. **When a case is genuinely ambiguous, fetch <https://semver.org> and follow what it says now** — that URL always serves the current specification, so the spec can move on without this skill being rewritten. Same for <https://www.conventionalcommits.org> if a commit-type question is unclear. Don't guess from memory, and don't assume the summary here is complete.

- Start at `0.1.0`.
- **Pre-1.0 (`0.y.z`) — where most projects live for a long time.** SemVer treats major version zero as initial development, so the rules shift down one level:
  - **Minor** (`0.X.0`) — new features, visible UI changes, breaking changes, anything substantial
  - **Patch** (`0.1.X`) — fixes, copy changes, small tweaks
  - Major stays at `0` until the user explicitly decides the software is stable and committed to its public interface. Never propose `1.0.0` on your own — that's a product decision, not a changelog one.
- **Post-1.0**, standard SemVer applies: MAJOR for breaking changes, MINOR for backwards-compatible features, PATCH for backwards-compatible fixes.
- Commit history is the cheapest input here: this project's commits follow **[Conventional Commits](https://www.conventionalcommits.org/)**, so the types since the last version tell you the bump directly — any `BREAKING CHANGE:` or `!` → major (minor while pre-1.0), any `feat:` → minor, otherwise `fix:` → patch. Types like `docs:`, `chore:`, `refactor:`, `test:`, `ci:`, and `style:` contribute **nothing** to a version; if that's all there is since the last cut, there's no version to cut.

**Manual mode:** show the user the summary and the proposed number, and **let them confirm or adjust before anything is written.**

**Automatic mode:** don't ask — check the guardrails below, then go straight to Step 5.

### Automatic guardrails

These exist so hands-off versioning can't run the number away. They only apply in automatic mode; a user running `/version` can override any of them.

- **Never reach `1.0.0` on your own, and never bump MAJOR.** While on `0.y.z`, breaking changes are a minor bump, as above. After `1.0.0`, if the changes call for a major bump, don't write — say one line: "Breaking changes since vX.Y.Z — run `/version` to cut 2.0.0 when you're ready." Majors are a product decision.
- **One cut per ship, at most one step.** Bump exactly one level from the last version — never skip numbers, never cut two versions in one run.
- **Batch, don't trickle.** Apply Step 3 strictly. A lone `fix:` or a feature that isn't usable yet waits for the next ship; it isn't lost, it rolls in. If the last version is from today and the only new material is patch-level, skip.
- **In doubt, skip.** Automatic mode's default is *no version*. A skipped cut is free; a wrong one is permanent.

### 5. Write

- Append a new entry to `.docs/versions.json` (create the file if needed). Path is always `.docs/versions.json`. Format:

```json
[
  {
    "version": "0.1.0",
    "date": "YYYY-MM-DD",
    "title": "Short milestone name",
    "changes": [
      "Change one",
      "Change two"
    ]
  }
]
```

- Keep the array sorted newest-first.
- Add a separator line in `.docs/changelog.md` after the processed entries, exactly as defined in `.docs/changelog-spec.md` (e.g. `---  v0.1.0 released`)

### 6. Check 1.0 readiness

Only while the project is on `0.y.z`, and only after a version was actually written, in either mode. Running only on real cuts means it comes up at most once per version, so it can't nag.

`1.0.0` means **ready for production**: someone besides the developer can rely on it for what it promises. That's a judgement about the product, not the commit count, so don't use version numbers, age, or how many features shipped as evidence. Check these, from evidence you can point to:

- **The promise is kept.** Every item under **Core Features** in `.docs/seed.md` is shipped and usable end-to-end, not just started or behind a flag. Verify it in the code and the changelog, not only by closed backlog items. Anything in **Non-Goals** doesn't count against it.
- **Nothing known is broken on the main path.** No open item in `.docs/backlog.md` or GitHub Issues breaks a core feature, and the latest report in `.docs/audits/` (if one exists) has no unresolved CRITICAL finding.
- **It runs somewhere other than the developer's machine.** There's a real way for a user to reach or install it (a deploy, a store build, a published package), and it doesn't depend on local-only config or dev secrets.

If all three hold, add one line to the report: "Looks 1.0-ready: <one clause of evidence>. Run `/version 1.0.0` if you agree." If any fails, or you can't tell (no seed, no way to verify), say nothing. A missing nudge costs nothing; a premature one is noise.

When the user asks for `1.0.0` in manual mode, run the same check and show what passed and what didn't. Then cut it if they still want it — it's their call, not a gate.

### 7. Report

- **Manual mode:** confirm what was written.
- **Automatic mode:** one line (plus the readiness line from Step 6, if it fired), whichever applies — `Cut v0.4.0 "Auth flow" (5 changes)`, or `No version: nothing user-facing since v0.3.1`, or the major-bump line from the guardrails. Nothing more.

**RULES:**

- In manual mode, never write a version without the user confirming the number. In automatic mode, write without asking — but only inside the guardrails.
- Prefer not cutting. A skipped version costs nothing — the changes roll into the next one. An unnecessary version is permanent.
- Keep the JSON clean and minimal. No metadata, no commit hashes, no timestamps beyond the date.
- The title should be 2-4 words capturing the milestone theme (e.g., "Project kickoff", "Auth flow", "Design polish").
- Don't remove entries from `.docs/changelog.md` — just add the separator line so the next `/version` knows where to start (see `.docs/changelog-spec.md`).
