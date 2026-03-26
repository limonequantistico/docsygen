I'm attaching wireframes of the project's main screens for analysis.

**Custom instructions from user:** $ARGUMENTS

**Read:**
- Seed document: `.docs/seed-document.md`
- Wireframes: `.docs/assets/imgs/prototypes/*.*`
- Reference screenshots (if any): `.docs/assets/imgs/references/*.*`

If no wireframes are found, check if the user attached images directly in the prompt.

**Important:** The wireframes may only cover some screens, not the full app. This is intentional — the user focuses on key screens and iterates. Don't flag missing screens as problems unless they break a core flow from the seed.

**Your task:**
Analyze the wireframes against the seed document and provide:

1. **Seed alignment** — Do the screens shown serve the core features in the seed? Is anything shown that's not in the seed (scope creep)?

2. **Information hierarchy** — Is the most important content/action on each screen immediately obvious? Or is it buried?

3. **Flow logic** — If multiple related screens are shown, is the navigation between them intuitive? Note: screens may be completely unrelated — the user might be prototyping individual views independently, and that's fine.

4. **UI patterns** — Are there standard patterns that would work better for what's shown? (e.g., a list that should be a card grid, a multi-step form that should be a wizard, tabs vs. sidebar navigation)

5. **Reference alignment** — If reference screenshots from other apps are provided in `.docs/assets/imgs/references/`, compare: what patterns from the references should be adopted? What should be done differently given this project's specific needs?

6. **Technical implications** — Flag anything that will affect tech stack decisions: real-time updates, drag-and-drop, complex state management, offline needs, file uploads, maps, etc. This feeds directly into `/stack`.

**RULES:**
- Compare against the seed, but don't expect completeness — the user may only prototype key screens
- Be specific: "the dashboard shows 6 widgets but the seed only lists 3 core features — consider removing X and Y" is useful. "Too many elements" is not.
- Only suggest changes that matter for UX. Don't nitpick visual style — that's `/design`'s job.
- Keep it concise. Per-screen feedback in 2-3 lines max.

**After the analysis, ask the user** if they're satisfied with the result, then suggest the appropriate next step:
- If wireframes need revision → iterate with the design tool using the specific feedback
- If wireframes are solid → `/stack` could be next (mention any technical implications discovered)
- If wireframes revealed gaps in the seed → `/seed-update` might be needed first
