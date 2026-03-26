You are helping me define a design system for a new project. Focus on the project mission, brand, and UI.

**Custom instructions from user:** $ARGUMENTS

**Read:**
- `.docs/seed-document.md` — project vision, target users, key features
- `.docs/assets/imgs/prototypes/` — if wireframes exist, extract UX patterns and structure (ignore current visual style, they're structural references only)
- `.docs/assets/imgs/references/` — if reference screenshots from other apps exist, use them as visual inspiration (even here mainly focus on the UX)

**Your task:**
Create a `.docs/design-system.md` file — a tech-agnostic design reference that a UI/UX designer could read fluently. No code, no framework specifics. Pure design decisions.

**Structure:**

1. **Design Style**
   - Name the overall aesthetic direction (e.g., "Modern minimal", "Glassmorphism", "Editorial light")
   - Justify why it fits the target users and project vision

2. **Visual Foundation**
   - **Colors**: primary, secondary, accent, neutrals, semantic (success, error, warning). Hex codes.
   - **Typography**: font families, sizes scale, weights, line heights
   - **Spacing**: base unit and scale (e.g., 4px grid: 4, 8, 12, 16, 24, 32, 48)
   - **Shadows, borders, radii**: defined values for each level of elevation

3. **Interaction & Motion**
   - Transition durations and easing for common interactions
   - Keep it minimal — only define what you'll actually use

4. **Accessibility Checklist**
   - Contrast ratios, focus states, keyboard navigation, screen reader considerations
   - Based on WCAG 2.1 standards

**Guidelines:**
- This is the first iteration — it will likely evolve as the project takes shape. Focus on getting a solid starting point.
- Base the design on target users and brand direction from the seed, not on the prototype visuals
- Be opinionated but justify choices based on the project needs
- Be specific: hex codes, px values, font names — not vague descriptions
- Keep it concise and scannable. This is a working reference, not a design essay.
- No code, no framework references, no implementation details. That's `/setup`'s job.

**Output:**
A complete `.docs/design-system.md` file.

**After completing, ask the user** if they're happy with the result. Suggest `/scaffold` as the next step to validate or create the project structure, followed by `/setup` to translate these tokens into code.
