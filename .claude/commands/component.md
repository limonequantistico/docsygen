You are building a new reusable component for this project.

**The user asked for this:** $ARGUMENTS

Before building anything new from scratch, check if something similar already exists in the project. If it does, extend or adapt it instead of creating a duplicate. Ask the user first how the change should be handled.

**Read:**
- The centralized styles/theme file (globals.css, tailwind.config, tamagui.config, or equivalent) — this is the source of truth for all visual values
- A few existing components in the project — understand the patterns, naming conventions, folder structure, and how they import and use the centralized tokens
- `.docs/design-system.md` — for broader design direction if needed

**Your task:**

### 1. Propose
Before writing code, present:
- **Component name** and where it should live in the project structure
- **Purpose** — what it does and where it will be used
- **Variants** — sizes, states, visual variations it needs
- **Similar existing components** — if any, and whether to extend them or create something new

**Wait for the user's approval before building.**

### 2. Build
- Create the component file in the right location, following the project's existing conventions
- Pull all visual values (colors, spacing, typography, radii, shadows) from the centralized styles — never hardcode
- Build it properly: fully styled, all approved variants working, polished
- If the component library (shadcn, MUI, etc.) has a base version, extend it rather than building from scratch

### 3. Showcase
- Add the new component to the showcase page with all its variants visible
- If no showcase page exists yet, mention it and ask the user if they want one created

**RULES:**
- Follow the exact same patterns as existing components in the project
- Don't over-build — only the variants the user needs, not every possible combination
- Ask before modifying any existing files
