---
name: to-issues
description: Break a plan, spec, or PRD into independently-grabbable backlog items using tracer-bullet vertical slices, then append them to .docs/backlog.md. Use when user wants to convert a plan into issues, create implementation tickets, or break down work into tasks.
---

# To Issues

Break a plan into independently-grabbable backlog items using vertical slices (tracer bullets), then write them into `.docs/backlog.md` so you can tackle them one at a time with `/new`.

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

### 5. Write the items to the backlog

For each approved slice, append an item to `.docs/backlog.md` in dependency order (blockers first). Match the existing backlog style — a top-level bullet per item with nested detail bullets. Use the shape below, condensed to fit the backlog:

<backlog-item-template>
- **<Title>** (`HITL`/`AFK`) — one-line description of the end-to-end behavior, not layer-by-layer implementation.
    - Acceptance: criterion 1; criterion 2; criterion 3
    - Blocked by: <other item title>, or "none — can start immediately"
    - Source: `.docs/prds/<slug>.md` (if the slices came from a PRD; otherwise omit)
</backlog-item-template>

Avoid specific file paths or code snippets — they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts.

Don't modify or remove unrelated existing backlog items. Once written, work through them in dependency order with `/new` (passing the item as context), and `/tidy` archives completed ones to the changelog.
