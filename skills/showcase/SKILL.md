---
name: showcase
description: Create or update a dev-only showcase page or screen that renders the project's design tokens and base components with their variants and states, in one place. Use when the user explicitly asks for a showcase or component gallery, runs /showcase, or accepts one when another skill (e.g. /setup) offers it.
---

You are building — or updating — a **showcase**: one dev-only page or screen where the project's design tokens and base components are rendered together, so they can be looked at instead of imagined.

It's optional by design. A showcase costs tokens and time to build and keep current; it pays off when someone is going to look at it — approving tokens, checking components, giving `/ux-review` something to see before real screens exist. If the user doesn't need that, skipping it is a valid choice.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

**Read:**

- `.docs/design-system.md` — the tokens and decisions being shown
- `.docs/tech-stack.md` — how a dev-only page or screen is done in this stack
- `.docs/preview.md` — how to see the running app, and whether a showcase is already recorded there
- The centralized styles file and the existing base components

If there's no styles file or design system in code yet, stop and point at `/setup` — there's nothing to show.

---

## Step 1 — Find what already exists

Look before creating anything: a Storybook, a `/showcase` or `/dev` route, a debug screen, a demo page, a showcase entry in `.docs/preview.md`.

- **One exists** → this is an update. Add the tokens and components it's missing — each in its group, in the standard frame from Step 3 — remove ones that no longer exist, and fix anything rendering stale values. Keep its structure; don't rebuild it. If it's a flat, ungrouped list, offer to reorganize it per Step 3 rather than doing it unasked.
- **None exists** → go to Step 2.

## Step 2 — Decide where it lives

Propose one location in a line or two, matched to the stack — a dev-only route on web, a debug-only screen or preview target on native — and how it stays out of production: gated to development builds, not linked from the product's navigation. Then build it.

Ask first only if the stack gives no clear answer. If another skill offered the showcase and the user already said yes, don't ask again — state the location and go.

Don't install Storybook or any other tool to host it. If the project would clearly benefit from one, say so once and let the user decide.

## Step 3 — Build it

Organize it the way a designer organizes a design-system file in Figma — foundations first, then components grouped by purpose, every component laid out the same way. A flat list in file order shows what exists; a structured one shows whether it holds together. Every value comes from the centralized styles file — the showcase is a consumer of the tokens, never a second copy of them.

**Index first.** A short index at the top linking to each group. On native, a first screen listing the groups, one screen per group.

1. **Foundations**, from primitive to composite — only what the project defines:
   - **Color** — the palette as swatches, then the role tokens that point at it, each labelled with its name and value. Show text roles on the surfaces they're meant for, so contrast is visible.
   - **Typography** — the type scale as real text at each step, labelled with size, weight, and line height.
   - **Spacing, radii, elevation** — small labelled samples, in scale order.
   - **Icons, motion** — only if the design system defines them.
2. **Components**, grouped by purpose. If the project's component folders already group them, use those groups so the showcase mirrors the code. Otherwise use these, keeping only groups that have something in them:
   - **Actions** — button, icon button, link
   - **Inputs** — text field, select, checkbox, radio, switch
   - **Navigation** — tabs, nav bar, breadcrumbs, pagination
   - **Feedback** — alert, toast, badge, progress, skeleton
   - **Data display** — card, list item, table, avatar
   - **Overlays** — modal, sheet, popover, tooltip
   - **Layout** — shell, section, divider

   Within a group, simpler components come before the ones built from them. **Every component gets the same frame**, like a Figma component set:
   - **Variants** as a labelled grid, one property per axis (e.g. style × size) — not a loose row.
   - **States** in a row beneath: default, focus, disabled, and loading, error, or empty where they apply. Focus is shown statically where possible; hover and press stay live.
   - **One awkward case** in the same position every time — a long label, a missing image, a zero count — because the tidy case is the one that never breaks.

   If a component's variants won't sit on clean axes, don't force the grid — flag it. Variants that don't form a coherent matrix usually weren't designed as a set.

If the project has more than one color mode, render both sections in each — side by side, or behind the project's own mode switch.

**Keep it small.** Labels and rendered examples, not documentation. No usage prose, no props tables, no interactive controls — it's a place to look, not a playground.

## Step 4 — Make it findable

Tell the user how to open it. Then offer to record it in `.docs/preview.md` under a **Showcase** heading — the path or route, and anything needed to reach it — so `/setup`, `/ux-review`, and later build work find it without asking. Don't start a dev server or simulator to view it without asking.

**RULES:**

- Update, don't duplicate. One showcase per project.
- Never hardcode a value in the showcase. If something can't be shown without a new token, flag it as a gap in the design system rather than inventing one.
- Dev-only. It must not ship in production builds or appear in the product's navigation.
- Match the project's own conventions for routes, screens, and file layout.

**After completing,** ask the user to open it and say whether anything looks off.

**Logging:** On success, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /showcase — [created or updated, and what it shows]`.
