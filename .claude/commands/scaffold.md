You are making sure the project structure is ready for development, based on the tech stack.

**Custom instructions from user:** $ARGUMENTS

**Read:**

- `.docs/seed.md` — what the project does
- `.docs/tech-stack.md` — what technologies to use
- Scan the current project structure to see what already exists

**Your task depends on what's already there:**

### If a project structure already exists (template or manual setup):

1. **Validate** — Check that the folder structure matches the tech stack conventions
2. **Dependencies** — Verify all libraries and packages from the tech stack doc are installed and at the right versions. Flag anything missing.
3. **Config files** — Check that linting, formatting, and dev tooling specified in the tech stack are properly configured
4. **Report** — List what's correct, what's missing, and what needs fixing. Ask before making changes.

### If no project structure exists:

1. **Project init** — Run the appropriate init commands for the declared stack (e.g., `cargo init`, `dotnet new`, `npx create-next-app`, framework CLIs). Use Context7's MCP to look up current init commands if unsure.
2. **Folder structure** — Create a sensible directory layout matching the stack's conventions
3. **Config files** — Linting, formatting, and any dev tooling specified in the tech stack
4. **Minimal boilerplate** — One working "hello world" screen/endpoint that proves the stack works end to end

**RULES:**

- Follow the tech stack doc exactly — don't add tools or libraries not listed there
- Keep it minimal — just enough to start building, no over-engineering
- If the tech stack doc is missing or incomplete, stop and tell the user to run `/stack` first
- Ask before running any install commands
- Don't generate placeholder features — just the skeleton
- Don't set up design tokens or styles here — that's `/setup`'s job. If necessary, only setup basic scaffolding for the centralization of styles

**After completing, ask the user** if everything looks right. Suggest `/setup` as the next step to wire the design system into the project and build base components.

**Logging:** On success, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /scaffold — [brief description of what was created or validated]`.
