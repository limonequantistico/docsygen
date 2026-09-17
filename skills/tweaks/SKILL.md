---
name: tweaks
description: Add or update a dev-only tweaks panel inside the running app — a small set of live design controls (color, fonts, type scale, shape, density), switchable presets, save, copy, and reset — then write the values the user settles on back into the styles file and design-system.md on approval. Works on any platform whose tokens can change at runtime. Use when the user explicitly asks to tweak or tune the design live, runs /tweaks, pastes a tweaks-panel payload, or accepts it when another skill (e.g. /setup) offers it.
---

You are adding — or updating — a **tweaks panel**: a dev-only panel inside the running app with a handful of design controls, so the user can tune the look on real screens instead of describing changes in chat. When they settle on something, the values come back into the code and the docs.

That return trip is the point. A panel whose results never reach the styles file is a toy, and one that writes to code but not to `.docs/design-system.md` leaves the two disagreeing.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

**Read:**

- `.docs/design-system.md` — the tokens, the chosen direction, and the alternatives considered
- `.docs/tech-stack.md` — platform, styling approach, how fonts are loaded
- `.docs/seed.md` — who the product is for, which bounds what a preset may propose
- `.docs/preview.md` — how to run the app, and what tooling can reach it
- The centralized styles file, and how components consume it

If there's no styles file or design system in code yet, stop and point at `/setup`.

---

## Step 1 — Check it's possible here

A panel can only move values the app reads at runtime. Establish that for this project before promising anything, and say plainly what you found:

- **How tokens are consumed.** Web: CSS custom properties can be overridden live; values baked in at build time (utility classes with literal values, compiled constants) can't. Native: tokens need to come from something observable — a SwiftUI environment object, a Compose theme, a React Native context, a Flutter `ThemeData` — not static constants.
- **Fonts.** Can a font be loaded at runtime on this platform in a dev build? On web, usually yes. On native, custom fonts often have to be bundled and registered at build time — then the font controls can only offer fonts already in the bundle.
- **Persistence and clipboard.** Whatever this platform offers for small local storage (web storage, `UserDefaults`, DataStore, `SharedPreferences`, a local file) and for copying text or sharing it.
- **Dev-only gating.** How a dev build is told apart from a release build here.

Then report: which controls will work, which won't, and why. **If a problem blocks part of the panel, tell the user before building** — and what would unblock it (usually moving tokens onto a runtime-readable layer, which is `/setup` or `/theming` territory). Don't quietly drop controls, and don't restructure the token layer as a side effect. If nothing meaningful is possible, say so and stop.

## Step 2 — Choose the controls

A few controls with real leverage, not one per token — a panel with sixty inputs is a config file with extra steps. Propose the set, grouped, derived from what `.docs/design-system.md` actually defines:

- **Color** — accent (with its on-accent contrast shown live), neutral temperature (cool, neutral, warm), mode switch if the project has more than one mode
- **Type** — heading font, body font, scale ratio, base size
- **Shape** — radius multiplier, density (spacing) multiplier, shadow strength

Controls that drive a whole scale — a multiplier, a ratio — keep the scale coherent; per-token editing is out of scope unless the user asks. Drop any control the design system gives nothing to act on, and any Step 1 ruled out.

**Font options** are a short curated list per slot: the design system's current fonts plus 4–6 candidates chosen for this product — not an open search. Check each candidate's license allows the use. In the panel, fonts may load at runtime where Step 1 said that works; installing one properly happens only in Step 5, on approval.

## Step 3 — Build the presets

A **preset** is a complete set of control values, selectable from the top of the panel.

- **Current** — always first: the committed tokens.
- **3–4 alternatives**, each genuinely distinct. Start from the directions `/design-system` considered and the user didn't pick, if the doc records them; then variations on the chosen direction ("same direction, warmer and denser"). Every one must stay plausible for the seed's users.
- **Contrast-check every preset in every mode before it goes in.** A preset that fails contrast is a trap the user will fall into by picking it.

Store the presets in a small file next to the panel, bundled only into dev builds.

## Step 4 — Build the panel

One self-contained component, mounted in one place, compiled or rendered only in dev builds — removing it should mean deleting its files and one mount line. Use the platform's native controls; don't add a tweaking library that isn't in `.docs/tech-stack.md` (if one would clearly save effort, mention it once).

Mount it on the app's real screens. If there aren't any yet — `/setup` just finished and only base components exist — mount it on the showcase if there is one; otherwise tell the user the panel pays off once the first screens exist, and offer to stop here.

Layout adapts to the device: a side panel on wide screens, a bottom sheet or equivalent on phones, collapsible so it never hides the screen being judged. It opens from a small dev-only affordance — a floating button, a debug gesture, whatever the platform does conventionally.

Top to bottom:

1. **Preset select** — Current, the generated presets, then the user's saved ones, marked as theirs.
2. **Controls**, grouped as in Step 2.
3. **Actions:**
   - **Save as preset** — names the current values and adds them to the select immediately, persisted in the platform's local storage. Local storage lives on that one device and can be wiped; say so next to the button.
   - **Copy for agent** — JSON of only the changed values and the preset name, headed by an instruction that names the skill — *"Run /tweaks to apply these values:"* — so pasting it in any session, even a fresh one, goes through Step 5 rather than straight into the styles file.
   - **Copy tokens** — the changed values in the styles file's own format, for editing by hand.
   - **Reset** — back to the committed tokens, discarding unsaved changes.

The panel shows a contrast warning whenever the current values make a text/surface role pair fail — not only accent — so a failing combination is visible before it's saved or copied.

Where copying to a clipboard doesn't reach the agent easily — a physical phone, a TV, a headset — also offer the platform's share action, and write the same JSON to the dev log, which the agent can read through the tooling recorded in `.docs/preview.md`.

## Step 5 — Bring values back

When the user pastes a **Copy for agent** payload, or asks you to read the values through tooling:

1. List every change as old → new, grouped as the panel groups them.
2. Check contrast for every text/surface pair affected, in every mode. Flag failures with a corrected value.
3. On approval, apply to the centralized styles file **and** `.docs/design-system.md`, carrying a line on why the direction moved if the user gave one. Install any newly chosen font properly.
4. If the payload is a saved preset the user wants to keep rather than apply, add it to the presets file instead — committed, it survives wiped storage and is shared with anyone else on the project.

Never write panel values to code or docs without approval.

## Step 6 — Verify and hand over

Run the app, open the panel, and exercise it once: switch presets, move each control, save, copy, reset. Confirm the screen actually responds. If the app can't be run, say the panel is "written, not run".

Tell the user how to open it, and offer to record that in `.docs/preview.md` under a **Tweaks** heading.

**On a later run**, update rather than duplicate: bring the controls and presets in line with the current tokens, refresh **Current**, and keep the local storage key and preset format backward-compatible, so presets the user saved on their devices still load — the agent can't see them to migrate them.

**RULES:**

- Dev-only. The panel, its presets file, and any runtime font loading must not ship in release builds.
- Feasibility first. Tell the user what won't work on this platform before building, not after.
- Few controls with leverage. Don't grow it into a token editor.
- The panel overrides tokens at runtime; it never edits source. Only Step 5, on approval, touches code and docs.
- No generated preset and no applied value that fails contrast. User-saved presets may fail — the panel warns, and Step 5 catches it before anything is written.

**After completing,** ask the user to try the presets on a real screen and report back what to keep.

**Logging:** On success, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /tweaks — [panel added or updated, platform, and any controls ruled out]`. When values are applied back, log that too: `- YYYY-MM-DD HH:mm applied /tweaks values — [what changed]`.
