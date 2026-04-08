# Changelog format (canonical)

All commands that write to the changelog must follow this spec. The file is **`.docs/changelog.md`**.

## Structure

1. **Optional title** — First line may be `# Changelog`. If the file is created from scratch, include this line.
2. **Blank line** — After the title, if present.
3. **Entries** — One bullet per line, chronological order. **New entries are always appended at the end of the file** (below any existing lines, including past version separators).

## Entry format

Every entry starts with a timestamp:

```markdown
- YYYY-MM-DD HH:mm <rest of line>
```

Use the **actual** current local date and time when writing (do not invent timestamps).

## Entry types

- **Completed work** (often from `/next` or `/tidy`): `- YYYY-MM-DD HH:mm [x] description`
- **Command / activity log**: `- YYYY-MM-DD HH:mm ran /command-name — short description`
- **Short command tag** (e.g. `/sync`): `- YYYY-MM-DD HH:mm /sync — ≤10 words`

Keep lines single-line where possible. Do not add sections, tags, or categories inside the changelog body.

## Version cuts (`/version`)

When `/version` processes the log, it **does not delete** prior entries. It inserts a **separator line** immediately **after** the block of entries that were rolled into that release:

```markdown
---  v0.2.0 released
```

(Exactly two spaces after the three dashes, then `v`, semver, space, `released`.)

The next `/version` run treats entries **below** the latest separator as “since last release.”

## Rules

- Do not reorder old entries.
- Do not edit the user’s wording when moving backlog items into the changelog (see `/tidy`).
- This file is **tracked in git** so the team shares the same history.
