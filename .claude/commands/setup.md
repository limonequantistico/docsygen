You are wiring the project's design system and docs into the actual codebase. This is the bridge between documentation and code.

**Custom instructions from user:** $ARGUMENTS

**Read:**
- `.docs/design-system.md` — the visual decisions (tokens, colors, typography, spacing)
- `.docs/tech-stack.md` — how styles should be implemented (Tailwind, CSS variables, Tamagui themes, etc.)
- `.docs/seed-document.md` — project features and scope
- `.docs/assets/imgs/prototypes/` — wireframes, to understand which UI elements are needed
- Scan the current project structure to understand where files should go

**Your task has two phases. Complete each one and wait for user approval before moving to the next.**

---

### Phase 1: Centralize styles
Create the global styles/theme file in the format the stack requires:
- **Tailwind** → customize `tailwind.config` with the design system tokens
- **Tamagui** → create/update `tamagui.config.ts` with themes and tokens
- **Vanilla CSS** → create `globals.css` with CSS custom properties
- **Other** → adapt to whatever the stack uses

All design tokens from the design system should live in this one place. No hardcoded values anywhere else.

**After creating the styles file, ask the user** if it looks right before proceeding.

---

### Phase 2: Propose base components
Based on the wireframes and seed features, propose a list of reusable components that should be built before feature work begins:
- Look at the wireframes: what elements appear on multiple screens? (buttons, cards, inputs, navigation, layout shells, etc.)
- If using a component library (shadcn, MUI, etc.), only list components that need customization or don't exist in the library

**Present the list to the user** with: component name, purpose, and key variants (e.g., Button: primary/secondary/ghost, sm/md/lg). **Do not start building until the user approves the list.**

Then, for each approved component:
- Create the actual component file in the right location for the project structure
- Each component must pull its values from the centralized styles file — never hardcode colors, spacing, or typography
- Build it properly: fully styled, all approved variants working, polished. These are the building blocks for the whole app — they should look and feel right.
- Build in small batches and check in with the user periodically

**Showcase:** Create a simple showcase page/screen where all built components are displayed together with their variants. This gives the user a single place to visually verify that everything looks right and works as expected. Keep it simple — just the components rendered with labels, not a full storybook.

---

**RULES:**
- Read the actual project structure before creating anything — don't assume folder conventions
- If the design system or tech stack doc is missing, stop and tell the user which command to run first
- Don't over-build. A Button with 3 variants is enough — don't add 15 props for hypothetical use cases
- If the project already has components or a styles file, integrate with what exists rather than replacing it
- Ask before overwriting any existing files

**After completing, ask the user** to check the showcase and verify the components. If everything looks good, suggest `/resume` to get a fresh assessment of where to go next.
