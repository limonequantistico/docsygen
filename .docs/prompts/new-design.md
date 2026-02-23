You are helping me define a design system for a new project.

**Context:**

- Read the attached `@.docs/seed-document.md` to understand the project vision, target users, and key features
- Review the prototype screenshots in the /docs/prototypes/ folder, if present, to extract visual patterns and UX
- Check `@.docs/tech-stack.md`, if present, to understand technical constraints

* If using Tailwind → reference Tailwind tokens and classes
* If using shadcn/ui → base components on shadcn defaults
* If using a specific component library → align with its design patterns
* Match the styling approach specified in the tech stack

**Your task:**
Create a `@.docs/design-system.md` file that serves as a living reference for building this app. The design system should be:

1. **Practical** - focused on components and patterns we'll actually use
2. **Specific** - concrete values (hex codes, px values, component variants)
3. **Aligned** - coherent with the project vision and prototypes
4. **Flexible** - easy to evolve as the project develops

**Structure to follow:**

1. Visual Foundation (colors, typography, spacing, shadows, borders)
   - Include suggested design tokens/CSS variables (e.g., `--color-primary`) for easy implementation
2. Core Components (identify 5-8 key components from the seed doc and prototypes)
3. Layout Patterns (common page structures we'll need)
4. Interaction & Motion (basic transition/animation guidelines)
5. Accessibility Checklist
6. References (links to other docs and prototypes)
7. Design Style (Glassmorphism, Neomorphism etc.)

**Guidelines:**

- Don't extract color palettes and typography from the prototypes if not necessary for your vision of the project, thedesign system should be based more on the user personas and the seed document's specs
- If the tech stack uses a component library (e.g., shadcn/ui, MUI), reference it and define only customizations
- Be opinionated but justify choices based on the project needs
- Include practical examples for each component
- Keep it concise - this should be scannable and actionable

**Output:**
A complete `@.docs/design-system.md` file.

Use Context7 for any needed deeper research.
