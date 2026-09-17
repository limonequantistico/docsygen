---
name: setup
description: Wire the design system into code and build base components. Use only when the user explicitly asks to set up styles or components or runs /setup.
---

You are wiring the project's design system and docs into the actual codebase. This is the bridge between design documentation and code.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

**Read:**

- `.docs/design-system.md` — the visual decisions (tokens, colors, typography, spacing)
- `.docs/tech-stack.md` — how styles should be implemented (Tailwind, CSS variables, Tamagui themes, etc.)
- `.docs/seed.md` — project features and scope
- `.docs/assets/imgs/prototypes/` — wireframes, to understand which UI elements are needed
- Scan the current project structure to understand where files should go

**Your task has two phases. Complete each one and wait for user approval before moving to the next.**

---

### Phase 1: Centralize styles

Create the global styles/theme file in the format the stack requires:

- **Tailwind** → theme tokens in CSS (`@theme` in v4) or `tailwind.config` (v3) — check which version the stack uses
- **Tamagui** → create/update `tamagui.config.ts` with themes and tokens
- **Vanilla CSS** → create `globals.css` with CSS custom properties
- **Other** → adapt to whatever the stack uses

All design tokens from the design system should live in this one place. No hardcoded values anywhere else.

**Two color layers, always.** Define the palette (the raw values), then **role tokens** that point at it — `surface`, `surface-raised`, `text`, `text-muted`, `border`, `accent`, `on-accent`, plus the semantic states. Components use role tokens only, never palette values. Only the roles this project needs. This holds even for a light-only project: it costs almost nothing now, and it's what makes a dark or alternative mode a second set of values later instead of a pass over every component.

Take the roles and their palette mapping from the **Color roles** section of `.docs/design-system.md`. If it has none (older design systems don't), propose the mapping, get approval, and write it back there before building the styles file — the doc and the code name the same roles.

Wire only the primary color mode here. Extra modes recorded in the design system are `/theming`'s job, offered below.

**After creating the styles file, ask the user** if it looks right before proceeding. In the same message, make up to two optional offers, each in a line or two:

- **`/theming`** — only if `.docs/design-system.md` records more than one color mode, or the user asked for one. Wires the modes now; it can also run later, since the role tokens keep that door open.
- **`/showcase`** — one dev-only page or screen that renders the tokens now and the components as Phase 2 builds them. It's for judging them by eye rather than by reading a config file; skipping it saves time when that isn't needed. If a showcase already exists, don't offer — just keep it current.

For each offer:

- **Yes** → run it, then continue with `/setup`. If both, run `/theming` first so the showcase renders every mode — and treat the showcase as `/theming`'s verification: skip its own verify step, closing question, and `/showcase` mention, and log it as one line.
- **No** → continue without it. Don't offer it again during this run. If `/theming` was declined while `.docs/design-system.md` records more than one mode, say so in the Phase 1 summary — "design-system.md records N modes; only <primary> is wired — run `/theming` when ready" — so the gap is visible, not silent.

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

**Craft floor.** Before presenting a batch, check the built result rather than the intention. Look at it rendered — if the project has a showcase, add the batch to it (following `/showcase` Step 3) and view it through `.docs/preview.md`. If there's no way to see it, don't set one up unasked: run the checks against the code, say plainly the batch is "written, not run", and suggest `/ux-review` to establish a preview path.

- **States** — every interactive component has hover, focus, disabled, and (where it applies) loading, error, and empty. The default state is the easy fifth of the work.
- **Real content** — long labels, long names, a missing image, a zero count. Fix what overflows or collapses.
- **Contrast** — body text ≥ 4.5:1, large text ≥ 3:1, including secondary text on colored surfaces, and in every color mode wired in code. Tint it from the surface rather than dropping in a gray.
- **Focus** — a visible, on-brand focus ring, not the browser default and never removed.
- **The surfaces nobody draws** — on web: text selection color, caret, scrollbars, link underline offset, tabular numerals in data. Themed from the palette, they're the cheapest sign a UI was built rather than assembled. Native platforms have their equivalents (tint color, pressed states, keyboard toolbar).
- **New values go through the tokens** — if a check needs a color or value the design system doesn't define (a tinted secondary text, a selection color), add it to the centralized styles file as a token and tell the user it's an addition to the design system. Never inline it.
- **Copy** — buttons name their action ("Save changes", not "Submit"); errors name the problem and the way out.

Keep this to one inspection round per batch, fix what it shows, and move on — don't loop on polish.

---

**RULES:**

- Read the actual project structure before creating anything — don't assume folder conventions
- If the design system or tech stack doc is missing, stop and tell the user which command to run first
- Don't over-build. A Button with 3 variants is enough — don't add 15 props for hypothetical use cases. The craft floor is about finishing the variants you have, not adding more
- If the project already has components or a styles file, integrate with what exists rather than replacing it
- Ask before overwriting any existing files

**After completing, ask the user** to verify the components — in the showcase if there is one, otherwise by listing what was built and what was "written, not run". In the same message, offer `/tweaks` once — a dev-only panel for tuning colors, fonts, and shape live on real screens, with presets to compare directions. It's optional; skip it when the direction already feels right. On yes, run `/tweaks`, then continue. If everything looks good, suggest `/resume` to get a fresh assessment of where to go next.

**Logging:** On success, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /setup — [brief description of what was wired up]`.
