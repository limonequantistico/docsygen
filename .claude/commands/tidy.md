You are cleaning up the user's backlog by archiving completed work only.

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

### 2. Preserve the backlog exactly

- Aside from removing items that are completed and moved to `.docs/changelog.md`, leave `.docs/backlog.md` exactly as is
- **Never edit, reword, reformat, deduplicate, reorder, prioritize, or categorize what the user wrote**
- Preserve spacing, structure, and the existing format of any backlog items that remain

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

- Backlog changes are limited to removing completed items that are being moved to the changelog
- Leave every non-completed backlog item exactly as written and in the same order
- Don't normalize or tidy the backlog format beyond removing completed items
- Don't add items from the seed, docs, or code — this is only for what the user writes
- If `.docs/changelog.md` doesn't exist yet, create it per `.docs/changelog-spec.md`
- If there's nothing to clean up or add to changelog, say so and move on
- Don't add version separator lines — that's `/version`'s job (see `.docs/changelog-spec.md`)
- The format `YYYY-MM-DD HH:mm` has to indicate the current day and time, retrieve them to make sure they are right. This is important
- Place new items in the changelog at the bottom of the list

**After completing, show the user** a quick summary: how many items added to changelog, how many still pending. If there's a good amount of unversioned work in the changelog, suggest running `/version`.
