---
name: tidy
description: Archive completed backlog items to the changelog (backlog cleanup only). Use only when the user explicitly asks to tidy the backlog or runs /tidy.
---

You are cleaning up the user's backlog by archiving completed work only.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

**Read:**

- `.docs/backlog.md` — the user's notepad with raw ideas and notes

**Your task:**

### 1. Check for completed items

- Default behavior: only treat commented items in the backlog as completed.
- Commented items in the backlog mean the user has already marked them as done — move those to the changelog.
- Do **not** inspect recent commits or the current codebase unless the user explicitly asks you to verify other items too.
- If the user explicitly asks for deeper verification, check the latest ~3 commits by default (unless they specify a different number) and the current codebase to see if any other backlog items have already been completed.
- Move completed items to `.docs/changelog.md` with today's date.
- Don't ask the user for permission to move done items — they asked you to run this command. Only ask if you're unsure whether an item is really complete.
- If there are no commented completed items and the user did not explicitly ask for deeper verification, say there's nothing to clean up and stop.
- If the user did ask for deeper verification and you still don't see anything clearly changed, tell the user after checking commits and edits.

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

**changelog.md format** (canonical grouped log — versions are handled by `/version`; see `.docs/changelog-spec.md`):

```markdown
# Changelog

## YYYY-MM-DD

### HH:mm
  - completed item
  - `/tidy` — moved N completed backlog items to changelog and left M pending

---  `v0.1.0 released`
```

**RULES:**

- Backlog changes are limited to removing completed items that are being moved to the changelog
- Leave every non-completed backlog item exactly as written and in the same order
- Don't normalize or tidy the backlog format beyond removing completed items
- Don't add items from the seed, docs, or code — this is only for what the user writes
- By default, this command is a backlog cleanup pass, not a repo audit
- If `.docs/changelog.md` doesn't exist yet, create it per `.docs/changelog-spec.md`
- If there's nothing to clean up or add to changelog, say so and move on
- Follow `.docs/changelog-spec.md` exactly for all changelog writes.
- Don't add version separator lines — that's `/version`'s job (see `.docs/changelog-spec.md`)
- Retrieve the current local day and time to make sure they are correct. This is important.
- Completed backlog items should be added as indented plain bullets under the current time block, preserving the user's original wording:

```markdown
  - completed item
```

- Wrap commands in backticks, e.g. `` `/tidy` ``.
- Do not add `[x]` markers to changelog entries.
- After moving completed items, append a final log entry for the command in the same time block, in this format:

```markdown
  - `/tidy` — moved 3 completed backlog items to changelog and left 12 pending
```

**After completing, show the user** a quick summary: how many items added to changelog, how many still pending. If there's a good amount of unversioned work in the changelog, suggest running `/version`.
