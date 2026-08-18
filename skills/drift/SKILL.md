---
name: drift
description: Find where the docs and the codebase have diverged — direction, stack, design, components — and propose a fix for each, in whichever direction is right. Use only when the user explicitly asks to check doc drift or reconcile docs with code, or runs /drift.
---

You are auditing the project's documentation against the actual state of the codebase. The goal is to find **drift** — places where the docs and reality have diverged — and propose a fix for each.

Drift is not always the doc's fault. For direction, stack, and undocumented work the code is the truth and the doc gets corrected; for design tokens and duplicated components the doc is the truth and the *code* is what's wrong. Decide per item, not per run.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

**Read:**

- `.docs/seed.md` — the project's stated direction
- `.docs/tech-stack.md` — the declared tech choices (if exists)
- `.docs/design-system.md` — the declared design tokens (if exists)
- `.docs/changelog.md` — check the last entry date to calibrate how far back in git history to look. Also check `.docs/versions.json` for the last version date if it exists. If both are empty or missing, ask the user.
- Recent git history — use the time gap from the changelog to decide how many commits to check. If the gap is unclear, ask the user (e.g., "How many recent commits should I look at to check for drift?").
- Scan the actual codebase structure, key files, and dependencies

**Compare and report:**

1. **Direction drift** — Does the code still match what the seed document describes? Features built that aren't in the seed? Seed features described but not built?

   **Distinguish drift from intent.** A feature in the seed with no code behind it may be abandoned — or it may simply not be built yet, which is what a seed is *for*. Never silently delete it. Ask which it is, or flag it as **[PLANNED?]** and leave it alone until the user says. Erasing a plan because the code hasn't caught up is the one way this command can do real damage.

2. **Stack drift** — Dependencies or tools in the code that aren't in the tech stack doc? Anything replaced or added without updating the doc?

3. **Design drift** — Are design tokens from the design system actually used in the centralized styles file? Are there hardcoded values that should reference the centralized tokens instead?

4. **Component drift** — Duplicate components doing the same thing? One-off UI elements that should be centralized into reusable components? Base components not using the centralized styles?

5. **Undocumented changes** — Significant code changes in recent commits that aren't reflected in any doc.

6. **Changelog update** — Check commits against `.docs/changelog.md`. If there's meaningful work not in the changelog, propose adding it. Also mention if it looks like a good time to run `/version` to cut a release.

**Output:**

- List each drift item with: what the doc says vs. what the code does
- For each item, propose the specific update needed:
  - **Doc updates** when the code is right and the doc is outdated (most common)
  - **Code suggestions** only for style centralization issues (hardcoded values that should use tokens, duplicate components that should be consolidated)
- Ask the user which updates to apply

**RULES:**

- For stack and undocumented changes: the code is always right, docs adapt to it. For direction, the code is right about what *exists* — but not about what's intended, so confirm before removing anything from the seed.
- For design and component drift: suggest code fixes too, since scattered styles and duplicate components are bugs, not intentional divergence.
- Only flag meaningful drift, not nitpicks
- If everything is in sync, say so and move on — don't invent problems

**Logging:** Append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm /drift — [≤10 words]`.
