---
name: init
description: Scaffold the baseline .docs/ structure and CLAUDE.md that other docsygen skills depend on, and bring a project set up under an older docsygen up to current conventions (idempotent). Use only when the user explicitly asks to initialize or update docsygen in this project, or runs /init.
---

You are initializing the **docsygen docs structure** in the current project. Create the baseline `.docs/` skeleton that the other docsygen commands depend on — most importantly `.docs/changelog-spec.md`, which ~15 commands reference when writing the changelog.

**This command has two jobs.** In a new project it scaffolds. In a project set up under an **older version of docsygen**, it also brings the conventions up to date — skills get added, renamed, and reworked over time, and a project scaffolded a few releases ago silently misses all of it. Re-running `/init` after updating the plugin is the intended way to catch up.

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

Your scratchpad. Dump ideas and tasks here anytime, one line each — pin this file in your IDE.
No network, no auth, no context switch, and the agent reads it on every task.

Work that's *definitely* happening, needs discussion, or someone else might pick up
belongs in GitHub Issues instead. An item graduates from here to there; it never lives
in both, so there's nothing to keep in sync.

`/to-issues` slices a plan into items and writes them to whichever you pick.
`/tidy` archives done items from this file to the changelog.
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
  - `/drift` — ≤10 words
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

**7. `.gitignore`** (at the project root) — if one **exists**, don't overwrite it: check whether it covers OS and editor junk, and append only the missing lines under a comment. If it's **missing**, create it with at least this baseline, then add stack-specific entries (`node_modules/`, `.venv/`, `build/`, `DerivedData/`, …) based on `.docs/tech-stack.md` or what's actually in the repo:

~~~gitignore
# OS
.DS_Store
Thumbs.db

# Editors
.vscode/
.idea/
*.swp

# Env & secrets — never commit these
.env
.env.*
!.env.example
*.pem
*.key
~~~

Committed OS junk like `.DS_Store` is the most common way a clean repo starts looking sloppy, and a missing `.env` line is how secrets leak. Getting this right at `/init` is cheaper than cleaning it up later.

**8. `CLAUDE.md`** (at the project root, not under `.docs/`) — the project rules docsygen commands assume. Create it only if missing; never overwrite an existing `CLAUDE.md`, since the project may already have its own rules. If one exists, leave it and tell the user to make sure it references the `.docs/` conventions below. Content to write:

~~~markdown
# Project Rules

- If useful documentation is available, use it. Use Context7's MCP for any needed deeper research.
- If the repo has a `.codegraph/` directory it is indexed by CodeGraph: reach for `codegraph explore "<symbols or question>"` before grep/find when you need to locate or understand code, and `codegraph impact <symbol>` before changing or renaming anything shared. One call returns the relevant symbols' source plus the call paths between them, including dynamic-dispatch hops grep can't follow. If there is no `.codegraph/` directory, ignore all of this and search normally — indexing is the user's decision, so never run `codegraph init` unprompted.
- Follow the tech stack defined in `.docs/tech-stack.md`. Don't introduce technologies not listed there.
- Follow the design system defined in `.docs/design-system.md`. Use global style variables, don't hardcode values.
- Before starting any task, check `.docs/seed.md` for project context. But docs may be outdated — when they conflict with the actual code, trust the code.
- Keep tasks small and sequential. Complete one thing fully before moving to the next.
- Document features as you build them, not after.
- If a technology or library not in the tech stack would solve a real problem you're facing right now, mention it once. Don't advocate — just flag it and let the user decide.
- When a domain term gets settled (or conflicts with existing usage), or a decision passes the Architecture Decision Record (ADR) test (hard to reverse, surprising without context, a real trade-off), **offer** to capture it with `/domain-modeling` — glossary in `CONTEXT.md`, ADRs in `.docs/adr/`. Propose it; don't silently edit the domain docs.
- Log completed work to `.docs/changelog.md` as you finish it, following `.docs/changelog-spec.md` — not only when a command runs. Work done by plain conversation is the work most likely to go unrecorded, and an empty changelog makes `/version` and `/tidy` useless.
- If a doc you're reading contradicts the code you're looking at, say so in one line and offer `/drift` — don't quietly work around it. Docs drift fastest right after a stretch of building, which is exactly when nobody thinks to check them.
- After pushing or merging, check whether the work since the last version in `.docs/versions.json` adds up to something a user would notice. If it does, propose cutting a version with `/version` — don't wait to be asked. If it doesn't, stay quiet: scaffolding, docs, refactors, and work-in-progress are not releases, and an inflated version number is worse than a missing one.

# Writing code

- Read a few nearby files of the same kind (components, routes, hooks, handlers) before writing new ones. New code should look like the same team wrote it — same naming, folder layout, import style, error handling.
- Extend before you duplicate. Search for an existing pattern, component, or utility that already does something close, and propose adapting it when possible. Only build a parallel implementation when there's a clear reason — and say what it is.
- If something is genuinely unclear, ask one batch of focused questions before starting. Don't drip-feed questions across turns, and don't ask about details you can reasonably default — decide, and mention the choice.
- Don't over-build. Only the variants, options, and surfaces actually needed.
- If the project has a storybook, showcase, or demo page, add new UI there. If it has none, mention it — don't create one without asking.
- Before calling a piece of work finished, verify it — and size the check to the change. Use what the project already gives you: build, typecheck, or lint first, then actually exercise the path you touched. For UI that means looking at it — `.docs/preview.md`, if it exists, records how to launch and view this app; follow it rather than working it out again. If tests already cover the area, run them; running the whole suite for a copy change is waste, and a docs-only change needs none of this. Then say what you checked and what you didn't — "done" means verified, and code that was written and read but never run is "written, not run". Never add a test framework, a preview setup, or any scaffolding just to satisfy this rule; that's `/test` and `/ux-review`'s job, and both need approval first.
- When something is broken, work from evidence rather than the first plausible cause. Trace the real code path, hold at least two competing explanations, and get an observation that kills one of them before you edit — adding logging and asking for a reproduction is usually cheaper than a wrong fix. Say which explanation the evidence supports, and remove any logging you added to find it. If a second fix attempt on the same symptom still hasn't produced a root cause you can state in one sentence, stop editing and say so — and mention `/debug` once, as something the user can run. Don't run it yourself, and don't raise it again.
- If the work added or changed behaviour on a critical path and no test covers it, say so once and offer `/test`. Don't write the test unprompted, and don't repeat the offer every turn.

# Custom Commands

- When executing a command, if the user added extra instructions after the command name, respect them — they override or extend the default behavior.
- If the user asks for something outside the current command's scope, don't try to handle everything. Suggest the appropriate command instead (run `/help` to see the full list).
- Chained flows are fine, but stay alert to runaway loops — both build/test retry loops and token-burning exploration loops. If the same failure repeats 4/5 times, stop and ask instead of trying again. If a task is ballooning in scope or token usage past what it should reasonably cost, pause and check in before continuing.
~~~

### Bringing an existing project up to date

If `.docs/` already exists, this is an update pass as well as a scaffold. Beyond creating missing files, check for convention drift and **report it — don't fix it silently**:

- **`CLAUDE.md` rules.** The template below is the current set. An existing `CLAUDE.md` is never overwritten, but compare it against the template and list any rules it's missing, with a one-line explanation of what each buys. Offer to append the missing ones; let the user choose. Their own custom rules stay untouched.
- **`.docs/changelog-spec.md`.** Canonical, not user data — if it differs from the version below, say it's outdated and offer to update it.
- **Stale command names.** Grep `.docs/` and `CLAUDE.md` for references to commands that no longer exist and name the replacements. As of now: `/new` (deleted — building needs no command), `/seed-update` (folded into `/seed`), `/design` (now `/design-system`), `/sync` (now `/drift`).
- **Code intelligence.** If the repo has no `.codegraph/` directory and the codebase is big enough that finding things costs real time, mention **once** that CodeGraph would let the agent answer code questions by call graph instead of grep — the `CLAUDE.md` rule above is written to use it and is otherwise inert. Which line to give depends on the machine: if the `codegraph` CLI is on PATH, it's `codegraph init` from the repo root; if it isn't, it's `npm install -g @colbymchenry/codegraph` first (scoped name — the bare `codegraph` npm package is unrelated). Offer it and move on; never install or index anything yourself, and don't raise it again if the user passes.
- **Newer artifacts the project has no idea about.** Don't create them — just mention which ones apply and which command produces them: `.docs/preview.md` (`/ux-review`), `.docs/logging.md` (`/logs`), `.docs/adr/` and `CONTEXT.md` (`/domain-modeling`), `.docs/versions.json` (`/version`), `.docs/audits/` (`/deep-audit`), `.docs/commit-convention.md` (`/commit`, `/merge`, `/push` — written automatically the first time one of them runs).

Keep this to a short list. If nothing has drifted, say so in one line and move on.

### After scaffolding

- `CLAUDE.md` is created above. If the project already had one, point out it was left untouched and that it should reference the `.docs/` conventions (`tech-stack.md`, `design-system.md`, `seed.md`).
- **Offer the two ways to start**, choosing which to lead with based on what's in `.docs/idea.md`:
  - **Empty or just-created** — say there are two routes and let the user pick: write raw notes into `.docs/idea.md` (best when they roughly know what they want), or run `/grill-with-docs` and let the interview find the idea while settling the vocabulary (best when it's still fuzzy — waiting until you can write a coherent brief is the wrong order). Either way, `/seed` comes next and can work from the notes *or* from the interview still in context.
  - **Already has content** — point straight at `/seed`, and mention `/grill-with-docs` only as the option if the notes feel unresolved.
- Suggest `/help` for the full workflow.

**Logging:** On success, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /init — [brief description of what was created or skipped]`.
