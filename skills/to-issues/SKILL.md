---
name: to-issues
description: Break a plan, spec, or PRD into independently-grabbable items using tracer-bullet vertical slices, then write them to .docs/backlog.md or to GitHub Issues. Use when user wants to convert a plan into issues, create implementation tickets, or break down work into tasks.
---

# To Issues

Break a plan into independently-grabbable items using vertical slices (tracer bullets), then write them where the project tracks work — `.docs/backlog.md` or GitHub Issues — so they can be tackled one at a time.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference as an argument (a path like `.docs/prds/<slug>.md`, or the name of a PRD), read its full body before slicing.

### 2. Load project context (optional)

If you have not already, load `.docs/seed.md`, `.docs/tech-stack.md`, and `.docs/design-system.md`, and skim nearby code to understand the current state. Item titles and descriptions should use the project's own vocabulary. When docs and code conflict, trust the code.

### 3. Draft vertical slices

Break the plan into **tracer bullet** items. Each item is a thin vertical slice that cuts through ALL integration layers end-to-end, NOT a horizontal slice of one layer.

Slices may be 'HITL' or 'AFK'. HITL slices require human interaction, such as an architectural decision or a design review. AFK slices can be implemented and merged without human interaction. Prefer AFK over HITL where possible.

<vertical-slice-rules>
- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests)
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
</vertical-slice-rules>

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each slice, show:

- **Title**: short descriptive name
- **Type**: HITL / AFK
- **Blocked by**: which other slices (if any) must complete first
- **User stories covered**: which user stories this addresses (if the source material has them)

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the dependency relationships correct?
- Should any slices be merged or split further?
- Are the correct slices marked as HITL and AFK?

Iterate until the user approves the breakdown.

### 5. Ask where the items go

Two destinations, and they are **not two copies of the same list** — they're different stages, so nothing needs syncing:

- **`.docs/backlog.md`** — the scratchpad. Zero friction, offline, private, sits in the repo next to the code. Right for *maybe* work and for anything you're the only person who'll touch.
- **GitHub Issues** — committed work. Right when an item is definitely happening, needs discussion, or someone else might pick it up. Buys assignment, comments, PR linking, and notifications; costs a network round-trip and a context switch.

**Pick a default, then confirm in one line — don't interrogate.** If the repo has a GitHub remote, `gh` is installed and authenticated (`gh auth status`), and the repo already has open issues, propose GitHub. Otherwise propose the backlog. Either way say which and let the user redirect.

If the user wants GitHub Issues but `gh` is missing or unauthenticated, say so, write to the backlog instead, and mention that re-running later can push them up.

### 6. Writing to the backlog

For each approved slice, append an item to `.docs/backlog.md` in dependency order (blockers first). Match the existing backlog style — a top-level bullet per item with nested detail bullets. Use the shape below, condensed to fit the backlog:

<backlog-item-template>
- **<Title>** (`HITL`/`AFK`) — one-line description of the end-to-end behavior, not layer-by-layer implementation.
    - Acceptance: criterion 1; criterion 2; criterion 3
    - Blocked by: <other item title>, or "none — can start immediately"
    - Source: `.docs/prds/<slug>.md` (if the slices came from a PRD; otherwise omit)
</backlog-item-template>

Avoid specific file paths or code snippets — they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts.

Don't modify or remove unrelated existing backlog items. Once written, work through them in dependency order — hand one item to the agent as the task — and `/tidy` archives completed ones to the changelog.

### 7. Writing to GitHub Issues

Create one issue per approved slice with `gh issue create`, in dependency order so the blockers exist first and can be referenced by number.

- **Title** — the slice title, no ticket prefix or numbering; GitHub numbers them.
- **Body** — the one-line behavior description, then `## Acceptance` as a checklist, then `Blocked by #<n>` referencing the issue created earlier (or omit the line entirely if nothing blocks it). Add `Source: .docs/prds/<slug>.md` when the slices came from a PRD.
- **Labels** — apply `HITL` / `AFK` as labels rather than title suffixes. Create a label only if the user agrees; if label creation fails or is declined, put the marker in the body instead. Never invent a taxonomy of new labels.
- Print the created issue numbers and URLs at the end so the user can see what landed.

**Don't also write these to `.docs/backlog.md`.** One item lives in one place. If an item is being *promoted* from the backlog to an issue, remove it from `backlog.md` in the same pass and note the issue number in your summary — the whole point is that nothing is duplicated and nothing needs reconciling.
