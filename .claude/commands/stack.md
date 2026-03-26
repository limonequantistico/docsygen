You are helping me define the technical stack for a new project.

**Custom instructions from user:** $ARGUMENTS

**Read:**
- `.docs/seed-document.md` — project goals, target users, features, constraints
- `.docs/assets/imgs/prototypes/` — if wireframes exist, check for technical implications (real-time features, drag-and-drop, file uploads, maps, etc.)

**User preferences:**
If I have stated preferences (framework, language, libraries), respect them and build around them. Don't argue for alternatives unless there's a clear compatibility issue or some major gain. If I haven't stated preferences, recommend based on the seed.

**Your task:**
Create a `.docs/tech-stack.md` file documenting all technical decisions for this project.

**Guidelines:**

1. **Start from what's decided** — If I've specified a framework or language, don't justify it. Focus on the surrounding choices: what complements it best.

2. **Be specific:**
   - Exact packages/libraries, not categories (e.g., "shadcn/ui + Radix UI primitives" not "component library")
   - Version numbers where relevant
   - Use up-to-date information: look up latest stable versions and current best practices. Remember to use Context7's MCP if necessary.

3. **Justify only what's not obvious:**
   - Why this database over that one? Why this auth provider?
   - Skip justifications for standard choices (e.g., don't explain why TypeScript)

4. **Consider the full stack:**
   - Don't assume frontend-only unless the seed says so
   - Auth, database, deployment, hosting — if the project needs them, include them
   - Development workflow: linting, formatting, testing framework

5. **Keep it practical:**
   - What we need now, not what we might need later
   - Prefer established, well-documented technologies
   - Flag vendor lock-in risks and significant cost implications for scaling
   - If the project is small/MVP, don't over-engineer

**Output:**
A complete `.docs/tech-stack.md` file. Organize by layer (frontend, backend, infrastructure, dev tools). Explain choices, don't just list them.