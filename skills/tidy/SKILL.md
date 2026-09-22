---
name: tidy
description: Archive completed backlog items to the changelog, and propose burying items untouched for 60+ days in .docs/graveyard.md (backlog cleanup only). Use only when the user explicitly asks to tidy the backlog or runs /tidy.
---

You are cleaning up the user's backlog: archiving completed work, and proposing to bury work that has sat untouched long enough that it's no longer really on the list.

The idea behind the graveyard: a backlog that only grows stops being read, and an item nobody has touched in months is not a plan — it's noise that hides the plan. Good ideas tend to come back on their own. The graveyard keeps every buried item searchable, so dropping it from the backlog loses nothing.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below. A duration (`/tidy 90 days`, `/tidy 6 weeks`) overrides the staleness threshold for this run.

**Read:**

- `.docs/backlog.md` — the user's notepad with raw ideas and notes
- `.docs/graveyard.md` — if it exists, for step 3

**Your task:**

### 1. Check for completed items

- Default behavior: only treat commented items in the backlog as completed.
- Commented items in the backlog mean the user has already marked them as done — move those to the changelog.
- Do **not** inspect recent commits or the current codebase unless the user explicitly asks you to verify other items too.
- If the user explicitly asks for deeper verification, check the latest ~3 commits by default (unless they specify a different number) and the current codebase to see if any other backlog items have already been completed.
- Move completed items to `.docs/changelog.md` with today's date.
- Don't ask the user for permission to move done items — they asked you to run this command. Only ask if you're unsure whether an item is really complete.
- If the user did ask for deeper verification and you still don't see anything clearly changed, tell the user after checking commits and edits.

### 2. Propose burying stale items

An item is **stale** when none of its lines has changed in more than **60 days** (or the duration the user gave).

- **Age comes from git, not from the file.** Run `git blame --date=short -w -M -- .docs/backlog.md`. An item's age is the date of its *newest* line — the bullet plus any indented sub-bullets or continuation lines under it. Lines marked `Not Committed Yet` are brand new.
- Editing an item resets its age. That is how the user keeps something alive — there is no marker to add.
- If the project isn't a git repo or `backlog.md` isn't tracked, skip this step and say so in one line.
- **Only list items are candidates** — bullet lines and the lines nested under them. Never headings, blank lines, prose notes, or commented (completed) items.
- If nothing is stale, skip to step 3 without comment.
- Otherwise, show the candidates grouped under their backlog section heading, each with its age in days, then ask once: bury all, bury all except some, or none. Nothing moves until the user answers — this is the one exception to leaving pending items alone, and it needs their say every time.
- For the items the user approves:
  - Append them to `.docs/graveyard.md` under a `## Buried YYYY-MM-DD` heading for today (reuse it if it already exists), grouped under a `### <section>` heading matching the backlog section they came from. Items with no section go directly under the date heading, before any `###`.
  - Copy each item **exactly** as written, including its nested lines, and add ` — added YYYY-MM-DD` to the end of its first line, using its blame date. Don't use an HTML comment for this — step 1 reads commented lines as done.
  - Remove those lines from `.docs/backlog.md`. Leave section headings in place even if they end up empty. If a removal leaves two blank lines in a row, collapse them to one.
- If `.docs/graveyard.md` doesn't exist yet, create it with:

```markdown
# Graveyard

Backlog items that sat untouched past `/tidy`'s staleness threshold. Nothing here is deleted.
To revive one, move it back into `.docs/backlog.md` — that resets its age.
```

### 3. Notice what came back

If `.docs/graveyard.md` has entries, compare the pending backlog items against them. When a backlog item clearly restates something buried — the same feature or fix, not just the same area — mention it: which item, when the old one was buried, and any context the old note had that the new one lacks. Offer to bring that context into the backlog item; only edit it if the user says yes.

Only flag clear matches. A resurfaced idea is a signal the idea matters, so a false match is worse than a missed one.

### 4. Preserve the backlog exactly

- Aside from removing completed items (moved to the changelog) and approved stale items (moved to the graveyard), leave `.docs/backlog.md` exactly as is
- **Never edit, reword, reformat, deduplicate, reorder, prioritize, or categorize what the user wrote**
- Preserve spacing, structure, and the existing format of any backlog items that remain

**backlog.md format** (keep it flat and simple):

```markdown
- raw idea or note
- another thought
- fix that thing on the settings page
```

**graveyard.md format:**

```markdown
# Graveyard

Backlog items that sat untouched past `/tidy`'s staleness threshold. Nothing here is deleted.
To revive one, move it back into `.docs/backlog.md` — that resets its age.

## Buried YYYY-MM-DD

- item with no section — added YYYY-MM-DD

### Settings
- stale item, word for word — added YYYY-MM-DD
  - its nested note, word for word
```

**changelog.md format** (canonical grouped log — versions are handled by `/version`; see `.docs/changelog-spec.md`):

```markdown
# Changelog

## YYYY-MM-DD

### HH:mm
  - completed item
  - `/tidy` — moved N completed backlog items to changelog, buried M stale items in the graveyard, and left K pending

---  `v0.1.0 released`
```

**RULES:**

- Backlog changes are limited to removing completed items (to the changelog) and user-approved stale items (to the graveyard)
- Leave every other backlog item exactly as written and in the same order
- Don't normalize or tidy the backlog format beyond those removals
- Don't add items from the seed, docs, or code — this is only for what the user writes
- `.docs/graveyard.md` is append-only: never reword, reorder, or remove what's there, unless the user asks to revive an item — then move it back to the backlog without its `— added` suffix, and remove it from the graveyard
- By default, this command is a backlog cleanup pass, not a repo audit
- If there are no completed items and no stale items, say there's nothing to clean up and stop
- If `.docs/changelog.md` doesn't exist yet, create it per `.docs/changelog-spec.md`
- Follow `.docs/changelog-spec.md` exactly for all changelog writes.
- Don't add version separator lines — that's `/version`'s job (see `.docs/changelog-spec.md`)
- Retrieve the current local day and time to make sure they are correct. This is important.
- Completed backlog items should be added as indented plain bullets under the current time block, preserving the user's original wording:

```markdown
  - completed item
```

- Buried items are **not** written to the changelog — only the count, in the command's log entry.
- Wrap commands in backticks, e.g. `` `/tidy` ``.
- Do not add `[x]` markers to changelog entries.
- After the run, append a final log entry for the command in the same time block, leaving out any part that's zero:

```markdown
  - `/tidy` — moved 3 completed backlog items to changelog, buried 12 stale items in the graveyard, and left 20 pending
```

**After completing, show the user** a quick summary: how many items went to the changelog, how many were buried, how many are still pending, and any resurfaced ideas from step 3. If there's a good amount of unversioned work in the changelog, suggest running `/version`.
