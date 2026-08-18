---
name: a11y
description: Run a WCAG-focused accessibility pass on the current UI, driving the real running app when it can be reached. Use only when the user explicitly asks for an accessibility/a11y review or runs /a11y.
---

You are running a focused **accessibility** pass (WCAG-oriented) on the **current** UI implementation. This complements `/ux-review`, which is broader; here the priority is **barriers** for disabled users and compliance-oriented issues.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

**Read:**

- `.docs/design-system.md` — contrast, focus, motion, typography targets if documented
- `.docs/seed.md` — any a11y requirements called out for the product
- UI code: pages, layouts, forms, dialogs, navigation, media

---

## Step 1 — Reach the running UI

Contrast ratios, tap-target sizes, focus order, and the accessibility tree are **measurable**. Reading source and estimating them is guesswork, and guesswork gets reported as fact. So establish which mode you're in before reviewing:

- **Measured** — you can reach the running UI. Always prefer this.
  - **Start with `.docs/preview.md`** — it records how to get this app running in front of you. If it's missing, follow the same proposal-and-record procedure `/ux-review` uses (Step 1 there): work out the realistic options, propose a ranked shortlist, let the user grant access, then write the working path into `.docs/preview.md` so the next pass is free.
  - **Web:** use a real audit rather than reimplementing one.
    - [`agent-browser`](https://github.com/vercel-labs/agent-browser) is the most direct fit: `agent-browser a11y --tags wcag2a,wcag2aa` runs axe-core against the page and `agent-browser snapshot` returns the accessibility tree with stable refs. It's a plain CLI, so it needs no MCP setup and works in any agent.
    - Otherwise Chrome DevTools tooling (the `chrome-devtools` MCP server, or a skill like `a11y-debugging`) — follow its guidance rather than reimplementing it. It gives you a Lighthouse accessibility audit, the accessibility tree via a page snapshot, browser-reported contrast and ARIA issues in the console, real tab-order traversal, and scripted tap-target measurement.
  - **Native (iOS, Android, desktop):** use the platform's own accessibility inspector against the running app, or screenshots plus the accessibility APIs. Don't invent equivalents that aren't there.
- **Inferred** — no runnable UI, no tooling, or the user declines. Review the source directly. This is a valid fallback, not a failure.

Ask **once**. If access is declined or two attempts fail, fall back to inferred and move on — don't retry or stall the review.

## Step 2 — Review

1. **Perceivable** — Color contrast (text, UI components, graphs), non-text content (`alt`, labels, captions), reflow/zoom, motion reduction where applicable.

2. **Operable** — Keyboard navigation order, focus visibility, focus trap in modals, skip links if needed, touch target size for relevant platforms.

3. **Understandable** — Form labels and errors, predictable navigation, language attribute if multi-locale.

4. **Robust** — Semantic HTML vs div soup, heading hierarchy, ARIA only where it fixes a real gap, duplicate interactive controls.

## Step 3 — Report

State the mode up front in one line: which surfaces you actually opened, or that the pass was code-only.

For each issue: **location** (file or screen), **WCAG criterion** (best-effort, e.g. 1.4.3), **user impact**, **fix**, and whether it was **measured** or **inferred**. Prioritize blockers (keyboard traps, missing names) over polish.

**RULES:**

- Never present an inferred finding as a measured one. "Contrast looks around 3.5:1" from reading a hex value is a hypothesis; a reported ratio from a real audit is a fact. Label them differently.
- If the project is not UI-heavy (API-only), say so and limit scope to any public docs sites or admin UIs, or stop.
- Be specific; avoid "improve accessibility" without a target.
- Do not claim legal compliance; phrase as "aligned with WCAG 2.1 AA targets" where appropriate.
- Browser tooling is an optional accelerator, never a prerequisite. If it isn't there, the code-only pass still runs.

**Logging:** On success, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /a11y — [brief summary, noting measured or inferred]`.
