# Project Rules

- If useful documentation is available, use it. Use Context7's MCP for any needed deeper research.
- Follow the tech stack defined in `.docs/tech-stack.md`. Don't introduce technologies not listed there.
- Follow the design system defined in `.docs/design-system.md`. Use global style variables, don't hardcode values.
- Before starting any task, check `.docs/seed.md` for project context. But docs may be outdated — when they conflict with the actual code, trust the code.
- Changelog entries must follow `.docs/changelog-spec.md`.
- Keep tasks small and sequential. Complete one thing fully before moving to the next.
- Document features as you build them, not after.
- If a technology or library not in the tech stack would solve a real problem you're facing right now, mention it once. Don't advocate — just flag it and let the user decide.

# Custom Commands

- When executing a command, if the user added extra instructions after the command name, respect them — they override or extend the default behavior.
- If the user asks for something outside the current command's scope, don't try to handle everything. Suggest the appropriate command instead (run `/help` to see the full list).
- Always ask the user before proceeding to the next step. Never chain commands automatically.
