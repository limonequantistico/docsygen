---
name: init
description: Scaffold the baseline .docs/ structure and CLAUDE.md that other docsygen skills depend on (idempotent). Use only when the user explicitly asks to initialize docsygen or runs /init.
---

You are initializing the **docsygen docs structure** in the current project. Create the baseline `.docs/` skeleton that the other docsygen commands depend on — most importantly `.docs/changelog-spec.md`, which ~15 commands reference when writing the changelog.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

### Rules

- This command is **idempotent and safe to re-run**. Never overwrite a file that already exists and contains work — `idea.md`, `backlog.md`, `changelog.md`, and any `prds/` content are user data. Only create files that are missing.
- `changelog-spec.md` is a canonical reference, not user data. If it is missing, create it. If it already exists but differs from the canonical content below, tell the user it's outdated and offer to update it — don't silently overwrite.
- Work from the project root (where you'd expect `.docs/` to live). If you're unsure of the root, confirm with the user before writing.
- At the end, print a short summary: which files were **created**, which were **skipped** (already present), and any that need attention.

### Files to create (only if missing)

**1. `.docs/idea.md`**
```markdown
# Idea

Drop your raw notes here — brain dump, bullet points, **voice transcription** (superwhisper, audio notes), anything.
This file is the input for `/seed`.
```

**2. `.docs/backlog.md`**
```markdown
# Backlog

Dump ideas and tasks here anytime. Pin this file in your IDE.
Use `/to-issues` to slice a plan into items, `/new` to work through them, `/tidy` to archive done items to the changelog.
```

**3. `.docs/changelog.md`**
```markdown
# Changelog
```

**4. `.docs/prototype-prompt.md`**
```markdown
# Prototype design-tool prompt

This file is filled by the `/prototype` command with a ready-to-paste prompt for tools like Google Stitch, Figma AI, or V0. Run `/prototype` to generate it.
```

**5. Asset folders** — create empty-but-tracked directories:
- `.docs/assets/imgs/prototypes/.gitkeep`
- `.docs/assets/imgs/references/.gitkeep`

**6. `.docs/changelog-spec.md`** — write **exactly** this content (this is the canonical spec; the `~~~` fence below wraps the literal file content, which itself contains ``` blocks):

~~~markdown
# Changelog format (canonical)

All commands that write to the changelog must follow this spec. The file is **`.docs/changelog.md`**.

## Structure

1. **Optional title** — First line may be `# Changelog`. If the file is created from scratch, include this line.
2. **Blank line** — After the title, if present.
3. **Date sections** — Entries are grouped under day headers:

```markdown
## YYYY-MM-DD
```

4. **Time blocks** — Entries written in the same batch are grouped under a time header:

```markdown
### HH:mm
```

5. **Entries** — Plain bullet lines under the current time block, indented by two spaces.
6. **Release separators** — `/version` may insert a release separator line between groups:

```markdown
---  `v0.2.0 released`
```

## Writing rules

- Use the **actual** current local date and time when writing. Do not invent timestamps.
- New entries should be appended in chronological order within the current day section.
- If today's `## YYYY-MM-DD` section already exists, append within it instead of creating a duplicate.
- If the current `### HH:mm` block already exists inside today's section, append to that block.
- If today's section exists but the current time block does not, create a new `### HH:mm` block at the bottom of today's section.
- If the file does not exist yet, create it with `# Changelog`, a blank line, today's `## YYYY-MM-DD`, and the current `### HH:mm`.
- Do not reorder old entries or move existing release separators.
- Indent bullets under each `### HH:mm` block by two spaces.

## Entry types

### Completed work

Use a plain bullet with the user's original wording. Do **not** add `[x]`.

```markdown
  - completed item
```

### Command / activity log

Wrap command names in backticks.

```markdown
  - ran `/command-name` — short description
```

### Short command tag

Short command tags should also use backticks.

```markdown
  - `/sync` — ≤10 words
```

### Untimed notes

Avoid untimed notes when writing new entries. If an existing changelog already contains older untimed material, preserve it.

## Version cuts (`/version`)

When `/version` processes the log, it **does not delete** prior entries. It inserts a **separator line** immediately **after** the block of entries that were rolled into that release:

```markdown
---  `v0.2.0 released`
```

Use exactly three dashes, two spaces, and a backticked label in the form `` `vX.Y.Z released` ``.

The next `/version` run treats entries **below** the latest separator as “since last release.”

## Rules

- Do not edit the user’s wording when moving backlog items into the changelog unless a command explicitly says to normalize it.
- Keep entries as single-line bullets where practical.
- Do not add `[x]` markers.
- Do not add extra categories inside a time block.
- This file is **tracked in git** so the team shares the same history.
~~~

**7. `CLAUDE.md`** (at the project root, not under `.docs/`) — the project rules docsygen commands assume. Create it only if missing; never overwrite an existing `CLAUDE.md`, since the project may already have its own rules. If one exists, leave it and tell the user to make sure it references the `.docs/` conventions below. Content to write:

~~~markdown
# Project Rules

- If useful documentation is available, use it. Use Context7's MCP for any needed deeper research.
- Follow the tech stack defined in `.docs/tech-stack.md`. Don't introduce technologies not listed there.
- Follow the design system defined in `.docs/design-system.md`. Use global style variables, don't hardcode values.
- Before starting any task, check `.docs/seed.md` for project context. But docs may be outdated — when they conflict with the actual code, trust the code.
- Keep tasks small and sequential. Complete one thing fully before moving to the next.
- Document features as you build them, not after.
- If a technology or library not in the tech stack would solve a real problem you're facing right now, mention it once. Don't advocate — just flag it and let the user decide.
- When a domain term gets settled (or conflicts with existing usage), or a decision passes the ADR test (hard to reverse, surprising without context, a real trade-off), **offer** to capture it with `/domain-modeling` — glossary in `CONTEXT.md`, ADRs in `.docs/adr/`. Propose it; don't silently edit the domain docs.

# Custom Commands

- When executing a command, if the user added extra instructions after the command name, respect them — they override or extend the default behavior.
- If the user asks for something outside the current command's scope, don't try to handle everything. Suggest the appropriate command instead (run `/help` to see the full list).
- Chained flows are fine, but stay alert to runaway loops — both build/test retry loops and token-burning exploration loops. If the same failure repeats 4/5 times, stop and ask instead of trying again. If a task is ballooning in scope or token usage past what it should reasonably cost, pause and check in before continuing.
~~~

### After scaffolding

- `CLAUDE.md` is created above. If the project already had one, point out it was left untouched and that it should reference the `.docs/` conventions (`tech-stack.md`, `design-system.md`, `seed.md`).
- Point the user at `.docs/idea.md` as the starting point, then `/seed`. Suggest `/help` for the full workflow.

**Logging:** On success, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /init — [brief description of what was created or skipped]`.
