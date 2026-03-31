You are cutting a new app version — reviewing what changed since the last release and producing a structured version record.

**Custom instructions from user:** $ARGUMENTS

**Read:**
- `.docs/versions.json` — previous versions (if exists)
- `.docs/changelog.md` — running log of completed work and command runs
- Recent git history — commits since the last version's date (or all commits if no versions exist yet)

**Your task:**

### 1. Gather changes
- Find the date of the last version in `versions.json`. If no versions exist, treat all changelog entries and recent commits as new.
- Collect everything that happened since that date:
  - Entries from `changelog.md`
  - Meaningful commits from git history (skip merge commits, typo fixes, and other noise)
- Deduplicate — if a changelog entry and a commit describe the same thing, keep one.

### 2. Summarize
- Group changes into a short list of human-readable bullet points (max ~8 items).
- Each item should be ≤15 words, written for an end user, not a developer. Think release notes, not commit messages.
- If there's nothing meaningful since the last version, tell the user and stop.

### 3. Propose version
- Show the user the summary and propose a version number.
- Versioning rules:
  - Start at `0.1.0`
  - **Patch** (`0.1.X`) — small fixes, copy changes, tweaks
  - **Minor** (`0.X.0`) — new features, visible UI changes, meaningful improvements
  - Major stays at `0` until the user explicitly says otherwise
- Let the user confirm or adjust the version number and summary before writing.

### 4. Write
- Append a new entry to `.docs/versions.json` (create the file if needed). Format:

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
- Add a separator line in `changelog.md` after the processed entries: `---  v0.1.0 released`

**RULES:**
- Never auto-bump — always ask the user to confirm the version.
- Keep the JSON clean and minimal. No metadata, no commit hashes, no timestamps beyond the date.
- The title should be 2-4 words capturing the milestone theme (e.g., "Project kickoff", "Auth flow", "Design polish").
- Don't remove entries from changelog.md — just add the separator line so the next `/version` knows where to start.
