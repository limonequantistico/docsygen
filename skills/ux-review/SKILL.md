---
name: ux-review
description: Get the agent's eyes on the real running product, then run a UI/UX quality check — hierarchy, flow, consistency, cognitive load. Sets up and records a reusable way to actually see the app. Use only when the user explicitly asks for a UX review or runs /ux-review.
---

You are running a UI/UX quality check on the project's current state.

Reviewing a UI by reading source is guessing. A component tree doesn't tell you which element wins the eye, whether a screen feels crowded, or what the empty state actually looks like. **So the first job of this skill is not reviewing — it's getting eyes on the running product.** That setup is reusable: once a working path exists, every future review (and every future build task) can use it.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

---

## Step 1 — Get eyes on the product

**First, check `.docs/preview.md`.** If it records a working way to see this app running, follow it and go to Step 2. If following it fails, say what broke and continue below.

If there's no recorded path, work one out — don't fall back to reading source yet, and don't silently give up.

**Investigate what's actually possible here.** Read `.docs/tech-stack.md`, package manifests, run scripts, CI config, and any test harness to establish what kind of product this is and how it starts. Then assemble the realistic options. Draw from these, but don't be limited by them — if this project has a better path, propose that:

- **Web** — two strong options:
  - [`agent-browser`](https://github.com/vercel-labs/agent-browser) (Vercel Labs), a native CLI built for agents. `agent-browser snapshot` gives an accessibility tree with stable `@e1` refs, `screenshot [path] --full` writes straight to a path you choose, `--annotate` labels elements by number, and `a11y --tags wcag2a,wcag2aa` runs a real axe-core audit. Install: `brew install agent-browser` / `npm i -g agent-browser`, then `agent-browser install` for its Chrome. Because it's a **plain CLI**, it works the same in any agent — no MCP configuration required — and it can also run as an MCP server via `agent-browser mcp`.
  - The `chrome-devtools` MCP server pointed at the dev server — live DOM, screenshots, console, Lighthouse, real interaction.

  Failing those: a Playwright/Puppeteer screenshot script, an existing e2e harness, or Storybook if the project has one.
- **iOS / macOS** — build and boot a simulator, then `xcrun simctl io booted screenshot`. Existing snapshot tests are a cheaper source of the same pixels. Note that web-browser tooling does **not** cover a native app — `agent-browser -p ios` drives Mobile Safari in the simulator, which is only useful if the target is a web view.
- **Android** — emulator plus `adb exec-out screencap`.
- **Desktop (Electron / Tauri)** — Chrome DevTools against the renderer process.
- **CLI / TUI** — run it and capture terminal output; for a TUI, a pty capture.
- **Last resort** — ask the user to take screenshots of the key screens and drop them in `.docs/assets/imgs/`. Slower and manual, but still far better than reading source.

**Then propose, don't act.** Present a short ranked shortlist — two or three options, not a catalogue. For each, state:

- **What it gets you** — live interaction and measurement, or static screenshots?
- **What it needs from the user** — a permission grant, an MCP server, a dev server left running, a simulator install, an API key for a seeded account?
- **What it costs** — rough setup effort, and whether it's one-time or per-run.

Recommend one and say why. Then **let the user decide** — they may know a better path, already have tooling you can't see, or not want the agent touching a given resource. Never install a dependency, start a long-running service, or reach for a resource that needs new permissions without asking first.

**Record what works.** As soon as a path succeeds, write it to `.docs/preview.md`: the exact commands, the URL or target, any prerequisite (dev server, seeded account, env vars), what it can and can't show, and anything that tripped you up. Create the file if it doesn't exist, update it if the setup has changed. Keep it short enough to follow without thinking.

**Flag better paths when you see them.** If the recorded setup works but something stronger is available — the project has Storybook and you're taking manual screenshots, or the `chrome-devtools` MCP server would replace a brittle script — say so once, with the concrete gain. Don't nag; the user decides.

**If the user declines everything,** run a code-only review, say so plainly, and mark every finding as inferred. That's a valid outcome, not a failure — it's just weaker, and it should read as weaker.

## Step 2 — Look

With access working, actually look before analysing:

- Walk the **main flow** end to end, not just the landing screen.
- Capture the **empty, loading, and error states**. These are where UIs are usually weakest and where source tells you least.
- Check at least one **narrow viewport** or small-device size. Most hierarchy problems only appear when space gets tight.

**Read for context:** `.docs/design-system.md`, and the code behind whichever screens look wrong — you'll want the file to point at when reporting.

### Keep the screenshots

If the access path produced image files (most do — `agent-browser screenshot <path>`, `simctl io booted screenshot`, a Playwright script), **save them** rather than throwing them away: `.docs/assets/imgs/screens/<YYYY-MM-DD>/`, or `<version>` if the project cuts versions via `/version`. Use the same filename per screen across runs (`checkout.png`, `settings-empty.png`) so the same screen lines up over time.

This costs nothing — the images already exist — and buys two things: a visual history you can scroll back through, and a **regression baseline**. When a prior set exists, comparing the current screen against its previous version is the cheapest way to catch a change nobody intended.

Three rules keep it from turning into a liability:

- **Never review from the archive.** Old screenshots are stale by definition. They are for comparison against something you just captured, never a substitute for capturing it. A finding sourced from an archived image is **inferred**, not seen.
- **Never load the folder wholesale.** Images are expensive in context. Open one prior screenshot to answer one specific question — not the set, and not the history.
- **Keep it to the screens that matter.** Five to eight key screens and states, not every permutation. These are binaries in git forever; prefer jpeg where fidelity isn't the point.

## Step 3 — Review

1. **Information hierarchy** — Is the most important content/action on each screen immediately clear? Is there visual noise competing for attention? (Hick's Law, visual weight)

2. **Navigation & flow** — Is it obvious how to move between screens? Are there dead ends, unnecessary steps, or confusing transitions? Can the user always tell where they are?

3. **Consistency** — Are similar actions handled the same way across screens? Are design tokens and components used consistently, or are there one-off styles that break patterns?

4. **Cognitive load** — Are screens doing too much? Are forms, lists, or dashboards overwhelming? (Miller's Law, progressive disclosure)

5. **Feedback & affordance** — Do interactive elements look interactive? Does the UI respond to user actions clearly? Are loading, empty, and error states handled?

6. **Accessibility basics** — Contrast, touch targets, keyboard navigation, semantic structure, alt text. Keep this shallow — `/a11y` is the real pass, and it can reuse the same access path.

7. **UI patterns** — Are there standard patterns that would work better for what's built? (e.g., a list that should be a card grid, a multi-step form that should be a wizard, tabs vs. sidebar)

## Step 4 — Report

Open with one line on what you actually looked at: which screens and states you opened, or that this was code-only.

Mark each finding **seen** (you looked at it rendered) or **inferred** (read from source). An inferred judgement about hierarchy or cognitive load is a hypothesis — say so rather than dressing it up as observation.

**RULES:**

- Focus on what's built right now, not what's planned
- Be specific: "the settings page has 12 ungrouped fields — split into sections by category" is useful. "Too cluttered" is not.
- Prioritize issues by impact on usability, not aesthetics
- Keep it concise. Per-screen feedback in 2-3 lines max ideally.
- Getting access is a proposal, never a fait accompli. Ask before installing, launching, or reaching for anything that needs a permission the agent doesn't already have.
- Don't burn the whole session on setup. If two access attempts fail, report what you tried, ask for a steer, and offer the code-only pass in the meantime.

**After the analysis, ask the user** if they want to act on any of the findings, and suggest concrete next steps.

**Logging:** On success, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /ux-review — [brief summary of findings, noting screens seen or code-only]`.
