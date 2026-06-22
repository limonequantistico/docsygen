---
name: ux-review
description: Broader UI/UX quality check — hierarchy, flow, consistency, cognitive load. Use only when the user explicitly asks for a UX review or runs /ux-review.
---

You are running a UI/UX quality check on the project's current state.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

**Read:**

- Design system: `.docs/design-system.md`
- The actual codebase — focus on pages, layouts, navigation, and component usage

**Your task:**
Review the project's UI/UX implementation against established best practices and flag issues.

1. **Information hierarchy** — Is the most important content/action on each screen immediately clear? Is there visual noise competing for attention? (Hick's Law, visual weight)

2. **Navigation & flow** — Is it obvious how to move between screens? Are there dead ends, unnecessary steps, or confusing transitions? Can the user always tell where they are?

3. **Consistency** — Are similar actions handled the same way across screens? Are design tokens and components used consistently, or are there one-off styles that break patterns?

4. **Cognitive load** — Are screens doing too much? Are forms, lists, or dashboards overwhelming? (Miller's Law, progressive disclosure)

5. **Feedback & affordance** — Do interactive elements look interactive? Does the UI respond to user actions clearly? Are loading, empty, and error states handled?

6. **Accessibility basics** — Contrast ratios, touch target sizes, keyboard navigation, semantic HTML, alt text on images

7. **UI patterns** — Are there standard patterns that would work better for what's built? (e.g., a list that should be a card grid, a multi-step form that should be a wizard, tabs vs. sidebar)

**RULES:**

- Focus on what's built right now, not what's planned
- Be specific: "the settings page has 12 ungrouped fields — split into sections by category" is useful. "Too cluttered" is not.
- Prioritize issues by impact on usability, not aesthetics
- Keep it concise. Per-screen feedback in 2-3 lines max ideally.

**After the analysis, ask the user** if they want to act on any of the findings, and suggest concrete next steps.

**Logging:** On success, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /ux-review — [brief summary of findings]`.
