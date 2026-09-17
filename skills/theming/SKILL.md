---
name: theming
description: Add or repair color modes — dark mode, high contrast, alternative brand themes — by routing the UI through semantic role tokens and wiring each mode the way the tech stack expects, on new or existing projects. Use when the user explicitly asks for dark mode, theming, or alternative color modes, runs /theming, or accepts it when another skill (e.g. /setup) offers it.
---

You are adding — or fixing — **color modes**: light and dark, high contrast, or alternative brand themes. They're all the same mechanism: one set of role tokens that components use, and one set of values per mode behind them.

Two things make a mode cheap or expensive, and this skill cares about both:

- **Whether components use role tokens** (`surface`, `text-muted`, `border`) or raw palette values (`gray-100`, `#1A1A1A`). With role tokens, a new mode is a second set of values. With raw values, it's a pass over every component.
- **Whether the mode's values were designed.** Dark mode isn't the light theme inverted — surfaces step differently to show elevation, accents usually need less saturation, shadows stop reading and borders take over, and contrast has to be checked all over again.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

**Read:**

- `.docs/design-system.md` — role tokens and per-mode values, if recorded
- `.docs/tech-stack.md` — how theming is done in this stack
- `.docs/preview.md` — how to see the app, and whether a showcase exists
- The centralized styles file, and enough of the components to see how they consume color

---

## Step 1 — Assess

Establish three things before proposing anything, and report them in a few lines:

1. **The token layer.** Does the styles file define role tokens, and do components use them — or do components reach for palette values and hardcoded colors directly? Search the component code and give a count and the worst offenders, not every line.
2. **The modes.** Which modes the user wants, and which already exist, fully or partly.
3. **The values.** Whether `.docs/design-system.md` records a value per role per mode.

If there's no styles file or design system in code at all, stop and point at `/setup`.

## Step 2 — Settle the values

Every mode needs its values decided before anything is wired.

- **Recorded in `.docs/design-system.md`** → use them.
- **Missing** → propose them: a value for every role token in the new mode, with the contrast ratio of each text/surface pair against WCAG 2.1 AA (4.5:1 body, 3:1 large text and UI components). Offer the main choices rather than one answer — e.g. near-black vs. dark gray base surface, accent kept vs. desaturated — with a recommendation. On approval, write them back into `.docs/design-system.md` as a column per mode. **Never wire values the user hasn't approved** — an invented palette in code is a design decision nobody made.

## Step 3 — Plan the wiring

Propose how the modes work in this stack. Check the current syntax against the stack's own documentation rather than memory — theming APIs change between major versions (Tailwind's dark variant moved from config to CSS in v4, for one). The usual shapes:

- **CSS / Tailwind** — role tokens as CSS custom properties, redefined per mode under `prefers-color-scheme` and an attribute or class override on the root element; Tailwind utilities pointed at those properties, with its dark variant configured to match.
- **CSS-in-JS / component libraries** (Tamagui, MUI, Chakra, styled-components) — the library's own theme objects or providers, one per mode.
- **SwiftUI / UIKit** — color sets in the asset catalog with Any/Dark (and High Contrast, if wanted) appearances, referenced by name; a manual override through the preferred color scheme.
- **Android** — `values` and `values-night` resources, or a Compose `ColorScheme` per mode.
- **React Native / Flutter** — the platform color scheme hook or theme data, feeding the same role tokens.

Decide with the user, briefly:

- **Default** — follow the system setting. A manual toggle and a persisted choice only if they ask.
- **Web first paint** — how the correct mode is applied before the page renders, so there's no flash of the wrong theme.

## Step 4 — Apply

Get approval on the plan, then:

1. **Role tokens first.** Add or complete them in the styles file, with a value per mode.
2. **Migrate components** from palette values and hardcoded colors to role tokens, in small batches, confirming the approach after the first batch. On an existing project this is most of the work — list the batches up front so the user sees the size.
3. **Wire the modes** per the plan.
4. **The details that break in a second mode:** shadows (often replaced or supplemented by borders in dark), images and illustrations that assume a light background, logos, syntax highlighting, charts, and third-party embeds. Fix what's in scope; list the rest.

## Step 5 — Verify

Look at every mode rendered: through the showcase if one exists, otherwise through `.docs/preview.md`. If neither exists, don't set one up unasked — mark the result "written, not run", and mention `/showcase` once.

Check, in each mode:

- Text/surface contrast, including muted text and text on accent colors
- Focus rings, which often vanish against dark surfaces
- **Anything that doesn't change between modes** — a hardcoded color the migration missed shows up here first

Keep it to one round, fix what it shows, and move on.

**RULES:**

- Components use role tokens only. A palette value in a component is the bug this skill exists to remove.
- Values come from `.docs/design-system.md`. When the skill decides a new one, it goes back there on approval — the doc and the code never disagree.
- Don't add a mode the user didn't ask for, and don't add a toggle when following the system setting is enough.
- Ask before migrating an existing project's components; show the batches first.
- Don't introduce a theming library that isn't in `.docs/tech-stack.md`. If one would solve a real problem, mention it once and let the user decide.

**After completing,** ask the user to check each mode — in the showcase if there is one — and report anything that was left out of scope.

**Logging:** On success, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /theming — [modes added or fixed, and how many components were migrated]`.
