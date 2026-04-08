You are cleaning up the user's backlog — organizing raw notes and archiving completed work.

**Custom instructions from user:** $ARGUMENTS

**Read:**

- `.docs/backlog.md` — the user's notepad with raw ideas and notes

**Your task:**

### 1. Check for completed items

- Commented items in the backlog mean the user has already marked them as done — treat these as completed.
- Check the latest ~3 commits if necessary (unless the user specifies a different number) and the current codebase to see if any other backlog items have already been completed.
- Move completed items to `.docs/changelog.md` with today's date.
- Don't ask the user for permission to move done items — they asked you to run this command. Only ask if you're unsure whether an item is really complete.
- If you don't see anything clearly changed, tell the user, but first check latest commits and edits.

### 2. Clean up the backlog

- Remove duplicates or items that are clearly the same thing
- **Never edit, reword, or reformat what the user wrote** — preserve their exact text
- Don't reorder, prioritize, or categorize items — the user decides what matters

**backlog.md format** (keep it flat and simple):

```markdown
- raw idea or note
- another thought
- fix that thing on the settings page
```

**changelog.md format** (flat chronological log — versions are handled by `/version`):

```markdown
- YYYY-MM-DD HH:mm [x] completed item
- YYYY-MM-DD HH:mm /command — what it did
```

**RULES:**

- Backlog stays clean — no changelog, no categories, no tags, no priorities
- Don't add items from the seed, docs, or code — this is only for what the user writes
- If `.docs/changelog.md` doesn't exist yet, create it per `.docs/changelog-spec.md`
- If there's nothing to clean up or add to changelog, say so and move on
- Don't add version separator lines — that's `/version`'s job (see `.docs/changelog-spec.md`)
- The format `YYYY-MM-DD HH:mm` has to indicate the current day and time, retrieve them to make sure they are right. This is important
- Place new items in the changelog at the bottom of the list

**After completing, show the user** a quick summary: how many items added to changelog, how many still pending. If there's a good amount of unversioned work in the changelog, suggest running `/version`.
