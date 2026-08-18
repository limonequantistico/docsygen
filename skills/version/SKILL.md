---
name: version
description: Cut a new app version — summarize changes since last release and write to versions.json. Use only when the user explicitly asks to cut a version or runs /version.
---

You are cutting a new app version — reviewing what changed since the last release and producing a structured version record.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

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

Show the user the summary and the proposed number, and **let them confirm or adjust before anything is written.**

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

**RULES:**

- Never write a version without the user confirming the number. Proposing one unprompted is fine and encouraged; deciding one silently is not.
- Prefer not cutting. A skipped version costs nothing — the changes roll into the next one. An unnecessary version is permanent.
- Keep the JSON clean and minimal. No metadata, no commit hashes, no timestamps beyond the date.
- The title should be 2-4 words capturing the milestone theme (e.g., "Project kickoff", "Auth flow", "Design polish").
- Don't remove entries from `.docs/changelog.md` — just add the separator line so the next `/version` knows where to start (see `.docs/changelog-spec.md`).
