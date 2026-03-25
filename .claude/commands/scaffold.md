You are setting up the initial project structure for a stack where the user doesn't have a pre-made template.

**Read:**
- `.docs/seed-document.md` — what the project does
- `.docs/tech-stack.md` — what technologies to use
- `.docs/design-system.md` — design tokens and patterns (if exists)

**Your task:**
Generate the initial project scaffolding:

1. **Project init** — Run the appropriate init commands for the declared stack (e.g., `cargo init`, `dotnet new`, `npm init`, framework CLIs)
2. **Folder structure** — Create a sensible directory layout matching the stack conventions
3. **Config files** — Set up linting, formatting, git hooks, CI basics as specified in the tech stack
4. **Design tokens** — If a design system doc exists, set up the global styles file (CSS variables, theme config, etc.)
5. **Minimal boilerplate** — One working "hello world" screen/endpoint that proves the stack works end to end

**RULES:**
- Follow the tech stack doc exactly — don't add tools or libraries not listed there
- Keep it minimal — just enough to start building features, no over-engineering
- If the tech stack doc is missing or incomplete, stop and tell the user to run `/stack` first
- Ask before running any install commands
- Don't generate placeholder features — just the skeleton
