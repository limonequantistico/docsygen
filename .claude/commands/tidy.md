You are cleaning up the user's backlog — organizing raw notes and archiving completed work.

**Custom instructions from user:** $ARGUMENTS

**Read:**
- `.docs/backlog.md` — the user's notepad with raw ideas and notes

**Your task:**

### 1. Check for completed items
Ask the user how many recent commits to check (e.g., "How many commits should I look at to check for completed items? Or should I skip this and just clean up?"). Then:
- Look at those commits and the current codebase to see if any backlog items have been completed
- Move completed items to `.docs/archive/archive.md` with today's date
- Ask the user to confirm before moving anything — don't assume

### 2. Clean up the backlog
- Remove duplicates or items that are clearly the same thing
- Lightly clean up wording if needed, but keep the user's intent — don't over-edit
- Don't reorder, prioritize, or categorize items — the user decides what matters

**backlog.md format** (keep it flat and simple):

```markdown
# Backlog

- raw idea or note
- another thought
- fix that thing on the settings page
```

**archive.md format** (chronological log):

```markdown
# Archive

- [x] ~~completed item~~ — 2026-03-26
- [x] ~~another completed item~~ — 2026-03-25
```

**RULES:**
- Backlog stays clean — no archive, no categories, no tags, no priorities
- Archive is a separate file that only `/tidy` writes to — it doesn't need to be read often
- Don't add items from the seed, docs, or code — this is only for what the user writes
- If backlog.md or archive.md don't exist yet, create them
- If there's nothing to clean up or archive, say so and move on

**After completing, show the user** a quick summary: how many items archived, how many still pending.