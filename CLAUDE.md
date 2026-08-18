# Project Rules

- If useful documentation is available, use it. Use Context7's MCP for any needed deeper research.
- Follow the tech stack defined in `.docs/tech-stack.md`. Don't introduce technologies not listed there.
- Follow the design system defined in `.docs/design-system.md`. Use global style variables, don't hardcode values.
- Before starting any task, check `.docs/seed.md` for project context. But docs may be outdated — when they conflict with the actual code, trust the code.
- Keep tasks small and sequential. Complete one thing fully before moving to the next.
- Document features as you build them, not after.
- If a technology or library not in the tech stack would solve a real problem you're facing right now, mention it once. Don't advocate — just flag it and let the user decide.
- When a domain term gets settled (or conflicts with existing usage), or a decision passes the ADR test (hard to reverse, surprising without context, a real trade-off), **offer** to capture it with `/domain-modeling` — glossary in `CONTEXT.md`, ADRs in `.docs/adr/`. Propose it; don't silently edit the domain docs.

# Shipping changes

When a change to the skills is ready to ship, keep these in sync so the update actually reaches users and the docs stay honest:

- **Bump the version — in all four spots.** Both agents cache by version, so updates only reach installed projects when it changes. Bump `version` in `.claude-plugin/plugin.json` **and** `.codex-plugin/plugin.json` (they must stay equal), then update both version spots in the `README.md` ASCII banner to match.
- **Keep the two plugin manifests in sync.** `.claude-plugin/plugin.json` (Claude Code) and `.codex-plugin/plugin.json` (Codex) describe the same plugin; `name`, `version`, and `description` should not drift. The Codex one additionally carries an `interface` block and an explicit `"skills": "./skills/"`.
- **Update `/help` and the README** when a skill is added, removed, or its behavior changes meaningfully. Sync the command list and workflow tips in `skills/help/SKILL.md`, and the workflow table + conventions in `README.md`. If the skill count changes, update it everywhere it's stated.
- **Run `python3 scripts/validate.py` before shipping.** It checks every `SKILL.md` has frontmatter with a `name` matching its directory and a `description`, that all four manifests parse, that the two `plugin.json` versions and both README banner spots agree, and that `/help` lists every skill. Fix what it reports before committing — the same script runs in CI, but by then the broken version may already be on `main`.
- A `/commit` message should mention the version bump.

# Custom Commands

- When executing a command, if the user added extra instructions after the command name, respect them — they override or extend the default behavior.
- If the user asks for something outside the current command's scope, don't try to handle everything. Suggest the appropriate command instead (run `/help` to see the full list).
- Chained flows are fine, but stay alert to runaway loops — both build/test retry loops and token-burning exploration loops. If the same failure repeats 4/5 times, stop and ask instead of trying again. If a task is ballooning in scope or token usage past what it should reasonably cost, pause and check in before continuing.
